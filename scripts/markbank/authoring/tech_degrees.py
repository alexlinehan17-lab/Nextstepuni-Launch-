#!/usr/bin/env python3
"""Technology's degree signs, as the SEC printed them: a raised small letter o.

    python3 scripts/markbank/authoring/tech_degrees.py        # every proven one, papers and schemes

The 2010 and 2011 papers and schemes set the degree sign as the LETTER o, in
its own span, 7.14pt beside 10.98pt digits and 4.9pt above their baseline:
"at 4oC", "up to 45o", "U2's 360o tour". The text layer reports the letter,
so a card lifted from it showed "4oC" -- which a student reads as 40C -- where
the page they sat printed 4 degrees C.

An o is a degree sign here only when the PDF itself proves it: the span holds
the o and nothing else that is a letter, it follows a span ending in a digit
on the same line, and it is set as a superscript (span flag), SMALLER than the
digit's span and RAISED above the digit's baseline. All three, read off the
span; never the spelling. DCG's append-scheme-degrees.py proved its scheme
cases the same way (flag and size); the baseline is added here.

A proof is (page, digits, the text that follows the o). The text is repaired
only where that same digit run is followed by an o and that same text, on that
page of the scheme (tech_mdclean) or in that sitting's paper (tech_all), and
never more times than the PDF proves.
"""
import functools
import os
import re
import sys

import fitz

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SUPERSCRIPT = 1                 # PyMuPDF span flag
DEGREE = '°'


@functools.lru_cache(maxsize=None)
def proofs(pdf):
    """((page, digits, following text), ...) for every raised o after a digit."""
    out = []
    if not os.path.exists(pdf):
        return ()
    with fitz.open(pdf) as doc:
        for pi, page in enumerate(doc):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = line['spans']
                    for i, span in enumerate(spans):
                        if i == 0 or not re.fullmatch(r'o(?![A-Za-z])\W*', span['text']):
                            continue
                        prev = spans[i - 1]
                        digits = re.search(r'(\d+)\s*$', prev['text'])
                        if not digits:
                            continue
                        raised = (span['flags'] & SUPERSCRIPT
                                  and span['size'] < prev['size'] - 1
                                  and span['origin'][1] < prev['origin'][1] - 1)
                        if not raised:
                            continue
                        after = span['text'][1:] + ''.join(s['text'] for s in spans[i + 1:])
                        out.append((pi, digits.group(1), after))
    return tuple(out)


def pattern(digits, after):
    """The text-layer form of one proof: the digits, the letter o, and the
    first two printed characters that follow it (whitespace normalised)."""
    follow = ' '.join(after.split())[:2] if after.strip() else ''
    if after[:1].isspace() and follow:
        follow = ' ' + follow[:1]
    return re.compile(r'(?<!\d)' + re.escape(digits) + r'o' + (r'(?=' + re.escape(follow) + r')' if follow else r'(?![A-Za-z])'))


def repair(text, proven):
    """`text` with each proven o as a degree sign, never more of one form than
    the PDF proves; (text, count)."""
    total = 0
    for (digits, after), times in proven.items():
        pat = pattern(digits, after)
        hits = pat.findall(text)
        if not hits:
            continue
        if len(hits) > times:
            raise SystemExit(f'tech_degrees: {len(hits)} x "{digits}o" in a text the PDF proves {times} of')
        text, n = pat.subn(digits + DEGREE, text)
        total += n
    return text, total


def counted(items):
    out = {}
    for digits, after in items:
        key = (digits, after)
        out[key] = out.get(key, 0) + 1
    return out


def paper_proofs(year, level):
    """{(digits, after): count} over both of a sitting's papers."""
    papers = os.path.join(ROOT, 'examiner-reports/technology/papers')
    items = []
    for name in sorted(os.listdir(papers)):
        if name.startswith(f'{year}-{level}-') and name.endswith('.pdf'):
            items += [(d, a) for _p, d, a in proofs(os.path.join(papers, name))]
    return counted(items)


def scheme_proofs(year, level):
    """{page: {(digits, after): count}} for a sitting's scheme."""
    pdf = os.path.join(ROOT, 'examiner-reports/technology/schemes', f'{year}-{level}.pdf')
    out = {}
    for page, d, a in proofs(pdf):
        out.setdefault(page, []).append((d, a))
    return {p: counted(v) for p, v in out.items()}


def main():
    import glob
    for pdf in sorted(glob.glob(os.path.join(ROOT, 'examiner-reports/technology/papers/*.pdf'))) \
            + sorted(glob.glob(os.path.join(ROOT, 'examiner-reports/technology/schemes/*.pdf'))):
        for page, d, a in proofs(pdf):
            print(f'{os.path.basename(pdf)} p{page + 1}: {d}o{a[:12]!r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
