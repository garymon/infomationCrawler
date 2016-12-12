#  -*- coding: euc-kr -*- 
import json;

import datetime;
import time;
import urllib2

# dizwe
app_id = " "
app_secret = " "
access_token = app_id + "|" + app_secret


# advaced information
def getFacebookPageFeedData(page_id, access_token, since, until):
    #  construct the URL string    
    base = "https://graph.facebook.com"
    node = "/" + page_id + "/feed"
    parameters1 = "/?fields=message,created_time,likes.limit(1).summary(true),"
    #  -b - cf -  comments.fields(message,parent).summary(true) (- cannot see replies)     
    # # -b - changed if you add parent in  filter(stream){message,id,"parent"}, you can see parent    
    parameters2 = "comments.summary(true).filter(stream){message}"
    time = "&since=%s&until=%s" % (since, until)
    access = "&access_token=%s" % access_token
    url = base + node + parameters1 + parameters2 + time + access
    print url  ###DEL        
    # retrieve data    
    data = json.loads(request_until_suceed(url))
    return data


def request_until_suceed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try:
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e  # wnat to know what error it is
            time.sleep(5)
            print "Error for url %s : %s" % (url, datetime.datetime.now())

    return response.read()


def fetch_feed():
    one_json = getFacebookPageFeedData(page_id, access_token, since, until)
    wan_data = []
    j = 0
    i = 0
    num = 0
    while True:
        try:
            test_status = one_json["data"][i]
            processed_test_status = processFacebookPageFeedStatus(test_status)
            wan_data.append(list(processed_test_status))
            print "%d th status in %d" % (i, num)
            i = i + 1
            num = num + 1
        except Exception, e:
            print e
            try:
                next_url = one_json["paging"]["next"]  # next url
                print next_url
                j = j + 1
                print "----"
                # print j #FOR CHECK
                one_json = json.loads(request_until_suceed(next_url))
                i = 0
                continue
            except KeyError:
                print 'End of Document'
                break

    return wan_data, num
