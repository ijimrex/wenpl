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

sentence = "查询2017年杭州市的报警"  # todo：需要预处理一下，去掉空格和无意义符号
sentence = sentence.replace(' ', '')

def parseCommonExpressionDate(sentence):
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
    # isValid=acceptDate(sentence)
    # print isValid
    # if not isValid:
    #     return 0
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
            else:
                return 'timeError'

    sentence1 = re.sub(
        r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]',
        "",
        sentence)

    #年月日
    # print "--------年月日--------"
    match = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日', sentence1)
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

    sentence2 = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', "", sentence1)


    # 月日时
    # print "--------月日时--------"
    match = re.findall(r'(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', sentence2)
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

    sentence3 = re.sub(r'(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', "", sentence2)


    # 月日
    # print "--------月日--------"
    match = re.findall(r'(\d{1,2})月(\d{1,2})日', sentence3)

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

    sentence4 = re.sub(r'(\d{1,2})月(\d{1,2})日', "", sentence3)
    # 日时
    # print "--------日时--------"
    match = re.findall(r'(\d{1,2})日(\d{1,2})[点|时]', sentence4)
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


    sentence5 = re.sub(r'(\d{1,2})日(\d{1,2})[点|时]', "", sentence4)

    # 年月
    # print "--------年月--------"
    match = re.findall(r'(\d{4})年(\d{1,2})月', sentence5)
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


    sentence6 = re.sub(r'(\d{4})年(\d{1,2})月', "", sentence5)

    # 年
    # print "--------年--------"
    match = re.findall(r'(\d{4})年', sentence6)
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

    sentence7 = re.sub(r'(\d{4})年', "", sentence6)

    # 月
    # print "--------月--------"
    match = re.findall(r'(\d{1,2})月', sentence7)
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


    sentence8 = re.sub(r'(\d{1,2})月', "", sentence7)

    # 日
    # print "--------日--------"
    match = re.findall(r'(\d{1,2})日', sentence8)
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


    sentence9 = re.sub(r'(\d{1,2})日', "", sentence8)

    # 时
    # print "--------时--------"
    match = re.findall(r'(\d{1,2})[点|时]', sentence9)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = yearOfMonth[0] + "-" + yearOfMonth[1] + \
                '-' + yearOfMonth[2] + " "+match[x] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                timeList.append(tempStartTime)
                tag.append("h")
    # print timeList 
    if len(timeList)==0:
        return 0
    return normalizeDate(operatetimeList(timeList,tag))

    










    # if tlen==2 and not needRerange:


    # if

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


def getStore():
    store = {}
    surl = "../wendata/store.json"
    fin = open(surl, 'r+')
    line = fin.readline()

    while line:
        j = json.loads(line)
        store[j.keys()[0].encode('utf-8')] = j[j.keys()[0]]
        line = fin.readline()
    # print store
    fin.close()
    return store


def mergePositions(l):
    positions = {}
    for x in l:
        for y in x:
            positions[y] = 'position'
    # purl="../wendata/dict/position.txt"
    # fin=open(purl,'r+')
    # p=fin.read()
    # jp=json.loads(p)
    # positions=toUTF8(jp)
    # print positions
    return positions


def getPosition(type):
    purl = "../wendata/dict/" + type + ".json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    # print positions
    return pros


def getPros():
    pros = {}
    purl = "../wendata/dict/pro.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    # print positions
    return pros


def getGenerals():
    generals = {}
    purl = "../wendata/dict/general.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    generals = toUTF8(jp)
    # print generals
    return generals

def getPoints():
    generals = {}
    purl = "../wendata/dict/points.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    generals = toUTF8(jp)
    # print generals
    return generals


def getPeople():
    people = {}
    purl = "../wendata/dict/people.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    people = toUTF8(jp)
    # print generals
    return people


def getDict(url):
    try:
        data = open(url, "r+").read()
        # print data
        return data
    except Exception as e:
        print e

def divide(str):
    # return the unicode format result
    words = pseg.cut(str)
    li = []

    for w in words:
        # print w.word
        # print w.flag
        li.append([w.word.encode('utf-8'), w.flag.encode('utf-8')])
    return li


def filt(li, type):
    # get the specific words depending on the type you want
    rli = []
    for w in li:
        if w[1] == type:
            rli.append(w[0])
    return rli


def paraFilter(store):
    # check parameters in store
    dictionary = {}
    for x in store.keys():
        dictionary[x] = []
        for y in x.split(" "):
            j = []
            j = re.findall(r'\w+', y)
            if j != []:
                dictionary[x].append(j)
    # print dictionary
    return dictionary


def getQueryTypeSet(li, dictionary, para, pro, paraCategory):
    # calculate the types of the query words
    # showp()
    qType = []
    Nkey = 0
    hasPosition = 0
    hasName = 0
    paradic = {}
    # print pro
    for w in li:
        word = w[0]
        if word in dictionary.keys():
            qType.append(dictionary[word])
            if word in pro:
                Nkey += 1
            if word in paraCategory.keys():
                paradic[paraCategory[word]] = word
    for x in paradic.values():
        para.append(x)
    if Nkey == 0:
        return 0
    return qType


def pointquery(li,points,devices,stations,para):
    # showDict(stations)
    point=""
    device=""
    station=""
    for w in li:
        word=w[0]
        # print 1
        if points.has_key(word):
            point=word
        elif devices.has_key(word):
            device=word
        elif stations.has_key(word):
            station=word
    if point!="" and station!="" and device!="":
        url ="/data/point_info_with_real_time?station_name="+station+"&device_name="+device+"&point_name="+point
        return getResult(url)
    else:
        return 0

        
def getPrefixHit(qType, store):
    # calculate the hit times of each prefix sentences in store
    count = {}
    setType = set(qType)
    for i in range(len(store.keys())):
        setStore = set(store.keys()[i].split(' '))
        count[store.keys()[i]] = len(setStore & setType)
    return count


def ranking(count, qType):
    # calculate the probability
    setType = set(qType)
    N = len(setType)
    p = {}
    for x in count.keys():
        p[x] = float(count[x] / float(N))
    p = sort(p)
    return p


def sort(p):
    dicts = sorted(p.iteritems(), key=lambda d: d[1], reverse=True)
    return dicts
    # print dicts


def revranking(count):
    # showDict(count)
    p = {}
    for x in count.keys():
        p[x] = float(count[x] / float(len(x.split(" "))))
    # showDict(p)
    p = sort(p)
    # print p
    return p


def excuteREST(p, rp, st, para, paraDict, qType,remember):

    # p:正排序后的store匹配度列表
    # rp:反排序后的store匹配度列表
    # st:store字典
    # para:输入语句中的参数列表
    # paraDict: store中参数列表
    # print showList()
    # p[[[],[]],[]]
    # st{:}
    p = resort(p, rp)
    # print p
    writeData(p)
    url=""
    if len(para) == 0:
        for x in p:
            if len(paraDict[x[0]]) == 0:
                url = st[x[0]]
                remember.append(x)
                break
    elif len(para) == 1:
        for x in p:
            if len(paraDict[x[0]]) == 1:
                # print paraDict[x[0]][0][0]
                if qType.count(paraDict[x[0]][0][0]) == 1:
                    url = st[x[0]] + para[0]
                    remember.append(x)
                    break
        if url=="":
            return 0

    elif len(para) == 2:
        for x in p:
            if len(paraDict[x[0]]) == 2:
                url = st[x[0]][0] + para[0] + st[x[0]][1] + para[1][0]+st[x[0]][2]+para[1][1]
                remember.append(x)
                break
        if url=="":
            return 0


    # url=st[p[0][0]]
    # if len(para)!=0:
    # 	url+=para[0]

    return getResult(url)


def getResult(url):
    turl = '../wendata/token'
    fin1 = open(turl, 'r+')
    token = fin1.read()
    url = 'http://www.intellense.com:3080' + url
    print url
    fin1.close()

    req = urllib2.Request(url)
    req.add_header('authorization', token)
    try:
        response = urllib2.urlopen(req)
    except Exception as e:
        return 0

    

    # print response.read()
    print url
    return response.read()


def resort(l1, l2):
    # 反向检查匹配度
    # print l2
    l1 = copy.deepcopy(l1)
    l2 = copy.deepcopy(l2)
    # print l1
    # print l2
    # for x in range(len(l1)-1):
    # 	if l1[x][1]==l1[x+1][1]:
    # 		for y in range(len(l2)-1):
    # 			if l2[y][0]==l1[x][0]:
    # 				break
    # 		for z in range(len(l2)):
    # 			if l2[z][0]==l1[x+1][0]:
    # 				break
    # 		print y
    # 		print z
    # 		if y>z:
    # 			temp=copy.deepcopy(l1[x+1])
    # 			l1[x+1]=copy.deepcopy(l1[x])
    # 			l1[x]=copy.deepcopy(temp)
    nl = []
    g = -1
    group = -1
    gdict = {}
    newlist = []
    for x in l1:
        if g != x[1]:
            group += 1
            g = x[1]
            nl.append([])
            nl[group].append(x)
        else:
            nl[group].append(x)
    for g in nl:
        for x in g:
            for y in range(len(l2)):
                if x[0] == l1[y][0]:
                    gdict[x] = y
                    break
        sublist = sort(gdict)
        for x in sublist:
            newlist.append(x[0])
    return newlist


def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except BaseException:
        return False


def writeData(list):
    url = 'test.txt'
    fout = open(url, 'w+')
    for item in list:
        fout.write(item[0] + " " + str(item[1]) + '\n')
    fout.close()


def connectTuring(a):
    kurl = '../wendata/turkey'
    fin = open(kurl, 'r+')
    key = fin.read()
    url = r'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + a
    reson = urllib2.urlopen(url)
    reson = json.loads(reson.read())
    fin.close()
    # print reson['text'],'\n'
    return reson['text']


def showResult(result,types):
    if types[0]=="查询 全部 工单":
        return get_order_relations(result)

    if types[0]=="查询 全部 设备 类型":
        return get_device_type(result)

    if types[0]=="查询 全部 设备":
        return monitoring_manage_get_devices(result)

    if types[0]=="查询 全部 采集点":
        return get_point_types(result)

    if types[0]=="查询 全部 应急 演练 预案":
        return get_drill_plan(result)

    if types[0]=="查询 局站 名称":
        return get_stations_name(result)

    if types[0]=="查询 全部 操作 日志":
        return get_operation_logs(result)

    if types[0]=="查询 position 报警 数量":
        return get_children_with_warning_count(result)

    if types[0]=="查询 position 员工":
        return get_staff_from_district(result)

    if types[0]=="查询 people 操作 日志 历史"or types[0]=="查询 people time 操作 日志 历史":
        return get_user_operation_log(result)

    if types[0]=="查询 people 历史 工单" or types[0]=="查询 people time 历史 工单":
        return get_work_orders(result)
    if types[0]=="查询 position 报警" or types[0]=="查询 position time 报警":
        return get_warning(result)
    if types[0]=="查询 position 设备":
        return get_devices_by_parents_name(result)
    if types[0]=="查询 people 通知":
        return get_received_messages(result)

def get_order_relations(result):
    print result
    rstr=""
    for x in result['message']:
        rstr+="设备编号:"
        rstr+=x['Device']
        rstr+='\n'
        rstr+="局站名称:"
        rstr+=x['Station']
        rstr+='\n'
        rstr+='工作人员:'
        rstr+='\n'
        for worker in x['Worker_Id']:
            rstr+=worker['name']
            rstr+='\n工号:'
            rstr+=worker['id']
            rstr+='\n'
        rstr+='\n\n'
    return rstr

def get_device_type(result):
    print result
    rstr=""
    for x in result['response'].values():
        rstr+=x
        rstr+='\n'
    return rstr

def monitoring_manage_get_devices(result):
    rstr=""
    for x in result['response']:
        rstr+="设备ID:"
        rstr+=x['ID']
        rstr+='\n'
        rstr+="设备类型:"
        rstr+=x['device_type']
        rstr+='\n'
        rstr+="设备名称:"
        rstr+=x['name']
        rstr+='\n'
        rstr+="设备位置:"
        for y in x['parents'].values():
            rstr+=y
            rstr+=" "
        rstr+='\n\n'
    return rstr

def get_point_types(result):
    rstr=""
    for x in result['response']:
        rstr+="采集点名称:"
        rstr+=x['name']
        rstr+='\n'
    return rstr

def get_drill_plan(result):
    rstr=""
    for x in result['message']:
        for y in x['plans']:
            url="/preplans/get_plan_by_id?plan_id="+y
            plan=getResult(url)
            plan=json.loads(plan)
            # print plan['message']
            insidex=plan['message']
            # print insidex
            rstr+="演练名称:"
            rstr+=insidex['name']
            rstr+="\n演练时间:"
            rstr+=insidex['time']
            rstr+="\n演练地点:"
            rstr+=insidex['location']
            rstr+="\n实施人员:"
            rstr+=insidex['operator']
            rstr+="\n联系电话:"
            rstr+=insidex['phone']
            rstr+="\n参演人员:"
            rstr+=insidex['operator']
            rstr+="\n演练步骤:"
            for step in range(len(insidex['description'])):
                rstr+="\n步骤"+str(step+1)+':'
                rstr+=insidex['description'][step]
    return rstr

def get_stations_name(result):
    rstr=""
    for x in result['response']:
        rstr+=x
        rstr+='\n'
    return rstr

def get_operation_logs(result):
    rstr=""
    for x in result['response']:
        rstr+="日期:"
        rstr+=x['timestamp']
        rstr+='\n'
        rstr+="处理人:"
        rstr+=x['operator']
        rstr+='\n'
        rstr+="操作信息:"
        if x['operations']!=[]:
            rstr+=x['operations'][0]['from'][0]['area']+'-'+x['operations'][0]['from'][0]['station']+'-'+x['operations'][0]['from'][0]['device_name']+'-'+x['operations'][0]['from'][0]['title']
        rstr+='\n'
        rstr+="操作结果:"
        rstr+=x['is_all_success']
        rstr+='\n\n'
    return rstr

def get_devices_by_parents_name(result):
    rstr="设备名称:\n"
    for x in result['response']:
        rstr+=x['name']
        rstr+='\n'
    return rstr


def get_children_with_warning_count(result):
    rstr=""
    for x in result['response']:
        rstr+='名字:'
        rstr+=x['name']
        rstr+='\n一般报警:'
        rstr+=str(x['warning_counts'][2])
        rstr+='\n紧急报警:'
        rstr+=str(x['warning_counts'][1])
        rstr+='\n严重报警:'
        rstr+=str(x['warning_counts'][0])
        rstr+="\n\n"

    return rstr


def get_staff_from_district(result):
    rstr=""
    for x in result["response"]:
        rstr+="姓名:"
        rstr+=x['name']
        rstr+="\n性别:"
        rstr+=x['gender']
        rstr+="\n电话:"
        rstr+=x['cellphone']
        rstr+="\n电邮:"
        rstr+=x['email']
        rstr+="\n公司:"
        rstr+=x['company']
        rstr+="\n类型:"
        rstr+=x['type']
        rstr+="\n区域:"
        rstr+=x['district']['name']
        rstr+="\n资格认证:"
        for y in x['qualification']:
            rstr+=y['name']
    return rstr

def get_received_messages(result):
    print result
    rstr=""
    for x in result['response']:
        rstr+="发件人:"
        rstr+=x['sender']
        rstr+='\n'
        rstr+="时间:"
        rstr+=x['timestamp']
        rstr+='\n'
        rstr+="标题:"
        rstr+=x['title']
        rstr+='\n'
        rstr+="内容:"
        rstr+=x['content']
        rstr+='\n\n'
    return rstr

def get_user_operation_log(result):
    rstr=""
    for x in result['response']:
        rstr+="操作人员:"
        for y in x['foreign1']:
            rstr+=y['name']
            rstr+=" "
        rstr+="\n权限:"
        for y in x['foreign2']:
            rstr+=y['name']
            rstr+=" "
        rstr+='\n操作内容:'
        rstr+=x['operation']
        rstr+='\n操作时间:'
        rstr+=x['timestamp']
        rstr+='\n\n'
    return rstr

def get_work_orders(result):
    status={'0':'已发送','1':'已确认','2':'已处理','3':'已完成'}
    rstr=""
    for x in result['response']:
        rstr+="工单编号:"
        rstr+=str(x['ID'])
        rstr+="\n处理人:"
        rstr+=x['worker_name']
        rstr+="\n地点:"
        rstr=rstr+x['event_detail']['Local_Network']+"-"+x['event_detail']['Area']+'-'+x['event_detail']['Local_Network']+x['event_detail']['Station']
        rstr+="\n产生时间:"
        rstr+=x['event_detail']['Start_Time']
        rstr+="\n工单内容:"
        rstr=rstr+x['event_detail']['Device']+'-'+x['event_detail']['Point']+'-'+x['event_detail']['Warning_Type']
        rstr+="\n当前状态:"
        rstr+=status[str(x['status']['current_status'])]
        rstr+='\n\n'
    return rstr

def get_point_info_with_real_time(result):
    rstr=""
    x=result['response']
    rstr+="区域:"
    rstr+=x['point']['area']
    rstr+="\n"
    rstr+="设备:"
    rstr+=x['point']['device_name']
    rstr+="\n"
    rstr+="监测点:"
    rstr+=x['point']['name']
    rstr+="\n"
    rstr+="时间:"
    rstr+=x['point_real_time']['time']
    rstr+="\n"
    rstr+="数值:"
    rstr=rstr+str(x['point_real_time']['value'])+x['point']['units']
    rstr+="\n"
    rstr+="状态:"
    rstr+=x['point']['warning_type']
    rstr+="\n"
    rstr+="\n\n"

    return rstr

def get_warning(result):
    rstr=""
    for x in result['response']:
        rstr+="位置:"
        rstr=rstr+x['Local_Network']+x['Area']+'-'+x['Station']+'-'+x['Device']
        rstr+='\n'
        rstr+="监控点:"
        rstr+=x['Point']
        rstr+='\n'
        rstr+="数值:"
        rstr=rstr+str(x['Value'])+x['Units']
        rstr+='\n'
        rstr+="开始时间:"
        rstr+=x['Start_Time']
        rstr+='\n'
        rstr+="类型:"
        rstr+=x['Warning_Type']
        rstr+='\n'
        rstr+="状态:"
        rstr+=x['Status']
        rstr+='\n\n'

    return rstr






def toUTF8(origin):
    # change unicode type dict to UTF-8
    result = {}
    for x in origin.keys():
        val = origin[x].encode('utf-8')
        x = x.encode('utf-8')
        result[x] = val
    return result


def showDict(l):
    for x in l.keys():
        print x + ' ' + str(l[x])


def showList(l):
    for x in l:
        print x


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
def test():
    people = getPeople()
    cities = getPosition('cities')
    towns = getPosition('towns')
    stations = getPosition('stations')
    devices = getPosition('devices')
    positions = mergePositions([cities, towns, stations, devices])
    points=getPoints()
    pro = getPros()
    general = getGenerals()
    paraCategory = dict(positions, **people)
    dict1 = dict(general, **pro)
    dict2 = dict(dict1, **paraCategory)
    st = getStore()  # store dict
    # print st
    para = []
    keyphrase = pro.keys()
    paraDict = paraFilter(st)
    date = parseDate(sentence)
    ftype=0
    remember=[]

    # print stations
    # print paraDict
    # keyphrase.append(positions.keys())
    divideResult = divide(sentence)  # list

    sentenceResult = getQueryTypeSet(
        divideResult,
        dict2,
        para,
        pro,
        paraCategory)  # set
    # print para[0]
    # print sentenceResult[2]

    pointResult=pointquery(divideResult,points,devices,stations,para)
    if pointResult!=0:
        print get_point_info_with_real_time(json.loads(pointResult))
    elif sentenceResult == 0:
        print ""
        print connectTuring(sentence)
    else:
        if date!=0:
            sentenceResult.append('time')
        hitResult = getPrefixHit(sentenceResult, st)  # dict
        rankResult = ranking(hitResult, sentenceResult)  # dict
        rerankingResult = revranking(hitResult)
        if date!=0:
            para.append(date)
        # print rankResult
        # showList(rankResult)
        # print rerankingResult
        excuteResult = excuteREST(
            rankResult,
            rerankingResult,
            st,
            para,
            paraDict,
            sentenceResult,remember)
        if excuteResult==0:
            print connectTuring(sentence)
        # b=filt(a,'v')
        else:
            print " "
            print showResult(json.loads(excuteResult),remember[0])
test()

