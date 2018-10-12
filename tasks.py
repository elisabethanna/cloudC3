from __future__ import absolute_import, unicode_literals
from .celery import app
import os
import json

@app.task
def readFile():
#loopa genom fler filer
    tweets = open('cloudC3/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3','r')
    tweets = tweets.read()
    tweets = tweets.split('\n\n')
    tweet_list = []
    for i in range(0,len(tweets)-1):
        single_tweet = json.loads(tweets[i])
        tweet_text=single_tweet["text"]
        tweet_list.append(tweet_text)
    return tweet_list

@app.task
def add(x,y):
    return x + y

@app.task
def countPronoun():
#retweets
    tweets = readFile()
    dic = {"han":0,
	   "hon":0,
	   "hen":0,
	   "den":0,
	   "det":0,
	   "denna":0,
           "denne":0}
    for i in tweets:
        if "han" in i:
           dic["han"] += 1
        if "hon" in i:
           dic["hon"] += 1
        if "hen" in i:
           dic["hen"] += 1
	if "den" in i:
           dic["den"] += 1
	if "det" in i:
           dic["det"] += 1
	if "denne" in i:
           dic["denne"] += 1
	if "denna" in i:
           dic["denna"] += 1
    return dic

