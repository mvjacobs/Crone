# encoding: utf-8

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.punkt import PunktWordTokenizer
import unicodedata
import nltk

# a list of (words-freq) pairs for each document
global_terms_in_doc = {}
# list to hold occurrences of terms across documents
global_term_freq = {}
num_docs = 0
lang = 'english'
lang_dictionary = {}
top_k = -1
supported_langs = ('english', 'french')

# support for custom language if needed
def loadLanguageLemmas(filePath):
    print('loading language from file: ' + filePath)
    f = open(filePath)
    for line in f:
        words = line.split()
        if words[1] == '=' or words[0] == words[1]:
            continue
        lang_dictionary[words[0]] = words[1]


def remove_diacritic(words):
    for i in range(len(words)):
        w = unicode(words[i], 'ISO-8859-1')
        w = unicodedata.normalize('NFKD', w).encode('ASCII', 'ignore')
        words[i] = w.lower()
    return words


# function to tokenize text, and put words back to their roots
def tokenize(text):
    text = ' '.join(text)
    tokens = PunktWordTokenizer().tokenize(text)

    # lemmatize words. try both noun and verb lemmatizations
    lmtzr = WordNetLemmatizer()
    for i in range(0, len(tokens)):
        if lang != 'english':
            if tokens[i] in lang_dictionary:
                tokens[i] = lang_dictionary[tokens[i]]
        else:
            res = lmtzr.lemmatize(tokens[i])
            if res == tokens[i]:
                tokens[i] = lmtzr.lemmatize(tokens[i], 'v')
            else:
                tokens[i] = res

    # don't return any single letters
    tokens = [t for t in tokens if len(t) > 1 and not t.isdigit()]
    return tokens


def remove_stopwords(text):
    # remove punctuation
    chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&',
             '*', '(', ')', ' - ', '_', '+', '=', '@', ':', '\\', ',',
             ';', '~', '`', '<', '>', '|', '[', ']', '{', '}', '–', '“',
             '»', '«', '°', '’']
    for c in chars:
        text = text.replace(c, ' ')

    text = text.split()

    if lang == 'english':
        stopwords = nltk.corpus.stopwords.words('english')
    else:
        stopwords = open(lang + '_stopwords.txt', 'r').read().split()
    content = [w for w in text if w.lower().strip() not in stopwords]
    return content
