__author__ = 'marc'

from output import Output
from resources import ActivistEvents
from filtering import TweetSetFilter
import random

#tweets = ActivistEvents.get_evaluation_factors('whaling_tweets_frank_iina', 0)
#tweets = [tweet for tweet in tweets if len(tweet['text']) > 100]
#sample = TweetSetFilter.create_random_sample(200, tweets)
tweets = ActivistEvents.get_tweets('whaling_tweets_2000_4', 0)
tweets = random.sample(tweets, 100)
Output.create_csv_for_frankiina_task(tweets, "out/crowdflower_100_1.csv")