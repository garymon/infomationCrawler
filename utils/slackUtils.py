#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from config import config


def send_data(message, username, channel):
    body = {
        'text': message,
    }
    headers = {'contents-type': 'application/json'}
    r = requests.post(config.SLACK_INCOMING_URL, json=body, headers=headers)
    print r.text
