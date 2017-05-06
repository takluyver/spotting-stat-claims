#!/usr/bin/env python3

import lxml.etree
import sys

def find_claims(paragraph):
    return [50]

BOLD = '\x1b[1m'
NORMAL = '\x1b[22m'

def show_claims(speech):
    speaker = speech.attrib.get('speakername', '[no speaker]')
    time = speech.attrib.get('time', '[no time]')
    claims = []
    for para in speech.xpath('p/text()'):
        for pos in find_claims(para):
            snippet = para[pos-40:pos+40]
            if snippet:
                claims.append(snippet)
    
    if claims:
        print(BOLD + speaker + NORMAL, 'at', time)
        for snippet in claims:
            print("\u2026" + snippet + "\u2026")
        print()

def check_hansard_file(path):
    tree = lxml.etree.parse(path)
    for speech in tree.xpath('/publicwhip/speech')[:100]:
        show_claims(speech)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    if len(argv) < 2:
        sys.exit("Usage: show hansard/src/debates2016-01-12b.xml [...]")
    
    for path in argv[1:]:
        check_hansard_file(path)

if __name__ == '__main__':
    main()
