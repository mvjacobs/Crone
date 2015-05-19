__author__ = 'marc'

import twitter

# Read configuration from config/twitter.cfg
lines = [line.strip() for line in open('config/twitter.cfg')]
consumer_key = lines[0]
consumer_secret = lines[1]
access_token = lines[2]
access_token_secret = lines[3]

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token,
    access_token_secret=access_token_secret
)

str_id = 574685555449073664
print api.GetStatus(str_id)
