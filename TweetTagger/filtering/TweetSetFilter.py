__author__ = 'marc'

from analysis import TweetSetAnalysis
from filtering import TweetFilter, TokenFilter


def filter_tweets(tweets):
    for tweet in tweets:
        # remove retweets
        if TweetSetAnalysis.is_retweet(tweet['text']):
            tweets.remove(tweet)
            continue

        # remove html tags from source
        tweet['source'] = TokenFilter.remove_html(tweet['source'])

    return tweets