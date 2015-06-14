__author__ = 'marc'

import microdata
import urllib
import json
import urllib2
import time

def get_article_body(guardian_article_url):
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(guardian_article_url)
        html = response.read()
        microdata_entities = microdata.get_items(html)
        entities = [json.loads(entity.json()) for entity in microdata_entities]
        body = []
        for entity in entities:
            if entity[u'type'] == [u'http://schema.org/NewsArticle']:
                return entity[u'properties']
    except:
        return []

    return body


def get_comments_from_article(guardian_article_url):
    read_url = urllib.urlopen(guardian_article_url)
    microdata_entities = microdata.get_items(read_url)
    entities = [json.loads(entity.json()) for entity in microdata_entities]
    comments = [entity['properties'] for entity in entities if 'http://schema.org/Comment' in entity['type']]
    return comments


def get_comments_count_from_article(guardian_article_url):
    return len(get_comments_from_article(guardian_article_url))


def add_content_to_articles(articles):
    articles_extended = []
    for key, article in enumerate(articles):
        try:
            article[u'body'] = article[u'blocks'][u'body'][0][u'bodyHtml']
            article[u'abstract'] = article[u'blocks'][u'body'][0][u'bodyTextSummary']
        except KeyError:
            try:
                article[u'body'] = article[u'fields'][u'body']
                article[u'abstract'] = article[u'fields'][u'headline']
            except KeyError:
                blocks = get_article_body(article[u'webUrl'])
                if not blocks:
                    print '%s deleted' % article[u'webUrl']
                    continue
                try:
                    article[u'body'] = blocks[u'articleBody']
                    article[u'abstract'] = blocks[u'description']
                except KeyError:
                    print '%s deleted' % article[u'webUrl']
                    continue

        article[u'comment_count'] = get_comments_count_from_article(article[u'webUrl'])
        article[u'comments'] = get_comments_from_article(article[u'webUrl'])
        articles_extended.append(article)
        time.sleep(1)

    return articles_extended
