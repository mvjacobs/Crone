__author__ = 'marc'

from Resources import Database
from Processors import GuardianProcessor, NyTimesProcessor
from Output import Mongo

guardian_blogs = Database.get_guardian_articles('blog')
nytimes_blogs = Database.get_nytimes_articles('blog')
nytimes_news = Database.get_nytimes_articles('news')
guardian_news = Database.get_guardian_articles('news')


crone_blogs = GuardianProcessor.map_guardian_to_crone(guardian_blogs)
crone_blogs += NyTimesProcessor.map_nytimes_to_crone(nytimes_blogs)
Mongo.store_articles(crone_blogs, 'whaling_blogs')


# crone_articles = NyTimesProcessor.map_nytimes_to_crone(nytimes_news)
# crone_articles += GuardianProcessor.map_guardian_to_crone(guardian_news)
# Mongo.store_articles(crone_articles, 'whaling_articles')