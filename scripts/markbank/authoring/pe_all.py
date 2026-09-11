#!/usr/bin/env python3
"""Author every Physical Education ask whose scheme STATES its answer.

    python3 scripts/markbank/authoring/pe_all.py --report   # covered/741 + buckets
    python3 scripts/markbank/authoring/pe_all.py            # emit JSON
    python3 scripts/markbank/authoring/pe_all.py --write    # authored/ + exclusions/

THE MEASUREMENT THIS SUBJECT TURNS ON.  Physical Education's written paper is
one of three components — the other two are a physical performance and a
coursework project, neither of which this corpus holds and neither of which
any paper prints.  The question that decides the written paper is whether its
scheme prints ANSWERS or BANDS, and it prints both:

    STATED   "Barriers may include: -Facilities -Access -Finance -Influence
              of family -Peer Group"                      (2024 HL Q2(b))
    BAND     "Clear and accurate definition. 2 / Some accuracy in the
              definition. 1"                              (2024 HL Q2(a))

Both are priced; only the first is liftable.  A band ladder states nothing a
student could have written, so it is EXCLUDED with its own printed lines as
the evidence — generated from the scheme reader, never hand-typed — and the
stated parts are carded.  The share swings hard by sitting, which is why the
verdict is counted per sitting and never read off one paper.

WHAT A TARIFF MAY COME FROM.  Only the scheme's own printed arithmetic:

    "8 (2 x 4 marks)"     a menu of answers, two claimable at four each
    "4 x 2 marks"         the same, written without the total
    "2x1marks=2"          the same again, spelled out with its total
    "3 marks + 3 marks"   the same as a repeat
    "2 marks", "1 mark"   one stated answer at its own printed value

Nothing is derived by dividing a total by a count the SEC did not state.  A
part whose tariff cannot be read one way is REFUSED, and every refusal is a
named bucket reported with a count and a real example.

WHAT THE PAPER PRINTS AND THE SCHEME DOES NOT.  Many asks are answered by the
candidate's OWN performance, project or chosen physical activity, and the
scheme prices them by band because there is no answer to print.  Those are
exclusions with the scheme's own lines as evidence, not gaps.  What is a gap
is an ask whose scheme prints a good answer this reader cannot reach; every
one of those is reported OPEN and none is laundered into an exclusion.

WHERE THIS STANDS, measured against the census's 741 leaf asks over thirteen
papers:

    229  covered by 225 cards
    480  excluded, each carrying the scheme's own printed lines
     32  OPEN, in the buckets `--report` prints, every one of them an ask
         whose SCHEME states an answer this reader cannot lift:

       8  the answer is in a printed table's other column and the flat text
          layer interleaves the two (2020 HL Q16(b)(iii)'s energy-system
          grid; 2026 OL Q15(a)(i)'s three-column concept table). pe_tables
          reads the tables that are drawn with RULES; these are aligned by
          whitespace, or wrap their cells differently line by line.
       6  the scheme marks its answer with a TICK in a printed column, and
          the text layer hands back the tick without the column.
       5  a marking point does not trace to its own scheme — the converter
          dropped the marks column into the middle of the SEC's sentence and
          no rebuilt form of it matches.
       5  the scheme prints no tariff that reads one way, mostly a part
          priced in two different groups at once (2024 HL Q8(a): "2 x 1 mark"
          for the injury and "2 x 2 marks" for its causes, in one table that
          also holds part (b)).
       3  no scheme part prices the ask at all.
       3  the ask points at a figure, table or case study whose answer is not
          on the paper page this reader found for it.
       1  the paper prints no ask text under the key (2022 OL Q18(a)(i), a
          figure caption the walker kept).
       1  the scheme's line holds its answer welded onto the criterion and
          cut in half by the wrap (2024 OL Q13(b)(i)).

    NONE of those thirty-two is excluded. An exclusion here claims the scheme
    prints nothing a student could have written, and for an ask whose answer
    is in a cell this reader could not read, that claim is exactly the thing
    it does not know.

"""
import argparse
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import pe_lib as L                                              # noqa: E402
import pe_scheme as S                                           # noqa: E402
import pe_tables as T                                           # noqa: E402
from pe_lib import ASK_OPENER, ask_text                         # noqa: E402
from pe_topics import concept_for, topic_for                    # noqa: E402
from paper import Paper                                         # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, point  # noqa: E402

OUT = os.path.join(ROOT, 'scripts/markbank/authored/physical-education.json')
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'physical-education.json')
BINDINGS = os.path.join(ROOT, 'scripts/markbank/card-source-bindings.json')
PAPERS = os.path.join(ROOT, 'examiner-reports', 'physical-education', 'papers')
# The build refuses a menu longer than this; see groupFault() in build-deck.mjs.
HARD_OPTION_CAP = 16
MAX_OPTION_CHARS = 700

card = make_card('physical-education', default_section='A')
audit = make_audit(HARD_OPTION_CAP)

# An ask the candidate cannot answer without the figure, case study, table or
# printed list beside it. Held rather than shipped blind: a card that quotes
# "Make two statements about doping in cycling based on information presented
# in Figure 12" without Figure 12 is unanswerable.
NEEDS_SOURCE = re.compile(
    r'\b(figure\s*\d+|in the (?:figure|table|graph|case study|photograph)'
    r'|shown (?:above|below)|depicted (?:above|below|in)'
    r'|the (?:image|photograph|graph|diagram) (?:above|below)'
    r'|with reference to the case study|from the case study'
    r'|in the case study|mentioned in the case|in the box'
    r'|the data (?:above|below|shown)|the score ?sheet'
    r'|(?:table|diagram|text) below)\b', re.I)
# The SEC's answer is a TICK IN A COLUMN. 2025 Ordinary Q1 prints four
# statements and puts a ✓ in the True or the False column beside each; the text
# layer hands back the statement and the tick and says nothing about which
# column the tick is in, so a card written from it would state the opposite
# answer as readily as the right one. The tick in the SCHEME is the signal —
# never the word "tick" in the QUESTION, which is a rubric ("Tick the box to
# indicate which term you are defining") and says nothing about the answer.
# Never the tick inside the RUBRIC's own "(✓)", which every such question
# prints in its instruction and which marks nothing.
SCHEME_TICK = re.compile(r'(?<!\()[✓✔\uf0fc\u2713](?!\))')
# An ask answered by COMPLETING A PRINTED TABLE — matching four explanations to
# four named methods, filling blanks from a word bank, ticking a column. The
# scheme answers it in the table's OTHER COLUMN, and the flat text layer reads
# the two columns across rather than down: "Run a sprint, rest, receive
# feedback, Distributed repeat." is the SEC's explanation with the SEC's answer
# posted into the middle of it. A card built from that states neither. The ask
# is refused by its own printed instruction rather than by trying to unpick the
# row — append-scheme-columns.py is the tool that would read it properly, and
# until it is run and checked here these stay OPEN and named.
TABLE_TASK = re.compile(
    r'^(?:match\b|complete the (?:following )?table|complete the table'
    r'|fill in the blanks?|put a tick|place a tick|insert a tick)', re.I)
# The same task set as a sentence rather than an instruction: "Describe each of
# the following concepts of physical activity by matching the concept to the
# relevant description", "Identify an appropriate timeframe for each of these
# cycles". The give-away is the printed COLUMN HEADING the scheme answers
# under — "please choose from above", "choose from above" — which is the
# table's other column and not an answer to anything.
TABLE_TASK_INLINE = re.compile(
    r'\bby matching the\b|\bmatch(?:ing)? (?:the|each)\b[^.]{0,60}\b(?:to|with) the\b'
    r'|\bchoose from above\b|\busing the (?:methods|words|terms) provided\b'
    r'|\b(?:by )?(?:putting|placing|inserting) a tick\b', re.I)
# A card must not cite an ask whose subject lives in a neighbouring part —
# "one of the measures named by you in question 13" answers nothing alone.
BACK_REFERENCE = re.compile(
    r'\bidentified by you in\b|\bnamed by you in\b|\bchosen by you in\b'
    r'|\bstated by you in\b|\boutlined by you in\b|\bcorrectly named in\b'
    r'|\bgiven by you in\b|\bin question \d|\bin part \(|\bin \([ivx]+\)'
    r'|\byou have identified\b|\byou identified\b', re.I)

# An option the SEC prints that is not an answer.
NOT_A_POINT = re.compile(
    r'^(?:etc\.?|and so on|any other\b|other relevant\b|accept\b|award\b'
    r'|allow\b|note:|no marks\b|max\b|total\b|marks?\b|description\b|or\b'
    # The paper's own rubric, reprinted inside the scheme's table. It tells the
    # candidate how to record their choice and answers nothing.
    r'|(?:please )?choose from above\b|(?:put|place) a tick\b|tick the box\b'
    r'|indicate which\b)', re.I)
# A fragment the converter left behind when it split a wrapped line — "and
# incomplete", "...displayed to promote others participation in physical
# activity enthusiastic, organised and v". Not the same thing as a rubric: a
# rubric states nothing and its ask is EXCLUDED, while a fragment is a line
# this reader lost half of and its ask stays OPEN.
FRAGMENT = re.compile(
    r'^(?:and|or|but)\b'
    r'|\b(?:and|or|but|with|of|to|the|in|for)(?:\s+\S{1,2})?$', re.I)
TARIFF_RESIDUE = re.compile(r'\b\d{1,2}\s*(?:m|marks?)\b|\d\s*[x×@]\s*\d', re.I)
# The marks column glued to the FRONT of the row it priced. What follows is
# the examiner's criterion cut off at its own first word: "3+3+2 opponent that
# could improve her defence and help her win the ball back".
LEADING_TARIFF = re.compile(
    r'^\d{1,2}\s*(?:[x×+]\s*\d{1,2}\s*)+'
    # ...and the bare word the marks column leaves behind when it wrapped:
    # "marks outdoor and adventure activities" is the tail of a cell, not an
    # answer that begins with the word marks.
    r'|^marks?\s+(?=\S)', re.I)
# The same bare word on either end of ONE item of a list, where the cell wrapped
# into the middle of the SEC's own comma-separated answers: "positive
# self-talk, visualisation, meditation marks" splits into three answers and a
# stray. Taken off each item, never from the middle, and the item is still
# checked against the scheme afterwards.
GLUED_MARK_WORD = re.compile(r'^marks?\s+|\s+marks?$', re.I)
# The SEC closes most of its lists by saying the list is not closed. That tail
# is not an answer — "Positivity, Excellent negotiation skills and other
# relevant" is one answer and a disclaimer — and the card says the same thing
# in its notes, in the scheme's own words.
OPEN_LIST_TAIL = re.compile(
    r'\s*(?:[,;]\s*)?(?:and|or)?\s*(?:other relevant(?:\s+\w+)?'
    r'|other appropriate(?:\s+\w+)?|any other relevant(?:\s+\w+)?'
    r'|etc\.?|and so on)\s*[.;,]?\s*$', re.I)


def tidy(s):
    return ' '.join((s or '').split())


# ------------------------------------------------------------------ asks ----

_PAPERS = {}


def paper_for(year, level):
    if (year, level) not in _PAPERS:
        _PAPERS[(year, level)] = Paper(L.SUBJECT, year, level)
    return _PAPERS[(year, level)]


# ------------------------------------------------------------ the source ----
# An ask that points at a printed figure, table or case study is not refused
# for pointing at one: the SEC's own page is in the Paper Trail index, and
# card-source-bindings.json attaches it so the student opens the exact
# examination page the question was set on. What still cannot be carded is an
# answer the SCHEME does not state in words — a tick in a column, or the other
# half of a matching table the columns reader cannot reach — and those keep
# their own named buckets.
_PAGES = {}


def _page_text(year, level):
    if (year, level) not in _PAGES:
        import pymupdf
        path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')
        with pymupdf.open(path) as doc:
            _PAGES[(year, level)] = [tidy(page.get_text()) for page in doc]
    return _PAGES[(year, level)]


def _flat(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').lower())


def source_pages(year, level, qtext):
    """The paper's own page(s) this ask and its source are printed on.

    One-based, as build-deck requires, and found by searching the paper for
    the ask's own words and for every figure it names — never guessed from the
    question number, which is a page apart from its figure often enough to put
    the wrong page in front of a student.
    """
    pages = _page_text(year, level)
    wanted = _flat(qtext)[:60]
    ask_page = None
    if wanted:
        for i, text in enumerate(pages):
            if wanted in _flat(text):
                ask_page = i + 1
                break
    found = [ask_page] if ask_page else []
    for label in re.findall(r'\bFigure\s*\d+\b', qtext, re.I):
        needle = _flat(label)
        hits = [i + 1 for i, text in enumerate(pages) if needle in _flat(text)]
        if not hits:
            continue
        # A case study NAMES its figures on its opening page and PRINTS them
        # two pages later, so the first page carrying the label is often the
        # contents rather than the chart. The page nearest the ask is the one
        # the candidate was looking at — and never the ask's own page, which
        # is already bound.
        other = [h for h in hits if h != ask_page]
        if not other:
            continue
        pick = min(other, key=lambda h: (abs(h - (ask_page or h)), h))
        if pick not in found:
            found.append(pick)
    return sorted(found)[:2]


# --------------------------------------------------------------- answers ----

def options_for(part, year, level, qtext):
    """The scheme's stated answers for one part, as a menu.

    Every option is SLICED from the scheme, checked against the scheme
    markdown the provenance gate reads, and refused if it is the ask's own
    words rather than an answer to it — the SEC reprints the question above
    its table often enough that a reader taking every content line would
    otherwise ship the question as its own answer.
    """
    out, untraceable, restated, criteria = [], [], [], []
    ask = re.sub(r'[^a-z0-9]+', '', (qtext or '').lower())
    for text, source in S.answers_of(part, with_source=True):
        text = tidy(GLUED_MARK_WORD.sub(
            '', tidy(OPEN_LIST_TAIL.sub('', tidy(text))))).strip(' .;,')
        # Four characters is the floor for a phrase; a NUMBER is an answer at
        # two. "2%" is the whole of what the 2021 Higher scheme prints for
        # "what percentage of post-primary school students do not get 60
        # minutes of MVPA on at least one day?", and a four-character floor
        # excluded the ask for having an answer too short to be one.
        if not text or (len(text) < 4 and not re.search(r'\d', text)):
            continue
        if NOT_A_POINT.match(text):
            criteria.append(text)         # the paper's rubric, not an answer
            continue
        if FRAGMENT.search(text):
            untraceable.append(text)      # half a line: the ask stays OPEN
            continue
        # A measured answer has no letters in it at all — "2%", "9.5 m/s" —
        # so the letters test cannot be the only one. What separates it from a
        # marks cell is that a marks cell is bare arithmetic.
        measured = re.fullmatch(r'\d+(?:[.,]\d+)?\s*(?:%|m/s|km/h|s|kg|m)?',
                                text, re.I)
        if (not measured and not re.search(r'[A-Za-z]{3}', text)) \
                or re.search(r'[x×]\s*\d', text):
            criteria.append(text)         # a marks cell, not an answer
            continue
        # A line that OPENS like a criterion or a band is the examiner talking
        # about the answer, not the answer: "Examines two approaches that can
        # be used to promote physical activity participation", "Two positive
        # and two negative effects of the media for spectators", "No link
        # between hosting and developing tourism mentioned". Applied to every
        # source, including the SEC's own lists, because a list that ran one
        # line past its end ends on exactly such a row.
        if (S.CLOSES_LIST.match(text) or S.BAND_OPENER.match(text)
                or S.EXAMINER_NOTE.match(text) or S.TABLE_HEAD.match(text)
                or LEADING_TARIFF.match(text)):
            criteria.append(text)
            continue
        if TARIFF_RESIDUE.search(text) or len(text) > MAX_OPTION_CHARS:
            untraceable.append(text)
            continue
        if not L.traces(year, level, text):
            untraceable.append(text)
            continue
        flat = re.sub(r'[^a-z0-9]+', '', text.lower())
        # Six characters before this test means anything: "2%" reduces to "2",
        # which is inside almost every ask ever printed, and the SEC's answer
        # to "what percentage..." was thrown away as the question's own words.
        if len(flat) >= 6 and ask and flat in ask:
            restated.append(text)         # the ask's own words, not an answer
            continue
        if text not in out:
            out.append(text)
    # A single answer line holding the SEC's own list — "Facilities; Access;
    # Finance" or "continuous training; weight training; plyometrics" — is that
    # list, not one answer. Split it only where the SEC's own separator is
    # there and every piece still traces to the scheme on its own.
    if len(out) == 1 and re.search(r'[;,]', out[0]):
        for sep in (r'\s*;\s*', r'\s*,\s*'):
            pieces = [tidy(GLUED_MARK_WORD.sub('', tidy(x))).strip(' .;,')
                      for x in re.split(sep, out[0])]
            pieces = [p for p in pieces if 3 <= len(p) <= 90]
            if len(pieces) >= 2 and all(L.traces(year, level, p) for p in pieces):
                out = pieces
                break
    return out[:HARD_OPTION_CAP], untraceable, restated, criteria


# --------------------------------------------------------------- tariffs ----

def menu_tariff(part):
    """(claim, per) for a part answered by ONE menu, or None.

    Every reading is the SEC's printed arithmetic. Where the part prints more
    than one distinct group the reading is ambiguous and the part is refused.
    """
    groups = sorted(set(part.tariffs))
    if len(groups) == 1:
        return groups[0]
    return None


def single_tariff(part):
    """The price of a part the scheme answers ONCE, or None.

    Read only where every marks value printed anywhere in the part agrees:
    two different values mean the part is priced in pieces, and choosing
    between them would be inventing a tariff.
    """
    values = set()
    for text in [part.cue] + part.rows + part.answers + part.cells:
        for m in re.finditer(r'(\d{1,2})\s*(?:marks?|m)\b', text or '', re.I):
            values.add(int(m.group(1)))
    if len(values) == 1:
        return next(iter(values))
    return None


# ------------------------------------------------------------------ refs ----

def ref_for(year, level, key):
    q, letter, roman = key
    tail = (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
    return f'{year} {level.upper()} Q{q}{tail}'


def ref_for_many(year, level, keys):
    """The citation for a card that answers SEVERAL of a question's asks.

    Named leaf by leaf, never by the letter or the question above them. A card
    written from a scheme part that prices Q3(b) and Q3(d) covers exactly those
    two, and citing it "2021 OL Q3" would claim (a) and (c) as well — which is
    what made the Q3(c) exclusion report stale, the ledger's way of saying two
    rows of it disagree about the same ask.
    """
    q = keys[0][0]
    tail = ', '.join((f'({letter})' if letter else '')
                     + (f'({roman})' if roman else '')
                     for _q, letter, roman in keys)
    return f'{year} {level.upper()} Q{q}{tail if tail.startswith("(") else ""}'


def card_id(year, level, key):
    q, letter, roman = key
    return f'pe-{year}-{level}-q{q}' + (letter or '') + (roman or '')


def back_reference_stem(order, texts, labels, key):
    """The earlier ask under the same question this one points back at."""
    if key not in order:
        return ''
    here = order.index(key)
    for other in reversed(order[:here]):
        if other[0] != key[0]:
            break
        text = tidy(texts.get(other) or '')
        if len(text) < 12 or BACK_REFERENCE.search(text):
            continue
        return tidy(f'{labels.get(other, "")}: {text}')[:400]
    return ''


def section_of(q, year):
    """The paper's own section for a question number.

    Read from the printed instructions every sitting sets on page 2: Section A
    short answers, Section B the case study, Section C the long questions.
    2020 sat an altered examination whose Section A ran to ten questions and
    whose Section C offered three rather than five, so its boundaries are its
    own.
    """
    if year == 2020:
        return 'A' if q <= 10 else ('B' if q == 11 else 'C')
    return 'A' if q <= 12 else ('B' if q == 13 else 'C')


NOTES = ('The list is what the SEC published and is not exhaustive — the '
         "scheme's own note says the suggestions and examples in it are not "
         'exhaustive and alternative valid answers are acceptable.')


def band_evidence(part):
    """The scheme's own printed lines, so an exclusion cites the document."""
    rows = [r for r in part.rows if not S.TABLE_HEAD.match(r)]
    if part.cue:
        rows = [part.cue] + rows
    return ' / '.join(rows[:4])[:400] or '(the scheme prints no row for this part)'


# What the converter leaves on the end of a criterion when the marks column
# wrapped: a bare "marks", a "+", a hyphen. The tariff itself is already off.
LABEL_RESIDUE = re.compile(r'(?:\s*(?:marks?|\+|[-–]))+\s*$', re.I)


def row_label(part, claim):
    """A label for the menu, in the scheme's own words for what it pays for."""
    lead = next((r for r in part.rows
                 if S.LEAD_IN.match(r) and len(tidy(r)) > 8), '')
    if not lead:
        lead = next((r for r in part.rows
                     if not S.TABLE_HEAD.match(r) and not S.EXAMINER_NOTE.match(r)
                     and not S.BAND_OPENER.match(r)
                     and len(S.strip_tariff(r)) > 12), '')
    label = tidy(LABEL_RESIDUE.sub('', tidy(re.sub(r'\s*[:.]\s*$', '',
                                                   S.strip_tariff(lead)))))
    if not label or len(label) < 8:
        label = f'Any {claim} of the answers the scheme states'
    elif len(label) > 110:
        label = label[:107].rsplit(' ', 1)[0] + '…'
    return label


# ----------------------------------------------------------------- build ----

def build():
    cards, refusals, excluded = [], collections.defaultdict(list), []
    covered, seen_parts, bindings = [], {}, {}

    for year, level in L.SITTINGS:
        lvl = 'higher' if level == 'hl' else 'ordinary'
        _paper, _parts, pairs, unpaired, _why = L.pair(year, level)
        printed = L.leaves(year, level)
        texts = {key: ask_text(year, level, key, text)
                 for key, _label, text in printed}
        labels = {key: label for key, label, _text in printed}
        order = [key for key, _label, _text in printed]
        for key, label, _text in unpaired:
            refusals['no scheme part prices this ask'].append(
                (year, level, ref_for(year, level, key), label))

        # One card per SCHEME PART, not per leaf: where the scheme prices a
        # letter the paper numbers romans under, the ask is inside that part
        # and one card covers every leaf beneath it — which is how
        # reconcile.py reads a citation one level up.
        siblings = collections.defaultdict(list)
        for _key, (a_part, _r, _s) in pairs.items():
            group = siblings[a_part.address[:2]]
            if a_part not in group:
                group.append(a_part)

        by_part = collections.OrderedDict()
        for key, (part, route, _sc) in pairs.items():
            by_part.setdefault(id(part), (part, []))[1].append(key)

        for part, keys in by_part.values():
            keys.sort()
            key = keys[0]
            ref = (ref_for(year, level, key) if len(keys) == 1
                   else ref_for_many(year, level, keys))
            qtext = texts.get(part.address) or texts.get(key) or ''
            # The TABLE first. A part the SEC answered inside its own printed
            # table states nothing in its flat text but the two columns welded
            # together, so every gate below would read it as stating nothing
            # and exclude it — which is the one verdict that is certainly
            # wrong, because the answer is right there in the cells.
            table_rows = T.rows_for(part, year, level)
            options, untraceable, restated, criteria = options_for(
                part, year, level, qtext)
            if table_rows:
                options = options or ['(answered in the printed table)']
            # The tick may be on a SIBLING: 2024 Ordinary lists three
            # statements as (i), (ii) and (iii) and ticks the one that is
            # right, so (i) and (iii) print no answer BECAUSE the answer is
            # the tick two lines below them. Excluding them as "the scheme
            # states no answer" would be false.
            # ...and only where THIS part is a bare printed statement with no
            # table of its own, which is the shape that prints a menu of them:
            # widened past that, one tick under a question blocked every part
            # of it, including four that print their own answers.
            ticked = [t for t in part.rows + part.answers
                      if SCHEME_TICK.search(t)]
            if not ticked and part.cue and not part.rows and not part.answers:
                ticked = [o.cue for o in siblings.get(part.address[:2], [])
                          if o.address[2] and o.cue and not o.rows
                          and SCHEME_TICK.search(o.cue)]


            def refuse(bucket, detail=''):
                for k in keys:
                    refusals[bucket].append((year, level, ref_for(year, level, k),
                                             detail))

            if not options and not table_rows and (
                    TABLE_TASK.match(qtext) or TABLE_TASK_INLINE.search(qtext)):
                # The answer to a matching task is in the table's other
                # column, so "the scheme states no answer" is exactly the
                # thing this reader cannot know about it. Never excluded on
                # that evidence — 2026 Ordinary Q15(a)(i) prints Play,
                # Outdoor and adventure and Mass Participation in cells this
                # reader could not separate, and excluding it would have said
                # the SEC printed nothing.
                refuse('the ask is answered inside a printed table whose '
                       'other column the flat text layer interleaves',
                       qtext[:80])
                continue
            if not options:
                # A part whose only stated content is the QUESTION reprinted
                # above its table states no answer either: the SEC sets
                # "Explain two of the following terms: Sports endorsement;
                # Sports merchandising; Sports related advertising" and then
                # a band ladder, and the three terms are what was ASKED. That
                # is the band-only case with the question quoted into it, and
                # it is excluded on the same evidence — unless the ask points
                # at a figure or table, where the answer is on the page rather
                # than in the scheme and the refusal belongs to the figure.
                if ticked and not table_rows:
                    refuse('the scheme marks its answer with a tick in a '
                           'printed column the text layer cannot place',
                           ticked[0][:80])
                elif S.band_only(part) or ((restated or criteria)
                                           and not NEEDS_SOURCE.search(qtext)):
                    for k in keys:
                        excluded.append({
                            'ref': ref_for(year, level, k),
                            'reason': ('the scheme prints this ask and its '
                                       'tariff and states no answer'
                                       if not part.rows else
                                       'the scheme prices this ask by band '
                                       'descriptor and states no answer')
                                      + (' beyond the question\'s own wording'
                                         if restated else '')
                                      + (' — every line it prints under this '
                                         'part is the examiner judging an '
                                         'answer rather than stating one'
                                         if criteria and not restated else ''),
                            'evidence': band_evidence(part),
                        })
                elif restated and (NEEDS_SOURCE.search(qtext)
                                   or any(SCHEME_TICK.search(t)
                                          for t in part.rows + part.answers
                                          if t)):
                    # The scheme names the labels and the paper prints the
                    # diagram they sit on: "Effort (2 marks) / Load (2 marks) /
                    # Fulcrum (2 marks)" answers "Label the load, effort and
                    # fulcrum on the diagram below" only with the diagram.
                    refuse('the ask depends on a figure, table or case study '
                           'the card cannot show', qtext[:80])
                elif untraceable:
                    refuse('a marking point does not trace to its own scheme',
                           untraceable[0][:70])
                else:
                    refuse('the scheme states nothing this reader can lift',
                           (part.rows or [''])[0][:70])
                continue

            # The build's own floor, mirrored here so the ask lands in a named
            # bucket instead of being dropped after the deck is written:
            # "Figure 16 400m" is a caption the walker kept, not a question.
            if len(qtext) < 16 and not ASK_OPENER.match(qtext):
                refuse('the paper prints no ask text under this key', qtext[:60])
                continue
            groups = sorted(set(part.tariffs))
            steps = next((st for text in [part.cue] + part.rows + part.cells
                          for st in [S.steps_in(text or '')] if st), [])
            if not table_rows and (TABLE_TASK.match(qtext)
                                   or TABLE_TASK_INLINE.search(qtext)):
                # Refused only where the flat reading cannot stand in for the
                # table either. 2025 Ordinary's fill-in-the-blanks prints its
                # eight answers one to a line — "Discrimination = 2" — and
                # those are answers whatever the ask calls itself.
                claim = groups[0][0] if len(groups) == 1 else None
                if claim is None or len(options) < claim:
                    refuse('the ask is answered inside a printed table whose '
                           'other column the flat text layer interleaves',
                           qtext[:80])
                    continue
            if not table_rows and ticked:
                refuse('the scheme marks its answer with a tick in a printed '
                       'column the text layer cannot place',
                       ticked[0][:80])
                continue
            groups = sorted(set(part.tariffs))
            steps = next((st for text in [part.cue] + part.rows + part.cells
                          for st in [S.steps_in(text or '')] if st), [])
            if not table_rows and (TABLE_TASK.match(qtext)
                                   or TABLE_TASK_INLINE.search(qtext)):
                # Refused only where the flat reading cannot stand in for the
                # table either. 2025 Ordinary's fill-in-the-blanks prints its
                # eight answers one to a line — "Discrimination = 2" — and
                # those are answers whatever the ask calls itself.
                claim = groups[0][0] if len(groups) == 1 else None
                if claim is None or len(options) < claim:
                    refuse('the ask is answered inside a printed table whose '
                           'other column the flat text layer interleaves',
                           qtext[:80])
                    continue
            if not table_rows and ticked:
                refuse('the scheme marks its answer with a tick in a printed '
                       'column the text layer cannot place',
                       ticked[0][:80])
                continue
            stem = ''
            if BACK_REFERENCE.search(qtext):
                # "Suggest reasons for one of the training patterns identified
                # by you in question 11 (b) (i)" answers nothing on its own —
                # but the part it points back at is printed two lines above it
                # on the same page, and putting THAT ask on the card as its
                # stem is what the stem field is for. Refused only where the
                # paper prints no earlier ask under the same question to point
                # at, which would mean the reference leaves the question.
                stem = back_reference_stem(order, texts, labels, key)
                if not stem:
                    refuse("the ask's subject was chosen in a neighbouring "
                           'part the paper prints nothing for', qtext[:80])
                    continue
            topic = (topic_for(qtext)
                     or topic_for(' '.join(part.rows + part.answers)))
            if topic is None:
                refuse('no LCPE topic matches the wording', qtext[:80])
                continue

            pages = []
            # The stem counts too: a back-referencing ask carries the part it
            # points at, and that part is the one that names the figure.
            if NEEDS_SOURCE.search(f'{qtext} {stem}'):
                pages = source_pages(year, level, f'{qtext} {stem}')
                if not pages:
                    refuse('the ask depends on a figure, table or case study '
                           'this reader cannot find a page for', qtext[:80])
                    continue

            if table_rows:
                # The SEC answered this one inside its own table. Each printed
                # row is one marking point — the prompt it set and the answer
                # it wrote beside it, in the cells it put them in.
                prices = [m for _p, _a, m in table_rows]
                if any(m is None for m in prices):
                    per = groups[0][1] if len(groups) == 1 else None
                    # The per-answer value is the SEC's; the COUNT is the
                    # table's own number of rows. Taken only where the two
                    # agree with something else the SEC printed — the group's
                    # own claim, or the total on the question — because the
                    # converter truncates a wrapped ladder: 2025 Ordinary Q1
                    # prints "2 + 2 + 2 + 2" and the flat text keeps "2 + 2 +
                    # 2 +", three values for a four-row table.
                    checks = {part.total, part.qtotal, None}
                    # A ladder the converter cut off says so: it ends on a
                    # dangling "+". 2023 Ordinary Q12 prints "2 + 2 + 2 + 2"
                    # across a wrap and the flat text keeps "2 + 2 + 2 +",
                    # which is the SEC saying the list continues.
                    dangling = any(
                        re.search(r'(?:\d{1,2}\s*\+\s*){2,}(?!\d)', text or '')
                        for text in [part.cue] + part.rows + part.cells)
                    if per and (groups[0][0] == len(table_rows) or dangling
                                or per * len(table_rows) in checks):
                        prices = [per] * len(table_rows)
                    elif len(steps) == len(table_rows):
                        prices = list(steps)
                    else:
                        prices = None
                if not prices:
                    refuse('the scheme prints no tariff that reads one way for '
                           'the rows of its own table', f'{part.tariffs}')
                    continue
                rows = [point(f'r-{i + 1}', f'{prompt} — {answer}', marks, '')
                        for i, ((prompt, answer, _m), marks)
                        in enumerate(zip(table_rows, prices))]
                total = sum(prices)
                notation = ' + '.join(str(m) for m in prices) + ' marks'
                kind, answer, of_parts, per_part = 'fixed', None, None, None
                cid = card_id(year, level, part.address if len(keys) > 1 else key)
                if cid in seen_parts:
                    refuse('a second scheme part claims an id already written',
                           seen_parts[cid])
                    continue
                seen_parts[cid] = ref
                if pages:
                    bindings[cid] = {'kind': 'illustration', 'pages': pages}
                cards.append(card(
                    cid, year, lvl, topic, concept_for(topic, qtext), ref,
                    qtext, notation, total, rows, NOTES,
                    section=section_of(part.address[0], year), stem=stem,
                    tariff_kind=kind))
                covered.extend(keys)
                continue

            total = part.total
            if len(groups) == 1 and len(options) >= groups[0][0]:
                claim, per = groups[0]
                total = claim * per
                rows = [anyN('r-1', row_label(part, claim), total, claim, per,
                             options,
                             f'{claim} answer{"s" if claim > 1 else ""} at {per} '
                             f'mark{"s" if per > 1 else ""} each, as the scheme '
                             f'prices it.')]
                notation = f'{claim} x {per} marks'
                kind, answer, of_parts, per_part = ('bestNofParts', claim,
                                                    len(options), per)
            elif steps and len(options) >= len(steps):
                # A DESCENDING tariff: the SEC's own note says the first
                # correct answer is worth the first step and each later one
                # the next. It is not a best-of, so it rides perOptionSteps.
                claim = len(steps)
                total = sum(steps)
                rows = [anyN('r-1', row_label(part, claim), total, claim,
                             steps[0], options,
                             'The scheme pays '
                             + ' then '.join(f'{m}' for m in steps)
                             + ' marks, in the order the answers are credited.',
                             steps=steps)]
                notation = ' + '.join(str(m) for m in steps) + ' marks'
                kind, answer, of_parts, per_part = 'fixed', None, None, None
            elif total is not None and len(options) == 1 \
                    and single_tariff(part) == total:
                rows = [point('r-1', options[0], total, '')]
                notation = f'{total} marks'
                kind, answer, of_parts, per_part = 'fixed', None, None, None
            elif total is not None:
                # The scheme prices the PART and states its answers without
                # ever saying what each is worth — a shape `questionTotal`
                # exists for. What a student may claim is bounded by the
                # printed total, and no per-answer value is invented.
                rows = [point(f'r-{i + 1}', text, None, '')
                        for i, text in enumerate(options[:16])]
                notation = f'{total} marks'
                kind, answer, of_parts, per_part = ('questionTotal', None,
                                                    None, None)
            else:
                refuse('the scheme prints no tariff that reads one way',
                       f'{sorted(set(part.tariffs))}')
                continue

            cid = card_id(year, level, part.address if len(keys) > 1 else key)
            if cid in seen_parts:
                refuse('a second scheme part claims an id already written',
                       seen_parts[cid])
                continue
            seen_parts[cid] = ref
            built = card(
                cid, year, lvl, topic, concept_for(topic, qtext), ref, qtext,
                notation, total, rows, NOTES,
                section=section_of(part.address[0], year), stem=stem,
                tariff_kind=kind,
                answer=answer, of_parts=of_parts, per_part=per_part)
            if pages:
                bindings[cid] = {'kind': 'illustration', 'pages': pages}
            if kind == 'questionTotal':
                # The type is `{ kind: 'questionTotal' }` and nothing else: the
                # scheme states no split, so the card must not carry fields
                # that imply one.
                built['tariffModel'] = {'kind': 'questionTotal'}
            cards.append(built)
            covered.extend(keys)

    return cards, refusals, excluded, covered, bindings


def report():
    cards, refusals, excluded, covered, _bindings = build()
    problems = audit(cards)
    total = sum(len(L.leaves(y, lv)) for y, lv in L.SITTINGS)
    n_open = total - len(covered) - len(excluded)
    print(f'{len(covered)}/{total} leaf asks covered by {len(cards)} card(s); '
          f'{len(excluded)} excluded; {n_open} open')
    print('\nOPEN BUCKETS')
    for bucket, rows in sorted(refusals.items(), key=lambda kv: -len(kv[1])):
        print(f'  {len(rows):>4}  {bucket}')
        print(f'          e.g. {rows[0]}')
    if problems:
        print('\nAUDIT')
        for p in problems[:20]:
            print('  ', p)
    by_year = collections.Counter((c['year'], c['level']) for c in cards)
    print('\nCARDS BY SITTING')
    for k in sorted(by_year):
        print(f'  {k[0]} {k[1]:<9}{by_year[k]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.report:
        report()
        return
    cards, refusals, excluded, covered, bindings = build()
    problems = audit(cards)
    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    if args.write:
        if problems:
            raise SystemExit('refusing to write: the audit is not clean')
        with open(OUT, 'w', encoding='utf-8') as fh:
            json.dump(cards, fh, ensure_ascii=False, indent=1)
        os.makedirs(os.path.dirname(EXCLUSIONS), exist_ok=True)
        with open(EXCLUSIONS, 'w', encoding='utf-8') as fh:
            json.dump(excluded, fh, ensure_ascii=False, indent=1)
        # The bindings file is SHARED with eight other subjects, so only this
        # subject's key is replaced — and at the TWO-SPACE indent the file is
        # already written in. Writing it at indent=1 reformatted all 4,120
        # lines of it and buried the one subject that had actually changed,
        # which is the same mistake reconcile.py's baseline writer records.
        book = json.load(open(BINDINGS, encoding='utf-8'))
        book['physical-education'] = bindings
        with open(BINDINGS, 'w', encoding='utf-8') as fh:
            json.dump({k: book[k] for k in sorted(book)}, fh,
                      ensure_ascii=False, indent=2)
            fh.write('\n')
        print(f'wrote {len(cards)} card(s), {len(excluded)} exclusion(s) and '
              f'{len(bindings)} source binding(s)')
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
