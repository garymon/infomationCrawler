#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from config import myConfig as config


def send_data(message, username):
    body = {
        'username': username,
        'text': message,
    }
    headers = {'contents-type': 'application/json'}
    r = requests.post(config.SLACK_INCOMING_URL, json=body, headers=headers)
    print r.text
