# -*- coding: utf-8 -*-
'''
Provides basic access to query the guardian's open platform api and
writes results to a give file.

Example use:
    $ python single.py search -q="facebook"

For more arg details:
    $ python single.py --help

For api use details:
    http://open-platform.theguardian.com/

NOTE: api key is required for use.
api info: http://open-platform.theguardian.com/

NOTE: Lots of results can be returned so this may take a while.

TODO: API seems to only support pagnating to page 176.
date_range.py makes more requests than is needed. prehaps make date chunk size
optional to optimise this better.
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import argparse

import json
import requests


api_key = os.environ['GUARDIAN_API_KEY']
api_url = 'https://content.guardianapis.com/'

search_roots = ('search', 'section', 'tags', '<single_page_url>')

parser = argparse.ArgumentParser(
    description="Access guardian OP API. prints json results to stdout")
parser.add_argument(
    'domain', type=str, help="type of query eg: %s" % repr(search_roots))
parser.add_argument(
    '-q', '--q', type=str, help="query terms")
parser.add_argument(
    '-f', '--file', type=str, help="file to write results to", default="result.json")
# the following will limit results to specific sections or tags.
parser.add_argument(
    '-s', '--section', type=str, help="limit results to section")
parser.add_argument(
    '-t', '--tags', type=str, help="limit results to tags")
args = parser.parse_args()

params = {
    'show-fields': 'all',
    # 'from-date': "2010-01-01",
    'api-key': api_key,
    'show-tags': 'tone,keyword',
    'show-elements': 'all',
    'lang': 'en',
    'page-size': 200,
}

def build_query(args):
    # setup query url.
    url = "{}{}".format(api_url, args.domain)
    if args.domain not in search_roots:
        # we are doing a single no other querys needed.
        return (url, params)
    # we are searching a colletion, add more params.
    args.domain = None
    for k, param in args.__dict__.items():
        if param and k not in ('domian', 'file'):
            params[k] = param
    return (url, params)


def guardian_search(url, params):
    results = []
    # get an initial response if there is an error it will just fail
    r = requests.get(url, params=params)
    data = r.json()
    if "results" not in data['response']:
        print("FAIL:", data['response'])
        return {}
    total_pages = data['response']['pages']
    results = data['response']['results']
    # show results
    print("total pages", total_pages)
    print("total results", data['response']['total'])
    params["page"] = 2
    # adjust if needed. over 5000 a day is the api's limit
    # this takes ages tbh.
    limit = min(total_pages, 300)
    while params["page"] < total_pages:
        try:
            print("...page", params["page"], "of", limit)
            r = requests.get(url, params=params)
            data = r.json()
            if not "results" in data['response']:
                print("FAIL:", data['response'])
                break
            results.extend(data['response']['results'])
            params["page"] += 1
        except KeyboardInterrupt:
            # so if you get bored you can exit and get your progress.
            break
    return results

if __name__ == '__main__':
    url, params = build_query(args)
    result = guardian_search(url, params)

    with open(args.file, "w+") as fp:
        json.dump(result, fp)
    print("wrote results to file:", args.file)
