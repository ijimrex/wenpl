#encoding=utf-8
import jieba.posseg as pseg
import jieba
import sys
import urllib2  
import json 
import re 
import copy
jieba.load_userdict('../wendata/dict/dict.txt')
jieba.load_userdict('../wendata/dict/dict_manual.txt')
reload(sys)
sys.setdefaultencoding('utf-8')

# st={"查询 机房":"check the temperature","查询 湿度 机房":"check the moisture"}



def getStore():
	store={}
	surl="../wendata/store.json"
	fin=open(surl,'r+')
	line = fin.readline()

	while line:
		j = json.loads(line)
		store[j.keys()[0].encode('utf-8')]=j[j.keys()[0]]
		line = fin.readline()
	# print store
	fin.close()
	return store

def mergePositions(l):
	positions={}
	for x in l:
		for y in x:
			positions[y]='position'
	# purl="../wendata/dict/position.txt"
	# fin=open(purl,'r+')
	# p=fin.read()
	# jp=json.loads(p)
	# positions=toUTF8(jp)
	# print positions
	return positions

def getPosition(type):
	purl="../wendata/dict/"+type+".json"
	fin=open(purl,'r+')
	p=fin.read()
	jp=json.loads(p)
	pros=toUTF8(jp)
	# print positions
	return pros

def getPros():
	pros={}
	purl="../wendata/dict/pro.json"
	fin=open(purl,'r+')
	p=fin.read()
	jp=json.loads(p)
	pros=toUTF8(jp)
	# print positions
	return pros

def getGenerals():
	generals={}
	purl="../wendata/dict/general.json"
	fin=open(purl,'r+')
	p=fin.read()
	jp=json.loads(p)
	generals=toUTF8(jp)
	# print generals
	return generals

def getPeople():
	people={}
	purl="../wendata/dict/people.json"
	fin=open(purl,'r+')
	p=fin.read()
	jp=json.loads(p)
	people=toUTF8(jp)
	# print generals
	return people

def divide(str):
	#return the unicode format result
    words = pseg.cut(str)
    li=[]

    for w in words:
    	print w.word
    	# print w.flag
    	li.append([w.word.encode('utf-8'),w.flag.encode('utf-8')])
    return li

def filt(li,type):
	#get the specific words depending on the type you want
	rli=[]
	for w in li:
		if w[1]==type:
			rli.append(w[0])
	return rli

def paraFilter(store):
	#check parameters in store
	dictionary={}
	for x in store.keys():
		dictionary[x]=[]
		for y in x.split(" "):
			j=[]
			j=re.findall( r'\w+', y)
			if j!=[]:
				dictionary[x].append(j)
	# print dictionary
	return dictionary

def getQueryTypeSet(li,dictionary,para,pro,paraCategory):
	#calculate the types of the query words
	# showp()
	qType=[]
	Nkey=0
	hasPosition=0
	hasName=0
	paradic={}
	# print dictionary
	for w in li:
		word=w[0]
		if dictionary.has_key(word):
			qType.append(dictionary[word])
			if pro.has_key(word):
				Nkey+=1
			if paraCategory.has_key(word):
				paradic[paraCategory[word]]=word
	for x in paradic.values():
		para.append(x)
	if Nkey==0:
		return 0 		
	setType=set(qType)
	return setType

def getPrefixHit(setType,store):
	#calculate the hit times of each prefix sentences in store 
	count={}
	# print store
	# isZero=True
	for i in range(len(store.keys())):
		# print store.keys()[i]
		setStore=set(store.keys()[i].split(' '))
		# print setType
		# print setStore
		# print store
		# print setStore&setType
		count[store.keys()[i]]=len(setStore&setType)

	# print count
	return count

def ranking(count,setType):
	#calculate the probability
	N=len(setType)
	p={}
	for x in count.keys():
		p[x]=float(count[x]/float(N))
	p=sort(p)
	# for x in p:
	return p

def sort(p):
	dicts= sorted(p.iteritems(), key=lambda d:d[1], reverse = True)
	return dicts
	# print dicts

def revranking(count):
	# showDict(count)
	p={}
	for x in count.keys():
		p[x]=float(count[x]/float(len(x.split(" "))))
	# showDict(p)
	p=sort(p)
	# print p
	return p


def excuteREST(p,rp,st,para,paraDict):
	#p:正排序后的store匹配度列表
	#rp:反排序后的store匹配度列表
	#st:store字典 
	#para:输入语句中的参数列表
	#paraDict: store中参数列表
	# print showList()
	#p[[[],[]],[]]
	#st{:}
	p=resort(p,rp)
	print p[0][0]
	if len(para)==0:
		for x in p:
			if len(paraDict[x[0]])==0:
				url=st[x[0]]
				break
	elif len(para)==1:
		for x in p:
			if len(paraDict[x[0]])==1:
				url=st[x[0]]+para[0]
				break
	else:
		for x in p:
			if len(paraDict[x[0]])==2:
				url=st[x[0]][0]+para[0]+st[x[0]][1]+para[1]
				break

	# url=st[p[0][0]]
	# if len(para)!=0:
	# 	url+=para[0]
	# print url
	return getResult(url)


def getResult(url):
    # print url
    turl='../wendata/token'  
    fin1=open(turl,'r+')
    token=fin1.read()
    url='http://www.intellense.com:3080'+url
    # print url
    req=urllib2.Request(url)
    req.add_header('authorization',token)
    # response = urllib2.urlopen(req)
    fin1.close()
    # print response.read()
    return url
    # return response.read()
def resort(l1,l2):
	# 反向检查匹配度
	# print l2
	l1=copy.deepcopy(l1)
	l2=copy.deepcopy(l2)
	for x in range(len(l1)-1):
		if l1[x][1]==l1[x+1][1]:
			for y in range(len(l2)-1):
				if l2[y][0]==l1[x][0]:
					break
			for z in range(len(l2)):
				if l2[z][0]==l1[x+1][0]:
					break
			# print y 
			# print z
			if y>z:
				temp=copy.deepcopy(l1[x+1])
				l1[x+1]=copy.deepcopy(l1[x])
				l1[x]=copy.deepcopy(temp)
	return l1




def connectTuring(a):
	kurl='../wendata/turkey'
	fin=open(kurl,'r+')
	key=fin.read()
	url = r'http://www.tuling123.com/openapi/api?key='+key+'&info='+a  
	reson = urllib2.urlopen(url)       
	reson = json.loads(reson.read())  
	fin.close()
	# print reson['text'],'\n'
	return reson['text']        
def getDict(url):
	try:
		data = open(url,"r+").read()
		# print data
		return data
	except Exception as e:
		print e	
def toUTF8(origin):
	#change unicode type dict to UTF-8
	result={}
	for x in origin.keys():
		val=origin[x].encode('utf-8')
		x=x.encode('utf-8')
		result[x]=val
	return result
def showDict(l):
	for x in l.keys():
		print x+' '+str(l[x])
def showList(l):
	for x in l:
		print l
# def getResult():
#     turl='../wendata/token'  
#     qurl='../wendata/urls'
#     fin1=open(turl,'r+')
#     fin2=open(qurl,'r+')
#     token=fin1.read()
#     url=fin2.read()
#     req=urllib2.Request(url)
#     req.add_header('authorization',token)
#     response = urllib2.urlopen(req)
#     fin1.close()
#     fin2.close()
#     # print response.read()
#     return response.read()
sentence="查看设备类型"#todo：需要预处理一下，去掉空格和无意义符号
sentence=sentence.replace(' ', '')
people=getPeople()
cities=getPosition('cities')
towns=getPosition('towns')
stations=getPosition('stations')
devices=getPosition('devices')
positions=mergePositions([cities,towns,stations,devices])
pro=getPros()
general=getGenerals()
paraCategory=dict(positions,**people)
dict1=dict(general, **pro)
dict2=dict(dict1, **paraCategory)
st=getStore()#store dict
para=[]
keyphrase=pro.keys()
# print st
paraDict=paraFilter(st)
# print 'dic' 
# print paraDict
# keyphrase.append(positions.keys())
divideResult=divide(sentence)#list
sentenceResult=getQueryTypeSet(divideResult,dict2,para,pro,paraCategory)#set
# print para
# print sentenceResult


if sentenceResult==0:
	print ""
	print connectTuring(sentence)
else:
	hitResult=getPrefixHit(sentenceResult,st)#dict
	rankResult=ranking(hitResult,sentenceResult)#dict
	rerankingResult=revranking(hitResult)
	# showList(rankResult)
	# print rerankingResult
	excuteResult=excuteREST(rankResult,rerankingResult,st,para,paraDict)
	# b=filt(a,'v')
	print ""
	print excuteResult

