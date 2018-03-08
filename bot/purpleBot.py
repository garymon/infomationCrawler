#!/usr/bin/python
# -*- coding: utf-8 -*-

import cStringIO
import random
import time


from config import config
from utils import utils
from utils import doorayUtils as dooray
from menuParser import menu_parser
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag
from PIL import Image
from sys import platform
from time import sleep
from datetime import datetime
import types
import re
import urllib, cStringIO

driver_path = config.ROOT + "/webDriver"

def get_team_purple_time():
    if platform == "linux" or platform == "linux2":
        print("linux phantomjs loading...")
        driver = webdriver.PhantomJS(driver_path + '/phantomjs_linux')
    elif platform == "darwin":
        print("mac phantomjs loading...")
        driver = webdriver.PhantomJS(driver_path + '/phantomjs_mac')
    elif platform == "win32":
        print("Not support for window platform")
        return None;

    driver.get('http://whatsup.nhnent.com/')
    print('sleep 5....')
    sleep(5)
    driver.implicitly_wait(5)

    print("try login...")
    driver.find_element_by_id('user_id').send_keys(config.WHATSUP_ID)
    driver.find_element_by_id('user_pw').send_keys(config.WHATSUP_PASSWORD)
    driver.find_element_by_class_name('btn_login').click()
    print('sleep 5....')
    sleep(5)
    driver.implicitly_wait(5)

    print("go to board...")
    driver.get('https://nharmony.nhnent.com/user/hrms/odm/attend/purpleTime.nhn?menuCd=X005531')
    print('sleep 5...')
    sleep(5)
    driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tbody = soup.find('div', {'id':'dtlLayer'}).find('tbody')
    trs = soup.find('div', {'id':'dtlLayer'}).find('tbody').findAll('tr')

    def get_text(element):
        text = ''
        skip_string = False
        for elem in element.recursiveChildGenerator():
            if skip_string:
                skip_string = False
                continue
            if isinstance(elem, Tag) and 'rowspan' in elem.attrs and elem['rowspan'] > 2:
                skip_string = True
            elif isinstance(elem, types.StringTypes):
                text += elem.strip()
                text += ' ' 
            elif elem.name == 'br':
                text += '\n'
        return text

    msg = []
    for tr in trs[1:]:
        msg.append(get_text(tr))
    print(msg)
    print(u'\n'.join(msg).encode('utf-8'))
    return u'\n'.join(msg).encode('utf-8')

def send_message(bot_name):
    if datetime.today().weekday() > 4:
        print("working day check False")
        return False
    data = []
    purple_time = get_team_purple_time()
    if len(purple_time) == 0:
        print("text is empty!")
        return False
    else:
        data.append(purple_time)
        post_data = "\n\n".join(data)
        icon_url = random.choice(config.ICON_URL)
        print(icon_url)
        # send to dooray-bot
        post_data = dooray.generate_post_data("\n" + post_data.strip(), icon_url, bot_name, includePrefix=False)
        response = cStringIO.StringIO()
        for url in config.PURPLE_HOOK_URL:
            print(url)
            dooray.send_data(url, post_data, response)
            response.close()
        print("return true")
        return True
