__author__ = 'marc'

from resources import ActivistEvents
from filtering import TweetSetFilter
from extraction import TweetSetExtraction


print ">>> get tweets from db"
tweets = ActivistEvents.get_tweets_sorted('whaling_tweets_relevancy_no_dups', [('seedwords_score', -1), ('wikiwords_score', -1)], 2000)

#tweets = TweetSetExtraction.update_stats(tweets)

# print ">>> remove duplicates"
# tweets = TweetSetFilter.remove_duplicates(tweets, 'text')
#
# print ">>> add wikiwords relevancy"
# tweets = TweetSetExtraction.add_wiki_scores_to_tweets(tweets, 'WordLists/wikiwords.csv')
#
# print ">>> add seedwords relevancy"
# tweets = TweetSetExtraction.add_seedwords_scores_to_tweets(tweets, 'WordLists/seedwords.csv')

print ">>> extract tokens without stop words and cleaned"
tweets = TweetSetExtraction.extract_filtered_tokens(tweets)

print ">>> add metric: sentiment analysis"
tweets = TweetSetExtraction.extract_sentiment_scores(tweets)

print ">>> analyze tweet text: extract text relations"
tweets = TweetSetExtraction.extract_word_types_and_relations(tweets)

print ">>> add wiki entities to the tweetset"
tweets = TweetSetExtraction.extract_wiki_entities(tweets)

print ">>> add metric: top 100 newser news sources"
tweets = TweetSetExtraction.extract_full_urls(tweets)

print ">>> add metric: word count"
tweets = TweetSetExtraction.extract_count_words(tweets)

print ">>> add metric: uppercase count"
tweets = TweetSetExtraction.extract_count_uppercase_characters(tweets)

print ">>> add metric: proper nouns count"
tweets = TweetSetExtraction.extract_proper_nouns(tweets)

print ">>> add metric: emoticons count"
tweets = TweetSetExtraction.extract_emoticons(tweets)

print ">>> add metric: numerical mentions count"
tweets = TweetSetExtraction.extract_numericals(tweets)

print ">>> add metric: punctuations count"
tweets = TweetSetExtraction.extract_punctuations(tweets)

print ">>> group metrics"
tweets = TweetSetExtraction.extract_boolean_metrics(tweets)

print ">>> store tweets in db"
ActivistEvents.store_tweets(tweets, 'whaling_tweets_2000_4')


