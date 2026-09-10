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
    # Art's real practice units are the separately marked task and fixed
    # printed choice, not the outer question number. The dedicated census also
    # preserves the legacy/current specification boundary and image bindings.
    'art': {'mode': 'art'},
    # Geography has one base task per printed short question or separately
    # selectable Part Two A/B/C task. Its dedicated census also records the
    # historical map/aerial tasks held until their companion sources exist.
    'geography': {'mode': 'geography'},
    'business': {'mode': 'sections'},
    # LCVP's Link Modules paper is COMMON level — one paper, sat by everyone,
    # filed under the level token 'cl'. Three sections that each restart at
    # Q.1, so the keys carry the section; but its own walker rather than the
    # Business/Home-Ec one, because two things here are LCVP's alone: every
    # head is printed "Q.1" (the shared QHEAD reads "1." and "Question 1"),
    # and Section C reprints EVERY question as a contents listing before
    # setting them, which the forward-only walker would have read as the
    # section itself and then rejected the real questions as going backwards.
    'lcvp': {'mode': 'sections', 'walker': 'lcvp'},
    'home-economics': {'mode': 'sections'},
    # Two booklets: 038 carries Section A (short answer, attempt any nine) and
    # Section B (long questions, attempt any two); 040 carries Section C, one
    # programming question answered on a computer. The sections are named on
    # the page, so the census reads them rather than the booklet code.
    'computer-science': {'mode': 'sections'},
    # Two booklets: 014 carries Section A (core short questions, all answered)
    # and 039 carries Section B (two core long questions) and Section C (five
    # options, one answered). The sections are named on the page, and each
    # section restarts its numbering at 1, so the census reads the sections.
    'technology': {'mode': 'sections'},
    # Religious Education restarts nothing and numbers almost nothing: three
    # UNITS hold ten lettered SECTIONS, and only Section A (Unit One) prints
    # "Question 1..3" at all. Sections B-J address their asks by part alone,
    # so an ask's key there carries q=None and its citation reads
    # "Section E Q(b)(ii)". Keys are still (section, q, letter, roman), so the
    # ledger reads it in `sections` mode; only the walker differs.
    'religious-education': {'mode': 'sections', 'walker': 're'},
    # History is TWO papers per sitting, not one: a candidate sits either the
    # Later Modern field of study or the Early Modern field, and the SEC prints
    # them as separate papers (subjects 004 and 096) under one marking scheme.
    # The field is therefore a component, exactly as Maths' two booklets are,
    # and a citation names it: "2021 HL Early Modern Section 1 Q1(a)".
    #
    # Inside a paper the numbering restarts twice over. Sections 2 and 3 are
    # divided into TOPICS that each set questions 1..4 (Higher) or parts A, B
    # and C (Ordinary), so a bare question number addresses nothing: the
    # section token carries the topic and the Ordinary part with it, and a key
    # reads ('2 Topic 1 A', 1, None, None) -> "Section 2 Topic 1 A Q1".
    'history': {'mode': 'sections', 'walker': 'history',
                'components': {'lm': 'Later Modern', 'em': 'Early Modern'}},
    # French sits TWO booklets at one sitting — the written paper and a
    # separate Listening Comprehension Test with its own SEC file id — and
    # numbers both from 1 inside every section, so the section carries the
    # address. Its section token is compound where the paper's own is not
    # enough to address an ask: Section A prints two reading comprehensions at
    # Higher and four at Ordinary, each numbering its questions from 1, so
    # "A1" is Section A's first comprehension and "LC" the listening test's
    # Section C. Its own walker, because both booklets are printed
    # bilingually in columns and the generic reader has no notion of a column.
    'french': {'mode': 'sections', 'walker': 'lang'},
}

MARKS = re.compile(r'\((\d{1,3})\s*marks?\)', re.I)
# "Section 1", "Section A" as a header — never "Sections 2 and 3", which is a
# cover line for a whole booklet, because \b cannot fall inside "Sections".
SECTION = re.compile(r'\bSection\s+([A-Z]|\d{1,2})\b')
# A marker block the walker can see, standing for "a new booklet starts here".
FILE_BREAK = '\x00FILE-BREAK\x00'

# Where a booklet stops setting questions and starts talking about itself.
BACK_MATTER = re.compile(
    r'^(?:Answerbook for Section|Acknowledgements\b|Copyright notice\b)')
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
        # 'cl' is the common-level token: LCVP is examined at one level, and
        # the SEC's own file id says so with the level letter C.
        # The component token is not always numeric. Maths files its two
        # booklets as 100/200, but History's two FIELDS OF STUDY are 'lm' and
        # 'em' — separate papers sat by different candidates on the same
        # afternoon, and a digits-only pattern found neither of them.
        m = re.fullmatch(r'(\d{4})-(hl|ol|cl)(?:-([a-z0-9]+))?-paper\.pdf', f)
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
        # A headless question (Religious Education's Sections B-J) sits
        # outside the numeric run but still prints a lettered run that can
        # gain a hole, so it is walked here as well.
        headless = [None] if any(k[:-3] == pre and k[-3] is None
                                 for k in keys) else []
        for q in qs + headless:
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
            # A headless section — Religious Education's Sections B-J — is
            # addressed by its part alone. The paper prints no number, so the
            # label prints none either.
            else 'Q' if q is None
            else f'Q{-q}-alt' if isinstance(q, int) and q < 0 else f'Q{q}')
    if letter:
        tail += f'({letter})'
    if roman:
        tail += f'({roman})'
    # A unit that is priced WHOLE and numbers nothing beneath it — History's
    # Ordinary parts B and C, which the scheme answers with one ceiling each —
    # is addressed by its section alone. A bare "Q" after it would name a
    # question the paper does not print.
    if q is None and letter is None and roman is None:
        return head.strip()
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
        for block in PP._blocks(path, subject=subject if subject in PP.MANGLED_PAPERS or subject in PP.GUTTER_MARKERS else None):
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


# Stimulus prose from the last census_sections() walk of each sitting, for
# authoring passes that need it. Written as a side table rather than returned,
# so census_subject()'s contract with every other reader is unchanged.
SECTION_STEMS = {}


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
        # A booklet boundary closes whatever question was open. The sitting's
        # SECTIONS run on across the two booklets, but a question does not:
        # the last question of Technology's Section A booklet was absorbing
        # the cover of the Section B and C booklet -- "Coimisiun na Scruduithe
        # Stait ... 136 marks Instructions" -- through the continuation rule.
        blocks.append(FILE_BREAK)
        for block in PP._blocks(path, subject=subject if subject in PP.MANGLED_PAPERS or subject in PP.GUTTER_MARKERS else None):
            # The answerbook's own back matter -- its instructions, its ruled
            # pages, the image acknowledgements and the copyright notice --
            # follows the last question in the SAME booklet, and the walker
            # ran straight on into it: the last question of Technology's
            # Section A came out carrying two thousand characters of "Start
            # each question on a new page" and a list of image URLs. Skipped
            # per FILE, not for the sitting, because the next booklet's
            # questions come after it.
            if BACK_MATTER.match(block):
                break
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
                        # Technology heads Section C's options "Option 3 -
                        # Information and Communication Technology" and every
                        # long part "3(a)" with no dot, both glued onto the
                        # prose that follows. Without the split the whole of
                        # Section C — five 40-mark options per paper — is
                        # invisible, which is what its census showed.
                        if subject == 'technology':
                            # "Answer 1(c) or 1(d)" is the rubric that offers
                            # the alternatives, not a part head; splitting on
                            # it keyed a part (c) whose whole text was "or".
                            text = re.sub(r'Answer\s+\d{1,2}\([a-d]\)\s+(?:and|or)\s+'
                                          r'\d{1,2}\([a-d]\)', ' ', text)
                        # "2(c)" may END a piece: the roman split above cuts
                        # the block before " (i)", which leaves the letter
                        # marker as the last token of the piece before it, and
                        # a rule demanding whitespace after the marker never
                        # saw it. Eight lettered parts across three Higher
                        # papers were invisible -- and their romans filed
                        # themselves under the letter above.
                        for text in (re.split(r'\s(?=(?:Option\s+\d\b|\d{1,2}\([a-d]\)(?:\s|$)))', text)
                                     if subject == 'technology' else [text]):
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

    def _value(i):
        return int(blocks[i].strip().rstrip('.').replace('\u2212', '-'))

    # A lone number belongs to a RUN of them -- an answerbook's ruled lines, a
    # matching table's rows, a graph axis -- and a run steps by one, or repeats
    # (a page number printed above the head that shares its value). A lone
    # number whose lone neighbours are neither is not part of their run: 2022
    # Higher Technology sets the answer lines "1." and "2." for Question 4
    # immediately above the head "5.", and treating "5." as more scaffolding
    # lost Question 5 whole, its two parts filed under Question 4.
    scaffold = {i for i in lone
                if any(j in lone and abs(_value(i) - _value(j)) <= 1
                       for j in (i - 1, i + 1))}
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
        if text is FILE_BREAK:
            q, letter, roman = None, None, None
            continue
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
        # Technology: Section C's five options are headed "Option N - Name",
        # and every long part in Sections B and C is "N(a)" with no dot.
        if subject == 'technology':
            op = re.match(r'Option\s+(\d)\b', text)
            if op:
                q, letter, roman = int(op.group(1)), None, None
                continue
            nl = re.match(r'(\d{1,2})\(([a-d])\)\s*', text)
            if nl and section in ('B', 'C'):
                q, letter, roman = int(nl.group(1)), nl.group(2), None
                key = (section, q, letter, None)
                parts.setdefault(key, [])
                rest = text[nl.end():].strip()
                if rest:
                    parts[key].append(rest)
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
    # The stimulus prose printed above a question's parts, keyed the same way.
    # The census itself does not need it -- a leaf is counted, not shown -- but
    # an authoring pass does: "Explain the term UHD." is the whole of a leaf
    # whose subject is named only in the sentence above it.
    SECTION_STEMS[(subject, year, level)] = {
        k: PP.unligature(' '.join(' '.join(v).split()))
        for k, v in stems.items()}
    return set(parts), texts, P.files


def census_lang(subject, year, level):
    """French: the written booklet and the listening booklet, read together.

    THE DENOMINATOR IS THE PAPER, and in this subject the paper needs help
    saying which of its printed markers is a question. A reading comprehension
    sets its passage in NUMBERED PARAGRAPHS — "1. Billie vit en banlieue
    parisienne…" — at the same margin and in the same shape as "1. (a) Comment
    Billie décrit-elle sa ville…". No feature of the layout separates them.

    So the reading asks are the printed blocks that the scheme's own reprinted
    question locates (fr_paper.find, which is align.py's rule), and the census
    then checks the paper INDEPENDENTLY in two ways:

      * every reading comprehension's item tariffs must add up to the total
        that comprehension prints on its own head. If the paper printed an ask
        the scheme did not price, that sum would be short — and it is short in
        exactly five comprehensions, each of which fr_scheme.py pins on one
        named ask (see its _checksum);
      * every printed marker block the scheme did NOT claim is scanned, and one
        that reads like a question — it ends in a question mark, or cites the
        passage section the answer is in — is FLAGGED. A passage paragraph
        never does either.

    Section B and the listening booklet need no such help: both print their own
    heads, and both are read from the paper alone.
    """
    import re as _re
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fr_paper import FrPaper                              # noqa: E402
    from fr_scheme import FrScheme                            # noqa: E402

    P = FrPaper(year, level, subject)
    S = FrScheme(year, level, subject)
    texts = {}
    claimed = set()
    for ask in S.reading():
        hit = P.find(ask.rc, ask.item, None if ask.letter_to else ask.letter, ask.cue)
        if hit is None:
            continue
        text = hit[0]
        section = f'A{ask.rc}'
        if ask.letter_to:
            # One head, four printed answer lines: "1.(a - d)" prices a
            # matching task whose parts the paper prints as (a) to (d), each
            # with its own answer space, so each is a leaf.
            for letter in _letters(ask.letter, ask.letter_to):
                part = P.candidates(ask.rc, ask.item, letter)
                body = max((b.text for b in part), key=len, default='')
                texts[(section, ask.item, letter, None)] = f'{text} ({letter}) {body}'.strip()
                claimed.add((ask.rc, ask.item, letter))
        else:
            texts[(section, ask.item, ask.letter, None)] = text
            claimed.add((ask.rc, ask.item, ask.letter))

    for q, letter, text, _page in P.section_b_asks():
        texts[('B', q, letter, None)] = text

    aural = P.aural_asks()
    lettered = {(sec, item) for sec, item, letter, _t in aural if letter}
    for sec, item, letter, text in aural:
        if letter is None and (sec, item) in lettered:
            continue                     # a head whose lettered parts are the asks
        texts[(f'L{sec}', item, letter, None)] = text

    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S, claimed


def _letters(first, last):
    lo, hi = LETTERS.index(first), LETTERS.index(last)
    return list(LETTERS[lo:hi + 1])


LETTERS = 'abcdefgh'
# A printed block that reads like a question rather than a passage paragraph:
# it ends in a question mark, or it names the passage section the answer is in,
# which is what every French reading ask does and no paragraph of the passage
# ever does.
LOOKS_LIKE_ASK = re.compile(r'\?\s*$|\((?:Section|Roinn)\s*\d\)\s*$', re.I)


def lang_flags(P, S, claimed):
    """What the PAPER prints that the scheme never priced. See census_lang."""
    flags = []
    for block in P.blocks:
        key = (block.rc, block.item, block.letter)
        # Short AND question-shaped. A paragraph of the passage can end in a
        # rhetorical question — 2025 Higher's fifth runs to four hundred
        # characters and closes with one — and flagging it as a lost ask would
        # bury the real signal under one false alarm per paper.
        if (key in claimed or len(block.text) > 300
                or not LOOKS_LIKE_ASK.search(block.text)):
            continue
        flags.append({
            'type': 'unpriced-ask',
            'where': f'Q.{block.rc} {block.item}{f"({block.letter})" if block.letter else ""}',
            'detail': f'the paper prints {block.text[:70]!r}, which no scheme ask claims'})
    for ask in S.reading():
        if ask.fault:
            flags.append({'type': 'tariff-disagreement',
                          'where': S.ref(ask), 'detail': ask.fault})
    return flags


def lang_cover_marks(paths):
    """The totals the two booklets print on their own covers, added.

    French has no per-question tariff on the paper at all — the marks live in
    the scheme — so there is nothing to sum question by question. The covers
    state what the sitting is worth, and a year that disagrees with its
    siblings has lost a booklet.
    """
    import pymupdf
    total = 0
    for path in paths:
        with pymupdf.open(path) as doc:
            m = re.search(r'(\d{2,3})\s*marks\b', doc[0].get_text(), re.I)
        if m:
            total += int(m.group(1))
    return total


def census_re(subject, year, level):
    """Religious Education: its own reader, for the reasons re_paper.py gives.

    The generic sections walker cannot see this paper. It requires a question
    head before it will key a part, and eight of the ten sections here print
    none — Section B opens straight into "(a)". Reading this sitting with it
    censuses Section A alone and calls the other 80% of the paper absent.
    """
    from re_paper import RePaper                             # noqa: E402
    P = RePaper(year, level)
    texts = {k: v for k, v in P.asks.items()}
    return set(texts), texts, [P.path]


def census_history(subject, year, level, field):
    """History: its own reader, for the reasons hist_paper.py gives.

    Two things the generic sections walker cannot do here. It reads ONE paper
    per sitting, and History sets two — the Later Modern and Early Modern
    fields of study. And it keys an ask by (section, question), where a History
    ask is addressed by section, TOPIC, Ordinary part and question, because
    every topic on the paper restarts at 1.
    """
    from hist_paper import HistPaper                         # noqa: E402
    P = HistPaper(year, level, field)
    return set(P.asks), dict(P.asks), [P.path], dict(P.marks), P.cover_marks


def re_cover_marks(path):
    """The total the paper prints on its own cover.

    Religious Education has no per-question checksum to sum: a candidate
    answers four of the ten sections, so adding up every printed tariff counts
    questions nobody sits. The cover states the total outright.
    """
    import pymupdf
    with pymupdf.open(path) as doc:
        m = re.search(r'Total Marks\s+(\d+)', doc[0].get_text())
    return int(m.group(1)) if m else None
# ---------------------------------------------------------------- LCVP ----
# LCVP prints every question head as "Q.1", never "1." or "Question 1", and
# glues it onto whatever precedes it: "PART 2 Q.4 ...", "Answer all three
# questions. Q.1 ...", and two questions in one block ("... (2 marks) Q.3 ...").
LCVP_HEAD = re.compile(r'Q\.\s*(\d{1,2})\b')
LCVP_SPLIT = re.compile(r'\s*(?=Q\.\s*\d{1,2}\b)')
# Section C reprints every question as a contents listing — "Q.4 Pages 27 to
# 29 Ireland has embraced diversity ... (a) ... (b) ..." — before setting the
# questions themselves. Read as questions those rows would walk the counter to
# Q.7 and every real question after them would be rejected as going backwards,
# which is exactly how Business lost four sittings' Section 1. The listing rows
# are the ones that carry their page range, and no real head does.
LCVP_INDEX = re.compile(r'\bPages\s+\d+\s+to\s+\d+', re.I)
# A section header the SEC sets over the section itself always prices it
# ("Section A Audio Visual 30 marks"). The cover page's examiner mark table
# and the instructions page name the same sections WITHOUT their marks, and
# the cover table also prints bare "Q.1".."Q.6" cells, which walked the
# counter to 6 before the paper began and threw all of Section A away.
LCVP_SECTION = re.compile(r'^Section\s+([A-C])\b(.{0,200})', re.S)
LCVP_MARKS = re.compile(r'\(?\s*(\d{1,3})\s*marks?\b\s*\)?', re.I)
LCVP_FURNITURE = re.compile(
    r'^(?:Leaving Certificate Vocational Programme'
    r'|Examiner only'
    r'|page running'
    r'|Do not write on this page'
    r'|You may use this page for extra work'
    r'|Make sure to label extra work'
    r'|Copyright notice'
    r'|Answer all (?:eight|three) questions'
    r'|Answer your chosen questions'
    r'|Answer any four questions'
    r'|This section has (?:six|seven) questions'
    r'|To help you decide'
    # "PART 2" / "Part 3" head the three showings of the Section A DVD; they
    # are not asks and, left in, they land in the previous question's text.
    r'|(?:PART|Part)\s+\d\s*$)', re.I)


def census_lcvp(subject, year, level):
    """LCVP's own section walker. See LCVP_HEAD/LCVP_INDEX above for why."""
    root = PP.papers_dir(subject)
    files = sorted(os.path.join(root, f) for f in os.listdir(root)
                   if re.fullmatch(rf'{year}-{level}-paper\.pdf', f))
    if not files:
        raise FileNotFoundError(f'no {year} {level} paper for {subject}')

    chunks = [c.strip() for path in files for block in PP._blocks(path)
              for c in LCVP_SPLIT.split(block) if c.strip()]

    parts, stems, marks = {}, {}, {}
    section = q = letter = roman = None
    started = False          # nothing counts before the first priced section
    index = False            # inside Section C's contents listing
    if True:
        if True:
            for position, chunk in enumerate(chunks):
                sh = LCVP_SECTION.match(chunk)
                if sh and 'Section' not in sh.group(2) \
                        and LCVP_MARKS.search(sh.group(2)):
                    # 2021 and 2022 head their Section B/C pages "Section B –
                    # Case Study and Section C – General Questions 100 marks",
                    # a cover line for both; the second "Section" rejects it.
                    if section is None or sh.group(1) >= section:
                        section, q, letter, roman = sh.group(1), None, None, None
                        started, index = True, False
                    continue
                if not started:
                    continue
                head = LCVP_HEAD.match(chunk)
                if head:
                    index = bool(LCVP_INDEX.search(chunk))
                    if index:
                        continue
                    found = int(head.group(1))
                    if q is not None and found <= q:
                        continue          # a repeat, not a new question
                    q, letter, roman = found, None, None
                    rest = chunk[head.end():].strip()
                    # The question's own tariff, wherever the SEC set it: after
                    # the ask in Sections A and B ("Q.1 Name the manager of the
                    # charity shop. (1 mark)") and before it in Section C
                    # ("Q.1 25 marks Marketing is an essential part of
                    # business."). Leftmost wins, so a part's own marks further
                    # down the same block never displace the question's.
                    m = LCVP_MARKS.search(rest)
                    if m:
                        marks[(section, q)] = int(m.group(1))
                        if m.start() == 0:
                            rest = rest[m.end():].strip()
                    chunk = rest
                    if not chunk:
                        continue
                if index or q is None:
                    continue
                for piece in PP.INLINE_MARKER.split(chunk):
                    piece = piece.strip()
                    if not piece or LCVP_FURNITURE.match(piece):
                        continue
                    # Sections A and B price the QUESTION and nothing under
                    # it, so a tariff found anywhere inside one is that
                    # question's — 2025 sets Q.6's "(6 marks)" on the line
                    # after its (ii). Section C prices every part, so a token
                    # found below its head would be a part's and is not taken.
                    if section in ('A', 'B') and (section, q) not in marks:
                        m = LCVP_MARKS.search(piece)
                        if m:
                            marks[(section, q)] = int(m.group(1))
                    fl, fr, rest = PP._leading(piece)
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
                    # 2023 sets the case study's title, "Ballyfert", ABOVE
                    # its own "Section B Case Study" header, so top-to-bottom
                    # order hands it to Section A's last question and it
                    # shipped inside that leaf's text. A short, unpunctuated
                    # line immediately before a section header belongs to the
                    # section it names, not to the question it follows.
                    if len(piece) < 40 and not re.search(r'[.?!:]$', piece) \
                            and position + 1 < len(chunks) \
                            and LCVP_SECTION.match(chunks[position + 1]):
                        continue
                    stems.setdefault((section, q, letter), []).append(piece)

    parts = {k: v for k, v in parts.items() if any(x.strip() for x in v)}
    for (section_, q_, letter_), lines in list(stems.items()):
        if letter_ is not None or not lines:
            continue
        if any(k[0] == section_ and k[1] == q_ for k in parts):
            continue
        parts[(section_, q_, None, None)] = list(lines)
    texts = {k: PP.unligature(' '.join(' '.join(v).split()))
             for k, v in parts.items()}
    stems = {k: PP.unligature(' '.join(' '.join(v).split()))
             for k, v in stems.items()}
    return set(parts), texts, files, marks, stems


def census_subject(subject):
    cfg = SUBJECTS.get(subject, {'mode': 'merged'})
    if cfg['mode'] == 'geography':
        path = os.path.join(
            ROOT, 'scripts', 'markbank', 'authored', 'geography-census.json')
        payload = json.load(open(path, encoding='utf-8'))
        tasks = payload['baseTasks']
        if payload.get('paperBaseTasks') != len(tasks):
            raise AssertionError('Geography authored census total is stale')
        papers = []
        for sitting in payload['sittings']:
            asks = [task for task in tasks
                    if task['year'] == sitting['year']
                    and task['level'] == sitting['level']]
            if sitting.get('paperBaseTasks') != len(asks):
                raise AssertionError(
                    f"Geography {sitting['year']} {sitting['level']} "
                    'census count is stale')
            papers.append({
                'year': sitting['year'], 'level': sitting['level'],
                'paper': None, 'leafCount': len(asks),
                'leaves': [{
                    'key': [ask['id']], 'label': ask['questionRef'],
                    'text': ask['title'], 'status': ask['status'],
                } for ask in asks],
                'marksSum': None, 'marksQuestions': 0, 'flags': [],
            })
        return {'subject': subject, 'mode': cfg['mode'], 'papers': papers}
    if cfg['mode'] == 'art':
        path = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'art-census.json')
        payload = json.load(open(path, encoding='utf-8'))
        papers = []
        for source in payload['papers']:
            cards = source['cards']
            if source.get('expectedCards') != len(cards):
                raise AssertionError(
                    f"Art {source['year']} {source['level']} census count is stale")
            papers.append({
                'year': source['year'], 'level': source['level'],
                'paper': None, 'leafCount': len(cards),
                'leaves': [{
                    'key': [card['cardId']], 'label': card['questionRef'],
                    'text': '', 'status': 'authored',
                } for card in cards],
                'marksSum': None, 'marksQuestions': 0, 'flags': [],
            })
        total = sum(p['leafCount'] for p in papers)
        if payload.get('expectedCards', {}).get('total') != total:
            raise AssertionError('Art authored census total is stale')
        return {'subject': subject, 'mode': cfg['mode'], 'papers': papers}
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
        elif cfg.get('components'):
            # A subject whose sitting is two SEPARATE papers a candidate
            # chooses between, rather than two booklets of one paper. Each is
            # censused whole and named in the citation.
            units = sorted((cfg['components'][c], c) for c in comps if c)
            missing = sorted(set(cfg['components']) - {c for c in comps if c})
            if missing:
                raise AssertionError(
                    f'{subject} {year} {level}: no paper on disk for '
                    f'{", ".join(cfg["components"][m] for m in missing)}')
        else:
            units = [(None, None)]
        for label, comp in units:
            marks = None
            cover = None
            try:
                if cfg.get('walker') == 'history':
                    parts, texts, files, marks, cover = census_history(
                        subject, year, level, comp)
                if cfg.get('walker') == 'lang':
                    parts, texts, files, P_, S_, claimed_ = census_lang(
                        subject, year, level)
                elif cfg.get('walker') == 're':
                    parts, texts, files = census_re(subject, year, level)
                elif cfg.get('walker') == 'lcvp':
                    parts, texts, files, marks, _stems = census_lcvp(
                        subject, year, level)
                elif cfg['mode'] == 'sections':
                    parts, texts, files = census_sections(subject, year, level)
                else:
                    parts, texts, files = census_merged(subject, year, level, comp)
            except Exception as e:                       # noqa: BLE001
                papers.append({'year': year, 'level': level, 'paper': label,
                               'error': f'{type(e).__name__}: {e}'})
                continue
            leaves = leaves_of(parts)
            flags = continuity_flags(parts, texts)
            if cfg.get('walker') == 'history':
                # A History paper is almost entirely CHOICE: eleven topics are
                # printed and a candidate answers two. Adding up every printed
                # tariff would count questions nobody sits, so the checksum is
                # the total the paper states on its own cover.
                marks = {(None, 0): cover} if cover else {}
            if cfg.get('walker') == 'lang':
                flags += lang_flags(P_, S_, claimed_)
                marks = {(None, 0): lang_cover_marks(files)}
            elif cfg.get('walker') == 're':
                total = re_cover_marks(files[0])
                marks = {(None, 0): total} if total else {}
            elif marks is None:
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
