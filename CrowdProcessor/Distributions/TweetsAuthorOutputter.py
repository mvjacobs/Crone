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
    credible_features = get_features_articles(documents1, 1)
    non_credible_features = get_features_articles(documents1, 2)

    documents2 = [document for document in documents if document['lesscredible'] == '1']
    non_credible_features += get_features_articles(documents2, 1)
    credible_features += get_features_articles(documents2, 2)

    documents3 = [document for document in documents if document['same'] == '1']
    non_credible_features += get_features_articles(documents3, 1)
    non_credible_features += get_features_articles(documents3, 2)

    return ([get_header()] + credible_features, [get_header()] + non_credible_features)


def get_header():
    return [
        'id',
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
            article['has_user_avatar%d' % article_number],
            article['has_user_background%d' % article_number],
            article['has_user_description%d' % article_number],
            article['user_created_at%d' % article_number],
            article['user_favourites_count%d' % article_number],
            article['user_followers_count%d' % article_number],
            article['user_friends_count%d' % article_number],
            article['user_listed_count%d' % article_number],
            article['user_statuses_count%d' % article_number],
            article['user_is_verified%d' % article_number]
        ]
        features.append(row)

    return features


def create_article_results_csv():
    articles = get_data_from_csv('../Results/tweets_author.csv')
    credibles, noncredibles = filter_features_articles(articles)
    write_article_to_csv(credibles, '../Output/dist_tweet_author_credibles.csv')
    write_article_to_csv(noncredibles, '../Output/dist_tweet_author_non_credibles.csv')

create_article_results_csv()

