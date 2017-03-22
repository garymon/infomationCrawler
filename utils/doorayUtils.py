#!/usr/bin/python
# -*- coding: utf-8 -*-
import pycurl
import json

# local settings


def send_data(url, post_data, response):
    ret = False

    # init curl
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    curl.setopt(pycurl.POSTFIELDS, post_data)
    curl.setopt(pycurl.WRITEFUNCTION, response.write)

    try:
        curl.perform()
        http_code = curl.getinfo(pycurl.HTTP_CODE)
        if http_code is 200:
            ret = True
    except Exception, e:
        print "Exception : %s" % e
    finally:
        curl.close()

    return ret


def generate_post_data(msg, icon_url, bot_name):
    # generate json data to post
    channelPrefix = "[@Channel](dooray://1387695619080878080/channels/1612808706219234589 \"channel\")\n"
    fmt = json.dumps({"botName": bot_name, "botIconImage": icon_url, "text": channelPrefix + msg, "attachments": []})
    return fmt


