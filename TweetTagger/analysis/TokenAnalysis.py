__author__ = 'marc'

import re
from nltk.corpus import sentiwordnet as swn


def calculate_sentiment_score(token):
    synsets = swn.senti_synsets(token)
    if len(synsets) == 0:
        return 0

    t = synsets[0]
    positive = t.pos_score()
    negative = t.neg_score()
    objectivity = 1 - (positive + negative)

    if objectivity >= 0.5:
        return 0

    if positive > negative:
        return positive
    else:
        return -negative


def is_url(text):
    """
    https://mathiasbynens.be/demo/url-regex

    :param text:
    :return true if url, else false:
    """
    p = re.compile(ur'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
                   ur'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
                   ur'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?]))')
    return bool(re.search(p, text))
