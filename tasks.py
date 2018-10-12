from flask import Flask
from celery import Celery
import os
import json

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] ='pyamqp://'
app.config['CELERY_RESULT_BACKEND'] ='rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def readFile():
#loopa genom fler filer
    tweets = open('0c7526e6-ce8c-4e59-884c-5a15bbca5eb3','r')
    tweets = tweets.read()
    tweets = tweets.split('\n\n')
    tweet_list = []
    for i in range(0,len(tweets)-1):
        single_tweet = json.loads(tweets[i])
        tweet_text=single_tweet["text"]
        tweet_list.append(tweet_text)
    return tweet_list

@celery.task
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
    json_pronoun = json.dumps(dic)
    return json_pronoun


@app.route('/countpronouns', methods=['GET'])
def main():
    pronoun = countPronoun.delay()
    while pronoun.ready() == False:
         if pronoun.ready() == True:
            return("anna")
    return("hej")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
