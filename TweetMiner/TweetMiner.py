__author__ = 'marc'

from TwitterStreamingListener import TwitterStreamingListener
import tweepy
import sys
import time

# Read configuration from config/twitter.cfg
lines = [line.strip() for line in open('config/twitter.cfg')]
consumer_key = lines[0]
consumer_secret = lines[1]
access_token = lines[2]
access_token_secret = lines[3]

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Tweet keyword and user filters
track = [
    '#JapanWhalingAssociation',
    '#InternationalWhalingCommission',
    '#InstituteofCetaceanResearch whale',
    '#UnitedNationsInternationalMaritimeOrganization whale',
    '#AntarcticTreatySystem whale',
    '#Greenpeace whale',
    '#WWF Whale',
    '#OceanAlliance whale',
    '#SeaShepherdConservationSociety',
    '#JapanFisheriesAgency',
    '#whaling',
    '#CommercialWhaling',
    '#NisshinMaru',
    'Commercial whaling',
    'whaling'
]
follow = []


def main():
    """The program starts here
    Make sure twitter.cfg is filled with:
    line 1: consumer_key
    line 2: consumer_secret
    line 3: access_token
    line 4: access_token_secret

    :return: mine tweets in mongodb database
    """
    mine_tweets()


def mine_tweets():
    """Mining tweets using the twitter streaming API

    :param track: list of twitter keywords and/or hashtags
    :return: mined tweets will be stored in a mongodb database
    """

    listen = TwitterStreamingListener(api, ou_type='mongo')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started on %s keywords and %s user ids..." % (len(track), len(follow))

    try:
        stream.filter(track=track, follow=follow)
    except KeyboardInterrupt:
        print "Interrupted by user.. Stopping streaming now.."
        stream.disconnect()
        exit()
    except:
        print "error! %s" % sys.exc_info()[0]
        stream.disconnect()
        time.sleep(60)
        mine_tweets()


if __name__ == '__main__':
    main()
