#!/usr/bin/env python3
"""Reviewed specs for the Finnish classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/finnish/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme, Unpriced)
from pl_listen_lib import Join  # noqa: F401
from sl_lib import paper_run, MARKER, clean_question  # noqa: F401,E402

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2010
# ================================================================ 2010 HL ===
# Drafted (small-languages lane, 20 Nov): all thirteen asks of this sitting,
# I1a-e, I2-I6, II1, III1, III2. No live card (the old reader excluded the
# whole sitting: "the scheme prices no ask at the address the paper prints").
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y106); "TEKSTI (liittyy kysymyksiin 1-6)" (p2 y188); the
# article "Kateus vie tuhkatkin pesästä" runs pp2-3 (title p2 y216, paragraphs
# 1-12 to the byline "- Paula Posti" p3 y726 and "(sanoja 785)" p3 y754);
# p4: "I Tehtävä: Vastaa kaikkiin kysymyksiin. 30p" (y78); Q1 "Selitä omin
# sanoin seuraavat ilmaisut:" over a.-e., "1p" at the right margin of each
# (rendered: bold, right column); Q2-Q6 "5p" each at the right margin of the
# question's own line (Q2-Q4 the FIRST line, Q5 the second, Q6 a cell on the
# second line); "II Tehtävä: 30p" (y460); "III Tehtävä: 40p" (y611), two
# titles numbered "1." / "2." (rendered p4).
# PRICES:
# - I1a-d: "1p" each (PP: the census reads the right-hand cell).
# - I1e: the census reads no price (tariff None): the paper PRINTS "1p" at the
#   end of the expression's own line (p4 y184, "... katkaisee kateudelta
#   terän 1p"; rendered, right column like a-d). PaperP cannot read it (its
#   mark words do not take the bare "p"), so priced from the scheme's own
#   printed "1 piste" under the answer (line 34, rendered p2: right margin,
#   bold), the same 1 (RX). Not a remainder, not 10i.
# - I2-I6: the census reads no price; the paper PRINTS "5p" for each (p4: Q2
#   y211, Q3 y253, Q4 y294 at the end of the first line; Q5 y349 end of the
#   second; Q6 a cell at y391). Same reader gap (bare "p"), so each is priced
#   from the scheme's own printed price at the end of its reprint of the
#   question: "5 p" (36), "5 p" (48), "5p" (60, a line of its own), "5p" (65),
#   "5 p" (73) -- each the same 5 (RX). If the lead adds the bare "p" to
#   PaperP's words: PaperP(4, '2. Miten sana') etc.
# - II1: "II Tehtävä: 30p" (paper p4 y460); PARTP reads no part total in this
#   sitting (the census prints {} for it: the head carries no bracket), so
#   priced from the scheme's own head "II Tehtävä: 30p" (84), the same 30 (RX).
# - III1/III2: "III Tehtävä:" + "40p" (paper p4 y611, a cell of its own);
#   scheme "III Tehtävä: 40p" (91), the same 40 (RX).
# WHAT THE SCHEME PRINTS (rendered scheme pp2-5 = printed pages 1-4):
# - "I Tehtävä: (30p)" / "Vastaa kaikkiin kysymyksiin." / "Selitä omin sanoin
#   seuraavat sanat:" (15-17): the scheme's instruction says "sanat" where the
#   paper prints "ilmaisut" (10f: quoted on each Q1 card).
# - Q1: each expression reprinted in bold (18, 22, 25, 29, 31), its gloss in
#   italics below, "1 piste" at the right (a, c, d, e at the end of the gloss;
#   b on a line of its own, 24). b. is reprinted as "Kaksijakoinen tunne"
#   (22), where the paper prints "Kateus on ambivalentti tunne" (10f: the
#   paper's words are the question; the scheme's quoted on the card).
# - Q2-Q6: the question reprinted in bold with its price, then ONE italic
#   paragraph of model answer each: Q2 37-42, Q3 49-58, Q4 61-63, Q5 66-71,
#   Q6 74-79 (rendered: no dashes, no split, no marks inside).
# - Part II (84-88 reprint the head and the task): one bold-italic
#   descriptive line, 89-90, "Noin sadan sanan mittainen kommentti, jossa
#   kirjoittaja osoittaa ymmärtäneensä tekstin pääasiat".
# - Part III (91-94 reprint the head, the instruction and both titles): two
#   italic descriptive lines, 95-96 ("Kielellisesti huoliteltu n. 300 sanan
#   essee, ..."), then "Hyvän vastauksen aineksia:" (97, italic) over thirteen
#   bullets, 98-110 (nothing per title).
# - Criteria (p5, 115-121): "HUOMAA: Tehtavien II ja III arvostelussa otetaan
#   huomioon seuraavat osa-alueet" -- for Parts II AND III -- then four
#   numbered criteria (116-117, 118-119, 120, 121) WITH NO PERCENTAGES and no
#   marks (rendered p5: each ends in a full stop, nothing after it).
# SHAPES:
# - I1a-e: one(gloss) each at 1 (a single stated answer).
# - I2-I6: one model paragraph each, shown, whole=True on the printed 5
#   (10a; the lane's shape for a model paragraph with no per-point marks).
# - II1: criteria printed for this part without percentages (ruling F): the
#   four criteria as shown rows on the paper's 30 (questionTotal); the
#   descriptive line and the criteria's lead quoted.
# - III1/III2: the same four criteria as shown rows on the paper's 40; the
#   two descriptive lines, the criteria's lead, and the thirteen items under
#   "Hyvän vastauksen aineksia:" quoted as examples, not a checklist (10a).
# JUDGEMENT CALLS:
# - I2-I6: one printed paragraph each -> one claimable row at 5 (the lead's
#   call: the lane convention and the live 2011-2016 shape; a priced scheme
#   answer is claimable). The drafter had them shown on 5.
# - The thirteen bullets sit under Part III's titles (rendered p4) with no
#   title of their own; their words echo Part II's statement (competition,
#   reward systems), but they are quoted where the scheme prints them, on both
#   Part III cards. Bullets 107-108 ("eettiset näkökulmat suhteessa" /
#   "yhteisöllisyyteen / yksilöllisyyteen") read as one item wrapped over two
#   bullets; quoted as the two printed bullets.
# - I1c-e: the census drops Q1's instruction from these three letters; it is
#   put back from the paper's own line (pre). I1e's question is the census
#   text (the "1p" is not in it).
# - I2-I4: the census glues the "5p" printed at the end of the first line
#   into the question ("... harhaanjohtava? 5p Perustele ..."): each question
#   is the run of its two printed lines with that printed price cut out
#   (_q_price_inside). I5: the run of its two lines with the "5p" at the end
#   of the second cut off the same way (QP keeps it: the bare "p" is no
#   bracketed price). The second line, "Perustele vastauksesi tekstin
#   avulla.", is printed identically under Q2, Q3 and Q4, so PL cannot select
#   it alone.
# - II1's question: the task line and the three printed lines of the quoted
#   statement (the census stops mid-word).
# - Reading text pp2-3 (rendered: title p2 y216, the text to "(sanoja 785)"
#   p3 y754; p4 holds only the questions): pages=(2, 3) on Part I and II1.
#   No live card of this sitting to compare.
# GLYPHS: none. ä ö read cleanly in every line used (paper and scheme;
# "pääasiat", "säilyttäjänä", "kyräilyyn" checked on the render). Printed as
# such (render), SEC typing, lifted as printed: "Tehtavien" (115, no
# umlaut), "toteutuminem" (109), "Kaksijakoinen tunne" in b.'s gloss font.



def _q_price_inside(page, first, last, price):
    """A question the SEC wrapped with its printed price inside the run, at
    the end of a printed line ("... harhaanjohtava? 5p" / "Perustele
    vastauksesi tekstin avulla."; "... tätä väitettä? 5p"): the run of
    printed lines, with its marker and that printed price cut out."""
    def q(d, _census=None):
        t = paper_run(d, page, first, last)
        anchor = f' {price}'
        if t.count(anchor) != 1:
            raise ValueError(f'paper p{page}: {anchor!r} not once in {t!r}')
        head, tail = t.split(anchor)
        return clean_question(MARKER.sub('', f'{head} {tail}', count=1))
    return q


STEM_2010 = quote(S(17), lead='The scheme reprints the instruction as')
Q1E_2010 = RX(34, r'(\d) piste$')
CRIT_ROWS_2010 = (L(116, 117), L(118, 119), S(120), S(121))


def _crit_note_2010_ii(d):
    return (f'Under Part II the scheme prints “{L(89, 90).text(d)}” Under “{S(115).text(d)}” it prints the '
            f'four criteria with no marks or percentages beside them, so they are shown and the part is scored '
            f'on its printed total.')


def _crit_note_2010_iii(d):
    return (f'Under the two titles the scheme prints “{L(95, 96).text(d)}” Under “{S(115).text(d)}” it '
            f'prints the four criteria with no marks or percentages beside them, so they are shown and the '
            f'part is scored on its printed total.')


III_NOTE_2010 = both(_crit_note_2010_iii, examples(S(97), *[S(n) for n in range(98, 111)]))
II_P_2010 = RX(84, r'(\d+)p$')
III_P_2010 = RX(91, r'(\d+)p$')
ESSAY_2010 = 'Kirjoita suunnilleen 300 sanan aine.'

SPECS[2010] = [
    R('I1a', [one(L(19, 21, before=' 1 piste'), PP())], rownote=STEM_2010, pages=(2, 3)),
    R('I1b', [one(S(23), PP())],
      rownote=both(STEM_2010, quote(S(22, after='b. '), lead='The scheme reprints this expression as')),
      pages=(2, 3)),
    R('I1c', [one(L(26, 28, before=' 1 piste'), PP())], rownote=STEM_2010,
      question=pre(4, '1. Selitä omin sanoin'), pages=(2, 3)),
    R('I1d', [one(S(30, before=' 1 piste'), PP())], rownote=STEM_2010,
      question=pre(4, '1. Selitä omin sanoin'), pages=(2, 3)),
    R('I1e', [one(L(32, 34, before=' 1 piste'), Q1E_2010)], total=Q1E_2010, rownote=STEM_2010,
      question=pre(4, '1. Selitä omin sanoin'), pages=(2, 3)),
    R('I2', [one(L(37, 42), RX(36, r'(\d) p$'))], total=RX(36, r'(\d) p$'),
      question=_q_price_inside(4, '2. Miten sana', 'Perustele vastauksesi', '5p'), pages=(2, 3)),
    R('I3', [one(L(49, 58), RX(48, r'(\d) p$'))], total=RX(48, r'(\d) p$'),
      question=_q_price_inside(4, '3. Mitä huonoa', 'Perustele vastauksesi', '5p'), pages=(2, 3)),
    R('I4', [one(L(61, 63), RX(60, r'^(\d)p$'))], total=RX(60, r'^(\d)p$'),
      rownote=quote(S(59, after='4. '), lead='The scheme reprints this question as'),
      question=_q_price_inside(4, '4. Miksi tekstin', 'Perustele vastauksesi', '5p'), pages=(2, 3)),
    R('I5', [one(L(66, 71), RX(65, r'(\d)p$'))], total=RX(65, r'(\d)p$'),
      question=_q_price_inside(4, '5. Kateuden tehtävänä', 'Kaivola selittää', '5p'), pages=(2, 3)),
    R('I6', [one(L(74, 79), RX(73, r'(\d) p$'))], total=RX(73, r'(\d) p$'),
      question=QP(4, '6. Jokainen on hyvä', 'tätä väitettä?'), pages=(2, 3)),
    R('II1', [shown(c) for c in CRIT_ROWS_2010], whole=True, total=II_P_2010, rownote=_crit_note_2010_ii,
      question=QP(4, 'Kirjoita suunnilleen 100', Run('”Aikamme trendi', 'Yksilöitä tulisi')), pages=(2, 3)),
    R('III1', [shown(c) for c in CRIT_ROWS_2010], whole=True, total=III_P_2010, rownote=III_NOTE_2010,
      question=QP(4, ESSAY_2010, '1. „Jokainen')),
    R('III2', [shown(c) for c in CRIT_ROWS_2010], whole=True, total=III_P_2010, rownote=III_NOTE_2010,
      question=QP(4, ESSAY_2010, '2. Kukaan')),
]


# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# finnish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y77); "TEKSTI (liittyy kysymyksiin 1-6)" (p2 y215); the
# article "Meidän lapsi on kaunein" runs pp2-3 (title p2 y257, paragraphs 1-8
# to "Roope Lipasti 632 sanaa" p3 y511); "I Tehtävä: Vastaa kaikkiin
# kysymyksiin." (p3 y553) with Q1-Q2 on p3 and Q3-Q6 on p4, "1p" / "5p" at the
# right margin; "II Tehtävä:" + "30p" (p4 y374, the price a cell of its own at
# the right); "III Tehtävä:" + "40p" (p4 y546); two titles lettered "a." /
# "b." (y629, y670), b. with its attribution line "(Abraham Lincoln, USA:n
# 16. presidentti 1809-1865)" (y691).
# PRICES:
# - II1: the paper's "30p" on the part's head line (p4 y374); PARTP reads no
#   part total in this sitting (the census prints {}: no bracket on the
#   head), and PaperP does not take the bare "p", so priced from the scheme's
#   own head "II Tehtävä: 30p" (66), the same 30 (RX).
# - III1/III2: the paper's "40p" (p4 y546); scheme "III Tehtävä: 40p" (82),
#   the same 40 (RX).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; pp2,
# 6-8 blank):
# - Part II (66-69 reprint the head and the task as the paper prints it):
#   seven bullets, the first a heading, "• Hyvän vastauksen aineksia:" (70),
#   then six items: 71, 72, 73, 74-75 (wrapped: "... oksitosiinihormoni
#   erittyy =" / "”vaistomainen rakkaus”"), 76, 77. No marks, no criteria.
# - Part III (82-86): the head "III Tehtävä: 40p", the instruction and both
#   titles reprinted, and NOTHING else: no answer, no content, no criteria.
# - The scheme prints no assessment criteria anywhere (rendered pp3-5: no
#   "HUOMAA", no percentages).
# SHAPES:
# - II1: the six items shown, priced as a whole on the paper's 30
#   (questionTotal, 10a), under the scheme's own heading "Hyvän vastauksen
#   aineksia:" (quoted on the first row).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's
#   40, the note saying what the scheme does print (ruling 4).
# JUDGEMENT CALLS:
# - The heading "Hyvän vastauksen aineksia:" is set as the first of seven
#   bullets (rendered p4), but it is a heading ("elements of a good answer"),
#   not an item: quoted as the heading, not shown as a row.
# - Titles "a." / "b." are cited Section III Q1 / Q2 (ruling B).
# - III2: the scheme reprints title b. with a full stop after the closing
#   quotation mark ("... olla”."): punctuation only, not quoted.
# - II1's question is cut from the paper's own lines (the census glues the
#   head's "30p" in front, which clean_question keeps: no bracket), and its
#   conceptId is taken from that question (concept='question'; the census
#   text would name it "30p-kirjoita-..."). The paper prints the quoted statement with no
#   closing quotation mark ("... koko homma jäisi.", rendered p4): as printed.
# - Reading text pp2-3 (rendered: title p2 y257, the text to the byline p3
#   y511; Q1 from p3 y553). II1 carries pages=(2, 3). The live 2011 cards
#   carry NO sourceMaterial at all (flagged, P).
# GLYPHS: none. ä ö clean in the lines used ("läsnäoloa", "elämänvaiheille",
# "päättävät"; render checked).

II_P_2011 = RX(66, r'(\d+)p$')
III_P_2011 = RX(82, r'(\d+)p$')
ESSAY_2011 = 'Kirjoita suunnilleen 300 sanan aine.'


def _part3_note_2011(d):
    return (f'Under “{S(82, before=" 40p").text(d)}” the scheme reprints only the instruction “{S(83).text(d)}” and '
            f'the two titles; it prints no answer, no content and no criteria for this part.')


SPECS[2011] = [
    R('II1', [shown(S(71)), shown(S(72)), shown(S(73)), shown(L(74, 75)), shown(S(76)), shown(S(77))],
      whole=True, total=II_P_2011, rownote=quote(S(70), lead='The scheme heads them'),
      question=QP(4, 'Kirjoita suunnilleen 100', Run('”Investointi', 'rakastumista olisi')), concept='question',
      pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2011)], total=III_P_2011,
      question=QP(4, ESSAY_2011, 'a. ”Veri on')),
    R('III2', [unprinted(_part3_note_2011)], total=III_P_2011,
      question=QP(4, ESSAY_2011, 'b. ”Useimmat', '(Abraham Lincoln')),
]


# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# finnish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y111); the article "KUN YSTÄVYYS PÄÄTTYY" runs pp2-3
# (title p2 y252, paragraphs 1-12 to the byline "Susanna Chazalmartin" p3
# y677); p4: "I Tehtävä: Vastaa kaikkiin kysymyksiin." + "(30 / 100)" (y111),
# Q1-Q6 with "1p" / "5p" at the right; "II Tehtävä:" + "(30 / 100)" (y523);
# "III Tehtävä:" + "(40 / 100)" (y615), two titles numbered "1." / "2."
# (y669, y694).
# PRICES: II1 the part head's "(30 / 100)", III1/III2 "(40 / 100)" (PARTP:
# the census reads each total from the head's own cell); the scheme prints
# the same "(30 / 100)" (94) and "(40 / 100)" (107).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-6 = unnumbered; p2 blank):
# - Criteria (p5, 87-93, printed after Q6's answer and before Part II):
#   "HUOMAA: Tehtävien II ja III arvostelussa otetaan huomioon seuraavat
#   osa-alueet:" -- for Parts II AND III -- then four criteria WITH
#   PERCENTAGES: 1. "... ovat oikeita. – 30%" (88-89), 2. "... oikein
#   tekstiin. - 30%" (90-91), 3. "... ajatuksiaan. – 30%" (92), 4. "...
#   välimerkit.- 10%" (93): 100 %.
# - Part II (94-96 reprint the head and the task): "Hyvän vastauksen
#   aineksia:" (97, bold) over six dashed items, 98-103 (bold, rendered p5).
# - Part III (p6, 107-110 reprint the head, the instruction and both
#   titles): NOTHING else (no content, no line per title).
# SHAPES:
# - II1: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3; head: the criteria's
#   own lead (87; the scheme prints no descriptive line for Part II); the six
#   items quoted under the scheme's own "Hyvän vastauksen aineksia:" as
#   examples, not a checklist (10a).
# - III1/III2: graded (10b), 12/12/12/4 of 40; the same head.
# JUDGEMENT CALLS:
# - The criteria are printed once, between Part I and Part II, and name
#   "Tehtävien II ja III" (Parts II and III): read as stated for both parts.
# - Questions cut from the paper's own lines (the census glues the head's
#   "(30 / 100)" in front of II1's task).
# - Reading text pp2-3 (rendered: title p2 y252, the text to the byline p3
#   y677; p4 holds only the questions). II1 carries pages=(2, 3). The live
#   2012 cards carry sourceMaterial.pages [4], the questions' page (flagged,
#   P).
# GLYPHS: none. ä ö clean in the lines used ("ystävyys", "päättyy",
# "välimerkit"; render checked).

CRIT_2012 = crit((88, 89), (90, 91), 92, 93)
HEAD_2012 = S(87)
ESSAY_2012 = 'Kirjoita suunnilleen 300 sanan essee.'

SPECS[2012] = [
    R('II1', [graded(HEAD_2012, PARTP(), CRIT_2012)],
      rownote=examples(S(97), *[S(n) for n in range(98, 104)]),
      question=QP(4, 'Kirjoita suunnilleen 100', '”Erota tavallaan'), pages=(2, 3)),
    R('III1', [graded(HEAD_2012, PARTP(), CRIT_2012)],
      question=QP(4, ESSAY_2012, '1. Parhaat')),
    R('III2', [graded(HEAD_2012, PARTP(), CRIT_2012)],
      question=QP(4, ESSAY_2012, '2. Nyky-yhteiskunnassa')),
]


# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# finnish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y78); "TEKSTI (liittyy kysymyksiin 1-6)" (p2 y189); the
# article "Kirppukielen kohtalo: Mitä suomi on tulevaisuudessa?" runs pp2-3
# (title p2 y217, paragraphs 1-11 to "Vesa Heikkinen ja Harri Mantila" /
# "Suomen Kuvalehti 5.5.2011(lyhennelty)" p3 y556-568); "I Tehtävä: ..." +
# "(30/100)" (p3 y623) with Q1 on p3 and Q2-Q6 on p4; "II Tehtävä:" +
# "(30/100)" (p4 y467); "III Tehtävä:" + "(40/100)" (p4 y633), two titles
# numbered "1." / "2." (y689, y709).
# PRICES: II1 the part head's "(30/100)", III1/III2 "(40/100)" (PARTP); the
# scheme prints the same "(30/100)" (102) and "(40/100)" (113).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = unnumbered; p2 the SEC's
# standard note):
# - Criteria (p4, 93-101, printed after Q6's answer and before Part II):
#   "Huomaa. Tehtävien II ja III arvostelussa otetaan huomioon seuraavat
#   osa-alueet:" -- for Parts II AND III -- then four criteria WITH
#   PERCENTAGES: 1. (94-95) "-30%", 2. (96-98) "-30%", 3. (99-100) "-30%",
#   4. (101) "-10%": 100 %.
# - Part II (102-107 reprint the head and the task): "Hyvän vastauksen
#   aineksia:" (108) over four dashed items, 109-112 (italic, rendered p4).
# - Part III (113-116 reprint the head, the instruction and both titles):
#   NOTHING else.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30; head: the criteria's own lead (93; no
#   descriptive line for Part II); the four items quoted under the scheme's
#   own "Hyvän vastauksen aineksia:" as examples, not a checklist (10a).
# - III1/III2: graded (10b), 12/12/12/4 of 40; the same head.
# JUDGEMENT CALLS:
# - III1 (10f): the paper prints "1. Minun kielellinen identiteettini" (p4
#   y689); the scheme reprints "1. Minun kieli-identiteettini" (115). The
#   paper's words are the question; the scheme's reprint is quoted on the
#   card.
# - The items' ">" (e.g. "kansalaisuus/kansallisuus>ero") are printed as
#   such (rendered p4); quoted as printed.
# - Questions cut from the paper's own lines (the census glues "(30/100)" in
#   front of II1's task).
# - Reading text pp2-3 (rendered: title p2 y217, the text to its source line
#   p3 y568; Q1 from p3 y623). II1 carries pages=(2, 3). The live 2013 cards
#   carry sourceMaterial.pages [3] (p2 holds the title and paragraphs 1-6;
#   flagged, P).
# GLYPHS: none. ä ö clean in the lines used. The paper prints Q1 a. as
# "Alkuperäiskans" (p3 y679, rendered at 200 dpi: no final "a"; the scheme
# "Alkuperäiskansa") and Q5 as "... kielten asemasta? . Mitä itse ajattelet"
# (p4 y300, rendered): SEC typing on the live cards' questions, as printed,
# not a text-layer fault.

CRIT_2013 = crit((94, 95), (96, 98), (99, 100), 101)
HEAD_2013 = S(93)
ESSAY_2013 = 'Kirjoita suunnilleen 300 sanan essee.'

SPECS[2013] = [
    R('II1', [graded(HEAD_2013, PARTP(), CRIT_2013)],
      rownote=examples(S(108), *[S(n) for n in range(109, 113)]),
      question=QP(4, 'Kirjoita suunnilleen 100', Run('”Soveltavan', 'EU:n kansalaisuus')), pages=(2, 3)),
    R('III1', [graded(HEAD_2013, PARTP(), CRIT_2013)],
      rownote=quote(S(115, after='1. '), lead='The scheme reprints this title as'),
      question=QP(4, ESSAY_2013, '1. Minun')),
    R('III2', [graded(HEAD_2013, PARTP(), CRIT_2013)],
      question=QP(4, ESSAY_2013, '2. Seuraa')),
]


# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I1b, I1d, I2, I4, II1, III1, III2. Live: I1a, I1c, I1e, I3, I5, I6 (6
# cards); not touched (audited: see finnish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y64); "TEKSTI (liittyy kysymyksiin 1-6)" (p2 y173); the
# article "PELAATKO KIELIPELIÄ ARKIPÄIVÄISISSÄ KESKUSTELUISSASI?" runs pp2-4
# (title p2 y199, the text to "dynamiikka paranee." and its source line
# "(Lyhennelmä Raili Mykkäsen artikkelista. Sara/2103)" p4 y153); then on p4
# "I Tehtävä" + "(30/100)" (y198), "Vastaa kaikkiin kysymyksiin.", Q1 "1.
# Selitä omin sanoin seuraavat ilmaisut:" over a.-e., ONE expression per
# printed line (a. jämäkkä y276, b. tykästynyt y292, c. nihkeä y308, d.
# mollata y323, e. kiehnätä y339; rendered and raw spans), "1p." at x482 on
# each; Q2-Q6 "5p."; "II Tehtävä:" + "(30/100)" (y584); "III Tehtävä:" +
# "40/100)" (y689: no opening bracket, rendered), two titles numbered "1." /
# "2." (y730, y762), 2. with "- Ralph Waldo Emerson" at the right of its
# second line (y778).
# CENSUS READER FAULT (for the lead): eu_paper joins each expression line
# with the next (16 pt lower, inside its cell tolerance), so the census reads
# a. "jämäkkä tykästynyt", b. "1p. 1p.", c. "nihkeä mollata", d. "1p. 1p.":
# I1b and I1d have no words of their own and no price. Their questions are
# lifted below from the reader's own a./c. lines, cut after a.'s / c.'s word
# (PC: the printed b./d. word), and their conceptId taken from that question
# (concept='question'; the census text "1p. 1p." would name them).
# PRICES:
# - I1b, I1d: the paper prints "1p." beside each (p4 y292, y323, x482;
#   rendered); the census reads none (above), and PaperP does not take the
#   bare "p.", so each is priced from the scheme's own "1p." at the end of its
#   gloss (49, 51), the same 1 (RX).
# - I2, I4: the paper prints "5p." at the end of the question's own line
#   (p4 y378 "... Uhleniuksen mukaan? 5p."; y449 "... tekstin mukaan? 5p.";
#   rendered); the census reads none. Priced from the scheme's own "5p." at
#   the end of its reprint of each (54, 68), the same 5 (RX).
# - II1: the part head's "(30/100)" (PARTP; scheme "(30/100)", 91).
# - III1/III2: the paper prints "40/100)" with no opening bracket (p4 y689,
#   rendered), so PARTP and PaperP read no total; priced from the scheme's
#   own head "III Tehtävä: (40/100)" (95), the same 40 (RX).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; p2 the
# SEC's standard note):
# - Q1 (47-52): "b. tykästynyt = pitää, olla kovin ihastunut/rakastunut
#   (puhekielinen, arkinen) 1p." (49), "d. mollata = haukkua, moittia,
#   arvostella 1p." (51): the expression, "=", the gloss, the price.
# - Q2 (53-54 reprint the question with "5p."): one paragraph, 55-59.
# - Q4 (67-68 reprint the question with "5p."): one paragraph, 69-73.
# - Part II (91-94): the head and the task reprinted, NOTHING else.
# - Part III (95-99): the head, the instruction and both titles reprinted,
#   nothing per title.
# - Criteria (100-108, after Part III): "HUOMAA: Tehtävien II ja III
#   arvostelussa otetaan huomioon seuraavat" / "osa-alueet" -- for Parts II
#   AND III -- then four criteria, each with its percentage on its FIRST line
#   ("1. Tekstin sisällön ymmärtäminen 30% : ..." 102-103, "2. ... rakenne30%:
#   ..." 104-105, "3. ... ilmaisu 30%: ..." 106-107, "4. Kieliasu 10%: ..."
#   108): 100 %.
# SHAPES:
# - I1b, I1d: one(gloss) each at 1, cut after the scheme's "= " and before
#   its "1p.".
# - I2, I4: one model paragraph each, shown, whole=True on the printed 5
#   (10a).
# - II1: graded (10b), 9/9/9/3 of 30; head: the criteria's own lead
#   (100-101; nothing else printed for the part).
# - III1/III2: graded (10b), 12/12/12/4 of 40; the same head.
# JUDGEMENT CALLS:
# - The graded parts are written out (CRIT_2014) rather than with crit():
#   each criterion prints its percentage on its first line, and crit() reads
#   it from a span's last line.
# - I2/I4: one printed paragraph each -> one claimable row at 5, as the live
#   2014 I3/I5/I6 (the lead's call; the drafter had them shown on 5).
# - III2: the scheme reprints the attribution as "-RalpWaldo Emerson" (99):
#   SEC typing, not quoted; the question keeps the paper's "- Ralph Waldo
#   Emerson". III1: the scheme drops the title's full stop (97): not quoted.
# - Reading text pp2-4 (rendered: title p2 y199, the text to its source line
#   p4 y153; I Tehtävä from p4 y198): pages=(2, 3, 4) on Part I and II1. The
#   live 2014 cards carry sourceMaterial.pages [4] (flagged, P).
# GLYPHS: none. ä ö clean in the lines used ("tykästynyt", "jämäkkä",
# "välimerkit"; render and raw spans checked).



def _q(*sels):
    """A question cut from printed paper lines: each line (or cut) in order,
    its own marker taken off, joined by a space."""
    return lambda d, _census=None: clean_question(' '.join(MARKER.sub('', s.text(d), count=1) for s in sels))


STEM_2014 = PL(4, '1. Selitä omin sanoin')
# percentage on the FIRST line of each criterion's span
CRIT_2014 = [(L(102, 103), 102), (L(104, 105), 104), (L(106, 107), 106), (S(108), 108)]
HEAD_2014 = L(100, 101)
III_P_2014 = RX(95, r'\((\d+)/100\)')
ESSAY_2014 = 'Kirjoita suunnilleen 300 sanan essee.'
Q1B_2014 = RX(49, r'(\d)p\.$')
Q1D_2014 = RX(51, r'(\d)p\.$')
Q2_2014 = RX(54, r'(\d)p\.$')
Q4_2014 = RX(68, r'(\d)p\.$')

SPECS[2014] = [
    R('I1b', [one(S(49, after='= ', before=' 1p.'), Q1B_2014)], total=Q1B_2014,
      question=_q(STEM_2014, PC(4, 'a. jämäkkä', after='jämäkkä ')), concept='question', pages=(2, 3, 4)),
    R('I1d', [one(S(51, after='= ', before=' 1p.'), Q1D_2014)], total=Q1D_2014,
      question=_q(STEM_2014, PC(4, 'c. nihkeä', after='nihkeä ')), concept='question', pages=(2, 3, 4)),
    R('I2', [one(L(55, 59), Q2_2014)], total=Q2_2014,
      question=_q(PC(4, '2. Mitä kielipelissä', before=' 5p.')), pages=(2, 3, 4)),
    R('I4', [one(Join(L(69, 72), S(73), sep=''), Q4_2014)], total=Q4_2014,
      question=_q(PC(4, '4. ”Tie', before=' 5p.')), pages=(2, 3, 4)),
    R('II1', [graded(HEAD_2014, PARTP(), CRIT_2014)],
      question=QP(4, 'Kirjoita suunnilleen 100', Run('”Sanat, joilla', 'ihmissuhteisiimme')), pages=(2, 3, 4)),
    R('III1', [graded(HEAD_2014, III_P_2014, CRIT_2014)], total=III_P_2014,
      question=QP(4, ESSAY_2014, '1. Kieli poliittisen')),
    R('III2', [graded(HEAD_2014, III_P_2014, CRIT_2014)], total=III_P_2014,
      question=QP(4, ESSAY_2014, Run('2. ”Vaikka', 'mukanamme'), '- Ralph Waldo')),
]


# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the five open asks of this sitting,
# I1b, I1d, II1, III1, III2. Live: I1a, I1c, I1e, I2-I6 (8 cards); not
# touched (audited: see finnish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y79); "TEKSTI (liittyy kysymyksiin 1-6)" (p2 y148); the
# article "Äidinkieli muilla mailla" runs pp2-3 (title p2 y176, paragraphs
# 1-14 to "Heini Huuhtinen (lyhennelmä artikkelista Kielikellossa 3/2013)" p3
# y754); p4: "I Tehtävä" + "(30/100)" (y79), "Vastaa kaikkiin
# kysymyksiin.", Q1 "1. Selitä omin sanoin seuraavat ilmaisut:" over a.-e.,
# ONE expression per printed line (a. totuttelupäivä y128, b. kompata y141,
# c. vikkelä y155, d. some y169, e. Joka kuuseen ... y183; raw spans and
# render), "1p" at x395 on each; Q2-Q6 "5p"; "II Tehtävä:" + "(30/100)"
# (y493); "III Tehtävä" + "(40/100)" (y617), two titles numbered "1." /
# "2." (y672, y714).
# CENSUS READER FAULT (for the lead): as 2014, eu_paper joins each
# expression line with the next (14 pt lower), so the census reads a.
# "totuttelupäivä kompata", b. "1p 1p", c. "vikkelä some", d. "1p 1p": I1b
# and I1d have no words and no price of their own. Their questions are cut
# from the reader's a./c. lines after a.'s / c.'s word (PC: the printed b./d.
# word), and their conceptId taken from that question (concept='question').
# PRICES:
# - I1b, I1d: the paper prints "1p" beside each (p4 y141, y169, x395;
#   rendered); the census reads none, and PaperP does not take the bare "p",
#   so each is priced from the scheme's own "1p" at the end of its gloss (54,
#   56), the same 1 (RX).
# - II1: the part head's "(30/100)" (PARTP); scheme "(30/100)" (104).
# - III1/III2: "(40/100)" (PARTP); scheme "(40/100)" (108).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; p2 the
# SEC's standard note):
# - Q1 (50-58): "b. kompata=olla samaa mieltä jnkn kanssa jstkn asiasta 1p"
#   (54), "d. some=sosiaalinen media 1p" (56): the expression, "=", the gloss
#   in bold, the price.
# - Part II (104-107): the head and the task reprinted, NOTHING else.
# - Part III (108-111): the head, the instruction and both titles reprinted,
#   nothing per title.
# - Criteria (p4, 112-120, bold, after Part III): "HUOMAA: Tehtävien II ja
#   III arvostelussa otetaan huomioon seuraavat osa-" / "alueet" -- for Parts
#   II AND III -- then four criteria, each with its percentage on its FIRST
#   line (114, 116, 118, 120: 30 %, 30 %, 30 %, 10 %): 100 %.
# SHAPES:
# - I1b, I1d: one(gloss) each at 1, cut after the scheme's "=" and before its
#   "1p".
# - II1: graded (10b), 9/9/9/3 of 30; head: the criteria's own lead (112-113;
#   nothing else printed for the part).
# - III1/III2: graded (10b), 12/12/12/4 of 40; the same head.
# JUDGEMENT CALLS:
# - The graded parts are written out (CRIT_2015), not with crit(): each
#   criterion prints its percentage on its first line.
# - The head joins "osa-" / "alueet" across the SEC's line break as "osa-
#   alueet" (the lane's line join; the word is "osa-alueet").
# - Titles: the scheme drops the paper's full stops ("1. Kielellä luodaan
#   maailmaa", "2. Eniten on sillä, joka tyytyy vähimpään (Sokrates)"):
#   punctuation only, not quoted.
# - Reading text pp2-3 (rendered: title p2 y176, the text to its source line
#   p3 y754; p4 holds only the questions): pages=(2, 3) on I1b, I1d and II1.
#   The live 2015 cards carry sourceMaterial.pages [4] (flagged, P).
# GLYPHS: the lines used are clean (ä ö é: "Sirén", "äidinkieli",
# "säilyttäminen"; render checked). The scheme's p1-p2 header lines (4-41:
# "&RLPLVL~QQD6FU~GXLWKH6WiLW", "0DUNLQJ6FKHPH" = "Coimisiún na Scrúduithe
# Stáit", "Marking Scheme", each code point shifted by -29) come from a font
# with no usable ToUnicode map; none is used by any card.



def _q(*sels):
    """A question cut from printed paper lines: each line (or cut) in order,
    its own marker taken off, joined by a space."""
    return lambda d, _census=None: clean_question(' '.join(MARKER.sub('', s.text(d), count=1) for s in sels))


STEM_2015 = PL(4, '1. Selitä omin sanoin')
CRIT_2015 = [(L(114, 115), 114), (L(116, 117), 116), (L(118, 119), 118), (S(120), 120)]
# the head's "osa-" / "alueet" is one word broken at the line end: joined without a space
HEAD_2015 = Join(S(112), S(113), sep='')
ESSAY_2015 = 'Kirjoita suunnilleen 300 sanan essee.'
Q1B_2015 = RX(54, r'(\d)p$')
Q1D_2015 = RX(56, r'(\d)p$')

SPECS[2015] = [
    R('I1b', [one(S(54, after='=', before=' 1p'), Q1B_2015)], total=Q1B_2015,
      question=_q(STEM_2015, PC(4, 'a. totuttelupäivä', after='totuttelupäivä ')), concept='question',
      pages=(2, 3)),
    R('I1d', [one(S(56, after='=', before=' 1p'), Q1D_2015)], total=Q1D_2015,
      question=_q(STEM_2015, PC(4, 'c. vikkelä', after='vikkelä ')), concept='question', pages=(2, 3)),
    R('II1', [graded(HEAD_2015, PARTP(), CRIT_2015)],
      question=QP(4, 'Kirjoita suunnilleen 100', Run('”Ilmaukset', 'juuriini')), pages=(2, 3)),
    R('III1', [graded(HEAD_2015, PARTP(), CRIT_2015)],
      question=QP(4, ESSAY_2015, '1. Kielellä')),
    R('III2', [graded(HEAD_2015, PARTP(), CRIT_2015)],
      question=QP(4, ESSAY_2015, '2. Eniten')),
]


# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# finnish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y72); "TEKSTI" (p2 y160); the article "Järjellä ja
# tunteella aviovuoteeseen – Suomalaisen avioliiton ja yhteiselämän
# historiaa" runs pp2-3 (title p2 y184, paragraphs 1-13 to "Vainio-Korhonen,
# Kirsi (lyhennelmä artikkelista lehdessä niin & näin 1/15)" p3 y770); p4:
# "I Tehtävä" + "(30/100)" (y74), Q1 a.-e. under one "(5 × 1)" (y215), Q2-Q6
# "(5)" each; "II Tehtävä" + "(30/100)" (y478); "III Tehtävä" + "(40/100)"
# (y599), "Kirjoita noin 300 sanan essee. Valitse aiheeksesi toinen näistä."
# (y626), title "1." (y650-665), "Tai" (y689), title "2." (y714-728) with
# "Fintan O’Toole, The Irish Times, 22.02.2016." at the right of its second
# line and a task under it, "Pohdi väitettä noin 300 sanan esseessä. ..."
# (y755-769).
# PRICES: II1 the part head's "(30/100)", III1/III2 "(40/100)" (PARTP); the
# scheme prints the same "(30/100)" (114) and "(40/100)" (128).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# SEC's standard note):
# - Part II (114-117 reprint the head and the task): two paragraphs of
#   guidance, 118-120 ("Kokelaan on hyvä sijoittaa ... Kanta ei vaikuta
#   pisteytykseen, vaan kokelaan perustelut.") and 121-123 ("Jos kokelas
#   osoittaa erimielisyyttä, ... yhdenvertaisuuden periaatteeseen."). No
#   marks, no criteria.
# - Part III (128-129 reprint the head and the instruction): under title 1
#   (130-131) one paragraph, 132-135 ("Esseen tulee olla rakenteellisesti
#   eheä: ... yksilön tasolla."); under title 2 (136-139, the title, its
#   attribution and its task) one paragraph, 140-143 ("Esseen tulee olla
#   rakenteellisesti eheä: ... Mitä uhkat ovat, jos emme toimi?").
# - No assessment criteria anywhere (rendered pp3-5: no "HUOMAA", no
#   percentages).
# SHAPES:
# - II1: the two paragraphs shown, priced as a whole on the paper's 30
#   (questionTotal, 10a).
# - III1, III2: each title's own paragraph shown, priced as a whole on the
#   paper's 40 (questionTotal, 10a).
# JUDGEMENT CALLS:
# - Part II's first paragraph ends with a marking note ("Kanta ei vaikuta
#   pisteytykseen, vaan kokelaan perustelut." -- the stance does not affect
#   the marks, the reasoning does): it is printed inside the paragraph
#   (rendered p4), so it stays in the shown row as printed.
# - III2's question: the title, its attribution as printed at the right of
#   its second line, and the task printed under it (the census stops
#   mid-word); III1's: the title's two lines (the census glues the "Tai"
#   printed between the titles).
# - The scheme reprints III2's attribution as "Fintan O’ Toole, The Irish
#   Times, 22.2.2016" (137): spacing and date format only, not quoted.
# - Reading text pp2-3 (rendered: title p2 y184, the text to its source line
#   p3 y770; p4 holds only the questions): II1 carries pages=(2, 3). The live
#   2016 cards carry sourceMaterial.pages [4] (flagged, P).
# GLYPHS: none. ä ö clean in the lines used ("pisteytykseen",
# "käsittelykappaleet", "kestävämpää"; render checked).

ESSAY_2016 = 'Kirjoita noin 300 sanan essee.'

SPECS[2016] = [
    R('II1', [shown(L(118, 120)), shown(L(121, 123))], whole=True,
      question=QP(4, 'Kirjoita noin 100', Run('”Jos haluamme', 'tuotava kaikkien')), pages=(2, 3)),
    R('III1', [shown(L(132, 135))], whole=True,
      question=QP(4, ESSAY_2016, Run('1. Rakkaus ja', 'puolia: rakkautta'))),
    R('III2', [shown(L(140, 143))], whole=True,
      question=QP(4, ESSAY_2016, Run('2. ”Maailma', 'kestävämpää'), 'Fintan O’Toole',
                  Run('Pohdi väitettä', 'kehityksestä huolehtiminen'))),
]


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the six open asks of this sitting,
# I3, I4, I5, II1, III1, III2. Live: I1a-e, I2, I6 (7 cards); not touched
# (audited: see finnish-live-faults-2018-2025.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y65); "TEKSTI" (p2 y168), the source line, the title
# "Suomi vuonna 2025" (p2 y234) and paragraphs (1)-(5) on p2, (5) running on
# to p3, the head "Keskusteleva koulu" (p3 y182), (6)-(10) to "(--)" p3 y702:
# the reading text runs pp2-3. p4 holds only the questions: "I Tehtävä" /
# "(30/100)" (p4 y65); Q1 a.-e. with "(5 x 1)" at the right of e. (y212);
# Q2-Q6 "(5)" each at the end of the question's last line; "II Tehtävä" /
# "(30/100)" (y476); "III Tehtävä" / "(40/100)" (y608), "Kirjoita noin 300
# sanan essee. Valitse aiheeksesi toinen näistä." over two titles numbered
# "1." / "2." joined by "Tai": cited Section III Q1/Q2 (ruling B).
# PRICES:
# - I3, I4, I5: "(5)" each, printed at the end of the question's own (last)
#   line (PP: the census reads it).
# - II1: the head's "(30/100)" (PARTP); the scheme prints the same head (140).
# - III1/III2: the head's "(40/100)" (PARTP), each title answered alone at
#   the part's 40; scheme head 149.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-6 = printed pages 1-4; p2 the
#   standard note, pp7-8 blank):
# - Every Part I question is reprinted in bold, then "Tekstissä:" (in the
#   text) over the paragraphs of the reading text that answer it, each led by
#   the text's own paragraph number "(n)"; no marks inside, no dashes.
# - Q3 (66-67 reprint): "Tekstissä seuraavat – kokelas käsittelee
#   valitsemaansa kolmea seikkaa:" (68: the candidate treats the three points
#   they choose), then five paragraphs: (1) 69-75, (2) 76-77, (3) 82-83 (p4),
#   (7) 84-87, (8) 88.
# - Q4 (89 reprint, worded "Millaisia syitä ...?" where the paper prints
#   "Kerro omin sanoin, millaisia syitä ..."): "Tekstissä:" (90), then (1)
#   91-93, (3) 94-97, (7) 98-100.
# - Q5 (101-103 reprint, adding "esimerkein" the paper does not print):
#   "Tekstissä:" (104), then (5) 105-110, (6) 111-112, (7) 113-114, and the
#   scheme's own closing sentence 115-116, "Näiden pohjalta kokelas esittelee
#   ja konkretisoi tilanteita, joissa koulutuksella pyritään ratkaisemaan
#   ongelmia." (rendered p4: plain type, a paragraph of its own).
# - Part II (140-143 reprint the head and the task): ONE paragraph, 144-148,
#   "Kokelaan on hyvä aloittaa määrittelystä, ... Kokoava yhteenveto on
#   eduksi." (rendered p5, small type). No criteria, no percentages anywhere
#   in this scheme (pp7-8 blank). The exclusion's "the scheme prints NOTHING
#   under this task" is wrong.
# - Part III (149-150 reprint the head and the instruction): each title
#   reprinted (151-153; 164-166) with ONE paragraph of its own under it:
#   158-162 (p6, "Esseen tulee olla rakenteellisesti eheä: ... näkökulman
#   tulisi olla Suomen tilannetta laajempi.") and 167-170 ("Esseen tulee olla
#   rakenteellisesti eheä: ... Aihe sallii persoonallisen tai pakinoivan
#   käsittely- ja ilmaisutavan."). The two share their first three sentences;
#   each ends with a sentence of its own about its title.
# SHAPES:
# - I3, I4, I5: the scheme's paragraphs shown, one row each, priced as a
#   whole on the paper's 5 (questionTotal: points with no per-point marks;
#   I3's "three of five" is the scheme's own instruction, quoted, never a
#   bestNofParts, since no mark per point is printed).
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a).
# - III1, III2: each title's own paragraph shown, priced as a whole on the
#   paper's 40 (10a: indicative content for that title, never "prints no
#   answer"; Danish 2025 the precedent).
# JUDGEMENT CALLS:
# - Each row keeps the text's paragraph number "(n)" as the scheme prints it
#   (it names the paragraph of the reading text the student should find).
#   The live I2 card cuts it off; both are the scheme's words.
# - I5's closing sentence (115-116) is shown as the last row: it is the
#   scheme's statement of what the answer does with the paragraphs above it.
# - I3's lead line and the "Tekstissä:" heads are quoted in the first row's
#   note, never rows (a heading is not an answer).
# - I4 and I5: the scheme's reprint differs from the paper's question; the
#   paper's words are the question (10f), the scheme's quoted on the card.
# - III1's question: the instruction, then the title's two printed lines
#   (the census glues "Tai" onto III1); III2 the instruction and its three
#   lines.
# - Reading text pp2-3 (rendered); II1 travels with it. The live cards of
#   this sitting carry sourceMaterial.pages [4] (the questions page): flagged
#   (P), not changed.
# GLYPHS: none. ä ö read cleanly in every line used (paper and scheme;
#   "ääriajattelu", "käsittelykappaleet", "kärsimyksiä" checked on the
#   render). The only non-Finnish letters in either text layer are the á/ú of
#   "Coimisiún na Scrúduithe Stáit" on the scheme cover.

def _head_2018(n):
    return quote(S(n), lead='The scheme heads its answer')


ESSAY_2018 = 'Kirjoita noin 300 sanan essee.'

SPECS[2018] = [
    R('I3', [shown(L(69, 75)), shown(L(76, 77)), shown(L(82, 83)), shown(L(84, 87)), shown(S(88))],
      whole=True, rownote=_head_2018(68), pages=(2, 3)),
    R('I4', [shown(L(91, 93)), shown(L(94, 97)), shown(L(98, 100))], whole=True,
      rownote=both(quote(S(89, after='4. '), lead='The scheme reprints this question as'), _head_2018(90)),
      pages=(2, 3)),
    R('I5', [shown(L(105, 110)), shown(L(111, 112)), shown(L(113, 114)), shown(L(115, 116))], whole=True,
      rownote=both(quote(L(101, 103, after='5. '), lead='The scheme reprints this question as'), _head_2018(104)),
      pages=(2, 3)),
    R('II1', [shown(L(144, 148))], whole=True,
      question=QP(4, 'Kirjoita noin 100 sanan', Run('”Nuorten keskuudessa', 'yhteiskunnan polarisaatio')),
      pages=(2, 3)),
    R('III1', [shown(L(158, 162))], whole=True,
      question=QP(4, ESSAY_2018, Run('1. Maailma vuonna 2025', 'Anna myös ihmisille'))),
    R('III2', [shown(L(167, 170))], whole=True,
      question=QP(4, ESSAY_2018, Run('2. ”Vaatteet miehen', 'päätelmiä ihmisistä'))),
]


# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the five open asks of this sitting,
# I2, I6, II1, III1, III2. Live: I1a-e, I3, I4, I5 (8 cards); not touched
# (audited: see finnish-live-faults-2018-2025.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin kolmeen tehtävään
# suomeksi. ..." (p2 y65); "TEKSTI" (p2 y152), the title "Sorron yön jälkeen
# häämöttää vapauden valo" (p2 y176) and paragraphs (1)-(10) on p2, (11)-(16)
# on p3 to the source "www.yle.fi 7.6.2018", "Janne Saarikivi" and the author
# note (p3 y518): the reading text runs pp2-3. "I Tehtävä" / "(30/100)" (p3
# y588), Q1 a.-e. under "(5 × 1)" (p3 y754); p4: Q2-Q6 each with "(5)" in a
# cell of its own at the right margin (x482) of the question's last line;
# "II Tehtävä" / "(30/100)" (p4 y430); "III Tehtävä" / "(40/100)" (p4 y588),
# "Kirjoita noin 300 sanan essee. Valitse aiheeksesi toinen näistä." over two
# titles numbered "1." / "2." joined by "Tai": Section III Q1/Q2 (ruling B).
# PRICES:
# - I2: "(5)" (p4 y65; PP()).
# - I6: the paper PRINTS "(5)" in a cell of its own at the right of Q6's last
#   line (p4 x482 y335; rendered). The census reads it WRONG: tariff (2, None,
#   13), notation "(8) + (5)", because it also takes the paragraph reference
#   "(8)" printed inside the question ("... sairaanhoitajan.” (8) Kommentoi
#   ...") for a price, so PP() would say 13. PY cannot read the cell (its
#   pattern needs a mark word; this paper prints a bare "(5)"), PaperP cannot
#   pick it (five lines of p4 open "(5)"), and the scheme prints no price for
#   Q2-Q6 at all (rendered scheme pp3-4). Priced by _cell_2019(4, 335): PY's
#   own reading of a price cell at (page, y), taking the bare "(5)" (the
#   printed figure, not inferred). If the lead extends PY to bare bracketed
#   cells: PY(4, 335). Not a remainder, not 10i.
# - II1: "(30/100)" (PARTP); scheme head "II Tehtävä (30/100)" (120).
# - III1/III2: "(40/100)" (PARTP), each title answered alone at the part's
#   40; scheme head 133.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
#   standard note, pp6-7 blank):
# - Each Part I question is reprinted in bold, then a plain lead ("Tekstissä:"
#   or "Tekstissä kirjoittaja vertailee:") over the paragraphs of the reading
#   text that answer it, each led by the text's paragraph number "(n)".
# - Q2 (59 reprint): "Tekstissä:" (60), then ONE paragraph, (3), 61-63.
# - Q6 (105-107 reprint, as the paper prints it): "Tekstissä kirjoittaja
#   vertailee:" (108), then (5) 109-110, (6) 111-114, (7) 115-117, and the
#   scheme's own closing paragraph 118-119, "Edellisen kommentoimisen lisäksi
#   kokelas ilmaisee oman näkemyksensä ja perustelee sen esimerkiksi
#   tuottavuuden ja talouskasvun näkökulmasta tai humanitaarisista
#   näkökulmista."
# - Part II (120-123 reprint the head and the task): ONE paragraph, 124-126
#   + 131-132 (it runs over the page break, p4 to p5): "Kokelaan on hyvä
#   aloittaa määrittelystä, mitä täystyöllisyydellä ja talouskasvulla
#   tarkoitetaan. ... Kokoava yhteenveto on eduksi." No criteria and no
#   percentages anywhere in this scheme. The exclusion's "the scheme prints
#   NOTHING under this task" is wrong.
# - Part III (133-134 reprint the head and the instruction): each title
#   reprinted (135-137; 143-144) with ONE paragraph of its own under it:
#   138-141 ("Esseen tulee olla rakenteellisesti eheä: ... näkökulman tulee
#   suuntautua selkeästi tulevaisuuteen.") and 145-149 ("Esseen tulee olla
#   rakenteellisesti eheä: ... Kokelaan tulee käsitellä aihetta sekä hyödyn
#   ja kokemuksen että menetetyn ajan näkökulmasta. ...").
# SHAPES:
# - I2: one printed paragraph = one row at the paper's 5 (the shape of the
#   live 2018 I2 and of Bulgarian's one-paragraph answers).
# - I6: the three paragraphs and the closing paragraph shown, priced as a
#   whole on the paper's 5 (questionTotal: points with no per-point marks).
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a).
# - III1, III2: each title's own paragraph shown, priced as a whole on the
#   paper's 40 (10a; Danish 2025 the precedent).
# JUDGEMENT CALLS:
# - Rows keep the text's paragraph number "(n)" as the scheme prints it; the
#   live 2019 rows cut it off. Both are the scheme's words.
# - The leads "Tekstissä:" / "Tekstissä kirjoittaja vertailee:" are quoted
#   in the first row's note, never rows.
# - I6's closing paragraph (118-119) is a row: it states what the answer
#   adds to the comparison above it (the candidate's own view).
# - Part II's paragraph is cut around the page foot ("3", 127) and head
#   ("## Page 5", 129): J(L(124, 126), L(131, 132)). Its "--" (125) is
#   printed so.
# - I6's question is cut from the paper's three printed lines (Run): the
#   census drops the paragraph reference "(8)" printed inside it (it took it
#   for a price). The opening "” En" keeps the space the paper prints after
#   the quotation mark (rendered p4), as does II1's "” Tavoitteenamme".
# - II1's question: the task line and the two lines of the quoted statement
#   (the census glues the head's "(30/100)" in front). III1/III2: the
#   instruction, then the title's lines (the census glues "Tai" onto III1).
# - Reading text pp2-3 (rendered); II1 travels with it. The live cards of
#   this sitting carry sourceMaterial.pages [3] (the page of Q1 and the end
#   of the text): flagged (P), not changed.
# GLYPHS: none. ä ö read cleanly in every line used ("häämöttää",
#   "näkökulmista", "määrittelystä" checked on the render). The scheme sets
#   "arbeta", "rabotat", "travailler" and "tripaliumin" in italic (Q5, a
#   live card's lines): plain letters in the text layer.

import re as _re


class _Cell2019:
    """A price the paper prints as a cell of its own at (page, y): PY's
    reading (sl_lib.PaperLinePrice), taking a bare bracketed number "(5)"
    as this paper prints it (PY's pattern needs a mark word)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = _re.compile(r'^\(\s*(\d{1,2})\s*\)$')
        hits = [ln for ln in doc['lines'] if ln.page == self.page and abs(ln.y - self.y) < 2
                and cell.match(ln.text.strip())]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} bare price cells')
        return 1, int(cell.match(hits[0].text.strip()).group(1)), hits[0].text.strip()


def _cell_2019(page, y):
    return _Cell2019(page, y)


def _head_2019(n):
    return quote(S(n), lead='The scheme heads its answer')


Q6P_2019 = _cell_2019(4, 335)
ESSAY_2019 = 'Kirjoita noin 300 sanan essee.'

SPECS[2019] = [
    R('I2', [one(L(61, 63), PP())], rownote=_head_2019(60), pages=(2, 3)),
    R('I6', [shown(L(109, 110)), shown(L(111, 114)), shown(L(115, 117)), shown(L(118, 119))], whole=True,
      total=Q6P_2019, rownote=_head_2019(108),
      question=QP(4, Run('6. ” En myöskään', 'Millaisesta työstä')), pages=(2, 3)),
    R('II1', [shown(J(L(124, 126), L(131, 132)))], whole=True,
      question=QP(4, 'Kirjoita noin 100 sanan', Run('” Tavoitteenamme', 'ihminen, joka ei')),
      pages=(2, 3)),
    R('III1', [shown(L(138, 141))], whole=True,
      question=QP(4, ESSAY_2019, Run('1. Kuvittele', 'hyödyntää aiheesta'))),
    R('III2', [shown(L(145, 149))], whole=True,
      question=QP(4, ESSAY_2019, Run('2. Välivuosi', 'ja anna perusteltu'))),
]


# ====================================================================== 2022
# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the five open asks of this sitting,
# I3, I4, I5, I6, II2. Live: I1a-e, I2 (6 cards); not touched (audited: see
# finnish-live-faults-2018-2025.json). A TWO-PART sitting (out of 70): Part
# II is the essay.
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin tehtäviin suomeksi.
# ..." (p2 y65), "Koko kokeen maksimipistemäärä on 70." (p2 y108); "TEKSTI 1"
# (p2 y194), its title and paragraphs 1)-7) to the byline "Tiina Laaninen,
# Helsingin Sanomat 25.1.2021 (lyhennetty)" (p2 y705); "TEKSTI 2:" (p3 y65),
# its title and paragraphs 8)-18) on p3, 19)-21) on p4 to the byline "Mikko
# Puttonen, Helsingin Sanomat 30.9.2021" (p4 y213): the reading texts run
# pp2-4. "I TEHTÄVÄ" / "(30/70)" (p4 y258); Q1 a.-e. under "(5 × 1)"; Q2,
# Q4, Q5, Q6 "(5)" each; "II TEHTÄVÄ" / "(40/70)" (p4 y650), "Kirjoita noin
# 300 sanan essee. Valitse aiheeksi toinen näistä." over two titles numbered
# "1." / "2." (p4 y709, y738).
# PRICES:
# - I3: the paper prints its price as a bare "5" welded to the question's
#   full stop, with no bracket ("... kautta esitetään.5", p4 y487; rendered:
#   the 5 sits on the text line, not in the right-hand price column). The
#   census reads no tariff (and the exclusion says "neither document states a
#   tariff": wrong). The scheme prints "(5)" at the end of its reprint of Q3
#   (line 60); priced from it (RX), the same 5 the paper prints. Not a
#   remainder, not 10i.
# - I4, I5, I6: "(5)" each (PP()).
# - II2: the head's "(40/70)" (PARTP); scheme head "II TEHTÄVÄ (40/70)" (96).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2; p2 the
#   standard note, pp5-6 blank):
# - Q3 (60 reprint, worded "Kerro, millainen ..." where the paper prints
#   "Kuvaa, millainen ..."; "(5)"): ONE paragraph, 61-63, "Tekstissä
#   korostetaan vanhemman roolia kannustajana ja motivaattorina, ...
#   Vanhempi ei ole vain auktoriteetti, vaan valmentaja."
# - Q4 (64-65 reprint, "(5)" on a line of its own): THREE paragraphs, each
#   opened by "Tekstissä:" and each PRICED at its end: 66-69 "(1 p.)", 70-71
#   "(2 p.)", 72-74 "(2 p.)" (rendered p3: 1 + 2 + 2 = the printed 5). The
#   exclusion's "the scheme states no answer for this ask, only its price"
#   is wrong.
# - Q5 (79-81 reprint, "(5)"): "Vastauksessa kokelaan on ymmärrettävä
#   tekstissä kohta:" (82, a lead) and THREE paragraphs: 82-87 (the text's
#   18) with the scheme's own remarks in brackets), 88-89, 90-91.
# - Q6 (92-93 reprint, worded "... miksi psykologisilla taidoilla ..." where
#   the paper prints "... millä tavalla psykologisilla taidoilla ..."; "(5)"):
#   ONE paragraph, 94-95, "Psykologiset taidot tukevat kouluoppimista.
#   Kokelas voi luetella tekstissä mainittuja taitoja (uteliaisuus,
#   luottamus, sisu) pohtia niiden merkitystä oppimisen tai elämän
#   kannalta."
# - Part II (96-99 reprint the head, the instruction and both titles): ONE
#   paragraph for both titles, 100-103, "Esseen tulee olla rakenteeltaan
#   eheä: johdanto, erilliset käsittelykappaleet sekä päätäntä.
#   Tehtävänannot ovat väitelauseita, joiden sisältöä tulee avata ja pohtia.
#   Oma kanta tulee perustella ja antaa käsitteisiin (kannustamisen
#   kulttuuri, sinnikäs optimisti, tärkeitä elämäntaitoja) sopivia sisältöjä
#   sekä esimerkkejä." No criteria, no percentages.
# SHAPES:
# - I3: one printed paragraph = one row at the printed 5.
# - I4: three point rows at the scheme's printed 1 + 2 + 2, adding to the
#   paper's (5) (fixed; CARD-STANDARD 2 "prints answers, each with its
#   marks"). Each row cut after its "Tekstissä: " lead and before its price.
# - I5: the three paragraphs shown, priced as a whole on the paper's 5.
# - I6: the paragraph shown, priced as a whole on the paper's 5: it states
#   one point and then what the candidate "voi" (may) do (a requirement,
#   not a stated answer to claim; Bulgarian 2010 I6 the precedent).
# - II2: R4 (unprinted) at the paper's 40, the note quoting the scheme's
#   paragraph: see JUDGEMENT CALLS.
# JUDGEMENT CALLS:
# - II2 R4, not shown: the one paragraph under both titles is general essay
#   guidance (structure, own view, examples), and its one specific sentence
#   does not fit title 2: it says the tasks are statements ("väitelauseita")
#   to open up, where title 2 is a question ("Miten todellinen ystävyys
#   syntyy?"), and the concepts it names ("sinnikäs optimisti", "tärkeitä
#   elämäntaitoja") are printed in neither title (only "kannustamisen
#   kulttuuri", title 1's). Read as ruling 4's descriptive line for this
#   title. If the lead reads it as indicative content: [shown(L(100,
#   103))], whole=True on the paper's 40.
# - CENSUS GAP (not mine to card, flagged): the census has NO II1. The paper
#   prints title 1 as "1.“Suomessa kannustamisen kulttuuri ei ole hirveän
#   vahva.”" (p4 y709) with NO space after "1.", and the census keys only
#   "2. Miten todellinen ystävyys syntyy?" (II2). Title 1 is a printed ask
#   with no card and no exclusion.
# - I3's question is cut from the paper's line before the welded "5" (PC,
#   after the marker): "Kuvaa, millainen käsitys kasvattamisesta tekstin
#   (teksti 1) kautta esitetään."
# - I5's lead (82, "Vastauksessa kokelaan on ymmärrettävä tekstissä kohta:")
#   is cut off the first row and quoted in its note; the bracketed remarks
#   inside that row are the scheme's own and stay.
# - I4's "Tekstissä:" leads quoted once, in the first row's note.
# - 10f: Q3 and Q6 are reprinted with different wording; the paper's words
#   are the questions, the scheme's quoted on the cards.
# - Reading text pp2-4 (rendered: TEKSTI 2 ends on p4 at y213, above "I
#   TEHTÄVÄ"). The live cards of this sitting carry sourceMaterial.pages [4]:
#   flagged (P), not changed. No `pages` on II2 (the essay of a two-part
#   sitting).
# GLYPHS: none. ä ö read cleanly in every line used. Both documents set
#   U+2010 HYPHEN in "Salmela‐Aro", "koulu‐ura", "‐nuorilla",
#   "15‐vuotiailla", "MOTIVAATIO‐": a real hyphen character (rendered "-"),
#   printed so, not a mis-mapped glyph.


def _head_2022(n, after=None, before=None, lead='The scheme heads its answer'):
    return quote(S(n, after=after, before=before), lead=lead)


def _reprint_2022(a, b, after):
    return quote(L(a, b, after=after, before=' (5)'), lead='The scheme reprints this question as')


def _q3_2022(d, _census=None):
    return PC(4, '3. Kuvaa', after='3. ', before='5').text(d)


ESSAY_2022 = 'Kirjoita noin 300 sanan essee.'
Q3P_2022 = RX(60, r'\((\d)\)\s*$')

SPECS[2022] = [
    R('I3', [one(L(61, 63), Q3P_2022)], total=Q3P_2022,
      rownote=_reprint_2022(60, 60, '3. '), question=_q3_2022, pages=(2, 3, 4)),
    R('I4', [one(L(66, 69, after='Tekstissä: ', before=' (1 p.)'), RX(69, r'\((\d) p\.\)')),
             one(L(70, 71, after='Tekstissä: ', before=' (2 p.)'), RX(71, r'\((\d) p\.\)')),
             one(L(72, 74, after='Tekstissä: ', before=' (2 p.)'), RX(74, r'\((\d) p\.\)'))],
      rownote=_head_2022(66, before=' Salmela'), pages=(2, 3, 4)),
    R('I5', [shown(L(82, 87, after='kohta: ')), shown(L(88, 89)), shown(L(90, 91))], whole=True,
      rownote=_head_2022(82, before=' Salmela'), pages=(2, 3, 4)),
    R('I6', [shown(L(94, 95))], whole=True,
      rownote=quote(L(92, 93, after='6. ', before=' (5)'), lead='The scheme reprints this question as'),
      pages=(2, 3, 4)),
    # Title 1 (census ADDED_ASKS: printed "1.“Suomessa ..." with no space, p4 y709): the scheme's one
    # paragraph under the two titles names title 1's concept ("kannustamisen kulttuuri") among those to
    # develop: indicative content for this title (10a), shown on the paper's 40 (the lead's call; title 2
    # keeps the drafter's R4, the paragraph quoted).
    R('II1', [shown(L(100, 103))], whole=True, total=PARTP(),
      question=_q(PL(4, ESSAY_2022), PC(4, '1.“Suomessa', after='1.'))),
    R('II2', [unprinted(quote(L(100, 103), lead='Under the two titles the scheme prints only'))],
      question=QP(4, ESSAY_2022, '2. Miten todellinen')),
]


# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): all thirteen asks of this sitting,
# I1a-e, I2-I6, II1, III1, III2. No live card (the old reader excluded the
# whole sitting: "the scheme prices no ask at the address the paper prints").
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin tehtäviin suomeksi.
# ..." (p2 y65), "Kokeen maksimipistemäärä on 100 pistettä." (p2 y119);
# "TEKSTI 1" (p2 y163), its title and paragraphs 1)-6) to the byline "Marja
# Alkio, ... mielipidekirjoitus" (p2 y775); "TEKSTI 2" (p3 y65), its title
# and paragraphs 7)-16) to "Katkelma Tarja Roinilan esseestä / Helsingin
# Sanomat 7.6.2020" (p3 y691): the reading texts run pp2-3. "I TEHTÄVÄ" /
# "(30/100)" (p3 y719); Q1 "1. Selitä omin sanoin seuraavat ilmaisut:" with
# a) b) on p3 and c) d) e) on p4, "(5 × 1)" at the right of e) (p4 y109);
# Q3-Q6 "(5)" each (p4 y190, y234, y277, y321); "II TEHTÄVÄ" / "(30/100)" (p4
# y409); "III TEHTÄVÄ" / "(40/100)" (p4 y602), "Kirjoita noin 300 sanan
# essee. Valitse aiheeksi toinen näistä." over two titles numbered "1." /
# "2." (Section III Q1/Q2, ruling B).
# PRICES:
# - I1a-e: "(5 × 1)": five expressions at 1 each, adding to Q1's 5 (the
#   census walks it down to the letters: PP() each). Per letter, as every
#   live Finnish Q1.
# - I2: the paper prints NO price (rendered p4: Q2's two lines y146-160 have
#   nothing in the right-hand column, where Q3-Q6 each print "(5)"), and the
#   scheme prints no price for Q2-Q6 at all. It is the ONE unpriced ask of a
#   part whose printed total and every other price fix it: REM(PARTP(), the
#   five "(5 × 1)" letters, Q3-Q6's "(5)") = 30 - 25 = 5, the note on the row
#   (CARD-STANDARD 10i clarification).
# - I3-I6: "(5)" each (PP()).
# - II1: "(30/100)" (PARTP); scheme head "II TEHTÄVÄ (30/100)" (77).
# - III1/III2: "(40/100)" (PARTP), each title answered alone at the part's
#   40; scheme head "III TEHTÄVÄ (40/100)" (89).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; pp6-7
#   blank):
# - Part I head "TEHTÄVÄ (30/70)" (45): no numeral, and "/70" where the paper
#   prints "(30/100)" (the 2022 sitting was out of 70). A printed scheme
#   error; the paper's (30/100) governs (10f), quoted on I2, whose mark it
#   fixes.
# - Q1 (46 the stem, no number): "a) vaivihkaa = huomaamatta" (47), b) 48,
#   c) 49, d) 50, e) 51; each gloss after " = ". The scheme reprints d) as
#   "opetuksen puitteissa" where the paper prints "Oman äidinkielen
#   opetuksen puitteissa" (10f: quoted on the card), and sets Q1's price
#   INSIDE e): "e) vertaisryhmä (5 x 1) = samassa tilanteessa olevien ryhmä"
#   (51; rendered p3 the same).
# - Q2-Q6: each question reprinted (no price) and ONE plain paragraph under
#   it: Q2 54-55, Q3 57-59, Q4 62-65, Q5 71-73, Q6 75-76 ("Vastauksessa
#   edetään referoiden jommankumman kirjoittajan kantaa ja sen pohjalta
#   muodostetaan oma näkökulma", no closing stop).
# - Part II (77-80 reprint the head and the task, "noin 100 kommentti"
#   without "sanan"): ONE paragraph, 81-84, "Kirjoittaja voi pohtia, missä
#   määrin kolme viikkotuntia tulee kielenkehitystä. ... läksyjen
#   kannalta."
# - Part III (89-93 reprint the head, the instruction and both titles,
#   unnumbered): ONE paragraph for both, 94-96, "Esseen tulee olla
#   rakenteellisesti eheä: aiheeseen johdatteleva aloituskappale, selkeät
#   käsittelykappaleet ja kokoava päätäntä. Tehtävänanto edellyttää
#   omakohtaista pohdintaa ja sitä voi havainnollistaa esimerkein." No
#   criteria and no percentages anywhere in this scheme.
# SHAPES:
# - I1a-e: one(gloss) each at the printed 1.
# - I2-I5: one printed paragraph = one row at the printed 5 (I2 at the
#   remainder 5).
# - I6: the paragraph shown, priced as a whole on the paper's 5: it says how
#   the answer proceeds (summarise one writer's view, then form one's own),
#   a requirement, not a stated answer to claim.
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a).
# - III1, III2: R4 (unprinted) at the paper's 40, the note quoting the one
#   paragraph the scheme prints under both titles (ruling 4: structure and
#   "omakohtaista pohdintaa" for any title, nothing of either title's
#   content).
# JUDGEMENT CALLS:
# - III R4, not shown: the paragraph is wholly generic (the 2018/2019
#   paragraphs are printed under each title with a sentence of their own
#   about that title; this one names neither). If the lead reads it as
#   indicative content: [shown(L(94, 96))], whole=True on the paper's 40.
# - I2 at the remainder rather than 10i: it is the only unpriced ask of Part
#   I; the remainder uses printed figures only.
# - I4's model answer prints "saksan kielensä olleet riittävän hyvä" (65),
#   the SEC's own wording, lifted as printed.
# - Questions: I1c-e are printed on p4 under the p3 stem; the census joins
#   the stem to each (checked). II1's question is cut from the paper's three
#   lines (the census glues "(30/100)" in front). III1/III2: the
#   instruction, then the title; III2 keeps its printed attribution line
#   "(Maija Vilkkumaa, suomalainen rockmuusikko)".
# - Reading text pp2-3 (rendered); II1 travels with it. No live card to
#   compare.
# GLYPHS: none. ä ö read cleanly in every line used ("kiistämättömät",
#   "Osattomuuden tunne vyöryi päälleni", "kyseenalaistaa" checked on the
#   render). The scheme's "tasa‐" (52) sets U+2010 HYPHEN, printed so.


def _rem_2023():
    return REM(PARTP(), PP('I1a'), PP('I1b'), PP('I1c'), PP('I1d'), PP('I1e'),
               PP('I3'), PP('I4'), PP('I5'), PP('I6'))


Q2P_2023 = _rem_2023()
ESSAY_2023 = 'Kirjoita noin 300 sanan essee.'
III_NOTE_2023 = quote(L(94, 96), lead='Under the two titles the scheme prints only')

SPECS[2023] = [
    R('I1a', [one(S(47, after='= '), PP())], pages=(2, 3)),
    R('I1b', [one(S(48, after='= '), PP())], pages=(2, 3)),
    R('I1c', [one(S(49, after='= '), PP())], pages=(2, 3)),
    R('I1d', [one(S(50, after='= '), PP())],
      rownote=quote(S(50, after='d) ', before=' ='), lead='The scheme reprints this expression as'),
      pages=(2, 3)),
    R('I1e', [one(S(51, after='= '), PP())], pages=(2, 3)),
    R('I2', [one(L(54, 55), Q2P_2023)], total=Q2P_2023,
      rownote=both(Q2P_2023.note, quote(S(45), lead='The scheme heads Part I')), pages=(2, 3)),
    R('I3', [one(L(57, 59), PP())], pages=(2, 3)),
    R('I4', [one(L(62, 65), PP())], pages=(2, 3)),
    R('I5', [one(L(71, 73), PP())], pages=(2, 3)),
    R('I6', [shown(L(75, 76))], whole=True, pages=(2, 3),
      rownote=quote(S(74, after='6. '), lead='The scheme reprints this question as')),
    R('II1', [shown(L(81, 84))], whole=True,
      rownote=quote(L(78, 80), lead='The scheme reprints the task as'),
      question=QP(4, Run('Kirjoita noin 100 sanan kommentti', 'opetuksen puitteissa.”')), pages=(2, 3)),
    R('III1', [unprinted(III_NOTE_2023)],
      question=QP(4, ESSAY_2023, '1. Monikielisen')),
    R('III2', [unprinted(III_NOTE_2023)],
      question=QP(4, ESSAY_2023, '2. ”Maailma on kaaos', '(Maija Vilkkumaa')),
]


# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this
# sitting, I2-I6, II1, III1, III2. Live: I1a-e (5 cards); not touched
# (audited: see finnish-live-faults-2018-2025.json).
# Paper (rendered pp2-4): the rule "Ohje: Vastaa kaikkiin tehtäviin suomeksi.
# ..." (p2 y65); "TEKSTI:" (p2 y138), the title "Moni ei enää jaksa keskittyä
# kirjojen lukemiseen – ..." (p2 y153) and paragraphs 1)-9) on p2, 10)-19) on
# p3 to the byline "Katri Kallionpää, Helsingin Sanomat 1.10.2023" (p3 y680):
# the reading text runs pp2-3. p4: "I TEHTÄVÄ" / "(30/100)" (y65); Q1 a.-e.
# under "(5 × 1 pistettä)" (y197); Q2-Q6 "(5 pistettä)" each in the right
# column (Q6's on its second line, y387); "II TEHTÄVÄ" / "(30/100)" (y446);
# "III TEHTÄVÄ" / "(40/100)" (y578), "Kirjoita noin 300 sanan essee. Valitse
# aiheeksi toinen näistä." over two titles numbered "1." / "2." joined by
# "tai" (Section III Q1/Q2, ruling B).
# PRICES:
# - I2-I6: "(5 pistettä)" each (PP(): the census reads every one).
# - II1: "(30/100)" (PARTP); scheme head "II TEHTÄVÄ (30/100)" (76).
# - III1/III2: "(40/100)" (PARTP), each title answered alone at the part's
#   40; scheme head "III TEHTÄVÄ (40/100)" (81).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2; pp5-6
#   blank):
# - Q2 (54): the question reprinted "2 Miksi ADT ei ole virallinen
#   diagnoosi?" and its answer on the SAME line, running on to 55: "Se on
#   itseaiheutettu eikä perinnöllinen tautiluokitettu neuropsykologinen
#   sairaus."
# - Q3-Q6: each reprinted (no price) over ONE plain paragraph: Q3 57-58, Q4
#   60-62, Q5 64-66, Q6 69-71.
# - Part II (76; 77-78 reprint the task in short, "Arvioi oman kokemuksesi
#   perusteella, ..."): ONE paragraph, 79-80, "Mielipide tulee rakentua
#   dialogissa kolmeen tekstissä esitettyyn rajoitukseen eli aikaan,
#   paikkaan ja ihmissuhteisiin liittyviin tilanteisiin. Oma reflektio tulee
#   olla mukana."
# - Part III (81; the instruction reprinted as "Kirjoita noin 300 sanan
#   pituinen yhtenäinen teksti." where the paper prints "Kirjoita noin 300
#   sanan essee.", 82): title 1 reprinted as the paper prints it (83) with
#   ONE paragraph, 84-86 ("Keskustelua on käyty hallitustasolla ...
#   argumentteja puolesta ja vastaan."). Title 2 is NOT the paper's: the
#   scheme prints "2. Kenellä on vastuu älylaitteiden käytöstä ‐
#   valmistajalla, valtiolla vai käyttäjillä? Kirjoita pohtiva teksti, jossa
#   tarkastelet asiaa monelta kannalta." (87-88; rendered scheme p4, bold)
#   and a paragraph answering THAT title (89-95, "Huotilainen tuo esiin, että
#   yksittäistä käyttäjää on turha syyllistää. ..."). The paper's title 2 is
#   "”Lukeminen parantaa muistia, lievittää stressiä ja jopa pidentää ikää”,
#   sanoo aivotutkija Minna Huotilainen. Kirjoita pohtiva teksti, jossa
#   tarkastelet lukemisen merkitystä aivoterveyden kannalta." (p4 y723-754).
#   No criteria, no percentages.
# SHAPES:
# - I2-I6: one printed paragraph = one row at the printed 5 each.
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a).
# - III1: title 1's own paragraph shown, priced as a whole on the paper's 40
#   (10a; Danish 2025 the precedent).
# - III2: R4 (unprinted) at the paper's 40 (10f: the paper wins). The note
#   quotes the different title the scheme reprints and says the scheme gives
#   no answer for the paper's title; the scheme's paragraph for its own
#   title is not shown (it answers a question the student was not asked).
# JUDGEMENT CALLS:
# - I2's row is cut after the reprinted question on the same line
#   ("diagnoosi? ").
# - II1 and III1 are shown, not R4: each paragraph says what this task's
#   answer works through (time, place and relationship limits; the debate
#   at government level, arguments for and against).
# - The scheme's differing reprints (Part II's shortened task, Part III's
#   instruction) are noted here only; neither changes an answer.
# - Questions: II1 cut from the paper's two lines (the census glues
#   "(30/100)" in front); III1 the instruction and the title (the census
#   glues "tai" onto it); III2 the instruction and the title's three lines.
# - Reading text pp2-3 (rendered); II1 travels with it. The live cards of
#   this sitting carry sourceMaterial.pages [4] (the questions page):
#   flagged (P), not changed.
# GLYPHS: none. ä ö read cleanly in every line used ("tarkkaavuusvajetta",
#   "älylaitteiden", "käyttökelpoisia" checked on the render). The scheme
#   sets U+2010 HYPHEN in "vapaa‐ajanviettotapana" (57) and its title 2's
#   dash (87): real hyphen characters, printed so.


def _other_title_2024(d):
    return (f'The marking scheme reprints a different title here (“{L(87, 88, after="2. ").text(d)}”) '
            f'and gives no answer for the title the paper prints.')


ESSAY_2024 = 'Kirjoita noin 300 sanan essee.'

SPECS[2024] = [
    R('I2', [one(L(54, 55, after='diagnoosi? '), PP())], pages=(2, 3)),
    R('I3', [one(L(57, 58), PP())], pages=(2, 3)),
    R('I4', [one(L(60, 62), PP())], pages=(2, 3)),
    R('I5', [one(L(64, 66), PP())], pages=(2, 3)),
    R('I6', [one(L(69, 71), PP())], pages=(2, 3)),
    R('II1', [shown(L(79, 80))], whole=True,
      rownote=quote(L(77, 78), lead='The scheme restates the task as'),
      question=QP(4, Run('Kirjoita noin 100', 'ovatko tutkijoiden')), pages=(2, 3)),
    R('III1', [shown(L(84, 86))], whole=True,
      rownote=quote(S(82), lead='The scheme reprints the instruction as'),
      question=QP(4, ESSAY_2024, '1. Pitäisikö koulussa')),
    R('III2', [unprinted(both(lambda d: quote(S(82), lead='The scheme reprints the instruction as')(d),
                              _other_title_2024))],
      question=QP(4, ESSAY_2024, Run('2. ”Lukeminen parantaa', 'kannalta.'))),
]


# ====================================================================== 2025
# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this
# sitting, II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched
# (audited: see finnish-live-faults-2018-2025.json).
# Paper (rendered pp2-4): "Ohje:" (p2 y65) over the rule "Vastaa kaikkiin
# tehtäviin suomeksi. ..." (p2 y89); "TEKSTI 1" (p2 y176), the title
# "Piipahdus luonnossa voi tehdä terveydelle ihmeitä: ..." (p2 y200) and
# paragraphs (1)-(5) on p2, (6)-(14) on p3 to the byline "Piia Elonen,
# Helsingin Sanomat 29.10.2024" (p3 y784): the reading text runs pp2-3. p4:
# "I TEHTÄVÄ" / "(30/100)" (y65), Q1-Q6; "II TEHTÄVÄ" / "(30/100)" (y442),
# the quotation "“Luontoa pitäisi tarjota hoitona terveydenhuollossa niin
# vastaanottokäynneillä kuin erilaisissa digitaalisissa hoitopoluissa.”"
# (y466-481) over "Kirjoita noin 100–150 sanaa kommentti artikkelin
# esittämään ajatukseen." (y510); "III TEHTÄVÄ" / "(40/100)" (y572),
# "Kirjoita vähintään 300 sanan pituinen essee. Valitse aiheeksi toinen
# näistä." (y596) over two titles numbered "1." / "2." joined by "tai"
# (Section III Q1/Q2, ruling B).
# PRICES:
# - II1: "(30/100)" (PARTP); scheme head "II TEHTÄVÄ (30/100)" (99).
# - III1/III2: "(40/100)" (PARTP), each title answered alone at the part's
#   40; scheme head "III TEHTÄVÄ (40/100)" (108).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 4-5; p3 the
#   annotations table, pp6-8 blank but for their page numbers):
# - Part II (99): the task reprinted at length, 100-102 ("Kirjoita noin
#   100–150 sanan kommentti artikkelin esittämään ajatukseen, jonka mukaan
#   Suomessa tulisi olla kansallinen luontoterveysohjelma, ... “niin
#   vastaanottokäynneillä kuin erilaisissa digitaalisessa hoitopoluissa”."),
#   then ONE paragraph of questions the comment can take up, 103-107 ("Miten
#   Suomen talvessa onnistuu luonnossa annettava synnytysvalmennus tai
#   uniapnean ryhmävastaanotto? ... Miten järjestetään turvallisia
#   luontopolkuja haja-asutusalueille?"). The exclusion's "the scheme prints
#   NOTHING under this task" is wrong.
# - Part III (108): the instruction reprinted as "Kirjoita noin 300 sanan
#   essee. Valitse aiheeksi toinen näistä." (109; the paper prints
#   "vähintään 300 sanan pituinen essee") and the two titles, unnumbered,
#   joined by "tai" (110-114). Nothing else: no answer, no guidance, no
#   criteria (rendered p5; pp6-8 blank).
# SHAPES:
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a); the
#   scheme's longer restatement of the task quoted in the note (10f: the
#   paper's task is the question).
# - III1, III2: R4 (unprinted) at the paper's 40, the note quoting what the
#   scheme prints (its instruction; ruling 4).
# JUDGEMENT CALLS:
# - II1's paragraph breaks the compound "haja-asutusalueille" at the line end
#   ("haja-" / "asutusalueille?", 106-107; rendered p5): joined with no space
#   (Join sep='', as Estonian 2023 Part II), so the row reads the printed
#   word.
# - III notes quote the scheme's instruction, which differs from the
#   paper's ("noin" for "vähintään ... pituinen"): the paper's words are the
#   question (10f).
# - Questions: II1 is the quotation and the task line as printed (the census
#   glues "(30/100)" in front); III1 the instruction and the title (the
#   census keys it as printed); III2 the instruction and the title's three
#   lines.
# - Reading text pp2-3 (rendered); II1 travels with it. The live cards of
#   this sitting carry sourceMaterial.pages [4] (the questions page):
#   flagged (P), not changed.
# GLYPHS: none. ä ö read cleanly in every line used. The scheme sets this
#   year in a font with "tt"/"ti" ligatures (rendered "artikkelin",
#   "tietoja"); the text layer reads them as plain letters (no stray code
#   points: checked over the whole .md).


ESSAY_2025 = 'Kirjoita vähintään 300 sanan'
III_NOTE_2025 = quote(S(109), lead='The scheme prints nothing under the two titles. It reprints the instruction as')

SPECS[2025] = [
    R('II1', [shown(J(L(103, 105), Join(S(106), S(107), sep='')))], whole=True,
      rownote=quote(L(100, 102), lead='The scheme restates the task as'),
      question=QP(4, Run('“Luontoa pitäisi tarjota', 'digitaalisissa hoitopoluissa'), 'Kirjoita noin 100–150'),
      pages=(2, 3)),
    R('III1', [unprinted(III_NOTE_2025)],
      question=QP(4, ESSAY_2025, '1. “Mennään metsään”')),
    R('III2', [unprinted(III_NOTE_2025)],
      question=QP(4, ESSAY_2025, Run('2. ”Ellemme varmuudella', 'nykymaailmassa.'))),
]
