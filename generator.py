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
		if j.has_key('name') and j.has_key('parents') and j['parents'].has_key('device'):
			# print j 
			names.append(j['name'])
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
			cities.append(j['parents']['city'])
	return set(cities)

def getTown(data):
	towns=[]
	for x in range(len(data)):
		# print data[x]
		j = json.loads(data[x])
		# print j 
		if j.has_key('parents') and  j['parents'].has_key('town'):
			# print j 
			towns.append(j['parents']['town'])
	return set(towns)

def getStation(data):
	stations=[]
	for x in range(len(data)):
		j = json.loads(data[x])
		if j.has_key('parents') and  j['parents'].has_key('station'):
			stations.append(j['parents']['station'])
	return set(stations)

def getDevice(data):
	devices=[]
	for x in range(len(data)):
		j = json.loads(data[x])
		if j.has_key('parents') and  j['parents'].has_key('device'):
			devices.append(j['parents']['device'])
	return set(devices)

def getOnlineDevices(url):

	# print url
	devices=[]
	deviceTemp=json.loads(getResult(url))['response'].values()
	for x in deviceTemp:
		devices.append(x)


	return deviceTemp




def getResult(url):
    turl='../wendata/token'  
    fin1=open(turl,'r+')
    token=fin1.read()
    url='http://www.intellense.com:3080'+url
    req=urllib2.Request(url)
    req.add_header('authorization',token)
    response = urllib2.urlopen(req)
    fin1.close()
    # print response.read()
    # return url
    return response.read()


def createDict(l):
	strs=""
	for item in l:
		for x in item:
			strs+=x+' 1000\n'
	url='../wendata/dict/dict.txt'
	fout=open(url,'w+')
	fout.write(strs.encode('utf-8'))




def writeData(list,type):
	url='../wendata/dict/'+type+'.txt'
	fout=open(url,'w+')
	for item in list:
		fout.write(item.encode('utf-8')+'\n')
	fout.close()



def writePros(l,type):
	# print l
	string="{"
	for y in l:			
		string+='\"'+y+'\"'+': \"'+type+'\",'
	string=string[:-1]
	string+="}"
	# print string
	url='../wendata/dict/'+type+'.json'
	fout=open(url,'w+')
	fout.write(string.encode('utf-8'))
	fout.close()


def writeDevice(l):
	string="{"
	for x in l:
		for y in x:			
			string+='\"'+y+'\"'+': \"devices\",'
	string=string[:-1]
	string+="}"
	# print string
	url='../wendata/dict/position.txt'
	fout=open(url,'w+')
	fout.write(string)
	fout.close()



def getAll(data):
	names=getName(data)
	cities=getCity(data)
	towns=getTown(data)
	stations=getStation(data)
	devices=getOnlineDevices("/get_device_type")
	writePros(devices,'devices')
	writePros(cities,'cities')
	writePros(towns,'towns')
	writePros(stations,'stations')
	createDict([cities,towns,stations,devices])
	writeData(names,'names')

	


jsonData= getJSON("../wendata/hierarchy_elements.json")
getAll(jsonData)


