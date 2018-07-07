import os

def stopwords(fname='stopwords'):
    filepath = os.path.join(path, fname)
    with open(filepath) as fp:
        sw = fp.read()
    return set(sw.split())

path = os.path.dirname(os.path.realpath(__file__))