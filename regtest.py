#encoding=utf-8

import sys
import json 
import re 
import copy
import datetime
import time


reload(sys)
sys.setdefaultencoding('utf-8')

# st={"查询 机房":"check the temperature","查询 湿度 机房":"check the moisture"}

sentence="查询2017年2月10日到2017年5月20日12"#todo：需要预处理一下，去掉空格和无意义符号
sentence=sentence.replace(' ', '')

def parseDate(string):
	#用户输入时间转成系统时间
	match = re.findall( r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})点|时', sentence)
	# print match

	# sentence = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})点|时', "", sentence)

	match = re.findall( r'(\d{4})年(\d{1,2})月(\d{1,2})日[A-Za-z]', sentence)
	print match

parseDate(sentence)
