__author__ = 'marc'
# http://open-platform.theguardian.com/documentation/search

from time import gmtime, strftime
import requests
import time
import microdata
import urllib
import json

guardian_api_key = [line.strip() for line in open('Config/guardian.cfg')][0]
now = strftime("%Y-%m-%d", gmtime())

# max page size = 200
def get_articles(q, section, from_date, to_date=now, limit=10):
    articles = []

    if limit > 200:
        current = 200
        total_pages = get_total_pages(q, section, 200, from_date, to_date)
        print 'Guardian: max pages %i' % total_pages

        for page in range(1, total_pages + 1):
            articles += get_articles_private(q, section, 200, from_date, to_date, page)
            print 'Guardian: %i articles are added.' % current
            current += 200
            if current > limit:
                break
            time.sleep(1)
    else:
        articles = get_articles_private(q, section, limit, from_date, to_date=now)

    return articles


def get_articles_private(q, section, limit, from_date, to_date=now, page=1):
    api_url = 'http://content.guardianapis.com/search'
    payload = {
        'q':                    q,
        'section':              section,
        'from-date':            from_date,
        'to-date':              to_date,
        'api-key':              guardian_api_key,
        'page-size':            limit,
        'page':                 page,
        'show-editors-picks':   'true',
        'show-elements':        'all',
        'show-fields':          'all',
        'show-references':      'all',
        'show-blocks':          'all',
        'show-tags':            'all',
    }
    response = requests.get(api_url, params=payload).json()

    return response['response']['results']


def get_total_pages(q, section, limit, from_date, to_date=now):
    api_url = 'http://content.guardianapis.com/search'
    payload = {
        'q':                    q,
        'section':              section,
        'from-date':            from_date,
        'to-date':              to_date,
        'api-key':              guardian_api_key,
        'page-size':            limit,
    }
    response = requests.get(api_url, params=payload).json()

    return response['response']['pages']


def get_comments_from_article(guardian_article_url):
    read_url = urllib.urlopen(guardian_article_url)
    microdata_entities = microdata.get_items(read_url)
    entities = [json.loads(entity.json()) for entity in microdata_entities]
    comments = [entity['properties'] for entity in entities if 'http://schema.org/Comment' in entity['type']]

    return comments


def get_comments_count_from_article(guardian_article_url):
    return len(get_comments_from_article(guardian_article_url))
