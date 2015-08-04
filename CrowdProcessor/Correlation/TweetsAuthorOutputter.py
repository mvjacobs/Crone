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
    documents1 = [document for document in documents if document['morecredible'] == '1']
    features1 = get_features_articles(documents1, 1)

    documents2 = [document for document in documents if document['lesscredible'] == '1']
    features2 = get_features_articles(documents2, 2)

    all_features = features1 + features2
    grouped_features = count_features(all_features)

    return [get_header()] + grouped_features


def get_header():
    return [
        'id',
        'credible_count',
        'has_user_avatar',
        'has_user_background',
        'has_user_description',
        'user_created_at',
        'user_favourites_count',
        'user_followers_count',
        'user_friends_count',
        'user_listed_count',
        'user_statuses_count',
        'user_verified'
    ]


def get_features_articles(articles, article_number):
    features = []
    for article in articles:
        row = [
            article['id%d' % article_number],
            article['result_has_user_avatar%d' % article_number],
            article['result_has_user_background%d' % article_number],
            article['result_has_user_description%d' % article_number],
            article['result_user_created_at%d' % article_number],
            article['result_user_favourites_count%d' % article_number],
            article['result_user_followers_count%d' % article_number],
            article['result_user_friends_count%d' % article_number],
            article['result_user_listed_count%d' % article_number],
            article['result_user_statuses_count%d' % article_number],
            article['result_user_verified%d' % article_number]
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


def create_article_results_csv():
    articles = get_data_from_csv('Results/tweets_author.csv')
    articles = filter_features_articles(articles)
    write_article_to_csv(articles, 'Output/tweet_author_features.csv')


create_article_results_csv()

