__author__ = 'marc'

from analysis import TweetSetAnalysis
from filtering import TokenFilter


def filter_tweets(tweets):
    # remove retweets
    filtered_tweets = [tweet for tweet in tweets if not TweetSetAnalysis.is_retweet(tweet['text'])]

    # remove html tags from source
    #filtered_tweets = [remove_tags_from_source(tweet) for tweet in filtered_tweets]

    return filtered_tweets


def remove_tags_from_source(tweet):
    tweet[u'source'] = TokenFilter.remove_html(tweet[u'source'])
    return tweet


def remove_tweets_without_retweets_or_likes(tweets):
    return TweetSetAnalysis.is_retweeted_or_liked(tweets)


def remove_duplicates(tweets, field):
    results = []

    for article in tweets:
        if not results:
            results.append(article)
        if article[field] not in [result[field] for result in results]:
            results.append(article)

    return results
