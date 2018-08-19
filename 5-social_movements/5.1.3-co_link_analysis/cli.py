import fire
import functools

class Quiz(object):
    '''all of a quizes methods are questions'''

    def unique(self, filedata, *substrs):
        'python cli.py unique "$(cat abc)" facebook'
        items = set(filedata.split())
        total = len(items)
        def inc(a, sub): return sub in a

        print(f'{"total":16}: {total}')
        for s in substrs:
            f = functools.partial(inc, sub=s)
            x = len(list(filter(f, items)))
            print(f'{s:16}: {x}')

# $ python cli.py unique "$(cat data/issuecrawler/occupy)" facebook twitter //t.co youtube youtu.be tumblr instagram
# total           : 2214
# facebook        : 57
# twitter         : 8
# youtube         : 5
# tumblr          : 10
# instagram       : 0
# $ python cli.py unique "$(cat data/issuecrawler/blm)" facebook twitter //t.co youtube youtu.be tumblr instagram
# total           : 107
# facebook        : 12
# twitter         : 0
# youtube         : 0
# tumblr          : 2
# instagram       : 0
# $ python cli.py unique "$(cat data/issuecrawler/metoo)" facebook twitter //t.co youtube youtu.be tumblr instagram
# total           : 7
# facebook        : 1
# twitter         : 1
# youtube         : 0
# tumblr          : 0
# instagram       : 0

if __name__ == '__main__':
    fire.Fire(Quiz)