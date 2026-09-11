#!/usr/bin/env python3
"""Author every Spanish ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/es_all.py --report
    python3 scripts/markbank/authoring/es_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/es_all.py > scripts/markbank/authored/spanish.json

Census-driven: the ten sittings print 653 leaf asks across three booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (es_paper.py) and its
marking points from the SCHEME (es_scheme.py). The two are joined on the three
things they both print — the address, the text's own TITLE and the tariff — and
the census checks all three (Law 4: join on whatever BOTH documents print; the
Spanish scheme never reprints the question, so align.py has nothing to score).

THE TEXT TRAVELS WITH THE CARD, FROM THE BOOKLET IT WAS PRINTED IN
------------------------------------------------------------------
Every reading answer is drawn from a text, so each card binds `sourceMaterial`
to the exact pages of its own text. For Section A that is the question paper.
For HIGHER SECTION B it is not: the article is printed on a two-page LOOSE
SHEET with its own SEC file id, and the paper says so — "The questions refer to
the text on the loose sheet provided separately." Those cards carry
`sourceLabel: 'Section B'`, which build-deck.mjs resolves against Paper Trail's
index into `sourceMaterial.sourceFileid`. A card that let it default to the
question paper would open a student on the page of QUESTIONS about an article
they cannot see, silently — the corruption `types/markBank.ts` warns about on
that very field.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Spanish sets some questions in Spanish and some in English, and both schemes
head every section "Questions must be answered in the language indicated on the
examination paper" — at Ordinary with the penalty spelled out, 50% of the marks
for a whole question in the wrong language and nothing at all for a sub-part.
Every card says which language is wanted and quotes that rule verbatim.

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report, and every
refusal that lands on a census leaf becomes an exclusions entry carrying the
scheme evidence for it (--exclusions writes them).
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

from es_paper import EsPaper                                   # noqa: E402
from es_scheme import EsScheme, ref_for                        # noqa: E402
from es_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, SAYS_SPANISH, SAYS_ENGLISH)
from paper_census import census_subject                        # noqa: E402

SUBJECT = 'spanish'
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts. Nothing in this corpus reaches it — the longest menu the
# Spanish scheme prints is nine — but the ceiling is stated so a later sitting
# is trimmed with disclosure rather than shipped as a wall of text.
MAX_OPTIONS = 16
# The most marking rows a `fixed` card may carry, from MAX_ROWS via rowCapFor
# in types/markBank.ts. A part listing more separate answers than this is
# refused rather than trimmed: trimming would delete answers the SEC pays for.
MAX_ROWS = 5

# The scheme's own direction to the examiner standing where an answer would be.
# "Discussion on any three relevant points" prices a 12-mark essay and states
# nothing a student can check themselves against; "[Any mark from 0 to 6 may be
# awarded for this question]" prices a rewriting task the same way.
DIRECTION_ONLY = re.compile(
    r'^Discussion on any\b|^Any mark from\b|^Marks? awarded\b', re.I)

# The section a card is filed under, which SecCardBase types as a single
# letter. The section TOKEN in a citation carries more than that — "A1a" is
# Section A's literature route — so the two are kept apart deliberately.
CARD_SECTION = {'A1a': 'A', 'A1b': 'A', 'A2': 'A', 'A': 'A', 'B': 'B', 'C': 'C'}

GRID_EVIDENCE = {
    'B': ('the scheme answers this ask with a BAND GRID and nothing else — '
          '"CONTENT/COMMUNICATION 25 marks · TOP · High level of coherence · '
          'Clear argumentation · Communicative intention fulfilled … BOTTOM · '
          'Lack of coherence", and the same again for Language. Those are the '
          'qualities of a piece of writing, not answers, and a card would ask '
          'a student to tick "Idiomatic Spanish" as something they were '
          'supposed to have written.'),
    'C': ('the scheme answers this ask with a BAND GRID and nothing else — '
          '"6 marks: Communicative intention fulfilled. Verbs must be correct '
          'for full marks. · 4-5 marks: Communicative intention more or less '
          'fulfilled … 0 marks: No communication of message." Those are the '
          'qualities of a piece of writing, not answers.'),
}

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet whose own instructions read '
    '"This will be played three times: first right through, then in two '
    'segments with a long pause after each segment, and finally, right through '
    'again", and neither the booklet nor the marking scheme prints a word of '
    'what is said — this subject\'s scheme carries no CD script at all. No '
    'verified playback copy of the SEC recording is bound to this deck, so the '
    'card would be unanswerable from what it shows.')


def card_id(year, level, section, q, letter, roman):
    parts = ['es', str(year), level, section.lower()]
    if q is not None:
        parts.append(str(q))
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def _task_line(region):
    """The region's own printed instruction, without the text beneath it.

    Read down from the question head and stopped at the first line that names
    a language — which is what the instruction exists to do — or at the text's
    own first numbered paragraph. Four lines at most: past that the paper has
    stopped instructing and started printing the article.
    """
    out = []
    for raw in region.lead_lines[:4]:
        s = re.sub(r'^(?:QUESTION|Question|Q)\s*\.?\s*\d\s*\.?\s*', '', raw)
        s = re.sub(r'\(\s*\d{1,3}\s*marks?\s*\)', '', s, flags=re.I).strip()
        if not s:
            continue
        if re.match(r'^\d{1,2}\s*\.', s):
            break
        out.append(s)
        if SAYS_SPANISH.search(s) or SAYS_ENGLISH.search(s):
            break
    return ' '.join(' '.join(out).split())


def _stem_text(block):
    """A question's printed head, with its own tariff taken off.

    "(15 marks)" is printed beside the head on the paper; leaving it on the
    stem puts a tariff where the card already shows one.
    """
    text = ' '.join((block.text or '').split())
    return re.sub(r'\s*\(\s*\d{1,3}\s*marks?\s*\)\s*', ' ', text, flags=re.I).strip()


def source_material(P, token, region, language, level, year):
    """The pages this card's text is printed on, in the booklet that prints it."""
    if token == 'B' and level == 'hl' and P.insert_pages:
        return {
            'kind': 'source-text',
            'label': 'SECTION B — LOOSE SHEET',
            'title': f'{P.insert_title or "Section B text"} — answer in {language}',
            'pages': list(P.insert_pages),
            # Resolved by build-deck.mjs from Paper Trail's index, never typed:
            # this document is NOT the question paper, and defaulting to the
            # paper's own id would open the wrong booklet.
            'sourceLabel': 'Section B',
            'attribution': (f'SEC Spanish {year} {LEVEL_TITLE[level]} Level '
                            f'examination — Section B text, printed on the loose '
                            f'sheet supplied with the paper. '
                            f'© State Examinations Commission.'),
            'presentationNote': (
                'The examination supplies this text on a separate loose sheet. '
                'Read it exactly as it was printed, then answer.'),
        }
    pages = region.text_pages or region.pages
    if not pages:
        return None
    # The text's own name, as the paper heads it: the article's title where it
    # prints one, and Higher Section A's prescribed-literature line — "1. (a)
    # Prescribed Literature: Gabriel García Márquez: Relato de un náufrago." —
    # where it prints prose with no title at all.
    head = re.sub(r'^(?:1\s*\.\s*)?\(\s*[ab]\s*\)\s*', '',
                  region.lead_lines[0] if region.lead_lines else '')
    title = (region.title or (head if head.lower().startswith('prescribed')
                              else '') or _task_line(region)
             or 'Reading comprehension').rstrip(' .:;,')
    return {
        'kind': 'source-text',
        'label': 'READING COMPREHENSION',
        'title': f'{title[:80]} — answer in {language}',
        'pages': list(pages),
        'attribution': (f'SEC Spanish {year} {LEVEL_TITLE[level]} Level examination '
                        f'paper — © State Examinations Commission.'),
        'presentationNote': ('Read the text exactly as the examination printed '
                             'it, then answer.'),
    }


def build():
    cards = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    excluded = []

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year in YEARS:
        for level in LEVELS:
            _sitting(year, level, cards, refuse)
    return cards, refused, examples, excluded


def _sitting(year, level, cards, refuse):
    P = EsPaper(year, level, SUBJECT)
    S = EsScheme(year, level, SUBJECT)
    by_key = S.by_key()
    grids = S.grids
    leaves = P.leaves()

    for q, letter, text, _page in P.aural_asks():
        ref = ref_for(year, level, 'L', q, letter, None)
        refuse('the ask needs the recording, which no card can carry', ref,
               f'{year} {level.upper()} Listening Comprehension Test, '
               f'Question {q}: {AUDIO_EVIDENCE}')

    for key in sorted(leaves, key=lambda k: tuple(str(x) for x in k)):
        section, q, letter, roman = key
        text, token, block = leaves[key]
        ref = ref_for(year, level, section, q, letter, roman)
        region = P.regions[token]

        if section in ('B', 'C') and (
                key in grids or (section, q, None, None) in grids
                or (section, q, letter, None) in grids):
            line = (grids.get(key) or grids.get((section, q, letter, None))
                    or grids.get((section, q, None, None)))
            refuse('the scheme prints a band grid for this ask, not an answer',
                   ref, f'{year} {level.upper()} scheme, "{line}": '
                        f'{GRID_EVIDENCE[section]}')
            continue

        ask = by_key.get(key)
        if ask is None:
            # A part the scheme priced under its parent: Higher Section A's
            # journalistic Q.4 is one 6-mark ask whose two phrases the paper
            # prints as (a) and (b).
            ask = by_key.get((section, q, None, None)) \
                or by_key.get((section, None, letter, None))
        if ask is None:
            refuse('the scheme prices no answer for this printed ask', ref,
                   f'{year} {level.upper()} scheme: no entry addresses '
                   f'{ref.split(" ", 2)[2]}')
            continue
        if ask.fault:
            refuse('the two halves of the printed tariff disagree, so neither '
                   'can be trusted and the ask cannot be priced', ref,
                   f'{year} {level.upper()} scheme, {ask.section} Q{ask.q}: '
                   f'{ask.fault}')
            continue

        stem_block = region.stems().get(q if section != 'A2' else letter)
        stem = _stem_text(stem_block) if stem_block else ''
        instruction = _task_line(region)
        if not stem and level == 'ol':
            stem = instruction
        question = block.printed if block else text

        language = answer_language(question, stem, instruction)
        rule = S.unit_rules.get(CARD_SECTION.get(section, 'A'))
        rows = _rows_for(ask, language, rule)
        if rows is None:
            refuse('the scheme states a direction to the examiner where the '
                   'answer would be, not an answer', ref,
                   f'{year} {level.upper()} scheme, {ask.section} Q{ask.q}'
                   f'{ask.letter or ""}: '
                   f'"{(ask.points[0][0] if ask.points else "; ".join(ask.notes))[:140]}"')
            continue
        if isinstance(rows, str):
            refuse(rows, ref, f'{year} {level.upper()} scheme, {ask.section} '
                              f'Q{ask.q}{ask.letter or ""}, tariff '
                              f'{"+".join(map(str, ask.terms or []))}')
            continue

        # The prescribed text is named on the paper's own HEAD line — "(a)
        # Prescribed Literature: Gabriel García Márquez: Relato de un
        # náufrago." — and nowhere else. Matching against the whole region
        # lead searched the EXTRACT too, and eight cards were filed under El
        # medallón perdido because the word "medalla" happens to appear in the
        # náufrago passage.
        head = region.lead_lines[0] if region.lead_lines else ''
        topic = topic_for(level, section,
                          head if section == 'A1a'
                          else (region.title or instruction))
        if topic is None:
            refuse('the paper does not name which prescribed text it has set, '
                   'so the card cannot be filed against one', ref,
                   f'{year} {level.upper()} paper, Section A Question 1(a): '
                   f'"{region.lead[:110]}"')
            continue

        card = {
            'id': card_id(year, level, section, q, letter, roman),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': CARD_SECTION[section],
            'topicId': topic,
            'conceptId': concept_for(question),
            'questionRef': ref,
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': ask.total,
            'rows': rows,
            'notes': (
                f'The scheme prices this ask '
                f'{"+".join(map(str, ask.terms or []))} marks; the paper prints '
                f'it on page {block.page + 1 if block else region.pages[0]} of '
                f'the question booklet.'),
        }
        if stem and len(stem) >= 15 and stem != question:
            card['stem'] = stem
        source = source_material(P, token, region, language, level, year)
        if source:
            card['sourceMaterial'] = source
        cards.append(card)


def _rows_for(ask, language, rule):
    """The card's marking rows, or None (a direction) or a refusal string."""
    note = language_note(language, rule)
    if ask.notes:
        note += (' The scheme adds: '
                 + '; '.join(f'“{n}”' for n in ask.notes[:3]) + '.')
    if ask.total is None or not ask.terms:
        return None
    if ask.quota:
        if not ask.options:
            return None
        if len(ask.terms) != ask.quota:
            return ('the scheme asks for a number of answers its tariff does '
                    'not price')
        options = ask.options[:MAX_OPTIONS]
        if len(options) < ask.quota:
            return 'the scheme prices more answers than it states'
        group = {'claimMax': ask.quota, 'perOption': ask.terms[0],
                 'options': options}
        if len(set(ask.terms)) > 1:
            # A descending tariff — "[First correct answer=4m]" then 3 and 3 —
            # is paid step by step, and perOptionSteps is the field the
            # renderer and the tariff gate both read.
            group['perOptionSteps'] = list(ask.terms)
        contextNote = note
        if len(ask.options) > MAX_OPTIONS:
            contextNote += (f' The scheme lists {len(ask.options) - MAX_OPTIONS} '
                            f'further accepted answer(s) beyond the ones shown.')
        return [{'id': 'r-1', 'kind': 'anyN',
                 'verbatim': 'The answers the scheme accepts',
                 'marks': None, 'contextNote': contextNote, 'group': group}]
    if not ask.points:
        return None
    if any(DIRECTION_ONLY.match(text) for text, _m in ask.points):
        return None
    if len(ask.points) > MAX_ROWS:
        return 'the scheme states more separate answers than one card may show'
    if sum(m or 0 for _t, m in ask.points) != ask.total:
        return 'the scheme\'s answers do not add up to the tariff it prints'
    return [{'id': f'r-{i}', 'kind': 'point', 'verbatim': text, 'marks': marks,
             **({'contextNote': note} if i == 1 else {})}
            for i, (text, marks) in enumerate(ask.points, start=1)]


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/spanish.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded = build()

    if args.exclusions:
        path = os.path.join(DIR, 'exclusions', f'{SUBJECT}.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(excluded, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'{len(excluded)} exclusion(s) written to {path}')
        return 0

    if args.report:
        census = census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} paper asks '
              f'({100 * len(cards) / total:.1f}%), {len(excluded)} refused')
        rows = sum(len(c['rows']) for c in cards)
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        print(f'{rows} marking rows holding {opts} stated answer(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:12} {n}')
        by_lang = collections.Counter(
            'Spanish' if 'answered in Spanish' in c['rows'][0].get('contextNote', '')
            else 'English' for c in cards)
        print(f'   answer language: {dict(by_lang)}')
        by_source = collections.Counter(
            (c.get('sourceMaterial') or {}).get('sourceLabel', 'question paper')
            for c in cards)
        print(f'   source booklet: {dict(by_source)}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:40 if args.all else 3]:
                print(f'             {e}')
        return 0

    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
