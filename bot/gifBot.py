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
    url = domain + "/Hangeul_doumi/"
    soap = utils.get_text_htmlparser(url)
    tweets = soap.find('li', {"data-item-type":"tweet"})
    permlinks = tweets.find('div', {'class':'tweet'})['data-permalink-path']
    divs = tweets.find('div',{"class":"content"}).find('p', {"class":"tweet-text"})
    msg = utils.replace_with_newlines(divs)
    return msg + "\n" + domain + permlinks + "\n"

def get_huribaro_bot_info():
    domain = "https://twitter.com"
    url = domain + "/hurry_pu/"
    soap = utils.get_text_htmlparser(url)
    tweets = [tag for tag in soap.find_all('li', {"data-item-type":"tweet"}) if "js-pinned" not in tag['class']][0]
    #permlinks = tweets.find('div', {'class':'tweet'})['data-permalink-path']
    divs = tweets.find('div',{"class":"content"}).find('p', {"class":"tweet-text"})
    msg = utils.replace_with_newlines(divs)
    return msg + "\n"

def checkWorkingDay():
    #except 5, 6
    if datetime.today().weekday() > 4:
        print("working day check False")
        return False

    current = datetime.now()
    print("Current Hour is " + str(current.hour))
    print(config.SEND_GIF_START_HOUR)
    print(config.SEND_GIF_END_HOUR)
    if config.SEND_GIF_START_HOUR <= current.hour and config.SEND_GIF_END_HOUR >= current.hour:
	if current.hour%2 == 0:		
	    print("working time check True")
            return True
	else:
	    print("working time chekc False, odd hour")
	    return False
    else:
        print("working time check False")
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
    if not checkWorkingDay():
        print("Time is Over")
        return True

    icon_url = getIcon()
    msg = get_anymarina_bot_info()
    msg += "\n" + get_huribaro_bot_info()
    # send to dooray-bot
    post_data = dooray.generate_post_data(icon_url + "\n" + msg, icon_url, bot_name, False)

    response = cStringIO.StringIO()
    for url in config.GIF_CHAT_HOOK_URL:
        print(url)
        dooray.send_data(url, post_data, response)

    response.close()
    print("return True")
    return True



