__author__ = 'marc'

from pymongo import MongoClient
from collections import Counter
from dateutil import parser
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import random
import sys


def get_tweets(collection, limit):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    tweets = db[collection].find().limit(limit)
    return list(tweets)


def get_tweets_sorted(collection, sort, limit):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    db[collection].create_index(sort)
    tweets = db[collection].find().sort(sort).limit(limit)
    return list(tweets)


def get_tweet_ids(source_collection, limit=10):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    tweets = [tweet['id_str'] for tweet in db[source_collection].find().limit(limit)]

    return tweets


def get_cf_tweet_factors(source_collection, limit=10):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    fields = {
        'id_str': 1,
        'text': 1,
        'favorite_count': 1,
        'retweet_count': 1,
        'source': 1,
        'entities.user_mentions': 1,
        'entities.hashtags': 1,
        'entities.urls.expanded_url': 1,
    }
    where = {}
    tweets = list(db[source_collection].find(where, fields))

    if limit > 0:
        tweets = random.sample(tweets, limit)

    return tweets


def get_wenjie_tweet_factors(source_collection, limit=10):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    fields = {
        'id_str': 1,
        'text': 1,
        'created_at': 1,
        'lang': 1,
        'favorite_count': 1,
        'place': 1,
        'in_reply_to_screen_name': 1,
        'retweet_count': 1,
        'user.followers_count': 1,
        'entities.hashtags.text': 1,
        'entities.urls.expanded_url': 1,
        'entities.user_mentions.screen_name': 1,
        'entities.media.type': 1
    }
    where = {}
    tweets = list(db[source_collection].find(where, fields))

    if limit > 0:
        tweets = random.sample(tweets, limit)

    return tweets


def get_evaluation_factors(source_collection, limit=0):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    fields = {
        'id_str': 1,
        'text': 1,
        'source': 1,
        'created_at': 1,
        'possibly_sensitive': 1,

        'favorite_count': 1,
        'retweet_count': 1,

        'user.id': 1,
        'user.statuses_count': 1,
        'user.friends_count': 1,
        'user.default_profile_image': 1,
        'user.name': 1,
        'user.screen_name': 1,
        'user.favourites_count': 1,
        'user.listed_count': 1,
        'user.followers_count': 1,
        'user.url': 1,
        'user.description': 1,
        'user.verified': 1,
        'user.created_at': 1,

        'entities.user_mentions': 1,
        'entities.urls': 1,
        'entities.hashtags': 1,

        'seedwords_found': 1
    }

    where = {
        'seedwords_score': {'$gt': 0.0},
    }

    tweets = list(db[source_collection].find(where, fields).limit(limit))

    return tweets


def get_cf_factors(source_collection, limit=0):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    fields = {
        'id_str': 1,
        'text': 1,
        'favorite_count': 1,
        'retweet_count': 1,
        'source': 1,
        'user.id': 1,
        'user.statuses_count': 1,
        'user.friends_count': 1,
        'user.default_profile_image': 1,
        'user.name': 1,
        'user.screen_name': 1,
        'user.favourites_count': 1,
        'user.listed_count': 1,
        'user.followers_count': 1,
        'user.url': 1,
        'user.description': 1,
        'user.verified': 1,
        'user.created_at': 1,
        'entities.user_mentions.id': 1,
        'entities.urls.expanded_url': 1,
        'entities.hashtags.text': 1,
    }
    where = {
        'lang': 'en'
    }

    tweets = db[source_collection].find(where, fields).limit(limit)

    return list(tweets)


def create_random_sample(amount, collection):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    coll = db[collection]
    documents = list(coll.find())
    random_sample = [documents[i] for i in sorted(random.sample(xrange(len(documents)), amount))]

    return random_sample


def store_tweets(tweets, target_collection):
    client = MongoClient('localhost', 27017)
    db = client.activist_events

    for key, tweet in enumerate(tweets):
        db[target_collection].insert(tweet)
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")


def count_documents_per_day(collection):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    docs = list(db[collection].find({}, {'created_at': 1}))
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

# counts = count_documents_per_day('whaling_tweets_frank_iina')
#
# draw_histogram(counts)






