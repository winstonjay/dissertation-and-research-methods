'''
condense all json files into a single csv file with each row containing:

videoId,text,published,totalReplyCount,likes

'''
import argparse
import csv
import json
import os


def main():
    out  = open(args.out, 'w+')
    w = csv.DictWriter(out, fieldnames=fieldnames)
    w.writeheader()
    for filepath in iter_dir(args.folder, ext='.json'):
        print(f'parsing file {filepath}')
        with open(filepath) as fp:
            w.writerows(parse_file(fp))
    out.close()
    print('done!')

fieldnames = 'videoId org text published totalReplyCount likeCount'.split()


def parse_file(fp):
    rows = []
    for obj in json.load(fp):
        snippet = obj['snippet']
        inner   = snippet['topLevelComment']['snippet']
        row = dict(videoId=snippet['videoId'],
                   org=org_codes[snippet['videoId']],
                   text=inner['textOriginal'].replace('\n', ''),
                   published=inner['publishedAt'],
                   totalReplyCount=snippet['totalReplyCount'],
                   likeCount=inner['likeCount'])
        rows.append(row)
    return rows

org_codes = {
    '6ValJMOpt7s': 'The Washington Post',
    'hJdxOqnCNp8': 'The Washington Post',
    'BylLTX05jSY': 'NBC',
    'snDGFwvLVm8': 'NBC',
    'Ziw70UJLVHc': 'Time',
    'CMZTbMFK5eA': 'Time',
    'mZaec_mlq9M': 'The Guardian',
    'H-paF1w8_y8': 'The Guardian',
    'cyJosQBtzsw': 'Bloomberg',
    '_Te_LKt5DpY': 'Bloomberg'
}


def iter_dir(path, ext='.json'):
    for f in os.listdir(path):
        if ext in f:
            yield os.path.join(path, f)

parser = argparse.ArgumentParser()
parser.add_argument(
    'folder', type=str, help='data folder path')
parser.add_argument(
    '-o', '--out', type=str, help='output filename', default='data/comments.csv')
args = parser.parse_args()


if __name__ == '__main__':
    main()