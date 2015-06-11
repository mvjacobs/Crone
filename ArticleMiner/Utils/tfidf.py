#!/usr/bin/env python
# encoding: utf-8

"""
File: tfidf.py
Author: Yasser Ebrahim
Date: Oct 2012

Generate the TF-IDF ratings for a collection of documents.

This script will also tokenize the input files to extract words (removes punctuation and puts all in
    lower case), and it will use the NLTK library to lemmatize words (get rid of stemmings)

IMPORTANT:
    A REQUIRED library for this script is NLTK, please make sure it's installed along with the wordnet
    corpus before trying to run this script

Usage:
    - Create a file to hold the paths+names of all your documents (in the example shown: input_files.txt)
    - Make sure you have the full paths to the files listed in the file above each on a separate line
    - For now, the documents are only collections of text, no HTML, XML, RDF, or any other format
    - Simply run this script file with your input file as a single parameter, for example:
            python tfidf.py input_files.txt
    - This script will generate new files, one for each of the input files, with the suffix "_tfidf"
            which contains terms with corresponding tfidf score, each on a separate line

"""

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.punkt import PunktWordTokenizer
import sys, re, math, unicodedata
import nltk


# a list of (words-freq) pairs for each document
global_terms_in_doc = {}
# list to hold occurrences of terms across documents
global_term_freq    = {}
num_docs            = 0
lang        = 'english'
lang_dictionary     = {}
top_k               = -1
supported_langs     = ('english', 'french')

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
    for i in range(0,len(tokens)):
        #tokens[i] = tokens[i].strip("'")
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
            '*', '(', ')', ' - ', '_', '+' ,'=', '@', ':', '\\', ',',
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

# __main__ execution
def process(file_list, mode):
    display_mode = mode
    reader = open(file_list)
    all_files = reader.read().splitlines()

    num_docs  = len(all_files)

    print('initializing..')
    for f in all_files:

        # local term frequency map
        terms_in_doc = {}

        doc_words = open(f).read().lower()
        doc_words = remove_stopwords(doc_words)
        doc_words = tokenize(doc_words)

        # increment local count
        for word in doc_words:
            if word in terms_in_doc:
                terms_in_doc[word] += 1
            else:
                terms_in_doc[word]  = 1

        # increment global frequency
        for (word,freq) in terms_in_doc.items():
            if word in global_term_freq:
                global_term_freq[word] += 1
            else:
                global_term_freq[word]  = 1

        global_terms_in_doc[f] = terms_in_doc

    print('working through documents.. ')
    for f in all_files:

        writer = open(f + '_tfidf', 'w')
        result = []
        # iterate over terms in f, calculate their tf-idf, put in new list
        max_freq = 0;
        for (term,freq) in global_terms_in_doc[f].items():
            if freq > max_freq:
                max_freq = freq
        for (term,freq) in global_terms_in_doc[f].items():
            idf = math.log(float(1 + num_docs) / float(1 + global_term_freq[term]))
            tfidf = float(freq) / float(max_freq) * float(idf)
            result.append([tfidf, term])

        # sort result on tfidf and write them in descending order
        result = sorted(result, reverse=True)
        for (tfidf, term) in result[:top_k]:
            if display_mode == 'both':
                writer.write(term + '\t' + str(tfidf) + '\n')
            else:
                writer.write(term + '\n')

    print('success, with ' + str(num_docs) + ' documents.')