#!/usr/bin/env python3
"""Author every Modern Greek ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/mgr_all.py --report
    python3 scripts/markbank/authoring/mgr_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/mgr_all.py \
        > scripts/markbank/authored/modern-greek.json

Census-driven: the sixteen sittings print 142 leaf asks, and this walks that
census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask, in Greek, answered in Greek. The question comes from the PAPER
and the answer from the SCHEME, and the two are paired by SUBTRACTION rather
than by scoring: the scheme reprints the paper's question and sets its answer
under it, so the answer is the scheme's block with the paper's own printed text
taken off the front. A block that does not reprint the question is a fault and
no card is made from it (see mgr_scheme).

Question 1 is one card with five rows. The SEC sets five underlined words or
phrases and prices the QUESTION — "(5 × 1)" in the recent sittings, "(5
βαθμοί)" in the older ones — never the word, so five separate cards would each
have to invent a tariff. The scheme glosses each word in turn, so the five
glosses are the five rows of the one card the paper actually sets.

THE ARTICLE TRAVELS WITH THE CARD
---------------------------------
Every comprehension answer quotes an article printed only in the question
paper, and three of the six questions name a paragraph of it. Each card binds
`sourceMaterial` to the pages the article was printed on in the QUESTION paper.

THE REFUSALS
------------
**Written production.** ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ asks for a 100-word commentary and
ΟΜΑΔΑ 3η ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ for a 300-word essay on one of two themes. The scheme
answers each with ONE indicative composition of its own and prices nothing
inside it — the same refusal the other nine languages make of their writing
tasks.

**No printed tariff.** 2014 prices its Question 1 and prints nothing at all on
Questions 2 to 6; 2016 prints nothing on any of the six. Neither the paper nor
the scheme states a per-question price in those two sittings, and the only
number either document gives is the "[30 / 100]" on the group's own head.

**2015's scheme is unreadable.** Every font in it is embedded with a broken
ToUnicode CMap: 0 of its characters come back as Greek, against 2,365 to 8,138
in every other scheme in the corpus, and derive_glyphs cannot repair it because
those glyph ids appear nowhere else with a correct mapping.
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

from mgr_paper import MgrPaper, sittings                        # noqa: E402
from mgr_scheme import MgrScheme, answers, has_scheme           # noqa: E402
from mgr_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                        language_note)
from paper_census import key_label                              # noqa: E402

SUBJECT = 'modern-greek'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
MAX_ROWS = 16

# Where the SEC breaks one stated answer into the next: a full stop or a Greek
# ano teleia that ends a sentence, or a bullet it sets its points under.
SEGMENT = re.compile('(?<=[.·;])\\s+(?=[A-ZΆ-Ϋ“"])|\\s*[•●]\\s*')

GRID_EVIDENCE = (
    'the scheme answers this task with ONE indicative composition of its own '
    'and prices nothing inside it. Under "ΟΜΑΔΑ 3η ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100] '
    '— Να επιλέξετε ένα από τα δύο θέματα και να αναπτύξετε τις απόψεις σας σε '
    'ένα κείμενο 300 περίπου λέξεων" it prints a finished essay, sometimes '
    'headed "Πιθανές περιοχές ανάπτυξης" — possible areas of development. '
    'There is no marking point in it and no tariff on any line of it, so a '
    'card would ask a student to reproduce a model composition rather than to '
    'answer anything.')

COMMENTARY_EVIDENCE = (
    'the scheme answers this task with ONE indicative paragraph of its own and '
    'prices nothing inside it. Under "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ [30 / 100] — Να '
    'σχολιάσετε σε περίπου 100 λέξεις" it prints a finished commentary on the '
    'phrase the paper quotes. That is a piece of writing to be judged, not a '
    'set of answers to be recalled, and no line of it carries marks.')

UNPRICED_EVIDENCE = (
    'neither document states a tariff for this ask. The paper prints no marks '
    'beside it and the scheme, which reprints the question verbatim, prints '
    'none either — the only number either states for the whole comprehension '
    'is the "[30 / 100]" on the group head. Every other sitting in the corpus '
    'prices these questions on the ask itself, "(5 βαθμοί)" or "(5)", and two '
    'do not.')

UNREADABLE_EVIDENCE = (
    'the scheme\'s text layer returns no Greek at all. Every font in the 2015 '
    'document is embedded with a broken ToUnicode CMap, so "ΟΜΑΔΑ 1η" comes '
    'back as "ɃɀȰȴȰ 1ɻ" and "Το σημαντικότερο" as "ȉȠ ıȘȝĮȞĲȚțȩĲİȡȠ": 0 Greek '
    'characters out of the whole file, against 2,365 to 8,138 in every other '
    'Modern Greek scheme in the corpus. derive_glyphs.py --subject '
    'modern-greek cannot repair it — the glyph ids in those subsets appear '
    'nowhere in the corpus with a correct mapping, and it repaired 61 '
    'sightings. The question paper is perfectly readable; the answers are not '
    'recoverable from what the SEC published.')


def card_id(year, level, key):
    section, q, letter, _roman = key
    parts = ['mgr', str(year), level, str(section).lower()]
    if q:
        parts.append(str(q))
    if letter:
        parts.append(letter)
    return '-'.join(parts)


def question_ref(year, level, key):
    return f'{year} {level.upper()} {key_label(key)}'


def build():
    cards, excluded = [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year, level in sittings(SUBJECT):
        P = MgrPaper(year, level, SUBJECT)
        asks = P.asks()      # …first: the rubric and the article's pages are
        stamp = f'{year} {level.upper()}'   # read while the paper is walked
        language = answer_language(P)
        got, _faults = answers(year, level, SUBJECT) \
            if has_scheme(year, level, SUBJECT) else ({}, [])
        readable = bool(got) or not has_scheme(year, level, SUBJECT)
        for ask in asks:
            ref = question_ref(year, level, ask.key)
            if ask.kind == 'essay':
                refuse('the scheme answers this essay with a model '
                       'composition and prices nothing inside it', ref,
                       f'{stamp} scheme, ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ: {GRID_EVIDENCE}')
                continue
            if ask.kind == 'commentary':
                refuse('the scheme answers this commentary with a model '
                       'paragraph and prices nothing inside it', ref,
                       f'{stamp} scheme, ΣΧΟΛΙΑΣΜΟΣ: {COMMENTARY_EVIDENCE}')
                continue
            if not readable:
                refuse('the scheme\'s text layer returns no Greek at all, so '
                       'no answer can be lifted from it', ref,
                       f'{stamp} scheme: {UNREADABLE_EVIDENCE}')
                continue
            if ask.marks is None:
                refuse('neither the paper nor the scheme states a tariff for '
                       'this ask', ref, f'{stamp}: {UNPRICED_EVIDENCE}')
                continue
            pair = got.get(ask.key)
            if pair is None:
                refuse('the scheme prints no block that reprints this '
                       'question, so the pair cannot be trusted', ref,
                       f'{stamp} paper: "{ask.text[:110]}" — no block of the '
                       f'scheme at this address reprints it')
                continue
            _card(P, ask, pair, year, level, language, cards, refuse, ref)
    return cards, refused, examples, excluded


def _card(P, ask, pair, year, level, language, cards, refuse, ref):
    answer, items = pair
    if items:
        rows = [{'id': f'r-{i + 1}', 'kind': 'point',
                 'verbatim': f'{word} — {gloss}', 'marks': None}
                for i, (word, gloss) in enumerate(items)]
        tariff = {'kind': 'orderedSplit', 'notation': f'{len(items)} × 1'} \
            if ask.marks == len(items) else {'kind': 'questionTotal'}
    else:
        parts = _segments(answer)
        if not parts:
            refuse('the scheme reprints this question and states nothing '
                   'under it', ref,
                   f'{year} {level.upper()} scheme: "{ask.text[:100]}" is '
                   f'reprinted with no answer beneath it')
            return
        rows = [{'id': f'r-{i + 1}', 'kind': 'point', 'verbatim': p,
                 'marks': None} for i, p in enumerate(parts)]
        tariff = {'kind': 'questionTotal'}
    note = language_note(language)
    if note:
        for row in rows:
            row['contextNote'] = note
    card = {
        'id': card_id(year, level, ask.key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': str(ask.section),
        'topicId': topic_for(ask),
        'conceptId': concept_for(ask.text),
        'questionRef': ref,
        'questionText': ask.text,
        'tariffModel': tariff,
        'totalMarks': ask.marks,
        'rows': rows,
        'notes': (f'The examination prints this ask at {ask.marks} marks, '
                  f'inside a group it heads {P.section_marks.get(ask.section)} '
                  f'marks. The paper prints it on page {ask.page} of the '
                  f'question booklet.'),
    }
    if ask.stem and len(ask.stem) >= 12 and ask.stem != ask.text:
        card['stem'] = ask.stem
    source = _source(P, year, level, language)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


def _segments(text):
    parts = [p.strip(' ·;.') for p in SEGMENT.split(text or '') if p]
    parts = [p for p in parts if len(p) > 3]
    if not parts:
        return []
    while len(parts) > MAX_ROWS:
        i = min(range(len(parts) - 1),
                key=lambda n: len(parts[n]) + len(parts[n + 1]))
        parts[i:i + 2] = [f'{parts[i]} {parts[i + 1]}']
    return parts


def _source(P, year, level, language):
    if not P.passage_pages:
        return None
    return {
        'kind': 'source-text',
        'label': 'ΤΟ ΚΕΙΜΕΝΟ',
        'title': f'The article this question is about — answer in {language}'
                 if language else 'The article this question is about',
        'pages': P.passage_pages,
        'attribution': (f'SEC Modern Greek {year} {LEVEL_TITLE[level]} Level '
                        'examination paper — © State Examinations Commission.'),
        'presentationNote': ('Read the article exactly as the examination '
                             'printed it, then answer. '
                             + language_note(language)).strip(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded = build()
    if args.exclusions:
        path = os.path.join(DIR, 'exclusions', f'{SUBJECT}.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(sorted(excluded, key=lambda e: e['ref']), fh,
                      ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'{len(excluded)} exclusion(s) written to {path}',
              file=sys.stderr)
        return 0
    if args.report:
        print(f'{len(cards)} card(s), {sum(refused.values())} refusal(s)')
        for reason, n in refused.most_common():
            print(f'  {n:>4}  {reason}')
            print(f'        e.g. {examples[reason][0]}')
        return 0
    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
