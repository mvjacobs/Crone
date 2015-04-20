__author__ = 'marc'

from database import ActivistEvents
import pprint
from output import Output

# get tweets from db
tweets = ActivistEvents.get_potential_credibility_factors(100)

# filter tweets
filtered_tweets = ActivistEvents.filter_tweets(tweets)

# sentiment analysis

# no wikipedia entities

# top 10000 domains

# number of twitter language words

# mentions user credibility

# google trending topics

# Test print
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(filtered_tweets)

# Output
Output.to_json(filtered_tweets)
