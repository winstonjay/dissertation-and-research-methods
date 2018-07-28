'''
collect.py : collect content to analyse from selected pages based
primarily on html tags and links.
'''
import urllib.parse
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

import json


def main():
    root = 'http://www.occupywallst.org/'
    with open('data/occupy.json', 'w+') as fp:
        json.dump(crawl(root), fp, indent=2)


def crawl(root):

    print('root', root)
    links = set()
    pages = defaultdict(list)
    max_depth = 3

    def _crawl(url, depth=0):
        print('visiting: %s' % url)
        for link in get_urls(get_page(url)):
            pages[url].append(link)
            if link in links:
                continue
            links.add(link)
            if valid_link(link) and depth <= max_depth:
                new_url = urllib.parse.urljoin(root, link)
                _crawl(new_url, depth+1)

        return {'total': len(links),
                'unique': list(links),
                'pages': pages}

    def valid_link(link):
        if not link:
            return False
        bars = set(['tel:', 'mailto:', '//', '@', '#', '.pdf'])
        return ((link.startswith(root) and link != root)
                or not any(x in link for x in bars))

    return _crawl(root)

def get_urls(page):
    soup = BeautifulSoup(page, 'html.parser')
    return (a.get('href') for a in soup.find_all('a'))

def get_page(url):
    r = requests.get(url, cookies={})
    if r.status_code == requests.codes.ok:
        r.raise_for_status()
    return r.text


if __name__ == '__main__':
    main()