__author__ = 'marc'

from pymongo import MongoClient
from collections import Counter
from dateutil import parser
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
db = client.activist_events

def store_articles(articles, target_collection):
    print 'Storing the articles'
    for article in articles:
        try:
            db[target_collection].insert(article)
        except:
            continue

    print 'Storing done'


def remove_duplicates(target_collection, field):
    db[target_collection].ensure_index([(field, 1), ("unique", True), ("dropDups", True)])


def count_documents_per_day(collection, filter_field):
    client = MongoClient('localhost', 27017)
    db = client.activist_events
    docs = list(db[collection].find({}, {filter_field: 1}))
    tweets = [parser.parse(tweet[filter_field]).date() for tweet in docs]
    counts = sorted(Counter(tweets).items())

    return counts


def draw_histogram(freq_list):
    x = [value[0] for value in freq_list]
    y = [value[1] for value in freq_list]

    ax = plt.subplot(311)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    ax.grid(True)
    ax.bar(x, y, width=1)
    ax.xaxis_date()

    plt.ylabel('doc count')
    plt.xlabel('month')
    plt.title('tweets')

    plt.show()

list = count_documents_per_day('whaling_events_new', 'created_at')
draw_histogram(list)
