#encoding=utf-8
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

dictionary={"温度":"温度","机房":"机房","房间":"机房","室内":"机房","查询":"查询","看看":"查询","看一看":"查询","检查":"查询","湿度":"湿度","坏掉":"损坏"}

st={"查询 机房":"check the temperature","查询 湿度 机房":"check the moisture"}

sentence="我要查询机房的湿度"

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
			qType.append(word)
	if len(qType)==0:
		return 0 		
	setType=set(qType)
	# print setType
	return setType

def getPrefixHit(setType,store):
	count={}
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

	# print st[p[0][0]]
	return st[p[0][0]]


divideResult=divide(sentence)
sentenceResult=getQueryTypeSet(divideResult,dictionary)
if sentenceResult==0:
	print ""
	print excuteResult
else:
	hitResult=getPrefixHit(sentenceResult,st)

	rankResult=ranking(hitResult,sentenceResult)
	excuteResult=excuteREST(rankResult,st)
	# b=filt(a,'v')
	print ""
	print excuteResult

