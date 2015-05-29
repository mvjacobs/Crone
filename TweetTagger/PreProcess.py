__author__ = 'marc'

from resources import ActivistEvents
from filtering import TweetSetFilter
from extraction import TweetSetExtraction
import pprint
from output import Output

# get tweets from db
tweets = ActivistEvents.get_evaluation_factors('whaling_events_may_rt', 10)

# filter tweets: remove retweets, handles and unnecessary html tags
tweets = TweetSetFilter.filter_tweets(tweets)

# remove tweets without retweets or likes
tweets = TweetSetFilter.remove_tweets_without_retweets_or_likes(tweets)

# extract tokens without stop words and cleaned
#TweetSetExtraction.extract_filtered_tokens(tweets)

# analyze tweet text: extract text relations
#TweetSetExtraction.extract_word_types_and_relations(tweets)

# add metric: sentiment analysis
#TweetSetExtraction.extract_sentiment_scores(tweets)

# add metric: count uppercase
#TweetSetExtraction.extract_count_uppercase_characters(tweets)

# TODO add metric: n/o wikipedia entities

# TODO add metric: top 100 newser news sources

# TODO add metric: number of twitter language words

# TODO add metric: mentions user credibility

# Test print
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(tweets)

# Output
#Output.to_json(filtered_tweets)

# store tweets in db
#ActivistEvents.store_tweets(tweets, 'whaling_events_may_rt_filtered')


