#!/usr/bin/env python3
"""Reviewed specs for the Romanian classic examination (small-languages lane).

One entry per printed ask; see sl_lib.py for the selector language. Line
numbers are lines of examiner-reports/romanian/schemes/<year>-hl.md.
"""
from sl_lib import (R, S, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


def bullets(*spans):
    """Shown rows, one per printed bullet: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after='• ')) if isinstance(a, int) else a
            for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


# ================================================================ 2010 HL ===
# Paper p3: Q1 "(5x1 puncte)" over five expressions; the scheme answers them as
# five unlettered bullets in the paper's order (each matches its expression's
# words: docu-, edu-, infotainment, plan de marketing, obiectivitate), priced
# "(5 puncte)" for the question. Q2-Q6 "(5 puncte)" each over points with no
# split: shown, priced as a whole (10a); Q3 is one explanation. Q2's first
# bullet is one sentence the SEC bulleted line by line (rendered p2): joined.
# Parts II (30) and III (40) on the four criteria the scheme prints for both
# (p4), 30/30/30/10 % (10b).
CRIT_2010 = crit((94, 95), (96, 97), (98, 99), 100)
SPECS[2010] = [
    R('I1a', [one(L(20, 21, after='• '), PP())]),
    R('I1b', [one(L(22, 23, after='• '), PP())]),
    R('I1c', [one(L(24, 25, after='• '), PP())]),
    R('I1d', [one(L(26, 27, after='• '), PP())]),
    R('I1e', [one(L(28, 29, after='• '), PP())]),
    R('I2', [shown(J(S(32, after='• '), S(33, after='• '), S(34, after='• '))), shown(L(35, 37, after='• ')),
             shown(L(38, 41, after='• '))], whole=True),
    R('I3', [one(L(44, 47), PP())]),
    R('I4', [shown(S(55, after='• '), lead=S(54)), shown(S(56, after='• '), lead=S(54)),
             shown(L(57, 58, after='• '), lead=S(54)), shown(S(60, after='• '), lead=S(59)),
             shown(S(61, after='• '), lead=S(59)), shown(L(62, 63, after='• '), lead=S(59))], whole=True,
      rownote=quote(S(53, after='4. '), lead='The scheme heads it')),
    R('I5', bullets((67, 69), (70, 72), (73, 74)), whole=True,
      rownote=quote(L(65, 66, after='5. '), lead='The scheme heads it')),
    R('I6', bullets((78, 80), 81, (82, 83), (84, 85), 86), whole=True,
      rownote=quote(L(76, 77, after='6. '), lead='The scheme heads it')),
    R('II1', [graded(L(102, 105), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints')),
    R('III1', [graded(L(107, 108), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints'),
      question=QP(4, 'Scrieţi un comentariu de aproximativ 300', '1. “Informaţia')),
    R('III2', [graded(L(107, 108), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints'),
      question=QP(4, 'Scrieţi un comentariu de aproximativ 300', '2. Nimeni')),
]


# ================================================================ 2011 HL ===
# Paper p4: PARTEA I "(30/100)", Q1 "(5 x 1 punct)" over five expressions a)-e);
# Q2-Q6 "(5 puncte)" each; PARTEA II "(30/100)"; PARTEA III "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13.
# Scheme (rendered pp3-5): Q1 answers the five expressions as five unlettered
# bullets in the paper's order, priced "(5 puncte)" for the question. Paired by
# order because each gloss's wording matches its expression: elita intelectuală
# / "mai aleşi intelectuali", s-a insinuat / "s-a strecurat", iscodesc /
# "cercetează ... să afle un secret", mediul academic / "societate de învăţaţi",
# a învigorat limba / "dă vigoare ... limbii". Q2 is one printed list (no
# bullets): one row at the printed price. Q3-Q6 print two or three bullets
# with no split: shown, priced as a whole (10a), each under the scheme's own
# heading. Parts II (30) and III (40) are marked on the four criteria printed
# on p4 (30/30/30/10 %, whole numbers of both totals: 10b), each part under its
# own descriptive line (p5). Under Part II the scheme also prints four bullets
# of content: quoted as examples, not a checklist. Printed error (10f): the
# scheme names the professor "Andrei Bulai", the paper "Alfred Bulai" (p4).
CRIT_2011 = crit((74, 75), (76, 77), (78, 79), 80)


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


def _bulai(d):
    paper = J(PC(4, 'Referindu-vă la text (p.5)', after='Profesorului '),
              PC(4, 'Bulai “Astea', before=' “Astea')).text(d)
    scheme = S(90, after='profesorul ', before=' relativizează').text(d)
    return f'The scheme names the speaker “{scheme}”; the paper prints “{paper}”.'


ESSAY_2011 = 'Scrieţi un comentariu de aproximativ 300'
SPECS[2011] = [
    R('I1a', [one(S(22, after='• '), PP())]),
    R('I1b', [one(S(23, after='• '), PP())]),
    R('I1c', [one(S(24, after='• '), PP())]),
    R('I1d', [one(S(25, after='• '), PP())]),
    R('I1e', [one(S(26, after='• '), PP())]),
    R('I2', [one(L(29, 31), PP())], rownote=_head(28, after='2. ')),
    R('I3', bullets(34, 35), whole=True, rownote=_head(33, after='3. ')),
    R('I4', bullets((39, 40), 41, (42, 43)), whole=True, rownote=_head(37, 38, after='4. ')),
    R('I5', bullets((51, 55), (56, 57)), whole=True, rownote=_head(49, 50, after='5. ')),
    R('I6', bullets((60, 63), (64, 66), (67, 70)), whole=True, rownote=_head(59, after='6. ')),
    R('II1', [graded(L(86, 89), PARTP(), CRIT_2011)],
      rownote=both(quote(S(73), lead='The scheme prints'),
                   examples(None, L(90, 93, after='• '), L(94, 95, after='• '), L(96, 98, after='• '),
                            L(99, 103, after='• ')),
                   _bulai)),
    R('III1', [graded(L(105, 106), PARTP(), CRIT_2011)],
      rownote=quote(S(73), lead='The scheme prints'),
      question=QP(4, ESSAY_2011, Run('1. În zilele noastre', 'simplificate.'))),
    R('III2', [graded(L(105, 106), PARTP(), CRIT_2011)],
      rownote=quote(S(73), lead='The scheme prints'),
      question=QP(4, ESSAY_2011, Run('2. ”Majoritatea', '(al 16-lea'))),
]
# The census reads the reading text as p4 (the questions page); the passage is
# printed on pp2-3 (rendered: title "DE CE VORBIM ÎN ENGLEZĂ?" on p2,
# paragraphs 1-8 over pp2-3, questions from p4).
for _s in SPECS[2011]:
    _s.pages = (2, 3)


# ================================================================ 2012 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 prints its five expressions
# a)-e) and ONE "(5 puncte)" under e) for the question as a whole (no "5 x 1"
# as 2010 and 2011 print); Q2-Q6 "(5 puncte)" each, every price on a line of
# its own under the question; PARTEA II "(30/100)"; PARTEA III "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13, but it
# reads three prices wrongly: it gives Q1's "(5 puncte)" to e) alone, does not
# read Q4's (p4 y202), and opens Q5's text with Q4's "puncte)". Q4 and Q5 are
# priced from their own printed lines (PY) and Q5's question is cut from the
# paper.
# Scheme (rendered pp3-6): Q1 answers the five expressions as five unlettered
# dashes in the paper's order and prices "(5 puncte)" for the question. Paired
# by order because each gloss's wording matches its expression: "democratizarea
# totală a publicatului" / "publicarea articolelor ... a devenit accesibilă
# orcui"; "lectura este pozitiv conotată" / "Cititul este perceput ... bună şi
# nobilă"; "citesc cu nesaţ" / "nerăbdători şi dornici să citească";
# "predispuşi să-l facă praf" / "abordează textul cu intenţia de a-l critica";
# "o fervoare a demascării" / "O pasiune ... de a face public ... părţile
# ascunse". Neither paper nor scheme prices an expression on its own, so Q1(a)-
# (e) are CARDING-STANDARD 10i asks (never split the 5): they are NOT in SPECS
# below but in Q1 (carded at the question)_2012, each with its scheme answer as a shown row;
# `total=` there is the Q1 price to lift into unpricedSection.totalMarks, not
# the card's own total (10i: questionTotal, totalMarks 0). sl_lib in this
# worktree has no unpricedSection shape (d9181d7ef is not in HEAD).
# Q2, Q3, Q4 and Q6 print two to five dashes with no split: shown, priced as a
# whole (10a), each under the scheme's own heading. Q5 prints one paragraph:
# one row at the printed price. Q6's second dash runs over the page break
# (p4 "Avem cu toţii ..." to p5 "lectură bună şi una mai puţin bună."): joined.
# Parts II (30) and III (40) are marked on the four criteria printed on p5
# (30/30/30/10 %, whole numbers of both totals: 10b), each under its own
# descriptive line. Under Part II the scheme also prints three dashes of
# content: quoted as examples, not a checklist (the third runs over the p5/p6
# break; the second's "responsabi-"/"litate" is joined as printed).


def dashes(*spans):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after='- ')) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2012 = crit((105, 106), (107, 108), (109, 110), 111)
ESSAY_2012 = Run('Scrieţi un comentariu de aproximativ 300', 'punctul vostru de vedere')
Q1P_2012 = PY(3, 771)
SPECS[2012] = [
    R('I2', dashes((38, 39), (40, 41), (42, 43), 44, (45, 47)), whole=True,
      rownote=_head(37, after='2. ')),
    R('I3', dashes((53, 55), (56, 57), (58, 61)), whole=True,
      rownote=_head(49, after='3. ')),
    R('I4', dashes((65, 70), (71, 73)), whole=True, total=PY(4, 202),
      rownote=_head(63, 64, after='4. ')),
    R('I5', [one(L(77, 83), PY(4, 308))], total=PY(4, 308),
      rownote=_head(75, 76, after='5. '),
      question=QP(4, '5. Explicaţi de ce este comparat', Run('“ Unele sînt', '(p.5)'))),
    R('I6', [shown(L(86, 88, after='- ')), shown(J(L(89, 92, after='- '), S(96))),
             shown(L(97, 101, after='- '))], whole=True,
      rownote=_head(85, after='6. ')),
    R('II1', [graded(L(113, 116), PARTP(), CRIT_2012)],
      rownote=both(quote(S(104), lead='The scheme prints'),
                   examples(None, L(117, 120, after='- '),
                            Join(L(121, 123, after='- '), L(124, 127), sep=''),
                            J(L(128, 134, after='- '), L(138, 139))))),
    R('III1', [graded(L(141, 142), PARTP(), CRIT_2012)],
      rownote=quote(S(104), lead='The scheme prints'),
      question=QP(4, ESSAY_2012, '1. Cuvântul scris')),
    R('III2', [graded(L(141, 142), PARTP(), CRIT_2012)],
      rownote=quote(S(104), lead='The scheme prints'),
      question=QP(4, ESSAY_2012, '2. În societatea modernă')),
]

# CARD-STANDARD 10i, not built by sl_lib here: see the comment above.

# The reading text is printed on pp2-3 (rendered: "Citind..." on p2, paragraphs
# 1-8 to Sever VOINESCU's byline on p3; questions from p3 y581).
SPECS[2012].insert(0, R('I1', [shown(L(22, 24, after='- ')), shown(S(25, after='- ')), shown(L(26, 28, after='- ')), shown(L(29, 32, after='- ')), shown(L(33, 35, after='- '))], whole=True, total=Q1P_2012,
      question=QL(3, Run('1. Explicaţi pe scurt cu', 'de context.'), 'a) democratizarea to', 'b) lectura este pozi', 'c) citesc cu nesaţ (', 'd) predispuşi să-l f', 'e) o fervoare a dema')))
for _s in SPECS[2012]:
    _s.pages = (2, 3)


# ================================================================ 2014 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroşat în text" (bold in the passage, pp2-3; each is
# reprinted in italics in the question, so no stem is needed) and prints ONE
# "(5 puncte)" under e) for the question as a whole; Q2-Q6 "(5 puncte)" each;
# PARTEA a II-a "(30/100)"; PARTEA a III-a "(40/100)", two titles joined by
# "SAU". The census's 13 asks are the paper's 13; it gives Q1's "(5 puncte)"
# to e) alone.
# Scheme (rendered pp3-5): Q1 letters its answers a)-e), reprinting each
# expression above its dash (e) as "indiferenţă", the paper's "indiferenţa"),
# and prices "(5 puncte)" for the question: CARD-STANDARD 10i asks, NOT in
# SPECS but in Q1 (carded at the question)_2014 (see 2012). Q2-Q6 print three or four dashes
# each with no split: shown, priced as a whole (10a), under the scheme's own
# heading; Q3's third dash opens p4 (no line runs over the break); Q6's last
# dash ends in "(5 puncte)" on its own line of text, cut before it. Parts II
# (30) and III (40) are marked on the four criteria printed on p5 (30/30/30/10
# %, whole numbers: 10b), under each part's own descriptive line. Under Part II
# the scheme prints one dash and two undashed paragraphs at the same indent
# (rendered p5): quoted as examples, not a checklist. Paper and scheme
# disagree on Part III's first title (paper "în primul rând", scheme "înainte
# de toate"): the paper wins on the question, the scheme's words quoted (10f).


def dashes(*spans, mark='– '):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after=mark)) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2014 = crit(149, (150, 151), (152, 153), 154)
NOTE_2014 = quote(L(147, 148), lead='The scheme prints')
ESSAY_2014 = Run('Scrieți un eseu', 'cuvinte):')
Q1P_2014 = PY(3, 582)
SPECS[2014] = [
    R('I2', dashes((68, 71), (72, 75), (76, 78)), whole=True, rownote=_head(67, after='2. ')),
    R('I3', dashes((81, 84), (85, 88), (93, 95)), whole=True, rownote=_head(80, after='3. ')),
    R('I4', dashes((99, 102), (103, 106), (107, 109)), whole=True, rownote=_head(97, 98, after='4. ')),
    R('I5', dashes((113, 116), (117, 118), (119, 121), (122, 124)), whole=True,
      rownote=_head(111, 112, after='5. ')),
    R('I6', dashes((127, 130), (131, 136), (137, 138)) + [shown(L(139, 141, after='– ', before=' (5 puncte)'))],
      whole=True, rownote=_head(126, after='6. ')),
    R('II1', [graded(L(156, 157), PARTP(), CRIT_2014)],
      rownote=both(NOTE_2014,
                   examples(None, L(158, 161, after='– '), L(162, 167), L(168, 173)))),
    R('III1', [graded(L(175, 176), PARTP(), CRIT_2014)],
      rownote=both(NOTE_2014,
                   quote(S(177, after='1 . '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2014, '1. Bogăția')),
    R('III2', [graded(L(175, 176), PARTP(), CRIT_2014)],
      rownote=NOTE_2014,
      question=QP(4, ESSAY_2014, '2. „Chiar')),
]

# CARD-STANDARD 10i, not built by sl_lib here (see 2012). The scheme letters
# each answer under its reprinted expression: a) line 51, b) 54, c) 56, d) 59,
# e) 63.

# The reading text is printed on pp2-3 (rendered: paragraphs to paragraph 8
# and Maria IORDĂNESCU's byline on p3; questions from p3 "ÎNTREBĂRI").
SPECS[2014].insert(0, R('I1', [shown(L(52, 53, after='– ')), shown(S(55, after='– ')), shown(L(57, 58, after='– ')), shown(L(60, 62, after='– ')), shown(L(64, 65, after='– '))], whole=True, total=Q1P_2014,
      question=QL(3, '1. Explicați următoarele cuvin', 'a) locuri incredibil', 'b) patrimoniu cultur', 'c) a imita', 'd) păreri proaspete', 'e) indiferența')))
for _s in SPECS[2014]:
    _s.pages = (2, 3)


# ================================================================ 2016 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroșat în text" (each reprinted in the question) and
# prints ONE "(5 puncte)" under e) for the question as a whole; Q2-Q6 "(5
# puncte)" each; PARTEA a II-a "(30/100)"; PARTEA a III-a "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13; it gives
# Q1's "(5 puncte)" to e) alone.
# Scheme (rendered pp3-6): Q1 letters its answers a)-e), each after its
# expression and a dash on the same line, and prices "(5 puncte)" for the
# question: CARD-STANDARD 10i asks, NOT in SPECS but in Q1 (carded at the question)_2016 (see
# 2012). Q2-Q5: the scheme reprints each question in italics under its
# heading, then three or four dashes with no split: shown, priced as a whole
# (10a), under the heading; Q5's first dash runs over the p4/p5 break
# ("poate" / "însemna"): joined. Q6 prints two indented paragraphs of model
# answer (rendered p5) under its reprinted question: shown, priced as a whole.
# Parts II (30) and III (40) are marked on the four criteria printed on p5
# (30/30/30/10 %, whole numbers: 10b). Part II prints no descriptive line of
# its own: its head is the scheme's line introducing the criteria (as 2015,
# and Dutch 2010-2011); under it the scheme reprints the task (as the paper
# prints it) and two paragraphs of model commentary, quoted as examples, not
# a checklist. Part III is headed by its own descriptive line (rendered p6).


def dashes(*spans, mark='- '):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after=mark)) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2016 = crit(160, (161, 162), (163, 164), 165)
NOTE_2016 = quote(L(158, 159), lead='The scheme prints')
ESSAY_2016 = Run('Scrieți un eseu', 'cuvinte):')
Q1P_2016 = PY(3, 653)
SPECS[2016] = [
    R('I2', dashes((67, 70), (71, 75), (76, 79)), whole=True, rownote=_head(65, after='2. ')),
    R('I3', dashes((88, 91), (92, 95), (96, 97)), whole=True, rownote=_head(85, after='3. ')),
    R('I4', dashes((103, 107), (108, 110), (111, 115), (116, 118)), whole=True,
      rownote=_head(99, 100, after='4. ')),
    R('I5', [shown(J(L(124, 125, after='- '), L(130, 132)))] + dashes((133, 134), (135, 138)), whole=True,
      rownote=_head(120, 121, after='5. ')),
    R('I6', [shown(L(143, 147)), shown(L(148, 155))], whole=True, rownote=_head(140, after='6. ')),
    R('II1', [graded(L(158, 159), PARTP(), CRIT_2016)],
      rownote=examples(None, L(174, 183), L(184, 187))),
    R('III1', [graded(L(189, 190), PARTP(), CRIT_2016)], rownote=NOTE_2016,
      question=QP(4, ESSAY_2016, Run('1 . „Cu cât', 'între noi.'))),
    R('III2', [graded(L(189, 190), PARTP(), CRIT_2016)], rownote=NOTE_2016,
      question=QP(4, ESSAY_2016, Run('2. „Lumea', 'democratică și'))),
]

# CARD-STANDARD 10i, not built by sl_lib here (see 2012). Each answer is cut
# after the dash that follows its expression on the scheme's own line.

# The reading text is printed on pp2-3 (questions from p3 PARTEA I, y451).
SPECS[2016].insert(0, R('I1', [shown(L(51, 54, after=' – ')), shown(L(55, 56, after=' – ')), shown(L(57, 58, after=' – ')), shown(L(59, 60, after=' – ')), shown(L(61, 63, after=' – '))], whole=True, total=Q1P_2016,
      question=QL(3, Run('1. Explicați pe scurt ur', 'perifraze și ținând cont'), 'a) oamenii de valoar', 'b) pseudo-vedete', 'c) trăncăneală', 'd) decăderea moravur', 'e) criza de încreder')))
for _s in SPECS[2016]:
    _s.pages = (2, 3)


for _s in SPECS[2010]:
    _s.pages = (2, 3)


def specs(year):
    return SPECS.get(year, [])
