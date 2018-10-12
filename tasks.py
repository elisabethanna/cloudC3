from celery import Celery
import os
import json

celery = Celery('Annas light-weight Flask server w/ Celery', broker='pyamqp://', backend= 'rpc://')

def readFile():
#loopa genom fler filer
    #root = 'pathToRootDir' #Rot-mappen alla separata filer ligger i :)
    #for file in getFiles()
        #tweets = open(root + file, 'r')
        #Fo what you want with each separate file :D

    tweets = open('0c7526e6-ce8c-4e59-884c-5a15bbca5eb3','r')

    tweets = tweets.read()
    tweets = tweets.split('\n\n')
    tweet_list = []
    for i in range(0,len(tweets)-1):
        single_tweet = json.loads(tweets[i])
        tweet_text=single_tweet["text"]
        tweet_list.append(tweet_text)
    return tweet_list

#def getFiles():
    #for root, dirs, files in os.walk(root):
        #for file in files:
            #yield file

@celery.task
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

if __name__ == '__main__':
    celery.start()
