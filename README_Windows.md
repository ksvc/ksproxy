# ksproxy简介
为了避免用户程序连接ksc接口时较复杂的认证过程，ksproxy将认证过程封装，对用外提供不需要认证的简单HTTP接口，只需将认证使用的ks_access_key_id、ks_secret_access_key配置在ksproxy的配置文件中即可。
# 运行平台
本程序在Ubuntu 14.04 (Python 2.7.9)、CentOS 6.5 (Python 2.6.6)、Windows 7 x86_64 (Python 2.7.12)上测试通过。以下为Windows平台的安装方法，Linux平台的安装步骤请参考 https://github.com/ksvc/ksproxy/blob/master/README.md
# 配置Python环境
Python的安装包，如：
```
https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi
```
安装后将Python路径添加到系统的环境变量。如将Python安装到 C:\Python27 目录，打开“控制面板-> 系统->高级->环境变量”，在PATH环境变量中添加:
```
C:\Python27;C:\Python27\Scripts
```
注意一定要添加第二个"Scripts"目录，否则后面命令行提示符中可能找不到pip或virtualenv命令。
# 安装Git工具
这里使用msysGit。为了在Windows命令行中使用，安装时选择"Use Git from the Windows Command Prompt":
```
https://github.com/git-for-windows/git/releases/download/v2.10.1.windows.1/Git-2.10.1-64-bit.exe
```
# 安装kscore
以下均在Windows命令行提示符下完成。
```
cd D:\koptest
git clone https://github.com/KscSDK/ksc-sdk-python.git
cd D:\koptest\ksc-sdk-python
python setup.py install
```
安装过程中，会将kscore和相关的依赖包安装到系统的python库路径中，如
```
C:\Python27\Lib\site-packages
```
如果不想对Python安装目录造成修改，推荐使用VirtualEnv。本文最后有VirtualEnv用法的简要介绍。
# 下载ksproxy代码
```
cd D:\koptest
git clone https://github.com/ksvc/ksproxy.git
cd D:\koptest\ksproxy
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
VirtualEnv可以创建独立的Python运行环境。在Windows配置好Python环境后，可在命令行提示符下通过如下命令安装:
```
pip install virtualenv
```
创建一个独立的运行环境:
```
cd D:\
virtualenv --no-site-packages koptest
```
激活该运行环境:
```
cd D:\koptest\Scripts
activate
```
激活后终端的命令提示符前会有个(koptest)的前缀:
```
(koptest) D:\koptest\Scripts>
```
之后pip等命令安装的包都是安装到创建的运行环境中，不会对系统产生影响。
