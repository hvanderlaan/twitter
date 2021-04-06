#!/usr/bin/env python3

""" twitter.py - commandline twitter scraper that will display tweets with
                 hashtags of tweets from users.

                 requirements:
                     TwitterSearch (pip install TwitterSearch)
                     twitter developers api credentials

    author : harald van der laan
    date   : 2020-01-22
    version: v2.0.0

    changelog:
        - v2.0.0: Update to use python3
        - v1.0.3: added proxy support
        - v1.0.2: added while loop with sleep of 60 seconds
        - v1.0.1: added support of multiple tag search values
        - v1.0.0: initial version
"""

import sys
import os.path
import argparse
import time
import subprocess
import configparser

try:
    import TwitterSearch
except ImportError:
    sys.stderr.write('[-] import error: could not import TwitterSearch\n')
    sys.exit(1)


def get_args():
    """ function for getting arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--amount', type=int, default=10,
                        help='display amount of tweets')
    parser.add_argument('-c', '--config', default='./twitter.cfg',
                        help='configuration file')
    parser.add_argument('-d', '--daemon', action='store_true',
                        help='automatic refresh every 60 seconds')
    parser.add_argument('-l', '--lang', default='en', choices=['en', 'nl'],
                        help='language of the tweet')
    parser.add_argument('-p', '--proxy', help='proxy server to connect to')
    parser.add_argument('-t', '--tag', nargs='+', default=[],
                        help='display tweets with hashtag')
    parser.add_argument('-u', '--user', help='display tweets from user')

    return parser.parse_args()


def twitter_user_search(ck, cs, at, ats, user, count, proxy=None):
    """ function for twitter search on a twitter user """
    tuo = TwitterSearch.TwitterUserOrder(user)
    if proxy:
        ts = TwitterSearch.TwitterSearch(ck, cs, at, ats, proxy=proxy)
    else:
        ts = TwitterSearch.TwitterSearch(ck, cs, at, ats)

    tweetcount = 0

    for tweet in ts.search_tweets_iterable(tuo):
        if tweetcount < count:
            print(f"@{tweet['user']['screen_name']} - {tweet['created_at']}")
            print(f"{tweet['text']}")
            print(f"")

            tweetcount = tweetcount + 1
        else:
            break


def twitter_tag_search(ck, cs, at, ats, tag, count, lang, proxy=None):
    """ function for twitter search on hashtags and keywords """
    tso = TwitterSearch.TwitterSearchOrder()
    tso.set_keywords(tag)
    if lang == 'en' or lang == 'nl':
        tso.set_language(lang)

    tso.set_result_type('recent')
    if proxy:
        ts = TwitterSearch.TwitterSearch(ck, cs, at, ats, proxy=proxy)
    else:
        ts = TwitterSearch.TwitterSearch(ck, cs, at, ats)

    tweetcount = 0

    for tweet in ts.search_tweets_iterable(tso):
        if tweetcount < count:
            print(f"@{tweet['user']['screen_name']} - {tweet['created_at']}")
            print(f"{tweet['text']}")
            print(f"")
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
        sys.stderr.write('[-] usage: {} [-h|--help]'.format(__file__))
        sys.exit(2)

    if args.user:
        twitter_user_search(consumer_key, consumer_secret, access_token,
                            access_token_secret, args.user, args.amount,
                            args.proxy)
    if args.tag:
        twitter_tag_search(consumer_key, consumer_secret, access_token,
                           access_token_secret, args.tag, args.amount,
                           args.lang, args.proxy)


if __name__ == "__main__":
    ARGS = get_args()

    if os.path.exists(ARGS.config):
        CONF = configparser.ConfigParser()
        CONF.read(ARGS.config)
    else:
        sys.stderr.write(f'[-] config: could not find file: {ARGS.config}')
        sys.stderr.write('\n')
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
