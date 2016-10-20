# ksproxy简介
为了避免用户程序连接kop接口时较复杂的认证过程，ksproxy将认证过程封装，对用户程序提供不需要认证的简单HTTP接口。认证需要的ks_access_key_id、ks_secret_access_key需要配置在ksproxy的配置文件中。

# 安装kscore
```
mkdir /data/koptest/
cd /data/koptest
git clone https://github.com/KscSDK/ksc-sdk-python.git
cd /data/koptest/ksc-sdk-python
python setup.py install
```
安装过程中，会将kscore和相关的依赖包安装到系统的python库路径中，如
```
/usr/local/lib/python2.7/site-packages
```
如果不想对系统造成修改，推荐使用VirtualEnv。以下有VirtualEnv的简要说明。

# 下载ksproxy代码
```
cd /data/koptest
git clone https://github.com/thinkphoebe/ksproxy.git
cd /data/ksproxy
```

# 修改配置文件
```
ksproxy.json，一般需修改region、ks_access_key_id、ks_secret_access_key等配置。
```

# 启动proxy程序
```
python ./ksproxy.py
```

# VirtualEnv
VirtualEnv可以创建独立的Python运行环境。在Ubuntu下可通过如下命令安装VirtualEnv软件:
```
sudo aptitude install python-pip
sudo pip install virtualenv
```

创建一个独立的运行环境:
```
cd /data
virtualenv --no-site-packages koptest
```

激活该运行环境:
```
cd /data/koptest
source ./bin/activate
```

激活后终端的命令提示符前会有个(koptest)的前缀:
```
(koptest) sunny@tiger:~$
```

之后pip等命令安装的包都是安装到创建的运行环境中，不会对系统产生影响。
