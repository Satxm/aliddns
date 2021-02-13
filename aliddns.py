from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from urllib.request import urlopen
import configparser
import requests
import logging
import json
import os
import re

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
enableipv4 = config.getboolean('enable', 'enableipv4')
enableipv6 = config.getboolean('enable', 'enableipv6')
accessKeyId = eval(config.get('access','accessKeyId'))
accessSecret = eval(config.get('access','accessSecret'))
domain = eval(config.get('domain','domain'))
names = eval(config.get('domain','names'))

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("logs.log",encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(message)s')

client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

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

#def getIPv6Address():
#    output = os.popen("ipconfig /all").read()
#    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
#    return result[0][0]

if enableipv4 == True:
    logs="=================================================================="
    logger.info(logs)
    ip = urlopen('https://api-ipv4.ip.sb/ip').read()  # 使用IP.SB的接口获取ipv4地址
    ipv4 = str(ip, encoding='utf-8')
    ipv4 = ipv4.strip()
    logs = "获取到本机IPv4地址：%s" % ipv4
    logger.info(logs)
    for name in names:
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_SubDomain(name + '.' + domain)
        response = client.do_action_with_exception(request)
        domain_list = json.loads(response)

        if domain_list['TotalCount'] == 0:
            add(domain, name, "A", ipv4)
            logs="域名（%s）新建解析成功" % (name + '.' + domain) 
        elif domain_list['TotalCount'] == 1:
            if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv4.strip():
                update(domain_list['DomainRecords']['Record'][0]['RecordId'], name, "A", ipv4)
                logs="域名（%s）解析修改成功" % (name + '.' + domain)
            else:
                logs="域名（%s）IPv4地址没变" % (name + '.' + domain)
        elif domain_list['TotalCount'] > 1:
            from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
            request = DeleteSubDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(domain)
            request.set_RR(name)
            response = client.do_action_with_exception(request)
            add(domain, name, "A", ipv4)
            logs="域名（%s）解析修改成功" % (name + '.' + domain)
        logger.info(logs)
    logs="=================================================================="
    logger.info(logs)
    

if enableipv6 == True:
    logs="=================================================================="
    logger.info(logs)
    ip = urlopen('https://api-ipv6.ip.sb/ip').read()  # 使用IP.SB的接口获取ipv6地址
    ipv6 = str(ip, encoding='utf-8')
    ipv6 = ipv6.strip()
    logs = "获取到本机IPv6地址：%s" % ipv6
    logger.info(logs)
    for name in names:
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_SubDomain(name + '.' + domain)
        response = client.do_action_with_exception(request)
        domain_list = json.loads(response)

        if domain_list['TotalCount'] == 0:
            add(domain, name, "AAAA", ipv6)
            logs="域名（%s）新建解析成功" % (name + '.' + domain) 
        elif domain_list['TotalCount'] == 1:
            if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv6.strip():
                update(domain_list['DomainRecords']['Record'][0]['RecordId'], name, "AAAA", ipv6)
                logs="域名（%s）解析修改成功" % (name + '.' + domain)
            else:
                logs="域名（%s）IPv6地址没变" % (name + '.' + domain)
        elif domain_list['TotalCount'] > 1:
            from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
            request = DeleteSubDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(domain)
            request.set_RR(name)
            response = client.do_action_with_exception(request)
            add(domain, name, "AAAA", ipv6)
            logs="域名（%s）解析修改成功" % (name + '.' + domain)
        logger.info(logs)
    logs="=================================================================="
    logger.info(logs)