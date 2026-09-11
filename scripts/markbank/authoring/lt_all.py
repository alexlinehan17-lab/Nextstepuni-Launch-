#!/usr/bin/env python3
"""Author every Lithuanian ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/lt_all.py --report
    python3 scripts/markbank/authoring/lt_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/lt_all.py > scripts/markbank/authored/lithuanian.json

Census-driven: the twenty-two sittings print 807 leaf asks across their
booklets, and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (lt_paper.py) and its
marking points from the SCHEME (lt_scheme.py). The two are read INDEPENDENTLY
and then paired on the address both documents print — which is safe here, and
only here, because the scheme REPRINTS the question above its answers, so every
pair is scored on wording as well and a pair that does not agree is refused
rather than shipped (Law 4).

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is a quotation from a text printed only in the question
paper. A card that asks for it without carrying the text is unanswerable, so
each one binds `sourceMaterial` to the exact pages of its own text in the
QUESTION paper — never the scheme, which is where the answers are.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
From 2022 one comprehension is set in two languages: 2024 Higher asks (a) to
(i) in Lithuanian and heads the next "Answer question (j) in English." The
scheme halves the marks for an answer in the wrong one, so every card of those
sittings says which, read from the language its own question is printed in
(lt_topics.answer_language).

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

from lt_paper import LtPaper, bag, score, sittings              # noqa: E402
from lt_scheme import LtScheme                                  # noqa: E402
from lt_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, LANGUAGE)
from paper_census import census_subject, key_label              # noqa: E402
import cardlint                                                 # noqa: E402

SUBJECT = 'lithuanian'
ID_PREFIX = {'lithuanian': 'lt', 'latvian': 'lv', 'czech': 'cs'}
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts.
MAX_OPTIONS = 16
# Below this the paper's ask and the scheme's reprint of it are not the same
# question, and the pair is refused rather than shipped. Measured against the
# corpus, exactly as pl_all did: a true pair scores 0.55 and above once the
# scheme's directive and tariff are stripped, and the few that fall below it
# are asks the scheme rewrote rather than reprinted.
MIN_AGREEMENT = 0.34


def card_id(subject, year, level, key):
    section, q, letter, roman = key
    parts = [ID_PREFIX[subject], str(year), level]
    if section:
        parts.append(str(section).lower())
    parts.append(str(q))
    if letter:
        parts.append(letter)
    if roman:
        parts.append(str(roman))
    return '-'.join(parts)


def question_ref(year, level, key):
    return f'{year} {level.upper()} {key_label(key)}'


def source_material(P, ask, language, level, year, subject):
    """The reading text's own printed pages, from the QUESTION paper."""
    pages = P.pages_for(ask.section, ask.q)
    if not pages:
        return None
    lead = P.lead(ask.section, ask.q) or f'Question {ask.q}'
    return {
        'kind': 'source-text',
        'label': lead.upper(),
        'title': f'Reading text — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC {LANGUAGE[subject]} {year} {LEVEL_TITLE[level]} '
                        f'Level examination paper — '
                        f'© State Examinations Commission.'),
        'presentationNote': (
            'Read the text exactly as the examination printed it, then answer. '
            + language_note(subject, language, year)),
    }


# --------------------------------------------------------------- refusals ----
GRID_EVIDENCE = (
    'the scheme answers this task with a MARKING GRID and nothing else. It '
    'heads the section "Mark content and language / expression separately" and '
    'then prints three bands for each: Content and Communication "TOP · Very '
    'good or excellent achievement of the task/s · High level of textual '
    'coherence · Clear argumentation · Full completion of communicative task" '
    'down to "BOTTOM · Lack of textual coherence · Communicative task barely '
    'fulfilled or not fulfilled at all"; Language "TOP · Very good range of '
    'vocabulary · Verb endings, tenses, agreements nearly always correct" down '
    'to "BOTTOM · Most words misspelt, wrong word formation". Those are the '
    'qualities of a piece of writing, not answers, and a card would ask a '
    'student to tick "Idiomatic Lithuanian" as something they were supposed to '
    'have written.')

ESSAY_EVIDENCE = (
    'the scheme answers this essay with a description of a good essay and '
    'nothing that could be marked right or wrong. Under the two titles it '
    'prints one sentence — "Rišliai parašytas rašinys, atsakantis į pasirinktą '
    'temą, atspindintis logišką minties dėstymą, parodantis, jog užduotis '
    'suprasta, parašytas aiškia ir taisyklinga kalba (apytiksliai 300 '
    'žodžių)" — which describes a coherent, well-argued, correctly written '
    'essay of about 300 words. No line of it is priced, so there is no tariff '
    'to put on a card.')

COMMENTARY_EVIDENCE = (
    'the scheme answers this commentary with one continuous MODEL ANSWER of '
    'its own and prices nothing inside it. The task is "Pakomentuokite šią '
    'ištrauką. Savo teiginius argumentuokite (ne mažiau kaip 100 žodžių)" — '
    'comment on this extract in at least a hundred words — and the scheme '
    'prints a hundred-odd words of finished commentary against the single '
    'printed total the part head carries. There is no marking point in it to '
    'claim and no split to divide it by, so a card would offer a whole essay '
    'as one thing to have written.')

MODEL_PARAGRAPH_EVIDENCE = (
    'the scheme answers this with a continuous MODEL PARAGRAPH and prices '
    'nothing inside it. The old examination sets its Questions 2 to 6 at five '
    'taškai each and answers each one with unbroken prose — measured across '
    'the twelve sittings the answers run from 131 to 1,789 characters, with no '
    'bullet, no directive, no "Any two of:" and no split beside the printed '
    'total. Five marks over an answer the SEC never divided cannot be turned '
    'into marking rows without inventing the division, which is the one thing '
    'this bank never does. Contrast the SAME question\'s part (a) to (e), '
    'which are priced one taškas each against a stated gloss and card in full.')

# A sitting whose SCHEME cannot be read at all, keyed the way paper.py keys an
# SEC misprint — (subject, year, level) — and never by a heuristic.
UNREADABLE = {
    ('czech', 2015, 'hl'): (
        'the 2015 scheme embeds a subset font whose ToUnicode map collapses '
        'several accented letters onto ONE code point, so the same character '
        'stands for different letters in different words and no map can undo '
        'it. Its text layer returns "VysvČtlete" for "Vysvětlete", "kterČ" '
        'for "které", "každČ" for "každé" and "vČznam" for "význam" — one '
        'glyph doing the work of ě, é and ý — and it returns "ýást 1" for '
        '"Část 1", a letter of the alphabet standing for another letter of '
        'the same alphabet. derive_glyphs.py\'s own rule applies: a mangled '
        'code point that means two different characters cannot be repaired '
        'from the character alone, so it is dropped rather than guessed. '
        'Every other sitting of this subject reads clean; the repair map for '
        'the ones that need one is in glyphmap-czech.json.'),
}

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet (component A00) whose own '
    'instructions read "The conversation will be played three times: first '
    'right through, then in segments with pauses, and finally right through '
    'again", and the booklet prints no text of what is said. The only printed '
    'source of that material is the marking scheme\'s own APPENDIX 2 CD SCRIPT '
    '— the ANSWER document — so carrying it on the card would hand the student '
    'the answers with the question. No verified playback copy of the SEC '
    'recording is bound to this deck, so the card would be unanswerable from '
    'what it shows.')


def build(subject=SUBJECT):
    cards, pairs, excluded = [], [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year, level in sittings(subject):
        P = LtPaper(year, level, subject)
        S = LtScheme(year, level, subject)
        priced = {a.key: a for a in S.reading()}
        priced.update(_order_pairs(P, S))
        printed = _scheme_text(subject, year, level)
        vocab = _vocabulary_questions(P, S)
        done_vocab = set()
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
            if section == 'B':
                refuse('the scheme prints a marking grid for this written task, '
                       'not an answer', ref,
                       f'{stamp} scheme, SECTION B Written Production: '
                       f'{GRID_EVIDENCE}')
                continue
            if section == 'III' or (section == 'II' and year == 2021):
                refuse('the scheme prices no line of this essay, so there is no '
                       'tariff to put on a card', ref,
                       f'{stamp} scheme, {"III" if section == "III" else "II"} '
                       f'DALIS: {ESSAY_EVIDENCE}')
                continue
            if section == 'II':
                refuse('the scheme answers this commentary with one continuous '
                       'model answer and prices nothing inside it', ref,
                       f'{stamp} scheme, II DALIS: {COMMENTARY_EVIDENCE}')
                continue
            group = (ask.section, ask.q)
            if ask.letter and group in vocab:
                if group not in done_vocab:
                    done_vocab.add(group)
                    _vocabulary_card(P, vocab[group], year, level, cards,
                                     refuse, subject, printed)
                continue
            _reading(P, S, priced, ask, year, level, ref, cards, refuse, pairs,
                     subject, printed)
    return cards, refused, examples, excluded, pairs


# The SEC's own words for a row it has filled in as the example, for an
# ordering task and for a matching task. All three are read from the printed
# rubric, not guessed.
WORKED_EXAMPLE = re.compile(
    r'pagal\s+pavyzd|kaip\s+pavyzdyje|according\s+to\s+the\s+example|'
    r'as\s+in\s+the\s+example', re.I)
ORDERING = re.compile(
    r'Sunumeruokite|Eiliškum|Number\s+them|'
    r'order\s+in\s+which\s+they\s+appear', re.I)
MATCHING = re.compile(
    r'[ĮI]rašykite\s+atsakymo\s+raid|Suderinkite\s+sakinius|'
    r'Sudarykite\s+sakinius|Suderinkite\s+žodžius|'
    r'Raskite\s+tekste\s+pabrauktų\s+žodžių\s+reikšmes|'
    r'Match\s+the\s+\w+|inserting\s+the\s+letters', re.I)
# A gap the paper prints for the candidate to fill.
GAP = re.compile(r'_{3,}')
# The five-mark prose questions of the old examination — see
# MODEL_PARAGRAPH_EVIDENCE.
def _is_model_paragraph(P, ask):
    """A five-mark question of the old examination, answered in prose.

    Read from the ERA and the printed address, not from the year: Latvian and
    Czech print the old examination in every one of their seventeen sittings,
    and a year test would have carded none of them the same way. It is checked
    BEFORE the scheme is consulted, because the reason these are refused has
    nothing to do with whether the scheme reader reached them — it is what the
    SEC printed.
    """
    return P.era != 'new' and ask.section == 'I' and ask.letter is None


def _order_pairs(P, S):
    """{paper key: scheme ask} where the two documents NUMBER the same rows
    differently.

    2025 Ordinary prints the five statements of Q2(i) as "1." to "5." and its
    scheme prints the same five as "i." to "v.", in the same order and in
    almost the same words. There is no address to join on, so they are joined
    in printed ORDER — and order is only safe under two independent checks,
    which is the rule the Italian reader is built on and the one pl_all's
    verdict groups use:

      * the two documents must print the SAME NUMBER of rows under that
        letter, and
      * every pair must agree in WORDING at or above MIN_AGREEMENT.

    One pair failing either test abandons the whole letter rather than
    shifting the rest by one, because an off-by-one here is a wrong verdict on
    a true/false row and passes every downstream gate.
    """
    out = {}
    paper_kids = collections.defaultdict(list)
    for a in P._asks:
        if a.roman:
            paper_kids[(a.section, a.q, a.letter)].append(a)
    scheme_kids = collections.defaultdict(list)
    for a in S._asks:
        if a.roman:
            scheme_kids[(a.section, a.q, a.letter)].append(a)
    for group, kids in paper_kids.items():
        theirs = scheme_kids.get(group) or []
        if len(kids) < 2 or len(kids) != len(theirs):
            continue
        if {k.roman for k in kids} == {t.roman for t in theirs}:
            continue                    # the two agree, so nothing to pair
        kids = sorted(kids, key=lambda a: (a.page, a.roman))
        theirs = sorted(theirs, key=lambda a: (a.page, a.roman))
        scored = [_agreement(k.full_text, f'{t.stem} {t.cue}'.strip())
                  for k, t in zip(kids, theirs)]
        if min(scored) < MIN_AGREEMENT:
            continue
        for k, t in zip(kids, theirs):
            out[k.key] = t
    return out


def _vocabulary_questions(P, S):
    """{(section, q): (parent, [(paper letter, scheme letter)])} for a question
    the scheme prices WHOLE over lettered parts it does not price separately.

    The old examination opens with a vocabulary task — "Skaidrojiet vārdus un
    frāzes!", "Vysvětlete vlastními slovy:" — that lists five expressions from
    the text and glosses each one. Lithuanian prices them a taškas each and
    they card one per letter. Latvian and Czech mostly do NOT: the price is
    printed once on the question, "[5 bodů]", and the five parts carry none.

    Dividing that by five would be inventing a tariff, so the card is made at
    the level the scheme priced — one card for the question, `questionTotal`,
    with the SEC's own gloss on a row for each expression. Nothing is guessed:
    the total is printed, the glosses are printed, and what a student may
    claim is bounded by the question's total, which is exactly what that
    tariff model is for.
    """
    out = {}
    scheme_kids = collections.defaultdict(list)
    for a in S._asks:
        if a.letter and a.roman is None:
            scheme_kids[(a.section, a.q)].append(a)
    for parent in S._asks:
        if parent.letter or parent.roman or parent.total is None:
            continue
        kids = sorted(scheme_kids.get((parent.section, parent.q)) or [],
                      key=lambda a: a.letter)
        if len(kids) < 2 or any(k.per is not None for k in kids):
            continue
        if not all(k.answers for k in kids):
            continue
        paper_kids = sorted(
            (a for a in P._asks
             if (a.section, a.q) == (parent.section, parent.q) and a.letter
             and a.roman is None),
            key=lambda a: a.letter)
        if [k.letter for k in paper_kids] != [k.letter for k in kids]:
            continue
        out[(parent.section, parent.q)] = (parent, list(zip(paper_kids, kids)))
    return out


def _vocabulary_card(P, pair, year, level, cards, refuse, subject, printed):
    parent, rows = pair
    key = (parent.section, parent.q, None, None)
    ref = question_ref(year, level, key)
    stamp = f'{year} {level.upper()}'
    options = [k.answers[0]['text'] for _p, k in rows]
    missing = _untraceable(printed, options)
    if missing:
        refuse('the scheme markdown the provenance gate reads does not hold '
               'this answer as one run of words', ref,
               f'{stamp} scheme, "{parent.cue[:80]}": "{missing[0][:80]}"')
        return
    printed_asks = ' '.join(f'({p.letter}) {p.text}' for p, _k in rows)
    question = _norm_space(f'{parent.cue} {printed_asks}')
    language = answer_language(subject, question)
    note = language_note(subject, language, year)
    cards.append({
        'id': card_id(subject, year, level, key),
        'subjectId': subject,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'U1',
        'topicId': topic_for(subject, year, parent.section, parent.q),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        # The scheme prices the QUESTION and none of its five parts, so what a
        # student may claim is bounded by that total rather than by a per-row
        # value the SEC never printed.
        'tariffModel': {'kind': 'questionTotal'},
        'totalMarks': parent.total,
        'rows': [{'id': f'r-{i + 1}', 'kind': 'point',
                  'verbatim': k.answers[0]['text'], 'marks': None,
                  'contextNote': (f'The scheme prints this as the meaning of '
                                  f'"{k.cue or p.text}". {note}')}
                 for i, (p, k) in enumerate(rows)],
        'notes': (f'The scheme prices this question {parent.notation!r} and '
                  f'prints no mark against any of its {len(rows)} parts, so '
                  f'the card carries the question total and the SEC\'s gloss '
                  f'for each expression. The paper prints the ask on page '
                  f'{rows[0][0].page} of the question booklet.'),
        **({'sourceMaterial': source_material(P, rows[0][0], language, level,
                                              year, subject)}
           if P.pages_for(parent.section, parent.q) else {}),
    })


def _norm_space(text):
    return re.sub(r'\s+', ' ', text).strip()


SCHEME_MD = os.path.join(ROOT, 'examiner-reports')


def _scheme_text(subject, year, level):
    """The scheme markdown the PROVENANCE GATE reads, normalised for lookup.

    Not the PDF and not this directory's own reader: the build compares a
    card's marking points against `examiner-reports/<subject>/schemes/<year>-
    <level>.md`, and a point that is not in there is dropped however faithfully
    it was lifted. So the check is made HERE, against the same file, and an ask
    that cannot be traced is refused with its reason rather than authored and
    silently dropped by the build — which is the difference between a ledger
    that closes and seven cards reported open forever.
    """
    path = os.path.join(SCHEME_MD, subject, 'schemes', f'{year}-{level}.md')
    if not os.path.exists(path):
        return ''
    with open(path, encoding='utf-8') as fh:
        return _flatten(fh.read())


TRACE_STRIP = re.compile(r'[^0-9a-ząčęėįšųūžāēģīķļņáéíóúýčďěňřšťůž ]+', re.I)


def _flatten(text):
    return re.sub(r'\s+', ' ', TRACE_STRIP.sub(' ', text.lower()))


def _untraceable(printed, options):
    """The stated answers that are NOT in the scheme markdown, in order."""
    if not printed:
        return []
    return [o for o in options if _flatten(o).strip()
            and _flatten(o).strip() not in printed]


def _reading(P, S, priced, ask, year, level, ref, cards, refuse, pairs,
             subject, printed=''):
    stamp = f'{year} {level.upper()}'
    stem = ask.stem or ''
    # The SHAPE of the task is read from the PAPER's own rubric, and it is read
    # before anything is asked of the scheme. An ordering task and a matching
    # task are refused whether or not the scheme keys a row under the address —
    # and it usually does not, because the scheme answers the whole table in
    # one line of letters. Tested after the scheme, thirty-eight of these
    # reported "the scheme prices no ask at that address", which is true and
    # says nothing about why the row cannot be carded.
    if ORDERING.search(stem) or ORDERING.search(ask.text):
        refuse('the ask is one row of an ordering task, and its answer is a '
               'position in a list the card cannot carry', ref,
               f'{stamp} paper: "{(stem or ask.text)[:110]}" — the answer to '
               f'this row is the number it takes in the sequence, and one row '
               f'of it is not a question a student can be asked on its own')
        return
    if MATCHING.search(stem) or MATCHING.search(ask.text):
        refuse('the scheme answers by naming a printed box the card cannot '
               'carry', ref,
               f'{stamp} paper: "{(stem or ask.text)[:110]}" — the scheme '
               f'answers this task with a row of letters under a row of '
               f'numbers ("1. 2. 3. / C A B"), where each letter names a '
               f'half-sentence printed in a facing column the card does not '
               f'hold')
        return
    unreadable = UNREADABLE.get((subject, year, level))
    if unreadable and ask.section == 'I' and ask.letter:
        refuse('the scheme\'s text layer cannot be read for this sitting', ref,
               f'{stamp} scheme: {unreadable}')
        return
    if _is_model_paragraph(P, ask):
        refuse('the scheme answers this with one continuous model paragraph '
               'and prices nothing inside it', ref,
               f'{stamp} scheme, "{ask.full_text[:90]}": '
               f'{MODEL_PARAGRAPH_EVIDENCE}')
        return
    sch = priced.get(ask.key)
    if sch is None:
        refuse('the scheme prices no ask at the address the paper prints', ref,
               f'{stamp} paper: "{ask.full_text[:110]}" — the scheme\'s reading '
               f'section prices no ask at this address')
        return
    if WORKED_EXAMPLE.search(stem) and ask.roman in ('i', '1'):
        refuse('the SEC prints this row as the worked example and prices it at '
               'no marks', ref,
               f'{stamp} paper: the ask above it reads "{stem[:110]}"')
        return
    if sch.fault:
        refuse('the scheme prices the ask two ways at once, so neither number '
               'can be trusted', ref,
               f'{stamp} scheme, "{sch.cue[:90]}": {sch.fault}')
        return
    if sch.total is None or sch.per is None:
        parent = next((a for a in S._asks
                       if (a.section, a.q, a.letter) ==
                       (ask.section, ask.q, ask.letter) and a.roman is None),
                      None)
        rows = sum(1 for a in P._asks
                   if (a.section, a.q, a.letter) ==
                   (ask.section, ask.q, ask.letter) and a.roman)
        if parent is not None and parent.count and rows and parent.count != rows:
            refuse('the scheme prices the task above this row over fewer rows '
                   'than the paper prints, so no row carries a stated tariff',
                   ref,
                   f'{stamp} scheme, "{parent.cue[:90]}" priced '
                   f'{parent.notation!r} — a split over {parent.count} where '
                   f'the paper prints {rows} rows under it, because the SEC '
                   f'answers one of them itself as the worked example or '
                   f'because only the correct rows are paid. The tariff for '
                   f'THIS row is nowhere on the page, and dividing the total '
                   f'by the rows would be inventing one.')
            return
        refuse('the scheme states no tariff for this ask', ref,
               f'{stamp} scheme, "{sch.cue[:110]}" — the scheme prints answers '
               f'with no marks beside them and no split above them')
        return
    answers = [a for a in sch.answers if a['text']]
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
    cue = f'{sch.stem} {sch.cue}'.strip() if sch.stem else sch.cue
    # Scored four ways and the best taken, because either document may carry
    # the parent's stem and the other may not — pl_all's reasoning, and the
    # same five correct pairs are refused without it.
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

    missing = _untraceable(printed, [a['text'] for a in answers])
    if missing:
        refuse('the scheme markdown the provenance gate reads does not hold '
               'this answer as one run of words', ref,
               f'{stamp} scheme, "{sch.cue[:80]}": the SEC sets these answers '
               f'in two columns and the flat extraction reads ACROSS the page, '
               f'so "{missing[0][:80]}" is printed with the other column\'s '
               f'words in the middle of it. The reader recovers the column and '
               f'the card would be right, but nothing on disk could be checked '
               f'against, and a marking point this bank cannot trace does not '
               f'ship.')
        return
    language = answer_language(subject, question)
    rows = _rows_for(sch, subject, language, year)
    card = {
        'id': card_id(subject, year, level, ask.key),
        'subjectId': subject,
        'level': LEVEL_WORD[level],
        'year': year,
        # The unit a student navigates by is the TASK, not the "Dalis A" tab
        # that only separates reading from writing — see the section union in
        # types/markBank.ts. Dalis A prints one to three tasks numbered by
        # Lithuanian ordinals, and the old examination's I DALIS is one text
        # with six questions on it, so it is the first task too.
        'section': f'U{ask.q}' if P.era == 'new' else 'U1',
        'topicId': topic_for(subject, year, ask.section, ask.q),
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
    lead = P.lead(ask.section, ask.q)
    if lead and len(lead) >= 12:
        card['stem'] = lead
    source = source_material(P, ask, language, level, year, subject)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


MIN_WORDS = 3


def _agreement(paper_text, cue):
    """How far the paper's ask and the scheme's reprint of it are one question.

    Divided by the SHORTER side, which is align.py's own rule and right here
    because both sides are whole asks: the scheme reprints the rubric above a
    true/false statement and the paper prints the statement alone. Guarded,
    because a one-word table cell divided by itself scores 1.00 against
    anything — under three content words the longer side decides.
    """
    a, b = bag(paper_text), bag(cue)
    if not a or not b:
        return 0.0
    shared = len(a & b)
    if min(len(a), len(b)) < MIN_WORDS:
        return shared / max(len(a), len(b))
    return shared / min(len(a), len(b))


def _rows_for(ask, subject, language, year):
    note = language_note(subject, language, year)
    if ask.part:
        # The part-credit rungs, verbatim and with the marks the scheme prints.
        # Not a row of their own: RowKind has no kind for an answer worth less
        # than the one above it, and the type says why — "Add it together with
        # its renderer, not before."
        rungs = '; '.join(f'“{r["text"]}” {r["marks"]} '
                          f'{"mark" if r["marks"] == 1 else "marks"}'
                          for r in ask.part[:4] if r['marks'] is not None)
        if rungs:
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
                  'options': options[:MAX_OPTIONS]},
    }
    if ask.open_list:
        row['openList'] = True
        row['contextNote'] += (' The scheme closes its list with "Etc.", so an '
                               'answer it does not print may still be right.')
    return [row]


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/<subject>.json from the refusals')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--subject', default=SUBJECT)
    args = ap.parse_args()
    cards, refused, examples, excluded, pairs = build(args.subject)

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
        print(f'{rows} marking rows holding {opts} stated answer(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:16} {n}')
        own = LANGUAGE[args.subject]
        by_lang = collections.Counter(
            own if f'answered in {own.upper()}' in (
                c['rows'][0].get('contextNote') or '') else 'English/Irish'
            for c in cards)
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
