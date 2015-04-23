__author__ = 'marc'

from pymongo import MongoClient
import re

def get_tweets(limit):
    client = MongoClient('localhost', 27017)
    db = client.activist_events

    tweets = []
    for tweet in db.whaling_events.find().limit(limit):
        tweets.append(tweet['text'])

    return tweets


def get_potential_credibility_factors(limit):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    cred_filter = {
        'id': 1,
        'text': 1,
        'favorite_count': 1,
        'retweet_count': 1,
        'source': 1,
        'user.statuses_count': 1,
        'user.friends_count': 1,
        'user.id': 1,
        'user.listed_count': 1,
        'user.followers_count': 1,
        'user.url': 1,
        'user.description': 1,
        'user.verified': 1,
        'user.created_at': 1,
        'entities.user_mentions.id': 1,
        'entities.urls.url': 1
    }

    tweets = list(db.whaling_events.find({}, cred_filter).limit(limit))

    return tweets








