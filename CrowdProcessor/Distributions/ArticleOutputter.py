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
    comments = [article['article_comments_count%d' % article_number] for article in articles if article['result_article_comments_count%d' % article_number] == credible]
    keywords = [article['article_keywords_count%d' % article_number] for article in articles if article['result_article_keywords_count%d' % article_number] == credible]
    nouns = [article['article_nouns_count%d' % article_number] for article in articles if article['result_article_nouns_count%d' % article_number] == credible]
    numbers = [article['article_numerical_count%d' % article_number] for article in articles if article['result_article_numerical_count%d' % article_number] == credible]
    punctuations = [article['article_punctuation_count%d' % article_number] for article in articles if article['result_article_punctuation_count%d' % article_number] == credible]
    uppercases = [article['article_uppercase_count%d' % article_number] for article in articles if article['result_article_uppercase_count%d' % article_number] == credible]
    entities = [article['article_wiki_entities_count%d' % article_number] for article in articles if article['result_article_wiki_entities_count%d' % article_number] == credible]
    words = [article['article_word_count%d' % article_number] for article in articles if article['result_article_word_count%d' % article_number] == credible]
    sentiments = [article['sentiment%d' % article_number] for article in articles if article['result_sentiment%d' % article_number] == credible]

    return [comments, keywords, nouns, numbers, punctuations, uppercases, entities, words, sentiments]


def create_dict(features1, features2):
    return {
        'comments_count': features1[0] + features2[0],
        'keywords_count': features1[1] + features2[1],
        'nouns_count': features1[2] + features2[2],
        'numerical_count': features1[3] + features2[3],
        'punctuation_count': features1[4] + features2[4],
        'uppercase_count': features1[5] + features2[5],
        'entities_count': features1[6] + features2[6],
        'word_count': features1[7] + features2[7],
        'sentiment_score': features1[8] + features2[8]
    }


def create_article_results_csv():
    articles = get_data_from_csv('../Results/articles.csv')
    credible_features, non_credible_features = filter_features_articles(articles)
    write_to_json(credible_features, '../Output/dist_articles_credibles.json')
    write_to_json(non_credible_features, '../Output/dist_articles_non_credibles.json')

create_article_results_csv()