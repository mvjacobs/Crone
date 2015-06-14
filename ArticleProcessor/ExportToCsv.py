__author__ = 'marc'

from Resources import Database
from Output import CsvOutputter

articles = Database.get_all_documents('activist_events', 'whaling_articles', sort='seedwords_score')
CsvOutputter.create_csv_for_articles(list(articles), 'whaling_articles.csv')
