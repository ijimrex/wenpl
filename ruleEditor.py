import urllib2  
import json
import socket
turl='../wendata/token'  
qurl='../wendata/urls'

fin=open(turl,'r+')
token=fin.read()
# print token
url='http://www.intellense.com:3080/warnings/warnings_by_level_name?levels=[%22%E6%B1%9F%E5%B9%B2%E5%8C%BA%22]&limit=10&page_no=1&status=0'
req=urllib2.Request(url)
req.add_header('authorization',token)
response = urllib2.urlopen(req)
print response.read()

