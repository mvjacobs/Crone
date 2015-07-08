__author__ = 'marc'

import unicodecsv


def create_csv_from_articles(headers, rows, filename):
    csv = unicodecsv.writer(open(filename, "wb+"))
    csv.writerow(headers)
    for row in rows:
        csv.writerow(row)


def create_csv_for_articles(articles, filename):
    headers = [
        'title',
        'url',
        'author',
        'source',
        'publication_date',
        'comment_count',
        'word_count',
        'extracted_from',
        'keywords',
        'seedwords_found',
        'wikiwords_found',
        'seedwords_score',
        'wikiwords_score'
    ]

    rows = []
    for key in range(0, len(articles)):
        if isinstance(articles[key][u'author'], (list, tuple)):
            articles[key][u'author'] = ', '.join(set(keyword for keyword in articles[key][u'author']))

        tweet = [
            articles[key][u"title"],
            articles[key][u"url"],
            articles[key][u'author'],
            articles[key][u"source"],
            articles[key][u"publication_date"],
            articles[key][u"comment_count"],
            articles[key][u"word_count"],
            articles[key][u"extracted_from"],
            ', '.join(keyword for keyword in articles[key][u'keywords']),
            articles[key][u'seedwords_found'],
            articles[key][u'wikiwords_found'],
             articles[key][u'seedwords_score'],
             articles[key][u'wikiwords_score'],
        ]

        print 'article %i added' % key

        rows.append(tweet)

    create_csv_from_articles(headers, rows, filename)


def create_csv_for_crowd_task(articles, filename):
    headers = [
        'title',
        'source',
        'author',
        'publication_date',
        'abstract',
        'url',
        'comment_count',
        'word_count',
        'keywords'
    ]

    rows = []
    for key in range(0, len(articles)):
        if isinstance(articles[key][u'author'], (list, tuple)):
            parsed_authors = []
            for author in set(articles[key][u"author"]):
                parsed_author = '<span class="label label-primary">%s</span>' % author
                parsed_authors.append(parsed_author)

            articles[key][u'author'] = ' '.join(parsed_authors)
        else:
            articles[key][u'author'] = '<span class="label label-primary">%s</span>' % articles[key][u'author']

        parsed_keywords = []
        for keyword in articles[key][u"keywords"]:
            parsed_keyword = '<span class="label label-success">%s</span>' % keyword
            parsed_keywords.append(parsed_keyword)

        tweet = [
            articles[key][u"title"],
            articles[key][u"source"],
            articles[key][u'author'],
            articles[key][u"publication_date"],
            articles[key][u"abstract"],
            articles[key][u"url"],
            articles[key][u"comment_count"],
            articles[key][u"word_count"],
            ' '.join(parsed_keywords),
        ]

        print 'article %i added' % key

        rows.append(tweet)

    create_csv_from_articles(headers, rows, filename)


def create_csv_for_frankiina_task(articles, filename):
    headers = [
        'id1',
        'text1',
        'article_uppercase_count1',
        'article_nouns_count1',
        'article_comments_count1',
        'article_numerical_count1',
        'article_wiki_entities_count1',
        'article_word_count1',
        'article_punctuation_count1',
        'article_keywords_count1',
        'sentiment1',
        'article_publication_date1',
        'id2',
        'text2',
        'article_uppercase_count2',
        'article_nouns_count2',
        'article_comments_count2',
        'article_numerical_count2',
        'article_wiki_entities_count2',
        'article_word_count2',
        'article_punctuation_count2',
        'article_keywords_count2',
        'sentiment2',
        'article_publication_date2'
    ]

    rows = []
    for key, article in enumerate(articles):
        next_article = key + 1

        if next_article > len(articles)-1:
            break

        article1 = _parse_article_comparison(articles, key)
        article2 = _parse_article_comparison(articles, next_article)
        rows.append(article1 + article2)
        print 'Tweet %i added' % key

    # link last tweet to the first tweet
    article1 = _parse_article_comparison(articles, len(articles)-1)
    article2 = _parse_article_comparison(articles, 0)
    rows.append(article1 + article2)
    create_csv_from_articles(headers, rows, filename)


def _parse_article_comparison(articles, key):
    row = [
        articles[key]['_id'],
        articles[key]['abstract'],
        articles[key]['counts']['article_uppercase_count'],
        articles[key]['counts']['article_nouns_count'],
        articles[key]['counts']['article_comment_count'],
        articles[key]['counts']['article_numerical_count'],
        articles[key]['counts']['article_wiki_entities_count'],
        articles[key]['counts']['article_word_count'],
        articles[key]['counts']['article_punctuation_count'],
        articles[key]['counts']['article_keywords_count'],
        articles[key]['sentiment']['sentiwordnet'],
        articles[key]['dates']['article_publication_date']
    ]

    return row

