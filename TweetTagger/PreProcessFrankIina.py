__author__ = 'marc'

from resources import ActivistEvents
from output import Output

tweets = ActivistEvents.create_random_sample(100, 'whaling_tweets_frank_iina')
Output.create_csv_for_frankiina_task(tweets, 'whaling_tweets.csv')

