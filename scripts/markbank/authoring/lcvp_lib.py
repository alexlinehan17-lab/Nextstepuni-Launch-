#!/usr/bin/env python3
"""LCVP binding of the shared authoring helpers.

The general helpers, and the reasoning behind each guard in them, are in
markbank_authoring.py. This file is what is true of LCVP and nothing else.

THE LEVEL. LCVP's Link Modules is examined at ONE level. The SEC's own file id
says so — LC462CLP000EV.pdf, level letter C — and the canonical curriculum in
curriculum.ts already records `levels: ["common"]` for it. So the token is 'cl'
on disk and the card field is 'common': not 'higher' with a note, which would
have every card cite a Higher Level paper that does not exist.

THE PAIRING (Law 4). The paper and the scheme are NEVER joined on the part key.
The 2021 scheme sets a specimen questionnaire numbered Q.1 to Q.8 inside the
model answer to Section C Q.3(c) and its Section C numbering runs past 7
afterwards; the 2019 scheme prints Section C Q.2(d) under a "Q.6" head. A key
join files both under the wrong question. Parts are paired by wording and
order, the way align.py does it, and a pair with no wording support is
reported rather than shipped.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import pymupdf                                               # noqa: E402
from align import bag, score                                 # noqa: E402
from lcvp_scheme import LcvpScheme                           # noqa: E402
from paper_census import census_lcvp                         # noqa: E402
from markbank_authoring import (  # noqa: F401,E402
    VALID_KINDS, anyN, make_audit, make_card, point, tidy,
)

YEARS = range(2018, 2026)
SECTION_ORDER = {'A': 0, 'B': 1, 'C': 2}
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
# What the deck may show at all, mirroring MAX_LONG_OPTION_ROWS in
# scripts/markbank/optionCap.mjs: past this the build refuses the card. The
# SOFT cap of eight for a short section is reported by the build rather than
# enforced, and it is deliberately not enforced here either — four Section A
# menus print nine to twelve one-line answers ("Flyers", "Email"), and cutting
# the SEC's own list to fit a reading-load proxy makes a correct answer
# impossible to self-mark.
MAX_OPTIONS = {'A': 16, 'B': 16, 'C': 16}
SOFT_OPTIONS = {'A': 8, 'B': 16, 'C': 16}


def order_key(key):
    section, q, letter, roman = key
    return (SECTION_ORDER[section], q, ord(letter) if letter else 0,
            ROMANS.index(roman) + 1 if roman else 0)


def ref(year, key):
    """'2025 CL Section C Q1(a)' — the paper's own address, level letter first.

    'CL' rather than 'HL'/'OL' because that is the level the SEC prints on the
    front of the paper: Common Level. reconcile.py's citation grammar reads it.
    """
    section, q, letter, roman = key
    tail = f'Q{q}'
    if letter:
        tail += f'({letter})'
    if roman:
        tail += f'({roman})'
    return f'{year} CL Section {section} {tail}'


def card_id(year, key, suffix=''):
    section, q, letter, roman = key
    return (f'lcvp-{year}-cl-{section.lower()}{q}{letter or ""}{roman or ""}'
            + (f'-{suffix}' if suffix else ''))


# ------------------------------------------------------------------ paper ---

class LcvpPaper:
    """One sitting's asks, straight out of the paper census walker."""

    def __init__(self, year):
        self.year = year
        parts, texts, files, marks, stems = census_lcvp('lcvp', year, 'cl')
        self.keys = sorted(parts, key=order_key)
        self.texts = texts
        self.files = files
        self.question_marks = marks
        self.stems = stems
        self._doc = None

    def text(self, key):
        return self.texts.get(key, '')

    def is_leaf(self, key):
        section, q, letter, roman = key
        if roman is not None:
            return True
        return not any(k[:2] == key[:2] and k[2:] != key[2:]
                       and (letter is None or k[2] == letter)
                       and (k[2] is not None or k[3] is not None)
                       for k in self.keys)

    def leaves(self):
        return [k for k in self.keys if self.is_leaf(k)]

    # The tariff the paper prints beside a part, e.g. "(6 marks)" after
    # Section C's (b). Taken ONLY where the paper prints it against the part
    # itself: Sections A and B price the whole question, and their last roman
    # simply happens to be the line the question's total lands on — reading
    # that as the roman's own tariff would price 2025's Section B Q2(iii) at
    # the twelve marks all three romans share.
    def part_marks(self, key):
        section, q, letter, roman = key
        if section != 'C' and (letter or roman):
            return None
        if section == 'C' and roman and letter:
            return None
        m = re.search(r'\(?\s*(\d{1,3})\s*marks?\s*\)?\s*$',
                      self.text(key).strip())
        return int(m.group(1)) if m else None

    def stem(self, key):
        """The lead-in the paper prints above this part, if any.

        Two levels, both needed and both the paper's own words. Section C sets
        a one-line scenario over each question — "Consider your local area." —
        without which (a)-(d) cannot be answered; and a lettered part may set
        its own material under that, which in 2024 is the Central Bank's
        forecast table, the one piece of printed matter in eight papers that a
        card must carry to be answerable.
        """
        section, q, letter, _roman = key
        parts = [self.stems.get((section, q, None), '')]
        if letter is not None:
            parts.append(self.stems.get((section, q, letter), ''))
        return _drop_marks(' '.join(p for p in parts if p))

    def pages(self):
        if self._doc is None:
            self._doc = pymupdf.open(self.files[0])
        return self._doc

    def av_theme(self):
        """The paper's own sentence naming what the Section A DVD showed.

        Section A marks a video the card cannot show, so the card says which
        video — in the paper's words, off its own instruction page.
        """
        doc = self.pages()
        for n in range(min(6, doc.page_count)):
            text = ' '.join(doc[n].get_text().split())
            m = re.search(r'You will be shown a DVD[^.]*\.', text)
            if m:
                return tidy(m.group(0))
        return ''

    def case_study_pages(self):
        """The one-based PDF pages carrying the Section B case study.

        Read off the pages themselves: from the page that heads "Section B
        Case Study" to the page before the one that opens "Answer all three
        questions."
        """
        doc = self.pages()
        start = end = None
        for n in range(doc.page_count):
            text = ' '.join(doc[n].get_text().split())
            if start is None and re.search(r'Section B\s+Case Study', text):
                start = n + 1
            elif start is not None and 'Answer all three questions' in text:
                end = n + 1
                break
        if start is None:
            return []
        last = (end - 1) if end and end - 1 >= start else start
        return list(range(start, last + 1))


def _drop_marks(text):
    text = re.sub(r'\(?\s*\d{1,3}\s*marks?\s*\)?', ' ', text or '')
    # The stripped tariff can leave its own bracket behind — the paper prints
    # "Q.1 (25 marks) Enterprise is essential..." and the census head reader
    # has already eaten "(25 marks", so a lone ")" opened the stem.
    return tidy(re.sub(r'^\s*[)\]]\s*', '', text))


# ----------------------------------------------------------------- pairing --

def pair(year, floor=0.30):
    """{scheme part index: (paper key, score)} by wording AND order.

    Needleman-Wunsch over the two documents in their own order, scored on
    shared content words, exactly as align.align_ordered does it — a pairing
    can never cross another, so one misread cannot slide the rest out of step
    the way a key join does. Pairs below `floor` are returned separately: they
    rest on position alone and are read, not shipped.
    """
    P = LcvpPaper(year)
    S = LcvpScheme(year)
    sparts = S.answering()
    pkeys = P.keys
    sbags = [bag(p.cue or ' '.join(p.points[:2])) for p in sparts]
    pbags = [bag(P.text(k)) for k in pkeys]

    n, m = len(sparts), len(pkeys)
    GAP = -0.10
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = best[i - 1][j - 1] + score(sbags[i - 1], pbags[j - 1])
            up, left = best[i - 1][j] + GAP, best[i][j - 1] + GAP
            cell = max(diag, up, left)
            best[i][j] = cell
            back[i][j] = 'diag' if cell == diag else ('up' if cell == up else 'left')

    pairs, positional = {}, {}
    i, j = n, m
    while i > 0 and j > 0:
        step = back[i][j]
        if step == 'diag':
            s = round(score(sbags[i - 1], pbags[j - 1]), 2)
            key = pkeys[j - 1]
            # The scheme's own numbering is not a key (see the module note),
            # but it is EVIDENCE. Where it names a different question from the
            # one the wording picked, the wording has to be strong to overrule
            # it: 2018's "Good managerial skills:" shares the single word
            # "skills" with a career question two parts later, which scores
            # 0.33 on a three-word heading and stole the pairing — and with it
            # both cards. A pairing that agrees on the question needs no such
            # corroboration.
            printed = sparts[i - 1].address[:2]
            # A one-word ask scores 1.0 against anything that repeats the
            # word: 2018's Section B Q1(i) is the single term "Volunteer", and
            # the answers to Q2(i), "Influences on where to volunteer", scored
            # a perfect match on it and shipped as that term's definition. Too
            # little text to identify a part is not evidence — align.py makes
            # the same argument with its min_cue.
            evidence = min(len(sbags[i - 1]), len(pbags[j - 1]))
            weak = printed != key[:2] and (s < 0.55 or evidence < 3)
            (positional if (s < floor or weak) else pairs)[i - 1] = (key, s)
            i, j = i - 1, j - 1
        elif step == 'up':
            i -= 1
        else:
            j -= 1
    return P, S, sparts, pairs, positional


# -------------------------------------------------------------- provenance --

SUP = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6',
       '⁷': '7', '⁸': '8', '⁹': '9'}


def normalise(text):
    """Mirrors normalise() in scripts/markbank/schemeText.mjs."""
    text = ''.join(SUP.get(c, c) for c in text)
    text = re.sub(r'[‐-―]', '-', text)
    return re.sub(r'[^a-z0-9]+', '', text.lower())


_scheme_text = {}


def comparable(year):
    """The scheme reduced the way the build's provenance gate reduces it."""
    if year not in _scheme_text:
        from lcvp_scheme import _lines
        _scheme_text[year] = normalise(' '.join(_lines(year)))
    return _scheme_text[year]


def traces(year, claim):
    return normalise(claim) in comparable(year)


def slice_after(haystack, needle):
    """The text of `haystack` that follows `needle`, compared the gate's way.

    Both sides are reduced with normalise() before the search, so a line break,
    a curly apostrophe or a double space between the two documents cannot stop
    the scheme's restatement of an ask being found in it. The offset is mapped
    back to the ORIGINAL characters, so what comes back is the SEC's own text,
    untouched — which is what the provenance gate will look for.
    """
    keep, index = [], []
    for i, ch in enumerate(haystack):
        reduced = normalise(ch)
        if reduced:
            keep.append(reduced)
            index.append(i)
    flat = ''.join(keep)
    target = normalise(needle)
    if not target:
        return None
    at = flat.find(target)
    if at < 0:
        # The scheme rarely restates an ask word for word — "Name two Trade
        # Unions." is answered under "Name any two trade unions eg: ...". Its
        # TAIL is what survives, so shorter and shorter tails are tried, never
        # below twelve characters of evidence.
        words = needle.split()
        for take in range(min(8, len(words)), 1, -1):
            target = normalise(' '.join(words[-take:]))
            if len(target) < 12:
                break
            at = flat.find(target)
            if at >= 0:
                break
        if at < 0:
            return None
    end = at + len(target)
    if end >= len(index):
        return ''
    return haystack[index[end]:]


# ----------------------------------------------------------------- cards ----

_card = make_card('lcvp', default_section='A')


def card(cid, year, key, topic, concept, qtext, notation, total, rows, notes,
         stem='', tariff_kind='bestNofParts', answer=None, of_parts=None,
         per_part=None, source_material=None):
    c = _card(cid, year, 'common', topic, concept, ref(year, key), qtext,
              notation, total, rows, notes, stem=stem, tariff_kind=tariff_kind,
              answer=answer, of_parts=of_parts, per_part=per_part,
              section=key[0])
    if source_material:
        c['sourceMaterial'] = source_material
    return c


def audit_for(section):
    return make_audit(MAX_OPTIONS[section])
