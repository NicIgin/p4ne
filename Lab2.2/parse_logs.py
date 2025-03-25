import ipaddress
import re
import glob

dInterfaces = dict()

def ip_address_line(line):
    if re.match("^ip address (.+) (.+)($| )",line.strip()):
        interface = re.search('^ip address (.+?) (.+?)($| )',line.strip())
        ip = interface.group(1)
        mask = interface.group(2)
        return ipaddress.IPv4Interface(ip + '/' + mask)


def find_hostname(lines):
    for l in lines:
        if re.match("(sysname|hostname) (.+)$",l.strip()):
            return re.search('(sysname|hostname) (.+)$', l.strip()).group(2)

def read_logs(path):
    for i in glob.glob(path):
        f = open(i)
        list_interfaces = []
        lines = list(f)
        hostname = find_hostname(lines)
        for j in lines:
            if ip_address_line(j) != None :
                list_interfaces.append(ip_address_line(j).with_prefixlen)
        dInterfaces[hostname] = list(set(list_interfaces))
        f.close()

def show_interfaces():
    read_logs("../Lab1.5/*.log")
    return dInterfaces

print(show_interfaces())