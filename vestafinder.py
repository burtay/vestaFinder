import requests
from Queue import Queue
import threading
import argparse
import re
requests.packages.urllib3.disable_warnings()


inputFile = ""
outputFile= ""
thread = ""

def banner():
    print ""
    print ""
    print "Haci Burtay"
    print "Twitter : @haciburtay"
    print "www.burtay.org"
    print "admin@burtay.org"
    print """
                 _            ___                 _     ___ _           _
 /\   /\___  ___| |_ __ _    / _ \__ _ _ __   ___| |   / __(_)_ __   __| | ___ _ __
 \ \ / / _ \/ __| __/ _` |  / /_)/ _` | '_ \ / _ \ |  / _\ | | '_ \ / _` |/ _ \ '__|
  \ V /  __/\__ \ || (_| | / ___/ (_| | | | |  __/ | / /   | | | | | (_| |  __/ |
   \_/ \___||___/\__\__,_| \/    \__,_|_| |_|\___|_| \/    |_|_| |_|\__,_|\___|_|"""
    print ""
    print ""

parser = argparse.ArgumentParser()
parser.add_argument("-i",help="IP List without http or https flag",required=True)
parser.add_argument("-o",help="Output file - default vestaFinder.txt",default="vestaFinder.txt")
parser.add_argument("-t",help="Thread count - default 10",default=10,type=int)
args = parser.parse_args()

inputFile = args.i
outputFile = args.o
thread = args.t

print "[+] Input file ",inputFile
print "[+] Output file",outputFile
print "[+] Thread count ",thread


banner()
q = Queue()

def yaz(dosya,data):
    ac = open(dosya,"a")
    ac.write(data)
    ac.close()

def ipList():
    ipler = open(inputFile,'r')
    ipler = re.split('\n',ipler.read())
    return ipler

def vestaControl(ip):
    print ip, " Checking..."
    try:
        vestaRequest = requests.get("https://"+ip+":8083",verify=False,timeout=2)
        es = re.search("vesta", vestaRequest.text)
        if es:
            print "Vesta Found -> ", ip
            yaz(outputFile,ip+"\n")
            return True
        else:
            return False
    except requests.Timeout:
        print ip," Timout"
    except requests.ConnectionError:
        pass

def worker():
    while True:
        item = q.get()
        vestaControl(item)
        q.task_done()

ipler = ipList()
for ip in ipler:
    q.put(ip)

for i in range(thread):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
q.join()