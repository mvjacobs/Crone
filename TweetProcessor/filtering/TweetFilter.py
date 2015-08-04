__author__ = 'marc'

from nltk.corpus import stopwords

from analysis import TokenAnalysis
from utils import Twokenize


def get_filtered_tweet_text(tweet_text):
    tokens = Twokenize.tokenize(tweet_text)
    tokens_filtered = [
        token for token in tokens
        if token not in stopwords.words('english')
        and len(token) > 1
        and not TokenAnalysis.is_url(token)
    ]

    return tokens_filtered
