__author__ = 'marc'

def map_guardian_to_crone(documents):
    crone_docs = []

    for document in documents:
        print 'processing %s' % document[u'webUrl']
        crone_doc = dict()

        try:
            crone_doc[u'word_count'] = document[u'fields'][u'wordcount']
        except KeyError:
            continue

        crone_doc[u'body'] = document[u'body']
        crone_doc[u'abstract'] = document[u'abstract']

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
        crone_doc[u'comment_count'] = document[u'comment_count']
        crone_doc[u'comments'] = document[u'comments']
        crone_doc[u'extracted_from'] = 'http://open-platform.theguardian.com/'

        crone_docs.append(crone_doc)

    return crone_docs
