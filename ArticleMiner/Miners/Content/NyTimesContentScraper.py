__author__ = 'marc'

import microdata
import urllib2
import json
import time

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


def add_body_to_articles(articles):
    articles_extended = []
    for key, article in enumerate(articles):
        body = get_article_body(article[u'web_url'])
        if len(body) == 0:
            continue
        article[u'content'] = body
        articles_extended.append(article)
        time.sleep(1)
    return articles_extended

