__author__ = 'marc'

from tweepy import StreamListener
from pymongo import MongoClient
import json
import time
import sys


class TwitterStreamingListener(StreamListener):
    """ Twitter listener
    Listens for new tweets based on keywords
    """
    def __init__(self, api=None, ou_type='mongo'):
        self.api = api
        self.counter = 0
        self.ou_type = ou_type

    def on_data(self, data):
        if 'in_reply_to_status' in data:
            self.on_status(data)

    def on_status(self, status):
        if self.ou_type == 'mongo':
            write_to_mongo("localhost", 27017, "activist_events", "whaling_events", status)

        time.sleep(0.5)
        print ">>> " + json.loads(status)['text']
        return

    def on_delete(self, status_id, user_id):
        sys.stderr.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(10)
        return


def write_to_mongo(server, port, db, collection, document):
    """ Store in MongoDB
    Write string in json format to MongoDB Database

    :param server: MongoDB server (i.e. localhost)
    :param port: MongoDB port (i.e. 27017)
    :param db: MongoDB database name (i.e. activist_events)
    :param collection: MongoDB collection name (i.e. whaling_evenst)
    :param document: json string to write to the DB
    :return: document is stored in the database
    """
    client = MongoClient(server, port)
    db = client[db]
    collection = db[collection]
    collection.insert(json.loads(document))
