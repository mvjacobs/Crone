__author__ = 'marc'

from output import Output
from resources import ActivistEvents

tweets = ActivistEvents.get_wenjie_tweet_factors('whaling_events_may', 2000)
Output.create_csv_for_wenjie_task(tweets, "wenjie_unfiltered.csv")
