#!/usr/bin/env python
#encoding:utf-8


import urllib2
import json
while 1:
    a=raw_input("A:")
    url = r'http://www.tuling123.com/openapi/api?key=005640f142244059a35c0ee5069c0070&info='+a  #请求的网址
    reson = urllib2.urlopen(url)       #得到 HTTP 的返回码
    reson = json.loads(reson.read())   #把Json格式字符串解码转换成Python对象
    print "B:",reson['text'],'\n'              #将字典中的'text'键的值打印                           
