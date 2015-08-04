__author__ = 'marc'

import unicodecsv
from collections import Counter
from operator import itemgetter


def pairwise_comparison(tweets):
    count_credible, count_same, count_not_credible = tweets

    scores = []
    for tweet_count, (date, text) in enumerate(count_same):
        score = 0
        score += float(count_same[(date, text)])
        score += float(count_credible[(date, text)])
        scores.append((date, text, score))

    return sorted(scores, key=itemgetter(2))


def tweet_results(tweets):
    count_credible, count_same, count_not_credible = tweets

    results = []
    for tweet_count, (date, text) in enumerate(count_same):
        results.append((
            date,
            text,
            count_credible[(date, text)],
            count_not_credible[(date, text)],
            count_same[(date, text)])
        )

    return results


def create_tweet_vector(tweets):
    tw_credible1 = [(tweet['created_at1'], tweet['_worker_id'], 1) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet1']
    tw_credible2 = [(tweet['created_at2'], tweet['_worker_id'], 1) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet2']
    tw_credible = tw_credible1 + tw_credible2

    tw_same1 = [(tweet['created_at1'], tweet['_worker_id'], 1) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'same']
    tw_same2 = [(tweet['created_at2'], tweet['_worker_id'], 1) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'same']
    tw_same = tw_same1 + tw_same2

    tw_not_credible1 = [(tweet['created_at1'], tweet['_worker_id'], 0) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet2']
    tw_not_credible2 = [(tweet['created_at2'], tweet['_worker_id'], 0) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet1']
    tw_not_credible = tw_not_credible1 + tw_not_credible2


def count_occurences(tweets):
    tw_credible1 = [(tweet['created_at1'], tweet['text1']) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet1']
    tw_credible2 = [(tweet['created_at2'], tweet['text2']) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet2']
    tw_credible = tw_credible1 + tw_credible2
    count_credible = Counter(tw_credible)

    tw_same1 = [(tweet['created_at1'], tweet['text1']) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'same']
    tw_same2 = [(tweet['created_at2'], tweet['text2']) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'same']
    tw_same = tw_same1 + tw_same2
    count_same = Counter(tw_same)

    tw_not_credible1 = [(tweet['created_at1'], tweet['text1']) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet2']
    tw_not_credible2 = [(tweet['created_at2'], tweet['text2']) for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet1']
    tw_not_credible = tw_not_credible1 + tw_not_credible2
    count_not_credible = Counter(tw_not_credible)

    return count_credible, count_same, count_not_credible


def count_occurences_articles(tweets):
    tw_credible1 = [(tweet['publication_date1'], tweet['title1']) for tweet in tweets if tweet['what_article_is_more_credible'] == 'title1']
    tw_credible2 = [(tweet['publication_date2'], tweet['title2']) for tweet in tweets if tweet['what_article_is_more_credible'] == 'title']
    tw_credible = tw_credible1 + tw_credible2
    count_credible = Counter(tw_credible)

    tw_same1 = [(tweet['publication_date1'], tweet['title1']) for tweet in tweets if tweet['what_article_is_more_credible'] == 'same']
    tw_same2 = [(tweet['publication_date2'], tweet['title2']) for tweet in tweets if tweet['what_article_is_more_credible'] == 'same']
    tw_same = tw_same1 + tw_same2
    count_same = Counter(tw_same)

    tw_not_credible1 = [(tweet['publication_date1'], tweet['title1']) for tweet in tweets if tweet['what_article_is_more_credible'] == 'title']
    tw_not_credible2 = [(tweet['publication_date2'], tweet['title2']) for tweet in tweets if tweet['what_article_is_more_credible'] == 'title1']
    tw_not_credible = tw_not_credible1 + tw_not_credible2
    count_not_credible = Counter(tw_not_credible)

    return count_credible, count_same, count_not_credible


def csv_to_json(path_to_csv):
    csvfile = open(path_to_csv, 'r')
    return list(unicodecsv.DictReader(csvfile))


def ranked_to_csv(path_to_csv, data):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)
        a.writerow(['created_at', 'text', 'score'])
        a.writerows(data)


def results_to_csv(path_to_csv, data):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)
        a.writerow(['date', 'text', 'credible', 'non-credible', 'same'])
        a.writerows(data)


tw1 = csv_to_json('Results/articles_crowd.csv')
counts = count_occurences_articles(tw1)
ranked_tw1 = pairwise_comparison(counts)
ranked_to_csv('articles_crowd_comparison.csv', ranked_tw1)

tw1_results = tweet_results(counts)
results_to_csv('articles_crowd_results.csv', tw1_results)
