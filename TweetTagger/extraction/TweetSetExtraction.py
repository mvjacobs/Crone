__author__ = 'marc'

from analysis import TweetAnalysis, TweetSetAnalysis
from filtering import TweetFilter
from utils import Tweebo
from collections import Counter
import tweepy
import time
import re
import unicodecsv
import sys


def extract_proper_nouns(tweets):
    for key, tweet in enumerate(tweets):
        nouns = TweetAnalysis.get_proper_nouns(tweet[u'nlp'])
        tweet[u'proper_nouns'] = nouns
        tweet[u'proper_nouns_count'] = len(nouns)
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_emoticons(tweets):
    for key, tweet in enumerate(tweets):
        emoticons = TweetAnalysis.get_emoticons(tweet[u'nlp'])
        tweet[u'emoticons'] = emoticons
        tweet[u'emoticons_count'] = len(emoticons)
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_numericals(tweets):
    for key, tweet in enumerate(tweets):
        numericals = TweetAnalysis.get_numericals(tweet[u'nlp'])
        tweet[u'numerical_mentions'] = numericals
        tweet[u'numerical_count'] = len(numericals)
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_punctuations(tweets):
    for key, tweet in enumerate(tweets):
        punctuations = TweetAnalysis.get_punctuation(tweet[u'nlp'])
        tweet[u'punctuations'] = punctuations
        tweet[u'punctuation_count'] = len(punctuations)
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_full_urls(tweets):
    for key, tweet in enumerate(tweets):
        tweet[u'full_urls'] = TweetAnalysis.get_full_urls([t[u'expanded_url'] for t in tweet[u"entities"][u'urls']])
        tweet[u'newser_top100'] = TweetAnalysis.get_urls_in_newser(tweet[u'full_urls'])
        tweet[u'newser_all'] = TweetAnalysis.get_urls_in_newser_all(tweet[u'full_urls'])
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")
    return tweets


def extract_word_types_and_relations(tweets):
    tweeb = Tweebo.Tweebo()
    tweet_texts = TweetSetAnalysis.get_tweet_texts(tweets)
    tweet_texts = [text.replace("\n", "") for text in tweet_texts]
    tweet_texts = [text.replace("\r", "") for text in tweet_texts]

    for key, parsed_tweet in enumerate(Tweebo.parse(tweeb, tweet_texts)):
        tweets[key][u'nlp'] = parsed_tweet.nodelist
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_filtered_tokens(tweets):
    for key, tweet in enumerate(tweets):
        tokens_filtered = TweetFilter.get_filtered_tweet_text(tweet[u'text'])
        tweet[u'filtered_text'] = tokens_filtered
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_wiki_entities(tweets):
    for key, tweet in enumerate(tweets):
        entities = TweetAnalysis.get_wiki_entities_count(tweet[u'text'])
        tweet[u'wiki_entities'] = entities
        tweet[u'wiki_entities_count'] = len(entities)
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_sentiment_scores(tweets):
    for key, tweet in enumerate(tweets):
        tweet[u'sentiment'] = {}
        try:
            tweet[u'sentiment'][u'sentiwordnet'] = TweetAnalysis.calculate_tweet_sentiment(tweet['filtered_text'])
        except KeyError:
            tweet[u'sentiment'][u'sentiwordnet'] = 0

        # try:
        #     tweet[u'sentiment'][u'happiness'] = TweetAnalysis.calculate_tweet_happiness(tweet['filtered_text'])
        # except KeyError:
        #     tweet[u'sentiment'][u'happiness'] = 0
        #
        # try:
        #     tweet[u'sentiment'][u'sadness'] = TweetAnalysis.calculate_tweet_sadness(tweet['filtered_text'])
        # except KeyError:
        #     tweet[u'sentiment'][u'sadness'] = 0
        #
        # try:
        #     tweet[u'sentiment'][u'emoticon_sentiment'] = TweetAnalysis.get_emoticon_sentiment(tweet['filtered_text'])
        # except KeyError:
        #     tweet[u'sentiment'][u'emoticon_sentiment'] = 0

        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    tweets = TweetSetAnalysis.calculate_tweet140_sentiment(tweets)

    return tweets


def extract_count_uppercase_characters(tweets):
    for key, tweet in enumerate(tweets):
        tweet[u'uppercase_count'] = sum(1 for c in tweet['text'] if c.isupper())
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_count_words(tweets):
    for key, tweet in enumerate(tweets):
        tweet[u'word_count'] = TweetAnalysis.word_count(tweet[u'text'])
        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return tweets


def extract_boolean_metrics(tweets):
    for key, tweet in enumerate(tweets):
        tweet[u'completeness'] = {}
        tweet[u'completeness'][u'has_user_description'] = int(bool(tweet[u'user'][u'description']))
        tweet[u'completeness'][u'has_user_url'] = int(bool(tweet[u'user'][u'url']))
        tweet[u'completeness'][u'has_user_avatar'] = int(not tweet[u'user'][u'default_profile_image'])
        tweet[u'completeness'][u'has_user_background'] = int(tweet[u'user'][u'profile_use_background_image'])
        tweet[u'completeness'][u'user_is_verified'] = int(tweet[u'user'][u'verified'])
        tweet[u'completeness'][u'url_in_newser100'] = int(tweet[u'newser_top100'])
        tweet[u'completeness'][u'url_in_newser'] = int(tweet[u'newser_all'])

        tweet[u'counts'] = {}
        tweet[u'counts'][u'user_statuses_count'] = tweet[u'user'][u'statuses_count']
        tweet[u'counts'][u'user_friends_count'] = tweet[u'user'][u'friends_count']
        tweet[u'counts'][u'user_favourites_count'] = tweet[u'user'][u'favourites_count']
        tweet[u'counts'][u'user_listed_count'] = tweet[u'user'][u'listed_count']
        tweet[u'counts'][u'user_followers_count'] = tweet[u'user'][u'followers_count']
        tweet[u'counts'][u'tweet_nouns_count'] = tweet[u'proper_nouns_count']
        tweet[u'counts'][u'tweet_numerical_count'] = tweet[u'numerical_count']
        tweet[u'counts'][u'tweet_favorite_count'] = tweet[u'favorite_count']
        tweet[u'counts'][u'tweet_user_mentions_count'] = len(tweet[u'entities'][u'user_mentions'])
        tweet[u'counts'][u'tweet_url_count'] = len(tweet[u'entities'][u'urls'])
        tweet[u'counts'][u'tweet_hashtag_count'] = len(tweet[u'entities'][u'hashtags'])
        #tweet[u'counts'][u'tweet_emoticons_count'] = tweet[u'emoticons_count']
        tweet[u'counts'][u'tweet_retweets_count'] = tweet[u'retweet_count']
        tweet[u'counts'][u'tweet_wiki_entities_count'] = tweet[u'wiki_entities_count']
        tweet[u'counts'][u'tweet_uppercase_count'] = tweet[u'uppercase_count']
        tweet[u'counts'][u'tweet_punctuation_count'] = tweet[u'punctuation_count']
        tweet[u'counts'][u'tweet_word_count'] = tweet[u'word_count']

        tweet[u'dates'] = {}
        tweet[u'dates'][u'user_created_at'] = tweet[u'user'][u'created_at']
        tweet[u'dates'][u'tweet_created_at'] = tweet[u'created_at']

        sys.stdout.write("\r%d of %d" % (key, len(tweets)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

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
    terms = [term[u'term'] for term in weights]
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(terms), flags=re.IGNORECASE)

    tweets = list(tweets)
    for tweet in tweets:
        matches = exact_match.findall(tweet[u'text'])
        matches = [match.lower() for match in matches]
        counts = Counter(matches)
        tweet[field_name_counts] = counts

        score = 0
        scorelist = []
        if matches:
            for word, count in counts.iteritems():
                score = [term for term in weights if str(term[u'term']).lower() == str(word).lower()]
                scorelist.append(float(score[0][u'weight']*count))

            # todo: what number should we divide the weightscores with?
            score = sum(scorelist) / len(weights)
        tweet[field_name_score] = float(score)

    return tweets


def get_wikiword_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    total = sum([int(word[1]) for word in words])
    terms = [{u'term': unicode(row[0]).replace('_', ' '), u'weight': float(row[1])/total} for row in words]

    return terms


def get_seedwords_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    weight = float(1.0/len(words))
    terms = [{u'term': unicode(row[0]), u'weight': weight} for row in words]

    return terms


def _get_crowd2015words():
    with open('WordLists/crowd2015.csv', 'rb') as csvfile:
        words = [re.escape(word[1]).lower() for word in unicodecsv.reader(csvfile)]
    weight = float(1.0/len(words))
    terms = [{u'term': unicode(row[0]), u'weight': weight} for row in words]

    return terms


def add_wiki_scores_to_tweets(tweets, wikiwords):
    wiki_weights = get_wikiword_weights(wikiwords)
    return add_relevance_scores(tweets, wiki_weights, u'wikiwords_found', u'wikiwords_score')


def add_seedwords_scores_to_tweets(tweets, seedwords):
    sw_weights = get_seedwords_weights(seedwords)
    return add_relevance_scores(tweets, sw_weights, u'seedwords_found', u'seedwords_score')




