__author__ = 'marc'

from analysis import Tweebo, TokenAnalysis
from collections import Counter
from nltk.corpus import stopwords
from analysis import Twokenize


def get_real_names(list_of_tweets):
    parsed_tweets = get_word_types_and_relations(list_of_tweets)

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


def get_word_types_and_relations(tweets):
    tweeb = Tweebo.Tweebo()

    i = 0
    for parsed_tweet in Tweebo.parse(tweeb, [tweet['text'] for tweet in tweets]):
        tweets[i]['nlp'] = parsed_tweet.nodelist
        i += 1
    return tweets


def remove_stop_words(list_of_tweets):
    for tweet in list_of_tweets:
        tokens = Twokenize.simpleTokenize(tweet['text'])
        tokens_filtered = [
            token for token in tokens
            if token not in stopwords.words('english')
            and len(token) > 1
            and not TokenAnalysis.is_url(token)
        ]

        tweet['filtered_text'] = tokens_filtered

    return list_of_tweets
