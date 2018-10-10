from celery import Celery
import os
import json
#import utf-8
app = Celery('tasks', backend='rpc://', broker='pyamqp://')
app.conf.task_serializer = 'json'
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
)
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y

def readFile():
    tweets = open('data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3','r')
    tweets = tweets.read()
    tweets = tweets.split('\n\n')
    tweet_list = []
    for i in range(0,len(tweets)-1):
        single_tweet = json.loads(tweets[i])
        tweet_text=single_tweet["text"]
        tweet_list.append(tweet_text)
    return tweet_list

def countPronoun():
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


def createFile():
    data = {}
    data['hon'] = []
    data['han'] = []
    data['hen'] = []
    data['hon'].append({
    'count':'1'
	})
    data['han'].append({
    'count':'2'
	})
    data['hen'].append({
    'count':'3'
        })
    with open('counter.txt', 'w') as outfile:
       json.dump(data,outfile)
    return(data)
