__author__ = 'marc'

import json
import csv
from bson import json_util
from pymongo import MongoClient


def to_json(list_of_objects, file_path='myfile.json'):
    with open(file_path, 'wb') as outfile:
        json.dump(list_of_objects, outfile, default=json_util.default)


def create_csv_from_tweet(source_collection, limit=0):
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
    }
    where = {}
    tweets = list(db[source_collection].find(where, fields).limit(limit))

    f = csv.writer(open("test.csv", "wb+"))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["id", "tweet", "favorite_count", "retweet_count", "source", "mentions_count", "hashtags_count"])

    for tweet in tweets:
        f.writerow([
            tweet[u"id_str"],
            tweet[u"text"],
            tweet[u"favorite_count"],
            tweet[u"retweet_count"],
            tweet[u"source"],
            str(len(tweet[u'entities'][u'user_mentions'])),
            str(len(tweet[u'entities'][u'hashtags']))
        ])

create_csv_from_tweet('whaling_events_may_rt_filtered', 10)
