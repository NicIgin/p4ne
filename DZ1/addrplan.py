import ipaddress
import re
import glob
import openpyxl


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

listInterfaces = sorted(list(set(listInterfaces)))

wb = openpyxl.Workbook()

ws = wb.active

ws.append(["Сеть","Маска"])

for i in listInterfaces:
    ws.append([i.network.with_prefixlen.split("/")[0],i.network.with_prefixlen.split("/")[1]])

wb.save("plan.xlsx")