__author__ = 'marc'

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
        crone_doc[u'body'] = document[u'content']
        crone_doc[u'comment_count'] = document[u'comment_count']
        crone_doc[u'comments'] = document[u'comments']
        crone_doc[u'extracted_from'] = 'http://developer.nytimes.com/docs/'

        crone_docs.append(crone_doc)

    return crone_docs
