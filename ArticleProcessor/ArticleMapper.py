__author__ = 'marc'

from Resources import Database
from Filtering import CollectionFilter
from Normalizing import GuardianNormalizer, NyTimesNormalizer
from Extraction import ArticleExtraction
from Output import Mongo

guardian_blogs = Database.get_guardian_articles('blog')
nytimes_blogs = Database.get_nytimes_articles('blog')
nytimes_news = Database.get_nytimes_articles('news')
guardian_news = Database.get_guardian_articles('news')

crone_articles = GuardianNormalizer.map_guardian_to_crone(guardian_blogs)
crone_articles += GuardianNormalizer.map_guardian_to_crone(guardian_news)
crone_articles += NyTimesNormalizer.map_nytimes_to_crone(nytimes_blogs)
crone_articles += NyTimesNormalizer.map_nytimes_to_crone(nytimes_news)

crone_articles = ArticleExtraction.add_wiki_scores_to_articles(crone_articles, 'WordLists/wikiwords.csv')
crone_articles = ArticleExtraction.add_seedwords_scores_to_articles(crone_articles, 'WordLists/seedwords.csv')
crone_articles = ArticleExtraction.add_crowdwords_scores_to_articles(crone_articles, 'WordLists/crowdnews.csv')

crone_articles = CollectionFilter.remove_duplicates(crone_articles, 'url')

Mongo.store_articles(crone_articles, 'whaling_articles_crowd')
