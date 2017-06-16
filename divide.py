#encoding=utf-8
import jieba.posseg as pseg
import jieba
import sys
import urllib2  
import json  
jieba.load_userdict('../wendata/dict/device.txt')
reload(sys)
sys.setdefaultencoding('utf-8')

general={"情况":"情况","状况":"情况","状态":"情况","样子":"情况","温度":"温度","查询":"查询","看看":"查询","看一看":"查询","显示":"查询","告诉":"查询","检查":"查询","查看":"查询","湿度":"湿度","全部":"全部","所有":"全部","位置":"位置","地理位置":"位置"}
pro={"机房":"监控点","局站":"局站","房间":"监控点","室内":"监控点","坏掉":"损坏","报警":"报警","告警":"报警","警报":"报警","一般":"一般","严重":"严重","紧急":"紧急","设备":"设备","机器":"设备","设施":"设备","类型":"类型","种类":"类型"}
dict_time={"昨天":"昨天","昨日":"昨天","昨儿":"昨天","今天":"今天","今日":"今天","今日":"今天","今儿":"今天","现在":"现在","此刻":"现在","此时":"现在","实时":"现在","当下":"现在"}
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
		# print data
	# print store
	fin.close()
	return store

def getParents():
	parents={}
	purl="../wendata/dict/parent.txt"
	fin=open(purl,'r+')
	p=fin.read()
	jp=json.loads(p)
	parents=toUTF8(jp)
	# print parents
	return parents

def divide(str):
	#return the unicode format result
    words = pseg.cut(str)
    li=[]

    for w in words:
    	# print w.word
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

def getQueryTypeSet(li,dictionary,para,keyphrase):
	#calculate the types of the query words
	qType=[]
	Nkey=0
	# print dictionary
	for w in li:
		word=w[0]
		if dictionary.has_key(word):
			qType.append(dictionary[word])
			if keyphrase.has_key(word):
				Nkey+=1
				para.append(word)
			# print dictionary[word]
	# print Nkey
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

	p={}
	for x in count.keys():
		p[x]=float(count[x]/float(len(x)))
	p=sort(p)
	return p


def excuteREST(p,st,para):
	# print p
	#p[[[],[]],[]]
	#st{:}
	# print p
	turl='../wendata/token' 
	fin1=open(turl,'r+')
	token=fin1.read()
	url=st[p[0][0]]
	if len(para)!=0:
		url+para[0]
	# print url
	return getResult(url)

def getDict(url):
	try:
		data = open(url,"r+").read()
		# print data
		return data
	except Exception as e:
		print e

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

def toUTF8(origin):
	#change unicode type dict to UTF-8
	result={}
	for x in origin.keys():
		val=origin[x].encode('utf-8')
		x=x.encode('utf-8')
		result[x]=val
	return result

sentence="杭州有哪些设备"

parents=getParents()
dic=dict(parents, **pro)
dictionary=dict(dic, **general)
# print dictionary
st=getStore()#store dict
para=[]
keyphrase=pro.keys()
keyphrase.append(parents)
divideResult=divide(sentence)#list
sentenceResult=getQueryTypeSet(divideResult,dictionary,para,dic)#set
# print sentenceResult


if sentenceResult==0:
	print ""
	print connectTuring(sentence)
else:
	hitResult=getPrefixHit(sentenceResult,st)#dict
	rankResult=ranking(hitResult,sentenceResult)#dict
	rerankingResult=revranking(hitResult)
	# print rerankingResult
	excuteResult=excuteREST(rankResult,st,para)
	# b=filt(a,'v')
	print ""
	print excuteResult

