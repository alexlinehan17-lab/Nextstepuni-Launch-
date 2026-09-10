#!/usr/bin/env python3
"""Modern Greek question papers — the printed ask, its tariff, its passage.

    python3 scripts/markbank/authoring/mgr_paper.py 2024 hl
    python3 scripts/markbank/authoring/mgr_paper.py 2021 hl --json

Modern Greek is a NON-CURRICULAR EU language, SEC subject 019, and it is the
simplest paper in the bank. One booklet, ONE level (the SEC's file letter is
'A' and every cover says Higher Level — there is no Ordinary paper in any year
on disk), no Listening Comprehension Test, and no second language: the paper is
printed entirely in Greek and states on its own rubric that the answers are too
— "Οι απαντήσεις να δοθούν στα νέα Ελληνικά". That sentence is the
answer-language rule the six curricular languages make you read per ask; here
it is one line and it rides on every card.

The shape, in the paper's own words
-----------------------------------
One passage, then three numbered GROUPS::

    ΟΜΑΔΑ 1η  ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ            [30 / 100]
        1.  five words or phrases to explain          (5 × 1)
        2. … 6.  one question each                       (5)
    ΟΜΑΔΑ 2η  ΣΧΟΛΙΑΣΜΟΣ                          [30 / 100]
        one phrase to comment on in 100 words
    ΟΜΑΔΑ 3η  ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ                      [40 / 100]
        1ο θέμα / 2ο θέμα — 300 words on one of two

Two sittings depart from it, and both are the SEC's own reduction:

  * **2021** prints "Μέρος πρώτο" and "Μέρος δεύτερο" instead of the three
    groups, and sets no commentary at all — comprehension (30) and essay (40),
    seventy marks. Its parts are keyed 'I' and 'II', which is what Polish's
    2021 paper is keyed for the same reason.
  * **2022** keeps the ΟΜΑΔΑ heads but prints only two of them, the second
    being the essay: "[30 / 70]" and "[40 / 70]".

The trap this reader exists for
-------------------------------
**The passage is set in NUMBERED PARAGRAPHS.** 2013 runs "1." to "9." down two
pages of prose before a single question is asked, and those numbers are printed
exactly like the question numbers that follow. Nothing in the line itself tells
them apart. What does is the page furniture: the questions open after the LAST
of "ΕΡΩΤΗΣΕΙΣ", "ΟΜΑΔΑ 1η" and "Μέρος πρώτο" the booklet prints — last,
because 2016 heads the PASSAGE "ΟΜΑΔΑ 1η" and then heads the questions
"ΕΡΩΤΗΣΕΙΣ", and 2010 prints "ΟΜΑΔΑ 1η" over each of them.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from markbank_text import unligature                          # noqa: E402

SUBJECT = 'modern-greek'
LETTERS = 'abcdefgh'
ROW_BAND = 6
ROW = '\x00'

FURNITURE = re.compile(
    r'^Leaving\s+Certi[fi]+cate(?:\s+Examination)?\b'
    r'|^Modern\s+Greek\s*[–—\-‐]\s*(?:Higher|Ordinary)\s+[Ll]evel'
    r'|^Coimisi[úu]n\s+na\s+Scr[úu]duithe|^State Examinations Commission'
    r'|^\d{4}\s*\.?\s*M\s*\.?\s*\d|^\d{4}L\d{3}[A-Z0-9]+\s*$'
    r'|^LEAVING\s+CERTIFICATE|^MODERN\s+GREEK|^HIGHER\s+LEVEL'
    r'|^Duration|^Monday|^Tuesday|^Wednesday|^Thursday|^Friday'
    r'|^\s*\d{1,3}\s*$', re.I)

# Where the questions start: the LAST of these the booklet prints.
QUESTIONS_OPEN = re.compile(
    r'^ΕΡΩΤΗΣΕΙΣ\b|^ΟΜΑΔΑ\s*1|^Μέρος\s+πρώτο\b|^ΜΕΡΟΣ\s+ΠΡΩΤΟ\b')
# The group heads, and the token each is keyed by. 'I'/'II' for 2021's two
# parts, the printed digit for the ΟΜΑΔΑ years.
# "ΟΜΑΔΑ 1η" — the ordinal ending belongs to the head, not to what follows it.
# Left on, the SCHEME's one-row head "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ" opened its
# commentary block with a stray "η" and the block stopped matching the paper's.
GROUP = re.compile(r'^ΟΜΑΔΑ\s*(\d)\s*[ηα]?\b\s*')
PART = re.compile(r'^Μέρος\s+(πρώτο|δεύτερο)\b|^ΜΕΡΟΣ\s+(ΠΡΩΤΟ|ΔΕΥΤΕΡΟ)\b')
PART_TOKEN = {'πρώτο': 'I', 'δεύτερο': 'II',
              'ΠΡΩΤΟ': 'I', 'ΔΕΥΤΕΡΟ': 'II'}

# A question number opening a printed line: "1.", "2)", "1 .", "3.Τι είναι".
QNUM = re.compile(r'^(\d{1,2})\s*[.)]\s*')
# An essay theme: "1ο θέμα:", "2ο θέμα:".
# "1ο θέμα:", and 2012's "2οθέμα:" with no space in it.
THEME = re.compile(r'^(\d)ο\s*θέμα\s*:?')
# One of the five items under Question 1 — bulleted in most sittings and
# lettered a) to e) in 2025 and 2026.
BULLET = re.compile(r'^[•●•\-–]\s*')
ITEM_LETTER = re.compile(r'^([a-e])\s*[).]\s*')

# "(5)", "(5 βαθμοί)", "(5 × 1)", "(5×1)", "[30 / 100]", "(30 μονάδες)",
# "(βαθμολογία 30 βαθμοί)", "(συνολική βαθμολογία 30 βαθμοί , 6 Χ 5 )".
TARIFF = re.compile(r'\(\s*(\d{1,3})\s*(?:βαθμο[ίύ]|μονάδες)?\s*\)')
# "(5 × 1)" on Question 1, and "6 Χ 5" inside the group head 2011 prints:
# "(συνολική βαθμολογία 30 βαθμοί , 6 Χ 5)". The second is the ONLY price that
# sitting states for its six comprehension questions, and without it all six
# were unpriced on a paper the SEC prices in full.
RATE = re.compile(r'\(\s*(\d)\s*[×xΧ]\s*(\d{1,3})\s*\)')
GROUP_RATE = re.compile(r'(\d{1,2})\s*[×xΧ]\s*(\d{1,3})')
# A group's own total, in every spelling the corpus prints: "[30 / 100]",
# "(30/100)", "(30 μονάδες)", "(βαθμολογία 30 βαθμοί)" and
# "(συνολική βαθμολογία 30 βαθμοί , 6 Χ 5)". Only ever read off a group HEAD,
# which is what keeps it apart from an ask's own "(5 βαθμοί)".
TOTAL = re.compile(r'[\[(]\s*(?:συνολική\s+)?(?:βαθμολογία\s+)?(\d{1,3})'
                   r'\s*(?:βαθμο[ίύ]|μονάδες)?\s*'
                   r'(?:/\s*(\d{1,3})\s*)?[,)\]]')


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, subject=SUBJECT):
    path = os.path.join(papers_dir(subject), f'{year}-{level}-paper.pdf')
    if not os.path.exists(path):
        raise FileNotFoundError(f'no {subject} paper for {year} {level}')
    return path


def sittings(subject=SUBJECT):
    out = []
    for name in sorted(os.listdir(papers_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)-paper\.pdf$', name)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def _clean(text):
    text = unligature(' '.join(str(text).replace(ROW, ' ').split()))
    return text.replace('‐', '-').replace('‑', '-').strip()


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'stem', 'marks',
                 'page', 'kind', 'items', 'raw')

    def __init__(self, section, q, letter, text, stem, marks, page, kind):
        self.section, self.q, self.letter, self.roman = section, q, letter, None
        self.text, self.stem, self.marks, self.page = text, stem, marks, page
        # The five words Question 1 sets, in printed order. They are the ask's
        # answer list, not parts of it — see _question.
        self.items = []
        # Every printed row of this ask, joined. The SCHEME reprints the
        # paper's question verbatim and sets the answer under it, so the
        # scheme's raw block minus the paper's own text IS the answer — which
        # is how mgr_scheme pairs the two documents without scoring wording.
        self.raw = ''
        # 'reading' for the comprehension group, 'commentary' for ΣΧΟΛΙΑΣΜΟΣ,
        # 'essay' for ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ. Read off the group's printed head, which
        # is what decides whether the ask is written production.
        self.kind = kind

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return f'<Ask {self.key} {self.marks}m {self.text[:44]!r}>'


class MgrPaper:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, subject)
        self._doc = pymupdf.open(self.path)
        self._runs = None
        self._asks = None
        self.section_marks = {}
        self.passage = ''
        self.passage_pages = []
        self.answer_language = None
        self.flags = []

    def _stream(self):
        if self._runs is not None:
            return self._runs
        runs = []
        for pno in range(len(self._doc)):
            page = self._doc[pno]
            lines = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = ''.join(s['text'] for s in line['spans'])
                    if not text.strip():
                        continue
                    x0, y0, _, y1 = line['bbox']
                    lines.append(((y0 + y1) / 2, x0, text))
            rows, anchor = [], None
            for y, x, text in sorted(lines):
                if anchor is None or y - anchor > ROW_BAND:
                    rows.append([])
                    anchor = y
                rows[-1].append((x, text))
            for row in rows:
                text = _clean(' '.join(t for _, t in sorted(row)))
                if text and not FURNITURE.match(text):
                    runs.append((pno + 1, text))
        self._runs = runs
        return runs

    def cover_marks(self):
        """The total the paper states — "Μέγιστη δυνατή βαθμολογία 100 Βαθμοί",
        or the denominator of the "[30 / 100]" it prints on every group."""
        text = ' '.join(t for _, t in self._stream())
        m = re.search(r'βαθμολογία\s+(\d{2,3})\s*Βαθμο', text, re.I)
        if m:
            return int(m.group(1))
        m = re.search(r'[\[(]\s*\d{1,3}\s*/\s*(\d{2,3})\s*[\])]', text)
        return int(m.group(1)) if m else None

    def asks(self):
        if self._asks is None:
            self._asks = self._walk()
        return self._asks

    def _walk(self):
        rows = self._stream()
        start = 0
        for i, (_pg, text) in enumerate(rows):
            if QUESTIONS_OPEN.match(text):
                start = i
        # Everything before the questions is the passage: the title, the
        # article and its source line. It is the stimulus every comprehension
        # ask depends on and it rides on the card.
        head = list(rows[:start])
        self.passage = '\n'.join(t for _, t in head)
        self.passage_pages = sorted({pg for pg, _ in head})
        for _pg, text in rows[:start] + rows[start:start + 4]:
            if 'απαντήσεις' in text and 'Ελληνικά' in text:
                self.answer_language = _clean(text)

        asks = []
        # A group is read in two phases: its HEAD — the title, the marks it
        # states and any rubric — runs until the first numbered ask, and
        # everything after belongs to a part. A group that never reaches a
        # numbered ask sets exactly one, and its head IS that ask: that is the
        # commentary, which the SEC prints with no number of its own.
        groups = []                   # [(section, [(page, text)] rows)]
        for pg, text in rows[start:]:
            m = GROUP.match(text)
            if m:
                # The head row carries the group's title and its total —
                # "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ (βαθμολογία 30 βαθμοί)" in 2011, the
                # title on the row BELOW in 2014 — so the remainder of the row
                # opens the group's own head block rather than being dropped.
                groups.append((m.group(1), [(pg, text[m.end():].strip())]))
                continue
            m = PART.match(text)
            if m:
                groups.append((PART_TOKEN[m.group(1) or m.group(2)],
                               [(pg, text[m.end():].strip())]))
                continue
            if not groups:
                # 2016 heads its PASSAGE "ΟΜΑΔΑ 1η" and its questions
                # "ΕΡΩΤΗΣΕΙΣ", so the comprehension group has no head of its
                # own after the cut. The questions are still Group 1 — the
                # paper's own rubric says "answer all 3 groups" — and read
                # without this the whole of that sitting's comprehension was
                # dropped: three asks censused where the paper sets thirteen.
                groups.append(('1', []))
            groups[-1][1].append((pg, text))
        for section, body in groups:
            asks += self._group(section, body)
        return asks

    def _group(self, section, body):
        """One printed group -> its asks."""
        cuts = []
        for i, (pg, text) in enumerate(body):
            m = THEME.match(text)
            if m:
                cuts.append((i, int(m.group(1)), m.end()))
                continue
            m = QNUM.match(text)
            if m:
                # The run opens at 1 — or at 2, because the 2018 SCHEME prints
                # Question 1's instruction and its five bullets with no number
                # at all and starts numbering at "2.". Requiring 1 threw that
                # whole comprehension away and reported six missing asks.
                want = (cuts[-1][1] + 1) if cuts else 1
                if int(m.group(1)) == want or (not cuts
                                               and int(m.group(1)) == 2):
                    cuts.append((i, int(m.group(1)), m.end()))
        head_rows = body[:cuts[0][0]] if cuts else body
        if cuts and cuts[0][1] == 2 and len(head_rows) > 1:
            # …and where it does, the head after the group's title IS
            # question 1.
            cuts.insert(0, (1, 1, 0))
            head_rows = body[:1]
        head = _clean(' '.join(t for _, t in head_rows))
        kind = self._kind(head) or 'reading'
        total = self._read_total(section, head)
        rate = GROUP_RATE.search(head)
        per = int(rate.group(2)) if rate else None
        if total:
            # Only the ONE span the group's own total occupies. Substituting
            # every TOTAL match took "(5 βαθμοί)" off 2017's head as well —
            # and that head is where that sitting sets Question 1's price,
            # because it prints the instruction above the number.
            head = _clean(head[:total.start()] + ' ' + head[total.end():])
        head = _clean(re.sub(
            r'^(?:ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ|ΣΧΟΛΙΑΣΜΟΣ|ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ'
            r'|ΕΚΘΕΣΗ[- ]ΔΟΚΙΜΙΟ|ΔΟΚΙΜΙΟ)\s*', '', head))
        if not cuts:
            # A group with no numbered ask sets exactly one — the commentary —
            # and prices it on its own head: "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ [30 / 100]".
            text, marks = self._split_marks(head)
            page = head_rows[0][0] if head_rows else 1
            marks = marks if marks is not None else self.section_marks.get(
                section)
            ask = Ask(section, None, None, text, '', marks, page, kind)
            ask.raw = _clean(' '.join(t for _, t in head_rows))
            return [ask] if text else []
        out = []
        for n, (i, q, off) in enumerate(cuts):
            stop = cuts[n + 1][0] if n + 1 < len(cuts) else len(body)
            rows = [(body[i][0], body[i][1][off:])] + body[i + 1:stop]
            out += self._question(section, q, rows, head, kind, per)
        return out

    def _question(self, section, q, rows, head, kind, per=None):
        """One numbered ask, and the five items Question 1 sets beneath it."""
        items, main = [], []
        for pg, text in rows:
            m = ITEM_LETTER.match(text)
            if m and kind == 'reading':
                items.append((pg, text[m.end():]))
                continue
            if BULLET.match(text) and kind == 'reading':
                items.append((pg, BULLET.sub('', text)))
                continue
            (items if items else main).append((pg, text))
        stem, marks = self._split_marks(' '.join(t for _, t in main))
        if not stem and head:
            # 2017 sets Question 1's instruction ABOVE its number: the group
            # head reads "…Να εξηγήσετε … (5 βαθμοί)" and the row that follows
            # is a bare "1." with the five words under it. Read strictly, that
            # ask had no text and no tariff at all.
            stem, hm = self._split_marks(head)
            marks = marks if marks is not None else hm
        if marks is None:
            marks = per
        if marks is None and kind == 'essay':
            # The essay's two themes are ALTERNATIVES under one printed total:
            # "ΟΜΑΔΑ 3η ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100] … choose one of the two."
            # Each is worth the forty the group states, and neither is priced
            # on its own line.
            marks = self.section_marks.get(section)
        page = rows[0][0] if rows else 1
        ask = Ask(section, q, None, stem, head, marks, page, kind)
        ask.raw = _clean(' '.join(t for _, t in rows))
        if not items:
            return [ask]
        # Question 1's five words are the ANSWER LIST of one ask, not five
        # asks. The SEC prices the question and never the word — "(5 × 1)" in
        # the recent sittings, "(5 βαθμοί)" in the older ones, and in 2018 and
        # 2019 that price is set hard right beside the last bullet rather than
        # on the instruction. Split into five leaves, four of them carried no
        # printed tariff at all and the fifth carried the question's; kept
        # whole, the ask is priced exactly as the paper prices it and the five
        # words become the card's five rows.
        joined = ' '.join(t for _, t in rows)
        rate = RATE.search(joined)
        if rate and ask.marks is None:
            ask.marks = int(rate.group(1)) * int(rate.group(2))
        if ask.marks is None:
            _text, own = self._split_marks(joined)
            ask.marks = own
        ask.items = [_clean(RATE.sub(' ', TARIFF.sub(' ', t)))
                     for _, t in items]
        ask.items = [t for t in ask.items if t]
        return [ask]

    def _read_total(self, section, text):
        m = TOTAL.search(text)
        if m:
            self.section_marks[section] = int(m.group(1))
        return m

    @staticmethod
    def _kind(head):
        # Accent-folded, because 2021 heads its second part in lower case with
        # its accents on — "Να γράψετε ένα δοκίμιο" — and a plain .upper()
        # leaves ΔΟΚΊΜΙΟ, which no ASCII-shaped test matches. Read as
        # comprehension, that sitting's two essay topics were censused as
        # reading asks and priced from the wrong group.
        low = ''.join(c for c in unicodedata.normalize('NFD', head.upper())
                      if not unicodedata.combining(c))
        if 'ΣΧΟΛΙΑΣΜ' in low:
            return 'commentary'
        if 'ΕΚΘΕΣΗ' in low or 'ΔΟΚΙΜΙΟ' in low:
            return 'essay'
        if 'ΚΑΤΑΝΟΗΣΗ' in low or 'ΕΡΜΗΝΕΙΑ' in low:
            return 'reading'
        return None

    @staticmethod
    def _split_marks(text):
        text = _clean(text)
        rate = RATE.search(text)
        if rate:
            return _clean(RATE.sub(' ', text)), \
                int(rate.group(1)) * int(rate.group(2))
        found = list(TARIFF.finditer(text))
        if not found:
            return text, None
        m = found[-1]
        return _clean(text[:m.start()] + ' ' + text[m.end():]), \
            int(m.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', nargs='?', default='hl')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    P = MgrPaper(args.year, args.level)
    asks = P.asks()
    if args.json:
        json.dump([{'key': list(a.key), 'marks': a.marks, 'kind': a.kind,
                    'text': a.text, 'stem': a.stem, 'page': a.page}
                   for a in asks], sys.stdout, ensure_ascii=False, indent=1)
        return 0
    print(f'{args.year} {args.level}: {len(asks)} asks, cover '
          f'{P.cover_marks()}, sections {P.section_marks}, '
          f'passage {len(P.passage)} chars on {P.passage_pages}')
    print(f'  answers: {P.answer_language}')
    for a in asks:
        print(f'  {str(a.key):22} {str(a.marks or "-"):>3} {a.kind:11} '
              f'{a.text[:70]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
