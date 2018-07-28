# -*- coding: utf-8 -*-
'''
youtube_pages.py :

This sample executes a search request for the specified search term,
writing the results to file in newline json format, one channel object
per line.

Sample usage:
    python youtube_search.py -o foo.ndjson 'bar' --limit=10

For more details:
    python youtube_search.py --help

NOTE: you must provide a developer key obtained in the Google APIs
Console. Search for "EDIT_HERE" in this code to find the correct place
to provide that key..

Enviroment varibles need to be set. this can be done by creating a .env file
as follows:

    TWITTER_CONSUMER_KEY=your_consumer_key
    TWITTER_CONSUMER_SECRET=your_consumer_secret
    TWITTER_ACCESS_TOKEN=your_access_Token
    TWITTER_ACCESS_TOKEN_SECRET=your_access_Token_secret

You can then set the env varibles with:

    $ for line in $(cat .env); do export $line; done

search refs:
https://developers.google.com/youtube/v3/docs/search
https://developers.google.com/youtube/v3/docs/standard_parameters

channel refs:
https://developers.google.com/youtube/v3/docs/channels
https://developers.google.com/youtube/v3/docs/channels/list
'''
from __future__ import print_function

import argparse
import json
import os

from apiclient.discovery import build

# EDIT_HERE: You can just replace all of this by just setting your env
# varibles directly.
DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES           = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION      = 'v3'

client = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)


def main():
    args = parse_args()
    print("performing search...")
    with open(args.out, 'w') as fp:
        i = 0
        for channel in search_channels(args.q, args.limit):
            try:
                channel_id = channel['id']['channelId']
            except KeyError as e:
                print(e, channel)
            fp.write(get_channel(channel_id))
            if i % 10 == 0:
                progress = 'progress: {}/{}'.format(i, args.limit)
                print(progress, end="\r", flush=True)
            i += 1
    print('finished. {}/{}'.format(i, args.limit))


def get_channel(channel_id):
    'for a given id return a detailed list of properties'
    response = client.channels().list(
        id=channel_id,
        part='id,snippet,statistics'
    ).execute()
    return '{}\n'.format(json.dumps(response['items'][0]))

def search_channels(q, limit):
    'search for channels based on query params'
    max_step = 50
    kwargs = dict(q=q,
                  part='id',
                  maxResults=max_step,
                  type='channel')
    for page in range(1, limit, max_step):
        response = client.search().list(**kwargs).execute()
        for channel in response.get("items", []):
            yield channel
        kwargs['pageToken'] = response.get('nextPageToken')

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
        default=20)
    return parser.parse_args()

if __name__ == '__main__':
    main()