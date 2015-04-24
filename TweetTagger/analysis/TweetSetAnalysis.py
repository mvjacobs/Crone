__author__ = 'marc'

from collections import Counter
import re

from analysis import TweetAnalysis


def get_proper_nouns(tweets):
    tweet_texts = get_tweet_texts(tweets)

    nouns = []
    for tweet_text in tweet_texts:
        nouns.append(TweetAnalysis.get_proper_nouns(tweet_text))

    return nouns


def get_proper_nouns_unique(tweets):
    return set(get_proper_nouns(tweets))


def count_proper_nouns(tweets):
    names = get_proper_nouns_unique(tweets)
    return Counter(names)


def get_tweet_texts(tweets):
    return [tweet['text'] for tweet in tweets]


def is_retweet(text):
    p = r"(RT|via)((?:\b\W*@\w+)+)"
    return bool(re.search(p, text))