# -*- coding: utf-8 -*-
'''
spamfilter.py

Performs basic spam filtering on tweets using hashtag frequencies.

'''
# TODO: this is a bit of a quick fix for now. If needed in the future
# work out a better strategy and refine implementation.
import collections

class HashtagSpamFilter(object):
    '''keep track of frequently occuring lists of hashtags, for tweets with a
    given minimum number of hashtags. If the number of ouccuracnes reaches a
    given threshold we will say that all any more that occur are spam.'''

    def __init__(self, floor=4, ceil=10, lim=20):
        self.ceil  = ceil
        self.floor = floor
        self.lim = lim
        self.maybe_spam = collections.Counter()
        self.spam = set()
        self.n = 0

    def filter_tags(self, tags, tags_n):
        # if the tag count is too high or we have seen the exact same
        # collection before we will say that it is spam.
        if tags_n > self.ceil or tags in self.spam:
            self.n += 1
            return True
        # if the tag count is high and the frequency of these tags within
        # the collection is unaturally high filter all future occurances.
        if tags_n > self.floor:
            if self.maybe_spam[tags] >= self.lim:
                del self.maybe_spam[tags]
                self.spam.add(tags)
                self.n += 1
                return True
            self.maybe_spam[tags] += 1
        return False

    def stats(self):
        "return some printable stats to monitor."
        return ("spam_sets={} | maybe_spam={} | spam={}".format(
                len(self.spam), len(self.maybe_spam), self.x))