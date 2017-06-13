#encoding=utf-8
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


sentence="我要查询"

def divide(str):
	#return the unicode format result
    words = pseg.cut(str)
    li=[]

    for w in words:
    	li.append([w.word,w.flag])
    return li

def filt(li,type):


def compare(li,store):


a=divide(sentence)
print a

