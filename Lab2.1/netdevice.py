import paramiko
import time
import re
import pprint
import requests


host_ip = '10.31.70.209'
login = 'restapi'
password = 'j0sg1280-7@'
BUF_SIZE = 20000
TIMEOUT = 1

ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy)

ssh_connection.connect(host_ip, username=login, password=password, look_for_keys=False, allow_agent=False)
session = ssh_connection.invoke_shell()

session.send("terminal length 0\n")
time.sleep(TIMEOUT)
session.send("show interface\n")
time.sleep(TIMEOUT*3)
ssh_output = session.recv(BUF_SIZE).decode().split('\n')
session.close()
interface_str = "SSH output:\n"
for line in ssh_output:
    if re.match('(.+?) is .*, line protocol',line):
        interface_str = interface_str + 'Interface: ' + (re.search('(.+?) is .*, line protocol',line).group(1)) + '\n'
    if re.match('.+([0-9]+) packets input, ([0-9]+) bytes.+',line):
        interface_str = interface_str + '   Packets input: ' + re.search('.+([0-9]+) packets input, ([0-9]+) bytes.+',line).group(1) + '\n'
    if re.match('.+([0-9]+) packets input, ([0-9]+) bytes.+',line):
        interface_str = interface_str + '   Bytes input: ' + re.search('.+([0-9]+) packets input, ([0-9]+) bytes.+',line).group(2) + '\n'
    if re.match('.+([0-9]+) packets output, ([0-9]+) bytes.+',line):
        interface_str = interface_str + '   Packets output: ' + re.search('.+([0-9]+) packets output, ([0-9]+) bytes.+',line).group(1) + '\n'
    if re.match('.+([0-9]+) packets output, ([0-9]+) bytes.+',line):
        interface_str = interface_str + '   Bytes output: ' + re.search('.+([0-9]+) packets output, ([0-9]+) bytes.+',line).group(2) + '\n\n'

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
r = requests.get('https://' + host_ip + '/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces', auth=(login, password), headers=headers, verify=False)

interface_str = interface_str + "API output:\n"

api_output = r.json()['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']
for interface in api_output:
    interface_str = interface_str + 'Interface: ' + interface['name'] + '\n' +\
                    '   Packets input: ' + interface['v4-protocol-stats']['in-pkts'] + '\n' + \
                    '   Bytes input: ' + interface['v4-protocol-stats']['in-octets'] + '\n' + \
                    '   Packets output: ' + interface['v4-protocol-stats']['out-pkts'] + '\n' + \
                    '   Bytes output: ' + interface['v4-protocol-stats']['out-octets'] + '\n\n'

print(interface_str)