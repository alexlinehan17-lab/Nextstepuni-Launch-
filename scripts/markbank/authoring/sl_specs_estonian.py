#!/usr/bin/env python3
"""Reviewed specs for the Estonian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/estonian/schemes/<year>-hl.md.
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
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# I4, II1, III1. Live: I1a-e, I2, I3, I5, I6 (9 cards); not touched (audited:
# see estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Vasta kõigile kolmele ülesandele. Kõikidele
# küsimustele tuleb vastata eesti keeles." (p2 y70); "I. ÜLESANNE (30 / 100)"
# (p2 y104); the article "KELLELE ON TRANSRASVAD KASULIKUD?" runs pp2-3
# (title p2 y162, paragraphs 1-10 to the byline "Roy Strider, ..." p3 y636);
# Q1 "(5 × 1)" (p3 y670) over a)-e); Q2-Q6 "(5)" each (p4); "II. ÜLESANNE
# (30 / 100)" (p4 y305); "III. ÜLESANNE (40 / 100)" (p4 y415), "Kirjuta umbes
# 300sõnaline kirjand. Vali üks antud teemadest." (y442) over two NUMBERED
# titles "1) Keegi ei ole saar" and "2) Mainimatajätmine ei tähenda
# valetamist" (rendered p4).
# PRICES:
# - I4: the census reads no price (tariff None): the paper PRINTS "(5)" on a
#   line of its own under the question (p4 y153, right margin, bold; rendered).
#   PY cannot read it (its cell pattern needs a mark word; this paper prints a
#   bare "(5)"), and PaperP cannot pick it (five lines of p4 open "(5)"). Priced
#   from the scheme's own printed "(5)" at the end of its reprint of Q4 (line
#   49, "kaasajal? (5)"), the same 5 (RX). If the lead extends PY to bare
#   bracketed cells: PY(4, 153). Not a remainder, not 10i.
# - II1: the part head's "(30 / 100)" (PARTP); the scheme heads the part "II.
#   ÜLESANNE kuni 30 punkti" (103).
# - III1: "(40 / 100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti" (120).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; answers in
# italics):
# - Q4 (48-49 reprint the question with "(5)"): "Võimalikud vastused:" (50,
#   italic) over three bullets, 51-55 ("Seni on kõige tervislikumaks ...
#   pikk."), 56-57 ("Keskkonnaprobleemid – ... saastatud."), 58-59
#   ("Tarbimishullus ... tooteid/brände."). Possible answers, no split.
# - Criteria (p4 top, 95-102): "II ja III ülesande hindamisel arvestatakse
#   järgmisi kriteeriume:" (bold underlined) -- for Parts II AND III. 1.
#   Teemast arusaamine ja sisu "– 30%" (96-97), 2. Teksti ülesehitus "30%"
#   (98-99), 3. Sõnavara ja stiil "– 30%" (100-101), 4. Õigekiri "– 10%" (102):
#   all four printed, 100 %.
# - Part II (103): a bold descriptive line, 104, "Umbes 100sõnaline ladus
#   kommentaar tõestamaks teksti sisust arusaamist."; "Näiteks:" (105) over six
#   indented italic items, 106, 107-108, 109-112, 113-115, 116-117, 118, and
#   "Jne." (119).
# - Part III (120): one descriptive line, 121-122, "Vähemalt 300sõnaline sidus
#   teemakohane kirjand läbimõeldud sisu, selge ülesehituse ning sorava
#   lausestusega." Nothing per title.
# SHAPES:
# - I4: the three bullets shown, priced as a whole on the 5 (questionTotal,
#   10a); the heading "Võimalikud vastused:" quoted.
# - II1: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3. Head: the descriptive
#   line (104); the items quoted under the scheme's own "Näiteks:" as examples,
#   not a checklist (10a); the criteria's lead quoted (it names Parts II and III).
# - III1: graded (10b), 12/12/12/4 of 40. Head: the descriptive line (121-122);
#   lead quoted.
# JUDGEMENT CALLS:
# - Part II's "Jne." (119, "etc.") is left out of the quoted examples: it is
#   not an example; the note already says "as examples, not a checklist".
# - Part II item 118 ("Aktiivsed kodanikud, ...") is set with no gap under
#   116-117 (rendered); quoted as its own item (it opens a new line and a new
#   topic, as every other item).
# - The scheme's descriptive line for Part III says "Vähemalt 300sõnaline"
#   (at least 300 words) where the paper asks "umbes 300sõnaline" (about 300):
#   the head is the scheme's own line, lifted as printed; the question is the
#   paper's (10f, paper wins on the question; the scheme's words are visible in
#   the head itself).
# - III1's question: the instruction line, then title 1. The text layer welds
#   title 2 onto title 1's line ("1) Keegi ei ole saar Mainimatajätmine ei
#   tähenda valetamist", p4 y470; "2)" alone at y484), so title 1 is cut from
#   that printed line before " Mainimatajätmine" (PC), the marker cut off.
# CENSUS GAP (for the lead): the paper prints TWO numbered titles (rendered
#   p4: "1) Keegi ei ole saar", "2) Mainimatajätmine ei tähenda valetamist"),
#   but the census keys only III1 (the welded line), so III2 is in neither the
#   live bank nor the exclusions. Under ruling B it is its own ask. Ready spec
#   once the census adds it (same graded head and criteria as III1):
#     R('III2', [graded(L(121, 122), PARTP(), CRIT_2010)], rownote=LEAD_2010,
#       question=_q(PL(4, 'Kirjuta umbes 300sõnaline'),
#                   PC(4, '1) Keegi', after='saar '))),
# - Reading text: pp2-3 (rendered: rule and title p2, the text to its byline
#   p3 y636; Q1 from p3 y670). I4 and II1 carry it: pages=(2, 3). The live
#   cards' sourceMaterial.pages [2, 3] agree with the render.
# GLYPHS: none. õ ä ö ü š ž read cleanly in every line used (paper and scheme;
#   "kokkujooksutamine", "Mainimatajätmine", "sabotaaž" checked on the render).

def _q(*sels):
    """A question cut from printed paper lines: each line (or cut) in order,
    joined by a space."""
    return lambda d, _q: ' '.join(s.text(d) for s in sels)


CRIT_2010 = crit((96, 97), (98, 99), (100, 101), 102)
LEAD_2010 = quote(S(95), lead='The scheme prints')
SPECS[2010] = [
    R('I4', [shown(L(51, 55)), shown(L(56, 57)), shown(L(58, 59))], whole=True,
      total=RX(49, r'\((\d)\)'), rownote=quote(S(50), lead='The scheme heads them'), pages=(2, 3)),
    R('II1', [graded(S(104), PARTP(), CRIT_2010)],
      rownote=both(examples(S(105), S(106), L(107, 108), L(109, 112), L(113, 115), L(116, 117), S(118)),
                   LEAD_2010),
      question=QP(4, Run('„Kui valitsused', 'Kirjuta umbes 100sõnaline')), pages=(2, 3)),
    R('III1', [graded(L(121, 122), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=_q(PL(4, 'Kirjuta umbes 300sõnaline'), PC(4, '1) Keegi', after='1) ', before=' Mainimatajätmine'))),
    # III2: the text layer welds title 2 onto title 1's line; the census keys it by
    # paper_census.ADDED_ASKS (lead, 20 Nov), title 2 cut from that line.
    R('III2', [graded(L(121, 122), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=_q(PL(4, 'Kirjuta umbes 300sõnaline'), PC(4, '1) Keegi', after='saar '))),
]


# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Vasta kõigile kolmele ülesandele.
# Kõikidele küsimustele tuleb vastata eesti keeles." (p2 y77); "I. ÜLESANNE
# (30 / 100)" (p2 y110); the article "KUIDAS TEKIVAD RAHVUSLIKUD
# STEREOTÜÜBID?" runs pp2-3 (title p2 y168, paragraphs 1-11 to the byline
# "Jaan Lahe, ..." p3 y472); Q1 "(5 × 1)" (p3 y527); Q2-Q6 "(5)" each (p3);
# "II. ÜLESANNE: (30 / 100)" on one line (p4 y77); "III. ÜLESANNE: (40 /
# 100)" (p4 y239), "Kirjuta umbes 300sõnaline kirjand. Vali üks antud
# teemadest." (y260) over two NUMBERED titles "1) „Enamik inimesi ...“.
# (Abraham Lincoln ...)" (y294-308) and "2) Võrdlemine on osa meie kõigi
# igapäevast" (y337).
# PRICES:
# - II1: the head's own "(30 / 100)" (PARTP; the census reads only Part I's
#   total this sitting, so PARTP reads the head's own line). The scheme heads
#   the part "II. ÜLESANNE kuni 30 punkti" (70).
# - III1/III2: "(40 / 100)" (PARTP, head's own line); scheme "III. ÜLESANNE
#   kuni 40 punkti" (87).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2; pp1-2
# cover and blank, pp5-8 blank):
# - Criteria (p4, 62-69): "II ja III ülesande hindamisel arvestatakse järgmisi
#   kriteeriume:" -- Parts II AND III. 1. Teemast arusaamine ja sisu "– 30%"
#   (63-64), 2. Teksti ülesehitus "30%" (65-66), 3. Sõnavara ja stiil "– 30%"
#   (67-68), 4. Õigekiri "– 10%" (69): all four printed, 100 %.
# - Part II (70): a descriptive line, 71, "Umbes 100sõnaline ladus
#   kommentaar, tõestamaks teksti sisust arusaamist."; "Näiteks:" (72) over
#   four bullets, 73-76, 77-80, 81-82, 83-85, and "Jne." (86).
# - Part III (87): one descriptive line, 88-89, "Vähemalt 300sõnaline sidus
#   teemakohane kirjand ...". Nothing per title.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (71); the
#   four bullets quoted under "Näiteks:" as examples, not a checklist (10a);
#   the criteria's lead quoted.
# - III1/III2: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (88-89); lead quoted.
# JUDGEMENT CALLS:
# - "Jne." (86) left out of the quoted examples (not an example).
# - Title 2 is printed "Võrdlemine on osa meie kõigi igapäevast" with no
#   further word (rendered p4: the line ends there, nothing below it; the
#   phrase reads as unfinished). Lifted as printed; flagged for the lead.
# - Part III: the scheme's line says "Vähemalt 300sõnaline" where the paper
#   asks "umbes 300sõnaline"; the head is the scheme's own line, the question
#   the paper's (10f).
# - II1's question is cut from the paper's lines (quotation, then the task);
#   the census glues the head's "(30 / 100)" in front.
# - III1 keeps the title's attribution "(Abraham Lincoln (1809–1865),
#   Ameerika Ühendriikide 16. president)", printed as part of the title over
#   two lines (y294-308).
# - Reading text: pp2-3 (rendered). II1 quotes paragraph 11, so the text
#   travels with it: pages=(2, 3). The live cards' sourceMaterial.pages [2, 3]
#   agree with the render.
# GLYPHS: none. õ ä ö ü read cleanly in every line used (paper and scheme).

CRIT_2011 = crit((63, 64), (65, 66), (67, 68), 69)
LEAD_2011 = quote(S(62), lead='The scheme prints')
ESSAY_2011 = 'Kirjuta umbes 300sõnaline'
SPECS[2011] = [
    R('II1', [graded(S(71), PARTP(), CRIT_2011)],
      rownote=both(examples(S(72), L(73, 76), L(77, 80), L(81, 82), L(83, 85)), LEAD_2011),
      question=QP(4, Run('„Stereotüüpidel', 'kommunikatsiooni'), Run('Kuidas teeb', 'suhtlemise lihtsamaks')),
      pages=(2, 3)),
    R('III1', [graded(L(88, 89), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, ESSAY_2011, Run('1) „Enamik', 'Lincoln (1809'))),
    R('III2', [graded(L(88, 89), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, ESSAY_2011, '2) Võrdlemine')),
]


# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the five open asks of this sitting,
# I4, I5, II1, III1, III2. Live: I1a-e, I2, I3, I6 (8 cards); not touched
# (audited: see estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the instruction and rule "Loe läbi alljärgnev tekst
# ja vasta küsimustele ülesannetes I, II ja III. Kõikidele küsimustele tuleb
# vastata eesti keeles." (p2 y78-92); the article "MIKS ME USUME
# MUINASJUTTUDESSE?" runs pp2-3 (title p2 y133, paragraphs 1-11 to the
# byline "Merit Valge, ..." p3 y685); "I. ÜLESANNE (30 / 100)" opens p4
# (y84); Q1 "(5 × 1)" (p4 y149); Q2-Q6 "(5)" each (p4); "II. ÜLESANNE: (30 /
# 100)" (p4 y543); "III. ÜLESANNE: (40 / 100)" (p4 y660), "Kirjuta umbes
# 300sõnaline kirjand. Vali üks antud teemadest." over two NUMBERED titles
# "1) Lootusel on mitu nägu" and "2) Meie tänapäeva ühiskonnas on kõik
# keskendunud siia ja praegu" (y708, y729).
# PRICES:
# - I4, I5: "(5)" each, a cell beside the question's last line (p4 y329,
#   y412; rendered), read by the census (PP). The scheme prints the same
#   "(5)" (41, 54).
# - II1: the head's "(30 / 100)" (PARTP); scheme "II. ÜLESANNE kuni 30
#   punkti" (93).
# - III1/III2: "(40 / 100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti"
#   (114).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; answers
# in italics):
# - Q4 (39-41 reprint the question with "(5)"): one paragraph, 42-49
#   ("Kommunistlik režiim püüdis usku ... Riikide religioosne taust on väga
#   erinev."). The exclusion's "the scheme states no answer for this ask" is
#   wrong: the paragraph is printed under the reprint (rendered p3).
# - Q5 (50-54 reprint the question with "(5)", p3): TWO paragraphs on p4,
#   58-65 ("Autor tõestab oma väidet Ameerika ja Malta näite varal. ... See
#   teeb Ameerikast ühe ebausklikuma lääne riigi.") and 66-69 ("Malta seevastu
#   on ... suhteliselt vastuvõtmatud."), a gap between them (rendered). The
#   answer opens a new page: the exclusion's "does not hold this answer as
#   one run of words" is the page break (lines 55-57); each paragraph is one
#   run in the .md.
# - Criteria (p4, 85-92, the lead underlined): "II ja III ülesande hindamisel
#   arvestatakse järgmisi kriteeriume:" -- Parts II AND III. 1. "– 30%"
#   (86-87), 2. "– 30%" (88-89), 3. "– 30%" (90-91), 4. "– 10%" (92): 100 %.
# - Part II (93): a descriptive line, 94, "Umbes 100sõnaline ladus
#   kommentaar, tõestamaks teksti sisust arusaamist."; on p5 "Näiteks:" (98)
#   over two italic paragraphs, 99-104 and 105-113.
# - Part III (114): one descriptive line, 115-116; then the two titles
#   reprinted as on the paper (117, 118) with nothing under either.
# SHAPES:
# - I4: one stated answer (one printed paragraph): one row at the paper's 5.
# - I5: the two paragraphs shown, priced as a whole on the paper's 5
#   (questionTotal, 10a; Romanian 2016 Q6, 2020 Q2-Q5: several paragraphs are
#   shown, one paragraph is one row).
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (94); the two
#   paragraphs quoted under "Näiteks:" as examples, not a checklist (10a);
#   the criteria's lead quoted.
# - III1/III2: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (115-116); lead quoted.
# JUDGEMENT CALLS:
# - I4: line 44 opens with a dash that belongs to the sentence ("... erinevalt"
#   / "– nt religiooni ...", rendered p3): kept with SR(44), which the bullet
#   strip of S would drop.
# - I5 shown, not one claimable row: the two paragraphs are one model answer
#   (America, then Malta). The live Part I cards of this subject claim
#   several-paragraph answers as one row (flagged as advisory in the live
#   faults file); if the lead prefers that here, flip to one(L(58, 69), PP()).
# - The scheme's Part III line says "Vähemalt 300sõnaline"; the paper asks
#   "umbes 300sõnaline" (10f: the paper's question, the scheme's head).
# - II1's question is cut from the paper's lines (the census glues the head's
#   "(30 / 100)" in front).
# - Reading text: pp2-3 (rendered: rule, title and paragraphs 1-5 on p2,
#   paragraphs 6-11 and the byline on p3; Part I opens p4). I4, I5, II1 carry
#   it: pages=(2, 3). The live cards' sourceMaterial.pages are [4] (the
#   questions' page): the render does not agree (flagged, P).
# GLYPHS: none. õ ä ö ü ž read cleanly in every line used ("režiimi" 42,
#   checked on the render).

CRIT_2012 = crit((86, 87), (88, 89), (90, 91), 92)
LEAD_2012 = quote(S(85), lead='The scheme prints')
ESSAY_2012 = 'Kirjuta umbes 300sõnaline'
SPECS[2012] = [
    R('I4', [one(J(L(42, 43), SR(44), L(45, 49)), PP())], pages=(2, 3)),
    R('I5', [shown(L(58, 65)), shown(L(66, 69))], whole=True, pages=(2, 3)),
    R('II1', [graded(S(94), PARTP(), CRIT_2012)],
      rownote=both(examples(S(98), L(99, 104), L(105, 113)), LEAD_2012),
      question=QP(4, Run('Artikkel kannab pealkirja', 'Kirjuta umbes 100sõnaline')), pages=(2, 3)),
    R('III1', [graded(L(115, 116), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, ESSAY_2012, '1) Lootusel')),
    R('III2', [graded(L(115, 116), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, ESSAY_2012, '2) Meie tänapäeva')),
]


# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1 and III1. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the instruction and rule "Loe läbi alljärgnev tekst
# ja vasta küsimustele I, II ja III ülesandes. Kõikidele küsimustele tuleb
# vastata eesti keeles." (p2 y64-78); the article "KAS JÄÄKARUD IKKA JÄÄVAD
# ELLU?" runs pp2-3 (title p2 y105, the text to the byline "Arvi Liiva, ..."
# p3 y701 and the author's note y721); "I. ÜLESANNE (30 / 100)" opens p4
# (y70); "II. ÜLESANNE: (30 / 100)" (p4 y567); "III. ÜLESANNE: (40 / 100)"
# (p4 y651), "Kirjuta umbes 300-sõnaline arutlev kirjand. Vali üks antud
# teemadest." (y672) over two UNNUMBERED titles, "Inimene on looduse kroon"
# (y706) and "Oma unistuste täide viimine – kibemagus teekond" (y761), with
# "VÕI" between them (y734): the census counts one ask, III1 (as Danish
# 2011-2012's dashed titles).
# PRICES:
# - II1: the head's "(30 / 100)" (PARTP); scheme "II. ÜLESANNE kuni 30
#   punkti" (118).
# - III1: "(40 / 100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti" (137).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# standard note to teachers):
# - Criteria (p4, 106-113, the lead bold): "II ja III ülesande hindamisel
#   arvestatakse järgmisi kriteeriume:" -- Parts II AND III. 1. "– 30%"
#   (107-108), 2. "– 30%" (109-110), 3. "– 30%" (111-112), 4. "– 10%" (113):
#   100 %.
# - Part II (p5, 118): a descriptive line, 119, "Umbes 100sõnaline ladus
#   kommentaar, tõestamaks teksti sisust arusaamist."; "Näiteks:" (120) over
#   five italic items, 121-124, 125-127, 128-130, 131-132, 133-135, and "Jne."
#   (136).
# - Part III (137): one descriptive line, 138-139. Nothing per title.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (119); the
#   five items quoted under "Näiteks:" as examples, not a checklist (10a);
#   the criteria's lead quoted.
# - III1: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (138-139); lead quoted. One card carries both unnumbered titles.
# JUDGEMENT CALLS:
# - "Jne." (136) left out of the quoted examples (not an example).
# - The paper asks for "umbes 100sõnaline arvamus" (Part II) and "umbes
#   300-sõnaline arutlev kirjand" (Part III); the scheme's lines say
#   "kommentaar" and "Vähemalt 300sõnaline sidus ... kirjand": each card's
#   question is the paper's, its head the scheme's own line (10f).
# - III1's question: the instruction, then each title on a line of its own
#   (QL), "VÕI" left out. If the lead wants a card per title, it needs a
#   coordinator ruling (the titles are unnumbered; the census keys one ask).
# - II1's question is cut from the paper's lines (the census glues the head's
#   "(30 / 100)" in front).
# - Reading text: pp2-3 (rendered: rule, title and the opening paragraphs on
#   p2, the rest, byline and author's note on p3; Part I opens p4). II1 cites
#   paragraph 4: pages=(2, 3). The live cards' sourceMaterial.pages are [4]:
#   the render does not agree (flagged, P).
# GLYPHS: none. The paper prints "Kyōto" with o-macron (U+014D) in the text
#   and Q2, and "(∗)" (U+2217) as a footnote mark in the text (p2): both
#   drawn so on the render; not in the lines used here.

CRIT_2013 = crit((107, 108), (109, 110), (111, 112), 113)
LEAD_2013 = quote(S(106), lead='The scheme prints')
SPECS[2013] = [
    R('II1', [graded(S(119), PARTP(), CRIT_2013)],
      rownote=both(examples(S(120), L(121, 124), L(125, 127), L(128, 130), L(131, 132), L(133, 135)),
                   LEAD_2013),
      question=QP(4, Run('Artikli 4. lõigus', 'pealkirja? Kirjuta')), pages=(2, 3)),
    R('III1', [graded(L(138, 139), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      # the paper prints "VÕI" on its own line between the two titles (second reader)
      question=QL(4, 'Kirjuta umbes 300-sõnaline', 'Inimene on looduse kroon', 'VÕI', 'Oma unistuste täide')),
]


# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Vasta küsimustele ülesannetes I, II ja
# III. Kõikidele küsimustele tuleb vastata eesti keeles." (p2 y77); "I.
# ÜLESANNE (30 / 100)" (p2 y139) over the article, which runs pp2-3 (to the
# byline "Maarja Vaino, ..." p3 y666 and the author's note y686); Q1 "(5 ×
# 1)" opens p4 (y78); Q2-Q6 "(5)" each; "II. ÜLESANNE (30 / 100)" (p4 y514),
# a quotation and "Kirjuta umbes 100sõnaline kommentaar selle seisukoha
# kohta." (y578); "III. ÜLESANNE (40 / 100)" (p4 y646), "Kirjuta umbes
# 300sõnaline kirjand. Vali üks antud teemadest." (y667) over two NUMBERED
# titles, "1) „Lugeja jõuab elada tuhat elu, mittelugeja vaid ühe.” (George
# R. R. Martin)" (y695) and "2) „Isegi kui käia läbi kogu maailm, ...”
# (Ralph Waldo Emerson)" (y739), each attribution in italics.
# PRICES:
# - II1: the head's "(30 / 100)" (PARTP); scheme "II. ÜLESANNE kuni 30
#   punkti" (102).
# - III1/III2: "(40 / 100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti"
#   (116).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; p2 the
# standard note to teachers):
# - Criteria (p4, 95-101, the lead bold): "II ja III ülesande hindamisel
#   arvestatakse järgmisi kriteeriume:" -- Parts II AND III. 1. "– 30%"
#   (96-97), 2. "– 30%" (98), 3. "–" / "30%" (99-100), 4. "– 10%" (101):
#   100 %.
# - Part II (102): a descriptive line, 103, "Umbes 100sõnaline ladus
#   kommentaar, tõestamaks teksti sisust arusaamist."; "Näiteks:" (104) over
#   eight italic items, 105-106, 107, 108, 109, 110, 111, 112, 113-114, and
#   "Jne" (115).
# - Part III (116): one descriptive line, 117-118. Nothing per title.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (103); the
#   eight items quoted under "Näiteks:" as examples, not a checklist (10a);
#   the criteria's lead quoted.
# - III1/III2: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (117-118); lead quoted.
# JUDGEMENT CALLS:
# - "Jne" (115) left out of the quoted examples (not an example).
# - Part III: the scheme's line says "Vähemalt 300sõnaline"; the paper asks
#   "umbes 300sõnaline" (10f: the paper's question, the scheme's head).
# - III1/III2 keep each title's printed attribution (italic, on the title's
#   own line).
# - II1's question is cut from the paper's lines (the census glues the head's
#   "(30 / 100)" in front).
# - Reading text: pp2-3 (rendered: Part I's head and the article on p2, the
#   rest with byline and author's note on p3; questions from p4). II1 quotes
#   the text: pages=(2, 3). The live cards' sourceMaterial.pages [2, 3] agree
#   with the render.
# GLYPHS: none in the lines used.

CRIT_2014 = crit((96, 97), 98, (99, 100), 101)
LEAD_2014 = quote(S(95), lead='The scheme prints')
ESSAY_2014 = 'Kirjuta umbes 300sõnaline'
SPECS[2014] = [
    R('II1', [graded(S(103), PARTP(), CRIT_2014)],
      rownote=both(examples(S(104), L(105, 106), S(107), S(108), S(109), S(110), S(111), S(112), L(113, 114)),
                   LEAD_2014),
      question=QP(4, Run('„Lugemise ja jutustamisega', 'inimese maailmataju'), 'Kirjuta umbes 100sõnaline'),
      pages=(2, 3)),
    R('III1', [graded(L(117, 118), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, ESSAY_2014, '1) „Lugeja')),
    R('III2', [graded(L(117, 118), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, ESSAY_2014, '2) „Isegi')),
]


# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Vasta küsimustele ülesannetes I, II ja
# III. Kõikidele küsimustele tuleb vastata eesti keeles." (p2 y78-92); "I.
# ÜLESANNE (30/100)" (p2 y124) and its instruction (y146) over the article,
# which runs pp2-3 (to the source note "(Martin Ehala, ajalehest Postimees,
# ... lühendatud.)" p3 y628-639); Q1 "(5 × 1)" opens p4 (y96); Q2-Q6 "(5)"
# each; "II. ÜLESANNE (30/100)" (p4 y506), a quotation and "Kommenteeri seda
# väidet umbes 100 sõnaga." (y538-565); "III. ÜLESANNE (40/100)" (p4 y629),
# "Kirjuta umbes 300sõnaline kirjand. Vali üks antud teemadest." (y661) over
# two NUMBERED titles, "1) Kas rahvuslik identiteet rikastab meie
# kultuurielu või muudab selle vaesemaks?" (y715) and "2) Rikkaim on see, kes
# on rahul vähesega. (Sokrates)" (y763).
# PRICES:
# - II1: the head's "(30/100)" (PARTP); scheme "II. ÜLESANNE kuni 30 punkti"
#   (127).
# - III1/III2: "(40/100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti"
#   (144).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 2-4; p2 the
# standard note to teachers):
# - Criteria (p4, 115-122, the lead bold): "II ja III ülesande hindamisel
#   arvestatakse järgmisi kriteeriume:" -- Parts II AND III. 1. "– 30%"
#   (116-117), 2. "– 30%" (118-119), 3. "– 30%" (120-121), 4. "– 10%" (122):
#   100 %.
# - Part II (p5, 127): a descriptive line, 128, "Umbes 100sõnaline ladus
#   kommentaar, tõestamaks teksti sisust arusaamist."; "Näiteks:" (129) over
#   five italic items, 130-133, 134-136, 137-138, 139-140, 141-142, and
#   "Jne" (143).
# - Part III (144): one descriptive line, 145-146; then both titles reprinted
#   as the paper prints them (147, 148), nothing under either.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (128); the
#   five items quoted under "Näiteks:" as examples, not a checklist (10a);
#   the criteria's lead quoted.
# - III1/III2: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (145-146); lead quoted.
# JUDGEMENT CALLS:
# - "Jne" (143) left out of the quoted examples (not an example).
# - Part III: the scheme's line says "Vähemalt 300sõnaline"; the paper asks
#   "umbes 300sõnaline" (10f: the paper's question, the scheme's head).
# - III2 keeps the title's printed attribution "(Sokrates)".
# - II1's question is cut from the paper's lines (the census glues the head's
#   "(30/100)" in front).
# - Reading text: pp2-3 (rendered). II1 quotes it: pages=(2, 3). The live
#   cards' sourceMaterial.pages [2, 3] agree with the render.
# GLYPHS: none in the lines used.

CRIT_2015 = crit((116, 117), (118, 119), (120, 121), 122)
LEAD_2015 = quote(S(115), lead='The scheme prints')
ESSAY_2015 = 'Kirjuta umbes 300sõnaline'
SPECS[2015] = [
    R('II1', [graded(S(128), PARTP(), CRIT_2015)],
      rownote=both(examples(S(129), L(130, 133), L(134, 136), L(137, 138), L(139, 140), L(141, 142)),
                   LEAD_2015),
      question=QP(4, Run('„Juba mõnekümne', 'sõnaga.')), pages=(2, 3)),
    R('III1', [graded(L(145, 146), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, ESSAY_2015, '1) Kas rahvuslik')),
    R('III2', [graded(L(145, 146), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, ESSAY_2015, '2) Rikkaim')),
]


# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Vasta küsimustele ülesannetes I, II ja
# III. Kõikidele küsimustele tuleb vastata eesti keeles." (p2 y78-92); "I.
# ÜLESANNE (30/100)" (p2 y131) over the article, which runs pp2-3 (to the
# editing note "Teksti on hindamise eesmärgil ... lühendatud." p3 y611); Q1
# "(5 × 1)" (p3 y647) over a)-e); Q2-Q6 "(5)" each (p4); "II. ÜLESANNE
# (30/100)" (p4 y409), a quotation and "Kommenteeri seda väidet 100–150
# sõnaga." (y428-456); "III. ÜLESANNE (40/100)" (p4 y551), "Kirjuta umbes
# 300sõnaline kirjand. Vali üks antud teemadest." (y571) over two NUMBERED
# titles, "1) Kes maksab, see tellib muusika?" (y603) and "2) „Maailm võib
# olla üsna ebameeldiv paik, ...”" (y630) with its source "Fintan O'Toole,
# The Irish Times, 22. veebruar 2016." set right under it (y657).
# PRICES:
# - II1: the head's "(30/100)" (PARTP); scheme "II. ÜLESANNE kuni 30 punkti"
#   (111).
# - III1/III2: "(40/100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti"
#   (127).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# standard note to teachers):
# - Criteria (p4, 103-110, the lead underlined): "II ja III ülesande
#   hindamisel arvestatakse järgmisi kriteeriume:" -- Parts II AND III. 1.
#   "– 30%" (104-105), 2. "– 30%" (106-107), 3. "– 30%" (108-109), 4. "–
#   10%" (110): 100 %.
# - Part II (111): a descriptive line, 112, "Umbes 100sõnaline ladus
#   kommentaar, tõestamaks teksti sisust arusaamist."; "Näiteks:" set at the
#   head of the first item's line (113, "Näiteks: Ränne, paremate võimaluste
#   otsimine lähemal ja kaugemal"), then items 114, and on p5 119-120, 121,
#   122-123, 124, 125, and "Jne" (126).
# - Part III (127): ONE line, 128, "Vähemalt 300sõnaline sidus teemakohane
#   kirjand läbimõeldud sisu, selge ülesehituse ning" -- the sentence stops
#   there (rendered p5: nothing follows; the other sittings go on "sorava
#   lausestusega."). Nothing per title.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (112); the
#   seven items quoted under "Näiteks:" (cut from line 113) as examples, not
#   a checklist (10a); the criteria's lead quoted.
# - III1/III2: graded (10b), 12/12/12/4 of 40. Head: line 128 as printed
#   (the SEC's unfinished sentence; flagged for the lead, 10f); lead quoted.
# JUDGEMENT CALLS:
# - "Jne" (126) left out of the quoted examples (not an example).
# - Part III head: line 128 is the scheme's own descriptive line, printed
#   unfinished. Lifted as printed rather than completed from another
#   sitting. If the lead prefers, quote it in the note instead and head the
#   row with the criteria's lead (S(103)).
# - The paper asks "100–150 sõnaga" (Part II) and "umbes 300sõnaline"
#   (Part III); the scheme's lines say "Umbes 100sõnaline" and "Vähemalt
#   300sõnaline": the paper's question, the scheme's head (10f).
# - III2 keeps the title's printed source line (y657).
# - II1's question is cut from the paper's lines (the census glues the head's
#   "(30/100)" in front).
# - Reading text: pp2-3 (rendered). II1 quotes it: pages=(2, 3). The live
#   cards' sourceMaterial.pages [2, 3] agree with the render.
# GLYPHS: none in the lines used.

CRIT_2016 = crit((104, 105), (106, 107), (108, 109), 110)
LEAD_2016 = quote(S(103), lead='The scheme prints')
ESSAY_2016 = 'Kirjuta umbes 300sõnaline'
def _BROKEN_2016(d):
    return 'The scheme\'s head line breaks off mid-sentence ("... ning"); it is shown as printed.'


SPECS[2016] = [
    R('II1', [graded(S(112), PARTP(), CRIT_2016)],
      rownote=both(examples(S(113, before=' Ränne'), S(113, after='Näiteks: '), S(114), L(119, 120), S(121),
                            L(122, 123), S(124), S(125)),
                   LEAD_2016),
      question=QP(4, Run('„Irooniliselt', 'ebakindluse eest'), 'Kommenteeri seda väidet'), pages=(2, 3)),
    R('III1', [graded(S(128), PARTP(), CRIT_2016)], rownote=both(LEAD_2016, _BROKEN_2016),
      question=QP(4, ESSAY_2016, '1) Kes maksab')),
    R('III2', [graded(S(128), PARTP(), CRIT_2016)], rownote=both(LEAD_2016, _BROKEN_2016),
      question=QP(4, ESSAY_2016, '2) „Maailm', 'Fintan O')),
]


# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# estonian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Vasta küsimustele ülesannetes I, II ja
# III. Kõikidele küsimustele tuleb vastata eesti keeles." (p2 y65); "I.
# ÜLESANNE (30/100)" (p2 y121) and its instruction (y142) over the article,
# which runs pp2-3 (to the byline "Tuul Sepp, Siim Sepp, ..." p3 y587 and the
# editing note y608); Q1 "(5 × 1)" (p3 y661) over a)-e); Q2-Q6 "(5)" each
# (p4); "II. ÜLESANNE (30/100)" (p4 y389), a quotation (y410-425) and
# "Kirjelda umbes 100-150 sõnaga seda suhkru kujundatud maailma. Tee vahet
# sõnadel „vajama“ ja „ihaldama“." (y445-460); "III. ÜLESANNE (40/100)" (p4
# y558), "Kirjuta umbes 300sõnaline kirjand. Vali üks antud teemadest."
# (y579) over two NUMBERED titles, "1) Me oleme see, mida sööme" (y611) and
# "2) „Minu arvamus on sama hea ...“ Arutle selle väite üle ... silmas
# pidades." (y695-724), "või" between them (y653).
# PRICES:
# - II1: the head's "(30/100)" (PARTP); scheme "II. ÜLESANNE kuni 30 punkti"
#   (116).
# - III1/III2: "(40/100)" (PARTP); scheme "III. ÜLESANNE kuni 40 punkti"
#   (128).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# standard note to teachers):
# - Criteria (p4, 108-115): "II ja III ülesande hindamisel arvestatakse
#   järgmisi kriteeriume:" -- Parts II AND III. 1. "– 30%" (109-110), 2. "–
#   30%" (111-112), 3. "– 30%" (113-114), 4. "Õigekiri: õigekeelsus ja
#   kirjavahemärgid – 10%" (115): 100 %.
# - Part II (116): a descriptive line, 117, "Umbes 100-150sõnaline ladus
#   kommentaar, et tõestada teksti sisust arusaamist."; "Näiteks:" set at the
#   head of the first item (118-119), then items 120-121 and 122, and on p5
#   "Jne." (127).
# - Part III (128): one descriptive line, 129-130, "Umbes 300sõnaline sidus
#   teemakohane kirjand ...". Nothing per title.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (117); the
#   three items quoted under "Näiteks:" (cut from line 118) as examples, not
#   a checklist (10a); the criteria's lead quoted.
# - III1/III2: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (129-130); lead quoted.
# JUDGEMENT CALLS:
# - "Jne." (127) left out of the quoted examples (not an example).
# - II1's question: the quotation, then the task (two runs of the paper's
#   lines); the census glues the head's "(30/100)" in front.
# - III2's title runs over three printed lines and carries its own task
#   ("Arutle selle väite üle ..."): all of it is the title, cut from the
#   paper's lines.
# - Reading text: pp2-3 (rendered). II1 quotes it: pages=(2, 3). The live
#   cards' sourceMaterial.pages [2, 3] agree with the render.
# GLYPHS: none in the lines used.

CRIT_2017 = crit((109, 110), (111, 112), (113, 114), 115)
LEAD_2017 = quote(S(108), lead='The scheme prints')
ESSAY_2017 = 'Kirjuta umbes 300sõnaline'
SPECS[2017] = [
    R('II1', [graded(S(117), PARTP(), CRIT_2017)],
      rownote=both(examples(S(118, before=' Magusatarbimise'), L(118, 119, after='Näiteks: '), L(120, 121), S(122)),
                   LEAD_2017),
      question=QP(4, Run('„See toitaine', 'maailma.'), Run('Kirjelda umbes', '„vajama“')), pages=(2, 3)),
    R('III1', [graded(L(129, 130), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, ESSAY_2017, '1) Me oleme')),
    R('III2', [graded(L(129, 130), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, ESSAY_2017, Run('2) „Minu arvamus', 'silmas pidades.'))),
]


# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the five open asks of this sitting,
# I5, I6, II1, III1, III2. Live: I1 (whole), I2, I3, I4 (4 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all four carry the wrong
# row).
# Paper (rendered pp2-4): the rule "Vasta küsimustele I, II ja III ülesandes.
# Kõikidele küsimustele tuleb vastata eesti keeles." (p2 y65); "I ÜLESANNE
# (30/100)" (p2 y100) and "... Iga õige vastus annab 5 punkti." (y121-136);
# the article "POLARISEERUMINE JA VALEUUDISED" runs pp2-3 (title p2 y156,
# paragraphs 1-11 to the byline "Maari Põim, ajalehest Postimees, ..." p3 y730
# and the editing note y748); p4 holds only questions: Q1 "(5 × 1)" (p4 y65)
# over 1)-5); Q2-Q6 "(5)" each, set at the right under or beside the
# question's last line (rendered p4); "II ÜLESANNE (30/100)" (p4 y510); "III
# ÜLESANNE (40/100)" (p4 y619), "Kirjuta umbes 300sõnaline kirjand. Vali üks
# antud teemadest." (bold, y640) over two NUMBERED titles "1) Igaühel on oma
# tõde, ..." (y673) and "2) „Riided teevad inimese“. ..." (y693).
# PRICES:
# - I5, I6: "(5)" each (census tariff (1, 5, 5): PP()); the scheme prints the
#   same "(5)" at the end of each reprint (lines 90, 111).
# - II1: the head's "(30/100)" (PARTP); scheme "II ÜLESANNE kuni 30 punkti"
#   (135).
# - III1, III2: "(40/100)" (PARTP); scheme "III ÜLESANNE kuni 40 punkti" (147).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; answers
# in italics):
# - Q5 (86-90 reprint the question with "(5)"): ONE italic paragraph, 91-106,
#   "Pidev infovoog on muutnud ... ei tähenda tingimata objektiivsust."
# - Q6 (107-111 reprint the question with "(5)"): THREE italic paragraphs
#   with a gap between each (rendered p4): 112-116 ("Teise poole arvamuse ...
#   kes kõvemini karjub."), 117-119 ("Kriitikat on üldiselt ... lahenduseni."),
#   120-122 ("Nii ühiskondliku kui ... faktipõhise väitlusega."). No split.
# - Criteria (p5 top, 127-134): "II ja III ülesande hindamisel arvestatakse
#   järgmisi kriteeriume:" (bold) -- for Parts II AND III. 1. "– 30%" (128-
#   129), 2. "– 30%" (130-131), 3. "– 30%" (132-133), 4. "– 10%" (134): all
#   four printed, 100 %.
# - Part II (135): the task reprinted (136-138), then "Näiteks:" (139, italic)
#   over six italic items, one per line (140-145), and "Jne." (146). No
#   descriptive line of its own this sitting.
# - Part III (147): one descriptive line, 148-149, "Umbes 300sõnaline sidus
#   teemakohane kirjand läbimõeldud sisu, selge ülesehituse ning sorava
#   lausestusega." Nothing per title.
# SHAPES:
# - I5: one printed paragraph = one row at the paper's 5 (one(), PP()), as
#   Bulgarian 2015 I5 and Danish 2018 I4/I5.
# - I6: three printed paragraphs and no split: three shown rows, priced as a
#   whole on the paper's 5 (questionTotal, 10a), as Romanian 2020 I3/I5.
# - II1: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3. With no descriptive line
#   for Part II, the head is the criteria's own lead (127), as Czech 2013/2014
#   and Romanian 2016/2017/2020 head a Part II that has none; the six items
#   quoted under the scheme's own "Näiteks:" as examples, not a checklist
#   (10a).
# - III1, III2: graded (10b), 12/12/12/4 of 40. Head: the descriptive line
#   (148-149); the criteria's lead quoted (it names Parts II and III).
# JUDGEMENT CALLS:
# - I6 shown, not one(): three separate paragraphs (rendered) are three
#   points of a model answer the scheme prices only as a whole. If the lead
#   prefers one claimable row (as the live 2019/2021 I6 cards): one(L(112,
#   122), PP()).
# - Part II's "Jne." (146, "etc.") is left out of the quoted examples, as in
#   helper A's 2010: not an example.
# - The scheme reprints Part II's task without the paper's "umbes" ("...
#   Kommenteeri oma seisukohta 100–150 sõnaga.", line 137-138; paper p4 y545
#   "... Kommenteeri oma seisukohta umbes 100–150 sõnaga."): a reprint, not
#   an answer; the paper wins on the question (10f) and the difference is a
#   single word, quoted on II1's row.
# - The scheme reprints Q6 with "peaks" moved ("kuidas kriitikat taluv ja
#   kaasvestleja arvamust austav suhtumine peaks aitama", 110-111; paper p4
#   y421 "kuidas peaks kriitikat taluv ... suhtumine aitama"): word order
#   only, the paper's words carded; quoted in the note (10f).
# - III1/III2 questions: the bold instruction, then the title, cut from the
#   paper's lines (the census gives the bare title).
# - Reading text pp2-3 (rendered: title p2 y156, the text to the byline and
#   editing note at the foot of p3; p4 opens with Q1). I5, I6, II1 carry
#   pages=(2, 3). The live 2018 cards' sourceMaterial.pages [2, 3] agree with
#   the render.
# GLYPHS: none. õ ä ö ü read cleanly in every line used (paper and scheme;
# "Õigekiri", "kõvemini", "väitlusega", "Küberkuritegevus" checked on the
# render); no š/ž in the lines used.

CRIT_2018 = crit((128, 129), (130, 131), (132, 133), 134)
LEAD_2018 = quote(S(127), lead='The scheme prints')
ESSAY_2018 = 'Kirjuta umbes 300sõnaline'


def _q6_reprint_2018(d):
    return (f'The scheme reprints the question’s last words as “{L(110, 111, after="kuidas ", before=" (5)").text(d)}” '
            f'(the paper: “{J(PC(4, "artikli põhjal, kuidas peaks", after="kuidas "), PL(4, "ehtsatel uudistel")).text(d)}”).')


def _p2_reprint_2018(d):
    return (f'The scheme reprints the task’s last words as “{L(137, 138, after="küsimuses? ").text(d)}” '
            f'(the paper: “{J(PC(4, "tähelepanu?“ Milline", after="küsimuses? "), PL(4, "100–150 sõnaga")).text(d)}”).')


SPECS[2018] = [
    R('I5', [one(L(91, 106), PP())], pages=(2, 3)),
    R('I6', [shown(L(112, 116)), shown(L(117, 119)), shown(L(120, 122))], whole=True,
      rownote=_q6_reprint_2018, pages=(2, 3)),
    R('II1', [graded(S(127), PARTP(), CRIT_2018)],
      rownote=both(examples(S(139), *[S(n) for n in range(140, 146)]), _p2_reprint_2018),
      pages=(2, 3)),
    R('III1', [graded(L(148, 149), PARTP(), CRIT_2018)], rownote=LEAD_2018,
      question=QP(4, ESSAY_2018, '1) Igaühel')),
    R('III2', [graded(L(148, 149), PARTP(), CRIT_2018)], rownote=LEAD_2018,
      question=QP(4, ESSAY_2018, '2) „Riided')),
]


# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I5, II1, III1, III2. Live: I1 (whole), I2, I3, I4, I6 (5 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all five carry a wrong or
# run-on row).
# Paper (rendered pp2-4): "I ÜLESANNE (30/100)" (p2 y65); the rule "Vasta
# küsimustele I, II ja III ülesandes. Kõikidele küsimustele tuleb vastata
# eesti keeles. ..." (p2 y86); the article "KASINUSE DISKREETNE VÕLU" runs
# pp2-3 (title p2 y177, paragraphs 1-7 to the byline "Mari Laaniste, ..." p3
# y594 and the editing note y613); Q1 "(5 × 1)" (p3 y653) over 1)-5) at the
# foot of p3; Q2-Q6 "(5)" each at the right of the question's last line (p4);
# "II ÜLESANNE (30/100)" (p4 y383); "III ÜLESANNE (40/100)" (p4 y543), "Kirjuta
# umbes 300sõnaline kirjand. Vali üks antud teemadest." (bold) over two
# NUMBERED titles "1) Saastatud keskkond ..." (y583) and "2) Vaheaasta ..."
# (y617, its second line "Esita oma seisukoht ... Kaalu mõlema poole
# argumente." set under it, one text-layer line).
# PRICES:
# - I5: "(5)" (p4 y233; census tariff (1, 5, 5): PP()); scheme "(5)" at the
#   end of its reprint (76).
# - II1: "(30/100)" (PARTP); scheme "II ÜLESANNE kuni 30 punkti" (105).
# - III1, III2: "(40/100)" (PARTP); scheme "III ÜLESANNE kuni 40 punkti" (115).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2):
# - Q5 (75-76 reprint the question with "(5)"): FOUR italic points, each
#   opening with "*" and on a line of its own (77, 78, 79, 80), then "Jne."
#   (81). No split.
# - Criteria (p4, 97-104): "II ja III ülesande hindamisel arvestatakse
#   järgmisi kriteeriume:" (bold) -- Parts II AND III; 30 % (98-99), 30 %
#   (100-101), 30 % (102-103), 10 % (104).
# - Part II (105): the descriptive line "Umbes 100–150sõnaline ladus
#   kommentaar, et tõestada teksti sisust arusaamist." (106), "Näiteks:" (107,
#   italic) over three italic items (108-110, 111-112, 113) and "Jne." (114).
# - Part III (115): one descriptive line, 116-117, "Umbes 300sõnaline sidus
#   teemakohane kirjand ...". Nothing per title.
# SHAPES:
# - I5: the four points shown, priced as a whole on the paper's 5
#   (questionTotal, 10a); the scheme's closing "Jne." quoted in the note (it
#   says the list is open).
# - II1: graded (10b), 9/9/9/3 of 30; head the descriptive line (106); the
#   items quoted under "Näiteks:" as examples, not a checklist (10a); the
#   criteria's lead quoted.
# - III1, III2: graded (10b), 12/12/12/4 of 40; head the descriptive line
#   (116-117); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I5's rows are cut after the printed "*" (the bullet strip does not take
#   it), as Maltese 2024 I4.
# - Part II's "Jne." (114) left out of the quoted examples, as 2010/2018.
# - III2's question is the instruction, then title 2 with the task line the
#   paper sets under it ("Esita oma seisukoht umbes 300sõnalises kirjandis.
#   Kaalu mõlema poole argumente."): one text-layer line, lifted whole.
# - Reading text pp2-3 (rendered: title p2 y177, the text to the byline and
#   editing note on p3 y594-613; Q1 at the foot of p3, Q2-Q6 on p4). I5 and
#   II1 carry pages=(2, 3). The live 2019 cards' sourceMaterial.pages [2, 3]
#   agree with the render.
# GLYPHS: none. õ ä ö ü clean in every line used ("Ökoloogiline",
# "Üksikisiku", "säästlikuma" checked on the render); no š/ž in the lines used.

CRIT_2019 = crit((98, 99), (100, 101), (102, 103), 104)
LEAD_2019 = quote(S(97), lead='The scheme prints')
ESSAY_2019 = 'Kirjuta umbes 300sõnaline'

SPECS[2019] = [
    R('I5', [shown(S(77, after='*')), shown(S(78, after='*')), shown(S(79, after='*')), shown(S(80, after='*'))],
      whole=True, rownote=quote(S(81), lead='The scheme closes the list with'), pages=(2, 3)),
    R('II1', [graded(S(106), PARTP(), CRIT_2019)],
      rownote=both(examples(S(107), L(108, 110), L(111, 112), S(113)), LEAD_2019),
      pages=(2, 3)),
    R('III1', [graded(L(116, 117), PARTP(), CRIT_2019)], rownote=LEAD_2019,
      question=QP(4, ESSAY_2019, '1) Saastatud')),
    R('III2', [graded(L(116, 117), PARTP(), CRIT_2019)], rownote=LEAD_2019,
      question=QP(4, ESSAY_2019, '2) Vaheaasta')),
]


# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# I5, II1, II2. Live: I1 (whole), I2, I3, I4, I6 (5 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all five carry a wrong or
# run-on row).
# A TWO-PART sitting: "Vasta I ja II ülesandele." / "Ülesannetele tuleb vastata
# eesti keeles." / "Kokku 70 punkti" (p2 y65-106); "I ÜLESANNE (30/70)" (p2
# y139); "II ÜLESANNE (40/70)" (p4 y601) is the essay, keys II1/II2 its two
# titles (ruling B; a two-part sitting's Part II is the essay).
# Paper (rendered pp2-4): the article runs pp2-4 (paragraphs 1-10, the text
# ending p4 y159, byline "Kristjan Otsmann, ajalehest Müürileht, ..." p4 y178,
# editing note y190); Q1 "(5 × 1)" (p4 y228) over 1)-5); Q2-Q6 "(5)" each at
# the right of the question's last line (p4); Part II: "Kirjuta kirjand
# (vähemalt 300 sõna). Vali üks antud teemadest." (y631) over "1) Tuleviku
# töömaailm ning seal vajaminevad oskused ja omadused." (y667), "Või" (y693,
# centred), "2) „Me ei saa välja mõelda omaenda fakte ... kuuleme.“" (y722)
# and "- Greta Thunberg" (y739, right).
# PRICES:
# - I5: "(5)" (p4 y457; census tariff (1, 5, 5): PP()); scheme "(5)" (82).
# - II1, II2: "(40/70)" (PARTP); scheme "II ÜLESANNE kuni 40 punkti" (136).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q5 (81-82 reprint the question with "(5)"): THREE italic paragraphs with a
#   gap between each (rendered p4): 83-92 ("Lühem töönädal eeldab ...
#   mittemateriaalseid hüvesid ja inimsuhteid."), 93-95 ("Artiklis mainitakse
#   Eesti puhul ka madalamat tootlikkust, ... töövahendeid."), 96-98 ("Lõpuks
#   tuleb arvestada ... kasulikult käima saada."). Key words UNDERLINED in each
#   ("inimväärne elatustase", "viisakas sissetulek", "madalamat tootlikkust",
#   "töökultuur ja tööharjumused"); no marks beside them, no split.
# - Criteria (p5, 128-135): "II ülesande hindamisel arvestatakse järgmisi
#   kriteeriume:" (underlined) -- for Part II, the essay -- then four criteria
#   WITH NO PERCENTAGES (rendered p5: 129-130 end "mõtteid esitama", 131-132
#   "eesmärgipärane", 133-134 "väljendamiseks", 135 "kirjavahemärgid"; the
#   2018-2019 "– 30%" / "– 10%" are gone).
# - Part II (136): one descriptive line, 137-138, "Vähemalt 300 sõnaline sidus
#   teemakohane kirjand läbimõeldud sisu, selge ülesehituse ning sorava
#   lausestusega.", then the two titles reprinted (139-142). Nothing per title.
# SHAPES:
# - I5: the three paragraphs shown, priced as a whole on the paper's 5
#   (questionTotal, 10a): three printed points of a model answer.
# - II1, II2: criteria printed for this part WITHOUT percentages: the four
#   criteria as shown rows on the paper's 40 (questionTotal; coordinator
#   ruling F, Bulgarian 2021); the descriptive line and the criteria's lead
#   quoted.
# JUDGEMENT CALLS:
# - I5 shown, not one(): three separate paragraphs (rendered). If the lead
#   prefers one claimable row: one(L(83, 98), PP()). The underlining is not
#   carried (a row is plain text); no mark hangs on it.
# - The criteria rows keep their printed numbers "1." to "4." (as the graded
#   parts of 2018/2019 do); line 135 is set at the margin, not indented like
#   1.-3. (rendered p5): layout only.
# - II1's question: the instruction, then title 1; the census glues the
#   centred "Või" (y693) to title 1 (JOINER takes it off). II2: the
#   instruction, title 2 and its attribution line "- Greta Thunberg" (printed
#   under the title at the right), as printed.
# - Reading text pp2-4 (rendered: the article from p2 to the editing note at
#   p4 y190; Q1 opens p4 y228). I5 carries pages=(2, 3, 4). The live 2021
#   cards' sourceMaterial.pages [2, 3, 4] agree with the render.
# - No `pages` on Part II (the essay of a two-part sitting).
# GLYPHS: none. õ ä ö ü clean in the lines used ("Õigekiri", "töönädal",
# "lüüasaamine"); the scheme types U+2010 HYPHEN in "40‐tunnise", "kaela‐" and
# "‐ Greta Thunberg" (lines 59, 65, 142): real hyphens, rendered as such, not
# in any row here.

CRIT_ROWS_2021 = (L(129, 130), L(131, 132), L(133, 134), S(135))
ESSAY_2021 = 'Kirjuta kirjand (vähemalt 300 sõna)'


def _crit_note_2021(d):
    return (f'Under Part II the scheme prints “{L(137, 138).text(d)}” Under “{S(128).text(d)}” it prints the '
            f'four criteria with no marks or percentages beside them, so they are shown and the part is scored '
            f'on its printed total.')


SPECS[2021] = [
    R('I5', [shown(L(83, 92)), shown(L(93, 95)), shown(L(96, 98))], whole=True, pages=(2, 3, 4)),
    R('II1', [shown(c) for c in CRIT_ROWS_2021], whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, '1) Tuleviku')),
    R('II2', [shown(c) for c in CRIT_ROWS_2021], whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, '2) „Me ei saa', '- Greta Thunberg')),
]


# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I5, I6, II1, II2. Live: I1 (whole), I2, I3, I4 (4 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all four carry the wrong
# row).
# A TWO-PART sitting: "Vasta I ja II ülesandele." / "Ülesannetele tuleb vastata
# eesti keeles. Kokku on võimalik saada kuni 70 punkti." (p2 y65-86); "I
# ÜLESANNE (30 punkti)" (p2 y118); "II ÜLESANNE (40 punkti)" (p4 y419) is the
# essay, keys II1/II2 its two titles (ruling B).
# Paper (rendered pp2-4): the article "KÕIK EI OLE ISAAC NEWTONID" runs pp2-3
# (title p2 y207, the text to the byline "Ilmar Tomusk, ajalehest Postimees,
# 30.11.2021" p3 y592 and the editing note y610); Q1 "(5 × 1)" (p3 y650) at
# the foot of p3; Q2-Q6 "(5)" each (p4; Q6's "(5)" at the end of its own last
# line, y324, which the census reads); Part II: "Kirjuta kirjand (vähemalt 300
# sõna), vali üks antud teemadest." (bold, y440) over "1) Tänapäeva Isaac
# Newtonite ees seisvad suurimad väljakutsed" with "Uued ajad, uued
# kangelased" set under it in the same item (y480, one text-layer line) and
# "2) Kuidas tekib tõeline sõprus?" (y553).
# PRICES:
# - I5, I6: "(5)" each (census tariff (1, 5, 5): PP()); scheme "(5)" (86, 99).
# - II1, II2: "(40 punkti)" (PARTP); scheme "II ÜLESANNE kuni 40 punkti" (126).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q5 (83-86 reprint the question, "(5)" on a line of its own): ONE italic
#   paragraph, 87-95, "Autori arvates on inimesed loodud ... väga oluline."
# - Q6 ("6." alone on line 96, the question reprinted 97-99 with "(5)"):
#   "Näiteks:" (100, italic) over TWO italic paragraphs with a gap between
#   them (rendered p4): 101-107, how technology CONNECTS ("digipädevus on
#   tänapäeva kooli elementaarne osa – ... õpetajate vahel, jne."), and
#   108-113, how it DIVIDES ("Digivahendite ületarbimine ... koolikius, jne.").
#   No split.
# - Criteria (p5, 118-125): "II ülesande hindamisel arvestatakse järgmisi
#   kriteeriume:" -- for Part II, the essay -- four criteria WITH NO
#   PERCENTAGES (rendered p5).
# - Part II (126): the instruction and both titles reprinted (127-130), then
#   the descriptive line "Vähemalt 300 sõna pikkune sidus teemakohane kirjand
#   läbimõeldud sisu, selge ülesehituse ning sorava lausestusega." (131-132).
# SHAPES:
# - I5: one printed paragraph = one row at the paper's 5 (one(), PP()).
# - I6: the two example paragraphs shown under the scheme's own "Näiteks:",
#   priced as a whole on the paper's 5 (questionTotal, 10a); the heading
#   quoted.
# - II1, II2: criteria printed for this part WITHOUT percentages: the four
#   criteria as shown rows on the paper's 40 (questionTotal; ruling F); the
#   descriptive line and the criteria's lead quoted.
# JUDGEMENT CALLS:
# - 10f, Q5: the scheme reprints the task as "Selgita, mispärast on autor
#   mures ... Kas see mure on sinu arvates õigustatud?" with no "Põhjenda oma
#   seisukohta." (84-85); the paper prints "Selgita, miks on autor mures ...
#   õigustatud? Põhjenda oma seisukohta." (p4 y210-254): the paper's words
#   carded, the scheme's quoted on the row.
# - 10f, Q6: the scheme reprints "Arutle loetule ja omaenda kogemusele" (98)
#   for the paper's "Arutle loetule ja oma kogemusele" (p4 y295): quoted.
# - I6's second paragraph: line 110 opens with the printed dash ("tervisele" /
#   "– keskendumisraskused ..."), which the bullet strip would drop: SR(110)
#   keeps it (Romanian 2015, Danish 2018 d)).
# - I6's two paragraphs answer the two sides the question offers ("pigem
#   ühendab või lahutab"); both shown, neither claimable alone.
# - II1's question keeps the subtitle line "Uued ajad, uued kangelased" the
#   paper prints under title 1 inside the same numbered item (rendered p4;
#   the scheme reprints both lines, 128-129); not a third title.
# - Reading text pp2-3 (rendered: title p2 y207 to the byline and editing note
#   on p3; Q1 at the foot of p3, Q2-Q6 on p4). I5 and I6 carry pages=(2, 3).
#   The live 2022 cards' sourceMaterial.pages [2, 3] agree with the render.
# - No `pages` on Part II (the essay of a two-part sitting).
# GLYPHS: none. õ ä ö ü clean in the lines used ("Õigekiri", "võõrandumine",
# "üleelamisi"); the scheme types U+2010 HYPHEN in "silmast‐silma" (87), a
# real hyphen (rendered "silmast-silma"), kept inside I5's row as printed.

CRIT_ROWS_2022 = (L(119, 120), L(121, 122), L(123, 124), S(125))
ESSAY_2022 = 'Kirjuta kirjand (vähemalt 300 sõna)'


def _crit_note_2022(d):
    return (f'Under Part II the scheme prints “{L(131, 132).text(d)}” Under “{S(118).text(d)}” it prints the '
            f'four criteria with no marks or percentages beside them, so they are shown and the part is scored '
            f'on its printed total.')


SPECS[2022] = [
    R('I5', [one(L(87, 95), PP())],
      rownote=quote(L(84, 85, after='avaldab.“ '), lead='The scheme reprints the task as'), pages=(2, 3)),
    R('I6', [shown(L(101, 107)), shown(J(L(108, 109), SR(110), L(111, 113)))], whole=True,
      rownote=both(quote(S(100), lead='The scheme heads them'),
                   quote(S(98, after='lahuta.“ ', before=', kas'), lead='It reprints the task as')),
      pages=(2, 3)),
    R('II1', [shown(c) for c in CRIT_ROWS_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, '1) Tänapäeva')),
    R('II2', [shown(c) for c in CRIT_ROWS_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, '2) Kuidas tekib')),
]


# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I5, II1, III1, III2. Live: I1 (whole), I2, I3, I4, I6 (5 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all five carry a wrong or
# run-on row).
# Paper (rendered pp2-4): "Vasta I, II ja III ülesandele." / "Ülesannetele
# tuleb vastata eesti keeles. Kokku on võimalik saada kuni 100 punkti." (p2
# y65-86); "I ÜLESANNE (30/100)" (p2 y118); the article "LOODUS EI ARVUSTA
# SIND" runs pp2-3 (title p2 y207, paragraphs 1-9 to the byline "Tuul Sepp,
# ajalehest Postimees, 7.11.2022" p3 y743 and the editing note y762); p4 holds
# only questions: Q1 "(5 × 1)" (y65), Q2-Q6 "(5)" each at the right of the
# question's last line; "II ÜLESANNE (30/100)" (y536); "III ÜLESANNE
# (40/100)" (y684), "Kirjuta umbes 300sõnaline kirjand. Vali üks antud
# teemadest." over "1. Ruum me ümber kujundab me mõtteviisi." (y733) and "2.
# „Ajad on teised, inimesed endised.” (Anton Hansen Tammsaare)" (y762).
# PRICES:
# - I5: "(5)" (p4 y409; census tariff (1, 5, 5): PP()); scheme "(5)" (90).
# - II1: "(30/100)" (PARTP); scheme "II ÜLESANNE kuni 30 punkti" (136).
# - III1, III2: "(40/100)" (PARTP); scheme "III ÜLESANNE kuni 40 punkti" (149).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q5 (87-90 reprint the question with "(5)"): ONE italic paragraph, 91-103,
#   "Loodus õpetab meid oma elu juhtima ... koostöö tähtsus."
# - Criteria (p5, 128-135): "II ja III ülesande hindamisel arvestatakse
#   järgmisi kriteeriume:" (bold) -- Parts II AND III; 30 % (129-130), 30 %
#   (131-132), 30 % (133-134), 10 % (135).
# - Part II (136): the task reprinted (137-140), "Näiteks:" (141) over three
#   italic items (142; 143-145; 146-147) and "Jne." (148). No descriptive
#   line of its own this sitting.
# - Part III (149): the descriptive line "Umbes 300sõnaline sidus teemakohane
#   kirjand ..." (150-151), then both titles reprinted (152-153).
# SHAPES:
# - I5: one printed paragraph = one row at the paper's 5 (one(), PP()).
# - II1: graded (10b), 9/9/9/3 of 30; with no descriptive line for Part II,
#   the head is the criteria's own lead (128), as 2018; the items quoted
#   under "Näiteks:" as examples, not a checklist (10a).
# - III1, III2: graded (10b), 12/12/12/4 of 40; head the descriptive line
#   (150-151); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - 10f, Q5: the scheme reprints "Arutle teksti põhjal" (88) for the paper's
#   "Arutle artikli põhjal" (p4 y365): the paper's words carded, the
#   scheme's quoted on the row.
# - Part II's third item breaks a hyphenated compound at the line end
#   ("vaatlemine‐uurimine‐" / "analüüs", 146-147, U+2010; rendered p5):
#   joined with no space (Join sep='', as Romanian 2020 I4), so the quoted
#   example reads the printed word "vaatlemine‐uurimine‐analüüs".
# - The scheme reprints Part II's quotation with THREE opening marks
#   ("„„„Loodus ei arvusta sind“", 137; rendered p5 the same) where the paper
#   prints two (p4 y557): a reprint, not used; the paper's text is the
#   question.
# - "Jne." (148) left out of the quoted examples, as 2018/2019.
# - III1/III2 questions: the instruction, then the title, cut from the
#   paper's lines (the census gives the bare title). Title 2 keeps the
#   paper's ” closing mark and its attribution "(Anton Hansen Tammsaare)".
# - Reading text pp2-3 (rendered: title p2 y207, the text to the byline and
#   editing note at the foot of p3; p4 opens with Q1). I5 and II1 carry
#   pages=(2, 3). The live 2023 cards' sourceMaterial.pages [2, 3] agree with
#   the render.
# GLYPHS: none. õ ä ö ü clean in the lines used ("Õigekiri", "Ükskõik",
# "tööprotsessis", "külvamine"); the scheme's U+2010 HYPHEN in
# "külvamine‐kasvatamine‐hooldamine‐hoolitsemine" (94, inside I5's row) and
# "vaatlemine‐uurimine‐" (146) are real hyphens (rendered as such).

CRIT_2023 = crit((129, 130), (131, 132), (133, 134), 135)
LEAD_2023 = quote(S(128), lead='The scheme prints')
ESSAY_2023 = 'Kirjuta umbes 300sõnaline'

SPECS[2023] = [
    R('I5', [one(L(91, 103), PP())],
      rownote=quote(S(88, after='võtmesõnad.“ ', before=','), lead='The scheme reprints the task’s opening as'),
      pages=(2, 3)),
    R('II1', [graded(S(128), PARTP(), CRIT_2023)],
      rownote=examples(S(141), S(142), L(143, 145), Join(S(146), S(147), sep='')),
      pages=(2, 3)),
    R('III1', [graded(L(150, 151), PARTP(), CRIT_2023)], rownote=LEAD_2023,
      question=QP(4, ESSAY_2023, '1. Ruum')),
    R('III2', [graded(L(150, 151), PARTP(), CRIT_2023)], rownote=LEAD_2023,
      question=QP(4, ESSAY_2023, '2. „Ajad')),
]


# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the nine open asks of this sitting,
# I1a-e, I5, II1, III1, III2. Live: I2, I3, I4, I6 (4 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all four carry a wrong or
# run-on row).
# Paper (rendered pp2-4): "Vasta I, II ja III ülesandele." / "Kõikidele
# ülesannetele tuleb vastata eesti keeles. Kokku on võimalik saada kuni 100
# punkti." (p2 y65-86); "I ÜLESANNE (30 punkti)" (p2 y118); the article
# "TEHISARU KASUTAMINE NÕUAB ARU" runs pp2-3 (title p2 y186, the text to the
# editing note p3 y616); p4 holds only questions: Q1's stem over two lines,
# "(5 × 1)" at the right of its second line (y86), over five LETTERED
# expressions a) digiriik, b) nutikas, c) äge, d) pärssima, e) maailmaga
# suhestuma (y106-189, italic); Q2-Q6 "(5)" each; "II ÜLESANNE (30/100)"
# (y575); "III ÜLESANNE (40/100)" (y696), "Kirjuta umbes 300sõnaline kirjand.
# Vali üks antud teemadest." (bold) over "1. Tehnoloogia areng – nagu kahe
# teraga mõõk" (y740) and "2. „Eesti suurim turvalisusrisk on harimatus.“
# (Jaak Jõerüüt)" (y766).
# PRICES:
# - I1a-e: "(5 × 1)": five expressions at 1 each, adding to Q1's 5; the
#   census walks the head down to the letters (tariff (1, 1, 1) each: PP()).
#   Per letter, as the brief rules for printed per-expression marks.
# - I5: "(5)" (p4 y427; PP()); scheme "(5)" (88).
# - II1: "(30/100)" (PARTP); scheme "II ÜLESANNE kuni 30 punkti" (123).
# - III1, III2: "(40/100)" (PARTP); scheme "III ÜLESANNE kuni 40 punkti" (134).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1 (50-51 reprint the stem with "(5 × 1)"): the five expressions NUMBERED
#   "1)" to "5)" where the paper LETTERS them a)-e), each reprinted with its
#   gloss after " – " (52-53, 54, 55, 56, 57). Paired by WORDS and order:
#   1) digiriik = a), 2) nutikas = b), 3) äge = c), 4) pärssima = d), 5)
#   maailmaga suhestuma = e). (The exclusions' "the scheme prices no ask that
#   pairs with it" is the letter/number mismatch, not a missing answer.)
# - Q5 (85-88 reprint the question with "(5)"): TWO italic paragraphs with a
#   gap between them (rendered p4): 89-91 ("Valikute tegemise oskus on
#   kõigepealt oluline ... suunanäitajana.") and 92-99 ("Valikute tegemise
#   oskus aitab meil ... töömeetodeid."). No split.
# - Criteria (p5, 115-122): "II ja III ülesande hindamisel arvestatakse
#   järgmisi kriteeriume:" -- Parts II AND III; 30/30/30/10 % (117, 119, 121,
#   122).
# - Part II (123): the task reprinted (124-127), "Näiteks:" (128) over ONE
#   italic run of topics, 129-132 ("digivahendid ja tehnoloogia, ... kodu,
#   kooli ja riigi roll;"), and "jne." (133). No descriptive line.
# - Part III (134): the descriptive line "Umbes 300sõnaline sidus
#   teemakohane kirjand ..." (135-136), then both titles reprinted (137-138).
# SHAPES:
# - I1a-e: one stated gloss each = one row at the paper's 1 (PP()), the
#   expression cut off (after " – ").
# - I5: the two paragraphs shown, priced as a whole on the paper's 5
#   (questionTotal, 10a).
# - II1: graded (10b), 9/9/9/3 of 30; with no descriptive line for Part II,
#   the head is the criteria's own lead (115), as 2018/2023; the topic run
#   quoted under "Näiteks:" as examples, not a checklist (10a).
# - III1, III2: graded (10b), 12/12/12/4 of 40; head the descriptive line
#   (135-136); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - 10f, Q1: the scheme reprints the stem as "Selgita järgmiste sõnade ja
#   väljendite tähendust, nii nagu need esinevad teksti kontekstis:" (50),
#   without the paper's "Sõnad ja väljendid on esitatud paksus kirjas." (p4
#   y86): the paper's words carded (the census text: stem and expression),
#   the scheme's line quoted on each Q1 row.
# - I1a's gloss is one entry with two phrasings joined by the scheme's ";"
#   ("riik, mis kasutab ...; riik, mida iseloomustab ..."): one row, as
#   printed (one gloss line wrapped onto 53).
# - Part II's topic run ends with the scheme's own ";" (132): kept as
#   printed inside the quote; "jne." (133) left out.
# - Reading text pp2-3 (rendered: title p2 y186 to the editing note p3 y616;
#   p4 opens with Q1). I1a-e, I5 and II1 carry pages=(2, 3). The live 2024
#   cards' sourceMaterial.pages [2, 3] agree with the render.
# GLYPHS: none. õ ä ö ü clean in the lines used ("äge", "pärssima",
# "Õigekiri", "töömeetodeid"); no š/ž in the lines used.

CRIT_2024 = crit((116, 117), (118, 119), (120, 121), 122)
LEAD_2024 = quote(S(115), lead='The scheme prints')
ESSAY_2024 = 'Kirjuta umbes 300sõnaline'
Q1HEAD_2024 = quote(S(50, after='1. '), lead='The scheme reprints the question as')

SPECS[2024] = [
    R('I1a', [one(L(52, 53, after='– '), PP())], rownote=Q1HEAD_2024, pages=(2, 3)),
    R('I1b', [one(S(54, after='– '), PP())], rownote=Q1HEAD_2024, pages=(2, 3)),
    R('I1c', [one(S(55, after='– '), PP())], rownote=Q1HEAD_2024, pages=(2, 3)),
    R('I1d', [one(S(56, after='– '), PP())], rownote=Q1HEAD_2024, pages=(2, 3)),
    R('I1e', [one(S(57, after='– '), PP())], rownote=Q1HEAD_2024, pages=(2, 3)),
    R('I5', [shown(L(89, 91)), shown(L(92, 99))], whole=True, pages=(2, 3)),
    R('II1', [graded(S(115), PARTP(), CRIT_2024)],
      rownote=examples(S(128), L(129, 132)),
      pages=(2, 3)),
    R('III1', [graded(L(135, 136), PARTP(), CRIT_2024)], rownote=LEAD_2024,
      question=QP(4, ESSAY_2024, '1. Tehnoloogia areng')),
    R('III2', [graded(L(135, 136), PARTP(), CRIT_2024)], rownote=LEAD_2024,
      question=QP(4, ESSAY_2024, '2. „Eesti suurim')),
]


# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the ten open asks of this sitting,
# I1a-e, I5, I6, II1, III1, III2. Live: I2, I3, I4 (3 cards); not touched
# (audited: see estonian-live-faults-2018-2025.json; all three carry the wrong
# row).
# Paper (rendered pp2-4): "Vasta I, II ja III ülesandele." / "Kõikidele
# ülesannetele tuleb vastata eesti keeles. Kokku on võimalik saada kuni 100
# punkti." (p2 y65-86); "I ÜLESANNE (30 punkti)" (p2 y112); the article
# "Eestlased ja protestid" runs pp2-3 (title p2 y168, paragraphs 1-10 to the
# byline "Anu Realo, lühendatult ajalehest Edasi.org, 10. juuni 2024" p3 y771
# and the editing note y784); p4 holds only questions: Q1 "Seleta oma
# sõnadega lahti järgmised sõnad ja väljendid:" over five LETTERED expressions
# a) innukas ... e) upitama, "(5 × 1)" at the right of e)'s line (y162);
# Q2-Q6 "(5)" each at the right of the question's last line (Q6's at y511);
# "II ÜLESANNE (30/100)" (y555); "III ÜLESANNE (40/100)" (y669), "Kirjuta
# vähemalt 300 sõna pikkune kirjand. Vali üks antud teemadest." (bold) over
# "1. Aktiivsed noored – ..." (y712) and "2. „Keskkond pole mitte meid
# ümbritsev, ... me sisaldume selles," / "oleme ise selle koostisosa.“" with
# the attribution "Fred Jüssi (bioloog, loodusfotograaf ja looduse
# populariseerija)" set small at the right of the second line (y742-757).
# PRICES:
# - I1a-e: "(5 × 1)": five expressions at 1 each, adding to Q1's 5; the
#   census walks the head down to the letters (tariff (1, 1, 1) each: PP()).
# - I5: "(5)" (p4 y401; PP()); scheme "(5)" (100).
# - I6: the census reads NO price (tariff None) and the exclusion says
#   "neither document states a tariff". BOTH ARE WRONG: the paper PRINTS
#   "(5)" at the right of Q6's last line "kogemusele tuginedes selle küsimuse
#   üle." (p4 y511 x482, rendered), and the scheme prints "(5)" at the end of
#   its reprint (line 118). The census misses it because the question's
#   quotation and its task are set as separate blocks (y442; y477-511) and it
#   keeps only the first. PY cannot read the paper's cell (its pattern needs a
#   mark word; this paper prints a bare "(5)") and PaperP cannot pick it (five
#   lines of p4 open "(5)"), so it is priced from the scheme's own printed
#   "(5)" on line 118 (RX), the same 5. If the lead extends PY to bare
#   bracketed cells: PY(4, 511). Not a remainder, not 10i.
# - II1: "(30/100)" (PARTP); scheme "II ÜLESANNE kuni 30 punkti" (134).
# - III1, III2: "(40/100)" (PARTP); scheme "III ÜLESANNE kuni 40 punkti" (143).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 4-6; p3 the
# annotations table, pp7-8 blank but for page numbers):
# - Q1 (62-63 reprint the stem with "(5 × 1)"): the expressions NUMBERED 1)-5)
#   where the paper LETTERS them a)-e), each with its gloss after " – "
#   (64-68). Paired by WORDS and order: 1) innukas = a), 2) murendama = b), 3)
#   keskne = c), 4) nappima = d), 5) upitama = e). (The exclusions' "prices no
#   ask that pairs with it" is the letter/number mismatch.)
# - Q5 (98-100 reprint the question in bold with "(5)"): SEVEN italic bullets
#   (101-103, 104, 105-106, 107-108, 109-111, 112, 113). No split.
# - Q6 (114-118 reprint the question in bold with "(5)"): SIX italic bullets
#   (119-120, 121-122, 123-124, 125-126, 127-128, 129), the second to sixth
#   each opening with a label ("Kanalid:", "Roll:", "Teemad:", "Omadused:",
#   "Tulemus:"). No split.
# - Part II (134): the task reprinted (135-139), then ONE italic run of
#   topics, 140-142 ("Rahumeelsed meeleavaldused ja vägivaldsed
#   väljaastumised, ... tehnoloogiline võimekus jne."), with no heading.
# - Part III (143): one descriptive line, 144-145, "Vähemalt 300 sõna pikkune
#   sidus teemakohane kirjand läbimõeldud sisu, selge ülesehituse ning sorava
#   lausestusega.", then both titles reprinted (146-149).
# - NO criteria and NO percentages anywhere in this scheme (rendered pp4-6;
#   the "II ja III ülesande hindamisel ..." block of 2018-2024 is gone).
# SHAPES:
# - I1a-e: one stated gloss each = one row at the paper's 1 (PP()), the
#   expression cut off (after " – ").
# - I5, I6: the bullets shown, priced as a whole on the 5 (questionTotal,
#   10a).
# - II1: the topic run is the scheme's content for the part (10a): one shown
#   row, priced as a whole on the paper's 30 (questionTotal), as Bulgarian
#   2025 II1; no criteria printed, so no graded row.
# - III1, III2: only a descriptive line and no criteria: R4 (unprinted) at
#   the paper's 40, the note quoting the line (ruling 4).
# JUDGEMENT CALLS:
# - 10f, Q1: the scheme reprints the stem as "Selgita järgmiste sõnade ja
#   väljendite tähendust (nii nagu need esinevad teksti kontekstis)." (62-63,
#   2024's wording) where the paper prints "Seleta oma sõnadega lahti
#   järgmised sõnad ja väljendid:" (p4 y65): the paper's words carded, the
#   scheme's quoted on each Q1 row.
# - I6's question is cut from the paper's lines: the quotation (y442) and the
#   task (y477-511); the census keeps only the quotation.
# - III2's question: the text layer files the right-hand attribution between
#   the title's two lines (y756 before y757); taken in the rendered order:
#   title line 1, "oleme ise selle koostisosa.“", then "Fred Jüssi (...)".
# - Part II's topic run keeps its closing "jne." (inside line 142).
# - The bullets' labels in I6 ("Kanalid:", "Roll:" ...) are the scheme's own
#   words at the head of each bullet: kept in the rows.
# - Reading text pp2-3 (rendered: title p2 y168 to the editing note p3 y784;
#   p4 opens with Q1). I1a-e, I5, I6, II1 carry pages=(2, 3). The live 2025
#   cards' sourceMaterial.pages [2, 3] agree with the render.
# GLYPHS: none. õ ä ö ü clean in the lines used ("ükskõiksed",
# "ühtekuuluvustunne", "väljaastumised", "Jüssi"); no š/ž in the lines used.
# The hyphens in "Kodu- ja välismaised" (119) and "ida- ja lõunaosas" (81) are
# ASCII hyphen-minus (checked), rendered as printed.

ESSAY_2025 = 'Kirjuta vähemalt 300 sõna pikkune'
Q1HEAD_2025 = quote(L(62, 63, after='1. ', before=' (5'), lead='The scheme reprints the question as')


def _essay_2025(d):
    return (f'Under Part III the scheme prints only “{L(144, 145).text(d)}” and reprints the two titles. '
            f'It prints no criteria and no split of the part\'s marks.')


SPECS[2025] = [
    R('I1a', [one(S(64, after='– '), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1b', [one(S(65, after='– '), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1c', [one(S(66, after='– '), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1d', [one(S(67, after='– '), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1e', [one(S(68, after='– '), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I5', [shown(L(101, 103)), shown(S(104)), shown(L(105, 106)), shown(L(107, 108)), shown(L(109, 111)),
             shown(S(112)), shown(S(113))], whole=True, pages=(2, 3)),
    R('I6', [shown(L(119, 120)), shown(L(121, 122)), shown(L(123, 124)), shown(L(125, 126)), shown(L(127, 128)),
             shown(S(129))], whole=True, total=RX(118, r'\((\d)\)'),
      question=QP(4, '6. „Usk enda', Run('Kui suurt rolli', 'kogemusele tuginedes')), pages=(2, 3)),
    R('II1', [shown(L(140, 142))], whole=True, pages=(2, 3)),
    R('III1', [unprinted(_essay_2025)],
      question=QP(4, ESSAY_2025, '1. Aktiivsed noored')),
    R('III2', [unprinted(_essay_2025)],
      question=QP(4, ESSAY_2025, '2. „Keskkond', 'oleme ise selle', 'Fred Jüssi')),
]


def specs(year):
    return SPECS.get(year, [])
