#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pycurl
import cStringIO
import base64
import json
import time
import config
from bs4 import BeautifulSoup
import requests
import urllib2
import types
import random



# CONFIGURATIONS
import datetime


ICON_URL = "http://38.media.tumblr.com/b3f4b71d4e15e5b3e2426b2948feff2a/tumblr_npu6c6AyAe1sev9umo2_r1_250.gif"
BOT_NAME = "굿모닝 정보통"

# local settings
response = cStringIO.StringIO()

def GetTextHTMLPARSER(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def send_data(url, post_data):
    ret = False

    # init curl
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    curl.setopt(pycurl.POSTFIELDS, post_data)
    curl.setopt(pycurl.WRITEFUNCTION, response.write)

    try:
        curl.perform()
        http_code = curl.getinfo(pycurl.HTTP_CODE)
        if http_code is 200:
            ret = True
    except Exception, e:
        print "Exception : %s" % e
    finally:
        curl.close()

    return ret


def getGoodMorningInfomation():
    url = "http://blog.naver.com/PostList.nhn?blogId=middlesky&from=postList&categoryNo=6"
    soap = GetTextHTMLPARSER(url)
    divs = soap.find('div', {'id': 'postViewArea'}).find('div').findAll('div')
    last_index = divs.__len__()
    msg = replace_with_newlines(divs[last_index - 1])
    if(isToday(msg)):
        return msg
    else:
        return ""


def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, types.StringTypes):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text


def generate_post_data(msg, icon_url):
    # generate json data to post
    fmt = json.dumps({"botName": BOT_NAME, "botIconImage": icon_url, "text": msg, "attachments": []})
    return fmt


def isToday(msg):
    today = time.strftime('%m월%d일')
    todayWithOutZeroPadding = today.replace('0','')
    if unicode(msg.replace(" ", "")).encode('utf-8').find(today) > -1 or unicode(msg.replace(" ", "")).encode('utf-8').find(todayWithOutZeroPadding) > -1:
        return True
    else:
        return False


def getTodayOhaasa():
    url = "http://twitter.com/hello_ohaasa?lang=ko"
    soap = GetTextHTMLPARSER(url)
    ps = soap.find('ol', {'id': 'stream-items-id'}).findAll('p', {'class':'tweet-text'})

    today = time.strftime('%Y년%m월%d일')
    result = []
    result.append("별자리 운세 " + today + "\n")
    for p in ps:
        if isToday(p.text):
            result.append('\n'.join(p.text.split("\n")[1:]).encode('utf-8') + "\n")
    if result.__len__() > 1:
        return "\n".join(result)
    else:
        return ""


def sendMessage():
    data = []
    gmi = getGoodMorningInfomation().strip()
    if(gmi.__len__() < 1):
        print("return false")
        return False
    else:
        data.append(gmi)
        data.append(getTodayOhaasa().strip().decode('utf-8'))
        post_data = "\n\n".join(data)
        icon_url = random.choice(config.ICON_URL)
        # send to dooray-bot
        post_data = generate_post_data(icon_url + "\n" + post_data.strip(), icon_url)

        for url in config.CHAT_HOOK_URL:
            print(url)
            send_data(url, post_data)

        response.close()
        print("return true")
        return True

count = 0
print("Max Try Count = " + str(config.MAX_TRY_COUNT))
while(sendMessage() == False):
    print(datetime.datetime.now())
    print("sendMessageFail")
    count += 1
    print("current count = " + str(count))
    if(count > config.MAX_TRY_COUNT):
        print("count over " + str(config.MAX_TRY_COUNT))
        exit(-1)
    time.sleep(300)

print("sendMessageSuccess");


