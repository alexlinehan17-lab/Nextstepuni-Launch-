#!/usr/bin/env python3
"""Author every Latin ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/lat_all.py --report
    python3 scripts/markbank/authoring/lat_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/lat_all.py > scripts/markbank/authored/latin.json

Census-driven: this walks the 328 leaf asks `paper_census.py latin` reads off
the eight papers and decides each one against the scheme, rather than choosing
what to card.

WHAT IS CARDED
--------------
*Comprehension* — Question 1 Section B. The scheme states the answers and
prices them phrase by phrase ("A maiden (3) and one of the hostages (3)"), so
the phrases are the rows and their printed marks are the rows' marks. The
Latin passage, its English summary and the SEC's own vocabulary list travel
with every one of these cards: the ask cannot be answered without them.

*Prescribed text and Roman civilisation* — Question 3's second part and
Question 5. The scheme prints a tariff and then, under "Indicative Notes—
Candidates may make valid points other than those listed below", the SEC's own
content. The tariff is an ordered split the card cannot give to individual
rows ("Three points (7 + 6 + 6); treatment of Tiberius — one good point 6
marks"), so it rides verbatim as the card's `orderedSplit` notation and the
rows carry the content with no marks of their own. Every list is open: the
scheme says so itself.

*Grammar* — Question 4(i) at Higher from 2023, where the scheme prints the
answers: "patriae=dative meaning 'for'; defendi=pres infin passive after
possent". The paper prints the Latin lines the ask is about, so they ride in
the question text.

WHAT IS EXCLUDED, AND ON WHAT EVIDENCE
--------------------------------------
*Every translation ask* — Question 1 Section A, all of Question 2, and the
first part of Question 3. That is 113 of the 328, and it is the whole reason
Latin is not the Applied Maths case. The scheme prices translation by segment,
but the segments are the SOURCE and not a model answer: it prints the LATIN cut
into units with a mark after each ("reportatur Segestam;/2"), or the ENGLISH of
a prose composition with a per-word tariff written above it, or — at Ordinary —
a deduction table and nothing else ("Major error= -3. i.e. for omission of verb,
wrong construction or mood"). There is no answer on the page to lift, and a
card would show a student the passage they were given and call it the answer.

*Principal parts and scansion* — Question 4(ii) and 4(iii), and the Ordinary
noun-case part. The scheme prices them and never states them: "(2+1+1) to max
of 10. (2+2 for loquor) (10)", "Metre 2 marks. -2 for any wrong syllables (10)".
The metre's NAME is printed in four of the eight schemes, but the ask is "Name
the metre of the following line and mark the quantities", and the scanned line
— the other eight marks — is nowhere in the document.

Every exclusion carries the scheme's own printed line, and `--exclusions`
writes them to exclusions/latin.json for reconcile.py to check.
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

from lat_paper import LatPaper                                # noqa: E402
from lat_scheme import LatScheme                              # noqa: E402
from lat_topics import (topic_for, concept_for, author_of,    # noqa: E402
                        STRAND)
from paper_census import key_label, census_subject            # noqa: E402
import cardlint                                               # noqa: E402

SUBJECT = 'latin'
SITTINGS = [(2021, 'hl'), (2021, 'ol'), (2022, 'hl'), (2022, 'ol'),
            (2023, 'hl'), (2023, 'ol'), (2024, 'hl'), (2025, 'hl')]
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
EXCLUSIONS = os.path.join(DIR, 'exclusions', f'{SUBJECT}.json')

# The display ceiling for a card's marking rows. Mirrors MAX_LONG_OPTION_ROWS
# in optionCap.mjs, which is the cap rowCapFor() applies to an orderedSplit
# card; a card past it is a wall of text rather than a flashcard.
MAX_ROWS = 16

# The scheme's own words for "this list is not exhaustive", which is what
# `openList` means on a row.
OPEN_LIST = re.compile(
    r'Indicative\s+Notes?|may make valid points|\bsuch as\b|\betc\b'
    r'|\bfor example\b|\be\.g\.', re.I)

# An ask that cannot be answered without the passage printed above it.
PASSAGE_CUE = re.compile(
    r'\bin the passage above\b|\bthe passage above\b|\babove passage\b'
    r'|\bthe passage printed above\b|\bin the above passage\b', re.I)
# An ask that cannot be answered without a plate at the back of the booklet.
# CASE-SENSITIVE on the letter, and closed with a word boundary. Written
# case-insensitively it read "photographs below" as naming Photograph B, and
# 2023 Ordinary's plate question then looked for a lettered plate its paper
# never prints and shipped with no photographs at all.
IMAGE_CUE = re.compile(
    r'\b[Pp]hotographs?\s+([A-E](?:\s*(?:,|and|or)\s*[A-E])*)\b')
# The same ask without letters to name: "Write notes on any two of the
# following, which are shown in the photographs below."
PLATE_CUE = re.compile(r'\b(?:shown|printed) (?:in|below)\b[^.]{0,40}'
                       r'photographs?|photographs? below', re.I)

# A marking point that is the SEC's arithmetic rather than its answer.
TARIFF_ONLY = re.compile(
    r'^[\s\d+×x/().,;:—–-]*(?:marks?)?[\s\d+×x/().,;:—–-]*$', re.I)
TARIFF_PROSE = re.compile(
    r'\bmarks? (?:for )?each\b|\b\d{1,2}\s*(?:x|×)\s*\d{1,2}\s*marks?\b'
    r'|^\s*any (?:one|two|three|four|five|\d+)\b[^.]*\bmarks?\b', re.I)
# The line the SEC repeats above every Indicative Notes block. It is the
# examiner being told the list is not closed, which the card says with
# `openList`; as a marking point it taught nothing.
NOT_EXHAUSTIVE = re.compile(
    r'^(?:N\.?B\.?\s*)?(?:candidates? may make valid points'
    r'|indicative (?:notes?|answers?)'
    r'|candidates may make valid points other than those listed below)',
    re.I)

# The scheme's phrase tariff inside a comprehension answer: "(3)", "(4+3 in any
# order)". Read as the SUM of the numbers inside the bracket, because that is
# what the bracket prices — "(4+3 in any order)" is seven marks for one
# printed answer, and reading only the first number lost three of them.
PHRASE_MARK = re.compile(r'\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})*)[^)]*\)')
# "----any three for full twelve marks", "(max 8)" — the SEC capping a menu it
# has just listed more options for than the ask is worth.
ANY_N = re.compile(r'any\s+(one|two|three|four|five|six)\b[^.]{0,40}?'
                   r'(?:for full|full)?\s*(?:\w+\s+)?marks?', re.I)
WORD_N = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
MAX_CAP = re.compile(r'\(\s*max\.?\s*(\d{1,2})\s*\)', re.I)


def card_id(year, level, key):
    section, q, letter, roman = key
    bits = ['lat', str(year), level]
    if section:
        bits.append(section.lower())
    bits.append(f'q{q}')
    tail = (roman or '') + (letter or '')
    if tail:
        bits.append(tail)
    return '-'.join(bits)


def question_ref(year, level, key):
    """The paper's own address, opened by the sitting.

    Mirrors `key_label(key, 'latin')` in paper_census.py exactly — reconcile
    matches a card to a census leaf through this string, and the two drifting
    apart is how a correct card becomes an orphan.
    """
    return f'{year} {level.upper()} {key_label(key, SUBJECT)}'


# --------------------------------------------------------------- scheme ----
def scheme_entry(scheme, key):
    """The scheme entry that prices this printed ask, and how it was found.

    Three readings, in order, each of them the scheme pricing something the
    paper prints rather than a fallback onto whatever is nearby:

      1. the ask's own address;
      2. the ROMAN above it, where the paper prints a choice of letters under
         one roman the scheme priced whole — Question 4(i) sets "(a) or (b)"
         and every scheme before 2023 prices "(i)" alone;
      3. the ROUTE above it, where the paper prints parts under a route the
         scheme priced whole — Ordinary Question 1 Section A sets five
         sentences and the scheme prices "Five sentences, 15 marks each".
    """
    if key in scheme:
        return scheme[key], 'exact'
    section, q, letter, roman = key
    roman_key = (section, q, None, roman)
    if letter is not None and roman_key in scheme:
        return scheme[roman_key], 'roman'
    route_key = (section, q, None, None)
    if route_key in scheme:
        return scheme[route_key], 'route'
    head_key = (None, q, None, None)
    if head_key in scheme:
        return scheme[head_key], 'question'
    return None, None


def evidence(entry, limit=420):
    return ' | '.join(entry.lines)[:limit] if entry else ''


def _content_lines(entry):
    """The scheme's stated content at this address, its own preamble dropped.

    Arithmetic is NOT dropped line by line, because a printed line is not a
    sentence: the 2025 Higher answer to Q1(iii) wraps as "…any three for full
    twelve" / "marks", and a line-level tariff test threw the second line
    away. What was left ended mid-phrase and the card lost the SEC's own
    instruction that three of the four answers are worth the whole twelve.
    Arithmetic is dropped from the POINTS, after the lines are joined.
    """
    return [l.strip() for l in entry.lines
            if l.strip() and not NOT_EXHAUSTIVE.match(l.strip())]


def _join(lines):
    """Printed lines as one run, with the SEC's own hyphenation closed."""
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


def _has_content(text, floor=2):
    """Is there an answer in here, or only the SEC's arithmetic?

    `floor` is one for a comprehension phrase, because a complete answer to a
    comprehension question is routinely one word — "Rhodes (4).", "A chair.
    (4)", "In winter (4)." Held to two, four correct answers were thrown away
    as empty and excluded as though the scheme had stated nothing.
    """
    bare = re.sub(r'[^A-Za-z ]+', ' ', text)
    return sum(1 for w in bare.split() if len(w) > 2) >= floor


# ------------------------------------------------- comprehension answers ----
def comprehension_rows(entry, marks):
    """The scheme's own answer phrases, each with the marks printed beside it.

    Returns (rows, tariffModel, notation) or (None, None, why-not).
    """
    text = _join(_content_lines(entry))
    if not text:
        return None, None, 'the scheme states no answer for this ask'
    spans = list(PHRASE_MARK.finditer(text))
    if not spans:
        # The SEC also sets a comprehension answer as a SOLIDUS list with one
        # tariff at the end — "He invites guests to dinner not an exercise in
        # social ranking/ he makes them equal at table and couch/ he treats
        # them equally in all respects." — which is the same answer written
        # another way, and refusing it threw two of 2024 Higher's away.
        pieces = [p.strip(' ./;') for p in text.split('/')]
        pieces = [p for p in pieces if _has_content(p, 1)]
        if len(pieces) >= 2:
            rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p,
                     'marks': None}
                    for i, p in enumerate(pieces[:MAX_ROWS], start=1)]
            return rows, {'kind': 'orderedSplit',
                          'notation': text[:200]}, None
        return None, None, 'the scheme prices no phrase of this answer'
    points, at = [], 0
    for m in spans:
        piece = text[at:m.start()].strip(' .;,–—-')
        value = sum(int(n) for n in re.findall(r'\d{1,2}', m.group(1)))
        if piece:
            points.append((piece, value))
        at = m.end()
    tail = text[at:].strip(' .;,–—-')
    if not points:
        return None, None, 'the scheme prices no phrase of this answer'

    cap = MAX_CAP.search(text)
    anyn = ANY_N.search(tail) or ANY_N.search(text[spans[-1].start():])
    values = {v for _t, v in points}
    if anyn and len(values) == 1:
        n = WORD_N[anyn.group(1).lower()]
        per = points[0][1]
        if n * per == marks and len(points) >= n:
            row = {'id': 'r-1', 'kind': 'anyN',
                   'verbatim': 'The answers the scheme accepts',
                   'marks': None,
                   'group': {'claimMax': n, 'perOption': per,
                             'options': [t for t, _v in points][:MAX_ROWS]}}
            return [row], {'kind': 'fixed'}, None
    if not cap and sum(v for _t, v in points) == marks:
        rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': t, 'marks': v}
                for i, (t, v) in enumerate(points, start=1)
                if _has_content(t, 1)]
        if len(rows) == len(points):
            return rows, {'kind': 'fixed'}, None
    # The phrases and the paper's tariff do not agree — the SEC has capped the
    # list ("(max 8)"), or printed more answers than the ask is worth, or
    # priced a phrase this reader cannot see. The card keeps the scheme's own
    # line as the notation and gives no row a mark of its own, which is what
    # `orderedSplit` is for.
    rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': t, 'marks': None}
            for i, (t, _v) in enumerate(points, start=1) if _has_content(t, 1)]
    if not rows:
        return None, None, 'the scheme states no answer for this ask'
    return rows[:MAX_ROWS], {'kind': 'orderedSplit',
                             'notation': text[:200]}, None


# ------------------------------------------------------ grammar answers ----
# How the SEC states a grammar answer, and the only shape it ever uses:
# "patriae=dative meaning 'for'", "sit=Jussive Subjunctive", "caelo = Ablative
# after sub". The right-hand side must open with a LETTER — "Metre-Alcaic= 2
# marks" and "Four nouns, 2 marks each = 8" are the SEC doing arithmetic, and
# a bare test for an equals sign carded both of them with their own tariff
# printed on the back as the answer.
GRAMMAR_ANSWER = re.compile(r'([A-Za-z]{2,})\s*=\s*(?=[A-Za-z])')
GRAMMAR_ITEM = re.compile(r'(?<=[;.])\s+')
# Where the ask stops naming the words it is about and starts printing the
# Latin they are printed in.
GRAMMAR_CUE = re.compile(r'\bin the following\b|\bin the passage\b', re.I)
# The arithmetic the scheme opens a Question 4 entry with: "4+3+3. (10)",
# "(2+1+1) for each verb (utor:2+2), to max of 10. (10)".
GRAMMAR_TARIFF = re.compile(r'^[\s\d+×x().,;:—–-]*(?:\(\d{1,3}\))?')


def _grammar_reason(ask):
    """Why this grammar ask has no answer to lift, in the ask's own terms."""
    low = ask.text.lower()
    if 'quantities' in low or low.startswith('scan '):
        return ('the scheme prices the scansion by deduction and never prints '
                'the scanned line — it names the metre in five of the eight '
                'sittings and states the quantities in none of them, and the '
                'quantities are eight of the ten marks')
    if 'principal parts' in low:
        return ('the scheme prices the principal parts and never states them: '
                'it prints the split and the verb that is worth more, and no '
                'part of any verb')
    if re.search(r'\bcase\b.*\bnouns\b|\bnumber\b.*\bnouns\b', low):
        return ('the scheme prices the four noun forms and never states any '
                'of them')
    return ('the scheme prices this ask and states no grammatical answer '
            'under it')


def grammar_rows(entry, ask):
    """The scheme's stated grammar answers for THIS alternative.

    Question 4(i) sets "Answer either (a) or (b)" and the schemes before 2023
    price the roman alone, so both alternatives' answers are printed at one
    address, one after the other. They are told apart by the words the ask
    itself names: (a) asks about `patriae`, `defendi` and `possent`, (b) about
    `iacerent`, `petens` and `Uticam`, and the scheme's items are keyed on
    exactly those words. That is a WORDING join (Law 4), not an order one —
    read in order, every card carried both answers and told a student that
    "Uticam = acc of motion towards" was part of the answer to (a).
    """
    text = _join(_content_lines(entry))
    items = [i.strip() for i in GRAMMAR_ITEM.split(text) if i.strip()]
    pairs = [i for i in items if GRAMMAR_ANSWER.search(i)]
    if not pairs:
        return None, None, _grammar_reason(ask)
    named = GRAMMAR_CUE.split(ask.text)[0].lower()
    chosen = [i for i in pairs
              if GRAMMAR_ANSWER.search(i).group(1).lower() in named]
    if ask.letter and not chosen:
        return None, None, ('the scheme states grammar answers at this '
                            'address but none of them name a word this ask '
                            'asks about')
    chosen = chosen or pairs
    rows = [{'id': f'r-{i}', 'kind': 'point',
             # The entry opens with its own arithmetic — "4+3+3. (10)" — and
             # the split leaves it on the head of the first answer, where it
             # read "(10) sit=Jussive Subjunctive" on the back of a card.
             'verbatim': GRAMMAR_TARIFF.sub('', p, count=1).strip(' ;.'),
             'marks': None}
            for i, p in enumerate(chosen[:MAX_ROWS], start=1)]
    notation = (GRAMMAR_TARIFF.match(text).group(0) or '').strip()
    return rows, {'kind': 'orderedSplit', 'notation': notation[:200]}, None


# ---------------------------------------------------- indicative content ----
# The SEC's own list marker inside an Indicative Notes paragraph: a name, then
# a dash. "Mark Antony – Consul in 44BCE…", "Syphax – Syphax was the king of
# the Masaesyli tribe…". A "write notes on any two of the following" question
# answers three to five of these in one block, and a row that ran across the
# boundary welded two people's lives into one marking point.
FIGURE_SEAM = re.compile(
    r'(?<=[.;])\s+(?=[A-Z][A-Za-z’\'.()& ]{2,40}?\s*[–—-]\s)')
SENTENCE = re.compile(r'(?<![A-Z])(?<=[.!?])\s+(?=[A-Z“(])')


def indicative_rows(entry):
    """The scheme's stated content, cut into marking points.

    Nothing is rewritten: every point is a contiguous run of the scheme's own
    characters, which is what the provenance gate checks and the only reason
    it can check anything.
    """
    lines = entry.note_lines or entry.lines
    lines = [l for l in lines
             if l.strip() and not TARIFF_ONLY.match(l.strip())
             and not NOT_EXHAUSTIVE.match(l.strip())]
    if not lines:
        return []
    text = _join(lines)
    chunks = [c.strip() for c in FIGURE_SEAM.split(text) if c.strip()]
    out = []
    for chunk in chunks:
        # A menu the examiner set out with semicolons is a list of separate
        # acceptable answers printed on one line; shown as one row it is a
        # paragraph a student cannot tick against.
        if chunk.count(';') >= 2:
            # Split AFTER the semicolon, keeping it: the rows of one chunk are
            # rejoined when the cap bites, and a stripped separator made the
            # joined row read "…along with Julius Caesar Seized Caesar's will",
            # which is a run-on the SEC never printed and which the provenance
            # gate has no way to trace back to a scheme.
            points = [p.strip() for p in re.split(r'(?<=;)\s+', chunk)]
        else:
            points = [p.strip() for p in SENTENCE.split(chunk)]
        # A DROPPED point is a chunk boundary, not a hole to close over. The
        # 2022 Ordinary answer on Germanicus reads "adopted as son by
        # Tiberius; consul at 27 ; led Roman armies against tribes along the
        # Rhine;"; dropping the middle clause and rejoining its neighbours
        # produced a run of text that is in no scheme, and the provenance gate
        # dropped the whole card for it. Every row this returns is a
        # CONTIGUOUS run of the scheme's own characters.
        run = []
        for point in points:
            if (not point or TARIFF_ONLY.match(point)
                    or TARIFF_PROSE.search(point) or not _has_content(point, 1)):
                if run:
                    out.append(run)
                run = []
                continue
            run.append(point)
        if run:
            out.append(run)
    return [c for c in out if c]


def regroup(points, cap):
    """The same text, cut into at most `cap` contiguous runs."""
    if len(points) <= cap:
        return points
    per = -(-len(points) // cap)
    return [' '.join(points[i:i + per]) for i in range(0, len(points), per)]


def regroup_chunks(chunks, cap):
    """Every chunk cut down until they fit the cap together.

    Never below one row per chunk: joining ACROSS a chunk boundary would weld
    two different answers into one marking point.
    """
    total = sum(len(c) for c in chunks)
    if total <= cap:
        return [p for c in chunks for p in c]
    caps = [max(1, (cap * len(c)) // total) for c in chunks]
    while sum(caps) > cap and max(caps) > 1:
        caps[caps.index(max(caps))] -= 1
    return [p for c, k in zip(chunks, caps) for p in regroup(c, k)]


# How the SEC opens an Indicative Note: it says how many points it will pay
# for, and then prints them. "Two points, such as---the surrender of all
# prisoners", "Any two points: to divert the Romans from their siege of
# Capua", "Two points on any two (3+2)+(3+2): Sertorius: one of Rome's best
# generals". Left on the row, the back of the card told a student how many
# points to make instead of what they were — 30 rows across the corpus.
#
# The clause between the count and the delimiter is optional but the
# DELIMITER is not: without that, "three points on the works of the chosen
# author to include a brief description of a work" — a Question 5 entry that
# is instruction all the way down and has no delimiter to stop at — was cut
# sixty characters in, mid-word.
LEAD_IN = re.compile(
    r'^(?:Any\s+)?(?:one|two|three|four|five|six)\s+'
    r'(?:points?|examples?|reasons?|factors?|features?|details?)'
    r'[^:;.—–-]{0,60}?'
    r'(?:\s*such as\s*|\s*[:,]\s*|\s*[-–—]{1,6}\s*)[-–—\s]*', re.I)
# What is left when the count ended at a comma and the "such as" came after it:
# "Two points, such as---the surrender of all prisoners".
SUCH_AS = re.compile(r'^\s*such as\s*[-–—]*\s*', re.I)


def clean_point(text):
    """One marking point with the SEC's arithmetic taken off its ends.

    Ends only, so what remains is a contiguous run of the scheme's own
    characters — which is what the provenance gate reads.
    """
    out = LEAD_IN.sub('', text.strip(), count=1)
    out = SUCH_AS.sub('', out, count=1)
    out = re.sub(r'^\(\s*(?:i{1,3}|iv|v|vi{1,3}|[a-f])\s*\)\s*', '', out)
    out = re.sub(r'\s*\(?\b\d{1,3}\s*(?:x|×)?\s*\d{0,3}\s*marks?\b'
                 r'(?:\s*each)?\)?[.,]?\s*$', '', out, flags=re.I).strip()
    out = re.sub(r'\s*\([\d+,;\s./]+\)\s*$', '', out).strip()
    return out.strip(' .,')


def notation_of(entry, ask):
    """The tariff the scheme prints for this ask, verbatim.

    Its arithmetic half — the lines above the Indicative Notes — is what the
    SEC tells the examiner about how the marks are split, and there is no
    TariffModel that can hold "Three points (7 + 6 + 6); treatment of Tiberius
    — one good point 6 marks". It rides as the orderedSplit notation, which is
    the field the type says is for exactly that.
    """
    lines = [l.strip() for l in entry.tariff_lines if l.strip()]
    lines = [l for l in lines if not NOT_EXHAUSTIVE.match(l)]
    if not lines:
        return ''
    return _join(lines)[:200]


# ------------------------------------------------------ source material ----
def passage_source(P, key, year, level, label, title, note):
    stim = P.stimulus.get(key)
    if not stim or not stim.get('pages'):
        return None
    return {
        'kind': 'source-text',
        'label': label[:120],
        'title': title,
        'pages': stim['pages'],
        'attribution': (f'SEC Latin {year} {LEVEL_TITLE[level]} Level '
                        'examination paper — © State Examinations Commission.'),
        'presentationNote': note,
    }


def photograph_source(P, letters, year, level):
    pages = sorted({p for L in letters for p in [P.photo_pages().get(L)] if p})
    if not pages:
        return None
    named = ', '.join(f'Photograph {L}' for L in letters)
    return {
        'kind': 'source-illustration',
        'label': named[:120],
        'title': 'The plates printed with this question',
        'pages': pages,
        # No `sourceLabel`: that names a SEPARATE official document to be
        # resolved in the Paper Trail index, the way Classical Studies names
        # its Paper X. Latin prints its plates on their own pages of the SAME
        # booklet as the questions, so the source is the question paper and
        # the pages are the address inside it.
        'attribution': (f'SEC Latin {year} {LEVEL_TITLE[level]} Level '
                        'examination paper — © State Examinations Commission.'),
        'presentationNote': ('The photographs exactly as the examination '
                            'printed them, on their own pages at the back of '
                            'the booklet.'),
    }


# ---------------------------------------------------------------- build ----
TRANSLATION_KINDS = ('translate-into-latin', 'translate-into-english')


def build():
    cards, exclusions = [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    stats = collections.Counter()
    joins = collections.Counter()

    def refuse(reason, ref, n=1):
        refused[reason] += n
        examples[reason].append(ref)

    def exclude(ref, reason, entry, extra=''):
        exclusions.append({'ref': ref, 'reason': reason,
                           'schemeEvidence': (extra or evidence(entry)
                                              or 'the scheme prices this ask '
                                                 'and states nothing under it')})

    for year, level in SITTINGS:
        P = LatPaper(year, level)
        S = LatScheme(year, level)
        scheme = S.entries()
        asks = P.asks()
        route_text = collections.defaultdict(str)
        for a in asks:
            route_text[(a.section, a.q)] += ' ' + a.text

        # Question 5(vi) sets two or three questions on the plates at the back
        # and prices the PAIR a candidate answers, never the single part: the
        # paper prints twenty-five marks over "answer two of the following"
        # and the scheme splits each part "4/5+4+4", which is twelve marks or
        # thirteen at the examiner's discretion. Neither document prints a
        # number that is one part's tariff, so the card is made where the
        # paper priced it — one card over the part's printed alternatives,
        # citing them as the range it covers.
        plate_group = [a for a in asks if a.q == 5 and a.letter and a.roman]
        grouped = {a.key for a in plate_group}

        for ask in sorted(asks, key=lambda a: tuple(str(x) for x in a.key)):
            if ask.key in grouped:
                continue
            ref = question_ref(year, level, ask.key)
            entry, how = scheme_entry(scheme, ask.key)

            if ask.route_kind in TRANSLATION_KINDS:
                exclude(ref, TRANSLATION_REASON[ask.route_kind], entry)
                stats['excluded-translation'] += 1
                continue
            if entry is None:
                exclude(ref, 'the scheme prices no address that covers this '
                             'printed ask', None)
                stats['excluded-unpriced'] += 1
                continue
            joins[how] += 1

            marks = ask.marks
            if not marks:
                refuse('neither document prints a tariff for this ask', ref)
                continue

            if ask.route_kind == 'comprehension':
                rows, model, why = comprehension_rows(entry, marks)
                if rows is None:
                    exclude(ref, why, entry)
                    stats['excluded-no-answer'] += 1
                    continue
                notation = ''
            elif ask.route_kind == 'grammar':
                rows, model, why = grammar_rows(entry, ask)
                if rows is None:
                    exclude(ref, why, entry)
                    stats['excluded-grammar'] += 1
                    continue
                if not model['notation'] and how == 'exact':
                    # 2023 Higher prices "(i) 4+3+3. (10)" once and then
                    # answers (a) and (b) under their own letters, so the
                    # answer's own entry carries no arithmetic. The tariff is
                    # the roman's, one level up, and it is printed.
                    above = scheme.get((None, ask.q, None, ask.roman))
                    if above:
                        model['notation'] = (
                            GRAMMAR_TARIFF.match(_join(above.lines))
                            .group(0).strip()[:200])
                notation = model['notation']
            else:
                chunks = indicative_rows(entry)
                if not chunks:
                    exclude(ref, 'the scheme prices this ask with its mark '
                                 'allocation alone and states no answer '
                                 'content', entry)
                    stats['excluded-no-answer'] += 1
                    continue
                # Regroup on the RAW points and clean the rows the regroup
                # produced: cleaning first strips a point's trailing
                # arithmetic, and joining across that strip makes a row the
                # scheme does not contain.
                points = [clean_point(p)
                          for p in regroup_chunks(chunks, MAX_ROWS)]
                points = [p for p in points if p and _has_content(p, 1)]
                if not points:
                    exclude(ref, 'the scheme prices this ask with its mark '
                                 'allocation alone and states no answer '
                                 'content', entry)
                    stats['excluded-no-answer'] += 1
                    continue
                notation = notation_of(entry, ask)
                if not notation:
                    refuse('the scheme prints no tariff notation for this ask',
                           ref)
                    continue
                open_list = bool(OPEN_LIST.search(' '.join(entry.lines)))
                rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p,
                         'marks': None,
                         **({'openList': True} if open_list else {})}
                        for i, p in enumerate(points, start=1)]
                model = {'kind': 'orderedSplit', 'notation': notation[:200]}

            card = _card(P, S, year, level, ask, ref, rows, model, entry,
                         route_text, notation)
            if card is None:
                refuse('the ask points at printed matter the card cannot '
                       'carry', ref)
                continue
            cards.append(card)
            stats['carded'] += 1

        if plate_group:
            card = _plate_card(P, S, year, level, plate_group, scheme,
                               route_text)
            if card is None:
                for a in plate_group:
                    exclude(question_ref(year, level, a.key),
                            'the scheme prices this part with its mark '
                            'allocation alone and states no answer content',
                            scheme_entry(scheme, a.key)[0])
                    stats['excluded-no-answer'] += 1
            else:
                cards.append(card)
                stats['carded'] += 1
                stats['plate-parts-covered'] += len(plate_group) - 1
    return cards, exclusions, refused, examples, stats, joins


TRANSLATION_REASON = {
    'translate-into-latin':
        'the scheme states no model translation for this ask — it prints the '
        'ENGLISH the candidate is given, with a per-word tariff written above '
        'it, or a table of deductions, and never the Latin that would be the '
        'answer',
    'translate-into-english':
        'the scheme states no model translation for this ask — it prints the '
        'LATIN the candidate is given, cut into units with a mark after each, '
        'and never the English that would be the answer',
}


def _card(P, S, year, level, ask, ref, rows, model, entry, route_text,
          notation):
    key = ask.key
    topic = topic_for(ask.q, ask.route_kind, route_text[(ask.section, ask.q)])
    if not topic:
        return None
    question = ask.text
    joined = f'{ask.stem} {question}'
    if cardlint.NAMES_LETTERS.search(joined) and not IMAGE_CUE.search(joined):
        return None
    card = {
        'id': card_id(year, level, key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        # The printed QUESTION, which is the unit Latin's paper divides
        # itself into. The "Section A"/"Section B" under three of its five
        # questions is a choice of ROUTES through one question, not a division
        # of the paper, and it is named in the citation where it belongs.
        'section': f'Q{ask.q}',
        'topicId': topic,
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': model,
        'totalMarks': ask.marks,
        'rows': rows,
        'notes': _note(entry, ask, notation),
    }
    if ask.stem and len(ask.stem) >= 20:
        card['stem'] = ask.stem[:600]
    source = _source_for(P, ask, year, level)
    if source:
        card['sourceMaterial'] = source
    return card


def _source_for(P, ask, year, level):
    if ask.route_kind == 'comprehension':
        return passage_source(
            P, (ask.section, ask.q, None), year, level,
            f'QUESTION {ask.q} SECTION {ask.section} — THE PASSAGE',
            'The Latin passage, its summary and the printed vocabulary',
            'Read the passage exactly as the examination printed it, with the '
            'vocabulary the SEC glossed it with, then answer in English.')
    if PASSAGE_CUE.search(ask.text):
        return passage_source(
            P, (ask.section, ask.q, 'i'), year, level,
            f'QUESTION {ask.q} SECTION {ask.section} — THE PRINTED PASSAGE',
            'The passage printed above this question',
            'The ask is about the passage the paper prints above it; this is '
            'that passage, exactly as it was set.')
    letters = IMAGE_CUE.search(ask.text)
    if letters:
        return photograph_source(
            P, sorted(set(re.findall(r'[A-E]', letters.group(1)))),
            year, level)
    if PLATE_CUE.search(ask.text):
        pages = P.image_pages()
        if not pages:
            return None
        return {
            'kind': 'source-illustration',
            'label': 'THE PHOTOGRAPHS PRINTED WITH THIS QUESTION',
            'title': 'The plates printed with this question',
            'pages': pages,
            'attribution': (f'SEC Latin {year} {LEVEL_TITLE[level]} Level '
                            'examination paper — © State Examinations '
                            'Commission.'),
            'presentationNote': ('The photographs exactly as the examination '
                                 'printed them.'),
        }
    return None


def _plate_card(P, S, year, level, parts, scheme, route_text):
    """One card for Question 5's plate question, over the parts it prices."""
    parts = sorted(parts, key=lambda a: a.letter)
    roman = parts[0].roman
    entries = [(a, scheme_entry(scheme, a.key)[0]) for a in parts]
    chunks, notation = [], []
    for a, entry in entries:
        if entry is None:
            continue
        notation.append(f'({a.letter}) ' + notation_of(entry, a))
        chunks += indicative_rows(entry)
    if not chunks:
        return None
    points = [clean_point(p) for p in regroup_chunks(chunks, MAX_ROWS)]
    points = [p for p in points if p and _has_content(p, 1)]
    if not points:
        return None
    stem = parts[0].stem
    question = ' '.join(f'({a.letter}) {a.text}' for a in parts)
    letters = sorted({L for a in parts
                      for m in IMAGE_CUE.finditer(f'{stem} {a.text}')
                      for L in re.findall(r'[A-E]', m.group(1))})
    source = photograph_source(P, letters, year, level) if letters else None
    if letters and not source:
        return None
    key = (None, 5, parts[0].letter, roman)
    ref = (f'{year} {level.upper()} Q5({roman})({parts[0].letter})'
           f'–({parts[-1].letter})')
    card = {
        'id': card_id(year, level, key) + f'-{parts[-1].letter}',
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'Q5',
        'topicId': topic_for(5, 'essay', ''),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'orderedSplit',
                        'notation': _join(notation)[:200]},
        'totalMarks': parts[0].marks,
        'rows': [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p,
                  'marks': None, 'openList': True}
                 for i, p in enumerate(points, start=1)],
        'notes': ('The paper prints one tariff over this part and asks for '
                  'TWO of its questions, so the card carries all of them and '
                  "the scheme's own split for each. "
                  + _join(notation))[:900],
    }
    if stem and len(stem) >= 20:
        card['stem'] = stem[:600]
    if source:
        card['sourceMaterial'] = source
    card['coversAsks'] = len(parts)
    return card


def _note(entry, ask, notation):
    bits = []
    if notation and re.search(r'\d', notation):
        bits.append(f'The scheme prints {notation!r} for this ask.')
    if ask.inherited:
        bits.append('The paper prints this tariff on the part above, over the '
                    'alternatives a candidate chooses between.')
    return ' '.join(bits)[:900]


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
        census = census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        accounted = sum(c.get('coversAsks', 1) for c in cards) + len(exclusions)
        print(f'{len(cards)} card(s) + {len(exclusions)} exclusion(s) = '
              f'{accounted} of {total} paper asks '
              f'({100 * accounted / total:.1f}%)')
        rows = sum(len(c['rows']) for c in cards)
        fixed = sum(1 for c in cards if c['tariffModel']['kind'] == 'fixed')
        print(f'{rows} marking rows; {fixed} fixed-tariff card(s), '
              f'{len(cards) - fixed} orderedSplit')
        print('paper/scheme join: ' + ', '.join(
            f'{n} at the {k}' for k, n in joins.most_common()))
        srcs = collections.Counter(
            (c.get('sourceMaterial') or {}).get('kind', 'none') for c in cards)
        print(f'source material: {dict(srcs)}')
        for k, n in sorted(stats.items()):
            print(f'   {n:5} {k}')
        by_year = collections.Counter((c['year'], c['level']) for c in cards)
        for k, n in sorted(by_year.items()):
            print(f'   {k[0]} {k[1]:9} {n}')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:12} {n}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:200 if args.all else 3]:
                print(f'             {e}')
        return 0

    for card in cards:
        card.pop('coversAsks', None)
    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
