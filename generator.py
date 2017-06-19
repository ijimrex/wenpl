'''
Author:Lei Jin

'''
import urllib2  
import json 

def getJSON(url):
	data=[]
	try:
		fin=open(url,"r+")
		line = fin.readline()
		while line:
			data.append(line)
			line = fin.readline()
		# print data
		fin.close()
		# print data[0]
		return data
	except Exception as e:
		print e


def getName(data):
	names=[]
	for x in range(len(data)):
		j = json.loads(data[x])
		# print j 
		if j.has_key('name'):
			# print j 
			names.append(j['name'].encode('utf-8'))
	return set(names)
	# print names

def getCity(data):
	cities=[]
	for x in range(len(data)):
		# print data[x]
		j = json.loads(data[x])
		# print j 
		if j.has_key('parents') and  j['parents'].has_key('city'):
			# print j 
			cities.append(j['parents']['city'].encode('utf-8'))
	return set(cities)

def getTown(data):
	towns=[]
	for x in range(len(data)):
		# print data[x]
		j = json.loads(data[x])
		# print j 
		if j.has_key('parents') and  j['parents'].has_key('town'):
			# print j 
			towns.append(j['parents']['town'].encode('utf-8'))
	return set(towns)

def getStation(data):
	stations=[]
	for x in range(len(data)):
		j = json.loads(data[x])
		if j.has_key('parents') and  j['parents'].has_key('station'):
			stations.append(j['parents']['station'].encode('utf-8'))
	return set(stations)

def getDevice(data):
	devices=[]
	for x in range(len(data)):
		j = json.loads(data[x])
		if j.has_key('parents') and  j['parents'].has_key('device'):
			devices.append(j['parents']['device'].encode('utf-8'))
	return set(devices)





def writeData(list,type):
	url='../wendata/dict/'+type+'.txt'
	fout=open(url,'w+')
	for item in list:
		fout.write(item+'\n')
	fout.close()



def writePros(l):
	string="{"
	for x in l:
		for y in x:			
			string+='\"'+y+'\"'+': \"position\",'
	string=string[:-1]
	string+="}"
	print string
	url='../wendata/dict/position.txt'
	fout=open(url,'w+')
	fout.write(string)
	fout.close()






def getAll(data):
	names=getName(data)
	cities=getCity(data)
	towns=getTown(data)
	stations=getStation(data)
	devices=getDevice(data)
	writePros([cities,towns,stations])
	writeData(names,'name')
	writeData(cities,'city')
	writeData(towns,'town')
	writeData(stations,'station')
	writeData(devices,'device')
	


jsonData= getJSON("../wendata/hierarchy_elements.json")
getAll(jsonData)


