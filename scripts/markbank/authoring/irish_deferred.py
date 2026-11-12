#!/usr/bin/env python3
"""The SEC's deferred Irish sittings, carded in the June shape (Higher and Ordinary, Paper 1 and Paper 2).

The deferred papers (deferredexams/, LC001[AG]LP[12]00IV) set the same paper layout as the same year's June papers, and
each card here has the June card's shape for that layout: one card per listening extract with a criterion (row) per
printed question, one card per composition title, the whole reading questions with every printed part and the
independently priced answers of a part as their own practice cards, one card per literature option with its printed
parts as criteria (and, at Ordinary Level, the printed parts of a prescribed text as their own cards). The marking is
the deferred scheme's (deferredmarkingschemes/, LC001[AG]LP000IV), lifted: every chunk is the scheme's text between
the printed question that opens it and the next, and every tariff is the one the scheme prints beside it.

Identity: "irish-2025-hl-deferred-p1-listening-a-f1" (the June card's key after "deferred-pN-"), cited
"2025 HL Paper 1 Cluastuiscint Cuid A · Fógra a hAon — Deferred sitting", paper "LC001ALP100IV-deferred". Each card
lists the census asks it covers (paper_census.census_irish_deferred) in its manifest's `covers`; the reconcile reads it.

The listening recordings are the SEC's deferred ones (archive/deferredexams/YEAR/LC001ZLP017IV.mp3), checked by HEAD
(12 Nov 2026) and distinct from June's. A sitting whose recording the SEC has not published is carded without audio
and its ledger flag `audio: unavailable` shows the approved note.

usage: irish_deferred.py [--check] [YEAR ...]
"""
from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import sys
import unicodedata
from contextlib import contextmanager
from pathlib import Path

import fitz

import irish_cards as legacy
from irish_lifted import printed_lead_in, scheme_words

ROOT = Path(__file__).resolve().parents[3]
DECK = ROOT / 'components/MarkBank/cards/irish'
SCHEME_TEXT = ROOT / 'examiner-reports/irish/schemes'
REVIEWED_AT = '2026-11-12'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
LEVEL_SHORT = {'higher': 'hl', 'ordinary': 'ol'}
LEVEL_REF = {'higher': 'HL', 'ordinary': 'OL'}
LEVEL_IRISH = {'higher': 'Ardleibhéal', 'ordinary': 'Gnáthleibhéal'}
DEFERRED = ' — Deferred sitting'

# The deferred sittings carded so far, and the SEC's deferred recording for each year (HEAD-checked 12 Nov 2026:
# 2025 = 44,032,055 bytes, 2024 = 44,430,350 bytes; June's are 41,807,615 and 43,417,495).
SITTINGS = {2025: ('higher', 'ordinary',), 2024: ('higher', 'ordinary',), 2023: ('higher', 'ordinary',), 2022: ('ordinary',)}
AUDIO = {2025: 'available', 2024: 'available', 2023: 'available', 2022: 'available'}

# Every deferred paper and scheme, pinned: a changed PDF must be read again.
SHA = {  # (year, level, paper; 0 = the scheme)
    (2025, 'higher', 1): '812104267ddf46cc880dd40b82477b05fc779f39c4f1aca255db12687a1b00b6',
    (2025, 'higher', 2): '87ef214cb1f702c801d1d3a90030905cf80f0872ef6095dfd1cf83340361d245',
    (2025, 'higher', 0): 'd93b85c33e21a626dfd6d5ba36cd5d011b89a3a7a7a3f89fa533eaca48096a39',
    (2025, 'ordinary', 1): '74b071faeabdf5195ba9b691757a54696912b35bd99ca33abdc4b41be3d90a4c',
    (2025, 'ordinary', 2): 'acf484dcca09373ac50e32f1de6ee62cb8542c27e69b68af5445d570f872e18a',
    (2025, 'ordinary', 0): '8ea9aedc8eff748e496563cbcc077d6cca36313fb25681b8838ab18c7793ba47',
    (2024, 'higher', 1): 'cae4c500c2514f4295130621f86ecbe94e43ea6ddcc2f962a3b770915baf56ef',
    (2024, 'higher', 2): 'd540eb0b3d8888e2728b636890cc3c58e096915a7a60ef033463115bfcde1178',
    (2024, 'higher', 0): '4aadfba5f3a47070897e368fabb7f50d7c285599b954964e00b864b236956be6',
    (2024, 'ordinary', 1): '133f1d50fd02283ba27ee5ddc9ff372532e7fd4c86edcce449810fe324230166',
    (2024, 'ordinary', 2): '3e61d99598264985fc8ebd522f945c2a39241af40c6e42f3dd1c82d30399dd7f',
    (2024, 'ordinary', 0): '19c28ffdf07f6f94164ff7b68fc8338c23564d4a244488fd4512cf71e1260ec1',
    (2023, 'higher', 1): 'e646969e24dac9a2dc03d710db498bf396a8ec3f24a2f4d28cda05748ba5f11a',
    (2023, 'higher', 2): 'a3060f6aa3bf091c5a721359f029ab1b2544908d1ce1c6aa059a85f07e8c030f',
    (2023, 'higher', 0): 'a72402672cbba38be725e75b0adb10914631ee4adfac891a8eb52fc34b829d90',
    (2023, 'ordinary', 1): 'a5c5c33f0bc335f3cd63e09e4906699beedefe851365d9744d20adc3f72fc18b',
    (2023, 'ordinary', 2): '97e0e1718e2c45575762be5e50643ca46b2a332064e2cd970d4435ba8a11ced9',
    (2023, 'ordinary', 0): 'b6d96bbcff2645e2a50491c8d3ce400f95d712eeb8a99b6fd2f94fa8cf6ee9e1',
    (2022, 'higher', 1): '78c17f6b8dad61886f860bece1cbc55b6f7e3834252e98da114c4fa0c057e29b',
    (2022, 'higher', 2): 'dab4369b62a8ec67f803fe12774e8fe81b7ca8e896aeca6b153c60e6b2ada7f8',
    (2022, 'higher', 0): '56a1638dea35544a15e55a61616138322dd79dcb7103533a6d94837797afa993',
    (2022, 'ordinary', 1): 'd82ab8cd491bc4cbc8d2d06c3a5f6aca260ca3d9af873ecbdcd43512e917e413',
    (2022, 'ordinary', 2): 'cdd6a5507820da8e5971b1dcd663536d44b69d2218814db2520b8ac2fee2b4ad',
    (2022, 'ordinary', 0): '476588290f702b51452a0625f453ad41f93a7a8fee60fa901e32ac4327588bfe',
}


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def code(level):
    return 'A' if level == 'higher' else 'G'


def paper_file(year, level, paper):
    return ROOT / f'paper-trail-corpus/deferredexams/{year}/LC001{code(level)}LP{paper}00IV.pdf'


def scheme_file(year, level):
    return ROOT / f'paper-trail-corpus/deferredmarkingschemes/{year}/LC001{code(level)}LP000IV.pdf'


def fileid(year, level, paper):
    return f'LC001{code(level)}LP{paper}00IV-deferred'


def scheme_fileid(level):
    return f'LC001{code(level)}LP000IV-deferred'


def audio(year, label):
    url = f'https://www.examinations.ie/archive/deferredexams/{year}/LC001ZLP017IV.mp3'
    return dict(kind='source-audio', label=label, title=f'Triail Chluastuisceana {year} (Scrúdú Iarchurtha)',
                playbackUrl=url, secFileid='LC001ZLP017IV.mp3', canonicalUrl=url, attribution=ATTRIBUTION,
                presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')


def source(year, level, paper, ref, pages, title=None):
    return dict(kind='source-text', label=ref,
                title=title or f'Gaeilge {LEVEL_IRISH[level]} {year} (Scrúdú Iarchurtha) · Páipéar {paper} · {ref}',
                pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def criterion(id, label, marks, guidance, kind='exact', permitted=None, deduction=False):
    return dict(id=id, label=label, kind='deduction' if deduction else 'award', maxMarks=marks,
                permittedMarks=list(permitted) if permitted is not None else list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


ACCENTS = {'a': '[aá]', 'e': '[eé]', 'i': '[ií]', 'o': '[oó]', 'u': '[uú]', 'á': '[aá]', 'é': '[eé]', 'í': '[ií]', 'ó': '[oó]', 'ú': '[uú]'}


def words_pattern(text, count=None, skip=0):
    """A regex for the text's words in order, whatever lies between them (hyphens, quotes, line breaks), with or
    without a síneadh fada (the scheme and the paper do not always agree on one)."""
    words = [w for w in re.findall(r'\w+', text.replace('‐', '-'))][skip:]
    if count:
        words = words[:count]
    return r'\W*'.join(''.join(ACCENTS.get(ch.lower(), re.escape(ch)) for ch in w) for w in words)


def find_prompt(text, prompt, start, stop, tries=((6, 0), (4, 0), (5, 1), (3, 0), (4, 3))):
    """Where the scheme restates a printed prompt, at or after `start` and before `stop`: its first six words, else
    four, else its words from the second on, else from the fourth (a slip in one word of the restatement: "Cé a chur
    amach" for the paper's "Cé a chuir amach")."""
    for count, skip in tries:
        m = re.compile(words_pattern(prompt, count, skip), re.I).search(text, start)
        if m and m.start() < stop:
            if skip:
                # Back up over the skipped words.
                back = re.search(r'(?:\S+\s*){%d}$' % skip, text[max(0, m.start() - 24 * skip):m.start()])
                return m.start() - (len(back.group(0)) if back else 0), m.end()
            return m.start(), m.end()
    return None


class Marked:
    """A document's pages joined with page markers, so a slice knows the PDF pages it spans."""

    def __init__(self, doc, first=1, last=None):
        last = last or len(doc)
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))

    def find(self, pattern, start=0, flags=0):
        m = re.compile(pattern, flags).search(self.text, start)
        return m

    def index(self, needle, start=0):
        return self.text.index(needle, start)

    def page_at(self, offset):
        return int(re.findall(r'⟦(\d+)⟧', self.text[:offset + 1])[-1])

    def chunk(self, a, b):
        """The text between offsets a and b, without page markers, and the pages it prints on."""
        raw = self.text[a:b]
        pages = {self.page_at(a)}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


class Sitting:
    """One deferred sitting: its two papers and its scheme, read once."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.ll = LEVEL_SHORT[level]
        self.paths = {1: paper_file(year, level, 1), 2: paper_file(year, level, 2), 0: scheme_file(year, level)}
        for key, path in self.paths.items():
            assert path.exists(), f'{path} is missing: link the deferred corpus from the main checkout'
            pinned = SHA.get((year, level, key))
            if pinned:
                assert hashlib.sha256(path.read_bytes()).hexdigest() == pinned, f'{path.name} changed: read it again'
        self.docs = {key: fitz.open(path) for key, path in self.paths.items()}
        self.texts = {key: [clean(page.get_text()) for page in doc] for key, doc in self.docs.items()}
        self.pages = {key: legacy.page_texts(str(path)) for key, path in self.paths.items()}
        self.scheme = Marked(self.docs[0])

    def sha(self):
        return {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in self.paths.items()}

    def card_id(self, paper, key):
        return f'irish-{self.year}-{self.ll}-deferred-p{paper}-{key}'

    def ref(self, paper, rest):
        return f'{self.year} {LEVEL_REF[self.level]} Paper {paper} {rest}{DEFERRED}'

    def paper_pages_with(self, paper, text):
        """The paper pages that print the text (compared without punctuation)."""
        want = comparable(text)
        return [i for i, page in enumerate(self.texts[paper], 1) if want in comparable(page)]

    def scheme_pages_with(self, text):
        want = comparable(text)
        return [i for i, page in enumerate(self.texts[0], 1) if want in comparable(page)]


@contextmanager
def legacy_sources(sitting):
    """The legacy builders read a scheme by year and level; point them at this deferred sitting's files.

    Only this process sees the change, and only inside the block: irish_cards.py itself is untouched."""
    saved = (legacy.paper_path, legacy.scheme_path, legacy.literature_scheme, legacy.additional_poetry_criteria, legacy.composition_scheme,
             legacy.lifted_gaeilge)
    legacy.paper_path = lambda year, level, paper: str(paper_file(year, level, paper))
    legacy.scheme_path = lambda year, level: str(scheme_file(year, level))

    def tolerant(prompt, scheme_pages):
        # The legacy trace finds an option's scheme page by its prompt; a deferred scheme that prints one band table
        # for a whole section (optional prose) has no prompt to find. The review below replaces this guidance.
        try:
            return saved[2](prompt, scheme_pages)
        except AssertionError:
            return 1, 0, []
    legacy.literature_scheme = tolerant
    # 4F's reviewed June scheme pages are June's; the review below reads the deferred scheme's 4F instead.
    legacy.additional_poetry_criteria = lambda year, scheme_pages: (
        1, [1], [legacy.criterion('eolas', 'Eolas', 35, [], guidance_kind='indicative')])

    def composition_scheme(year, level, scheme_pages):
        # The legacy reader expects June's composition pages; the review below lifts the deferred scheme's own.
        try:
            return saved[4](year, level, scheme_pages)
        except (AssertionError, ValueError, StopIteration):
            return 1, [legacy.criterion('placeholder', 'Placeholder', 100 if level == 'higher' else 50, [], guidance_kind='quality')]
    legacy.composition_scheme = composition_scheme
    # The legacy lift reads a row's mark after "\) " only; 2022's Higher scheme prints "deilbhíocht). 2".
    legacy.lifted_gaeilge = gaeilge_found
    try:
        yield
    finally:
        (legacy.paper_path, legacy.scheme_path, legacy.literature_scheme, legacy.additional_poetry_criteria,
         legacy.composition_scheme, legacy.lifted_gaeilge) = saved


# ---------------------------------------------------------------------------------------------------------- Paper 1

SEGMENTS = {
    'higher': [
        ('a-f1', 'L-A-F1', 'A', 'Fógra a hAon', r'FÓGRA A hAON', 'irish-1-0'),
        ('a-f2', 'L-A-F2', 'A', 'Fógra a Dó', r'FÓGRA A DÓ', 'irish-1-0'),
        ('b-c1-first', 'L-B-C1-M1', 'B', 'Comhrá a hAon · An Chéad Mhír', r'COMHRÁ A hAON', 'irish-1-1'),
        ('b-c1-second', 'L-B-C1-M2', 'B', 'Comhrá a hAon · An Dara Mír', r'An Dara Mír', 'irish-1-1'),
        ('b-c2-first', 'L-B-C2-M1', 'B', 'Comhrá a Dó · An Chéad Mhír', r'COMHRÁ A DÓ', 'irish-1-1'),
        ('b-c2-second', 'L-B-C2-M2', 'B', 'Comhrá a Dó · An Dara Mír', r'An Dara Mír', 'irish-1-1'),
        ('c-p1', 'L-C-P1', 'C', 'Píosa a hAon', r'PÍOSA A hAON', 'irish-1-2'),
        ('c-p2', 'L-C-P2', 'C', 'Píosa a Dó', r'PÍOSA A DÓ', 'irish-1-2'),
    ],
    'ordinary': [
        ('a-f1', 'L-A-F1', 'A', 'Fógra a hAon', r'FÓGRA A hAON', 'irish-1-0'),
        ('a-f2', 'L-A-F2', 'A', 'Fógra a Dó', r'FÓGRA A DÓ', 'irish-1-0'),
        ('b-c1', 'L-B-C1', 'B', 'Comhrá a hAon', r'COMHRÁ A hAON', 'irish-1-1'),
        ('b-c2', 'L-B-C2', 'B', 'Comhrá a Dó', r'COMHRÁ A DÓ', 'irish-1-1'),
        ('c-p1', 'L-C-P1', 'C', 'Píosa a hAon', r'PÍOSA A hAON', 'irish-1-2'),
        ('c-p2', 'L-C-P2', 'C', 'Píosa a Dó', r'PÍOSA A DÓ', 'irish-1-2'),
    ],
}
# A segment's printed heading in the scheme ends the chunk before it: "FÓGRA A DÓ (8 marc)", "CUID B (28 marc)",
# "An Chéad Mhír", the listening total panel ("Eolas (60) = Gaeilge (0-6) = Iom. (60) =").
HEADING = re.compile(r'\s*(?:(?:CUID|Cuid) [ABC] \(\d+ m?h?arc\)|(?:FÓGRA|COMHRÁ|PÍOSA) A (?:hAON|DÓ) \(\d+ m?h?arc\)'
                     r'|An (?:Chéad Mhír|Dara Mír)|Eolas \(60\) = Gaeilge \(0 ?- ?\d\) = Iom\. \(60\) =)\s*$')
SYMBOLS = re.compile(r'\s*(?:Na )?Siombailí Anótála[^⟦]*')


def listening_questions(sitting, card):
    """The card's printed questions in order: (number, letter or '', prompt, the Mír heading it is printed under)."""
    # The page's furniture after the last question ("Cuid I An Chluastuiscint 60 marc", the running head, the
    # answer-line labels "(i) (ii)") is not a prompt.
    text = re.split(r'\s(?:Cuid I\b|Scrúdú na hArdteist|Gaeilge, Páipéar|\(i\)\s*\(ii\))', card['questionText'])[0]
    out = []
    pieces = re.split(r'\s*(An Chéad Mhír|An Dara Mír)\s*', ' ' + text)
    heading = ''
    for piece in pieces:
        if piece in ('An Chéad Mhír', 'An Dara Mír'):
            heading = piece
            continue
        # "1. (a) Cá bhfuil …? (b) Cén t-am …? 2. (a) …": numbers, then the letters under each.
        for m in re.finditer(r'(?:^|\s)(\d)\.\s+(.*?)(?=\s\d\.\s|$)', piece.strip()):
            number, body = m.group(1), m.group(2)
            letters = list(re.finditer(r'(?:^|\s)\(([a-d])\)\s+', body))
            if not letters:
                out.append((number, '', clean(body), heading))
                continue
            assert letters[0].start() == 0, (card['id'], body[:60])
            for i, lm in enumerate(letters):
                end = letters[i + 1].start() if i + 1 < len(letters) else len(body)
                out.append((number, lm.group(1), clean(body[lm.end():end]), heading))
    return out


def printed_listening(questions):
    """The question as the paper prints it: "An Chéad Mhír 1. (a) … (b) … 2. …"."""
    out, heading = [], ''
    for number, letter, prompt, mir in questions:
        if mir != heading:
            out.append(mir)
            heading = mir
        out.append((f'{number}. ' if not letter or letter == 'a' else '') + (f'({letter}) ' if letter else '') + prompt)
    return ' '.join(out)


def listening(sitting, base):
    """The legacy listening cards, each printed question its own criterion at its printed tariff, lifted from the
    deferred scheme (the June 2024/2025 reviews' method: irish_higher_2025_p1.py, irish_ordinary_2025_p1.py)."""
    s, level = sitting.scheme, sitting.level
    higher = level == 'higher'
    unit = 2 if higher else 3
    by_key = {c['id'].split('-p1-', 1)[1]: c for c in base if c['id'].split('-p1-', 1)[1].startswith('listening-')}
    note = s.find(r'Bainfear ó 0 go \d ar chaighdeán na Gaeilge\.')
    assert note, 'listening: the scheme prints no language deduction'
    language_pages = [p for p in range(1, len(sitting.texts[0]) + 1) if 'Bainfear ó 0 go' in sitting.texts[0][p - 1]]
    deduction = re.search(r'Bainfear ó 0 go (\d)', note.group(0)).group(1)
    language = (f'Scheme PDF {" and ".join(map(str, language_pages))}: “{note.group(0)}” This 0–{deduction} deduction applies '
                'once to the whole listening section (Tuiscint 60 − Cumas Gaeilge 0–' + deduction + '), never inside a single '
                + ('card.' if higher else 'question.'))
    # The answers start at the first segment heading after the transcript (which prints the same headings in prose).
    answers = s.find(r'(?:CUID|Cuid) A \(\d+ m?h?arc\)\s*FÓGRA A hAON')
    assert answers, 'listening: answer section not found'
    cursor = answers.start()
    # The answers end at the language note, the section's mark panel or the composition, whichever is first.
    stop_m = min((m for m in (s.find(r'Bainfear ó 0 go \d ar chaighdeán na Gaeilge\.', cursor),
                              s.find(r'Eolas \(60\) =', cursor), s.find(r'Cuid II\b|An Mharcáil:', cursor)) if m),
                 key=lambda m: m.start())
    plan = []
    for suffix, atlas, part, title, heading, topic in SEGMENTS[level]:
        card = by_key[f'listening-{suffix}']
        questions = listening_questions(sitting, card)
        assert questions, card['id']
        # The question as the paper prints it: "1. (a) … (b) … 2. …".
        card['questionText'] = printed_listening(questions)
        for number, letter, prompt, _ in questions:
            # The scheme restates the question: find its first words after the previous question.
            found = find_prompt(s.text, prompt, cursor, stop_m.start())
            assert found, (card['id'], number, letter, prompt[:60])
            # Open the chunk at the printed number or letter before the words ("1. (a) Cá bhfuil …", "(b) Cén …").
            head = re.search(r'(?:\d\.\s*)?(?:\([a-d]\)\s*)?(?:⟦\d+⟧\s*)?$', s.text[max(0, found[0] - 24):found[0]])
            start = found[0] - (len(head.group(0)) if head else 0)
            plan.append((suffix, number, letter, prompt, start))
            cursor = found[1]
    stamped = []
    for index, (suffix, number, letter, prompt, start) in enumerate(plan):
        end = plan[index + 1][4] if index + 1 < len(plan) else stop_m.start()
        raw = s.text[start:end]
        raw = SYMBOLS.sub(' ', raw)
        while True:
            trimmed = HEADING.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                break
            raw = trimmed
        chunk, pages = s.chunk(start, start + len(raw))
        chunk = clean(re.sub(r'⟦\d+⟧', ' ', raw))
        tariff = re.search(r'(\d) mh?arc(?: \+ (\d) mh?arc)?', chunk)
        assert tariff and int(tariff.group(1)) == unit, (suffix, number, letter, chunk[:120])
        marks = unit + (int(tariff.group(2)) if tariff.group(2) else 0)
        plan[index] = (suffix, number, letter, prompt, chunk, pages, marks)
    for suffix, atlas, part, title, heading, topic in SEGMENTS[level]:
        card = by_key[f'listening-{suffix}']
        rows = [q for q in plan if q[0] == suffix]
        assert sum(q[6] for q in rows) == card['totalMarks'], (card['id'], [q[6] for q in rows], card['totalMarks'])
        criteria = []
        mir = 0
        for _, number, letter, prompt, chunk, pages, marks in rows:
            if higher:
                cid, label = f'q{number}{letter}', f'Ceist {number}' + (f'({letter})' if letter else '')
                permitted = range(marks + 1) if '= 1 mharc' in chunk else range(0, marks + 1, 2)
            else:
                if suffix.startswith('b-'):
                    mir += number == '1'
                    cid = f'm{mir}-q{number}'
                    label = ('An Chéad Mhír' if mir == 1 else 'An Dara Mír') + f' · Ceist {number}'
                else:
                    cid, label = f'q{number}{letter}', f'Ceist {number}' + (f'({letter})' if letter else '')
                values = {0, 3} | {int(v) for v in re.findall(r'= (\d) mharc', chunk)}
                permitted = sorted(values if marks == 3 else {a + b for a in values for b in values if a + b <= marks})
            criteria.append(criterion(cid, label, marks, [chunk], 'exact', permitted=permitted))
        pages = sorted({p for q in rows for p in q[5]})
        paper_page = card['paperPage']
        ref = f'Cluastuiscint Cuid {part} · {title}'
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=[paper_page],
                    schemeFileid=scheme_fileid(level), schemePage=pages[0], schemePages=pages,
                    sourceMaterial=source(sitting.year, level, 1, ref, [paper_page]), criteria=criteria,
                    markingGuideNote=f'The listed responses and tariffs come from the {sitting.year} SEC deferred marking scheme; '
                                     'equivalent wording with the same meaning is accepted. '
                                     + ('Each printed question is marked at its own published tariff (2, or 2 + 2 for two points). '
                                        if higher else 'Each printed question is marked at its own published tariff (3, or 3 + 3 for two points). ')
                                     + language)
        stamped.append(card['id'])
    return stamped


COMPOSITION_FORMS = {
    'higher': {'A': 'AISTE nó ALT NUACHTÁIN/IRISE', 'B': 'SCÉAL', 'C': 'DÍOSPÓIREACHT/ÓRÁID'},
    'ordinary': {'A': 'Giota Leanúnach/Blag', 'B': 'Scéal', 'C': 'Litir/Ríomhphost', 'D': 'Comhrá'},
}
# The June reviews' notes (irish_higher_2025_p1.py, irish_ordinary_2025_p1.py): choice is not a route.
COMPOSITION_REASONS = {
    'A': 'AISTE nó ALT NUACHTÁIN/IRISE is a choice of writing form inside one response, marked by the same Stíl/Ábhar/Gaeilge scheme; it is not a separate route.',
    'B': 'Each printed title is a separate route; the story itself is open.',
    'C': '“ar son … nó ina aghaidh” is the speaker’s stance inside one speech; both stances are marked identically.'}


def page_text(sitting, key, page):
    """A page's text on one line, without the page number the SEC prints at its top or bottom."""
    return re.sub(r'\s+\d+$', '', re.sub(r'^\d+\s', '', sitting.texts[key][page - 1])).strip()


def scheme_page(sitting, needle, after=0):
    found = [p for p in sitting.scheme_pages_with(needle) if p > after]
    assert found, f'{sitting.year} {sitting.level}: the scheme prints no “{needle}”'
    return found[0]


def printed_lines(text):
    """A paper's run of sentences, one printed instruction to a line (“Caillfear …” continues its sentence)."""
    sentences = [x.strip() for x in re.split(r'(?<=[.?!])\s+', clean(text)) if x.strip()]
    lines = []
    for sentence in sentences:
        if lines and sentence.startswith('Caillfear'):
            lines[-1] += ' ' + sentence
        else:
            lines.append(sentence)
    return lines


def option_lines(title):
    """A long option as the paper sets it: a statement after its colon, and the closing instruction, on lines of their own."""
    title = re.sub(r':\s+', ':\n', title)
    return re.sub(r'\s+(Scríobh an (?:píosa cainte|litir|comhrá))', r'\n\1', title)


def composition(sitting, base):
    """Each composition title one card with the deferred scheme's composition marking, lifted."""
    level, year = sitting.level, sitting.year
    higher = level == 'higher'
    forms = COMPOSITION_FORMS[level]
    page7 = sitting.texts[1][6]
    for form in forms.values():
        assert comparable(form) in comparable(page7), (year, level, form)
    stamped = []
    if higher:
        p = scheme_page(sitting, 'An Mharcáil:')
        marking = page_text(sitting, 0, p).split('An Mharcáil:', 1)[1].strip().removesuffix('Cuid II An Cheapadóireacht 100 marc').strip()
        if 'Don Scrúdaitheoir' in marking:
            # 2022 prints the listening totals panel after the marking, and its assessment steps on the next page.
            marking = marking.split('Don Scrúdaitheoir', 1)[0].strip()
            following = page_text(sitting, 0, p + 1)
            if following.startswith('An Measúnú'):
                marking += ' ' + following.split(' Stíl (5) =', 1)[0].strip()
        p_stil = scheme_page(sitting, 'Stíl chuí scríbhneoireachta (5 mharc)', p)
        text = page_text(sitting, 0, p_stil)
        if 'Ionramháil Ábhair (15 mharc)' in text:
            stil = text.split('Stíl chuí scríbhneoireachta (5 mharc)', 1)[1].split('Ionramháil Ábhair (15 mharc)', 1)[0].strip()
            abhar = text.split('Ionramháil Ábhair (15 mharc)', 1)[1].strip()
        else:
            # 2022 prints Stíl above the annotation key and the deficient-attempt table, and finishes it (and prints
            # Ionramháil Ábhair) on the next page.
            following = page_text(sitting, 0, p_stil + 1)
            stil = (text.split('Stíl chuí scríbhneoireachta (5 mharc)', 1)[1].lstrip(':').split('Siombailí Anótála', 1)[0].strip() + ' '
                    + following.split('Ionramháil Ábhair (15 mharc)', 1)[0].strip())
            abhar = following.split('Ionramháil Ábhair (15 mharc)', 1)[1].lstrip(':').strip()
        p_gaeilge = scheme_page(sitting, 'Cumas Gaeilge (80 marc)', p)
        text = page_text(sitting, 0, p_gaeilge)
        gaeilge = [text[text.index('Cumas Gaeilge (80 marc)'):].strip(), page_text(sitting, 0, p_gaeilge + 1)]
        p_graded = scheme_page(sitting, 'An Grádú Marcála', p)
        text = page_text(sitting, 0, p_graded)
        graded = text[text.index('An Grádú Marcála'):].strip()
        assert stil.startswith('Stíl (5 mharc) = 5 mharc'), stil[:60]
        assert all(x in abhar for x in ['13, 14, 15', '11, 12', '9, 10', '6, 7, 8', '3, 4, 5', '0, 1, 2']), abhar[-200:]
        assert all(x in gaeilge[1] for x in ['76-80', '64-67', '52-55', '40-43', '28-31']), gaeilge[1][:200]
        assert all(x in graded for x in ['S1', 'S2', 'S3', 'S4']) or all(x in graded for x in ['(68)', '(56)', '(44)']), graded[:200]
        s4 = re.search(r'Easnamhach i gcás (.+?)\s+Stíl \((\d+)\)\s+Ábhar \((\d+)\)\s+Gaeilge \((\d+)\)', graded)
        assert s4, graded[-200:]
        s4_titles = set(re.findall(r'([ABC]) ?\(([a-e])\)', s4.group(1)))
        smm = [q for q in sitting.scheme_pages_with('Scéim Mharcála Mhodhnaithe') if q > p_graded]
        scheme_pages = list(range(p, p_graded + 1))
        page = 7
        # The running head is "Gaeilge, Páipéar 1 – Ardleibhéal" (2023 on) or "Gaeilge – Ardleibhéal" (2022).
        head_text = clean(re.split(r'Gaeilge(?:, Páipéar 1)? – Ardleibhéal', page7, maxsplit=1)[1].split('Scríobh AISTE', 1)[0])
        head = '\n'.join(printed_lines(head_text))
        assert head.startswith('Freagair do rogha CEANN AMHÁIN'), head[:80]
        for card in base:
            m = re.match(r'.*-p1-composition-([a-d])-([a-e]|i{1,3})$', card['id'])
            if not m:
                continue
            group, letter = m.group(1).upper(), m.group(2)
            instruction, title = card['questionText'].split(f' ({letter}) ', 1)
            s4_line = ([f'S4 applies to this title: “Easnamhach i gcás {s4.group(1)}” — Stíl ({s4.group(2)}) Ábhar ({s4.group(3)}) Gaeilge ({s4.group(4)}).']
                       if (group, letter) in s4_titles else [])
            smm_line = ([f'Scéim Mharcála Mhodhnaithe (scheme PDF {smm[0]}): for eligible candidates spelling and the listed grammar features '
                         'are not counted in the 80-mark Cumas Gaeilge award.'] if smm else [])
            card.update(atlasQuestionId=f'W-{group}-{letter}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[page], paperPage=page,
                        schemeFileid=scheme_fileid(level), schemePage=scheme_pages[0], schemePages=scheme_pages,
                        questionText=head + f'\n\n{group} · {forms[group]} (100 marc)\n{instruction}\n\n({letter}) {option_lines(title)}'
                                     f'\n\nAn rogha don chárta seo: {group}({letter}).',
                        sourceMaterial=source(year, level, 1, f'Ceapadóireacht {group}({letter})', [page]),
                        taskRequirements=['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                          'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Timpeall 500–600 focal.'],
                        criteria=[criterion('stil', 'Stíl chuí scríbhneoireachta', 5, [stil, graded], 'quality'),
                                  criterion('abhar', 'Ionramháil Ábhair', 15, [abhar, marking], 'quality'),
                                  criterion('gaeilge', 'Cumas Gaeilge', 80, gaeilge + smm_line + s4_line, 'quality')],
                        markingGuideNote='Whole 100-mark composition: Stíl 5, Ionramháil Ábhair 15, Cumas Gaeilge 80, assessed as one unit. '
                                         'Deficient-length attempts use the printed S1–S4 grades. ' + COMPOSITION_REASONS[group])
            assert card['totalMarks'] == 100
            stamped.append(card['id'])
    else:
        p = scheme_page(sitting, 'Freagair do rogha dhá cheann de A, B, C, D')
        marking = page_text(sitting, 0, p)
        marking = re.sub(r'\s*Cuid II An Cheapadóireacht 100 marc$', '', marking[marking.index('Freagair do rogha dhá cheann'):].strip())
        assert 'Tasc' in marking and 'An tÁbhar (8 marc)' in marking and 'An Cumas Gaeilge (40 marc)' in marking, marking[:300]
        tables = [q for q in range(p + 1, min(p + 4, len(sitting.texts[0])) + 1)
                  if re.search(r'Réimse Catagóir|Siombailí Anótála', sitting.texts[0][q - 1])]
        extra = [page_text(sitting, 0, q) for q in tables]
        table40 = next(t for t in extra if '95%' in t)
        table_short = next(t for t in extra if 'M F1 F2 F3' in t)
        assert '38 34 29 19 10' in table_short, table_short[:200]
        columns = re.search(r'Réimse Catagóir 40 (\d+) (\d+) (\d+) (\d+) Siombailí', table_short)
        assert columns, table_short[:120]
        smm = [q for q in sitting.scheme_pages_with('Scéim Mharcála Mhodhnaithe') if q > p]
        smm_line = ([f'Scéim Mharcála Mhodhnaithe (scheme PDF {"–".join(map(str, smm[:2]))}): eligible candidates are assessed on named grammar '
                     'features; spelling is not counted.'] if smm else [])
        scheme_pages = sorted({p, *tables})
        unlabel = lambda piece: re.sub(r'\s*\(i{1,3}\)$', '', piece.strip())
        head_text = clean(sitting.texts[1][5].split('Treoracha', 1)[1])
        head = 'Treoracha: ' + head_text + '\n\nFreagair do rogha dhá cheann de A, B, C, D anseo.'
        assert comparable('Freagair do rogha dhá cheann de A, B, C, D anseo.') in comparable(page7)
        for card in base:
            m = re.match(r'.*-p1-composition-([a-d])-(i{1,3})$', card['id'])
            if not m:
                continue
            group, roman = m.group(1).upper(), m.group(2)
            parts = card['questionText'].split(f'({roman}) ', 1)
            instruction, title = parts[0].strip(), parts[1]
            body = head + f'\n\n{group} · {forms[group]} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {option_lines(title)}'
            card.update(atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[7], paperPage=7,
                        schemeFileid=scheme_fileid(level), schemePage=scheme_pages[0], schemePages=scheme_pages,
                        questionText=body + f'\n\nAn rogha don chárta seo: {group}({roman}).',
                        sourceMaterial=source(year, level, 1, f'Ceapadóireacht {group}({roman})', [7]),
                        taskRequirements=['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                          'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.'],
                        # 2022 numbers the three awards "(i) … (ii) An tÁbhar … (iii) An Cumas Gaeilge": a label is its own award's.
                        criteria=[criterion('tasc', 'An Tasc', 2, [unlabel(marking.split('An tÁbhar (8 marc)')[0])], 'quality', permitted=[0, 2]),
                                  criterion('abhar', 'An tÁbhar', 8, [unlabel(marking.split('An tÁbhar (8 marc)', 1)[1].split('An Cumas Gaeilge (40 marc)')[0])], 'quality'),
                                  criterion('gaeilge', 'An Cumas Gaeilge', 40,
                                            [marking.split('An Cumas Gaeilge (40 marc)', 1)[1].strip(), *extra] + smm_line, 'quality')],
                        markingGuideNote='Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. Short attempts use the published M/F1/F2/F3 columns '
                                         f'({"/".join(columns.groups())}) on scheme PDF {tables[-1]}, so the Cumas Gaeilge award can take any value from 0 to 40. '
                                         'The letter or email (C) and the conversation partner (D) are flexible forms inside one response, not separate routes.')
            assert card['totalMarks'] == 50
            stamped.append(card['id'])
    assert len(stamped) == 9, stamped
    return stamped


# ---------------------------------------------------------------------------------------------------------- Paper 2

READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
READING_PART_OL = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                 'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Retained whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
ORDER_NOTE = 'Order-dependent award: the first correct item earns 2 and the other 1 (0, 2 or 3).'
PART_LABELS = {'a': '(a)', 'b': '(b)', 'bi': '(b)(i)', 'bii': '(b)(ii)'}


def printed_values(chunk, marks):
    return sorted({0, marks} | {int(v) for v in re.findall(r'= (\d+) mh?arc', chunk) if int(v) <= marks})


class Tariff:
    """A part's tariff read from one of 2022's looser layouts, answering .group() as the braced form's match does."""

    def __init__(self, total, first=None, second=None):
        self.groups = (None, str(total), first, second)

    def group(self, n):
        return self.groups[n]


def loose_tariff(chunk):
    """2022's Higher scheme sets a part's tariff in several ways besides "{3 mharc: 2 mharc + 1 mharc}": "(Alt 4) 3 mharc",
    "pointe amháin eolais (2 mharc)", "3 mharc (2 mharc + 1 mharc)", "Dhá shampla (3 mharc) 2 mharc + 1 mharc", "2mharc
    (1 mharc + 1 mharc)", "{1 mharc + 1 mharc}". The first one printed before the sample answers is the part's."""
    head = chunk.split('•', 1)[0]
    m = re.search(r'(\d+) ?mharc(?:[\s:()]*(\d) ?mharc\s*\+\s*(\d) ?mharc)?', head)
    if not m:
        return None
    if m.group(2) is None:
        alone = re.match(r'\s*\+\s*(\d) ?mharc', head[m.end():])
        if alone:
            return Tariff(int(m.group(1)) + int(alone.group(1)), m.group(1), alone.group(1))
    return Tariff(int(m.group(1)), m.group(2), m.group(3))


def reading_parts(question, higher):
    """A whole reading question's printed parts: [(part, prompt as printed)], e.g. ('bi', '(b) (i) Cén fáth …? (Alt 1)')."""
    body = re.sub(r'\s*\((?:7|10|15) m?h?arc\)\s*$', '', re.sub(r'^\d\.\s*', '', question))
    marks = list(re.finditer(r'(?:(?<=\s)|^)\((a|b)\)\s+(?:\((i)\)\s+)?|(?<=\s)\((ii)\)\s+', body))
    out = []
    for index, m in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(body)
        part = (m.group(1) or 'b') + ((m.group(2) or m.group(3) or '') if higher else '')
        out.append((part, body[m.start():end].strip()))
    return out


def relift_labels(sitting, card):
    """The legacy page reader can drop a part label the paper prints (2022's Higher A 1(b) loses its "(ii)"): where it
    has, the question is read again from the paper's own text layer, which keeps the label. No other word may differ."""
    question = card['questionText']
    paper = ' '.join(sitting.texts[2])
    head = re.compile(words_pattern(question, 10), re.I).search(paper)
    assert head, question[:80]
    tail = re.compile(r'\(\d+ m?h?arc\)').search(paper, head.end())
    printed = clean(paper[head.start():tail.end()])
    unlabelled = lambda text: comparable(re.sub(r'\((?:i{1,3}|iv|v)\)', ' ', text))
    if comparable(printed) != comparable(question):
        assert unlabelled(printed) == unlabelled(question), (card['id'], printed[:120])
        card['questionText'] = printed


def reading(sitting, base):
    """Every reading question whole, every printed part as its own card, and each independently priced answer or point
    of a part as its own practice card (the June shape: irish_higher_2026_p2.py, irish_ordinary_2025_p2.py)."""
    s, level, year = sitting.scheme, sitting.level, sitting.year
    higher = level == 'higher'
    whole = {c['id'].split('-p2-', 1)[1]: c for c in base if '-p2-reading-' in c['id']}
    assert len(whole) == (12 if higher else 10), len(whole)
    for card in whole.values():
        relift_labels(sitting, card)
    starts = {letter: s.find(r'LÉAMHTHUISCINT ' + letter + r' \(50 marc\)' if higher else
                             r'(?:LÉAMHTHUISCINT|Léamhthuiscint) ' + letter + r'\b') for letter in 'AB'}
    shared_notes, notes_of = None, {}
    if not higher:
        # Ordinary prints each passage's notes above its Ceist 1 ("Nóta: Má tá dhá phointe/phíosa eolais i gceist …
        # Nóta: Gearrfar pionós i ngeall ar iomarcaíocht."); the passage starts at its notes. A scheme that prints them
        # once, under "Freagair A agus B anseo." (2022), shares them, and B starts at its Ceist 1 restated.
        blocks = list(re.finditer(r'Nóta: Má tá dhá (?:phointe|phíosa) eolais i gceist.*?Nóta: Gearrfar pionós i ngeall ar iomarcaíocht\.', s.text))
        assert blocks, 'reading: the Ordinary notes are not printed'
        first = lambda letter: re.sub(r'^\(a\)\s*', '', reading_parts(whole[f'reading-{letter}-q1']['questionText'], False)[0][1])
        a_at = find_prompt(s.text, first('a'), blocks[0].start(), len(s.text))
        b_at = find_prompt(s.text, first('b'), a_at[1], len(s.text))
        assert a_at and b_at, 'reading: Ordinary Ceist 1 not found'
        before_a = [m for m in blocks if m.end() <= a_at[0]]
        before_b = [m for m in blocks if a_at[1] <= m.start() and m.end() <= b_at[0]]
        assert before_a, 'reading: no notes above A'
        notes_of['A'] = before_a[-1]
        if before_b:
            notes_of['B'] = before_b[-1]
            starts = {'A': before_a[-1].start(), 'B': before_b[-1].start()}
        else:
            shared_notes = notes_of['B'] = before_a[-1]
            label = re.search(r'(?:1\.\s*)?(?:\(a\)\s*)?(?:⟦\d+⟧\s*)?$', s.text[max(0, b_at[0] - 20):b_at[0]])
            starts = {'A': before_a[-1].start(), 'B': b_at[0] - len(label.group(0))}
    else:
        starts = {k: v.start() for k, v in starts.items()}
        assert all(starts.values()), starts
    general = ''
    if higher:
        g = s.find(r'Tá Ceist 1 – 5 ar cómharc')
        end = s.find(r'Siombailí Anótála|Cuir an marc iomlán|Ceist 1 LÉAMHTHUISCINT', g.start())
        general = clean(re.sub(r'⟦\d+⟧', ' ', s.text[g.start():end.start()]))
        lead = s.find(r'Freagair Léamhthuiscint A agus Léamhthuiscint B\.')
        if lead and lead.start() < g.start() and g.start() - lead.end() < 8:
            general = clean(re.sub(r'⟦\d+⟧', ' ', s.text[lead.start():end.start()]))
    # The reading section ends where the literature's notes begin.
    reading_end = s.find(r'Nóta: I gcás na gceisteanna 2|Ceist 2\s*PRÓS|Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)|Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha',
                         starts['B'] + 10)
    assert reading_end, 'reading: end not found'
    cards, stamped = [], []
    lang_read = s.find(r'\[Gaeilge lochtach: 0 ?[-‐] ?5 a bhaint den iomlán a gnóthaíodh\]') if not higher else None
    for letter in 'AB':
        cursor = starts[letter]
        stop = starts['B'] if letter == 'A' else reading_end.start()
        notes = ''
        if not higher:
            notes = clean(re.sub(r'⟦\d+⟧', ' ', notes_of[letter].group(0)))
            notes = re.sub(r'\s*Siombailí Anótála.*$', '', notes)
        plan = []
        for q in range(1, (7 if higher else 6)):
            card = whole[f'reading-{letter.lower()}-q{q}']
            for part, prompt in reading_parts(card['questionText'], higher):
                words = re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
                found = find_prompt(s.text, words, cursor, stop)
                assert found, (letter, q, part, words[:60])
                label = re.search(r'(?:\d\.\s*)?(?:\([ab]\)\s*)?(?:\(i{1,2}\)\s*)?(?:⟦\d+⟧\s*)?$', s.text[max(0, found[0] - 20):found[0]])
                plan.append([q, part, prompt, found[0] - len(label.group(0))])
                cursor = found[1]
        for index, item in enumerate(plan):
            end = plan[index + 1][3] if index + 1 < len(plan) else stop
            chunk, pages = s.chunk(item[3], end)
            if not higher:
                chunk = re.split(r'\s*\[Gaeilge lochtach', chunk)[0]
                # The text layer can store a one-answer part's tariff after its answer ("(Alt 1) • Tugadh … nua 5 mharc"):
                # the scheme prints it beside the question, so it is read there. No word changes.
                late = re.fullmatch(r'(.*?\(Alt \d\))\s+(•[^=]*?)\s+(\d+ mharc)', chunk)
                if late:
                    chunk = f'{late.group(1)} {late.group(3)} {late.group(2)}'
            item += [chunk, pages]
        if not higher:
            # 2022 prints B 3(b)'s "5 mharc" in the margin beside it, but the text layer stores it at the head of the next part
            # ("4. (a) … (Alt 4) 5 mharc 3 mharc + 2 mharc = 5 mharc"). Read on the page: a price whose line lies above the
            # next question's is this part's, and it is read beside this question. No word changes.
            for index, item in enumerate(plan[:-1]):
                following = plan[index + 1]
                if re.search(r'\d ?mharc', item[4]):
                    continue
                stray = re.match(r'(.*?\(Alt \d\))\s+(\d+ mharc)\s+(\d+ mharc \+ \d+ mharc = \d+ ?mharc\b.*)$', following[4])
                assert stray, (letter, item[0], item[1], item[4][:80])
                page = sitting.docs[0][following[5][0] - 1]
                words = page.get_text('words')
                price = [w for w in words if w[4] == 'mharc' and w[0] > 400]
                asked = [w for w in words if w[4] == f'{following[0]}.' and w[0] < 100]
                assert price and asked and min(w[1] for w in price) < asked[0][1], (letter, item[0], item[1], 'the price is not printed above the next question')
                item[4] = re.sub(r'^(.*?\?)\s+', lambda m: f'{m.group(1)} {stray.group(2)} ', item[4], count=1)
                following[4] = f'{stray.group(1)} {stray.group(3)}'
        title = whole[f'reading-{letter.lower()}-q1']['sourceMaterial']['title']
        pages = whole[f'reading-{letter.lower()}-q1']['sourceMaterial']['pages']
        topic = 'irish-3-0' if letter == 'A' else 'irish-3-1'
        src = source(year, level, 2, f'Léamhthuiscint {letter}', pages, title=title)
        by_question = {}
        for q, part, prompt, _, chunk, spages in plan:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            ref = f'Léamhthuiscint {letter} · Ceist {label}'
            slug = f'reading-{letter.lower()}-q{q}-{part}'
            atlas = f'R-{letter}-{q}-{part}'
            extra_topics = None
            if higher:
                tariff = re.search(r'\{(\d+) mharc(?:\s*[:=]\s*(\d) mharc\s*\+\s*(\d) mharc)?\s*\}', chunk) or loose_tariff(chunk)
                marks = 12 if (q == 6 and part == 'b') else int(tariff.group(1)) if tariff else None
                assert marks == (3 if part == 'a' else 2 if part.startswith('b') and q < 6 else 12), (letter, q, part, chunk[:120])
                ordered = bool(tariff and tariff.group(2) == '2' and tariff.group(3) == '1') or bool(
                    re.search(r'An chéad \w+ (?:\w+ )?atá ceart = 2 mharc; an dara', chunk))
                slots = part.startswith('b') and q < 6 and bool(
                    (tariff and tariff.group(2) == '1' and tariff.group(3) == '1')
                    or re.search(r'An chéad \w+ (?:\w+ )?atá ceart = 1 mharc; an dara \w+ (?:\w+ )?atá ceart = 1 mharc', chunk))
                if q == 6 and part == 'a':
                    mode = 'grammar'
                elif q == 6:
                    # An opinion or claim and two supports (the scheme's panel "T (2) = P1 (5) = P2 (5)"), else two points 6 + 6.
                    panel = re.search(r'\bT \(2\) = ([A-Z])1 \(5\) = \1 ?2 \(5\)', chunk)
                    # 2022 asks how the passage affected the reader and prices that "C (2)= 2 mharc", then two points at 5.
                    affect = re.search(r'(Conas a chuaigh an sliocht seo i bhfeidhm ort\?) C \(2\) ?= ?2 mharc', chunk)
                    affect = affect if affect and re.search(r'Pointe eolais 1 = .*?= 5 mharc.*?Pointe eolais 2 = .*?= 5 mharc', chunk) else None
                    mode = ('opinion' if (panel or affect or re.search(r'Tuairim \(T\) = 2 mharc', chunk)) else
                            'points' if re.search(r'6 mharc \+ 6 mharc', chunk) else 'whole')
                else:
                    mode = 'ordered' if ordered else 'slots' if slots else None
                if mode == 'points':
                    unit = 'Tréith' if 'Tréith 1' in chunk else 'Léargas' if 'Léargas 1' in chunk else 'Pointe eolais'
                    crits = [criterion(f'point-{n}', f'{unit} {n}', 6, [chunk, general]) for n in (1, 2)]
                elif mode == 'opinion':
                    short = panel.group(1) if panel else 'P'
                    unit = {'F': 'Fáth', 'S': 'Sampla', 'P': 'Pointe eolais'}[short]
                    claim = (f'{affect.group(1)} (C)' if affect else
                             'Tuairim (T)' if 'Tuairim (T)' in chunk else 'Tábhacht (T)' if 'Tábhacht a lua' in chunk else 'Tuairim (T)')
                    crits = [criterion('opinion', claim, 2, [chunk, general]),
                             criterion('reason-1' if short == 'F' else 'point-1', f'{unit} 1 ({short}1)', 5, [chunk]),
                             criterion('reason-2' if short == 'F' else 'point-2', f'{unit} 2 ({short}2)', 5, [chunk])]
                elif mode == 'whole':
                    crits = [criterion('b', 'Freagra', 12, [chunk, general])]
                elif mode in ('grammar', 'ordered'):
                    crits = [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general, ORDER_NOTE], permitted=[0, 2, 3])]
                else:
                    # The braced split prices each answer ("{2 mharc: 1 mharc + 1 mharc}", 2023): a single answer earns its share.
                    split = {int(tariff.group(n)) for n in (2, 3) if tariff and tariff.group(n)} if mode == 'slots' else set()
                    if isinstance(tariff, Tariff):
                        # 2022 can print a one-point answer's split after its sample ("Pointe amháin 2 mharc … (1 mharc + 1 mharc)").
                        split |= {int(v) for m in re.finditer(r'\((\d) ?mharc \+ (\d) ?mharc\)', chunk) for v in m.groups() if int(v) < marks}
                        # … and a reduced award for an incomplete answer ("Gan ‘le móramh’ (3-1) =2").
                        split |= {int(m.group(1)) for m in re.finditer(r'\(\d ?- ?\d\) ?= ?(\d)\b', chunk) if int(m.group(1)) < marks}
                    crits = [criterion(part, 'Freagra', marks, [chunk, general], permitted=sorted(set(printed_values(chunk, marks)) | split))]
                here = 'irish-3-3' if mode == 'grammar' else topic
                extra_topics = [topic] if mode == 'grammar' else None
                requirements = READING_PART
                note = PART_NOTE
            else:
                assert re.search(r'5 ?mharc', chunk), (letter, q, part, chunk[:80])  # 2023 prints "= 5mharc"
                two = '3 mharc + 2 mharc' in chunk
                permitted = [0, 3, 5] if (two or re.search(r'=\s?3 mharc', chunk)) else [0, 5]
                crits = [criterion(part, 'Freagra', 5, [chunk, notes], permitted=permitted)]
                mode, here, requirements = None, topic, READING_PART_OL
                note = ('SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.')
                        + f' Scheme: “{lang_read.group(0)}” — one deduction from each passage total (50), never inside a single part.')
            card = part_card(sitting, atlas, slug, ref, text, here, pages, spages, crits, requirements, note, src, extra_topics)
            cards.append(card)
            by_question.setdefault(q, []).append((part, prompt, card, mode))
            if mode == 'slots':
                for n in (1, 2):
                    cards.append(part_card(sitting, f'{atlas}-{n}', f'{slug}-{n}', f'{ref} · Freagra {n}', text, topic, pages, spages,
                                           [criterion(f'{part}-{n}', f'Freagra {n}', 1, [chunk, general])], READING_PART,
                                           'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + PART_NOTE,
                                           src, None, practiceFocus=f'One of the two answers (answer {n}, 1 mark)'))
            if mode == 'points':
                for n in (1, 2):
                    unit = crits[n - 1]['label'].rsplit(' ', 1)[0]
                    word = {'Tréith': 'traits', 'Léargas': 'insights'}.get(unit, 'points of information')
                    cards.append(part_card(sitting, f'{atlas}-{n}', f'{slug}-{n}', f'{ref} · {unit.split()[0]} {n}', text, topic, pages, spages,
                                           [crits[n - 1]], READING_PART,
                                           'The scheme prices the two points 6 + 6 independently; this card practises one of them. ' + PART_NOTE,
                                           src, None, practiceFocus=f'One of the two {word}, in your own words ({word.split()[0][:-1]} {n}, 6 marks)'))
        for q, parts in by_question.items():
            card = whole[f'reading-{letter.lower()}-q{q}']
            crits = []
            for part, _, part_card_, mode in parts:
                for c in part_card_['criteria']:
                    c = copy.deepcopy(c)
                    c['label'] = (PART_LABELS[part] + (' ' + c['label'] if c['label'] != 'Freagra' else ' Freagra')) if higher else f'({part}) Freagra'
                    crits.append(c)
            assert sum(c['maxMarks'] for c in crits) == card['totalMarks'], (card['id'], [c['maxMarks'] for c in crits])
            card.update(atlasQuestionId=f'R-{letter}-{q}', reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
                        schemeFileid=scheme_fileid(level), schemePage=min(p for _, _, pc, _ in parts for p in pc['schemePages']),
                        schemePages=sorted({p for _, _, pc, _ in parts for p in pc['schemePages']}), criteria=crits,
                        taskRequirements=READING_WHOLE if higher else READING_WHOLE[:2], sourceMaterial=src,
                        markingGuideNote=('Complete printed question. Score each published part separately using these SEC allocations. '
                                          'Two-answer grammar is one 0/2/3 placement; opinion and point conditions remain inside their response awards.'
                                          if higher else
                                          'Complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. '
                                          f'Scheme: “{lang_read.group(0)}” — one deduction from each passage total (50), never inside a single part.'))
            if higher and q == 6:
                card['additionalTopicIds'] = ['irish-3-3']
            stamped.append(card['id'])
    return cards, stamped


def part_card(sitting, atlas, slug, ref, text, topic, pages, scheme_pages, criteria, requirements, note, src, extra_topics, **extra):
    """A practice card the June reviews add beside the legacy ones (a printed part, or one answer of it)."""
    level = sitting.level
    return dict(id=sitting.card_id(2, slug), year=sitting.year, level=level, paper=2, section='2',
                atlasQuestionId=atlas, questionRef=sitting.ref(2, ref), questionText=text,
                totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
                **({'additionalTopicIds': extra_topics} if extra_topics else {}),
                conceptId=f'irish-{sitting.ll}-p2-{slug}', paperFileid=fileid(sitting.year, level, 2), schemeFileid=scheme_fileid(level),
                schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
                taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src, **extra)


LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
# A page's running head, and the section label 2022 and 2023 print in the margin ("B – PRÓS ROGHNACH – (50 marc)",
# "3B – FILÍOCHT ROGHNACH"), which the text layer stores after the page's last option.
PAPER_FURNITURE = re.compile(r'\s*(?:Scrúdú na hArdteistiméireachta|Gaeilge, Páipéar 2 – (?:Ardleibhéal|Gnáthleibhéal)'
                             r'|[23]?[AB]\s*– (?:PRÓS|FILÍOCHT) (?:AINMNITHE|ROGHNACH)(?: – \(50 marc\))?)\s*\d*\s*$')


def option_start(s, prompt, start, stop, label='', span=False):
    """Where the scheme restates a literature option: its printed words (after the option's own label), backed up over
    the label ("(a) ", "nó (b) ", "4A. ") that opens it."""
    words = re.sub(r'^(?:\((?:[a-f]|i{1,3})\)\s*|4[A-F]\.\s*)+', '', prompt)
    # A literature option's opening words are shared by its neighbours ("Freagair an cheist thíos ar an …"): match long.
    found = find_prompt(s.text, words, start, stop, tries=((12, 0), (9, 0), (7, 0), (8, 1)))
    if not found:
        # 2023 sets "Eolas = 25 marc" between a prescribed text's title and its statement, and rewords the statement
        # ("áibhéalach … sa scéal seo" for the paper's "áibhéileach … sa scéal"): the title, that line, then the
        # statement's first three words.
        for count in range(6, 0, -1):
            m = re.compile(words_pattern(words, count) + r'\W*Eolas\s*=\s*\d+\s*m?h?arc\W*' + words_pattern(words, 3, count),
                           re.I).search(s.text, start)
            if m and m.start() < stop:
                found = (m.start(), m.end())
                break
    if not found:
        return None
    head = re.search(r'(?:nó\s*)?(?:\([a-f]\)\s*)?(?:\(i\)\s*)?(?:4[A-F]\.\s*)?(?:⟦\d+⟧\s*)?$', s.text[max(0, found[0] - 24):found[0]])
    at = found[0] - (len(head.group(0)) if head else 0)
    return (at, found[1]) if span else at


# The prescribed prose that prints two texts as one option ("ar an scannán Cáca Milis nó ar an dráma An Lasair
# Choille"): each text is its own card, as June 2024 and 2026 card them (irish_higher_routes.py, irish_higher_2026_p2.py).
CHOICE_TEXTS = (('caca-milis', 'Cáca Milis', 'irish-4-6'), ('an-lasair-choille', 'An Lasair Choille', 'irish-4-8'))


def two_texts(question):
    """[(slug, title, topic, intro, the text's own question)] when an option prints the two prescribed texts, else []."""
    if not all(title in question for _, title, _ in CHOICE_TEXTS):
        return []
    # The option's opening sentence names both texts; each text's own question starts with its title after it.
    after = question.index('. ') + 1
    marks = [question.index(' ' + title + ' ', after) for _, title, _ in CHOICE_TEXTS]
    assert marks[0] < marks[1], question[:200]
    intro = question[:after].strip()
    # Each text's title is a line of its own above its question, as the paper sets it.
    # The "nó" printed between the two texts belongs to neither.
    blocks = [re.sub(r'^(' + re.escape(title) + r')\s+', r'\1\n', re.sub(r'\s+nó$', '', block))
              for (_, title, _), block in zip(CHOICE_TEXTS, [question[marks[0]:marks[1]].strip(), question[marks[1]:].strip()])]
    return [(slug, title, topic, intro, block) for (slug, title, topic), block in zip(CHOICE_TEXTS, blocks)]


def eolas_cap(piece):
    caps = re.search(r'(?:Eolas|Míniú|Plé)\s*=\s*(\d+)\s*m?h?arc', piece)
    # 2022 prints a part's cap as "Eolas - 13" above its own split ("Príomhthéama T(2) = 2 mharc; Plé/Eolas = 11 mharc"),
    # and in Ceist 4F as "Eolas – 19 marc", "Míniú – 7 marc", "Eolas 9 marc".
    loose = re.search(r'(?<![/\w])(?:Eolas|Míniú)\s*(?:[-–]\s*)?(\d+)\s*m?h?arc\b|(?<![/\w])Eolas - (\d+)\b', piece)
    if loose and (not caps or loose.start() < caps.start()):
        return int(loose.group(1) or loose.group(2))
    return int(caps.group(1)) if caps else None


def sub_pieces(chunk, prompt, labels=('ii', 'iii')):
    """A chunk cut at the scheme's restatement of each later printed part ("(ii) Cén mothúchán …")."""
    cuts = [0]
    for label in labels:
        m = re.search(r'\(' + label + r'\)\s+([A-ZÁÉÍÓÚ‘“\'].*?)(?=\s\((?:i{1,3}|iv|v)\)\s|\(\d+ m?h?arc\)|$)', prompt)
        assert m, (label, prompt[:120])
        found = find_prompt(chunk, m.group(1), cuts[-1] + 1, len(chunk))
        assert found, (label, m.group(1)[:60], chunk[:200])
        head = re.search(r'\(' + label + r'\)\s*$', chunk[max(0, found[0] - 8):found[0]])
        if not head:
            # A reworded restatement matched from its second word ("(iii) Conas mar a chuaigh …" for the paper's "Conas a
            # chuaigh …"): the part still starts at its label.
            head = re.search(r'\(' + label + r'\)\s*(?:\S+\s+){1,2}$', chunk[max(0, found[0] - 40):found[0]])
        cuts.append(found[0] - (len(head.group(0)) if head else 0))
    return [chunk[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk)])]


def literature_higher(sitting, base):
    """Each prose, poetry and Ceist 4 option one card: its Eolas at the deferred scheme's printed caps, and the one shared
    five-mark Gaeilge award (irish_higher_2025_p2.py's apply_legacy_review, on the deferred scheme)."""
    s, level, year = sitting.scheme, sitting.level, sitting.year
    by_key = {c['id'].split('-p2-', 1)[1]: c for c in base if '-p2-' in c['id'] and '-reading-' not in c['id']}
    assert len(by_key) == 14, sorted(by_key)
    table, note5 = gaeilge_table(sitting.docs[0])
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [table, note5], 'quality')
    lit_start = s.find(r'Nóta: I gcás na gceisteanna 2 \(Prós\)')
    assert lit_start, 'literature notes not found'
    n = s.find(r'Nóta: Níl na nótaí tacaíochta seo uileghabhálach', lit_start.start())
    notes = clean(re.sub(r'⟦\d+⟧', ' ', s.text[n.start():s.find(r'Gaeilge \(5 mharc\)|Freagair Ceist 2A', n.start()).start()]))
    pt = s.find(r'Catagóir Eolas \(25 marc\)')
    assert pt, 'prose band table not found'
    prose_table = clean(re.sub(r'⟦\d+⟧', ' ', s.text[pt.start():s.find(r'Ceist 2\s*PRÓS|⟦', pt.end()).start()]))
    assert '22-25' in prose_table and '0-9' in prose_table, prose_table[-120:]
    sec2 = s.find(r'2A\. Prós Ainmnithe', lit_start.start())
    sec3 = s.find(r'Freagair Ceist 3A|3A\. Filíocht Ainmnithe', sec2.start())
    sec3b = s.find(r'3B\. Filíocht Roghnach', sec3.start())
    sec4 = s.find(r'Freagair do rogha ceann amháin as Ceist 4', sec3.start())
    assert sec2 and sec3 and sec4, 'literature sections not found'
    q4_panel = s.find(r'Ceist 4\s*LITRÍOCHT BHREISE \(40 marc\)', sec4.start())
    g4 = s.find(r'Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', sec4.start())
    assert g4, 'Ceist 4 directions not found'
    # The directions and band table end at the separate Gaeilge table or the section's box; a band table that prints the
    # Gaeilge column beside the Eolas one (2023) keeps it.
    # 2022 restates the options straight after the table ("4A. An Triail …"), so the table ends there.
    general4 = clean(re.sub(r'⟦\d+⟧', ' ', s.text[g4.start():s.find(r'Gaeilge \(5 mharc\)\s*Sárchumas|Ceist 4\s*LITRÍOCHT|⟦\d+⟧\s*4A\.\s', g4.end()).start()]))
    assert '30-35' in general4, general4[-200:]
    stamped = []

    def stamp(key, atlas, chunk_pages, criteria, note, extra_pages=()):
        card = by_key[key]
        card['questionText'] = PAPER_FURNITURE.sub('', card['questionText'])
        m = re.match(r'(prose|poetry|literature)-(\d[ab]?)-([a-f])', key)
        heading = {'prose': 'Prós', 'poetry': 'Filíocht', 'literature': 'Litríocht'}[m.group(1)]
        address = f'{m.group(2).upper()}({m.group(3)})' if m.group(1) != 'literature' else f'4{m.group(3).upper()}'
        # 4F is a prescribed poem, printed "4F. Dánta Breise – A Chlann": it is named so, never "Dán roghnach".
        breise = re.search(r'4F\.\s*(Dánta Breise\s*[–-]\s*.+?)\s+Freagair', card['questionText']) if key == 'literature-4-f' else None
        card['questionRef'] = sitting.ref(2, f'{heading} {address} · {card.pop("_title", None) or (breise.group(1) if breise else title_of(card["questionText"]))}')
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=[card['paperPage']], schemeFileid=scheme_fileid(level),
                    schemePage=min(chunk_pages | set(extra_pages)), schemePages=sorted(chunk_pages | set(extra_pages)),
                    criteria=criteria, markingGuideNote=note, taskRequirements=LIT_REQUIREMENTS)
        if 'sourceMaterial' in card:
            card['sourceMaterial'] = dict(card['sourceMaterial'], attribution=ATTRIBUTION)
        assert sum(c['maxMarks'] for c in criteria) == card['totalMarks'], (card['id'], [c['maxMarks'] for c in criteria])
        stamped.append(card['id'])

    # Prose: 2A(a), 2A(b) are restated in the scheme with their notes; a scheme that prints one band table for the
    # whole section (2B, the optional prose) marks it by that table alone.
    prose = []
    for key, atlas in [('prose-2a-a', 'P-2A-a'), ('prose-2a-b', 'P-2A-b'), ('prose-2b-a', 'P-2B-a'), ('prose-2b-b', 'P-2B-b')]:
        card = by_key[key]
        question = card['questionText']
        if key.startswith('prose-2a') and all(title in question for _, title, _ in CHOICE_TEXTS) and question.count(' marc)') < 2:
            # The legacy builder stops an option at its first tariff, which drops the second text: read the option whole.
            page = clean(sitting.texts[2][card['paperPage'] - 1])
            intro = re.sub(r'^\([ab]\)\s*', '', question.split('. ', 1)[0] + '.')
            at = comparable(page).index(comparable(intro))
            raw = page[next(i for i in range(len(page)) if comparable(page[:i]) == comparable(page)[:at]):]
            # The match ends at the label's last letter ("(a"): its closing bracket is not the option's text.
            raw = re.sub(r'^\)\s*', '', raw)
            raw = re.split(r'\s(?:nó\s+)?\(b\)\s|\s2B\b', raw)[0]
            question = f'({key[-1]}) ' + PAPER_FURNITURE.sub('', raw).strip()
            assert question.count(' marc)') == 2, question
        texts = two_texts(question) if key.startswith('prose-2a') else []
        if not texts and key == 'prose-2a-a':
            # 2022 sets the two texts as titled alternatives of (a), each with its own statement and tariff ("Cáca Milis (a)
            # ‘…’ (30 marc) nó An Lasair Choille ‘…’ (30 marc)"); the legacy reader keeps only the first.
            page = clean(sitting.texts[2][card['paperPage'] - 1])
            m = re.search(r'Cáca Milis \(a\) (‘.*?\(30 marc\)) nó An Lasair Choille (‘.*?\(30 marc\))', page)
            if m:
                texts = [(slug, title, topic, None, f'{title}\n{block}')
                         for (slug, title, topic), block in zip(CHOICE_TEXTS, m.groups())]
                assert comparable(texts[0][4].split('\n', 1)[1]) in comparable(question), question
        if not texts:
            prose.append((key, atlas, card['questionText']))
            continue
        base.remove(card)
        del by_key[key]
        for slug, title, topic, intro, block in texts:
            twin = copy.deepcopy(card)
            option = key[-1]
            twin.update(id=sitting.card_id(2, f'{key}-{slug}'), topicId=topic, conceptId=f'irish-prose-2a-{topic}', _title=title,
                        questionText=f'{intro}\n\n{block}' if intro else f'({option}) {block}')
            base.append(twin)
            by_key[f'{key}-{slug}'] = twin
            # A titled alternative is found in the scheme by its statement: 2022 prints "Cáca Milis (a) ‘…’" there too.
            prose.append((f'{key}-{slug}', f'{atlas}-{slug}', block if intro else block.split('\n', 1)[1]))
    starts, cursor = [], sec2.start()
    for key, atlas, prompt in prose:
        found = option_start(s, prompt, cursor, sec3.start())
        starts.append(found)
        cursor = found + 1 if found else cursor
    band_pages = {s.page_at(pt.start())}
    for index, (key, atlas, _) in enumerate(prose):
        if starts[index] is None:
            assert key.startswith('prose-2b') and not s.find(r'2B\. Prós Roghnach'), (key, 'a prescribed option the scheme does not restate')
            guidance, pages = [prose_table, notes], band_pages
        else:
            section_end = (s.find(r'2B\. Prós Roghnach|Nóta: Níl na nótaí tacaíochta', starts[index] + 50) or sec3).start()
            end = next((x for x in starts[index + 1:] if x), None) or section_end
            # 2023 restates the optional prose too: a prescribed option still stops at the 2B heading, and the shared
            # Gaeilge table printed after an option's marking boxes is the Gaeilge award's, not the option's.
            if key.startswith('prose-2a'):
                end = min(end, section_end)
            table_at = s.find(r'Gaeilge \(5 mharc\)\s*Sárchumas', starts[index])
            if table_at:
                end = min(end, table_at.start())
            end = min(end, sec3.start())
            chunk, pages = s.chunk(starts[index], end)
            chunk = re.sub(r'^nó ', '', chunk)
            # 2022 sets the next prescribed text's title after an option's notes ("… nó An Lasair Choille"): it is the next card's.
            chunk = re.sub(r'\s+nó\s+(?:' + '|'.join(re.escape(t) for _, t, _ in CHOICE_TEXTS) + r')$', '', chunk)
            # The Eolas as each scheme prints it: "Eolas = 25 marc"; 2022's "Eolas – 25", its band table's "Eolas (25 marc)",
            # its "Eolas 13 + 12 = 25" for two headings, and its "an marc as 25 [(13 + 12)] (Eolas)" under an optional option.
            assert (re.search(r'Eolas = 25 m?h?arc|Eolas – 25|Eolas \(25 marc\)|Eolas 13 \+ 12 = 25|an marc as 25 (?:\(13 \+ 12\) )?\(Eolas\)', chunk)
                    and 'Gaeilge (5 mharc) Sárchumas' not in chunk), (key, chunk[:200])
            guidance, pages = [chunk] + ([prose_table] if prose_table not in chunk else []) + [notes], set(pages) | band_pages
        two_heads = starts[index] is not None and 'an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12' in guidance[0]
        if two_heads:
            # 2022: two of three printed headings, "an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12".
            eolas = [criterion('eolas-1', 'An ceann is fearr', 13, guidance, 'indicative'), criterion('eolas-2', 'An ceann eile', 12, guidance, 'indicative')]
        else:
            eolas = [criterion('eolas', 'Eolas', 25, guidance, 'indicative')]
        # The one-aspect rule only where this sitting's scheme prints it (2025: "… Déan measúnú ar fhiúntas an phlé sa
        # fhreagra as 18 marc."; its band table's 18-mark column).
        out_of_18 = '18 marc' in ' '.join(guidance)
        # 2022 restates its optional prose with no notes (no "Nótaí", no sample points): its band table is the marking.
        noteless = starts[index] is None or not re.search(r'Nótaí|•', guidance[0])
        notes_line = '' if (noteless and starts[index] is not None) else ' Supporting notes are indicative rather than exhaustive'
        stamp(key, atlas, set(pages), eolas + [gaeilge()],
              ('One complete SEC response: two of the three printed headings, the better one marked out of 13 and the other out of 12, and a '
               'single shared 5-mark Gaeilge award.' + (notes_line + '.' if notes_line else '') if two_heads else
               'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award.' + notes_line
               + ('; with only one of the required aspects discussed, the scheme marks the Eolas out of 18.' if out_of_18 else '.' if notes_line else ''))
              + ((' The deferred scheme prints no notes for the optional prose: its Treoir and band table are the marking.'
                  if starts[index] is not None and 'Treoir' in guidance[0] else
                  ' The deferred scheme prints no notes for the optional prose: its band table is the marking.') if noteless else ''))

    poems = [('poetry-3a-a', 'F-3A-a'), ('poetry-3a-b', 'F-3A-b'), ('poetry-3b-a', 'F-3B-a'), ('poetry-3b-b', 'F-3B-b')]
    # Each poem searched for after the one before it: 2023 restates both optional poems, and they open alike ("Maidir le dán
    # nua-aimseartha roghnach a ndearna tú staidéar air …").
    starts, cursor = [], sec3.start()
    for key, _ in poems:
        found = option_start(s, by_key[key]['questionText'], cursor, sec4.start(), span=True)
        assert found is None or not key.startswith('poetry-3b') or re.match(r'(?:nó\s*)?\(' + key[-1] + r'\)', s.text[found[0]:]), (key, s.text[found[0]:found[0] + 60])
        starts.append(found[0] if found else None)
        cursor = found[1] if found else cursor
    assert all(starts[:2]), [k for (k, _), x in zip(poems, starts) if not x]
    for index, (key, atlas) in enumerate(poems):
        if starts[index] is None:
            # The deferred scheme prints no key for the optional poetry: its note's “san Fhilíocht 25 ar Eolas agus 5 ar
            # Ghaeilge” is the marking, so the Eolas is one 25-mark award (no part caps are printed to split it by).
            assert key.startswith('poetry-3b') and not sec3b, (key, 'a poem the scheme does not restate')
            asked = [re.sub(r'\s*\(\d+ m?h?arc\)$', '', prompt).strip() for _, prompt, _ in printed_parts(PAPER_FURNITURE.sub('', by_key[key]['questionText']))]
            stamp(key, atlas, {s.page_at(lit_start.start())}, [criterion('eolas', 'Eolas', 25, asked, 'indicative'), gaeilge()],
                  f'{UNPRINTED} The deferred scheme prints no key for the optional poetry: its note gives poetry 25 for Eolas and 5 for Gaeilge, '
                  'so the Eolas is one 25-mark award judged on merit (the paper’s part tariffs, 15, 6 and 9, include the shared Gaeilge).')
            continue
        end = next((x for x in starts[index + 1:] if x), None) or sec4.start()
        if key == 'poetry-3a-b' and sec3b:
            end = min(end, sec3b.start())
        chunk, pages = s.chunk(starts[index], end)
        chunk = re.sub(r'^nó ', '', lifted_table_out(chunk, table)).strip()
        pieces = sub_pieces(chunk, by_key[key]['questionText'])
        caps = [eolas_cap(p) for p in pieces]
        assert None not in caps and sum(caps) == 25, (key, caps)
        guidance0 = [pieces[0], notes] if atlas.startswith('F-3A') else [pieces[0]]
        stamp(key, atlas, set(pages), [criterion('eolas-i', '(i) Eolas', caps[0], guidance0, 'indicative'),
                                       criterion('eolas-ii', '(ii) Eolas', caps[1], [pieces[1]], 'indicative'),
                                       criterion('eolas-iii', '(iii) Eolas', caps[2], [pieces[2]], 'indicative'), gaeilge()],
              f'One complete SEC response with one shared five-mark Gaeilge award. The Eolas criteria keep the printed caps ({", ".join(map(str, caps))}) '
              'and conditions. Supporting notes are indicative rather than exhaustive.')

    letters = 'abcdef'
    q4 = []
    for letter in letters:
        heading = None
        for m in re.finditer(r'4' + letter.upper() + r'\.\s', s.text[sec4.start():]):
            at = sec4.start() + m.start()
            ahead = s.text[at:at + 2500]
            # Read up to the next option's heading: 2022 restates 4A–4E with no notes, and 4F's caps ("Eolas – 19 marc")
            # lie within reach of them.
            following = re.compile(r'\s4[A-F]\.\s').search(ahead, 4)
            if following and letter != 'f' and re.search(r'Eolas – \d+ m?h?arc', s.text[sec4.start():]):
                ahead = ahead[:following.start()]
            if re.search(r'Eolas = \d+ m?h?arc', ahead) or (letter == 'f' and re.search(r'Eolas – \d+ m?h?arc', ahead)):
                heading = at
                break
        q4.append(heading)
    assert q4[-1], 'the scheme prints no 4F key'
    for index, letter in enumerate(letters):
        key, atlas = f'literature-4-{letter}', f'X-4{letter.upper()}'
        if q4[index] is None:
            # The deferred scheme prints no notes for this option: Ceist 4's directions and band table are its marking.
            stamp(key, atlas, {s.page_at(g4.start())}, [criterion('eolas', 'Eolas', 35, [general4], 'indicative'), gaeilge()],
                  'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. The deferred scheme prints no '
                  'notes for this option, so Ceist 4’s directions and band table are its marking.')
            continue
        end = next((x for x in q4[index + 1:] if x), None) or len(s.text)
        chunk, pages = s.chunk(q4[index], end)
        chunk = re.split(r'\s*(?:Socruithe Réasúnta|Ceist 4F \(40\) =)', lifted_table_out(chunk, table))[0].strip()
        pages = {p for p in pages if p <= s.page_at(q4[index] + len(chunk))}
        if letter != 'f':
            assert re.search(r'Eolas = 35 m?h?arc', chunk), (key, chunk[:200])
            stamp(key, atlas, set(pages), [criterion('eolas', 'Eolas', 35, [chunk, general4], 'indicative'), gaeilge()],
                  'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
                  {s.page_at(g4.start())})
        else:
            pieces = sub_pieces(chunk, by_key[key]['questionText'])
            caps = [eolas_cap(p) for p in pieces]
            assert None not in caps and sum(caps) == 35, (key, caps)
            stamp(key, atlas, set(pages), [criterion(f'eolas-{r}', f'({r}) Eolas', cap, [piece], 'indicative')
                                           for r, cap, piece in zip(('i', 'ii', 'iii'), caps, pieces)] + [gaeilge()],
                  f'One complete SEC response with one shared five-mark Gaeilge award. The Eolas criteria keep the printed caps ({", ".join(map(str, caps))}). '
                  'Supporting notes are indicative rather than exhaustive.')
    assert len(stamped) == 14 + sum(1 for k in by_key if k.startswith('prose-2a-') and k.count('-') > 3) // 2, stamped
    return stamped


def gaeilge_found(doc, first_page=1):
    """The printed five-row Gaeilge (5 mharc) table and its note, with their pages (irish_gaeilge.lifted's lift),
    reading a row's mark after its closing bracket with or without a full stop ("deilbhíocht). 2", 2022's Higher scheme)."""
    from irish_gaeilge import NOTE, ROWS, TABLE
    table = note = None
    for number in range(first_page, len(doc) + 1):
        text = re.sub(r'^\d+\s', '', clean(doc[number - 1].get_text()))
        if note is None and NOTE.search(text):
            note = (NOTE.search(text).group(0), number)
        if table is None and TABLE.search(text):
            table = (TABLE.search(text).group(0), number)
        if table and note:
            break
    assert table and note, 'Gaeilge table or note not found'
    assert [row for row in ROWS if row in table[0]] == list(ROWS) and re.findall(r'\)\.? ([1-5])\b', table[0]) == ['5', '4', '3', '2', '1'], table[0]
    assert 'gan fiúntas' not in table[0]
    return table[0], note[0], table[1], note[1]


def gaeilge_table(doc):
    table, note, _, _ = gaeilge_found(doc)
    return table, note


def lifted_table_out(chunk, table):
    """The printed Gaeilge table can sit between a key's parts; it belongs to the shared award, not to the Eolas."""
    return clean(chunk.replace(table, ' '))


TITLES = ['Oisín i dTír na nÓg', 'An Gnáthrud', 'Seal i Neipeal', 'Dís', 'Hurlamaboc', 'Cáca Milis', 'An Lasair Choille',
          'An Spailpín Fánach', 'Géibheann', 'An tEarrach Thiar', 'Mo ghrá-sa (idir lúibíní)', 'Colscaradh',
          'An Triail', 'A Thig Ná Tit Orm', 'Tóraíocht Dhiarmada agus Ghráinne', 'Gafa', 'Canary Wharf']
OPTIONAL = [('scannán roghnach nó', 'Scannán nó dráma roghnach'), ('gearrscéal roghnach', 'Gearrscéal roghnach'),
            ('scéal béaloidis roghnach', 'Scéal béaloidis roghnach'), ('úrscéal roghnach', 'Giota as úrscéal roghnach'),
            ('dán', 'Dán roghnach')]
HEADS_OL = {
    '2a': 'Freagair 2A (Prós Ainmnithe) nó 2B (Prós Roghnach).\n2A Prós Ainmnithe — Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.',
    '2b': ('Freagair 2A (Prós Ainmnithe) nó 2B (Prós Roghnach).\n2B Prós Roghnach — Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna '
           'freagraí ar an bPrós Roghnach. Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.'),
    '3a': 'Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).\n3A Filíocht Ainmnithe — Freagair do rogha dhá cheann as (a), (b) nó (c).',
    '3b': ('Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).\n3B Filíocht Roghnach — Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a '
           'úsáid sna freagraí ar an bhFilíocht Roghnach. Freagair do rogha dhá cheann as (a), (b) nó (c) thíos. Níl cead an dán roghnach céanna '
           'a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.'),
}
CHOOSE = 'Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.'
CHOOSE_3A = 'Freagair do rogha dhá cheann as (a), (b) nó (c).'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
SAME_POEM = 'Níl cead an dán roghnach céanna a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.'
LIT_OL = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
UNPRINTED = 'The scheme prints no answer for this part.'
ROMANS = ('i', 'ii', 'iii', 'iv', 'v')
# The section heads and choice rules as 2023's and 2022's deferred papers print them (each line is checked against the
# paper before use); 2024 and 2025 print HEADS_OL. 2022 sets the year's two-questions-from-the-section rule, as June 2022.
OL_PRINTED = {
    2023: ({'2a': 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).\nA – PRÓS AINMNITHE — Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.',
            '2b': ('Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).\nB – PRÓS ROGHNACH — Níl cead aon ábhar a bhaineann le Prós Ainmnithe a '
                   'úsáid sna freagraí ar an bPrós Roghnach. Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.'),
            '3a': 'Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).\nA – FILÍOCHT AINMNITHE — Freagair do rogha dhá cheann as (a), (b) nó (c).',
            '3b': ('Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).\nB – FILÍOCHT ROGHNACH — Níl cead aon ábhar a bhaineann le Filíocht '
                   'Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach. Freagair do rogha dhá cheann as (a), (b) nó (c) thíos. Níl cead an '
                   'dán roghnach céanna a úsáid faoi dhó.')},
           {'2a': CHOOSE, '2b': CHOOSE, '3a': CHOOSE_3A, '3b': CHOOSE}, 'Níl cead an dán roghnach céanna a úsáid faoi dhó.'),
    2022: ({'2a': '2A – PRÓS AINMNITHE',
            '2b': '2B – PRÓS ROGHNACH\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.',
            '3a': '3A – FILÍOCHT AINMNITHE',
            '3b': '3B – FILÍOCHT ROGHNACH\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'},
           dict.fromkeys(('2a', '2b', '3a', '3b'), 'Freagair dhá cheist as an roinn seo.'), None),
}


def title_of(question):
    """The printed text an option names, or the kind of open text an optional one asks about."""
    found = [t for t in TITLES if comparable(t) in comparable(question)]
    if found:
        return min(found, key=lambda t: comparable(question).index(comparable(t)))
    return next(label for needle, label in OPTIONAL if needle in question)


def printed_parts(question, romans=ROMANS):
    """An option's printed parts as [(roman, prompt, printed tariff or None)], and its nested lettered questions."""
    marks = list(re.finditer(r'(?:(?<=\s)|^)\((' + '|'.join(romans) + r')\)\s+', question))
    out = []
    for index, m in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(question)
        # The title line the optional poem prints after its last part is not that part.
        body = question[m.end():end].strip().split(' Ní mór teideal')[0].strip()
        tariff = re.search(r'\((\d+) m?h?arc\)\s*$', body)
        out.append((m.group(1), body, int(tariff.group(1)) if tariff else None))
    return out


def literature_ordinary(sitting, base):
    """Each prose and poetry option one card, with each printed part its own criterion at the deferred scheme's tariff, and
    each part of a prescribed text (and each question nested in one) its own practice card (irish_ordinary_2024_p2.py,
    irish_ordinary_2025_p2.py). An option the scheme prints no key for is carded at the paper's printed tariffs with the
    fixed sentence “The scheme prints no answer for this part.” (the 2011 aural's rule)."""
    s, level, year = sitting.scheme, sitting.level, sitting.year
    paper_text = ' '.join(sitting.texts[2])
    heads, choose, same_poem = OL_PRINTED.get(year, (HEADS_OL, {'2a': CHOOSE, '2b': CHOOSE, '3a': CHOOSE_3A, '3b': CHOOSE}, SAME_POEM))
    for head in [*heads.values(), *choose.values(), *([same_poem] if same_poem else [])]:
        for line in re.split(r'\n| — ', head):
            assert comparable(line) in comparable(paper_text), line
    by_key = {c['id'].split('-p2-', 1)[1]: c for c in base if '-p2-' in c['id'] and '-reading-' not in c['id']}
    assert len(by_key) == 12, sorted(by_key)
    lang = s.find(r'\[Gaeilge lochtach: 0[-‐]4 a bhaint den iomlán a gnóthaíodh\.?\]')
    assert lang, 'literature deduction not printed'
    lang = lang.group(0)
    # The deduction exactly as printed; each card's note says it applies once to the whole answer.
    deduction = lambda: criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [lang], 'quality', deduction=True)
    sections = {'2a': s.find(r'Freagair 2A \(Prós Ainmnithe\) nó 2B \(Prós Roghnach\)\.') or s.find(r'2A – PRÓS AINMNITHE'),
                '3a': s.find(r'Freagair 3A \(Filíocht Ainmnithe\) nó 3B \(Filíocht Roghnach\)\.') or s.find(r'3A – FILÍOCHT AINMNITHE')}
    if not any(sections.values()):
        # 2022's text layer stores each section heading inside its first key: a section opens at its own
        # "Nóta: Níl sé i gceist …", printed once for the prose and once for the poetry.
        opened = list(re.finditer(r'Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', s.text))
        assert len(opened) == 2, len(opened)
        sections = {'2a': opened[0], '3a': opened[1]}
    assert all(sections.values()), sections
    notes = {}
    for key, m in sections.items():
        n = s.find(r'Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha.*?de réir a bhfiúntais\.', m.start())
        assert n, key
        notes[key] = clean(re.sub(r'⟦\d+⟧', ' ', n.group(0)))
    ends = {'2a': sections['3a'].start(), '3a': len(s.text)}
    cards, stamped = [], []

    def key_of(section, option, title):
        """The scheme's key for an option: "(a) Oisín i dTír na nÓg (25 marc)", up to its language deduction."""
        lo, hi = sections[section].start(), ends[section]
        if title in ('Cáca Milis', 'An Lasair Choille'):
            # One of two texts printed as one option: its own key opens "Cáca Milis (25 marc)".
            m = re.compile(words_pattern(title) + r'\s*(?:⟦\d+⟧\s*)?\(25 marc\)', re.I).search(s.text, lo)
        else:
            m = re.compile(r'\(' + option + r'\)\s*(?:⟦\d+⟧\s*)?(?:[^()⟦]{0,120}?)?' + words_pattern(title), re.I).search(s.text, lo)
        if not m or m.start() >= hi:
            return None
        stop = s.find(r'\[Gaeilge lochtach', m.end())
        chunk, pages = s.chunk(m.start(), min(stop.start(), hi))
        return chunk, pages

    def cut(chunk, parts):
        """The key cut at each later part's restatement; each piece carries its printed tariff."""
        cuts = [0]
        for roman, prompt, _ in parts[1:]:
            words = re.sub(r'^\([a-d]\)\s*', '', prompt)
            # The part's own label before its first words; else its words alone (a scheme that drops the label).
            labelled = re.compile(r'\(' + roman + r'\)\s*(?:\([a-d]\)\s*)?' + words_pattern(words, 3), re.I).search(chunk, cuts[-1] + 1)
            if labelled:
                cuts.append(labelled.start())
                continue
            found = find_prompt(chunk, words, cuts[-1] + 1, len(chunk))
            assert found, (roman, words[:60], chunk[:160])
            head = re.search(r'\(' + roman + r'\)\s*(?:\([a-d]\)\s*)?$', chunk[max(0, found[0] - 12):found[0]])
            cuts.append(found[0] - (len(head.group(0)) if head else 0))
        # A piece never ends with the next part's label: 2022 labels Dís's (v) "(iv)", so it is cut at its words.
        pieces = [re.sub(r'\s*\((?:i{1,3}|iv|v)\)$', '', chunk[a:b].strip()) for a, b in zip(cuts, cuts[1:] + [len(chunk)])]
        # 2022's text layer stores a part's heading before its prices and its tariff after them ("… véarsa a dó. Freagra samplach:
        # Dhá phointe eolais = 4 mharc + 4 mharc (8 marc) • …"); the page prints the tariff beside the question, then the prices,
        # then the samples under their heading. Read in that order. No word changes.
        pieces = [re.sub(r'^(.*?)\s+(Freagra(?:í)? [Ss]amplach(?:a)?:)\s+([^•\uf0b7]*?=[^•\uf0b7]*?)\s+(\(\d+ m?h?arc\))\s+([•\uf0b7].*)$',
                         r'\1 \4 \3 \2 \5', piece) for piece in pieces]
        if parts and parts[0][0] == 'i':
            # The first piece starts at the option's heading; its part starts at "(i)".
            pieces[0] = pieces[0][pieces[0].index('(i)'):] if '(i)' in pieces[0] else pieces[0]
        return pieces

    def tariff_of(piece):
        m = re.search(r'\((\d+) m?h?arc\)', piece)
        return int(m.group(1)) if m else None

    def unit_tariff(piece):
        """2022 prices some parts without a bracketed total: by their priced lines ("An sórt duine = 1 mharc Dhá phointe
        eolais = 2 mharc + 2 mharc"), or by a bare total after the question ("… ar an bpáipéar? 5 mharc")."""
        head = re.split(r'Freagra(?:í)? Samplach', piece)[0]
        lines = re.findall(r'=\s*(\d+) mharc((?:\s*\+\s*\d+ mharc)*)', head)
        if lines:
            return sum(int(a) + sum(int(x) for x in re.findall(r'(\d+) mharc', rest)) for a, rest in lines)
        bare = re.search(r'\?\s+(\d+) mharc\b', head)
        return int(bare.group(1)) if bare else None

    cursors = {'2': 0, '3': 0}

    def plain_words(text, count):
        bare = ''.join(ch for ch in unicodedata.normalize('NFD', text.replace('‐', '-').lower()) if not unicodedata.combining(ch))
        return re.findall(r'\w+', bare)[:count]

    def optional_key(section, option, text):
        """An optional option's key where the deferred scheme restates it (2022, 2023; 2024 and 2025 print none): its own
        label followed by its printed words (the three optional poems open alike, and 2023's restatement of 3B(a) drops
        a word: "Maidir dán nua‐aimseartha"), to its language deduction; one chunk per printed alternative ("scannán
        roghnach … NÓ … dráma roghnach", each keyed in full and each closed by its own deduction)."""
        home = section[0] + 'a'
        lo, hi = max(sections[home].start(), cursors[section[0]]), ends[home]
        want = plain_words(re.sub(r'^(?:\((?:[a-d]|i{1,3})\)\s*)+', '', text), 12)
        start = None
        for m in re.compile(r'\(' + option + r'\)\s*(?:⟦\d+⟧\s*)?(?:\(i\)\s*)?').finditer(s.text, lo, hi):
            got = plain_words(re.sub(r'⟦\d+⟧', ' ', s.text[m.end():m.end() + 400]), 12)
            if difflib.SequenceMatcher(None, want, got).ratio() >= 0.85:
                start = m.start()
                break
        if start is None:
            return None
        cursors[section[0]] = start + 1
        alternatives, pages = [], set()
        for n in range(max(1, len(re.findall(r'Ní mór teideal', text)))):
            if n:
                # The next alternative opens with its own printed "Maidir le …" after the previous one's deduction.
                start = s.find(r'Maidir le', start).start()
            stop = s.find(r'\[Gaeilge lochtach', start)
            assert stop and stop.start() < hi, (section, words[:60])
            chunk, at = s.chunk(start, stop.start())
            alternatives.append(chunk)
            pages |= set(at)
            start = stop.end()
        return alternatives, sorted(pages)

    def subset_sums(values):
        sums = {0}
        for v in values:
            sums |= {x + v for x in sums}
        return sorted(sums)

    def title_criterion(key, alternatives, marks):
        """The title (and writer) the option asks for, priced as the key prints it ("Teideal an ghiota = 1 mharc Ainm an
        údair = 1 mharc"); a bracketed tariff the text layer stores after it is not part of the line."""
        lines = []
        for chunk in alternatives:
            at = chunk.index('Ní mór teideal')
            # The title's own tariff after its lines stays ("… Ainm an scríbhneora = 1 mharc (2 mharc)", as June's cards keep it);
            # another stored beside it does not (2022 2B(a): "… = 1 mharc (23 marc) (2 mharc)").
            lines.append(re.sub(r'(?:\s*\(\d+ m?h?arc\))+\s*$',
                                lambda m: f' ({marks} mharc)' if re.search(r'\(%d m?h?arc\)' % marks, m.group(0)) else '', chunk[at:]).strip())
        units = [[int(v) for v in re.findall(r'= (\d+) m?h?arc', line)] for line in lines]
        assert all(sum(u) == marks for u in units) and len({tuple(u) for u in units}) == 1, (key, lines)
        label = 'Teideal + ainm' if len(units[0]) > 1 else 'Teideal'
        return criterion('teideal', label, marks, list(dict.fromkeys(lines)), 'exact', permitted=subset_sums(units[0]))

    def permitted_for(piece, marks):
        if marks == 5 and '3 mharc + 2 mharc' in piece:
            return [0, 3, 5]
        return None

    def add(card):
        cards.append(card)
        return card

    for section in ('2a', '2b', '3a', '3b'):
        prose = section.startswith('2')
        family = 'prose' if prose else 'poetry'
        for option in 'abc':
            legacy_key = f'{family}-{section}-{option}'
            card = by_key[legacy_key]
            question = PAPER_FURNITURE.sub('', card['questionText'])
            texts = two_texts(question) if section == '2a' else []
            routes = ([(f'{legacy_key}-{slug}', f'{"P" if prose else "F"}-{section.upper()}-{option}-{slug}', title, topic, intro + '\n' + block)
                       for slug, title, topic, intro, block in texts] if texts else
                      [(legacy_key, f'{"P" if prose else "F"}-{section.upper()}-{option}', title_of(question), card['topicId'], question)])
            if texts:
                base.remove(card)
            for key, atlas, title, topic, text in routes:
                route = card if not texts else copy.deepcopy(card)
                if texts:
                    base.append(route)
                ref = f'{"Prós" if prose else "Filíocht"} {section.upper()}({option}) · {title}'
                # The option's own total after its last part ("… go hÉirinn. (25 marc)") is not that part's tariff.
                parts = printed_parts(re.sub(r'\s*\(25 marc\)\s*$', '', text))
                prescribed = section.endswith('a')
                found = key_of(section, option, title) if prescribed else None
                requirements = [choose[section]] + (
                    [NO_PRESCRIBED_PROSE] if section == '2b' else [NO_PRESCRIBED_POETRY] + ([same_poem] if same_poem else []) if section == '3b' else []) + LIT_OL
                if texts:
                    requirements.insert(1, texts[0][3].split(') ', 1)[1])
                body = re.sub(r'\s+(?=\((?:' + '|'.join(ROMANS) + r')\)\s)', '\n', text)
                route.update(id=sitting.card_id(2, key), topicId=topic, questionRef=sitting.ref(2, ref), questionText=heads[section] + '\n' + body,
                             atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=[route['paperPage']], schemeFileid=scheme_fileid(level),
                             taskRequirements=requirements)
                if not route.get('sourceMaterial'):
                    # The option's printed page in the source reader (irish_ordinary_2025_p2.py attaches it to every option).
                    shelf = {'2a': 'Prós Ainmnithe', '2b': 'Prós Roghnach', '3a': 'Filíocht Ainmnithe', '3b': 'Filíocht Roghnach'}[section]
                    route['sourceMaterial'] = source(year, level, 2, shelf, [route['paperPage']],
                                                     title=title if section != '3b' else f'3B({option}) · Dán roghnach')
                keyed = None if prescribed else optional_key(section, option, text)
                if keyed:
                    alternatives, spages = keyed
                    titles = [int(m) for m in re.findall(r'Ní mór teideal[^()]*?\.\s*\((\d+) m?h?arc\)', text)]
                    assert len(set(titles)) == 1 and len(titles) == len(alternatives), (key, titles)
                    if parts:
                        assert len(alternatives) == 1, key
                        chunk = alternatives[0]
                        pieces = cut(chunk[:chunk.index('Ní mór teideal')], parts)
                        caps = []
                        for (roman, prompt, printed_cap), piece in zip(parts, pieces):
                            assert len(printed_parts(prompt, romans=('a', 'b', 'c', 'd'))) <= 1, (key, roman)
                            cap = printed_cap or tariff_of(piece)
                            assert cap and re.search(r'\(%d m?h?arc\)' % cap, piece), (key, roman, printed_cap, piece[:120])
                            caps.append(cap)
                        criteria = [criterion(f'eolas-{roman}', f'({roman}) Eolas', cap, [piece], 'indicative', permitted=permitted_for(piece, cap))
                                    for (roman, _, _), cap, piece in zip(parts, caps, pieces)]
                        summary = ', '.join(f'({r}) {c}' for (r, _, _), c in zip(parts, caps))
                    else:
                        paper_units = re.findall(r'\s*(.*?)\s*\((\d+) m?h?arc\)', text.split(') ', 1)[1])
                        eolas_marks = {int(m) for u, m in paper_units if not u.startswith('Ní mór teideal')}
                        assert len(eolas_marks) == 1, (key, paper_units)
                        eolas_marks = eolas_marks.pop()
                        # Each alternative's key: its priced lines ("An phríomhphearsa … a ainmniú = 1 mharc", "Na heachtraí … =
                        # 22 marc") before its points rule ("5 phointe eolais ag teastáil …"), which goes with the largest line.
                        shapes = []
                        for chunk in alternatives:
                            body = chunk[:chunk.index('Ní mór teideal')]
                            after = body.split('(25 marc)', 1)
                            assert len(after) == 2, (key, body[:160])
                            rule = re.search(r'\d phointe eolais ag teastáil', after[1])
                            assert rule, (key, after[1][:160])
                            lines = [(m.group(0).strip(), m.group(1).strip(), int(m.group(2)))
                                     for m in re.finditer(r'\s*(.+?) = (\d+) m?h?arc', after[1][:rule.start()])]
                            shapes.append((lines, after[1][rule.start():].strip()))
                        marks_of = {tuple(m for _, _, m in lines) for lines, _ in shapes}
                        assert len(marks_of) == 1, (key, marks_of)
                        lines0 = shapes[0][0]
                        assert sum(m for _, _, m in lines0) in (0, eolas_marks), (key, lines0, eolas_marks)
                        if not lines0:
                            criteria = [criterion('eolas', 'Eolas', eolas_marks, list(dict.fromkeys(rule for _, rule in shapes)), 'indicative')]
                        else:
                            big = max(range(len(lines0)), key=lambda i: lines0[i][2])
                            criteria = []
                            for i, (_, label, marks) in enumerate(lines0):
                                guidance = list(dict.fromkeys(lines[i][0] + (' ' + rule if i == big else '') for lines, rule in shapes))
                                ident = 'eolas' if i == big else 'ainmniu' if 'ainmniú' in label else 'lua' if label.endswith(' a lua') else f'line-{i + 1}'
                                criteria.append(criterion(ident, label, marks, guidance, 'indicative' if i == big else 'exact',
                                                          permitted=None if i == big else range(marks + 1)))
                        summary = ', '.join(f'{c["label"]} {c["maxMarks"]}' for c in criteria)
                    criteria.append(title_criterion(key, alternatives, titles[0]))
                    assert sum(c['maxMarks'] for c in criteria) == 25, (key, [c['maxMarks'] for c in criteria])
                    note = (f'One complete SEC response: {summary}, {criteria[-1]["label"].lower()} {titles[0]}, then the 0–4 Gaeilge deduction once. '
                            'The optional text is open content chosen by the candidate; its points are judged on merit against these '
                            'allocations (indicative rather than exhaustive).')
                    if len(alternatives) > 1:
                        note += (f' {section.upper()}({option}) prints {len(alternatives)} alternatives keyed alike; one card carries the '
                                 'scheme lines of each.')
                    route.update(schemePage=spages[0], schemePages=spages, criteria=criteria + [deduction()], markingGuideNote=note)
                    stamped.append(route['id'])
                    continue
                if found is None:
                    # No key: the paper's own printed tariffs, each part judged on merit. Units the paper prices:
                    # "Maidir le … (23 marc)", "(i) … (9 marc)", "Ní mór teideal … (2 mharc)". Printed alternatives ("scannán
                    # roghnach nó … dráma roghnach") price the same units: one criterion carries each alternative's words.
                    titles = list(dict.fromkeys((u.strip(), int(m)) for u, m in re.findall(r'(Ní mór teideal[^()]*?\.)\s*\((\d+) m?h?arc\)', text)))
                    if parts:
                        criteria = [criterion(f'eolas-{roman}', f'({roman}) Eolas', marks,
                                              [re.sub(r'\s*\(\d+ m?h?arc\)$', '', prompt.split(' Ní mór teideal')[0]).strip()], 'indicative')
                                    for roman, prompt, marks in parts]
                    else:
                        units = re.findall(r'\s*(.*?)\s*\((\d+) m?h?arc\)', text.split(') ', 1)[1])
                        eolas = [(u, int(m)) for u, m in units if not u.startswith('Ní mór teideal')]
                        assert eolas and len({m for _, m in eolas}) == 1, (key, units)
                        criteria = [criterion('eolas', 'Eolas', eolas[0][1], [u for u, _ in eolas], 'indicative')]
                    if titles:
                        assert len({m for _, m in titles}) == 1, (key, titles)
                        criteria.append(criterion('teideal', 'Teideal + ainm', titles[0][1], [u for u, _ in titles], 'exact', permitted=range(titles[0][1] + 1)))
                    assert sum(c['maxMarks'] for c in criteria) == 25, (key, [c['maxMarks'] for c in criteria])
                    pages = [s.page_at(sections['2a' if prose else '3a'].start())]
                    # The 0-4 deduction applies here only where the scheme prints it for the whole question (2024's
                    # modified-marking page: "Ceist 2: An Prós - … sna freagraí próis [Gaeilge lochtach: 0 - 4 …]"); printed
                    # under the keyed options alone (2025), it is theirs, not this option's (coordinator ruling, 12 Nov).
                    whole = s.find(r'Ceist 2: An Prós - An measúnú a dhéantar ar chaighdeán na Gaeilge sna freagraí próis \[Gaeilge lochtach: 0 ?[-‐] ?4 a bhaint den iomlán a gnóthaíodh\]'
                                   if prose else
                                   r'Ceist 3: An Fhilíocht - An measúnú a dhéantar ar chaighdeán na Gaeilge sna freagraí filíochta \[Gaeilge lochtach: 0 ?[-‐] ?4 a bhaint den iomlán a gnóthaíodh\]')
                    if whole:
                        pages = sorted({*pages, s.page_at(whole.start())})
                        criteria.append(criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [whole.group(0)], 'quality', deduction=True))
                    route.update(schemePage=pages[0], schemePages=pages, criteria=criteria,
                                 markingGuideNote=f'{UNPRINTED} The deferred scheme prints keys for the prescribed texts only; this option is marked at the '
                                                  'paper’s printed tariffs, judged on merit'
                                                  + (f', then the 0–4 Gaeilge deduction the scheme prints for the whole question (scheme PDF {s.page_at(whole.start())}) once.'
                                                     if whole else '. The scheme prints its 0–4 Gaeilge deduction under the keyed options only, so none applies here.'))
                    stamped.append(route['id'])
                    continue
                chunk, spages = found
                pieces = cut(chunk, parts) if parts else [chunk]
                if parts:
                    # A part's tariff as the scheme prints it beside the part; a part of nested questions ("(i) (a) … (2 mharc)
                    # (b) …") is priced on the paper ("(8 marc)") and the scheme prices its questions, which must add up to it.
                    caps = []
                    for (roman, prompt, printed_cap), piece in zip(parts, pieces):
                        nested = printed_parts(prompt, romans=('a', 'b', 'c', 'd'))
                        if len(nested) > 1:
                            sub_caps = [int(x) for x in re.findall(r'\((\d+) m?h?arc\)', piece)]
                            assert printed_cap and sum(sub_caps[:len(nested)]) == printed_cap, (key, roman, printed_cap, sub_caps)
                            caps.append(printed_cap)
                        else:
                            caps.append(tariff_of(piece) or unit_tariff(piece))
                            assert printed_cap in (None, caps[-1]), (key, roman, printed_cap, caps[-1])
                    assert None not in caps and sum(caps) == 25, (key, caps)
                    criteria = [criterion(f'eolas-{roman}', f'({roman}) Eolas', cap, [piece, notes[section]], 'indicative',
                                          permitted=permitted_for(piece, cap) or ([0, 2, 4, 6, 8] if re.search(r'\(i\)\s*\(a\)', piece) and cap == 8 else None))
                                for (roman, _, _), cap, piece in zip(parts, caps, pieces)]
                    note = (f'One complete SEC response: {", ".join(f"({r}) {c}" for (r, _, _), c in zip(parts, caps))} at their printed tariffs, '
                            'then the 0–4 Gaeilge deduction once. The sample answers are indicative rather than exhaustive.')
                else:
                    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk or 'Eolas' in chunk, (key, chunk[:200])
                    criteria = [criterion('eolas', 'Eolas', 25, [chunk, notes[section]], 'indicative')]
                    note = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once. '
                            'The sample points are indicative rather than exhaustive.')
                if texts:
                    note += f' {section.upper()}({option}) offers {texts[0][1]} or {texts[1][1]}; this card is {title}.'
                route.update(schemePage=spages[0], schemePages=spages, criteria=criteria + [deduction()], markingGuideNote=note)
                stamped.append(route['id'])
                if not parts:
                    continue
                # Each printed part its own practice card, and each question nested in a part.
                lead = text.split(' (i) ', 1)[0]
                src = route.get('sourceMaterial') or source(year, level, 2, ref, [route['paperPage']])
                for (roman, prompt, _), cap, piece in zip(parts, caps, pieces):
                    nested = printed_parts(prompt, romans=('a', 'b', 'c', 'd'))
                    one = re.sub(r'\s+(?=\([a-d]\)\s)', '\n', prompt)
                    shown = one if re.search(r'\(\d+ m?h?arc\)$', one) else f'{one} ({cap} marc)'
                    add(part_card(sitting, f'{atlas}-{roman}', f'{key}-{roman}', f'{ref} · ({roman})', heads[section] + '\n' + lead + f'\n({roman}) {shown}',
                                  topic, [route['paperPage']], spages, [criterion('eolas', 'Eolas', cap, [piece, notes[section]], 'indicative',
                                                                                  permitted=criteria[ROMANS.index(roman)]['permittedMarks'])],
                                  requirements[:1] + LIT_OL[1:],
                                  f'One printed sub-question at its published {cap}-mark tariff. Scheme: “{lang}” applies to the whole 25-mark answer, '
                                  'never inside one sub-question.', src, None))
                    if len(nested) > 1:
                        subs = cut(piece, [(n[0], n[1], n[2]) for n in nested])
                        subs[0] = subs[0][subs[0].index('(a)'):] if '(a)' in subs[0] else subs[0]
                        for (letter, sub_prompt, _), sub in zip(nested, subs):
                            sub_cap = tariff_of(sub)
                            assert sub_cap, (key, roman, letter, sub[:80])
                            values = [0, sub_cap] if '2 mharc + 2 mharc' not in sub else [0, 2, sub_cap]
                            asked = re.sub(r'\s*\(\d+ m?h?arc\)$', '', sub_prompt)
                            add(part_card(sitting, f'{atlas}-{roman}-{letter}', f'{key}-{roman}-{letter}', f'{ref} · ({roman})({letter})',
                                          heads[section] + '\n' + lead + f'\n({roman}) ({letter}) {asked}',
                                          topic, [route['paperPage']], spages, [criterion('eolas', 'Freagra', sub_cap, [sub], 'exact', permitted=values)],
                                          requirements[:1] + LIT_OL[1:],
                                          f'One printed {sub_cap}-mark question inside {section.upper()}({option})({roman}). Scheme: “{lang}” applies to the whole 25-mark answer.',
                                          src, None))
    assert len(stamped) >= 12, stamped
    return cards, stamped


# ------------------------------------------------------------------------------------------------- the whole sitting

# The scheme's boxed page headings, stored inside the text it frames. Removed by exact string only (irish_furniture.py's
# rule), with the shared list's own headings.
FURNITURE = ('Ceist 1 LÉAMHTHUISCINT 100 marc Páipéar 2 (200 marc)', 'Ceist 2 PRÓS (30 marc)', 'Ceist 2 PRÓS 30 marc',
             'Ceist 3 FILÍOCHT 30 marc', 'Ceist 4 LITRÍOCHT BHREISE (40 marc)', 'Ceist 4 LITRÍOCHT BHREISE 40 marc',
             'Cuid I An Chluastuiscint 60 marc', 'Cuid II An Cheapadóireacht 100 marc', 'CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc',
             'Ceist 2 Prós Ainmnithe nó Roghnach 50 marc', 'Ceist 3 Filíocht Ainmnithe nó Roghnach 50 marc',
             'Ceist 2 Prós – Ainmnithe nó Roghnach 50 marc', 'Ceist 3 Filíocht – Ainmnithe nó Roghnach 50 marc',
             '2A PRÓS AINMNITHE 50 marc', '3A FILÍOCHT AINMNITHE 50 marc', 'Páipéar II (200 marc)',
             # 2022's and 2023's margin labels, stored inside the key beside them.
             'A – (50 marc)', 'B – (50 marc)', '2B – PRÓS ROGHNACH', 'B PRÓS ROGHNACH', '– FILÍOCHT ROGHNACH –',
             'CEIST 3 FILÍOCHT AINMNITHE nó ROGHNACH A –FILÍOCHT AINMNITHE')


def strip_furniture(card):
    from irish_furniture import HEADINGS
    pattern = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(set(HEADINGS) | set(FURNITURE), key=len, reverse=True)))
    # The examiner's empty total box after the Eolas and Gaeilge boxes ("Gaeilge (5) = C 2 A (a) (30) =", "… = C3B (30) =",
    # "… = 2 A (b) 30 ="), 2022's and 2023's: the boxes are the examiner's form, not marking.
    box = re.compile(r'(Gaeilge \(5\) =)\s*(?:C ?)?\d ?[ABF]?(?: ?[ABF])? ?(?:\([a-f]\) ?)?\(?\d+\)? ?=?(?=\s|$)')
    # The margin label's letter, stored apart from its words ("… = 1 mharc B Dhá shampla …", 2022 Ordinary 3B(a)).
    margin = re.compile(r'(?<=\d mharc) [AB](?= [A-ZÁÉÍÓÚ][a-záéíóú])')
    count = 0
    for c in card['criteria']:
        lines = []
        for line in c['guidance']:
            new, n = pattern.subn(' ', line)
            new, m = box.subn(r'\1', new)
            new, k = margin.subn('', new)
            count += n + m + k
            lines.append(clean(new))
        c['guidance'] = [line for line in lines if line]
    return count


LISTENING_SEGMENT = {'a-f1': 'Fógra A Haon', 'a-f2': 'Fógra A Dó', 'b-c1': 'Comhrá A Haon', 'b-c2': 'Comhrá A Dó',
                     'b-c1-first': 'Comhrá A Haon · An Chéad Mhír', 'b-c1-second': 'Comhrá A Haon · An Dara Mír',
                     'b-c2-first': 'Comhrá A Dó · An Chéad Mhír', 'b-c2-second': 'Comhrá A Dó · An Dara Mír',
                     'c-p1': 'Píosa A Haon', 'c-p2': 'Píosa A Dó'}


def census_address(key):
    """The census address a card covers, from its key ("reading-a-q1-bi" → "Léamhthuiscint · A 1(b)(i)"), and whether
    everything printed under that address is covered (a whole question or option) or that address alone (one part)."""
    m = re.fullmatch(r'listening-([abc]-[fcp]\d(?:-first|-second)?)', key)
    if m:
        return f'Cluastuiscint · {LISTENING_SEGMENT[m.group(1)]} · ', True
    m = re.fullmatch(r'composition-([a-d])-([a-e]|i{1,3})', key)
    if m:
        return f'Ceapadóireacht · {m.group(1).upper()}({m.group(2)})', False
    m = re.fullmatch(r'reading-([ab])-q(\d)(?:-([ab])(i{1,2})?(?:-\d)?)?', key)
    if m:
        letter, q, part, roman = m.groups()
        if not part:
            return f'Léamhthuiscint · {letter.upper()} {q}(', True
        return f'Léamhthuiscint · {letter.upper()} {q}({part})' + (f'({roman})' if roman else ''), False
    m = re.fullmatch(r'(?:prose|poetry)-(\d[ab])-([a-c])(?:-(?:caca-milis|an-lasair-choille))?(?:-(i{1,3}|iv|v))?(?:-([a-d]))?', key)
    if m:
        section, option, roman, letter = m.groups()
        return f'Litríocht · {section.upper()}({option})' + (f'({roman})' if roman else '') + (f'({letter})' if letter else ''), True
    m = re.fullmatch(r'literature-4-([a-f])', key)
    if m:
        return f'Litríocht · 4{m.group(1).upper()}', True
    raise AssertionError(f'no census address for {key}')


def covers(sitting, cards):
    """Each card's census asks (paper_census.census_irish_deferred): the leaves its address names. Every leaf is covered."""
    from paper_census import census_irish_deferred
    leaves = {}
    for paper in census_irish_deferred():
        if paper['year'] == sitting.year and paper['level'] == sitting.ll:
            for leaf in paper['leaves']:
                address = leaf['label'].split(f' Paper {paper["paper"][-1]} ', 1)[1].removesuffix(DEFERRED)
                leaves[(int(paper['paper'][-1]), address)] = leaf['key'][0]
    assert leaves, f'{sitting.year} {sitting.level}: no deferred census (link the deferred papers)'
    out = {}
    for card in cards:
        key = card['id'].split('-deferred-p', 1)[1][2:]
        address, whole = census_address(key)
        found = [leaf for (paper, label), leaf in leaves.items() if paper == card['paper']
                 and (label == address or (whole and (label.startswith(address) and (address.endswith(('(', ' · ')) or label[len(address)] == '('))))]
        assert found, (card['id'], address)
        if key.startswith('listening-'):
            asked = [c for c in card['criteria'] if c['kind'] == 'award']
            assert len(found) == len(asked), (card['id'], len(found), len(asked))
        out[card['id']] = found
    missing = set(leaves.values()) - {leaf for found in out.values() for leaf in found}
    assert not missing, (sitting.year, sitting.level, sorted(missing))
    return out


def deferred_identity(sitting, card):
    """A legacy-built card becomes the deferred sitting's: its id, citation, paper, recording and source titles."""
    m = re.match(r'^irish-\d{4}-(?:hl|ol)-p([12])-(.+)$', card['id'])
    if m:
        card['id'] = sitting.card_id(int(m.group(1)), m.group(2))
    if not card['questionRef'].endswith(DEFERRED):
        card['questionRef'] += DEFERRED
    card['paperFileid'] = fileid(sitting.year, sitting.level, card['paper'])
    card['schemeFileid'] = scheme_fileid(sitting.level)
    if card.get('audioMaterial'):
        card['audioMaterial'] = audio(sitting.year, card['audioMaterial']['label'])
    if card.get('sourceMaterial'):
        card['sourceMaterial'] = dict(card['sourceMaterial'], attribution=ATTRIBUTION)
    for field in ('paperTraceScore', 'schemeTraceScore'):
        card.pop(field, None)
    return card


def build_sitting(year, level):
    sitting = Sitting(year, level)
    with legacy_sources(sitting):
        p1 = legacy.listening_cards(year, level, sitting.pages[1], sitting.pages[0]) + \
            legacy.composition_cards(year, level, sitting.pages[1], sitting.pages[0])
        p2 = legacy.reading_cards(year, level, sitting.pages[2], sitting.pages[0]) + \
            legacy.literature_cards(year, level, sitting.pages[2], sitting.pages[0])
    listening(sitting, p1)
    composition(sitting, p1)
    added, _ = reading(sitting, p2)
    if level == 'higher':
        literature_higher(sitting, p2)
        literature = []
    else:
        literature, _ = literature_ordinary(sitting, p2)
    cards = [deferred_identity(sitting, card) for card in p1 + p2 + added + literature]
    for card in cards:
        assert card.get('reviewedAt') == REVIEWED_AT and card.get('atlasQuestionId'), card['id']
    ids = [c['id'] for c in cards]
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})
    atlas = [(c['paper'], c['atlasQuestionId']) for c in cards]
    assert len(atlas) == len(set(atlas)), sorted({a for a in atlas if atlas.count(a) > 1})
    stripped = sum(strip_furniture(card) for card in cards)
    printed_lead_in(cards)
    scheme_words(cards)
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'], (card['id'], c['id'], 'no scheme words left')
    return sitting, cards, covers(sitting, cards), stripped


def scheme_export(sitting):
    """The deferred scheme's page text, searchable beside June's (irish_cards.scheme_text_exports' form)."""
    chunks = [f'# SEC Gaeilge {LEVEL_IRISH[sitting.level]} marking scheme {sitting.year} (deferred sitting)', '',
              'Extracted page text used for Mark Bank provenance checks.', '']
    for page_no, page in enumerate(sitting.pages[0], 1):
        chunks.extend([f'## Page {page_no}', '', legacy.clean_lines(page, drop_answer_slots=False), ''])
    return '\n'.join(chunks).rstrip() + '\n'


def outputs(year, level):
    sitting, cards, covered, stripped = build_sitting(year, level)
    ll = LEVEL_SHORT[level]
    review = dict(year=year, level=level, sitting='deferred',
                  paperFileids=[fileid(year, level, 1) + '.pdf', fileid(year, level, 2) + '.pdf'], schemeFileid=scheme_fileid(level) + '.pdf',
                  sha256={('paper1' if k == 1 else 'paper2' if k == 2 else 'scheme'): v for k, v in sitting.sha().items()},
                  reviewDate=REVIEWED_AT, audio=AUDIO[year], furnitureStripped=stripped,
                  cardCount=len(cards), censusAsks=len({leaf for found in covered.values() for leaf in found}))
    manifest = json.dumps(dict(review=review, covers=covered, cards=cards), ensure_ascii=False, indent=2) + '\n'
    out = {DECK / f'{level}-{year}-deferred-authored.json': manifest,
           SCHEME_TEXT / f'{year}-{ll}-deferred.md': scheme_export(sitting)}
    # Close this sitting's documents now: PyMuPDF can trap with many documents left open across a full run.
    for doc in sitting.docs.values():
        doc.close()
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('years', nargs='*', type=int)
    args = parser.parse_args()
    stale = []
    for year in args.years or sorted(SITTINGS):
        for level in SITTINGS[year]:
            for path, content in outputs(year, level).items():
                if args.check:
                    if not path.exists() or path.read_text(encoding='utf-8') != content:
                        stale.append(str(path.relative_to(ROOT)))
                else:
                    path.write_text(content, encoding='utf-8')
                    print(f'wrote {path.relative_to(ROOT)}')
    if stale:
        print('Irish deferred outputs are stale; run irish_deferred.py:\n  ' + '\n  '.join(stale), file=sys.stderr)
        return 1
    if args.check:
        print('Irish deferred outputs match')
    return 0


if __name__ == '__main__':
    code = main()
    # PyMuPDF can trap while the interpreter tears down the many documents a full run leaves open (exit 133 after every
    # output is written). Everything is written and flushed by now: leave without the teardown.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)
