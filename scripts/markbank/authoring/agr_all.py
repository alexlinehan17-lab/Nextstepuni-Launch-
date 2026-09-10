#!/usr/bin/env python3
"""Author every Ancient Greek ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/agr_all.py --report
    python3 scripts/markbank/authoring/agr_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/agr_all.py \
        > scripts/markbank/authored/ancient-greek.json

Census-driven: the 27 sittings on disk print 758 leaf asks, and this walks that
census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (agr_paper) and its marking
points from the SCHEME's "Additional notes and indicative answers" section
(agr_scheme). The two are read independently and paired on the address both
documents print — which is safe here because the schemes' tariff table repeats
the paper's own skeleton question for question and route for route, and
`agr_flags` checks every address one holds against the other before a card is
made.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Question 1 Section B's eight questions are about a Greek passage printed only
in the question paper, and its grammar and scansion parts quote words out of
it. Each of those cards binds `sourceMaterial` to the exact pages of its own
passage in the QUESTION paper — never the scheme, which is where the answers
are. Question 4's photograph parts bind the plate pages the same way.

THE THREE REFUSALS, AND WHY EACH IS THE SCHEME'S OWN DOING
----------------------------------------------------------
**Translation into Greek** (Question 1 Section A). The scheme prices the
ENGLISH the candidate is given, cut into units with a mark after each, and
never prints the Greek that would be the answer. That is Latin's finding in
Greek.

**Translation into English** (Question 2 everywhere, Question 3(i) at Higher,
Questions 1 and 2(i) at Ordinary). The scheme prices the GREEK the candidate
is given, cut into units with a mark after each — "ἔπειτα δὲ γίγνεται ……
πορεύεσθαι· 7" — and prints no English at all. Its own note says why: "Each
mark allocation represents a complete unit of meaning to be translated."

**No marking scheme at all.** The SEC published none for eleven of the 27
sittings the corpus holds a paper for — every Ordinary sitting but 2015, 2019
and 2023, and 2021 Higher. Those papers are censused all the same, so the
denominator stays the paper, and every ask on them is excluded with the file
listing as its evidence.
"""
import argparse
import collections
import json
import os
import re
import sys
import unicodedata

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from agr_paper import AgrPaper, sittings                        # noqa: E402
from agr_scheme import AgrScheme, has_scheme                    # noqa: E402
from agr_topics import topic_for, concept_for                   # noqa: E402
from paper_census import key_label                              # noqa: E402
import cardlint                                                 # noqa: E402

SUBJECT = 'ancient-greek'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
MAX_ROWS = 16

# What the SEC prints when it means "mark the whole answer out of ten by
# impression" — a ceiling, not a split.
IMPRESSION = re.compile(r'^Impression\s+ex\s+(\d{1,3})', re.I)
# A printed SPLIT: "8 + 8 + 7 + 7", "(8 + 7) + (8 + 7)", "5 + (5 + 5)".
SPLIT = re.compile(r'^[\d\s+()]+$')
# Where a plate is named, so its pages can be bound to the card.
PLATE_REF = re.compile(r'Photograph[s]?\s+([A-E])(?:\s*(?:,|and|&)\s*([A-E]))?'
                       r'(?:\s*(?:,|and|&)\s*([A-E]))?', re.I)


def card_id(year, level, key):
    section, q, letter, roman = key
    parts = ['agr', str(year), level]
    if section:
        parts.append(str(section).lower())
    parts.append(f'q{q}')
    if roman:
        parts.append(roman)
    if letter:
        parts.append(letter)
    return '-'.join(parts)


def question_ref(year, level, key):
    return f'{year} {level.upper()} {key_label(key, SUBJECT)}'


# --------------------------------------------------------------- evidence ---
COMPOSITION_EVIDENCE = (
    'the scheme states no Greek for this ask. It prints the ENGLISH the '
    'candidate is given, cut into the units it prices — "The philosopher '
    '................................................ unlocked. 6", "One '
    'night ........................................... valuable. 7" — and '
    'the Greek that would be the answer appears nowhere in the document. Its '
    'only other line on the ask is "Apply Positive Credit Marking system." '
    'Measured across the sixteen schemes on disk: the 81 priced lines under '
    'Question 1 Section A carry 0 Greek characters between them and 1.36 '
    'English function words each.')

UNSEEN_EVIDENCE = (
    'the scheme states no English for this ask. It prints the GREEK the '
    'candidate is given, cut into units with a mark after each — "ἔπειτα δὲ '
    'γίγνεται ....................... πορεύεσθαι· 7", "οὐ γὰρ '
    '............................ ἐπιτήδεια. 4" — and no translation of any '
    'of it. The scheme says so itself under Qu. 2: "Each mark allocation '
    'represents a complete unit of meaning to be translated. Full marks are '
    'awarded per unit of meaning based on demonstrating thorough '
    'understanding of syntax and vocabulary." Measured across the sixteen '
    'schemes on disk: 707 priced translation lines carry 12,507 Greek '
    'characters and 26 English function words between them — 17.8 Greek '
    'characters and 0.03 English function words per line at Higher, against '
    '0 and 1.36 on the composition, which is the same measurement the other '
    'way round.')

NO_SCHEME_EVIDENCE = (
    'the State Examinations Commission published no marking scheme for this '
    'sitting. The corpus holds 27 Ancient Greek question papers and 16 '
    'marking schemes: Higher for every year on disk except 2021, and Ordinary '
    'for 2015, 2019 and 2023 only. With no scheme there is no stated answer '
    'and no printed tariff, so no card can be made from the paper alone.')

TARIFF_ONLY_EVIDENCE = (
    'the scheme prints its tariff table and stops. 2019 and 2023 Ordinary '
    'carry no "ADDITIONAL NOTES" section at all — where every Higher scheme '
    'and 2015 Ordinary print one — so this ask has a price ({note}) and no '
    'stated answer anywhere in the document.')


def build():
    cards, excluded = [], []
    refused = collections.Counter()
    examples = collections.defaultdict(list)

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason,
                         'schemeEvidence': evidence})

    for year, level in sittings(SUBJECT):
        P = AgrPaper(year, level, SUBJECT)
        stamp = f'{year} {level.upper()}'
        S = AgrScheme(year, level, SUBJECT) \
            if has_scheme(year, level, SUBJECT) else None
        entries = S.entries() if S else {}
        asks = P.asks()
        # Where the scheme answers the ROMAN and the paper letters it — 2023
        # and 2024 answer Question 4(viii) "Photo A Theatre: … Photo B Red
        # figure vase … Photo C The Artemision Bronze" without separating (a),
        # (b) and (c) — one card is made on the roman and it covers the
        # letters beneath it, because that is what the card holds.
        rolled = _rolled_up(asks, entries)
        done = set()
        for ask in asks:
            ref = question_ref(year, level, ask.key)
            if S is None:
                refuse('the SEC published no marking scheme for this sitting',
                       ref, f'{stamp}: {NO_SCHEME_EVIDENCE}')
                continue
            if ask.kind == 'translate-into-greek':
                refuse('the scheme prices the English the candidate is given, '
                       'not the Greek that would be the answer', ref,
                       f'{stamp} scheme, Qu. 1A: {COMPOSITION_EVIDENCE}')
                continue
            if ask.kind == 'translate-into-english':
                refuse('the scheme prices the Greek the candidate is given, '
                       'not the English that would be the answer', ref,
                       f'{stamp} scheme, Qu. 2: {UNSEEN_EVIDENCE}')
                continue
            group = (ask.section, ask.q, ask.roman)
            if group in rolled:
                if group in done:
                    continue
                done.add(group)
                _card(P, S, rolled[group], year, level, cards, refuse,
                      covers=[a for a in asks
                              if (a.section, a.q, a.roman) == group])
                continue
            _card(P, S, ask, year, level, cards, refuse)
    return cards, refused, examples, excluded


def _rolled_up(asks, entries):
    """{(section, q, roman): the roman's own ask} where the scheme answers the
    roman and none of the letters beneath it."""
    out = {}
    by_group = collections.defaultdict(list)
    for a in asks:
        if a.letter:
            by_group[(a.section, a.q, a.roman)].append(a)
    for group, kids in by_group.items():
        section, q, roman = group
        parent = entries.get((section, q, None, roman))
        if parent is None or not parent.answer:
            continue
        if any((entries.get(k.key) or _blank()).answer for k in kids):
            continue
        stand_in = kids[0]
        out[group] = _Parent(section, q, roman, parent, kids, stand_in)
    return out


class _blank:
    answer = None
    marks = None
    note = None


class _Parent:
    """The roman as one ask, made of the letters the paper prints under it."""

    __slots__ = ('section', 'q', 'roman', 'letter', 'kind', 'page', 'stem',
                 'text', 'marks', 'inherited', 'letter_ids')

    def __init__(self, section, q, roman, entry, kids, stand_in):
        self.section, self.q, self.roman, self.letter = section, q, roman, None
        self.kind = stand_in.kind
        self.page = stand_in.page
        self.stem = stand_in.stem
        self.text = ' '.join(f'({k.letter}) {k.text}' for k in kids)
        # The ROMAN's tariff is what the PAPER prints on the question it is one
        # of — "Answer any three of the following questions. Each question
        # carries thirty marks" — which is the value its letters inherit.
        # Summed instead, a card that carries three fifteen-mark photograph
        # parts a candidate answers TWO of claimed ninety marks.
        self.marks = (stand_in.marks if stand_in.inherited and stand_in.marks
                      else entry.marks)
        self.inherited = True
        self.letter_ids = [k.letter for k in kids]

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)


def _card(P, S, ask, year, level, cards, refuse, covers=None):
    stamp = f'{year} {level.upper()}'
    ref = question_ref(year, level, ask.key)
    entry = S.entries().get(ask.key)
    if isinstance(ask, _Parent):
        entry = S.entries().get((ask.section, ask.q, None, ask.roman))
        # The citation names every letter the card carries. Cited by the roman
        # alone, "2023 HL Q4(viii)" matched no leaf at all — the census keys
        # the three photograph parts (a), (b) and (c) and a letterless roman
        # deliberately does not reach them — so it reported an orphan card and
        # three open asks for the one card that holds them.
        first = (ask.section, ask.q, ask.letter_ids[0], ask.roman)
        ref = question_ref(year, level, first) + ''.join(
            f', ({L})' for L in ask.letter_ids[1:])
    if entry is None or entry.marks is None and not isinstance(ask, _Parent):
        refuse('the scheme prices no ask at the address the paper prints', ref,
               f'{stamp} paper: "{ask.text[:110]}" — the scheme\'s tariff '
               f'table prices no ask at this address')
        return
    marks = ask.marks if isinstance(ask, _Parent) else entry.marks
    if not entry.answer:
        refuse('the scheme prices this ask and states no answer for it', ref,
               TARIFF_ONLY_EVIDENCE.format(note=entry.note or f'{marks} marks')
               if not S.states_answers else
               f'{stamp} scheme, {key_label(ask.key, SUBJECT)} priced '
               f'{entry.note or marks!r} with no answer printed under it')
        return
    question = ask.text
    floating = FLOATING_MARK.findall(entry.answer or '')
    if floating:
        refuse('the scheme answers this by marking the quantities OVER the '
               'printed line, which a row of text cannot reproduce', ref,
               f'{stamp} scheme, {key_label(ask.key, SUBJECT)}: the answer is '
               f'a scansion diagram — {len(floating)} combining quantity '
               f'mark(s) set over the verse with no letters under them, e.g. '
               f'"{_show(entry.answer)}"')
        return
    if cardlint.NAMES_LETTERS.search(question):
        refuse('the ask points at printed matter the card cannot carry', ref,
               f'{stamp} paper: "{question[:110]}"')
        return
    tariff, rows = _rows(entry, marks, question)
    if not rows:
        refuse('the scheme states no marking point for this ask, only its '
               'price', ref,
               f'{stamp} scheme, {key_label(ask.key, SUBJECT)}: '
               f'"{(entry.answer or "")[:90]}"')
        return
    route_text = _route_text(P, ask)
    card = {
        'id': card_id(year, level, ask.key),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': f'Q{ask.q}',
        'topicId': topic_for(level, ask.q, ask.kind, route_text),
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': tariff,
        'totalMarks': marks,
        'rows': rows,
        'notes': _notes(entry, ask, marks, covers),
    }
    stem = _stem(ask)
    if stem:
        card['stem'] = stem
    source = _source(P, ask, year, level, question)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


# A combining mark with no letter under it. The SEC scans a line of verse by
# setting breves and macrons ABOVE it, in their own printed row, so the text
# layer hands back a run of floating diacritics — "_ _ ̆ _ ̆ _ ̆ _" — that no row
# of text can put back over the words they belong to.
FLOATING_MARK = re.compile('(?<![^\\s_|.-])[\u0300-\u036f]')


def _show(text):
    return ' '.join((text or '').split())[:70]


# Where the printed rubric stops and the Greek passage begins.
GREEK_START = re.compile('[\u0370-\u03ff\u1f00-\u1fff]')


def _stem(ask):
    """The rubric this ask sits under, WITHOUT the passage.

    Question 1 Section B's rubric and its Greek passage are one printed block,
    so the stem carried nine lines of Xenophon on every one of its eight cards
    — beside a sourceMaterial that already opens the page it is printed on.
    The rubric is what comes before the first Greek letter: the instruction and
    the English summary the SEC sets in brackets above the passage.
    """
    text = (ask.stem or '').strip()
    m = GREEK_START.search(text)
    if m:
        text = text[:m.start()].strip()
        # …up to the last complete sentence or bracket, so the stem does not
        # stop mid-word where the passage happened to start.
        cut = max(text.rfind(')'), text.rfind('.'))
        if cut > 20:
            text = text[:cut + 1]
    return text.strip() if len(text.strip()) >= 12 else None


def _route_text(P, ask):
    """Everything the paper printed in this ask's route, for agr_topics."""
    stim = P.stimulus.get((ask.section, ask.q, None, ask.roman)) \
        or P.stimulus.get((ask.section, ask.q, None, 'i')) \
        or P.stimulus.get((ask.section, ask.q, None, None))
    return (stim or {}).get('text', '') + ' ' + (ask.stem or '')


# The printed list an ask offers a choice from: "Write notes on any two of the
# following: March of the 10,000; Tissaphernes; rule of The Thirty; Pericles;
# Epaminondas."
OPTIONS = re.compile(r'(?:any\s+(?:two|three|four)\s+of\s+the\s+following'
                     r'|of\s+the\s+following)\b(?P<list>.+)$', re.I)


def _fold(text):
    # "&" folded to "and", because the paper and the scheme do not agree on
    # it: 2024 lists "Pylos and Sphacteria" among its battles and answers
    # "Pylos & Sphacteria: 425 BC".
    text = (text or '').lower().replace('&', 'and')
    return re.sub(r'[^0-9a-zαβγδεζηθικλμνξοπρστυφχψω]', '',
                  unicodedata.normalize('NFD', text))


def _by_options(question, answer):
    """The answer cut at the options the ASK lists, or [].

    2024 Higher Question 4(ii) names five battles and the scheme answers each
    in turn — "Arginusae: 406 BC … Mantinea: 418 BC … Chaeronea: 338 BC …".
    Cut on the sentence boundary instead, that one card ran to nineteen rows
    and two of them had to be glued back together across a page break, which
    then could not be found in the scheme at all. Cut on the names the paper
    itself prints, it is five rows, one per battle, and each is a contiguous
    run of the scheme's own text.
    """
    m = OPTIONS.search(question or '')
    if not m:
        return []
    # The list itself starts after the LAST colon the ask prints: 2024 sets
    # "Choose any two of the following battles. Identify who fought in them,
    # briefly outline their course, and explain their importance: Arginusae;
    # Mantinea; …" and everything before that colon is instruction.
    listed = m.group('list')
    if ':' in listed:
        listed = listed.rsplit(':', 1)[1]
    names = [n.strip(' .;') for n in re.split(r'[;]', listed)]
    names = [n for n in names if len(n) > 2]
    if len(names) < 2:
        return []
    # The folded answer, and the index of the ORIGINAL character every folded
    # character came from, so a cut found in the folded text maps back onto the
    # scheme's own characters. Built per character rather than by folding the
    # whole string and counting: "&" folds to three characters, so a single
    # count put every cut after the first ampersand three places out and one
    # row opened "s: 333 BC" where "Issus: 333 BC" belongs.
    fa, idx = '', []
    for i, ch in enumerate(answer):
        f = _fold(ch)
        fa += f
        idx += [i] * len(f)
    cuts, pos = [], 0
    for name in names:
        fn = _fold(name)
        # The head of the name: the SEC writes "rule of The Thirty" in the
        # question and "Rule of The Thirty:" in the scheme, and "Pylos and
        # Sphacteria" against "Pylos & Sphacteria".
        head = fn[:max(6, int(len(fn) * 0.6))]
        at = fa.find(head, pos)
        if at < 0:
            return []
        cuts.append(at)
        pos = at + len(head)
    out = []
    for n, at in enumerate(cuts):
        stop = cuts[n + 1] if n + 1 < len(cuts) else len(idx)
        lo = idx[at] if at < len(idx) else len(answer)
        hi = idx[stop] if stop < len(idx) else len(answer)
        part = answer[lo:hi].strip(' ;.')
        if len(part) < 4:
            return []
        out.append(part)
    return out


def _rows(entry, marks, question=''):
    """The scheme's answer, cut into marking rows, and the tariff it carries.

    Three tariff shapes, all read off the scheme's own printed notation:

    * "Impression ex 10" — the examiner marks the whole answer out of ten and
      the scheme prints no split at all, which is `questionTotal`.
    * "8 + 8 + 7 + 7", "(8 + 7) + (8 + 7)", "5 + (5 + 5)" — a printed ladder,
      which is `orderedSplit` and rides on the card VERBATIM.
    * a bare number on a comprehension ask — one answer, one price, `fixed`.
    """
    text = ' '.join((entry.answer or '').split())
    if not text:
        return None, []
    note = (entry.note or '').strip()
    parts = _by_options(question, text) or _segments(text)
    if IMPRESSION.match(note):
        return ({'kind': 'questionTotal'},
                [{'id': f'r-{i + 1}', 'kind': 'point', 'verbatim': p,
                  'marks': None} for i, p in enumerate(parts)])
    if '+' in note and SPLIT.match(note.rstrip('.')):
        return ({'kind': 'orderedSplit', 'notation': note.rstrip('.')},
                [{'id': f'r-{i + 1}', 'kind': 'point', 'verbatim': p,
                  'marks': None} for i, p in enumerate(parts)])
    if len(parts) == 1:
        return ({'kind': 'fixed'},
                [{'id': 'r-1', 'kind': 'point', 'verbatim': parts[0],
                  'marks': marks}])
    # Several stated points under one price the scheme does not divide.
    return ({'kind': 'questionTotal'},
            [{'id': f'r-{i + 1}', 'kind': 'point', 'verbatim': p,
              'marks': None} for i, p in enumerate(parts)])


# Where the SEC breaks one stated answer into the next: a semicolon, a full
# stop that ends a sentence, or the start of a new named note ("Iokaste:").
SEGMENT = re.compile(
    '(?<=[;.])\\s+(?=[A-Z\u0386-\u03ab\u1f00-\u1ffe\u201c"])'
    # …and before a roman the SEC uses to cut ONE answer in two: 2010 answers
    # Question 1 Section B(c) "(i) He had been a slave. (ii) He recognized the
    # language of the people." Left joined, an 8-mark ask split "4 + 4"
    # shipped both halves as one row.
    '|\\s+(?=\\((?:i|ii|iii|iv|v|vi)\\)\\s)')


# An abbreviation that never ends a sentence, so the full stop after it is not
# a break: "passing Mt. Athos", "Xerxes' opinion vs. Demaratos'", "Anabasis,
# Hellenica, Memorabilia, Cyropaedia, etc. Assess significance". Cut there, one
# row ended "passing Mt." and the next opened "Athos;". "BC." is NOT in the
# list — these schemes end a sentence with it constantly ("Arginusae: 406 BC.
# Athenian naval victory").
NEVER_FINAL = re.compile(r'\b(?:Mt|St|Dr|Mr|Mrs|vs|etc|cf|No|e\.g|i\.e)\.$')


def _segments(text):
    parts = []
    for part in SEGMENT.split(text):
        if parts and NEVER_FINAL.search(parts[-1]):
            parts[-1] = f'{parts[-1]} {part}'
            continue
        parts.append(part)
    parts = [p.strip(' ;') for p in parts]
    parts = [p for p in parts if len(p) > 2]
    if not parts:
        return [text]
    while len(parts) > MAX_ROWS:
        # Join the two shortest neighbours rather than dropping anything: the
        # scheme's own words all ship, and the card stays inside its cap.
        i = min(range(len(parts) - 1),
                key=lambda n: len(parts[n]) + len(parts[n + 1]))
        parts[i:i + 2] = [f'{parts[i]} {parts[i + 1]}']
    return parts


def _notes(entry, ask, marks, covers):
    bits = []
    if entry.note:
        bits.append(f'The examiner\'s printed allocation for this ask is '
                    f'{entry.note!r}.')
    else:
        bits.append(f'The examination prints this ask at {marks} marks.')
    bits.append(f'The paper prints it on page {ask.page} of the question '
                f'booklet.')
    if covers and len(covers) > 1:
        letters = ', '.join(f'({c.letter})' for c in covers)
        bits.append(f'The examination letters this ask {letters} and answers '
                    f'all of them together, so one card carries all three.')
    return ' '.join(bits)


def _source(P, ask, year, level, question):
    """The passage or the plates this ask cannot be answered without."""
    plates = PLATE_REF.findall(question)
    if plates:
        # Every plate the ask names, not the first: 2023's Question 4(viii)
        # sets "(a) … Photograph A? (b) … Photograph B? (c) … Photograph C",
        # three separate mentions, and a single search bound page 9 alone
        # while B and C sit on pages 10 and 11.
        letters = sorted({L.upper() for run in plates for L in run if L})
        pages = sorted({p for L, p in P.photo_pages().items() if L in letters})
        if not pages:
            return None
        return {
            'kind': 'source-illustration',
            'label': ', '.join(f'Photograph {L}' for L in letters)[:120],
            'title': 'The photographs printed with this question',
            'pages': pages,
            'attribution': (f'SEC Ancient Greek {year} {LEVEL_TITLE[level]} '
                            'Level examination paper — © State Examinations '
                            'Commission.'),
            'presentationNote': ('The plates exactly as the examination '
                                 'printed them at the back of the booklet.'),
        }
    stim = P.stimulus.get((ask.section, ask.q, None, ask.roman))
    if stim is None and ask.kind == 'comprehension':
        stim = P.stimulus.get((ask.section, ask.q, None, None))
    if stim is None or not stim.get('pages'):
        return None
    return {
        'kind': 'source-text',
        'label': f'QUESTION {ask.q}'
                 + (f' SECTION {ask.section}' if ask.section else ''),
        'title': 'The Greek passage this question is about',
        'pages': stim['pages'],
        'attribution': (f'SEC Ancient Greek {year} {LEVEL_TITLE[level]} Level '
                        'examination paper — © State Examinations Commission.'),
        'presentationNote': ('Read the passage exactly as the examination '
                             'printed it, then answer in English.'),
    }


# ------------------------------------------------------------------ output --
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
