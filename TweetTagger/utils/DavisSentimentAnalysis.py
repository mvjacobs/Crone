import numpy as np
import os


def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row

    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])

    return happy_log_probs, sad_log_probs


def classifySentiment(words, happy_log_probs, sad_log_probs):
    # Get the log-probability of each word under each sentiment
    happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
    sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]

    # Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
    tweet_happy_log_prob = np.sum(happy_probs)
    tweet_sad_log_prob = np.sum(sad_probs)

    # Calculate the probability of the tweet belonging to each sentiment
    prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
    prob_sad = 1 - prob_happy

    return prob_happy, prob_sad


def getHappiness(words):
    happy_log_probs, sad_log_probs = readSentimentList(
        '%s/data/twitter_sentiment_list.csv' % os.path.dirname(os.path.realpath(__file__))
    )
    happy, sad = classifySentiment(words, happy_log_probs, sad_log_probs)
    return happy


def getSadness(words):
    happy_log_probs, sad_log_probs = readSentimentList(
        '%s/data/twitter_sentiment_list.csv' % os.path.dirname(os.path.realpath(__file__))
    )
    happy, sad = classifySentiment(words, happy_log_probs, sad_log_probs)
    return sad


def test():
    # We load in the list of words and their log probabilities
    happy_log_probs, sad_log_probs = readSentimentList(
        '%s/data/twitter_sentiment_list.csv' % os.path.dirname(os.path.realpath(__file__))
    )

    # Here we have tweets which we have already tokenized (turned into an array of words)
    tweet1 = ['I', 'love', 'holidays']
    tweet2 = ['very', 'sad']

    # Calculate the probabilities that the tweets are happy or sad
    tweet1_happy_prob, tweet1_sad_prob = classifySentiment(tweet1, happy_log_probs, sad_log_probs)
    tweet2_happy_prob, tweet2_sad_prob = classifySentiment(tweet2, happy_log_probs, sad_log_probs)
    print getHappiness(tweet2)
    print getSadness(tweet2)
    #print "The probability that tweet1 (", tweet1, ") is happy is ", tweet1_happy_prob, "and the probability that it is sad is ", tweet1_sad_prob
    #print "The probability that tweet2 (", tweet2, ") is sad is ", tweet2_happy_prob, "and the probability that it is sad is ", tweet2_sad_prob