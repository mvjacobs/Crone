__author__ = 'marc'

from pymongo import MongoClient

events_database = 'activist_events'
nytimes_news_collection = 'whaling_articles_nytimes'
nytimes_blogs_collection = 'whaling_blogs_nytimes'
guardian_news_collection = 'whaling_articles_guardian'
guardian_blogs_collection = 'whaling_blogs_guardian'


def get_nytimes_articles(article_type, limit=0):
    if article_type == 'blog':
        coll = nytimes_blogs_collection
    else:
        coll = nytimes_news_collection

    credibility_fields = {
        'headline.main': 1,
        'abstract': 1,
        'word_count': 1,
        'source': 1,
        'web_url': 1,
        'content': 1,
        'byline.person.firstname': 1,
        'byline.person.lastname': 1,
        'byline.organization': 1,
        'keywords.value': 1,
        'doc_type': 1,
        'pub_date': 1,
        'comments': 1,
        'comment_count': 1
    }
    credibility_filter = {}
    sort = 'pub_date'

    nytimes_articles = perform_query(
        events_database,
        coll,
        fields=credibility_fields,
        qfilter=credibility_filter,
        sort=sort,
        limit=limit
    )

    return list(nytimes_articles)


def get_guardian_articles(article_type, limit=0):
    if article_type == 'blog':
        coll = guardian_blogs_collection
    else:
        coll = guardian_news_collection

    credibility_fields = {
        'webPublicationDate': 1,
        'webTitle': 1,
        'webUrl': 1,
        'tags.webTitle': 1,
        'body': 1,
        'blocks.body.bodyHtml': 1,
        'blocks.body.bodyTextSummary': 1,
        'blocks.body.createdBy.firstName': 1,
        'blocks.body.createdBy.lastName': 1,
        'blocks.body.createdBy.email': 1,
        'blocks.body.createdBy.lastModifiedBy': 1,
        'fields.byline': 1,
        'fields.wordcount': 1,
        'fields.publication': 1,
        'fields.commentable': 1,
        'abstract': 1,
        'comments': 1,
        'comment_count': 1
    }
    credibility_filter = {}
    sort = 'webPublicationDate'

    guardian_articles = perform_query(
        events_database,
        coll,
        fields=credibility_fields,
        qfilter=credibility_filter,
        sort=sort,
        limit=limit
    )

    articles = list(guardian_articles)

    for article in articles:
        tags = [tag['webTitle'] for tag in article['tags']]
        article['tags'] = tags

    return articles


def get_all_documents(db, coll, sort=None):
    client = MongoClient('localhost', 27017)
    db = client[db]
    coll = db[coll]
    articles = coll.find()
    if sort:
        articles.sort(sort)
    return articles


def perform_query(database, collection, fields, qfilter, sort, limit=0):
    client = MongoClient('localhost', 27017)
    db = client[database]
    coll = db[collection]
    articles = coll.find(qfilter,fields).sort(sort).limit(limit)
    return articles