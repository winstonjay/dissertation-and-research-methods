import json
import csv
import os
import pprint
import re


def parse_folder(root, name):
    keys = load_keys(os.path.join(root, f'{name}.map.csv'))
    data = load_filtered(os.path.join(root, f'{name}.ndjson'), keys)
    if len(data) == 0:
        return []

    if 'id_str' in data[0]:
        return twitter_parse(data)
    else:
        return youtube_parse(data)


def load_filtered(path, keys):
    rows = []
    with open(path) as fp:
        for i, line in enumerate(fp):
            if i in keys:
                rows.append(json.loads(line))
    return rows

def load_keys(path):
    with open(path) as fp:
        return set(int(row['idx']) for row in csv.DictReader(fp))


def twitter_parse(data):
    urls = []
    for d in data:
        urls.extend(twitter_url(d['entities']))
    return urls


def youtube_parse(data):
    urls = []
    for d in data:
        snippet = d.get('snippet')
        if snippet:
            urls.extend(youtube_url(snippet['description']))
    return urls

def youtube_url(a):
    matches = url_pattern.findall(a)
    return [''.join(m) for m in matches] if matches else []

# https://stackoverflow.com/questions/161738/what-is-the-best-regular-expression-to-check-if-a-string-is-a-valid-url
url_pattern = re.compile(
    r'''(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))''')

def twitter_url(a):
    page_url = a.get('url', None)
    urls = []
    if page_url:
        urls.append(twitter_urlex(page_url['urls'][0]))
    desc_urls = a['description']['urls']
    if desc_urls:
        for u in desc_urls:
            urls.append(twitter_urlex(u))
    return urls

def twitter_urlex(u):
    url = u.get("expanded_url", None)
    if url is None or url == 'null':
        url = u.get('url', None)
    return url.lower()

def append_urls(urls, name):
    with open(f'data/{name}_urls', 'a+') as fp:
        for url in urls:
            fp.write(url)
            fp.write('\n')


if __name__ == '__main__':
    for site in ('youtube', 'twitter'):
        root = f'data/{site}'
        for name in os.listdir(root):
            if name.startswith('_'):
                continue
            path = os.path.join(root, name)
            urls = parse_folder(path, name)
            append_urls(urls, name)
