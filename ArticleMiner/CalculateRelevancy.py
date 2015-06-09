__author__ = 'marc'

from Resources import Database
from Output import Mongo
from collections import Counter
import unicodecsv
import re
import string

def add_wiki_relevance_scores(articles):
    with open('Relevancy/wikiwords.csv', 'rb') as csvfile:
        reader = unicodecsv.reader(csvfile)
        words = [{'word': row[0], 'weight': row[1]} for row in reader]

    wordlist = [(unicode(word['word']).replace('_', ' ').lower()) for word in words]
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(wordlist), flags=re.IGNORECASE)

    articles = list(articles)
    for article in articles:
        if isinstance(article['content'], (list, tuple)):
            article['content'] = string.join(article['content'])
        counts = Counter(exact_match.findall(article['content']))
        article['wikiwords_found'] = counts

        word_score = 0
        if counts:
            for value in counts.iterkeys():
                try:
                    weight = [word for word in words if word['word'] == str(value).lower()]
                    word_score += int(weight[0]['weight'])
                except IndexError:
                    continue

        article['wikiwords_score'] = word_score

    return articles


def add_event_relevance_scores(articles):
    with open('Relevancy/articlewords.csv', 'rb') as csvfile:
        reader = unicodecsv.reader(csvfile, delimiter='\t')
        words = [{'word': row[0], 'weight': row[1]} for row in reader]

    wordlist = [(unicode(word['word']).replace('_', ' ')) for word in words]
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(wordlist), flags=re.IGNORECASE)

    articles = list(articles)
    for article in articles:
        if isinstance(article['content'], (list, tuple)):
            article['content'] = string.join(article['content'])
        counts = Counter(exact_match.findall(article['content']))
        article['eventwords_found'] = counts

        event_score = 0.0
        if counts:
            for value in counts:
                try:
                    weight = [word['weight'] for word in words if word['word'] == value][0]
                    event_score += float(weight)
                except IndexError:
                    continue

        article['eventwords_score'] = event_score

    return articles


def add_sw_relevance_scores(articles):
    with open('Relevancy/seedwords.csv', 'rb') as csvfile:
        reader = unicodecsv.reader(csvfile)
        seedwords = [row[0] for row in reader]

    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(seedwords), flags=re.IGNORECASE)

    articles = list(articles)
    for article in articles:
        if isinstance(article['content'], (list, tuple)):
            article['content'] = string.join(article['content'])
        counts = Counter(exact_match.findall(article['content']))
        article['seedwords_found'] = counts

        seedword_count = 0
        if counts:
            for count in counts.itervalues():
                seedword_count += int(count)

        article['seedwords_score'] = seedword_count

    return articles

# whaling_articles = Database.get_all_documents('activist_events', 'whaling_articles', 'publication_date')
# docs = add_sw_relevance_scores(whaling_articles)
# docs = add_wiki_relevance_scores(docs)
# docs = add_event_relevance_scores(docs)
# Mongo.store_articles(docs, 'whaling_articles_relevancy')