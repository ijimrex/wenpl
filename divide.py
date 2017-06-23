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


reload(sys)
sys.setdefaultencoding('utf-8')


sentence = "查询2017年3月3日1点到1月的信息"  # todo：需要预处理一下，去掉空格和无意义符号
sentence = sentence.replace(' ', '')

def parseDate(string):
    preDate = getDate()
    word = None
    tl = []
    tag = ""
    yearOfMonth = []
    today = datetime.date.today()
    today = str(today).split('-')
    yearOfMonth = today
    # print yearOfMonth
    needReraneg=False
    # tl.append(str(datetime.datetime.now()))
    for key in preDate.keys():
        word = re.match(key, sentence)
        if word:
            break
    if word is not None and preDate[word.group()] == '现在':
        endTime = str(datetime.datetime.now()) + 'Z'
        # tl.append(str(datetime.datetime.now()))

    # 用户输入时间转成系统时间
    #年月日时
    match = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', sentence)
    print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = match[x][0] + '-' + match[x][1] + \
                '-' + match[x][2] + " " + match[x][3] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[0]=match[x][0]
                yearOfMonth[1]=match[x][1]
                yearOfMonth[2]=match[x][2]
                yearOfMonth.append(match[x][3])


                tag = "ymdh"
            else:
                return 'timeError'

    sentence1 = re.sub(
        r'(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]',
        "",
        sentence)



    #年月日
    match = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日', sentence1)
    # print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = match[x][0] + '-' + \
                match[x][1] + '-' + match[x][2] + " 00:00:00"
            print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[0]=match[x][0]
                yearOfMonth[1]=match[x][1]
                yearOfMonth[2]=match[x][2]
                tag = "ymd"
            else:
                return 'timeError'

    sentence2 = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', "", sentence1)


    # 月日时
    match = re.findall(r'(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', sentence2)
    if match != []:
        if len(tl)==1:
            tempStartTime = yearOfMonth[0] + '-' + match[x][0] + '-' + match[x][1] + " " + match[x][2] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[1] = match[x][0]
                yearOfMonth[2] = match[x][1]
                yearOfMonth.append(match[x][2])
                tag = "mdh"
            else:
                return 'timeError'
        else:
            if len(match)==2:
                needReraneg=True
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
                tl.append(tempStartTime)
                yearOfMonth[1] = match[x][0]
                yearOfMonth[2] = match[x][1]
                yearOfMonth.append(match[x][2])
                tag = "mdh"
            else:
                return 'timeError'
    print yearOfMonth

    sentence3 = re.sub(r'(\d{1,2})月(\d{1,2})日(\d{1,2})[点|时]', "", sentence2)


    # 月日
    match = re.findall(r'(\d{1,2})月(\d{1,2})日', sentence3)

    # print match
    if match != []:
        if len(tl)==1:
            tempStartTime = yearOfMonth[0] + '-' + match[x][0] + '-' + match[x][1] + " 00:00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[1] = match[x][0]
                yearOfMonth[2] = match[x][1]
                tag = "md"
            else:
                return 'timeError'
        else:
            if len(match)==2:
                needReraneg=True
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
                print tempStartTime
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    tl.append(tempStartTime)
                    yearOfMonth[1] = match[x][0]
                    yearOfMonth[2] = match[x][1]
                    tag = "md"
                else:
                    return 'timeError'
    sentence4 = re.sub(r'(\d{1,2})月(\d{1,2})日', "", sentence3)
    # 日时
    match = re.findall(r'(\d{1,2})日(\d{1,2})[点|时]', sentence4)
    print match

    if match != []:
        if len(tl)==1:
            tempStartTime = yearOfMonth[0] + '-' + yearOfMonth[1] + '-' + match[x][0] + " " + match[x][1] + ":00:00"
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[2] = match[x][0]
                yearOfMonth.append(match[x][1])
                tag = "dh"
            else:
                return 'timeError'
        else:
            for x in range(len(match)):
                j1 = int(today[2])
                j2 = int(match[x][0])
                print j2
                if j1 < j2:
                    if int(today[1]) != 1:
                        tempStartTime = today[0] + '-' + str(int(today[1]) - 1) + '-' + match[x][0] + " " + match[x][1] + ":00:00"
                    else:
                        tempStartTime = today[0] + '-' + '12' + '-' + match[x][0] + " " + match[x][1] + ":00:00"
                else:
                    tempStartTime = today[0] + '-' + today[1] + \
                        '-' + match[x][0] + " " + match[x][1] + ":00:00"
                print tempStartTime
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    tl.append(tempStartTime)
                    yearOfMonth[2] = match[x][0]
                    yearOfMonth.append(match[x][1]) 
                    tag = "dh"
                else:
                    return 'timeError'

    sentence5 = re.sub(r'(\d{1,2})日(\d{1,2})[点|时]', "", sentence4)

    # 年月
    match = re.findall(r'(\d{4})年(\d{1,2})月', sentence5)
    print match
    if match != []:
        if len(match)==2:
            needReraneg=True
        for x in range(len(match)):
            monthRange = calendar.monthrange(int(match[x][0]), int(match[x][1]))
            print monthRange
            tempStartTime = match[x][0] + '-' + \
                match[x][1] +"-"+ str(monthRange[1]) + " 23:59:59"
            print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[0] = match[x][0]
                yearOfMonth[1] = match[x][1]
                tag = "ym"
            else:
                return 'timeError'

    sentence6 = re.sub(r'(\d{4})年(\d{1,2})月', "", sentence5)

    # 年
    match = re.findall(r'(\d{4})年', sentence6)
    print match
    if match != []:
        if len(match)==2:
            needReraneg=True
        for x in range(len(match)):
            tempStartTime = match[x] + '-12-31' + " 23:59:59"
            print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[0] = match[0]
                tag = "y"
            else:
                return 'timeError'
    sentence7 = re.sub(r'(\d{4})年', "", sentence6)

    # 月
    match = re.findall(r'(\d{1,2})月', sentence7)
    print match
    if match != []:
        if len(match)==2:
            needReraneg=True
        if len(tl) == 1 :
            if len(match) == 1:
                if int(match[0]) < int(yearOfMonth[1]):
                    monthRange = calendar.monthrange(int(yearOfMonth[0]), int(yearOfMonth[1]))
                    tempStartTime = str(yearOfMonth[0]) + "-" + match[x] + '-1' + " 00:00:00"
                    tl[0] = str(yearOfMonth[0]) + "-" + str(yearOfMonth[1]) + '-' + str(monthRange[1]) + " 23:59:59"
                else:
                    monthRange = calendar.monthrange(
                        int(yearOfMonth[0]), int(match[0]))
                    tempStartTime = str(yearOfMonth[0]) + "-" + match[x] + '-' + str(monthRange[1]) + " 23:59:59"
                # print tempStartTime
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    tl.append(tempStartTime)
                    yearOfMonth[1] = match[0]
                    tag = ""
                else:
                    return 'timeError'
        else:
            if len(match)==2:
                needReraneg=True
            for x in range(len(match)):
                tempStartTime = today[0] + "-" + match[x] + '-1' + " 00:00:00"
                if isVaildDate(tempStartTime):
                    # startTime=tempStartTime+'Z'
                    tl.append(tempStartTime)
                    yearOfMonth[1] = match[0]
                    # yearOfMonth[1]=match[0]
                    tag = "m"
                else:
                    return 'timeError'

    sentence8 = re.sub(r'(\d{1,2})月', "", sentence7)

    # 日
    match = re.findall(r'(\d{1,2})日', sentence8)
    print match
    if match != []:
        if len(match)==2:
            needReraneg=True
        for x in range(len(match)):
            tempStartTime = yearOfMonth[0] + "-" + \
                yearOfMonth[1] + '-' + match[x] + " 00:00:00"
            print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                yearOfMonth[2] = match[0]
                tag = ""
            else:
                return 'timeError'

    sentence9 = re.sub(r'(\d{1,2})日', "", sentence8)

    # 时
    match = re.findall(r'(\d{1,2})[点|时]', sentence9)
    print match
    if match != []:
        for x in range(len(match)):
            tempStartTime = today[0] + "-" + today[1] + \
                '-' + today[2] + match[x] + ":00:00"
            print tempStartTime
            if isVaildDate(tempStartTime):
                # startTime=tempStartTime+'Z'
                tl.append(tempStartTime)
                tag = ""
            else:
                return 'timeError'

    print tl

    # if

# print 'date'
    # print startTime
    # return match
    # print ((datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M"))


def getDate():
    pros = {}
    purl = "../wendata/dict/time.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    # print positions
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


def getPeople():
    people = {}
    purl = "../wendata/dict/people.json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    people = toUTF8(jp)
    # print generals
    return people


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
    # print dictionary
    for w in li:
        word = w[0]
        if word in dictionary:
            qType.append(dictionary[word])
            if word in pro:
                Nkey += 1
            if word in paraCategory:
                paradic[paraCategory[word]] = word
    for x in paradic.values():
        para.append(x)
    if Nkey == 0:
        return 0
    return qType


def getPrefixHit(qType, store):
    # calculate the hit times of each prefix sentences in store
    count = {}
    setType = set(qType)
    # print store
    # isZero=True
    for i in range(len(store.keys())):
        # print store.keys()[i]
        setStore = set(store.keys()[i].split(' '))
        # print setType
        # print setStore
        # print store
        # print setStore&setType
        count[store.keys()[i]] = len(setStore & setType)

    # print count
    return count


def ranking(count, qType):
    # calculate the probability
    setType = set(qType)
    N = len(setType)
    p = {}
    for x in count.keys():
        p[x] = float(count[x] / float(N))
    p = sort(p)
    # for x in p:
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


def excuteREST(p, rp, st, para, paraDict, qType):
    """
    :param p:
    :
    """
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
    if len(para) == 0:
        for x in p:
            if len(paraDict[x[0]]) == 0:
                url = st[x[0]]
                break
    elif len(para) == 1:
        for x in p:
            if len(paraDict[x[0]]) == 1:
                print 'insadsasas'
                print paraDict[x[0]][0][0]
                print qType
                if qType.count(paraDict[x[0]][0][0]) == 1:
                    print 'ok'
                    url = st[x[0]] + para[0]
                    break
    else:
        for x in p:
            if len(paraDict[x[0]]) == 2:
                url = st[x[0]][0] + para[0] + st[x[0]][1] + para[1]
                break

    # url=st[p[0][0]]
    # if len(para)!=0:
    # 	url+=para[0]

    return getResult(url)


def getResult(url):
    # print url
    turl = '../wendata/token'
    fin1 = open(turl, 'r+')
    token = fin1.read()
    url = 'http://www.intellense.com:3080' + url
    # print url
    req = urllib2.Request(url)
    req.add_header('authorization', token)
    # response = urllib2.urlopen(req)
    fin1.close()
    # print response.read()
    return url
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


def getDict(url):
    try:
        data = open(url, "r+").read()
        # print data
        return data
    except Exception as e:
        print e


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
def test():
    people = getPeople()
    cities = getPosition('cities')
    towns = getPosition('towns')
    stations = getPosition('stations')
    devices = getPosition('devices')
    positions = mergePositions([cities, towns, stations, devices])
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
    # print 'dic'
    # print paraDict
    # keyphrase.append(positions.keys())
    divideResult = divide(sentence)  # list
    sentenceResult = getQueryTypeSet(
        divideResult,
        dict2,
        para,
        pro,
        paraCategory)  # set
    # print para
    # print sentenceResult


    if sentenceResult == 0:
        print ""
        # print connectTuring(sentence)
    else:
        hitResult = getPrefixHit(sentenceResult, st)  # dict
        rankResult = ranking(hitResult, sentenceResult)  # dict
        rerankingResult = revranking(hitResult)
        # print rankResult
        # showList(rankResult)
        # print rerankingResult
        excuteResult = excuteREST(
            rankResult,
            rerankingResult,
            st,
            para,
            paraDict,
            sentenceResult)
        # b=filt(a,'v')
        print ""
        print excuteResult
test()

