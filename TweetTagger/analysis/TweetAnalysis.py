__author__ = 'marc'

import TokenAnalysis
from utils import DaviesSentimentAnalysis, Twokenize


class RelatedNames:
    def __init__(self, list_of_tokens):
        self.tokens = list_of_tokens
        self.depth = 0

    def add_related_words(self, token_to_check):
        word = ""
        deps = token_to_check["deps"]

        for token in self.tokens:
            if deps:
                if token["address"] in deps:
                    word = token["word"] + " " + token_to_check["word"]
                    token["processed"] = "true"
                    token_to_check["processed"] = "true"
                    if self.depth < 4:
                        self.depth += 1
                        self.add_related_words(token)
                    else:
                        self.depth = 0
                        break
        return word

    def get_names_from_tweets(self):
        words = []

        for token in self.tokens:
            token["processed"] = "false"

        for token in self.tokens:
            if token["tag"] == "^" and token["deps"]:
                words.append(self.add_related_words(token))

        words_without = [
            token["word"] for token in self.tokens
            if token["tag"] == "^" and token["processed"] == "false"
        ]

        return words + words_without


def get_proper_nouns(tweet):
    token_analysis = RelatedNames(tweet)
    words = token_analysis.get_names_from_tweets()

    return words


def calculate_tweet_sentiment(tokens):
    score = 0
    for token in tokens:
        score += TokenAnalysis.calculate_sentiment_score(token)

    return score


def calculate_tweet_happiness(tokens):
    return DaviesSentimentAnalysis.getHappiness(tokens)


def calculate_tweet_sadness(tokens):
    return DaviesSentimentAnalysis.getSadness(tokens)



def get_emoticon_sentiment(text):
    tokens = Twokenize.tokenize(text)
    positive_emoticons = [':)', ':-)', ':=)', ':D', ':-D', ':=D', '^_^', ';)', ';-)', ';=)']
    negative_emoticons = [':(', ':-(', ':=(', ":'(", ';(', ';-(', ';=(']

    happies = 0
    saddies = 0
    for token in tokens:
        if token in positive_emoticons:
            happies += 1
        if token in negative_emoticons:
            saddies += 1

    if happies > saddies:
        return '+'
    elif happies < saddies:
        return '-'
    else:
        return 0






