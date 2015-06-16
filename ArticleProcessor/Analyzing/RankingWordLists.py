__author__ = 'marc'

import unicodecsv

def get_ranking_word_lists():
    seedwords = _get_words('WordLists/seedwords.csv')
    article_topics = _get_topic_list()
    wiki_words = _get_words('WordLists/wikiwords.csv')
    annotated_words = _get_words('WordLists/annotatedwords.csv')
    tweets = _get_words('WordLists/tweets.csv')
    tweets2015 = _get_words('WordLists/tweets2015.csv')

    word_lists = {
        'seedwords': seedwords,
        'article_topics': article_topics,
        'wiki_words': wiki_words,
        'annotated_words': annotated_words,
        'tweets': tweets,
        'tweets2015': tweets2015
    }

    return word_lists


def _get_words(path_to_csv, column=0, dialect=None):
    with open(path_to_csv, 'rb') as csvfile:
        words = []
        if dialect == 'tsv':
            for word in unicodecsv.reader(csvfile, dialect="excel-tab"):
                words.append(word[column].strip())
        else:
            for word in unicodecsv.reader(csvfile):
                words.append(word[column].strip())
    return set(words)


def _get_topic_list():
    topics = _get_words('WordLists/topics.csv', 2, 'tsv')
    topic_words = []
    for topic in topics:
        for word in topic.split(' '):
            topic_words.append(word)
    return set(topic_words)