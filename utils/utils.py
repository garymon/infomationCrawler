#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import types
import time


def is_today(msg):
    today = time.strftime('%m월%d일')
    today_without_zeropadding = today.replace('0','')
    if unicode(msg.replace(" ", "")).encode('utf-8').find(today) > -1 or unicode(msg.replace(" ", "")).encode('utf-8').find(today_without_zeropadding) > -1:
        return True
    else:
        return False


def get_text_htmlparser(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, types.StringTypes):
            if 'SE3-TEXT' not in elem:
                text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text

