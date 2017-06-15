#encoding=utf-8
import jieba.posseg as pseg
import jieba
import sys
import urllib2  
import json  
jieba.load_userdict('../wendata/dict/device.txt')
reload(sys)
sys.setdefaultencoding('utf-8')

dictionary={"情况":"情况","状况":"情况","状态":"情况","样子":"情况","温度":"温度","机房":"机房","局站":"机房","房间":"机房","室内":"机房","查询":"查询","看看":"查询","看一看":"查询","显示":"查询","告诉":"查询","检查":"查询","查看":"查询","湿度":"湿度","坏掉":"损坏","报警":"报警","告警":"报警","警报":"报警","一般":"一般","严重":"严重","紧急":"紧急"}
dic_time={"昨天":"昨天","昨日":"昨天","昨儿":"昨天","今天":"今天","今日":"今天","今日":"今天","今儿":"今天","现在":"现在","此刻":"现在","此时":"现在","实时":"现在","当下":"现在"}
# st={"查询 机房":"check the temperature","查询 湿度 机房":"check the moisture"}

sentence="看下机房情况"
def getStore():
	store={}
	surl="../wendata/store.json"
	fin=open(surl,'r+')
	line = fin.readline()
	# print line
	while line:
		j = json.loads(line)
		store[j.keys()[0].encode('utf-8')]=j[j.keys()[0]]
		line = fin.readline()
		# print data
	# print store
	fin.close()
	return store



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


def getQueryTypeSet(li,dictionary):
	#calculate the types of the query words
	qType=[]
	for w in li:
		word=w[0]
		if dictionary.has_key(word):
			qType.append(dictionary[word])
	if len(qType)==0:
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
	return p

def sort(p):
	dicts= sorted(p.iteritems(), key=lambda d:d[1], reverse = True)
	return dicts
	# print dicts

def excuteREST(p,st):
	#p[[[],[]],[]]
	#st{:}
	# print p
	turl='../wendata/token' 
	fin1=open(turl,'r+')
	token=fin1.read()
	url=st[p[0][0]]
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





st=getStore()#dict
divideResult=divide(sentence)#list
sentenceResult=getQueryTypeSet(divideResult,dictionary)#set
# print sentenceResult
if sentenceResult==0:
	print ""
	print connectTuring(sentence)
else:
	hitResult=getPrefixHit(sentenceResult,st)#dict

	rankResult=ranking(hitResult,sentenceResult)#dict
	excuteResult=excuteREST(rankResult,st)
	# b=filt(a,'v')
	print ""
	print excuteResult

