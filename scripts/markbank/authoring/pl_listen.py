#!/usr/bin/env python3
"""Polish listening: the Listening Comprehension Test as Mark Bank cards.

    python3 scripts/markbank/authoring/pl_listen.py draft 2026 hl   # paper + scheme, side by side
    python3 scripts/markbank/authoring/pl_listen.py cards 2026 hl   # the cards the spec builds

Treatment D (REVIEW/2026-11-pack1/D-languages, approved 18 Nov 2026): one card
per printed listening question, scored on its own, carrying the year's SEC
recording (data/polishAudio.json, one file a year for both levels) and the
booklet page the question is printed on, as live German listening does
(de_listen.py).

WHY A REVIEWED SPEC, NOT A READER
---------------------------------
The Polish listening scheme is set as tables and lists the SEC varies sitting
by sitting: two-column tables welded into one text row ("(a) Wymień 2 wady ...
(b) Wymień 2 zalety ..."), a lower-paid alternative after "or" ("- zamieszanie
(1m)"), "Any N of:" over a tariff that prices a different N, true/false answered
"F". A reader that guessed among those shapes would ship a wrong row the gates
cannot see. So every card is a SPEC (pl_listen_specs.py) whose every string is
a SELECTOR: a line of the scheme's .md (the text the build's provenance check
reads) or of the paper's text layer, named by its line number, optionally cut at
printed anchors. Nothing a student reads is typed here; the spec only chooses
which printed lines are the question and which are the answers, and the marks
are read from the printed tariff and checked against the rows.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import pl_paper                                                  # noqa: E402

AUDIO = os.path.join(ROOT, 'data', 'polishAudio.json')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

LISTEN_START = re.compile(r'^Listening\s+comprehension\b', re.I)
LISTEN_END = re.compile(r'^(?:APPENDIX|<!-- markbank:)', re.I)
SECTION_HEAD = re.compile(r'^Cz[eę][sś][cć]\s+([A-F])\b')
Q_HEAD = re.compile(r'^(\d{1,2})\s*\.?\s*(?=\S)')
PAGE_MARK = re.compile(r'^##\s*Page\s*(\d+)\s*$')
TARIFF_ANY = re.compile(
    r'\(\s*(?:(\d{1,2})\s*[x×]\s*)?(\d{1,2})\s*(?:m|marks?)\s*\)'
    r'|\(\s*(\d{1,2})((?:\s*\+\s*\d{1,2}){1,7})\s*(?:m|marks?)\s*\)', re.I)


# ------------------------------------------------------------ the scheme ---
def scheme_md_path(year, level):
    return os.path.join(ROOT, 'examiner-reports', 'polish', 'schemes', f'{year}-{level}.md')


def scheme_lines(year, level):
    """The .md, numbered from 1 as an editor shows it."""
    with open(scheme_md_path(year, level), encoding='utf-8') as fh:
        return fh.read().split('\n')


def scheme_page_of(lines, n):
    """The PDF page a .md line sits on (the extractor's own "## Page N")."""
    page = None
    for i in range(min(n, len(lines))):
        m = PAGE_MARK.match(lines[i].strip())
        if m:
            page = int(m.group(1))
    return page


def scheme_blocks(year, level):
    """{(section, q): (first line, last line)} of the listening section.

    A head is the next number in its section's run, so a "1990." or a bare
    answer number inside a block is never a head.
    """
    lines = scheme_lines(year, level)
    start = next(i for i, l in enumerate(lines) if LISTEN_START.match(l.strip()))
    end = next((i for i in range(start + 1, len(lines)) if LISTEN_END.match(lines[i].strip())),
               len(lines))
    blocks, section, q, first = {}, None, 0, None

    def close(last):
        if section and q and first is not None:
            blocks[(section, q)] = (first + 1, last)

    for i in range(start + 1, end):
        text = lines[i].strip()
        sm = SECTION_HEAD.match(text)
        if sm:
            close(i)
            section, q, first = sm.group(1), 0, None
            continue
        qm = Q_HEAD.match(text)
        if section and qm and int(qm.group(1)) == q + 1:
            close(i)
            q, first = int(qm.group(1)), i
    close(end)
    return blocks


# -------------------------------------------------------------- the paper ---
def aural_lines(year, level):
    path = pl_paper.paper_path(year, level, 'A00')
    lines = pl_paper.read_lines(path)
    return [l for l in lines if not (pl_paper.FURNITURE.match(l.text) and len(l.text) < 60)]


def paper_blocks(year, level):
    """{(section, q): [Line]} for every numbered question of the booklet.

    The block is everything the booklet prints between this question's number
    and the next one's, in its own section: its words, a table's row labels,
    a multiple-choice question's options, and the answer-box markers.
    """
    lines = aural_lines(year, level)
    by_page = pl_paper.PlPaper._section_by_page(lines, pl_paper.AURAL_TAB)
    blocks, section, q = {}, None, 0
    for line in lines:
        page_section = by_page.get(line.page)
        if page_section != section:
            section, q = page_section, 0
        if section is None or pl_paper.AURAL_TAB.match(line.text):
            continue
        nm = pl_paper.NUMBERED.match(line.text)
        if nm and int(nm.group(1)) == q + 1:
            q = int(nm.group(1))
            blocks[(section, q)] = [line]
            continue
        if q:
            blocks[(section, q)].append(line)
    return blocks


def section_heads(year, level):
    """{section: (head line, its page)}: "Część A Wywiad z ..." as printed."""
    out = {}
    for line in aural_lines(year, level):
        m = pl_paper.AURAL_TAB.match(line.text)
        if m and m.group(1) not in out:
            out[m.group(1)] = (line.text, line.page)
    return out


# --------------------------------------------------------------- the CLI ---
def draft(year, level):
    lines = scheme_lines(year, level)
    sb = scheme_blocks(year, level)
    pb = paper_blocks(year, level)
    heads = section_heads(year, level)
    keys = sorted(set(sb) | set(pb))
    for key in keys:
        if key[1] == 1:
            print(f'\n######## Część {key[0]}: {heads.get(key[0], ("?", None))[0]}')
        print(f'\n=== L{key[0]} Q{key[1]}')
        for l in pb.get(key, []):
            print(f'   P p{l.page} y{l.y:5.0f} x{l.x:4.0f} | {l.text}')
        if key in sb:
            a, b = sb[key]
            for n in range(a, b + 1):
                if lines[n - 1].strip():
                    print(f'   S {n:4d} | {lines[n - 1]}')
        else:
            print('   S (no scheme block)')


def main():
    cmd, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if cmd == 'draft':
        draft(year, level)
    elif cmd == 'cards':
        import pl_listen_specs
        for c in pl_listen_specs.cards(year, level):
            print(json.dumps(c, ensure_ascii=False)[:600])
    return 0


if __name__ == '__main__':
    sys.exit(main())
