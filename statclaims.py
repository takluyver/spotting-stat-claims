#!/usr/bin/env python3

import lxml.etree
import sys
from stats_functions import Extractor


def find_claims(paragraph):
    # Dummy function for testing interface
    return [(50, 55)]

BOLD = '\x1b[1m'
NORMAL = '\x1b[0m'
HIGHLIGHT = '\x1b[30;48;5;11m'

def get_snippet(para, start, end):
    """Format a match for display"""
    l = len(para)
    snipfrom = start - 36
    ellipsis_pre = ellipsis_post = "\u2026"
    if snipfrom <= 0:
        snipfrom = 0
        ellipsis_pre = ''
    
    snipto = max(end + 40, snipfrom + 80)
    if snipto >= l:
        snipto = l
        ellipsis_post = ''
    
    return (ellipsis_pre + para[snipfrom:start] + 
        HIGHLIGHT + para[start:end] + NORMAL +
        para[end:snipto] + ellipsis_post)


def show_claims(speech):
    speaker = speech.attrib.get('speakername', '[no speaker]')
    time = speech.attrib.get('time', '[no time]')
    claims = []
    for para in speech.xpath('p/text()'):
        for (start, end) in Extractor(para).extract_stats_from_text():
            claims.append(get_snippet(para, start, end))
    
    if claims:
        print(BOLD + speaker + NORMAL, 'at', time)
        for snippet in claims:
            print(snippet)
        print()

def check_hansard_file(path):
    tree = lxml.etree.parse(path)
    for speech in tree.xpath('/publicwhip/speech')[:100]:
        show_claims(speech)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    if len(argv) < 2:
        sys.exit("Usage: statclaims.py hansard/src/debates2016-01-12b.xml [...]")
    
    for path in argv[1:]:
        check_hansard_file(path)

if __name__ == '__main__':
    main()
