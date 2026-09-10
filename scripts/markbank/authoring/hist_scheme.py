#!/usr/bin/env python3
"""History marking schemes — what the SEC states, and what it only bands.

    python3 scripts/markbank/authoring/hist_scheme.py 2021 hl lm

ONE DOCUMENT, TWO FIELDS OF STUDY
---------------------------------
The SEC publishes ONE scheme per year and level, and it answers BOTH fields:
"LEAVING CERTIFICATE 2021 / MARKING SCHEME / HISTORY / LATER MODERN" opens the
first half and the same title page with EARLY MODERN opens the second. The two
halves address their asks identically — "Section 1 ... 1. Comprehension ...
(a)", "Ireland: Topic 1 ... A1." — so reading the file whole would key each ask
twice and hand the Early Modern paper the Later Modern answers. The reader
splits on those title pages and returns one field.

WHAT THE SCHEME ACTUALLY STATES
-------------------------------
Two things, and they are not the same kind of thing:

*Stated answers.* The DBQ's comprehension parts get a flat right-hand tariff
list — "(a) To fight desegregation/maintain segregation 5M". The DBQ's
comparison and criticism parts get the examiner's own model answer, a lead
statement and then either bullets or a paragraph per document, priced 10M on
the ask with no per-point split. Ordinary Level's Part A gets five one-line
answers at (6) each. All of those are liftable.

*Bands.* Every essay on the paper — Higher Level's Sections 2 and 3, Ordinary
Level's parts B and C, and the DBQ's contextualisation part — is answered with
nothing but a ceiling: "Max. CM = 60 Max. OE = 40". There is no content to
lift, and none is invented: those asks are EXCLUDED, with that line as the
evidence, in exclusions/history.json.

THE BAND GRID IS DISCARDED, and audit() asserts it. The grid's rows are wordy
enough to survive any prose-length test — "Excellent: 11-12 marks Outstanding
piece of analysis, exposition or commentary" — and stage 0 counted 391 of them
as stated answers. Not one reaches a card.

THE TARIFF IS NEVER GUESSED. A comprehension part carries its own printed
marks and the card states them; a comparison or criticism part carries one
printed total and no split, so the card is `questionTotal` and its rows carry
`marks: null`. Nothing here divides a total the SEC left whole.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def scheme_path(year, level):
    return os.path.join(ROOT, 'examiner-reports', 'history', 'schemes',
                        f'{year}-{level}.md')


# The two title pages that divide the document. They are printed alone on their
# own page, in capitals in 2021 and in title case afterwards.
FIELD_TITLE = {'lm': re.compile(r'^(?:LATER MODERN|Later Modern)\s*$'),
               'em': re.compile(r'^(?:EARLY MODERN|Early Modern)\s*$')}
# append-scheme-columns.py appends a second rendering of the whole file for the
# provenance gate. It is the same content flattened, so reading it would double
# every ask.
APPENDED = re.compile(r'^<!--\s*markbank:')
PAGE_MARK = re.compile(r'^## Page \d+\s*$')

DBQ_START = re.compile(r'^Section 1:\s*DOCUMENTS-BASED QUESTION', re.I)
# Where the marking of the paper stops. Every scheme closes with the SEC's
# bonus-mark table for candidates answering through Irish, and it carries no
# marker of its own — so the last Part A answer of the 2024 and 2025 Early
# Modern schemes swallowed the whole appendix.
END_OF_SCHEME = re.compile(
    r'^(?:Coimisi[u\u00fa]n na Scr[u\u00fa]duithe St[a\u00e1]it'
    r'|Marcanna Breise|Bain [u\u00fa]s[a\u00e1]id as|Bunmharc)', re.I)
DBQ_HEAD = re.compile(
    r'^(\d)\.\s+(Comprehension|Comparison|Criticism|Contextualisation)\b'
    r'\s*\((\d{2})\s*marks\)')
SEC_HEAD = re.compile(r'^SECTION\s+([23])\s*:')
# "Ireland: Topic 1", "Ireland:Topic 6", "Ireland:  Topic 2" — the SEC's own
# spacing varies and one year drops the space after the colon entirely.
TOPIC_HEAD = re.compile(
    r'^(Ireland|Europe and the wider world)\s*:\s*Topic\s+(\d)\b', re.I)
# A Higher Level essay: the whole scheme entry for a 100-mark question.
ESSAY = re.compile(r'^(\d)\.\s+Max\.?\s*CM\s*=?\s*(\d+)\s+Max\.?\s*OE\s*=?\s*(\d+)')
# An Ordinary Level Part A answer.
A_LINE = re.compile(r'^A(\d)\.\s*(.*)$')
# The whole scheme entry for an Ordinary Level part B or C.
BC_LINE = re.compile(r'^([BC])\s*-\s*Max\s*CM\s*=\s*(\d+)\s*marks?\s*'
                     r'Max\s*OE\s*=\s*(\d+)\s*marks?')
EXTRA_HEAD = re.compile(
    r'^Extra (?:Section|Part) A questions on page \d+ of the '
    r'exam(?:ination)? paper', re.I)
LETTER_HEAD = re.compile(r'^\(([a-f])\)\s*(.*)$')
BULLET = re.compile(r'^[•●▪·]\s*(.*)$')
TRAILING_M = re.compile(r'\s*(\d{1,3})M\s*(?:max)?\s*$', re.I)
# The ask's CEILING, wherever the SEC writes it: "Max = 10M", "max 10M",
# "Max. 5m". It is the authority on what a part is worth, because the flat
# figures beside it are the split ("5M + 5M") or a partial-credit rule ("If
# only one doc, max. 5m") rather than the total.
MAX_M = re.compile(r'\bmax\.?\s*=?\s*(\d{1,3})M\b', re.I)
TRAILING_PAREN = re.compile(r'\s*\((\d{1,3})\)\s*$')
DOC_PARA = re.compile(r'^(Doc(?:ument)?\s+[AB])\s*:\s*(.*)$', re.I)
PAGE_FOOTER = re.compile(r'^\d{1,3}$')
# The TITLE PAGE of the field that follows. Splitting the file on the "Early
# Modern" line leaves the three lines printed above it — "LEAVING CERTIFICATE
# 2024 / MARKING SCHEME / HISTORY" — at the end of the Later Modern half, where
# they landed inside the last Part A answer and the provenance gate dropped
# three cards. Also the bonus-mark banner the 2025 schemes print on the same
# page.
SCHEME_FURNITURE = re.compile(
    r'^(?:LEAVING CERTIFICATE \d{4}$|MARKING SCHEME$|HISTORY$'
    r'|(?:HIGHER|ORDINARY) LEVEL$|\d{3}@\d{1,2}%$)', re.I)

# The cue that introduces the examiner's own list. Everything after it is
# content; the sentence before it is the scheme's own summary answer.
CUE = re.compile(
    r'^(?:Answers?|Points?|Reasons?|Supporting points?|The answer|'
    r'Relevant points?|Possible points?|Such points?)\b[^.]*'
    r'(?:include|contain)\b.*:?\s*$', re.I)

# The marking APPARATUS: the band grid, the tariff arithmetic and the
# instructions to the examiner. None of it is an answer, and all of it survives
# any prose-length test — which is why stage 0 counted 391 grid rows as stated
# answers. Kept as notes on the ask, never as a marking point.
GRID_LINE = re.compile(
    r'^(?:Each document to be marked'
    r'|Mark (?:the )?quality of'
    # Every printing of the sliding-scale instruction across the ten schemes:
    # "Mark on a sliding scale", "Mark each document on a sliding scale out of
    # 5:", "Mark the answer on a sliding scale out of 10:". The Early Modern
    # half words it differently from the Later Modern half in the same file,
    # and the narrower list let four band grids run on into the answer rows.
    r'|Marks?\b[^.]{0,60}\bsliding scale\b'
    r'|Mark by the principle of Core Statement'
    r'|Assess (?:the )?answer on'
    r'|Excellent\s*[:=]|Very good\s*[:=]|Good\s*[:=]|Fair\s*[:=]'
    r'|Weak\s*[:=]|Poor\s*[:=]'
    r'|Reference to (?:both|only|ALL|BOTH)'
    r'|Answer referring to'
    r'|Look for (?:two|three|ONE|TWO)\b'
    r'|One reason, well explained'
    r'|Max\.?\s*=|Max\.?\s*CM|Max\.?\s*OE'
    r'|\d+M\s*\+\s*\d+M'
    r'|Note that the question is looking for'
    r'|A Core Statement may be defined'
    r'|To apply the principle'
    r'|Here, in question \d'
    r'|In question \d, marking by paragraph'
    # "One opinion = 5M", "Explanation = 5M": the scheme dividing the tariff
    # and stating no content at all. 2021 Ordinary Q3(b) is nothing but these
    # two lines, and it is excluded rather than carded.
    r'|[A-Z][\w \u2019\'-]{0,34}=\s*\d{1,3}M\b)', re.I)

# The wording that proves a row came out of the band grid rather than the
# answer. audit() asserts no shipped row contains any of it.
GRID_WORDS = re.compile(
    r'sliding scale|Max\.?\s*CM|Max\.?\s*OE|Cumulative Mark|Overall Evaluation'
    r'|Excellent\s*[:=]|Very good\s*[:=]|Weak\s*[:=]|paragraph equivalent'
    r'|Core Statement|\bmks\b|award \d+ marks?\b|marked on a', re.I)

# An examiner instruction the SEC prints on the SAME line as the answer:
# "Bombing of homes/... Any TWO; if only ONE, award 3 marks." The clause is
# not part of the answer and must not be recited to a student as one, so it is
# lifted off the row and kept as the row's contextNote.
INSTRUCTION_TAIL = re.compile(
    r'\s*(?:Any (?:TWO|THREE|ONE)\b[^.]*\.?'
    r'|If only (?:ONE|TWO)\b[^.]*\.?'
    r'|\(?(?:any )?(?:one|two) elements? only = \d+m\)?'
    r'|\(?any two,? \d+m \+ \d+m\)?'
    r'|\(?\d+m \+ \d+m\)?)\s*$', re.I)

# A sentence that instructs the EXAMINER rather than answering the question.
# The SEC sets these in the same paragraph as its model answer — "Accept A or B
# and mark on the quality of the answer. Answers could include points such
# as:" — so they survive the line-level grid filter and reach a row. A student
# reading "Evaluate the answer on the quality of the points made" has been told
# nothing about the history.
INSTRUCTION_POINT = re.compile(
    r'^(?:Mark\b|Marks\b|Evaluate the answer|Assess\b|Award\b'
    r'|Accept\b[^.]{0,60}\bmark\b'
    r'|Examiners?\b|Reference to (?:both|only|ALL|BOTH)'
    r'|Look for\b|Answers? (?:could|may|might) include'
    r'|Points? could include|The answer could contain)', re.I)

# The document label the SEC prints at the END of a printed line rather than on
# one of its own — "...be kept within the city walls, etc. Doc B" in the 2023
# Early Modern scheme. Left in place it closes a marking row with the heading
# of the NEXT one.
TRAILING_DOC_LABEL = re.compile(r'\s+(Doc\.?(?:ument)?\s*[AB])\s*[:.]?\s*$')

# A document heading the scheme sets over its own bullets ("Document A:" on a
# line of its own). It says which document the points under it come from, so it
# rides on those rows as their contextNote rather than becoming a row itself.
DOC_HEAD = re.compile(r'^(Doc(?:ument)?\s+[AB])\s*:\s*$', re.I)

# The contents listing the Ordinary scheme prints before the DBQ itself.
DBQ_CONTENTS = re.compile(r'^There are four parts in the Documents-based question')

# A sentence boundary that is safe to split on: a full stop, question mark or
# closing quote followed by a capital. Initials ("E. D. Nixon"), "e.g." and
# "Doc A." are excluded, because splitting there would leave a fragment that
# is not a point.
SENTENCE = re.compile(
    r'(?<![A-Z])(?<!e\.g)(?<!i\.e)(?<!Doc)(?<!Mr)(?<!Mrs)(?<!Dr)(?<!St)'
    r'(?<!Fr)(?<!Rev)(?<!Prof)(?<!Sr)(?<!Co)(?<!No)'
    r'[.?!]["\u201d]?\s+(?=[A-Z\u201c"])')

def _halve(raw, field):
    """The lines of ONE field of study, in order."""
    lines = []
    for line in raw.split('\n'):
        if APPENDED.match(line):
            break
        lines.append(line.rstrip())
    starts = {}
    for key, pat in FIELD_TITLE.items():
        hits = [i for i, l in enumerate(lines) if pat.match(l.strip())]
        if len(hits) != 1:
            raise AssertionError(
                f'{key}: expected one "{pat.pattern}" title line, found {len(hits)}')
        starts[key] = hits[0]
    if starts['lm'] >= starts['em']:
        raise AssertionError('Early Modern is printed before Later Modern')
    lo = starts[field]
    hi = starts['em'] if field == 'lm' else len(lines)
    return [l.strip() for l in lines[lo:hi]]


class Ask:
    """One priced ask the scheme answers, or bands."""

    def __init__(self, key, kind, total, notation):
        self.key = key          # (section, q, letter, roman) — the paper's key
        self.kind = kind        # 'stated' | 'banded'
        self.total = total
        self.notation = notation
        self.lead = ''
        self.points = []
        self.notes = []
        self.evidence = ''
        self.cue = ''           # the scheme's own words, for the Law 4 join

    def __repr__(self):
        return f'<Ask {self.key} {self.kind} {self.total} {len(self.points)}pt>'


class HistScheme:
    def __init__(self, year, level, field):
        self.year, self.level, self.field = year, level, field
        self.path = scheme_path(year, level)
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        with open(self.path, encoding='utf-8') as fh:
            self.lines = _halve(fh.read(), field)
        self.asks = []
        self.by_key = {}
        self.refused = []
        self.dbq_totals = {}
        self.dbq_names = {}
        self.topic_titles = {}
        self._read()

    # -- reading ---------------------------------------------------------
    def _read(self):
        section = None
        topic = None
        extra = False
        dbq_q = None
        started = False
        listing = 0             # the Ordinary DBQ contents block
        want_title = None       # the topic title line expected next
        cur = None              # the open lettered/numbered block
        buf = []

        def close():
            nonlocal cur, buf
            if cur is not None:
                self._finish(cur, buf)
            cur, buf = None, []

        for line in self.lines:
            if (not line or PAGE_MARK.match(line) or PAGE_FOOTER.match(line)
                    or SCHEME_FURNITURE.match(line)):
                continue
            if END_OF_SCHEME.match(line):
                close()
                break
            if DBQ_START.match(line):
                close()
                started, section, topic, extra = True, '1', None, False
                continue
            if not started:
                continue
            if DBQ_CONTENTS.match(line):
                # "There are four parts in the Documents-based question:" is
                # followed by the four heads as a CONTENTS listing, and the
                # first real head repeats them. Read as heads they price four
                # asks the scheme has not answered yet, and 2021 Ordinary's
                # Q4 was keyed twice.
                listing = 4
                continue
            m = SEC_HEAD.match(line)
            if m:
                close()
                section, topic, extra, dbq_q = m.group(1), None, False, None
                continue
            m = TOPIC_HEAD.match(line)
            if m:
                close()
                topic, extra = int(m.group(2)), False
                if section == '1':
                    section = '2' if m.group(1).lower() == 'ireland' else '3'
                # The topic's printed TITLE follows on the next line, exactly
                # as it does on the paper. hist_all.py joins the two documents
                # on it.
                want_title = f'{section} Topic {topic}'
                continue
            if want_title:
                self.topic_titles[want_title] = line
                want_title = None
                continue
            if EXTRA_HEAD.match(line):
                close()
                extra, topic = True, None
                continue
            m = ESSAY.match(line)
            if m:
                close()
                ask = Ask((f'{section} Topic {topic}', int(m.group(1)),
                           None, None), 'banded',
                          int(m.group(2)) + int(m.group(3)), line)
                ask.evidence = line
                self._add(ask)
                continue
            m = BC_LINE.match(line)
            if m:
                close()
                ask = Ask((f'{section} Topic {topic} {m.group(1)}',
                           None, None, None), 'banded',
                          int(m.group(2)) + int(m.group(3)), line)
                ask.evidence = line
                self._add(ask)
                continue
            m = A_LINE.match(line)
            if m and (topic is not None or extra):
                close()
                unit = 'Extra A' if extra else f'{section} Topic {topic} A'
                cur = Ask((unit, int(m.group(1)), None, None), 'stated',
                          None, '')
                buf = [m.group(2)]
                continue
            if section == '1':
                m = DBQ_HEAD.match(line)
                if m:
                    if listing:
                        listing -= 1
                        continue
                    close()
                    dbq_q = int(m.group(1))
                    self.dbq_totals[dbq_q] = int(m.group(3))
                    self.dbq_names[dbq_q] = m.group(2)
                    if m.group(2) == 'Contextualisation':
                        # The scheme's whole answer here is the paragraph-band
                        # apparatus: "Cumulative Mark = Max. 24 marks Overall
                        # Evaluation = Max 16 marks" at Higher, the Core
                        # Statement rules at Ordinary. Nothing is stated. The
                        # block is still READ, so the exclusion's evidence is
                        # what the SEC actually prints under the head rather
                        # than the head alone.
                        cur = Ask(('1', dbq_q, None, None), 'banded',
                                  int(m.group(3)), line)
                        cur.evidence = line
                        buf = []
                    continue
                m = LETTER_HEAD.match(line)
                if m and dbq_q is not None:
                    close()
                    cur = Ask(('1', dbq_q, m.group(1), None), 'stated',
                              None, '')
                    buf = [m.group(2)]
                    continue
            if cur is not None:
                buf.append(line)
        close()

    def _add(self, ask):
        if ask.key in self.by_key:
            self.refused.append((ask.key, 'the scheme prices this ask twice'))
            return
        self.by_key[ask.key] = ask
        self.asks.append(ask)

    # -- one block -------------------------------------------------------
    def _tariff(self, lines, parent_total=None, lettered=False):
        """What the SEC prices this ask at, and the lines without the tariff.

        The ceiling wins where the scheme states one. "5M + 5M Max = 10M" is a
        split and a total on one line, and reading the first figure prices a
        ten-mark part at five; so does "Point with quote/explanation can earn
        5m", which is a partial-credit rule. The LAST ceiling on the block is
        the ask's own — a line may state a partial credit ("If only one doc,
        max. 5m") before the real total.

        The one ceiling that is NOT the ask's own is the comprehension
        question's recap: the Ordinary paper prints each part's "8M" and then
        "Max = 40M" under the last of them, which prices the QUESTION. It is
        recognised by being equal to the parent question's own printed total on
        a lettered part, never by position.
        """
        ceiling = None
        flat = None
        out = []
        for line in lines:
            for m in MAX_M.finditer(line):
                value = int(m.group(1))
                if lettered and parent_total is not None and value == parent_total:
                    continue
                ceiling = value
            m = TRAILING_M.search(line)
            if m:
                if flat is None:
                    flat = int(m.group(1))
                line = TRAILING_M.sub('', line)
            else:
                m = TRAILING_PAREN.search(line)
                if m and flat is None:
                    flat = int(m.group(1))
                    line = TRAILING_PAREN.sub('', line)
            out.append(line.strip())
        return (ceiling if ceiling is not None else flat), out

    def _finish(self, ask, buf):
        text = [t for t in buf if t.strip()]
        if ask.kind == 'banded':
            # Already known to be a ceiling; the block is kept as the printed
            # evidence for its exclusion, trimmed to what fits a ledger entry.
            ask.evidence = ' '.join(
                (ask.evidence + ' ' + ' '.join(text[:4])).split())[:400]
            self._add(ask)
            return
        if not text:
            self.refused.append((ask.key, 'the scheme states nothing here'))
            return
        # The grid is classified on the PRINTED line, before its tariff is
        # stripped: "One opinion = 5M" is the scheme dividing a total, and once
        # the 5M has been removed "One opinion =" no longer looks like it.
        grid = [bool(GRID_LINE.match(line)) for line in text]
        parent = (self.dbq_totals.get(ask.key[1]) if ask.key[0] == '1'
                  else None)
        ask.total, cleaned = self._tariff(
            text, parent, lettered=bool(ask.key[2]))
        ask.notation = f'{ask.total}M' if ask.total is not None else ''

        lead, points, notes = [], [], []
        doc = None              # the document heading currently in force
        mode = 'lead'
        for is_grid, line in zip(grid, cleaned):
            if not line:
                continue
            if is_grid:
                notes.append(line)
                mode = 'grid'
                continue
            if CUE.match(line):
                notes.append(line)
                mode = 'points'
                continue
            m = DOC_HEAD.match(line)
            if m:
                doc, mode = m.group(1), 'points'
                continue
            m = BULLET.match(line)
            if m:
                mode = 'points'
                points.append([doc, [m.group(1)], True])
                continue
            m = DOC_PARA.match(line)
            if m:
                mode = 'points'
                points.append([m.group(1), [m.group(2)], False])
                continue
            if mode == 'grid':
                notes.append(line)
                continue
            if mode == 'points' and points:
                points[-1][1].append(line)
                continue
            lead.append(line)

        ask.lead = ' '.join(' '.join(lead).split())
        ask.notes = [' '.join(n.split()) for n in notes]
        ask.points = []
        for label, chunk, bulleted in points:
            joined = ' '.join(' '.join(chunk).split())
            # A BULLET is already the scheme's own unit, however many sentences
            # the examiner wrote inside it — splitting one further is inventing
            # a segmentation the SEC did not make, and it took 2022 Higher
            # Q3(a) from the eleven bullets the scheme prints to twenty-three
            # rows, past the deck's own ceiling. Only a paragraph the scheme
            # left unsegmented is split.
            if bulleted:
                ask.points.append((label, joined))
                continue
            for piece in self._sentences(joined):
                ask.points.append((label, piece))
        if not ask.points and ask.lead:
            # A flat comprehension answer, or an Ordinary Part A answer: the
            # block IS the marking point, and stays whole because the SEC set
            # it as one line.
            if ask.total is not None and ask.total <= 8:
                ask.points = [(None, ask.lead)]
            else:
                ask.points = [(None, p) for p in self._sentences(ask.lead)]
            ask.lead = ''
        elif ask.lead:
            # The scheme's own summary answer, printed before its list.
            ask.points = [(None, p) for p in self._sentences(ask.lead)] + ask.points
            ask.lead = ''
        # An examiner instruction printed on the answer's own line is lifted
        # off the row and kept beside it.
        repaired = []
        for label, point in ask.points:
            m = TRAILING_DOC_LABEL.search(point)
            if m:
                doc_label = ' '.join(m.group(1).replace('.', '. ').split())
                point = point[:m.start()].strip()
                ask.notes.append(f'the next points are from {doc_label}')
            if INSTRUCTION_POINT.match(point):
                ask.notes.append(point)
                continue
            note = None
            m = INSTRUCTION_TAIL.search(point)
            if m and len(point) - len(m.group(0)) >= 12:
                note = m.group(0).strip()
                point = point[:m.start()].strip().rstrip(';,')
            repaired.append((label, point, note))
        ask.points = repaired
        ask.cue = ' '.join((' '.join(p for _l, p, _n in ask.points)).split())
        if not ask.points:
            # Nothing but tariff arithmetic under this head — 2021 Ordinary
            # Q3(b) is exactly "One opinion = 5M / Explanation = 5M / Max =
            # 10M". The evidence is the PRINTED block, not the notes the
            # tariff stripper has already taken the figures out of.
            ask.kind = 'banded'
            ask.evidence = ' '.join(' '.join(text).split())[:400]
        self._add(ask)

    @staticmethod
    def _sentences(text):
        """One paragraph as the sentences the examiner set out in it.

        Segmentation, never composition: no word changes and none is added.
        A comparison or criticism answer is printed as a paragraph per
        document — "Police were told to \u201cbreak up\u201d the boycotter car pools...
        Also, all black people waiting for lifts were to be charged with
        \u201cloitering\u201d." — and each of those sentences is a point the examiner
        credits. Left whole it is one 110-word row that no student can claim
        against. Short paragraphs stay whole.
        """
        text = text.strip()
        if len(text) <= 220:
            return [text] if text else []
        pieces, out = SENTENCE.split(text), []
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            # A fragment shorter than this is not a point; it is the tail of
            # the sentence before it, and it goes back onto that row.
            if out and len(piece) < 30:
                out[-1] = f'{out[-1]} {piece}'
            else:
                out.append(piece)
        return out or [text]

    # -- the assertion ---------------------------------------------------
    def audit(self):
        bad = [(a.key, p) for a in self.asks for _l, p, _n in a.points
               if GRID_WORDS.search(p)]
        return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=('hl', 'ol'))
    ap.add_argument('field', choices=('lm', 'em'))
    args = ap.parse_args()
    S = HistScheme(args.year, args.level, args.field)
    stated = [a for a in S.asks if a.kind == 'stated']
    banded = [a for a in S.asks if a.kind == 'banded']
    for a in S.asks:
        print(f'{str(a.key):<34} {a.kind:<7} total={a.total} '
              f'{len(a.points)}pt  '
              f'{(a.points[0][1] if a.points else a.evidence)[:80]}')
    print(f'{len(stated)} stated, {len(banded)} banded, '
          f'{len(S.refused)} refused')
    for key, why in S.refused[:10]:
        print(f'   REFUSED {key} {why}')
    bad = S.audit()
    print(f'band-grid leakage: {len(bad)}')
    for key, p in bad[:10]:
        print(f'   {key} {p[:90]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
