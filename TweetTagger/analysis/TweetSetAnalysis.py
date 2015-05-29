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
    return [tweet for tweet in tweets if (tweet['retweet_count'] > 0 or tweet['favorite_count'] > 0)]
