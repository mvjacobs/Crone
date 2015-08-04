__author__ = 'marc'

from collections import Counter
import re
import urllib2
import json
from analysis import TweetAnalysis


def get_proper_nouns(tweets):
    tweet_texts = get_tweet_texts(tweets)

    nouns = []
    for tweet_text in tweet_texts:
        nouns.append(TweetAnalysis.get_proper_nouns(tweet_text))

    return nouns


def get_proper_nouns_unique(tweets):
    return set(get_proper_nouns(tweets))


def get_full_urls(tweets):
    urls = []
    for tweet in tweets:
        urls = TweetAnalysis.get_full_urls(tweet[u"entities"][u'urls'][u'expanded_url'])

    return urls


def count_proper_nouns(tweets):
    names = get_proper_nouns_unique(tweets)
    return Counter(names)


def get_tweet_texts(tweets):
    return [tweet[u'text'] for tweet in tweets]


def is_retweet(text):
    f1 = bool(re.search(r"(RT|via)((?:\b\W*@\w+)+)", text))
    f2 = bool(re.search(r"RT @", text))
    f3 = bool(re.search(r"MT @", text))
    f4 = bool(re.search(r"^(@\w *)+", text))
    f5 = bool(re.search(r"^@", text))
    f6 = bool(re.search(r"\n{3,}", text))
    f7 = bool(re.search(r"^.@", text))
    f8 = bool(re.search(r"(rt|mt)", text))

    return f1 or f2 or f3 or f4 or f5 or f6 or f7 or f8


def is_retweeted_or_liked(tweets):
    return [tweet for tweet in tweets if (tweet[u'retweet_count'] > 0 or tweet[u'favorite_count'] > 0)]


def calculate_tweet140_sentiment(tweets):
    url = 'http://www.sentiment140.com/api/bulkClassifyJson?jacobsmv@gmail.com'
    texts = [{'text': ' '.join(tweet['filtered_text']), 'id':tweet['id_str']} for tweet in tweets]
    data = '{"data": %s}' % json.dumps(texts)
    response = urllib2.urlopen(url, data)
    sentiments = json.loads(unicode(response.read(), 'latin-1'))

    for sentiment in sentiments['data']:
        for tweet in tweets:
            if sentiment['id'] == tweet['id_str']:
                tweet['sentiment']['sentiment140'] = sentiment['polarity']

    return tweets
