# ksproxy简介
为了避免用户程序连接ksc接口时较复杂的认证过程，ksproxy将认证过程封装，对用外提供不需要认证的简单HTTP接口，只需将认证使用的ks_access_key_id、ks_secret_access_key配置在ksproxy的配置文件中即可。
# 运行平台
本程序在Ubuntu 14.04 (Python 2.7.9)、CentOS 6.5 (Python 2.6.6)、Windows 7 x86_64 (Python 2.7.12)上测试通过。以下为Linux平台的安装方法，Windows平台的安装步骤请参考 https://github.com/ksvc/ksproxy/blob/master/README_Windows.md
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
如果不想对系统造成修改，或没有root权限，推荐使用VirtualEnv。本文最后有VirtualEnv用法的简要介绍。
# 下载ksproxy代码
```
cd /data/koptest
git clone https://github.com/ksvc/ksproxy.git
cd /data/ksproxy
```
# 修改配置文件
```
ksproxy.json，一般需修改region、ks_access_key_id、ks_secret_access_key等配置。
```
# 启动proxy程序
注意：如果有防火墙，请关闭或将程序绑定端口添加到防火墙例外。
```
python ./ksproxy.py
```
# VirtualEnv
VirtualEnv可以创建独立的Python运行环境。在Ubuntu 14.04可通过如下命令安装VirtualEnv软件:
```
sudo aptitude install python-pip
sudo pip install virtualenv
```
CentOS 6.5可通过如下命令安装：
```
sudo yum install python-setuptools python-devel
sudo easy_install virtualenv
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
