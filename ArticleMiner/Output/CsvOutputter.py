__author__ = 'marc'

import unicodecsv
from Resources import Database

def create_csv_from_articles(headers, rows, filename):
    csv = unicodecsv.writer(open(filename, "wb+"))
    csv.writerow(headers)
    for row in rows:
        csv.writerow(row)


def create_csv_for_articles(articles, filename):
    headers = [
        'title',
        'url',
        'author',
        'source',
        'publication_date',
        'comment_count',
        'word_count',
        'extracted_from',
        'keywords',
        'seedwords_found',
        'articlewords_found',
        'wikiwords_found',
        'seedwords_score',
        'articlewords_score',
        'wikiwords_score'
    ]

    rows = []
    for key in range(0, len(articles)):
        if isinstance(articles[key][u'author'], (list, tuple)):
            articles[key][u'author'] = ', '.join(set(keyword for keyword in articles[key][u'author']))

        tweet = [
            articles[key][u"title"],
            articles[key][u"url"],
            articles[key][u'author'],
            articles[key][u"source"],
            articles[key][u"publication_date"],
            articles[key][u"comment_count"],
            articles[key][u"word_count"],
            articles[key][u"extracted_from"],
            ', '.join(keyword for keyword in articles[key][u'keywords']),
            articles[key][u'seedwords_found'],
            articles[key][u'eventwords_found'],
            articles[key][u'wikiwords_found'],
             articles[key][u'seedwords_score'],
             articles[key][u'eventwords_score'],
             articles[key][u'wikiwords_score'],
        ]

        print 'article %i added' % key

        rows.append(tweet)

    create_csv_from_articles(headers, rows, filename)


whaling_articles = Database.get_all_documents('activist_events', 'whaling_blogs_relevancy', 'publication_date')
create_csv_for_articles(list(whaling_articles), 'blogs.csv')
