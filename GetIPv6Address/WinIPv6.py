import os
import re

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
    print("获取到本机IPv6地址：%s" % ipv6)