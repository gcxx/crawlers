#-*- coding: UTF-8 -*-
# coding=gbk
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import re, urlparse
import json
import urllib2
from bs4 import BeautifulSoup
import webbrowser
import re
import json
import time
import pymongo
import stem
import stem.connection
import urllib2
from stem import Signal
from stem.control import Controller
import time, threading

class bcolors:
    HEADER = '\033[95m'#purple
    OKBLUE = '\033[94m'#blue
    OKGREEN = '\033[92m'#green
    WARNING = '\033[93m'#yello
    FAIL = '\033[91m'#red
    ENDC = '\033[0m'

def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()

def loop():
    
    while True:
        print threading.current_thread().name
        print threading.active_count()
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        if len(iidbuf) is not 0:    
            print 10000000-len(iidbuf)
            iid= iidbuf[0]
            iidbuf.pop(0)
            print iid
            
            try:
                if imdb_ids.find_one({'imdbID': iid}) == None:
                    url='http://www.imdb.com/title/'+iid+'/'
                    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
                    cont = urllib2.urlopen(req).read()
                    soup = BeautifulSoup(cont, "lxml")
                    data={}
                    data['imdbID']=iid
                    data['html_full']=cont
                    imdb_ids.insert_one(data)
                    print bcolors.OKGREEN+ "ADDED" + bcolors.ENDC
            except:
                print '!!!'
            end=time.time()
            print bcolors.OKBLUE+str((end-start)/60) + "M" + bcolors.ENDC
    
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}

client = pymongo.MongoClient('localhost', 27017)
db = client['imdbIDs']
imdb_ids=db['imdbIDs']
imdb_ids.ensure_index("imdbID",unique=True)

iidbuf=[]
start_num=0
while start_num<10000000:
    iid= str(start_num).zfill(7)
    iid='tt'+iid
    # print iid
    iidbuf.append(iid)
    start_num+=1
    if start_num%100000==0:
        print start_num
print len(iidbuf)

start=time.time()

for i in range(1):
    #print i
    #time.sleep(i*2)
    t = threading.Thread(target=loop, name='T'+str(i))
    #t1 = threading.Thread(target=loop, name='2')
    t.start()
    #t1.start()
    #print threading.active_count()

time.sleep(1)
count_changeIP=0
while 1:
    if threading.active_count()<200:
        t = threading.Thread(target=loop, name='T'+str(i))
        i+=1
        t.start()
    count_changeIP+=1
    try:
        if count_changeIP>=20:
            count_changeIP=0
            renew_connection()
            newIP = request("http://icanhazip.com/")
            print bcolors.FAIL+str(newIP)+bcolors.ENDC
    except:
        print 
    time.sleep(1)
    