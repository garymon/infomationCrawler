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
from PIL import Image
from sys import platform
import re
import urllib, cStringIO


def get_menu_image():

    if platform == "linux" or platform == "linux2":
        print("linux phantomjs loading...")
        driver = webdriver.PhantomJS('./webDriver/phantomjs_linux')
    elif platform == "darwin":
        print("mac phantomjs loading...")
        driver = webdriver.PhantomJS('./webDriver/phantomjs_mac')
    elif platform == "win32":
        print("Not support for window platform")
        return None;

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    driver.implicitly_wait(3)
    driver.get('http://whatsup.nhnent.com/')

    print("try login...")
    driver.find_element_by_id('user_id').send_keys(config.WHATSUP_ID)
    driver.find_element_by_id('user_pw').send_keys(config.WHATSUP_PASSWORD)
    driver.find_element_by_class_name('btn_login').click()

    print("go to board...")
    #총무/복리후생
    driver.get('http://whatsup.nhnent.com/ne/board/list/1560')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print("find first PORT629 link...")
    alinks = soup.findAll('a', text=re.compile('PORT629'), attrs={'class': 'pageableInfo'})
    #find first PORT629
    if len(alinks) == 0:
        print("Can not find link!!!")
        return None;

    print("http://whatsup.nhnent.com/ne/board" + alinks[0]['href'][2:])
    print("go to link...")

    driver.get("http://whatsup.nhnent.com/ne/board" + alinks[0]['href'][2:])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print("find image...")
    image = soup.find('div', {'class': 'view_post'}).find('img')
    if image is not None:
        file = cStringIO.StringIO(urllib.urlopen(image['src']).read())
        print("save Image...")
        menu_parser.get_day_meal_image(Image.open(file), time.strftime('%A'), 0).save("today_menu.png")
        return menu_parser.get_day_meal_image(Image.open(file), time.strftime('%A'), 0)
    else:
        print("image not found!")
        return None;


def send_message(bot_name):
    data = []
    today_menu_image = get_menu_image()

    if today_menu_image is None:
        print("image is None!")
        return False
    else:
        print("Found Image!")
        return True
    # info = get_goodmorning_infomation().strip()
    # if(info.__len__() < 1):
    #     print("return false")
    #     return False
    # else:
    #     data.append(info)
    #     data.append(get_today_ohaasa().strip().decode('utf-8'))
    #     post_data = "\n\n".join(data)
    #     icon_url = random.choice(config.ICON_URL)
    #     # send to dooray-bot
    #
    #     post_data = dooray.generate_post_data(icon_url + "\n" + post_data.strip(), icon_url, bot_name)
    #
    #     response = cStringIO.StringIO()
    #     for url in config.CHAT_HOOK_URL:
    #         print(url)
    #         dooray.send_data(url, post_data, response)
    #
    #     response.close()
    #     print("return true")
    #     return True



