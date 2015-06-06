__author__ = 'marc'
# http://developer.nytimes.com/docs/read/article_search_api_v2

from nytimesarticle import articleAPI
import time, math
from time import gmtime, strftime

nytimes_api_key = [line.strip() for line in open('Config/nytimes.cfg')][0]
now = strftime("%Y%m%d", gmtime())


def get_articles(keyword, from_date, end_date=now, page_limit=1):
    articles = []
    max_pages = int(math.ceil(get_hits_count(keyword, from_date, end_date)/10))
    print 'NYTimes: max pages %i' % max_pages

    if page_limit > 1:
        for page_number in range(0, max_pages):
            if page_number >= page_limit:
                break
            articles += get_10_articles(keyword, from_date, end_date, page_number)
            print 'NYTimes: articles of page %i are added.' % page_number
            time.sleep(1)
    else:
        articles = get_10_articles(keyword, from_date, end_date, 0)

    return articles


# max page_size = 10
# '8a67ef87ae6f8768fae7687fae6', 'whaling', 20110101, 20131231, 1
def get_10_articles(keyword, from_date, end_date, page_number):
    api = articleAPI(nytimes_api_key)

    articles = api.search(
        q=keyword,
        fq={'document_type': 'article'},
        begin_date=from_date,
        end_date=end_date,
        facet_field=['source'],
        facet_filter=True,
        page=page_number
    )

    return articles['response']['docs']


def get_hits_count(keyword, from_date, end_date):
    api = articleAPI(nytimes_api_key)

    articles = api.search(
        q=keyword,
        fq={'document_type': 'article'},
        begin_date=from_date,
        end_date=end_date,
        facet_field=['source'],
        facet_filter=True,
        page=1
    )

    return articles['response']['meta']['hits']
