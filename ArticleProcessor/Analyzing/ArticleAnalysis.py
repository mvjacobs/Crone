__author__ = 'marc'

from Analyzing import TokenAnalysis
import requests
import time
from Helpers import UrlHelper
import tldextract
import json
import nltk


# http://www.nltk.org/book/ch05.html
def get_proper_nouns(tokens_with_pos):
    nouns = [word for word, pos_type in tokens_with_pos if pos_type in ['NNP', 'NNPS']]

    return nouns


# http://www.nltk.org/book/ch05.html
def get_numericals(tokens_with_pos):
    numbers = [word for word, pos_type in tokens_with_pos if pos_type in ['CD']]

    return numbers


# http://www.nltk.org/book/ch05.html
def get_punctuation(tokens_with_pos):
    numbers = [word for word, pos_type in tokens_with_pos if pos_type in ['SYM', ',']]

    return numbers


def calculate_article_sentiment(tokens):
    score = 0
    for token in tokens:
        score += TokenAnalysis.calculate_sentiment_score(token)

    return score


def get_article_emoticon_sentiment(tokens):
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
    sentences = nltk.sent_tokenize(text)

    TAGME_API_KEY = [line.strip() for line in open('Config/tagme.cfg')][0]
    entities = []

    for sentence in sentences:
        parameters = {
            'key': TAGME_API_KEY,
            'text': sentence,
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


def get_emoticons_from_article(text):
    emoticons = ":-) :) :D :o) :] :3 :c) :> =] 8) =) :} :^) :-D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D :-)) >:[ :-( " \
                ":(  :-c :c :-<  :< :-[ :[ :{ ;( :-|| >:( :'-( :'( :'-) :') D:< D: D8 D; D= DX v.v D-': >:O " \
                ":-O :O :-o :o 8-0 O_O o-o O_o o_O o_o O-O :* :^* ;-) ;) *-) *) ;-] ;] ;D ;^) :-, >:P :-P :P X-P x-p " \
                "xp XP :-p :p =p :-b :b d: >:\ >:/ :-/ :-. :/ :\ =/ =\ :L =L :S >.< :| :-| :$ :-X :X :-# " \
                ":# O:-) 0:-3 0:3 0:-) 0:) 0;^) >:) >;) >:-) }:-) }:) 3:-) 3:) |;-) |-O :-J :-& :& #-) %-) %) :-###.. " \
                ":###.. <:-| \o/ *\\0/* 5:-) ~:-\ <3 </3".split(" ")

    tokens = nltk.word_tokenize(text)
    matches = [emoticon for emoticon in emoticons if emoticon in tokens]

    return matches
