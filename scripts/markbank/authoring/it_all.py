#!/usr/bin/env python3
"""Author every Italian ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/it_all.py --report
    python3 scripts/markbank/authoring/it_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/it_all.py > scripts/markbank/authored/italian.json

Census-driven: the ten sittings print 705 leaf asks across two booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (it_paper.py) and its
marking points from the SCHEME (it_scheme.py).

HOW THE TWO ARE JOINED
----------------------
Not on the part key, and not on wording either — this scheme never reprints the
question it is answering, so there is no wording to score. They are joined on
what BOTH documents print: the SECTION, and the ORDER inside it. That is only
safe because two independent counts say the two documents hold the same asks:

  * every reading section in every sitting prices its asks to exactly the total
    it prints on its own head (it_scheme's checksum, ten sittings, no
    disagreements), so no ask inside one was lost by either reader;
  * the number of asks the paper prints in a section equals the number the
    scheme prices in it, in all ten sittings and all 385 reading asks.

Where the two disagree about an ask's NAME — four times in the corpus, all of
them the SEC leaving the "(a)" off an item's first part — the census flags it
and the PAPER's name is the one cited, because the paper is what the student is
holding.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is drawn from a passage, an advertisement or a literary
extract printed only in the question paper, on the page facing the questions.
Each card binds `sourceMaterial` to that page in the QUESTION paper — never the
scheme, which is where the answers are.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Higher sets its reading questions in Italian and answers them in Italian; the
last ask of each comprehension is set in Irish and English and answered in one
of those; Ordinary is set and answered in Irish or English throughout. A card
that does not say which marks a right answer wrong, so every card says it
(it_topics.answer_language).

THE LESSER ANSWERS, AND WHY THEY ARE A NOTE
-------------------------------------------
Both levels print, under the full answer, the shorter forms that earn part of
the marks — "(Best friend +/- extra information 4 marks)". They ship as a note
on the row, verbatim and with the marks the scheme prints, because `RowKind`
has no kind for a rung worth less than the row above it and the type says why:
add it together with its renderer, not before.

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report, and every
refusal that lands on a census leaf becomes an exclusions entry carrying the
scheme evidence for it (--exclusions writes them).
"""
import argparse
import collections
import json
import re
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from it_paper import ItPaper                                  # noqa: E402
from it_rows import split_priced                              # noqa: E402
from it_scheme import ItScheme, confirm_headings              # noqa: E402
from it_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, ITALIAN, SEQUENCING)
from paper_census import census_subject                       # noqa: E402
import cardlint                                               # noqa: E402

SUBJECT = 'italian'
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts. The twenty-mark summary ask at the end of a Higher
# comprehension lists up to twenty indicative points, and a card showing them
# all would be a wall of text rather than a question. The list is trimmed in
# the SEC's own printed order and the trim is DISCLOSED on the row, which is
# the pattern the bank already uses for an over-cap menu.
MAX_OPTIONS = 25      # the build's MAX_LONG_OPTION_ROWS: never drop a printed answer
# How many lesser answers a card's note shows before it says it is trimming.
MAX_RUNGS = 40      # every shorter answer the scheme prices is quoted: never drop one

# The name the section takes on the card. `SecCardBase.section` is a single
# letter, and the paper's own sections are A, B and C.
CARD_SECTION = {'A': 'A', 'B': 'B', 'C': 'C'}


def card_id(year, level, section, item, letter, suffix=None):
    parts = ['it', str(year), level, section.lower()]
    if item is not None:
        parts.append(str(item))
    if letter:
        parts.append(letter)
    if suffix:
        parts.append(suffix)
    return '-'.join(parts)


def question_ref(year, level, section, item, letter, letter_to=None):
    ref = f'{year} {level.upper()} Section {section} Q'
    if item is not None:
        ref += str(item)
    if letter:
        ref += f'({letter})'
        if letter_to:
            ref += f'–({letter_to})'
    return ref


SECTION_TITLE = {
    'A': 'Journalistic passage', 'A1': 'Reading comprehension 1',
    'A2': 'Reading comprehension 2', 'B1': 'Unseen literary passage',
    'B2A': 'Prescribed novel — passage A',
    'B2B': 'Prescribed novel — passage B',
}


def source_material(P, token, language, level, year):
    """The printed matter this ask is answered from, in the QUESTION paper."""
    pages = P.source_pages.get(token)
    if not pages:
        return None
    if level == 'ol' and token.startswith('B'):
        title = f'Publicity piece {token[1:]}'
    else:
        title = SECTION_TITLE.get(token, f'Section {token}')
    return {
        'kind': 'source-text',
        'label': f'SECTION {token}',
        'title': f'{title} — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC Italian {year} {LEVEL_TITLE[level]} Level '
                        f'examination paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the printed material exactly as the examination set it, then '
            'answer. ' + language_note(language)),
    }


# A list bullet marks a printed line; it is not part of the answer quoted.
LIST_BULLET = re.compile(r'^[•●▪■]\s*')


def ladder_note(rungs, language):
    """The lesser answers, verbatim, with the marks the scheme prints."""
    kept = [(LIST_BULLET.sub('', t), m) for t, m in rungs if t and m is not None]
    if not kept:
        return language_note(language)
    shown = kept[:MAX_RUNGS]
    parts = '; '.join(f'“{t}” {m} {"mark" if m == 1 else "marks"}'
                      for t, m in shown)
    tail = (f' The scheme lists {len(kept) - len(shown)} further lesser '
            f'answer(s) for this ask.' if len(kept) > len(shown) else '')
    return (f'{language_note(language)} The scheme also pays part marks for a '
            f'shorter answer: {parts}.{tail}')


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
            P = ItPaper(year, level, SUBJECT)
            S = ItScheme(year, level, SUBJECT)
            _reading(P, S, year, level, cards, refuse)
            _essay(P, year, level, refuse)
            _writing(P, year, level, refuse)
            _listening(P, year, level, refuse)
    # A price the scheme prints inside an answer is a row of its own, and a
    # shorter answer it prices a printed step (it_rows.py).
    return [split_priced(card) for card in cards], refused, examples, excluded


# ------------------------------------------------- Sections A and B ---------
def _reading(P, S, year, level, cards, refuse):
    paper = P.asks()
    for token in sorted({a[0] for a in paper}):
        pp = [a for a in paper if a[0] == token]
        ss = [a for a in S.asks if a.section == token]
        if len(pp) != len(ss):
            for section, item, letter, _text, _page in pp:
                refuse('the paper and the scheme do not print the same number '
                       'of asks in this section, so nothing in it can be paired',
                       question_ref(year, level, section, item, letter),
                       f'{year} {level.upper()} Section {token}: the paper '
                       f'prints {len(pp)} ask(s), the scheme prices {len(ss)}')
            continue
        matching = any(a.notation == 'matching' for a in ss)
        if matching:
            _matching_card(P, S, pp, ss, token, year, level, cards, refuse)
            continue
        for (section, item, letter, text, page), ask in zip(pp, ss):
            _one_card(P, S, section, item, letter, text, page, ask,
                      year, level, cards, refuse)


def _one_card(P, S, section, item, letter, text, page, ask, year, level,
              cards, refuse):
    ref = question_ref(year, level, section, item, letter)
    where = f'{year} {level.upper()} scheme, Section {section} ask {ask.item}' \
            f'{ask.letter or ""}'
    if ask.fault:
        refuse('the section\'s printed total and its own asks disagree, so no '
               'tariff in it can be trusted', ref, f'{where}: {ask.fault}')
        return
    if ask.total is None:
        refuse('the scheme prints no tariff this reads for the ask', ref, where)
        return
    rows = []
    trimmed = 0
    for n, part in enumerate(ask.parts, start=1):
        row = _row_for(part, n, ask, text)
        if isinstance(row, str):
            refuse(row, ref, f'{where}: {_evidence(part)}')
            return
        for r in (row if isinstance(row, list) else [row]):
            trimmed += r.pop('_trimmed', 0)
            rows.append(r)

    language = answer_language(level, text)
    note = ladder_note([r for p in ask.parts for r in p.rungs], language)
    rows[0]['contextNote'] = f"{note} {rows[0].get('contextNote', '')}".strip()
    if trimmed:
        rows[0]['contextNote'] += (
            f' The scheme lists {trimmed} further accepted answer(s) than this '
            f'card shows, in the order it prints them.')

    if cardlint.NAMES_LETTERS.search(text):
        refuse('the ask points at printed matter the card cannot carry', ref,
               f'{year} {level.upper()} paper: "{text[:110]}"')
        return

    card = {
        'id': card_id(year, level, section, item, letter),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': CARD_SECTION[section[0]],
        'topicId': topic_for(level, section),
        'conceptId': concept_for(text),
        'questionRef': ref,
        'questionText': text,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': ask.total,
        'rows': rows,
        'notes': (f'The scheme prints the tariff as '
                  f'{"; ".join(p.notation for p in ask.parts)!r}; the paper '
                  f'prints this ask on page {page} of the question booklet.'),
    }
    source = source_material(P, section, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


def _evidence(part):
    return (f'tariff {part.notation!r}, directive {part.directive!r}, '
            f'{len(part.answers)} stated answer(s): '
            + ' | '.join(a[:60] for a in part.answers[:3]))


COUNT_PRINTED = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'a': 1, 'an': 1}
SKIP_WORDS = {'any', 'three', 'five', 'the', 'and', 'from', 'with', 'her', 'his', 'one', 'two', 'four',
              'what', 'about', 'learn', 'points', 'point'}
AFTER_COUNT = re.compile(r'\(\s*(one|two|three|four)\s+(?:[a-z]+\s+)?points?\s*\)'
                         r'|\bgive\s+(one|two|three|four)\s+(?:[a-z]+\s+)?points?\b')
BEFORE_COUNT = re.compile(r'\b(one|two|three|four|a|an)\s+(?:[^\W\d_]+\s+){0,2}$')


def _heading_counts(groups, question):
    """(label, count) for each group: how many points the PAPER asks for under
    each heading the scheme prints, read from the question's own words —
    "the founders (one point)", "one advantage", "three reasons why", "What is
    Riccardo's view …? Give two points". A first group with no heading of its
    own (2019 Higher B1 Q5's points on the father, under "Four points are
    required:") takes the count the paper prints before the first heading,
    and the paper's own words for a label ("the narrator's father"). None
    where the paper does not say for every group."""
    q = ' '.join(question.split())
    low = q.lower()
    spots, start = [], 0
    for head, _answers in groups:
        if head is None:
            spots.append(None)
            continue
        words = [w for w in reversed(re.findall(r"[^\W\d_]+", head.lower()))
                 if len(w) > 2 and w not in COUNT_PRINTED and w not in SKIP_WORDS] or [
            w for w in re.findall(r"[^\W\d_]+", head.lower()) if len(w) > 2]   # "What" alone
        at = None
        for w in words:
            stem = w[:6] if len(w) >= 6 else w
            m = re.compile(r'(?<![^\W\d_])' + re.escape(stem)).search(low, start)
            if m:
                at = m.start()
                break
        if at is None:
            return None
        spots.append(at)
        start = at + 1
    named = [x for x in spots if x is not None]
    if not named or named != sorted(named):
        return None
    out = []
    for k, ((head, _answers), at) in enumerate(zip(groups, spots)):
        nxt = next((x for x in spots[k + 1:] if x is not None), len(low))
        if at is None:
            if k != 0:
                return None
            m = list(AFTER_COUNT.finditer(low[:nxt]))
            if not m:
                return None
            m = m[-1]
            lead = q[:m.start()].rstrip(' ,')
            label = ' '.join(re.split(r'\s+', re.split(r'\babout\b|\bof\b|,', lead)[-1].strip())[-3:])
            out.append((label, COUNT_PRINTED[m.group(1) or m.group(2)]))
            continue
        after = AFTER_COUNT.search(low, at, nxt)
        prev = max([x for x in spots[:k] if x is not None] or [0])
        # The count may stand before the heading's FIRST word: "two points
        # about Jacopo's hopes" (2021 Higher A Q5) is found at "hopes".
        first_word = next((w for w in re.findall(r"[^\W\d_]+", head.lower())
                           if len(w) > 2 and w not in SKIP_WORDS), None)
        lead_at = at
        if first_word:
            m0 = re.compile(r'(?<![^\W\d_])' + re.escape(first_word[:6])).search(low, prev, at + 1)
            if m0:
                lead_at = m0.start()
        before = BEFORE_COUNT.search(low[prev:lead_at]) or BEFORE_COUNT.search(low[prev:at])
        if after:
            out.append((head, COUNT_PRINTED[after.group(1) or after.group(2)]))
        elif before:
            out.append((head, COUNT_PRINTED[before.group(1)]))
        else:
            return None
    return out


def _paper_label(name, question):
    """The paper's words for an inline name: "Riccardo" -> "Riccardo's view"."""
    m = re.search(re.escape(name) + r"[’']s\s+[^\W\d_]+", ' '.join(question.split()))
    return m.group(0) if m else name


def _own_lesser(part, rows, heads):
    """Each group row quotes the shorter answers printed under its own heading;
    the first group's stay in the card's note, with any whose place is unknown."""
    groups = part.rung_groups or []
    for row, head in list(zip(rows, heads))[1:]:
        mine = [(t, m) for (t, m), g in zip(part.rungs, groups) if g == head and t and m is not None]
        if mine:
            quoted = '; '.join(f'“{LIST_BULLET.sub("", t)}” {m} {"mark" if m == 1 else "marks"}' for t, m in mine)
            row['contextNote'] = (f'The scheme also pays part marks for a shorter answer: {quoted}. '
                                  + row.get('contextNote', '')).strip()
    moved = set(heads[1:])
    keep = [k for k, g in enumerate(groups) if g not in moved] + list(range(len(groups), len(part.rungs)))
    part.rungs = [part.rungs[k] for k in keep]
    part.rung_groups = [groups[k] if k < len(groups) else None for k in keep]
    return rows


def _grouped_rows(part, n, ask, question):
    """One option group per heading the scheme prints over a twenty-mark
    summary ask, each claiming as many points as the paper asks for under it.
    Where the paper does not say how many for every heading (the novel ask:
    "the passage and the novel as a whole"), one group over every answer,
    each led by the heading the scheme prints it under."""
    counts = _heading_counts(part.groups, question) if n == 1 else None
    equal = (part.split and len(part.split) > 1 and len(set(part.split)) == 1
             and sum(part.split) == part.total)
    if part.counted and part.claim > 1 and part.split and len(part.split) != part.claim \
            and sum(part.split) == part.total and not equal:
        return None     # a count and a split that disagree: _row_for refuses it
    claim, per = part.claim, part.per
    if equal:
        # "Two of 20 marks" over "Benefit (5+5+5+5)" (2018 Higher A Q5): the
        # count is the first heading's, the split prices the whole ask.
        claim, per = len(part.split), part.split
    if per is None or len(set(per)) > 1 or not claim or claim < 2:
        return None
    heads = [h for h, _a in part.groups if h]
    full = lambda h: part.fullnames.get(h, h)
    if any(len(a) > MAX_OPTIONS for _h, a in part.groups):
        return 'the scheme prints more answers under one heading than a card can show'
    prices = part.prices or {}
    if prices and n == 1 and len(part.groups) == len(heads):
        # A heading that prices its own points, and one that does not: the
        # second takes what is left of the total, at the split's own share.
        rest = [h for h in heads if h not in prices]
        left = part.total - sum(t for _c, t, _s, _x in prices.values())
        if len(rest) == 1 and left > 0 and left % per[0] == 0:
            rows = []
            for k, (head, answers) in enumerate(part.groups, start=1):
                if head in prices:
                    count, _t, steps, printed = prices[head]
                    group = {'claimMax': count, 'perOption': steps[0], 'options': list(answers)}
                    if len(set(steps)) > 1:
                        group['perOptionSteps'] = steps
                    note = f'The scheme prints “{printed}”.'
                else:
                    count = left // per[0]
                    group = {'claimMax': count, 'perOption': per[0], 'options': list(answers)}
                    note = (f'The scheme prints these answers under the heading “{full(head)}”, '
                            f'{left} of the {part.total} marks.')
                if len(answers) < count:
                    break
                rows.append({'id': f'r-{k}', 'kind': 'anyN',
                             'verbatim': f'{head} — the answers the scheme accepts',
                             'marks': None, 'group': group, 'contextNote': note})
            else:
                return _own_lesser(part, rows, [h for h, _a in part.groups])
    if counts and sum(c for _l, c in counts) == claim \
            and all(len(a) >= c for (_h, a), (_l, c) in zip(part.groups, counts)):
        rows = []
        for k, ((head, answers), (label, count)) in enumerate(zip(part.groups, counts), start=1):
            pts = f'{count} {"point" if count == 1 else "points"}'
            if head is None:
                show, note = label, (f'The paper asks for {pts} on {label}; the scheme prints '
                                     f'these answers for it, before its first heading.')
            elif head in part.inline:
                show = _paper_label(head, question)
                note = (f'The scheme begins each of these answers with “{head}:”; the paper asks '
                        f'for {pts} on {show}.')
            else:
                show, note = head, (f'The scheme prints these answers under the heading '
                                    f'“{full(head)}”; the paper asks for {pts} on it.')
            rows.append({'id': f'r-{k}', 'kind': 'anyN',
                         'verbatim': f'{show} — the answers the scheme accepts', 'marks': None,
                         'group': {'claimMax': count, 'perOption': per[0], 'options': list(answers)},
                         'contextNote': note})
        return _own_lesser(part, rows, [h for h, _a in part.groups])
    options = [a if h is None else f'{h} — {a}' for h, answers in part.groups for a in answers]
    if len(options) > MAX_OPTIONS:
        return 'the scheme prints more answers than a card can show'
    return [{'id': f'r-{n}', 'kind': 'anyN',
             'verbatim': 'The answers the scheme accepts in full', 'marks': None,
             'group': {'claimMax': claim, 'perOption': per[0], 'options': options},
             'contextNote': (f'The scheme prints these answers under the '
                             f'heading{"s" if len(heads) > 1 else ""} '
                             + ', '.join(f'“{full(h)}”' for h in heads)
                             + '; the paper does not say how many points it wants under each.')}]


def _row_for(part, n, ask, question=None):
    """One marking row for one priced component, or the reason there is none.
    A twenty-mark summary ask whose scheme prints two or more headings gets a
    list of rows, one option group per heading."""
    if question is not None:
        confirm_headings(part, question)
    rows = _row_for_settled(part, n, ask, question)
    if isinstance(rows, str):
        return rows
    first = rows[0] if isinstance(rows, list) else rows
    noted = [a[1:] if a.startswith('§') else f'The scheme prints: “{a}”.' for a in (part.notes or [])]
    noted += [f'The scheme also prints: “{a}”.' for a in (part.asides or []) if a.startswith('(')]
    noted = list(dict.fromkeys(noted))
    if noted:
        first['contextNote'] = f"{first.get('contextNote', '')} {' '.join(noted)}".strip()
    return rows


def _row_for_settled(part, n, ask, question):
    if part.components:
        if all(len(a.split()) <= 3 for a in part.answers):
            # Separate short answers, not pieces of one: "1. (a) Rest 8 marks
            # (3+3+2)" over "Dance", "Food". The first share goes to the first
            # answer GIVEN, in any order.
            return [{'id': f'r-{n}', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                     'marks': None,
                     'group': {'claimMax': len(part.split), 'perOption': part.split[0],
                               'perOptionSteps': list(part.split), 'options': list(part.answers)},
                     'contextNote': (f'The scheme prints “({"+".join(map(str, part.split))})”: '
                                     f'{", ".join(map(str, part.split))} marks for the first, second and '
                                     f'further answers given, in any order.')}]
        return [{'id': f'r-{n}-{k}' if len(part.answers) > 1 else f'r-{n}', 'kind': 'point',
                 'verbatim': a, 'marks': m}
                for k, (a, m) in enumerate(zip(part.answers, part.split), start=1)]
    if part.groups and ask.total == 20:
        grouped = _grouped_rows(part, n, ask, question)
        if grouped:
            return grouped
    if (part.groups and n == 1 and all(h for h, _a in part.groups) and part.split
            and len(set(part.split)) == 1 and len(part.split) == len(part.groups)
            and sum(part.split) == part.total):
        # "4 marks (2+2)" over "One of / People (who are)" and "One of / Who
        # will" (2023 Ordinary B1 Q4): one answer from each heading.
        full = lambda h: (part.fullnames or {}).get(h, h)
        return [{'id': f'r-{k}', 'kind': 'anyN',
                 'verbatim': f'{full(h)} — the answers the scheme accepts', 'marks': None,
                 'group': {'claimMax': 1, 'perOption': part.split[0], 'options': list(a)},
                 'contextNote': (f'The scheme prints these answers under the heading “{full(h)}”: '
                                 f'one of them earns {part.split[0]} marks.')}
                for k, (h, a) in enumerate(part.groups, start=1)]
    answers = [a for a in part.answers if a and a.strip()]
    if not answers:
        return 'the scheme states no answer for this ask'
    if part.total is None:
        return 'the scheme prints no tariff this reads for the ask'
    if part.claim is not None:
        if part.counted and part.claim > 1 and part.split \
                and len(part.split) != part.claim \
                and sum(part.split) == part.total:
            # The scheme printed BOTH a count and a split, and they disagree.
            # 2021 Higher A Q5 heads "Two of 20 marks" and then prints
            # "Advantage (5+5+5+5)" — two of something, over four points at
            # five. Neither reading is the SEC's, so the ask is not priced.
            #
            # Only where the count was PRINTED and asks for more than one. A
            # count this reader inferred is not evidence of anything, and a
            # printed "One of 4 marks (3+1)" is one answer whose halves are
            # worth three and one, not a disagreement at all.
            return ('the scheme prints a count and a split that disagree, so '
                    'what one answer is worth is not stated')
        per = part.per
        if per is None:
            return ('the scheme asks for more answers than its printed tariff '
                    'divides into, so what one answer is worth is not stated')
        if len(answers) < part.claim:
            return 'the scheme asks for more answers than it states'
        if part.groups:
            # Two or more headings over the answers ("You can see" over four
            # pieces of one view, "You can" over another): each answer is led
            # by the heading the scheme prints it under.
            answers = [a if h is None else f'{h} — {a}' for h, group in part.groups for a in group]
        if len(answers) > MAX_OPTIONS:
            return 'the scheme prints more answers than a card can show'
        shown = answers
        group = {'claimMax': part.claim, 'perOption': per[0],
                 'options': shown}
        if len(set(per)) > 1:
            group['perOptionSteps'] = per
        label = None if part.groups else part.label
        row = {'id': f'r-{n}', 'kind': 'anyN',
               'verbatim': (f'{label} — the answers the scheme accepts'
                            if label else
                            'The answers the scheme accepts in full'),
               'marks': None, 'group': group,
               '_trimmed': len(answers) - len(shown)}
        if part.groups:
            named = [h for h, _g in part.groups if h]
            row['contextNote'] = (f'The scheme prints these answers under the '
                                  f'heading{"s" if len(named) > 1 else ""} '
                                  + ', '.join(f'“{(part.fullnames or {}).get(h, h)}”' for h in named) + '.')
        elif label:
            row['contextNote'] = _label_note(part, label)
        return row
    if len(answers) > 1:
        # The scheme lists several answers under a bare tariff and never says
        # how many of them are wanted. Reading them as alternatives states a
        # tariff the SEC did not print; reading them as one answer states an
        # answer it did not print either.
        return ('the scheme lists several answers under one tariff without '
                'saying how many of them are wanted')
    row = {'id': f'r-{n}', 'kind': 'point', 'verbatim': answers[0],
           'marks': part.total}
    if part.label:
        row['contextNote'] = _label_note(part, part.label)
    return row


def _label_note(part, label):
    """What a row's label is: the stem its answers complete ("They can"), or
    the heading the scheme prints over them ("The 30x30 campaign")."""
    if part.stem:
        return f'Each answer completes the scheme’s “{label}”.'
    return f'The scheme prints these answers under the heading “{label}”.'


# ----------------------------------------------------- the matching task ----
def _matching_card(P, S, pp, ss, token, year, level, cards, refuse):
    """The Ordinary put-them-in-order task, as two cards over its eight items.

    The paper prints eight topics and, on the page before, eight numbered
    points; the scheme answers "a) 7  b) 3 …". Eight cards each asking for one
    number would be eight copies of the same reading task, so the items are
    carded together — and in two halves of four rather than one card of eight,
    because `MAX_ROWS` in types/markBank.ts caps a fixed-tariff card at five
    rows and means it: one card is one memory, and eight rows do not fit a
    phone. Each half cites the range it covers, Q(a)–(d) and Q(e)–(h), and each
    row carries the topic the paper prints beside the number the scheme prints
    for it.

    Not modelled as one `anyN` menu of eight options, which would fit the row
    cap: an option is checked against the scheme WHOLE, and half of each of
    these is the paper's topic, which the scheme never prints. A `point` row is
    checked on what follows its em dash — the number — which is exactly what
    the scheme states.
    """
    ref_all = question_ref(year, level, token, None, pp[0][2], pp[-1][2])
    per = ss[0].total
    if per is None or any(a.total != per for a in ss):
        refuse('the scheme prints no tariff this reads for the matching task',
               ref_all, f'{year} {level.upper()} Section {token}')
        return
    language = answer_language(level, '')
    stem = P.matching_stem(token) or (
        'Which of the points on the previous page refer to the following '
        'topics? Write your answer by placing the correct number in the '
        'space provided.')
    half = (len(pp) + 1) // 2
    for start in range(0, len(pp), half):
        chunk = list(zip(pp[start:start + half], ss[start:start + half]))
        letters = [ask_row[2] for ask_row, _ask in chunk]
        rows = []
        for n, ((_s, _i, letter, text, _page), ask) in enumerate(chunk, start=1):
            answer = ask.parts[0].answers[0]
            rows.append({'id': f'r-{n}', 'kind': 'point',
                         'verbatim': f'({letter}) {" ".join(text.split())} — {answer}',
                         'marks': per})
        rows[0]['contextNote'] = (
            'Each topic is matched to the number of the printed point it '
            'refers to, on the page this card opens. The examination prints '
            f'{len(pp)} topics; this card takes {len(chunk)} of them. '
            + language_note(language))
        ref = question_ref(year, level, token, None, letters[0], letters[-1])
        cards.append({
            'id': card_id(year, level, token, None, letters[0], 'match'),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': CARD_SECTION[token[0]],
            'topicId': topic_for(level, token, matching=True),
            'conceptId': 'match-printed-points-to-topics',
            'questionRef': ref,
            'questionText': stem,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': per * len(rows),
            'rows': rows,
            'notes': (f'The scheme prices the task '
                      f'{S.section_totals.get(token)} marks over its '
                      f'{len(pp)} items; the paper prints the points on page '
                      f'{P.source_pages.get(token)}.'),
            **({'sourceMaterial': src} if (src := source_material(
                P, token, language, level, year)) else {}),
        })


# ------------------------------------------------ what is not an answer ----
ESSAY_EVIDENCE = (
    'the scheme answers this ask with a BAND GRID and nothing else. Its head '
    'reads "B 3 Essay on prescribed text — Use the descriptors in Appendix 1", '
    'and Appendix 1 prints five bands of prose: "(51 - 60 marks) Answers the '
    'question fully · Demonstrates excellent knowledge of the text as a whole '
    '· Accurate quotes/references to the text in support of all points made". '
    'Those are qualities of an essay, not answers, and a card would ask a '
    'student to tick "no irrelevant material" as something they were supposed '
    'to have written. The indicative points the scheme prints beneath are '
    'introduced "Some examples include" and carry no tariff at all.')

WRITING_EVIDENCE = (
    'the scheme answers Section C with CONTENT AND COMMUNICATION DESCRIPTORS '
    'and nothing else — "Good level of coherence · Clear argumentation · Full '
    'completion of communicative task · Good range of vocabulary" — and a '
    'separate Language band, "Idiomatic Italian, very good/excellent '
    'vocabulary". Where it lists points at all they are the communicative '
    'tasks the paper itself printed in the question ("Introduzione", "perché '
    'il tirocinio in Italia"), not answers to it.')

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet whose own instructions read '
    '"Sa roinn seo cloisfidh tú ocht ráiteas nó mír nuachta san Iodáilis" — in '
    'this section you will hear eight statements or news items in Italian — '
    'and the paper prints no text of what is said. The only printed source of '
    'that material is the marking scheme\'s own "Script for Listening '
    'Comprehension Test", the ANSWER document, so carrying it on the card '
    'would hand the student the answers with the question. No verified '
    'playback copy of the SEC recording is bound to this deck, so the card '
    'would be unanswerable from what it shows.')


def _essay(P, year, level, refuse):
    for route, item, _text, _page in P.essay_asks():
        refuse('the scheme prints a band grid for this ask, not an answer',
               question_ref(year, level, f'B3{route}', item, None),
               f'{year} {level.upper()} scheme, Section B3: {ESSAY_EVIDENCE}')


def _writing(P, year, level, refuse):
    for item, letter, _text, _page in P.writing_asks():
        refuse('the scheme prints a band grid for this ask, not an answer',
               question_ref(year, level, 'C', item, letter),
               f'{year} {level.upper()} scheme, Section C: {WRITING_EVIDENCE}')


def _listening(P, year, level, refuse):
    for section, item, _text in P.aural_asks():
        refuse('the ask needs the recording, which no card can carry',
               question_ref(year, level, f'L{section}', item, None),
               f'{year} {level.upper()} Listening Comprehension Test, '
               f'Section {section}: {AUDIO_EVIDENCE}')


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/italian.json from the refusals')
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
        points = sum(1 for c in cards for r in c['rows'] if not r.get('group'))
        print(f'{rows} marking rows: {points} stated answer(s) and '
              f'{opts} menu option(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:14} {n}')
        by_lang = collections.Counter(
            ITALIAN if f'in {ITALIAN}' in (c.get('sourceMaterial') or {}).get(
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
