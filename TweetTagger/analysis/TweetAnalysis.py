__author__ = 'marc'

from utils import DaviesSentimentAnalysis
from helpers import UrlHelper
import requests
import time
import TokenAnalysis
import tldextract
import json
import re


class RelatedNames:
    def __init__(self, list_of_tokens):
        self.tokens = list_of_tokens
        self.depth = 0

    def add_related_words(self, token_to_check):
        word = ""
        deps = token_to_check[u'deps']

        for token in self.tokens:
            if deps:
                if token[u'address'] in deps:
                    word = token[u'word'] + " " + token_to_check[u'word']
                    token[u'processed'] = "true"
                    token_to_check[u'processed'] = "true"
                    if self.depth < 4:
                        self.depth += 1
                        self.add_related_words(token)
                    else:
                        self.depth = 0
                        break
        return word

    def get_emoticons(self):
        words = [token[u'word'] for token in self.tokens if token[u'tag'] == "E"]
        return words

    def get_numericals(self):
        words = [token[u'word'] for token in self.tokens if token[u'tag'] == "$"]
        return words

    def get_punctuation(self):
        words = [token[u'word'] for token in self.tokens if token[u'tag'] == ","]
        return words

    def get_names_from_tweets(self):
        words = []

        for token in self.tokens:
            token[u'processed'] = "false"

        for token in self.tokens:
            if token[u'tag'] == "^" and token[u'deps']:
                words.append(self.add_related_words(token))

        words_without = [
            token[u'word'] for token in self.tokens
            if token[u'tag'] == "^" and token[u'processed'] == "false"
        ]

        return words + words_without


def get_proper_nouns(tweet):
    token_analysis = RelatedNames(tweet)
    words = token_analysis.get_names_from_tweets()

    return words


def get_numericals(tweet):
    token_analysis = RelatedNames(tweet)
    words = token_analysis.get_numericals()

    return words


def get_punctuation(tweet):
    token_analysis = RelatedNames(tweet)
    words = token_analysis.get_punctuation()

    return words


def get_emoticons(text):
    token_analysis = RelatedNames(text)
    words = token_analysis.get_emoticons()

    return words


def calculate_tweet_sentiment(tokens):
    score = 0
    for token in tokens:
        score += TokenAnalysis.calculate_sentiment_score(token)

    return score


def calculate_tweet_happiness(tokens):
    return DaviesSentimentAnalysis.getHappiness(tokens)


def calculate_tweet_sadness(tokens):
    return DaviesSentimentAnalysis.getSadness(tokens)


def get_emoticon_sentiment(tokens):
    positive_emoticons = [':)', ':-)', ':=)', ':D', ':-D', ':=D', '^_^', ';)', ';-)', ';=)']
    negative_emoticons = [':(', ':-(', ':=(', ":'(", ';(', ';-(', ';=(']

    score = 0
    for token in tokens:
        if token in positive_emoticons:
            score += 1
        if token in negative_emoticons:
            score -= 1

    return score


def get_wiki_entities_count(text):
    TAGME_API_KEY = [line.strip() for line in open('config/tagme.cfg')][0]
    entities = []

    parameters = {
        'key': TAGME_API_KEY,
        'text': text,
        'lang': 'en'
    }
    url = 'http://tagme.di.unipi.it/tag'

    retry = True
    retry_count = 0
    while retry:
        try:
            time.sleep(0.5)
            response = requests.get(url, params=parameters)
            response = response.json()
            retry = False
        except requests.Timeout:
            if retry_count < 9:
                retry = True
                retry_count += 1
            else:
                return []
        except:
            return []

    for annotation in response[u'annotations']:
        if float(annotation[u'rho']) > 0.1:
            entities.append({u'entity': annotation['title'], u'rho': annotation['rho']})

    return entities


def get_full_urls(urls):
    parsed_urls = []
    for url in urls:
        full_url = UrlHelper.unshorten_url(url)
        parsed_urls.append(full_url)

    return parsed_urls


def get_urls_in_newser(urls):
    with open('data/newser.json') as data_file:
        news_urls = [url['url'] for url in json.load(data_file)]

    for url in urls:
        try:
            parsed_uri = tldextract.extract(url)
            domain = '%s.%s' % (parsed_uri.domain, parsed_uri.suffix)
            if domain in news_urls:
                return 1
        except:
            continue

    return 0


def get_urls_in_newser_all(urls):
    with open('data/newser_all.json') as data_file:
        news_urls = [url['url'] for url in json.load(data_file)]

    for url in urls:
        try:
            parsed_uri = tldextract.extract(url)
            domain = '%s.%s' % (parsed_uri.domain, parsed_uri.suffix)
            if domain in news_urls:
                return 1
        except:
            continue

    return 0


def word_count(tweet):
    # Find all non-whitespace patterns.
    list = re.findall("(\S+)", tweet)
    # Return length of resulting list.
    return len(list)
