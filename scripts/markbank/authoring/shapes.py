#!/usr/bin/env python3
"""What shapes does this subject's marking scheme use, and how common is each?

    python3 scripts/markbank/authoring/shapes.py construction-studies
    python3 scripts/markbank/authoring/shapes.py <subject> --show "group tariff"

RUN THIS BEFORE WRITING A LINE OF A SUBJECT'S READER.

Every subject in this bank has been authored the same wrong way: build a reader
for the first shape noticed, author what it reaches, report a card count, and
then discover — only when pushed — that most of the paper used a shape the
reader could not see. Construction Studies went 64 -> 129 -> 144 -> 191 -> 237
that way, and every jump was a shape found late, not new content.

The number a card count needs is the DENOMINATOR, and the thing a reader needs
before it is written is the list of shapes it has to cover. This prints both,
off the raw scheme text, with no subject-specific parsing and nothing filtered
by what any reader can already handle. That last part matters most: a coverage
probe that shares the reader's assumptions cannot see what the reader is blind
to, which is exactly how 46 Construction Studies parts stayed invisible.

Read the output top down and build for the shapes in order of how many priced
lines they hold. Anything in `unclassified` is a shape nobody has looked at yet
— read those lines before believing any coverage number.
"""
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
REPORTS = os.path.join(ROOT, 'examiner-reports')

# Ordered: the first match wins, so the specific forms come before the general.
SHAPES = [
    ('group tariff',
     r'\b(?:any\s+)?\d{1,2}\s*[x×]\s*\d{1,3}\s*marks?\b',
     'N answers at M marks each — a best-of menu over the list beside it'),
    ('split tariff on a row',
     r'\(\s*\d{1,3}(?:\s*\+\s*\d{1,3})+\s*marks?\s*\)',
     '"(8 + 5 marks)" — one answer priced in parts, usually note plus sketch'),
    ('part total',
     r'\(\s*\d{1,3}\s*marks?\s*\)\s*$',
     'the part\'s own total — use it to CHOOSE between competing readings'),
    ('sub-total row',
     r'\b(?:sub-?\s*total|total)\b\s*\d{1,3}|\btotal\s+\d{1,3}\s*marks',
     'a total, never an answer row — counting it breaks same-mark tests'),
    ('quality band',
     r'(?:excellent|very good|good|fair|weak)\s*[:\-–]?\s*\d',
     'graded presentation marks — priced, but nothing to lift'),
    ('scaffold row',
     r'^(?:advantage|disadvantage|reason|risk|feature|guideline|point|method|'
     r'consideration|answer|benefit|way|factor|use|example|item|area|aspect|'
     r'requirement|precaution|approach|step|stage|task|option)s?\s*\d*\s+\d{1,3}$',
     'names nothing — "Advantage 1  5" means the CONTENT is in the other half'),
    ('presentation row',
     r'^(?:notes?|sketch(?:es)?|drawing|discussion|presentation|layout)'
     r'(?:\s*[/&]\s*\w+)?\s+\d{1,3}$',
     'marks for the drawing itself — a legitimate shortfall, never an answer'),
    ('named row with mark',
     r'^.{4,90}?\s+\d{1,3}$',
     'a named answer and its mark — the richest shape, and often the ONLY '
     'place the content lives'),
]
COMPILED = [(n, re.compile(p, re.I | re.M), d) for n, p, d in SHAPES]

PRICED = re.compile(r'\d')
FOLD = re.compile(r'^<!--\s*markbank:')
FURNITURE = re.compile(
    r'^(##\s*Page|Leaving Certificate|Coimisi|State Examinations|-\s*\d+\s*-'
    r'|\d{1,3}\s*$|PERFORMANCE CRITERIA|MAXIMUM|MARK\s*$)', re.I)

# Characters that are a bullet but do not look like one. The 2024 and 2025
# Construction Studies papers use , the Symbol font's bullet in the
# private use area; read as text it is not a separator and every enumerated
# question in those papers silently refused to split.
ODD_BULLETS = re.compile(r'[-]')
# Text that did not survive its own font.
MANGLED = re.compile(r'[\U0001D400-\U0001D7FF଀-୿ƟƜ]')


def scheme_files(subject):
    d = os.path.join(REPORTS, subject, 'schemes')
    if not os.path.isdir(d):
        raise SystemExit(f'no schemes at {d} — fetch the corpus first')
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.md'))


def lines_of(path):
    out = []
    for raw in open(path, errors='ignore'):
        t = raw.strip()
        if FOLD.match(t):
            break
        if t and not FURNITURE.match(t):
            out.append(t)
    return out


def main(subject, show=None):
    tally, examples = Counter(), defaultdict(list)
    unclassified, odd, mangled = [], [], []
    per_file, priced_total = Counter(), 0
    for path in scheme_files(subject):
        stem = os.path.basename(path)[:-3]
        for line in lines_of(path):
            if ODD_BULLETS.search(line):
                odd.append((stem, line))
            if MANGLED.search(line):
                mangled.append((stem, line))
            if not PRICED.search(line):
                continue
            priced_total += 1
            per_file[stem] += 1
            for name, rx, _ in COMPILED:
                if rx.search(line):
                    tally[name] += 1
                    if len(examples[name]) < 4:
                        examples[name].append(f'{stem}: {line[:88]}')
                    break
            else:
                unclassified.append(f'{stem}: {line[:88]}')

    print(f'{subject}: {priced_total} lines carrying a number, '
          f'across {len(per_file)} scheme(s)\n')
    if show:
        for e in examples.get(show, []) or unclassified[:30]:
            print('   ', e)
        return
    desc = {n: d for n, _, d in SHAPES}
    for name, n in tally.most_common():
        print(f'{n:>5}  {name}')
        print(f'        {desc[name]}')
        for e in examples[name][:2]:
            print(f'        e.g. {e}')
    print(f'\n{len(unclassified):>5}  UNCLASSIFIED — read these before trusting any '
          f'coverage number')
    for e in unclassified[:8]:
        print(f'        {e}')
    if odd:
        print(f'\n{len(odd):>5}  lines with a PRIVATE-USE character (a bullet or '
              f'glyph that is not what it looks like)')
        for stem, l in odd[:3]:
            print(f'        {stem}: {l[:80]!r}')
    if mangled:
        print(f'\n{len(mangled):>5}  lines whose text did not survive its own font')
        for stem, l in mangled[:3]:
            print(f'        {stem}: {l[:80]}')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        raise SystemExit('name a subject')
    show = None
    if '--show' in sys.argv:
        show = sys.argv[sys.argv.index('--show') + 1]
    main(args[0], show)
