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
        'sentiment140_score',
        'sentiwordnet_score',
        'created_at',
        'favorite_count',
        'hashtag_count',
        'nouns_count',
        'numerical_count',
        'punctuation_count',
        'retweets_count',
        'uppercase_count',
        'url_count',
        'user_mentions_count',
        'wiki_entities_count',
        'word_count',
        'url_in_newser',
        'url_in_newser100'
    ]


def get_features_articles(articles, article_number):
    features = []
    for article in articles:
        row = [
            article['id%d' % article_number],
            article['sentiment140_score%d' % article_number],
            article['sentiwordnet_score%d' % article_number],
            article['tweet_created_at%d' % article_number],
            article['tweet_favorite_count%d' % article_number],
            article['tweet_hashtag_count%d' % article_number],
            article['tweet_nouns_count%d' % article_number],
            article['tweet_numerical_count%d' % article_number],
            article['tweet_punctuation_count%d' % article_number],
            article['tweet_retweets_count%d' % article_number],
            article['tweet_uppercase_count%d' % article_number],
            article['tweet_url_count%d' % article_number],
            article['tweet_user_mentions_count%d' % article_number],
            article['tweet_wiki_entities_count%d' % article_number],
            article['tweet_word_count%d' % article_number],
            article['url_in_newser%d' % article_number],
            article['url_in_newser100_%d' % article_number]
        ]
        features.append(row)

    return features


def create_article_results_csv():
    articles = get_data_from_csv('../Results/tweets_other.csv')
    credibles, noncredibles = filter_features_articles(articles)
    write_article_to_csv(credibles, '../Output/dist_tweet_other_credibles.csv')
    write_article_to_csv(noncredibles, '../Output/dist_tweet_other_non_credibles.csv')

create_article_results_csv()