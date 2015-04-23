__author__ = 'marc'

from database import ActivistEvents
from analysis import SentimentAnalysis, TweetSetAnalysis
import pprint
from output import Output

# get tweets from db
tweets = ActivistEvents.get_potential_credibility_factors(10)

# filter tweets: remove retweets and unnecessary html tags
ActivistEvents.filter_tweets(tweets)

# TODO filter tweets: filter bots

# filter tweet text: remove stop words
TweetSetAnalysis.remove_stop_words(tweets)

# TODO filter tweet text: optional stemming

# analyze tweet text: find text relations
TweetSetAnalysis.get_word_types_and_relations(tweets)

# add metric: sentiment analysis
SentimentAnalysis.get_tweet_sentiment(tweets)

# TODO add metric: count uppercase

# TODO add metric: no wikipedia entities

# TODO add metric: top 10000 domains

# TODO add metric: number of twitter language words

# TODO add metric: mentions user credibility

# TODO add metric: google trending topics

# Test print
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tweets)

# Output
#Output.to_json(filtered_tweets)
