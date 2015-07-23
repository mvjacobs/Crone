__author__ = 'marc'

import unicodecsv
from itertools import groupby
from operator import itemgetter


def get_data_from_csv(path_to_csv):
    csvfile = open(path_to_csv, 'r')
    return list(unicodecsv.DictReader(csvfile))


def write_article_to_csv(articles, path_to_csv):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)

        for article in articles:
            a.writerow(article)


def filter_features_articles(documents):
    output = [get_header()]

    documents1 = [document for document in documents if document['morecredible'] == '1']
    features1 = get_features_articles(documents1, 1)

    documents2 = [document for document in documents if document['lesscredible'] == '1']
    features2 = get_features_articles(documents2, 2)

    all_features = features1 + features2

    grouped_features = count_features(all_features)

    output += grouped_features

    return output


def get_header():
    return [
        'id',
        'credible_count',
        'comments_count',
        'keywords_count',
        'nouns_count',
        'numerical_count',
        'publication_date',
        'punctuation_count',
        'uppercase_count',
        'entities_count',
        'word_count',
        'sentiment_count'
    ]


def get_features_articles(articles, article_number):
    features = []
    for article in articles:
        row = [
            article['id%d' % article_number],
            article['result_article_comments_count%d' % article_number],
            article['result_article_keywords_count%d' % article_number],
            article['result_article_nouns_count%d' % article_number],
            article['result_article_numerical_count%d' % article_number],
            article['result_article_publication_date%d' % article_number],
            article['result_article_punctuation_count%d' % article_number],
            article['result_article_uppercase_count%d' % article_number],
            article['result_article_wiki_entities_count%d' % article_number],
            article['result_article_word_count%d' % article_number],
            article['result_sentiment%d' % article_number]
        ]
        features.append(row)

    return features


def count_features(articles):
    out = []
    sorted_input = sorted(articles, key=itemgetter(0))
    for id, vectors in groupby(sorted_input, key=itemgetter(0)):
        feature_vectors = [vector[1:] for vector in vectors]
        credible_count = len(feature_vectors)
        for key1, features in enumerate(feature_vectors):
            for key2, feature in enumerate(features):
                feature_vectors[key1][key2] = int(feature)

        feature_totals = [ sum(x) for x in zip(*feature_vectors) ]
        out.append([id] + [credible_count] + feature_totals)

    return out


articles = get_data_from_csv('Results/articles.csv')
articles = filter_features_articles(articles)
write_article_to_csv(articles, 'Output/articles_features.csv')

