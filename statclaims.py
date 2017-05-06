#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import lxml.etree
import os.path
import sys
from stats_functions import Extractor
from types import SimpleNamespace

this_dir = os.path.dirname(__file__)


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
    
    return (ellipsis_pre + para[snipfrom:start],
         para[start:end], para[end:snipto] + ellipsis_post)

def terminal_format_snippet(before, match, after):
    return before + HIGHLIGHT + match + NORMAL + after

def check_speech(speech):
    speaker = speech.attrib.get('speakername', '[no speaker]')
    time = speech.attrib.get('time', '[no time]')
    claims = []
    for para in speech.xpath('p/text()'):
        for (start, end) in Extractor(para).extract_stats_from_text():
            claims.append(get_snippet(para, start, end))
    
    return SimpleNamespace(
        speaker=speaker,
        time=time,
        snippets=claims,
    )

def show_claims(speech):
    res = check_speech(speech)
    if res.snippets:
        print(BOLD + res.speaker + NORMAL, 'at', res.time)
        for snippet in res.snippets:
            print(terminal_format_snippet(*snippet))
        print()

def check_hansard_file(path):
    tree = lxml.etree.parse(path)
    for speech in tree.xpath('/publicwhip/speech'):
        show_claims(speech)

def check_hansard_files_htmlout(paths):
    debates = []
    for path in paths:
        tree = lxml.etree.parse(path)
        speech_res = []
        for speech in tree.xpath('/publicwhip/speech'):
            r = check_speech(speech)
            if r.snippets:
                speech_res.append(r)
        debates.append((os.path.basename(path), speech_res))
    
    jinja_env = Environment(loader=FileSystemLoader(this_dir),
                            autoescape=True)
    template = jinja_env.get_template('results.tpl')
    
    output_file = os.path.join(this_dir, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        template.stream(debates=debates).dump(f)
    
    

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    if len(argv) < 2:
        sys.exit("Usage: statclaims.py hansard/src/debates2016-01-12b.xml [...]")
    
    if argv[1] == '--html':
        return check_hansard_files_htmlout(argv[2:])
    
    for path in argv[1:]:
        check_hansard_file(path)

if __name__ == '__main__':
    main()
