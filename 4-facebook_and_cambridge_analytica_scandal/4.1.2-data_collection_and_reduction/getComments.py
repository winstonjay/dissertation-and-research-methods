# -*- coding: utf-8 -*-
"get comments from and individual video by video id."
# Most of the code is just straigh lifted of their demo site with only some
# extra glue bits to get multiple pages of reponses. Again just another quick
# make do script.
#
# REFERENCES: https://developers.google.com/youtube/v3/docs/commentThreads
#
# NOTE:
#   To use this program, you must provide a developer key obtained in the
#   Google APIs Console. Add your on key to a '.env_key' file or Search for
#   "REPLACE_ME" in this code to find the correct place to provide that key.
import argparse
import os
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    client = get_authenticated_service()
    kwargs = dict(part='snippet,replies',
                  videoId=args.video_id,
                  maxResults=100)
    print('collecting from video {}'.format(args.video_id))
    data = collect_all_comments(client, **kwargs)
    print('collected {} comments'.format(len(data)))
    write_data(args.out, data)


def collect_all_comments(client, **kwargs):
    items = []
    i = 1
    while True:
        print(f"collecting page {i}")
        i += 1
        try:
            response = comment_threads_list_by_video_id(client, **kwargs)
        except HttpError:
            break
        items.extend(response["items"])
        if "nextPageToken" not in response:
            break
        kwargs.update({"pageToken": response["nextPageToken"]})
    return items

def write_data(path, data):
    'write data to json file.'
    with open(path, 'w') as fp:
        json.dump(data, fp)


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES           = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION      = 'v3'

# REPLACE_ME (if needed)
DEVELOPER_KEY = os.environ.get('YOUTUBE_DEVELOPER_KEY')

def get_authenticated_service():
    'get_authenticated_service uses googleapiclient to create a service.'
    return build(API_SERVICE_NAME,
                 API_VERSION,
                 developerKey=DEVELOPER_KEY)

def remove_empty_kwargs(**kwargs):
    'Remove keyword arguments that are not set'
    if kwargs is None:
        return {}
    return {k: v for k, v in kwargs.items() if v}

def comment_threads_list_by_video_id(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.commentThreads().list(**kwargs).execute()
    return response

parser = argparse.ArgumentParser()
parser.add_argument(
    'video_id', type=str, help='Youtube video id.')
parser.add_argument(
    '-o', '--out', type=str, help='output filename', default='out.json')
args = parser.parse_args()

if __name__ == '__main__':
    main()