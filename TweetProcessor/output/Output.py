__author__ = 'marc'

import json
import unicodecsv
from bson import json_util
from helpers import TextHelper, UrlHelper
from urlparse import urlparse


def to_json(list_of_objects, file_path='myfile.json'):
    with open(file_path, 'wb') as outfile:
        json.dump(list_of_objects, outfile, default=json_util.default)


def create_csv_from_tweets(headers, rows, filename):
    csv = unicodecsv.writer(open(filename, "wb+"))
    csv.writerow(headers)
    for row in rows:
        csv.writerow(row)


def create_csv_for_tweet_cf_task(tweets, filename):
    headers = [
        "id1", "tweet1", "favorite_count1", "retweet_count1", "source1", "mentions_count1", "hashtags_count1", "url1",
        "id2", "tweet2", "favorite_count2", "retweet_count2", "source2", "mentions_count2", "hashtags_count2", "url2"
    ]

    rows = []
    for key in xrange(0, len(tweets), 2):
        if key < len(tweets)-1:
            tweet1 = [
                tweets[key][u"id_str"],
                TextHelper.remove_linebreaks_from_text(tweets[key][u"text"]),
                tweets[key][u"favorite_count"],
                tweets[key][u"retweet_count"],
                tweets[key][u"source"],
                str(len(tweets[key][u'entities'][u'user_mentions'])),
                str(len(tweets[key][u'entities'][u'hashtags'])),
                ' '.join([UrlHelper.unshorten_url(url[u"expanded_url"]) for url in tweets[key][u"entities"][u'urls']])
            ]

            key += 1

            tweet2 = [
                tweets[key][u"id_str"],
                TextHelper.remove_linebreaks_from_text(tweets[key][u"text"]),
                tweets[key][u"favorite_count"],
                tweets[key][u"retweet_count"],
                tweets[key][u"source"],
                str(len(tweets[key][u'entities'][u'user_mentions'])),
                str(len(tweets[key][u'entities'][u'hashtags'])),
                ' '.join([UrlHelper.unshorten_url(url[u"expanded_url"]) for url in tweets[key][u"entities"][u'urls']])
            ]

            both_tweets = tweet1 + tweet2

            rows.append(both_tweets)

    create_csv_from_tweets(headers, rows, filename)

def create_csv_for_wenjie_task(tweets, filename):
    headers = [
        'id',
        'text',
        'created_at',
        'lang',
        'favorite_count',
        'place',
        'in_reply_to_screen_name',
        'retweet_count',
        'user.followers_count',
        'entities.hashtags',
        'entities.urls.expanded_url',
        'entities.user_mentions.screen_name',
        'entities.media.type'
    ]

    rows = []
    for key in range(0, len(tweets)):

        tweet = [
            tweets[key][u"id_str"],
            TextHelper.remove_linebreaks_from_text(tweets[key][u"text"]),
            tweets[key][u"created_at"],
            tweets[key][u"lang"],
            tweets[key][u"favorite_count"],
            tweets[key][u"place"],
            tweets[key][u"in_reply_to_screen_name"],
            tweets[key][u"retweet_count"],
            tweets[key][u"user"][u'followers_count'],
            ' '.join(hashtag[u'text'] for hashtag in tweets[key][u'entities'][u'hashtags']),
            ' '.join([UrlHelper.unshorten_url(url[u"expanded_url"]) for url in tweets[key][u"entities"][u'urls']]),
            ' '.join(handler[u'screen_name'] for handler in tweets[key][u'entities'][u'user_mentions'])
        ]

        try:
            tweet.append(' '.join(media[u'type'] for media in tweets[key][u'entities'][u'media']))
        except KeyError:
            tweet.append(' ')

        print 'Tweet %i added' % key

        rows.append(tweet)

    create_csv_from_tweets(headers, rows, filename)


def create_csv_for_frankiina_task(tweets, filename):
    headers = [
        'id1',
        'text1',
        'tweet_wiki_entities_count1',
        'tweet_numerical_count1',
        'tweet_uppercase_count1',
        'tweet_user_mentions_count1',
        'tweet_punctuation_count1',
        'tweet_nouns_count1',
        'tweet_url_count1',
        'tweet_favorite_count1',
        'tweet_hashtag_count1',
        'tweet_retweets_count1',
        'tweet_word_count1',
        'user_listed_count1',
        'user_favourites_count1',
        'user_friends_count1',
        'user_statuses_count1',
        'user_followers_count1',
        'url_in_newser100_1',
        'url_in_newser1',
        'has_user_avatar1',
        'has_user_background1',
        'user_is_verified1',
        'has_user_decription1',
        'user_created_at1',
        'tweet_created_at1',
        'sentiwordnet_score1',
        'sentiment140_score1',
        'id2',
        'text2',
        'tweet_wiki_entities_count2',
        'tweet_numerical_count2',
        'tweet_uppercase_count2',
        'tweet_user_mentions_count2',
        'tweet_punctuation_count2',
        'tweet_nouns_count2',
        'tweet_url_count2',
        'tweet_favorite_count2',
        'tweet_hashtag_count2',
        'tweet_retweets_count2',
        'tweet_word_count2',
        'user_listed_count2',
        'user_favourites_count2',
        'user_friends_count2',
        'user_statuses_count2',
        'user_followers_count2',
        'url_in_newser100_2',
        'url_in_newser2',
        'has_user_avatar2',
        'has_user_background2',
        'user_is_verified2',
        'has_user_decription2',
        'user_created_at2',
        'tweet_created_at2',
        'sentiwordnet_score2',
        'sentiment140_score2',
    ]

    rows = []
    for key, tweet in enumerate(tweets):
        next_tweet = key + 1

        if next_tweet > len(tweets)-1:
            break

        tweet1 = _parse_tweet_comparison(tweets, key)
        tweet2 = _parse_tweet_comparison(tweets, next_tweet)
        rows.append(tweet1 + tweet2)
        print 'Tweet %i added' % key

    # link last tweet to the first tweet
    tweet1 = _parse_tweet_comparison(tweets, len(tweets)-1)
    tweet2 = _parse_tweet_comparison(tweets, 0)
    rows.append(tweet1 + tweet2)
    create_csv_from_tweets(headers, rows, filename)


def _parse_tweet_comparison(tweets, key):
    row = [
        tweets[key]['id'],
        tweets[key]['text'],
        tweets[key]['counts']['tweet_wiki_entities_count'],
        tweets[key]['counts']['tweet_numerical_count'],
        tweets[key]['counts']['tweet_uppercase_count'],
        tweets[key]['counts']['tweet_user_mentions_count'],
        tweets[key]['counts']['tweet_punctuation_count'],
        tweets[key]['counts']['tweet_nouns_count'],
        tweets[key]['counts']['tweet_url_count'],
        tweets[key]['counts']['tweet_favorite_count'],
        tweets[key]['counts']['tweet_hashtag_count'],
        tweets[key]['counts']['tweet_retweets_count'],
        tweets[key]['counts']['tweet_word_count'],
        tweets[key]['counts']['user_listed_count'],
        tweets[key]['counts']['user_favourites_count'],
        tweets[key]['counts']['user_friends_count'],
        tweets[key]['counts']['user_statuses_count'],
        tweets[key]['counts']['user_followers_count'],
        tweets[key]['completeness']['url_in_newser100'],
        tweets[key]['completeness']['url_in_newser'],
        tweets[key]['completeness']['has_user_avatar'],
        tweets[key]['completeness']['has_user_background'],
        tweets[key]['completeness']['user_is_verified'],
        tweets[key]['completeness']['has_user_description'],
        tweets[key]['dates']['user_created_at'],
        tweets[key]['dates']['tweet_created_at'],
        tweets[key]['sentiment']['sentiwordnet'],
        tweets[key]['sentiment']['sentiment140']
    ]

    return row

# def _parse_tweet_cf(tweets, key):
#     parsed_urls = []
#     for url in tweets[key][u"entities"][u'urls']:
#         full_url = UrlHelper.unshorten_url(url[u"expanded_url"])
#         parsed_uri = urlparse(full_url)
#         domain = '{uri.netloc}'.format(uri=parsed_uri)
#         parsed_url = '<a class="label label-success" href="%s" target="blank">%s</a>' % (url[u'expanded_url'], domain)
#         parsed_urls.append(parsed_url)
#
#     parsed_hashtags = []
#     for hashtag in tweets[key][u"entities"][u"hashtags"]:
#         parsed_hashtag = '<a class="label label-default" href="https://www.twitter.com/hashtag/%s" target="blank">#%s</a>' % (hashtag['text'], hashtag['text'])
#         parsed_hashtags.append(parsed_hashtag)
#
#     parsed_handles = []
#     for handle in tweets[key][u"entities"][u"user_mentions"]:
#         parsed_handle = '<a class="label label-primary" href="https://www.twitter.com/%s" target="blank">@%s</a>' % (handle['screen_name'], handle['screen_name'])
#         parsed_handles.append(parsed_handle)
#
#     tweet = [
#         tweets[key][u"id_str"],
#         TextHelper.remove_linebreaks_from_text(tweets[key][u"text"]),
#         tweets[key][u"favorite_count"],
#         tweets[key][u"retweet_count"],
#
#         tweets[key][u"user"][u'id'],
#         tweets[key][u"user"][u'statuses_count'],
#         tweets[key][u"user"][u'friends_count'],
#         not tweets[key][u"user"][u'default_profile_image'],
#
#         tweets[key][u"user"][u'favourites_count'],
#         tweets[key][u"user"][u'listed_count'],
#         tweets[key][u"user"][u'followers_count'],
#         bool(tweets[key][u"user"][u'url']),
#         bool(tweets[key][u"user"][u'description']),
#         tweets[key][u"user"][u'verified'],
#         tweets[key][u"user"][u'created_at'],
#
#         ' '.join(parsed_hashtags),
#         ' '.join(parsed_urls),
#         ' '.join(parsed_handles)
#     ]
#
#     return tweet
