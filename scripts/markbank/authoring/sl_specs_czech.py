#!/usr/bin/env python3
"""Reviewed specs for the Czech classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/czech/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2010 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2010-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "Část 1 [30 bodů]" (p2 y235) over the reading text
# "Mazej ze školy" (p2 y259, eight numbered paragraphs to "(upraveno podle
# www.respekt.cz)" p3 y490); questions from p3 y539: Q1 "[5 bodů]" over a)-e)
# (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4 y209), the commentary,
# ONE task with no number; "Část 3 [40 bodů]" (p4 y365), the instruction and
# two titles "1."/"2.".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I2 "[5 bodů]" at the end of the question's last line (p3 y682,
#   "Vysvětlete na základě textu. [5 bodů]"): PaperP.
# - I3 "[5 bodů]" at the end of "základě textu. [5 bodů]" (p3 y722): PaperP.
# - I4 "[5 bodů]" at the end of "Co tuto situaci činí tak absurdní? [5 bodů]"
#   (p3 y761): PaperP.
# - I5 "[5 bodů]" on a line of its own under the question (p4 x467 y106).
#   PY cannot read it (its cell pattern takes "bodu"/"bod", not "bodů": PY(4,
#   106) returns 0 cells); it is the only line of p4 opening "[5 bodů]", so
#   PaperP(4, '[5 bodů]') reads the printed cell itself.
# - I6 "[5 bodů]" at the end of the question's own line (p4 y131): PaperP.
# - II: the part head "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40
#   bodů]" (PARTP). The scheme prints the same totals on its own heads (68, 78).
# WHAT THE SCHEME PRINTS (rendered scheme pp2-3; answers in a smaller type):
# - Q2 (25-26 reprint the question, "[5 bodů]"): one paragraph, 27-31 ("Přístup
#   ke vzdělání nebyl svobodný. ... podepisoval petice apod.").
# - Q3 (32-33): one paragraph, 34-37.
# - Q4 (38-39): one paragraph, 40-43.
# - Q5 (44-46): one paragraph, 47-49.
# - Q6 (54-55, p3): one paragraph, 56-60.
#   No bullet, no split, no mark inside any of them: model answers (10a).
# - Criteria (p3, 61-67, between Part I and Part II): "Poznámka: V částech 2 a
#   3 jsou odpovědi posuzovány podle následujích kritérií:" -- for Parts 2 AND
#   3 -- then 1. "– 30 %." (62), 2. "– 30 %." (63-64), 3. "– 30 %." (65-66,
#   the percentage wrapped onto its own line), 4. "– 10 %." (67): all four
#   printed, 100 %.
# - Part II (68-72 reprint the head and the task): the descriptive line
#   "Správný, plynulý komentář o minimálně 100 slovech." (73, normal type),
#   then one paragraph of content in the smaller type (74-77, "Bubliny jsou
#   něco velmi lehkého ...").
# - Part III (78-81 reprint the head, the instruction and both titles): one
#   descriptive line only (82-83, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the paper's printed
#   5 (10a; the brief: never an exclusion, never split where the scheme does
#   not split).
# - II: graded on the four criteria (10b): 30/30/30/10 % of the paper's 30 =
#   9 / 9 / 9 / 3. Head: the part's own descriptive line (73). The criteria's
#   lead quoted (it names the parts they serve) and the content paragraph
#   quoted as examples, not a checklist (10a).
# - III1/III2: graded (10b): 30/30/30/10 % of 40 = 12 / 12 / 12 / 4; head the
#   part's descriptive line (82-83); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2-I6 shown (self-assessed), not one(): each is a model paragraph the
#   scheme prices only as a whole (brief: 10a, whole=True). Bulgarian 2013 I6
#   and 2015 I2-I6 claim such a paragraph as one row; the brief for Czech
#   settles the other way.
# - Part II is keyed 'II' (cited "Section II") as the census keys it; its
#   question is the census's text (checked against p4: the quotation and the
#   task, no price).
# - Part III questions: the instruction and the title, cut from p4 (the census
#   gives the bare title).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none (no character outside Czech letters and punctuation in either
# text layer). Printed as such on the render, lifted as printed: "následujích"
# (61, the criteria's lead, for "následujících"), "souvislousti" (42, Q4's
# row), "lehkého lehkého" (74, a doubled word in Part II's content), "a a
# vhodnou" (63, a doubled word in criterion 2).

CRIT_2010 = crit(62, (63, 64), (65, 66), 67)
LEAD_2010 = quote(S(61, after='Poznámka: '), lead='The scheme prints')
ESSAY_2010 = 'Napište esej'

SPECS[2010] = [
    R('I2', [shown(L(27, 31))], whole=True, total=PaperP(3, 'Vysvětlete na základě textu.'), pages=(2, 3)),
    R('I3', [shown(L(34, 37))], whole=True, total=PaperP(3, 'základě textu.'), pages=(2, 3)),
    R('I4', [shown(L(40, 43))], whole=True, total=PaperP(3, 'Co tuto situaci'), pages=(2, 3)),
    R('I5', [shown(L(47, 49))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I6', [shown(L(56, 60))], whole=True, total=PaperP(4, '6. Autor popisuje'), pages=(2, 3)),
    R('II', [graded(S(73), PARTP(), CRIT_2010)],
      rownote=both(LEAD_2010, examples(None, L(74, 77))), pages=(2, 3)),
    R('III1', [graded(L(82, 83), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, ESSAY_2010, '1. Svoboda')),
    R('III2', [graded(L(82, 83), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, ESSAY_2010, '2. Nikdo')),
]


# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2011-hl-i-1); not
# touched.
# Paper (rendered pp2-4): an italic lead-in and "Část 1 [30 bodů]" on p2, the
# reading text "Smlouva s rodiči" from p2 to its byline "Jan-Michal Mleziva
# (nar. 1965), učitel" / "(upraveno podle Rodina a škola 8/2010)" (p3
# y495-519); questions from p3 y562: Q1 "[5 bodů]" over a)-e) (live); Q2-Q6
# "[5 bodů]" each; "Část 2 [30 bodů]" (p4 y270), the commentary, ONE task with
# no number; "Část 3 [40 bodů]" (p4 y394), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I2 and I3: the paper prints each "[5 bodů]" on a line of its own under the
#   question (p3 x480 y693 and p3 x480 y748; rendered p3, right margin). Two
#   lines of p3 open "[5 bodů]", so PaperP cannot single either out, and PY
#   cannot read the cell (its cell pattern takes "bodu"/"bod", not "bodů").
#   Priced from the scheme's own printed "[5 bodů]" on the question's reprint
#   (RX: line 29 "mysli. [5 bodů]", line 35 "na základě textu. [5 bodů]"),
#   the same 5 the paper prints. If the lead adds "bodů" to PY's cell pattern,
#   these become PY(3, 693) and PY(3, 748).
# - I4 "[5 bodů]" on a line of its own (p4 x480 y77), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - I5 "[5 bodů]" at the end of "názor na toto tvrzení. [5 bodů]" (p4 y131),
#   I6 at the end of "rodiče. [5 bodů]" (p4 y200): PaperP.
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5; answers in italics):
# - Q2 (28-29 reprint): one paragraph, 30-32. Q3 (33-35): one paragraph,
#   36-40. Q4 (41-42): one paragraph, 43-50. Q5 (55-57, p4): one paragraph,
#   58-64. Q6 (65-67): one paragraph, 68-71. No split, no mark inside any:
#   model answers (10a).
# - Criteria (p4, 72-78): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30%." (73),
#   "– 30%." (74-75), "– 30%." (76-77, wrapped), "– 10%." (78): 100 %.
# - Part II (79-82 reprint the head and the task): the bold descriptive line
#   "Správný, plynulý komentář o minimálně 100 slovech." (83), then one italic
#   paragraph of content (84-87, "Souhlas, nesouhlas. Dříve měli učitelé ...").
# - Part III (p5, 92-93 the head and the instruction): the bold descriptive
#   line "Jasně psaná kompozice, ..." (94-95) printed ABOVE the two titles
#   (96-98).
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line (83);
#   the criteria's lead quoted; the paragraph quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive
#   line (94-95); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2/I3 priced from the scheme (RX), not the paper: the paper's cells are
#   printed but not readable by the selectors this branch has (see PRICES).
# - Part III title 2 is the quotation and its attribution line (p4 y476-490),
#   joined.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer. Printed as such (rendered), lifted as
# printed: "ústě" (44, Q4's row; for "úctě"), "vykovává" (61, Q5's row).

CRIT_2011 = crit(73, (74, 75), (76, 77), 78)
LEAD_2011 = quote(S(72, after='Poznámka: '), lead='The scheme prints')
ESSAY_2011 = 'Napište esej'
BODU = r'\[(\d+) bodů\]'

SPECS[2011] = [
    R('I2', [shown(L(30, 32))], whole=True, total=RX(29, BODU), pages=(2, 3)),
    R('I3', [shown(L(36, 40))], whole=True, total=RX(35, BODU), pages=(2, 3)),
    R('I4', [shown(L(43, 50))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I5', [shown(L(58, 64))], whole=True, total=PaperP(4, 'názor na toto tvrzení.'), pages=(2, 3)),
    R('I6', [shown(L(68, 71))], whole=True, total=PaperP(4, 'rodiče.'), pages=(2, 3)),
    R('II', [graded(S(83), PARTP(), CRIT_2011)],
      rownote=both(LEAD_2011, examples(None, L(84, 87))), pages=(2, 3)),
    R('III1', [graded(L(94, 95), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, ESSAY_2011, '1. Učení')),
    R('III2', [graded(L(94, 95), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, ESSAY_2011, '2. „Většina', '(Abraham Lincoln')),
]


# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2012-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and the reading text "Jak mluví ženy a jak
# muži?" in ten numbered paragraphs over pp2-3, to its byline "(Václav
# Cvrček, jazykovědec)" / "(upraveno podle aktualne.cz)" (p3, foot); p4 opens
# "Část 1 [30 bodů]" (p4 y98) over the questions: Q1 "[5 bodů]" over a)-e)
# (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4 y531), the commentary,
# ONE task with no number; "Část 3 [40 bodů]" (p4 y658), the instruction and
# two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I2 and I5: the paper prints each "[5 bodů]" on a line of its own under the
#   question (p4 x455 y287 and p4 x455 y429; rendered p4, right margin). Two
#   lines of p4 open "[5 bodů]", so PaperP cannot single either out, and PY
#   cannot read the cell (its pattern takes "bodu"/"bod", not "bodů"). Priced
#   from the scheme's printed "[5 bodů]" on the question's reprint (RX: line 28,
#   a line of its own; line 45 "... na celý text. [5 bodů]"), the same 5 the
#   paper prints. With "bodů" in PY's pattern: PY(4, 287), PY(4, 429).
# - I3 "jazyka? [5 bodů]" (p4 y325), I4 "Na základě textu vysvětlete rizika
#   ... [5 bodů]" (p4 y364), I6 "napište krátký text odkazující k textu. [5
#   bodů]" (p4 y481): the price at the end of the question's last line, PaperP.
# - II: "Část 2 [30 bodů]" (PARTP; the scheme prints "[30 bodů]" beside its
#   descriptive line, 76); III1/III2: "Část 3 [40 bodů]" (PARTP; scheme 80).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (27-28 reprint): one paragraph, 29-32. Q3 (33-34): one paragraph,
#   35-36. Q4 (37-38): one paragraph, 39-42. Q5 (43-45): one paragraph, 46-51.
#   Q6 (52-54, p3): one paragraph on p4, 58-63. No split, no mark inside any:
#   model answers (10a).
# - Criteria (p4, 64-70): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (65),
#   "– 30 %." (66-67), "– 30 %." (68-69), "– 10 %." (70): 100 %.
# - Part II (71-75 reprint the head and the task): the descriptive line
#   "Správný, plynulý komentář o minimálně 100 slovech." with "[30 bodů]" set
#   in its right-hand cell (76), then one paragraph of content in the smaller
#   type (77-79, "Souhlas, nesouhlas. Mohou jazyk ...", three questions).
# - Part III (80-83 reprint the head, the instruction and both titles): one
#   descriptive line only (84-85, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line (76, cut
#   before its "[30 bodů]"); the criteria's lead quoted; the paragraph quoted as
#   examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (84-85); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2/I5 priced from the scheme (RX), not the paper (see PRICES).
# - Reading text: pp2-3 (rendered: p2 opens with the rule and the title, the
#   text runs to the byline at the foot of p3; p4 holds only the questions).
#   The live Q1 card's sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none in either text layer. Lifted as printed: the scheme's straight
# quotation marks in Q5's row ("vyčistit", "popisnice", "munjovoz", 47-49);
# "s kamarádi" (40, Q4's row), "požití" (78, Part II's content).

CRIT_2012 = crit(65, (66, 67), (68, 69), 70)
LEAD_2012 = quote(S(64, after='Poznámka: '), lead='The scheme prints')
ESSAY_2012 = 'Napište esej'
BODU = r'\[(\d+) bodů\]'

SPECS[2012] = [
    R('I2', [shown(L(29, 32))], whole=True, total=RX(28, BODU), pages=(2, 3)),
    R('I3', [shown(L(35, 36))], whole=True, total=PaperP(4, 'jazyka?'), pages=(2, 3)),
    R('I4', [shown(L(39, 42))], whole=True, total=PaperP(4, 'Na základě textu vysvětlete rizika'),
      pages=(2, 3)),
    R('I5', [shown(L(46, 51))], whole=True, total=RX(45, BODU), pages=(2, 3)),
    R('I6', [shown(L(58, 63))], whole=True, total=PaperP(4, 'napište krátký text'), pages=(2, 3)),
    R('II', [graded(S(76, before=' [30'), PARTP(), CRIT_2012)],
      rownote=both(LEAD_2012, examples(None, L(77, 79))), pages=(2, 3)),
    R('III1', [graded(L(84, 85), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, ESSAY_2012, '1. Stereotypy')),
    R('III2', [graded(L(84, 85), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, ESSAY_2012, '2. V naší')),
]


# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2013-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and "Část 1 [30 bodů]" (p2 y190) over the
# reading text "Bez mámy se neobejdu", eight numbered paragraphs over pp2-3 to
# "(Zuzana Dastychová, upraveno podle časopisu Instinkt)" (p3 y651); p4 holds
# the questions: Q1 "[5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y470), the commentary, ONE task with no number;
# "Část 3 [40 bodů]" (p4 y626), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" in the right-hand cell of the question's own last
# line (rendered p4), read with PaperP: Q2 "2. Popište ..." (y234), Q3 "3.
# Vysvětlete ..." (y260), Q4 "rozdíly ve vnímání ..." (y299), Q5 "Myslíte si,
# ..." (y339), Q6 "s rodiči, včetně ..." (y392). II: "Část 2 [30 bodů]"
# (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The scheme prints the same
# "[5 bodů]" on each reprint, "[30 bodů]" (102) and "[40 bodů]" (109).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (58): one paragraph, 59-61. Q3 (62): one paragraph, 63-65. Q4 (66-67):
#   one paragraph, 68-71. Q5 (72-73): one paragraph, 74-78. Q6 (82-84, p4): one
#   paragraph, 85-90. No split, no mark inside any: model answers (10a).
# - Criteria (p4, 91-97): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (92),
#   "– 30 %." (93-94), "– 30 %." (95-96), "– 10 %." (97): 100 %.
# - Part II (98-102 reprint the head and the task, "[30 bodů]"): NO
#   descriptive line this sitting; one paragraph of content in the smaller
#   type (103-108, "Souhlas, nesouhlas. Dítě by nemělo být přívěškem ...").
# - Part III (109-112 reprint the head, the instruction and both titles): one
#   descriptive line only (113-114, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30. With no descriptive line, the head
#   is the criteria's own lead (91, cut after "Poznámka: "), as Dutch 2010
#   heads its Part II; the paragraph quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (113-114); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - Q3: the paper prints "důvody mamánkovsví" (rendered p4 at 200 dpi: the
#   SEC's typing, a letter short); the scheme reprints it "mamánkovství" (62).
#   The paper wins on the question (10f); the scheme's reprint is quoted on the
#   row's note.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render. (The live Q1 card's c) is a scheme matter
#   outside this draft: the scheme reprints "pokerovém stole světa", the paper
#   "pokerovém stole tohoto světa".)
# GLYPHS: none in either text layer (no character outside Czech letters and
# punctuation); the rows match the rendered scheme pp3-4.

CRIT_2013 = crit(92, (93, 94), (95, 96), 97)
LEAD_2013 = quote(S(91, after='Poznámka: '), lead='The scheme prints')
ESSAY_2013 = 'Napište esej'

SPECS[2013] = [
    R('I2', [shown(L(59, 61))], whole=True, total=PaperP(4, '2. Popište'), pages=(2, 3)),
    R('I3', [shown(L(63, 65))], whole=True, total=PaperP(4, '3. Vysvětlete'), pages=(2, 3),
      rownote=quote(S(62, after='3. ', before=' [5'), lead='The scheme reprints this question as')),
    R('I4', [shown(L(68, 71))], whole=True, total=PaperP(4, 'rozdíly ve vnímání'), pages=(2, 3)),
    R('I5', [shown(L(74, 78))], whole=True, total=PaperP(4, 'Myslíte si'), pages=(2, 3)),
    R('I6', [shown(L(85, 90))], whole=True, total=PaperP(4, 's rodiči, včetně'), pages=(2, 3)),
    R('II', [graded(S(91, after='Poznámka: '), PARTP(), CRIT_2013)],
      rownote=examples(None, L(103, 108)), pages=(2, 3)),
    R('III1', [graded(L(113, 114), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, ESSAY_2013, '1. Opičí')),
    R('III2', [graded(L(113, 114), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, ESSAY_2013, '2. Jít')),
]


# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2014-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2014", the rule and "Část 1 [30 bodů]"
# (p2 y191) over the reading text "Jmenují se Emma Smetana, či Petra Svoboda.
# Proč to té češtině dělají?" (an italic lead-in, then ten numbered
# paragraphs over pp2-3 to "(Kristina Komůrková, upraveno podle idnes.cz)", p3
# y609); Q1 "[5 bodů]" over a)-e) on p3 (live); Q2-Q6 on p4, "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y417), the commentary, ONE task with no number; "Část
# 3 [40 bodů]" (p4 y584), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" in the right-hand cell of the question's own last
# line (rendered p4), read with PaperP: Q2 "2. Jaký ..." (y78), Q3 "3. Jaké
# ..." (y119), Q4 "4. Popište ..." (y161), Q5 "s jazyky uvedenými ..." (y216),
# Q6 "svůj souhlas nebo nesouhlas ..." (y299). II: "Část 2 [30 bodů]"
# (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The scheme prints the same
# "[5 bodů]", "[30 bodů]" (105) and "[40 bodů]" (111).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (61): ONE sentence, 62-63 ("Ženské příjmení v češtině má ve většině
#   případů na konci přidanou koncovku -ová, např. Novák / Nováková.").
# - Q3 (64): one paragraph, 65-69. Q4 (70): one paragraph, 71-74. Q5 (75-76):
#   one paragraph, 77-83. Q6 (87-90, p4): one paragraph, 91-93. No split, no
#   mark inside any: model answers (10a).
# - Criteria (p4, 94-100): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (95),
#   "– 30 %." (96-97), "– 30 %." (98-99), "– 10 %." (100): 100 %.
# - Part II (101-105 reprint the head and the task, "[30 bodů]"): NO
#   descriptive line; one paragraph of content (106-110, "Souhlas, nesouhlas.
#   Toto tvrzení velmi silně souvisí s historií naší země, ...").
# - Part III (111-115 reprint the head, the instruction and both titles): one
#   descriptive line only (116-117, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2: ONE stated answer (a single fact, one sentence): one(row) at the
#   paper's 5, claimable.
# - I3-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead (94,
#   no descriptive line this sitting; as 2013 and Dutch 2010); the paragraph
#   quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (116-117); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2 one() (claimable) rather than shown: the scheme states one fact, not a
#   model paragraph. If the lead prefers every Czech Part I answer
#   self-assessed, flip to shown, whole=True.
# - I2's row runs over a line break after a spaced slash ("Novák /" on 62,
#   "Nováková." on 63; rendered p3). L()/J() glue a line ending "/" to the
#   next with no space ("Novák /Nováková."), so the two lines are joined by
#   the small Spaced helper below with the printed space. If the lead would
#   rather not carry a helper, L(62, 63) builds the card with the space lost.
# - Part II (10f): the paper prints only the quotation and "Napište komentář
#   (minimum 100 slov), ve kterém vysvětlíte svůj názor na toto tvrzení." (p4
#   y485); the scheme's reprint adds "Vysvětlete, proč si toto autorka myslí, a
#   napište komentář ..." (104-105). The paper wins on the question; the
#   scheme's reprint quoted on the row's note.
# - Part III title 1 (10f): the paper prints "Z vlastní zkušenosti - myslíte,
#   že nastal konečně čas změnit pravidla českého pravopisu?" (p4 y643-657);
#   the scheme reprints "Nastal čas změnit pravidla českého pravopisu?" (113).
#   The paper's title is the question; the scheme's words quoted.
# - The scheme's reprints of Q4 ("jaká je postoj", paper "jaký je postoj") and
#   Q6 (word order "křehkou ženu přivlastňuje") differ from the paper in
#   question text only; not quoted (no row depends on them).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.

class Spaced:
    """Two cuts the SEC wrapped at a spaced slash ("např. Novák /" over
    "Nováková."), joined with the printed space: Join glues a line that ends
    in "/" to the next ("sport centres/" over "schools"), which would print
    "Novák /Nováková"."""
    def __init__(self, *parts):
        self.parts = parts

    def text(self, doc):
        return ' '.join(p.text(doc) for p in self.parts)


CRIT_2014 = crit(95, (96, 97), (98, 99), 100)
LEAD_2014 = quote(S(94, after='Poznámka: '), lead='The scheme prints')
ESSAY_2014 = 'Napište esej'

SPECS[2014] = [
    R('I2', [one(Spaced(S(62), S(63)), PaperP(4, '2. Jaký'))], total=PaperP(4, '2. Jaký'), pages=(2, 3)),
    R('I3', [shown(L(65, 69))], whole=True, total=PaperP(4, '3. Jaké'), pages=(2, 3)),
    R('I4', [shown(L(71, 74))], whole=True, total=PaperP(4, '4. Popište'), pages=(2, 3)),
    R('I5', [shown(L(77, 83))], whole=True, total=PaperP(4, 's jazyky uvedenými'), pages=(2, 3)),
    R('I6', [shown(L(91, 93))], whole=True, total=PaperP(4, 'svůj souhlas'), pages=(2, 3)),
    R('II', [graded(S(94, after='Poznámka: '), PARTP(), CRIT_2014)],
      rownote=both(examples(None, L(106, 110)),
                   quote(L(102, 105, before=' [30'), lead='The scheme reprints the task as')),
      pages=(2, 3)),
    R('III1', [graded(L(116, 117), PARTP(), CRIT_2014)],
      rownote=both(LEAD_2014, quote(S(113, after='1. '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2014, Run('1. Z vlastní', 'pravopisu?'))),
    R('III2', [graded(L(116, 117), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, ESSAY_2014, Run('2. I když', 's sebou.'))),
]


# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): every ask of this sitting, Q1 carded
# whole at the parent key I1 (its listed asks I1a-I1e), I2-I6, II, III1, III2.
# No live 2015 card.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2015", the rule and "Část 1 [30 bodů]"
# (p2 y191) over the reading text "Děti úplňku", eleven numbered paragraphs
# over pp2-3 to "(Petr Třešňák, upraveno podle respekt.ihned.cz)" (p3 y740);
# p4 holds the questions: Q1 "1. Vysvětlete vlastními slovy: [5 bodů]" (p4
# y78) over a)-e), NO mark beside any expression (rendered p4: the five
# expressions indented, nothing in the right margin); Q2-Q6 "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y510), the commentary, ONE task with no number; "Část
# 3 [40 bodů]" (p4 y642), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I1: "[5 bodů]" for the question as a whole, on its stem line (p4 y78):
#   PaperP. The paper prints no per-expression mark and the scheme none either
#   (50: "1. Vysvětlete vlastními slovy: [5 bodů]", then a)-e) unpriced). So Q1
#   is carded WHOLE at the parent key I1, the five glosses as shown rows on the
#   paper's 5, as the live Czech Q1 cards of 2010-2014, 2016, 2017 are (brief;
#   Romanian 2010-2019). Not 10i: the paper prints Q1's own total.
# - Q2-Q6: "[5 bodů]" in the right-hand cell of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y216), Q3 "3. Popište ..."
#   (y258), Q4 "zdravotnická a sociální zařízení." (y320), Q5 "„A nelze
#   vyloučit ..." (y382), Q6 "6. Vysvětlete ..." (y430).
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The
#   scheme prints the same totals on its heads (103, 111).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; the .md repaired from glyph
# ids, checked against the render word by word for every line used):
# - Q1 (50): a) to e), each the expression, a colon (a, b) or a hyphen (c-e),
#   and its gloss: a) 51-52, b) 53-54, c) 55, d) 56-57, e) 58-59.
# - Q2 (60): ONE sentence, 61-62 ("Mezi tajuplné a nevysvětlené otázky kolem
#   autismu patří fakt, že záchvaty často propukají kolem úplňku měsíce.").
# - Q3 (63): one paragraph, 64-70. Q4 (71-72): one paragraph, 73-78.
# - Q5 (79-80): one paragraph, 81-87, then a line of its own (88, "Vlastní
#   interpretace tohoto trvrzení, vlastními slovy.": rendered p3, flush left
#   under the short last line "může klamat.").
# - Q6 (93, p4): a requirement only, one paragraph 94-95 ("Úkolem je vlastními
#   slovy vysvětlit, jestli se případně chápání autismu změnilo, ...").
# - Criteria (p4, 96-102): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (97),
#   "– 30 %." (98-99), "– 30" / "%." (100-101, the sign wrapped alone), "– 10
#   %." (102): 100 %.
# - Part II (103-105 reprint the head and the task): one paragraph of content
#   (106-109, "Souhlas, nesouhlas. I nemocný člověk, ..."), then a line of its
#   own, "Vlastními slovy, bez opsání frází z textu." (110).
# - Part III (111-114 reprint the head, the instruction and both titles): one
#   descriptive line only (115-116, "Jasně psaná kompozice, ...").
# SHAPES:
# - I1: questionTotal on the paper's 5, five shown rows (one gloss each, cut
#   after the expression and its colon or hyphen), each led by the PAPER's
#   expression.
# - I2: ONE stated answer (one fact, one sentence): one row at the paper's 5,
#   claimable (as 2014 I2).
# - I3, I4: one model paragraph each, shown, whole=True on the printed 5 (10a).
# - I5: the model paragraph and the scheme's own requirement line, two shown
#   rows (the scheme sets them apart), whole=True on the printed 5.
# - I6: the requirement-only answer shown, whole=True on the printed 5
#   (requirement-only answers are shown and self-assessed; Dutch 2011 Q5).
# - II, III1, III2: the right shape is graded (10b: 30/30/30/10 % of 30 and of
#   40 are whole numbers), BUT the shared reader cannot take it this sitting:
#   criterion 3 prints its percentage wrapped over two lines, "... jasně a
#   plynule – 30" (100) / "%." (101) (rendered p4: the sign alone on the next
#   line), and percent_of reads ONE line for "N %" (graded() raises "scheme
#   line 101 prints 0 percentages"). So SPECS below carries the shape that
#   builds today: the four criteria, with their printed percentages, as shown
#   rows on the paper's printed total (questionTotal 30 / 40; ruling F's shape,
#   10b's "show the percentages and score on the printed total"), the part's
#   own line and the criteria's lead quoted on the note. The graded entries
#   are written out in the block "PREFERRED" at the end of this file: swap
#   them in once percent_of reads a percentage wrapped over a crit span's
#   lines (a shared-code change for the lead; 9 / 9 / 9 / 3 and 12 / 12 / 12
#   / 4).
# JUDGEMENT CALLS:
# - Q1 c) (10f): the paper prints "„dostat do širšího povědomí“" (p4 y137);
#   the scheme reprints "„dostat se do širšího povědomí“" (55). The row is led
#   by the paper's words; the scheme's reprint is quoted on the first row's
#   note.
# - Q1's question is the paper's stem and its five expressions, each on its
#   own line with its printed letter (QL's shape), as the lane's whole-Q1
#   cards are built (Romanian 2012-2016); the live Czech Q1 cards (built by
#   lt_all) set them inline as "(a) petice (b) ...". The stem is cut before
#   its "[5 bodů]" by a small callable (_q1_2015): clean_question does not take
#   "bodů" as a price word, so QL itself would keep the price in the question.
# - I2 one() (claimable): see 2014 I2.
# - Part II's own line: the scheme prints no "Správný, plynulý komentář ..."
#   line this sitting; its requirement line (110) is the part's own line (the
#   graded head in PREFERRED; quoted on the note in SPECS). 2013 and 2014,
#   which print neither, are headed by the criteria's lead.
# - Reading text: pp2-3 (rendered). No live 2015 card to compare.
# GLYPHS: the repaired .md matches the render in every line used (no
# character outside Czech letters and punctuation; Č / ý, the pair the raw
# layer confuses, checked word by word in 45-117). Printed as such on the
# render (200 dpi crops of p3), SEC typing, lifted as printed: "smylsu" (53),
# "sitace" (58), "autististy", "nekdy", "prípad", "vytvočit", "sparavována"
# (73-77), "protže", "agličtinou", "ostaními", "nedopovídal" (81-84),
# "trvrzení" (88).

ESSAY_2015 = 'Napište esej'
CRIT_2015 = crit(97, (98, 99), (100, 101), 102)
LEAD_2015 = quote(S(96, after='Poznámka: '), lead='The scheme prints')
Q1P_2015 = PaperP(4, '1. Vysvětlete vlastními slovy:')
# The four criteria as printed, each with its percentage (shown rows).
CRIT_LINES_2015 = [S(97), L(98, 99), L(100, 101), S(102)]


def _crit_note_2015(d):
    return (f'Under “Poznámka:” the scheme prints “{S(96, after="Poznámka: ").text(d)}” and four criteria '
            'with their percentages, 30 / 30 / 30 / 10 %; the part is scored on its printed total.')


def _q1c_2015(d):
    return (f'The scheme reprints expression c) as “{S(55, after="c) ", before=" - ").text(d)}”; the paper prints '
            f'“{PC(4, "c) „dostat", after="c) ").text(d)}”.')


def _q1_2015(d, _census=None):
    """QL's shape (the stem, then each expression on its own line with its
    printed letter), the stem cut before its "[5 bodů]": clean_question does
    not take "bodů" for a price word, so QL would keep it."""
    stem = PC(4, '1. Vysvětlete vlastními slovy:', after='1. ', before=' [5').text(d)
    items = [PL(4, o).text(d) for o in ('a) rituál', 'b) stereotypní', 'c) „dostat', 'd) „obávaná', 'e) „pud')]
    return '\n'.join([stem] + items)


SPECS[2015] = [
    R('I1', [shown(L(51, 52, after='a) rituál: '), lead=PC(4, 'a) rituál', after='a) ')),
             shown(L(53, 54, after='b) stereotypní: '), lead=PC(4, 'b) stereotypní', after='b) ')),
             shown(S(55, after='povědomí“ - '), lead=PC(4, 'c) „dostat', after='c) ')),
             shown(L(56, 57, after='legenda“ - '), lead=PC(4, 'd) „obávaná', after='d) ')),
             shown(L(58, 59, after='sebezáchovy“ - '), lead=PC(4, 'e) „pud', after='e) '))],
      whole=True, total=Q1P_2015, rownote=_q1c_2015,
      question=_q1_2015,
      pages=(2, 3)),
    R('I2', [one(L(61, 62), PaperP(4, '2. Vysvětlete'))], total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(64, 70))], whole=True, total=PaperP(4, '3. Popište'), pages=(2, 3)),
    R('I4', [shown(L(73, 78))], whole=True, total=PaperP(4, 'zdravotnická a sociální'), pages=(2, 3)),
    R('I5', [shown(L(81, 87)), shown(S(88))], whole=True, total=PaperP(4, '„A nelze vyloučit'),
      pages=(2, 3)),
    R('I6', [shown(L(94, 95))], whole=True, total=PaperP(4, '6. Vysvětlete'), pages=(2, 3)),
    R('II', [shown(c) for c in CRIT_LINES_2015], whole=True, total=PARTP(),
      rownote=both(quote(S(110), lead='The scheme heads it'), _crit_note_2015,
                   examples(None, L(106, 109))), pages=(2, 3)),
    R('III1', [shown(c) for c in CRIT_LINES_2015], whole=True, total=PARTP(),
      rownote=both(quote(L(115, 116), lead='The scheme heads it'), _crit_note_2015),
      question=QP(4, ESSAY_2015, '1. „Láska')),
    R('III2', [shown(c) for c in CRIT_LINES_2015], whole=True, total=PARTP(),
      rownote=both(quote(L(115, 116), lead='The scheme heads it'), _crit_note_2015),
      question=QP(4, ESSAY_2015, '2. „Člověk')),
]

# PREFERRED, in force (lead, 20 Nov): sl_lib now reads the percentage the
# scheme wraps over lines 100-101 ("– 30" / "%."), so Parts II and III are
# graded on the four criteria (9/9/9/3 of 30, 12/12/12/4 of 40) as 2010-2017.
SPECS[2015][-3:] = [
    R('II', [graded(S(110), PARTP(), CRIT_2015)],
      rownote=both(LEAD_2015, examples(None, L(106, 109))), pages=(2, 3)),
    R('III1', [graded(L(115, 116), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, ESSAY_2015, '1. „Láska')),
    R('III2', [graded(L(115, 116), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, ESSAY_2015, '2. „Člověk')),
]


# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2016-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2016", the rule and "Část 1 [30 bodů]"
# (p2 y203) over the reading text "Recept od čtyř režisérů. Jak vyrobit
# legendární pohádku?", eleven numbered paragraphs running over pp2-3 INTO p4
# (paragraph 11, p4 y174, to "(Jiří Göth, upraveno podle lidovky.cz)", p4
# y252; a footnote on Švejk at the foot of p3); questions from p4 y282: Q1
# "[5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4
# y584), the commentary, ONE task with no number; "Část 3 [40 bodů]" (p4
# y666), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2-Q5: "[5 bodů]" at the end of the question's own last line (rendered
#   p4), PaperP: Q2 "tím má na mysli." (y392), Q3 "3. Popište ..." (y420), Q4
#   "příliš uspět nedá“." (y462), Q5 "tak populární." (y504).
# - Q6: "[5 bodů]" on a line of its own (p4 x475 y545), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]') (PY cannot read "bodů").
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same totals on its heads (103, 114).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5; answers in a smaller type):
# - Q2 (57-58 reprint): one paragraph, 59-62. Q3 (63-64): one paragraph,
#   65-68. Q4 (69-70): one paragraph, 71-76. Q5 (81-82, p4): one paragraph,
#   83-91. No split, no mark inside any: model answers (10a).
# - Q6 (92-93): a requirement only, one paragraph 94-96 ("Úkolem je vlastními
#   slovy vysvětlit, proč nelze klasickou pohádku považovat za
#   „Teletubbies“, ...").
# - Criteria (p4, 97-102): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (98),
#   "– 30 %." (99-100), "– 30%." (101), "– 10 %." (102): 100 %.
# - Part II (103-105 reprint the head and the task): one paragraph of content
#   (106-108, "Kompilace názorů čtyř úspěšných režisérů, ..."), then a line of
#   its own, "Vlastními slovy, bez opsání frází z textu." (109).
# - Part III (p5, 114-119 reprint the head, the instruction and both titles):
#   one descriptive line only (120-121, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I5: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - I6: the requirement-only answer shown, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (109; no "Správný, plynulý komentář" line this sitting, as 2015); the
#   criteria's lead quoted; the paragraph quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (120-121); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - The scheme's reprints of Q3 (ends "?", the paper ".") and Q4 ("že s
#   „originalitou", the paper "že „s originalitou") differ in punctuation
#   only; not quoted.
# - Part III title 2 is the two printed lines and the attribution (p4
#   y731-758), joined.
# - Reading text: pp2-4 (rendered: paragraph 11 and the byline are on p4, above
#   the questions). The live Q1 card's sourceMaterial.pages [2, 3, 4] AGREE
#   with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.
# Lifted as printed: "něaký" (66, Q3's row), "ušišlaná" (85, Q5's row).

CRIT_2016 = crit(98, (99, 100), 101, 102)
LEAD_2016 = quote(S(97, after='Poznámka: '), lead='The scheme prints')
ESSAY_2016 = 'Napište esej'

SPECS[2016] = [
    R('I2', [shown(L(59, 62))], whole=True, total=PaperP(4, 'tím má na mysli.'), pages=(2, 3, 4)),
    R('I3', [shown(L(65, 68))], whole=True, total=PaperP(4, '3. Popište'), pages=(2, 3, 4)),
    R('I4', [shown(L(71, 76))], whole=True, total=PaperP(4, 'příliš uspět'), pages=(2, 3, 4)),
    R('I5', [shown(L(83, 91))], whole=True, total=PaperP(4, 'tak populární.'), pages=(2, 3, 4)),
    R('I6', [shown(L(94, 96))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3, 4)),
    R('II', [graded(S(109), PARTP(), CRIT_2016)],
      rownote=both(LEAD_2016, examples(None, L(106, 108))), pages=(2, 3, 4)),
    R('III1', [graded(L(120, 121), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, ESSAY_2016, '1. Jestliže')),
    R('III2', [graded(L(120, 121), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, ESSAY_2016, Run('2. Svět', '(Fintan'))),
]


# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2017-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and "Část 1 [30 bodů]" (p2 y156) over the
# reading text "Nemyslím, tedy jsem" (unnumbered paragraphs) over pp2-3 to
# "(Linda Kholová, upraveno podle časopisu Instinkt)" (p3 y771); p4 holds the
# questions: Q1 "[5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each; "Část 2
# [30 bodů]" (p4 y528), the commentary, ONE task with no number; "Část 3 [40
# bodů]" (p4 y636), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" in the right-hand cell of the question's own last
# line (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y235), Q3 "3. Popište
# ..." (y279), Q4 "workholismus. ..." (y345), Q5 "5. Proč ..." (y389), Q6
# "sobě.“ (odst. 1) ..." (y455). II: "Část 2 [30 bodů]" (PARTP); III1/III2:
# "Část 3 [40 bodů]" (PARTP). The scheme prints the same totals (107, 114).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4):
# - Q2 (63): one paragraph, 64-67. Q3 (68): one paragraph, 69-71. Q5 (89):
#   one paragraph, 90-94. No split, no mark inside: model answers (10a).
# - Q4 (72-73): one paragraph running over the p3/p4 break, 74-82 and 87-88
#   ("... Otázka k diskuzi" / "je, zda je to tak správně, ... Prostor pro
#   vlastní názor."; 83-85 are the page number and the page head, left out).
# - Q6 (95-96): a requirement only, one paragraph 97-100 ("Úkolem je vlastními
#   slovy vysvětlit, proč mohou být informace tak mocnou zbraní ...").
# - Criteria (p4, 101-106): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (102),
#   "– 30 %." (103-104), "– 30 %." (105), "– 10 %." (106): 100 %.
# - Part II (107-109 reprint the head and the task): one block, 110-112 ("Vlastní
#   názor na uvedené tvrzení, lze vyjádřit souhlas i nesouhlas, ... Cokoliv, co
#   se vymkne kontrole, ...") and its last line "Vlastními slovy, bez opsání
#   frází z textu." (113, a sentence on a line of its own).
# - Part III (114-120 reprint the head, the instruction and both titles): one
#   descriptive line only (121-122, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I5: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - I6: the requirement-only answer shown, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (113, as 2015 and 2016); the criteria's lead quoted; 110-112 quoted
#   as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (121-122); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - Q5: the scheme's reprint doubles a word ("Proč je pro náš mozek dostat
#   důležité dostat se ...", 89); Part III title 1's reprint prints "doobu"
#   (117) for the paper's "dobu"; Part II's reprint "100–150" for the paper's
#   "100-150". Reprints of the question only, the paper's words stand; not
#   quoted (no row depends on them). The lead may quote 89 on I5 under 10f.
# - Q4's row joins 74-82 and 87-88 (one paragraph over the page break).
# - Part III titles cut from the paper's wrapped lines (title 1 p4 y684-714,
#   title 2 y742-772).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.
# Lifted as printed: "využívajíci" (65, Q2's row), "jestě" (70, Q3's row),
# "činnosti pro činnost" and "pamět" (91-93, Q5's row).

CRIT_2017 = crit(102, (103, 104), 105, 106)
LEAD_2017 = quote(S(101, after='Poznámka: '), lead='The scheme prints')
ESSAY_2017 = 'Napište esej'

SPECS[2017] = [
    R('I2', [shown(L(64, 67))], whole=True, total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(69, 71))], whole=True, total=PaperP(4, '3. Popište'), pages=(2, 3)),
    R('I4', [shown(J(L(74, 82), L(87, 88)))], whole=True, total=PaperP(4, 'workholismus.'), pages=(2, 3)),
    R('I5', [shown(L(90, 94))], whole=True, total=PaperP(4, '5. Proč'), pages=(2, 3)),
    R('I6', [shown(L(97, 100))], whole=True, total=PaperP(4, 'sobě.“'), pages=(2, 3)),
    R('II', [graded(S(113), PARTP(), CRIT_2017)],
      rownote=both(LEAD_2017, examples(None, L(110, 112))), pages=(2, 3)),
    R('III1', [graded(L(121, 122), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, ESSAY_2017, Run('1. Filozof', 'vlastní názor.'))),
    R('III2', [graded(L(121, 122), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, ESSAY_2017, Run('2. „Můj názor', 'média.'))),
]


def specs(year):
    return SPECS.get(year, [])
