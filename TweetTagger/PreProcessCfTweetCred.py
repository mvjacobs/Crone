__author__ = 'marc'

from output import Output
from resources import ActivistEvents

tweets = ActivistEvents.get_cf_tweet_factors('whaling_events_may_rt_filtered')
Output.create_csv_for_tweet_cf_task(tweets, "url_filter.csv")