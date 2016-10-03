# -*- coding: utf-8 -*-
#!/usr/bin/python  
#import urllib.request

########################################################################
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
#
#       Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#   Everyone is permitted to copy and distribute verbatim or modified
#   copies of this license document, and changing it is allowed as long
#   as the name is changed.
#
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#            0. You just DO WHAT THE FUCK YOU WANT TO.
########################################################################


import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re
import time
import sys   
reload(sys)  
ISOTIMEFORMAT='%Y-%m-%d %X'

def loginIn(userName,passWord):
    #设置cookie处理器
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
    urllib2.install_opener(opener)  
    #打开选课页面
    #获取验证码
    image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode')
    f = open('code.jpg','wb')
    f.write(image.read())
    f.close()
    #读取验证码
    code = raw_input('please input the checkcode!')
    #构造post数据
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
    header ={   
                'Host' : 'xk.urp.seu.edu.cn',   
                'Proxy-Connection' : 'keep-alive',
                'Origin' : 'http://xk.urp.seu.edu.cn',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
                }
    data = {
            'userId' : userName,
            'userPassword' : passWord, #你的密码，  
            'checkCode' : code,           #验证码 
            'x' : '33',     #别管
            'y' : '5'       #别管2
            }
            
    #post登录数据
    text = postData(posturl,header,data)
    print "login success"
    return text

def selectSemester(semesterNum):
    print "switch semester..."
    time.sleep(5)
    #构造选择学期的包
    geturl ='http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=2014&selectXq='+str(semesterNum)+'&selectTime=2014-05-30%2013:30~2014-06-07%2023:59'
    header = {  'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',        
    }
    data = {}
    #get获取学期课程
    text = getData(geturl,header,data)
    return text

def postData(posturl,headers,postData):
    postData = urllib.urlencode(postData)  #Post数据编码   
    request = urllib2.Request(posturl, postData, headers)#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
    response = urllib2.urlopen(request)  
    text = response.read().decode('utf-8')
    return text

def getData(geturl,header,getData):
    getData = urllib.urlencode(getData)
    request = urllib2.Request(geturl, getData, header)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-8') 
    return text

def stateCheck(textValue):
    print textValue    
    text = textValue.encode('gbk')
    #if (text.find('成功选择') != -1)or(text.find('服从推荐') != -1):
    if (text.find('成功选择') != -1)or(text.find('服从推荐') != -1):
        return 0
    if text.find('已满') != -1:
        return 1
    if text.find('失败') != -1:
        return 2

def Mode1(semesterNum):
    s =  semesterNum
    text = selectSemester(s)
    #寻找可以“服从推荐”的课程
    print "==============\n模式1，开始选课\n=============="
    courseList = []
    pattern = re.compile(r'\" onclick=\"selectThis\(\'.*\'')
    pos = 0
    m = pattern.search(text,pos)
    while m:
        pos = m.end()
        tempText = m.group()
        course = [tempText[23:31],tempText[34:51],tempText[54:56],1]
        courseList.append(course)
        m=pattern.search(text,pos)  #寻找下一个
    times = 0
    success = 0
    total = len(courseList)
    while True:
        if total == 0:
            break
        time.sleep(5)#sleep
        times = times +1
        print "\nthe"+str(times)+"times success"+str(success)+"门"
        for course in courseList:
            if 1 == course[3]:
            #构造选课post
                posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+course[1]+'&select_xkkclx='+course[2]+'&select_jhkcdm='+course[0]
                headers = { 'Host' : 'xk.urp.seu.edu.cn',
                        'Proxy-Connection' : 'keep-alive',
                        'Content-Length' : '2',
                        'Accept' : 'application/json, text/javascript, */*',
                        'Origin':'http://xk.urp.seu.edu.cn',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        }
                data = {'{}':''
                }
                #post选课包，并获取返回状态
                flag = stateCheck(postData(posturl,headers,data))
                #根据选课状态返回信息
                if 0 == flag:
                    course[3] = 0
                    success = success + 1
                    total = total - 1
                    print 'Nice, 课程'+str(course[0])+" 选择成功"
                if 1 == flag:
                    print '课程'+str(course[0])+" 名额已满"
                if 2 == flag:
                    print '课程'+str(course[0])+" 选课失败，原因未知"
       
def Mode2(semesterNum,courseName):
    s =  semesterNum
    text = selectSemester(s)
    print "==============\n模式2，开始选课\n=============="
    #获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    text = getData(geturl1,header1,data1)
    #构造RE  
    #print text
    text = text.encode('utf-8') 
    pattern = (courseName+'.*?(\"8%\" id=\"(.{0,20})\" align)').decode('gbk').encode('utf-8')
    #获取课程编号
    courseNo = re.findall(pattern,text,re.S)[0][1]
    #构造数据包
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    print "我开始选课了,课程编号："+courseNo
    times = 0
    while True :
        #判断是否选到课
        times = times+1
        text = getData(geturl1,header1,data1)
        text = text.encode('utf-8')
        pattern2 = ('已选(.{0,200})align=\"').decode('gbk').encode('utf-8')
        result = re.findall(pattern2,text,re.S)
        #print result
        success = len(result) #为0为不成功 继续
        if (0 != success)and(result[0].find(courseNo)!=-1):
            print "Nice，已经选到课程:"+courseNo
            break
        #发送选课包
        print "第"+str(times)+"次尝试选择课程"+courseNo+",但是没选到！"
        postData(posturl,headers,data)
        time.sleep(5)#sleep
    return 
def postRw(courseNo):
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    text = postData(posturl,headers,data)
    return text
def checkRwState(text):
    text = text.encode('gbk')
    if text.find('true') != -1:  #选课成功
        return 0
    if text.find('名额已满') != -1:
        return 1
    if text.find('冲突') != -1:
        return 2
    return

def Mode4(semester):
    s = semester
    text = selectSemester(s)
    print "==============\nMode 4\n=============="
    while True:
        posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh=04064030201620000&select_xkkclx=11&select_jhkcdm=04064030'
        headers = { 'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
        data = {'{}':''
        }
        #post选课包，并获取返回状态
        flag = stateCheck(postData(posturl,headers,data))
        print "seizing...\n"
        print time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
        #根据选课状态返回信息
        if 0 == flag:
            course[3] = 0
            success = success + 1
            total = total - 1
            print 'Nice, class'+str(course[0])+"success"
        if 1 == flag:
            print 'class'+str(course[0])+" no rest"
        if 2 == flag:
            print 'class'+str(course[0])+" fail and unknowable"
        time.sleep(3)


def Mode3(semester):
    s =  semester
    text = selectSemester(s)
    print "==============\n模式3，开始选课\n=============="
    #获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    text = getData(geturl1,header1,data1)
    text = text.encode('utf-8')
    #获取所有的课程编号
    pattern = ('\"8%\" id=\"(.{0,20})\" align').decode('gbk').encode('utf-8')
    courseList = re.findall(pattern,text,re.S)
    #print courseList 
    courseCtList =[]
    #找出并去掉冲突的课程
    for course in courseList:
        backText = postRw(course)
        state = checkRwState(backText)
        if state == 2:
            courseCtList.append(course)
        if state == 0:
            print "Nice 选到了一门课："+course
            return   #成功了
    #print courseCtList
    courseTemp = [i for i in courseList if (i not in courseCtList)]
    #print courseTemp
    times = 0
    while True:
        times = times + 1
        #找出已满的课程
        pattern = ('已满.+?(\"8%\" id=\")(.{0,20})\" align').decode('gbk').encode('utf-8')
        courseYmList = [i[1] for i in re.findall(pattern,text,re.S)]
        #print courseYmList
        #找出可以选的课程编号
        courseAva = [i for i in courseTemp if (i not in courseYmList) ]
        print courseAva
        #选课了
        if len(courseAva) == 0:
                    print "第"+str(times)+"次刷新，每门课都选不了.."
        else:
            for course in courseAva:
                state = checkRwState(postRw(course))
                if 0 == state:
                    print "Nice 选到了一门课："+course
                    return
                if 1 == state:
                    print "人品不好 眼皮子底下的课被抢了"
        #刷新人文选课界面
        text = getData(geturl1,header1,data1)
        text = text.encode('utf-8')
        time.sleep(5)

    


if __name__ == "__main__":
    print "\n\n\n\n"
    print "===================================================================== "
    print "                    Seu_Jwc_Fker \n"
    print "     visit github.com/SnoozeZ/seu_jwc_fker know more"
    print "===================================================================== "
    print "mode :"
    print "1. same school mode"
    print "2. desperat mode for humanity"
    print "3. violent mode for humanity"
    print "4. information security"
    #print "4. 只值守子界面“自然科学与技术科学类”中的指定一门课程（开发中）"
    #print "5. 输入指定任意门课程的名字并值守（课程类型不限）（开发中）"
    #mode = input('\nmode?：')
    #userId = raw_input('card?(eg:213111111)：')
    #passWord = raw_input('password?(eg:65535)：')
    #semester = input('semester(short semester = 1，autumn semester = 2，spring semester = 3)：')
    mode = 4
    userId = "213141027"
    passWord = "DOngda0818"
    semester = 2
    loginIn(userId,passWord)
    try:
        if 1 == mode:
            loginIn(userId,passWord)
            Mode1(semester)
        if 2 == mode:
            courseName = raw_input('请输入你想值守的人文课名称或者其关键词（如:音乐鉴赏）：')
            loginIn(userId,passWord)
            Mode2(semester,courseName)
        if 3 == mode:
            loginIn(userId,passWord)
            Mode3(semester)
        if 4 == mode:
            Mode4(semester)
    except:
        print Exception,":",ex
        input('haha')
    finally:
        input('按任意键退出')