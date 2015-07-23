from Output import Mongo, CsvOutputter
from Resources import Database

print ">>> get tweets from db"
articles = Database.get_all_documents('activist_events', 'whaling_articles_features', sort='crowdwords_score')

print ">>> write to csv"
CsvOutputter.create_csv_for_frankiina_task(articles, 'Out/article_cred_features_3.csv')