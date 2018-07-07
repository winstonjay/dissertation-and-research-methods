# -*- coding: utf-8 -*-
'''
Bulk access articles from the guardian open platform api per date range.
Writes a day of artiles per .ndjson line as a json object.

NOTE: api key is required for use.
api info: http://open-platform.theguardian.com/

Example use:
    $ python date_range.py -a="2018-03-17" -z="2018-03-24" -q="cats"

For more arg details:
    $ python date_range.py --help

For api use details:
    http://open-platform.theguardian.com/

refs:
    https://gist.github.com/dannguyen/c9cb220093ee4c12b840

'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import argparse
import json

from datetime import datetime, timedelta

import requests

api_key = os.environ['GUARDIAN_API_KEY']
api_url = 'https://content.guardianapis.com/search'

params = {
    'from-date': "",
    'to-date': "",
    'show-fields': 'all',
    'api-key': api_key,
    'show-tags': 'tone,keyword',
    'show-elements': 'all',
    'lang': 'en',
    'page-size': 200,
}

parser = argparse.ArgumentParser(
    description="Access guardian OP API. prints json results to stdout")

# for more details about api params
# http://open-platform.theguardian.com/documentation/
parser.add_argument('-q', '--query', type=str, required=True,
                    help="query string keywords")
parser.add_argument('-o', '--out_filename', default="data.ndjson",
                    help="output name of .ndjson")
parser.add_argument('-a', '--start_date', type=str, required=True,
                    help="start-date: YYYY-DD-MM")
parser.add_argument('-z', '--end_date', type=str, required=True,
                    help="end-date: YYYY-DD-MM")
args = parser.parse_args()

# make sure the date entered is valid and in the correct format to avoid
# any confusions. This is the same format the api uses.
#   eg: 2009-22-01 (YYYY-DD-MM).
date_format = "%Y-%m-%d"
try:
    start_date = datetime.strptime(args.start_date, date_format)
    end_date   = datetime.strptime(args.end_date, date_format)
except ValueError as e:
    raise e

# add a query if we have one. if not we just get all articles.
if args.query:
    print("keyword query={}".format(args.query))
    params["q"] = args.query
else:
    print("collecting all articles")

print("from: {}. to: {}.".format(start_date, end_date))

def date_range(start_date, end_date, increment=1):
    for day_delta in range((end_date-start_date).days + increment):
        day = start_date + timedelta(days=day_delta)
        yield day

with open(args.out_filename, "w") as out_file:
    print("Outputing contents to file:", args.out_filename)
    for date in date_range(start_date, end_date):
        results = []
        date_str = date.strftime(date_format)
        print("Fetching articles from:", date_str)
        params["from-date"] = date_str
        params["to-date"]   = date_str
        params["page"] = 1
        total_pages = 2
        while params["page"] < total_pages:
            print("...page", params["page"])
            r = requests.get(api_url, params=params)
            data = r.json()
            results.extend(data['response']['results'])
            params["page"] += 1
            total_pages = data['response']['pages']
            print("total_pages", total_pages)
        out_file.write(json.dumps(results))
        out_file.write("\n")
print("fin.")