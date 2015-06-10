__author__ = 'marc'

from Resources import Database
from Output import Mongo
from collections import Counter
import unicodecsv
import re
import string

def add_relevance_scores(articles, weights, field_name_counts, field_name_score):
    terms = [term['term'] for term in weights]
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(terms), flags=re.IGNORECASE)

    articles = list(articles)
    for article in articles:
        if isinstance(article['content'], (list, tuple)):
            article['content'] = string.join(article['content'])
        matches = exact_match.findall(article['content'])
        counts = Counter(matches)
        article[field_name_counts] = counts

        word_score = 0
        if matches:
            for word in matches:
                weight = [term for term in weights if str(term['term']).lower() == str(word).lower()]
                word_score += float(weight[0]['weight'])

            # todo: what number should we divide the weightscores with?
            article[field_name_score] = float(word_score)# / float(len(matches))

    return articles


# def add_event_relevance_scores(articles):
#     with open('Relevancy/articlewords.csv', 'rb') as csvfile:
#         reader = unicodecsv.reader(csvfile, delimiter='\t')
#         words = [{'word': row[0], 'weight': row[1]} for row in reader]
#
#     wordlist = [(unicode(word['word']).replace('_', ' ')) for word in words]
#     exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(wordlist), flags=re.IGNORECASE)
#
#     articles = list(articles)
#     for article in articles:
#         if isinstance(article['content'], (list, tuple)):
#             article['content'] = string.join(article['content'])
#         counts = Counter(exact_match.findall(article['content']))
#         article['eventwords_found'] = counts
#
#         event_score = 0.0
#         if counts:
#             for value in counts:
#                 try:
#                     weight = [word['weight'] for word in words if word['word'] == value][0]
#                     event_score += float(weight)
#                 except IndexError:
#                     continue
#
#         article['eventwords_score'] = event_score
#
#     return articles


# def add_sw_relevance_scores(articles):
#     weights = get_seedwords_weights('Relevancy/seedwords.csv')
#
#     exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(weights), flags=re.IGNORECASE)
#
#     articles = list(articles)
#     for article in articles:
#         if isinstance(article['content'], (list, tuple)):
#             article['content'] = string.join(article['content'])
#         counts = Counter(exact_match.findall(article['content']))
#         article['seedwords_found'] = counts
#
#         seedword_count = 0
#         if counts:
#             for count in counts.itervalues():
#                 seedword_count += int(count)
#
#         article['seedwords_score'] = float(seedword_count) / float(total_seedwords)
#
#     return articles


def get_wikiword_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    total = sum([int(word[1]) for word in words])
    weights = [{'term': unicode(row[0]).replace('_', ' '), 'weight': float(row[1])/float(total)} for row in words]

    return weights


def get_seedwords_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    weight = float(1.0/len(words))
    weights = [{'term': unicode(row[0]), 'weight': weight} for row in words]

    return weights


whaling_articles = Database.get_all_documents('activist_events', 'whaling_articles', 'publication_date')

wiki_weights = get_wikiword_weights('Relevancy/wikiwords.csv')
docs = add_relevance_scores(whaling_articles, wiki_weights, 'wikiwords_found', 'wikiwords_score')

sw_weights = get_seedwords_weights('Relevancy/seedwords.csv')
docs = add_relevance_scores(docs, sw_weights, 'seedwords_found', 'seedwords_score')

#docs = add_event_relevance_scores(docs)
Mongo.store_articles(docs, 'whaling_articles_relevancy2')