import os
import re

def ShortIPv6Address():
    output = os.popen("ifconfig").read()
    result = re.findall(r"        inet6 ([a-f0-9:]*::[a-f0-9:]*)  prefixlen 128  scopeid 0x0<global>", output, re.I)
    return result
    
def LongIPv6Address():
    output = os.popen("ifconfig").read()
    result = re.findall(r"        inet6 ([a-f0-9:]*:[a-f0-9:]*)  prefixlen 64  scopeid 0x0<global>", output, re.I)
    return result

if __name__ == "__main__":
    print("获取到本机短IPv6地址：%s" % ShortIPv6Address())
    print("获取到本机长IPv6地址：%s" % LongIPv6Address())
    ipv6 = ShortIPv6Address()
    if ipv6 == []:
        ipv6 = LongIPv6Address()[0]
    else:
        ipv6 = ShortIPv6Address()[0]
    print("获取到本机IPv6地址：%s" % ipv6)