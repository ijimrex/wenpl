#encoding=utf-8
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

dictionary={"温度":"温度","机房":"机房","房间":"机房","室内":"机房","查询":"查询","看看":"查询","看一看":"查询","检查":"查询","湿度":"湿度","坏掉":"损坏"}
st={["查询","温度"]:"check the temperature",["查询","湿度"]:"check the moisture"}
sentence="坏掉了"

def divide(str):
	#return the unicode format result
    words = pseg.cut(str)
    li=[]

    for w in words:
    	print w.word
    	print w.flag
    	li.append([w.word,w.flag])
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
	setType=set(qType)
	return setType

def getPrefixHit(setType,store):
	count={}
	for i in range(len(store)):
		setStore=set(store[i])
		count[store[i]]=len(setStore&setType)
	return count

def ranking(count,setType):
	N=len(setType)
	p={}
	for x in count.keys():
		p[x]=float(count[x]/float(N))
	return p






# m=set([1,2,4])


a=divide(sentence)
# b=getQueryTypeSet(a,dictionary)
# c=getPrefixHit(b,st)
# d=ranking(c,b)
# b=filt(a,'v')
print a

