#!/usr/bin/env python3
"""What German and Spanish would take, measured rather than guessed.

    python3 scripts/markbank/authoring/lang_scout.py
    python3 scripts/markbank/authoring/lang_scout.py german --heads

French shipped first (fr_scheme.py, fr_paper.py, fr_all.py). The brief for that
wave said the other two modern languages would come "through the same reader",
and the measurement below is why they cannot: the three subjects share a paper
LAYOUT and share nothing of their scheme grammar.

WHAT IS SHARED, AND WORTH REUSING
---------------------------------
The German paper is printed bilingually exactly as the French one is, and
fr_paper.py's reader — baseline grouping, the page's own column BOUND taken
from the markers printed down it, the six-point seam guard — reads it as
cleanly. `--papers` measures it: five or six pages of every German Higher
sitting and fourteen to sixteen of every Ordinary one carry a bilingual column
bound, and the German paper sets its Questions 2 to 4 in Irish and English
columns just as the French Ordinary paper does.

Spanish does NOT: nought to two pages a sitting. It sets each section in one
language and says which on the page ("All answers must be in Spanish"), so the
column reader is not what Spanish needs. What Spanish needs instead is a second
document: its Section A journalistic text is printed in a separate two-page
insert (2024-hl-015-paper.pdf), which means `sourceMaterial.sourceFileid` —
the field that exists because Art's illustrations live in a companion booklet —
rather than the card's own paperFileid.

WHAT IS NOT SHARED
------------------
The scheme grammar. French prices one ask on one head — "1.(a) ....... 5 Marks"
— and answers it with bullets that carry their own marks. Neither of the others
does:

  German  three levels of head, and the tariff is a SPLIT rather than a value:
          "TEXT I: LESEVERSTÄNDNIS (60 marks) (14, 18, 18, 10)", then
          "Frage 1: (14 marks: (a) 4 marks; (b) 4 marks; (c) 6 marks)", then
          "(a) (4 marks)" and a directive "(Any two: 2 x 2 marks)" over answers
          NUMBERED 1..n. The split notation has at least six printed forms —
          "5 x 2 marks", "3, 2, 1", "(i) 2 marks (ii) 2 x 2 marks",
          "(1 + 2 x 1 mark)", "a: 3 marks; b: 3 marks", "Any two: 2 x 5 marks"
          — and several nest inside one another.

  Spanish "Q. 1 3 × 3m = 9 marks", "Q. 3 4 + 3 + 3 = 10 marks",
          "Q. 4 (2+1) + (2+2+2) + (2+2+2) = 15 marks": the tariff is an
          ARITHMETIC EXPRESSION whose terms are the parts, and Section A is a
          printed CHOICE between prescribed literature and a journalistic text,
          which the census has to keep as two variants rather than as
          duplicates.

Spanish Ordinary is the simplest of the three and the closest to shippable:
"Question 1. LA HABANA: CAPITAL DE CUBA (50 marks)" and then one line per part,
each carrying its own printed mark — "(a) (Porque) hay interesantes museos …
(5m)", "(e) Two of: delfines/estrellas de mar/tortugas marinas (3+3m)". The
head's arithmetic is a CHECKSUM there rather than something to parse: the parts
price themselves.

All three are readable. None is readable by the French reader, and pointing the
French reader at them would produce cards with tariffs nobody printed — the
failure this bank has had five times.

WHAT THIS SCRIPT ESTABLISHES
----------------------------
The scheme's own arithmetic, checked, so the next pass starts from a
denominator rather than from an assumption: every German reading text prints
the split of its own questions, and every one of those splits adds up to the
total printed beside it, in all ten sittings. That is the checksum a German
census would be measured against.
"""
import argparse
import os
import re
import sys
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# --------------------------------------------------------------- German ----
# A reading text and the split of its own questions, printed on its head.
DE_TEXT = re.compile(
    r'^TEXT\s+([IVX]+)\s*:?\s*(LESEVERST\w+)\s*:?\s*\((\d{1,3})\s*marks?\)\s*\(([\d,\s]+)\)',
    re.I)
# The other things a German scheme answers, none of which is a reading ask.
DE_OTHER = re.compile(
    r'^TEXT\s+[IVX]+\s*:?\s*(ANGEWANDTE GRAMMATIK|[ÄA]U[ßS]ERUNG ZUM THEMA)|^SCHRIFTLICHE PRODUKTION',
    re.I)
DE_LISTEN = re.compile(r'^(First|Second|Third|Fourth)\s+Part\s*:', re.I)
# A priced question or part head, in any of the forms the corpus prints.
DE_HEAD = re.compile(r'^(?:Frage|Question)?\s*(\d{1,2})[.:]\s*\(?\s*(\d{1,3})\s*marks?\b', re.I)
DE_PART = re.compile(r'^\(([a-e])\)\s*\(?\s*(\d{1,2})\s*marks?\b|^\(([a-e])\)\s*\((\d{1,2})\s*marks?', re.I)

# -------------------------------------------------------------- Spanish ----
ES_SECTION = re.compile(r'^SECTION\s+([A-E])\b\s*(?:\((\d{1,3})\s*MARKS?\)|TOTAL MARKS:\s*(\d{1,3}))', re.I)
ES_ROUTE = re.compile(r'^(\d)\.\s*\(([ab])\)\s*(.*?)\((\d{1,3})\s*marks?\)', re.I)
ES_HEAD = re.compile(r'^Q\.\s?(\d{1,2})\.?\s*(.*?)=\s*(\d{1,3})\s*marks?\s*$', re.I)
ES_HEAD_PLAIN = re.compile(r'^Q\.\s?(\d{1,2})\.?\s*\((\d{1,3})\s*marks?\)', re.I)
ES_AURAL = re.compile(r'^Aural\b', re.I)


def schemes(subject):
    return sorted(glob.glob(os.path.join(
        ROOT, 'examiner-reports', subject, 'schemes', '*.md')))


def german(show_heads=False):
    print('GERMAN')
    total_texts = total_questions = bad = 0
    for path in schemes('german'):
        stem = os.path.basename(path)[:-3]
        lines = [l.strip() for l in open(path, encoding='utf-8').read().split('\n')]
        texts, other, listen, heads, parts = [], [], 0, 0, 0
        for line in lines:
            m = DE_TEXT.match(line)
            if m:
                split = [int(x) for x in re.findall(r'\d+', m.group(4))]
                texts.append((m.group(1), int(m.group(3)), split))
                continue
            m = DE_OTHER.match(line)
            if m:
                other.append(' '.join(line.split())[:34])
                continue
            if DE_LISTEN.match(line):
                listen += 1
            if DE_HEAD.match(line):
                heads += 1
            if DE_PART.match(line):
                parts += 1
        ok = all(sum(s) == t for _r, t, s in texts)
        if not ok:
            bad += 1
        total_texts += len(texts)
        total_questions += sum(len(s) for _r, _t, s in texts)
        print(f'  {stem}: {len(texts)} reading text(s) holding '
              f'{sum(len(s) for _r, _t, s in texts)} printed questions, splits add up: {ok}')
        print(f'      {heads} priced head(s), {parts} lettered part head(s), '
              f'{listen} listening part(s), also: {", ".join(other) or "—"}')
        if show_heads:
            for roman, tot, split in texts:
                print(f'      TEXT {roman}: {tot} = {" + ".join(map(str, split))}')
    print(f'  TOTAL: {total_texts} reading texts, {total_questions} printed '
          f'questions, {bad} sitting(s) whose printed split does not add up')
    print('  The LEAF is the lettered part beneath each question, which needs the')
    print('  split notation parsed — six printed forms, several of them nested.')


def spanish(show_heads=False):
    print('SPANISH')
    for path in schemes('spanish'):
        stem = os.path.basename(path)[:-3]
        lines = [l.strip() for l in open(path, encoding='utf-8').read().split('\n')]
        sections, routes, heads, expr, aural = [], [], 0, 0, 0
        for line in lines:
            m = ES_SECTION.match(line)
            if m:
                sections.append((m.group(1), int(m.group(2) or m.group(3))))
                continue
            m = ES_ROUTE.match(line)
            if m:
                routes.append(f'{m.group(1)}({m.group(2)}) {m.group(3)[:26].strip()}')
                continue
            if ES_AURAL.match(line):
                aural += 1
            m = ES_HEAD.match(line)
            if m:
                heads += 1
                if re.search(r'[+×x(]', m.group(2)):
                    expr += 1
                continue
            if ES_HEAD_PLAIN.match(line):
                heads += 1
        print(f'  {stem}: sections {sections}')
        print(f'      {heads} priced question head(s), {expr} of them an arithmetic '
              f'expression, {len(routes)} printed route(s), {aural} aural block(s)')
        if show_heads and routes:
            for r in routes:
                print(f'      ROUTE {r}')
    print('  Section A at Higher is a printed CHOICE — prescribed literature OR a')
    print('  journalistic text — so its census keys have to carry the route, the way')
    print('  a Construction Studies choice variant does.')


def papers(subject):
    """Whether the bilingual column reader already handles this subject's pages."""
    from fr_paper import _rows, _column_x                      # noqa: E402
    root = os.path.join(ROOT, 'examiner-reports', subject, 'papers')
    found = 0
    for name in sorted(os.listdir(root)):
        if not name.endswith('-paper.pdf') or 'A00' in name or '015' in name:
            continue
        path = os.path.join(root, name)
        import pymupdf
        with pymupdf.open(path) as doc:
            width = doc[0].rect.width
            pages = doc.page_count
        split_pages = 0
        rows = _rows(path)
        by_page = {}
        for pno, groups in rows:
            by_page.setdefault(pno, []).append((pno, groups))
        for pno, page_rows in by_page.items():
            if any(side == 'R' for _p, gs in page_rows for _x, side, _t in gs):
                split_pages += 1
        found += 1
        print(f'  {name}: {pages} pages, {split_pages} with a bilingual column bound')
    if not found:
        print('  no written booklets on disk')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject', nargs='?', choices=['german', 'spanish'])
    ap.add_argument('--heads', action='store_true')
    ap.add_argument('--papers', action='store_true')
    args = ap.parse_args()
    targets = [args.subject] if args.subject else ['german', 'spanish']
    for subject in targets:
        if args.papers:
            print(subject.upper() + ' PAPERS')
            papers(subject)
        elif subject == 'german':
            german(args.heads)
        else:
            spanish(args.heads)
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
