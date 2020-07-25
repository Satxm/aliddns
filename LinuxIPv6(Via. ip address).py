import os
import re

def ShortIPv6Address():
    output = os.popen("ip address").read()
    result = re.findall(r"    inet6 ([a-f0-9:]*::[a-f0-9:]*)/128 scope global dynamic noprefixroute", output, re.I)
    return result[0]

def LongIPv6Address():
    output = os.popen("ip address").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

if __name__ == "__main__":
    print("获取到本机短IPv6地址：%s" % ShortIPv6Address())
    print("获取到本机长IPv6地址：%s" % LongIPv6Address())
