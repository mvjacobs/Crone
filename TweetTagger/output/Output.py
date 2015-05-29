__author__ = 'marc'

import json
import unicodecsv
from bson import json_util
from helpers import TextHelper, UrlHelper


def to_json(list_of_objects, file_path='myfile.json'):
    with open(file_path, 'wb') as outfile:
        json.dump(list_of_objects, outfile, default=json_util.default)


def create_csv_from_tweets(headers, rows, filename):
    csv = unicodecsv.writer(open(filename, "wb+"))
    csv.writerow(headers)
    for row in rows:
        csv.writerow(row)


def create_csv_for_tweet_cf_task(tweets, filename):
    headers = [
        "id1", "tweet1", "favorite_count1", "retweet_count1", "source1", "mentions_count1", "hashtags_count1", "url1",
        "id2", "tweet2", "favorite_count2", "retweet_count2", "source2", "mentions_count2", "hashtags_count2", "url2"
    ]

    rows = []
    for key in xrange(0, len(tweets), 2):
        if key < len(tweets)-1:
            tweet1 = [
                tweets[key][u"id_str"],
                TextHelper.remove_linebreaks_from_text(tweets[key][u"text"]),
                tweets[key][u"favorite_count"],
                tweets[key][u"retweet_count"],
                tweets[key][u"source"],
                str(len(tweets[key][u'entities'][u'user_mentions'])),
                str(len(tweets[key][u'entities'][u'hashtags'])),
                ' '.join([UrlHelper.unshorten_url(url[u"expanded_url"]) for url in tweets[key][u"entities"][u'urls']])
            ]

            key += 1

            tweet2 = [
                tweets[key][u"id_str"],
                TextHelper.remove_linebreaks_from_text(tweets[key][u"text"]),
                tweets[key][u"favorite_count"],
                tweets[key][u"retweet_count"],
                tweets[key][u"source"],
                str(len(tweets[key][u'entities'][u'user_mentions'])),
                str(len(tweets[key][u'entities'][u'hashtags'])),
                ' '.join([UrlHelper.unshorten_url(url[u"expanded_url"]) for url in tweets[key][u"entities"][u'urls']])
            ]

            both_tweets = tweet1 + tweet2

            rows.append(both_tweets)

    create_csv_from_tweets(headers, rows, filename)