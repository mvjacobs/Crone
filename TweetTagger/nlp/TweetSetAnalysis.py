__author__ = 'marc'

from nlp import tweebo, TokenAnalysis
from collections import Counter


def get_real_names(list_of_tweets):
    parsed_tweets = parse_tweets(list_of_tweets)

    words = []
    for tweet in parsed_tweets:
        token_analysis = TokenAnalysis.TokenAnalysis(tweet)
        words = words + token_analysis.get_names_from_tweets()

    return words


def get_real_names_unique(list_of_tweets):
    return set(get_real_names(list_of_tweets))


def count_real_names(list_of_tweets):
    names = get_real_names(list_of_tweets)
    return Counter(names)


def parse_tweets(tweets):
    tweeb = tweebo.Tweebo()
    parsed_tweets = []

    for tweet in tweebo.parse(tweeb, tweets):
        parsed_tweet = []
        for node in tweet.nodelist:
            parsed_tweet.append(node)
        parsed_tweets.append(parsed_tweet)

    return parsed_tweets