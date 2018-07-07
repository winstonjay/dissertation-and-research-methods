# -*- coding: utf-8 -*-
'''
twitter_pages.py :

Retrieve User objects Twitter search results and write to file in newline json
format, one user per line.

Sample usage:
    python twitter_search.py -o foo.ndjson 'bar' --limit=10

For more details:
    python twitter_search.py --help

NOTE: Requires app authentication from https://apps.twitter.com/ with read -
write privileges. You set your authentication tokens as enviroment varibles
that the app provides.

Enviroment varibles need to be set. this can be done by creating a .env file
as follows:

    TWITTER_CONSUMER_KEY=your_consumer_key
    TWITTER_CONSUMER_SECRET=your_consumer_secret
    TWITTER_ACCESS_TOKEN=your_access_Token
    TWITTER_ACCESS_TOKEN_SECRET=your_access_Token_secret

You can then set the env varibles with:

    $ for line in $(cat .env); do export $line; done

Alternatively just set your env varibles directly. Search 'EDIT_HERE' to see
where to do this.

Twitter user object ref:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html

Tweepy library ref:
    http://tweepy.readthedocs.io/en/v3.5.0/api.html#user-methods
'''
from __future__ import print_function

import argparse
import json
import os

import tweepy

# EDIT_HERE: You can just replace all of this by just setting your env
# varibles directly.
consumer_key        = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret     = os.environ['TWITTER_CONSUMER_SECRET']
access_token        = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# init api.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,
                wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True)

def main():
    args = parse_args()
    print("performing search...")
    # write user json objects line by line to the output file.
    with open(args.out, 'w') as fp:
        i = 0
        for user in search_users(args.q, limit=args.limit):
            fp.write(user_json(user))
            if i % 10 == 0:
                progress = 'progress: {}/{}'.format(i, args.limit)
                print(progress, end="\r", flush=True)
            i += 1
    print('finished. {}/{}'.format(i, args.limit))


def search_users(q, limit):
    'wrapper for tweepy cursor iterator that yields User objects'
    # Tweepy ref:
    # API.search_users(q[, per_page][, page]) -> list of User objects
    cursor = tweepy.Cursor(api.search_users, q=q)
    for user in cursor.items(limit):
        yield user

def user_json(user):
    'convert tweepy User object into a json string'
    return '{}\n'.format(json.dumps(user._json))

def parse_args():
    'Parse args and return formatted args.'
    parser = argparse.ArgumentParser()
    parser.add_argument('q', type=str, help='query param.')
    parser.add_argument(
        '-o',
        '--out',
        type=str,
        help='output file path',
        default='out.ndjson')
    parser.add_argument(
        '-l',
        '--limit',
        type=int,
        default=100)
    return parser.parse_args()

if __name__ == '__main__':
    main()