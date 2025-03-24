import ipaddress
import re
import glob

listInterfaces = []

def ip_address_line(line):
    if re.match("^.+ip address (.+) (.+)",line):
        interface = re.search('^.+ip address (.+?) (.+?)($| )',line)
        ip = interface.group(1)
        mask = interface.group(2)
        listInterfaces.append(ipaddress.IPv4Interface(ip + '/' + mask))

def read_logs(path):
    for i in glob.glob(path):
        f = open(i)
        lines = list(f)
        for j in lines:
            ip_address_line(j)

read_logs("../Lab1.5/*.log")

for i in listInterfaces:
    print(i.ip)