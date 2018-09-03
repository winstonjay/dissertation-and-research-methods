import collections
import time
import re
import sys

# --- third party modules. ---
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nltk.stem.snowball import SnowballStemmer

from IPython.core.display import HTML, display

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


sys.path.append('../../lib/')

# --- local modules. ---
import rake

# --- set up keyword extractor. ---
stopwords = set(open('../../lib/stopwords').read().split())

stopwords = stopwords | set('''https
mr congressman senator chairman gentlemen gentleman yield
time recognizes chair gentlelady expired crosstalk laughter
'''.split())

stopwords = stopwords |  set('https'.split())
# --- functions ---

def collection_keywords(series):
    'return the most essetinial keywords of the collection.'
    keyext    = rake.KeywordExtractor(stopwords)
    collectop = rake.CollectionOperator(keyext)
    collectop.fit(list(series))
    return collectop


def count_keywords(df):
    c = collections.Counter()
    for k in df.keywords:
        c.update(k)
    return c


def plot_counter(ax, counter, n=15, title=None, size=(5,6)):
    labels, values = list(zip(*counter.most_common(n)[::-1]))
    ind = np.arange(len(labels))
    width = 0.8
    a = ax.barh(ind, values, width)
    ax.set_yticks(ind)
    ax.set_yticklabels(labels)
    ax.legend(a, ("counts",))
    if title is not None:
        ax.set_title(title, y=1.05)


def plot_ngrams(series, n0, n1, top=20, **kwargs):
    n1 += 1
    z = n1 - n0
    fig, axis = plt.subplots(1, z)
    fig.set_size_inches(10, 6)
    if 'title' in kwargs:
        plt.suptitle(kwargs['title'], fontsize=16)
        del kwargs['title']
    for i in range(z):
        tfidf_vect = TfidfVectorizer(max_df=0.5, min_df=2,
                                     max_features=5000,
                                     ngram_range=(n0 + i, n0 + i + 1),
                                     stop_words=stopwords)
        tfidf_features = tfidf_vect.fit_transform(series)
        vocab = tfidf_vect.get_feature_names()
        values = tfidf_features.toarray().sum(axis=0)
        sample = [(values[i], k) for i, k in enumerate(vocab)]
        v, k = zip(*sorted(sample, reverse=True)[:top])
        dd = pd.DataFrame(index=k, data={"key": k, "tfidf": v})
        dd.plot(kind="barh", ax=axis[i], legend=False, title=f"$N = {i+1}$", **kwargs).invert_yaxis()
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()


def clean_text(series):
    '''converts the text to lowercase remove all non words,
    stopwords, non ascii characters and links. stem the remaining
    words and concatinate the result into a new string.'''
    return cat(stemmer.stem(w) for w in rx0.findall(series.lower())
                if 3 < len(w) < 20
                if w not in stopwords)

rx0     = re.compile(r"\w+")
cat     = " ".join
stemmer = SnowballStemmer("english")
