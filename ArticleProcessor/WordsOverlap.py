__author__ = 'marc'

from Analyzing import RankingWordLists
import pprint
import unicodecsv


wordLists = RankingWordLists.get_ranking_word_lists()

results = {}
blacklist = []

csv = unicodecsv.writer(open('wordsoverlap.csv', "wb+"))
csv.writerow(['set1', 'set1_size', 'set2', 'set2_size', 'matches_count', 'overlap'])

for name in wordLists:
    spans = set([span.lower() for span in wordLists[name]])
    otherWordLists = [wordList for wordList in wordLists if (wordList is not name) and (wordList not in blacklist)]
    matches = []
    results[name] = []
    for otherWordListName in otherWordLists:
        otherSpans = set([otherSpan.lower() for otherSpan in wordLists[otherWordListName]])
        matches = [span for span in otherSpans if span in spans]
        results[name].append({otherWordListName: matches})
        csv.writerow([name, len(spans), otherWordListName, len(otherSpans), len(matches), ', '.join(matches)])
    blacklist.append(name)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(results)