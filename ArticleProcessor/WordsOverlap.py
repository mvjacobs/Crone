__author__ = 'marc'

from Analyzing import RankingWordLists
from collections import Counter
import unicodecsv
from dateutil import parser
from Resources import Database
from operator import itemgetter
from itertools import groupby
import re

def create_dataset_overlap_matrix():
    word_lists = RankingWordLists.get_ranking_word_lists()
    results = {}
    blacklist = []

    csv = unicodecsv.writer(open('wordsoverlap_tweets.csv', "wb+"))
    csv.writerow(['set1', 'set1_size', 'set2', 'set2_size', 'matches_count', 'overlap'])

    for name in word_lists:
        spans = set([span.lower() for span in word_lists[name]])
        otherWordLists = [wordList for wordList in word_lists if (wordList is not name) and (wordList not in blacklist)]

        results[name] = []
        for otherWordListName in otherWordLists:
            otherSpans = set([otherSpan.lower() for otherSpan in word_lists[otherWordListName]])
            matches = [span for span in otherSpans if span in spans]
            results[name].append({otherWordListName: matches})
            csv.writerow([name, len(spans), otherWordListName, len(otherSpans), len(matches), ', '.join(matches)])
        blacklist.append(name)


def create_tweet_overlap_per_entity_type(seedwords, texts):
    tweets_glued = ' '.join([text for text in texts])
    matches = []
    for seedword in seedwords:
        exact_match = re.compile(r'\b%s\b' % seedword, flags=re.IGNORECASE)
        search = exact_match.findall(tweets_glued)
        if search:
            matches += search
    matches = [match.lower() for match in matches]
    counted_entities = Counter(matches)
    return sorted(dict(counted_entities).items(), key=itemgetter(1), reverse=True)


def _get_seedwords():
    with open('WordLists/seedwords.csv', 'rb') as csvfile:
        words = [word[0] for word in unicodecsv.reader(csvfile, dialect="excel-tab")]
    return words

def _get_wikiwords():
    with open('WordLists/wikiwords.csv', 'rb') as csvfile:
        words = [word[0] for word in unicodecsv.reader(csvfile)]
    return words

def _get_crowd2015words():
    with open('WordLists/crowd2015.csv', 'rb') as csvfile:
        words = [re.escape(word[1]).lower() for word in unicodecsv.reader(csvfile)]
    return set(words)

def _get_crowd2014words():
    with open('WordLists/crowd2014.csv', 'rb') as csvfile:
        words = [re.escape(word[1]).lower() for word in unicodecsv.reader(csvfile)]
    return set(words)


def _get_tweets(year=None):
    with open('Corpora/tweets.csv', 'rb') as csvfile:
        tweets = list(unicodecsv.reader(csvfile))
    if year:
        for tweet in tweets:
            tweet.append(parser.parse(tweet[1]).year)
        words = [tweet[0] for tweet in tweets if tweet[2] == year]
    else:
        words = [tweet[0] for tweet in tweets]
    return words


def _get_tweets2015(year=None):
    tweets = list(Database.get_all_documents('activist_events', 'whaling_tweets'))
    if year:
        for tweet in tweets:
            tweet['year'] = parser.parse(tweet['created_at']).year
        words = [tweet['text'] for tweet in tweets if tweet['year'] == year]
    else:
        words = [tweet['text'] for tweet in tweets]
    return words

def _get_articles_tommaso(year=None):
    with open('Corpora/articles.csv', 'rb') as csvfile:
        articles = list(unicodecsv.reader(csvfile))
    articles = list(map(itemgetter(0), groupby(articles)))

    if year:
        for article in articles:
            article.append(parser.parse(article[1]).year)
        words = [article[0] for article in articles if article[2] == year]
    else:
        words = [article[0] for article in articles]
    return set(words)


def _get_articles(year=None):
    articles = list(Database.get_all_documents('activist_events', 'whaling_articles', sort='seedwords_score'))
    if year:
        for article in articles:
            article['year'] = parser.parse(article['publication_date']).year
        articles = [article['body'] for article in articles if article['year'] == year]
    else:
        articles = [article['body'] for article in articles]
    return articles


print 'processing tweets 2014..'
c14words = _get_crowd2014words()

c14_results = {
    'news articles/blogs (all)': create_tweet_overlap_per_entity_type(c14words, _get_articles()),
    'news articles/blogs (2010)': create_tweet_overlap_per_entity_type(c14words, _get_articles(2010)),
    'news articles/blogs (2011)': create_tweet_overlap_per_entity_type(c14words, _get_articles(2011)),
    'news articles/blogs (2012)': create_tweet_overlap_per_entity_type(c14words, _get_articles(2012)),
    'news articles/blogs (2013)': create_tweet_overlap_per_entity_type(c14words, _get_articles(2013)),
    'news articles/blogs (2014)': create_tweet_overlap_per_entity_type(c14words, _get_articles(2014)),
    'news articles/blogs (2015)': create_tweet_overlap_per_entity_type(c14words, _get_articles(2015)),
    'news articles tomasso (all)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso()),
    'news articles tomasso (2005)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso(2005)),
    'news articles tomasso (2006)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso(2006)),
    'news articles tomasso (2007)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso(2007)),
    'news articles tomasso (2008)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso(2008)),
    'news articles tomasso (2009)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso(2009)),
    'news articles tomasso (2010)': create_tweet_overlap_per_entity_type(c14words, _get_articles_tommaso(2010)),
    'tweets2015 (all)': create_tweet_overlap_per_entity_type(c14words, _get_tweets2015())
}

csv = unicodecsv.writer(open('c14overlap_all.csv', "wb+"))
for dataset in c14_results:
    csv.writerow([dataset])
    csv.writerow(['c14_annotation','count'])
    for word, count in c14_results[dataset]:
        csv.writerow([word, count])
    csv.writerow([])

print 'processing tweets 2015..'
c15words = _get_crowd2015words()

c15_results = {
    'news articles/blogs (all)': create_tweet_overlap_per_entity_type(c15words, _get_articles()),
    'news articles/blogs (2010)': create_tweet_overlap_per_entity_type(c15words, _get_articles(2010)),
    'news articles/blogs (2011)': create_tweet_overlap_per_entity_type(c15words, _get_articles(2011)),
    'news articles/blogs (2012)': create_tweet_overlap_per_entity_type(c15words, _get_articles(2012)),
    'news articles/blogs (2013)': create_tweet_overlap_per_entity_type(c15words, _get_articles(2013)),
    'news articles/blogs (2014)': create_tweet_overlap_per_entity_type(c15words, _get_articles(2014)),
    'news articles/blogs (2015)': create_tweet_overlap_per_entity_type(c15words, _get_articles(2015)),
    'news articles tomasso (all)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso()),
    'news articles tomasso (2005)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso(2005)),
    'news articles tomasso (2006)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso(2006)),
    'news articles tomasso (2007)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso(2007)),
    'news articles tomasso (2008)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso(2008)),
    'news articles tomasso (2009)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso(2009)),
    'news articles tomasso (2010)': create_tweet_overlap_per_entity_type(c15words, _get_articles_tommaso(2010)),
    'tweets2015 (all)': create_tweet_overlap_per_entity_type(c15words, _get_tweets2015())
}

csv = unicodecsv.writer(open('c15overlap_all.csv', "wb+"))
for dataset in c15_results:
    csv.writerow([dataset])
    csv.writerow(['c15_annotation','count'])
    for word, count in c15_results[dataset]:
        csv.writerow([word, count])
    csv.writerow([])

print 'processing seedwords..'
seedwords = _get_seedwords()

seedwords_results = {
    'tweets (all)': create_tweet_overlap_per_entity_type(seedwords, _get_tweets()),
    'tweets (2014)': create_tweet_overlap_per_entity_type(seedwords, _get_tweets(2014)),
    'tweets (2015)': create_tweet_overlap_per_entity_type(seedwords, _get_tweets(2015)),
    'news articles/blogs (all)': create_tweet_overlap_per_entity_type(seedwords, _get_articles()),
    'news articles/blogs (2010)': create_tweet_overlap_per_entity_type(seedwords, _get_articles(2010)),
    'news articles/blogs (2011)': create_tweet_overlap_per_entity_type(seedwords, _get_articles(2011)),
    'news articles/blogs (2012)': create_tweet_overlap_per_entity_type(seedwords, _get_articles(2012)),
    'news articles/blogs (2013)': create_tweet_overlap_per_entity_type(seedwords, _get_articles(2013)),
    'news articles/blogs (2014)': create_tweet_overlap_per_entity_type(seedwords, _get_articles(2014)),
    'news articles/blogs (2015)': create_tweet_overlap_per_entity_type(seedwords, _get_articles(2015)),
    'news articles tomasso (all)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso()),
    'news articles tomasso (2005)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso(2005)),
    'news articles tomasso (2006)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso(2006)),
    'news articles tomasso (2007)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso(2007)),
    'news articles tomasso (2008)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso(2008)),
    'news articles tomasso (2009)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso(2009)),
    'news articles tomasso (2010)': create_tweet_overlap_per_entity_type(seedwords, _get_articles_tommaso(2010)),
    'tweets2015 (all)': create_tweet_overlap_per_entity_type(seedwords, _get_tweets2015())
}

csv = unicodecsv.writer(open('seedwordsoverlap_all.csv', "wb+"))
for dataset in seedwords_results:
    csv.writerow([dataset])
    csv.writerow(['seedword','count'])
    for seedword, count in seedwords_results[dataset]:
        csv.writerow([seedword, count])
    csv.writerow([])

print 'processing wikiwords..'
wikiwords = _get_wikiwords()

wikiwords_results = {
    'tweets (all)': create_tweet_overlap_per_entity_type(wikiwords, _get_tweets()),
    'tweets (2014)': create_tweet_overlap_per_entity_type(wikiwords, _get_tweets(2014)),
    'tweets (2015)': create_tweet_overlap_per_entity_type(wikiwords, _get_tweets(2015)),
    'news articles/blogs (all)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles()),
    'news articles/blogs (2010)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles(2010)),
    'news articles/blogs (2011)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles(2011)),
    'news articles/blogs (2012)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles(2012)),
    'news articles/blogs (2013)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles(2013)),
    'news articles/blogs (2014)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles(2014)),
    'news articles/blogs (2015)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles(2015)),
    'news articles tomasso (all)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso()),
    'news articles tomasso (2005)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso(2005)),
    'news articles tomasso (2006)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso(2006)),
    'news articles tomasso (2007)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso(2007)),
    'news articles tomasso (2008)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso(2008)),
    'news articles tomasso (2009)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso(2009)),
    'news articles tomasso (2010)': create_tweet_overlap_per_entity_type(wikiwords, _get_articles_tommaso(2010)),
    'tweets2015 (all)': create_tweet_overlap_per_entity_type(wikiwords, _get_tweets2015())
}

csv = unicodecsv.writer(open('wikiwordsoverlap_all.csv', "wb+"))
for dataset in wikiwords_results:
    csv.writerow([dataset])
    csv.writerow(['wiki_entity','count'])
    for seedword, count in wikiwords_results[dataset]:
        csv.writerow([seedword, count])
    csv.writerow([])


