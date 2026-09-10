#!/usr/bin/env python3
"""Author every Japanese ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/ja_all.py --report
    python3 scripts/markbank/authoring/ja_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/ja_all.py > scripts/markbank/authored/japanese.json

Census-driven: the ten sittings print 1,108 leaf asks across two booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Which document supplies its question depends on what the SEC
printed, and this paper prints two different shapes:

  * a STATED question — "What is the name of the non-alcoholic cocktail?" —
    which the scheme reprints above its answer. The scheme's reprint is the
    card's question, because it is the SEC's own English (or Japanese) and the
    paper prints it twice over, Irish beside English on one line;
  * a printed ITEM — 外国人, 抹茶を飲みます。, a kanji with four readings under
    it — which the scheme answers without reprinting anything. There the card's
    question is the item the PAPER prints and its stem is the part's own
    instruction, because the instruction is the whole of what is being asked:
    "Write the meaning of any FIVE of the following Kanji in English".

The family is decided per PART, from how many of its scheme leaves carry a
reprinted question, not per ask — a part is one task type throughout.

HOW THE TWO DOCUMENTS ARE JOINED
--------------------------------
Not on the part key (Law 4). The scheme letters its parts independently and
visibly disagrees: 2024 Ordinary heads question 2's four parts "A.", "B.",
"Part B." and "Part C." where the paper heads them "A.", "B.", "C. KANJI" and
"D.". They are paired in printed ORDER inside each component, and only where
two independent counts agree first — the same number of parts, and the same
number of asks inside each paired part (paper_census.ja_flags). Where either
disagrees, nothing in that part is carded: the asks stay OPEN in the ledger
rather than being paired on a guess.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is drawn from a web page, an article, a blog or an e-mail
printed only in the question paper. Each card binds `sourceMaterial` to those
pages in the QUESTION paper — never the scheme, which is where the answers are.

FURIGANA
--------
The SEC sets a kana reading above the kanji it glosses. A card is one line of
text and the paper sets it on two, so ja_text.py folds each run in after the
character it was centred over — 秋葉原（あきはばら） — and every card carrying
Japanese discloses the convention (ja_topics.FURIGANA_NOTE).

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report, and every
refusal that lands on a census leaf becomes an exclusions entry carrying the
evidence for it (--exclusions writes them).
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

from ja_paper import JaPaper, sittings                        # noqa: E402
from ja_scheme import JaScheme                                # noqa: E402
from ja_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, FURIGANA_NOTE, JAPANESE, HIRAGANA)
from paper_census import census_subject, key_label            # noqa: E402
import cardlint                                               # noqa: E402

SUBJECT = 'japanese'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_OPTION_ROWS in
# types/markBank.ts. A trim is DISCLOSED on the row, in the SEC's own order.
MAX_OPTIONS = 8

# How the scheme prints a bounded choice inside one answer: "any three details,
# 1 mark each", "any two details, 2 marks + 1 mark", "(Any 2, 1 mark each)".
ANY_N = re.compile(
    r'\(?\s*any\s+(two|three|four|five|six|seven|eight|\d{1,2})\s*'
    r'(?:details?|answers?|points?|of\s+the\s+above)?\s*,?\s*'
    r'(?:(\d{1,2})\s*marks?\s*each'
    r'|((?:\d{1,2}\s*(?:marks?)?\s*\+\s*)+\d{1,2}\s*marks?))?', re.I)
WORDS = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
         'eight': 8, 'nine': 9, 'ten': 10}
# The part-marks the scheme sets inside an answer to show how it divides.
INLINE_MARKS = re.compile(r'\s*\(\s*\d{1,2}\s*marks?\s*\)', re.I)
SENTENCE_END = re.compile(r'[?？。｡.]')
# How an ask ENDS, as against an answer: a question mark, or the か。 that
# closes every Japanese-set question in these papers. A full stop closes both —
# the scheme answers 2022 Ordinary's grammar item (vi) "かえりました。" — so
# a full stop cannot be the test.
QUESTION_END = re.compile(r'[?？]\s*$|[かカ]\s*[。｡]\s*$')
MARKER_ONLY = re.compile(r'[\s(]*[a-hivx]{1,4}[).\s]*', re.I)
TABLE = re.compile(r'Complete\s+the\s+(?:following\s+)?(?:table|chart)'
                   r'|Comhl[áa]naigh\s+an\s+(?:t[áa]bla|chairt)', re.I)


def card_id(year, level, section, q, letter, roman):
    parts = ['ja', str(year), level, section.lower()]
    parts += [str(x) for x in (q, letter, roman) if x is not None]
    return '-'.join(parts)


def question_ref(year, level, key):
    """The citation, in the census's own words — key_label is the authority."""
    return f'{year} {level.upper()} {key_label(key)}'


def source_material(P, section, year, level, language):
    pages = P.source_pages(section)
    if not pages:
        return None
    return {
        'kind': 'source-text',
        'label': f'問題{section[0]}',
        'title': f'Question {section[0]} — printed material',
        'pages': pages,
        'attribution': (f'SEC Japanese {year} {LEVEL_TITLE[level]} Level '
                        f'examination paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the printed material exactly as the examination set it, then '
            f'answer. {language_note(language, level)} {FURIGANA_NOTE}'),
    }


def _clean(text):
    return ' '.join((text or '').split())


def _key(text):
    """Text with its punctuation and case removed, for comparing two copies."""
    return re.sub(r'[^0-9a-z\u00c0-\u017f\u3040-\u30ff\u3400-\u9fff]+', '',
                  (text or '').lower())


def _bilingual_english(text):
    """The English half of an ask the paper prints in Irish and in English.

    Higher sets both on one line divided by a slash — "Cén fáth a ndéantar Lá
    Pocky & Pretz a cheiliúradh ar 11 Samhain?/Why is Pocky & Pretz Day
    celebrated on November 11th?" — so the half after the last slash is the
    English one. Returned only where the split is unambiguous; a question set
    in Japanese has no slash and is returned whole.
    """
    t = _clean(text)
    if '/' not in t:
        return t
    # The MIDDLE-most slash, not the last one. A kanji instruction prints its
    # worked example after the English half — "… i nGaeilge. / Write the
    # meaning of any FIVE of the following Kanji in English. e.g. 日本 An
    # tSeapáin / Japan" — and cutting at the last slash left "Japan" as the
    # whole instruction, then failed its own length guard and left both
    # languages on the card.
    cuts = [i for i, ch in enumerate(t) if ch == '/'
            and len(t[:i].strip()) >= 8 and len(t[i + 1:].strip()) >= 8]
    if not cuts:
        return t
    cut = min(cuts, key=lambda i: abs(i - len(t) / 2))
    return t[cut + 1:].strip()


# A scheme line short enough to be a table CELL rather than a sentence. The
# kanji sections set three answers across a row — the kanji, the option letter,
# and the meaning — and joining them with spaces makes a string the scheme
# never printed contiguously, which the build's provenance gate rightly refuses.
# Joined with em dashes they are checked on the last piece, which is the
# convention the bank already uses for a two-part answer.
CELL = 25


def _verbatim(leaf):
    lines = [INLINE_MARKS.sub(' ', l).strip(' .,;:—-') for l in leaf.lines]
    lines = [l for l in lines if l]
    if not lines:
        return ''
    if len(lines) > 1 and all(len(l) <= CELL for l in lines):
        return ' — '.join(lines)
    return _clean(' '.join(lines))


def _english_column(ask):
    """The English half of an Ordinary ask, which is set in a second COLUMN.

    Higher divides its two languages with a slash on one line; Ordinary sets
    Irish in a left column and English in a right one, and the reader joins the
    row, so the two arrive with nothing between them: "Déan cur síos ar dhá rud
    faoi chlub Akira. 3. Describe two things about Akira's club."

    What separates them is the ask's OWN MARKER, printed a second time at the
    head of the English column. So the cut is that marker, printed again inside
    the line — which is the paper's own furniture, not a guess about wording.
    """
    text = _clean(ask.text)
    marks = [f'{ask.q}.'] + [f'({t})' for t in (ask.letter, ask.roman) if t]
    cut = None
    for tok in marks:
        i = text.rfind(tok)
        if i > 8 and i + len(tok) < len(text) - 8:
            cut = max(cut or 0, i + len(tok))
    if cut:
        return text[cut:].strip()
    # No repeated marker to cut on — the kanji sections number the ROW and set
    # the item itself twice, once over the Irish options and once over the
    # English: "何 (a)cathain (b) cá (c) cad (d) conas 何 (a) when (b) where
    # (c) what (d) how". There the repeat of the item's own opening is the
    # column bound, and the two halves are the same length either side of it.
    head = text[:4].strip()
    if len(head) >= 2:
        i = text.rfind(head)
        if i > 6 and 0.6 <= (len(text) - i) / i <= 1.6 \
                and LATIN.search(text[i:]):
            return text[i:].strip()
    return text


def _options(body):
    """The answers the scheme accepts, and how many of them it wants.

    Returns (options, claim, per) or None. The scheme states the count and the
    rate in its own words — "(any three details, 1 mark each)", "(any two
    details, 2 marks + 1 mark)" — and where it states neither there is no
    bounded choice to model and the whole line is one answer.
    """
    m = ANY_N.search(body)
    if not m:
        return None
    claim = WORDS.get(m.group(1).lower()) if not m.group(1).isdigit() \
        else int(m.group(1))
    if not claim:
        return None
    stated = body[:m.start()].strip(' .,')
    stated = INLINE_MARKS.sub(' ', stated)
    opts = [o.strip(' .,') for o in re.split(r'[/,、]|\bor\b', stated)
            if len(o.strip(' .,')) > 1]
    if len(opts) < claim:
        return None
    if m.group(2):
        per = [int(m.group(2))] * claim
    elif m.group(3):
        per = [int(x) for x in re.findall(r'\d{1,2}', m.group(3))]
        if len(per) != claim:
            return None
    else:
        return None
    return opts, claim, per


def build():
    cards = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    excluded = []
    open_asks = []
    seen = set()

    def refuse(reason, ref, evidence='', stated=True):
        """Record a refusal, and say whether it is an EXCLUSION or an OPEN ask.

        An exclusion is a claim about the DOCUMENTS — that the SEC prints no
        answer this card model can hold — and it needs the printed evidence for
        that claim. A refusal that is a claim about this READER, that it cannot
        pair the paper with the scheme here or cannot find the tariff, is not
        an exclusion at all: it is work not done, and it belongs in the ledger
        as OPEN so that it goes on being counted against the denominator.
        """
        if ref in seen:
            return
        seen.add(ref)
        refused[reason] += 1
        examples[reason].append(ref)
        if stated:
            excluded.append({'ref': ref, 'reason': reason,
                             'evidence': evidence})
        else:
            open_asks.append({'ref': ref, 'reason': reason,
                              'evidence': evidence})

    def emit(card):
        cards.append(card)
        seen.add(card['questionRef'])

    for year, level in sittings(SUBJECT):
        P = JaPaper(year, level, SUBJECT)
        S = JaScheme(year, level, SUBJECT)
        _listening(P, year, level, refuse)
        _writing(P, year, level, refuse)
        _reading(P, S, year, level, emit, refuse)
    return cards, refused, examples, excluded, open_asks


# --------------------------------------------------------------- reading ---
def _reading(P, S, year, level, emit, refuse):
    """Pair the two documents QUESTION by question, then part by part.

    Both documents print the question number — the paper as 問題1 … 問題3, the
    scheme as "Question 1" — so the pairing never crosses a question boundary.
    It matters: the 2025 Ordinary scheme divides question 1 into two parts
    where the paper heads none, and pairing across the whole component then
    put question 2's first part against question 1's second, six asks against
    six asks, which every count check passes and every card would be wrong.
    """
    paper = collections.OrderedDict()
    for ask in P.asks():
        if ask.section[0] in '123':
            paper.setdefault(ask.section, []).append(ask)
    scheme = S.by_part()
    for q in ('1', '2', '3'):
        pkeys = [k for k in paper if k[0] == q]
        skeys = [k for k in scheme if k[0] == 'R' and str(k[1]) == q]
        if not pkeys:
            continue
        blocks = _align(pkeys, skeys, paper, scheme)
        if blocks is None:
            for pk in pkeys:
                for ask in paper[pk]:
                    refuse('the paper and the scheme do not head the same '
                           'number of parts in this question, so no part of '
                           'it can be paired',
                           question_ref(year, level, ask.key),
                           f'{year} {level.upper()} 問題{q}: the paper heads '
                           f'{len(pkeys)} part(s) ({", ".join(pkeys)}) and '
                           f'the scheme prices {len(skeys)}', stated=False)
            continue
        for pks, sks in blocks:
            pp = [a for pk in pks for a in paper[pk]]
            ss = [lf for sk in sks for lf in scheme[sk]]
            _part(P, pp, ss, '+'.join(pks), q, year, level, emit, refuse)


def _align(pkeys, skeys, paper, scheme):
    """Pair the two documents' parts, allowing one to SUBDIVIDE the other.

    The two do not always head the same number of parts, and where they differ
    it is because one of them divided a part the other kept whole: the 2022
    Ordinary scheme sets question 3's first part in two ("A: (19 marks)" and
    "B: (9 marks)") where the paper heads one, and the 2025 Ordinary scheme
    divides question 1 the same way.

    So the two lists are cut wherever their RUNNING TOTALS agree, and a block
    is accepted only where one side of it is a single part. A block that is
    several parts on BOTH sides pairs nothing, because then the totals agreeing
    says only that the paper and the scheme hold the same number of asks
    somewhere in that stretch — not that any one of them is the same ask.
    """
    pn = [len(paper[k]) for k in pkeys]
    sn = [len(scheme[k]) for k in skeys]
    if len(pn) == len(sn):
        # Same number of heads: pair them off, and let each pair answer for
        # itself. A part the scheme heads and leaves empty is refused alone,
        # not treated as a reason to give up on the question around it.
        return [([p], [s]) for p, s in zip(pkeys, skeys)]
    if sum(pn) != sum(sn):
        return None
    blocks, i, j = [], 0, 0
    while i < len(pn) and j < len(sn):
        pi, sj, a, b = i, j, pn[i], sn[j]
        i += 1
        j += 1
        while a != b:
            if a < b and i < len(pn):
                a, i = a + pn[i], i + 1
            elif b < a and j < len(sn):
                b, j = b + sn[j], j + 1
            else:
                return None
        if i - pi > 1 and j - sj > 1:
            return None
        blocks.append((pkeys[pi:i], skeys[sj:j]))
    if any(pn[i:]) or any(sn[j:]):
        return None
    return blocks


NO_ANSWER_EVIDENCE = (
    'the scheme HEADS this part and then prints no answer under it. The '
    'culture-and-society section is set "Deirtear go bhfuil réim bia na '
    'Seapánach an-sláintiúil. Luaigh dhá fháth go bhfuil sé sin amhlaidh. / '
    'The Japanese diet is said to be very healthy. Give two reasons why." and '
    'the scheme answers it with the tariff alone — "D: (4 marks) … 2 marks '
    'each for any 2 points" — because what it credits is the candidate\'s own '
    'knowledge of Japan, marked on its merits. There is nothing printed to '
    'lift, and inventing the two reasons would be writing the answer.')


def _part(P, pp, ss, pk, q, year, level, emit, refuse):
    if not ss:
        for ask in pp:
            refuse('the scheme states no answer for this ask',
                   question_ref(year, level, ask.key),
                   f'{year} {level.upper()} Section {pk}: {NO_ANSWER_EVIDENCE}')
        return
    if len(pp) != len(ss):
        for ask in pp:
            refuse('the paper and the scheme do not print the same number '
                   'of asks in this part, so nothing in it can be paired',
                   question_ref(year, level, ask.key),
                   f'{year} {level.upper()} Section {pk}: the paper prints '
                   f'{len(pp)} ask(s), the scheme prices {len(ss)}', stated=False)
        return
    stated = sum(1 for lf in ss if len(lf.head) > 12) >= 0.5 * len(ss)
    if stated and not _wording_agrees(pp, ss):
        for ask in pp:
            refuse('the scheme\'s reprinted questions do not match the '
                   'paper\'s in this part, so the order pairing is not '
                   'trusted', question_ref(year, level, ask.key),
                   f'{year} {level.upper()} Section {pk}: the scheme reprints '
                   f'the question it is answering and fewer than half of its '
                   f'reprints share wording with the paper ask paired to them', stated=False)
        return
    for ask, lf in zip(pp, ss):
        _one_card(P, ask, lf, stated, year, level, emit, refuse)


def _rubric_stem(rubric):
    """The part's instruction, as the card's stem: English, and no marker.

    Dropped where the two printed columns interleave past recovering. The
    Ordinary instruction is set in two columns and its wrapped lines arrive
    shuffled — "Cuir ciorcal thart ar an mbrí cheart (a), (b), (c) nó (d) atá
    leis na Kanji seo a leanas mar atá sa 3. Circle the correct meaning …" —
    and cardlint's own label-junk rule is what says so, imported rather than
    reimplemented so the build cannot drift from the lint.
    """
    t = _bilingual_english(rubric)
    t = re.sub(r'^\s*\d{1,2}\s*[.)]\s*', '', t)
    t = re.sub(r'^\s*[A-D]\s*[:.]\s*', '', t)
    t = _clean(t)
    return None if not t or cardlint.label_junk(t) else t


WORD = re.compile(r"[A-Za-z\u00c0-\u017f]{4,}")
LATIN = re.compile(r"[A-Za-z]{3,}")
JA_CHAR = re.compile(r'[぀-ヿ㐀-鿿]')


def _wording_agrees(pp, ss):
    """align.py's rule, in the one place this paper allows it.

    Where the scheme REPRINTS the question it is answering, the pairing can be
    checked rather than trusted: the reprint and the paper's own ask share
    words. A Latin-script ask is scored on words of four letters or more; an
    ask set in Japanese is scored on the characters themselves, because
    Japanese sets no spaces and there are no words to split on.
    """
    hits = 0
    scored = 0
    for ask, lf in zip(pp, ss):
        head, text = lf.head, ask.text
        # Only where the scheme actually reprinted a question. A part mixes
        # shapes — 2023 Higher's 問題1 opens with a matching task the scheme
        # answers "Global Sales 6" and then sets four stated questions — and
        # counting the matching items as failures refused the whole part.
        if len(head) <= 12 or not text:
            continue
        scored += 1
        a = set(w.lower() for w in WORD.findall(head))
        b = set(w.lower() for w in WORD.findall(text))
        if a and b:
            if len(a & b) >= 2 or (len(a) <= 2 and a & b):
                hits += 1
            continue
        ja = set(JA_CHAR.findall(head)) & set(JA_CHAR.findall(text))
        if len(ja) >= 3:
            hits += 1
    return scored == 0 or hits >= 0.5 * scored


def _one_card(P, ask, lf, stated, year, level, emit, refuse):
    ref = question_ref(year, level, ask.key)
    where = (f'{year} {level.upper()} scheme, question {lf.q} part {lf.part} '
             f'item {lf.address}')
    if lf.marks is None:
        refuse('the scheme prints no tariff this reads for the ask', ref,
               f'{where}: answer {lf.body[:90]!r}', stated=False)
        return
    rubric = P.item_rubric(ask.section, ask.q)
    body = _clean(lf.body)
    # Where the scheme sets the ANSWER on the marker's own row and nothing
    # under it — the Ordinary kanji section prints "(iii) b" and stops — the
    # head is the answer, not a reprinted question. Read the other way round it
    # said "the scheme states no answer for this ask" about thirteen asks the
    # scheme answers in one character, which is an open ask laundered into an
    # exclusion; the ratchet refused the re-measure and was right to.
    if not body and lf.head and not QUESTION_END.search(lf.head) \
            and len(lf.head) <= 60:
        lf.lines, lf.head, body = [lf.head], '', lf.head
    # The scheme's reprinted question WRAPS onto the row that carries the
    # answer: 2025 Higher prints "Name two travel items recommended on" and
    # then "April 20th. ear plugs, neck pillow, slippers (any 2 …)". Left as
    # it stood, the card asked half a question and offered the other half as
    # an accepted answer.
    if body and lf.head and not SENTENCE_END.search(lf.head):
        m = SENTENCE_END.search(body[:48])
        if m:
            lf.head = f'{lf.head} {body[:m.end()]}'.strip()
            first = lf.lines[0] if lf.lines else ''
            cut = min(m.end(), len(first))
            rest = _clean(first[cut:])
            lf.lines = ([rest] if rest else []) + lf.lines[1:]
            body = _clean(' '.join(lf.lines))
    if not _verbatim(lf).strip(' .,;:—-'):
        body = ''
    if not body:
        refuse('the scheme states no answer for this ask', ref,
               f'{where}: the scheme prints the question and a tariff and '
               f'nothing between them')
        return

    # Decided per ASK, not per part: 問題1's first item is a matching task the
    # scheme answers with "Global Sales 6" and its second a stated question it
    # reprints in full, and one part holds both. Where the scheme reprinted the
    # question, that reprint is the card's question, because the paper prints
    # its own twice over — Irish beside English — and wraps it across rows.
    stem = _rubric_stem(rubric)
    if stated and len(lf.head) > 12:
        question = _bilingual_english(lf.head)
    else:
        question = _bilingual_english(_english_column(ask))
    # ONE character can be a whole ask. 2024 Higher's kanji section prints
    # "(iii) 話" and asks for its reading; a three-character floor written for
    # a Latin-script language refused twenty-eight of them.
    if TABLE.search(question) or TABLE.search(rubric) or TABLE.search(body):
        # The answer to "Complete the table" IS a table: a grid of cells whose
        # column and row heads are printed in the paper and whose contents are
        # printed in the scheme, laid out across the page. Flattened onto one
        # line it is not an answer to anything — 2021 Higher's reads "Name of
        # the top-selling item Description of item (two details) For men The
        # North Face 20 litres/ for hiking" — and a card model that cannot
        # render a grid cannot hold it. Excluded until the model can.
        refuse('the answer is a table, which this card model cannot render',
               ref, f'{where}: the scheme answers this ask with a grid — '
                    f'{body[:120]!r}')
        return
    if MARKER_ONLY.fullmatch(question):
        refuse('the paper prints no question text this reads for the ask', ref,
               f'{where}: paper text {ask.text[:90]!r}', stated=False)
        return
    if not question:
        refuse('the paper prints no question text this reads for the ask', ref,
               f'{where}: paper text {ask.text[:90]!r}', stated=False)
        return

    # The scheme reprints the question ABOVE its answer, and where its reprint
    # and the answer share a row they arrive as one string: 2025 Higher's
    # "Give details about Ronan's friend Tsuyoshi. same maths course, sits
    # beside him, …". Left in, the question became the first accepted answer
    # on its own card. Where the scheme's copy runs on past the paper's — the
    # paper wraps its asks and the reader takes the marker's own row — the
    # scheme's fuller sentence is the question, because it is the SEC's own.
    if body.lower().startswith(question.lower()[:40]) and len(question) > 12:
        end = SENTENCE_END.search(body, max(len(question) - 4, 0))
        cut = end.end() if end and end.end() - len(question) < 50 \
            else len(question)
        question = _clean(body[:cut]) or question
        # Cut it out of the LINES too, not just the joined body: the row is
        # rebuilt from the lines, and stripping only the copy left the question
        # standing as the first accepted answer on two cards.
        first = lf.lines[0] if lf.lines else ''
        if first.lower().startswith(question.lower()[:40]):
            rest = _clean(first[len(question):])
            lf.lines = ([rest] if rest else []) + lf.lines[1:]
        body = _clean(' '.join(lf.lines)) or body

    language = answer_language(question, rubric)
    note = language_note(language, level)
    opts = _options(body)
    if opts:
        options, claim, per = opts
        shown = options[:MAX_OPTIONS]
        if sum(per[:claim]) != lf.marks:
            # The scheme's own count and rate do not add up to the tariff it
            # prints beside them. Neither reading is the SEC's, so the ask is
            # not priced — and NEVER GUESS A TARIFF.
            refuse('the scheme\'s printed count and rate do not add up to the '
                   'tariff printed beside them', ref,
                   f'{where}: {lf.marks} marks against {claim} answer(s) at '
                   f'{"+".join(map(str, per))}', stated=False)
            return
        group = {'claimMax': claim, 'perOption': per[0], 'options': shown}
        if len(set(per)) > 1:
            group['perOptionSteps'] = per
        row = {'id': 'r-1', 'kind': 'anyN',
               'verbatim': 'The answers the scheme accepts',
               'marks': None, 'group': group, 'contextNote': note}
        if len(options) > len(shown):
            row['contextNote'] += (
                f' The scheme lists {len(options) - len(shown)} further '
                f'accepted answer(s) than this card shows, in the order it '
                f'prints them.')
        rows = [row]
    else:
        rows = [{'id': 'r-1', 'kind': 'point',
                 'verbatim': _verbatim(lf),
                 'marks': lf.marks, 'contextNote': note}]

    card = {
        'id': card_id(year, level, ask.section, ask.q, ask.letter, ask.roman),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': ask.section[0],
        'topicId': topic_for(int(ask.section[0]), rubric),
        'conceptId': concept_for(
            question, fallback=f'ja-{ask.section.lower()}-'
                               f'{ask.q or 0}{ask.letter or ""}{ask.roman or ""}'),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': lf.marks,
        'rows': rows,
        'notes': (f'The scheme prices this ask {lf.marks} '
                  f'{"mark" if lf.marks == 1 else "marks"}; the paper prints '
                  f'it on page {ask.page + 1} of the question booklet.'),
    }
    # A stem that repeats the question is noise on the card, not a lead-in —
    # and it repeats it down to the SEC's own comma: "What did Kai buy for his
    # dog and when will he use the item?" against "…dog, and when…".
    if stem and _key(stem) not in _key(question) and _key(question) not in _key(stem):
        card['stem'] = stem
    source = source_material(P, ask.section, year, level, language)
    if source:
        card['sourceMaterial'] = source
    emit(card)


# ------------------------------------------------ what is not an answer ----
AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet (component A00) whose own '
    'cover reads "Seinnfear gach píosa trí huaire: an chéad uair ó thús '
    'deireadh, ansin ina míreanna agus sosanna iontu" — each part will be '
    'played three times — and the booklet prints no text of what is said. The '
    'only printed source of that material is the marking scheme\'s own '
    'TAPESCRIPT, which is the ANSWER document: 2024 Higher prints Part B as '
    '"ス： はい、皆さんこんにちは。スカイ・ブラウンと言います。" beside the '
    'answers to the questions about it. Carrying it on the card would hand the '
    'student the answers with the question, and no verified playback copy of '
    'the SEC recording is bound to this deck, so the card would be '
    'unanswerable from what it shows.')

WRITING_EVIDENCE = (
    'the scheme prices this ask with a CONTENT AND EXPRESSION GRID and states '
    'no answer. 2024 Higher heads question 4 "Content marks 20 marks / 18 '
    'marks (2 x 9 marks) / 2 discretionary marks" and then prints its '
    'expression bands as prose about the candidate\'s writing rather than '
    'about the question: "Vocabulary use good – rich, idiomatic and '
    'appropriate. Few word order mistakes. No or very few mistakes using '
    'Hiragana and Katakana. Good use of Kanji." Those are qualities of a '
    'composition, not answers to a question, and a card would ask a student '
    'to tick "good use of Genkouyoushi" as something they were supposed to '
    'have written. The paper itself sets the ask as a free composition — '
    '"Scríobh ar a laghad 200 carachtar Seapáinise / Write about (a) OR (b) '
    'OR (c) in no less than 200 Japanese characters".')


def _listening(P, year, level, refuse):
    for ask in P.aural_asks():
        refuse('the ask needs the recording, which no card can carry',
               question_ref(year, level, ask.key),
               f'{year} {level.upper()} Listening Comprehension Test, '
               f'{ask.section}: {AUDIO_EVIDENCE}')


def _writing(P, year, level, refuse):
    for ask in P.asks():
        if ask.section[0] in '45':
            refuse('the scheme prices this ask with a content-and-expression '
                   'grid, not an answer',
                   question_ref(year, level, ask.key),
                   f'{year} {level.upper()} scheme, question '
                   f'{ask.section[0]}: {WRITING_EVIDENCE}')


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/japanese.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded, open_asks = build()

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
              f'({100 * len(cards) / total:.1f}%), {len(excluded)} excluded, '
              f'{len(open_asks)} open')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:14} {n}')
        by_lang = collections.Counter(
            JAPANESE if JAPANESE in (c['rows'][0].get('contextNote') or '')
            else HIRAGANA if HIRAGANA in (c['rows'][0].get('contextNote') or '')
            else 'English or Irish' for c in cards)
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
