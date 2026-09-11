#!/usr/bin/env python3
"""Classical Studies marking schemes — what the SEC states, and what it bands.

    python3 scripts/markbank/authoring/cl_scheme.py 2024 hl
    python3 scripts/markbank/authoring/cl_scheme.py --audit

Two documents under one subject
-------------------------------
The schemes straddle the same 2023 syllabus break the papers do:

  * **2021 and 2022** answer every lettered part of every topic with a PROSE
    MODEL ANSWER — "The battle of Mantinea took place in 418-417 BC. The
    Spartans with their allies invaded the territory of Mantinea and laid waste
    the countryside…" — and close it with the printed tariff and its split,
    "A coherent account of the battle. (12, 12, 11.) (35 marks)". Every one of
    those parts is liftable.
  * **2023-2025** answer Section A with a mixture: a stated answer key ("1 mark
    each: 1: frieze, 2: capital; 3: caryatid", "2 marks: (Deus ex) machina or
    mechane"), a stated menu ("Examples: libations, lock of hair, ointment
    flasks, lekythoi…"), an "Indicative Material" list, or — for some parts —
    NOTHING but a band ladder. Section B's Question 11(b) and Questions 12-16
    print one common essay grid with no content at all.

This reader keeps the two apart per ask, because that distinction is the whole
admissions question for this subject and the bank's earlier rejection —
recorded as "Very Thorough 16-20, Thorough 10-15, Basic 5-9" — quoted the
RESEARCH STUDY REPORT grid, which is the coursework rubric printed on pages 3-5
of every scheme, not the written paper at all.

Where the tariff is printed
---------------------------
Three layouts, all read, none guessed:

  * old era: hard right at the end of the requirement line, "(35 marks)", with
    its split beside it, "(12, 12, 11.)";
  * 2023 and 2024: in a MARKS COLUMN, which the shared extractor rejoins onto
    the end of the part's opening line — "1. (a) Name of Temple: Parthenon,
    2 marks. Location: Acropolis, 2 marks. 4";
  * 2024 Ordinary and 2025: inline at the head of the part — "(a) 6 marks,
    2 marks each" or "(a) 1 mark each: true, false, false. (3 marks)".
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'classical-studies'
TOPIC_ERA = (2021, 2022)
ROMANS = ['i', 'ii', 'iii', 'iv', 'v']


def scheme_path(year, level, subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes',
                        f'{year}-{level}.md')


PAGE = re.compile(r'^## Page \d+\s*$')
# Boilerplate the SEC prints in front of every scheme: the note to teachers,
# the annotation table, and the Research Study Report grids. None of it prices
# a printed ask, and the RSR grid is the band ladder the bank's earlier
# verdict mistook for the paper.
RSR = re.compile(r'Research Study Report|Online Marking Annotations'
                 r'|Note to teachers and students|Future Marking Schemes'
                 r'|Marking schemes published by the State Examinations', re.I)

# A line that says how well, not what. These are the quality descriptors.
BAND = re.compile(
    r'^\s*(?:\d{1,3}\s*[-–]\s*\d{1,3}|\d{1,3})\s*(?:marks?)?\s*[:–-]\s*'
    r'(?:full|partial|basic|incomplete|very basic|good|excellent|an? |the )'
    r'|^\s*(?:full|partial|very basic|basic|incomplete)\s*:\s*\d'
    r'|\bbanded\b|\bbased on (?:level|quality|the level|development)\b'
    r'|^\s*\d{1,3}\s*(?:-|–)\s*\d{1,3}\s*$', re.I)
# A line that states content a student could be told to write.
STATES = re.compile(
    r'\bIndicative (?:Material|Answers?|points?)\b|\bExamples?\s*:'
    r'|\bAccept\b|\bsuch as\b|\be\.g\.', re.I)

# The tariff that closes an old-era answer. The closing bracket is OPTIONAL:
# on 2022 Ordinary page 22 the marks column clipped the line to "(20 mark",
# and requiring the bracket dropped that part's answer into its neighbour's.
# The vocabulary of SHAPE. A scheme that prices an ask with these words and
# nothing else has told the examiner how good an answer must be and told the
# candidate nothing about what to write.
SHAPE_WORDS = {
    'the', 'and', 'for', 'with', 'from', 'that', 'this', 'their', 'they',
    'are', 'was', 'were', 'has', 'have', 'not', 'but', 'its', 'his', 'her',
    'any', 'one', 'two', 'three', 'four', 'five', 'six', 'each', 'both',
    'marks', 'mark', 'full', 'partial', 'basic', 'incomplete', 'banded',
    'band', 'bands', 'based', 'level', 'levels', 'quality', 'detail',
    'details', 'detailed', 'point', 'points', 'developed', 'development',
    'candidate', 'candidates', 'answer', 'answers', 'answered', 'award',
    'awarded', 'accept', 'accepted', 'valid', 'accurate', 'accuracy',
    'description', 'describe', 'describes', 'explanation', 'explain',
    'explains', 'explained', 'account', 'discussion', 'discuss', 'opinion',
    'evidence', 'reference', 'references', 'referred', 'refer', 'brief',
    'briefly', 'coherent', 'coherence', 'clear', 'clearly', 'good', 'very',
    'may', 'must', 'should', 'will', 'can', 'question', 'questions', 'above',
    'following', 'given', 'give', 'gives', 'note', 'max', 'maximum',
    'credit', 'credited', 'relevant', 'reasons', 'reason', 'analysis',
    'understanding', 'knowledge', 'general', 'generic', 'specific',
    'required', 'requires', 'require', 'need', 'needed', 'least', 'more',
    'less', 'other', 'others', 'made', 'make', 'makes', 'marking', 'scheme',
    'order', 'per', 'nec', 'etc', 'also', 'well', 'where', 'when', 'which',
    'used', 'use', 'shows', 'show', 'shown', 'sufficient', 'top', 'awarding',
    'supported', 'support', 'supports', 'supporting', 'including', 'include',
    'includes', 'included', 'attempt', 'attempts', 'attempted', 'correct',
    'incorrect', 'value', 'either', 'agree', 'disagree', 'response',
    'responses', 'material', 'materials', 'aspect', 'aspects', 'link',
    'links', 'linked', 'stated', 'state', 'states', 'name', 'names', 'named',
    'term', 'terms', 'part', 'parts', 'item', 'items', 'list', 'lists',
    'listed', 'chosen', 'choose', 'first', 'second', 'third', 'fourth',
    'apply', 'applies', 'applied', 'overall', 'total', 'section',
    'fully', 'partially', 'inaccurate', 'invalid', 'accurately', 'wholly',
    'engagement', 'evaluation', 'impression', 'developed', 'coherently',
    'substantiated', 'comments', 'comment', 'qualities', 'quality', 'ways',
    'effects', 'causes', 'pieces', 'piece', 'views', 'view', 'treated',
}

# A name: a capitalised word that is not the first word of the line, and not
# one of the shape words a band ladder capitalises ("Full", "Partial").
PROPER = re.compile(r'(?<![.\u2022]\s)(?<!^)(?<![:;]\s)\b(?!Full|Partial|Basic|Very'
                    r'|Award|Accept|Indicative|Answer|Marks|NB|OR\b)'
                    r'[A-Z][a-z\u00e0-\u00ff]{2,}')
# An answer key printed as a run of letters or digits: "C, D, E, B, A".
KEYLIKE = re.compile(r'\b[A-Za-z0-9](?:\s*,\s*[A-Za-z0-9]){2,}\b')

# The band ladder does not always START a printed line: the converter rejoins a
# table row, so "- relevant terms" and "13-15: An accurate, full of
# description" arrive as one. Everything from the bound onwards is ladder.
INLINE_BAND = re.compile(r'\s(?=\d{1,2}\s*[-\u2013]\s*\d{1,2}\s*:'
                         r'|\d{1,2}\s*marks?\s*[:\u2013-]\s*(?:full|partial'
                         r'|basic|very|good|excellent))', re.I)

# The scheme's own running head, which lands inside an answer when the
# converter rejoins a page.
HEADER = re.compile(
    r'^(?:Leaving Certificate|Written Examination|Marking Scheme'
    r'|(?:Higher|Ordinary) Level|\d{4} Leaving Certificate'
    r'|Classical Studies)\b', re.I)

# The SEC telling the examiner what an answer must DO to earn the marks —
# "Experience of audiences at both venues should be described for full marks",
# "Must refer to specific points from the extract and other studied evidence
# for top band". It reads like content because it names the subject of the
# question, and it states no answer: a card whose whole back was one of these
# told the student to describe the thing they had just failed to describe.
# Never applied to a line that opens a MENU, because the SEC writes the same
# words inside one — "at least one temple must be referenced for full marks"
# ends an Indicative Material list whose items are the answer.
# Anchored on the MARKS, not on the modal verb. An earlier version matched any
# "must be" or "should be" and threw away the SEC's own prose — "it is a crime
# of disobedience which must be brutally punished" is Aeschylus, not a marking
# instruction — cutting seven model answers in half.
REQUIREMENT = re.compile(
    r'\bfor (?:full|top|the top) (?:marks|band)\b'
    r'|\brequired for (?:full|top) marks\b', re.I)

# The common extended-answer grid. Wherever these words appear the scheme is
# describing how to weigh an essay, not what the essay should say — and the ask
# it is the whole answer for is an exclusion, not a card.
GRID_WORDS = re.compile(
    r'\bunits? of development\b|\bOverall Quality\b|\bsame marking scheme\b'
    r'|\bDevelopment of [Mm]aterial\b|\bhas the same marking\b'
    r'|\bGrade descriptors\b', re.I)

# The seam between two entries the scheme printed at the SAME address — the
# three options of a "write notes on any two of the following" question. A
# marking point never runs across it.
SEAM = '\x00'

MARKS_TAIL = re.compile(r'\((\d{1,3})\s*marks?\)?\s*$', re.I)
SPLIT_TAIL = re.compile(r'\(([\d,;\s.a-z]+)\)\s*\((\d{1,3})\s*marks?\)\s*$', re.I)


class Entry:
    __slots__ = ('key', 'marks', 'note', 'lines')


    def __init__(self, key, marks, note, lines):
        self.key, self.marks, self.note, self.lines = key, marks, note, lines

    @property
    def band_lines(self):
        return [l for l in self.lines if BAND.search(l)]

    @property
    def stated_lines(self):
        """Everything the scheme prints that is content, not a band.

        A band line is dropped; so is the requirement sentence, which says what
        an answer must DO ("A coherent account of the battle") rather than what
        it must say. What is left is the model answer, the answer key and the
        indicative menu — the liftable half.
        """
        out = []
        in_band = False

        def seam():
            # A dropped line is a BOUNDARY, not a gap to close over. The
            # comparison text `comparableScheme` builds keeps the band ladder
            # and the running head, so a marking point welded across one is a
            # run of characters that appears nowhere in the scheme — which is
            # how twenty correct cards were dropped for quoting the SEC's own
            # answer. (A page marker or a bare marks cell is NOT a boundary:
            # the comparison text removes those, so a point does run across
            # them, and the old scheme's model answers do.)
            if out and out[-1] != SEAM:
                out.append(SEAM)

        for line in self.lines:
            stripped = line.strip()
            if stripped == SEAM:
                seam()
                in_band = False
                continue
            if HEADER.match(stripped):
                seam()
                continue
            if BAND.search(line):
                in_band = True
                seam()
                continue
            if PAGE.match(line):
                # A page break is not a band: the SEC's answers run across
                # one, and treating it as one dropped the lower-case
                # continuation of a sentence that had been cut in half.
                continue
            # The SEC's asterisked aside to the examiner — "**if military or
            # political is not addressed, 14 marks max", "*Award 1 mark for
            # valid but not exact" — is a ruling about marks, not an answer.
            # One of them was the whole back of a 20-mark card.
            if stripped.startswith('**'):
                seam()
                continue
            if REQUIREMENT.search(stripped) and not STATES.search(stripped):
                in_band = True
                seam()
                continue
            cut = INLINE_BAND.split(stripped, maxsplit=1)
            if len(cut) > 1:
                stripped, in_band = cut[0].strip(), True
                if stripped:
                    out.append(stripped)
                seam()
                continue
            # A band ladder WRAPS. "13-15: An accurate, full of description
            # with an amount of detail, that clearly / captures audience
            # experience. Full marks require reference to perspective from /
            # seating arrangement." is one printed descriptor over three lines,
            # and only its first line begins with a band bound — the other two
            # leaked into eight cards as marking points, none of which could be
            # found in the scheme because they start mid-sentence. A line
            # continuing a dropped one begins in lower case; a new marking
            # point does not.
            if in_band and stripped[:1].islower():
                continue
            if in_band:
                seam()
            in_band = False
            if not stripped or re.fullmatch(r'\d{1,3}', stripped):
                continue
            out.append(stripped)
        while out and out[-1] == SEAM:
            out.pop()
        return out

    @property
    def content_words(self):
        """The words left once every way of saying HOW WELL is removed.

        A marking scheme line either states something a candidate could have
        written or describes the shape of the answer and leaves the content to
        the examiner. Stripping the tariff, the band ladder and the vocabulary
        of shape — "full", "partial", "banded", "based on level of detail",
        "two developed points", "candidates may" — leaves the words that are
        content and nothing else. "Relief sculpture is sculpture which is
        raised from its background, but still attached to it" keeps eight;
        "10 marks, banded: 1-5: very basic/basic (general); 6-10: partial/full
        (specific details)" keeps none.
        """
        words = 0
        for line in self.stated_lines:
            bare = re.sub(r'\(?\b\d{1,3}\s*(?:[x\u00d7]\s*\d{1,3}\s*)?'
                          r'marks?\b\)?', ' ', line, flags=re.I)
            bare = re.sub(r'\b\d{1,3}\s*[-\u2013]\s*\d{1,3}\b', ' ', bare)
            bare = re.sub(r"[^A-Za-z\u2019' ]+", ' ', bare)
            words += sum(1 for w in bare.split()
                         if len(w) > 2 and w.lower() not in SHAPE_WORDS)
        return words

    @property
    def states_content(self):
        """Does this ask have a stated, liftable answer?

        Two printings count, and both were checked against the PDF before they
        were believed: a named menu the scheme heads itself ("Indicative
        Material", "Examples:", "such as"), and any block that survives the
        shape-word strip with real words left in it — which covers the old
        scheme's prose model answers, the answer keys ("Cronos. 2 marks.",
        "E: Parthenon, Pericles"), and the one-line facts ("It is built in the
        Doric Order").
        """
        if any(GRID_WORDS.search(l) for l in self.lines):
            return False
        lines = self.stated_lines
        if any(STATES.search(l) for l in lines):
            return True
        for line in lines:
            # A capitalised word that does not open the line is a name — the
            # thing the ask is about. "The painter was Exekias.", "Either Zeus
            # or Poseidon.", "In the Forum Romanum." are each a whole answer,
            # and each is too short to survive a word count.
            if PROPER.search(line):
                return True
            # An answer KEY: "(i) C, D, E, B, A", "1 mark each: 2, 4, 1, 3".
            if KEYLIKE.search(line):
                return True
        words = self.content_words
        if words >= 2:
            return True
        # A terse answer — "Temple", "Hadrian.", "This is an amphora." — is
        # one content word and nothing else, which is the whole answer.
        # "This is an amphora. One point. (5.) (5 marks)" and "It is a
        # temple. One point. (10.) (10 marks)" are each a whole printed answer
        # with its pricing beside it, and nine or ten words long.
        return words >= 1 and sum(len(l.split()) for l in lines) <= 12

    def as_dict(self):
        return {'key': list(self.key), 'marks': self.marks, 'note': self.note,
                'lines': self.lines, 'states': self.states_content}


def _late_marks(lines):
    """The tariff when it is not printed on the part's opening line.

    Two printings, both read off the page rather than assumed:

      * the MARKS COLUMN lands on whichever printed line its cell's vertical
        centre matched, which is not always the first — 2023 Higher Q2(a)
        prices "6 x 1 mark" on its head and puts the 6 at the end of the NEXT
        line, "1: Hermes, Mercury 6";
      * an inline "(12 marks)" wraps onto the following line, which is how
        2025 Higher Q6(a) prints it.

    Only the first three lines are read: past that a trailing integer is a band
    bound, not a tariff.
    """
    for line in lines[:3]:
        # "(14 marks)", and also "(20 marks: 7+7+6, in any order)" — the
        # bracket does not always close on the word, and requiring it left
        # 2025 Higher Q7 and Q10(b) unpriced over a colon.
        m = re.search(r'\((\d{1,3})\s*marks?\b', line, re.I)
        if m:
            return int(m.group(1))
        # The marks column on its own line, or leading its own band head:
        # 2024 Higher Q5(c) prints "14" and then "14 marks, banded".
        m = re.match(r'^\s*(\d{1,3})\s*(?:marks?\b)?\s*(?:,\s*banded)?\s*$',
                     line, re.I)
        if m:
            return int(m.group(1))
        if BAND.search(line):
            continue
        m = re.search(r'(?<=[a-z.,;)])\s(\d{1,3})\s*$', line)
        if m:
            return int(m.group(1))
    return None


def _drop_question_heads(entries):
    """Drop the Ordinary scheme's "1. 30 marks" line once its parts are read.

    The Ordinary schemes print the QUESTION total on a line of its own before
    the first part — "1. 30 marks", then "(a) 6 marks, 2 marks each" — and a
    head read as an ask invented eleven priced asks per Ordinary sitting that
    the paper never sets. It is only a head where the same question also prints
    lettered parts; where it does not (2025 Higher Question 7, priced whole
    because its (a) and (b) are alternatives), it IS the ask.
    """
    lettered = {e.key[:2] for e in entries if e.key[2] is not None}
    return [e for e in entries
            if e.key[2] is not None or e.key[:2] not in lettered]


def _normalise_letters(entries):
    """Two printings the old scheme uses for a question's FIRST part.

    The SEC sometimes omits the "(a)" and starts the first part's answer
    directly under the roman — 2021 Higher Topic 6(i), 2021 Ordinary Topic
    2(iii) — and sometimes prints "(a)" over a question the PAPER never
    subdivides at all — 2021 Higher Topic 7(i), a single 50-mark question.
    Both are the same shape read from opposite ends, and both are settled
    against the siblings the scheme itself prints: a letterless entry followed
    by a "(b)" is part (a); a lone "(a)" with no sibling is the whole question.
    """
    by_section = {}
    for e in entries:
        by_section.setdefault(e.key[0], []).append(e)
    for section, group in by_section.items():
        letters = [e.key[2] for e in group]
        if letters and letters[0] is None and 'b' in letters:
            group[0].key = (section, None, 'a', None)
        elif letters == ['a']:
            group[0].key = (section, None, None, None)
    return entries


class ClScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        self.era = 'topics' if year in TOPIC_ERA else 'sections'
        self.text = open(self.path, encoding='utf-8').read()
        self.entries = (self._topic_entries() if self.era == 'topics'
                        else self._section_entries())

    def by_key(self):
        """One entry per printed address, with repeats MERGED.

        The old Ordinary paper sets "Write notes on any two of the following:
        Cleon; Agis; Alcibiades", and its scheme answers each of the three in
        full at 25 marks and then closes the question with "Any two of the
        above. (50 marks)". Those are four entries at one address, and keeping
        the last alone threw away all three answers and left the question
        looking like a band. Merged, the address holds every line the scheme
        printed under it and the tariff the scheme closed it with.
        """
        merged = {}
        for e in self.entries:
            prev = merged.get(e.key)
            if prev is None:
                merged[e.key] = Entry(e.key, e.marks, e.note, list(e.lines))
                continue
            prev.lines.append(SEAM)
            prev.lines.extend(e.lines)
            prev.note = e.note
            prev.marks = e.marks or prev.marks
        return merged

    # ------------------------------------------------------- 2021 and 2022 --
    def _topic_entries(self):
        lines = self.text.splitlines()
        # The answers begin at the first topic head; everything before it is
        # the note to teachers and the introduction.
        start = next((i for i, l in enumerate(lines)
                      if re.match(r'^Topic\s+\d{1,2}[.:]', l)), None)
        if start is None:
            raise AssertionError(f'{self.path}: no "Topic 1." head')
        out = []
        topic = roman = letter = None
        buf = []
        for line in lines[start:]:
            if PAGE.match(line) or re.fullmatch(r'\s*\d{1,3}\s*', line):
                continue
            if re.match(r'^Appendix\b', line.strip()):
                break
            m = re.match(r'^Topic\s+(\d{1,2})[.:]', line)
            if m:
                topic, roman, letter, buf = int(m.group(1)), None, None, []
                continue
            m = re.match(r'^\((i{1,3}|iv|v)\)\s*(.*)$', line)
            if m:
                roman, letter, buf = m.group(1), None, []
                if m.group(2).strip():
                    buf.append(m.group(2).strip())
                continue
            m = re.match(r'^\(([a-f])\)\s*(.*)$', line)
            if m and topic is not None:
                letter, buf = m.group(1), []
                if m.group(2).strip():
                    buf.append(m.group(2).strip())
                continue
            if topic is None or roman is None:
                continue
            buf.append(line.strip())
            tail = MARKS_TAIL.search(line)
            if tail:
                key = (f'Topic {topic}({roman})', None, letter, None)
                out.append(Entry(key, int(tail.group(1)), line.strip(),
                                 list(buf)))
                buf = []
        return _normalise_letters(out)

    # ---------------------------------------------------------- 2023 onward --
    def _section_entries(self):
        lines = [l for l in self.text.splitlines() if not PAGE.match(l)]
        start = next((i for i, l in enumerate(lines)
                      if re.search(r'SECTION A|Section A\s*:?\s*(?:Stimulus|\d)',
                                   l)), None)
        if start is None:
            raise AssertionError(f'{self.path}: no Section A head')
        out = []
        q = letter = roman = None
        marks = None
        buf = []
        note = ''

        def close():
            if q is None:
                return
            # Sectionless on purpose: the paper numbers straight through.
            key = (None, q, letter, roman)
            if buf or marks:
                out.append(Entry(key, marks if marks else _late_marks(buf),
                                 note, list(buf)))

        # Whether the previous printed line was itself numbered. The scheme's
        # own Indicative Answers are NUMBERED LISTS — "1. theatron/ cavea/
        # auditorium/ seats", "2. cult statue/Athena Parthenos" — and the
        # second of those looks exactly like a question head. A head never
        # follows another numbered line, and the questions run 1 to 16 in
        # order, so the two guards together cannot be fooled by a list.
        prev_numbered = False
        for line in lines[start:]:
            raw = line.rstrip()
            if not raw.strip() or RSR.search(raw):
                continue
            numbered, was_numbered = bool(
                re.match(r'^\d{1,2}[.)]\s', raw)), prev_numbered
            prev_numbered = numbered
            # "11a (i) 25 marks" / "11a (ii) 15 marks" / "11 (a) …"
            m = re.match(r'^(\d{1,2})\s*\(?([a-f])\)?\s*\((i{1,3}|iv|v)\)\s*'
                         r'(\d{1,3})\s*marks?\b\s*(.*)$', raw)
            if m:
                close()
                q, letter, roman = int(m.group(1)), m.group(2), m.group(3)
                marks, note, buf = int(m.group(4)), raw, []
                if m.group(5).strip():
                    buf.append(m.group(5).strip())
                continue
            m = re.match(r'^Question\s+(\d{1,2})\s*\(?([a-f])\)?\.?\s*'
                         r'\((\d{1,3})\s*marks?\)\s*(.*)$', raw)
            if m:
                close()
                q, letter, roman = int(m.group(1)), m.group(2), None
                marks, note, buf = int(m.group(3)), raw, []
                if m.group(4).strip():
                    buf.append(m.group(4).strip())
                continue
            # "1. (a) …" or "1. 30 marks" or "1." alone
            # A question head is "1." followed by a part marker, a tariff, or
            # nothing — and it is the NEXT question. Both guards are needed:
            # the scheme's own Indicative Answers are numbered lists, so
            # "2. cult statue/Athena Parthenos" on 2023 Ordinary page 11 looks
            # exactly like a question head, and reading it as one reopened
            # Question 2 inside Section B and filed the whole essay grid under
            # it. A forward-only walk cannot be fooled that way: the questions
            # run 1 to 16 in order, on every paper in the corpus.
            m = re.match(r'^(\d{1,2})\.\s*(.*)$', raw)
            if m and int(m.group(1)) == (1 if q is None else q + 1) \
                    and int(m.group(1)) <= 16 and not was_numbered:
                close()
                q, letter, roman, buf = int(m.group(1)), None, None, []
                rest = m.group(2)
                marks, note, rest = self._lead_marks(rest)
                if rest.strip():
                    m2 = re.match(r'^\(([a-f])\)\s*(.*)$', rest.strip())
                    if m2:
                        letter = m2.group(1)
                        marks2, note2, rest2 = self._lead_marks(m2.group(2))
                        marks = marks2 or marks
                        note = note2 or note
                        if rest2.strip():
                            buf.append(rest2.strip())
                    else:
                        buf.append(rest.strip())
                continue
            m = re.match(r'^\(([a-f])\)\s*(.*)$', raw)
            if m and q is not None:
                close()
                letter, roman, buf = m.group(1), None, []
                marks, note, rest = self._lead_marks(m.group(2))
                # "6 marks – full explanation: 3 brief points…" is a BAND head.
                # Appending what is left after the tariff — "– full
                # explanation: …" — hid that from the band test, which reads
                # the start of the line, and shipped a quality descriptor as a
                # marking point.
                if rest.strip() and not BAND.search(m.group(2)):
                    buf.append(rest.strip())
                continue
            m = re.match(r'^\((i{1,3}|iv|v)\)\s*(.*)$', raw)
            if m and q is not None and letter is not None and re.search(
                    r'\d{1,3}\s*marks?', m.group(2), re.I):
                close()
                roman, buf = m.group(1), []
                marks, note, rest = self._lead_marks(m.group(2))
                if rest.strip():
                    buf.append(rest.strip())
                continue
            # Where the answers stop and the common essay grid begins. Every
            # line after it belongs to Question 11(b) and Questions 12-16,
            # which are marked by one grid and answered by no content — and
            # left running, that grid attached itself to whichever ask was
            # open, so four cards quoted "Development of material required to
            # fully answer the question" as a marking point.
            if re.search(r'Question 11 ?\(b\)\s*[-–]\s*Question 16'
                         r'|Questions? 12\s*[-–]\s*16'
                         r'|Question 11 ?\(b\)\s*:?\s*$', raw, re.I):
                close()
                q = letter = roman = None
                continue
            if q is not None:
                buf.append(raw.strip())
        close()
        return _drop_question_heads(out)

    @staticmethod
    def _lead_marks(text):
        """The part's tariff, the line it was printed on, and what is left.

        Both spellings are read: the marks COLUMN, which the extractor rejoins
        as a bare integer at the end of the opening line, and the inline
        "(6 marks)" or "6 marks," the 2024 Ordinary and 2025 schemes print at
        the head of the part. A bare integer is only a tariff at the END of the
        line — "4 x 5 marks" and "1: Athena" are neither.
        """
        m = re.match(r'^\((\d{1,3})\s*marks?\)\s*(.*)$', text, re.I)
        if m:
            return int(m.group(1)), text, m.group(2)
        # "1 mark each: true, false, false. (3 marks)" opens with a RATE, not
        # a tariff. Reading the rate as the tariff priced that ask at 1 mark
        # and swallowed the answer key with it.
        m = re.match(r'^(\d{1,3})\s*marks?\b(?!\s*(?:each|for each|per|x\b))'
                     r'[,:.]?\s*(.*)$', text, re.I)
        if m:
            return int(m.group(1)), text, m.group(2)
        m = re.search(r'\s(\d{1,3})\s*$', text)
        if m:
            return int(m.group(1)), text, text[:m.start()]
        m = re.search(r'\((\d{1,3})\s*marks?\)', text, re.I)
        if m:
            return int(m.group(1)), text, text
        return None, text, text


def sittings(subject=SUBJECT):
    root = os.path.join(ROOT, 'examiner-reports', subject, 'schemes')
    out = []
    for name in sorted(os.listdir(root)):
        m = re.match(r'^(\d{4})-(hl|ol)\.md$', name)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int, nargs='?')
    ap.add_argument('level', nargs='?')
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    if args.audit:
        tot = stated = 0
        for year, level in sittings():
            S = ClScheme(year, level)
            n = len(S.entries)
            st = sum(e.states_content for e in S.entries)
            tot, stated = tot + n, stated + st
            print(f'  {year} {level}: {n:3} priced asks, {st:3} with stated '
                  f'content ({100 * st // max(n, 1)}%)')
        print(f'  TOTAL: {tot} priced asks, {stated} stated '
              f'({100 * stated // max(tot, 1)}%)')
        return 0
    S = ClScheme(args.year, args.level)
    if args.json:
        print(json.dumps([e.as_dict() for e in S.entries], indent=1,
                         ensure_ascii=False))
        return 0
    for e in S.entries:
        flag = 'STATED' if e.states_content else 'band  '
        print(f'{str(e.key):34} {str(e.marks or "-"):>4} {flag} '
              f'{" | ".join(e.stated_lines)[:110]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
