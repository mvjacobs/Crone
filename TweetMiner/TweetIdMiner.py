__author__ = 'marc'

import tweepy

# Read configuration from config/twitter.cfg
lines = [line.strip() for line in open('config/twitter.cfg')]
consumer_key = lines[0]
consumer_secret = lines[1]
access_token = lines[2]
access_token_secret = lines[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

str_id = 574685555449073664
print api.get_status(str_id)
