__author__ = 'marc'

from pymongo import MongoClient
from random import randint
from collections import Counter
from dateutil import parser
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


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


def create_random_sample(amount):
    client = MongoClient('localhost', 27017)
    db = client.activist_events

    tweets = []
    max_count = db.whaling_events.count()

    for i in range(1, amount):
        tweets.append(list(db.whaling_events.find().limit(-1).skip(randint(1, max_count))))

    return tweets


def count_documents_per_day():
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    docs = list(db.whaling_events_new.find({}, {'created_at': 1}))
    tweets = [parser.parse(tweet['created_at']).date() for tweet in docs]
    counts = sorted(Counter(tweets).items())

    return counts


def draw_histogram(freq_list):
    x = [value[0] for value in freq_list]
    y = [value[1] for value in freq_list]

    ax = plt.subplot(111)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    ax.grid(True)
    ax.bar(x, y, width=1)
    ax.xaxis_date()

    plt.show()


draw_histogram(count_documents_per_day())






