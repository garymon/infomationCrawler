#!/usr/bin/python
# -*- coding: utf-8 -*-

import cStringIO
import random
import time


from config import config
from utils import utils
from utils import doorayUtils as dooray


def get_goodmorning_infomation():
    url = "http://blog.naver.com/PostList.nhn?blogId=middlesky&from=postList&categoryNo=6"
    soap = utils.get_text_htmlparser(url)
    divs = soap.find('div', {'id': 'postViewArea'}).find('div').findAll('div')
    last_index = divs.__len__()
    msg = utils.replace_with_newlines(divs[last_index - 1])
    if(utils.is_today(msg)):
        return msg
    else:
        return ""


def get_today_ohaasa():
    url = "http://twitter.com/hello_ohaasa?lang=ko"
    soap = utils.get_text_htmlparser(url)
    ps = soap.find('ol', {'id': 'stream-items-id'}).findAll('p', {'class':'tweet-text'})

    today = time.strftime('%Y년%m월%d일')
    result = []
    result.append("별자리 운세 " + today + "\n")
    for p in ps:
        if utils.is_today(p.text):
            result.append('\n'.join(p.text.split("\n")[1:]).encode('utf-8') + "\n")
    if result.__len__() > 1:
        return "\n".join(result)
    else:
        return ""


def send_message(bot_name):
    data = []
    info = get_goodmorning_infomation().strip()
    if(info.__len__() < 1):
        print("return false")
        return False
    else:
        data.append(info)
        data.append(get_today_ohaasa().strip().decode('utf-8'))
        post_data = "\n\n".join(data)
        icon_url = random.choice(config.ICON_URL)
        # send to dooray-bot

        post_data = dooray.generate_post_data(icon_url + "\n" + post_data.strip(), icon_url, bot_name)

        response = cStringIO.StringIO()
        for url in config.CHAT_HOOK_URL:
            print(url)
            dooray.send_data(url, post_data, response)

        response.close()
        print("return true")
        return True



