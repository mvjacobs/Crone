__author__ = 'marc'

from Resources import Database
import string
import unicodedata
import PyTfIdf
import TextFilter
import unicodecsv
import pprint
from operator import itemgetter

articles = Database.get_all_documents('activist_events', 'whaling_blogs', 'publication_date')

# def create_txt_files(articles):
#     file_list = []
#     for article in articles:
#         file_path = 'input/%s.txt' % str(article['_id'])
#         file_list.append(file_path + '\n')
#         file = open(file_path, "w")
#         if isinstance(article['content'], (list, tuple)):
#             article['content'] = string.join(article['content'])
#         file.write('%s\n' % unicodedata.normalize('NFKD', article['content']).encode('ascii','ignore'))
#         file.close()
#
#     list = open('input/list.txt', "w")
#     list.writelines(file_list)
#     list.close()


def get_words(path_to_csv):
    with open(path_to_csv, 'rb') as csvfile:
        words = []
        for word in unicodecsv.reader(csvfile):
            words.append(word[0])
    return words

sw = get_words('../Relevancy/seedwords.csv')
wiki = get_words('../Relevancy/wikiwords.csv')
article = get_words('../Relevancy/articlewords.csv')

#tfidf.process('input/list.txt', 'both')

table = PyTfIdf.tfidf()
# for article in articles:
#     # local term frequency map
#     if isinstance(article['content'], (list, tuple)):
#         article['content'] = string.join(article['content'])
#     doc_words = unicodedata.normalize('NFKD', article['content']).encode('ascii','ignore')
#     doc_words = TextFilter.remove_stopwords(doc_words)
#     doc_words = TextFilter.tokenize(doc_words)
#     table.addDocument(article["url"], doc_words)
table.addDocument('wiki', wiki)


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(sorted(table.similarities(sw), key=itemgetter(1), reverse=True))



