#!/usr/bin/env python3
"""Classical Studies question papers — the printed ask, and its printed tariff.

    python3 scripts/markbank/authoring/cl_paper.py 2024 hl
    python3 scripts/markbank/authoring/cl_paper.py 2021 ol --json

Why this subject needs its own reader
-------------------------------------
**It is TWO papers under one subject slug.** The syllabus changed for 2023, and
the corpus straddles the break:

  * 2021 and 2022 print TEN TOPICS. A topic sets four questions numbered
    "(i)" to "(iv)", each subdivided "(a)"/"(b)"/"(c)", and a candidate answers
    four questions in total — one from each of three groups, plus a free
    choice. There is no Section A, no "Question 1", and nothing the generic
    merged or sections walker can key on: the address of an ask is the topic,
    the roman and the letter, and the topic is not a section header the shared
    SECTION regex would ever see.
  * 2023-2025 print Section A (Questions 1-10, all answered, stimulus
    questions built on images and passages) and Section B (Question 11
    compulsory, one of Questions 12-16 chosen). The numbering runs ON across
    the two sections — Section B opens at Question 11 — so the section is NOT
    part of an ask's address and the citation names the question alone.

**Every marker is glued into one block.** pymupdf reads a whole topic, its four
roman-numbered questions and their lettered parts as a SINGLE text block:

    (i) (a) Give an account of the Battle of Mantinea in 418 BC. (40) (b) How
    did the Spartan victory at Mantinea change the situation in the
    Peloponnese? (10) (ii) ...

so the markers are cut out of a joined text stream rather than read off block
boundaries. The tariff is printed bare in parentheses — "(40)" — at the end of
the ask it prices, and is read the same way.

**The images are on a second booklet.** Both eras set questions on photographs
and drawings printed on an accompanying "Paper X" (SEC component 004), which
carries no questions of its own. It is not walked for asks; it is where the
figures come from.
"""
import argparse
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'classical-studies'
# The syllabus break. 2021 and 2022 are the ten-topic paper; 2023 onwards is
# the Section A / Section B paper.
TOPIC_ERA = (2021, 2022)

ROMANS = ['i', 'ii', 'iii', 'iv', 'v']
LETTERS = 'abcdef'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_paths(year, level, subject=SUBJECT):
    """(question booklet, Paper X or None) for one sitting.

    The fetcher drops the component token when a sitting holds one file, which
    2024 Ordinary does — its Paper X is not in the corpus — so both spellings
    are looked for and the absence of Paper X is returned, never guessed at.
    """
    root = papers_dir(subject)
    main = None
    figures = None
    for name in sorted(os.listdir(root)):
        m = re.match(r'^(\d{4})-(hl|ol)(?:-([0-9A-Za-z]{3}))?-paper\.pdf$', name)
        if not m or int(m.group(1)) != year or m.group(2) != level:
            continue
        comp = m.group(3)
        if comp == '004':
            figures = os.path.join(root, name)
        else:
            main = os.path.join(root, name)
    return main, figures


# Furniture: printed on the page but never part of an ask.
FURNITURE = re.compile(
    r'Leaving Certificate Examination \d{4}|Classical Studies\s*[–-]\s*'
    r'(?:Higher|Ordinary) Level|^\s*\d{1,2}\s*$|This answer box continues'
    r'|Do not write on this page|Optional Planning Space|Optional Space for'
    r' Diagram|Answer Space for optional|Answer for Question'
    r'|Section B\s*[–-]\s*Extended Answers\s*[–-]\s*begins on page'
    r'|^GROUP [IV]+: Topics', re.I)

# "(25,25)" prices a "write notes on any TWO of the following" question, whose
# two chosen notes are marked separately. It is one printed tariff for one
# printed ask, so it is read as its sum — not averaged, and not dropped, which
# left three Ordinary questions unpriced in each of 2021 and 2022.
TARIFF = re.compile(r'\((\d{1,3})(?:\s*,\s*(\d{1,3}))?\s*(?:marks)?\)', re.I)
MARK_TOKEN = re.compile(r'\s*\((\d{1,3})(?:\s*marks)?\)\s*', re.I)


# The old paper sets its tariff hard right, in its OWN block, on the same
# printed line as the ask it prices — and the two blocks' tops differ by a
# point or so. Sorting on the raw top put "(10)" a line ABOVE the "(b)" it
# belonged to on 2021 Higher page 8, which handed the tariff to part (a) and
# left (b) unpriced. Rounding the top to the nearest band puts the two blocks
# on one row, where x then orders them left column first.
ROW_BAND = 6


def _page_text(page):
    """One page, blocks in reading order, furniture dropped."""
    out = []
    for b in sorted(page.get_text('blocks'),
                    key=lambda b: (int(b[1] / ROW_BAND), b[0])):
        text = ' '.join(b[4].split())
        if not text or FURNITURE.search(text):
            continue
        out.append(text)
    return out


# Subset fonts on one 2025 page render "ti" as a single glyph and the "ff"
# family as ligatures. Folding them is reversible and lossless — never a
# rewrite of what the SEC set. (Digits are NOT folded: foldDigits once cost a
# Chemistry card its subscripts.)
LIGATURES = {'\u019f': 'ti', '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl',
             '\ufb03': 'ffi', '\ufb04': 'ffl', '\uf0b7': '\u2022',
             '\uf0fc': ' ', '\uf0e0': ' '}


def unligature(text):
    for bad, good in LIGATURES.items():
        text = text.replace(bad, good)
    return text


# The sentence a new-syllabus question prints to say how its parts are to be
# answered. It carries "(a)", "(b)" and "(i)" tokens that are NOT part markers,
# and splitting on them invented a duplicate ask under every subdivided
# question in Section B.
RUBRIC = re.compile(
    r'\bAnswer\s+(?:part\s+\((?:i|ii)\)\s+(?:and|or)\s+part\s+\((?:i|ii)\)'
    r'|either\s+\([a-f]\)\s+or\s+\([a-f]\)'
    r'|\([a-f]\)\s+(?:and|or)\s+\([a-f]\)'
    r'|one of the following questions'
    r'|one of the five questions below)\.?', re.I)

# A question that refers back to a part it has already set — "how one term
# from part (a) contributed", "Why is the military event named in part (b)
# considered a key moment" — prints the SAME token a part marker uses. Split
# on it and the sentence is cut in half and its tail filed under a part that
# was set three lines earlier: 2024 Higher Q1(b) and 2023 Ordinary Q4(d) both
# lost their second half that way. A marker preceded by "part"/"parts" is a
# cross-reference, never a new part.
BACKREF = r'(?<!\bpart )(?<!\bparts )(?<!\bPart )'


def _clean(text):
    text = unligature(' '.join(text.split()))
    text = FURNITURE.sub(' ', text)
    # The next section's own banner sits at the foot of the page the last
    # Section A question ends on, and joined onto that question's ask.
    text = re.split(r'\bSection [AB]\s+(?:Extended Answers|Stimulus Questions)',
                    text)[0]
    text = re.sub(r'\s+OR\s*$', '', ' '.join(text.split()))
    # The paper rules a run of underscores under an answer line and between
    # topics; that is the ruled line, not the ask. The ask's own full stop
    # STAYS — stripping it left every question text ending mid-sentence.
    text = re.sub(r'[_\s]+$', '', ' '.join(text.split()))
    return text.strip()


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'stem', 'marks',
                 'page', 'inherited')

    def __init__(self, section, q, letter, roman, text, stem, marks, page,
                 inherited=False):
        self.section, self.q, self.letter, self.roman = section, q, letter, roman
        self.text, self.stem, self.marks, self.page = text, stem, marks, page
        # True when the tariff was not printed on this ask but on the LETTER
        # above it. Question 11(b) prints "(80 marks)" once over three options
        # a candidate chooses between, so each option is worth 80; Question
        # 11(a) prints "(40 marks)" once over two parts that are BOTH
        # answered, and the scheme splits it 25 and 15. An inherited tariff is
        # therefore a ceiling, not a price, and is never checked against the
        # scheme's own.
        self.inherited = inherited

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    @property
    def band(self):
        """Which half of the new paper this ask belongs to, for reports."""
        if self.q is None:
            return 'topic'
        return 'A' if self.q <= 10 else 'B'

    def __repr__(self):
        return f'<Ask {self.key} {self.marks}m {self.text[:50]!r}>'


class ClPaper:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path, self.figures_path = paper_paths(year, level, subject)
        if self.path is None:
            raise FileNotFoundError(f'no {subject} paper for {year} {level}')
        self.era = 'topics' if year in TOPIC_ERA else 'sections'
        self._doc = pymupdf.open(self.path)
        self._asks = None
        # {(section, q): the tariff the paper prints on the question's own
        # head}. The new paper prices the QUESTION and leaves the split
        # between its parts to the scheme, so this is the only independent
        # check that a question was read whole.
        self.question_marks = {}

    # -- the joined stream, with the page each run of text came from ---------
    def _stream(self, start=0):
        runs = []
        for pno in range(start, len(self._doc)):
            for text in _page_text(self._doc[pno]):
                runs.append((pno + 1, unligature(text)))
        return runs

    def asks(self):
        if self._asks is None:
            self._asks = (self._topic_asks() if self.era == 'topics'
                          else self._section_asks())
        return self._asks

    # ------------------------------------------------------- 2021 and 2022 --
    def _topic_asks(self):
        runs = self._stream()
        # Topic heads open a topic; everything after one belongs to it until
        # the next. The title is printed on the head's own line.
        chunks = []
        cur = None
        for page, text in runs:
            for piece in re.split(r'(?=\bTopic\s+\d{1,2}\.\s)', text):
                piece = piece.strip()
                if not piece:
                    continue
                m = re.match(r'^Topic\s+(\d{1,2})\.\s*(.*)$', piece)
                if m:
                    cur = {'topic': int(m.group(1)),
                           'title': _clean(m.group(2).split('(i)')[0]),
                           'page': page, 'text': m.group(2)}
                    chunks.append(cur)
                elif cur is not None:
                    cur['text'] += ' ' + piece
        asks = []
        for chunk in chunks:
            asks += self._topic_parts(chunk)
        return asks

    def _topic_parts(self, chunk):
        text = ' '.join(chunk['text'].split())
        out = []
        # (i)..(iv) open the topic's questions; a letter before the first roman
        # would be a mis-read, and there is none in the corpus.
        pieces = re.split(r'(?=\((?:i|ii|iii|iv|v)\)\s)', text)
        for piece in pieces[1:]:
            m = re.match(r'^\((i|ii|iii|iv|v)\)\s*(.*)$', piece)
            if not m:
                continue
            roman, body = m.group(1), m.group(2)
            section = f'Topic {chunk["topic"]}({roman})'
            halves = re.split(r'(?=\(([a-f])\)\s)', body)
            stem = _clean(halves[0])
            if len(halves) == 1:
                marks, ask = self._split_marks(stem)
                out.append(Ask(section, None, None, None, ask, '', marks,
                               chunk['page']))
                continue
            # re.split with a capturing group interleaves the letter
            for i in range(1, len(halves), 2):
                letter = halves[i]
                body_i = halves[i + 1] if i + 1 < len(halves) else ''
                body_i = re.sub(r'^\(' + letter + r'\)\s*', '', body_i.strip())
                marks, ask = self._split_marks(_clean(body_i))
                out.append(Ask(section, None, letter, None, ask, stem, marks,
                               chunk['page']))
        return out

    @staticmethod
    def _split_marks(text):
        """The printed tariff, and the ask with it removed.

        A tariff is the LAST bare parenthesised number in the ask — the paper
        sets it hard right on the ask's own last line. A year ("in 418 BC") is
        not parenthesised and an attribution ("(Plutarch)") is not a number, so
        neither can be read as one.
        """
        found = list(TARIFF.finditer(text))
        if not found:
            return None, text
        last = found[-1]
        marks = int(last.group(1)) + int(last.group(2) or 0)
        text = (text[:last.start()] + ' ' + text[last.end():])
        return marks, _clean(text)

    # ---------------------------------------------------------- 2023 onward --
    def _first_question_page(self):
        """The page Section A opens on.

        The instructions page lists the paper's own structure — "Answer
        Question 11. (120 marks)", "Answer one from Questions 12-16." — in the
        same words a question head uses, and walking from page 1 read those
        listings as Question 11 and Question 12 themselves. Section A opens
        where the paper tells the candidate to answer its ten questions.
        """
        for pno in range(len(self._doc)):
            text = ' '.join(_page_text(self._doc[pno]))
            if re.search(r'Answer all (?:ten|10) of the following questions',
                         text, re.I):
                return pno
        raise AssertionError(
            f'{self.year} {self.level}: no "Answer all ten" page — Section A '
            'was not found, so the walk would start in the instructions')

    def _section_asks(self):
        runs = self._stream(self._first_question_page())
        joined = []
        for page, text in runs:
            joined.append((page, text))
        # Question heads: "Question 7" or "Question 7 (30 marks)".
        stream = []
        for page, text in joined:
            for piece in re.split(r'(?=\bQuestion\s+\d{1,2}\b)', text):
                if piece.strip():
                    stream.append((page, piece.strip()))
        chunks = []
        cur = None
        for page, piece in stream:
            m = re.match(r'^Question\s+(\d{1,2})\b\s*(.*)$', piece)
            if m:
                cur = {'q': int(m.group(1)), 'page': page, 'text': m.group(2)}
                chunks.append(cur)
            elif cur is not None:
                cur['text'] += ' ' + piece
        # "OR Question 13 Assess ..." puts the choice marker in front of the
        # head; it is furniture on the head, not part of the ask.
        out = []
        for chunk in chunks:
            out += self._section_parts(chunk)
        return out

    def _section_parts(self, chunk):
        text = RUBRIC.sub(' ', ' '.join(chunk['text'].split()))
        text = re.sub(r'\bOR\s+$', '', text).strip()
        # The new paper numbers Questions 1-16 straight through Sections A and
        # B, so the section is not part of an ask's address and the key does
        # not carry one. `band` names the section for a human reading a
        # report; the KEY stays sectionless.
        section = None
        q = chunk['q']
        head_marks, text = self._lead_marks(text)
        if head_marks:
            self.question_marks.setdefault((section, q), head_marks)
        halves = re.split(BACKREF + r'(?=\(([a-f])\)\s)', text)
        stem = _clean(halves[0])
        if len(halves) == 1:
            return [Ask(section, q, None, None, stem, '', head_marks,
                        chunk['page'])]
        out = []
        for i in range(1, len(halves), 2):
            letter = halves[i]
            body = halves[i + 1] if i + 1 < len(halves) else ''
            body = re.sub(r'^\(' + letter + r'\)\s*', '', body.strip())
            marks, body = self._lead_marks(body)
            romans = re.split(BACKREF + r'(?=\((?:i|ii|iii|iv|v)\)\s)', body)
            letter_stem = _clean(romans[0])
            if len(romans) == 1:
                out.append(Ask(section, q, letter, None, letter_stem, stem,
                               marks, chunk['page']))
                continue
            carried = ''
            for piece in romans[1:]:
                m = re.match(r'^\((i|ii|iii|iv|v)\)\s*(.*)$', piece)
                if not m:
                    continue
                body_r = re.sub(r'^\s*OR\s+', '', m.group(2)).strip()
                # "… 1. 2. 3. 4. OR Image Z: The Circus Maximus (ii) Name any
                # four architectural elements in Image Z." The words after the
                # standalone OR are the NEXT option's stem, printed before its
                # own marker; left in place they became part of this option's
                # ask.
                cut = re.split(r'\s+OR\s+', body_r, maxsplit=1)
                body_r, nxt = cut[0], (cut[1] if len(cut) > 1 else '')
                rmarks, body_r = self._lead_marks(body_r)
                out.append(Ask(section, q, letter, m.group(1), _clean(body_r),
                               ' '.join(x for x in (stem, letter_stem, carried)
                                        if x),
                               rmarks or marks, chunk['page'],
                               inherited=rmarks is None and marks is not None))
                carried = _clean(nxt)
        return out

    # -------------------------------------------------------- Paper X ------
    def figure_pages(self):
        """Where the illustration booklet prints each thing the paper cites.

        Paper X carries no questions — only the photographs and images the
        question booklet refers to — and it says on each page which of them it
        is holding. The two eras say it differently, and BOTH are read off the
        page rather than assumed:

          * 2021-2022 head each photograph with its own letter, "A." to "K.",
            and the booklet's last page acknowledges them by those letters;
          * 2023-2025 head each page "Ceist 1 / Question 1", naming the
            question the images on it belong to.

        Returns {label: page}, where a label is "A".."K" in the old era and
        "1".."10" in the new one.
        """
        if self.figures_path is None:
            return {}
        pages = {}
        doc = pymupdf.open(self.figures_path)
        for pno, page in enumerate(doc, 1):
            text = page.get_text().replace('\xa0', ' ')
            if self.era == 'topics':
                found = re.findall(r'^\s*([A-K])\.\s*$', text, re.M)
            else:
                found = re.findall(r'\bQuestion\s+(\d{1,2})\b', text)
            for label in found:
                # EVERY page a label appears on, not the first: 2025 Higher
                # prints Question 5's two images across two pages, and a card
                # bound to the first alone would hide half of what its ask
                # refers to.
                pages.setdefault(label, [])
                if pno not in pages[label]:
                    pages[label].append(pno)
        return pages

    @staticmethod
    def _lead_marks(text):
        """The "(40 marks)" the new paper prints beside a head, and the rest.

        The new paper prints its tariff as "(30 marks)" immediately after the
        head or part marker, not hard right at the end of the ask, so the FIRST
        such token is the tariff and a later parenthesised number in the ask's
        own wording — "Books 10-12", "(Aristotle)" — is not a tariff at all.
        """
        m = re.search(r'\((\d{1,3})\s*marks\)', text)
        if not m:
            return None, _clean(text)
        return int(m.group(1)), _clean(text[:m.start()] + ' ' + text[m.end():])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    P = ClPaper(args.year, args.level)
    asks = P.asks()
    if args.json:
        print(json.dumps([{'key': list(a.key), 'marks': a.marks,
                           'text': a.text, 'stem': a.stem, 'page': a.page}
                          for a in asks], indent=1, ensure_ascii=False))
        return 0
    print(f'{args.year} {args.level} ({P.era}): {len(asks)} asks, '
          f'{sum(a.marks or 0 for a in asks)} marks')
    for a in asks:
        print(f'  {str(a.key):38} {str(a.marks or "-"):>4}  {a.text[:90]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
