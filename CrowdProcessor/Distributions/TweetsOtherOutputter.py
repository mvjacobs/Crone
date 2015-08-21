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
        [article['sentiment140_score%d' % article_number] for article in articles if article['result_sentiment140_score%d' % article_number] == credible],
        [article['sentiwordnet_score%d' % article_number] for article in articles if article['result_sentiwordnet_score%d' % article_number] == credible],
        [article['tweet_favorite_count%d' % article_number] for article in articles if article['result_tweet_favorite_count%d' % article_number] == credible],
        [article['tweet_hashtag_count%d' % article_number] for article in articles if article['result_tweet_hashtag_count%d' % article_number] == credible],
        [article['tweet_nouns_count%d' % article_number] for article in articles if article['result_tweet_nouns_count%d' % article_number] == credible],
        [article['tweet_numerical_count%d' % article_number] for article in articles if article['result_tweet_numerical_count%d' % article_number] == credible],
        [article['tweet_punctuation_count%d' % article_number] for article in articles if article['result_tweet_punctuation_count%d' % article_number] == credible],
        [article['tweet_retweets_count%d' % article_number] for article in articles if article['result_tweet_retweets_count%d' % article_number] == credible],
        [article['tweet_uppercase_count%d' % article_number] for article in articles if article['result_tweet_uppercase_count%d' % article_number] == credible],
        [article['tweet_url_count%d' % article_number] for article in articles if article['result_tweet_url_count%d' % article_number] == credible],
        [article['tweet_user_mentions_count%d' % article_number] for article in articles if article['result_tweet_user_mentions_count%d' % article_number] == credible],
        [article['tweet_wiki_entities_count%d' % article_number] for article in articles if article['result_tweet_wiki_entities_count%d' % article_number] == credible],
        [article['tweet_word_count%d' % article_number] for article in articles if article['result_tweet_word_count%d' % article_number] == credible],
        [article['url_in_newser%d' % article_number] for article in articles if article['result_url_in_newser%d' % article_number] == credible],
        [article['url_in_newser100_%d' % article_number] for article in articles if article['result_url_in_newser100_%d' % article_number] == credible]
    ]


def create_dict(features1, features2):
    return {
        'sentiment140_score': features1[0] + features2[0],
        'sentiwordnet_score': features1[1] + features2[1],
        'favorite_count': features1[2] + features2[2],
        'hashtag_count': features1[3] + features2[3],
        'nouns_count': features1[4] + features2[4],
        'numerical_count': features1[5] + features2[5],
        'punctuation_count': features1[6] + features2[6],
        'retweets_count': features1[7] + features2[7],
        'uppercase_count': features1[8] + features2[8],
        'url_count': features1[9] + features2[9],
        'user_mentions_count': features1[10] + features2[10],
        'wiki_entities_count': features1[11] + features2[11],
        'word_count': features1[12] + features2[12],
        'url_in_newser': features1[13] + features2[13],
        'url_in_newser100': features1[14] + features2[14],
    }


def create_article_results_csv():
    articles = get_data_from_csv('../Results/tweets_other.csv')
    credible_features, non_credible_features = filter_features_articles(articles)
    write_to_json(credible_features, '../Output/dist_tweet_other_credibles.json')
    write_to_json(non_credible_features, '../Output/dist_tweet_other_non_credibles.json')

create_article_results_csv()