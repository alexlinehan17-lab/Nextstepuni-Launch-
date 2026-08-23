#!/usr/bin/env python3
"""Mark Bank — the denominator, counted from the papers themselves.

    python3 scripts/markbank/authoring/paper_census.py maths
    python3 scripts/markbank/authoring/paper_census.py --all
    python3 scripts/markbank/authoring/paper_census.py biology --json out.json

Every coverage failure this bank has had reduces to one habit: measuring
against a number produced by the same reader that was losing the content. The
scheme reader said Maths had 756 priced parts while it was silently dropping
whole questions, so "94% of 756" was announced while a student could open the
2021 paper and find Question 1 absent. The paper is what a student sees, so
the paper is the denominator — this tool counts every ask the papers print
and never reads a marking scheme at all.

What it emits per paper:
  * every LEAF ask — a part with no sub-parts under it, or a question asked
    whole — with the text the reader extracted for it;
  * marks printed against each question, and a checksum: the sum should agree
    with the same paper's other years (the SEC does not change a paper's
    total), so a year that disagrees has lost or invented a question;
  * continuity flags. Question numbers run 1..N with no gaps; letters run
    (a),(b),(c); romans run (i),(ii),(iii). A gap is how every keying bug so
    far has actually presented — an axis label swallowing parts (d)-(g) shows
    up here as a letter gap, not as silence.

A flag is not always a reader bug — but it is always somebody's job to
explain. The census is finished when every flag has a diagnosis.

Layout families (the reason one tool has three modes):
  * merged     — one sitting, numbering runs on across booklets (Biology's
                 Section C booklet continues at Q10). paper.py handles this.
  * papers     — several papers that EACH start at Q1 (Mathematics). Each
                 component is censused as its own paper.
  * sections   — numbering restarts inside the sitting (Business Section 3
                 starts back at Q1; Home Economics restarts per section).
                 paper.py's forward-only question tracking would reject every
                 restarted head as going backwards, so this mode walks the
                 blocks itself and keys every ask by (section, q, part).
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper as PP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

# mode + how a component code maps to a display name. Subjects not listed use
# 'merged' with no component split.
SUBJECTS = {
    'biology': {'mode': 'merged'},
    'chemistry': {'mode': 'merged'},
    'physics': {'mode': 'merged'},
    'agricultural-science': {'mode': 'merged'},
    'economics': {'mode': 'merged'},
    'construction-studies': {'mode': 'merged'},
    'maths': {'mode': 'papers', 'papers': {'100': 'Paper 1', '200': 'Paper 2'}},
    'business': {'mode': 'sections'},
    'home-economics': {'mode': 'sections'},
}

MARKS = re.compile(r'\((\d{1,3})\s*marks?\)', re.I)
# "Section 1", "Section A" as a header — never "Sections 2 and 3", which is a
# cover line for a whole booklet, because \b cannot fall inside "Sections".
SECTION = re.compile(r'\bSection\s+([A-Z]|\d{1,2})\b')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii']


def sittings(subject):
    """[(year, level, [component codes])] for every paper PDF on disk.

    The corpus IS the file listing — Construction Studies holds 2016-2025
    where the others hold 2021-2025, and hard-coding a span would silently
    ignore half of its papers.
    """
    root = PP.papers_dir(subject)
    found = collections.defaultdict(list)
    for f in sorted(os.listdir(root)):
        m = re.fullmatch(r'(\d{4})-(hl|ol)(?:-(\d+))?-paper\.pdf', f)
        if m:
            found[(int(m.group(1)), m.group(2))].append(m.group(3))
    return [(y, l, comps) for (y, l), comps in sorted(found.items())]


def leaves_of(parts):
    """The keys a student actually answers: no sub-parts underneath."""
    keys = set(parts)
    out = []
    for k in keys:
        q, letter, roman = k[-3], k[-2], k[-1]
        if roman is None and letter is not None and any(
                o[:-1] == k[:-1] and o[-1] is not None for o in keys):
            continue                      # (q, a, None) is a parent of (q, a, i)
        out.append(k)
    return sorted(out, key=lambda k: tuple(str(x) for x in k))


def continuity_flags(parts, texts):
    """Every gap in the numbering, which is where keying bugs surface."""
    flags = []
    keys = set(parts)
    prefixes = sorted({k[:-3] for k in keys})     # () or (section,)
    for pre in prefixes:
        qs = sorted({k[-3] for k in keys if k[:-3] == pre})
        want = list(range(min(qs), min(qs) + len(qs))) if qs else []
        if qs != want:
            flags.append({'type': 'question-gap', 'where': str(pre or ''),
                          'detail': f'questions found: {qs}'})
        for q in qs:
            letters = sorted({k[-2] for k in keys
                              if k[:-3] == pre and k[-3] == q and k[-2]})
            if letters:
                expect = [chr(ord('a') + i) for i in range(len(letters))]
                if letters != expect:
                    flags.append({'type': 'letter-gap',
                                  'where': f'{pre or ""} Q{q}',
                                  'detail': f'letters found: {letters}'})
            for letter in {k[-2] for k in keys if k[:-3] == pre and k[-3] == q}:
                roms = sorted({k[-1] for k in keys if k[:-3] == pre
                               and k[-3] == q and k[-2] == letter and k[-1]},
                              key=lambda r: ROMANS.index(r) if r in ROMANS else 99)
                if roms and roms != ROMANS[:len(roms)]:
                    flags.append({'type': 'roman-gap',
                                  'where': f'{pre or ""} Q{q}({letter or ""})',
                                  'detail': f'romans found: {roms}'})
    for k in leaves_of(parts):
        text = texts.get(k, '')
        # isalnum, not ASCII: the papers set variables in the Mathematical
        # Alphanumeric block, and stripping those flagged "Find |AD|." as empty.
        if sum(c.isalnum() for c in text) < 6 and len(text) < 16:
            flags.append({'type': 'empty-leaf', 'where': key_label(k),
                          'detail': f'extracted text: {text!r}'})
    return flags


def key_label(k):
    """(section?, q, letter, roman) -> 'Section A Q3(b)(ii)'."""
    parts = list(k)
    q, letter, roman = parts[-3], parts[-2], parts[-1]
    head = f'Section {parts[0]} ' if len(parts) == 4 else ''
    tail = f'Q{q}'
    if letter:
        tail += f'({letter})'
    if roman:
        tail += f'({roman})'
    return head + tail


def marks_by_question(P_files, subject):
    """{(section?, q): marks} read independently of the part reader.

    An independent pass on purpose: if this map and the part reader disagree
    about which questions exist, one of them is wrong, and that disagreement
    is exactly what the census exists to surface.
    """
    out = {}
    section = None
    q = None
    for path in P_files:
        for block in PP._blocks(path):
            s = SECTION.search(block[:80])
            if s and len(block) < 200:
                section = s.group(1)
            h = re.match(r'^(?:Question\s+(\d{1,2})\b|(\d{1,2})\.\s+(?=[A-Z(\d]))',
                         block.strip())
            if not h:
                un = PP.RUBRIC_HEAD.sub('', block.strip())
                if un != block.strip():
                    h = re.match(r'^(?:Question\s+(\d{1,2})\b|(\d{1,2})\.\s+)',
                                 un)
                    block = un
            if h:
                q = int(h.group(1) or h.group(2))
            m = MARKS.search(block)
            if m and q is not None and (section, q) not in out:
                out[(section, q)] = int(m.group(1))
    return out


def census_merged(subject, year, level, component=None):
    P = PP.Paper(subject, year, level, component=component)
    P._adopt_unlettered()
    texts = {k: (P.text(*k) or '') for k in P.parts}
    return set(P.parts), texts, P.files


def census_sections(subject, year, level):
    """The section-restart walker: Business and Home Economics.

    paper.py reads a sitting as one forward-numbered sequence, and these
    papers start again at Question 1 (or lose their section letter) part way
    through — so every restarted question would be rejected as going
    backwards, which is invisible from outside. Keys carry the section.
    """
    P = PP.Paper.__new__(PP.Paper)
    P.subject, P.year, P.level, P.component = subject, year, level, None
    root = PP.papers_dir(subject)
    P.files = sorted(os.path.join(root, f) for f in os.listdir(root)
                     if re.fullmatch(rf'{year}-{level}(-\d+)?-paper\.pdf', f))
    if not P.files:
        raise FileNotFoundError(f'no {year} {level} paper for {subject}')

    parts, stems = {}, {}
    section, q, letter, roman = None, None, None, None
    for path in P.files:
        blocks = []
        for block in PP._blocks(path):
            for text in PP.INLINE_QHEAD.split(block):
                text = text.strip()
                if not text:
                    continue
                head = re.match(r'(\d{1,2}\.)\s+(?=\()', text)
                prefix = ''
                if head:
                    prefix, text = head.group(1) + ' ', text[head.end():]
                pieces = [p.strip() for p in PP.INLINE_MARKER.split(text)
                          if p.strip()]
                for i, piece in enumerate(pieces):
                    blocks.append((prefix + piece) if i == 0 else piece)
        for text in blocks:
            s = SECTION.search(text[:80])
            if s and len(text) < 200:
                if s.group(1) != section:
                    section, q = s.group(1), None
            m = PP.QHEAD.match(text)
            if not m:
                un = PP.RUBRIC_HEAD.sub('', text, count=1)
                if un != text:
                    text, m = un, PP.QHEAD.match(un)
            if m:
                found = int(m.group(1) or m.group(2))
                # Within a section numbering only moves forward, and a fresh
                # section accepts any small start. The guard is the same one
                # paper.py carries: a number leaping ahead is a numbered list
                # inside an answer, not a head.
                if q is None or q < found <= q + 3:
                    q = found
                    letter = roman = None
                    rest = text[m.end():].strip()
                    if rest and PP._leading(rest)[:2] != (None, None):
                        text = rest
                    else:
                        if rest and not PP.RUBRIC.match(rest):
                            stems.setdefault((section, q, None), []).append(rest)
                        continue
            if q is None:
                continue
            if PP.RUBRIC.match(text):
                continue
            # Business prints its part markers in capitals — (A), (B), (C) —
            # and paper.py's marker grammar is lowercase, so every lettered
            # part of every Business question was invisible and the census
            # saw only whole questions. Normalised here, at the marker
            # position only.
            while True:
                u = re.match(r'\(([A-H])\)\s*', text)
                if not u:
                    break
                text = f'({u.group(1).lower()}) ' + text[u.end():]
                break
            fl, fr, rest = PP._leading(text)
            if fl or fr:
                if fl:
                    letter, roman = fl, fr
                else:
                    roman = fr
                key = (section, q, letter, roman)
                parts.setdefault(key, [])
                if rest:
                    parts[key].append(rest)
                continue
            if PP.FURNITURE.match(text):
                continue
            stems.setdefault((section, q, letter), []).append(text)

    # A question with no marker anywhere is asked whole — Home Economics
    # Section A is nothing but these.
    for (section_, q_, letter_), lines in list(stems.items()):
        if letter_ is not None or not lines:
            continue
        if any(k[0] == section_ and k[1] == q_ for k in parts):
            continue
        parts[(section_, q_, None, None)] = list(lines)

    texts = {k: PP.unligature(' '.join(' '.join(v).split())) for k, v in parts.items()}
    return set(parts), texts, P.files


def census_subject(subject):
    cfg = SUBJECTS.get(subject, {'mode': 'merged'})
    papers = []
    for year, level, comps in sittings(subject):
        if cfg['mode'] == 'papers':
            units = [(cfg['papers'].get(c, c), c) for c in comps if c]
        else:
            units = [(None, None)]
        for label, comp in units:
            try:
                if cfg['mode'] == 'sections':
                    parts, texts, files = census_sections(subject, year, level)
                else:
                    parts, texts, files = census_merged(subject, year, level, comp)
            except Exception as e:                       # noqa: BLE001
                papers.append({'year': year, 'level': level, 'paper': label,
                               'error': f'{type(e).__name__}: {e}'})
                continue
            leaves = leaves_of(parts)
            flags = continuity_flags(parts, texts)
            marks = marks_by_question(files if cfg['mode'] != 'papers' else
                                      [f for f in files], subject)
            papers.append({
                'year': year, 'level': level, 'paper': label,
                'leafCount': len(leaves),
                'leaves': [{'key': list(k), 'label': key_label(k),
                            'text': texts.get(k, '')[:160]} for k in leaves],
                'marksSum': sum(marks.values()) if marks else None,
                'marksQuestions': len(marks),
                'flags': flags,
            })
    # The checksum: a paper's total does not change year to year, so the mode
    # is the expectation and a deviating year has lost or invented content.
    sums = collections.Counter()
    for p in papers:
        if p.get('marksSum'):
            sums[(p['level'], p.get('paper'), p['marksSum'])] += 1
    expected = {}
    for (level, label, total), n in sums.items():
        cur = expected.get((level, label))
        if cur is None or n > cur[1]:
            expected[(level, label)] = (total, n)
    for p in papers:
        if p.get('marksSum') and expected.get((p['level'], p.get('paper'))):
            want = expected[(p['level'], p.get('paper'))][0]
            if p['marksSum'] != want:
                p['flags'].append({
                    'type': 'marks-checksum',
                    'where': f"{p['year']} {p['level']} {p.get('paper') or ''}",
                    'detail': f"marks sum {p['marksSum']}, other years say {want}"})
    return {'subject': subject, 'mode': cfg['mode'], 'papers': papers}


def report(result):
    subject = result['subject']
    total = sum(p.get('leafCount', 0) for p in result['papers'])
    nflags = sum(len(p.get('flags', [])) for p in result['papers'])
    errs = [p for p in result['papers'] if 'error' in p]
    print(f"{subject}: {total} leaf asks across {len(result['papers'])} papers"
          f" ({result['mode']} mode), {nflags} flag(s), {len(errs)} unreadable")
    for p in result['papers']:
        tag = f"{p['year']} {p['level'].upper()}" + \
              (f" {p['paper']}" if p.get('paper') else '')
        if 'error' in p:
            print(f"  {tag}: ERROR {p['error']}")
            continue
        line = f"  {tag}: {p['leafCount']} asks"
        if p.get('marksSum'):
            line += f", marks sum {p['marksSum']} over {p['marksQuestions']} questions"
        print(line)
        for f in p['flags']:
            print(f"      FLAG {f['type']:14} {f['where']}: {f['detail']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--json')
    args = ap.parse_args()
    targets = sorted(SUBJECTS) if args.all else [args.subject]
    if not targets or targets == [None]:
        ap.error('name a subject or pass --all')
    out = []
    for s in targets:
        result = census_subject(s)
        report(result)
        out.append(result)
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(out if args.all else out[0], fh, ensure_ascii=False, indent=1)
        print(f'wrote {args.json}')


if __name__ == '__main__':
    main()
