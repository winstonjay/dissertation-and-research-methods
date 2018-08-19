import argparse
import csv
from transcriptParser import TranscriptParser

def main():
    parser = TranscriptParser(open(args.filename))
    with open(args.out, 'w+') as fp:
        w = csv.writer(fp)
        w.writerow(('name', 'longname', 'speech'))
        for line in parser.parse():
            w.writerow(line)
    print('wrote to file: {}'.format(args.out))

p = argparse.ArgumentParser()
p.add_argument(
    'filename', type=str, help='filename of transcript to parse')
p.add_argument(
    '-o', '--out', type=str, help='output filename', default='out.csv')
args = p.parse_args()

if __name__ == '__main__':
    main()