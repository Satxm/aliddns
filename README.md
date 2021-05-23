# Python实现阿里云DDNS域名——AliDDNS 使用教程
## AliDDNS介绍

### 下载
项目地址:
	[Github](https://github.com/Satxm/aliddns)
	
	[Gitee](https://gitee.com/satxm/aliddns)

发布地址：
	[Github-Releases](https://github.com/Satxm/aliddns/releases)
	
	[Gitee-Releases](https://gitee.com/satxm/aliddns/releases)

### Windows
直接下载```aliddns-win.exe```运行

### Linux
请下载```aliddns-linux.zip```解压运行

### 如果使用```aliddns.py```
需要```python3``` 和以下pip包
```
pip3 install aliyun-python-sdk-core-v3
pip3 install aliyun-python-sdk-domain
pip3 install aliyun-python-sdk-alidns
pip3 install requests
pip3 install pyinstaller
pip3 install colorlog
pip3 install apscheduler
```

## 配置文件说明
```
config.json 配置文件说明：

	accessKeyId：你获取的阿里云accessKeyId
	accessSecret：你获取的阿里云accessSecret

	enableipv4/6：是否启用IPv4/6的DDNS动态域名更新
		true 为启用，false 为禁用

	domain：你的域名
	names: 你的主机记录值（支持多个）

	enabletimedrun: 是否启用后台自动间隔运行
		true 为启用，false 为禁用
	timedruntime: 为间隔运行时间（单位为秒）
```
