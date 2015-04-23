__author__ = 'marc'

from nltk.corpus import sentiwordnet as swn


def install():
    import nltk
    nltk.download()


def get_tweet_sentiment(tweets):
    for tweet in tweets:

        score = 0
        for token in tweet['filtered_text']:
            synsets = swn.senti_synsets(token)
            if len(synsets) == 0:
                continue

            t = synsets[0]
            positive = t.pos_score()
            negative = t.neg_score()
            objectivity = 1 - (positive + negative)

            if objectivity >= 0.5:
                continue

            if positive > negative:
                score += positive
            else:
                score += -negative

        tweet['sentiwordnet'] = score

    return tweets


def get_tweet_emoticon_sentiment(text):
    return text

