__author__ = 'marc'

from Resources import Database
from collections import Counter
import csv
import re
import string

def add_sw_relevance_scores(articles):
    with open('Relevancy/seedwords.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        seedwords = []
        for row in reader:
            seedwords.append(row[0])

    exact_match = re.compile(r'\b%s\b' % '\\b|\\b'.join(seedwords), flags=re.IGNORECASE)

    for article in articles:
        if isinstance(article['content'], (list, tuple)):
            article['content'] = string.join(article['content'])
        counts = Counter(exact_match.findall(article['content']))

        print '%s: %s' % (article['url'], counts)


whaling_articles = Database.get_all_documents('activist_events', 'whaling_blogs', 'publication_date')
add_sw_relevance_scores(whaling_articles)


