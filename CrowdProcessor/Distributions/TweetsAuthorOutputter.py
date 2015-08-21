__author__ = 'marc'

import unicodecsv
import json


def get_data_from_csv(path_to_csv):
    csvfile = open(path_to_csv, 'r')
    return list(unicodecsv.DictReader(csvfile))


def write_to_json(dict, path_to_json):
    with open(path_to_json, 'w') as outfile:
        json.dump(dict, outfile)


def filter_features_articles(documents):
    documents1 = [document for document in documents if document['morecredible'] == '1']
    documents2 = [document for document in documents if document['lesscredible'] == '1']

    credible_features1 = get_features_articles(documents1, 1)
    credible_features2 = get_features_articles(documents2, 2)
    credible_dict = create_dict(credible_features1, credible_features2)

    non_credible_features1 = get_features_articles(documents1, 1, '0')
    non_credible_features2 = get_features_articles(documents2, 2, '0')
    non_credible_dict = create_dict(non_credible_features1, non_credible_features2)

    return credible_dict, non_credible_dict


def get_features_articles(articles, article_number, credible='1'):
    return [
        [article['has_user_avatar%d' % article_number] for article in articles if article['result_has_user_avatar%d' % article_number] == credible],
        [article['has_user_background%d' % article_number] for article in articles if article['result_has_user_background%d' % article_number] == credible],
        [article['has_user_description%d' % article_number] for article in articles if article['result_has_user_description%d' % article_number] == credible],
        [article['user_favourites_count%d' % article_number] for article in articles if article['result_user_favourites_count%d' % article_number] == credible],
        [article['user_followers_count%d' % article_number] for article in articles if article['result_user_followers_count%d' % article_number] == credible],
        [article['user_friends_count%d' % article_number] for article in articles if article['result_user_friends_count%d' % article_number] == credible],
        [article['user_listed_count%d' % article_number] for article in articles if article['result_user_listed_count%d' % article_number] == credible],
        [article['user_statuses_count%d' % article_number] for article in articles if article['result_user_statuses_count%d' % article_number] == credible],
        [article['user_is_verified%d' % article_number] for article in articles if article['result_user_verified%d' % article_number] == credible]
    ]


def create_dict(features1, features2):
    return {
        'has_user_avatar': features1[0] + features2[0],
        'has_user_background': features1[1] + features2[1],
        'has_user_description': features1[2] + features2[2],
        'user_favourites_count': features1[3] + features2[3],
        'user_followers_count': features1[4] + features2[4],
        'user_friends_count': features1[5] + features2[5],
        'user_listed_count': features1[6] + features2[6],
        'user_statuses_count': features1[7] + features2[7],
        'user_verified': features1[8] + features2[8]
    }


def create_article_results_csv():
    articles = get_data_from_csv('../Results/tweets_author.csv')
    credible_features, non_credible_features = filter_features_articles(articles)
    write_to_json(credible_features, '../Output/dist_tweet_author_credibles.json')
    write_to_json(non_credible_features, '../Output/dist_tweet_author_non_credibles.json')

create_article_results_csv()

