#!/usr/bin/env python3
"""Construction Studies asks found by the independent paper census.

The original twenty paper plans authored the parts their flat scheme reader
could price.  A later paper-only census found the remainder, chiefly rows whose
MAXIMUM MARK cell disappeared from the markdown text.  This pass reads those
cells from the official scheme PDF coordinates (``Scheme.pdf_mark_rows``) and
keeps every answer phrase as a slice of the scheme markdown.

It deliberately does not handle Question 10 Alternative.  The published
schemes print only generic ``discussion point`` / ``guideline`` slots for those
essays and no accepted content; each is documented in the subject exclusion
ledger instead of being turned into an invented model answer.
"""
import difflib
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

from cs_lib import Author, CONTENT_FREE, MAX_OPTIONS_SHOWN, _squash  # noqa: E402
from cs_topics import concept_for, topic_for                       # noqa: E402
from markbank_authoring import make_audit, make_card, make_emit     # noqa: E402

SUBJECT = 'construction-studies'
card = make_card(SUBJECT, default_section='B')
emit = make_emit(make_audit(MAX_OPTIONS_SHOWN))

# Every non-alternative leaf which reconcile.py reported open before this pass.
# The list is pinned rather than recomputed from the shipped deck: after a build
# these leaves are no longer open, and a generator driven by that changed state
# would delete its own cards on the next run.
TARGETS = {
    (2016, 'hl'): [(-10, None), (1, 'a'), (1, 'b'), (5, 'a'), (8, 'b'), (9, 'b')],
    (2016, 'ol'): [(9, 'b')],
    (2017, 'hl'): [(-10, None), (1, 'a'), (5, 'a'), (9, 'b')],
    (2017, 'ol'): [(2, 'c'), (3, 'c'), (4, 'a'), (4, 'c')],
    (2018, 'hl'): [(-10, None), (10, 'b')],
    (2018, 'ol'): [(4, 'b'), (4, 'c'), (6, 'a'), (8, None)],
    (2019, 'hl'): [(-10, None), (1, 'a'), (2, 'b'), (3, 'c'), (4, 'b'), (9, 'a')],
    (2019, 'ol'): [(2, 'a'), (4, 'a'), (8, None)],
    (2020, 'hl'): [(1, 'a'), (3, 'b'), (5, 'c'), (8, 'b'), (10, 'b')],
    (2020, 'ol'): [(4, 'b')],
    (2021, 'hl'): [(5, 'a'), (5, 'c')],
    (2021, 'ol'): [(2, 'b'), (2, 'c'), (4, 'c'), (7, 'a')],
    (2022, 'hl'): [(5, 'a'), (10, 'b'), (10, 'c')],
    (2022, 'ol'): [(2, 'a'), (4, 'b'), (5, 'b')],
    (2023, 'hl'): [(5, 'a'), (5, 'c'), (8, 'b'), (10, 'b')],
    (2023, 'ol'): [(2, 'b'), (4, 'c'), (7, 'c')],
    (2024, 'hl'): [(2, 'b'), (2, 'c'), (3, 'a'), (4, 'c'), (5, 'a'),
                   (5, 'b'), (9, 'a'), (9, 'b')],
    (2024, 'ol'): [(2, 'b'), (4, 'c'), (5, 'a'), (7, 'c'), (9, 'a')],
    (2025, 'hl'): [(2, 'b'), (3, 'a'), (4, 'b'), (4, 'c'), (5, 'a'),
                   (5, 'b'), (6, 'a'), (7, 'a'), (8, 'b'), (9, 'b'),
                   (10, 'c')],
    (2025, 'ol'): [(8, None), (9, 'a')],
}

PRESENTATION = re.compile(
    r'^(quality|scale|drafting|draughting|sketch(?:es)?|drawing|annotation)\b',
    re.I)
FURNITURE = re.compile(
    r'^(?:material element|details|marks|formulae?:|alternative method:|'
    r'leaving certificate|question\s+\d+|total\b)', re.I)


def clean_options(A, q, letter):
    """The scheme's accepted content, in its own order, without furniture."""
    groups = A.S.groups(q, letter, 'indicative')
    source = [item for _, _, items in groups for item in items]
    if not source:
        source = A.S.indicative.get((q, letter), [])[1:]
    out, seen = [], set()
    for raw in source:
        text = ' '.join(raw.replace('\x00', ' ').replace('\uf020', ' ').split()).strip(' •;')
        if (not text or len(text) < 3 or FURNITURE.match(text)
                or re.fullmatch(r'[\d.,/×x=+–\- ]+', text)
                or CONTENT_FREE.match(text)):
            continue
        # A very long paragraph is usually the next item welded on by a broken
        # column.  It is still provenance-bearing, but not a usable answer row.
        if len(text) > 620:
            continue
        key = _squash(text)
        if key and key not in seen and key in A.raw:
            seen.add(key)
            out.append(text)
    return groups, out


def same_label(a, b):
    x, y = _squash(a), _squash(b)
    if not x or not y:
        return False
    blocks = difflib.SequenceMatcher(None, x, y).get_matching_blocks()
    hit = sum(block.size for block in blocks)
    return hit / min(len(x), len(y)) >= 0.72


def source_label(A, label):
    """Use a provenance-bearing spelling of a PDF row label."""
    if _squash(label) in A.raw:
        return label
    candidates = [lab for lab, _ in A.S.mark_rows(*A._completion_key)]
    hit = next((lab for lab in candidates if same_label(lab, label)), None)
    if hit:
        return hit
    # The part heading is always in both the flat scheme and its PDF table.  It
    # is less specific than the lost label but never invented.
    for line in A.S.marks.get(A._completion_key, []):
        line = ' '.join(line.replace('\x00', ' ').split()).strip()
        if line and _squash(line) in A.raw:
            return line
    raise ValueError(f'{A.year} {A.level} {A._completion_key}: no source label')


def rows_for(A, q, letter, cid):
    scheme_q = '10alt' if isinstance(q, int) and q < 0 else q
    scheme_letter = letter
    # The 2016 mark table keeps Question 1 whole, while the paper publishes
    # (a) and (b).  Later older tables sometimes omit only the leading (a).
    if (scheme_q, scheme_letter) not in A.S.marks and (scheme_q, None) in A.S.marks:
        scheme_letter = None
    A._completion_key = (scheme_q, scheme_letter)
    priced = (A.S.pdf_mark_rows(scheme_q, scheme_letter)
              or A.S.mark_rows(scheme_q, scheme_letter))
    groups, options = clean_options(A, scheme_q, scheme_letter)
    if q == 1 and A.year == 2016 and scheme_letter is None:
        ingress = re.compile(r'(?:prevent|ingress).*(?:water|rain)|water.*ingress', re.I)
        if letter == 'b':
            priced = [row for row in priced if ingress.search(row[0])]
        else:
            priced = [row for row in priced if not ingress.search(row[0])]
    if not priced:
        # A total is still a published mark boundary.  This path is rare and
        # remains explicit in stderr so it cannot masquerade as a priced row.
        totals = A._printed_totals(scheme_q, scheme_letter)
        if not totals:
            raise ValueError(f'Q{q}({letter}): no PDF mark rows or printed total')
        heading = source_label(A, A.S.marks[(q, letter)][0])
        priced = [(heading, min(totals))]

    rows = []
    attached = False
    for i, (raw_label, marks) in enumerate(priced):
        if marks <= 0:
            continue
        label = source_label(A, raw_label)
        row = {
            'id': f'{cid}-r{i + 1}',
            'kind': 'criterion',
            'verbatim': label,
            'marks': marks,
            'openList': True,
        }
        # Put the scheme's model content beside the first content-bearing
        # criterion.  Repeating the same twenty accepts under every Notes and
        # Sketches row would obscure the tariff rather than explain it.
        if options and not attached and not PRESENTATION.match(label):
            row['accepts'] = options[:MAX_OPTIONS_SHOWN]
            note = ('The accepted examples are the official scheme\'s own '
                    'indicative content for this part.')
            if len(options) > MAX_OPTIONS_SHOWN:
                note += (f' It prints {len(options)} examples; the first '
                         f'{MAX_OPTIONS_SHOWN} are shown here in scheme order.')
            row['contextNote'] = note
            attached = True
        elif PRESENTATION.match(label):
            row['contextNote'] = (
                'These marks are awarded for communicating the requested '
                'construction detail in the notes or freehand sketch, as '
                'specified by the official mark table.')
        rows.append(row)

    # Some graphical-only parts have no textual indicative list.  The mark
    # table criterion is still the complete published self-check boundary.
    if not rows:
        raise ValueError(f'Q{q}({letter}): no positive priced rows')
    return rows


def question_ref(A, q, letter):
    number = f'{-q}-alt' if isinstance(q, int) and q < 0 else str(q)
    return f'{A.year} {A.level.upper()} Q{number}' + (f'({letter})' if letter else '')


cards = []
for (year, level), parts in sorted(TARGETS.items()):
    A = Author(year, level)
    for q, letter in parts:
        qtext = A.question(q, letter)
        if not qtext:
            raise SystemExit(f'{year} {level} Q{q}({letter}): paper has no ask')
        number = f'{-q}-alt' if isinstance(q, int) and q < 0 else str(q)
        cid = f'cons-{year}-{level}-q{number}' + (f'-{letter}' if letter else '') + '-completion'
        rows = rows_for(A, q, letter, cid)
        stem = A.P.stem(q, letter) or A.P.stem(q) or ''
        indicative = ' '.join(A.S.indicative.get(A._completion_key, [])[:8])
        topic, matched = topic_for(' '.join((stem, qtext, indicative)))
        if q == 8 and letter is None:
            # Ordinary Level's fixed construction-terms menu spans several
            # elements; the syllabus's drawings/symbols/notation shelf is the
            # established home used by every other year of this same task.
            topic = 'cons-1-5'
        if not topic:
            raise SystemExit(f'{year} {level} Q{q}({letter}): no topic for {qtext[:80]!r}')
        total = sum(row['marks'] for row in rows)
        notes = (
            'Recovered from the official scheme PDF because one or more '
            'MAXIMUM MARK cells are absent from the flattened scheme text.')
        cards.append(card(
            cid, year, A.deck_level, topic, concept_for(qtext),
            question_ref(A, q, letter), qtext, str(total), total, rows, notes,
            stem=stem, tariff_kind='fixed'))

emit(cards)
