import ipaddress
import random

class IPv4RandomNetwork(ipaddress.IPv4Network):
    def __init__(self):
        ip = ipaddress.IPv4Address(random.randint(0x0b000000, 0xdf000000))
        mask = random.randint(8, 24)
        ipaddress.IPv4Network.__init__(self,(ip, mask),strict=False)

a = 1
listNets = []

while a <= 20:
    newNet = IPv4RandomNetwork()
    if not newNet.is_private:
        listNets.append(newNet)
        a = a + 1

def key_value(net):
    return  (int(net.netmask),int(net.network_address))

print(sorted(listNets,key=key_value))



