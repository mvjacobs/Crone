__author__ = 'marc'

from Utils import TfIdf
import unicodecsv


def tf_idf_wordlist_comparison(wordlist_to_compare, wordlists):
    table = TfIdf()

    for wordlist_name in wordlists:
        if wordlists[wordlist_name] != wordlist_to_compare:
            table.add_document(wordlist_name, wordlists[wordlist_name])

    return table.similarities(wordlists[wordlist_to_compare])


def tf_idf_wordlists_comparison(wordlists):

    wordlists_compared = {}
    for current_wordlist_name in wordlists:
        table = TfIdf()
        for w in wordlists:
            if w != current_wordlist_name:
                table.add_document(w, wordlists[w])

        wordlists_compared[current_wordlist_name] = table.similarities(wordlists[current_wordlist_name])

    return wordlists_compared


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


def get_wikiword_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    total = sum([int(word[1]) for word in words])
    terms = [{'term': row[0].replace('_', ' '), 'weight': float(row[1])/total} for row in words]

    return terms


def get_seedwords_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile, dialect="excel-tab"))
    weight = float(1.0/len(words))
    weights = [{'term': row[0], 'weight': weight} for row in words]

    return weights


def get_crowdwords_weights(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = list(unicodecsv.reader(csvfile))
    words = set([word[0].lower() for word in words])
    weight = float(1.0/len(words))
    weights = [{'term': row, 'weight': weight} for row in words]

    return weights


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