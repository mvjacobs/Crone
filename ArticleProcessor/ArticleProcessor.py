__author__ = 'marc'

from Resources import Database
from Normalizing import GuardianNormalizer, NyTimesNormalizer
from Output import Mongo

guardian_blogs = Database.get_guardian_articles('blog')
nytimes_blogs = Database.get_nytimes_articles('blog')
nytimes_news = Database.get_nytimes_articles('news')
guardian_news = Database.get_guardian_articles('news')

crone_articles = GuardianNormalizer.map_guardian_to_crone(guardian_blogs)
crone_articles += GuardianNormalizer.map_guardian_to_crone(guardian_news)
crone_articles += NyTimesNormalizer.map_nytimes_to_crone(nytimes_blogs)
crone_articles += NyTimesNormalizer.map_nytimes_to_crone(nytimes_news)

Mongo.store_articles(crone_articles, 'whaling_articles')
Mongo.remove_duplicates('whaling_articles', 'url')
