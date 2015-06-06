__author__ = 'marc'

from pymongo import MongoClient

def store_articles(articles, target_collection):
    print 'Storing the articles'
    client = MongoClient('localhost', 27017)
    db = client.activist_events

    for article in articles:
        try:
            db[target_collection].insert(article)
        except:
            continue

    print 'Storing done'
