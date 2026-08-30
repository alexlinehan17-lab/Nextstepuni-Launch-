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
    # English choices and holistic subparts cannot be represented by the
    # generic leaf parser. `english_census.py` is its paper-only denominator;
    # this entry keeps it inside every `--all` coverage run.
    'english': {'mode': 'english'},
    # Irish's selectable units cross listening halves, composition choices and
    # holistic literature options. irish_cards.py reads all twenty papers and
    # emits the dedicated, count-pinned census used by the generic ratchet.
    'irish': {'mode': 'irish'},
    'business': {'mode': 'sections'},
    'home-economics': {'mode': 'sections'},
    # Two booklets: 038 carries Section A (short answer, attempt any nine) and
    # Section B (long questions, attempt any two); 040 carries Section C, one
    # programming question answered on a computer. The sections are named on
    # the page, so the census reads them rather than the booklet code.
    'computer-science': {'mode': 'sections'},
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
        # Negative numbers are printed choice VARIANTS (Construction Studies
        # sets Q10 twice joined by OR; the alternative files under -10) and sit
        # outside the run.
        # Negative numbers are choice variants, and 'ABQ' is Business's
        # headless compulsory question — neither sits in the numeric run.
        qs = sorted({k[-3] for k in keys if k[:-3] == pre
                     and isinstance(k[-3], int) and k[-3] > 0})
        want = list(range(min(qs), min(qs) + len(qs))) if qs else []
        if qs != want:
            flags.append({'type': 'question-gap', 'where': str(pre or ''),
                          'detail': f'questions found: {qs}'})
        # A paper starts at Question 1. A census that starts later has LOST a
        # leading question — Economics lost Q1 twice with no flag firing,
        # because a gap detector only sees interior holes.
        if qs and isinstance(qs[0], int) and qs[0] > 1:
            flags.append({'type': 'question-gap', 'where': str(pre or ''),
                          'detail': f'first question found is Q{qs[0]}'})
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
    tail = ('ABQ' if q == 'ABQ'
            else f'Q{-q}-alt' if isinstance(q, int) and q < 0 else f'Q{q}')
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


ROM_INLINE = re.compile(r'\((i{1,3}|iv|v)\)\s*')


def complete_leading_romans(parts, texts, stem=lambda q, letter: ''):
    """Synthesize the roman leaves a part carries but never opens.

    Two printings, one rule. Chemistry writes "(i) ..., (ii) ..." INSIDE a
    letter's sentence and only breaks to block-leading markers at (iii), so
    the census saw romans starting mid-run and 16 shipped cards orphaned
    against asks that were on the page all along. Agricultural Science prints
    a letter whose body IS its first ask and then numbers the next one (ii).
    In both cases the parent's own text supplies the missing leading romans.
    """
    parts = set(parts)
    for (q, letter) in {(k[-3], k[-2]) for k in parts if k[-2] and k[-1]}:
        roms = sorted((k[-1] for k in parts if k[-3] == q and k[-2] == letter
                       and k[-1]),
                      key=lambda r: ROMANS.index(r) if r in ROMANS else 99)
        first = ROMANS.index(roms[0]) if roms[0] in ROMANS else 0
        if first == 0:
            continue
        # The run can sit in the letter's own text OR in its stem — Chemistry
        # prints the (i)/(ii) sentence after the part's sealed opening, which
        # files it as stimulus prose.
        parent = ' '.join(t for t in (texts.get((q, letter, None), ''),
                                      stem(q, letter) or '') if t)
        need = ROMANS[:first]
        markers = [m.group(1) for m in ROM_INLINE.finditer(parent)]
        if markers[:len(need)] == need:
            spans = list(ROM_INLINE.finditer(parent))
            for i, rom in enumerate(need):
                start = spans[i].end()
                end = spans[i + 1].start() if i + 1 < len(spans) else len(parent)
                parts.add((q, letter, rom))
                texts[(q, letter, rom)] = parent[start:end].strip()
        elif len(need) == 1 and sum(c.isalnum() for c in parent) >= 6:
            parts.add((q, letter, 'i'))
            texts[(q, letter, 'i')] = parent.strip()
    return parts


def census_merged(subject, year, level, component=None):
    P = PP.Paper(subject, year, level, component=component)
    P._adopt_unlettered()
    texts = {k: (P.text(*k) or '') for k in P.parts}
    parts = complete_leading_romans(P.parts, texts, stem=P.stem)
    return parts, texts, P.files


def census_sections(subject, year, level):
    """The section-restart walker: Business and Home Economics.

    paper.py reads a sitting as one forward-numbered sequence, and these
    papers start again at Question 1 (or lose their section letter) part way
    through — so every restarted question would be rejected as going
    backwards, which is invisible from outside. Keys carry the section.

    The first audit of this walker found five ways it lost content, all now
    guarded here: section tokens taken from instruction prose ("Write your
    answer in the answerbook containing Section A." flipped 2025's Section B
    into A); capital part markers Business prints as (A)-(E); ruled answer
    blanks ("(i)" over a blank line) keyed as parts, which also blocked the
    real ask from whole-question adoption; the Applied Business Question,
    which is compulsory, worth 80 marks, and headless; and Home Economics'
    Section C electives, whose sub-heads print glued as "1.(a)" / "or 1.(c)".
    """
    P = PP.Paper.__new__(PP.Paper)
    P.subject, P.year, P.level, P.component = subject, year, level, None
    root = PP.papers_dir(subject)
    P.files = sorted(os.path.join(root, f) for f in os.listdir(root)
                     if re.fullmatch(rf'{year}-{level}(-\d+)?-paper\.pdf', f))
    if not P.files:
        raise FileNotFoundError(f'no {year} {level} paper for {subject}')

    # Assemble the block stream first, with the glued-head and capital-marker
    # splits applied, so the neighbour guards can see the whole paper.
    blocks = []
    for path in P.files:
        for block in PP._blocks(path):
            for text in PP.INLINE_QHEAD.split(block):
                # Capital markers mid-block: Business glues "(B) Outline..."
                # onto the tail of (A)'s prose.
                for text in re.split(
                        r'\s(?=\((?:[A-H]|[a-hj-l]|i{1,3}|iv|vi{0,3}|ix|xi{0,3})\)'
                        r'\s+[A-Z(0-9\u201c"])', text):
                    # Home Economics Section C glues its elective sub-heads:
                    # "or 1.(c)" / "and 3.(b)" / "4.(a)" — split each onto its
                    # own line so the walker can read it as a head.
                    for text in re.split(r'\s(?=(?:and\s+|or\s+)?\d\.\([a-z])', text):
                        text = text.strip()
                        if not text:
                            continue
                        head = re.match(r'(\d{1,2}\.)\s+(?=\()', text)
                        prefix = ''
                        if head:
                            prefix, text = head.group(1) + ' ', text[head.end():]
                        pieces = [x.strip() for x in PP.INLINE_MARKER.split(text)
                                  if x.strip()]
                        for i, piece in enumerate(pieces):
                            blocks.append((prefix + piece) if i == 0 else piece)

    # A lone number beside other lone numbers is a matching-table row or an
    # answerbook rule, not a head — the same neighbour argument paper.py makes
    # for axis labels. 2022 HL Business lost Q2-Q5 to a matching table.
    lone = [i for i, t in enumerate(blocks)
            if re.fullmatch(r'[-\u2212]?\d{1,2}\.?', t.strip())]
    scaffold = {i for i in lone if i - 1 in lone or i + 1 in lone}
    # A run of short numbered lines is an option list inside a question
    # ('1. Merger  2. Strategic alliance  ...'), not a run of question heads —
    # walking it re-keyed four Business sittings' Section 1.
    # Option rows are bare terms with no sentence punctuation ('1. Merger');
    # a short numbered ASK ends in one ('7. List the uses of flour.') and Home
    # Economics' Section A is made of exactly those — the guard must split on
    # the full stop, not the length.
    listy = [i for i, t in enumerate(blocks)
             if re.fullmatch(r'\d{1,2}\.\s+[^.?!]{1,40}', t.strip())]
    for i in listy:
        if (i - 1 in listy and i + 1 in listy) \
                or (i + 1 in listy and i + 2 in listy) \
                or (i - 1 in listy and i - 2 in listy):
            scaffold.add(i)

    parts, stems = {}, {}
    section, q, letter, roman = None, None, None, None
    for index, text in enumerate(blocks):
        if index in scaffold:
            continue
        # A marker-only block — "(B)" alone, its content following — is a real
        # two-line part opening, so it keys normally; a ruled answer BLANK
        # (the same shape with nothing after it) dies in the post-walk
        # empty-part drop instead. Skipping them all here lost Business its
        # every (B).
        # A section header is a heading, not a mention: anchored at the block
        # start, never containing a second "Section" (booklet covers read
        # "Section B and Section C"), and short or marks-bearing.
        sh = re.match(r'(?:SECTION|Section)\s+([A-C]|\d{1,2})\b(.{0,160})', text)
        if sh and 'Section' not in sh.group(2) \
                and (len(text) < 200 or 'marks' in sh.group(2).lower()):
            # Two guards, both earned. Sections only move FORWARD — the
            # answerbook repeats earlier sections' names and re-opening one
            # keyed hundreds of phantom questions from ruled pages. And a new
            # section only opens once the CURRENT one holds a part — the
            # instructions page lists every section with its marks ('Section
            # B 130 marks Answer Question 1...'), and following that listing
            # walked the tracker to C before the paper had begun, filing all
            # of Section A under C.
            if sh.group(1) != section and (section is None
                                           or sh.group(1) > section) \
                    and (section is None
                         or any(k[0] == section for k in parts)):
                section, q, letter, roman = sh.group(1), None, None, None
            # 'Section 2 Applied Business Question 80 marks' is one block —
            # the header AND the headless compulsory question it opens.
            if re.search(r'Applied\s+Business\s+Question', sh.group(2)):
                q = 'ABQ'
            continue
        # The Applied Business Question: compulsory, 80 marks, and headless —
        # it never says "Question N", so it needs its own key.
        if re.match(r'Applied\s+Business\s+Question', text):
            q, letter, roman = 'ABQ', None, None
            continue
        # Home Economics Section C: "Elective 1 – Home Design..." heads the
        # elective, whose sub-heads then use the elective's own number.
        el = re.match(r'Elective\s+(\d)\b', text)
        if el and str(section) == 'C':
            q, letter, roman = int(el.group(1)), None, None
            continue
        # Glued elective sub-head: "1.(a) ..." (often prefixed and/or or-ed).
        gl = re.match(r'(?:and\s+|or\s+)?(\d)\.\(([a-z])\)\s*', text)
        if gl and str(section) == 'C':
            q, letter, roman = int(gl.group(1)), gl.group(2), None
            key = (section, q, letter, None)
            parts.setdefault(key, [])
            rest = text[gl.end():].strip()
            if rest:
                parts[key].append(rest)
            continue
        m = PP.QHEAD.match(text)
        if not m:
            un = PP.RUBRIC_HEAD.sub('', text, count=1)
            if un != text:
                text, m = un, PP.QHEAD.match(un)
        if not m and isinstance(q, int):
            # Business Section 1 sets some heads as a bare '6.' in a block of
            # its own, the ask following. Only the next number due, never one
            # from a scaffold run — and only when real prose follows: the
            # answerbook's ruled pages interleave bare numbers with 'Question'
            # and 'Start each question on a new page', which walked the
            # counter to a phantom Q16.
            ln = re.match(r'^(\d{1,2})\.?$', text)
            if ln and int(ln.group(1)) == q + 1:
                ahead = ' '.join(blocks[index + 1:index + 5])
                prose = re.sub(
                    r'\b(Question|Part|Start each question on a new page'
                    r'|SECTION|Section)\b', '', ahead)
                if len(prose.strip()) >= 30:
                    q, letter, roman = q + 1, None, None
                continue
        if m and re.match(r'\s*(?:\([a-z]+\)\s*)?(?:is|are)\s+worth\b'
                          r'|\s*carr(?:ies|y)\b', text[m.end():]):
            # 'Question 1 is worth 80 marks.' is the instructions pricing a
            # question, not the question — reading it as a head walked the
            # counter to 4 before the paper began and threw Q1-Q3 away as
            # going backwards, in every sitting.
            m = None
        if m:
            found = int(m.group(1) or m.group(2))
            # Within a section numbering only moves forward, and a fresh
            # section accepts any small start.
            if q in (None, 'ABQ') or (isinstance(q, int) and q < found <= q + 3):
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
        u = re.match(r'\(([A-H])\)\s*', text)
        if u:
            text = f'({u.group(1).lower()}) ' + text[u.end():]
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

    # Drop keys that never accumulated text (unlabelled blanks), THEN adopt
    # whole questions — the order matters, because a phantom part suppresses
    # adoption for its whole question.
    parts = {k: v for k, v in parts.items() if any(x.strip() for x in v)}
    scaffold_text = re.compile(
        r'^(?:(?:Question|Part|Start each question on a new page|SECTION'
        r'\s+\d|Section\s+\w|and Answerbook)\s*)+$')
    parts = {k: v for k, v in parts.items()
             if not scaffold_text.match(' '.join(' '.join(v).split()))}
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
    if cfg['mode'] == 'irish':
        path = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'irish-census.json')
        payload = json.load(open(path, encoding='utf-8'))
        papers = []
        for source in payload['papers']:
            asks = [ask for ask in payload['asks']
                    if ask['year'] == source['year']
                    and ask['level'] == source['level']
                    and ask['paper'] == source['paper']]
            papers.append({
                'year': source['year'], 'level': source['level'],
                'paper': f"Paper {source['paper']}",
                'leafCount': len(asks),
                'leaves': [{
                    'key': [ask['id']], 'label': ask['questionRef'],
                    'text': '', 'status': ask['status'],
                } for ask in asks],
                'marksSum': None, 'marksQuestions': 0, 'flags': [],
            })
        if payload.get('cardUnitCount') != sum(p['leafCount'] for p in papers):
            raise AssertionError('Irish authored census count is stale')
        return {'subject': subject, 'mode': cfg['mode'], 'papers': papers}
    if cfg['mode'] == 'english':
        # Import lazily so the ordinary census remains independent of PyMuPDF
        # until English is actually requested.
        from english_census import build as build_english  # noqa: E402
        payload = build_english()
        papers = []
        for source in payload['papers']:
            paper_number = int(source['component']) // 100
            asks = [ask for ask in payload['asks']
                    if ask['year'] == source['year']
                    and ask['level'] == source['level']
                    and ask['paper'] == paper_number]
            papers.append({
                'year': source['year'], 'level': source['level'],
                'paper': f'Paper {paper_number}',
                'leafCount': len(asks),
                'leaves': [{
                    'key': [ask['id']], 'label': ask['questionRef'],
                    'text': '', 'status': ask['status'],
                } for ask in asks],
                'marksSum': None, 'marksQuestions': 0, 'flags': [],
            })
        return {'subject': subject, 'mode': cfg['mode'], 'papers': papers}
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
