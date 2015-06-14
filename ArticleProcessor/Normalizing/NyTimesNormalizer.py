__author__ = 'marc'

import microdata
import urllib2
import json
import requests
import time

nytimes_community_api_key = [line.strip() for line in open('Config/nytimes.cfg')][1]


def get_article_body(nytimes_article_url):
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(nytimes_article_url)
        html = response.read()
        microdata_entities = microdata.get_items(html)
        entities = [json.loads(entity.json()) for entity in microdata_entities]
        body = []
        for entity in entities:
            body += entity[u'properties'][u'articleBody']
    except:
        return []

    return body


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


def map_nytimes_to_crone(documents):
    crone_docs = []

    for document in documents:
        print 'processing %s' % document[u'web_url']
        crone_doc = dict()
        crone_doc[u'title'] = document[u'headline'][u'main']
        crone_doc[u'abstract'] = document[u'abstract']
        crone_doc[u'word_count'] = document[u'word_count']
        crone_doc[u'source'] = document[u'source']
        crone_doc[u'url'] = document[u'web_url']
        try:
            if len(document[u'byline'][u'person']) == 0:
                try:
                    crone_doc[u'author'] = document[u'byline'][u'organization']
                except:
                    crone_doc[u'author'] = []
            else:
                for person in document[u'byline'][u'person']:
                    try:
                        persons.append('%s %s' % (person[u'firstname'], person[u'lastname']))
                    except:
                        persons = []
                crone_doc[u'author'] = persons
        except KeyError:
            crone_doc[u'author'] = []

        keywords = []
        for keyword in document[u'keywords']:
            keywords.append(keyword[u'value'])
        crone_doc[u'keywords'] = keywords
        crone_doc[u'publication_date'] = document[u'pub_date']
        body = get_article_body(document[u'web_url'])
        if len(body) == 0:
            continue
        crone_doc[u'content'] = body
        crone_doc[u'comment_count'] = get_comments_count_from_url(document[u'web_url'])
        crone_doc[u'comments'] = get_comments_from_url(document[u'web_url'])
        crone_doc[u'extracted_from'] = 'http://developer.nytimes.com/docs/'
        time.sleep(1)

        crone_docs.append(crone_doc)

    return crone_docs
