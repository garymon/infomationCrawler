#!/usr/bin/python
# -*- coding: utf-8 -*-

import cStringIO
import random
import json
from datetime import datetime, timedelta
import os
from config import config
from utils import utils
from utils import doorayUtils as dooray


def get_anymarina_bot_info():
    domain = "https://twitter.com"
    url = domain + "/anymarina/"
    soap = utils.get_text_htmlparser(url)
    tweets = soap.find('li', {"data-item-type":"tweet"})
    permlinks = tweets.find('div', {'class':'tweet'})['data-permalink-path']
    divs = tweets.find('div',{"class":"content"}).find('p', {"class":"tweet-text"})
    msg = utils.replace_with_newlines(divs)
    return msg + "\n" + domain + permlinks + "\n"

def checkWorkingDay():
    #except 5, 6
    if datetime.today().weekday() > 4:
        print("false")
        return False

    current = datetime.now()
    print("Current Hour is " + str(current.hour))
    print(config.SEND_GIF_START_HOUR)
    print(config.SEND_GIF_END_HOUR)
    if config.SEND_GIF_START_HOUR < current.hour and config.SEND_GIF_END_HOUR > current.hour:
        print("true")
        return True
    else:
        print("false")
        return False

def getIcon():
    try:
        dataFile = open('GifSendHistory.json', 'r')
        historyData = json.load(dataFile)
    except:
        historyData = {}

    with open('GifSendHistory.json', 'w') as data_file:
        if len(config.ICON_URL) - 2 == len(historyData.keys()):
            historyData = {}
        while(1):
            url = random.choice(config.ICON_URL)
            if url not in historyData:
                historyData[url] = 1
                json.dump(historyData, data_file)
                print("get icon url = " + url)
                return url
            else:
                print("url history exist = " + url)


def send_message(bot_name):
    if checkWorkingDay():
        print("Time is Over")
        return True

    icon_url = getIcon()
    msg = get_anymarina_bot_info()

    # send to dooray-bot
    post_data = dooray.generate_post_data(icon_url + "\n" + msg, icon_url, bot_name, False)

    response = cStringIO.StringIO()
    for url in config.GIF_CHAT_HOOK_URL:
        print(url)
        dooray.send_data(url, post_data, response)

    response.close()
    print("return true")
    return True



