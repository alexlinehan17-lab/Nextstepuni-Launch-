#!/usr/bin/env python3
"""Author every ask a non-curricular EU language paper prints and its scheme
answers.

    python3 scripts/markbank/authoring/eu_all.py portuguese --report
    python3 scripts/markbank/authoring/eu_all.py portuguese --exclusions
    python3 scripts/markbank/authoring/eu_all.py portuguese \\
        > scripts/markbank/authored/portuguese.json

Census-driven: this walks the census rather than choosing what to card, and
every ask it does not card becomes an exclusions entry carrying the scheme's
or the paper's own words as evidence.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (eu_paper.py) and its
marking points from the SCHEME (eu_scheme.py). The two are read INDEPENDENTLY
and then paired on the address both documents print — which is safe here, and
only here, because the scheme REPRINTS the question above its answers, so
every pair is scored on wording as well and a pair that does not agree is
refused rather than shipped (Law 4).

WHERE THE TARIFF COMES FROM depends on the era, and on nothing else:
* MODERN (Portuguese 2022 onward) — the scheme prices every ask, and the
  arithmetic is checked against the total the scheme prints on each question's
  own head before a card is written.
* CLASSIC (Portuguese 2021; every Romanian and Dutch sitting) — the scheme
  prints answers with no marks at all, and the QUESTION PAPER prices each ask
  in its right-hand margin: "(5)", "(5×1)". That is the printed tariff, and it
  is checked against the total the paper prints on the part's own head.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is a quotation from a text printed only in the question
paper, so each card binds `sourceMaterial` to the exact pages of its own text
in the QUESTION paper — never the scheme, which is where the answers are.
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

from eu_paper import EuPaper, bag, score, sittings, LANGS       # noqa: E402
from eu_scheme import EuScheme, pairs_by_question               # noqa: E402
from eu_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, LANGUAGE_NAME)
from paper_census import census_subject, key_label              # noqa: E402
import cardlint                                                 # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts.
MAX_OPTIONS = 16
# Below this the paper's ask and the scheme's reprint of it are not the same
# question, and the pair is refused rather than shipped. Measured against the
# corpus, exactly as the Polish reader's was.
MIN_AGREEMENT = 0.34
# An id prefix per subject, so two subjects on one reader never collide.
PREFIX = {'portuguese': 'por', 'romanian': 'ron', 'dutch': 'nld'}


def card_id(subject, year, level, key):
    section, q, letter, roman = key
    parts = [PREFIX[subject], str(year), level]
    if section:
        parts.append(str(section).lower())
    parts.append(str(q))
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def question_ref(year, level, key):
    return f'{year} {level.upper()} {key_label(key)}'


def source_material(P, ask, subject, language, level, year):
    """The reading text's own printed pages, from the QUESTION paper."""
    pages = P.pages_for(ask.q)
    if not pages:
        return None
    lead = P.lead(ask.q) or f'Question {ask.q}'
    return {
        'kind': 'source-text',
        'label': lead.upper()[:60],
        'title': f'Reading text — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC {LANGUAGE_NAME[subject]} {year} '
                        f'{LEVEL_TITLE[level]} Level examination paper — '
                        f'© State Examinations Commission.'),
        'presentationNote': (
            'Read the text exactly as the examination printed it, then '
            'answer. ' + language_note(subject, language)),
    }


# --------------------------------------------------------------- refusals ----
GRID_EVIDENCE = (
    'the scheme answers this task with a CONTENT AND LANGUAGE BAND GRID and '
    'nothing else. It prices the two tasks "30 Marks" and "20 Marks" and then '
    'describes the bands in prose — Content and Communication "TOP · Very '
    'good or excellent achievement of the task · High level of textual '
    'coherence · Clear and well-structured text · Full completion of '
    'communicative task 11-15", down to "BOTTOM · Barely adequate or '
    'inadequate achievement of the task · Lack of textual coherence 0-5"; '
    'Language "TOP · Very good range of vocabulary · Verb endings, tenses, '
    'agreements nearly always correct 11-15" down to "BOTTOM · Vocabulary '
    'very inadequate with interference or direct translation 0-5". Those are '
    'the qualities of a piece of writing, not answers, and a card would ask a '
    'student to tick "Very good range of vocabulary" as something they were '
    'supposed to have written.')

ESSAY_CLASSIC_EVIDENCE = (
    'the scheme answers this with a MODEL COMMENTARY, not a marking list, and '
    'prices no line of it. Its head reads "PARTE II (40 pontos) (Comentário '
    'pessoal, correcto e fluente em cerca de 300 palavras.)" and then prints '
    'three hundred words of continuous prose an examiner is to read as an '
    'example. There is no tariff beside any sentence of it, so there is '
    'nothing a student could be marked right or wrong against.')

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet (component A00) whose own '
    'instructions read "Each Listening Comprehension piece will be played '
    'three times", and the booklet prints no text of what is said. The only '
    'printed source of that material is the marking scheme\'s own APPENDIX 2 '
    'Audio Scripts — the ANSWER document — so carrying it on the card would '
    'hand the student the answers with the question. No verified playback '
    'copy of the SEC recording is bound to this deck, so the card would be '
    'unanswerable from what it shows.')

TICK_EVIDENCE = (
    'the scheme answers this ask GRAPHICALLY and the text layer does not '
    'carry which box it ticked. Four sittings print three different '
    'conventions for it and no two can be read the same way: 2025 Ordinary '
    'heads the table "True False" as ONE text cell, so there is no column '
    'position for either word to measure a tick against; 2024 Ordinary sets '
    '"Verdadeiro" and "Falso" each followed by a Wingdings box glyph, U+F063 '
    'for the empty box and U+F0FE for the marked one; and 2023 Ordinary '
    'prints its ticks in a table whose statement rows carry no tick in the '
    'text layer at all. Guessing which of two boxes the SEC marked is the one '
    'thing this pipeline must never do, so the ask is counted and refused '
    'rather than answered.')


def build(subject):
    cards, pairs, excluded = [], [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    faults = []

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year, level in sittings(subject):
        P = EuPaper(year, level, subject)
        S = EuScheme(year, level, subject)
        # Law 4: the address is tried and then CHECKED, question by question,
        # and where it does not hold the two documents are joined in printed
        # order — with every pair scored on wording below.
        priced, how = pairs_by_question(P.reading_asks(), S.reading())
        stamp = f'{year} {level.upper()}'
        for ask in P.all_asks():
            key = ask.key
            ref = question_ref(year, level, key)
            section = ask.section or ''
            if section.startswith('L'):
                refuse('the ask needs the recording, which no card can carry',
                       ref, f'{stamp} Listening Comprehension Test, '
                            f'Part {section[1:]}: {AUDIO_EVIDENCE}')
                continue
            if section in ('II', 'III'):
                refuse('the scheme answers this with a model commentary and '
                       'prices no line of it', ref,
                       f'{stamp} scheme, Segunda Parte: '
                       f'{ESSAY_CLASSIC_EVIDENCE}')
                continue
            if section == 'B':
                refuse('the scheme prints a content-and-language band grid '
                       'for this task, not an answer', ref,
                       f'{stamp} scheme, Written Production: {GRID_EVIDENCE}')
                continue
            _reading(P, S, priced, ask, subject, year, level, ref, cards,
                     refuse, pairs, how.get((ask.section, ask.q), 'address'))
        faults += [(f'{stamp} Q{q}', want, got)
                   for (_sec, q), want, got in S.unsettled]
    return cards, refused, examples, excluded, pairs, faults


# The paragraph reference the SEC closes a reprinted question with, and
# whatever it prints AFTER that reference.
AFTER_REF = re.compile(
    r'^(?P<question>.*\((?:par[áa]grafos?|paragraphs?|parte|part|alinea)\b'
    r'[^)]*\))\s*(?P<answer>\S.*)$', re.I)
# How much of a recovered answer may also appear in the paper's own question
# before it stops being an answer and starts being more of the question.
MAX_ECHO = 0.2
# The SEC's own words for an ordering task, read from the printed rubric.
ORDERING = re.compile(
    r'\bNumere\b|Ponha\s+por\s+ordem|Number\s+the\s+following|'
    r'order\s+in\s+which\s+they\s+appear|Enter\s+the\s+correct\s+answer\s+'
    r'number', re.I)
# A tick-one-box or true/false ask, in the paper's own rubric. Anchored on the
# rubric the SEC actually prints and never on a word that can appear in prose:
# "Verdadeiro" alone refused 2021 Question 6, whose ask is "Faça um comentário
# ao VERDADEIRO sentido da frase" and has no box in it at all.
TICK_ASK = re.compile(
    r'Assinale\s*[(✓]|Assinale\s+(?:a|as|com|o)\b|Tick\s*\(|'
    r'Tick\s+the\b|True\s+or\s+False|Verdadeiro\s+Falso|'
    r'the\s+True\s+\(T\)|resposta\s+correta|op[çc][õo]es\s+corretas',
    re.I)


def _reading(P, S, priced, ask, subject, year, level, ref, cards, refuse,
             pairs, joined_by='address'):
    stamp = f'{year} {level.upper()}'
    sch = priced.get(ask.key)
    question = ask.full_text
    # The shape of the ask is read from the PAPER first, before anything is
    # asked of the scheme: a tick-one-box ask whose unticked options the scheme
    # never reprints would otherwise be refused for the wrong reason.
    if ORDERING.search(question) or ORDERING.search((sch and sch.cue) or ''):
        refuse('the ask is an ordering task, and its answer is a set of '
               'positions in a list the card cannot carry', ref,
               f'{stamp} paper: "{question[:110]}" — the scheme answers it by '
               f'writing a number beside each printed sentence, and a card '
               f'that cannot show the sentences in their printed boxes cannot '
               f'ask for them')
        return
    if TICK_ASK.search(question) or TICK_ASK.search((sch and sch.cue) or ''):
        refuse('the scheme answers this ask by ticking a box, and the text '
               'layer does not carry which one', ref,
               f'{stamp} scheme, "{(sch.cue if sch else question)[:90]}": '
               f'{TICK_EVIDENCE}')
        return
    if sch is None:
        refuse('the scheme prices no ask at the address the paper prints', ref,
               f'{stamp} paper: "{ask.full_text[:110]}" — the scheme\'s '
               f'reading section prices no ask that pairs with it')
        return
    if sch.fault:
        refuse('the scheme prices the ask two ways at once, so neither number '
               'can be trusted', ref,
               f'{stamp} scheme, "{sch.cue[:90]}": {sch.fault}')
        return

    # The tariff: from the SCHEME in the modern era and from the PAPER in the
    # classic one, and printed in both. Nothing here averages or infers.
    if P.era == 'classic':
        if not ask.tariff:
            refuse('neither document states a tariff for this ask', ref,
                   f'{stamp} paper: "{question[:110]}" — the paper prints no '
                   f'marks in its right-hand margin and the scheme prints '
                   f'none at all')
            return
        count, per, total = ask.tariff
        notation = ask.notation
    else:
        if sch.total is None:
            refuse('the scheme states no tariff for this ask', ref,
                   f'{stamp} scheme, "{sch.cue[:110]}" — the scheme prints '
                   f'answers with no marks beside them')
            return
        count, per, total = sch.count, sch.per, sch.total
        notation = sch.notation

    answers = [a for a in sch.answers if a['text']]
    if not answers:
        sch.answers = _recovered_answer(sch, question)
        answers = sch.answers
    if not answers:
        refuse('the scheme states no answer for this ask, only its price', ref,
               f'{stamp} scheme, "{sch.cue[:110]}" priced {notation!r} with '
               f'no marking point printed under it')
        return

    cue = _cue_of(sch)
    agreement = max(_agreement(question, cue), _agreement(question, sch.cue),
                    _agreement(ask.text, cue), _agreement(ask.text, sch.cue))
    if P.era == 'classic':
        # The classic scheme reprints NOTHING: its head is "Tópicos de
        # correcção" and under each number it prints the answer alone. There
        # is no wording to score, and scoring it refused every ask in the
        # sitting. What stands in for it is the numbering itself, which both
        # documents print and which the census checks question by question.
        agreement = None
    elif agreement < MIN_AGREEMENT:
        refuse('the paper and the scheme do not print the same question at '
               'this address, so the pair cannot be trusted', ref,
               f'{stamp} paper: "{question[:90]}" against scheme: '
               f'"{cue[:90]}" — wording agreement {agreement:.2f}')
        return
    else:
        pairs.append((ref, agreement))

    if cardlint.NAMES_LETTERS.search(question):
        refuse('the ask points at printed matter the card cannot carry', ref,
               f'{stamp} paper: "{question[:110]}"')
        return

    if any(PRIVATE_USE.search(a['text']) for a in answers):
        refuse('the scheme answers this ask with a font-private box glyph, '
               'not with words', ref,
               f'{stamp} scheme, "{sch.cue[:90]}" answered '
               f'"{answers[0]["text"][:60]}" — the Wingdings box U+F063 for '
               f'the empty box and U+F0FE for the marked one, which is the '
               f'SEC ticking a box rather than writing an answer')
        return
    if all(BARE_NUMBER.fullmatch(a['text']) for a in answers):
        refuse('the scheme answers this ask with a bare number, which no '
               'provenance check can tell from a marks cell', ref,
               f'{stamp} scheme, "{sch.cue[:90]}" answered '
               f'"{answers[0]["text"][:40]}" — the printed line is the digits '
               f'and nothing else, so the deck build cannot separate the '
               f'answer from the tariff beside it')
        return
    language = answer_language(subject, question)
    rows = _rows_for(subject, sch, language, count, per, total,
                     joined=(P.era == 'classic'))
    if rows is None:
        refuse('the scheme states fewer answers than it prices, and more than '
               'one, so which of them earns the marks is not stated', ref,
               f'{stamp} scheme, {notation} over {len(answers)} stated '
               f'answer(s) for "{sch.cue[:80]}"')
        return
    claimed = sum(r['group']['claimMax'] * r['group']['perOption']
                  if r.get('group') else (r['marks'] or 0) for r in rows)
    if claimed != total:
        refuse('the scheme prices this ask in groups the card model cannot '
               'hold as one', ref,
               f'{stamp} scheme, "{sch.cue[:80]}" priced {notation!r}: the '
               f'menu the card would show is worth {claimed} against the '
               f'{total} the scheme states, because the SEC prices the ask as '
               f'several separate groups — 2023 Higher 1(e) prices "Manhã", '
               f'"Tarde" and "Noite" at "2 marks: 2 x 1 mark (any 2)" each '
               f'under one six-mark head, and one anyN row cannot say that')
        return
    card = {
        'id': card_id(subject, year, level, ask.key),
        'subjectId': subject,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': ask.section,
        'topicId': topic_for(subject, P.era, ask.section),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': total,
        'rows': rows,
        'notes': (
            f'The {"paper" if P.era == "classic" else "scheme"} prints the '
            f'tariff as {notation!r}; the paper prints this ask on page '
            f'{ask.page} of the question booklet.'
            + (f' Paper and scheme are joined on the printed {joined_by}'
               + ('' if joined_by == 'address' else
                  ' inside the question, because the scheme letters it two '
                  'letters out of step with the paper')
               + f', wording agreement {agreement:.2f}.'
               if agreement is not None else
               ' The scheme of this sitting reprints no question, so the two '
               'documents are joined on the numbering they both print, which '
               'the census checks question by question.')),
    }
    lead = P.lead(ask.q)
    if lead and len(lead) >= 12:
        card['stem'] = lead
    source = source_material(P, ask, subject, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


def _recovered_answer(sch, paper_text):
    """The answer the scheme printed on the ask's own row, not under it.

    Two shapes, both read from the documents rather than assumed:

    * A TAIL. The scheme prints "aparece (parágrafo 2) surge" — the word the
      paper asks about, the paragraph it stands in, and then the synonym that
      answers it. Whatever follows the paragraph reference is the answer, and
      it is only taken when the paper does not print those words itself.
    * NO REPRINT AT ALL. 2022 Ordinary answers Question 1(f)(i) with the two
      words "Emprego / Carreira" and reprints nothing, because the paper
      already prints "trabalho (parágrafo 2)" and the scheme is a table of
      answers beside it. Where the scheme's line shares almost no wording with
      the paper's ask, the line IS the answer.
    """
    if not sch.cue or sch.answers:
        return []
    m = AFTER_REF.match(sch.cue)
    if m:
        tail = m.group('answer').strip()
        if len(tail) >= 3 and score(bag(tail), bag(paper_text)) <= MAX_ECHO:
            sch.cue = m.group('question')
            return [{'text': tail, 'marks': sch.per}]
    if score(bag(sch.cue), bag(paper_text)) <= MAX_ECHO and len(sch.cue) >= 3:
        text = sch.cue
        sch.cue = ''
        return [{'text': text, 'marks': sch.per}]
    return []


# A marking point printed as digits alone, and the SEC's font-private box
# glyphs. Both are answers a card cannot carry: the first is what the deck
# build's own provenance check reads as a marks cell, and the second is a
# ticked box rather than a word.
BARE_NUMBER = re.compile(r'^[\d\s.,/-]+$')
PRIVATE_USE = re.compile(r'[\ue000-\uf8ff]')

MIN_WORDS = 3


def _agreement(paper_text, cue):
    """How far the paper's ask and the scheme's reprint of it are one question.

    Divided by the SHORTER side, which is align.py's own rule and right here
    because both sides are whole asks. Guarded, because a one-word table cell
    divided by itself scores 1.00 against anything — under three content words
    the longer side decides.
    """
    a, b = bag(paper_text), bag(cue)
    if not a or not b:
        return 0.0
    shared = len(a & b)
    if min(len(a), len(b)) < MIN_WORDS:
        return shared / max(len(a), len(b))
    return shared / min(len(a), len(b))


def _cue_of(ask):
    """The question the scheme reprints, with its own stem in front of it."""
    return f'{ask.stem} {ask.cue}'.strip() if ask.stem else ask.cue


def _rows_for(subject, ask, language, count, per, total, joined=False):
    note = language_note(subject, language)
    if ask.part:
        # The rungs, verbatim and with the marks the scheme prints. Not a row
        # of their own: RowKind has no kind for an answer worth less than the
        # one above it, and the type says why — "Add it together with its
        # renderer, not before."
        rungs = '; '.join(f'“{r["text"]}” {r["marks"]} '
                          f'{"mark" if r["marks"] == 1 else "marks"}'
                          for r in ask.part[:4])
        note += (f' The scheme also pays part marks for a shorter answer: '
                 f'{rungs}.')
    options = [a['text'] for a in ask.answers if a['text']]
    if joined:
        # A classic scheme prints ONE model answer per question, broken over
        # as many printed lines as it needs. Offering its sentences as
        # separate things to claim would price half an answer.
        options = [' '.join(options)]
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': options[0],
                 'marks': total, 'contextNote': note}]
    if ask.additive:
        # Every answer is one ITEM of the ask and all of them are wanted, so
        # each is its own row at the marks the SEC printed beside it.
        return [dict({'id': f'r-{i + 1}', 'kind': 'point',
                      'verbatim': a['text'], 'marks': a['marks']},
                     **({'contextNote': note} if i == 0 else {}))
                for i, a in enumerate(
                    [x for x in ask.answers if x['marks'] is not None])
                ][:MAX_OPTIONS]
    priced = [a for a in ask.answers if a['marks'] is not None]
    if len(options) > 1 and len(priced) == len(options) \
            and all(a['marks'] == total for a in priced):
        # Several answers each priced at the WHOLE tariff: the SEC's
        # alternatives, of which a candidate offers one.
        claim, per_option = 1, total
    elif ask.any_n:
        claim, per_option = ask.any_n, per
    else:
        claim, per_option = count or 1, per
    if per_option is None:
        return None
    if claim == 1 and len(options) == 1:
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': options[0],
                 'marks': total, 'contextNote': note}]
    if len(options) < claim and len(options) > 1:
        # Several stated answers and a price for more of them: which of the
        # several the marks are earned on is not stated, so nothing is shipped.
        return None
    if len(options) < claim:
        # The scheme states fewer answers than it prices. That is not a menu:
        # it is one answer holding several details, and the SEC's own split is
        # disclosed on the row rather than turned into options that are not
        # there.
        return [{'id': 'r-1', 'kind': 'point',
                 'verbatim': ' / '.join(options), 'marks': total,
                 'contextNote': (
                     note + f' The scheme prices this answer {ask.notation!r}: '
                            f'the marks are earned detail by detail inside '
                            f'it.')}]
    trimmed = len(options) - MAX_OPTIONS
    return [{
        'id': 'r-1', 'kind': 'anyN',
        'verbatim': 'The answers the scheme accepts in full',
        'marks': None,
        'contextNote': (note + (
            f' The scheme lists {trimmed} further accepted answer(s) for this '
            f'ask.' if trimmed > 0 else '')),
        'group': {'claimMax': claim, 'perOption': per_option,
                  'options': options[:MAX_OPTIONS]},
    }]


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/<subject>.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded, pairs, faults = build(args.subject)

    if args.exclusions:
        path = os.path.join(DIR, 'exclusions', f'{args.subject}.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(excluded, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'{len(excluded)} exclusion(s) written to {path}')
        return 0

    if args.report:
        census = census_subject(args.subject)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} paper asks '
              f'({100 * len(cards) / total:.1f}%), {len(excluded)} refused')
        if pairs:
            worst = min(pairs, key=lambda t: t[1])
            print(f'pairing: {len(pairs)} pairs, weakest {worst[0]} at '
                  f'{worst[1]:.2f}')
        rows = sum(len(c['rows']) for c in cards)
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        print(f'{rows} marking rows holding {opts} stated answer(s) in menus')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:16} {n}')
        for where, want, got in faults:
            print(f'   UNSETTLED {where}: the scheme heads it {want} marks '
                  f'and its leaves add to {got}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:40 if args.all else 3]:
                print(f'             {e}')
        return 0

    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
