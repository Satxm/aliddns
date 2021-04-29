#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError
from aliyunsdkcore.client import AcsClient
from urllib.request import urlopen
import colorlog
import logging
import json
import time
import sys

class Log:
    logsa="---------------------------------------------------------"
    logsb="========================================================="
    log_colors_config = {
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
    }
    logger = logging.getLogger("logger_name")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename="logs.log",encoding="utf8")

    logger.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] : %(message)s",
        datefmt="%Y-%m-%d  %H:%M:%S"
        )
    console_formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s %(asctime)s [%(levelname)s] : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=log_colors_config
        )
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    console_handler.close()
    file_handler.close()

class GetConfig:
    def getconfig(key=None, default=None, path="config.json"):
        if not hasattr(GetConfig.getconfig, "config"):
            try:
                with open(path) as config:
                    GetConfig.getconfig.config = json.load(config)
            except IOError:
                Log.logger.error("配置文件config.json不存在！")
                with open(path, "w") as config:
                    configure = {
                            "accessKeyId": "youraccessKeyId",
                            "accessSecret": "youraccessSecret",
                            "enableipv4": True,
                            "enableipv6": True,
                            "domain": "your.domain",
                            "names": [
                                "host1",
                                "host2"
                                ],
                            "enabletimedrun": True,
                            "timedruntime": "600"
                        }
                    json.dump(configure, config, indent=4, sort_keys=False)
                sys.stdout.write("已生成新的配置文件config.json！\n\n")
                Log.logger.warning("已生成新的配置文件config.json！\nconfig.json 配置文件说明：\n\n    accessKeyId：你获取的阿里云accessKeyId\n    accessSecret：你获取的阿里云accessSecret\n\n    enableipv4/6：是否启用IPv4/6的DDNS动态域名更新\n    true 为启用，false 为禁用\n\n    domain：你的域名\n    names: 你的主机记录值（支持多个）\n\n    enabletimedrun: 是否启用后台自动间隔运行\n    true 为启用，false 为禁用\n    timedruntime: 为间隔运行时间（单位为秒）\n")
                try:
                    input("已生成新的配置文件，详细填写说明可以查看log文件，填入你的信息，并重新打开本程序！")
                except (KeyboardInterrupt):
                    sys.exit(0)
                sys.exit(0)
            except:
                Log.logger.error("无法从config.json加载配置文件！")
                sys.exit("无法从config.json加载配置文件！")
        if key:
            return GetConfig.getconfig.config.get(key, default)
        else:
            return GetConfig.getconfig.config

class DDNSUnit:
    def client():
        try:
            client = AcsClient(accessKeyId, accessSecret, "cn-hangzhou")
        except:
            Log.logger.error("运行中出现错误，请检查配置文件！")
            input("运行中出现错误，请检查配置文件！")
            sys.exit(0)
        return client

    def response(request):
        try:
            response = DDNSUnit.client().do_action_with_exception(request)
        except:
            Log.logger.error("运行中出现错误，请检查配置文件！")
            input("运行中出现错误，请检查配置文件！")
            sys.exit(0)
        return response

    def update(RecordId, RR, Type, Value):
        from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
        request = UpdateDomainRecordRequest()
        request.set_accept_format("json")
        request.set_RecordId(RecordId)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(Value)
        DDNSUnit.response(request)
        
    def add(DomainName, RR, Type, Value):
        from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
        request = AddDomainRecordRequest()
        request.set_accept_format("json")
        request.set_DomainName(DomainName)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(Value)
        DDNSUnit.response(request)
        
    def delete(Domain, Name):
        from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
        request = DeleteSubDomainRecordsRequest()
        request.set_accept_format("json")
        request.set_DomainName(Domain)
        request.set_RR(Name)
        DDNSUnit.response(request)
        
    def getinfo(Domain, Name):
        from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format("json")
        request.set_DomainName(Domain)
        request.set_SubDomain(Name + "." + Domain)
        response = DDNSUnit.response(request)
        info = json.loads(response)
        return info
        
    def index(i):
        Log.logger.info("类型：%s" % (info["DomainRecords"]["Record"][i]["Type"]))
        Log.logger.info("值：%s" % (info["DomainRecords"]["Record"][i]["Value"]))
        Log.logger.info(Log.logsa)

class GetIP:
    def getipv4():
        try:
            ipv4 = urlopen("https://api-ipv4.ip.sb/ip").read()
            ipv4 = str(ipv4, encoding="utf-8")
            ipv4 = ipv4.strip()
            Log.logger.info("获取到本机IPv4地址：%s" % ipv4)
        except:
            ipv4 = None
            Log.logger.error("无法获取本机IPv4地址，请检查配置！")
        return ipv4
        
    def getipv6():
        try:
            ipv6 = urlopen("https://api-ipv6.ip.sb/ip").read()
            ipv6 = str(ipv6, encoding="utf-8")
            ipv6 = ipv6.strip()
            Log.logger.info("获取到本机IPv6地址：%s" % ipv6)
        except:
            ipv6 = None
            Log.logger.error("无法获取本机IPv6地址，请检查配置！")
        return ipv6

class DDNS:
    def newaddipv4():
        if enableipv4 == True:
            ipv4 = GetIP.getipv4()
            if ipv4 != None:
                DDNSUnit.add(domain, name, "A", ipv4)
                Log.logger.info("域名（%s）新建解析成功" % (name + "." + domain))
                Log.logger.info(Log.logsa)
                
    def newaddipv6():
        if GetConfig.getconfig("enableipv6") == True:
            ipv6 = GetIP.getipv6()
            if ipv6 != None:
                DDNSUnit.add(domain, name, "AAAA", ipv6)
                Log.logger.info("域名（%s）新建解析成功" % (name + "." + domain))
                Log.logger.info(Log.logsa)
                
    def changeipv4():
        if enableipv4 == True:
            ipv4 = GetIP.getipv4()
            if ipv4 != None:
                if info["DomainRecords"]["Record"][i]["Value"].strip() != ipv4.strip():
                    DDNSUnit.update(info["DomainRecords"]["Record"][i]["RecordId"], name, "A", ipv4)
                    Log.logger.info("域名（%s）解析修改成功" % (name + "." + domain))
                else:
                    Log.logger.info("域名（%s）IPv4地址没变" % (name + "." + domain))
                Log.logger.info(Log.logsa)
                
    def changeipv6():
        if enableipv6 == True:
            ipv6 = GetIP.getipv6()
            if ipv6 != None:
                if info["DomainRecords"]["Record"][i]["Value"].strip() != ipv6.strip():
                    DDNSUnit.update(info["DomainRecords"]["Record"][i]["RecordId"], name, "AAAA", ipv6)
                    Log.logger.info("域名（%s）解析修改成功" % (name + "." + domain))
                else:
                    Log.logger.info("域名（%s）IPv6地址没变" % (name + "." + domain))
                Log.logger.info(Log.logsa)

    def Main():
        global domain,name ,info,i,enableipv4,enableipv6,accessKeyId,accessSecret
        enableipv4 = GetConfig.getconfig("enableipv4")
        enableipv6 = GetConfig.getconfig("enableipv6")
        accessKeyId = GetConfig.getconfig("accessKeyId")
        accessSecret = GetConfig.getconfig("accessSecret")
        domain = GetConfig.getconfig("domain")
        names = GetConfig.getconfig("names")
        for name in names:
            info = DDNSUnit.getinfo(domain, name)
            Log.logger.info(Log.logsb)
            Log.logger.info("域名：（%s）" % (name + "." + domain))
            Log.logger.info("总记录个数：%s" % (info["TotalCount"]))
            Log.logger.info("IPv4地址DDNS功能：{0}" .format("启用" if enableipv4 == True else "禁用"))
            Log.logger.info("IPv6地址DDNS功能：{0}" .format("启用" if enableipv6 == True else "禁用"))
            Log.logger.info(Log.logsa)
            if info["TotalCount"] == 0:
                DDNS.newaddipv4()
                DDNS.newaddipv6()
            elif info["TotalCount"] != 0:
                for i, element in enumerate(info["DomainRecords"]["Record"]):
                    if info["DomainRecords"]["Record"][i]["Type"] == "A":
                        DDNS.changeipv4()
                        if info["TotalCount"] == 1:
                            DDNS.newaddipv6()
                    elif info["DomainRecords"]["Record"][i]["Type"] == "AAAA":
                        DDNS.changeipv6()
                        if info["TotalCount"] == 1:
                            DDNS.newaddipv4()

class Timed:
    def Main():
        enabletimedrun = GetConfig.getconfig("enabletimedrun")
        timedruntime = int(GetConfig.getconfig("timedruntime"))
        Log.logger.info("计划任务执行功能：{0}" .format("启用" if enabletimedrun == True else "禁用"))
        if enabletimedrun == True:
            Log.logger.info("计划任务执行时间间隔：%s秒" %timedruntime)
            BackgroundScheduler().start()
            Log.logger.info("=====================开始执行计划任务====================")
            Log.logger.info("在运行中输入 Ctrl + C 可以退出本程序!")
            try:
                while True:
                    DDNS.Main()
                    time.sleep(timedruntime)
            except (KeyboardInterrupt):
                sys.exit(0)
            except (SchedulerNotRunningError):
                sys.exit(0)
        else:
            DDNS.Main()

if __name__ == "__main__":
        Timed.Main()