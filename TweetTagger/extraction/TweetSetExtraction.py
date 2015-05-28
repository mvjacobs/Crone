__author__ = 'marc'

from analysis import TweetAnalysis, TweetSetAnalysis
from filtering import TweetFilter
from utils import Tweebo
import tweepy
import time


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
        tweet[u'filtered_text'] = tokens_filtered

    return tweets


def extract_sentiment_scores(tweets):
    for tweet in tweets:
        try:
            tweet[u'sentiment'] = {}
            tweet[u'sentiment'][u'sentiwordnet'] = TweetAnalysis.calculate_tweet_sentiment(tweet['filtered_text'])
            tweet[u'sentiment'][u'happiness'] = TweetAnalysis.calculate_tweet_happiness(tweet['filtered_text'])
            tweet[u'sentiment'][u'sadness'] = TweetAnalysis.calculate_tweet_sadness(tweet['filtered_text'])
            tweet[u'sentiment'][u'emoticon_sentiment'] = TweetAnalysis.get_emoticon_sentiment(tweet['text'])
        except KeyError:
            tweet[u'sentiment'][u'sentiwordnet'] = 0
            tweet[u'sentiment'][u'happiness'] = 0
            tweet[u'sentiment'][u'sadness'] = 0
            tweet[u'sentiment'][u'emoticon_sentiment'] = 0

    return tweets


def extract_count_uppercase_characters(tweets):
    for tweet in tweets:
        tweet[u'uppercase_count'] = sum(1 for c in tweet['text'] if c.isupper())

    return tweets


def update_stats(tweet_ids):
    # Read configuration from ../config/twitter.cfg
    lines = [line.strip() for line in open('config/twitter.cfg')]
    consumer_key = lines[0]
    consumer_secret = lines[1]
    access_token = lines[2]
    access_token_secret = lines[3]

    new_tweets = []
    maximum = len(tweet_ids)
    start = 0
    if maximum <= 100:
        end = maximum
        finish = True
    else:
        end = 100
        finish = False

    while True:
        ids = [tweet_id for tweet_id in tweet_ids[start:end]]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        search = ids

        try:
            print 'looking for tweets.. start: %s end: %s max: %s' % (start, end, maximum)
            new_tweets = new_tweets + api.statuses_lookup(search, include_entities=True)
            new_tweets = [
                new_tweet for new_tweet in new_tweets
                if (new_tweet['retweet_count'] > 0 or new_tweet['favorite_count'] > 0)
            ]
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue

        if finish:
            break

        start += 100
        if (end+100) < maximum:
            end += 100
        elif (end+100) == maximum:
            end += 100
            finish = True
        else:
            end += (maximum % 100)
            finish = True

    return new_tweets




