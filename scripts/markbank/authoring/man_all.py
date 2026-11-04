#!/usr/bin/env python3
"""Author every Mandarin Chinese ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/man_all.py --report
    python3 scripts/markbank/authoring/man_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/man_all.py \
        > scripts/markbank/authored/mandarin-chinese.json

Census-driven: the ten sittings print 683 leaf asks across three booklets, and
this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask of Section A, Reading. The question comes from the PAPER and
the marking points from the SCHEME, and the two are paired by SUBTRACTION: the
scheme reprints the paper's question verbatim and sets its answer under it, so
the answer is the scheme's block with the paper's own text taken off the front
(man_scheme.split_against). A block that does not reprint the question is a
fault and no card is made from it.

The answer LANGUAGE rides on the card, read per ask from the ask's own printed
words — "Answer in Chinese" against nothing at all — because in this subject it
is not a constant. So does the paper's own rule for what the Chinese must look
like: simplified characters, never pinyin.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every comprehension answer depends on a text printed only in the question
paper — a weather table, a nursery rhyme, an email, a flyer — so each card
binds `sourceMaterial` to the pages its question's stimulus was printed on.

THE REFUSALS, each attacked before it was accepted
--------------------------------------------------
**Written production (Section B).** The scheme answers Questions 5 and 6 with a
band grid and nothing else: "Marks for Question 5/6 are broken down as follows:
Communication = 20 marks, Language = 20 marks", then three bands described by
qualities — "Material easily comprehensible", "Mostly correct word order". Not
one line of it states an answer, and there is no model composition to lift
either. This is the refusal all eleven carded languages make of their writing
tasks.

**The Listening Comprehension Test.** Its scheme prices and answers every ask,
and the ask is still not one a card can put: "Where is the conversation taking
place? — a (Chinese) restaurant" is answerable only by someone who has just
heard the recording, which the SEC does not publish. The booklet is read and
counted so the denominator is the paper; nothing in it is carded.

**A printed GRID.** Four sittings set a radical table and two set a
character-structure table, and the SEC prints the answers in a four-column grid
whose cells this reader can price but cannot re-associate: read by baseline the
2024 Higher table hands back "家 宀 roof / shelter", "home", "fire", "黑 black
灬" — the right cells in the wrong rows. The tariff is recovered (twelve blanks
at one mark each, which closes the question's printed 22) but the CONTENT is
not, and a card that pairs 灬 with the wrong meaning is exactly the corruption
this pipeline exists to prevent. Refused with the cells named, not guessed at.
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

from man_paper import ManPaper, sittings, bag, score            # noqa: E402
from man_scheme import ManScheme, has_scheme                    # noqa: E402
from man_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                        language_note, SIMPLIFIED)
from paper_census import key_label                              # noqa: E402

SUBJECT = 'mandarin-chinese'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
MAX_ROWS = 16
PAIR_FLOOR = 0.5

GRID_EVIDENCE = (
    'the scheme answers Section B with a band grid and nothing else. Under '
    '"WRITING - 80 MARKS / MARKING INSTRUCTIONS FOR WRITING" it prints '
    '"Marks for Question 5/6 are broken down as follows: Communication = 20 '
    'marks, Language = 20 marks" and then three bands described by qualities — '
    '"14 to 20 marks / High level of achievement: 1. Material easily '
    'comprehensible 2. Clearly conveyed intention and purpose" — with no '
    'marking point and no model composition anywhere in it. There is nothing '
    'to lift.')

LISTENING_EVIDENCE = (
    'the ask is the RECORDING. The scheme prices and answers it — "1. (a) '
    'Where is the conversation taking place? (1 x 2 marks) a (Chinese) '
    'restaurant" — but the question paper prints only the question, and the '
    'audio the answer depends on is not published. A card would ask a student '
    'to recall an answer to a conversation they cannot hear. The booklet is '
    'censused so the denominator is the paper, and every ask in it is '
    'excluded, which is the refusal all eleven carded languages make of their '
    'listening tests.')

TABLE_EVIDENCE = (
    'the scheme sets this answer in a four-column GRID and the text layer '
    'hands its cells back in the wrong rows. 2024 Higher Question 2(e) prints '
    '"Character in the text | Meaning of the character | Radical of the '
    'character | Meaning of the radical" and then four rows of cells, and read '
    'by baseline they arrive as "家 宀 roof / shelter", "home", "1 mark 1 mark '
    '1mark", "fire", "黑 black 灬" — every cell present and no row intact. The '
    'tariff IS recoverable and is checked: the twelve one-mark blanks sum to '
    'the twelve marks that close the question\'s printed 22. The pairing of '
    'character to radical to meaning is not, and a card that pairs 灬 with the '
    'wrong meaning teaches the wrong thing. Refused rather than guessed at.')

UNPAIRED_EVIDENCE = (
    'the scheme prints no block at this address that reprints the paper\'s '
    'question, so the pair would rest on the part key alone — which is Law 4, '
    'and which this bank has measured wrong in every subject that tried it.')


def card_id(year, level, key):
    section, q, letter, roman = key
    parts = ['man', str(year), level, str(section).lower(), str(q)]
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def question_ref(year, level, key, variant=False):
    """The citation, in the bank's grammar: "2024 HL Section A Q1(c)(i)".

    No "-alt" suffix anywhere, and that is a fact about this paper rather than
    a shortcut. The suffix exists to separate a choice VARIANT from the
    question it repeats the number of, and Mandarin never repeats one: 2022
    Higher's only whole-question choice is "Answer either Question 1 OR
    Question 2" — two different numbers — and its only part choice is "Answer
    either part (f) OR part (g)", two different letters. Suffixed anyway, all
    fourteen of Question 2's cards cited a part the paper does not print and
    reconcile reported them as orphans.
    """
    section, q, letter, roman = key
    ref = f'{year} {level.upper()} Section {section} Q{q}'
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


def build():
    cards, excluded = [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year, level in sittings(SUBJECT):
        P = ManPaper(year, level, SUBJECT)
        asks = P.asks()
        stamp = f'{year} {level.upper()}'
        S = ManScheme(year, level, SUBJECT) if has_scheme(year, level, SUBJECT) \
            else None
        pairs, groups = {}, {}
        if S is not None:
            texts = {a.key: a.full_text for a in asks}
            S.split_against(texts.get)
            pairs, groups = _pair(asks, S)
        grouped = {p.key: key for key, (_parent, rows) in groups.items()
                   for p in rows}
        for key, (parent, paper_rows) in sorted(groups.items()):
            ref = question_ref(year, level, (key[0], key[1], key[2], None))
            if parent.table and parent.wide:
                refuse('the scheme sets this answer in a printed grid whose '
                       'rows cannot be recovered from the text layer', ref,
                       f'{stamp} scheme Q{key[1]}: {TABLE_EVIDENCE}')
                continue
            if not parent.answers:
                refuse('the scheme reprints this question and states nothing '
                       'under it', ref,
                       f'{stamp} scheme: "{paper_rows[0].text[:100]}" is '
                       f'reprinted with no answer beneath it')
                continue
            if parent.marks < len(paper_rows):
                # The scheme priced ONE of the rows, not the group: 2022
                # Ordinary prints "(1 mark)" beside each of Question 4(f)'s two
                # translations and no total above them, and the block reader
                # takes the first. One mark spread over two rows is a tariff
                # the SEC never printed, so the ask is refused rather than
                # guessed at — five separate incidents in this bank say so.
                refuse('the scheme prices this ask below the number of rows '
                       'it sets, so its per-row tariff cannot be read', ref,
                       f'{stamp} scheme Q{key[1]}({key[2]}): the SEC prices '
                       f'{parent.marks} mark(s) over {len(paper_rows)} printed '
                       f'rows and states no split.')
                continue
            _card(P, S, paper_rows[0], parent, year, level, cards,
                  key=(key[0], key[1], key[2], None), items=paper_rows)
        for ask in asks:
            if ask.key in grouped:
                continue      # carded once, at the level the scheme priced
            ref = question_ref(year, level, ask.key, ask.variant)
            if ask.kind == 'writing':
                refuse('the scheme answers Section B with a band grid and '
                       'states no marking point', ref,
                       f'{stamp} scheme, WRITING: {GRID_EVIDENCE}')
                continue
            if ask.kind == 'listening':
                refuse('the ask is the recording, which the SEC does not '
                       'publish', ref,
                       f'{stamp} Listening Comprehension Test: '
                       f'{LISTENING_EVIDENCE}')
                continue
            if S is None:
                refuse('the SEC published no marking scheme for this sitting',
                       ref, f'{stamp}: no scheme in the corpus')
                continue
            pair = pairs.get(ask.key)
            if pair is None and S is not None:
                at = {a.key: a for a in S.leaves()
                      if a.unit == 'reading'}.get(ask.key)
                if at is not None and at.wide:
                    refuse('the scheme sets this answer in a printed grid '
                           'whose rows cannot be recovered from the text '
                           'layer', ref,
                           f'{stamp} scheme Q{ask.q}: {TABLE_EVIDENCE}')
                    continue
            if pair is None:
                refuse('the scheme prints no block that reprints this '
                       'question', ref, f'{stamp} paper: "{ask.text[:110]}" — '
                       f'{UNPAIRED_EVIDENCE}')
                continue
            if pair.wide:
                refuse('the scheme sets this answer in a printed grid whose '
                       'rows cannot be recovered from the text layer', ref,
                       f'{stamp} scheme Q{ask.q}: {TABLE_EVIDENCE}')
                continue
            if not pair.marks:
                refuse('neither document states a tariff for this ask', ref,
                       f'{stamp}: the scheme prints no marks on this ask and '
                       f'the paper prints none either')
                continue
            if not pair.answers and pair.directives:
                refuse('the scheme answers this ask with a directive and '
                       'states no marking point', ref,
                       f'{stamp} scheme: under "{ask.text[:80]}" the SEC '
                       f'prints only "{pair.directives[0]}" — an instruction '
                       f'to the examiner, not an answer a student could have '
                       f'written. There is nothing to lift.')
                continue
            if not pair.answers:
                refuse('the scheme reprints this question and states nothing '
                       'under it', ref,
                       f'{stamp} scheme: "{ask.text[:100]}" is reprinted with '
                       f'no answer beneath it')
                continue
            _card(P, S, ask, pair, year, level, cards)
    return cards, refused, examples, excluded


def _pair(asks, S):
    """Law 4, twice over: by address AND by wording, and never by one alone.

    The scheme reprints the paper's question, so the pair is EARNED. Four
    shapes are handled, in this order:

    1. **An ordinary part.** The addresses agree and the wording is scored.
    2. **A true/false row.** The addresses do NOT agree, because 2022 Higher's
       Question 4(f) numbers its four rows "(a)" to "(d)" where the paper
       numbers the same four "(i)" to "(iv)". Those pair on printed ORDER under
       two independent checks, as the Baltic languages do: the two documents
       must print the SAME NUMBER of rows under that letter, and every pair
       must agree in wording. One pair failing either test abandons the whole
       letter rather than shifting the rest by one.
    3. **The scheme priced ONE LEVEL UP.** 2023 Higher's Question 1(a) sets a
       four-row table on the paper — (i) to (iv) — and the scheme prices the
       LETTER once, "(4 x 2 marks)", listing the four answers beneath it. The
       ask is priced, not missing: the letter is carded once with the paper's
       four romans printed in the question and the scheme's four answers as its
       rows, and each roman is covered through the part the scheme priced it
       under.
    4. **A grid the SEC does not reprint.** Every Ordinary paper opens with a
       word-and-picture matching question whose scheme block begins straight on
       "Word | Letter" with no question above it. There is no wording to score,
       so the pair rests on the address plus TWO printed counts that must
       agree: the number of rows the grid sets, and the number of one-mark
       prices it prints beside them.
    """
    scheme = {a.key: a for a in S.leaves() if a.unit == 'reading'}
    out, groups = {}, {}
    for ask in asks:
        if ask.kind != 'reading':
            continue
        got = scheme.get(ask.key)
        if got is None:
            continue
        if got.table and not got.cue:
            # The word-and-picture grid, which the SEC does not reprint. Two
            # printed counts have to agree before the address alone is
            # trusted: the rows the grid sets and the marks it prices them at.
            if got.marks and len(got.answers) == got.marks:
                out[ask.key] = got
            continue
        if _agrees(ask, got):
            out[ask.key] = got
    # 1b — a true/false table whose addresses agree row for row. The SEC
    # rewords the odd row between the paper and its scheme — 2022 Higher
    # prints "姚明 began playing basketball in NBA in 2011" and the scheme
    # "姚明 begins to play basketball in NBA since 2011" — so the group is
    # judged as a GROUP: same count, same addresses, and the wording agreeing
    # on average. One reworded row does not abandon three that agree, and a
    # group that does not agree on average is not paired at all.
    paper_rows_by = collections.defaultdict(list)
    for ask in asks:
        if ask.kind == 'reading' and ask.roman:
            paper_rows_by[(ask.section, ask.q, ask.letter)].append(ask)
    for key, paper_rows in paper_rows_by.items():
        if all(p.key in out for p in paper_rows):
            continue
        mine = [scheme.get(p.key) for p in paper_rows]
        if any(m is None for m in mine):
            continue
        scores = [score(bag(p.full_text), bag(m.cue))
                  for p, m in zip(paper_rows, mine)]
        if sum(scores) / len(scores) < PAIR_FLOOR:
            continue
        for p, m in zip(paper_rows, mine):
            out[p.key] = m
    # 2 — whatever is left, matched by order inside its letter.
    by_letter = collections.defaultdict(list)
    for ask in asks:
        if ask.kind == 'reading' and ask.roman and ask.key not in out:
            by_letter[(ask.section, ask.q, ask.letter)].append(ask)
    rows = collections.defaultdict(list)
    for a in scheme.values():
        if a.roman and a.key not in out:
            rows[(a.section, a.q, a.letter)].append(a)
    for key, paper_rows in by_letter.items():
        scheme_rows = rows.get(key) or []
        if len(scheme_rows) != len(paper_rows):
            continue
        if not all(_agrees(p, s) for p, s in zip(paper_rows, scheme_rows)):
            continue
        for p, s in zip(paper_rows, scheme_rows):
            out[p.key] = s
    # 3 — the scheme priced the LETTER the paper split into romans.
    for key, paper_rows in by_letter.items():
        if all(p.key in out for p in paper_rows):
            continue
        parent = scheme.get((key[0], key[1], key[2], None))
        if parent is None or parent.wide or not parent.marks:
            continue
        if not _agrees(paper_rows[0], parent):
            continue
        groups[key] = (parent, paper_rows)
    return out, groups


def _agrees(ask, got):
    """Do the two documents say the same thing about this ask?

    Scored on content words, with the SHORT-CUE case allowed through: the SEC
    sometimes reprints a two-word question ("What is the meaning of ‘乒乓球’?")
    whose bag holds one scorable word, and a Jaccard floor on one word is
    noise. Where the cue is that short the CHINESE in it is the evidence, and
    it has to appear on both sides.
    """
    if not got.cue:
        return False
    a, b = bag(ask.full_text), bag(got.cue)
    han_a = set(re.findall(r'[一-鿿]', ask.full_text))
    han_b = set(re.findall(r'[一-鿿]', got.cue))
    if han_a and han_b and not (han_a & han_b) and score(a, b) < PAIR_FLOOR:
        return False
    if len(a) < 3 or len(b) < 3:
        return bool(han_a & han_b) or score(a, b) >= PAIR_FLOOR
    return score(a, b) >= PAIR_FLOOR


MARKER = re.compile(r'^\(?\s*(?:[ivx]{1,4}|[a-l])\s*\)\s*')


def _subtract_items(lines, items):
    """One row per sub-item, with the sub-QUESTION taken off the front of each.

    A card made at the level the scheme priced carries the paper's own
    sub-items in its question, and the SEC sets those two ways one page apart.
    2023 Higher's Question 1(a) prints only the four answers — "(i) C1", "(ii)
    B2" — while its Question 2(a) reprints each sub-question above its answer:
    "(i) What is the earliest time one can enter the zoo on a Tuesday?" then
    "9:00 am". Read as answers, the reprinted questions shipped as marking
    points; read as questions, the four bare answers of 1(a) would be thrown
    away.

    So the two are told apart by whether the scheme's lines reproduce the
    paper's sub-questions at all, and the subtraction is sequential — the same
    knife split_against uses one level up. A sub-item left with no answer
    abandons the whole split rather than shifting the rest by one.
    """
    if not lines or len(items) < 2:
        return None
    wants = [_fold(i.text) for i in items]
    reprints = any(w and _fold(MARKER.sub('', line)) and
                   w.startswith(_fold(MARKER.sub('', line)))
                   for w in wants for line in lines)
    if not reprints:
        return list(lines) if len(lines) == len(items) else None
    out, i = [], 0
    for n, want in enumerate(wants):
        seen = ''
        while i < len(lines) and seen != want:
            folded = _fold(MARKER.sub('', lines[i]))
            if folded and want.startswith(seen + folded):
                seen += folded
                i += 1
                continue
            break
        nxt = wants[n + 1] if n + 1 < len(wants) else None
        answer = []
        while i < len(lines):
            folded = _fold(MARKER.sub('', lines[i]))
            if nxt and folded and nxt.startswith(folded):
                break
            answer.append(lines[i])
            i += 1
        text = ' '.join(answer).strip()
        if not text:
            return None
        out.append(text)
    return out


def _fold(text):
    return re.sub(r'[^0-9a-z\u4e00-\u9fff]+', '', (text or '').lower())


ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']


def _question_text(ask, items):
    """The printed question, and where the paper split it, its own sub-items.

    The scheme prices the LETTER and lists one answer per row, so one card
    carries the letter's instruction and the rows it numbers — printed in the
    paper's own order and with the paper's own markers.
    """
    if not items:
        return ask.text
    head = ask.stem or ''
    parts = []
    for item in items:
        body = item.text
        if head and body.startswith(head):
            body = body[len(head):].strip()
        parts.append(f'({item.roman}) {body}' if item.roman else body)
    return re.sub(r'\s+', ' ', f'{head} ' + ' '.join(parts)).strip()


SEGMENT = re.compile(r'\s*/\s*(?![^(]*\))|\s*;\s*')


def _card(P, S, ask, pair, year, level, cards, key=None, items=()):
    key = key or ask.key
    stimulus = P.passages.get((ask.section, ask.q), '')
    language = answer_language(ask, stimulus)
    rows = _rows(pair, items)
    tariff = ({'kind': 'orderedSplit', 'notation': pair.notation}
              if pair.notation and len(rows) > 1
              else {'kind': 'questionTotal'})
    note = language_note(language)
    for row in rows:
        if note:
            row['contextNote'] = note
    card = {
        'id': card_id(year, level, key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        # The paper's own tab, as a token: 'A' for Reading and 'B' for
        # Writing. The citation spells it out ("Section A Q1(a)"); the field
        # carries the letter, which is what the card model's union accepts.
        'section': str(ask.section),
        'topicId': topic_for(ask, stimulus),
        'conceptId': concept_for(ask.full_text),
        'questionRef': question_ref(year, level, key, ask.variant),
        'questionText': _question_text(ask, items),
        'tariffModel': tariff,
        'totalMarks': pair.marks,
        'rows': rows,
        'notes': (f'The scheme prices this ask at {pair.marks} marks inside a '
                  f'Reading section it heads {P.section_marks.get(ask.section)}'
                  f' marks. The paper prints it on page {ask.page} of the '
                  f'written booklet.'),
    }
    if ask.stem and len(ask.stem) >= 12 and ask.stem != ask.text:
        card['stem'] = ask.stem
    if pair.directives:
        card['answerNote'] = ' '.join(pair.directives)
    source = _source(P, ask, year, level, language)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


def _rows(pair, items=()):
    """The scheme's stated answer, cut into the rows it printed.

    Only where the SEC's own notation says there are several: "(2 x 2 marks)"
    over "Weather: rainy / Temperature: 17" is two rows, and a single "(1 x 2
    marks)" over one line is one. A "/" inside one printed line is the SEC's
    ALTERNATIVES for one row — "6:30 p.m. / 18:30 / 6:30 in the afternoon" —
    and splitting on it would claim three marks where the SEC prints two.
    """
    parts = [p.strip() for p in pair.answers if p and p.strip()]
    if items:
        parts = _subtract_items(parts, items) or parts
    if not parts:
        return []
    want = None
    if pair.notation:
        m = re.fullmatch(r'(\d+) × (\d+)', pair.notation)
        if m:
            want = int(m.group(1))
    if want and len(parts) < want:
        # The SEC separates two answers of one ask with a SEMICOLON and the
        # alternatives for one answer with a slash: "green tea; scented tea"
        # under "(2 x 2 marks)" is two rows, while "6:30 p.m. / 18:30 / 6:30
        # in the afternoon" under "(2 x 2 marks)" is one. Only the semicolon
        # is cut, and only where the SEC's own notation asks for more rows
        # than the printed lines give.
        cut = [bit.strip() for part in parts for bit in part.split(';')
               if bit.strip()]
        if len(cut) == want:
            parts = cut
    if want and len(parts) > want:
        while len(parts) > want:
            i = min(range(len(parts) - 1),
                    key=lambda n: len(parts[n]) + len(parts[n + 1]))
            parts[i:i + 2] = [f'{parts[i]} {parts[i + 1]}']
    while len(parts) > MAX_ROWS:
        i = min(range(len(parts) - 1),
                key=lambda n: len(parts[n]) + len(parts[n + 1]))
        parts[i:i + 2] = [f'{parts[i]} {parts[i + 1]}']
    kind = 'anyN' if len(parts) > (want or len(parts)) else 'point'
    return [{'id': f'r-{i + 1}', 'kind': kind, 'verbatim': p, 'marks': None}
            for i, p in enumerate(parts)]


def _source(P, ask, year, level, language):
    pages = P.passage_pages.get((ask.section, ask.q)) or []
    text = P.passages.get((ask.section, ask.q)) or ''
    if not pages or len(text) < 20:
        return None
    presentation = ('Read the material exactly as the examination printed it, '
                    'then answer. ' + language_note(language)).strip()
    return {
        'kind': 'source-text',
        'label': f'Question {ask.q}',
        'title': 'The material this question is about',
        'pages': pages,
        'attribution': (f'SEC Mandarin Chinese {year} {LEVEL_TITLE[level]} '
                        'Level examination paper — '
                        '© State Examinations Commission.'),
        'presentationNote': presentation,
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
