import urllib2  
import json  
def getJosn(url):
	data=[]
	try:
		fin=open(url,"r+")
		line = fin.readline()
		while line:
			data.append(line)
			line = fin.readline()
		# print data
		return data
	except Exception as e:
		print e


# def getName(data):


print getJosn("./hierarchy_elements.json")