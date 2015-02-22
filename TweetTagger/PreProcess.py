__author__ = 'marc'

from nlp import tweebo
import os
import json

import logging
logger = logging.getLogger('Tweebo.py')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

with open(os.path.join(os.curdir, 'dump/tweet1.json')) as data_file:
    tweets = json.load(data_file)

text = []
text.append(tweets["text"])
text.append("Word I'm bout to holla at her via twitter RT @iamJay_Fresh : #trushit - im tryna fucc nicki minaj lol")

tweeb = tweebo.Tweebo()
parsedTweets = []

for x in tweebo.parse(tweeb, text):
    parsedTweet = []
    for node in x.nodelist:
        parsedTweet.append(node)
    parsedTweets.append(parsedTweet)

f = open('myfile.json', 'w')
f.write(json.dumps(parsedTweets))
f.close()