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
import unicodedata

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
    # One booklet per sitting, questions 1..10 running on, both sides of the
    # 2023 syllabus break. The old papers set 'Question 1' as a bare '1.' in a
    # left gutter and the new ones head it 'Question 1' in the answer booklet;
    # both are QHEAD's own two spellings, so the generic merged walker reads
    # them once the subset fonts are repaired (see MANGLED_PAPERS).
    'applied-maths': {'mode': 'merged'},
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
    # German sits the same two booklets as French and numbers both from 1
    # inside every section, so the section carries the address — but its
    # sections are the paper's own TEXTS rather than a lettered Section A:
    # "T1" is TEXT I's reading comprehension, "AG" the applied grammar, "AT"
    # the Äußerung zum Thema, "SP" the Schriftliche Produktion and "L1" the
    # first part of the Listening Comprehension Test. Its own walker, because
    # both booklets are printed bilingually in columns AND a German ask is
    # addressed three levels deep, "2.(b)(ii)", which the French walker's
    # (question, letter) key cannot hold.
    'german': {'mode': 'sections', 'walker': 'de'},
    # Spanish sits THREE documents at one sitting: the written paper, a
    # separate Listening Comprehension Test with its own SEC file id, and — at
    # Higher — a two-page LOOSE SHEET carrying the Section B article, which is
    # the text every Section B question is about and which the question paper
    # does not contain. Its own walker, because its section tokens carry a
    # CHOICE the paper's numbering cannot: Higher Section A prints Question 1
    # twice over, once as prescribed literature and once as a journalistic
    # text, and each alternative numbers its own questions from 1. "A1a" is the
    # literature route, "A1b" the journalistic one, "A2" the section's second
    # question, and "L" the listening test.
    'spanish': {'mode': 'sections', 'walker': 'es'},
    # Italian sits the same two booklets as French and the same three sections
    # in the written one, but nothing else about it is French: its Higher paper
    # is set in ITALIAN rather than bilingually, its scheme never reprints the
    # question it is answering, and its Section B is a printed choice of three
    # routes at Higher and five publicity pieces at Ordinary. So it has its own
    # walker, keyed on the section token the paper itself prints — "B2A" is
    # the first of the two prescribed novels, "LB3" the listening test's third
    # dialogue — and its own join: with no reprinted question there is nothing
    # to score wording against, so the scheme is paired to the paper by ORDER
    # inside a section, under the two checks that make order safe (see
    # census_it).
    'italian': {'mode': 'sections', 'walker': 'italian'},
    # Russian sits the same two booklets as French — a bilingual written paper
    # and a separate Listening Comprehension Test — and its section token
    # names the printed QUESTION rather than a letter, because the paper
    # numbers "Question 1" three times in one sitting: once in Section I, once
    # in Section II and once in the listening booklet. "C1" is Higher's first
    # comprehension, "GR" the grammar, "MM" Ordinary's mix-and-match and "L2"
    # the listening test's second section; see UNIT_NAME in ru_scheme.py. Its
    # own walker, because the reading asks are located the way French's are —
    # by the question the scheme reprints above its answers (Law 4) — while
    # every other question of the paper is read from the paper alone.
    'russian': {'mode': 'sections', 'walker': 'ru'},
    # Japanese sits the same two booklets as French — the written paper (SEC
    # component 000) and a Listening Comprehension Test (A00) — and heads the
    # written one in Japanese: 問題1 … 問題5, the first three reading
    # comprehension and the last two written production. Inside a question the
    # SEC heads its parts "Cuid A / Part A" or with a bare letter at the
    # margin ("B: KANJI", "C: GRAMADACH / GRAMMAR"), and each part numbers its
    # own items from 1 — or prints bare romans with no number above them.
    #
    # So the section token carries the question AND the part: "2B" is 問題2's
    # kanji section, "3D" its grammar section, "4" the composition, which heads
    # no parts, and "LC" the listening booklet's Part C. A citation reads
    # "2024 HL Section 2B Q1(i)".
    #
    # Its own walker for two reasons no other language has. The pages carry a
    # SECOND LAYER OF TYPE — furigana, a kana reading set small above the kanji
    # it glosses — which the generic reader interleaves into the line below it
    # and destroys (ja_text.py folds it back in brackets). And the scheme's own
    # part letters disagree with the paper's: 2024 Ordinary heads question 2's
    # four parts "A.", "B.", "Part B." and "Part C." where the paper heads them
    # "A.", "B.", "C. KANJI" and "D.", so the two are paired in printed ORDER
    # under the checks in ja_flags — Law 4.
    'japanese': {'mode': 'sections', 'walker': 'ja'},
    # Classical Studies is TWO papers under one slug, either side of the 2023
    # syllabus break, and the census reads both:
    #
    #   * 2021-2022 print TEN TOPICS, each setting questions "(i)" to "(iv)"
    #     with lettered parts under them. The topic and the roman TOGETHER are
    #     the address — there is no question number at all — so the section
    #     token carries both and an ask is cited "2021 HL Topic 1(i) Q(a)".
    #   * 2023-2025 print Section A (Questions 1-10) and Section B (Questions
    #     11-16) with the numbering running ON across the two, so the section
    #     is NOT part of the address and the section token is None: an ask is
    #     cited "2024 HL Q3(b)". Keying those under 'A' and 'B' would have
    #     made Section B look like a paper whose first question is Q11.
    #
    # Its own walker, because neither shape is one the generic reader can key:
    # the old paper glues a whole topic into ONE pymupdf block, and the new one
    # prices the question while the scheme prices its parts.
    'classical-studies': {'mode': 'sections', 'walker': 'clas'},
    # Polish is a NON-CURRICULAR EU language (SEC subject 548) and its shape is
    # its own. It is sat at ONE level up to 2021 — the SEC's file letter is 'A'
    # and its cover says "Higher Level", so it is Higher-only, not LCVP's
    # common 'C' — and at TWO from 2022, when the examination was rebuilt: a
    # written booklet holding Section A Reading and Section B Written
    # Production, plus a Listening Comprehension Test in its own booklet
    # (component A00) that did not exist before.
    #
    # The section token is the paper's own: 'A' and 'B' for the two sections
    # the written booklet tabs in its margin, 'LA' to 'LE' for the listening
    # booklet's five parts, and 'I' and 'II' for the two parts of the 2021
    # examination, which numbers questions the later papers letter. A citation
    # reads "2024 HL Section A Q1(b)(ii)" or "2021 HL Section I Q1(a)".
    #
    # Its own walker, for a reason none of the six carded languages has: the
    # SEC prints Polish in SEPARATE English and Irish editions rather than one
    # bilingual booklet, so there are no columns to cut apart — and the one
    # marker that is genuinely ambiguous, "(i)", is settled on the printed
    # column plus the letter sequence rather than on wording (see pl_paper).
    'polish': {'mode': 'sections', 'walker': 'pl'},
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
# Through xv, because a list can run that long: the Japanese kanji sections at
# Ordinary print thirteen items and answer any ten, and a list that stopped at
# xii reported a gap in a run that has none.
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii', 'xiii', 'xiv', 'xv']


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
    # Sorted by the STRING of the prefix: one paper may key some of its asks
    # under a section token and some under none, which is what Polish does —
    # its written booklet numbers straight through its two sections while its
    # listening booklet restarts inside each of its five — and sorting None
    # beside 'LA' raises before a single flag is computed.
    prefixes = sorted({k[:-3] for k in keys},
                      key=lambda pre: tuple(str(x) for x in pre))
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
        #
        # Unless the numbering RUNS ON: Polish tabs Questions 1 and 2 "Część A"
        # and Questions 3 to 5 "Część B" in one booklet, so Section B's first
        # question is Q3 and nothing at all is missing. The exemption is
        # evidence, not a guess — every question below this one has to be
        # printed under some OTHER prefix of the same paper, which a genuinely
        # lost leading question never is.
        elsewhere = {k[-3] for k in keys if k[:-3] != pre
                     and isinstance(k[-3], int)}
        runs_on = qs and isinstance(qs[0], int) and qs[0] > 1 and all(
            n in elsewhere for n in range(1, qs[0]))
        if qs and isinstance(qs[0], int) and qs[0] > 1 and not runs_on:
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
        # A CJK character is worth six Latin ones here, which is the whole floor:
        # ONE kanji is a whole ask in the Japanese kanji sections — "Write the
        # meaning of 今" — and counting characters flagged seventy of them empty.
        weight = sum(6 if '\u3040' <= c <= '\u9fff' else 1
                     for c in text if c.isalnum())
        if weight < 6 and len(text) < 16:
            flags.append({'type': 'empty-leaf', 'where': key_label(k),
                          'detail': f'extracted text: {text!r}'})
    return flags


def key_label(k):
    """(section?, q, letter, roman) -> 'Section A Q3(b)(ii)'."""
    parts = list(k)
    q, letter, roman = parts[-3], parts[-2], parts[-1]
    # A section token of None means the subject is keyed in sections mode but
    # this paper does not address an ask by section: Classical Studies numbers
    # Questions 1-16 straight through Sections A and B, so "Section A Q3" would
    # name an address the paper never prints. A token that already names its
    # own unit — "Topic 1(i)" — prints itself, without a "Section" in front.
    head = ''
    if len(parts) == 4 and parts[0] is not None:
        head = (f'{parts[0]} ' if str(parts[0]).startswith('Topic ')
                else f'Section {parts[0]} ')
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


def census_ja(subject, year, level):
    """Japanese: the written booklet and the listening booklet, read together.

    THE DENOMINATOR IS THE PAPER, and here it can be read from the paper
    alone: every ask the SEC sets is opened by a printed marker under a printed
    part head, and ja_paper.py walks them. The scheme is read beside it — not
    to say which asks exist, but to price them and to be CHECKED against them,
    which is what ja_flags does.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ja_paper import JaPaper                                # noqa: E402
    from ja_scheme import JaScheme                              # noqa: E402

    P = JaPaper(year, level, subject)
    S = JaScheme(year, level, subject)
    texts = {}
    for ask in P.all_asks():
        texts[ask.key] = ask.text
    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S


def ja_flags(P, S):
    """What the paper and the scheme disagree about. See census_ja.

    Three checks, and they are the only reason pairing the two documents by
    printed ORDER is safe (Law 4):

      * each component sets the same NUMBER of parts in both documents;
      * paired part for paired part, both hold the same number of asks;
      * every question's scheme tariffs add up to the total the PAPER prints
        on its own 問題 head.

    A part that fails any of them is flagged, never quietly re-keyed — the
    asks under it stay open in the ledger until the disagreement is settled.
    """
    flags = []
    paper = collections.OrderedDict()
    for ask in P.asks():
        paper.setdefault(ask.section, []).append(ask)
    aural = collections.OrderedDict()
    for ask in P.aural_asks():
        aural.setdefault(ask.section, []).append(ask)
    scheme = S.by_part()
    groups = [
        ('reading', [k for k in paper if k[0] in '123'],
         [k for k in scheme if k[0] == 'R']),
        ('written production', [k for k in paper if k[0] in '45'],
         [k for k in scheme if k[0] == 'W']),
        ('listening', list(aural), [k for k in scheme if k[0] == 'L']),
    ]
    for name, pkeys, skeys in groups:
        if len(pkeys) != len(skeys):
            flags.append({
                'type': 'scheme-parts',
                'where': name,
                'detail': f'the paper heads {len(pkeys)} part(s) '
                          f'({", ".join(map(str, pkeys))}) and the scheme '
                          f'{len(skeys)}; they cannot be paired in order'})
            continue
        for pk, sk in zip(pkeys, skeys):
            pn = len(paper.get(pk) or aural.get(pk) or [])
            sn = len(scheme[sk])
            if pn != sn:
                flags.append({
                    'type': 'scheme-count',
                    'where': f'Section {pk}',
                    'detail': f'the paper prints {pn} ask(s) here and the '
                              f'scheme prices {sn}'})
    # The tariff checksum is read off the PART HEADS, not off the leaves.
    # Almost every part of this paper is a CHOICE — "Write the meaning of any
    # FIVE of the following Kanji", six items printed and five answered — so
    # the leaves under a part are worth MORE than the part is, by design, and
    # adding them up flags thirty-four questions that are priced correctly.
    # A part head states what the part is worth whatever the candidate picks.
    for q, printed in sorted(P.question_marks.items()):
        parts = [k for k in S.by_part() if k[0] in ('R', 'W') and k[1] == q]
        heads = [S.part_marks.get(k) for k in parts]
        if not parts or any(h is None for h in heads):
            continue
        if sum(heads) != printed:
            flags.append({
                'type': 'tariff-checksum',
                'where': f'Q{q}',
                'detail': f'the scheme heads this question\'s parts '
                          f'{sum(heads)} against the {printed} the paper '
                          f'prints on its own head'})
    return flags


def census_de(subject, year, level):
    """German: the written booklet and the listening booklet, read together.

    THE DENOMINATOR IS THE PAPER. The reading asks are the printed blocks the
    scheme's own reprinted question locates (de_paper.find, which is align.py's
    rule), and the twenty asks whose scheme prints an answer KEY rather than a
    question — the Ordinary paragraph-headings, matching and true/false
    questions — are located by their printed address, which is the only thing
    both documents state about them.

    Everything else is read from the paper alone and needs no help: the applied
    grammar prints "1." and "2." and a candidate answers one; Äußerung zum
    Thema and Schriftliche Produktion print "(a)" and "(b)" the same way; and
    the listening booklet numbers its own four parts.

    The census then checks the paper INDEPENDENTLY in three ways, in
    `de_flags`: every scheme ask must have found a printed block, every printed
    reading block must have been claimed by a scheme ask, and the item counts
    of the listening booklet must equal the splits the scheme prints on the
    heads of its own four parts.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from de_paper import DePaper                               # noqa: E402
    from de_scheme import DeScheme                             # noqa: E402

    P = DePaper(year, level, subject)
    S = DeScheme(year, level, subject)
    texts = {}
    claimed = set()
    for ask in S.reading():
        hit = P.find(ask.unit, ask.q, ask.letter, ask.roman, ask.cue)
        if hit is None:
            hit = P.by_key(ask.unit, ask.q, ask.letter, ask.roman)
        if hit is None:
            continue
        texts[ask.key] = hit[0]
        claimed.add(ask.key)
    for q, text, _page in P.grammar_alternatives():
        texts[('AG', q, None, None)] = text
    for unit in ('AT', 'SP'):
        for letter, text, _page in P.written_alternatives(unit):
            texts[(unit, None, letter, None)] = text
    for part, item, roman, text in P.aural_asks():
        texts[(f'L{part}', item, None, roman)] = text
    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S, claimed


# A printed block that reads like a question rather than a stray fragment: it
# ends in a question mark, or it names the place in the text its answer is
# found, which is what every German reading ask does.
LOOKS_LIKE_ASK_DE = re.compile(
    r'\?\s*$|\((?:Zeile[n]?|line|lines|Par\.|Absatz|Abschnitt|Alt|Introduction|'
    r'Einleitung|R[ée]amhr[áa]|Headline|Tipp)[^)]*\)\s*$', re.I)


def de_flags(P, S, claimed):
    """What the two documents disagree about. See census_de."""
    flags = []
    for ask in S.reading():
        if ask.key not in claimed:
            flags.append({
                'type': 'unpaired-ask', 'where': S.ref(ask),
                'detail': f'the scheme prices this ask and no printed block on '
                          f'the paper matches its wording: "{ask.cue[:70]}"'})
    for block in P.blocks:
        if block.key in claimed or len(block.text) > 400:
            continue
        if not LOOKS_LIKE_ASK_DE.search(block.text):
            continue
        flags.append({
            'type': 'unpriced-ask',
            'where': f'Section {block.key[0]} Q{block.q}'
                     f'{f"({block.letter})" if block.letter else ""}'
                     f'{f"({block.roman})" if block.roman else ""}',
            'detail': f'the paper prints {block.text[:70]!r}, which no scheme '
                      f'ask claims'})
    items = collections.defaultdict(set)
    for part, item, _roman, _text in P.aural_asks():
        items[part].add(item)
    for part in sorted(set(items) | {int(u[1]) for u in S.unit_splits
                                     if u.startswith('L')}):
        printed = S.unit_splits.get(f'L{part}')
        if printed is None:
            flags.append({
                'type': 'listening-head', 'where': f'Listening part {part}',
                'detail': 'the scheme prints no tariff on this part\'s own head, '
                          'so its item count cannot be checked against the paper'})
        elif len(printed) != len(items.get(part, ())):
            flags.append({
                'type': 'listening-count', 'where': f'Listening part {part}',
                'detail': f'the paper prints {len(items.get(part, ()))} items and '
                          f'the scheme prices {len(printed)}'})
    return flags

def census_es(subject, year, level):
    """Spanish: the written paper, the loose sheet and the listening booklet.

    THE DENOMINATOR IS THE PAPER. Every leaf here is a marker the paper itself
    prints with an ask beside it, read by es_paper.py; the scheme is consulted
    only to CHECK the reading, never to produce it.

    Two things this paper does that a generic reader cannot see:

      * Higher Section A's journalistic text is printed in NUMBERED PARAGRAPHS
        at the same margin and in the same shape as its questions, so "1." on
        the page is as likely to open the article as the ask. The questions are
        the last run of markers in the region (es_paper.Region.ask_blocks);
      * a "Give three details" ask is followed by "1.", "2." and "3." printed
        alone on the answer lines. A marker with nothing after it is an answer
        box, and is not counted.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from es_paper import EsPaper                              # noqa: E402
    from es_scheme import EsScheme                            # noqa: E402

    P = EsPaper(year, level, subject)
    S = EsScheme(year, level, subject)
    texts = {k: v[0] for k, v in P.leaves().items()}
    for q, letter, text, _page in P.aural_asks():
        texts[('L', q, letter, None)] = text
    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S


def es_flags(P, S):
    """What the PAPER prints that the scheme does not agree with.

    Three independent checks, because the two documents share three things and
    a mis-read shows up in a different one of them each time:

      * the SECTION total, printed on the paper's own section head and again on
        the scheme's;
      * the QUESTION tariff, printed beside the question on the paper and on
        the scheme's question head;
      * the text's own TITLE, printed above the article on the paper and above
        its answers in the scheme.

    Plus the fourth thing that is not an agreement at all: a leaf the paper
    prints that no scheme ask claims and no band grid covers.
    """
    flags = []
    for letter, printed in sorted(P.section_marks.items()):
        want = S.unit_totals.get(letter)
        if want is not None and want != printed:
            flags.append({
                'type': 'section-total', 'where': f'Section {letter}',
                'detail': f'the paper prints {printed} marks, the scheme {want}'})
    for token, region in sorted(P.regions.items()):
        for item, stem in sorted(region.stems().items()):
            key = _es_scheme_key(token, item)
            want = S.q_totals.get(key)
            got = stem.marks
            if want is not None and got is not None and want != got:
                flags.append({
                    'type': 'tariff-disagreement', 'where': f'{token} Q{item}',
                    'detail': f'the paper prices this question {got}, '
                              f'the scheme {want}'})
        # Section B's text is not in the question paper, so its title is the
        # one printed on the loose sheet.
        title = ((region.title or P.insert_title) if token == 'B'
                 else region.title)
        want_title = S.titles.get(_es_title_key(token))
        if title and want_title and not _title_agrees(title, want_title):
            flags.append({
                'type': 'title-disagreement', 'where': token,
                'detail': f'the paper heads this text {title!r}, '
                          f'the scheme {want_title!r}'})
    priced = {a.key for a in S.asks}
    grid_cover = set()
    for (sec, q, letter, _roman) in S.grids:
        grid_cover.add((sec, q, letter))
    for key in sorted(P.leaves(), key=lambda k: tuple(str(x) for x in k)):
        section, q, letter, roman = key
        if (section, q, letter, roman) in priced:
            continue
        # A scheme ask priced WHOLE covers every part the paper prints beneath
        # it: Higher Section A's Q.4 journalistic ask is one 6-mark question
        # whose two phrases the paper prints as (a) and (b).
        if (section, q, None, None) in priced or (section, None, letter, None) in priced:
            continue
        if (section, q, letter) in grid_cover or (section, q, None) in grid_cover:
            continue
        flags.append({
            'type': 'unpriced-ask', 'where': key_label(key),
            'detail': 'the paper prints this ask and no scheme entry claims it'})
    return flags


def census_it(subject, year, level):
    """Italian: the written booklet and the listening booklet, read together.

    THE DENOMINATOR IS THE PAPER, and this paper says which of its printed
    markers is a question without any help from the scheme: a passage, an
    advertisement or a literary extract is printed on a page with nothing to
    write on, and the questions on the page after it with ruled lines under
    them. So the reading asks are read from the paper alone (it_paper.py),
    which is what French could not do.

    What the paper cannot do alone is say whether the reader lost one, and the
    scheme is the independent check for that — TWICE:

      * every reading section prints what it is worth on its own head, and the
        tariffs of the asks beneath it add up to that figure in all ten
        sittings, in every section (it_scheme.audit);
      * the number of asks the scheme prices in a section equals the number the
        paper prints in it, in all ten sittings and all 385 asks.

    Where the two disagree about an ask's NAME they are flagged and the paper
    wins: the SEC leaves the "(a)" off the first part of an item four times in
    the corpus — 2024 Ordinary prices "2." where the paper prints "2. (a)" —
    and the paper is what a student is holding.

    The marks checksum flags 2021 and 2022 at both levels, and that is the
    paper changing rather than the reader losing anything. Those two sittings
    print "Freagair Roinn A nó Roinn B / Answer either Section A or Section B"
    at Higher and set ONE of two reading comprehensions at Ordinary, and their
    written booklets say so on their own covers: 160 marks at Higher and 180 at
    Ordinary, against 220 for each of 2023, 2024 and 2025. Every ask printed in
    the section a candidate did not answer is still an ask the paper printed,
    so all of them are censused.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from it_paper import ItPaper                              # noqa: E402
    from it_scheme import ItScheme                            # noqa: E402

    P = ItPaper(year, level, subject)
    S = ItScheme(year, level, subject)
    texts = {}
    for section, item, letter, text, _page in P.asks():
        texts[(section, item, letter, None)] = text
    for route, item, text, _page in P.essay_asks():
        texts[(f'B3{route}', item, None, None)] = text
    for item, letter, text, _page in P.writing_asks():
        texts[('C', item, letter, None)] = text
    for section, item, text in P.aural_asks():
        texts[(f'L{section}', item, None, None)] = text
    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S


def es_flags(P, S):
    """What the PAPER prints that the scheme does not agree with.

    Three independent checks, because the two documents share three things and
    a mis-read shows up in a different one of them each time:

      * the SECTION total, printed on the paper's own section head and again on
        the scheme's;
      * the QUESTION tariff, printed beside the question on the paper and on
        the scheme's question head;
      * the text's own TITLE, printed above the article on the paper and above
        its answers in the scheme.

    Plus the fourth thing that is not an agreement at all: a leaf the paper
    prints that no scheme ask claims and no band grid covers.
    """
    flags = []
    for letter, printed in sorted(P.section_marks.items()):
        want = S.unit_totals.get(letter)
        if want is not None and want != printed:
            flags.append({
                'type': 'section-total', 'where': f'Section {letter}',
                'detail': f'the paper prints {printed} marks, the scheme {want}'})
    for token, region in sorted(P.regions.items()):
        for item, stem in sorted(region.stems().items()):
            key = _es_scheme_key(token, item)
            want = S.q_totals.get(key)
            got = stem.marks
            if want is not None and got is not None and want != got:
                flags.append({
                    'type': 'tariff-disagreement', 'where': f'{token} Q{item}',
                    'detail': f'the paper prices this question {got}, '
                              f'the scheme {want}'})
        # Section B's text is not in the question paper, so its title is the
        # one printed on the loose sheet.
        title = ((region.title or P.insert_title) if token == 'B'
                 else region.title)
        want_title = S.titles.get(_es_title_key(token))
        if title and want_title and not _title_agrees(title, want_title):
            flags.append({
                'type': 'title-disagreement', 'where': token,
                'detail': f'the paper heads this text {title!r}, '
                          f'the scheme {want_title!r}'})
    priced = {a.key for a in S.asks}
    grid_cover = set()
    for (sec, q, letter, _roman) in S.grids:
        grid_cover.add((sec, q, letter))
    for key in sorted(P.leaves(), key=lambda k: tuple(str(x) for x in k)):
        section, q, letter, roman = key
        if (section, q, letter, roman) in priced:
            continue
        # A scheme ask priced WHOLE covers every part the paper prints beneath
        # it: Higher Section A's Q.4 journalistic ask is one 6-mark question
        # whose two phrases the paper prints as (a) and (b).
        if (section, q, None, None) in priced or (section, None, letter, None) in priced:
            continue
        if (section, q, letter) in grid_cover or (section, q, None) in grid_cover:
            continue
        flags.append({
            'type': 'unpriced-ask', 'where': key_label(key),
            'detail': 'the paper prints this ask and no scheme entry claims it'})
    return flags


def _es_scheme_key(token, item):
    if token in ('A1a', 'A1b', 'B'):
        return (token, item)
    m = re.fullmatch(r'A(\d)', token)
    return ('A', int(m.group(1))) if m else (token, item)


def _es_title_key(token):
    if token in ('A1a', 'A1b'):
        return (token, None)
    if token == 'B':
        return ('B', None)
    m = re.fullmatch(r'A(\d)', token)
    if m:
        return ('A', int(m.group(1)))
    if re.fullmatch(r'A2[ab]', token):
        return ('A2', token[2])
    return (token, None)


def _title_words(text):
    """A title's content words, accent-folded, for comparison."""
    folded = ''.join(c for c in unicodedata.normalize('NFKD', (text or '').lower())
                     if not unicodedata.combining(c))
    return {w for w in re.findall(r'[a-z0-9]+', folded) if len(w) > 1}


def _title_agrees(a, b):
    """Do the paper's and the scheme's titles name the same text?

    Scored on shared words rather than on the string, because the two
    documents render the SAME title three ways: the paper breaks a long one
    across two printed lines ("ESPAÑA GANA EL / MUNDIAL"), it spells a number
    the scheme sets as a numeral ("CINCO MILLONES" against "5 MILLONES"), and
    one of them mis-keys a letter ("SAN CRISTÓBAL" against the scheme's "SAN
    CRISTÓBOL"). Requiring the strings to contain one another reported all
    three as disagreements and would have buried a title naming a DIFFERENT
    text under them. Two thirds of the shorter side's words is the bar: the
    worst real pair in the corpus shares five of six.
    """
    x, y = _title_words(a), _title_words(b)
    if not x or not y:
        return True
    return len(x & y) / min(len(x), len(y)) >= 0.66


def es_cover_marks(paths):
    """The totals the booklets print on their own covers, added."""
    import pymupdf
    total = 0
    for path in paths:
        with pymupdf.open(path) as doc:
            m = re.search(r'(\d{2,3})\s*marks\b', doc[0].get_text(), re.I)
        if m:
            total += int(m.group(1))
    return total

def it_flags(P, S):
    """What the paper and the scheme disagree about. See census_it."""
    flags = list(P.flags)
    paper = P.asks()
    for token in sorted({a[0] for a in paper} | {a.section for a in S.asks}):
        pp = [a for a in paper if a[0] == token]
        ss = [a for a in S.asks if a.section == token]
        if len(pp) != len(ss):
            flags.append({
                'type': 'scheme-count',
                'where': f'Section {token}',
                'detail': f'the paper prints {len(pp)} ask(s) here and the '
                          f'scheme prices {len(ss)}'})
            continue
        for a, b in zip(pp, ss):
            if (a[1], a[2]) != (b.item, b.letter):
                flags.append({
                    'type': 'scheme-key',
                    'where': f'Section {token}',
                    'detail': f'the paper prints {a[1]}{a[2] or ""} where the '
                              f'scheme prices {b.item or ""}{b.letter or ""}; '
                              f'they are paired in printed order and the '
                              f'paper\'s name is the one cited'})
    for token, printed in sorted(S.section_totals.items()):
        asks = [a for a in S.asks if a.section == token]
        if not asks or any(a.total is None for a in asks):
            continue
        got = sum(a.total for a in asks)
        if got != printed:
            flags.append({
                'type': 'tariff-checksum',
                'where': f'Section {token}',
                'detail': f'the scheme prices its asks {got} against the '
                          f'{printed} it prints on the section head'})
    return flags


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


def census_ru(subject, year, level):
    """Russian: the written booklet and the listening booklet, read together.

    THE DENOMINATOR IS THE PAPER, and this paper needs the same help French's
    does to say which of its printed markers is a question: a comprehension
    sets its passage in NUMBERED PARAGRAPHS at the same margin and in the same
    shape as its questions. So the reading asks are the printed blocks the
    scheme's own reprinted question locates (ru_paper.find, which is align.py's
    rule), and the PAPER's address is the one keyed even where the scheme
    disagrees — the 2021 Ordinary scheme numbers the retrieval text's last two
    asks "(vii)" and "(vii)" where the paper prints "(vii)" and "(viii)".

    Everything else is read from the paper alone and needs no help. Each of
    the paper's other printed questions is ONE leaf — the grammar, the
    matching task, the structuring-discourse gap-fill, the short essay — with
    two exceptions the paper itself numbers: Higher's language-awareness
    questions, which print a choice of two tasks and price both ("Answer ONE
    of the following: Q. 1.2(i) or 1.2(ii)"), and the guided-writing and
    extended-writing questions, which number their alternatives 1, 2 and 3.

    The census then checks the paper INDEPENDENTLY, in `ru_flags`: every
    scheme ask must have found a printed block, no two may have found the
    same one, and every unit that prints a total must be reached exactly by
    its own asks.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ru_paper import RuPaper                                # noqa: E402
    from ru_scheme import RuScheme, READING_UNITS               # noqa: E402

    P = RuPaper(year, level, subject)
    S = RuScheme(year, level, subject)
    texts = {}
    claimed = set()
    for ask in S.asks:
        if ask.unit not in READING_UNITS:
            continue
        hit = P.find(ask.unit, ask.item, ask.roman, ask.cue, claimed)
        if hit is None:
            continue
        text, _page, block = hit
        claimed.add(id(block))
        texts[(block.unit, block.item, None, block.roman)] = text

    for unit in RU_WHOLE_UNITS:
        if unit not in P.unit_pages:
            continue
        romans = P.choice_romans(unit) if unit in RU_CHOICE_UNITS else []
        items = P.unit_items(unit) if unit in RU_NUMBERED_UNITS else []
        head = ' '.join(P.unit_head.get(unit, unit).split())
        if romans:
            for r in romans:
                texts[(unit, None, None, r)] = f'{head} ({r})'
        elif items:
            for i in items:
                texts[(unit, i, None, None)] = f'{head} {i}'
        else:
            texts[(unit, None, None, None)] = head

    for unit, item, roman, text in P.aural_asks():
        texts[(unit, item, None, roman)] = text

    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S, claimed


# The paper's other printed questions, each of which is one census leaf unless
# the paper numbers alternatives inside it.
RU_WHOLE_UNITS = ('LA1', 'LA2', 'CA1', 'SD', 'GR', 'SE', 'GW', 'MM', 'SA', 'EW')
RU_CHOICE_UNITS = ('LA1', 'LA2', 'CA1')
RU_NUMBERED_UNITS = ('GW', 'EW')


def ru_flags(P, S, claimed):
    """What the paper and the scheme disagree about. See census_ru."""
    flags = []
    seen = set()
    for ask in S.asks:
        if ask.unit not in {'C1', 'C2', 'IR1', 'IR2', 'CD'}:
            continue
        hit = P.find(ask.unit, ask.item, ask.roman, ask.cue, seen)
        if hit is None:
            flags.append({
                'type': 'unmatched-scheme-ask',
                'where': S.ref(ask),
                'detail': f'the scheme prices {ask.cue[:70]!r} and no printed '
                          f'question in that unit matches its wording'})
            continue
        block = hit[2]
        seen.add(id(block))
        if (block.item, block.roman) != (ask.item, ask.roman):
            flags.append({
                'type': 'scheme-key',
                'where': S.ref(ask),
                'detail': f'the paper prints this ask as '
                          f'{block.item or ""}{f"({block.roman})" if block.roman else ""} '
                          f'and the paper\'s name is the one cited'})
    for unit, printed, got, _n in S.checksum():
        if printed is not None and printed != got:
            flags.append({
                'type': 'tariff-checksum',
                'where': f'{S.year} {S.level.upper()} {unit}',
                'detail': f'the scheme prices its asks {got} against the '
                          f'{printed} it prints on the unit head'})
    return flags

def census_pl(subject, year, level):
    """Polish: the written booklet and, from 2022, the listening booklet.

    THE DENOMINATOR IS THE PAPER, and this paper can be read from the paper
    alone. Its reading passage is set in numbered paragraphs, exactly as
    French's is, but it letters its questions "(a)" to "(l)" — so no printed
    marker is ambiguous between passage and ask, and no wording has to be
    scored to find one. The scheme is read beside it to price the asks and to
    be CHECKED against them, which is what pl_flags does.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pl_paper import PlPaper                                # noqa: E402
    from pl_scheme import PlScheme                              # noqa: E402

    P = PlPaper(year, level, subject)
    S = PlScheme(year, level, subject)
    texts = {ask.key: ask.full_text for ask in P.all_asks()}
    files = [P.path] + ([P.aural_path] if P.aural_path else [])
    return set(texts), texts, files, P, S


def pl_flags(P, S):
    """Where the paper and the scheme disagree about what was asked.

    The two documents are read independently — the paper for its asks, the
    scheme for its prices — so every ask one holds and the other does not is a
    reader fault, an SEC misprint or a real difference, and all three have to
    be looked at rather than reconciled away. This is Law 3's independent
    check: the census's own continuity flags see only interior gaps, and an
    ask keyed under its NEIGHBOUR's letter leaves no gap at all.
    """
    flags = list(P.flags)
    paper = {a.key for a in P.reading_asks()}
    scheme = {a.key for a in S.reading()}
    # An ask the scheme prices ONE LEVEL UP is priced, not missing. 2022 Higher
    # numbers Question 2(i)'s four true/false statements (i) to (iv) and the
    # scheme prices the table once, "(4 x 1m)", printing its statements with no
    # markers at all; the same shape answers every tick-one-box question in the
    # corpus. Counting those as unpriced reported five flags on a table the SEC
    # priced in full.
    priced_parents = {(a.section, a.q, a.letter) for a in S._asks
                      if a.roman is None and a.per is not None}
    for key in sorted(paper - scheme, key=str):
        if (key[0], key[1], key[2]) in priced_parents:
            continue
        flags.append({'type': 'unpriced-ask', 'where': key_label(key),
                      'detail': 'the paper prints this ask and the scheme '
                                'prices no ask at that address'})
    paper_parents = {(a.section, a.q, a.letter) for a in P.reading_asks()}
    for key in sorted(scheme - paper, key=str):
        if (key[0], key[1], key[2]) in paper_parents:
            continue                     # the paper numbers what the scheme
        flags.append({'type': 'orphan-scheme-ask', 'where': key_label(key),
                      'detail': 'the scheme prices this address and the paper '
                                'prints no ask there'})
    for ask in S.reading():
        if ask.fault:
            flags.append({'type': 'tariff-disagreement',
                          'where': key_label(ask.key), 'detail': ask.fault})
    return flags


def census_clas(subject, year, level):
    """Classical Studies: the printed ask, in whichever of its two papers.

    THE DENOMINATOR IS THE PAPER. `cl_paper.ClPaper` reads it — the ten-topic
    paper of 2021-2022 and the Section A/B paper of 2023-2025 — and the scheme
    is read beside it only so the two can be CHECKED against each other, never
    so the scheme can supply an ask the paper does not print.

    The check is unusually strong here, because the two documents share an
    address. In the old paper every one of the 388 printed parts has exactly
    one scheme entry at the same (topic, roman, letter) and no scheme entry is
    left over; in the new one every scheme entry lands on a printed ask, at its
    own address or at the letter or question it was priced under. `clas_flags`
    asserts both, and asserts the tariffs agree.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cl_paper import ClPaper                               # noqa: E402
    from cl_scheme import ClScheme                             # noqa: E402

    P = ClPaper(year, level, subject)
    S = ClScheme(year, level, subject)
    texts = {}
    for ask in P.asks():
        texts[ask.key] = f'{ask.stem} {ask.text}'.strip()
    return set(texts), texts, [P.path], P, S


def clas_flags(P, S):
    """Everything that would be true if both readers read the same paper."""
    flags = []
    paper_keys = {a.key for a in P.asks()}
    scheme = S.by_key()
    for key in sorted(scheme, key=str):
        if key in paper_keys:
            continue
        # The scheme may price a LETTER whole where the paper prints romans
        # under it, or a QUESTION whole where the paper prints alternatives.
        if any(p[:3] == key[:3] for p in paper_keys):
            continue
        if key[2] is None and any(p[:2] == key[:2] for p in paper_keys):
            continue
        flags.append({'type': 'scheme-orphan', 'where': str(key),
                      'detail': 'the scheme prices an address the paper '
                                'does not print'})
    if P.era == 'topics':
        totals = collections.defaultdict(int)
        for ask in P.asks():
            totals[ask.section] += ask.marks or 0
        if len(totals) != 40:
            flags.append({'type': 'question-count', 'where': 'topics',
                          'detail': f'{len(totals)} questions, expected 40 '
                                    '(ten topics x four questions)'})
        for section, total in sorted(totals.items()):
            if total != 50:
                flags.append({'type': 'marks-checksum', 'where': section,
                              'detail': f'parts sum to {total}, the paper '
                                        'prints fifty marks per question'})
        for key in sorted(paper_keys, key=str):
            if key not in scheme:
                flags.append({'type': 'unpriced-ask',
                              'where': key_label(key),
                              'detail': 'no scheme entry at this address'})
    else:
        qs = sorted({a.q for a in P.asks() if a.q})
        if qs != list(range(1, 17)):
            flags.append({'type': 'question-gap', 'where': 'Questions',
                          'detail': f'questions found: {qs}'})
        missing = [q for q in range(1, 11)
                   if (None, q) not in P.question_marks]
        if missing:
            flags.append({'type': 'unpriced-question', 'where': 'Section A',
                          'detail': f'no printed tariff on Q{missing}'})
    for key in sorted(paper_keys & set(scheme), key=str):
        ask = next(a for a in P.asks() if a.key == key)
        entry = scheme[key]
        if ask.marks and entry.marks and ask.marks != entry.marks \
                and not ask.inherited \
                and key not in _CLAS_TARIFF_SPLITS.get(
                    (P.year, P.level), ()):
            flags.append({'type': 'tariff-disagreement',
                          'where': key_label(key),
                          'detail': f'paper prints {ask.marks}, scheme '
                                    f'prints {entry.marks}'})
    return flags


# Where the SEC's own two documents price the SAME printed part differently.
# Every one was read off both PDFs before it was entered here, and each is one
# of two shapes:
#
#   * the two documents SPLIT a fifty-mark question differently and both add
#     up — 2021 Higher Topic 1(i) is 40+10 on the paper and 35+15 in the
#     scheme, 2021 Higher Topic 4(ii) is 20+10+20 against 20+15+15;
#   * the scheme's printed total contradicts the scheme's OWN split, and the
#     split agrees with the paper — 2022 Higher Topic 8(iii)(d) reads
#     "(8, 7.) (20 marks)" over a part the paper prices at 15, and 2022
#     Ordinary Topic 9(iv)(b) reads "(10, 10.) (10 marks)" over a part the
#     paper prices at 20. In both the sub-totals are right and the total is
#     the misprint.
#
# The paper wins in every case, which is the bank's rule when the two
# disagree, and a card carries the paper's tariff.
_CLAS_TARIFF_SPLITS = {
    (2021, 'hl'): {('Topic 1(i)', None, 'a', None),
                   ('Topic 1(i)', None, 'b', None),
                   ('Topic 4(ii)', None, 'b', None),
                   ('Topic 4(ii)', None, 'c', None),
                   ('Topic 4(iii)', None, 'b', None)},
    (2022, 'hl'): {('Topic 8(iii)', None, 'd', None)},
    (2022, 'ol'): {('Topic 9(iv)', None, 'b', None)},
}


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
                elif cfg.get('walker') == 'lang':
                    parts, texts, files, P_, S_, claimed_ = census_lang(
                        subject, year, level)
                elif cfg.get('walker') == 'de':
                    parts, texts, files, P_, S_, claimed_ = census_de(
                        subject, year, level)
                elif cfg.get('walker') == 'es':
                    parts, texts, files, P_, S_ = census_es(subject, year, level)
                elif cfg.get('walker') == 'italian':
                    parts, texts, files, P_, S_ = census_it(
                        subject, year, level)
                elif cfg.get('walker') == 'ru':
                    parts, texts, files, P_, S_, claimed_ = census_ru(
                        subject, year, level)
                elif cfg.get('walker') == 'ja':
                    parts, texts, files, P_, S_ = census_ja(
                        subject, year, level)
                elif cfg.get('walker') == 'clas':
                    parts, texts, files, P_, S_ = census_clas(
                        subject, year, level)
                elif cfg.get('walker') == 'pl':
                    parts, texts, files, P_, S_ = census_pl(
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
            elif cfg.get('walker') == 'lang':
                flags += lang_flags(P_, S_, claimed_)
                marks = {(None, 0): lang_cover_marks(files)}
            elif cfg.get('walker') == 'de':
                flags += de_flags(P_, S_, claimed_)
                marks = {(None, 0): lang_cover_marks(files)}
            elif cfg.get('walker') == 'es':
                flags += es_flags(P_, S_)
                marks = {(None, 0): es_cover_marks(files)}
            elif cfg.get('walker') == 'italian':
                flags += it_flags(P_, S_)
                marks = {(None, 0): lang_cover_marks(files)}
            elif cfg.get('walker') == 'ru':
                flags += ru_flags(P_, S_, claimed_)
                marks = {(None, 0): lang_cover_marks(files)}
            elif cfg.get('walker') == 'ja':
                flags += ja_flags(P_, S_)
                marks = {(None, 0): lang_cover_marks(files)}
            elif cfg.get('walker') == 'clas':
                flags += clas_flags(P_, S_)
                # The 2023 syllabus change made this a different paper: 200
                # marks over ten topics before it, 400 over Sections A and B
                # after. Naming the era keeps the cross-year marks checksum
                # comparing each paper with its OWN kind, which is what the
                # checksum is for; without it every old sitting reported a
                # 200-mark "shortfall" against the new ones.
                label = ('Ten Topics' if P_.era == 'topics'
                         else 'Sections A and B')
                # A Classical Studies paper is almost entirely CHOICE — four
                # questions out of forty in the old paper, one essay out of
                # five in the new — so adding up every printed tariff would
                # count questions nobody sits. The checksum is the total the
                # paper states on its own cover.
                marks = {(None, 0): 400 if P_.era == 'sections' else 200}
            elif cfg.get('walker') == 'pl':
                flags += pl_flags(P_, S_)
                marks = {(None, 0): P_.cover_marks()}
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
