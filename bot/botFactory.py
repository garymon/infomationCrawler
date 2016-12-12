#!/usr/bin/python
# -*- coding: utf-8 -*-
import itBot, gmiBot


class BotFactory:

    def __init__(self, name):
        if name == "gmi":
            self.bot_name = "굿모닝 정보통"
            self.send_message = gmiBot.send_message
        elif name == "it":
            self.bot_name = "미국발 IT 뉴스"
            self.send_message = itBot.send_message
        else:
            print("bot is not exist")
            print("bot list : gmi, it")
            exit(-1)