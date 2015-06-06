__author__ = 'marc'
# http://developer.nytimes.com/docs/read/article_search_api_v2

from nytimesarticle import articleAPI
import time, math, requests, pprint
from time import gmtime, strftime

nytimes_api_key = [line.strip() for line in open('Config/nytimes.cfg')][0]
nytimes_community_api_key = [line.strip() for line in open('Config/nytimes.cfg')][1]
now = strftime("%Y%m%d", gmtime())


def get_articles(keyword, from_date, end_date=now, page_limit=1):
    articles = []
    max_pages = int(math.ceil(get_hits_count(keyword, from_date, end_date)/10))
    print 'NYTimes: max pages %i' % max_pages

    if page_limit > 1:
        for page_number in range(0, max_pages):
            if page_number >= page_limit:
                break
            articles += _get_news_articles(keyword, from_date, end_date, page_number)['response']['docs']
            print 'NYTimes: articles of page %i are added.' % page_number
            time.sleep(1)
    else:
        articles = _get_news_articles(keyword, from_date, end_date, 0)

    return articles


def get_hits_count(keyword, from_date, end_date):
    articles = _get_news_articles(keyword, from_date, end_date, 0)

    return articles['response']['meta']['hits']


def get_comments_from_url(url, page):
    api_url = 'http://api.nytimes.com/svc/community/v3/user-content/url.json'
    payload = {
        'api-key': nytimes_community_api_key,
        'url': url,
        'offset': page
    }
    response = requests.get(api_url, params=payload).json()

    return response['results']


def get_comments_count_from_url(url):
    return get_comments_from_url(url, 0)['totalCommentsFound']


# max page_size = 10
# '8a67ef87ae6f8768fae7687fae6', 'whaling', 20110101, 20131231, 1
def _get_articles(keyword, query_filter, from_date, end_date, page_number):
    api = articleAPI(nytimes_api_key)

    articles = api.search(
        q=keyword,
        fq=query_filter,
        begin_date=from_date,
        end_date=end_date,
        page=page_number
    )

    return articles

def _get_news_articles(keyword, from_date, end_date, page_number):
    query_filter = {
        'section_name.contains': ['World', 'U.S.'],
        'type_of_material.contains': ['News', 'Brief']
    }
    return _get_articles(keyword, query_filter, from_date, end_date, page_number)


def _get_blog_articles(keyword, from_date, end_date, page_number):
    query_filter = {
        'section_name.contains': ['World', 'U.S.'],
        'type_of_material.contains': ['Blog']
    }
    return _get_articles(keyword, query_filter, from_date, end_date, page_number)