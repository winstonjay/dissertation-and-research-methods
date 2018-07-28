# -*- coding: utf-8 -*-
'''
preprocess2.py

proccess twitter data collected twitter_go_v1 tool

usage: update
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from datetime import datetime
import json
import re
import os
import zipfile
import argparse

from spamfilter import HashtagSpamFilter


# TODO: restructure and refactor spam detection to loop though the data first
# before writing any data. This is kinda a mess but probs wont fix.
def write_data(filename, out_filename, spam_filter):
    '''read zip archive of .ndjson files and write to a single file then
    compress into a new zip archieve.'''
    # set up scoped function varibles
    i = 0
    tmp_filename = "__" + out_filename
    with open(tmp_filename, "w") as tmp_file:
        print("Started writing to file:", tmp_filename)
        with zipfile.ZipFile(filename) as z:
            for fn in z.namelist()[1:]:
                print("reading:", fn, "|", spam_filter.stats())
                with z.open(fn) as f:
                    for line in extract_tweets(f, spam_filter):
                        print(line, file=tmp_file)
                        i += 1
    # log result
    print("Finished first loop:", tmp_filename)
    print("removing excess spam from:", tmp_filename)
    with open(out_filename, "w") as out_file:
        with open(tmp_filename) as tmp_file:
            for line in tmp_file:
                w0, w1, tags = line.split("\t")
                if tags.strip() in spam_filter.spam:
                    spam_filter.x += 1
                    continue
                out_file.write(line)
    print(spam_filter.stats())
    print("Spam examples")
    for s in spam_filter.spam:
        print("\t", s)

    # compress tmp file into local zip.
    print("Total tweets:", i)
    print("spam percent=", (spam_filter.x / i) * 100)
    print("compressing file...")
    z_filename = out_filename + ".zip"
    with zipfile.ZipFile(z_filename, "w") as z:
        z.write(out_filename, compress_type=zipfile.ZIP_DEFLATED)
    print("wrote to file", z_filename)
    # clean up temp files.
    for f in (tmp_filename, out_filename):
        print("cleaning up uncompressed file:", f)
        os.remove(f)


def extract_tweets(f, spam_filter):
    "extract tweet created_at, tags and text from each tweet json object."
    for line in f:
        t = json.loads(line)
        tags, tags_n = extract_hashtags(t["extended_tweet"]["entities"])
        if not tags or spam_filter.filter_tags(tags, tags_n):
            continue
        text = extract_text(t["extended_tweet"]["full_text"])
        if not text:
            continue
        time = datetime.strptime(t["created_at"], time_read)
        time_str = time.strftime(time_write)
        yield tab([time_str, text, tags or "null"])

tab = "\t".join
time_read  = "%a %b %d %H:%M:%S +0000 %Y"
time_write = "%d/%m/%Y %H:%M:%S"


def extract_text(text):
    '''clean_line converts the text to lowercase remove all non words,
    stopwords, non ascii characters and links and groups all corpora specfic
    terms so that they will be processed as one entity. Eg: Hello World ->
    hello_world.'''
    s = re.sub(r'[^\x00-\x7F]+|\n|http\S+', ' ', text.lower())
    return cat(w for w in rx.findall(s)
                if 3 < len(w) < 20
                if w not in stop_words)


rx = re.compile(r"[#@]\w+|\w+")

cat = " ".join

stop_words_path = "../resources/stopwords.txt"
stop_words = set(open(stop_words_path).read().split())


def extract_hashtags(entities):
    "gets tags tweet by tweet returning their names seperated by spaces."
    tags = [t['text'] for t in entities["hashtags"]]
    return (cat(tags), len(tags)) if is_ascii(tags) else (None, -1)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="proccess twitter data collected twitter_go_v1 tool")
    parser.add_argument(
        "-f", "--file", type=str, help="input filename", required=True)
    parser.add_argument(
        "-o", "--out", type=str, help="output filename", required=True)
    args = parser.parse_args()

    write_data(args.file, args.out, HashtagSpamFilter())
    print("done!")
