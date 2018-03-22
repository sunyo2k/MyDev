# -*- coding: utf-8 -*-
"""
function:
    - twitter search api を利用し15分以内の間、データ取得
version:
    prototype
data location:
├── log
│   └── search_tweets_api_201803.log
└── out
    └── search_tweets_api_20180320.csv
system prerequisites:
    - python3
memo:
    - python search_tweets_api.py --q '橋本環奈'
--q:
    # "任天堂 AND switch OR スイッチ"
    # "デジカメ OR 一眼レフ lang:ja (filter:images) min_retweets:10"
    # "剛 AND 結婚 since:2018-03-16_10:20:00_JST until:2018-03-16_10:26:00_JST"
written by:
    20180320. lee
"""
from requests_oauthlib import OAuth1
from datetime import datetime
import json
import requests
import urllib
import sys
import io
import csv
import argparse
import time

#EXE_DIR = "/home/userid/python/batch/"
EXE_DIR = "/"
DATE_NOW = datetime.now()
DATE_DAY = DATE_NOW.strftime('%Y%m%d')
DATE_MONTH = DATE_NOW.strftime('%Y%m')
LOG_FILENAME = EXE_DIR + "log/search_tweets_api_" + DATE_MONTH + ".log"
CSV_FILENAME = EXE_DIR + "out/search_tweets_api_" + DATE_DAY + ".csv"

# 15分以内に強制終了
TIME_OUT = 60 * 14
START_TIME = time.time()

def printlog(msg):
  line = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(msg)
  with open(LOG_FILENAME, "a") as file:
    file.write(line + '\r\n')
  print(line)

def get_auth():
    # lee account keys
    keys = {"consumer_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "consumer_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "access_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    # share account keys
#    keys = {"consumer_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#            "consumer_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#            "access_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    auth = OAuth1(keys['consumer_key'], keys['consumer_secret'], keys['access_token'], keys['access_secret'])
    return auth

def wait_n_get_remain():
    time.sleep(2)
    bLoop = True
    while bLoop:
        auth = get_auth()
        resp = requests.get("https://api.twitter.com/1.1/application/rate_limit_status.json", auth = auth)
        dat = resp.json()
        try:
            i_remain = int(dat['resources']['search']['/search/tweets']['remaining'])
        except:
            i_remain = 0

        if i_remain == 0:
            printlog("wait_n_get_remain remaining 0:{}".format(dat))
            bLoop = False

        if (time.time() - START_TIME) > TIME_OUT:
            printlog("wait_n_get_remain remaining {0}, TIME_OUT:{1}".format(i_remain, dat))
            bLoop = False

        if i_remain > 0:
            bLoop = False

    return i_remain

def write_csvs(data):
    filename = CSV_FILENAME
    try:
        with open(filename,"a") as f:
            #writer = csv.writer(f)
            writer = csv.writer(f, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
            writer.writerows(data)
            #printlog("write_csvs " + filename  + " " +  str(len(data)))
    except Exception as e:
        printlog("error write_csvs " + str(e))

def get_search_tweets(qry):
    # access_count and tweets_count
    respon_cnt = 0
    tweets_cnt = 0
    remain_cnt = 0

    # params 
    values = {"count": "100", "lang": "ja", "q": qry}
    params = urllib.parse.urlencode(values)

    # twitter search api request
    url = "https://api.twitter.com/1.1/search/tweets.json?" + params
    
    # get 1st auth and request
    auth = get_auth()
    if (not auth):
        printlog("get 1st auth error")
        return None
    # request
    response = requests.get(url, auth = auth)
    respon_cnt += 1
    data = response.json()['statuses']
    remain_cnt = wait_n_get_remain()
    printlog("api remaining {0}, response:{1}th, {2}".format(remain_cnt, respon_cnt, url))
    
    while remain_cnt > 0:
        # response data csv out
        if len(data) == 0:
            break
        else:
            rs = []
            for tweet in data:
                rs.append([tweet["user"]["id_str"],        # user id
                           tweet["user"]["screen_name"],   # user screen name
                           tweet["id_str"],                # tweet id
                           tweet["created_at"],            # tweet created time
                           tweet["retweet_count"],
                           tweet["favorite_count"],
                           tweet["text"],
                           qry])
                tweets_cnt += 1
                maxid = int(tweet["id_str"]) - 1
            write_csvs(rs)

        # get 2nd~ auth and request
        values = {"count": "100", "lang": "ja", "q": qry, "max_id":str(maxid)}
        params = urllib.parse.urlencode(values)
        url = "https://api.twitter.com/1.1/search/tweets.json?" + params
        # get auth
        auth = get_auth()
        if (not auth):
            printlog("get {0}th auth error".format(respon_cnt))
            return None
        response = requests.get(url, auth = auth)
        respon_cnt += 1
        data = response.json()['statuses']
        remain_cnt = wait_n_get_remain()
        printlog("api remaining {0}, response:{1}th, {2}".format(remain_cnt, respon_cnt, url))
    
    return tweets_cnt
#    print("tweets_cnt:" + str(tweets_cnt))    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", help="search twitter query", required=True)
    args = parser.parse_args()
    if args.q:
        #print(args.q)
        start_time = datetime.now()
        tweets_totcnt = get_search_tweets(args.q)
        end_time = datetime.now()
        printlog('finished. total tweets: {0}, q: {1}, duration: {2}'.format(tweets_totcnt, args.q, (end_time - start_time)))
    else:
        print('usage : search_tweets_api.py --q ["search twitter query"]')

if __name__ == "__main__":
    main()
