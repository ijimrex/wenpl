#!/usr/bin/env python
#encoding:utf-8


import urllib2
import json
while 1:
    a=raw_input("A:")
    url = r'http://www.tuling123.com/openapi/api?key=77aa5b955fcab122b096f2c2dd8434c8&info='+a  
    reson = urllib2.urlopen(url)       #得到 HTTP 的返回码
    reson = json.loads(reson.read())   #把Json格式字符串解码转换成Python对象
    print "B:",reson['text'],'\n'              #将字典中的'text'键的值打印                           
