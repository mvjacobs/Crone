__author__ = 'marc'
# http://open-platform.theguardian.com/documentation/search

from time import gmtime, strftime
from Content import GuardianContentScraper
import requests
import time

guardian_api_key = [line.strip() for line in open('Config/guardian.cfg')][0]
now = strftime("%Y-%m-%d", gmtime())

# max page size = 200
def get_articles(q, section, from_date, to_date=now, limit=10, article_type='news'):
    articles = []

    print "Guardian: getting articles."
    if limit > 200:
        current = 200
        total_pages = get_total_pages(q, section, 200, from_date, to_date, article_type)

        for page in range(1, total_pages + 1):
            articles += _get_articles(q, section, 200, from_date, to_date, page, article_type)
            current += 200
            if current > limit:
                break
            time.sleep(1)
    else:
        articles = _get_articles(q, section, limit, from_date, to_date=now, article_type=article_type)

    print "Guardian: adding content to articles."
    articles = GuardianContentScraper.add_content_to_articles(articles)

    return articles


def get_total_pages(q, section, limit, from_date, to_date=now, article_type='news'):
    if article_type == 'blog':
        tag = ['blog', 'tone/blog']
    else:
        tag = []

    api_url = 'http://content.guardianapis.com/search'
    payload = {
        'q':                    q,
        'section':              section,
        'tag':                  tag,
        'from-date':            from_date,
        'to-date':              to_date,
        'api-key':              guardian_api_key,
        'page-size':            limit,
    }
    response = requests.get(api_url, params=payload).json()

    return response['response']['pages']

def _get_articles(q, section, limit, from_date, to_date=now, page=1, article_type='news'):
    if article_type == 'blog':
        tag = ['blog', 'tone/blog']
    else:
        tag = []

    api_url = 'http://content.guardianapis.com/search'
    payload = {
        'q':                    q,
        'section':              section,
        'from-date':            from_date,
        'to-date':              to_date,
        'tag':                  tag,
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
