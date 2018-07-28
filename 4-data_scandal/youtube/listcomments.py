# -*- coding: utf-8 -*-
"get comments from and individual video by video id."
# Most of the code is just straigh lifted of their demo site with only some
# extra glue bits to get multiple pages of reposnses. Again just another quick
# make do script.
#
# REFERENCES: https://developers.google.com/youtube/v3/docs/commentThreads
#
# NOTE:
#   To use this program, you must provide a developer key obtained in the
#   Google APIs Console. Add your on key to a '.env_key' file or Search for
#   "REPLACE_ME" in this code to find the correct place to provide that key.
import os
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

with open(".env") as env:
    DEVELOPER_KEY = env.read().strip() # REPLACE_ME

def get_authenticated_service():
  # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  # credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)

def print_response(response):
  print(json.dumps(response))

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def comment_threads_list_by_video_id(client, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)
  response = client.commentThreads().list(
    **kwargs
  ).execute()
  return response


if __name__ == '__main__':

  import sys
  if len(sys.argv) < 2:
    print("need video id arg!")
    sys.exit(1)

  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()
  kwargs = dict(part='snippet,replies', videoId=sys.argv[1], maxResults=100)

  items = []
  for _ in range(30):
    response = comment_threads_list_by_video_id(client, **kwargs)
    items.extend(response["items"])
    if "nextPageToken" in response:
        kwargs.update({"pageToken": response["nextPageToken"]})
    else:
        break

  print(len(items))
  print_response(items)