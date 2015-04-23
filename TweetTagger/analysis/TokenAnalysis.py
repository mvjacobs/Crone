__author__ = 'marc'

import re


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


def is_url(text):
    p = re.compile(ur'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
                   ur'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
                   ur'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?]))')
    return bool(re.search(p, text))

