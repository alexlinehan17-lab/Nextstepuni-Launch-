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
      question=QL(4, 'Kirjuta umbes 300-sõnaline', 'Inimene on looduse kroon', 'Oma unistuste täide')),
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
SPECS[2016] = [
    R('II1', [graded(S(112), PARTP(), CRIT_2016)],
      rownote=both(examples(S(113, before=' Ränne'), S(113, after='Näiteks: '), S(114), L(119, 120), S(121),
                            L(122, 123), S(124), S(125)),
                   LEAD_2016),
      question=QP(4, Run('„Irooniliselt', 'ebakindluse eest'), 'Kommenteeri seda väidet'), pages=(2, 3)),
    R('III1', [graded(S(128), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, ESSAY_2016, '1) Kes maksab')),
    R('III2', [graded(S(128), PARTP(), CRIT_2016)], rownote=LEAD_2016,
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


def specs(year):
    return SPECS.get(year, [])
