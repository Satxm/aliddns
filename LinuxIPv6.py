import os
import re

def IPv6Address():
    output = os.popen("ip address").read() #使用ip address读取IP
    # output = os.popen("ifconfig").read() #使用ifconfig读取IP
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

if __name__ == "__main__":
    print(IPv6Address())
