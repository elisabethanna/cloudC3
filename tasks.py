from celery import Celery
import re
import os
import json

celery = Celery('Annas light-weight Flask server w/ Celery', broker='pyamqp://', backend= 'rpc://')

def readFile():
    directory = './data/'
    tweet_list = []

    for file in getFiles():
        tweets = open(directory + file, 'r')
        tweets = tweets.read()
        tweets = tweets.split('\n\n')
        for i in range(0, len(tweets)-1):
            single_tweet = json.loads(tweets[i])
            tweet_text = single_tweet["text"]
            tweet_list.append(tweet_text)
    return tweet_list

def getFiles():
    for root, dirs, files in os.walk("./data"):
        for file in files:
            yield file

@celery.task
def countPronoun():
    tweets = readFile()
    dic = {"han": 0,
           "hon": 0,
           "hen": 0,
           "den": 0,
           "det": 0,
           "denna": 0,
           "denne": 0}
    for tweet in tweets:
	if tweet[0:2] != "RT":
             for word in tweet.split():
	         word = re.sub(r"[^A-Za-z]+", " ", word)
                 if "han" == word:
                     dic["han"] += 1
                 if "hon" == word:
                     dic["hon"] += 1
                 if "hen" == word:
                     dic["hen"] += 1
                 if "den" == word:
                     dic["den"] += 1
                 if "det" == word:
                     dic["det"] += 1
                 if "denne" == word:
                     dic["denne"] += 1
                 if "denna" == word:
                     dic["denna"] += 1
    print(dic)
    return dic

if __name__ == '__main__':
    celery.start()
