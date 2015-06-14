__author__ = 'marc'

from collections import Counter
import re
import string
import unicodecsv


def add_relevance_scores(articles, weights, field_name_counts, field_name_score):
    terms = [term['term'] for term in weights]
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(terms), flags=re.IGNORECASE)

    articles = list(articles)
    for article in articles:
        if isinstance(article['body'], (list, tuple)):
            article['body'] = string.join(article['body'])
        matches = exact_match.findall(article['body'])
        matches = [match.lower() for match in matches]
        counts = Counter(matches)
        article[field_name_counts] = counts

        score = 0
        scorelist = []
        if matches:
            for word, count in counts.iteritems():
                score = [term for term in weights if str(term['term']).lower() == str(word).lower()]
                scorelist.append(float(score[0]['weight']*count))

            # todo: what number should we divide the weightscores with?
            score = sum(scorelist) / len(weights)
        article[field_name_score] = float(score)

    return articles


def get_wikiword_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    total = sum([int(word[1]) for word in words])
    terms = [{'term': unicode(row[0]).replace('_', ' '), 'weight': float(row[1])/total} for row in words]

    return terms


def get_seedwords_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    weight = float(1.0/len(words))
    weights = [{'term': unicode(row[0]), 'weight': weight} for row in words]

    return weights


def add_wiki_scores_to_articles(articles, wikiwords):
    wiki_weights = get_wikiword_weights(wikiwords)
    return add_relevance_scores(articles, wiki_weights, 'wikiwords_found', 'wikiwords_score')


def add_seedwords_scores_to_articles(articles, seedwords):
    sw_weights = get_seedwords_weights(seedwords)
    return add_relevance_scores(articles, sw_weights, 'seedwords_found', 'seedwords_score')
