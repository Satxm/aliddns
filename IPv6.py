import os
import re
import logging
import sys

sys = sys.platform
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("logs.log",encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(message)s')


if sys == "linux":
    def ShortIPv6Address():
        output = os.popen("ifconfig").read()
        result = re.findall(r"        inet6 ([a-f0-9:]*::[a-f0-9:]*)  prefixlen 128  scopeid 0x0<global>", output, re.I)
        return result
    
    def LongIPv6Address():
        output = os.popen("ifconfig").read()
        result = re.findall(r"        inet6 ([a-f0-9:]*:[a-f0-9:]*)  prefixlen 64  scopeid 0x0<global>", output, re.I)
        return result

if sys == "win32":
    def ShortIPv6Address():
        output = os.popen("ipconfig /all").read()
        result = re.findall(r"IPv6 地址 . . . . . . . . . . . . : ([a-f0-9:]*::[a-f0-9:]*)", output, re.I)
        return result
    def LongIPv6Address():
        output = os.popen("ipconfig /all").read()
        result = re.findall(r"IPv6 地址 . . . . . . . . . . . . : ([a-f0-9:]*:[a-f0-9:]*)", output, re.I)
        return result

if __name__ == "__main__":
    ipv6 = ShortIPv6Address()
    if ipv6 == []:
        ipv6 = LongIPv6Address()[0]
    else:
        ipv6 = ShortIPv6Address()[0]
    logs = "获取到本机IPv6地址：%s" % ipv6
    logger.info(logs)