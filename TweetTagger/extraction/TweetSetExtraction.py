__author__ = 'marc'

from analysis import TweetAnalysis, TweetSetAnalysis
from filtering import TweetFilter
from utils import Tweebo


def extract_proper_nouns(tweets):
    tweet_texts = TweetSetAnalysis.get_tweet_texts(tweets)
    i = 0
    for tweet_text in tweet_texts:
        tweets[i]['proper_nouns'] = TweetAnalysis.get_proper_nouns(tweet_text)
        i += 1

    return tweets


def extract_proper_nouns_unique(tweets):
    tweet_texts = TweetSetAnalysis.get_tweet_texts(tweets)
    i = 0
    for tweet_text in tweet_texts:
        tweets[i]['proper_nouns'] = TweetAnalysis.get_proper_nouns(tweet_text)
        i += 1

    return set(tweets)


def extract_word_types_and_relations(tweets):
    tweeb = Tweebo.Tweebo()
    tweet_texts = TweetSetAnalysis.get_tweet_texts(tweets)

    i = 0
    for parsed_tweet in Tweebo.parse(tweeb, tweet_texts):
        tweets[i]['nlp'] = parsed_tweet.nodelist
        i += 1

    return tweets


def extract_filtered_tokens(tweets):
    for tweet in tweets:
        tokens_filtered = TweetFilter.get_filtered_tweet_text(tweet['text'])
        tweet['filtered_text'] = tokens_filtered

    return tweets


def extract_sentiment_scores(tweets):
    for tweet in tweets:
        try:
            tweet['sentiwordnet'] = TweetAnalysis.calculate_tweet_sentiment(tweet['filtered_text'])
        except KeyError:
            tweet['sentiwordnet'] = 0

    return tweets





