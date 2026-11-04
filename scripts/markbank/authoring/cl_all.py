#!/usr/bin/env python3
"""Author every Classical Studies ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/cl_all.py --report
    python3 scripts/markbank/authoring/cl_all.py > scripts/markbank/authored/classical-studies.json
    python3 scripts/markbank/authoring/cl_all.py --exclusions   # rewrite the ledger

Census-driven: this walks the 640 leaf asks `paper_census.py classical-studies`
reads off the ten papers, and decides each one against the scheme rather than
choosing what to card.

WHY THIS SUBJECT IS IN THE BANK AT ALL
--------------------------------------
It was recorded as REJECTED, on the note "Very Thorough 16-20, Thorough 10-15,
Basic 5-9". Those bands are real, and they are the RESEARCH STUDY REPORT grid —
the coursework rubric printed on pages 3 to 5 of every Classical Studies scheme,
in front of the written paper's own marking scheme and about a document that is
not the written paper at all. Re-measured against the paper:

    640 leaf asks on the papers; 586 of them priced by the schemes;
    547 of those 586 answered with stated content, 39 with a band alone.

The 54 unpriced asks are Section B's essays, which one common grid marks. See
`cl_scheme.py` for the rule that separates a stated answer from a band, and
`--report` for the counts as built: 516 cards covering 525 printed asks, and
115 exclusions each carrying the printed line it was refused on.

WHAT IS CARDED, AND WHAT IS EXCLUDED
------------------------------------
*Carded.* Every ask whose own scheme entry states content — which is nearly all
of Section A on the new paper and nearly all of both levels' topic parts on the
old one. The old scheme answers a 35-mark part with the examiner's own model
answer in prose; the new one answers a Section A part with a key ("1 mark each:
1: frieze, 2: capital; 3: caryatid"), a menu ("Examples: libations, lock of
hair, ointment flasks, lekythoi…"), or an Indicative Material list.

*Excluded, with the scheme's own printed line as evidence.* Two families:

  * **the extended answers** — Question 11(b) and Questions 12-16 on the
    2023-2025 paper. The scheme prices all six with ONE grid: "Development of
    material required to fully answer the question (60 marks)", "15 marks per
    unit of development", "18-20: High Quality". There is no content under it
    to lift, in any sitting.
  * **band-only Section A parts** — an ask the scheme prices with a ladder and
    nothing else, e.g. 2024 Ordinary Q5(a) "10 marks, banded: 1-5: very basic/
    basic (general); 6-10: partial/full (specific details)."

THE TARIFF
----------
The PAPER's printed tariff, always — it is the number the candidate saw. Where
the scheme's own differs (seven parts across 2021 and 2022; see
`_CLAS_TARIFF_SPLITS` in paper_census.py) the difference is the SEC's, is
recorded there with its diagnosis, and the card carries the paper's. Where the
paper prices only the QUESTION and leaves the split to the scheme — every
Section A part of the new paper — the card carries the SCHEME's printed part
tariff. Nothing is averaged and nothing is inferred: an ask neither document
prices is refused.

THE SOURCE ON THE CARD
----------------------
A Classical Studies question is usually about something printed: a photograph or
image on the accompanying **Paper X**, or a passage set in the question booklet
itself. An answer that cannot be reached from what the card shows must not ship,
so both are bound as official SEC source material and opened before the reveal:

  * Paper X as a `source-illustration`, at the pages that booklet itself heads
    with the photograph letter (2021-2022) or the question number (2023-2025) —
    read off the booklet by `ClPaper.figure_pages`, never guessed;
  * the printed passage as a `source-text`, at the question booklet's own page.

An ask that names an image whose Paper X page cannot be resolved is REFUSED, not
shipped without it.
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

from cl_paper import ClPaper, TOPIC_ERA                       # noqa: E402
from cl_scheme import (ClScheme, BAND, KEYLIKE, SEAM,         # noqa: E402
                       SHAPE_WORDS)
from cl_topics import legacy_topic, current_topic             # noqa: E402
from hist_topics import concept_for                           # noqa: E402

YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'classical-studies.json')

# The scheme's own words for "this list is not exhaustive", which is what
# `openList` on a row means and what turns on the session's "I wrote a
# different valid point".
OPEN_LIST = re.compile(
    r'\bIndicative (?:Material|Answers?|points?)\b|\bExamples?\s*:'
    r'|\bmay include\b|\bcould include\b|\bsuch as\b|\betc\.', re.I)

# A line that is the SEC talking to the examiner about arithmetic rather than
# about the answer. Stripped from the head of a marking point, which leaves a
# substring of the SEC's own line, so the provenance gate still finds it.
ALLOCATION = re.compile(
    r'^(?:\(?\d{1,3}\s*(?:x|×)?\s*\d{0,3}\s*marks?\)?'
    r'(?:\s*(?:each|for each|per|in any order|banded))?'
    r'|Indicative (?:Material|Answers?|points?)'
    r'|Examples?|Accept(?:able)?|Award)\s*[:,.–-]*\s*', re.I)

# A marking point must not BE a tariff — build-deck refuses one that is, and it
# is right to: a student reading "2 marks each" on the back of a card has
# learned nothing.
TARIFF_PROSE = re.compile(r'\bmarks? (?:for )?each\b'
                          r'|\b\d{1,2}\s*(?:x|\u00d7)\s*\d{1,2}\s*marks?\b'
                          r'|^\s*any (?:one|two|three|four|five|\d+)\b[^.]*'
                          r'\bmarks?\b', re.I)

# The scheme's REQUIREMENT sentence, in the old paper's own words: "A coherent
# account of the battle.", "A clear evaluation, showing understanding of…",
# "A brief explanation of one term's contribution." It names the shape of the
# answer and nothing in it, and it is not a marking point — 48 of them shipped
# as the first row of a card, telling the student to give a coherent account of
# the thing they had just failed to recall. Recognised by its opening, which is
# an article and a shape noun; a sentence that names something ("The Corinthian
# architectural order.") never matches.
REQUIREMENT_SENTENCE = re.compile(
    r'^(?:A|An)\s+(?:\w+\s+)?(?:account|description|explanation|evaluation'
    r'|discussion|analysis|examination|comment|opinion|response|answer'
    r'|reference|summary)\b'
    # …and the SEC addressing the examiner directly about what a candidate is
    # allowed to do: "Can choose any one device from part (a) or (b) and
    # explain how it contributes to Homer's/Virgil's storytelling."
    r'|^(?:Can|May|Must|Award|Accept|Candidates?\s+(?:may|can|must|should|will)'
    r'|Answers?\s+(?:may|can|must|should))\b', re.I)

# The scheme saying only that the answer must be VALID — "Any valid military
# event named", "any valid facts about Zeus", "A clear, accurate description of
# either text in their own words". It names no event, no fact and no text, and
# a card whose whole back reads like that has taught nothing. Never applied
# where a colon follows: the SEC writes "Any valid point: goddess of the
# hearth, goddess of the eternal flame of Rome", and everything after the colon
# is the answer.
VALIDITY_ONLY = re.compile(r'^(?:Any|One|Two|Three|Four|Five|A|An)\b[^:]*$',
                           re.I)
# "Three points of comparison", "Two points substantiated by references to the
# text" — the SEC counting what it will pay for, with nothing counted.
COUNT_ONLY = re.compile(
    r'^(?:One|Two|Three|Four|Five|Six)\s+(?:points?|reasons?|qualities|'
    r'examples?|comments?|views?|effects?|ways?|aspects?|features?|'
    r'identifications?|differences?|similarities)\b[^:]*$', re.I)
VALIDITY_CUE = re.compile(r'\bvalid\b|\baccurate\b|\bclear\b|\bcoherent\b'
                          r'|\bdetailed\b|\bbrief\b', re.I)

# Where a card must show the printed source to be answerable.
# "Photograph J", and also "Photographs F and G", "Images K and L", "Image A,
# Image B or Image C" — the paper names them singly and in runs, and a rule
# that read only the singular left five cards without the booklet their own
# question is about.
IMAGE_CUE = re.compile(
    r'\b(?:Images?|Photographs?)\s+([A-Z]\b(?:\s*(?:,|and|or)\s*[A-Z]\b)*)')
PASSAGE_CUE = re.compile(
    r'\b(?:Text|Extract)\s+[A-Z]\b|\bthis extract\b|\bthe extract\b'
    r'|\bthe passage\b|\bthese (?:opening )?lines\b|\bthis passage\b'
    r'|\bRead (?:the|this|Text|Extract)\b|\bthis poem\b|\babove quote\b'
    r'|\bthe above\b|\bthis statement\b|\bthis quote\b', re.I)

# The display ceiling a card's marking rows may not pass. Mirrors
# MAX_LONG_OPTION_ROWS in optionCap.mjs, which is the largest verified SEC
# menu; a card past it is a wall of text rather than a flashcard.
MAX_ROWS = 16

SENTENCE = re.compile(r'(?<=[.;:!?])\s+(?=[A-Z“‘(])')


def card_id(year, level, key):
    section, q, letter, roman = key
    bits = ['clas', str(year), level]
    if section and str(section).startswith('Topic '):
        m = re.match(r'Topic (\d{1,2})\((i{1,3}|iv|v)\)', str(section))
        bits.append(f't{m.group(1)}{m.group(2)}')
    if q is not None:
        bits.append(f'q{q}')
    tail = (letter or '') + (roman or '')
    if tail:
        if len(bits) == 3:
            bits.append(tail)
        else:
            bits[-1] += tail
    return '-'.join(bits)


def question_ref(year, level, key):
    """The paper's own address, opened by the sitting.

    Mirrors `key_label` in paper_census.py exactly — reconcile matches a card
    to a census leaf through this string, and the two drifting apart is how a
    correct card becomes an orphan.
    """
    section, q, letter, roman = key
    ref = f'{year} {level.upper()}'
    if section is not None:
        ref += (f' {section}' if str(section).startswith('Topic ')
                else f' Section {section}')
    if q is None and letter is None and roman is None and section is not None:
        return ref
    ref += ' Q' + ('' if q is None else str(q))
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


def scheme_entry(scheme, key, paper_keys):
    """The scheme entry that prices this printed ask.

    Three readings, in order, and each is the scheme pricing something the
    paper prints rather than a fallback onto whatever is nearby:

      1. the ask's own address;
      2. the LETTER above it, where the paper prints romans under a letter the
         scheme priced whole — 2023 Ordinary Q4(a)(i) and (ii) share one
         "(a) 8 marks" entry;
      3. the QUESTION above it, where the paper prints alternatives the scheme
         priced whole — 2025 Higher Q7 is priced once over its (a) and (b).
    """
    if key in scheme:
        return scheme[key], 'exact'
    letter_key = (key[0], key[1], key[2], None)
    if key[2] is not None and letter_key in scheme:
        return scheme[letter_key], 'letter'
    q_key = (key[0], key[1], None, None)
    if q_key in scheme and not any(
            k[:2] == key[:2] and k[2] is not None for k in scheme):
        return scheme[q_key], 'question'
    return None, None


def marking_points(entry):
    """The scheme's stated content, cut into marking points.

    Two printings, both the SEC's own division of its own answer:

      * a LIST — the old scheme's "Any two of the above", the new scheme's
        Indicative Material bullets and its keys — one point per printed item;
      * a MODEL ANSWER — the old scheme's prose paragraph — one point per
        sentence, which is where the examiner's own full stops fall.

    Nothing is rewritten: every point is a contiguous run of the scheme's own
    characters, which is what the provenance gate checks and the only reason it
    can check anything.
    """
    lines = [l for l in entry.stated_lines if not BAND.search(l)]
    # A line whose tail is the SEC's own pricing — the note that closes an old
    # scheme's answer, and, in a merged "write notes" entry, the same closing
    # line under each of its three options — has that pricing taken off. It is
    # NOT dropped: 2022 Ordinary Topic 10(i)(b) prints the answer and the
    # pricing on one line, "The Corinthian architectural order. One point.
    # (10.) (10 marks)", and dropping the line lost the answer with it.
    lines = [_strip_requirement(l) if _is_priced_tail(l) else l for l in lines]
    lines = [l for l in lines if l.strip()]
    if not lines:
        return []
    # A marking point never runs across the SEAM between two answers the
    # scheme printed at ONE address — the three options of a "write notes on
    # any two of the following" question. Joined across it, a point read
    # "…negotiated the Peace of Nicias Demosthenes: Athenian general", which is
    # two answers welded together and is in no scheme.
    chunks, cur = [], []
    for line in lines:
        if line.strip() == SEAM:
            chunks.append(_points_of(cur))
            cur = []
        else:
            cur.append(line)
    chunks.append(_points_of(cur))
    return [c for c in chunks if c]


# The marks COLUMN, as the converter rejoins it: a bare mark at the END of a
# printed line, which is a table cell rather than a word of the answer. Left in
# place it lands in the middle of the joined sentence — "professional, well- 5
# trained, well-supplied" — because the answer wraps and the cell does not.
COLUMN_CELL = re.compile(r'(?<=[A-Za-z,;:).!\u2019-])\s+(?:[1-9]|[12]\d|30)\s*$')


def _drop_column_cell(line):
    return COLUMN_CELL.sub('', line.rstrip())


def _join_lines(lines):
    """The printed lines as one run, with the SEC's own hyphenation closed.

    A word broken across a printed line — "well-" then "trained" — is one word,
    and joining on a space made the card read "well- trained". The comparison
    text the provenance gate builds strips punctuation and spacing from both
    sides, so closing the break changes nothing it can see.
    """
    out = ''
    for line in lines:
        piece = line.strip()
        if out.endswith('-') and piece[:1].islower():
            out += piece
        elif out:
            out += ' ' + piece
        else:
            out = piece
    return out


def _points_of(lines):
    lines = [_drop_column_cell(l) for l in lines if l.strip()]
    lines = [l for l in lines if l.strip()]
    if not lines:
        return []
    # A printed LIST: the scheme's Indicative Material bullets, and the
    # numbered answer key a table question is answered with — "1: Caduceus,
    # winged sandals; travellers, merchants, psychopomp, etc.", one line per
    # god. Cut at the marker the examiner printed, not at the punctuation
    # inside an item, which split one god's symbols from his domains.
    marker = re.compile(r'^\s*(?:[-•\u2013]\s+|\d{1,2}\s*[:.]\s+)')
    bullets = [l for l in lines if marker.match(l)]
    if len(bullets) >= 2:
        points, cur = [], None
        for line in lines:
            if marker.match(line):
                if cur:
                    points.append(cur)
                cur = marker.sub('', line).strip()
            elif cur is not None:
                cur += ' ' + line.strip()
            elif _has_content(line) and not line.rstrip().endswith(':'):
                # A line ending in a colon introduces the list — "3 sets of
                # symbols and 3 domains:" — and is a heading, not an answer.
                points.append(line.strip())
        if cur:
            points.append(cur)
        return [p for p in points if p]
    text = _join_lines(lines)
    # The lone bullet the new scheme sets its Indicative Material on. Left in
    # place it blocks the allocation strip, and the card's marking point then
    # opened "• Indicative Material:" — the examiner's filing label, printed
    # where the answer belongs.
    text = re.sub(r'^\s*[-•–]\s*', '', text)
    text = ALLOCATION.sub('', text).strip()
    if not text:
        return []
    # Cut at a full stop the examiner wrote, and also in front of the marks
    # the examiner printed INSIDE a wrapped answer — "…hills. 2 marks. *Award
    # 1 mark for valid but not exact…". Quoting across that tariff is what a
    # card must never do, because the scheme does not read that way; stopping
    # at it leaves both halves quotable.
    # Never cut inside a dated abbreviation. "In 26 A.D. Agrippina requested
    # Tiberius…" splits after "A." on a naive rule, which leaves "In 26 A." —
    # a fragment with no content, dropped — and "D. Agrippina requested…", and
    # the sentence between them disappears from the card.
    points = [p.strip() for p in
              re.split(r'(?<![A-Z]\.)(?<=[.!?])\s+(?=[A-Z“(*•\u2013-])', text)]
    points = [p.rstrip() for p in points if len(p.strip()) > 3]
    # A MENU the examiner set out with semicolons — "enjoyable/ captivating –
    # staging, actors, storyline; communal/ thought-provoking – catharsis" — is
    # a list of separate acceptable answers printed on one line, and shown as
    # one row it is a paragraph the student cannot tick against. Cut at the
    # examiner's own semicolons, which leaves every row a contiguous run of the
    # scheme's own characters.
    # …but a short one is an answer KEY, not a menu: "True; True; False." is
    # three ticks in the order the paper prints its three statements, and cut
    # into three rows it reads as three unattached words.
    if len(points) == 1 and points[0].count(';') >= 2 and len(points[0]) > 60:
        points = [p.strip(' ;') for p in points[0].split(';')]
        points = [p for p in points if len(p) > 3]
    return points


def _is_priced_tail(line):
    """Does this printed line END in the scheme's own pricing?

    Both spellings: bracketed, "(35 marks)", and bare, "6 x 1 mark." — the
    second is how the new scheme prices a table of answers, and reading only
    the first left "3 sets of symbols and 3 domains: 6 x 1 mark." standing at
    the head of a card's first marking point.
    """
    text = line.strip()
    return bool(re.search(r'\(\s*\d{1,3}\s*marks?\s*\)?\s*$', text, re.I)
                or re.search(r'\b\d{1,3}\s*(?:x|\u00d7)\s*\d{1,3}\s*marks?\.?\s*$',
                             text, re.I))


def _strip_requirement(line):
    """One printed line with its pricing instruction taken off the end.

    The instruction is the scheme's LAST sentence before the tariff and it says
    only how much and how well — "One point.", "Two developed points.",
    "Engagement, 14; Development, 14; Overall evaluation, 7." Recognised by
    having no content word left once the vocabulary of shape is removed, which
    is the same test `cl_scheme.Entry.content_words` uses, so the two cannot
    disagree about what a content word is.
    """
    text = re.sub(r'\(\s*[\d,;\s.]*\)\s*$', '', line.strip()).strip()
    text = re.sub(r'\(\s*\d{1,3}\s*marks?\s*\)?\s*$', '', text,
                  flags=re.I).strip()
    text = re.sub(r'\(\s*[\d,;\s.]*\)\s*$', '', text).strip()
    parts = re.split(r'(?<![A-Z]\.)(?<=[.!?])\s+', text)
    while parts and (not _has_content(parts[-1])
                     or REQUIREMENT_SENTENCE.match(parts[-1])):
        parts.pop()
    return ' '.join(parts).strip()


def _has_content(sentence):
    stripped = re.sub(r'\(?\b\d{1,3}\s*(?:x|×)?\s*\d{0,3}\s*marks?\b\)?', ' ',
                      sentence, flags=re.I)
    # An answer KEY is content with no words in it — 2025 Higher Q2(b) answers
    # a matching table with "1 mark each: 2, 4, 1, 3." and nothing else, and a
    # word test alone threw that answer away.
    if KEYLIKE.search(stripped):
        return True
    bare = re.sub(r"[^A-Za-z’' ]+", ' ', stripped)
    return any(len(w) > 2 and w.lower() not in SHAPE_WORDS for w in bare.split())


def regroup_chunks(chunks, cap):
    """Every chunk cut down until they fit the cap together.

    The cap is shared out in proportion to how much each chunk holds, and
    never below one row per chunk: joining ACROSS a chunk boundary would weld
    two different answers into one marking point, which is the fault the seam
    exists to prevent and which dropped six Ordinary cards.
    """
    total = sum(len(c) for c in chunks)
    if total <= cap:
        return [p for c in chunks for p in c]
    caps = [max(1, (cap * len(c)) // total) for c in chunks]
    while sum(caps) > cap and max(caps) > 1:
        caps[caps.index(max(caps))] -= 1
    return [p for c, k in zip(chunks, caps) for p in regroup(c, k)]


def regroup(points, cap):
    """The same text, cut into at most `cap` contiguous runs.

    The old scheme answers a 35-mark part with a paragraph the examiner wrote,
    and cutting it at every full stop can produce more marking rows than a card
    may show (rowCapFor, types/markBank.ts). Nothing is dropped and nothing is
    rewritten: adjacent sentences are JOINED, so every row is still one
    contiguous run of the scheme's own characters — which is what the
    provenance gate reads and the only reason it can read anything.
    """
    if len(points) <= cap:
        return points
    per = -(-len(points) // cap)
    return [' '.join(points[i:i + per]) for i in range(0, len(points), per)]


def clean_point(text):
    """A marking point with the SEC's arithmetic taken off its head and tail.

    Both ends only, and only the arithmetic: what remains is a contiguous run
    of the scheme's own characters, so the provenance gate still finds it.
    """
    # The scheme's own part marker, printed in front of the answer it belongs
    # to when one entry answers several parts: "(ii) any valid point: …".
    out = re.sub(r'^\(\s*(?:i{1,3}|iv|v|[a-f])\s*\)\s*', '', text.strip())
    out = ALLOCATION.sub('', out).strip()
    out = re.sub(r'\s*\(?\b\d{1,3}\s*(?:x|×)?\s*\d{0,3}\s*marks?\b'
                 r'(?:\s*each)?\)?[.,]?\s*$', '', out, flags=re.I).strip()
    out = re.sub(r'\s*\([\d,;\s.]+\)\s*$', '', out).strip()
    # The marks COLUMN, which the converter rejoined onto the end of whichever
    # printed line its cell lined up with. It is a tariff, not a word of the
    # answer, and left on it read "…near Colosseum / forum 2".
    out = re.sub(r'(?<=[a-z.,;)\u2019])\s+\d{1,3}\s*$', '', out).strip()
    return out.strip(' .;,')


def source_materials(P, ask, fig_pages, year, level):
    """The official documents this ask cannot be answered without."""
    text = f'{ask.stem} {ask.text}'
    out = []
    letters = sorted({L for run in IMAGE_CUE.findall(text)
                      for L in re.findall(r'\b([A-Z])\b', run)})
    if letters or (P.era == 'sections'
                   and re.search(r'\bImage\b', text, re.I)):
        if P.era == 'topics':
            pages = sorted({p for L in letters for p in fig_pages.get(L, [])})
            label = 'PAPER X — ' + ', '.join(f'Photograph {L}' for L in letters)
        else:
            pages = sorted(fig_pages.get(str(ask.q), []))
            label = f'PAPER X — Question {ask.q}'
        if not pages:
            return None, 'the illustration booklet page for this image is not resolvable'
        out.append({
            'kind': 'source-illustration',
            'label': label[:120],
            'title': 'Paper X — the printed images',
            'pages': pages,
            'sourceLabel': 'Picture/Illustration',
            'attribution': (f'SEC Classical Studies {year} {LEVEL_TITLE[level]} '
                            'Level Paper X — © State Examinations Commission.'),
            'presentationNote': ('The accompanying illustration booklet, exactly '
                                 'as it was printed for the examination.'),
        })
    if PASSAGE_CUE.search(text):
        out.append({
            'kind': 'source-text',
            'label': 'OFFICIAL EXTRACT',
            'title': 'The printed passage',
            'pages': [ask.page],
            'attribution': (f'SEC Classical Studies {year} {LEVEL_TITLE[level]} '
                            'Level examination paper — © State Examinations '
                            'Commission.'),
            'presentationNote': ('Read the exact source as it appeared in the '
                                 'examination paper, then answer the question '
                                 'above.'),
        })
    return out, None


def build():
    cards, exclusions = [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    stats = collections.Counter()
    joins = {'exact': 0, 'letter': 0, 'question': 0}

    def refuse(reason, ref, n=1):
        refused[reason] += n
        examples[reason].append(ref)

    for year in YEARS:
        for level in LEVELS:
            P = ClPaper(year, level)
            S = ClScheme(year, level)
            scheme = S.by_key()
            fig_pages = P.figure_pages()
            paper_keys = {a.key for a in P.asks()}
            # One card per PRICED ASK, which is not always one card per
            # printed ask. Where the scheme prices a LETTER whole and the
            # paper prints romans under it — 2025 Higher Q1(a) is one
            # true/false key answered "true, false, false" over three printed
            # statements — a card per roman would put the whole key on the
            # back of each, three times, and tell a student that the answer to
            # (ii) is all three values. The card is made at the address the
            # SCHEME priced, and covers every printed ask under it.
            grouped = collections.OrderedDict()
            for ask in sorted(P.asks(), key=lambda a: tuple(str(x)
                                                            for x in a.key)):
                entry, how = scheme_entry(scheme, ask.key, paper_keys)
                at = ask.key if entry is None else entry.key
                grouped.setdefault(at, {'asks': [], 'entry': entry,
                                        'how': how})['asks'].append(ask)
            for at, group in grouped.items():
                asks, entry, how = group['asks'], group['entry'], group['how']
                ask = asks[0]
                key = at
                ref = question_ref(year, level, key)
                if entry is None:
                    # One entry per PRINTED ask, not per group: an exclusion
                    # reconciles by citation, and a sibling left uncited stays
                    # open forever.
                    for a in asks:
                        exclusions.append({
                            'ref': question_ref(year, level, a.key),
                            'reason': ('the scheme prices this ask with the '
                                       'common extended-answer grid and states '
                                       'no answer content for it'),
                            'schemeEvidence': _grid_evidence(S),
                        })
                        stats['excluded-grid'] += 1
                    continue
                joins[how] += len(asks)
                if not entry.states_content:
                    for a in asks:
                        exclusions.append({
                            'ref': question_ref(year, level, a.key),
                            'reason': ('the scheme prices this ask with a band '
                                       'ladder and states no answer content'),
                            'schemeEvidence': ' | '.join(entry.lines)[:400],
                        })
                        stats['excluded-band'] += 1
                    continue

                joined_text = _joined_question(asks)
                topic_id = (legacy_topic(int(re.match(
                    r'Topic (\d{1,2})', str(key[0])).group(1)))
                    if year in TOPIC_ERA
                    else current_topic(f'{ask.stem} {joined_text}'))
                if not topic_id:
                    refuse('the ask names no part of the course', ref,
                           len(asks))
                    continue

                total = ask.marks or entry.marks
                if not total and how == 'question':
                    # The scheme priced the QUESTION whole because its parts
                    # are alternatives a candidate chooses between — 2025
                    # Higher Q7 sets "Answer (a) or (b)" — so the question's
                    # own printed tariff IS this part's price. Read off the
                    # paper's head, not inferred: `question_marks` is the
                    # number the candidate saw.
                    total = P.question_marks.get((None, ask.q))
                if not total:
                    refuse('neither document prints a tariff for this ask',
                           ref, len(asks))
                    continue
                # The paper prices the QUESTION on the new paper and the scheme
                # prices its parts; where the paper's number is the letter's
                # ceiling rather than this ask's own price, the scheme's is the
                # ask's price.
                if ask.inherited and entry.marks and how == 'exact':
                    total = entry.marks
                if ask.marks is None and entry.marks:
                    total = entry.marks

                # The tariff test runs on the PRINTED point, before the
                # arithmetic is taken off it: "(i) Explanation of any two
                # features, 1-4 marks each." is a tariff, and cleaning it
                # first left "(i) Explanation of any two features, 1-" —
                # which is no longer recognisable as one, and shipped.
                chunks = [[clean_point(p) for p in chunk
                           if not TARIFF_PROSE.search(p)
                           and not REQUIREMENT_SENTENCE.match(p)
                           and not (VALIDITY_ONLY.match(p)
                                    and VALIDITY_CUE.search(p))
                           and not COUNT_ONLY.match(p)
                           and not p.rstrip().endswith(':')]
                          for chunk in marking_points(entry)]
                chunks = [[p for p in chunk if p] for chunk in chunks]
                chunks = [c for c in chunks if c]
                points = [p for c in chunks for p in c]
                points = [p for p in points if _has_content(p)]
                chunks = [[p for p in c if _has_content(p)] for c in chunks]
                chunks = [c for c in chunks if c]
                if not points:
                    # Nothing survived the strip, which means the scheme's
                    # entry was its arithmetic and its ladder and nothing else
                    # — 2025 Higher Q10(b) prices "Any four architectural
                    # features named and described (18 marks: 5,5,4,4, in any
                    # order)" and never says which four. That is an exclusion
                    # with the printed evidence, not a refusal to be counted
                    # against coverage: there is no answer to lift.
                    for a in asks:
                        exclusions.append({
                            'ref': question_ref(year, level, a.key),
                            'reason': ('the scheme prices this ask with its '
                                       'mark allocation alone and states no '
                                       'answer content'),
                            'schemeEvidence': ' | '.join(entry.lines)[:400],
                        })
                        stats['excluded-band'] += 1
                    continue
                points = regroup_chunks(chunks, MAX_ROWS)

                sources, source_fault = source_materials(
                    P, ask, fig_pages, year, level)
                if source_fault:
                    refuse(source_fault, ref, len(asks))
                    continue

                open_list = bool(OPEN_LIST.search(' '.join(entry.lines)))
                single = len(points) == 1
                rows = []
                for i, point in enumerate(points, start=1):
                    row = {'id': f'r-{i}', 'kind': 'point', 'verbatim': point,
                           'marks': total if single else None}
                    if open_list and not single:
                        row['openList'] = True
                    rows.append(row)

                card = {
                    'id': card_id(year, level, key),
                    'subjectId': 'classical-studies',
                    'level': LEVEL_WORD[level],
                    'year': year,
                    'section': _section_of(key, year),
                    'topicId': topic_id,
                    # Level-independent identity, derived from the ask's own
                    # words so a Higher card and the Ordinary card asking the
                    # same thing share it. That is what keeps a student's work
                    # when they drop level in spring.
                    'conceptId': concept_for(joined_text),
                    'questionRef': ref,
                    'questionText': joined_text,
                    'tariffModel': ({'kind': 'fixed'} if single
                                    else {'kind': 'questionTotal'}),
                    'totalMarks': total,
                    'rows': rows,
                    'notes': _note(entry, ask if len(asks) == 1 else None),
                }
                stem = min((a.stem for a in asks if a.stem), key=len,
                           default='')
                if stem and len(stem) >= 20:
                    card['stem'] = stem[:600]
                if sources:
                    card['sourceMaterial'] = sources[0]
                    if len(sources) > 1:
                        card['additionalSourceMaterials'] = sources[1:]
                card['coversAsks'] = len(asks)
                cards.append(card)
                stats['carded'] += 1
    return cards, exclusions, refused, examples, stats, joins


def _joined_question(asks):
    """The printed ask, or every printed ask the one scheme entry answers.

    Where a card covers several printed parts the question text carries them
    all, each behind the marker the paper printed it under, so the student sees
    the whole of what the SEC priced together.
    """
    if len(asks) == 1:
        return asks[0].text
    out = []
    for ask in asks:
        marker = ''.join(f'({x})' for x in (ask.letter, ask.roman) if x)
        out.append(f'{marker} {ask.text}'.strip())
    return ' '.join(out)


def _section_of(key, year):
    """The paper's own section, as the card model records it."""
    if year in TOPIC_ERA:
        return str(key[0])
    return 'A' if (key[1] or 0) <= 10 else 'B'


def _note(entry, ask=None):
    """The scheme's own pricing line, verbatim, and the paper's if it differs.

    The partial-credit ladder rides here rather than becoming a row: it is the
    SEC's instruction to the examiner about how much of the answer earns what,
    and there is no RowKind for it.
    """
    bits = []
    # Only where the note is the SEC's own PRICING line. On some asks the
    # scheme's opening line is the answer itself — "Anchises – father of
    # Aeneas;" — and quoting that as "the scheme prints…" said nothing the
    # card's own rows do not already say.
    note = entry.note.strip()
    if note and re.search(r'\bmarks?\b|\bbanded\b', note, re.I):
        bits.append(f'The scheme prints {note!r} for this ask.')
    ladder = [l.strip() for l in entry.lines if BAND.search(l)]
    if ladder:
        bits.append('Partial credit: ' + ' '.join(ladder)[:400])
    if ask and ask.marks and entry.marks and ask.marks != entry.marks:
        bits.append(f'The paper prints {ask.marks} marks for this part and the '
                    f'scheme prints {entry.marks}; the card carries the '
                    f"paper's.")
    return ' '.join(bits)[:900]


def _grid_evidence(S):
    """The common essay grid, quoted from this scheme's own page."""
    text = S.text
    m = re.search(r'(Question 11 ?\(b\).{0,4000}?|Questions? 12\s*[-–]\s*16.{0,4000}?)'
                  r'Overall Quality.{0,300}', text, re.S | re.I)
    if m:
        return ' '.join(m.group(0).split())[:600]
    m = re.search(r'Development of [Mm]aterial.{0,600}', text, re.S)
    return ' '.join(m.group(0).split())[:600] if m else \
        'the scheme prints one common grid for Question 11(b) and Questions 12-16'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, exclusions, refused, examples, stats, joins = build()

    if args.exclusions:
        os.makedirs(os.path.dirname(EXCLUSIONS), exist_ok=True)
        with open(EXCLUSIONS, 'w', encoding='utf-8') as fh:
            json.dump(exclusions, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'{len(exclusions)} exclusion(s) written to {EXCLUSIONS}',
              file=sys.stderr)
        return 0

    if args.report:
        from paper_census import census_subject
        census = census_subject('classical-studies')
        total = sum(p['leafCount'] for p in census['papers'])
        # A card may cover SEVERAL printed asks, so coverage counts asks.
        accounted = sum(c.pop('coversAsks', 1) for c in cards) + len(exclusions)
        print(f'{len(cards)} card(s) + {len(exclusions)} exclusion(s) = '
              f'{accounted} of {total} paper asks '
              f'({100 * accounted / total:.1f}%)')
        rows = sum(len(c['rows']) for c in cards)
        fixed = sum(1 for c in cards if c['tariffModel']['kind'] == 'fixed')
        print(f'{rows} marking rows; {fixed} fixed-tariff card(s), '
              f'{len(cards) - fixed} questionTotal')
        print(f'paper/scheme join: {joins["exact"]} at the ask\'s own address, '
              f'{joins["letter"]} through the letter the scheme priced whole, '
              f'{joins["question"]} through the question')
        srcs = sum(1 for c in cards if c.get('sourceMaterial'))
        illus = sum(1 for c in cards
                    if (c.get('sourceMaterial') or {}).get('kind')
                    == 'source-illustration')
        print(f'{srcs} card(s) carry official source material '
              f'({illus} open Paper X)')
        by_year = collections.Counter((c['year'], c['level']) for c in cards)
        for k, n in sorted(by_year.items()):
            print(f'   {k[0]} {k[1]:9} {n}')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:24} {n}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:200 if args.all else 3]:
                print(f'             {e}')
        return 0

    for card in cards:
        card.pop('coversAsks', None)     # a build-time count, not a card field
    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
