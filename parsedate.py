# encoding=utf-8
import jieba.posseg as pseg
import jieba
import sys
import urllib2
import json
import re
import copy
import datetime
import time
import calendar

jieba.load_userdict('../wendata/dict/dict.txt')
jieba.load_userdict('../wendata/dict/dict_manual.txt')
jieba.load_userdict('../wendata/dict/dict_date.txt')
jieba.load_userdict('../wendata/dict/dict2.txt')
reload(sys)
sys.setdefaultencoding('utf-8')



def parseCommonExpressionDate(sentence):
    '''
    把常规说法换成日期区间
    '''
    preDate = getDate()
    words = []
    timeList = []
    tag = []
    numbers=[]
    yearOfMonth=[]
    today = datetime.date.today()
    today = str(today).split('-')
    yearOfMonth = today
    for key in preDate.keys():
        words.append(re.search(key, sentence))
    for word in words:
        numbers=[]
        if word is not None and (preDate[word.group()] == '现在' or preDate[word.group()] == '今天'):
            numbers=time.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            tempStartTime = str(numbers.tm_year) + '-' + str(numbers.tm_mon) + '-' + str(numbers.tm_mday) + " 00:00:00"
            timeList.append(tempStartTime)
            tag.append('ymd')
        if word is not None and preDate[word.group()] == '昨天':
            numbers=time.strptime((datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            tempStartTime = str(numbers.tm_year) + '-' + str(numbers.tm_mon) + '-' + str(numbers.tm_mday) + " 00:00:00"
            timeList.append(tempStartTime)
            tag.append('ymd')
        if word is not None and preDate[word.group()] == '前天':
            numbers=time.strptime((datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            tempStartTime = str(numbers.tm_year) + '-' + str(numbers.tm_mon) + '-' + str(numbers.tm_mday) + " 00:00:00"
            timeList.append(tempStartTime)
            tag.append('ymd')
        if word is not None:
            yearOfMonth[0]=str(numbers.tm_year)
            yearOfMonth[1]=str(numbers.tm_mon)
            yearOfMonth[2]=str(numbers.tm_mday)
    return [timeList,tag,yearOfMonth]

def parseCountExpressionDate(SENTENCE,TIMELIST,TAG,YEAROFMONTH):
    sentence=copy.deepcopy(SENTENCE)
    timeList=copy.deepcopy(TIMELIST)
    tag=copy.deepcopy(TAG)
    yearOfMonth=copy.deepcopy(YEAROFMONTH)
    words = []
    timeList = []
    tag = []
    match = re.findall(r'(\d+)天前', sentence)
    sentence1 = re.sub(r'(\d+)天前',"",sentence)
    for m in match:
        numbers=[]
        if m is not None:
            numbers=time.strptime((datetime.datetime.now()-datetime.timedelta(days=int(m))).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            tempStartTime = str(numbers.tm_year) + '-' + str(numbers.tm_mon) + '-' + str(numbers.tm_mday) + " 00:00:00"
            timeList.append(tempStartTime)
            tag.append('ymd')
            yearOfMonth[0]=str(numbers.tm_year)
            yearOfMonth[1]=str(numbers.tm_mon)
            yearOfMonth[2]=str(numbers.tm_mday)
    match = re.findall(r'(\d+)小时前', sentence1)
    sentence2 = re.sub(r'(\d+)小时前',"",sentence1)
    for m in match:
        numbers=[]
        if m is not None:
            numbers=time.strptime((datetime.datetime.now()-datetime.timedelta(hours=int(m))).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            tempStartTime = str(numbers.tm_year) + '-' + str(numbers.tm_mon) + '-' + str(numbers.tm_mday) + " "+str(numbers.tm_hour)+":00:00"
            timeList.append(tempStartTime)
            tag.append('ymdh')
            yearOfMonth[0]=str(numbers.tm_year)
            yearOfMonth[1]=str(numbers.tm_mon)
            yearOfMonth[2]=str(numbers.tm_mday)
            yearOfMonth.append(str(numbers.tm_hour))
    return [timeList,tag,yearOfMonth,sentence]

def toYMDH(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', sentence)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = match[x][0] + '-' + match[x][1] + \
                '-' + match[x][2] + " " + match[x][3] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[0]=match[x][0]
                yearOfMonth[1]=match[x][1]
                yearOfMonth[2]=match[x][2]
                yearOfMonth.append(match[x][3])
                tag.append("ymdh")

    return re.sub(
        r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]',
        "",
        sentence)

def toYMD(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日', sentence)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = match[x][0] + '-' + \
                match[x][1] + '-' + match[x][2] + " 00:00:00"
            # print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[0]=match[x][0]
                yearOfMonth[1]=match[x][1]
                yearOfMonth[2]=match[x][2]
                tag.append("ymd")

    return re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', "", sentence)

def toMDH(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', sentence)
    if match != []:
        if len(timeList)==1:
            tempStartTime = yearOfMonth[0] + '-' + match[x][0] + '-' + match[x][1] + " " + match[x][2] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[1] = match[x][0]
                yearOfMonth[2] = match[x][1]
                yearOfMonth.append(match[x][2])
                tag.append("mdh")
        else:
            for x in range(len(match)):
                j1 = int(today[1]) * 100 + int(today[2])
                j2 = int(match[x][0]) * 100 + int(match[x][1])
                # print j2
                if j1 < j2:
                    tempStartTime = str(int(
                        today[0]) - 1) + '-' + match[x][0] + '-' + match[x][1] + " " + match[x][2] + ":00:00"
                else:
                    tempStartTime = today[0] + '-' + match[x][0] + \
                        '-' + match[x][1] + " " + match[x][2] + ":00:00"
                # print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[1] = match[x][0]
                yearOfMonth[2] = match[x][1]
                yearOfMonth.append(match[x][2])
                tag.append("mdh")
    return re.sub(r'(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', "", sentence)


def toMD(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{1,2})月(\d{1,2})日', sentence)

    # print match
    if match != []:
        if len(timeList)==1:
            tempStartTime = yearOfMonth[0] + '-' + match[0][0] + '-' + match[0][1] + " 00:00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[1] = match[0][0]
                yearOfMonth[2] = match[0][1]
                tag.append("md")
        else:
            for x in range(len(match)):
                j1 = int(today[1]) * 100 + int(today[2])
                j2 = int(match[x][0]) * 100 + int(match[x][1])
                # print j2
                if j1 < j2:
                    tempStartTime = str(
                        int(today[0]) - 1) + '-' + match[x][0] + '-' + match[x][1] + " 00:00:00"
                else:
                    tempStartTime = today[0] + '-' + \
                        match[x][0] + '-' + match[x][1] + " 00:00:00"
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    timeList.append(tempStartTime)
                    yearOfMonth[1] = match[x][0]
                    yearOfMonth[2] = match[x][1]
                    tag.append( "md")

    return re.sub(r'(\d{1,2})月(\d{1,2})日', "", sentence)


def toDH(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{1,2})日(\d{1,2})[点|时]', sentence)
    # print match

    if match != []:
        if len(timeList)==1:
            tempStartTime = yearOfMonth[0] + '-' + yearOfMonth[1] + '-' + match[x][0] + " " + match[x][1] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[2] = match[x][0]
                yearOfMonth.append(match[x][1])
                tag.append("dh")
 
        else:
            for x in range(len(match)):
                j1 = int(today[2])
                j2 = int(match[x][0])
                # print j2
                if j1 < j2:
                    if int(today[1]) != 1:
                        tempStartTime = today[0] + '-' + str(int(today[1]) - 1) + '-' + match[x][0] + " " + match[x][1] + ":00:00"
                    else:
                        tempStartTime = today[0] + '-' + '12' + '-' + match[x][0] + " " + match[x][1] + ":00:00"
                else:
                    tempStartTime = today[0] + '-' + today[1] + \
                        '-' + match[x][0] + " " + match[x][1] + ":00:00"
                # print tempStartTime
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    timeList.append(tempStartTime)
                    yearOfMonth[2] = match[x][0]
                    yearOfMonth.append(match[x][1]) 
                    tag.append("dh")


    return re.sub(r'(\d{1,2})日(\d{1,2})[点|时]', "", sentence)


def toYM(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{4})年(\d{1,2})月', sentence)
    # print match
    if match != []:
        for x in range(len(match)):
            # monthRange = calendar.monthrange(int(match[x][0]), int(match[x][1]))
            # print monthRange
            tempStartTime = match[x][0] + '-' + \
                match[x][1] +"-1 00:00:00"
            # print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[0] = match[x][0]
                yearOfMonth[1] = match[x][1]
                tag.append("ym")

    return re.sub(r'(\d{4})年(\d{1,2})月', "", sentence)

def toY(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{4})年', sentence)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = match[x] + '-1-1' + " 00:00:00"
            # print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[0] = match[0]
                tag.append("y")

    return re.sub(r'(\d{4})年', "", sentence)

def toM(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{1,2})月', sentence)
    # print match
    if match != []:
        if len(timeList) == 1 :
            if len(match) == 1:
                print match
                if int(match[0]) < int(yearOfMonth[1]):
                    monthRange = calendar.monthrange(int(yearOfMonth[0]), int(yearOfMonth[1]))
                    tempStartTime = str(yearOfMonth[0]) + "-" + match[0] + '-1' + " 00:00:00"
                    timeList[0] = str(yearOfMonth[0]) + "-" + str(yearOfMonth[1]) + '-' + str(monthRange[1]) + " 00:00:00"
                else:
                    monthRange = calendar.monthrange(
                        int(yearOfMonth[0]), int(match[0]))
                    tempStartTime = str(yearOfMonth[0]) + "-" + match[0] + '-' + str(monthRange[1]) + " 00:00:00"
                # print tempStartTime
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    timeList.append(tempStartTime)
                    yearOfMonth[1] = match[0]
                    tag.append("m")

        else:
            for x in range(len(match)):
                tempStartTime = today[0] + "-" + match[x] + '-1' + " 00:00:00"
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    timeList.append(tempStartTime)
                    yearOfMonth[1] = match[0]
                    # yearOfMonth[1]=match[0]
                    tag.append("m")
    return re.sub(r'(\d{1,2})月', "", sentence)

def toD(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{1,2})日', sentence)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = yearOfMonth[0] + "-" + \
                yearOfMonth[1] + '-' + match[x] + " 00:00:00"
            print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                yearOfMonth[2] = match[0]
                tag.append("d")


    return re.sub(r'(\d{1,2})日', "", sentence)

def toH(sentence,timeList,tag,yearOfMonth):
    match = re.findall(r'(\d{1,2})[点|时]', sentence)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = yearOfMonth[0] + "-" + yearOfMonth[1] + \
                '-' + yearOfMonth[2] + " "+match[x] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                tag.append("h")

def parseDate(sentence):
    word = None
    timeList = []
    tag = []
    yearOfMonth = []
    today = datetime.date.today()
    today = str(today).split('-')
    yearOfMonth = today
    other=False
    # print yearOfMonth
    needRerange=False
    timeList=parseCommonExpressionDate(sentence)[0]
    tag=parseCommonExpressionDate(sentence)[1]
    yearOfMonth=parseCommonExpressionDate(sentence)[2]
    pced=parseCountExpressionDate(sentence,timeList,tag,yearOfMonth)
    timeList.extend(pced[0])
    tag.extend(pced[1])
    yearOfMonth=pced[2]
    sentence=pced[3]

    # 用户输入时间转成系统时间

    #年月日时
    # print "--------年月日时--------"

    sentence1=toYMDH(sentence,timeList,tag,yearOfMonth)

    #年月日
    # print "--------年月日--------"
    
    sentence2=toYMD(sentence1,timeList,tag,yearOfMonth)

    # 月日时
    # print "--------月日时--------"
    sentence3=toMDH(sentence2,timeList,tag,yearOfMonth)
    


    # 月日
    # print "--------月日--------"
    sentence4=toMDH(sentence3,timeList,tag,yearOfMonth)
    # 日时
    # print "--------日时--------"
    sentence5=toDH(sentence4,timeList,tag,yearOfMonth)

    # 年月
    # print "--------年月--------"
    
    sentence6=toYM(sentence5,timeList,tag,yearOfMonth)
    # 年
    # print "--------年--------"
    
    sentence7=toY(sentence6,timeList,tag,yearOfMonth)
    # 月
    # print "--------月--------"
    sentence8=toM(sentence7,timeList,tag,yearOfMonth)

    # 日
    # print "--------日--------"
    sentence9=toD(sentence8,timeList,tag,yearOfMonth)

    # 时
    # print "--------时--------"
    toH(sentence9,timeList,tag,yearOfMonth)
    # print timeList 
    if len(timeList)==0:
        return 0
    return normalizeDate(operatetimeList(timeList,tag))



def acceptDate(sentence):
    print sentence
    match=[]
    match.append(re.findall(r'(\d{4})年(\d{1,2})日', sentence))
    match.append(re.findall(r'(\d{4})年(\d{1,2}点)|(\d{1,2}时)', sentence))
    match.append(re.findall(r'(\d{1,2})月(\d{1,2}点)|(\d{1,2}时)', sentence))
    print match
    for x in match:
        if x!=None:
            return False
    return True

def compDate(l1,l2):
    c1=((l1.year*100+l1.month)*100+l1.day)*100+l1.hour
    c2=((l2.year*100+l2.month)*100+l2.day)*100+l2.hour
    return c1-c2

def findMin(l,tag):
    mini=l[0]
    t=tag[0]
    for x in range(1,len(l)):
        # print l[x]
        if compDate(mini,l[x])>0:
            mini=l[x]
            t=tag[x]
    return [mini,t]

def findMax(l,tag):
    maxi=l[0]
    t=tag[0]
    for x in range(1,len(l)):
        if compDate(maxi,l[x])<0:
            maxi=l[x]
            t=tag[x]
    return [maxi,t]

def conDate(y,m,d,h,mi,s):
    return str(y)+'-'+str(m)+'-'+str(d)+' '+str(h)+':'+str(mi)+':'+str(s)
def normalizeDate(l):
    returnList=[]
    for x in l:
        half=x.split(' ')[0]
        returnList.append(half+'%2002:42:12.134Z')
    return returnList

def operatetimeList(timeList,tag):
    timeListlen=len(timeList)
    returnList=[]
    today = datetime.date.today()
    today = str(today).split('-')
    todayTime=str(today[0]) + "-" + str(today[1]) + '-' + str(today[2]) + " 23:59:59"
    timecheck=[]
    for x in range(timeListlen):
        timecheck.append(datetime.datetime.strptime(timeList[x], "%Y-%m-%d %H:%M:%S"))
    # print timecheck[0].year
    if timeListlen==0 and tag==[]:
        return 0
    if timeListlen==1:
        returnList.append(timeList[0])
        monthRange = calendar.monthrange(timecheck[0].year, timecheck[0].month)
        if tag[0]=='y':
            returnList.append(conDate(timecheck[0].year,12,31,23,59,59))
        elif tag[0]=='ym' or tag[0]=='m':
            returnList.append(conDate(timecheck[0].year,timecheck[0].month,monthRange[1],23,59,59))
        elif tag[0]=='ymd' or tag[0]=='md' or tag[0]=='d':
            returnList.append(conDate(timecheck[0].year,timecheck[0].month,timecheck[0].day,23,59,59))
        elif tag[0]=='ymdh' or tag[0]=='mdh' or tag[0]=='dh' or tag[0]=='h':
            returnList.append(conDate(timecheck[0].year,timecheck[0].month,timecheck[0].day,timecheck[0].hour,59,59))
        return returnList
    if timeListlen>=2:
        # print timeList
        maxi=findMax(timecheck,tag)
        mini=findMin(timecheck,tag)
        timecheck[0]=mini[0]
        timecheck[1]=maxi[0]
        tag[1]=maxi[1]
        tag[0]=mini[1]
        if compDate(timecheck[0],timecheck[1])<0:
            returnList.append(conDate(timecheck[0].year,timecheck[0].month,timecheck[0].day,timecheck[0].hour,00,00))
            monthRange = calendar.monthrange(timecheck[1].year, timecheck[1].month)
            if tag[1]=='y':
                returnList.append(conDate(timecheck[1].year,12,31,23,59,59))
            elif tag[1]=='ym' or tag[1]=='m':
                returnList.append(conDate(timecheck[1].year,timecheck[1].month,monthRange[1],23,59,59))
            elif tag[1]=='ymd' or tag[1]=='md' or tag[1]=='d':
                returnList.append(conDate(timecheck[1].year,timecheck[1].month,timecheck[1].day,23,59,59))
            elif tag[1]=='ymdh' or tag[1]=='mdh' or tag[1]=='dh' or tag[1]=='h':
                returnList.append(conDate(timecheck[1].year,timecheck[1].month,timecheck[1].day,timecheck[1].hour,59,59))
        else:
            returnList.append(conDate(timecheck[1].year,timecheck[1].month,timecheck[1].day,timecheck[1].hour,00,00))
            monthRange = calendar.monthrange(timecheck[0].year, timecheck[0].month)
            if tag[0]=='y':
                returnList.append(conDate(timecheck[0].year,12,31,23,59,59))
            elif tag[0]=='ym' or tag[0]=='m':
                returnList.append(conDate(timecheck[0].year,timecheck[0].month,monthRange[1],23,59,59))
            elif tag[0]=='ymd' or tag[0]=='md' or tag[0]=='d':
                returnList.append(conDate(timecheck[0].year,timecheck[0].month,timecheck[0].day,23,59,59))
            elif tag[0]=='ymdh' or tag[0]=='mdh' or tag[0]=='dh' or tag[0]=='h':
                returnList.append(conDate(timecheck[0].year,timecheck[0].month,timecheck[0].day,timecheck[0].hour,59,59))
    return returnList


def getDate():
    pros = {}
    purl = "../wendata/dict/time.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    # print positionsge
    return pros


def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except BaseException:
        return False


def toUTF8(origin):
    # change unicode type dict to UTF-8
    result = {}
    for x in origin.keys():
        val = origin[x].encode('utf-8')
        x = x.encode('utf-8')
        result[x] = val
    return result
