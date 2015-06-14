__author__ = 'marc'

from TfIdf import TfIdf

def tf_idf_wordlist_comparison(wordlist_to_compare, wordlists):
    table = TfIdf()

    for wordlist_name in wordlists:
        if wordlists[wordlist_name] != wordlist_to_compare:
            table.add_document(wordlist_name, wordlists[wordlist_name])

    return table.similarities(wordlists[wordlist_to_compare])


def tf_idf_wordlists_comparison(wordlists):

    wordlists_compared = {}
    for current_wordlist_name in wordlists:
        table = TfIdf()
        for w in wordlists:
            if w != current_wordlist_name:
                table.add_document(w, wordlists[w])

        wordlists_compared[current_wordlist_name] = table.similarities(wordlists[current_wordlist_name])

    return wordlists_compared
