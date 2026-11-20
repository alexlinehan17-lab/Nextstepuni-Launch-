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
    R('I4', [one(L(69, 73), Q4_2014)], total=Q4_2014,
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
HEAD_2015 = L(112, 113)
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
