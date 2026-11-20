#!/usr/bin/env python3
"""Reviewed specs for the Hungarian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/hungarian/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme, Unpriced)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2010 HL ===
# Carded by the lead (20 Nov). Live: Part I. Paper p4: II. RÉSZ "(30 pont / 100
# pont)" (y70), the commentary on one sentence; III. RÉSZ "(40 pont / 100 pont)"
# (y217), two titles ("1. lehetőség" / "vagy" / "2. lehetőség"). Scheme p3-4:
# "A II. és III. részben elérhető pontok az alábbi szempontok szerint oszlanak
# meg:" (103) and the four criteria at 30/30/30/10 % (104-110): both parts
# graded (10b). Part II's head is its requirement line (77), its "Lehetséges
# irányok:" (78) quoted as examples; Part III's head is its own line (94), each
# title's "Egyéni válasz körülbelül 300 szóban." left to the head. The labels
# "1. lehetőség" / "2. lehetőség" are not part of the titles.
CRIT_2010 = crit((104, 105), (106, 107), (108, 109), 110)
LEAD_2010 = quote(S(103), lead='The scheme prints')
SPECS[2010] = [
    R('II1', [graded(S(77), PARTP(), CRIT_2010)],
      rownote=both(LEAD_2010, examples(S(78), L(79, 80, after='• '), L(81, 82, after='• '), L(83, 84, after='• '),
                                       S(85, after='• '), S(86, after='• '), S(87, after='• '))),
      question=QP(4, 'A szöveg alapján kommentáld', 'Pénzt kell költeni'), pages=(2, 3)),
    R('III1', [graded(S(94), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, 'A két téma közül', 'Reklámok: hiszünk')),
    R('III2', [graded(S(94), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, 'A két téma közül', Run('„Senki sem', '(J. Donne'))),
]


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I1a, II1, III1, III2. Live: I1b-e, I2-I6 (9 cards); not touched here (see the
# live audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y78 ("Válaszolj érthetően magyarul az I., II.
# és III. részben feltett kérdésekre!"); reading text "Nemzetközi tizenegy -
# Foci és identitás" p2 y107 to the byline "Vajna Tamás, Weyer Béla, HVG 2010.,
# adaptáció" p3 y327 (paragraphs 1-4 on p2, 5-6 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y373; Q1 a)-e) each "(1 pont)" at the right margin; Q2-Q6 "(5
# pont)"; "II. RÉSZ (30 pont / 100 pont)" p4 y79; "III. RÉSZ (40 pont / 100
# pont)" p4 y247, two titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES:
# - I1a: the census reads no price (tariff None): the text layer welds the
#   question number and a)'s margin price into one line "1. (1 pont)" (p3 x74
#   y429), with "a, Magyarázd meg ..." a separate cell at x108 on the same y.
#   Rendered p3: "(1 pont)" sits at the right margin on a)'s own line, as for
#   b)-e). Priced from that printed line (PaperP); the scheme prints the same
#   "(1 pont)" on its reprint of a) (line 19). Not a remainder, not 10i.
# - II1: the part head's "(30 pont / 100 pont)" (PARTP); III1/III2: "(40 pont /
#   100 pont)" (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q1 a) (19 reprints the expression with "(1 pont)"): one italic gloss,
#   lines 20-22, "A 4. bekezdésben található szó saját szavaiddal kifejezve: a
#   „morális” szó azt jelenti, hogy erkölcsös, erkölcsi. Azon normák alapján
#   élő, amelyeket társadalmi szinten helyesnek tartunk." One stated answer: one
#   row at the paper's "(1 pont)", lead kept as the live b)-e) keep theirs.
# - Criteria (p4, under Q6, before Part II): "A II. és III. részben elérhető
#   pontok az alábbi szempontok szerint oszlanak meg:" (72) and the four
#   criteria at 30/30/30/10 % (73-78), stated for Parts II and III: both graded
#   (10b), 9/9/9/3 of 30 and 12/12/12/4 of 40, as the lead's 2010.
# - Part II (79-83 reprint the part head and the task): the requirement line
#   "A minimum 100 szóban tisztán, érthetően kifejtett saját vélemény." (88) is
#   the graded row's head; "Lehetséges irányok:" (89) and the list under it
#   (rendered p5: italic, two bold-italic sub-heads "a) Németország a pozitív
#   példa:" / "b) Franciaország a negatív példa:" with five and four bullets,
#   and "c) Saját szavakkal kifejtett vélemény") quoted as examples, every
#   printed line in order, sub-heads included.
# - Part III (114-124): "Tisztán, érthetően és világosan megírt esszé." (116),
#   the graded rows' head; each title reprinted with "Egyéni válasz minimum 300
#   szóban." (119, 124), left to the head as in 2010.
# SHAPES: I1a one(); II1, III1, III2 graded(head, PARTP(), CRIT_2011).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on I1a and II1. The live I1b-e
#   and I2-I6 carry [3]: flagged in the live audit.
# - II1's question is cut from the paper's own lines (the census glues the
#   part head's "(30 pont / 100 pont) Kommentár" in front); the instruction line
#   kept, as the lead's 2010.
# - III1/III2: the instruction line plus the title, the labels "1. lehetőség"
#   / "2. lehetőség" left out, as the lead's 2010; title 2 keeps its printed
#   attribution line "(Abraham Lincoln, ...)".
# GLYPHS: none in the lines used (á é í ó ö ő ú ü ű read clean, render checked).
CRIT_2011 = crit(73, (74, 75), (76, 77), 78)
LEAD_2011 = quote(S(72), lead='The scheme prints')
SPECS[2011] = [
    R('I1a', [one(L(20, 22), PaperP(3, '1. (1 pont)'))], total=PaperP(3, '1. (1 pont)'), pages=(2, 3)),
    R('II1', [graded(S(88), PARTP(), CRIT_2011)],
      rownote=both(LEAD_2011, examples(S(89), S(90), L(91, 93), L(94, 97), L(98, 100), L(101, 102),
                                       L(103, 104), S(105), L(106, 107), S(108), L(109, 110), L(111, 112),
                                       S(113))),
      question=QP(4, 'A szöveg alapján kommentáld', Run('Kommentáld, hogyan', 'véleményedet!')), pages=(2, 3)),
    R('III1', [graded(S(116), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, 'A két téma közül', 'A diverzitás')),
    R('III2', [graded(S(116), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, 'A két téma közül', Run('„A legtöbben', '(Abraham Lincoln'))),
]


# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y78-94 ("Olvassa el a következő szöveget, és
# válaszoljon érthetően magyarul az I., II. és III. részben feltett
# kérdésekre!"), "(100 pont)" p2 y120; reading text "Köszbizalom" p2 y149 to
# the byline "Balázs Zsuzsanna, HVG, 2011/36. szám, adaptáció" p3 y309
# (paragraphs 1-5 on p2, the end of 5 and 6 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y346; "II. RÉSZ (30 pont / 100 pont)" p4 y78; "III. RÉSZ (40 pont /
# 100 pont)" p4 y253, two titles printed "1." / "vagy" / "2." (no "lehetőség"
# labels on the paper; the scheme adds them, 128/132).
# PRICES: II1 the part head's "(30 pont / 100 pont)" (PARTP); III1/III2 "(40
# pont / 100 pont)" (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6): "A II. és III. részben elérhető pontok az alábbi
#   szempontok" / "szerint oszlanak meg:" (89-90) and the four criteria at
#   30/30/30/10 % (91-97), for Parts II and III: both graded (10b).
# - Part II (101-105 reprint the head and the task): requirement line "A
#   minimum 100 szóban tisztán, érthetően kifejtett saját vélemény." (106), the
#   graded head; "Lehetséges irányok:" (107) and four dashed points (108-124),
#   quoted as examples.
# - Part III (125-134): "Tisztán, érthetően és világosan megírt esszé." (127),
#   the head; each title with "Egyéni válasz minimum 300 szóban." left to it.
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2012).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. The live Part I cards
#   carry [3]: flagged in the live audit.
# - II1's question: the instruction line and the task cut from the paper's own
#   lines (the census glues "(30 pont / 100 pont) Kommentár" in front). The
#   paper prints the quotation opening „ [A] with a space after the mark: lifted
#   as printed.
# - III1/III2: the instruction line plus the title, its printed "1." / "2."
#   taken off as a marker (ruling B cites them Section III Q1/Q2).
# GLYPHS: none in the lines used.
CRIT_2012 = crit((91, 92), (93, 94), (95, 96), 97)
LEAD_2012 = quote(L(89, 90), lead='The scheme prints')
SPECS[2012] = [
    R('II1', [graded(S(106), PARTP(), CRIT_2012)],
      rownote=both(LEAD_2012, examples(S(107), L(108, 112), L(113, 115), L(116, 119), L(120, 124))),
      question=QP(4, 'A szöveg alapján kommentálja', Run('„ [A] viszonosság', '100 szóban!')), pages=(2, 3)),
    R('III1', [graded(S(127), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, 'A két téma közül', '1. Jobb tisztességben')),
    R('III2', [graded(S(127), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, 'A két téma közül', '2. Modern társadalmunkban')),
]


# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y64-78; reading text "Kikapcs - Tévét nem
# nézők. ..." p2 y107 to the byline "Dobszay János, HVG, 2012, adaptáció" p3
# y368 (paragraphs 1-6 on p2, the end of 6 and 7-8 on p3); "I. RÉSZ (30 pont /
# 100 pont)" p3 y478 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100 pont)"
# p4 y382; "III. RÉSZ (40 pont / 100 pont)" p4 y564, titles "1. lehetőség" /
# "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)", each
# on its part head (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6; set in a grey box): "A II. és III. részben elérhető
#   pontok az alábbi szempontok" / "szerint oszlanak meg:" (103-104) and the
#   four criteria at 30/30/30/10 % (105-111), for Parts II and III: graded.
# - Part II (112-117 reprint the head and the task): requirement line "A
#   minimum 100 szóban tisztán, érthetően kifejtett saját vélemény." (118), the
#   graded head; "Lehetséges irányok:" (119, foot of p4) and six dashed points
#   on p5 (124-140), quoted as examples. Line 136 ends "(5. bk)l": the stray l
#   is printed (rendered p5), lifted as printed.
# - Part III (141-150): "Tisztán, érthetően és világosan megírt esszé." (143),
#   the head.
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2013).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the instruction line and the task from the paper's lines
#   (the scheme's reprint opens with an extra „ at 115; the paper's does not).
# - III1/III2: instruction line plus title, labels left out (2010 model).
# GLYPHS: none in the lines used.
CRIT_2013 = crit((105, 106), (107, 108), (109, 110), 111)
LEAD_2013 = quote(L(103, 104), lead='The scheme prints')
SPECS[2013] = [
    R('II1', [graded(S(118), PARTP(), CRIT_2013)],
      rownote=both(LEAD_2013, examples(S(119), L(124, 127), L(128, 132), L(133, 135), S(136), L(137, 138),
                                       L(139, 140))),
      question=QP(4, 'A szöveg alapján kommentálja', Run('A cikk alapján magyarázza', 'televízió”!')),
      pages=(2, 3)),
    R('III1', [graded(S(143), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, 'A két téma közül', '„[A] tévé nemcsak')),
    R('III2', [graded(S(143), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, 'A két téma közül', 'Álmaid követése')),
]


# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y64-78; reading text "Szomszédságpolitika -
# Magyarok és a bevándorlás" p2 y105 to the byline "Dobszay János, HVG, 2013,
# adaptáció" p3 y357 (paragraphs 1-6 on p2, the end of 6 and 7 on p3); "I.
# RÉSZ (30 pont / 100 pont)" p3 y424 (Q1-Q4 on p3, Q5-Q6 on p4); "II. RÉSZ (30
# pont / 100 pont)" p4 y286; "III. RÉSZ (40 pont / 100 pont)" p4 y495, titles
# "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6, grey box): "A II. és III. részben elérhető pontok
#   az alábbi szempontok szerint" / "oszlanak meg:" (110-111) and the four
#   criteria at 30/30/30/10 % (112-117), for Parts II and III: graded.
# - Part II (118-122 reprint the head and the task): requirement line (123),
#   the graded head; "Lehetséges irányok:" (124, foot of p4), then on p5 an
#   italic lead paragraph "Azért mondhatjuk, ... Budapestre, mert" (129-134)
#   and five dashed points (135-151), all quoted as examples, in order.
# - Part III (152-162): "Tisztán, érthetően és világosan megírt esszé." (154).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2014).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the paper's instruction (it ends "!" on the paper, ":" in
#   2011-2013) and the task, from the paper's own lines.
# - III2 keeps its printed attribution "- Ralph Waldo Emerson" (same line).
# GLYPHS: none in the lines used.
CRIT_2014 = crit(112, (113, 114), (115, 116), 117)
LEAD_2014 = quote(L(110, 111), lead='The scheme prints')
SPECS[2014] = [
    R('II1', [graded(S(123), PARTP(), CRIT_2014)],
      rownote=both(LEAD_2014, examples(S(124), L(129, 134), L(135, 137), L(138, 141), L(142, 143),
                                       L(144, 148), L(149, 151))),
      question=QP(4, 'A szöveg alapján kommentálja', Run('A cikk alapján magyarázza', 'valósult meg Szent')),
      pages=(2, 3)),
    R('III1', [graded(S(154), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, 'A két téma közül', 'A sokszínűség előnyei')),
    R('III2', [graded(S(154), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, 'A két téma közül', Run('„Beutazhatjuk', 'hordoznunk, különben'))),
]


# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# (Was HOLD, resolved by the lead: the .md repaired from glyph ids by sl_glyphs.py
# hungarian, 280 -> ő, 294 -> ű, 293 -> Ű, derived by vote; line numbers unchanged.)
# The 2015 scheme's text layer is mangled in the bold/italic
# Times New Roman runs (TimesNewRoman,Bold / TimesNewRoman,Italic): it reads
# U+0118 (Ę) where the render shows ő (U+0151), U+0126 (Ħ) where it shows ű
# (U+0171), U+0125 (ĥ) where it shows Ű (U+0170) (rendered scheme p3 at 130
# dpi: "MAGYAR NYELVŰ MEGOLDÓKULCS" read "NYELVĥ" at 49; "következő" read
# "következĘ" at 51; p4/p5 "megfelelĘ", "egyszerĦek"). Every line these cards
# lift that carries ő/ű comes out mangled: the criteria lead 99 ("elérhetĘ"),
# criterion 2 (103, "megfelelĘ"), criterion 3 (105-106, "megfelelĘen",
# "összefüggĘen"), the Part II head 112 and the Part III head 141
# ("érthetĘen"), and examples 118-136 ("döntĘ", "szépségérĘl", "szereplĘket",
# "egyszerĦek", "beszĦkítenek", "elsĘsorban", "köszönhetĘen", "elĘtt"). Not
# hand-mapped (brief): needs a scheme glyph map derived from glyph ids (as
# glyphmap-polish-2015-hl.json) applied to the .md before these cards build.
# The specs below are otherwise final. The live 2015 cards I1a, I1b, I3, I5, I6
# already carry U+0118 (flagged in the live audit).
# Paper (rendered pp2-4; its text layer is clean): rule p2 y79-93; reading text
# "A bőség zavaros - ..." p2 y121 to the byline "Illényi Balázs, HVG, 2014,
# adaptáció" p3 y453 (paragraphs 1-4 on p2, 5-7 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y482; "II. RÉSZ (30 pont / 100 pont)" p4 y260; "III. RÉSZ (40 pont
# / 100 pont)" p4 y454, titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6): "A II. és III. részben elérhetĘ pontok az alábbi
#   szempontok" / "szerint oszlanak meg:" (99-100) and the four criteria at
#   30/30/30/10 % (101-107), for Parts II and III: graded.
# - Part II (108-111 reprint the head and the task): requirement line (112),
#   the graded head; "Lehetséges irányok:" (113), a lead sentence "Azért
#   mondhatjuk, hogy „ a képek elfogyasztják a valóságot”, mert:" (114) and
#   five dashed points (115-138), quoted as examples in order.
# - Part III (139-149): "Tisztán, érthetĘen és világosan megírt esszé." (141).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2015).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - III1: the paper opens the title with an English-style “ (U+201C), the
#   scheme reprints it with no quotation marks (143-144): the paper's printing
#   is the question (10f).
CRIT_2015 = crit((101, 102), (103, 104), (105, 106), 107)
LEAD_2015 = quote(L(99, 100), lead='The scheme prints')
SPECS[2015] = [
    R('II1', [graded(S(112), PARTP(), CRIT_2015)],
      rownote=both(LEAD_2015, examples(S(113), S(114), L(115, 117), L(118, 122), L(127, 132), L(133, 136),
                                       L(137, 138))),
      question=QP(4, 'A szöveg alapján kommentálja', '„ [A] képek'), pages=(2, 3)),
    R('III1', [graded(S(141), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, 'A két téma közül', Run('“Minden, amit', 'vagyok tőle.”'))),
    R('III2', [graded(S(141), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, 'A két téma közül', 'Az a leggazdagabb')),
]


# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y79-93; reading text "Nem egyedülálló
# helyzetek - ..." p2 y121 to the byline "Lindner András: HVG, 2015,
# adaptáció" p3 y480 (paragraphs 1-3 on p2, the end of 3 and 4-5 on p3; the
# footnote "1 Paradoxon: ..." p3 y764 belongs to paragraph 4); "I. RÉSZ (30
# pont / 100 pont)" p3 y557 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100
# pont)" p4 y343; "III. RÉSZ (40 pont / 100 pont)" p4 y525, titles "1.
# lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6, grey box): "A II. és III. részben elérhető pontok
#   az alábbi szempontok" / "szerint oszlanak meg:" (105-106) and the four
#   criteria at 30/30/30/10 % (107-113), for Parts II and III: graded. (The
#   exclusions file calls these "percentages of qualities ... no answer": the
#   criteria are exactly what 10b grades on.)
# - Part II (114-119 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett saját
#   vélemény." (120), the graded head; "Lehetséges irányok:" (121), a lead "A
#   szerző arra utal az alábbi mondatával, hogy:" (122) and six dashed points
#   on p5 (127-147), quoted as examples in order.
# - Part III (148-160): "Tisztán, érthetően és világosan megírt esszé." (150).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2016).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the paper's instruction (two lines, its word limit "(min.
#   100, max. 150 szóban)" inside it, no colon; the scheme's reprint adds one)
#   and the quoted sentence, from the paper's own lines.
# - III2 keeps its printed attribution line "Fintan O'Toole, The Irish Times,
#   2016. február. 22.02.2016." as the paper prints it (rendered p4; the scheme
#   prints "2016. február. 22." only).
# GLYPHS: none in the lines used.
CRIT_2016 = crit((107, 108), (109, 110), (111, 112), 113)
LEAD_2016 = quote(L(105, 106), lead='The scheme prints')
SPECS[2016] = [
    R('II1', [graded(S(120), PARTP(), CRIT_2016)],
      rownote=both(LEAD_2016, examples(S(121), S(122), L(127, 129), L(130, 131), L(132, 134), L(135, 139),
                                       L(140, 144), L(145, 147))),
      question=QP(4, Run('A szöveg alapján kommentálja', 'véve, hogy'), Run('„Az egyik', 'nincs igazi')),
      pages=(2, 3)),
    R('III1', [graded(S(150), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, 'A két téma közül', Run('“[H]a egyszer', 'soha.”'))),
    R('III2', [graded(S(150), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, 'A két téma közül', Run('A világ elég rossz', 'Fintan O'))),
]


# ====================================================================== 2017
# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y65-80, "Az elérhető maximális pontszám 100
# pont" p2 y109; reading text "Perszonalizált világ" p2 y138 to the byline
# "Szauer Tamás: HVG, 2016, adaptáció" p3 y433 (paragraphs 1-4 on p2 with the
# footnote "1 A beépített okos szenzorok ..." p2 y767, 5-7 on p3); "I. RÉSZ (30
# pont / 100 pont)" p3 y533 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100
# pont)" p4 y343 with "Kommentár (min. 100, max. 150 szóban)" y373; "III. RÉSZ
# (40 pont / 100 pont)" p4 y519, titles "1. lehetőség" / "vagy" / "2.
# lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6):
# - Criteria (p4, under Q6): "A II. és III. részben elérhető pontok az alábbi
#   szempontok" / "szerint oszlanak meg:" (112-113) and the four criteria at
#   30/30/30/10 % (114-120), for Parts II and III: graded.
# - Part II (p5; 125-129 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett saját
#   vélemény." (130), the graded head; "Lehetséges irányok:" (131), a lead "A
#   szerző azért állítja, ... mert:" (132) and eight dashed points (133-157),
#   quoted as examples in order.
# - Part III (p6, 162-174): "Tisztán, érthetően és világosan megírt esszé."
#   (164).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2017).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the paper prints the word limit only on the task's own
#   head, "Kommentár (min. 100, max. 150 szóban)" (p4 y373), then the task
#   (y402-431). Both lifted (head line + task) so the card keeps the printed
#   word limit; the lead's 2010 lifts the instruction line that carries it.
# - III2: the title's two printed sentences, the instruction "Fejtse ki ..."
#   included (it is the title as printed, p4 y739-754).
# GLYPHS: none in the lines used.
CRIT_2017 = crit((114, 115), (116, 117), (118, 119), 120)
LEAD_2017 = quote(L(112, 113), lead='The scheme prints')
SPECS[2017] = [
    R('II1', [graded(S(130), PARTP(), CRIT_2017)],
      rownote=both(LEAD_2017, examples(S(131), S(132), S(133), L(134, 137), L(138, 139), L(140, 145),
                                       L(146, 150), L(151, 152), L(153, 155), L(156, 157))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'is szól”!')), pages=(2, 3)),
    R('III1', [graded(S(164), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, 'A két téma közül', Run('„Egy ponton', 'tegye meg!”'))),
    R('III2', [graded(S(164), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, 'A két téma közül', Run('„A véleményem', 'az álláspontot a modern'))),
]


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y65-80; reading text "Jólétet mindenkinek!"
# p2 y109 to the byline "Weyer Béla: HVG, 2017, adaptáció" p3 y404
# (paragraphs 1-6 on p2, the end of 6 and 7-8 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y489 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100 pont)" p4
# y329 with "Kommentár (min. 100, max. 150 szóban)" y358; "III. RÉSZ (40 pont /
# 100 pont)" p4 y475, titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6):
# - Criteria: the lead "A II. és III. részben elérhető pontok az alábbi
#   szempontok szerint oszlanak meg:" at the foot of p4 (124), the four
#   criteria at 30/30/30/10 % at the top of p5 (129-135), for Parts II and
#   III: graded.
# - Part II (p5; 136-140 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett saját
#   vélemény." (141), the graded head; "Lehetséges irányok:" (142), a lead
#   "Azért nem minden úgy valósult meg, ... mert:" (143-145) and eight dashed
#   points (146-177; the sixth runs over the page break, 162-164 + 169-170),
#   quoted as examples in order.
# - Part III (p6, 178-191): "Tisztán, érthetően és világosan megírt esszé."
#   (180).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2018).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: head line "Kommentár (min. 100, max. 150 szóban)" + the
#   task, as 2017 (the task itself also says "min. 100 szóban").
# - III1: the paper prints the title with no closing stop; the scheme's reprint
#   opens with a doubled „„ (182). The paper's is the question.
# - III2: the title's three printed sentences, the instruction included.
# GLYPHS: none in the lines used.
CRIT_2018 = crit((129, 130), (131, 132), (133, 134), 135)
LEAD_2018 = quote(S(124), lead='The scheme prints')
SPECS[2018] = [
    R('II1', [graded(S(141), PARTP(), CRIT_2018)],
      rownote=both(LEAD_2018, examples(S(142), L(143, 145), L(146, 149), L(150, 154), S(155), L(156, 161),
                                       J(L(162, 164), L(169, 170)), L(171, 172), L(173, 177))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'megjelent, mindenkinek')), pages=(2, 3)),
    R('III1', [graded(S(180), PARTP(), CRIT_2018)], rownote=LEAD_2018,
      question=QP(4, 'A két téma közül', Run('„Az ország csak', 'elveinek, ha a jelenleginél'))),
    R('III2', [graded(S(180), PARTP(), CRIT_2018)], rownote=LEAD_2018,
      question=QP(4, 'A két téma közül', Run('A ruha teszi', 'véleményét egy min.'))),
]


# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80 ("Olvassa el a következő szöveget, és
# válaszoljon érthetően magyarul az I., II. és III. részben feltett
# kérdésekre!"); reading text "Tárt karokkal? – Magyarország ..." p2 y124 to
# the byline "Muharay Katalin: HVG, 2018, adaptáció" p3 y372 (paragraphs 1-5
# on p2, the end of 5 and 6-7 on p3); "I. RÉSZ (30 pont / 100 pont)" p3 y415;
# "II. RÉSZ (30 pont / 100 pont)" p4 y241 with "Kommentár (min. 100, max. 150
# szóban)" y270; "III. RÉSZ (40 pont / 100 pont)" p4 y446, titles "1.
# lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts (paper or scheme).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6, grey-boxed lead): "A II. és III. részben elérhető
#   pontok az alábbi szempontok szerint oszlanak meg:" (116) and the four
#   criteria at 30/30/30/10 % (117-123), for Parts II and III: both graded
#   (10b), 9/9/9/3 of 30 and 12/12/12/4 of 40, as the lead's 2010.
# - Part II (p5; 128-132 reprint the head, the task and the sentence): the
#   requirement line "A minimum 100, maximum 150 szóban tisztán, érthetően
#   kifejtett, szövegen alapuló saját vélemény." (133-134), the graded head;
#   "Lehetséges irányok:" (135, italic), the sub-head "Talán igen:" (136), four
#   dashed points (137-146) and "Talán nem, ha ..." (147), quoted as examples in
#   order, sub-head included.
# - Part III (p5, 148-160): "Tisztán, érthetően és világosan megírt esszé."
#   (150, bold), the graded rows' head; each title reprinted with "Egyéni válasz
#   minimum 300 szóban." (155, 160), left to the head as in 2010.
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2019).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. The live Part I cards
#   carry [3]: flagged (P) in the live audit.
# - II1's question: the head line "Kommentár (min. 100, max. 150 szóban)", the
#   task (two printed lines) and the sentence to comment on, as 2018; the census
#   glues the part head's "(30 pont / 100 pont)" in front, so cut from the
#   paper's own lines (QP).
# - III1/III2: the instruction line plus the title (III1 with its printed
#   attribution "(Barack Obama)"); the labels "1. lehetőség" / "2. lehetőség"
#   left out, as the lead's 2010.
# GLYPHS: none (á é í ó ö ő ú ü ű read clean in paper and scheme; no code point
#   outside the Hungarian alphabet in the scheme .md).
CRIT_2019 = crit((117, 118), (119, 120), (121, 122), 123)
LEAD_2019 = quote(S(116), lead='The scheme prints')
SPECS[2019] = [
    R('II1', [graded(L(133, 134), PARTP(), CRIT_2019)],
      rownote=both(LEAD_2019, examples(S(135), S(136), S(137), L(138, 139), L(140, 142), L(143, 146), S(147))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'szóban!'), 'Talán Magyarországnak'),
      pages=(2, 3)),
    R('III1', [graded(S(150), PARTP(), CRIT_2019)], rownote=LEAD_2019,
      question=QP(4, 'A két téma közül', Run('A válság az', 'és falakat'))),
    R('III2', [graded(S(150), PARTP(), CRIT_2019)], rownote=LEAD_2019,
      question=QP(4, 'A két téma közül', Run('Egy év halasztást', 'Esszéjében'))),
]


# ====================================================================== 2020
# ================================================================ 2020 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y85 ("Válaszolj érthetően magyarul az I., II.
# és III. részben feltett kérdésekre!"); reading text "Így cifrázták ők. A
# bulváretalon: Az Est." p2 y118 to the byline "Serf András, HVG (adaptáció)"
# p3 y306 (paragraphs 1-4 on p2, the end of 4 and 5 on p3); "I. RÉSZ (30 pont/
# 100 pont)" p3 y362; "II. RÉSZ" p4 y75 with "(30 pont/ 100 pont)" at x424 on
# the same line; "III. RÉSZ (40 pont/ 100 pont)" p4 y266, titles "1.
# lehetőség" / "vagy" / "2. lehetőség".
# PRICES:
# - II1: the text layer sets the head as three cells, "II." (x57), "RÉSZ"
#   (x83) and "(30 pont/ 100 pont)" (x424), so the census reads no Part II
#   total and PARTP() refuses ("part heads print []"). Rendered p4: "II. RÉSZ
#   (30 pont/ 100 pont)" on one line. Priced from that printed cell:
#   PaperP(4, '(30 pont/', k=0) = 30 (the FIRST worded price; k=-1 would read
#   the paper's 100). The scheme prints the same "(30 pont / 100 pont)" (114).
# - III1/III2: "(40 pont/ 100 pont)" (PARTP, read cleanly).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6, grey-boxed lead): "A II. és III. részben elérhető
#   pontok az alábbi szempontok szerint oszlanak meg:" (105) and the four
#   criteria at 30/30/30/10 % (106-112), for Parts II and III: graded.
# - Part II (p4-5; 113-118 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett, szövegen
#   alapuló saját vélemény." (119-120), the graded head; "Lehetséges irányok:"
#   (125, top of p5) and seven dashed points (126-139), quoted as examples.
# - Part III (p5, 140-151): "Tisztán, érthetően és világosan megírt esszé."
#   (143).
# SHAPES: II1, III1, III2 graded(head, <printed total>, CRIT_2020).
# JUDGEMENT CALLS:
# - The scheme reprints the Part II task in other words ("Fejtsd ki véleményedet
#   minimum 100 szóban az alábbi témáról!", 116) than the paper ("Fejtsd ki
#   álláspontodat min. 100 szóban a 2. bekezdésben található alábbi mondattal
#   kapcsolatban!", p4 y135-150): the paper's is the question (10f). The
#   scheme's head adds "maximum 150 szóban", which the paper does not print; it
#   is the scheme's own requirement line, kept as the graded head.
# - II1's question: "Kommentár", the task (two lines) and the quoted sentence
#   (two lines), cut from the paper (the census glues "(30 pont/ 100 pont)").
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. The live Part I cards
#   carry [3]: flagged (P).
# GLYPHS: none. The paper sets U+2010 HYPHEN ("színe‐javának", "1938‐ban"), a
#   real hyphen on the render; not in any line used here.
CRIT_2020 = crit((106, 107), (108, 109), (110, 111), 112)
LEAD_2020 = quote(S(105), lead='The scheme prints')
PART2_2020 = PaperP(4, '(30 pont/', k=0)
SPECS[2020] = [
    R('II1', [graded(L(119, 120), PART2_2020, CRIT_2020)], total=PART2_2020,
      # the scheme rewords the task (116): quoted, the paper's words stand (10f; second reader); the bare
      # sub-head "Kommentár" left out, as 2010-2016 (2017-2019, 2023-2026 keep theirs: it prints the word limit)
      rownote=both(quote(S(116), lead='The scheme reprints the task as'), LEAD_2020,
                   examples(S(125), L(126, 127), L(128, 129), L(130, 131), L(132, 133), L(134, 135),
                            L(136, 137), L(138, 139))),
      question=QP(4, Run('Fejtsd ki álláspontodat', 'kapcsolatban!'), Run('„Azonban mit sem', 'nem kellően')),
      pages=(2, 3)),
    R('III1', [graded(S(143), PARTP(), CRIT_2020)], rownote=LEAD_2020,
      question=QP(4, 'A két téma közül', 'Mi a konfliktus')),
    R('III2', [graded(S(143), PARTP(), CRIT_2020)], rownote=LEAD_2020,
      question=QP(4, 'A két téma közül', Run('Figyelembe véve', 'sztárokat, mit'))),
]


# ====================================================================== 2021
# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this TWO-PART
# sitting, II1 and II2 (Part II is the essay: cited Section II Q1/Q2, filed as
# Part III's is). Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80 ("Válaszoljon mindkét részre: az I. és
# a II. részre is!" / "Minden válaszát magyarul írja le!"), "Max. 70 pont";
# "I. RÉSZ (30 pont / 70 pont)" p2 y124 over the reading text "Elveszett
# paradicsomok" p2 y227 to the byline "Nagy Gábor: HVG, 2018, 2019, adaptáció"
# p3 y681; Q1 a)-b) p3, c)-e) and Q2-Q6 p4; "II. RÉSZ (40 pont / 70 pont)" p4
# y475, "Esszé", the instruction "A két téma közül válasszon ki egyet, és írjon
# egy minimum 300 szavas esszét!" (y534) and two titles "1. lehetőség" /
# "vagy" / "2. lehetőség", each with an attribution line set at the right
# ("- Patrick James Rothfuss: A bölcs ember félelme" y607, "- Greta Thunberg"
# y721).
# PRICES: "(40 pont / 70 pont)" on the part head (PARTP). Nothing else.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5): NO criteria anywhere in this
# scheme (no "A II. ... részben elérhető pontok" lead, no percentages). Under
# "II. RÉSZ (40 pont / 70 pont)" / "Esszé" (127-128) it prints only the
# descriptive line "Tisztán, érthetően és világosan megírt esszé." (129) and,
# under each reprinted title, "Egyéni válasz minimum 300 szóban." (133, 138).
# SHAPES: II1, II2 unprinted(note quoting both lines) at the paper's 40 (R4;
# brief: "nothing printed for that part (or only a descriptive line)").
# JUDGEMENT CALLS:
# - Questions: the instruction line, then the title and its printed
#   attribution line, as the paper prints them (QP); the scheme reprints title 1
#   without its quotation marks and title 2's attribution as "(Greta
#   Thunberg)": punctuation only, not quoted.
# - No `pages`: a two-part sitting's Part II is the essay (sl_lib attaches no
#   reading text). LIVE PAGES: the live 2021 cards carry [2, 3], which agree
#   with the render.
# GLYPHS: none. The scheme sets its text in NO-BREAK SPACES (U+00A0, 621 of
#   them) and U+2010 HYPHEN ("jegy‐ és", "egyetért‐e"), real hyphens on the
#   render; neither is a mangled letter.


def _essay_2021(d):
    return (f'Under Part II the scheme prints only “{S(129).text(d)}” and, under each title, “{S(133).text(d)}” '
            f'It prints no criteria and no split of the part\'s marks.')


ESSAY_2021 = 'A két téma közül'
SPECS[2021] = [
    R('II1', [unprinted(_essay_2021)], question=QP(4, ESSAY_2021, '„Egy hosszú út', '- Patrick James')),
    R('II2', [unprinted(_essay_2021)], question=QP(4, ESSAY_2021, 'Nem találhatsz ki', '- Greta Thunberg')),
]


# ====================================================================== 2022
# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this TWO-PART
# sitting, II1 and II2 (Part II is the essay). Live: I1a-e, I2-I6 (10 cards);
# not touched here (see the live audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80 ("Válaszoljon mindkét részre: az I. és
# a II. részre is!" / "Minden válaszát magyarul írja le!"); reading text
# "Poszttraumás nemzedék" p2 y124 to the byline "Balla Györgyi, Bihari Ádám:
# HVG, 2020, adaptáció" p3 y519; "I. RÉSZ (30 pont / 70 pont)" p3 y563 (Q1 on
# p3, Q2-Q6 on p4); "II. RÉSZ (40 pont / 70 pont)" p4 y431, "Esszé", the
# instruction (y519) and titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: "(40 pont / 70 pont)" on the part head (PARTP). Nothing else.
# WHAT THE SCHEME PRINTS (rendered scheme p5):
# - Above Part II, grey-boxed: "A II. részben elérhető pontok az alábbi
#   szempontok szerint oszlanak meg:" (127) and the four criteria "1. Megértés
#   – ...", "2. A válasz koherenciája – ...", "3. Nyelvi képesség – ...", "4.
#   Nyelvhelyesség – ..." (128-134) with NO percentages and no marks (the 2019
#   and 2023 schemes print "– 30%" etc. on the same criteria; this one does
#   not). Stated for Part II.
# - Under "II. RÉSZ (40 pont / 70 pont)" (135) it reprints "Esszé", the
#   instruction and the two titles (136-143) and prints nothing else (no
#   "Tisztán, érthetően ..." line this year).
# SHAPES: coordinator ruling F (criteria printed for the part without
#   percentages, Bulgarian 2021): the four criteria as shown rows on the
#   paper's 40 (whole=True, questionTotal), their lead quoted in the rownote.
# JUDGEMENT CALLS:
# - The criteria rows keep their printed numbers "1." to "4.", as Bulgarian and
#   Estonian 2021 keep theirs.
# - Questions: the instruction line, then the title (title 1 with its printed
#   attribution "(Andrew Matthews)"); the census reads II2 as "2. lehetőség"
#   only, so both are cut from the paper's own lines (QP).
# - No `pages` (the essay of a two-part sitting). LIVE PAGES: the live Part I
#   cards carry [3]; the text runs pp2-3: flagged (P).
# GLYPHS: none. U+00A0 spacing and U+2010 HYPHEN ("Z‐nek", "it‐tőkével",
#   "egyetért‐e") in scheme and paper are real hyphens on the render.
CRIT_ROWS_2022 = (L(128, 129), L(130, 131), L(132, 133), S(134))


def _crit_note_2022(d):
    return (f'Under “{S(127).text(d)}” the scheme prints the four criteria with no marks or percentages beside them, '
            f'so they are shown and the part is scored on its printed total. Under Part II itself it reprints the '
            f'instruction and the two titles and prints nothing else.')


ESSAY_2022 = 'A két téma közül'
SPECS[2022] = [
    R('II1', [shown(c) for c in CRIT_ROWS_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, Run('Az élet attól', 'elsorvasztja'))),
    R('II2', [shown(c) for c in CRIT_ROWS_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, 'Hogyan jön létre')),
]


# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80; reading text "Kütyühalmokon kinőtt
# romantika" p2 y124 to the byline "Csatlós Hanna: HVG, 2022, adaptáció" p3
# y460; "I. RÉSZ (30 pont / 100 pont)" p3 y503 (Q1-Q2 p3, Q3-Q6 p4); "II. RÉSZ
# (30 pont / 100 pont)" p4 y343 with "Kommentár (min. 100, max. 150 szóban)"
# y373; "III. RÉSZ (40 pont / 100 pont)" p4 y519, titles "1. lehetőség" /
# "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp5-6):
# - Criteria (top of p5, grey-boxed lead): "A II. és III. részben elérhető
#   pontok az alábbi szempontok szerint oszlanak meg:" (131) and the four
#   criteria at 30/30/30/10 % (132-138), for Parts II and III: graded.
# - Part II (p5; 139-144 reprint the head, the task and the sentence):
#   requirement line "A minimum 100, maximum 150 szóban tisztán, érthetően
#   kifejtett, szövegen alapuló saját vélemény." (145-146), the graded head;
#   "Lehetséges irányok:" (147) and five dashed points (148-162), quoted as
#   examples in order.
# - Part III (p6, 167-178): "Tisztán, érthetően és világosan megírt esszé."
#   (169).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2023).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged (P).
# - II1's question: head line, task (two lines), and the quoted sentence (two
#   lines), cut from the paper (QP).
# - III1: the paper prints the title in quotation marks with "(Amy Harmon)"; the
#   scheme reprints it without them (171): the paper's is the question.
# GLYPHS: none. U+00A0 spacing (954) and U+2010 HYPHEN ("gyermek‐ és",
#   "Netflix‐sorozat") in the scheme are real hyphens on the render.
CRIT_2023 = crit((132, 133), (134, 135), (136, 137), 138)
LEAD_2023 = quote(S(131), lead='The scheme prints')
SPECS[2023] = [
    R('II1', [graded(L(145, 146), PARTP(), CRIT_2023)],
      rownote=both(LEAD_2023, examples(S(147), L(148, 149), L(150, 153), L(154, 155), L(156, 159), L(160, 162))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'szóban!'), Run('„Az általunk', 'közül a Z')),
      pages=(2, 3)),
    R('III1', [graded(S(169), PARTP(), CRIT_2023)], rownote=LEAD_2023,
      question=QP(4, 'A két téma közül', '„Olvasás közben')),
    R('III2', [graded(S(169), PARTP(), CRIT_2023)], rownote=LEAD_2023,
      question=QP(4, 'A két téma közül', Run('„A legtöbb technikai', 'vívmányok túlnőnek'))),
]


# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80; reading text "Csak azért is
# kisajátítás" p2 y124 to the byline "- Fülöp István: HVG, 2023, adaptáció" p3
# y372; "I. RÉSZ (30 pont / 100 pont)" p3 y430 (Q1-Q3 p3, Q4-Q6 p4); "II. RÉSZ
# (30 pont / 100 pont)" p4 y329 with "Kommentár (min. 100, max. 150 szóban)"
# y358; "III. RÉSZ (40 pont / 100 pont)" p4 y490, titles "1. lehetőség" /
# "vagy" / "2. lehetőség" (title 2's attribution "(Csányi Vilmos)" set at the
# right on its own line, y727).
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp5-6):
# - Criteria (p5, under Q6): "A II. és III. részben elérhető pontok az alábbi
#   szempontok szerint oszlanak meg:" (138) and the four criteria at 30/30/30/10
#   % (139-145), for Parts II and III: graded.
# - Part II (p5-6; 146-151 reprint the head, the task and the sentence):
#   requirement line (152-153), the graded head; "Lehetséges irányok:" (154) and
#   seven dashed points (155-177; the first ends p5, 155-157, the rest on p6
#   from 162), quoted as examples in order.
# - Part III (p6, 178-189): "Tisztán, érthetően és világosan megírt esszé."
#   (180).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2024).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged (P).
# - III2: the title, then its attribution line "(Csányi Vilmos)" as printed (the
#   paper sets it on a line of its own); the scheme reprints the title without
#   quotation marks (187-188): the paper's is the question.
# - Example 2 ends "... szempontokat sem, (2. bk);" with a stray comma: the
#   scheme's own punctuation, quoted as printed.
# GLYPHS: none. U+00A0 spacing and U+2010 HYPHEN ("többé‐kevésbé",
#   "Airbnb‐n") are real hyphens on the render.
CRIT_2024 = crit((139, 140), (141, 142), (143, 144), 145)
LEAD_2024 = quote(S(138), lead='The scheme prints')
SPECS[2024] = [
    R('II1', [graded(L(152, 153), PARTP(), CRIT_2024)],
      rownote=both(LEAD_2024, examples(S(154), L(155, 157), L(162, 165), L(166, 167), L(168, 170), L(171, 173),
                                       L(174, 175), L(176, 177))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'szóban!'), '„A megosztáson alapuló'),
      pages=(2, 3)),
    R('III1', [graded(S(180), PARTP(), CRIT_2024)], rownote=LEAD_2024,
      question=QP(4, 'A két téma közül', Run('A megosztási gazdaság', 'fenntarthatóbb fogyasztási'))),
    R('III2', [graded(S(180), PARTP(), CRIT_2024)], rownote=LEAD_2024,
      question=QP(4, 'A két téma közül', '„A közösség az egyén', '(Csányi Vilmos)')),
]


# ====================================================================== 2025
# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I3, II1, III1, III2. Live: I1a-e, I2, I4-I6 (9 cards); not touched here (see
# the live audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80; reading text "Van-e még életre
# szóló?" p2 y124 to the byline "Csendes-Erdei Emese: HVG, 2024, adaptáció" p3
# y518; "I. RÉSZ (30 pont / 100 pont)" p3 y561 (Q1 p3, Q2-Q6 p4); "II. RÉSZ
# (30 pont / 100 pont)" p4 y358 with "Kommentár (min. 100, max. 150 szóban)"
# y387; "III. RÉSZ (40 pont / 100 pont)" p4 y534, titles "1. lehetőség" /
# "vagy" / "2. lehetőség".
# PRICES:
# - I3: "(5 pont)" at the right of its own line (p4 x453 y109), read by the
#   census (PP); the scheme prints the same "(5 pont)" (85).
# - II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the part
#   heads (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6):
# - I3 (p4, 85-92): the lead "Válasz a 3. bekezdésben: A barátság
#   kialakulásának akadálya lehet" (86) and five obstacles lettered "a," to
#   "e," (87-92), one per line, no per-point marks. (The census found no scheme
#   ask for I3 at the paper's address; the scheme's Q3 reprint, 85, is the
#   paper's question word for word.)
# - NO criteria anywhere in this scheme (no "A II. és III. részben ..." lead,
#   no percentages).
# - Part II (p6; 145-149 reprint the head, the sentence and the task): the
#   requirement line "A minimum 100, maximum 150 szóban tisztán, érthetően
#   kifejtett, szövegen alapuló saját vélemény." (150-151), "Lehetséges
#   irányok:" (152, italic) and six dashed points (153-164).
# - Part III (p6, 165-174): only "Tisztán, érthetően és világosan megírt
#   esszé." (167) and, under each title, "Egyéni válasz minimum 300 szóban."
#   (170, 174).
# SHAPES:
# - I3: five shown rows (one per lettered obstacle, the letters cut off),
#   whole=True on the paper's 5 (points with no per-point marks); the lead in
#   the rownote. Not one(): the scheme lists points, not one stated answer.
# - II1: the six dashed points as shown rows, whole=True on the paper's 30
#   (indicative points the scheme prices only as a whole, 10a); the requirement
#   line and the heading "Lehetséges irányok:" in the rownote (a heading never
#   in a row). Not graded: no criteria are printed this year.
# - III1/III2: unprinted(note quoting the two descriptive lines), R4.
# JUDGEMENT CALLS:
# - I3 rows keep the scheme's trailing ";" (87-90) and its unstopped d) line
#   (91): punctuation as printed.
# - II1 point 3 ends "... az életében, (3. bk);" and point 4 prints no "(bk)"
#   reference: as printed.
# - Reading text pp2-3 (rendered); pages=(2, 3) on I3 and II1. The live Part I
#   cards carry [3]: flagged (P).
# - II1's question: head line, the quoted sentence, then the task (two lines),
#   in the paper's order (QP).
# GLYPHS: none (the scheme .md carries no code point outside the alphabet).
#   NOTE (not a glyph fault): the paper prints Q1 e) "örödként" where the scheme
#   prints "ördögként"; and the scheme prints above Q1 (62-63) that every
#   candidate was given e)'s mark. Live I1e only; reported in the live audit.


def _comment_2025(d):
    return (f'The scheme prints no criteria for this part. It prints “{L(150, 151).text(d)}” and, under its '
            f'heading “{S(152).text(d)}”, the points shown, as examples, not a checklist; the part is scored on '
            f'its printed total.')


def _essay_2025(d):
    return (f'Under Part III the scheme prints only “{S(167).text(d)}” and, under each title, “{S(170).text(d)}” '
            f'It prints no criteria and no split of the part\'s marks.')


SPECS[2025] = [
    R('I3', [shown(L(87, 88, after='a, ')), shown(S(89, after='b, ')), shown(S(90, after='c, ')),
             shown(S(91, after='d, ')), shown(S(92, after='e, '))], whole=True,
      rownote=quote(S(86), lead='The scheme opens its answer with'), pages=(2, 3)),
    R('II1', [shown(L(153, 154)), shown(L(155, 156)), shown(L(157, 158)), shown(S(159)), shown(L(160, 161)),
              shown(L(162, 164))], whole=True, rownote=_comment_2025,
      question=QP(4, 'Kommentár (min.', '„A tartós barátság', Run('Kommentálja ezt az', 'alapján!')),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2025)], question=QP(4, 'A két téma közül', 'Fontos emberek az')),
    R('III2', [unprinted(_essay_2025)], question=QP(4, 'A két téma közül', 'Bátorság kell ahhoz')),
]


# ====================================================================== 2026
# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2019-2026.json).
# Paper (rendered pp2-4): rule p2 y65-80; reading text "Testvériesen vagy
# fele-fele?" p2 y109 to the byline "Szabó Yvette: HVG, 2023, adaptáció" p3
# y505; "I. RÉSZ (30 pont / 100 pont)" p3 y549 (Q1 p3, Q2-Q6 p4); "II. RÉSZ
# (30 pont / 100 pont)" p4 y358 with "Kommentár (min. 100, max. 150 szóban)"
# y387; "III. RÉSZ (40 pont / 100 pont)" p4 y490, titles "1. lehetőség" /
# "vagy" / "2. lehetőség" (title 2's "(Csányi Vilmos)" on a line of its own at
# the right, y752).
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp6-7):
# - NO criteria anywhere in this scheme (no lead, no percentages).
# - Part II (p6-7; 134-138 reprint the head, the task and the sentence): the
#   requirement line "A minimum 100, maximum 150 szóban tisztán, érthetően
#   kifejtett, szövegen alapuló saját vélemény." (139-140), "Lehetséges
#   irányok:" (141) and six dashed points (142-166; the fourth runs over the
#   page break, 153-154 + 159-160).
# - Part III (p7, 167-181): under each title only "Egyéni válasz minimum 300
#   szóban." and "Tisztán, érthetően és világosan megírt esszé." (173-174,
#   180-181).
# SHAPES: II1 six shown rows, whole=True on the paper's 30 (indicative points,
#   10a; as 2025), the requirement line and heading in the rownote; III1/III2
#   unprinted(note quoting the two descriptive lines), R4.
# JUDGEMENT CALLS:
# - II1 point 4 joins its two halves across the page break (J(L(153, 154),
#   L(159, 160)); the page number "6" and page marker, 155-158, left out).
# - II1's question: head line, task, sentence, as printed (QP).
# - III2: the title (two lines) and its attribution line "(Csányi Vilmos)", as
#   printed.
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged (P).
# GLYPHS: none (the scheme .md carries no code point outside the alphabet; the
#   live I4 row's "közösségéíptés" is the scheme's own misprint, 101, on the
#   render too).


def _comment_2026(d):
    return (f'The scheme prints no criteria for this part. It prints “{L(139, 140).text(d)}” and, under its '
            f'heading “{S(141).text(d)}”, the points shown, as examples, not a checklist; the part is scored on '
            f'its printed total.')


def _essay_2026(d):
    return (f'Under Part III the scheme prints only, under each title, “{S(173).text(d)}” and '
            f'“{S(174).text(d)}” It prints no criteria and no split of the part\'s marks.')


SPECS[2026] = [
    R('II1', [shown(L(142, 143)), shown(L(144, 147)), shown(L(148, 152)), shown(J(L(153, 154), L(159, 160))),
              shown(L(161, 164)), shown(L(165, 166))], whole=True, rownote=_comment_2026,
      question=QP(4, 'Kommentár (min.', 'Kommentálja ezt a kijelentést', 'Változóban van'),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2026)],
      question=QP(4, 'A két téma közül', Run('A közösségi gazdaságon', 'térben éljük'))),
    R('III2', [unprinted(_essay_2026)],
      question=QP(4, 'A két téma közül', Run('„A jelenlegi kultúrában', 'őszülsz, festesd'), '(Csányi Vilmos)')),
]
