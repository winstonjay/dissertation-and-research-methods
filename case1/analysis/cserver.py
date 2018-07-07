
'''
cserver.py : A simple interface for qualitive analysis of Twitter and
YouTube datasets. It combines both a GUI and prints additional
information to a cli.

usage: cserver.py [-h] [-n LIMIT] file

positional arguments:
  file                  ndjson file to explore

optional arguments:
  -h, --help            show this help message and exit
  -n LIMIT, --limit LIMIT
                        number of examples to rate.

'''
from __future__ import print_function

import argparse
import functools
import json
import os
import io
import random
import webbrowser

import tkinter as tk

import requests
from PIL import ImageTk, Image


def main():
    config = Config(parse_args())
    with Record(config.fname) as fp:
        cursor = DataCursor(fp, config)
        root = tk.Tk()
        master = ContentServer(root, cursor)
        root.mainloop()



class ContentServer:


    def __init__(self, root, cursor):
        self.cursor = cursor
        self.root = root
        root.title("Content GUI")
        root.geometry("275x275")

        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)

        # init components
        self.init_image(self.cursor.curr_img)
        self.init_text(self.cursor.curr_title)
        self.init_page_btn()
        self.init_btns()

        self.frame.pack(side="bottom", fill="both", expand="yes")

        # print the first entry to the cli
        self.cursor.print_curr()

    def init_image(self, img):
        self.frame.rowconfigure(0, weight=1)
        self.img = ImageTk.PhotoImage(img)
        self.row0 = tk.Label(self.frame, image=self.img)
        self.row0.grid(row=0, column=0, columnspan=6, sticky=tk.NSEW)

    def init_page_btn(self):
        page_btn = tk.Button(self.frame, text='visit', command=self.visit_page)
        page_btn.grid(row=2, column=0, columnspan=6)
        self.frame.rowconfigure(2, weight=1)

    def init_btns(self):
        'inialaise all buttons for the ui'
        for col in range(6):
            btn = tk.Button(self.frame,
                            text=f"{col}",
                            command=functools.partial(self.update, col))
            btn.grid(row=3, column=col)
            self.frame.columnconfigure(col, weight=1)

    def init_text(self, text):
        self.v = tk.StringVar()
        self.row1 = tk.Label(self.frame, textvariable=self.v)
        self.row1.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW)
        self.frame.rowconfigure(1, weight=1)
        self.v.set(text)

    def update(self, score):
        if not self.cursor.done:
            clear_output()
            print("score:", score)
            self.cursor.advance(score)
            self.cursor.print_curr()
            self.update_img(self.cursor.curr_img)
            self.v.set(self.cursor.curr_title)

    def update_img(self, img):
        new = ImageTk.PhotoImage(img)
        self.row0.configure(image=new)
        self.row0.image = new

    def visit_page(self):
        self.cursor.visit_page()


class Record:
    '''
    Record : a append only file written to by a DataCursor.
    '''
    def __init__(self, filename):
        self.filename = f'{filename}.record'

    def __enter__(self):
        exists = os.path.exists(self.filename)
        self.fp = open(self.filename, 'a+')
        print(f'loading record {self.filename}. [new={not exists}]')
        # provide access to the user.
        return self.fp

    def __exit__(self, exception_type, exception_val, trace):
        print(exception_type, exception_val, trace)
        try:
           self.fp.close()
        except AttributeError:
           print('Not closable.')
           return True # exception handled successfully



class DataCursor:
    '''
    DataCursor :

    '''
    def __init__(self, fp, config):
        with open(config.fname) as rp:
            data = [(i, json.loads(line)) for i, line in enumerate(rp)]
        # random.shuffle(data)
        self.data = data[:config.limit]
        self.pos  = 0
        self.size = len(self.data)
        self.curr = self.data[self.pos]
        self.config = config
        self.fp = fp
        print(self.fp)

    @property
    def done(self):
        return not (self.pos < self.size)

    def advance(self, score):
        self.write(score)
        if self.pos < self.size:
            self.pos += 1
            self.curr = self.data[self.pos]
            return True
        print("FINISHED...")
        return False

    def print_curr(self):
        i, entry = self.curr
        print("-"*72)
        for k, v in self.config.get_info(entry):
            print(f"{k:16}: ", end='')
            print_value(v)
        print("-"*72)

    def write(self, score):
        i, entry = self.curr
        _id = self.config.get_id(entry)
        self.fp.write(f'{i},{_id},{score}\n')

    @property
    def curr_img(self):
        i, entry = self.curr
        img_url = self.config.get_image(entry)
        response = requests.get(img_url)
        image = Image.open(io.BytesIO(response.content))
        image = image.resize((128, 128), Image.ANTIALIAS)
        return image

    @property
    def curr_title(self):
        i, entry = self.curr
        return self.config.get_title(entry)

    def visit_page(self):
        _, entry = self.curr
        webbrowser.open(self.config.get_page(entry))


def parse_args():
    'Parse args and return formatted args.'
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='ndjson file to explore')
    parser.add_argument('platform', type=str, help="youtube or twitter")
    parser.add_argument(
        '-n',
        '--limit',
        type=int,
        help='number of examples to rate.',
        default=50)
    return parser.parse_args()

def print_value(item, indent=18):
    if indent > 18 and not item:
        print('\n')
        return
    if isinstance(item, list):
        for v in item:
            print_value(v, indent+4)
    elif isinstance(item, dict):
        for k, v in item.items():
            print("\n{}{}: ".format(' '*indent, k), end='')
            print_value(v, indent+4)
    else:
        print(item)



class Config:

    def __init__(self, args):
        self.fname    = args.file
        self.limit    = args.limit
        self.platform = args.platform
        self.ops = platforms.get(args.platform)
        self.ops['fmt'] = self.build_fmt(args.platform)

    def get_title(self, entry): return self.ops['title'](entry)
    def get_image(self, entry): return self.ops['img'](entry)
    def get_info(self, entry):  return self.ops['fmt'](entry)
    def get_id(self, entry):    return self.ops['id'](entry)
    def get_page(self, entry):  return self.ops['page'](entry)

    def build_fmt(self, platform):
        if platform == 'twitter':
            def f(user):
                return ((k, v) for k, v in user.items()
                        if k in twitter_fields)
        elif platform == 'youtube':
            def f(user):
                data = {k: v for k, v in user['snippet'].items()
                        if k in youtube_fields}
                data.update(user['statistics'])
                return ((k, v) for k, v in data.items())
        else:
            raise ValueError("unkown platform")
        return f

twitter_fields = frozenset('''
id_str name screen_name location description url entities protected
followers_count friends_count listed_count created_at favourites_count
time_zone geo_enabled verified statuses_count lang
'''.split())

youtube_fields = frozenset('title description customUrl publishedAt'.split())

platforms = {
    'twitter': {
        'title': lambda p: '{}, {}'.format(p['name'], p['screen_name']),
        'img':   lambda p: p['profile_image_url_https'],
        'id':    lambda p: p['id_str'],
        'page':  lambda p: 'https://twitter.com/{}'.format(p['screen_name'])
    },
    'youtube': {
        'title': lambda p: p['snippet']['title'],
        'img':   lambda p: p['snippet']['thumbnails']['default']['url'],
        'id':    lambda p: p['id'],
        'page':  lambda p: 'https://www.youtube.com/user/{}'.format(p['snippet']['customUrl'])
    }
}

def clear_output(): print("\033[;H\033[2J") # ANSI terminal home and clear

if __name__ == '__main__':
    main()