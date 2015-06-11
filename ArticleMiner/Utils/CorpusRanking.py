__author__ = 'marc'

from Resources import Database
import string
import unicodedata
import PyTfIdf
import TextFilter
import unicodecsv
import pprint
from operator import itemgetter

def get_words(path_to_csv, dialect=None):
    with open(path_to_csv, 'rb') as csvfile:
        words = []
        if dialect == 'tsv':
            for word in unicodecsv.reader(csvfile, dialect="excel-tab"):
                words.append(word[0])
        else:
           for word in unicodecsv.reader(csvfile):
                words.append(word[0])
    return words


sw = get_words('../Relevancy/seedwords.csv')
wiki = get_words('../Relevancy/wikiwords.csv')
article = get_words('../Relevancy/articlewords.csv', 'tsv')

table = PyTfIdf.tfidf()
table.addDocument('wiki', wiki)
table.addDocument('doc', article)
print 'seedwords:'
print sorted(table.similarities(sw), key=itemgetter(1), reverse=True)


table = PyTfIdf.tfidf()
table.addDocument('seedwords', sw)
table.addDocument('doc', article)

print 'wikiwords:'
print sorted(table.similarities(wiki), key=itemgetter(1), reverse=True)