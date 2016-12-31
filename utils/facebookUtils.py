#  -*- coding: euc-kr -*- 
import json;
import csv;
import datetime;
import time;
import urllib2
import gzip
from StringIO import StringIO

from config import myConfig as config


def get_facebook_page_feed(page_id, since, until):

    app_id = config.FACEBOOK_APP_ID
    app_secret = config.FACEBOOK_ACCESS_TOKEN
    access_token = app_id + "|" + app_secret

    base = "https://graph.facebook.com"
    feed_url = "/" + page_id + "/feed"
    parameters1 = "/?fields=message"
    time = "&since=%s&until=%s" % (since, until)
    access = "&access_token=%s" % access_token
    url = base + feed_url + parameters1 + time + access
    data = json.loads(request_to_url(url))
    return data


def request_to_url(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try:
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            print "Error for url %s : %s" % (url, datetime.datetime.now())

    return response.read()


def get_lastest_feed(page_id, since, until):
    one_json = get_facebook_page_feed(page_id, since, until)
    if len(one_json["data"]) > 0 :
        feed = one_json["data"][0]["message"]
        return feed
    else:
        return ""



