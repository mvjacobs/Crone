__author__ = 'marc'

from analysis import TweetAnalysis, TweetSetAnalysis
from filtering import TweetFilter
from utils import Tweebo
from collections import Counter
import tweepy
import time
import re
import string
import unicodecsv


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
            # new_tweets = [
            #     new_tweet for new_tweet in new_tweets
            #     if (new_tweet['retweet_count'] > 0 or new_tweet['favorite_count'] > 0)
            # ]
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


def add_relevance_scores(tweets, weights, field_name_counts, field_name_score):
    terms = [term['term'] for term in weights]
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(terms), flags=re.IGNORECASE)

    tweets = list(tweets)
    for tweet in tweets:
        matches = exact_match.findall(tweet['text'])
        matches = [match.lower() for match in matches]
        counts = Counter(matches)
        tweet[field_name_counts] = counts

        score = 0
        scorelist = []
        if matches:
            for word, count in counts.iteritems():
                score = [term for term in weights if str(term['term']).lower() == str(word).lower()]
                scorelist.append(float(score[0]['weight']*count))

            # todo: what number should we divide the weightscores with?
            score = sum(scorelist) / len(weights)
        tweet[field_name_score] = float(score)

    return tweets


def get_wikiword_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    total = sum([int(word[1]) for word in words])
    terms = [{'term': unicode(row[0]).replace('_', ' '), 'weight': float(row[1])/total} for row in words]

    return terms


def get_seedwords_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    weight = float(1.0/len(words))
    weights = [{'term': unicode(row[0]), 'weight': weight} for row in words]

    return weights


def add_wiki_scores_to_tweets(tweets, wikiwords):
    wiki_weights = get_wikiword_weights(wikiwords)
    return add_relevance_scores(tweets, wiki_weights, 'wikiwords_found', 'wikiwords_score')


def add_seedwords_scores_to_tweets(tweets, seedwords):
    sw_weights = get_seedwords_weights(seedwords)
    return add_relevance_scores(tweets, sw_weights, 'seedwords_found', 'seedwords_score')




