__author__ = 'marc'

import requests
import time

nytimes_community_api_key = [line.strip() for line in open('Config/nytimes.cfg')][1]


def get_comments_from_url(url):
    total_pages = int(get_comments_count_from_url(url)/25) + 1

    if total_pages == 1:
        return _get_comments_from_url(url, 0)[u'comments']
    else:
        comments = []
        for offset in range(0, total_pages):
            comments += _get_comments_from_url(url, offset)[u'comments']
            time.sleep(1)

        return comments


def _get_comments_from_url(url, page):
    api_url = 'http://api.nytimes.com/svc/community/v3/user-content/url.json'
    payload = {
        'api-key': nytimes_community_api_key,
        'url': url,
        'offset': page
    }
    response = requests.get(api_url, params=payload).json()

    return response['results']


def get_comments_count_from_url(url):
    return _get_comments_from_url(url, 0)[u'totalCommentsFound']


def add_comments_to_articles(articles):
    for article in articles:
        article[u'comment_count'] = get_comments_count_from_url(article[u'web_url'])
        article[u'comments'] = get_comments_from_url(article[u'web_url'])

    return articles