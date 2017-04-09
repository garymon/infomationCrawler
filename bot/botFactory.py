#!/usr/bin/python
# -*- coding: utf-8 -*-
import itBot, gmiBot, stockBot, gifBot


class BotFactory:

    def __init__(self, name):
        if name == "gmi":
            self.bot_name = "굿모닝 정보통"
            self.send_message = gmiBot.send_message
        elif name == "it":
            self.bot_name = "미국발 IT 뉴스"
            self.send_message = itBot.send_message
        elif name == "stock":
            self.bot_name = "재무주치의"
            self.send_message = stockBot.send_message
        elif name == "gif":
            self.bot_name = "움짤과 아무말 봇"
            self.send_message = gifBot.send_message
        else:
            print("bot is not exist")
            print("bot list : gmi, it, stock")
            exit(-1)