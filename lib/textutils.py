import collections
import re

from nltk.stem.snowball import SnowballStemmer


def clean_text(text, stopwords):
    '''converts the text to lowercase remove all non words,
    stopwords, non ascii characters and links. stem the remaining
    words and concatinate the result into a new string.'''
    return cat(stemmer.stem(w) for w in rx0.findall(text.lower())
                if 3 < len(w) < 20
                if w not in stopwords)

rx0     = re.compile(r'\w+')
cat     = ' '.join
stemmer = SnowballStemmer('english')
