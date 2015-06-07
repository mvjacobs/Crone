__author__ = 'marc'

import microdata
import urllib
import json
import time
import urllib2


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


def map_guardian_to_crone(documents):
    crone_docs = []

    for document in documents:
        print 'processing %s' % document[u'webUrl']
        crone_doc = dict()

        try:
            crone_doc[u'word_count'] = document[u'fields'][u'wordcount']
        except KeyError:
            continue

        try:
            crone_doc[u'content'] = document[u'blocks'][u'body'][0][u'bodyHtml']
            crone_doc[u'abstract'] = document[u'blocks'][u'body'][0][u'bodyTextSummary']
        except KeyError:
            blocks = get_article_body(document[u'webUrl'])
            if not blocks:
                continue
            try:
                crone_doc[u'content'] = blocks[u'articleBody']
                crone_doc[u'abstract'] = blocks[u'description']
            except KeyError:
                continue

        try:
            crone_doc[u'author'] = '%s %s' % (
                document[u'blocks'][u'body'][0][u'createdBy'][u'firstName'],
                document[u'blocks'][u'body'][0][u'createdBy'][u'lastName']
            )
        except KeyError:
            try:
                crone_doc[u'author'] = document[u'fields'][u'byline']
            except KeyError:
                continue

        crone_doc[u'title'] = document[u'webTitle']
        crone_doc[u'source'] = document[u'fields'][u'publication']
        crone_doc[u'url'] = document[u'webUrl']
        crone_doc[u'keywords'] = document[u'tags']
        crone_doc[u'publication_date'] = document[u'webPublicationDate']
        crone_doc[u'comment_count'] = get_comments_count_from_article(document[u'webUrl'])
        crone_doc[u'comments'] = get_comments_from_article(document[u'webUrl'])
        crone_doc[u'extracted_from'] = 'http://open-platform.theguardian.com/'
        time.sleep(1)

        crone_docs.append(crone_doc)

    return crone_docs
