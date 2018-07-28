# -*- coding: utf-8 -*-
'''
parseTranscript.py :

a basic transcript parser.

basic grammar for the parser is defined as follows:

    transcript  ::= <line> \n <transcript>

    line        ::= <speakerdec> <speech>
                  | <speech>
                  | <empty>

    speaker_dec ::= <speaker> ':'

    speech      ::= <any_character>

    speaker     ::= <caplital> <name_part>

    name_part   ::= <vaild_char> <name_part> | <vaild_char>

    vaild_char  ::= <capital> | '-' | '.' | ' ' | '(' | ')'

    capital     ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I'
                  | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R'
                  | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'

Example input:

    MARIO CART (O.B.E.): Lorem ipsum dolor sit amet,
    consectetur
    GOOFY: sed do eiusmod tempor incididunt ut labore et dolore
    MARIO: Ut enim ad minim veniam

From the above example the output of TranscriptParser.parse() would be:

    [('MARIO', 'MARIO CART (O.B.E.)', 'Lorem ipsum dolor sit amet, consectetur'),
     ('GOOFY', 'GOOFY', 'sed do eiusmod tempor incididunt ut labore et dolore'),
     ('MARIO', 'MARIO CART (O.B.E.)', 'Ut enim ad minim veniam')]

'''


class TranscriptParser:
    '''
    TranscriptParser parses transcripts which can be given as a iterable
    of lines of a file pointer. The parse method can only be called once
    per instance and the caller is responsible for opening and closing the
    file.
    '''
    def __init__(self, transcript):
        self.fp      = transcript # an open file or iterable lines
        self.names   = {}         # {shortname: longname, ...}
        self.entries = []         # [(speaker, speech), ...]
        self.speaker = None       # who the current speaker is.
        # set up an iterator so we can call next on each line anywhere
        # in the class also skipping the blank ones. the parse will be
        # done in one pass of the file.
        self.lines = (ln.strip() for ln in self.fp if ln.strip())
        # this is for the name pattern matching.
        self.capitals  = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.validname = self.capitals | set('-.() ')

    def parse(self):
        '''return (name, longname, speech) for each speaker turn in
        the transcript.'''
        if not self.fp:
            raise Exception('Nothing to parse.')
        # main parsing stage for connaticating lines and matching speaker
        # turns with speeches.
        entries = self.parse_speech()
        if isinstance(self.fp, file):
            self.fp.close()
        # map long names by swapping long and short name pairs
        self.longs = {v: k for k, v in self.names.items()}
        # last pass on the transcript to place the long and short names.
        return ((n, self.names[n], speech) if n in parser.names else
                (self.longs[n], n, speech) for n, speech in entries)

    def parse_speech(self):
        '''return [(speaker, speech)...] for each speech instance
        concatinating multiple lines of speech into one entry.'''
        curr_speech = []
        for line in self.lines:
            # find out who is speaking on the current line.
            (new_speaker, speech) = self.speaker_match(line)
            # if there is a speech and no one is speaking somethings
            # wrong.
            if not new_speaker:
                raise Exception("No speaker found during parsing.")
            # if the same person is still speaking just append their
            # speech to the current speech list and continue.
            if self.speaker == new_speaker:
                curr_speech.append(speech)
                continue
            if new_speaker not in self.names:
                self.name_register(new_speaker)
            # if someone has already been speaking but we have found a
            # new speaker then the last persons speaking has ended to
            # add them to our transcripts entries.
            if curr_speech:
                self.entries.append((self.speaker, cat(curr_speech)))
            # update the new current speaker and initalise their lines
            # of speech.
            self.speaker = new_speaker
            curr_speech  = [speech]
        # catch the last speech.
        if curr_speech:
            self.entries.append((self.speaker, cat(curr_speech)))
        return self.entries

    def speaker_match(self, line):
        '''return the split (speaker, speech) from a given line. if no
        speaker is found return the last know speaker.'''
        # speaker declarations take the form <speaker> ':'. A valid
        # speaker name can only be composed by from the characters
        # defined in self.valid name and must start with a capital.
        # When we reach a colon (':') this ends the declarations.
        # regular expresiion form would be: '^[A-Z][A-Z-\.\(\)\ ]*:'.
        if line[0] in self.capitals:
            for i, char in enumerate(line):
                if char == ':':
                    return (line[:i], line[i+1:].strip())
                if char not in self.validname:
                    break
        return (self.speaker, line)

    def name_register(self, new_speaker):
        'add a speaker to the register. match long and short names.'
        # NOTE: probally want a better data structure here but this is
        # good enough for now. also there may be some name collision
        # problems but for now this assumes that the transcript writer
        # is specific in who they are taking about and speakers dont
        # have surnames that are other peoples surnames.
        for name in self.names:
            if new_speaker in name:
                self.names[new_speaker] = name
                del self.names[name]
                return
        self.names[new_speaker] = new_speaker

cat = ' '.join


if __name__ == '__main__':
    import argparse
    import csv

    p = argparse.ArgumentParser()
    p.add_argument(
        'filename', type=str, help='filename of transcript to parse')
    p.add_argument(
        '-o', '--out', type=str, help='output filename', default='out.csv')
    args = p.parse_args()


    parser = TranscriptParser(open(args.filename))
    with open(args.out, 'w+') as fp:
        w = csv.writer(fp)
        w.writerow(('name', 'longname', 'speech'))
        for line in parser.parse():
            w.writerow(line)
    print('wrote to file: {}'.format(args.out))
