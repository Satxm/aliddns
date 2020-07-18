from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import requests
from urllib.request import urlopen
import json
import os
import re
import logging

accessKeyId = "accessKeyId"  # 将accessKeyId改成自己的accessKeyId
accessSecret = "accessSecret"  # 将accessSecret改成自己的accessSecret
domain = "domain.main"  # 你的主域名
names = ['name1','name2','name3']  # 要进行ipv6 ddns解析的子域名

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("logs.log")
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

def getIPv6Address():
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

if __name__ == "__main__":
    ipv6 = getIPv6Address()
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
