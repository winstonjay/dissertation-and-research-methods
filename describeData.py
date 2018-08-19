'''
describeData.py :

Because of GDPR and other privacy reasons, sharing datasets is kind of
difficult to do properly, as such the actual data files are not shared
within the repository. Instead we will just descibe their meta data.

Loop though all child directories and for every `data/` directory
create a readme listing the directories contents detailing each
files size, name and created date.
'''
from __future__ import print_function

import os
import datetime

exclude = {'./.git', './env', './misc', './lib'}



def walk(root, printing=False, indent='\t', fp=None):
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if path in exclude:
            continue
        if os.path.isdir(path):
            printing = '/data/' in path
            if fp and not printing:
                fp.close()
            if path.endswith('data'):
                n = os.path.join(path, 'README.md')
                fp = open(n, 'w+')
            if printing and not 'README' in path:
                print(indent + path.split('/')[-1] + "/", file=fp)
                walk(path, printing, indent + '\t', fp)
            else:
                walk(path, printing, indent, fp)
        elif printing and not name.startswith('.'):
            s = os.stat(path)
            print(f'{indent}{name:32} {s.st_size}', file=fp)


def describe_dir(path):
    pass

def descibe_file(indent, path, name):
    s = os.stat(path)
    # t = datetime.datetime.fromtimestamp(s.st_mtime).strftime('%x')
    print(f'{indent}{s.st_size:>10}   {name}', file=fp)



if __name__ == '__main__':
    # clean data dirs.
    # find . -name READMETEST.md -type f -delete
    walk('.')