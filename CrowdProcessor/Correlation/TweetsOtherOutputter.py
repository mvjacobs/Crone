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
            article['result_sentiment140_score%d' % article_number],
            article['result_sentiwordnet_score%d' % article_number],
            article['result_tweet_created_at%d' % article_number],
            article['result_tweet_favorite_count%d' % article_number],
            article['result_tweet_hashtag_count%d' % article_number],
            article['result_tweet_nouns_count%d' % article_number],
            article['result_tweet_numerical_count%d' % article_number],
            article['result_tweet_punctuation_count%d' % article_number],
            article['result_tweet_retweets_count%d' % article_number],
            article['result_tweet_uppercase_count%d' % article_number],
            article['result_tweet_url_count%d' % article_number],
            article['result_tweet_user_mentions_count%d' % article_number],
            article['result_tweet_wiki_entities_count%d' % article_number],
            article['result_tweet_word_count%d' % article_number],
            article['result_url_in_newser%d' % article_number],
            article['result_url_in_newser100_%d' % article_number]
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
    articles = get_data_from_csv('Results/tweets_other.csv')
    articles = filter_features_articles(articles)
    write_article_to_csv(articles, 'Output/tweet_other_features.csv')

create_article_results_csv()