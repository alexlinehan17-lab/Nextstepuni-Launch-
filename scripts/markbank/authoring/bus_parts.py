#!/usr/bin/env python3
"""Every part the Business marking scheme sets, read from the scheme itself.

    python3 scripts/markbank/authoring/bus_parts.py 2023 hl

Business is an answerbook subject: the paper interleaves question text with
ruled answer space and the generic parser returns page furniture for most of
it, so sixty-six of its parts could not be measured at all. Its scheme does not
have that problem. Sections 2 and 3 print a table of question, tariff and max
mark, and the question in that table is the question the paper asks:

    (B) (i) Outline three provisions of the Sale of Goods and Supply of   3 x 6m  ⟨20⟩
            Services Act 1980 regarding a consumer's statutory rights.    (3+3)
        (ii) Explain the 'right to cancel' (cooling off period) for       2m
             consumers in Ireland.

Section 1 is not here. Its table is tariff only — "2. 3,2,2,2,1 ⟨10⟩" — with no
wording at all, so those parts have to come from the paper.

'clean' says the part's tariff was printed on the same line as its question. When
it was not, the reader had no boundary to cut at and the text it returns is the
question with some of its own answer welded on — a card built from that would
show a student the answer inside the question, so bus_lib refuses it.

Each part is returned as a dict: section, question, part, roman, text, marks,
and — at Ordinary Level, where the scheme prints the answer under the question
in the same cell — answers, the lines that follow it before the next marker.
A part's question line is the one carrying its own tariff in angle brackets;
everything after it until the next marker is the answer to it.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEMES = os.path.join(ROOT, 'examiner-reports/business/schemes')

SECTION = re.compile(r'^SECTION\s+([123])\b')
QHEAD = re.compile(r'^Question\s+(\d{1,2})\b', re.I)
PART = re.compile(r'^\(([A-E])\)\s*(?:\((i{1,3}|iv|vi{0,3})\)\s*)?(.*)$')
# Ordinary Level sets its part marker as a bare capital — "A (i) What do the
# letters CCPC stand for? ⟨10m⟩" — and prints the answer under it, which is a
# better table than the Higher Level one. A bare capital is also how an ordinary
# sentence starts, so it is only read as a marker when the line carries a tariff
# in its own angle brackets AND the letter is the next one due. Both are needed:
# "A Takeover is when one company buys out another company ⟨5m⟩" is an answer to
# part E of 2021 Ordinary Level Question 9, and the tariff test alone read it as
# a second part A, which then overwrote the real one.
PART_BARE = re.compile(r'^([A-E])\s+(?:\((i{1,3}|iv|vi{0,3})\)\s*)?(.*)$')
# Ordinary Level prints its Section 1 support notes AFTER the Section 2 table,
# with no heading between them — the numbered questions simply begin. Read as a
# continuation of Section 2 they land under whatever part was open last, which
# is how 2023 Ordinary Level ended up with six different parts all called
# Q9(E)(i). They are worth having in their own right: unlike the Section 1
# tariff table at the front, these notes print the question AND its answer.
NOTES_Q = re.compile(r'^(\d{1,2})\.\s+(?:\((i{1,3}|iv|vi{0,3})\)\s*)?([A-Z].*)$')
ROMAN = re.compile(r'^\((i{1,3}|iv|vi{0,3})\)\s*(.*)$')
# The tariff column bleeds into the text column when the table is flattened.
# Anything that is only marks, or only a bracketed split, belongs to the tariff.
TARIFF = re.compile(r'^[\d@x×\s,+()⟨⟩.]*m?(?:arks?)?[\d@x×\s,+()⟨⟩.]*$', re.I)
MARKS = re.compile(r'⟨(\d{1,3})\s*m?(?:arks?)?⟩', re.I)
ANGLE = re.compile(r'⟨([^⟩]*)⟩')
NOISE = re.compile(
    r'^(LEAVING CERTIFICATE|MARKING SCHEME|Available Marks|Section \d Available|'
    r'This is a compulsory|Answer \w+ questions?|All questions carry|Part \d|'
    r'Max$|Mark$|Applied Business Question|## Page|⟨\d+⟩$|'
    r'Possible Responses|Examples?:|Marks$)', re.I)
# Words the tariff column adds to a question line: "Source, explain, link".
CUE_NOISE = re.compile(r'^(Source|State|Variable)[,.]? (explain|discussion), link\.?$', re.I)


# The tariff column is flattened into the same line as the question, so its
# fragments land inside the wording: "the 'right to cancel' (cooling off period)
# for 2m consumers in Ireland". Each of these is a tariff form, not English.
BLEED = [
    re.compile(r'⟨[^⟩]*⟩'),                       # ⟨2@8m (4+4)⟩, ⟨20⟩
    re.compile(r'\b\d+\s*[x×@]\s*\d+\s*m?\b', re.I),   # 3 x 6m, 2@8m
    re.compile(r'\b\d+m\b', re.I),                # 2m, 20m
    re.compile(r'\(\s*\d+\s*[+,]\s*[\d+, ]*\)'),    # (2+3+2), (3+3)
    re.compile(r'\bMax\s+Mark\b', re.I),
    re.compile(r'\b\d+\s*marks?\b', re.I),          # 20 marks
    re.compile(r'(?<=\s),[\d,]+(?=\s)'),            # ",7,6" left by "3@7,7,6"
    re.compile(r'\b\d+@\d+\b'),                    # 3@7
]
# The Part heading of the NEXT question is set in the same cell as the last line
# of this one — "...Workplace Relations Commission Enterprise Managing Mark".
TRAILING_HEADING = re.compile(
    r'\s+(?:People in Business|Business Environment|Enterprise|Managing|'
    r'Domestic Environment|International Environment|Finance|Insurance|'
    r'Human Resource Management)?\s*(?:Managing|Enterprise|Mark)+\s*$', re.I)


def _clean(text):
    for pat in BLEED:
        text = pat.sub(' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = TRAILING_HEADING.sub('', text)
    return text.strip(' .,')


def parts(year, level):
    path = os.path.join(SCHEMES, f'{year}-{level}.md')
    with open(path, encoding='utf-8') as fh:
        lines = fh.read().split('\n')

    out, section, question, part, roman = [], None, None, None, None
    notes_q = 0
    for raw in lines:
        line = raw.strip()
        # The repair passes append their own blocks to the end of the scheme
        # markdown. The last part of the table has no marker after it to stop
        # at, so without this it swallows every appended line — 2021 Ordinary
        # Level Q9(E) came back with 268 answer lines, most of them the note to
        # teachers, chopped into fragments.
        if line.startswith('<!-- markbank:'):
            break
        if not line or NOISE.match(line) or CUE_NOISE.match(line):
            continue
        m = SECTION.match(line)
        if m:
            found = int(m.group(1))
            # The scheme prints its tariff table first and its support notes
            # after, and the notes restart the section headings from 1. Ordinary
            # Level 2024 read 219 parts in Sections 2 and 3 — more parts than
            # that paper sets — because every marker in the notes was taken for
            # another part. The table is the first pass through the sections, so
            # a heading that goes backwards ends it.
            if section is not None and found <= section:
                break
            section, question, part, roman = found, None, None, None
            # Section 2 is one compulsory question and never prints a head.
            if section == 2:
                question = 0
            continue
        if section not in (1, 2, 3):
            continue
        if section == 1 and notes_q == 0:
            continue
        m = QHEAD.match(line)
        if m:
            question, part, roman = int(m.group(1)), None, None
            continue
        # A numbered head that carries its own tariff, one past the last one
        # seen, is the next Section 1 note rather than more of Section 2.
        m = NOTES_Q.match(line) if '⟨' in line else None
        if m and int(m.group(1)) == notes_q + 1:
            section, notes_q = 1, int(m.group(1))
            question, part, roman = notes_q, None, m.group(2)
            out.append({'section': 1, 'question': question, 'part': None,
                        'roman': roman, 'text': _clean(m.group(3)),
                        'marks': MARKS.findall(raw), 'answers': [],
                        'clean': bool(MARKS.findall(raw))})
            continue

        m = PART.match(line)
        if not m and '⟨' in line:
            bare = PART_BARE.match(line)
            if bare:
                nxt = 'a' if part is None else chr(ord(part) + 1)
                if bare.group(1).lower() == nxt:
                    m = bare
        if m:
            part, roman = m.group(1).lower(), (m.group(2) or None)
            rest = _clean(m.group(3))
            out.append({'section': section, 'question': question, 'part': part,
                        'roman': roman, 'text': rest, 'marks': MARKS.findall(raw),
                        'answers': [], 'clean': bool(MARKS.findall(raw))})
            continue
        m = ROMAN.match(line)
        if m and part:
            roman = m.group(1)
            out.append({'section': section, 'question': question, 'part': part,
                        'roman': roman, 'text': _clean(m.group(2)),
                        'marks': MARKS.findall(raw), 'answers': [],
                        'clean': bool(MARKS.findall(raw))})
            continue
        # A continuation of the part above: the table wraps its question over
        # several lines and only the first carries the marker.
        if out and not TARIFF.match(line) and question is not None:
            extra = _clean(line)
            if not extra or len(extra) <= 2:
                continue
            # A part's own question ends where its tariff is printed. Ordinary
            # Level sets the answer in the same cell, under the question, and
            # those lines carry the split of that tariff rather than a tariff of
            # their own — so once this part has been given its marks, what
            # follows is answer, not more question.
            if out[-1]['marks']:
                out[-1]['answers'].append(extra)
                # The split for each marking point is printed in the tariff
                # column beside it — "⟨8m⟩" then "⟨(4 + 4)⟩" — and a card's marks
                # have to be those, not a share of the total worked out here.
                out[-1].setdefault('splits', []).extend(
                    t for t in ANGLE.findall(raw) if any(ch.isdigit() for ch in t))
            else:
                out[-1]['text'] = (out[-1]['text'] + ' ' + extra).strip()
                out[-1]['marks'] += MARKS.findall(raw)
    # A part can be read twice where the scheme repeats its table. Keep the
    # fuller reading of each — the one that captured the answer lines and their
    # splits — rather than whichever came last.
    best = {}
    for p in out:
        if len(p['text']) <= 12:
            continue
        key = (p['section'], p['question'], p['part'], p['roman'])
        prev = best.get(key)
        if prev is None or len(p['answers']) > len(prev['answers']):
            best[key] = p
    return list(best.values())


def ref(p, year, level):
    tail = (f"({p['part'].upper()})" if p['part'] else '')
    tail += f"({p['roman']})" if p['roman'] else ''
    q = f"Q{p['question']}" if p['question'] else 'ABQ'
    return f"{year} {level.upper()} Section {p['section']} {q}{tail}"


if __name__ == '__main__':
    y, l = int(sys.argv[1]), sys.argv[2]
    ps = parts(y, l)
    for p in ps:
        print(f"{ref(p, y, l):<34} {','.join(p['marks']) or '-':>6}  {p['text'][:100]}")
        if p.get('splits'):
            print(f"{'':<34} {'':>6}  splits: {' '.join(p['splits'][:8])}")
        for a in p['answers'][:3]:
            print(f"{'':<34} {'':>6}  · {a[:100]}")
    print(f'\n{len(ps)} parts in {y} {l.upper()} Sections 2 and 3')
