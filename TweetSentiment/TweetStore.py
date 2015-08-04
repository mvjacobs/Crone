__author__ = 'marc'

from pymongo import MongoClient
import json


client = MongoClient('localhost', 27017)
db = client.museums

data = []
allHashtags = []

for museum in db.museum_locations.find():
    collectedHashtags = []
    relatedMuseums = []
    name = museum['id']

    for hashtag in db.museum_hashtags.find():
        allHashtags.append(hashtag['hashtag'].replace("#", ""))