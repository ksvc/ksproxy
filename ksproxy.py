# -*- encoding:utf-8 -*-
'''
请求的URL格式: http://serve_ip:serve_port/service_name/method?params
如：http://127.0.0.1:9000/offline/GetPresetDetail?preset=test
service_name, method, GET或POST, 及GET/POST的参数和响应格式请参考相应服务的API手册
'''
import threading
import BaseHTTPServer
import SocketServer
import urlparse
import json
import traceback
import os
import sys
import logging
import logging.handlers
import kscore
from kscore.session import get_session

format_str = '[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)-80s'
g_logger = None
g_session = None
g_clients = dict()
g_mutex = threading.Lock()


class _request_handler(BaseHTTPServer.BaseHTTPRequestHandler):
    # 重定向日志信息到logger
    def log_message(self, args, *vargs):
        g_logger.info("[%s] %s" % (self.client_address[0], args % vargs))

    def _handle_request(self, is_post):
        global g_clients

        # 解析请求URL。paths[0]为service_name, paths[1]为method
        parsed_url = urlparse.urlparse(self.path)
        paths = os.path.normpath(parsed_url.path.strip('/')).split('/')
        if len(paths) < 2:
            g_logger.error('[%s] invalid request url:%s', self.client_address[0], self.path)
            self.send_response(400, 'Bad Request URL')
            self.end_headers()
            return

        # 每个service对应一个client。请求的service对应的client不存在时尝试创建
        if paths[0] not in g_clients:
            g_mutex.acquire()
            try:
                client = g_session.create_client(paths[0], g_config['region'], use_ssl=False,
                                                 ks_access_key_id=g_config['ks_access_key_id'],
                                                 ks_secret_access_key=g_config['ks_secret_access_key'])
            except kscore.session.UnknownServiceError:
                g_logger.error('[%s] got exception [UnknownServiceError] on create client for [%s]',
                               self.client_address[0], self.path)
                self.send_response(400, 'Unknown Service')
                self.end_headers()
                g_mutex.release()
                return
            except:
                g_logger.error('[%s] got exception on create client for [%s], %s', self.client_address[0],
                               self.path, traceback.format_exc())
                self.send_response(500, 'Create client FAILED')
                self.end_headers()
                g_mutex.release()
                return
            g_clients[paths[0]] = client
            g_mutex.release()

        # URL中的method形如GetPresetDetail，对应Python SDK的函数名形如get_preset_detail，这里做转换
        l = list()
        for index, a in enumerate(paths[1]):
            if a.isupper():
                if index != 0:
                    l.append('_')
                l.append(a.lower())
            else:
                l.append(a)
        method_name = ''.join(l)

        # 根据URL请求的service_name、method找到Python的对应client对象及函数
        try:
            method = getattr(g_clients[paths[0]], method_name)
        except AttributeError:
            g_logger.error('[%s] got exception on find method for [%s], probably the method [%s] requested does not exist',
                           self.client_address[0], self.path, method_name)
            self.send_response(400, 'Method does not exist')
            self.end_headers()
            return

        params = dict()
        if is_post:
            # 读取POST请求，解析成dict
            try:
                post_msg = self.rfile.read(int(self.headers['content-length']))
            except (IOError, KeyError):
                g_logger.error('[%s] got exception on read post for [%s], %s', self.client_address[0],
                               self.path, traceback.format_exc())
                self.send_response(500, 'Unknow error')
                self.end_headers()
                return
            g_logger.debug('[%s] POST content:%s', self.client_address[0], post_msg)
            params = json.loads(post_msg)
        else:
            # 将URL中形如"param1=value1&param2=value2"的查询参数转换成调用Python SDK的dict参数
            if len(parsed_url.query) > 0:
                pairs = parsed_url.query.split('&')
                for pair in pairs:
                    kv = pair.split('=')
                    params[kv[0]] = kv[1]

        try:
            # 调用URL请求的Python对应函数，将函数返回信息转换成json，写入HTTP响应
            res = method(**params)
            self._write_response(200, json.dumps(res))
            return
        except kscore.validate.ParamValidationError:
            g_logger.error('[%s] got exception [ParamValidationError] on call method for [%s]',
                           self.client_address[0], self.path)
            self.send_response(400, 'Parameter validation failed')
        except kscore.client.ClientError:
            g_logger.error('[%s] got exception [ClientError] on call method for [%s], probably you configured an invalid [ks_access_key_id]',
                           self.client_address[0], self.path)
            self.send_response(500, 'Invalid security token configured')
        except ValueError:
            g_logger.error('[%s] got exception [ValueError] on call method for [%s], probably you configured an invalid [ks_secret_access_key]',
                           self.client_address[0], self.path)
            self.send_response(500, 'Invalid security token configured')
        except:
            g_logger.error('[%s] got exception on call method for [%s]',
                           self.client_address[0], self.path, traceback.format_exc())
            self.send_response(500, 'Unknow error')
        self.end_headers()

    def _write_response(self, code=200, msg=''):
        try:
            self.send_response(code)
            self.send_header('Content-Length', len(msg))
            self.end_headers()
            self.wfile.write(msg)
            g_logger.debug('[%s] write response OK: %d, %s', self.client_address[0], code, msg)
            return True
        except IOError:
            g_logger.warning('[%s] write response FAILED: %d, %s, traceback: %s',
                             self.client_address[0], code, msg, traceback.format_exc())
            return False

    def do_GET(self):
        try:
            self._handle_request(False)
        except:
            g_logger.error('[%s] got exception on GET [%s], %s',
                           self.client_address[0], self.path, traceback.format_exc())

    def do_POST(self):
        try:
            self._handle_request(True)
        except:
            g_logger.error('[%s] got exception on POST [%s], %s',
                           self.client_address[0], self.path, traceback.format_exc())


class _threaded_httpserver(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    daemon_threads = True  # 主线程退出时，结束所有子线程
    allow_reuse_address = True


def _getpwd():
    pwd = sys.path[0]
    if os.path.isfile(pwd):
        pwd = os.path.dirname(os.path.realpath(pwd))
    return pwd


def _load_config():
    try:
        # 读取和ksproxy.py同一目录下的ksproxy.json文件
        jstr = open(os.path.join(_getpwd(), 'ksproxy.json'), 'rb').read()

        # 去掉//和/**/的注释，不支持注释和代码在一行内混合的情况。
        lines = jstr.split('\n')
        for line in lines[:]:
            line_strip = line.strip()
            if line_strip.startswith('//'):
                lines.remove(line)
            if line_strip.startswith('/*') and line_strip.endswith('*/'):
                lines.remove(line)

        jstr = '\n'.join(lines)
        cfg = json.loads(jstr)
    except:
        print 'load config FAILED!'
        return False

    if not _check_convert_config(cfg):
        return False

    global g_config
    g_config = cfg
    return True


def _check_convert_config(cfg):
    # 检验配置文件的正确性
    if not ('bind_ip' in cfg and 'bind_port' in cfg and 'log_path' in cfg and
            'log_level' in cfg and 'region' in cfg and
            'ks_access_key_id' in cfg and 'ks_secret_access_key' in cfg):
        print 'invalid config'
        return False

    # 如果log路径是相对路径，转换成绝对路径
    if not os.path.isabs(cfg['log_path']):
        cfg['log_path'] = os.path.join(_getpwd(), cfg['log_path'])
    return True


def _init_log():
    global g_logger
    g_logger = logging.getLogger('ksproxy')
    g_logger.setLevel(g_config['log_level'])

    try:
        if not os.path.exists(g_config['log_path']):
            os.makedirs(g_config['log_path'])
        handler_file = logging.handlers.TimedRotatingFileHandler(os.path.join(g_config['log_path'], 'ksproxy.log'),
                                                                 when='D', interval=1, backupCount=100)
    except (IOError, OSError):
        print 'can not write log file to [%s]' % g_config['log_path']
        return False

    formatter = logging.Formatter(format_str)
    handler_file.setFormatter(formatter)
    g_logger.addHandler(handler_file)
    return True


if __name__ == '__main__':
    if not _load_config():
        sys.exit(-1)

    if not _init_log():
        sys.exit(-1)

    g_session = get_session()
    server = _threaded_httpserver((g_config['bind_ip'], g_config['bind_port']), _request_handler)
    g_logger.info('run server on %s:%s', g_config['bind_ip'], g_config['bind_port'])

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        g_logger.info('receive keyboard interrupt, quit program')
