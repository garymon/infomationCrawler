#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import utils
from utils import slackUtils as slack


def get_goodmorning_infomation():
    url = "http://blog.naver.com/PostList.nhn?blogId=gaessim&from=postList&categoryNo=19&parentCategoryNo=19"
    soap = utils.get_text_htmlparser(url)
    divs = soap.find('div', {'id': 'postListBody'}).find('div', {'id': 'postViewArea'}).findAll('div')
    last_index = divs.__len__()
    msg = utils.replace_with_newlines(divs[last_index - 1])
    if(utils.is_today(msg)):
        return msg
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
        post_data = "\n\n".join(data)
        slack.send_data(post_data)
        print("return true")
        return True



