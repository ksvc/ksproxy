# ksproxy���
Ϊ�˱����û���������kop�ӿ�ʱ�ϸ��ӵ���֤���̣�ksproxy����֤���̷�װ�����û������ṩ����Ҫ��֤�ļ�HTTP�ӿڡ���֤��Ҫ��ks_access_key_id��ks_secret_access_key��Ҫ������ksproxy�������ļ��С�

# ��װkscore
```
mkdir /data/koptest/
cd /data/koptest
git clone https://github.com/KscSDK/ksc-sdk-python.git
cd /data/koptest/ksc-sdk-python
python setup.py install
```
��װ�����У��Ὣkscore����ص���������װ��ϵͳ��python��·���У���
```
/usr/local/lib/python2.7/site-packages
```
��������ϵͳ����޸ģ��Ƽ�ʹ��VirtualEnv��������VirtualEnv�ļ�Ҫ˵����

# ����ksproxy����
```
cd /data/koptest
git clone https://github.com/thinkphoebe/ksproxy.git
cd /data/ksproxy
```

# �޸������ļ�
```
ksproxy.json��һ�����޸�region��ks_access_key_id��ks_secret_access_key�����á�
```

# ����proxy����
```
python ./ksproxy.py
```

# VirtualEnv
VirtualEnv���Դ���������Python���л�������Ubuntu�¿�ͨ���������װVirtualEnv���:
```
sudo aptitude install python-pip
sudo pip install virtualenv
```

����һ�����������л���:
```
cd /data
virtualenv --no-site-packages koptest
```

��������л���:
```
cd /data/koptest
source ./bin/activate
```

������ն˵�������ʾ��ǰ���и�(koptest)��ǰ׺:
```
(koptest) sunny@tiger:~$
```

֮��pip�����װ�İ����ǰ�װ�����������л����У������ϵͳ����Ӱ�졣
