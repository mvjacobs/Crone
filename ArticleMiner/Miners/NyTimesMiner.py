__author__ = 'marc'
# http://developer.nytimes.com/docs/read/article_search_api_v2

from nytimesarticle import articleAPI
import time
import math
from time import gmtime, strftime
from Content import NyTimesCommentMiner, NyTimesContentScraper

nytimes_api_key = [line.strip() for line in open('Config/nytimes.cfg')][0]
now = strftime("%Y%m%d", gmtime())


def get_articles(keyword, from_date, end_date=now, page_limit=1, article_type='news'):
    articles = []
    max_pages = int(math.ceil(get_hits_count(keyword, from_date, end_date, article_type)/10))
    print 'NYTimes: max pages %i' % max_pages

    if page_limit > 1:
        for page_number in range(0, max_pages):
            if page_number >= page_limit:
                break
            articles += _get_articles(keyword, from_date, end_date, page_number, article_type)['response']['docs']
            print 'NYTimes: articles of page %i are added.' % page_number
            time.sleep(1)
    else:
        articles = _get_articles(keyword, from_date, end_date, 0, article_type)

    print "NYTimes: adding body to articles."
    articles = NyTimesContentScraper.add_body_to_articles(articles)

    print "NYTimes: adding comments to articles."
    articles = NyTimesCommentMiner.add_comments_to_articles(articles)

    return articles


def get_hits_count(keyword, from_date, end_date, article_type):
    articles = _get_articles(keyword, from_date, end_date, 0, article_type)

    return articles['response']['meta']['hits']


# max page_size = 10
# params example: 'whaling', 20110101, 20131231, 1, 'news'
def _get_articles(keyword, from_date, end_date, page_number, article_type):
    api = articleAPI(nytimes_api_key)

    if article_type == 'blog':
        query_filter = {
            'section_name.contains': ['World', 'U.S.', 'Opinion'],
            'type_of_material.contains': ['Blog']
        }
    else:
        query_filter = {
            'section_name.contains': ['World', 'U.S.'],
            'type_of_material.contains': ['News', 'Brief']
        }

    articles = api.search(
        q=keyword,
        fq=query_filter,
        begin_date=from_date,
        end_date=end_date,
        page=page_number
    )

    return articles

