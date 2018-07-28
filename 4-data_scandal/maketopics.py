'''
maketopics.py :

# topic similarity?
https://blakeboswell.github.io/2016/07/15/gensim-hellinger.html
'''
import sys

import pandas as pd
from nltk.stem.snowball import SnowballStemmer

# local modules.
sys.path.append('../')
from lib import topicmodel
from lib import stopwords
from lib import textutils

stop_words = stopwords.load()



def hearing_topics(fp):

    stopwords1 = stop_words | set('''
    mr congressman senator chairman gentlemen gentleman yield
    time recognizes chair gentlelady expired crosstalk laughter
    '''.split())
    h0 = pd.read_csv('data/hearing/hearings.csv')
    h0['cleaned'] = h0.speech.apply(lambda a: textutils.clean_text(a, stopwords1))
    witness = h0[h0.name == 'ZUCKERBERG'].cleaned
    pannel  = h0[h0.name != 'ZUCKERBERG'].cleaned
    # free up a little memory.
    del h0
    m0 = topicmodel.TopicModel(max_iter=50)
    m0.fit(pannel)
    for t in m0.topics(25):
        print(t)
    print('\n')
    m1 = topicmodel.TopicModel(max_iter=50)
    m1.fit(witness)
    for t in m1.topics(25):
        print(t)


def twitter_topics():
    from nltk.corpus import stopwords as stop_words
    spanish_words = set(ntlk_stopwords.words('spanish'))
    from nltk.corpus import stopwords