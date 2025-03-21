import glob

listIP = []

for i in glob.glob("*.log"):
    f = open(i)
    lines = list(f)
    for j in lines:
        posSubstr = j.find("ip address ")
        if posSubstr > -1 :
            ip = j.strip()[posSubstr + 10:].split(" ")[0]
            b = j.strip()[posSubstr + 10:].split(" ")
            if len(b) > 1 :
                mask = j.strip()[posSubstr + 10:].split(" ")[1]
            else:
                mask = ""
            print("IP: %-15s   Mask: %-15s" % (ip,mask))