__author__ = 'marc'

from Resources import Database
from Extraction import ArticleExtraction
from Output import Mongo

print ">>> get tweets from db"
articles = Database.get_all_documents('activist_events', 'whaling_articles_crowd', sort='crowdwords_score')

print ">>> analyze articles text: remove html tags from body"
articles = ArticleExtraction.extract_filtered_text(articles)

print ">>> extract raw tokens with POS type"
articles = ArticleExtraction.extract_tokens_pos(articles)

print ">>> extract tokens without stop words and cleaned"
articles = ArticleExtraction.extract_filtered_tokens(articles)

print ">>> add metric: sentiment analysis"
articles = ArticleExtraction.extract_sentiment_scores(articles)

print ">>> add metric: uppercase count"
articles = ArticleExtraction.extract_count_uppercase_characters(articles)

print ">>> add metric: emoticons count"
articles = ArticleExtraction.extract_emoticons(articles)

print ">>> add metric: proper nouns count"
articles = ArticleExtraction.extract_proper_nouns(articles)

print ">>> add metric: numerical mentions count"
articles = ArticleExtraction.extract_numericals(articles)

print ">>> add metric: punctuations count"
articles = ArticleExtraction.extract_punctuations(articles)

print ">>> extract wiki entities from the articles"
articles = ArticleExtraction.extract_wiki_entities(articles)

print ">>> group metrics"
articles = ArticleExtraction.extract_boolean_metrics(articles)

print ">>> store tweets in db"
Mongo.store_articles(articles, 'whaling_articles_features')
