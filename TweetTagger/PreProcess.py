__author__ = 'marc'

from nlp import TweetSetAnalysis
from database import ActivistEvents
import pprint

#list_of_tweets = ActivistEvents.get_tweets(100)
#words = TweetSetAnalysis.get_real_names_unique(list_of_tweets)
#print words

# number of retweets

# sentiment analysis

# no wikipedia entities

# top 10000 domains

# number of twitter language words

# mentions user credibility

# google trending topics

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(ActivistEvents.get_potential_credibility_factors(100))