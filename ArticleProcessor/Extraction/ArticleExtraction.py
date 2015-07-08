__author__ = 'marc'

from collections import Counter
from Analyzing import ArticleAnalysis, WordListAnalysis
from Filtering import ArticleFilter
import re
import string
import sys


def extract_filtered_text(articles):
    for key, article in enumerate(articles):
        text_filtered = ArticleFilter.remove_html_from_article(article[u'body'])
        article[u'body'] = text_filtered
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_filtered_tokens(articles):
    for key, article in enumerate(articles):
        tokens_filtered = ArticleFilter.get_filtered_article_text(article[u'body'])
        article[u'filtered_text'] = tokens_filtered
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_tokens_pos(articles):
    for key, article in enumerate(articles):
        tokens_filtered = ArticleFilter.get_tokens_with_pos(article[u'body'])
        article[u'tokens_with_pos'] = tokens_filtered
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_emoticons(articles):
    for key, article in enumerate(articles):
        emoticons = ArticleAnalysis.get_emoticons_from_article(article[u'body'])
        article[u'emoticons'] = emoticons
        article[u'emoticons_count'] = len(emoticons)
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_proper_nouns(articles):
    for key, article in enumerate(articles):
        nouns = ArticleAnalysis.get_proper_nouns(article['tokens_with_pos'])
        article[u'proper_nouns'] = nouns
        article[u'proper_nouns_count'] = len(nouns)
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_wiki_entities(articles):
    for key, article in enumerate(articles):
        entities = ArticleAnalysis.get_wiki_entities_count(article[u'body'])
        article[u'wiki_entities'] = entities
        article[u'wiki_entities_count'] = len(entities)
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_sentiment_scores(articles):
    for key, article in enumerate(articles):
        article[u'sentiment'] = {}
        try:
            article[u'sentiment'][u'sentiwordnet'] = ArticleAnalysis.calculate_article_sentiment(article['filtered_text'])
        except KeyError:
            article[u'sentiment'][u'sentiwordnet'] = 0

        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_count_uppercase_characters(articles):
    for key, article in enumerate(articles):
        article[u'uppercase_count'] = sum(1 for c in article['body'] if c.isupper())
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_numericals(articles):
    for key, article in enumerate(articles):
        numericals = ArticleAnalysis.get_numericals(article[u'tokens_with_pos'])
        article[u'numerical_mentions'] = numericals
        article[u'numerical_count'] = len(numericals)
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_punctuations(articles):
    for key, article in enumerate(articles):
        punctuations = ArticleAnalysis.get_punctuation(article[u'tokens_with_pos'])
        article[u'punctuations'] = punctuations
        article[u'punctuation_count'] = len(punctuations)
        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def extract_boolean_metrics(articles):
    for key, article in enumerate(articles):
        article[u'counts'] = {}
        article[u'counts'][u'article_word_count'] = article[u'word_count']
        article[u'counts'][u'article_comment_count'] = article[u'comment_count']
        article[u'counts'][u'article_keywords_count'] = len(article[u'keywords'])
        article[u'counts'][u'article_nouns_count'] = article[u'proper_nouns_count']
        article[u'counts'][u'article_numerical_count'] = article[u'numerical_count']
        article[u'counts'][u'article_wiki_entities_count'] = article[u'wiki_entities_count']
        article[u'counts'][u'article_uppercase_count'] = article[u'uppercase_count']
        article[u'counts'][u'article_punctuation_count'] = article[u'punctuation_count']
        article[u'counts'][u'article_emoticons_count'] = article[u'emoticons_count']

        article[u'dates'] = {}
        article[u'dates'][u'article_publication_date'] = article[u'publication_date']

        sys.stdout.write("\r%d of %d" % (key, len(articles)-1))
        sys.stdout.flush()
    sys.stdout.write("\n")

    return articles


def add_wiki_scores_to_articles(articles, wikiwords):
    wiki_weights = WordListAnalysis.get_wikiword_weights(wikiwords)
    articles = _add_relevance_scores(articles, wiki_weights, 'wikiwords_found', 'wikiwords_score')
    return articles


def add_seedwords_scores_to_articles(articles, seedwords):
    sw_weights = WordListAnalysis.get_seedwords_weights(seedwords)
    articles = _add_relevance_scores(articles, sw_weights, 'seedwords_found', 'seedwords_score')
    return articles


def add_crowdwords_scores_to_articles(articles, crowdwords):
    sw_weights = WordListAnalysis.get_crowdwords_weights(crowdwords)
    articles = _add_relevance_scores(articles, sw_weights, 'crowdwords_found', 'crowdwords_score')
    return articles


def _add_relevance_scores(articles, weights, field_name_counts, field_name_score):
    articles = list(articles)
    for article in articles:
        if isinstance(article['body'], (list, tuple)):
            article['body'] = string.join(article['body'])

        matches_in_doc = []
        for weight in weights:
            exact_match = re.compile(r'\b%s\b' % re.escape(weight['term']), flags=re.IGNORECASE)
            matches = exact_match.findall(article['body'])
            matches_in_doc += [match.lower() for match in matches]
        counts = Counter(matches_in_doc)
        article[field_name_counts] = counts

        score = 0
        scorelist = []
        if matches_in_doc:
            for word, count in counts.iteritems():
                score = [weight['weight'] for weight in weights if weight['term'].lower() == word]
                scorelist.append(float(score[0]*count))

            # todo: what number should we divide the weightscores with?
            score = sum(scorelist) / len(weights)
        article[field_name_score] = float(score)

    return articles
