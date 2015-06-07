__author__ = 'marc'

from Output import Mongo
from Miners import NyTimesMiner, GuardianMiner

articles1 = NyTimesMiner.get_articles(
    keyword='whaling',
    from_date=20100101,
    page_limit=10
)

articles2 = GuardianMiner.get_articles(
    q='whaling',
    section='environment',
    from_date='2010-01-01',
    limit=100
)

blogs1 = NyTimesMiner.get_articles(
    keyword='whaling',
    from_date=20100101,
    page_limit=10,
    article_type='blog'
)

blogs2 = GuardianMiner.get_articles(
    q='whaling',
    section='environment',
    from_date='2010-01-01',
    limit=100,
    article_type='blog'
)

Mongo.store_articles(articles1, 'whaling_articles_nytimes')
Mongo.store_articles(articles2, 'whaling_articles_guardian')
Mongo.store_articles(blogs1, 'whaling_blogs_nytimes')
Mongo.store_articles(blogs2, 'whaling_blogs_guardian')

