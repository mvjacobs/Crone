__author__ = 'marc'

from nltk.corpus import stopwords
from BeautifulSoup import BeautifulSoup
from Analyzing import TokenAnalysis
import nltk


def get_filtered_article_text(text):
    tokens = nltk.word_tokenize(text)
    tokens_filtered = [
        token for token in tokens
        if token not in stopwords.words('english')
        and len(token) > 1
        and not TokenAnalysis.is_url(token)
    ]

    return tokens_filtered


def get_tokens_with_pos(text):
    tokens = nltk.word_tokenize(text)
    tokens_with_pos = nltk.pos_tag(tokens)

    return tokens_with_pos


def remove_html_from_article(text):
    return BeautifulSoup(text).text
