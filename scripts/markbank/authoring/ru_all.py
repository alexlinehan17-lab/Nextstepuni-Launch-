#!/usr/bin/env python3
"""Author every Russian ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/ru_all.py --report
    python3 scripts/markbank/authoring/ru_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/ru_all.py > scripts/markbank/authored/russian.json

Census-driven: the ten sittings print 478 leaf asks across two booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (ru_paper.py) and its
marking points from the SCHEME (ru_scheme.py).

HOW THE TWO ARE JOINED
----------------------
On the WORDING, which is Law 4's own rule and which this subject makes easy:
the scheme reprints the English half of the ask above its answers, verbatim,
in every comprehension and every retrieval text. The paper's own address is
the one cited even where the scheme disagrees — the 2021 Ordinary scheme
numbers a retrieval text's last two asks "(vii)" and "(vii)" where the paper
prints "(vii)" and "(viii)", and 2022 Ordinary numbers in romans what the
paper numbers 1 to 6.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is drawn from a text printed only in the question paper.
Each card binds `sourceMaterial` to the pages of the QUESTION paper the
question was printed under — never the scheme, which is where the answers are.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Comprehension and retrieval are answered in English or Irish; language
awareness is answered in Russian. The scheme prices the difference on its own
first page — "When it should be Russian: award NO marks" — so every card says
which (ru_topics.answer_language).

THE LESSER ANSWERS, AND WHY THEY ARE A NOTE
-------------------------------------------
The scheme prints, under the full answer, the shorter forms that earn part of
the marks — "assign 1 mark: • they saw a cat", "• Cheap 1 mark". They ship as
a note on the row, verbatim and with the marks the scheme prints, because
`RowKind` has no kind for a rung worth less than the row above it and the type
says why: add it together with its renderer, not before.

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
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from ru_paper import RuPaper                                   # noqa: E402
from ru_scheme import RuScheme, READING_UNITS, UNIT_NAME       # noqa: E402
from ru_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, RUSSIAN)
from paper_census import (census_subject, RU_WHOLE_UNITS,      # noqa: E402
                          RU_CHOICE_UNITS, RU_NUMBERED_UNITS)
import cardlint                                                # noqa: E402

SUBJECT = 'russian'
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts. A Higher summary ask lists up to seventeen accepted
# points for its eight content marks; the list is trimmed in the SEC's own
# printed order and the trim is DISCLOSED on the row, which is the pattern the
# bank already uses for an over-cap menu.
MAX_OPTIONS = 16
# How many lesser answers a card's note shows before it says it is trimming.
MAX_RUNGS = 6


def card_id(year, level, unit, item, roman, suffix=None):
    parts = ['ru', str(year), level, unit.lower()]
    if item is not None:
        parts.append(str(item))
    if roman:
        parts.append(roman)
    if suffix:
        parts.append(suffix)
    return '-'.join(parts)


def question_ref(year, level, unit, item=None, roman=None):
    ref = f'{year} {level.upper()} Section {unit} Q'
    if item is not None:
        ref += str(item)
    if roman:
        ref += f'({roman})'
    return ref


def source_material(P, unit, language, level, year):
    """The printed matter this ask is answered from, in the QUESTION paper."""
    pages = P.unit_pages.get(unit)
    if not pages:
        return None
    return {
        'kind': 'source-text',
        'label': UNIT_NAME.get(unit, unit).split(' — ')[0].upper(),
        'title': f'{UNIT_NAME.get(unit, unit)} — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC Russian {year} {LEVEL_TITLE[level]} Level '
                        f'examination paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the printed material exactly as the examination set it, then '
            'answer. ' + language_note(language)),
    }


def ladder_note(rungs):
    """The lesser answers, verbatim, with the marks the scheme prints."""
    # A rung worth NOTHING is not part marks: 2022 prints "assign no marks:
    # warm weather" to tell the examiner what does not pay, and a note saying
    # the scheme "also pays part marks" for it would be false.
    kept = [(t, m) for t, m in rungs if t and m]
    if not kept:
        return ''
    shown = kept[:MAX_RUNGS]
    parts = '; '.join(f'“{t}” {m} {"mark" if m == 1 else "marks"}'
                      for t, m in shown)
    tail = (f' The scheme lists {len(kept) - len(shown)} further lesser '
            f'answer(s) for this ask.' if len(kept) > len(shown) else '')
    return (f' The scheme also pays part marks for a shorter answer: '
            f'{parts}.{tail}')


# ------------------------------------------------ what is not an answer ----
ESSAY_EVIDENCE = (
    'the scheme answers this ask with a BAND GRID and nothing else. It prices '
    'the essay "Content (C) = 10 marks; Language + expression (E) = 20 marks" '
    'and then describes the bands in prose — "18-20 Rich and complex language, '
    'employing a wide range of appropriate lexis. Tone and register wholly '
    'suited to chosen task. Almost flawless in terms of accuracy." Those are '
    'qualities of a piece of writing, not answers, and the only content it '
    'states is the rule that pays them: "Award 2 marks for each relevant '
    'content detail (up to a maximum of 10 marks)", with no detail named.')

WRITING_EVIDENCE = (
    'the scheme answers the guided-writing question with a BAND GRID and '
    'nothing else: "1. Communication + content (C) = 15 marks; 2. Language + '
    'expression (E) = 15 marks; 3. Textual coherence (TC) = 10 marks", then '
    '"9-10 Excellent organisation. A high degree of coherence throughout" and '
    '"Vocabulary use good – rich, idiomatic and appropriate. Spelling mistakes '
    'rare, grammar generally correct." Where it lists points at all they are '
    'the communicative tasks the PAPER printed in the question itself — '
    '"opening (A)", "where the cat lives now (B)" — not answers to it.')

SHORT_ANSWER_EVIDENCE = (
    'the scheme answers Ordinary\'s short-answer question with a content RULE '
    'and a coherence grid, and names no content at all: "Allocate 8 marks for '
    'each correct idea/concept up to a maximum of 24 marks. There must be some '
    'Russia-specific information in the detail for 8 marks to be awarded", '
    'then "6 marks Excellent organisation. A high degree of coherence '
    'throughout". A candidate writes three to five sentences on one of five '
    'printed topics and the scheme states not one of the facts that would earn '
    'the marks.')

EXTENDED_EVIDENCE = (
    'the scheme answers Ordinary\'s extended-writing question with a band grid '
    'and repeats the paper\'s own prompts, saying so in its own words: "The '
    'prompts for the questions below are suggestions only." The prompts are '
    'the question ("When were you in the camp?", "Who were you with?"), not '
    'the answer, and the marks are awarded against "Content", "Expression" and '
    '"Textual coherence" descriptors.')

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet whose own instructions read '
    '"Seinnfear an t-ábhar trí huaire: an chéad uair ó thús deireadh, ansin '
    'ina thrí mhír agus sosanna eatarthu" — the material will be played three '
    'times, first right through, then in three segments with pauses — and the '
    'paper prints no text of what is said. The only printed source of that '
    'material is the marking scheme\'s own "APPENDIX 2: AURAL TEXTS", the '
    'ANSWER document, so carrying it on the card would hand the student the '
    'answers with the question. No verified playback copy of the SEC '
    'recording is bound to this deck, so the card would be unanswerable from '
    'what it shows.')

REFUSAL_EVIDENCE = {
    'SE': ESSAY_EVIDENCE, 'GW': WRITING_EVIDENCE,
    'SA': SHORT_ANSWER_EVIDENCE, 'EW': EXTENDED_EVIDENCE,
}
BAND_UNITS = ('SE', 'GW', 'SA', 'EW')
# The questions that set one instruction over a printed table or menu.
TASK_UNITS = ('LA1', 'LA2', 'CA1')


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
            P = RuPaper(year, level, SUBJECT)
            S = RuScheme(year, level, SUBJECT)
            _reading(P, S, year, level, cards, refuse)
            _other_units(P, S, year, level, cards, refuse)
            _listening(P, year, level, refuse)
    return cards, refused, examples, excluded


# ------------------------------------------------------ the reading asks ----
def _reading(P, S, year, level, cards, refuse):
    claimed = set()
    for ask in S.asks:
        if ask.unit not in READING_UNITS:
            continue
        hit = P.find(ask.unit, ask.item, ask.roman, ask.cue, claimed)
        if hit is None:
            refuse('no printed question in the paper matches the ask the '
                   'scheme reprints', S.ref(ask),
                   f'{year} {level.upper()} scheme, {ask.unit}: '
                   f'{ask.cue[:110]!r}')
            continue
        text, page, block = hit
        claimed.add(id(block))
        _one_card(P, S, ask, text, page, block, year, level, cards, refuse)


def _one_card(P, S, ask, text, page, block, year, level, cards, refuse):
    ref = question_ref(year, level, block.unit, block.item, block.roman)
    where = f'{year} {level.upper()} scheme, {block.unit} {ask.label}'
    if ask.fault:
        refuse('the scheme prices the ask two ways that disagree', ref,
               f'{where}: {ask.fault}')
        return
    if ask.total is None:
        refuse('the scheme prints no tariff this reads for the ask', ref, where)
        return
    answers = [t for t, _m in ask.answers if t and t.strip()]
    if not answers:
        refuse('the scheme states no answer for this ask', ref, where)
        return
    if cardlint.NAMES_LETTERS.search(text):
        refuse('the ask points at printed matter the card cannot carry', ref,
               f'{year} {level.upper()} paper: "{text[:110]}"')
        return

    language = answer_language(block.unit, text)
    claim = ask.claim or 1
    per = ask.per
    if per is None:
        refuse('the scheme prints no tariff this reads for the ask', ref, where)
        return
    if len(answers) < claim:
        refuse('the scheme asks for more answers than it states', ref,
               f'{where}: {claim} wanted, {len(answers)} stated')
        return

    shown = answers[:MAX_OPTIONS]
    total = ask.content if ask.content is not None else ask.total
    note = language_note(language) + ladder_note(ask.rungs)
    if ask.content is not None:
        note += (' ' + S.unit_split_words.get(block.unit, '').rstrip(':') +
                 f'. This card carries the {ask.content} content marks; the '
                 f'other {ask.discretionary} are awarded for how the paragraph '
                 f'is written.')
    if len(answers) > len(shown):
        note += (f' The scheme lists {len(answers) - len(shown)} further '
                 f'accepted answer(s) than this card shows, in the order it '
                 f'prints them.')

    if claim == 1 and len(shown) == 1:
        rows = [{'id': 'r-1', 'kind': 'point', 'verbatim': shown[0],
                 'marks': total, 'contextNote': note.strip()}]
    else:
        rows = [{'id': 'r-1', 'kind': 'anyN',
                 'verbatim': 'The answers the scheme accepts in full',
                 'marks': None, 'contextNote': note.strip(),
                 'group': {'claimMax': claim, 'perOption': per,
                           'options': shown}}]
        if claim * per != total:
            refuse('the scheme prices the ask two ways that disagree', ref,
                   f'{where}: {claim} answer(s) at {per} is {claim * per}, '
                   f'and the ask is priced {total}')
            return

    cards.append({
        'id': card_id(year, level, block.unit, block.item, block.roman),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': block.unit,
        'topicId': topic_for(block.unit),
        'conceptId': concept_for(text),
        'questionRef': ref,
        'questionText': text,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': total,
        'rows': rows,
        'notes': (_tariff_note(ask, claim, per) +
                  f' The paper prints this ask on page {page} of the question '
                  f'booklet.'),
        **({'sourceMaterial': src} if (src := source_material(
            P, block.unit, language, level, year)) else {}),
    })


def _tariff_note(ask, claim, per):
    """Where the card's tariff came from, in the scheme's own terms."""
    if ask.notation:
        return f'The scheme prints the tariff as {ask.notation!r};'
    return (f'The scheme prints no tariff beside this ask: it states {per} '
            f'marks for each correct idea, the ask itself asks for {claim}, '
            f'and {claim} at {per} is the total its own question head prints.')


# ------------------------------------------------ the paper's other asks ----
# A task question's own instruction, lifted from the paper, must read as one.
# A run this reader could not resolve — "English or Russian)", "Russian." —
# is a fragment of the instruction, not the instruction, and a card whose
# question is a fragment is the wrong card.
MIN_INSTRUCTION_WORDS = 6


def _task_cards(P, S, unit, year, level, cards, refuse):
    """The language- and cultural-awareness questions, where they validate.

    Each is one printed instruction over a printed TABLE or MENU, and each
    alternative the paper offers is its own census leaf. Nothing here is
    inferred: the tariff is the one the scheme prints, the answers are the
    ones it states, and every one of the four things a card needs — an
    instruction lifted from the paper, a printed tariff, stated answers, and a
    count that agrees with the tariff — is checked before a card is built. A
    task that fails any of them is refused with what failed as its evidence.
    """
    romans = P.choice_romans(unit)
    tasks = S.tasks(unit)
    refs = _unit_refs(P, unit, year, level)
    if romans and len(tasks) != len(romans):
        for ref in refs:
            refuse('the paper and the scheme print a different number of '
                   'alternatives for this task', ref,
                   f'{year} {level.upper()} {UNIT_NAME.get(unit, unit)}: the '
                   f'paper prints {len(romans)} alternative(s) and the scheme '
                   f'answers {len(tasks)}')
        return
    if not romans and len(tasks) != 1:
        for ref in refs:
            refuse('the paper and the scheme print a different number of '
                   'alternatives for this task', ref,
                   f'{year} {level.upper()} {UNIT_NAME.get(unit, unit)}: the '
                   f'paper prints one task and the scheme answers {len(tasks)}')
        return
    for i, task in enumerate(tasks):
        roman = romans[i] if i < len(romans) else None
        ref = question_ref(year, level, unit, None, roman)
        _one_task_card(P, S, task, unit, roman, ref, year, level, cards, refuse)


def _one_task_card(P, S, task, unit, roman, ref, year, level, cards, refuse):
    where = f'{year} {level.upper()} scheme, {UNIT_NAME.get(unit, unit)}'
    if task.cursive:
        refuse('the scheme states no answer for this task', ref,
               f'{where}: the task asks the candidate to write phrases the '
               f'paper has already printed in cursive script, and the scheme '
               f'answers it with a marking instruction and nothing else — '
               f'"Three phrases in handwritten/cursive script. 3 x 2 marks. '
               f'2 marks per phrase. Do not penalise for repeated errors. '
               f'Take a global view. Award 2 marks if answer is almost '
               f'completely correct." There is no answer to lift: the answer '
               f'is the candidate\'s own handwriting.')
        return
    tariff = task.tariff or S.unit_tariffs.get(unit)
    if tariff is None and task.rate:
        # No "N x M marks" on the task and none on its head, but the scheme
        # states a RATE — "Give two marks for each correct answer" — and the
        # question states a total. The claim is then the count the ask itself
        # prints, or, where it prints none, the number of answers the scheme
        # states; either is read only where rate times claim reaches the
        # printed total exactly, which is the same checksum the reading asks
        # are priced under and not an average of anything.
        expected = S.expected_total(unit)
        for want in (S._count_wanted(task.instruction),
                     len(task.pairs) or len(task.options)):
            if want and expected and want * task.rate == expected:
                tariff = (want, task.rate, expected)
                break
    if tariff is None:
        refuse('the scheme prints no tariff this reads for the task', ref,
               f'{where}: the task prints no "N x M marks" of its own, its '
               f'question head prints none, and its stated rate does not '
               f'divide the total the unit prints')
        return
    claim, per, total = tariff
    text = P.instruction(unit, roman, task.instruction)
    if not text or len(text.split()) < MIN_INSTRUCTION_WORDS:
        refuse('no printed instruction in the paper matches the task the '
               'scheme answers', ref,
               f'{where}: the scheme reprints {task.instruction[:80]!r} and '
               f'the paper\'s own English column yields {text!r}')
        return
    language = answer_language(unit, text + " " + " ".join(task.lines[:3]))

    if task.pairs:
        if len(task.pairs) < claim:
            refuse('the scheme states fewer answers than its own tariff pays '
                   'for', ref,
                   f'{where}: {claim} wanted, {len(task.pairs)} stated')
            return
        options = [f'{left} — {right}' for left, right in task.pairs]
    elif task.options:
        if len(task.options) < claim:
            refuse('the scheme states fewer answers than its own tariff pays '
                   'for', ref,
                   f'{where}: {claim} wanted, {len(task.options)} stated')
            return
        options = task.options
    else:
        refuse('the scheme states no answer for this task', ref, where)
        return

    shown = options[:MAX_OPTIONS]
    note = language_note(language)
    if len(options) > len(shown):
        note += (f' The scheme lists {len(options) - len(shown)} further '
                 f'accepted answer(s) than this card shows, in the order it '
                 f'prints them.')
    row = {'id': 'r-1', 'kind': 'anyN',
           'verbatim': 'The answers the scheme accepts in full',
           'marks': None, 'contextNote': note,
           'group': {'claimMax': claim, 'perOption': per, 'options': shown}}
    if task.open:
        row['openList'] = True
        row['contextNote'] += (' The scheme closes this list "This list is '
                               'not exhaustive", so another word of the same '
                               'field earns the marks too.')
    cards.append({
        'id': card_id(year, level, unit, None, roman),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': unit,
        'topicId': topic_for(unit),
        'conceptId': concept_for(text),
        'questionRef': ref,
        'questionText': text,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': total,
        'rows': [row],
        'notes': (f'The scheme prices this task {claim} x {per} marks; the '
                  f'paper prints it on page '
                  f'{P.unit_pages.get(unit, ["?"])[0]} of the question '
                  f'booklet.'),
        **({'sourceMaterial': src} if (src := source_material(
            P, unit, language, level, year)) else {}),
    })


def _other_units(P, S, year, level, cards, refuse):
    """Every printed question that is not a comprehension and not the aural.

    Each is refused for its own reason, with the scheme's own words as the
    evidence, and each refusal lands on the census leaf the paper prints.
    """
    for unit in RU_WHOLE_UNITS:
        if unit not in P.unit_pages:
            continue
        if unit in TASK_UNITS:
            _task_cards(P, S, unit, year, level, cards, refuse)
            continue
        if unit in BAND_UNITS:
            reason = 'the scheme prints a band grid for this ask, not an answer'
            evidence = (f'{year} {level.upper()} scheme, '
                        f'{UNIT_NAME.get(unit, unit)}: '
                        f'{REFUSAL_EVIDENCE[unit]}')
        else:
            reason, evidence = _task_refusal(S, unit, year, level)
        for ref in _unit_refs(P, unit, year, level):
            refuse(reason, ref, evidence)


def _unit_refs(P, unit, year, level):
    romans = P.choice_romans(unit) if unit in RU_CHOICE_UNITS else []
    items = P.unit_items(unit) if unit in RU_NUMBERED_UNITS else []
    if romans:
        return [question_ref(year, level, unit, None, r) for r in romans]
    if items:
        return [question_ref(year, level, unit, i, None) for i in items]
    return [question_ref(year, level, unit)]


TASK_REASON = ('the scheme prints this task\'s answers as a printed KEY the '
               'card cannot pair to the printed prompts')
TASK_EVIDENCE = {
    'GR': ('the scheme answers the grammar question by reprinting the whole '
           'passage with the corrected forms inside the brackets the paper '
           'left blank — "И только через девять (часов) поздравляют друг друга '
           'с праздником москвичи" against the paper\'s "через девять (часы) '
           '……………" — and prices it "Award 2 marks per correct form: 15 x 2 '
           'marks". The answers are stated, but each is stated only in its '
           'place in a 300-word passage: a card would have to reproduce the '
           'passage and the fifteen blanks in it, and this deck has no row '
           'kind for a gap-fill.'),
    'MM': ('the scheme answers the matching task with the numbers alone, '
           'printed against the ten Russian items — "2 Мы забросим как можно '
           'больше мячей в корзину!" — and prices it "B. MIX AND MATCH 10 x 4 '
           'marks". Half of each answer is the numbered list the PAPER prints '
           'and the scheme never reproduces, so nothing this card could show '
           'would let the answer be checked against what the scheme states.'),
    'SD': ('the scheme answers the structuring task the same way: at Higher '
           'the ten news items with the genre number printed beside each, at '
           'Ordinary the dialogue reprinted with the missing words already in '
           'place. Both state the answer only in a printed layout — a number '
           'in a box, a word in a gap — and this deck has no row kind for '
           'either.'),
    'LA1': None, 'LA2': None, 'CA1': None,
}
LA_EVIDENCE = (
    'the language-awareness question sets a TABLE — five verbs to put into the '
    'infinitive, five noun phrases whose case is to be named, five words to be '
    'matched to a part of speech — and the scheme answers it by reprinting the '
    'table with its second column filled in ("стали стать", "мы с подругой '
    'Instrumental case / Творительный падеж"). The prompts are the paper\'s '
    'column and the answers are the scheme\'s, and this deck has no row kind '
    'for a two-column table; where the task is instead "find five words '
    'related to Employment and list them in Russian" the scheme prints a menu '
    'it closes with "This list is not exhaustive", so no bounded set of '
    'answers is stated either.')


def _task_refusal(S, unit, year, level):
    evidence = TASK_EVIDENCE.get(unit) or LA_EVIDENCE
    return TASK_REASON, (f'{year} {level.upper()} scheme, '
                         f'{UNIT_NAME.get(unit, unit)}: {evidence}')


def _listening(P, year, level, refuse):
    for unit, item, roman, _text in P.aural_asks():
        refuse('the ask needs the recording, which no card can carry',
               question_ref(year, level, unit, item, roman),
               f'{year} {level.upper()} Listening Comprehension Test, '
               f'{UNIT_NAME.get(unit, unit)}: {AUDIO_EVIDENCE}')


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/russian.json from the refusals')
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
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        points = sum(1 for c in cards for r in c['rows'] if not r.get('group'))
        print(f'{sum(len(c["rows"]) for c in cards)} marking rows: '
              f'{points} stated answer(s) and {opts} menu option(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:14} {n}')
        by_lang = collections.Counter(
            RUSSIAN if f'in {RUSSIAN}' in (c.get('sourceMaterial') or {}).get(
                'title', '') else 'English or Irish' for c in cards)
        print(f'   answer language: {dict(by_lang)}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:40 if args.all else 3]:
                print(f'             {e}')
        return 0

    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
