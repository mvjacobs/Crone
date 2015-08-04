__author__ = 'marc'

from resources import ActivistEvents
from extraction import TweetSetExtraction
from filtering import TweetSetFilter
import random

#tweets = ActivistEvents.get_evaluation_factors('whaling_events_new')
tweet_ids = ActivistEvents.get_tweet_ids('whaling_events_may', 0)
tweets = TweetSetExtraction.update_stats(tweet_ids)
#tweets = TweetSetFilter.filter_tweets(tweets)
#tweets = random.sample(tweets, 600)
#tweets = TweetSetFilter.remove_tweets_without_retweets_or_likes(tweets)
ActivistEvents.store_tweets(tweets, 'whaling_events_may_rt')

