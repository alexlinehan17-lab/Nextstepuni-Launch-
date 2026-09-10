#!/usr/bin/env python3
"""Author every Polish ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/pl_all.py --report
    python3 scripts/markbank/authoring/pl_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/pl_all.py > scripts/markbank/authored/polish.json

Census-driven: the nine sittings print 553 leaf asks across two booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (pl_paper.py) and its
marking points from the SCHEME (pl_scheme.py). The two are read INDEPENDENTLY
and then paired on the address both documents print — which is safe here, and
only here, because the scheme REPRINTS the question above its answers, so
every pair is scored on wording as well and a pair that does not agree is
refused rather than shipped (Law 4).

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is a quotation from a text printed only in the question
paper. A card that asks for it without carrying the text is unanswerable, so
each one binds `sourceMaterial` to the exact pages of its own text in the
QUESTION paper — never the scheme, which is where the answers are.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
One comprehension is set in two languages: 2023 Higher asks (a) to (d) in
Polish and heads its next page "Answer questions (e) – (h) in English." The
scheme halves the marks for an answer in the wrong one, so every card says
which, read from the language its own question is printed in
(pl_topics.answer_language).

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

from pl_paper import PlPaper, bag, score, sittings              # noqa: E402
from pl_scheme import PlScheme                                  # noqa: E402
from pl_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, POLISH)
from paper_census import census_subject, key_label              # noqa: E402
import cardlint                                                 # noqa: E402

SUBJECT = 'polish'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts.
MAX_OPTIONS = 16
# Below this the paper's ask and the scheme's reprint of it are not the same
# question, and the pair is refused rather than shipped. Measured against the
# corpus: a true pair scores 0.55 and above once the scheme's directive and
# tariff are stripped, and the few that fall below it are asks the scheme
# rewrote rather than reprinted.
MIN_AGREEMENT = 0.34


def card_id(year, level, key):
    section, q, letter, roman = key
    parts = ['pl', str(year), level]
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


def source_material(P, ask, language, level, year):
    """The reading text's own printed pages, from the QUESTION paper."""
    pages = P.pages_for(ask.q)
    if not pages:
        return None
    lead = P.lead(ask.q) or f'Question {ask.q}'
    return {
        'kind': 'source-text',
        'label': lead.upper(),
        'title': f'Reading text — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC Polish {year} {LEVEL_TITLE[level]} Level '
                        f'examination paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the text exactly as the examination printed it, then answer. '
            + language_note(language)),
    }


# --------------------------------------------------------------- refusals ----
GRID_EVIDENCE = (
    'the scheme answers this task with a CONTENT AND EXPRESSION GRID and '
    'nothing else. It prices the task "(30 marks: Content 15 marks, '
    'Expression 15 marks)" and then describes the bands in prose — Content '
    '"Very good 15-12 · Stimulus material well exploited · High level of '
    'textual coherence · Clarity in argumentation", down to "Weak 3-0 · Lack '
    'of textual coherence"; Expression "Very good 15-12 · Idiomatic Polish · '
    'Rich vocabulary · Complex sentences well handled", down to "Weak 3-0 · '
    'Frequent spelling and grammar mistakes make text hard to understand". '
    'Those are the qualities of a piece of writing, not answers, and a card '
    'would ask a student to tick "Idiomatic Polish" as something they were '
    'supposed to have written.')

ESSAY_2021_EVIDENCE = (
    'the scheme answers this essay with a list of QUALITIES and a menu of '
    'things a candidate might think of, not an answer. Its own head reads '
    '"Przy przyznawaniu punktów brane pod uwagę następujące elementy: 1. '
    'Przejrzystość celu … 2. Spójność wypowiedzi … 3. Znajomość języka … 4. '
    'Zasady – gramatyka i ortografia", and under the title it prints '
    '"Refleksje typu:" followed by suggestions. No line of it is priced, so '
    'there is no tariff to put on a card and nothing a student could be marked '
    'right or wrong against.')

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet (component A00) whose own '
    'instructions read "Each listening comprehension piece will be played '
    'three times", and the booklet prints no text of what is said. The only '
    'printed source of that material is the marking scheme\'s own APPENDIX 2 '
    'CD SCRIPT — the ANSWER document — so carrying it on the card would hand '
    'the student the answers with the question. No verified playback copy of '
    'the SEC recording is bound to this deck, so the card would be '
    'unanswerable from what it shows.')


def build():
    cards, pairs, excluded = [], [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year, level in sittings(SUBJECT):
        P = PlPaper(year, level, SUBJECT)
        S = PlScheme(year, level, SUBJECT)
        priced = {a.key: a for a in S.reading()}
        choices = _choice_asks(S)
        verdicts = _verdict_groups(S, P)
        done_choices = set()
        stamp = f'{year} {level.upper()}'
        for ask in P.all_asks():
            key = ask.key
            ref = question_ref(year, level, key)
            section = ask.section or ''
            if section.startswith('L'):
                refuse('the ask needs the recording, which no card can carry',
                       ref, f'{stamp} Listening Comprehension Test, '
                            f'Section {section[1:]}: {AUDIO_EVIDENCE}')
                continue
            if section == 'II':
                refuse('the scheme prices no line of this essay, so there is '
                       'no tariff to put on a card', ref,
                       f'{stamp} scheme, CZĘŚĆ II: {ESSAY_2021_EVIDENCE}')
                continue
            if section == 'B':
                refuse('the scheme prints a content-and-expression grid for '
                       'this task, not an answer', ref,
                       f'{stamp} scheme, Część B Pisanie: {GRID_EVIDENCE}')
                continue
            group = (ask.section, ask.q, ask.letter)
            if ask.roman and group in verdicts:
                _verdict_card(P, verdicts[group], ask, year, level, ref, cards,
                              refuse)
                continue
            if ask.roman and group in choices:
                # A "tick the correct statement" ask. The paper letters the
                # rubric and numbers the options under it, so the census reads
                # four leaves; the SCHEME prices the ASK once and ticks one
                # option, so there is one tariff and one card. It cites the
                # letter, which is the address the scheme priced, and that
                # covers the options printed beneath it.
                if group not in done_choices:
                    done_choices.add(group)
                    _choice_card(P, S, choices[group], year, level, cards,
                                 refuse)
                continue
            _reading(P, S, priced, ask, year, level, ref, cards, refuse, pairs)
    return cards, refused, examples, excluded, pairs


def _choice_asks(S):
    """{(section, q, letter): (parent, ticked)} for every tick-one-box ask.

    Recognised from the scheme alone and from two facts together: the LETTER
    carries the tariff, and exactly one of the romans beneath it carries a tick
    in a right-hand column under no true/false heading. One tick and one price
    is one ask, however many boxes the paper prints under it.
    """
    kids = collections.defaultdict(list)
    for a in S._asks:
        if a.roman:
            kids[(a.section, a.q, a.letter)].append(a)
    out = {}
    for parent in S._asks:
        if parent.roman or parent.letter is None or parent.per is None:
            continue
        group = kids.get((parent.section, parent.q, parent.letter)) or []
        ticked = [k for k in group
                  if any(t['verdict'] is None for t in k.ticks)]
        if len(group) >= 2 and len(ticked) == 1 and not parent.answers \
                and not any(k.per for k in group):
            out[(parent.section, parent.q, parent.letter)] = (parent, ticked[0])
    return out


def _verdict_groups(S, P):
    """{(section, q, letter): (parent, [tick rows])} for a true/false table the
    scheme prints WITHOUT the paper's roman markers.

    2022 Higher prices Question 2(i) "(4 x 1m)" and then prints its four
    statements one under another with a tick in the Prawda or Fałsz column and
    no marker in front of any of them, where the paper numbers them (i) to
    (iv). There is no address to join on, so they are joined in printed ORDER —
    and order is only safe under two independent checks, which is the rule the
    Italian reader is built on: the scheme's row COUNT must equal the paper's,
    and every pair must agree in wording. _verdict_card enforces both.
    """
    out = {}
    kids = collections.defaultdict(list)
    for a in S._asks:
        if a.roman:
            kids[(a.section, a.q, a.letter)].append(a)
    for parent in S._asks:
        if parent.roman or parent.letter is None or parent.per is None:
            continue
        if kids.get((parent.section, parent.q, parent.letter)):
            continue
        ticks = [t for t in parent.ticks if t['verdict']]
        if len(ticks) < 2 or len(ticks) != len(parent.ticks):
            continue
        romans = [a for a in P._asks if a.section == parent.section
                  and a.q == parent.q and a.letter == parent.letter and a.roman]
        if len(romans) != len(ticks):
            continue
        out[(parent.section, parent.q, parent.letter)] = (parent, ticks)
    return out


def _verdict_card(P, pair, ask, year, level, ref, cards, refuse):
    parent, ticks = pair
    stamp = f'{year} {level.upper()}'
    romans = [a for a in P._asks if a.section == ask.section and a.q == ask.q
              and a.letter == ask.letter and a.roman]
    romans.sort(key=lambda a: (a.page, a.roman))
    try:
        i = [a.roman for a in romans].index(ask.roman)
    except ValueError:
        refuse('the scheme prints no verdict for this statement', ref,
               f'{stamp} scheme, "{parent.cue[:100]}"')
        return
    tick = ticks[i]
    question = ask.full_text
    agreement = _agreement(question, tick['statement'])
    if agreement < MIN_AGREEMENT:
        refuse('the paper and the scheme do not print the same statement in '
               'this row of the true/false table, so the pair cannot be '
               'trusted', ref,
               f'{stamp} paper: "{question[:90]}" against scheme row {i + 1}: '
               f'"{tick["statement"][:90]}" — wording agreement {agreement:.2f}')
        return
    language = answer_language(question)
    cards.append({
        'id': card_id(year, level, ask.key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'A' if year > 2021 else 'I',
        'topicId': topic_for(year, ask.section),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': f'{parent.cue} {question}'.strip(),
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': parent.per,
        'rows': [{'id': 'r-1', 'kind': 'point', 'verbatim': tick['verdict'],
                  'marks': parent.per,
                  'contextNote': (language_note(language) + ' The scheme marks '
                                  'this row by ticking one of the two columns '
                                  f'and prices the table {parent.notation!r}; '
                                  'more than one answer offered scores zero.')}],
        'notes': (f'The scheme prices this table {parent.notation!r} and answers '
                  f'this row by a tick in the {tick["verdict"]} column; the '
                  f'paper prints the statement on page {ask.page} of the '
                  f'question booklet. Paper/scheme wording agreement '
                  f'{agreement:.2f}.'),
        **({'sourceMaterial': source_material(P, ask, language, level, year)}
           if P.pages_for(ask.q) else {}),
    })


def _choice_card(P, S, pair, year, level, cards, refuse):
    parent, ticked = pair
    # The section is part of the address — see pl_paper.Ask.key. Dropped here
    # the citation read "2024 HL Q1(i)" and reconcile matched it onto the
    # LISTENING booklet's Section A question 1, which then reported four
    # correct exclusions stale and four covered asks open.
    key = (parent.section, parent.q, parent.letter, None)
    ref = question_ref(year, level, key)
    stamp = f'{year} {level.upper()}'
    paper_parent = next((a for a in P._asks
                         if a.q == parent.q and a.letter == parent.letter
                         and a.roman is None), None)
    options = [a for a in P._asks
               if a.q == parent.q and a.letter == parent.letter and a.roman]
    if paper_parent is None or len(options) < 2:
        refuse('the scheme ticks one option of a choice the paper does not '
               'print under that address', ref,
               f'{stamp} scheme, "{parent.cue[:100]}"')
        return
    printed = ' '.join(f'({o.roman}) {o.text}' for o in options)
    question = f'{paper_parent.text} {printed}'.strip()
    answer = ticked.ticks[0]['statement'] or ticked.cue
    answer = re.sub(r'^\(\s*[ivx]{1,4}\s*\)\s*', '', answer).strip()
    if not answer:
        refuse('the scheme ticks a box with no statement printed beside it',
               ref, f'{stamp} scheme, "{parent.cue[:100]}"')
        return
    language = answer_language(question)
    cards.append({
        'id': card_id(year, level, key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'A' if year > 2021 else 'I',
        'topicId': topic_for(year, parent.section),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': parent.total,
        'rows': [{'id': 'r-1', 'kind': 'point', 'verbatim': answer,
                  'marks': parent.per,
                  'contextNote': (language_note(language) + ' The scheme ticks '
                                  'one box and prices the whole question '
                                  f'{parent.notation!r}; more than one answer '
                                  'offered scores zero.')}],
        'notes': (f'The scheme prices this ask {parent.notation!r} and marks '
                  f'its answer by ticking one of the printed statements; the '
                  f'paper prints the options on page {paper_parent.page} of '
                  f'the question booklet.'),
        **({'sourceMaterial': source_material(P, paper_parent, language, level,
                                              year)}
           if P.pages_for(parent.q) else {}),
    })


def _reading(P, S, priced, ask, year, level, ref, cards, refuse, pairs):
    stamp = f'{year} {level.upper()}'
    sch = priced.get(ask.key)
    if sch is None:
        refuse('the scheme prices no ask at the address the paper prints', ref,
               f'{stamp} paper: "{ask.full_text[:110]}" — the scheme\'s Section '
               f'A prices no ask at this address')
        return
    example = WORKED_EXAMPLE.search(ask.stem or '')
    if example and ask.roman == 'i':
        refuse('the SEC prints this row as the worked example and prices it at '
               'no marks', ref,
               f'{stamp} paper: the ask above it reads "{ask.stem[:110]}" — the '
               f'SEC fills this row in for the candidate, and the scheme prices '
               f'it {sch.notation or "with a dash"} accordingly')
        return
    if ORDERING.search(ask.stem or ''):
        refuse('the ask is one row of an ordering task, and its answer is a '
               'position in a list the card cannot carry', ref,
               f'{stamp} paper: "{ask.stem[:110]}" — the scheme answers this '
               f'row "{sch.cue[:60]}", where the number at the end is the place '
               f'the event takes in the sequence. One row of it is not a '
               f'question a student can be asked on its own.')
        return
    if sch.fault:
        refuse('the scheme prices the ask two ways at once, so neither number '
               'can be trusted', ref,
               f'{stamp} scheme, "{sch.cue[:90]}": {sch.fault}')
        return
    if sch.total is None or sch.per is None:
        refuse('the scheme states no tariff for this ask', ref,
               f'{stamp} scheme, "{sch.cue[:110]}" — the scheme prints answers '
               f'with no marks beside them')
        return
    answers = [a for a in sch.answers if a['text']]
    if GAP.search(ask.full_text or ''):
        # A COMPLETION. The paper prints the sentence with a hole in it and the
        # scheme prints it whole, so everything the scheme prints under this
        # address is the answer — cue and marking rows together. Read as a
        # reprinted question and an answer beneath it, the 2025 Ordinary
        # completions shipped their last word alone: "polskim." for
        # "W programach profesora Miodka widzowie zadają pytania związane
        # z językiem polskim."
        whole = ' '.join([sch.cue] + [a['text'] for a in answers]).strip()
        if whole:
            answers = [{'text': ' '.join(whole.split()), 'marks': sch.per}]
            sch.answers = answers
    if not answers:
        # Written back onto the ask, not just returned: the rows are built from
        # the ask, and a recovery that only reached the local name shipped
        # twenty cards whose menu listed nothing at all.
        sch.answers = _recovered_answer(sch, ask.full_text)
        answers = sch.answers
    if not answers:
        refuse('the scheme states no answer for this ask, only its price', ref,
               f'{stamp} scheme, "{sch.cue[:110]}" priced {sch.notation!r} with '
               f'no marking point printed under it')
        return
    if sch.count and len(answers) < sch.count:
        refuse('the scheme prices more answers than it states', ref,
               f'{stamp} scheme, {sch.notation} over {len(answers)} stated '
               f'answer(s) for "{sch.cue[:80]}"')
        return

    question = ask.full_text
    cue = _cue_of(sch)
    # Scored four ways and the best taken, because either document may carry
    # the parent's stem and the other may not: the paper prints "Wyjaśnij
    # znaczenie podanych wyrażeń:" over "(i) czuć się wypalonym" while the
    # scheme reprints the roman alone, and scoring only the two full forms
    # against each other refused five correct pairs on the stem's own words.
    agreement = max(_agreement(question, cue), _agreement(question, sch.cue),
                    _agreement(ask.text, cue), _agreement(ask.text, sch.cue))
    if agreement < MIN_AGREEMENT:
        refuse('the paper and the scheme do not print the same question at '
               'this address, so the pair cannot be trusted', ref,
               f'{stamp} paper: "{question[:90]}" against scheme: '
               f'"{cue[:90]}" — wording agreement {agreement:.2f}')
        return
    pairs.append((ref, agreement))

    boxes = [o['text'].strip().rstrip('.') for o in answers]
    if boxes and all(len(b) == 1 and b.isupper() for b in boxes) \
            and not all(re.search(rf'\b{b}[.)]', question) for b in boxes):
        # The scheme answers by NAMING a printed box — "C (2 marks)" — and the
        # boxes are set in a table the card does not carry. Where the paper
        # prints the options in the question itself the card is answerable and
        # ships; where it prints them only as boxes, "C" is not an answer a
        # student could have reached from what the card shows.
        refuse('the scheme answers by naming a printed box the card cannot '
               'carry', ref,
               f'{stamp} scheme, "{sch.cue[:80]}" answered '
               f'{", ".join(boxes)} — the paper prints those options in a '
               f'table of boxes the card does not hold')
        return
    if cardlint.NAMES_LETTERS.search(question):
        refuse('the ask points at printed matter the card cannot carry', ref,
               f'{stamp} paper: "{question[:110]}"')
        return

    language = answer_language(question)
    rows = _rows_for(sch, language)
    card = {
        'id': card_id(year, level, ask.key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'A' if year > 2021 else 'I',
        'topicId': topic_for(year, ask.section),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': sch.total,
        'rows': rows,
        'notes': (f'The scheme prints the tariff as {sch.notation!r}; the paper '
                  f'prints this ask on page {ask.page} of the question booklet. '
                  f'Paper/scheme wording agreement {agreement:.2f}.'),
    }
    lead = P.lead(ask.q)
    if lead and len(lead) >= 12:
        card['stem'] = lead
    source = source_material(P, ask, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


# The paragraph reference the SEC closes a reprinted question with, and
# whatever it prints AFTER that reference.
AFTER_REF = re.compile(
    r'^(?P<question>.*\((?:akapit\w*|akapity|paragraphs?|sections?|'
    r'cz[eę][sś][cć]\w*|p)\b[^)]*\))\s*(?P<answer>\S.*)$', re.I)
# A gap the paper prints for the candidate to fill.
GAP = re.compile(r'_{3,}')
# How much of the recovered tail may also appear in the paper's own question
# before it stops being an answer and starts being more of the question.
MAX_ECHO = 0.2


def _recovered_answer(sch, paper_text):
    """The answer the scheme printed on the ask's own row, not under it.

    Two shapes, both read from the documents rather than assumed:

    * A COMPLETION. The paper prints "Zdaniem Sary ludziom ________ jest
      łatwiej." and the scheme prints the same sentence finished — "Zdaniem
      Sary ludziom otwartym jest łatwiej." The gap in the paper is the proof:
      the scheme's line is not a reprint of the question, because the question
      has a hole in it.
    * A TAIL. The paper prints "Tatuaż był odmiennie postrzegany w różnych
      kulturach. (akapit 2)" and the scheme reprints exactly that and then adds
      "różnie/niejednolicie/odrębnie" on the same line. Whatever follows the
      paragraph reference is the answer, and it is only taken when the paper
      does not print those words itself — otherwise it is more of the question.
    """
    if not sch.cue or sch.answers:
        return []
    if GAP.search(paper_text or ''):
        return [{'text': sch.cue, 'marks': sch.per}]
    m = AFTER_REF.match(sch.cue)
    if not m:
        return []
    tail = m.group('answer').strip()
    if len(tail) < 3:
        return []
    if score(bag(tail), bag(paper_text)) > MAX_ECHO:
        return []
    sch.cue = m.group('question')
    return [{'text': tail, 'marks': sch.per}]


# The SEC's own words for a row it has filled in as the example, and for an
# ordering task. Both are read from the paper's printed rubric, not guessed.
WORKED_EXAMPLE = re.compile(
    r'zgodnie\s+z\s+przykładem|według\s+przykładu|'
    r'according\s+to\s+the\s+example|as\s+in\s+the\s+example|'
    r'example\s*\(\s*i\s*\)', re.I)
ORDERING = re.compile(
    r'Ponumeruj|Number\s+them|order\s+in\s+which\s+they\s+appear|'
    r'Put\s+the\s+sentences\s+below\s+in\s+the\s+order', re.I)

MIN_WORDS = 3


def _agreement(paper_text, cue):
    """How far the paper's ask and the scheme's reprint of it are one question.

    Divided by the SHORTER side, which is align.py's own rule and right here
    because both sides are whole asks: the scheme reprints the rubric above a
    true/false statement and the paper prints the statement alone, so dividing
    by the longer side scores a correct pair at 0.20 and refused sixteen of
    them. Guarded, because a one-word table cell divided by itself scores 1.00
    against anything — under three content words the longer side decides.
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
    cue = f'{ask.stem} {ask.cue}'.strip() if ask.stem else ask.cue
    return cue


def _rows_for(ask, language):
    note = language_note(language)
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
    if ask.count == 1 and len(options) == 1:
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': options[0],
                 'marks': ask.per, 'contextNote': note}]
    trimmed = len(options) - MAX_OPTIONS
    row = {
        'id': 'r-1', 'kind': 'anyN',
        'verbatim': 'The answers the scheme accepts in full',
        'marks': None,
        'contextNote': (note + (
            f' The scheme lists {trimmed} further accepted answer(s) for this '
            f'ask.' if trimmed > 0 else '')),
        'group': {'claimMax': ask.count, 'perOption': ask.per,
                  'options': options[:MAX_OPTIONS],
                  # A DESCENDING ladder rides as the steps the SEC printed. The
                  # 2021 scheme pays "3 punkty za jeden przykład, po 1 punkcie
                  # za każdy następny" against a printed total of five, which
                  # is 3 + 1 + 1; flattened to three-at-three the card would
                  # tell a student the question is worth nine.
                  **({'perOptionSteps': ask.steps} if ask.steps else {})},
    }
    if ask.steps:
        row['contextNote'] += (
            f' The scheme pays a descending ladder here, in its own words: '
            f'"{ask.directive}" — {", ".join(str(n) for n in ask.steps)} '
            f'marks, in that order, to a printed total of {ask.total}.')
    return [row]


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/polish.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded, pairs = build()

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
        if pairs:
            worst = min(pairs, key=lambda t: t[1])
            print(f'pairing: {len(pairs)} pairs, weakest {worst[0]} at '
                  f'{worst[1]:.2f}')
        rows = sum(len(c['rows']) for c in cards)
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        print(f'{rows} marking rows holding {opts} stated answer(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:14} {n}')
        by_lang = collections.Counter(
            POLISH if language_note(POLISH) in (c['rows'][0].get('contextNote') or '')
            else 'English/Irish' for c in cards)
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
