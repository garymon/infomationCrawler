#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import random
import sys
import time
from bot import botFactory
from config import config

count = 0


if len(sys.argv) < 2:
    print("error")
    print("command : python main.py {bot}")
    print("bot : [gmi, it, stock]")
    exit(-1)

module_name = sys.argv[1]

task = botFactory.BotFactory(module_name)
print("Max Try Count = " + str(config.MAX_TRY_COUNT))

while(task.send_message(task.bot_name) == False):
    print(datetime.datetime.now())
    print("sendMessageFail")
    count += 1
    print("current count = " + str(count))
    if(count > config.MAX_TRY_COUNT):
        print("count over " + str(config.MAX_TRY_COUNT))
        exit(-1)
    time.sleep(300)

print("sendMessageSuccess");