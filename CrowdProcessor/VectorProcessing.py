__author__ = 'marc'

import unicodecsv
import Metrics
from operator import itemgetter


def get_data_from_csv(path_to_csv):
    csvfile = open(path_to_csv, 'r')
    return list(unicodecsv.DictReader(csvfile))


def prepocess_vectors(tweets):
    tw_credible1 = [
        [tweet['_worker_id'], '%s/%s' %(tweet['created_at1'], tweet['created_at2']), 1, 0, 0] + get_features(tweet)
        for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet1'
    ]

    tw_credible2 = [
        [tweet['_worker_id'], '%s/%s' %(tweet['created_at2'], tweet['created_at1']), 1, 0, 0] + get_features(tweet)
        for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet2'
    ]

    tw_same1 = [
        [tweet['_worker_id'], '%s/%s' %(tweet['created_at1'], tweet['created_at2']), 0, 1, 0] + get_features(tweet)
        for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'same'
    ]

    tw_same2 = [
        [tweet['_worker_id'], '%s/%s' %(tweet['created_at2'], tweet['created_at1']), 0, 1, 0] + get_features(tweet)
        for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'same'
    ]

    tw_not_credible1 = [
        [tweet['_worker_id'], '%s/%s' % (tweet['created_at1'], tweet['created_at2']), 0, 0, 1] + get_features(tweet)
        for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet2'
    ]

    tw_not_credible2 = [
        [tweet['_worker_id'], '%s/%s' %(tweet['created_at2'], tweet['created_at1']), 0, 0, 1] + get_features(tweet)
        for tweet in tweets if tweet['what_tweet_is_more_credible'] == 'tweet1'
    ]

    return tw_credible1 + tw_credible2 + tw_same1 + tw_same2 + tw_not_credible1 + tw_not_credible2


def get_features(tweet):
    return [
        int(bool(tweet['resultauthorname1']) | bool(tweet['resultauthorname2'])),
        int(bool(tweet['resultinteraction1']) | bool(tweet['resultfavourited2'])),
        int(bool(tweet['resultfriendlists1']) | bool(tweet['resultfriendlists2'])),
        int(bool(tweet['resulthandles1']) | bool(tweet['resulthandles2'])),
        int(bool(tweet['resulthashtags1']) | bool(tweet['resulthashtags2'])),
        int(bool(tweet['resultretweets1']) | bool(tweet['resultretweets2'])),
        int(bool(tweet['resulturl1']) | bool(tweet['resulturl2'])),
        int(bool(tweet['resultuserfavourites1']) | bool(tweet['resultuserfavourites2'])),
        int(bool(tweet['resultuserfollowers1']) | bool(tweet['resultuserfollowers2'])),
        int(bool(tweet['resultuserfriends1']) | bool(tweet['resultuserfriends2'])),
        int(bool(tweet['resultuserstatuses1']) | bool(tweet['resultuserstatuses2'])),
        int(bool(tweet['resultuserverified1']) | bool(tweet['resultuserverified2']))
    ]


def get_unit_vectors(rows):
    workers = Metrics.groupby_element(rows, 0, 2, 17)
    worker_vectors = [(worker, Metrics.get_group_vector(worker_matrix)) for worker, worker_matrix in workers]
    return worker_vectors


def get_worker_vectors(rows):
    features = Metrics.groupby_element(rows, 0, 2, 17)
    feature_vectors = [(feature, Metrics.get_group_vector(feature_matrix)) for feature, feature_matrix in features]
    return feature_vectors


def process_tweet_vectors(rows):
    tweets = Metrics.groupby_element(rows, 1, 2, 17)
    tweet_vectors = [(tweet, Metrics.get_group_vector(tweet_matrix)) for tweet, tweet_matrix in tweets]
    return append_rows_with_cosine(rows, 1, tweet_vectors, 2, 17)


def process_tweet_credibility_vectors(rows):
    tweets = Metrics.groupby_element(rows, 1, 2, 5)
    score_vectors = get_credibility_scores(tweets)
    score_matrix = get_score_matrix(score_vectors)
    scores_to_csv('Output/scores_t2.csv', score_matrix)
    tweet_vectors = [(tweet, Metrics.get_group_vector(tweet_matrix)) for tweet, tweet_matrix in tweets]
    return append_rows_with_cosine(rows, 1, tweet_vectors, 2, 5)


def get_score_matrix(score_vectors):
    matrix = []
    for tweet_combi, vector in score_vectors:
        tweet_split = tweet_combi.split('/')
        matrix.append([tweet_split[0], (tweet_split[1], sum(vector))])
    grouped = Metrics.groupby_one_element(matrix, 0, 1)

    table = []
    for group in grouped:
        aggr = Metrics.groupby_one_element(group[1], 0, 1)
        aggr = [(id, sum(counts)) for (id, counts) in aggr]
        aggr.append((group[0], 'x'))
        table.append([group[0], aggr])

    return table


def process_worker_vectors(rows, worker_vectors):
    worker_vector_to_csv('Output/worker_vector_t2.csv', worker_vectors)
    return append_rows_with_cosine(rows, 0, worker_vectors, 2, 17)

def process_tweet_features_vectors(rows, feature_vectors):
    #feature_vector_to_csv('Output/feature_vector_t2.csv', feature_vectors)
    return append_rows_with_cosine(rows, 1, feature_vectors, 5, 17)


def append_rows_with_cosine(rows, group_index, group_vectors, start_unit_vector_index, end_unit_vector_index):
    for row in rows:
        group_vector = [group_vector[1] for group_vector in group_vectors if group_vector[0] == row[group_index]]
        unit_vector = row[start_unit_vector_index:end_unit_vector_index]
        row.append(Metrics.get_cosine_similarity(unit_vector, group_vector))
    return rows


def get_credibility_scores(tweet_cred_vectors):
    credibility_vectors = []
    for tweet_id, cred_vectors in tweet_cred_vectors:
        credibility_vector = []
        for cred_vector in cred_vectors:
            if cred_vector[1] == 1:
                credibility_vector.append(0)
            else:
                credibility_vector.append(1)

        credibility_vectors.append((tweet_id, credibility_vector))
    return credibility_vectors


def results_to_csv(path_to_csv, vector):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)
        a.writerow(['worker_id', 'tweet_id', 'credible', 'non-credible', 'same', 'author_name', 'favourited', 'author_friendlists',
                    'handles', 'hashtags', 'retweets', 'urls', 'author_favourites', 'author_followers', 'author_friends',
                    'author_statuses', 'author_verified', 'worker_similarity', 'tweet_similarity', 'tweet_credibility_similarity',
                    'tweet_feature_similarity'])
        for row in vector:
            a.writerow(row)


def scores_to_csv(path_to_csv, vector):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)

        for tweet in vector:
            sorted_tweet = (sorted(tweet[1], key=itemgetter(0)))
            a.writerow([''] + [tweet_id for (tweet_id, scores) in sorted_tweet])
            break

        for tweet in vector:
            sorted_tweet = (sorted(tweet[1], key=itemgetter(0)))
            a.writerow([tweet[0]] + [scores for (tweet_id, scores) in sorted_tweet])


def feature_vector_to_csv(path_to_csv, vector):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)
        a.writerow(['tweet_id', 'f1_author_name', 'f2_favourited', 'f3_author_friendlists',
                    'f4_handles', 'f5_hashtags', 'f6_retweets', 'f7_urls', 'f8_author_favourites', 'f9_author_followers', 'f10_author_friends',
                    'f11_author_statuses', 'f12_author_verified'])

        for row in vector:
            tweet_id, feature_vector = row
            a.writerow([tweet_id] + [str(feature) for feature in feature_vector])


def worker_vector_to_csv(path_to_csv, vector):
    with open(path_to_csv, 'w') as fp:
        a = unicodecsv.writer(fp)
        a.writerow(['worker_id', 'credible', 'same', 'non-credible', 'f1_author_name', 'f2_favourited', 'f3_author_friendlists',
                    'f4_handles', 'f5_hashtags', 'f6_retweets', 'f7_urls', 'f8_author_favourites', 'f9_author_followers', 'f10_author_friends',
                    'f11_author_statuses', 'f12_author_verified'])
        for row in vector:
            worker_id, feature_vector = row
            a.writerow([worker_id] + [str(feature) for feature in feature_vector])


tw1 = get_data_from_csv('Results/2tw.csv')
rows = prepocess_vectors(tw1)
rows = process_worker_vectors(rows, get_worker_vectors(rows))
rows = process_tweet_vectors(rows)
rows = process_tweet_credibility_vectors(rows)
rows = process_tweet_features_vectors(rows)
rows = Metrics.replace_nan_to_zero(rows)
results_to_csv('Output/worker_vector_tweets1.csv', rows)
