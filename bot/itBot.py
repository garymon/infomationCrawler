#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

from config import config
from utils import slackUtils as slack
from utils import facebookUtils as facebook

def get_it_information():
    today = time
    yesterday = datetime.now() - timedelta(days=1)
    feed = facebook.get_lastest_feed(config.FACEBOOK_IT_PAGE_ID, yesterday.strftime("%y-%m-%d"), today.strftime("%y-%m-%d"))
    return feed

def is_sended_info(info):
    try:
        f_read = open("./lastest_send_feed.txt", "r");
    except IOError, e:
        print("not file exist")
        f_write = open("./lastest_send_feed.txt", "w");
        f_write.write(info.encode("utf-8"))
        f_write.close()
        return False

    print(info[:30])
    read_info = unicode(f_read.read(), "utf-8")
    print(read_info[:30])
    if info[:30] == read_info[:30]:
        f_read.close()
        return True
    else:
        f_read.close()
        f_write = open("./lastest_send_feed.txt", "w");
        f_write.write(info.encode("utf-8"))
        f_write.close()
        return False

def send_message(bot_name):
    data = []
    info = get_it_information().strip()

    if(info.__len__() < 1 or is_sended_info(info)):
        print("return false")
        return False
    else:
        data.append(info)
        post_data = "\n\n".join(data)
        slack.send_data(post_data)
        print("return true")
        return True



