__author__ = 'marc'

import pprint
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

Mongo.store_articles(articles1, 'whaling_articles_nytimes')
Mongo.store_articles(articles2, 'whaling_articles_guardian')

#print len(articles2)

#pp = pprint.PrettyPrinter(indent=4)

#pp.pprint(articles2)

