__author__ = 'marc'

from Analyzing import RankingWordLists
from collections import Counter
from operator import itemgetter
import unicodecsv
from dateutil import parser
import re

def create_dataset_overlap_matrix():
    wordLists = RankingWordLists.get_ranking_word_lists()
    results = {}
    blacklist = []

    csv = unicodecsv.writer(open('wordsoverlap.csv', "wb+"))
    csv.writerow(['set1', 'set1_size', 'set2', 'set2_size', 'matches_count', 'overlap'])

    for name in wordLists:
        spans = set([span.lower() for span in wordLists[name]])
        otherWordLists = [wordList for wordList in wordLists if (wordList is not name) and (wordList not in blacklist)]

        results[name] = []
        for otherWordListName in otherWordLists:
            otherSpans = set([otherSpan.lower() for otherSpan in wordLists[otherWordListName]])
            matches = [span for span in otherSpans if span in spans]
            results[name].append({otherWordListName: matches})
            csv.writerow([name, len(spans), otherWordListName, len(otherSpans), len(matches), ', '.join(matches)])
        blacklist.append(name)


def create_tweet_overlap_per_entity_type(seedwords, tweets):
    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(seedwords), flags=re.IGNORECASE)
    tweets_glued = ' '.join([tweet[0] for tweet in tweets])
    matches = exact_match.findall(tweets_glued)
    matches = [match.lower() for match in matches]
    counted_entities = Counter(matches)

    return counted_entities


def _get_seedwords():
    with open('WordLists/seedwords.csv', 'rb') as csvfile:
        words = [word[0] for word in unicodecsv.reader(csvfile, dialect="excel-tab")]
    return  words


def _get_tweets(year=None):
    with open('Corpora/tweets.csv', 'rb') as csvfile:
        words = [word for word in unicodecsv.reader(csvfile)]
    if year:
        for word in words:
            word.append(parser.parse(word[1]).year)
        words = [word for word in words if word[2] == year]
    return sorted(words, key=itemgetter(1), reverse=True)

seedwords = _get_seedwords()

tweets = _get_tweets()
print create_tweet_overlap_per_entity_type(seedwords, tweets)
print
tweets = _get_tweets(2014)
print create_tweet_overlap_per_entity_type(seedwords, tweets)
print
tweets = _get_tweets(2015)
print create_tweet_overlap_per_entity_type(seedwords, tweets)

