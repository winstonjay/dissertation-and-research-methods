
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


class TopicModel(object):

    # vectorizer defuault args.
    max_features = 5000
    max_df       = 0.5
    min_df       = 2
    stop_words   = 'english'
    ngram_range  = (1, 2)

    # LDA defualt args.
    n_topics        = 7
    max_iter        = 1000
    learning_offset = 50.0
    random_state    = 0

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.model    = None
        self._topics  = None

    def fit(self, data):
        '''convienience wrapper to return a fitted a
        sklearn.decomposition.LatentDirichletAllocation model.'''
        vectorizer = CountVectorizer(
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.max_features,
            stop_words=self.stop_words,
            ngram_range=self.ngram_range)

        # fit the count vectorizer
        tf_features = vectorizer.fit_transform(data)
        self.labels = vectorizer.get_feature_names()
        # init model.
        self.model = LatentDirichletAllocation(
            n_components=self.n_topics,
            max_iter=self.max_iter,
            learning_method='online',
            learning_offset=self.learning_offset,
            random_state=self.random_state)

        print("Fitting LDA models with tf features, "
              "\nmax_iter=%d. number of topics=%d. "
              "features_shape=(%d, %d)..."
               % (self.max_iter, self.n_topics, *tf_features.shape))

        # this will take a while. reduce max_iter to reduce this.
        t0 = time.time()
        self.model.fit(tf_features)
        print("Model fitted in: {:.2f} secs".format(time.time() - t0))
        return self.model

    def labeled_topics(self, n_samples):
        self._topics = []
        for topic_idx, topic in enumerate(self.model.components_):
            _topic = []
            for i in topic.argsort()[:-n_samples - 1:-1]:
                _topic.append((self.labels[i], topic[i]))
            self._topics.append(_topic)
        return self._topics

    def topics(self, n_samples):
        self._topics = self.labeled_topics(n_samples)
        cat = ', '.join
        return [cat(t for t, _ in topic) for topic in self._topics]

    def inspect(self, n_samples):
        self._topics = self.labeled_topics(n_samples)
        for i, topic in enumerate(self._topics):
            print(f"topic {i}:")
            for sample in topic:
                print("{} ({:.2f})".format(*sample), end=", ")
            print()
    # https://medium.com/ml2vec/topic-modeling-is-an-unsupervised-learning-approach-to-clustering-documents-to-discover-topics-fdfbf30e27df
    def get_topics(self, n_samples):
        word_dict = {}
        self._topics = self.labeled_topics(n_samples)
        for i, topic in enumerate(self._topics):
            word_dict[f'topic {i+1}'] = [t for t, _ in topic]
        return pd.DataFrame(word_dict)