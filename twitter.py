#!/usr/bin/env python

""" twitter.py - commandline twitter scraper that will display tweets with hashtags of tweets
                 from users.

                 requirements:
                     TwitterSearch (pip install TwitterSearch)
                     twitter developers api credentials

    author : harald van der laan
    date   : 2017/09/08
    version: v1.0.2

    changelog:
        - v1.0.2: added while loop with sleep of 60 seconds
        - v1.0.1: added support of multiple tag search values
        - v1.0.0: initial version
"""

from __future__ import print_function, unicode_literals

import sys
import os.path
import argparse
import time
import subprocess
import ConfigParser

try:
    from TwitterSearch import *
except ImportError:
    sys.stderr.write('[-] import error: could not import TwitterSearch\n')
    sys.exit(1)

def get_args():
    """ function for getting arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--amount', type=int, default=10,
                        help='display amount of tweets')
    parser.add_argument('-c', '--config', default='./twitter.cfg', help='configuration file')
    parser.add_argument('-d', '--daemon', action='store_true', help='automatic refresh every 60 seconds')
    parser.add_argument('-l', '--lang', default='en', choices=['en', 'nl'],
                        help='language of the tweet')
    parser.add_argument('-t', '--tag', nargs='+', default=[],
                        help='display tweets with hashtag')
    parser.add_argument('-u', '--user', help='display tweets from user')

    return parser.parse_args()

def twitter_user_search(ck, cs, at, ats, user, count):
    """ function for twitter search on a twitter user """
    tuo = TwitterUserOrder(user)
    ts = TwitterSearch(ck, cs, at, ats)
    tweetcount = 0

    for tweet in ts.search_tweets_iterable(tuo):
        if tweetcount < count:
            print('@{} - {}\n{}\n' .format(tweet['user']['screen_name'], tweet['created_at'],
                                           tweet['text']))
            tweetcount = tweetcount + 1
        else:
            break

def twitter_tag_search(ck, cs, at, ats, tag, count, lang):
    """ function for twitter search on hashtags and keywords """
    tso = TwitterSearchOrder()
    tso.set_keywords(tag)
    if lang == 'en' or lang == 'nl':
        tso.set_language(lang)
    tso.set_result_type('recent')
    ts = TwitterSearch(ck, cs, at, ats)
    tweetcount = 0

    for tweet in ts.search_tweets_iterable(tso):
        if tweetcount < count:
            print('@{} - {}\n{}\n' .format(tweet['user']['screen_name'], tweet['created_at'],
                                           tweet['text']))
            tweetcount = tweetcount + 1
        else:
            break

def main(args, conf):
    """ main function for putting it all together """
    consumer_key = conf.get('twitter', 'consumerkey')
    consumer_secret = conf.get('twitter', 'consumersecret')
    access_token = conf.get('twitter', 'accesstoken')
    access_token_secret = conf.get('twitter', 'accesstokensecret')

    if not args.user and not args.tag:
        sys.stderr.write('[-] usage: {} [-h] [-a AMOUNT] [-c CONFIG] [-l en,nl] [-t TAG] [-u USER]\n'.format(__file__))
        sys.exit(2)

    if args.user:
        twitter_user_search(consumer_key, consumer_secret, access_token, access_token_secret,
                            args.user, args.amount)
    if args.tag:
        twitter_tag_search(consumer_key, consumer_secret, access_token, access_token_secret,
                           args.tag, args.amount, args.lang)

if __name__ == "__main__":
    ARGS = get_args()

    if os.path.exists(ARGS.config):
        CONF = ConfigParser.ConfigParser()
        CONF.read(ARGS.config)
    else:
        sys.stderr.write('[-] config: could not find file: {}\n' .format(ARGS.config))
        sys.exit(1)

    if ARGS.daemon:
        try:
            while True:
                subprocess.Popen('clear')
                main(ARGS, CONF)
                time.sleep(60)
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        subprocess.Popen('clear')
        main(ARGS, CONF)
        sys.exit(0)
