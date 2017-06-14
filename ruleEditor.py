import urllib2  
import json
import socket

get
def getResult():
    turl='../wendata/token'  
    qurl='../wendata/urls'
    fin1=open(turl,'r+')
    fin2=open(qurl,'r+')
    token=fin1.read()
    url=fin2.read()
    req=urllib2.Request(url)
    req.add_header('authorization',token)
    response = urllib2.urlopen(req)
    print response.read()
getResult()

