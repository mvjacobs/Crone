__author__ = 'marc'

from analysis import TweetSetAnalysis
from filtering import TokenFilter


def filter_tweets(tweets):
    # remove retweets
    filtered_tweets = [tweet for tweet in tweets if not TweetSetAnalysis.is_retweet(tweet['text'])]

    # remove html tags from source
    filtered_tweets = [remove_tags_from_source(tweet) for tweet in filtered_tweets]

    return filtered_tweets


def remove_tags_from_source(tweet):
    tweet[u'source'] = TokenFilter.remove_html(tweet[u'source'])
    return tweet