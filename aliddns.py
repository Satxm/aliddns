from aliyunsdkcore.client import AcsClient
from urllib.request import urlopen
import logging
import json
import sys

logs1="---------------------------------------------------------"
logs2="========================================================="

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("logs.log",encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s [%(levelname)s] %(message)s')

def getconfig(key=None, default=None, path="config.json"):
    if not hasattr(getconfig, "config"):
        try:
            with open(path) as config:
                getconfig.config = json.load(config)
        except IOError:
            logging.error('配置文件%s不存在！' % path)
            with open(path, 'w') as config:
                configure = {
                    "enableipv4": True,
                    "enableipv6": True,
                    "accessKeyId":"youraccessKeyId",
                    "accessSecret":"youraccessSecret",
                    "domain":"your.domain",
                    "names": [
                        "host"
                    ]
                    
                }
                json.dump(configure, config, indent=2, sort_keys=True)
            sys.stdout.write("已生成新的配置文件%s！\n" % path)
            input('已生成新的配置文件，快去修改它，填入信息！')
        except:
            logging.error('无法从%s加载配置文件！' % path)
            sys.exit('无法从%s加载配置文件！' % path)
    if key:
        return getconfig.config.get(key, default)
    else:
        return getconfig.config

def update(RecordId, RR, Type, Value):
    from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)

def add(DomainName, RR, Type, Value):
    from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(DomainName)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)

def delete(Domain, Name):
    from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
    request = DeleteSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(Domain)
    request.set_RR(Name)
    response = client.do_action_with_exception(request)

def getinfo(Domain, Name):
    from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(Domain)
    request.set_SubDomain(Name + '.' + Domain)
    response = client.do_action_with_exception(request)
    info = json.loads(response)
    return info

def index(index):
    logger.info('类型：%s' % (info['DomainRecords']['Record'][index]['Type']))
    logger.info('值：%s' % (info['DomainRecords']['Record'][index]['Value']))
    logger.info(logs1)

def getipv4():
    ipv4 = urlopen('https://api-ipv4.ip.sb/ip').read()
    ipv4 = str(ipv4, encoding='utf-8')
    ipv4 = ipv4.strip()
    logs = "获取到本机IPv4地址：%s" % ipv4
    logger.info(logs)
    return ipv4

def getipv6():
    ipv6 = urlopen('https://api-ipv6.ip.sb/ip').read()
    ipv6 = str(ipv6, encoding='utf-8')
    ipv6 = ipv6.strip()
    logs = "获取到本机IPv6地址：%s" % ipv6
    logger.info(logs)
    return ipv6

def newaddipv4():
    if enableipv4 == True:
        ipv4 = getipv4()
        add(domain, name, "A", ipv4)
        logs="域名（%s）新建解析成功" % (name + '.' + domain)
        logger.info(logs)
        logger.info(logs1)

def newaddipv6():
    if enableipv6 == True:
        ipv6 = getipv6()
        add(domain, name, "AAAA", ipv6)
        logs="域名（%s）新建解析成功" % (name + '.' + domain)
        logger.info(logs)
        logger.info(logs1)

def changeipv4():
    ipv4 = getipv4()
    if enableipv4 == True:
        if info['DomainRecords']['Record'][i]['Value'].strip() != ipv4.strip():
            update(info['DomainRecords']['Record'][i]['RecordId'], name, "A", ipv4)
            logs="域名（%s）解析修改成功" % (name + '.' + domain)
        else:
            logs="域名（%s）IPv4地址没变" % (name + '.' + domain)
        logger.info(logs)
        logger.info(logs1)

def changeipv6():
    ipv6 = getipv6()
    if enableipv6 == True:
        if info['DomainRecords']['Record'][i]['Value'].strip() != ipv6.strip():
            update(info['DomainRecords']['Record'][i]['RecordId'], name, "AAAA", ipv6)
            logs="域名（%s）解析修改成功" % (name + '.' + domain)
        else:
            logs="域名（%s）IPv6地址没变" % (name + '.' + domain)
        logger.info(logs)
        logger.info(logs1)

if True == True:
    enableipv4 = getconfig('enableipv4')
    enableipv6 = getconfig('enableipv6')
    accessKeyId = getconfig('accessKeyId')
    accessSecret = getconfig('accessSecret')
    domain = getconfig('domain')
    names = getconfig('names')
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    for name in names:
        info = getinfo(domain, name)
        logger.info(logs2)
        logger.info('域名（%s）' % (name + '.' + domain))
        logger.info('总记录个数：%s' % (info['TotalCount']))
        logger.info(logs1)
        if info['TotalCount'] == 0:
                newaddipv4()
                newaddipv6()
        elif info['TotalCount'] == 1:
            if  info['DomainRecords']['Record'][0]['Type'] == "A":
                i = 0
                changeipv4()
                newaddipv6()
            elif  info['DomainRecords']['Record'][0]['Type'] == "AAAA":
                i = 0
                changeipv6()
                newaddipv4()
        elif info['TotalCount'] == 2:
            for i, element in enumerate(info['DomainRecords']['Record']):
                index(i)
                if  info['DomainRecords']['Record'][i]['Type'] == "A":
                        changeipv4()
                if info['DomainRecords']['Record'][i]['Type'] == "AAAA":
                        changeipv6()
