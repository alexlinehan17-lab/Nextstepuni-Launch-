#!/usr/bin/env python3
"""Reviewed specs for the Latvian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/latvian/schemes/<year>-hl.md.
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


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2010
# ================================================================ 2010 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2010-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits – 100"
# and the instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y109-122); the reading text "Izglābušies un glābj citus" (p2 y153), twelve
# numbered paragraphs over pp2-3 to "Fragments no Jāņa Tropa raksta, ”Diena”,
# 02.10.2008" (p3 y712); p4 holds the questions: "I daļa (30 punkti)" (y79),
# Q1 "(5 punkti)" over a)-e) (live), Q2-Q6 "(5 punkti)" each; "II daļa (30
# punkti)" (y421), the commentary, ONE task with no number; "III daļa (40
# punkti)" (y549), two UNNUMBERED titles with "vai" between them and the
# instruction "Uzrakstiet eseju (vismaz 300 vārdu)!" under both (y665).
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "(5 punkti)" at the end of the question's own last line
# (rendered p4, right margin), read with PaperP: Q2 "2. No kā ..." (y230), Q3
# "3. Kāpēc ..." (y256), Q4 "savu viedokli ar piemēriem no teksta ." (y297),
# Q5 "Pamato savu viedokli ..." (y338), Q6 "tam aizdomāties." (y380). II: "II
# daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)" (PARTP). The
# scheme prints the same "(5 punkti)" on each reprint, "(30 punkti)" (56) and
# "(40 punkti)" (65).
# WHAT THE SCHEME PRINTS (rendered scheme pp2-3 = printed pages 1-2; answers
# in italics under each bold reprint):
# - Q2 (24 reprint): one paragraph, 25-27.
# - Q3 (28): one paragraph, 29-31.
# - Q4 (32-33): one paragraph, 34-36.
# - Q5 (37-38): THREE paragraphs, each opening a new line (rendered p2): 39-40
#   ("Sākumā Juris ir neveiksminieks. ... bijis sodīts."), 41-43 ("Viņš meklēja
#   risinājumus, ... iepazīšanās ar Nairu."), 44-45 ("Uzskatu, ka Juris kopumā
#   ir veiksmīgs cilvēks, ... nonākušiem.").
# - Q6 (46-47): one paragraph, 48-51.
#   No mark inside any answer.
# - Part II (56-59 reprint the head and the task): "Piemēram:" (60, bold) over
#   four bullets, 61-64.
# - Part III (65-69 reprint the head, both titles, "vai" and the instruction).
# - Criteria (70-76, printed once under Part III): "Piešķirot vērtējumu II un
#   III daļā tiks ņemti vērā šādi elementi:" -- for Parts II AND III -- then 1.
#   "– 30%" (71), 2. "30 %" (72-73), 3. "30 %" (74-75), 4. "10 %" (76): all four
#   printed, 100 %.
# SHAPES:
# - I2, I3, I4, I6: one printed model paragraph each: ONE claimable row,
#   one(sel, price) at the paper's 5 (lane convention, Finnish/Estonian).
# - I5: three paragraphs: three shown rows, whole=True on the printed 5 (10a).
# - II: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3. No descriptive line is
#   printed for the part, so the head is the criteria's own lead (70), as
#   Czech 2013-2014 and Dutch 2010; the four bullets quoted under the scheme's
#   own "Piemēram:" as examples, not a checklist (10a).
# - III1/III2: graded (10b), 12/12/12/4 of 40; head the criteria's lead (70).
# JUDGEMENT CALLS:
# - Part III's titles are unnumbered but the census keys them III1/III2;
#   each card's question is its title and the instruction printed under both
#   ("Uzrakstiet eseju (vismaz 300 vārdu)!"), in printed order (the census
#   gives III1 the bare title and III2 the title and the instruction).
# - Q6's row opens by restating the question ('Nairai un Jurim ir sapnis
#   izveidot " pusceļa mājas", jo ...'): that is the scheme's own answer
#   sentence, not a reprint (the reprint is 46-47 above it), so it stays.
# - Reading text: pp2-3 (rendered: the title and paragraphs 1-5 on p2, 6-12
#   and the byline on p3; p4 holds only the questions). The live Q1 card's
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none. No character outside Latvian letters and punctuation in
# either text layer; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in
# every line used. Lifted as printed: "Juri dzīve" (39, for "Jura dzīve"),
# "zin kā" (71).

CRIT_2010 = crit(71, (72, 73), (74, 75), 76)
HEAD_2010 = S(70)

SPECS[2010] = [
    R('I2', [one(L(25, 27), PaperP(4, '2. No kā'))], total=PaperP(4, '2. No kā'), pages=(2, 3)),
    R('I3', [one(L(29, 31), PaperP(4, '3. Kāpēc'))], total=PaperP(4, '3. Kāpēc'), pages=(2, 3)),
    R('I4', [one(L(34, 36), PaperP(4, 'savu viedokli ar'))], total=PaperP(4, 'savu viedokli ar'),
      pages=(2, 3)),
    R('I5', [shown(L(39, 40)), shown(L(41, 43)), shown(L(44, 45))], whole=True,
      total=PaperP(4, 'Pamato savu viedokli'), pages=(2, 3)),
    R('I6', [one(L(48, 51), PaperP(4, 'tam aizdomāties.'))], total=PaperP(4, 'tam aizdomāties.'),
      pages=(2, 3)),
    R('II', [graded(HEAD_2010, PARTP(), CRIT_2010)],
      rownote=examples(S(60), S(61), S(62), S(63), S(64)), pages=(2, 3)),
    R('III1', [graded(HEAD_2010, PARTP(), CRIT_2010)],
      question=QP(4, '"Palīdzība', 'Uzrakstiet eseju')),
    R('III2', [graded(HEAD_2010, PARTP(), CRIT_2010)],
      question=QP(4, '"Pilnīgi', 'Uzrakstiet eseju')),
]


# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2011-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the title "Jānis Rudzītis savā klasē uzņēma meiteni
# ratiņkrēslā" and its byline "Fragments no Ievas Albertes raksta, ”Diena”,
# 02.10.2010" (p2 y57-85), "Maksimālais punktu skaits – 100" and the
# instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y136-149); the text, ten numbered paragraphs, p2 y174 to p3 y400 ("Nu,
# forši, vai ne?"); "I daļa (30 punkti)" (p3 y443) and the questions on p3:
# Q1 "(5 punkti)" over a)-e) (live), Q2-Q6 "(5 punkti)" each; "II daļa (30
# punkti)" (p4 y57), the commentary, ONE task with no number; "III daļa (40
# punkti)" (p4 y202), the instruction "Uzrakstiet eseju (vismaz 300 vārdu)!"
# (y230) over two UNNUMBERED titles with "vai" between them (y260, y316).
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "2. Kāpēc ..." (p3 y612), Q3 "3. Ar 3 piemēriem ..." (y642), Q4 "4.
#   Kā tu domā ..." (y669): "(5 punkti)" at the end of the question's own
#   line (rendered p3, right margin), PaperP. Q5: at the end of its second
#   line "teksta. (5 punkti)" (y713), PaperP.
# - Q6: "(5 punkti)" on a line of its own under the question (p3 x474 y757).
#   Two lines of p3 open "(5 punkti)" (Q1's, y513), so PaperP cannot single it
#   out: PY(3, 757) reads that printed cell.
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (50, 58).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2; pp2 and
# 5-8 blank; answers in italics):
# - Q2 (25 reprint): one paragraph, 26-27. Q3 (28-29): one paragraph, 30-31.
#   Q4 (32): one paragraph, 33-34. Q5 (35-36): one paragraph, 37-39. Q6
#   (40-41): one paragraph, 42-45. No mark inside any.
# - Part II (50-53 reprint the head and the task): "Piemēram:" (54, bold) over
#   three bullets, 55, 56, 57. No criteria, no percentages.
# - Part III (58-62): the head, the instruction, both titles and "vai" -- and
#   nothing under them (rendered p4: the page ends at title 2; pp5-8 blank).
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I2-I6: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - II: an indicative list under "Piemēram:" with no mark on any point and no
#   criteria: the three bullets as shown rows on the paper's 30
#   (questionTotal, 10a; Czech 2024 II), the heading in the rownote, labelled
#   as examples.
# - III1/III2: nothing printed for the part -> unprinted (ruling 4) at the
#   paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS:
# - Q6 (10f): the paper prints "Pamato savu atbildi kāpēc vai kāpēc nav."
#   (p3 y743); the scheme reprints "... kāpēc ir vai kāpēc nav" (40). The
#   paper's words are the question; the scheme's reprint quoted on the row.
# - III2's question: the instruction printed above both titles, then title 2
#   (the census gives the bare title); III1's census text already reads the
#   instruction and title 1, in printed order.
# - Part III title 1: the scheme reprints it '"Mīlestība neko nemaksā ”' with
#   a space before the closing mark (60): spacing only, not quoted.
# - Reading text: pp2-3 (rendered: title, byline and paragraphs 1-7 on p2,
#   8-10 on p3 above "I daļa"). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Lifted as printed: "kopā grūtā brīdī ." and "lai palīdzētu ."
# (43, 45, a space before the stop), „Latvijas lepnums " (44).

ESSAY_2011 = 'Uzrakstiet eseju'


def _points_2011(d):
    return (f'The scheme heads them “{S(54).text(d)}”: examples, not a checklist. None carries a mark of its '
            f'own, and the scheme prints no criteria for the part.')


def _essay_2011(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria, no descriptive line and no split of the part\'s marks.')


SPECS[2011] = [
    R('I2', [one(L(26, 27), PaperP(3, '2. Kāpēc'))], total=PaperP(3, '2. Kāpēc'), pages=(2, 3)),
    R('I3', [one(L(30, 31), PaperP(3, '3. Ar 3'))], total=PaperP(3, '3. Ar 3'), pages=(2, 3)),
    R('I4', [one(L(33, 34), PaperP(3, '4. Kā tu'))], total=PaperP(3, '4. Kā tu'), pages=(2, 3)),
    R('I5', [one(L(37, 39), PaperP(3, 'teksta.'))], total=PaperP(3, 'teksta.'), pages=(2, 3)),
    R('I6', [one(L(42, 45), PY(3, 757))], total=PY(3, 757), pages=(2, 3),
      rownote=quote(S(40, after='6. '), lead='The scheme reprints this question as')),
    R('II', [shown(S(55)), shown(S(56)), shown(S(57))], whole=True, rownote=_points_2011, pages=(2, 3)),
    R('III1', [unprinted(_essay_2011)]),
    R('III2', [unprinted(_essay_2011)], question=QP(4, ESSAY_2011, '„Mēs esam')),
]


# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2012-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the instruction with the rule "... Visām atbildēm
# jābūt latviski." (p2 y77-90), "Maksimālais punktu skaits – 100", the title
# "Drošās rokas, kurās iekrist un nelaisties vaļā" (p2 y144); fourteen
# numbered paragraphs p2 y172 to p3 y462, the byline "Fragments no Gunitas
# Nagles raksta, ”NRA”, 02.10.2010" (p3 y489); "I daļa (30 punkti)" (p3 y519)
# and Q1 "(5 punkti)" over a)-e) on p3 (live); Q2-Q6 on p4, "(5 punkti)" each;
# "II daļa (30 punkti)" (p4 y398), the commentary, ONE task with no number;
# "III daļa (40 punkti)" (p4 y510), the instruction "Uzrakstiet eseju (vismaz
# 300 vārdu)!" (y537) over two UNNUMBERED titles with "vai" between them.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "(5 punkti)" at the end of the question's own last line
# (rendered p4, right margin), read with PaperP: Q2 "2. Kāpēc autore ..."
# (y78), Q3 "3. Kāpēc Nauris ..." (y133), Q4 "4. Kāpēc Līga ..." (y187), Q5
# 'un pazust".' (y256), Q6 "Analizē šīs ..." (y331). II: "II daļa (30
# punkti)" (PARTP); III1/III2: "III daļa (40 punkti)" (PARTP). The scheme
# prints the same "(5 punkti)" on each reprint, "(30 punkti)" (52) and "(40
# punkti)" (60).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2; pp2, 5-6
# blank; answers in italics):
# - Q2 (26 reprint): TWO paragraphs (rendered p3: line 28 ends short at
#   "reputāciju." and "Stāsts lieliski parāda" opens the next line): 27-28 and
#   29-30.
# - Q3 (31): one paragraph, 32-33. Q4 (34): one paragraph, 35-36. Q5 (37-38):
#   one paragraph, 39-41.
# - Q6 (42-43): TWO paragraphs: 44-46 ("Labsirdība un labestība ... domājošam
#   cilvēkam.", the last line short at the foot of p3) and 50-51 on p4 ("Šī
#   īpašības ir pamats, ... savu ģimeni.").
#   No mark inside any answer.
# - Part II (52 the head; 53-54 reprint the task's second line only, not
#   "Ka tu vari raksturot Nauri, ..."): "Piemēram:" (55, bold) over four bold
#   bullets, 56-59 ("patstāvīgi domājošs," / "tāds, kam rūp citi," /
#   "atvērts," / "cilvēcīgs."). No criteria, no percentages.
# - Part III (60-64): the head, the instruction, both titles and "vai" -- and
#   nothing under them (rendered p4; pp5-6 blank). NO criteria anywhere in
#   this scheme.
# SHAPES:
# - I3, I4, I5: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I2, I6: two paragraphs each: shown rows, whole=True on the printed 5.
# - II: an indicative list under "Piemēram:", no mark on any point, no
#   criteria: the four bullets as shown rows on the paper's 30
#   (questionTotal, 10a), the heading in the rownote, labelled as examples.
# - III1/III2: nothing printed for the part -> unprinted (ruling 4) at the
#   paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS:
# - Q2 (10f): the paper prints "Kāpēc autore 3 rindkopā saka, ..." (p4 y78,
#   rendered); the scheme reprints "2 rindkopā" (26). The paper's words are
#   the question; the scheme's reprint quoted on the row. (The phrase "Gandrīz
#   laimīgām." closes paragraph 2 of the text, rendered p2.)
# - I2 and I6 split at the scheme's own line breaks (a short last line, then
#   a new sentence on a new line), as 2010 Q5; neither break carries a gap.
#   If the lead reads either as one paragraph, flip to one(L(27, 30), ...) /
#   one(J(L(44, 46), L(50, 51)), ...).
# - Part II's bullets keep their printed trailing commas (lifted as printed).
# - III2's question: the instruction printed above both titles, then title 2
#   (the census gives the bare title); III1's census text already reads the
#   instruction and title 1.
# - Reading text: pp2-3 (rendered: title and paragraphs 1-9 on p2, 10-14 and
#   the byline on p3 above "I daļa"). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Printed as such (paper p4 cropped at 300 dpi): "sabiedribā"
# (title 2, i without a macron; the scheme reprints it the same, 64), "raktura"
# (Q6), "nezin" (Part II). Lifted as printed: "Atbalstāms it tas" (39), "atzīst
# ," (40), "'Otra" (45), "Šī īpašības" (50).

ESSAY_2012 = 'Uzrakstiet eseju'


def _points_2012(d):
    return (f'The scheme heads them “{S(55).text(d)}”: examples, not a checklist. None carries a mark of its '
            f'own, and the scheme prints no criteria for the part.')


def _essay_2012(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria, no descriptive line and no split of the part\'s marks.')


SPECS[2012] = [
    R('I2', [shown(L(27, 28)), shown(L(29, 30))], whole=True, total=PaperP(4, '2. Kāpēc'), pages=(2, 3),
      rownote=quote(S(26, after='2. ', before=' (5'), lead='The scheme reprints this question as')),
    R('I3', [one(L(32, 33), PaperP(4, '3. Kāpēc'))], total=PaperP(4, '3. Kāpēc'), pages=(2, 3)),
    R('I4', [one(L(35, 36), PaperP(4, '4. Kāpēc'))], total=PaperP(4, '4. Kāpēc'), pages=(2, 3)),
    R('I5', [one(L(39, 41), PaperP(4, 'un pazust'))], total=PaperP(4, 'un pazust'), pages=(2, 3)),
    R('I6', [shown(L(44, 46)), shown(L(50, 51))], whole=True, total=PaperP(4, 'Analizē šīs'), pages=(2, 3)),
    # the scheme reprints the task without the paper's question about Nauris (second reader): quoted (10f)
    R('II', [shown(S(56)), shown(S(57)), shown(S(58)), shown(S(59))], whole=True,
      rownote=both(quote(L(53, 54), lead='The scheme reprints the task as'), _points_2012),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2012)]),
    R('III2', [unprinted(_essay_2012)], question=QP(4, ESSAY_2012, '"Mūsdienu')),
]


# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2013-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the instruction with the rule "... Visām atbildēm
# jābūt latviski." (p2 y63-76), the title "Ja es kļūšu slavens" (p2 y103),
# "Maksimālais punktu skaits – 100"; fourteen numbered paragraphs p2 y156 to
# p3 y632, the byline "Fragments no Ievas Puķes raksta „Ir ",14.12.2011" (p3
# y657); p4 holds the questions: "I daļa (30 punkti)" (y67), Q1 "(5 punkti)"
# over a)-e) (live), Q2-Q6 "(5 punkti)" each; "II daļa (30 punkti)" (y534),
# the commentary, ONE task with no number; "III daļa (40 punkti)" (y622), the
# instruction "Uzrakstiet eseju par vienu no esejām (vismaz 300 vārdu)!"
# (y647) over two UNNUMBERED titles, the first on two lines (y672-696), "vai"
# (y721), the second (y745).
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "2. Izskaidro ..." (p4 y282), Q3 "3. Izskaidro ..." (y321, printed
#   "(5punkti)."), Q4 "kāpēc nav viegli rakstīt bestsellerus?" (y378), Q6 "pēc
#   tavām domām ..." (y484): the price at the end of the question's own last
#   line (rendered p4, right-hand column), PaperP.
# - Q5: "(5 punkti)" on a line of its own under the question (p4 x447 y435):
#   PY(4, 435).
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (104, 119).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# standard note to teachers; answers in italics):
# - Q2 (55 reprint): one paragraph, 56-59.
# - Q3 (60-61 reprint, "(5punkti)." on a line of its own): under the italic
#   heading "KĀ" (62) the points 63-64 ("Lasot grāmatas, ... runājošā vidē,"),
#   under "KĀPĒC" (65) 66-68 ("Lasot daudz zinātniskās fantastikas grāmatas,
#   ... darbus rakstīšanu.").
# - Q4 (69-71 reprint): TWO paragraphs, 72-74 ("Lielā mērā tas ir talanta
#   jautājums. ... tas ir jāizkopj.", the last line short at the foot of p3)
#   and 79-82 on p4 ("Tomam rakstīt patika jau skolas laikā. ... lai
#   rakstītu romānu.").
# - Q5 (83-86 reprint): TWO paragraphs, 87-90 ("Kad cilvēks ir apsēsts ...
#   savai apsēstībai.", line 90 short) and 91-95 ("Cilvēkam nav jābūt apsēstam
#   ... rakstīt prasmes.").
# - Q6 (96-97 reprint, no price on it): one paragraph, 98-103, with "(5
#   punkti)" set at the end of its last line (103, rendered p4).
# - Part II (104-107 reprint the head and the task): one italic paragraph,
#   112-118 (p5), "Tomam ir svarīgi ne tikai zināt, ... satura izjūtā."
# - Part III (119-122 reprint the head, the instruction and title 1): FIVE
#   italic bullets under title 1, 123-127; then "vai" and title 2 (128-129)
#   with nothing under it.
#   NO criteria anywhere in this scheme (rendered pp3-5; pp6-7 blank).
# SHAPES:
# - I2, I6: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I3: two points under two printed headings: shown rows, whole=True on the
#   printed 5; each heading ("KĀ", "KĀPĒC") on its own row's note (the row's
#   lead), never in the row.
# - I4, I5: two paragraphs each: shown rows, whole=True on the printed 5.
# - II: one paragraph of model content for a 30-mark commentary with no
#   criteria: shown, whole=True on the paper's 30 (10a; Finnish 2025 II1).
# - III1: the five bullets the scheme prints under title 1, shown on the
#   paper's 40 (questionTotal, 10a), labelled as examples.
# - III2: nothing printed under title 2 -> unprinted (ruling 4) at the
#   paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS (10f: the paper's words are the question; where the scheme
# rewords one, its reprint is quoted on the row's note):
# - Q3: paper "Izskaidro kā un kāpēc Toms iemācijās angļu valodu
#   (6.paragrāfs)?", scheme "Izskaidro, kā un kāpēc Toms iemācījās angļu
#   valodu (6.rindkopa)!" (60). Quoted. The question is cut from the paper's
#   line before its "(5punkti)." (the census keeps the stop after the price).
# - Q4: the scheme adds "(7.rindkopa)" and ends "!" (69-70). Quoted.
# - Q5: the scheme adds "(13.rindkopa)" (83-85; the quotation is in paragraph
#   9 of the text, rendered p3). Quoted.
# - III1: paper "Uzrakstiet eseju par vienu no esejām" / '"Toms izpakojot
#   čemodānus, jau kā jauns vīrietis. "' / "... kāpēc / kāpēc nē !"; scheme
#   "... par vienu no tēmām ..." (120), '"Toms izpakoja čemodānus jau ..."'
#   (121), "... kāpēc / kāpēc ne!" (122). Quoted.
# - Q2, Q6, Part II: the scheme's reprints differ in punctuation only (commas,
#   "!" for "?"); not quoted.
# - I4, I5 split at the scheme's own paragraph ends (a short last line, the
#   next sentence on a new line, rendered pp3-4); if the lead reads either as
#   one paragraph, flip to one(...).
# - Q3's points keep their printed trailing comma (64: "... runājošā vidē,").
# - III2's question: the instruction printed above both titles, then title 2
#   (the census gives the bare title); III1's census text already reads the
#   instruction and title 1's two lines.
# - Reading text: pp2-3 (rendered: title and paragraphs 1-7 on p2, 8-14 and
#   the byline on p3; p4 holds only the questions). The live Q1 card's
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Lifted as printed: "studējot ," (63), "darbus rakstīšanu" (67),
# "rakstīt prasmes" (95, 116), "raksta ,t.i.," and "saka :„Nekad" (113-114),
# "svešvalodu valodas" (125).

ESSAY_2013 = 'Uzrakstiet eseju'
REPRINT = 'The scheme reprints this question as'


def _part2_2013(d):
    return ('The scheme prints this one paragraph under the task, with no mark inside it and no criteria '
            'for the part.')


def _title1_2013(d):
    return (f'The scheme reprints the instruction and this title as “{S(120).text(d)}” “{S(121).text(d)}” '
            f'“{S(122).text(d)}” Under it, with no heading and no mark, it prints these points: examples, '
            f'not a checklist. It prints no criteria for the part.')


def _title2_2013(d):
    return ('The scheme reprints the part\'s head, the instruction and both titles. It prints five points '
            'under the first title and nothing under this one: no criteria, no descriptive line and no '
            'split of the part\'s marks.')


SPECS[2013] = [
    R('I2', [one(L(56, 59), PaperP(4, '2. Izskaidro'))], total=PaperP(4, '2. Izskaidro'), pages=(2, 3)),
    R('I3', [shown(L(63, 64), lead=S(62)), shown(L(66, 68), lead=S(65))], whole=True,
      total=PaperP(4, '3. Izskaidro'), pages=(2, 3),
      rownote=quote(S(60, after='3. '), lead=REPRINT),
      question=lambda d, _q: PC(4, '3. Izskaidro', after='3. ', before='(5punkti)').text(d)),
    R('I4', [shown(L(72, 74)), shown(L(79, 82))], whole=True, total=PaperP(4, 'kāpēc nav viegli'),
      pages=(2, 3), rownote=quote(L(69, 70, after='4. '), lead=REPRINT)),
    R('I5', [shown(L(87, 90)), shown(L(91, 95))], whole=True, total=PY(4, 435), pages=(2, 3),
      rownote=quote(L(83, 85, after='5. '), lead=REPRINT)),
    R('I6', [one(L(98, 103, before='(5'), PaperP(4, 'pēc tavām domām'))], total=PaperP(4, 'pēc tavām domām'),
      pages=(2, 3)),
    R('II', [shown(L(112, 118))], whole=True, rownote=_part2_2013, pages=(2, 3)),
    R('III1', [shown(S(123)), shown(S(124)), shown(S(125)), shown(S(126)), shown(S(127))], whole=True,
      rownote=_title1_2013),
    R('III2', [unprinted(_title2_2013)], question=QP(4, ESSAY_2013, '"Ja sekosi')),
]


# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I2-I6, II1, II2. Live: I1 (Q1 carded whole, lv-2014-hl-i-1); not touched
# (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits –
# 100", the instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y95-108); the interview "Latvijai jāsargā savs derīgais izraktenis" (p2
# y133), a lead-in and seven numbered questions with their answers, p2 y159
# to p3 y754, "(980 vārdi) Fragments no A.Burves-Rozītes intervijas
# laikrakstā „Ir”,2013.gada 26.septembris" (p3 y775); p4 holds the questions:
# "I daļa (30 punkti)" (y63), Q1 "(5 punkti)" over a)-e) (live), Q2-Q6 "(5
# punkti)" each; "II daļa (30 punkti)" (y521), the commentary, ONE task with
# no number; then the essay part, which the paper MISPRINTS as "II daļa (40
# punkti)" (y618; rendered p4: "II", not "III"), the instruction
# "Uzrakstiet pārspriedumu par vienu no tēmām! (ne mazāk kā 300 vārdu)"
# (y646) over two titles numbered "1." (y674) and "2." (y729-743), "vai"
# between them. The scheme heads it "III daļa (40 punkti)" (143).
# CENSUS (for the lead): because of the misprint the lt walker reads both
# heads as Part II: it keys the essay titles II1/II2 (the asks this brief
# lists) and keys NO ask for the commentary "„Cilvēkresursi ir tas derīgais
# izraktenis, ..." (p4 y549-562), which is in neither the live bank nor the
# exclusions. Under ruling B the titles are Section III Q1/Q2 and the
# commentary is Section II. Drafted here at the census keys as the brief
# requires; the lead decides the keys and the citation ("2014 HL Section II
# Q1/Q2" as keyed). The topic is unaffected: lt_topics files Latvian
# commentary and essay under the same id (latvian-1-0). sl_lib reads the
# sitting as two-part (no 'III' key), so II1/II2 carry no reading text, as an
# essay should.
# Ready spec for the commentary once the census keys it (as 'II', source
# forced because the sitting reads as two-part):
#   R('II', [shown(L(121, 122)), shown(S(123)), shown(L(124, 125)), shown(L(126, 127)),
#            shown(L(128, 129)), shown(L(135, 139)), shown(L(140, 142))], whole=True,
#     total=PaperP(4, 'II daļa (30'), source='text', pages=(2, 3),
#     rownote=both(quote(L(119, 120), lead='The scheme reprints the task as'), _points_2014),
#     question=QP(4, Run('„Cilvēkresursi', 'apgalvojumu, balstoties'))),
#   (the paper prints "Izsakiet viedokli", the scheme "Izsaki viedokli": 10f.)
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "(5 punkti)" at the end of the question's own last line
# (rendered p4, right margin), read with PaperP: Q2 "2. Kas Latvijā ..."
# (y229), Q3 "3. Kāpēc ..." (y285), Q4 "šāda secinājuma? ..." (y354), Q5
# "viedokli par šo apgalvojumu!" (y424), Q6 "6. Raksturojiet ..." (y479).
# II1/II2: the misprinted head's own "(40 punkti)" (PaperP on "II daļa (40";
# PARTP refuses, the two "II daļa" heads printing 30 and 40).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# standard note to teachers; answers in italics, each point opening "✓"):
# - Q2 (62 reprint): five ✓ points, 63-67, one line each.
# - Q3 (68): seven ✓ points, 69, 70, 71, 72, 73-74, 75, 76-78.
# - Q4 (79-80): three ✓ points, 86-88, 89-90, 91-93 (p4).
# - Q5 (94-95): four ✓ points, 96-97, 98-99, 100, 101-102.
# - Q6 (103): seven ✓ points, 104-106, 107-108, 109, 110-111, 112-113,
#   114-115, 116-117.
#   No mark on any point, none says how many are wanted.
# - Commentary (118-120 reprint): seven ✓ points, 121-142 (see the ready spec).
# - Essay (143 "III daļa (40 punkti)", 144-148 reprint the instruction and
#   both titles): nothing under them (rendered p5; pp6-7 blank). NO criteria
#   anywhere in this scheme.
# SHAPES:
# - I2-I6: points with no per-point mark: shown rows, whole=True on the
#   paper's printed 5 (10a).
# - II1/II2: nothing printed under the titles -> unprinted (ruling 4) at the
#   paper's 40; the note quotes the paper's misprinted head and the scheme's
#   (10f: an SEC printed error on the first row's note).
# JUDGEMENT CALLS:
# - Q2 prints five points for five marks, but the scheme gives no mark to any
#   point and does not say "1 punkts" each: shown, not claimable at 1 each
#   (never guess a mark).
# - Q4 point 3 (91-93) and Q6 points are lifted as printed, without a full
#   stop where the scheme sets none.
# - Questions: the census's text for I2-I6 (checked on the render; no price);
#   II1/II2 the instruction line and the title, cut from the paper's lines
#   (the census gives II1 the title with the "vai" printed under it, II2 the
#   bare title). Title 2's attribution "Ralfs Valdo Emersons (1803-1882)",
#   printed on its second line, is kept.
# - Reading text: pp2-3 (rendered: title, lead-in and interview questions 1-3
#   on p2, 4-7 and the byline on p3; p4 holds only the questions). The live
#   Q1 card's sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used ("✓" U+2713 is the scheme's own tick, taken off as a bullet).
# Lifted as printed: "Vjačelavs" (92), "palīdz, rada" (102), "Imigrācija"
# (126, for emigration).

ESSAY_2014 = 'Uzrakstiet pārspriedumu'


def _points_2014(d):
    return ('The scheme gives no mark to any of these points and does not say how many are wanted: '
            'shown as the scheme prints them, scored on the question\'s total.')


def _essay_2014(d):
    # 10f, in plain words (coordinator ruling 2, 20 Nov): the essay part is Part III, though the paper misprints
    # its heading
    return (f'This is Part III of the paper, the essay. The paper misprints its heading as '
            f'“{PL(4, "II daļa (40").text(d)}”, the same number as the commentary before it; the scheme heads '
            f'it “{S(143).text(d)}”. The scheme reprints the instruction and the two titles and prints nothing '
            f'under them: no criteria, no descriptive line and no split of the part\'s marks.')


SPECS[2014] = [
    R('I2', [shown(S(63)), shown(S(64)), shown(S(65)), shown(S(66)), shown(S(67))], whole=True,
      total=PaperP(4, '2. Kas Latvijā'), rownote=_points_2014, pages=(2, 3)),
    R('I3', [shown(S(69)), shown(S(70)), shown(S(71)), shown(S(72)), shown(L(73, 74)), shown(S(75)),
             shown(L(76, 78))], whole=True, total=PaperP(4, '3. Kāpēc'), rownote=_points_2014, pages=(2, 3)),
    R('I4', [shown(L(86, 88)), shown(L(89, 90)), shown(L(91, 93))], whole=True,
      total=PaperP(4, 'šāda secinājuma?'), rownote=_points_2014, pages=(2, 3)),
    R('I5', [shown(L(96, 97)), shown(L(98, 99)), shown(S(100)), shown(L(101, 102))], whole=True,
      total=PaperP(4, 'viedokli par šo'), rownote=_points_2014, pages=(2, 3)),
    R('I6', [shown(L(104, 106)), shown(L(107, 108)), shown(S(109)), shown(L(110, 111)), shown(L(112, 113)),
             shown(L(114, 115)), shown(L(116, 117))], whole=True, total=PaperP(4, '6. Raksturojiet'),
      rownote=_points_2014, pages=(2, 3)),
    # Section III (the census re-keys the misprinted "II daļa (40 punkti)" head as Part III: lt_paper.MISPRINTED_PART)
    R('III1', [unprinted(_essay_2014)], total=PaperP(4, 'II daļa (40'),
      question=QP(4, ESSAY_2014, '1. „Zinātne')),
    R('III2', [unprinted(_essay_2014)], total=PaperP(4, 'II daļa (40'),
      question=QP(4, ESSAY_2014, Run('2. „Mēs varam', 'neglabāsim'))),
]

# The commentary (bare 'II', as the other sittings; keyed by the walker once the misprinted essay head is read
# as Part III; the lead, from the drafter's ready spec above): its points shown on the head's printed 30.
SPECS[2014].insert(5, R('II', [shown(L(121, 122)), shown(S(123)), shown(L(124, 125)), shown(L(126, 127)),
                               shown(L(128, 129)), shown(L(135, 139)), shown(L(140, 142))], whole=True,
                        total=PaperP(4, 'II daļa (30'), source='text', pages=(2, 3),
                        rownote=both(quote(L(119, 120), lead='The scheme reprints the task as'), _points_2014),
                        question=QP(4, Run('„Cilvēkresursi', 'apgalvojumu, balstoties'))))


# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2015-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json). Q1 is not open
# this sitting (the live card holds it), so nothing is carded at 'I1' here.
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits –
# 100", the instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y104-132); a lead-in naming the two texts (p2 y159-187), the title "Modrā
# fotoacs" (p2 y228), twelve numbered paragraphs p2 y254 to p3 y440, "(662
# vārdi)" and the byline "Inga Žolude, laikraksts ”Kultūras diena”, 2014.
# gada 1. septembris" (p3 y466-492); "I daļa (30 punkti)" (p3 y531), Q1 "(5
# punkti)" over a)-e) (live) and Q2 on p3, Q3-Q6 on p4, "(5 punkti)" each;
# "II daļa (30 punkti)" (p4 y422), the commentary, ONE task with no number;
# "III daļa (40 punkti)" (p4 y560), the instruction "Uzrakstiet
# pārspriedumu par vienu no tēmām! (ne mazāk kā 300 vārdu)" (y588) over two
# titles numbered "1." (y616) and "2." (y685), "vai" between them.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "piekrītat autores sacītajam? (5 punkti)" (p3 y725), Q3 "3.
#   Paskaidrojiet ..." (p4 y57), Q6 "tekstā minētā mūsdienu parādība?" (p4
#   y336): the price at the end of the question's own last line, PaperP.
# - Q4 and Q5: "(5 punkti)" on a line of its own under the question (p4 x453
#   y168 and y251; rendered p4, right margin). Two lines of p4 open "(5
#   punkti)", so PaperP cannot single either out: PY(4, 168), PY(4, 251).
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (219, 244).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-9 = printed pages 2-8; p2 the
# note to teachers; pp10-11 blank). It REPRINTS THE WHOLE READING TEXT first
# (47-113), then Q1 (114-123), then each question with its answer points in
# italics, each point under a check mark ✓:
# - Q2 (128-129 reprint): four points, 130-132, 133-134, 135-136, 137-139.
# - Q3 (140): four points, 141-143, 144-145, 146-147, 148-149.
# - Q4 (150-152, "(5punkti)"): four points, 153-156, 157-163, 164-165 + 170-171
#   (over the page break), 172-175 (closing on its own question "Kādas var būt
#   šādas rīcības sekas?", inside the point on the render).
# - Q5 (176-178): four points, 179-181, 182-184, 185-186, 187-189.
# - Q6 (190-192): five points, 193-196, 197-200, 201-207, 208-209 + 214-215
#   (over the page break), 216-218.
# - Part II (219-222 reprint the head and the task as the paper prints it):
#   four points, 223-227, 228-231, 232-237, 238-243.
# - Part III (244-245 the head and the instruction): under title 1 (246) an
#   italic paragraph 247-251 ("Mēs dzīvojam moderno tehnoloģiju laikmetā. ...
#   un citiem faktoriem:") over eleven ✓ items, 252, 257-258, 259-260, 261,
#   262, 263, 264, 265, 266, 267, 268, and a twelfth "u.c." (269); then two
#   starred notes defining the title's words, "*Virtuāls ir ..." (270-272) and
#   "**vajadzības - ..." (273-274). Under title 2 (275): five ✓ paragraphs,
#   276-281, 282-286, 287-294, 295-298 + 303-304 (over the page break),
#   305-309.
#   No mark on any point, no criteria anywhere in this scheme.
# SHAPES:
# - I2-I6: points with no per-point mark: shown rows, whole=True on the
#   paper's printed 5 (10a).
# - II: four points, shown, whole=True on the paper's 30 (10a).
# - III1: the paragraph and the eleven items, shown, whole=True on the
#   paper's 40 (10a); the two starred notes quoted on the row's note.
# - III2: the five paragraphs, shown, whole=True on the paper's 40 (10a).
# JUDGEMENT CALLS:
# - III1's opening paragraph is the scheme's own content (five lines), not a
#   bare heading, so it is a row, though it ends "citiem faktoriem:" leading
#   into the list. If the lead reads it as a heading, move it to the rownote.
# - III1's "u.c." (269, "etc.") is left out of the rows (not an item); the
#   note says the items are examples, not a checklist.
# - The starred notes (270-274) define "virtuāls" and "vajadzības", the
#   title's words: quoted on the note, not rows (they are definitions, not an
#   essay's content).
# - Questions: the census's text for I2-I6 and II (checked on the render; no
#   price); III1/III2 the instruction line and the title (the census gives
#   the bare titles).
# - Reading text: pp2-3 (rendered: lead-in, title and paragraphs 1-6 on p2,
#   7-12, the word count and the byline on p3 above "I daļa"). The live Q1
#   card's sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS (reported, not mapped): the scheme's tick bullets are a Wingdings
# glyph that the text layer reads as U+0039 DIGIT NINE ("9 Mūsdienās ...",
# 130 ff.); the render shows a check mark ✓. Each point is cut after its "9 "
# (the bullet), so no row carries it. The scheme's cover and note pages (lines
# 4-41) are in a font with no usable text layer (Caesar-shifted ASCII and
# control characters U+0003, U+0013-U+0018, "&RLPLVL~Q" for "Coimisiún");
# nothing is lifted from them. Every Latvian letter in the lines used reads as
# the render shows it. Lifted as printed: "neieciešams" (157), "lietam"
# (306), "garīgā,t.i.," (303), "Rietumeiropas ... reizēm" (295).

ESSAY_2015 = 'Uzrakstiet pārspriedumu'


def _tick_2015(a, b=None):
    """A ✓ point, its Wingdings tick (read "9") cut off its first line."""
    return L(a, b, after='9 ')


def _points_2015(d):
    return ('The scheme gives no mark to any of these points and does not say how many are wanted: '
            'shown as the scheme prints them, scored on the question\'s total.')


def _part2_2015(d):
    return ('The scheme prints these points under the task, with no mark on any of them and no criteria '
            'for the part: examples, not a checklist.')


def _title1_2015(d):
    return (f'The scheme prints this paragraph and these items under the title, with no mark on any of them '
            f'and no criteria for the part: examples, not a checklist. The list ends “{S(269, after="9 ").text(d)}”. '
            f'It adds two notes on the title\'s words: “{L(270, 272).text(d)}” “{L(273, 274).text(d)}”')


def _title2_2015(d):
    return ('The scheme prints these paragraphs under the title, with no mark on any of them and no '
            'criteria for the part: examples, not a checklist.')


SPECS[2015] = [
    R('I2', [shown(_tick_2015(130, 132)), shown(_tick_2015(133, 134)), shown(_tick_2015(135, 136)),
             shown(_tick_2015(137, 139))], whole=True,
      total=PaperP(3, 'piekrītat autores'), rownote=_points_2015, pages=(2, 3)),
    R('I3', [shown(_tick_2015(141, 143)), shown(_tick_2015(144, 145)), shown(_tick_2015(146, 147)),
             shown(_tick_2015(148, 149))], whole=True,
      total=PaperP(4, '3. Paskaidrojiet'), rownote=_points_2015, pages=(2, 3)),
    R('I4', [shown(_tick_2015(153, 156)), shown(_tick_2015(157, 163)),
             shown(J(_tick_2015(164, 165), L(170, 171))), shown(_tick_2015(172, 175))], whole=True,
      total=PY(4, 168), rownote=_points_2015, pages=(2, 3)),
    R('I5', [shown(_tick_2015(179, 181)), shown(_tick_2015(182, 184)), shown(_tick_2015(185, 186)),
             shown(_tick_2015(187, 189))], whole=True,
      total=PY(4, 251), rownote=_points_2015, pages=(2, 3)),
    R('I6', [shown(_tick_2015(193, 196)), shown(_tick_2015(197, 200)), shown(_tick_2015(201, 207)),
             shown(J(_tick_2015(208, 209), L(214, 215))), shown(_tick_2015(216, 218))], whole=True,
      total=PaperP(4, 'tekstā minētā'), rownote=_points_2015, pages=(2, 3)),
    R('II', [shown(_tick_2015(223, 227)), shown(_tick_2015(228, 231)), shown(_tick_2015(232, 237)),
             shown(_tick_2015(238, 243))], whole=True, rownote=_part2_2015, pages=(2, 3)),
    R('III1', [shown(L(247, 251))] + [shown(_tick_2015(a, b)) for a, b in
                                      ((252, 252), (257, 258), (259, 260), (261, 261), (262, 262), (263, 263),
                                       (264, 264), (265, 265), (266, 266), (267, 267), (268, 268))],
      whole=True, rownote=_title1_2015, question=QP(4, ESSAY_2015, '1. „Manas')),
    R('III2', [shown(_tick_2015(276, 281)), shown(_tick_2015(282, 286)), shown(_tick_2015(287, 294)),
               shown(J(_tick_2015(295, 298), L(303, 304))), shown(_tick_2015(305, 309))], whole=True,
      rownote=_title2_2015, question=QP(4, ESSAY_2015, '2. „Visbagātākais')),
]


# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2016-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits –
# 100", the instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y136-156); the title "Nenāc manā istabā, es nesaprotu latviski" (p2 y190),
# nine numbered paragraphs p2 y224 to p3 y738, the byline "Daiga Kamerāde,
# laikraksts “Ir”, 2015.gada 26.augusts." (p3 y750); p4 holds the questions:
# "I daļa (30 punkti)" (y63), Q1 "(5 punkti)" over a)-e) (live), Q2-Q6 "(5
# punkti)" each; "II daļa (30 punkti)" (y524), the commentary, ONE task with
# no number; "III daļa (40 punkti)" (y619), the instruction "Uzrakstiet
# pārspriedumu par vienu no tēmām! (ne mazāk kā 300 vārdu)" (y646) over two
# titles numbered "1." (y673) and "2." (y727-740), "Vai" between them.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "2. Paskaidrojiet ..." (p4 y241), Q3 "par mītnes zemes valodu?"
#   (y281), Q4 "4. Kā latvieši ..." (y308), Q5 "iespējām ārzemēs?" (y403):
#   "(5 punkti)" at the end of the question's own last line, PaperP.
# - Q6: "(5 punkti)" on a line of its own under the question (p4 x446 y484):
#   PY(4, 484).
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (144, 167).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-7 = printed pages 1-5; p2 the
# note to teachers; pp8-9 blank; each point under a check mark ✓, which the
# text layer reads as U+2713 and the selectors take off as a bullet):
# - Q2 (53 reprint): four points, 54, 55-56, 57-59, 60.
# - Q3 (61-62): four points, 63-66, 67-68, 69-70, 71-72.
# - Q4 (77): seven points, 78-79, 80, 81, 82, 83, 84, 85-86.
# - Q5 (87-92): four points, 93-96, 97-100, 101-103, 104-106.
# - Q6 (107-108 + 113-115, over the page break): seven points, 116-118,
#   119-124, 125-128, 129-130, 131-133, 134-136, 137-139.
# - Part II (144-146): six points, 147-150, 151-152, 153-155, 156-160,
#   161-163, 164-166.
# - Part III (167-168 the head and the instruction): under title 1 (169) nine
#   points, 170, 171, 172, 177-179, 180-181, 182-183, 184, 185, 186-187; title
#   2 (188-189) with nothing under it (rendered p7; pp8-9 blank).
#   No mark on any point, no criteria anywhere in this scheme.
# SHAPES:
# - I2-I6: points with no per-point mark: shown rows, whole=True on the
#   paper's printed 5 (10a).
# - II: six points, shown, whole=True on the paper's 30 (10a), labelled as
#   examples.
# - III1: nine points, shown, whole=True on the paper's 40 (10a), labelled as
#   examples.
# - III2: nothing printed under title 2 -> unprinted (ruling 4) at the
#   paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS (10f: the paper's words are the question; where the scheme
# rewords one, its reprint is quoted on the row's note):
# - Q6: the paper prints "Izskatiet savu viedokli par šo apgalvojumu, ..."
#   (p4 y457; rendered: "Izskatiet", the SEC's typing); the scheme reprints
#   "Izsakiet savu viedokli ..." (113-115). Quoted.
# - Part II: the paper prints "Latviešu valodas zināšanas ir ..." (p4 y551),
#   the scheme "Latviešu valodas zināšana ir ..." (145). Quoted.
# - Title 2's attribution: the paper prints "(Fintan O’’Toole, The Irish
#   Times, 22.02.2016)", the scheme "(Fintan O’ Toole, ...)" (189):
#   punctuation only, not quoted.
# - Q2's first point is printed without its opening quotation mark
#   ('English Latvian” ir latviešu ...', 54; rendered p3): lifted as printed.
# - III1's question: the instruction line and title 1 (the census carries
#   the "Vai" printed under the title); III2's the instruction and title 2's
#   two lines (the census gives the bare title).
# - Reading text: pp2-3 (rendered: title and paragraphs 1-4 on p2, 5-9 and
#   the byline on p3; p4 holds only the questions). The live Q1 card's
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Lifted as printed: "ir viena no nosacījumiem" (153),
# "saglābšana" (159), "runā Latviski" (164), "( piem.," (147).

ESSAY_2016 = 'Uzrakstiet pārspriedumu'


def _points_2016(d):
    return ('The scheme gives no mark to any of these points and does not say how many are wanted: '
            'shown as the scheme prints them, scored on the question\'s total.')


def _examples_2016(d):
    return ('The scheme prints these points with no mark on any of them and no criteria for the part: '
            'examples, not a checklist.')


def _title2_2016(d):
    return ('The scheme reprints the part\'s head, the instruction and both titles. It prints nine points '
            'under the first title and nothing under this one: no criteria, no descriptive line and no '
            'split of the part\'s marks.')


SPECS[2016] = [
    R('I2', [shown(S(54)), shown(L(55, 56)), shown(L(57, 59)), shown(S(60))], whole=True,
      total=PaperP(4, '2. Paskaidrojiet'), rownote=_points_2016, pages=(2, 3)),
    R('I3', [shown(L(63, 66)), shown(L(67, 68)), shown(L(69, 70)), shown(L(71, 72))], whole=True,
      total=PaperP(4, 'par mītnes zemes valodu?'), rownote=_points_2016, pages=(2, 3)),
    R('I4', [shown(L(78, 79)), shown(S(80)), shown(S(81)), shown(S(82)), shown(S(83)), shown(S(84)),
             shown(L(85, 86))], whole=True,
      total=PaperP(4, '4. Kā latvieši'), rownote=_points_2016, pages=(2, 3)),
    R('I5', [shown(L(93, 96)), shown(L(97, 100)), shown(L(101, 103)), shown(L(104, 106))], whole=True,
      total=PaperP(4, 'iespējām ārzemēs?'), rownote=_points_2016, pages=(2, 3)),
    R('I6', [shown(L(116, 118)), shown(L(119, 124)), shown(L(125, 128)), shown(L(129, 130)),
             shown(L(131, 133)), shown(L(134, 136)), shown(L(137, 139))], whole=True,
      total=PY(4, 484), pages=(2, 3),
      rownote=both(_points_2016, quote(J(S(113, after='Vilburs. '), S(114), S(115, before=' (5')),
                                       lead='The scheme reprints the instruction as'))),
    R('II', [shown(L(147, 150)), shown(L(151, 152)), shown(L(153, 155)), shown(L(156, 160)),
             shown(L(161, 163)), shown(L(164, 166))], whole=True, pages=(2, 3),
      rownote=both(_examples_2016, quote(S(145, before=' Izsakiet'), lead='The scheme reprints the statement as'))),
    R('III1', [shown(S(170)), shown(S(171)), shown(S(172)), shown(L(177, 179)), shown(L(180, 181)),
               shown(L(182, 183)), shown(S(184)), shown(S(185)), shown(L(186, 187))], whole=True,
      rownote=_examples_2016, question=QP(4, ESSAY_2016, '1. Kā es')),
    R('III2', [unprinted(_title2_2016)], question=QP(4, ESSAY_2016, Run('2. “Ja visi', 'var izrādīties'))),
]


# ====================================================================== 2017
# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2017-hl-i-1); not
# touched (audited: see latvian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits –
# 100", the instruction with the rule "... Visām atbildēm jābūt latviski."
# (p2 y116-160); the interview "Triju Zvaigžņu ordeņa un triju bērnu
# komandieris Jānis Mažeiks: „Kamēr cilvēkam ir gaiss, viņš to nepamana.”"
# (p2 y182-204), its text with line numbers in the left margin ("55", "60",
# "65"), p2 y226 to p3 y526, the byline "Krišs Kairis, AVĢ Lavīze" (p3 y540);
# "I daļa (30 punkti)" (p3 y591) and Q1 "(5 punkti)" over a)-e) on p3 (live);
# Q2-Q6 on p4, "(5 punkti)" each; "II daļa (30 punkti)" (p4 y415), the
# commentary, ONE task with no number; "III daļa (40 punkti)" (p4 y573), the
# instruction "Uzraksti pārspriedumu par vienu no tematiem! (ne mazāk kā 300
# vārdu)" (y605) over two titles numbered "1." (y636) and "2." (y700-723),
# "vai" between them.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 'bērnu komandieris”!' (p4 y80), Q4 "cilvēka dzīvi un karjeru!" (y197),
#   Q5 'saknes”?' (y263), Q6 "ņemot vērā, ..." (y327): "(5 punkti)" at the end
#   of the question's own last line, PaperP.
# - Q3: "(5 punkti)" on a line of its own under the question (p4 x489 y138):
#   PY(4, 138).
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (124, 135).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3, headed
# "Atbildes"; p2 the note to teachers; pp6-7 blank; answers in italics):
# - Q2 (59-60 reprint): an opening paragraph, 61-62 ("Trīs zvaigžņu ordeni
#   Latvijā piešķir ... šajā valstī."), four lettered points a)-d), 63-65,
#   66-68, 69-71, 72-73, and a closing paragraph set under them, 74-76
#   ("Fakti – virsraksts, teksta ievadā, ... kā pats uzskata par pareizu.").
# - Q3 (77-78): five lettered points a)-e), 79-80, 85-86 (p4), 87, 88-89,
#   90-91.
# - Q4 (92-93): five, 94, 95-96, 97-99, 100, 101.
# - Q5 (102-104): five, 105, 106, 107-108, 109-110, 111.
# - Q6 (112-113): two, 114-116, 117-119.
# - Part II (124-127 reprint the head and the task as the paper prints it):
#   two lettered points, 128-130, 131-134.
# - Part III (135-136 the head and the instruction): under title 1 (137) five
#   lettered points, 138-141, 142-147, 148-149, 150-152, 153-154; under title 2
#   (155) three, 156-158, 159-160, 161-163.
#   No mark on any point, no criteria anywhere in this scheme.
# SHAPES:
# - I2-I6: points (and Q2's two paragraphs) with no per-point mark: shown
#   rows, whole=True on the paper's printed 5 (10a).
# - II, III1, III2: the scheme's lettered points, shown, whole=True on the
#   paper's 30 / 40 (10a), labelled as examples.
# JUDGEMENT CALLS:
# - Each lettered point is cut after its own letter ("a) ", "b) ", ...): the
#   letter is the scheme's list marker, not answer text.
# - Q2's closing paragraph (74-76) says where in the text the facts are and
#   why he is "commander": scheme content under the question, so a shown row,
#   not a note.
# - III2: the scheme reprints title 2 without the paper's second line
#   ("Atklājiet šo tematu modernās pasaules un sociālo mediju lietošanas
#   kontekstā!", p4 y723); the question is the paper's two lines (10f), the
#   scheme rewords nothing it reprints, so nothing is quoted.
# - Questions: the census's text for I2-I6 and II (checked on the render; no
#   price); III1/III2 the instruction line and the title (the census gives
#   the titles alone).
# - Reading text: pp2-3 (rendered: title and the interview from p2 to the
#   byline on p3 y540, above "I daļa"). The live Q1 card's
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Printed as such on both documents (rendered): "viedoklļi" (title
# 2), "veidokli" (156), "pa nepieņemama" (147), "ārzemes" (151).

ESSAY_2017 = 'Uzraksti pārspriedumu'


def _pt_2017(a, b, letter):
    """A lettered point of the scheme, its letter ("a) ") cut off."""
    return shown(L(a, b, after=f'{letter}) '))


def _points_2017(d):
    return ('The scheme gives no mark to any of these points and does not say how many are wanted: '
            'shown as the scheme prints them, scored on the question\'s total.')


def _examples_2017(d):
    return ('The scheme prints these points with no mark on any of them and no criteria for the part: '
            'examples, not a checklist.')


SPECS[2017] = [
    R('I2', [shown(L(61, 62)), _pt_2017(63, 65, 'a'), _pt_2017(66, 68, 'b'), _pt_2017(69, 71, 'c'),
             _pt_2017(72, 73, 'd'), shown(L(74, 76))], whole=True,
      total=PaperP(4, 'bērnu komandieris'), rownote=_points_2017, pages=(2, 3)),
    R('I3', [_pt_2017(79, 80, 'a'), _pt_2017(85, 86, 'b'), _pt_2017(87, 87, 'c'), _pt_2017(88, 89, 'd'),
             _pt_2017(90, 91, 'e')], whole=True,
      total=PY(4, 138), rownote=_points_2017, pages=(2, 3)),
    R('I4', [_pt_2017(94, 94, 'a'), _pt_2017(95, 96, 'b'), _pt_2017(97, 99, 'c'), _pt_2017(100, 100, 'd'),
             _pt_2017(101, 101, 'e')], whole=True,
      total=PaperP(4, 'cilvēka dzīvi'), rownote=_points_2017, pages=(2, 3)),
    R('I5', [_pt_2017(105, 105, 'a'), _pt_2017(106, 106, 'b'), _pt_2017(107, 108, 'c'), _pt_2017(109, 110, 'd'),
             _pt_2017(111, 111, 'e')], whole=True,
      total=PaperP(4, 'saknes”?'), rownote=_points_2017, pages=(2, 3)),
    R('I6', [_pt_2017(114, 116, 'a'), _pt_2017(117, 119, 'b')], whole=True,
      total=PaperP(4, 'ņemot vērā'), rownote=_points_2017, pages=(2, 3)),
    R('II', [_pt_2017(128, 130, 'a'), _pt_2017(131, 134, 'b')], whole=True, rownote=_examples_2017,
      pages=(2, 3)),
    R('III1', [_pt_2017(138, 141, 'a'), _pt_2017(142, 147, 'b'), _pt_2017(148, 149, 'c'), _pt_2017(150, 152, 'd'),
               _pt_2017(153, 154, 'e')], whole=True, rownote=_examples_2017,
      question=QP(4, ESSAY_2017, '1. “Nākotnes')),
    # the scheme reprints the title without the paper's second sentence (second reader): quoted (10f)
    R('III2', [_pt_2017(156, 158, 'a'), _pt_2017(159, 160, 'b'), _pt_2017(161, 163, 'c')], whole=True,
      rownote=both(quote(S(155, after='2. '), lead='The scheme reprints this title as'), _examples_2017),
      question=QP(4, ESSAY_2017, '2. “Mans', 'Atklājiet šo tematu')),
]


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2018-hl-i-1); not
# touched (audited: see latvian-live-faults-2018-2026.json; no fault found).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits – 100",
# the instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y109-153); the title "Beznosacījuma stāstus meklējot" (p2 y197), nine
# numbered paragraphs p2 y219 to p3 y760 (an interview, no byline); p4 holds
# the questions: "I daļa (30 punkti)" (y65), Q1 "(5 punkti)" over a)-e)
# (live), Q2-Q6 "(5 punkti)" each; "II daļa (30 punkti)" (y491), the
# commentary, ONE task with no number ("Izsakiet savu viedokli par šo
# apgalvojumu! (vismaz 100 vārdu)" over the statement-question, y521-567);
# "III daļa (40 punkti)" (y614), the instruction "Uzrakstiet pārspriedumu par
# vienu no tematiem! (ne mazāk kā 300 vārdu)" (y638) over titles printed
# "1.“Tas ..." (y662) and "2.“Neskati ..." (y710-741), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2). The
# census text for I4 keeps the paper's "(5 punkti)." with the stop the paper
# sets AFTER the price (p4 y331), so the question is cut from the paper's
# lines here; III1's text ends with the "vai" printed under it.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "2. Paskaidrojiet ..." (p4 y243), Q3 'dzīvība.” (5 punkti)' (y288), Q4
#   "fragmentārajai pasaulei! (5 punkti)." (y331), Q6 "ceremoniju Latvijas
#   lepnums, ..." (y427): "(5 punkti)" at the end of the question's own last
#   line (rendered p4, right-hand column), PaperP.
# - Q5: "(5 punkti)" on a line of its own under the question (p4 x431 y383),
#   PY(4, 383).
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same "(5 punkti)" on each reprint, "(30
#   punkti)" (98) and "(40 punkti)" (105).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; p2 the
# note to teachers; pp5-6 blank; answers in italics under each reprint):
# - Q2 (61 reprint): one paragraph, 62-66. Q3 (67-68): one paragraph, 69-73.
#   Q4 (74-75): one paragraph, 76-80. Q5 (85): one paragraph, 86-91. Q6
#   (92-93): one paragraph, 94-97. No mark inside any answer.
# - Part II (98 the head; 99-100 reprint the task's second and third lines
#   only, with "(ap 100 vārdu)"): one italic paragraph, 101-104.
# - Part III (105 the head): title 1 with "(ne mazāk kā 300 vārdu)" (106) over
#   one italic paragraph, 107-108; "vai" (109); title 2 (110-112) over one
#   italic paragraph, 113-116.
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I2-I6: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - II: one paragraph of model content for a 30-mark commentary with no
#   criteria: shown, whole=True on the paper's 30 (10a; as 2013 II).
# - III1/III2: one paragraph of model content under each title, no criteria:
#   shown, whole=True on the paper's 40 (10a), labelled as an example.
# JUDGEMENT CALLS:
# - Part II (10f): the paper prints "Izsakiet savu viedokli par šo
#   apgalvojumu! (vismaz 100 vārdu)" over the task; the scheme reprints the
#   task alone with "(ap 100 vārdu)" (99-100). The paper's words are the
#   question (the census's text); the scheme's reprint quoted on the row.
# - Q2: the scheme's reprint ends "?" where the paper prints "!" (61);
#   punctuation only, not quoted. Q6's reprint differs in spacing only.
# - I4's question: the paper's two lines, the second cut before its price
#   (the census keeps "(5 punkti)." and the stop would be left standing).
# - III1/III2's questions: the instruction line and the title, the title's
#   printed number "1." / "2." (set without a space before the quotation mark,
#   which the marker reader does not take) cut off at its own anchor.
# - Reading text: pp2-3 (rendered: the title and paragraphs 1-5 on p2, 6-9 on
#   p3; p4 holds only the questions). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used (the only non-Latvian letters are the cover's á ú). Lifted as
# printed: "veiklāk pamanīt" (69), "viedo sižetus", "atzīsts" (78-79),
# "mazāk vērtīgāki" (77), "ieguldīs ... sasniegs" (107-108).

ESSAY_2018 = 'Uzrakstiet pārspriedumu'


def _part2_2018(d):
    return ('The scheme prints this one paragraph under the task, with no mark inside it and no criteria '
            f'for the part. It reprints the task as “{L(99, 100).text(d)}”')


def _essay_2018(d):
    return ('The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            'the part: an example, not a checklist.')


def _q4_2018(d, _q=None):
    return f"{PC(4, '4. Izmantojot', after='4. ').text(d)} {PC(4, 'fragmentārajai', before=' (5').text(d)}"


def _title1_2018(d, _q=None):
    return f"{PL(4, ESSAY_2018).text(d)} {PC(4, '1.“Tas', after='1.').text(d)}"


def _title2_2018(d, _q=None):
    return (f"{PL(4, ESSAY_2018).text(d)} {PC(4, '2.“Neskati', after='2.').text(d)} "
            f"{PL(4, 'par cilvēku pēc').text(d)} {PL(4, 'apgalvojuma patiesumu').text(d)}")


SPECS[2018] = [
    R('I2', [one(L(62, 66), PaperP(4, '2. Paskaidrojiet'))], total=PaperP(4, '2. Paskaidrojiet'), pages=(2, 3)),
    R('I3', [one(L(69, 73), PaperP(4, 'dzīvība.”'))], total=PaperP(4, 'dzīvība.”'), pages=(2, 3)),
    R('I4', [one(L(76, 80), PaperP(4, 'fragmentārajai'))], total=PaperP(4, 'fragmentārajai'), pages=(2, 3),
      question=_q4_2018),
    R('I5', [one(L(86, 91), PY(4, 383))], total=PY(4, 383), pages=(2, 3)),
    R('I6', [one(L(94, 97), PaperP(4, 'ceremoniju Latvijas'))], total=PaperP(4, 'ceremoniju Latvijas'),
      pages=(2, 3)),
    R('II', [shown(L(101, 104))], whole=True, rownote=_part2_2018, pages=(2, 3)),
    R('III1', [shown(L(107, 108))], whole=True, rownote=_essay_2018, question=_title1_2018),
    R('III2', [shown(L(113, 116))], whole=True, rownote=_essay_2018, question=_title2_2018),
]


# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2019-hl-i-1); not
# touched (audited: see latvian-live-faults-2018-2026.json; no fault found).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits – 100",
# the instruction with the rule "... Visām atbildēm jābūt latviski." (p2
# y141-155); the title "Arābs ar Daugavas asinīm" and "Fragments no
# intervijas ar Hosamu Abu Meri." (p2 y181-195), ten numbered paragraphs p2
# y217 to p3 y408, the byline "Pēteris Rudaks, „Diena”, 2007.gada septembris"
# (p3 y429); "I daļa (30 punkti)" (p3 y493), Q1 "(5 punkti)" over a)-e) (live)
# and Q2 on p3, Q3-Q6 on p4, "(5 punkti)" each; "II daļa (30 punkti)" (p4
# y369), the commentary, ONE task with no number; "III daļa (40 punkti)" (p4
# y514), the instruction "Uzrakstiet pārspriedumu par vienu no tēmām! (ne
# mazāk kā 300 vārdu)" (y543) over two titles numbered "1." (y585) and "2."
# (y643-672), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2). The
# census text for I1d is the expression alone, without the stem "Izskaidrojiet
# vārdus un frāzes!" the other letters carry (I1 is live, carded whole);
# III1's text ends with the "vai" printed under it.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "2. Kāpēc Abu Meri ... (5 punkti)" (p3 y726), Q3 "3. Par kādiem ..."
#   (p4 y64), Q5 "apgalvojumu! (5 punkti)" (p4 y211), Q6 "atbildība? (5
#   punkti)" (p4 y283): the price at the end of the question's own last line,
#   PaperP.
# - Q4: "(5 punkti)" on a line of its own under the question (p4 x89 y137),
#   PY(4, 137).
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (101, 115).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2; p2 the
# note to teachers; pp5-6 blank; each point opens with a check mark ✓, which
# the text layer reads as U+2713 and the selectors take off as a bullet):
# - Q2 (59 reprint): four points, 60-61, 62, 63, 64.
# - Q3 (65): three points, 66-67, 68, 69.
# - Q4 (70-71): two points, 72, 73-76.
# - Q5 (77-78): three points, 83-85, 86-88, 89-90 (p4).
# - Q6 (91-92): four points, 93-94, 95-97, 98, 99-100.
#   No mark on any point, none says how many are wanted.
# - Part II (101-104 reprint the head and the task as the paper prints it):
#   four points, 105-108, 109-110, 111-112, 113-114.
# - Part III (115-120): the head, the instruction, both titles and "vai" --
#   and nothing under them (rendered p4; pp5-6 blank). NO criteria anywhere in
#   this scheme.
# SHAPES:
# - I2-I6: points with no per-point mark: shown rows, whole=True on the
#   paper's printed 5 (10a).
# - II: four points, shown, whole=True on the paper's 30 (10a), labelled as
#   examples.
# - III1/III2: nothing printed under the titles -> unprinted (ruling 4) at
#   the paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS:
# - Part II's second point runs over a line that opens with a dash, "– tā ir
#   viņa identitāte." (110, rendered p4): the dash is printed inside the
#   sentence, so line 110 is lifted raw (SR), keeping it.
# - Q2's first point and Q4's second carry the text's own quotations,
#   lifted as printed.
# - III2's title: the paper prints "... noderīgi vai laika tērēšana”. / Lūdzu
#   analizējiet abus aspektus!" (p4 y643-672); the scheme reprints the second
#   line as "Lūdzu analizējiet abus aspektus!”." (120): punctuation only, not
#   quoted.
# - Questions: the census's text for I2-I6 and II (checked on the render; no
#   price); III1/III2 the instruction line and the title (III1's census text
#   carries the "vai", III2's is the bare title).
# - Reading text: pp2-3 (rendered: title and paragraphs 1-6 on p2, 7-10 and
#   the byline on p3 above "I daļa"). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Lifted as printed: "iegūstos pilsonību" (93), "latviešu valdu"
# (106), "sajūtas vairāk piederīgs" (live Q1 row, 57).

ESSAY_2019 = 'Uzrakstiet pārspriedumu'


def _points_2019(d):
    return ('The scheme gives no mark to any of these points and does not say how many are wanted: '
            'shown as the scheme prints them, scored on the question\'s total.')


def _examples_2019(d):
    return ('The scheme prints these points with no mark on any of them and no criteria for the part: '
            'examples, not a checklist.')


def _essay_2019(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria, no descriptive line and no split of the part\'s marks.')


SPECS[2019] = [
    R('I2', [shown(L(60, 61)), shown(S(62)), shown(S(63)), shown(S(64))], whole=True,
      total=PaperP(3, '2. Kāpēc'), rownote=_points_2019, pages=(2, 3)),
    R('I3', [shown(L(66, 67)), shown(S(68)), shown(S(69))], whole=True,
      total=PaperP(4, '3. Par kādiem'), rownote=_points_2019, pages=(2, 3)),
    R('I4', [shown(S(72)), shown(L(73, 76))], whole=True,
      total=PY(4, 137), rownote=_points_2019, pages=(2, 3)),
    R('I5', [shown(L(83, 85)), shown(L(86, 88)), shown(L(89, 90))], whole=True,
      total=PaperP(4, 'apgalvojumu!'), rownote=_points_2019, pages=(2, 3)),
    R('I6', [shown(L(93, 94)), shown(L(95, 97)), shown(S(98)), shown(L(99, 100))], whole=True,
      total=PaperP(4, 'atbildība?'), rownote=_points_2019, pages=(2, 3)),
    R('II', [shown(L(105, 108)), shown(J(S(109), SR(110))), shown(L(111, 112)), shown(L(113, 114))],
      whole=True, rownote=_examples_2019, pages=(2, 3)),
    R('III1', [unprinted(_essay_2019)], question=QP(4, ESSAY_2019, '1. „Ko')),
    R('III2', [unprinted(_essay_2019)], question=QP(4, ESSAY_2019, '2. „Brīvs', 'Lūdzu analizējiet')),
]


# ====================================================================== 2020
# ================================================================ 2020 HL ===
# Drafted (small-languages lane, 20 Nov): the nine open asks of this sitting,
# I1 (Q1 whole), I2-I6, II, III1, III2. No live card in this sitting.
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits – 100"
# and the instruction with the rule "... Visām atbildēm jābūt latviski." (p2);
# the interview text, seven numbered questions with their answers, p2 to p3
# y549, the byline "Marta Sondare, „Diena”, 2007.gada 5.marts" (p3 y561); "I
# daļa (30 punkti)" (p3 y597), Q1 "1. Izskaidrojiet vārdus un vārdu
# savienojumus! (5 punkti)" (p3 y641) over a)-e) with NO price of their own
# (y670-758); Q2-Q6 on p4, "(5 punkti)" each; "II daļa (30 punkti)" (p4
# y392), the commentary, ONE task with no number; "III daļa" (p4 y526) with NO
# total on its head: "(40 punkti)" is printed at the end of the instruction
# line under it, "Uzrakstiet pārspriedumu par vienu no tēmām! (ne mazāk kā 300
# vārdu) (40 punkti)" (y560); two UNNUMBERED titles, '"Katrs pats savas laimes
# kalējs." (Latviešu sakāmvārds)' (y592) and "Uzrakstiet, kādi pasākumi, ..."
# (y659), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2); III1's
# census text is the instruction (with its price) and title 1, III2's the bare
# title 2.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q1: "(5 punkti)" on the stem's own line (p3 y641), the expressions
#   unpriced: Q1 carded WHOLE at 'I1' (as the live Latvian Q1 cards and
#   Romanian 2010-2019), PaperP on the stem.
# - Q2 "2. Kāpēc Ēriks ..." (p4 y82), Q3 "3. Miniet ..." (y132), Q6
#   "izdosies sasniegt savu mērķi? ..." (y312): the price at the end of the
#   question's own last line, PaperP.
# - Q4, Q5: "(5 punkti)" on a line of its own under the question (p4 x482 y198
#   and y253): two lines of p4 open "(5 punkti)", so each is read at its own
#   height, PY(4, 198), PY(4, 253).
# - II: "II daļa (30 punkti)" (PARTP). III1/III2: the "(40 punkti)" on the
#   instruction line (PaperP; PARTP finds no total on "III daļa"). The scheme
#   sets them the same way (90; 98-99).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3, headed
# "ATBILDES"; p2 the note to teachers; pp6-7 blank):
# - Q1 (50): a)-e), each the expression, a dash and its gloss in italics:
#   51-52, 53-54, 55, 56, 57. No mark on any.
# - Q2 (58 reprint, no price): one paragraph, 59-60. Q3 (61): one paragraph,
#   62-63. Q5 (68): one paragraph, 69-75.
# - Q4 (64): TWO paragraphs (rendered p3: line 66 ends short at "stāstus.",
#   "Lektoram iespējams ..." opens the next line): 65-66 and 67.
# - Q6 (80-81, p4): TWO paragraphs (line 84 ends short at "kā tas
#   atrisināt."): 82-84 and 85-89.
#   No mark inside any answer.
# - Part II (90-92 reprint the head and the task): one italic paragraph,
#   93-97.
# - Part III (98-99 the head and the instruction): under title 1 (100) one
#   italic paragraph, 101-106; under title 2 (111, p5) "Jebkura loģiska
#   argumentēta atbilde." (112) over four ✓ points, 113, 114, 115-116, 117.
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I1: five glosses with no mark of their own under a question priced as a
#   whole: five shown rows, whole=True on the paper's 5, each row led by the
#   expression as the paper prints it.
# - I2, I3, I5: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I4, I6: two paragraphs each: shown rows, whole=True on the printed 5.
# - II: one model paragraph, no criteria: shown, whole=True on the paper's 30
#   (10a).
# - III1: one model paragraph: shown, whole=True on the paper's 40 (10a).
# - III2: four points under the scheme's own line "Jebkura loģiska
#   argumentēta atbilde.": shown, whole=True on the paper's 40; that line is
#   quoted on the note, not a row (it says what is accepted, it is not
#   content).
# JUDGEMENT CALLS (10f: the paper's words are the question; where the scheme
# rewords one, its reprint is quoted on the row's note):
# - Q1 a): the paper prints "lektori (1.rinkopa)" (sic), the scheme glosses
#   "lektors" (51). Quoted on the first row.
# - Q3: the paper prints "Miniet trīs kritērijus, kādus projekta autori
#   ..."; the scheme reprints "kādu" (61). Quoted. The answer is one
#   paragraph naming the three criteria in three sentences with no mark on
#   any: one claimable row on the convention. Flip to three shown rows
#   (whole=True) only if the lead reads the sentences as the scheme's points.
# - III2: the paper prints "... Jūsuprāt, Latvijā būtu jāveic, ..."; the
#   scheme reprints "... Jūsuprāt, būtu Latvijā būtu jāveic, ..." (111).
#   Quoted.
# - I4 and I6 split at the scheme's own paragraph ends (a short last line,
#   the next sentence on a new line); if the lead reads either as one
#   paragraph, flip to one(...). III1's line 104 runs to the right margin, so
#   "Vai es esmu laimīgs? ..." (105) continues the same paragraph.
# - III1's question is the census's text (the instruction, its price taken
#   off, and title 1); III2's the instruction line and title 2.
# - Reading text: pp2-3 (rendered: the text from p2 to the byline at p3 y561,
#   Q1 below it on p3). No live card to compare.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Printed as such: "Rosinātāvā" and "uzkata" (Q2, paper and
# scheme), "1.rinkopa" (paper). Lifted as printed: "drabieki" (70), "kaut
# kaut ko" (94), "mudina mudina" (88), "savus mērķu" (88), "Personiskajās
# attiecības" (105).

Q1P_2020 = PaperP(3, '1. Izskaidrojiet')
ESSAY_2020 = 'Uzrakstiet pārspriedumu'
REPRINT = 'The scheme reprints this question as'


def _q1_2020(d):
    return (f'The scheme glosses expression a) as “{S(51, after="a) ", before=" –").text(d)}”; the paper prints '
            f'“{PC(3, "a) lektori", after="a) ").text(d)}”. Each gloss carries no mark of its own: the paper prices '
            f'the question as a whole.')


def _part2_2020(d):
    return ('The scheme prints this one paragraph under the statement, with no mark inside it and no criteria '
            'for the part.')


def _title1_2020(d):
    return ('The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            'the part: an example, not a checklist.')


def _title2_2020(d):
    return (f'The scheme reprints this title as “{S(111, after="2. ").text(d)}” Under it it prints '
            f'“{S(112).text(d)}” and these points, with no mark on any of them and no criteria for the part: '
            f'examples, not a checklist.')


SPECS[2020] = [
    R('I1', [shown(L(51, 52, after='– '), lead=PC(3, 'a) lektori', after='a) ')),
             shown(L(53, 54, after='– '), lead=PC(3, 'b) ambīcijas', after='b) ')),
             shown(S(55, after='– '), lead=PC(3, 'c) aplauzties', after='c) ')),
             shown(S(56, after='– '), lead=PC(3, 'd) dūša', after='d) ')),
             shown(S(57, after='– '), lead=PC(3, 'e) vakances', after='e) '))],
      whole=True, total=Q1P_2020, rownote=_q1_2020, pages=(2, 3),
      question=QL(3, '1. Izskaidrojiet', 'a) lektori', 'b) ambīcijas', 'c) aplauzties', 'd) dūša', 'e) vakances')),
    R('I2', [one(L(59, 60), PaperP(4, '2. Kāpēc'))], total=PaperP(4, '2. Kāpēc'), pages=(2, 3)),
    R('I3', [one(L(62, 63), PaperP(4, '3. Miniet'))], total=PaperP(4, '3. Miniet'), pages=(2, 3),
      rownote=quote(S(61, after='3. '), lead=REPRINT)),
    R('I4', [shown(L(65, 66)), shown(S(67))], whole=True, total=PY(4, 198), pages=(2, 3)),
    R('I5', [one(L(69, 75), PY(4, 253))], total=PY(4, 253), pages=(2, 3)),
    R('I6', [shown(L(82, 84)), shown(L(85, 89))], whole=True, total=PaperP(4, 'izdosies sasniegt'), pages=(2, 3)),
    R('II', [shown(L(93, 97))], whole=True, rownote=_part2_2020, pages=(2, 3)),
    R('III1', [shown(L(101, 106))], whole=True, total=PaperP(4, ESSAY_2020), rownote=_title1_2020),
    R('III2', [shown(S(113)), shown(S(114)), shown(L(115, 116)), shown(S(117))], whole=True,
      total=PaperP(4, ESSAY_2020), rownote=_title2_2020, question=QP(4, ESSAY_2020, 'Uzrakstiet, kādi')),
]


# ====================================================================== 2021
# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, Q1
# (as its five lettered expressions, I1a-I1e), I2-I6, II1, II2. No live card
# in this sitting.
# TWO-PART sitting: the instruction "... atbildiet uz pirmās un otrās daļas
# jautājumiem! ..." (p2 y65), "I daļa (30 punkti)" (p2 y153) and "II daļa (40
# punkti)" (p4 y356), the essay; no commentary. Keys II1/II2 are the essay's
# two titles (ruling B), cited Section II Q1/Q2.
# Paper (rendered pp2-4): the reading text (Oto Brantevics and the film
# "Dvēseļu putenis"), nine numbered paragraphs p2 to p3 y515, the byline "Laura
# Dumbere, „IR”, 2019. gada 6.novembris" (p3 y528); "Atbildiet uz
# jautājumiem!" (p3 y582) and Q1 "1. Izskaidrojiet vārdus un vārdu
# savienojumus! (5 × 1 punkti)" (p3 y604) over a)-e); Q2-Q6 on p4, each
# priced "(5)"; Part II the instruction "Uzrakstiet pārspriedumu par vienu no
# tēmām! (ne mazāk kā 300 vārdu)" (y386) over two titles numbered "1." (y429)
# and "2." (y513), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II1, II2).
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q1: the paper prints "(5 × 1 punkti)" on the stem's line (rendered p3,
#   right-hand column): one mark for EACH expression, so Q1 is carded per
#   letter (the brief: "if the paper prints per-expression marks that add to
#   the whole, card per letter"; live 2023/2024 Q1 the precedent), each at the
#   "1 punkti" PaperP reads off that line. The scheme prints "(5 punkti)" for
#   the question (50), the same total.
# - Q2 "... “Dvēseļu putenis”? (5)" (p4 y65), Q3 "... par vīrieti! (5)"
#   (y109), Q4 "īstenojās? (5)" (y168), Q5 "... filmēšanas laikā? (5)"
#   (y212), Q6 "cilvēkiem, bet ļoti smags, svarīgs darbs”! (5)" (y270): a bare
#   "(5)" at the end of the question's own last line, PaperP.
# - II1/II2: "II daļa (40 punkti)" (PARTP, 40). The scheme prints the same
#   (110).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3, headed
# "ATBILDES"; pp6-7 blank; answers in italics):
# - Q1 (50): each expression with its paragraph reference on one line and its
#   gloss in italics on the next: 52, 54, 56, 58, 60. No mark on any.
# - Q2 (61 reprint): one paragraph, 62-67.
# - Q3 (68): FOUR paragraphs, 69-73 (its last line short at the foot of p3),
#   78-79, 80-82, 83 (p4; each a new line after a short one).
# - Q4 (84-85): TWO paragraphs, 86-88 and 89-91 (a blank line between).
# - Q5 (92): one paragraph, 93-96.
# - Q6 (97-98): THREE paragraphs, 99-100, 101-103, 104-105.
#   No mark inside any answer.
# - Part II (110-111, p5, the head and the instruction): under title 1 (112)
#   one italic paragraph, 113-117; under title 2 (118) one italic paragraph,
#   119-121, ending with the bracketed instruction "(Skolēnu atbildēs jābūt
#   konkrētiem piemēriem.)".
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I1a-I1e: one stated gloss each: ONE claimable row at the paper's 1.
# - I2, I5: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I3, I4, I6: several paragraphs: shown rows, whole=True on the printed 5.
# - II1/II2: one model paragraph under each title, no criteria: shown,
#   whole=True on the paper's 40 (10a), labelled as an example.
# JUDGEMENT CALLS:
# - Q1 per letter, not whole: the paper prices each expression ("5 × 1"). If
#   the lead keeps Q1 whole at the parent (the exclusions list "2021 HL
#   Section I Q1" whole), the same rows go shown on R('I1', ..., whole=True,
#   total=PaperP(3, '1. Izskaidrojiet')) -- which would read 1, not 5: then
#   use SP(50).
# - II2: the bracketed line closing the scheme's paragraph, "(Skolēnu atbildēs
#   jābūt konkrētiem piemēriem.)" (120-121), tells the examiner what answers
#   must hold; it is cut off the row (at the row's end) and quoted on the note.
# - II2 (10f, punctuation only): the paper prints '... nepatīk.” - Grēta
#   Tūnberga', the scheme '... nepatīk.” (Grēta Tūnberga)' (118): not quoted.
# - Q4: the scheme's reprint drops the comma before "un vai" (84): not quoted.
# - Questions: the census's text for I1a-e and I2-I6 (checked on the render;
#   no price); II1/II2 the instruction line and the title.
# - No `pages` on II1/II2: a two-part sitting's Part II is the essay. Part I
#   pages (2, 3): the text from p2 to its byline at p3 y528, Q1 below it on
#   p3; Q2-Q6 on p4.
# GLYPHS: none (U+00A0 spaces in the scheme read as spaces); ā č ē ģ ī ķ ļ ņ
# š ū ž read as the render shows them in every line used. Lifted as printed:
# "atbilda šīm tēlam" (64), "Filmēšanā prasa" (99), "būtu būtu" (paper p3
# y442, not lifted).

ESSAY_2021 = 'Uzrakstiet pārspriedumu'
Q1P_2021 = PaperP(3, '1. Izskaidrojiet')


def _points_2021(d):
    return ('The scheme prints these paragraphs under the question, with no mark on any of them: shown as '
            'the scheme prints them, scored on the question\'s total.')


def _title1_2021(d):
    return ('The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            'the part: an example, not a checklist.')


def _title2_2021(d):
    return (f'The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            f'the part: an example, not a checklist. It closes it with “{L(120, 121, after="labu.").text(d)}”')


SPECS[2021] = [
    R('I1a', [one(S(52), Q1P_2021)], total=Q1P_2021, pages=(2, 3)),
    R('I1b', [one(S(54), Q1P_2021)], total=Q1P_2021, pages=(2, 3)),
    R('I1c', [one(S(56), Q1P_2021)], total=Q1P_2021, pages=(2, 3)),
    R('I1d', [one(S(58), Q1P_2021)], total=Q1P_2021, pages=(2, 3)),
    R('I1e', [one(S(60), Q1P_2021)], total=Q1P_2021, pages=(2, 3)),
    R('I2', [one(L(62, 67), PaperP(4, '2. Kāpēc'))], total=PaperP(4, '2. Kāpēc'), pages=(2, 3)),
    R('I3', [shown(L(69, 73)), shown(L(78, 79)), shown(L(80, 82)), shown(S(83))], whole=True,
      total=PaperP(4, '3. Pamatojiet'), rownote=_points_2021, pages=(2, 3)),
    R('I4', [shown(L(86, 88)), shown(L(89, 91))], whole=True, total=PaperP(4, 'īstenojās?'),
      rownote=_points_2021, pages=(2, 3)),
    R('I5', [one(L(93, 96), PaperP(4, '5. Kā'))], total=PaperP(4, '5. Kā'), pages=(2, 3)),
    R('I6', [shown(L(99, 100)), shown(L(101, 103)), shown(L(104, 105))], whole=True,
      total=PaperP(4, 'cilvēkiem, bet ļoti'), rownote=_points_2021, pages=(2, 3)),
    R('II1', [shown(L(113, 117))], whole=True, total=PARTP(), rownote=_title1_2021,
      question=QP(4, ESSAY_2021, '1. "Es neesmu')),
    R('II2', [shown(L(119, 120, before=' (Skolēnu'))], whole=True, total=PARTP(), rownote=_title2_2021,
      question=QP(4, ESSAY_2021, '2. “Fakti')),
]


# ====================================================================== 2022
# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I2-I6, II1, II2. Live: I1 (Q1 carded whole, lv-2022-hl-i-1); not touched
# (audited: see latvian-live-faults-2018-2026.json: its first two rows are in
# the scheme's order, which swaps a) and b)).
# TWO-PART sitting: "Maksimālais punktu skaits – 70" (p2 y91), "I daļa (30
# punkti)" (p2 y118) and "II daļa (40 punkti)" (p4 y509), the ESSAY
# ("Uzrakstiet pārspriedumu par vienu no tēmām! (ne mazāk kā 300 vārdu)",
# y556, over two titles numbered "1." (y596) and "2." (y694), "Vai" between
# them); no commentary. The exclusions file calls II1/II2 a "commentary":
# wrong, both are essay titles (rendered p4). Keys II1/II2, cited Section II
# Q1/Q2 (ruling B).
# Paper (rendered pp2-4): the instruction with the rule "... Visām atbildēm
# jābūt latviski!" (p2 y64-78); the interview "Kristaps Liepiņš: Virsotne ir
# tikai pusceļš" (p2 y185), fifteen numbered paragraphs p2 y212 to p3 y751,
# the byline "Kaspars Ozols .Intervija portālam tvnet.lv, 2020.gada
# 9.februāris" (p3 y764); p4 holds the questions: "Atbildiet uz jautājumiem!
# (5 × 1 punkts)" (y80) over Q1 a)-e) (live); Q2-Q6 each priced "(5)".
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II1, II2).
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q3 "3. Kuri klienti, ... un kāpēc? (5)" (p4 y309), Q4 "nepieciešamas
#   alpīnistam? (5)" (y355), Q5 "Vai grūtību pārvarēšana ir tā vērtas? ...
#   (5)" (y401), Q6 "viedokli par šo apgalvojumu, ... (5)" (y448): a bare "(5)"
#   at the end of the question's own last line, PaperP.
# - Q2: "(5)" on a line of its own under the question (p4 x510 y278), the only
#   line of p4 opening "(5)": PaperP(4, '(5)') (PY reads only a worded cell).
# - II1/II2: "II daļa (40 punkti)" (PARTP, 40). The scheme prints the same
#   (194).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-7 = printed pages 1-5; pp8-9
# blank): it REPRINTS THE WHOLE READING TEXT first (51-143), then Q1 (144-150,
# live), then each question with its answer in italics:
# - Q2 (151-152 reprint, "(5)"): one paragraph, 153-157.
# - Q3 (162): one paragraph, 163-167.
# - Q4 (168-169): TWO paragraphs, 170-173 and 174-175 (rendered p6: line 173
#   ends short at "nepiesārņot vidi.", "Alpīnistam jābūt ..." opens the next).
# - Q5 (176-177): TWO paragraphs, 178-181 and 182-183 (line 181 short).
# - Q6 (184-185): one paragraph, 186-189.
#   No mark inside any answer.
# - Part II (194-198, p7): the head, the instruction, both titles and "Vai" --
#   and nothing under them (rendered p7; pp8-9 blank). NO criteria anywhere in
#   this scheme.
# SHAPES:
# - I2, I3, I6: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I4, I5: two paragraphs each: shown rows, whole=True on the printed 5.
# - II1/II2: nothing printed under the titles -> unprinted (ruling 4) at the
#   paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS (10f: the paper's words are the question; where the scheme
# rewords one, its reprint is quoted on the row's note):
# - Q5: the paper prints "Vai grūtību pārvarēšana ir tā vērtas?" (p4 y401);
#   the scheme reprints "Vai šīs sajūtas ir grūtību pārvarēšanas vērtas?"
#   (176-177). Quoted.
# - Q2-Q4, Q6: the scheme's reprints differ in spacing or a space after the
#   closing quotation mark only; not quoted.
# - I4, I5 split at the scheme's own paragraph ends; if the lead reads either
#   as one paragraph, flip to one(...).
# - Questions: the census's text for I2-I6 (checked on the render; no price;
#   Q6 keeps the paper's "dzīves.”Izsakiet" with no space, as printed); II1/II2
#   the instruction line and the title.
# - No `pages` on II1/II2 (the essay). Part I pages (2, 3): the text from p2 to
#   its byline at p3 y764; p4 holds only the questions. The live Q1 card's
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none (U+00A0 spaces in the scheme read as spaces; U+2010 "‐" is the
# SEC's own hyphen glyph, printed as a dash in the text and in Q1, rendered
# p5); ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every line used.
# Lifted as printed: "Jau bērnība", "Avairs Bojārs" (153-154), "radīju"
# (157), "K.Liepinā", "paišiem" (163), "pārvarēti sevi" (146, live).

ESSAY_2022 = 'Uzrakstiet pārspriedumu'


def _essay_2022(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria, no descriptive line and no split of the part\'s marks.')


def _paras_2022(d):
    return ('The scheme prints these paragraphs under the question, with no mark on any of them: shown as '
            'the scheme prints them, scored on the question\'s total.')


SPECS[2022] = [
    R('I2', [one(L(153, 157), PaperP(4, '(5)'))], total=PaperP(4, '(5)'), pages=(2, 3)),
    R('I3', [one(L(163, 167), PaperP(4, '3. Kuri'))], total=PaperP(4, '3. Kuri'), pages=(2, 3)),
    R('I4', [shown(L(170, 173)), shown(L(174, 175))], whole=True, total=PaperP(4, 'nepieciešamas alpīnistam'),
      rownote=_paras_2022, pages=(2, 3)),
    R('I5', [shown(L(178, 181)), shown(L(182, 183))], whole=True, total=PaperP(4, 'Vai grūtību'), pages=(2, 3),
      # the whole reprint, its "Paskaidro, kāpēc jā vai kāpēc ne!" included (second reader)
      rownote=both(_paras_2022, quote(L(176, 177, after='5. ', before=' (5)'),
                                      lead='The scheme reprints this question as'))),
    R('I6', [one(L(186, 189), PaperP(4, 'viedokli par šo'))], total=PaperP(4, 'viedokli par šo'), pages=(2, 3)),
    R('II1', [unprinted(_essay_2022)], total=PARTP(), question=QP(4, ESSAY_2022, '1. “Mani')),
    R('II2', [unprinted(_essay_2022)], total=PARTP(), question=QP(4, ESSAY_2022, '2. Kā rodas')),
]


# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the nine open asks of this sitting,
# I1b, I2-I6, II, III1, III2. Live: I1a, I1c, I1d, I1e (Q1 carded per letter at
# 1 each); not touched (audited: see latvian-live-faults-2018-2026.json:
# lv-2023-hl-i-1-e splits its one gloss into two "alternatives").
# Paper (rendered pp2-4): the instruction with the rule "... Visām atbildēm
# jābūt latviski!" (p2 y65-80); the interview lead-in on Bob Hartley and the
# Latvian ice-hockey team (y109-124), ten numbered paragraphs p2 y143 to p3
# y651 (no byline); p4 holds the questions: "Atbildiet uz
# visiem jautājumiem, ..." (y65), "I daļa (30 punkti)" (y108), Q1 "1.
# Izskaidrojiet vārdu savienojumus un frāzes!" (y159) over a)-e), "(5 × 1
# punkti)" at the end of e)'s line (y246); Q2-Q6 each priced "(5)"; "II daļa
# (30 punkti)" (y522), the commentary, ONE task with no number; "III daļa (40
# punkti)" (y640), the instruction "Uzrakstiet pārspriedumu par vienu no
# tēmām! (ne mazāk kā 300 vārdu)" (y663) over two titles numbered "1." (y692)
# and "2." (y744), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2); III1's
# census text ends with the "vai" printed under it.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q1(b): the paper's "(5 × 1 punkti)" (p4 y246, on e)'s line): one mark for
#   each expression, as the live a), c)-e) cards read it; PaperP on e)'s line
#   reads the "1 punkti".
# - Q2 "mērķis? (5)" (y297), Q3 "3. Raksturojiet ... (5)" (y324), Q4 "komanda
#   neizcīna titulu”? (5)" (y368), Q5 "spēlētājiem gan laukumā, gan
#   ģērbtuvēs? (5)" (y411), Q6 "nepiekrītat? (5)" (y472): a bare "(5)" at the
#   end of the question's own last line, PaperP.
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints the same (99, 110).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; pp6-7
# blank; answers in plain type under each reprint):
# - Q1 (47): each expression, a dash and its gloss on one line, 48-54; b) is
#   "b) saliedēt komandu –vienot" (49): the gloss "vienot" set straight after
#   the dash with no space (rendered p3). The exclusions file says "the scheme
#   states no answer for this ask, only its price": wrong, it prints "vienot".
# - Q2 (55-56 reprint): one paragraph, 57-60.
# - Q3 (61): TWO paragraphs, 62-64 and 65-68 (a gap between, rendered p3).
# - Q4 (69-70): one paragraph running over the p3/p4 break, 71-73 and 78-79
#   (74-76 the page number and the page head, left out).
# - Q5 (80-81): FOUR paragraphs, 82-84, 85-86, 87-88, 89-90 (gaps between,
#   rendered p4).
# - Q6 (91-93): one paragraph, 94-98.
#   No mark inside any answer.
# - Part II (99-101 reprint the head, the instruction and the statement): one
#   paragraph, 102-105.
# - Part III (110-111, p5, the head and the instruction): under title 1 (112)
#   one paragraph, 113-116, saying what the student writes about; "vai"
#   (117); under title 2 (118) one paragraph, 119-122.
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I1b: one stated gloss: ONE claimable row at the paper's 1, as the live
#   a), c)-e) cards.
# - I2, I4, I6: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I3, I5: several paragraphs: shown rows, whole=True on the printed 5.
# - II: one model paragraph, no criteria: shown, whole=True on the paper's 30
#   (10a).
# - III1/III2: one paragraph of indicative content under each title, no
#   criteria: shown, whole=True on the paper's 40 (10a), labelled as an
#   example.
# JUDGEMENT CALLS:
# - I4's row joins its paragraph over the page break (J of 71-73 and 78-79),
#   as Czech 2021 Q4 and Latvian 2015 Q4: one paragraph on the render.
# - The scheme's reprints differ from the paper in spacing only ("B.  Hārtlijs
#   raksturo", "(100 ‐ 150 vārdu)" with the SEC's hyphen glyph); not quoted.
# - Questions: the census's text for I1b and I2-II (checked on the render; no
#   price; Q6 keeps the paper's "Boba Hārlija", as printed); III1/III2 the
#   instruction line and the title.
# - Reading text: pp2-3 (rendered: the lead-in and paragraphs 1-5 on p2, 6-10
#   on p3 to y651; p4 holds only the questions). The live Q1 cards'
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none (U+00A0 spaces in the scheme read as spaces; U+2010 "‐" is the
# SEC's hyphen glyph, rendered as a dash); ā č ē ģ ī ķ ļ ņ š ū ž read as the
# render shows them in every line used. Lifted as printed: "trieks bortā"
# (59), "augstākā kaluma" (60), "ka uzvarēt" (78), "uzturēto" (89), "Izcilība
# sasniedzam" (97), "B. Hartlijs" (87).

ESSAY_2023 = 'Uzrakstiet pārspriedumu'


def _paras_2023(d):
    return ('The scheme prints these paragraphs under the question, with no mark on any of them: shown as '
            'the scheme prints them, scored on the question\'s total.')


def _part2_2023(d):
    return ('The scheme prints this one paragraph under the statement, with no mark inside it and no criteria '
            'for the part.')


def _essay_2023(d):
    return ('The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            'the part: an example, not a checklist.')


Q1P_2023 = PaperP(4, 'e) panākumu')

SPECS[2023] = [
    R('I1b', [one(S(49, after='–'), Q1P_2023)], total=Q1P_2023, pages=(2, 3)),
    R('I2', [one(L(57, 60), PaperP(4, 'mērķis?'))], total=PaperP(4, 'mērķis?'), pages=(2, 3)),
    R('I3', [shown(L(62, 64)), shown(L(65, 68))], whole=True, total=PaperP(4, '3. Raksturojiet'),
      rownote=_paras_2023, pages=(2, 3)),
    R('I4', [one(J(L(71, 73), L(78, 79)), PaperP(4, 'komanda neizcīna'))], total=PaperP(4, 'komanda neizcīna'),
      pages=(2, 3)),
    R('I5', [shown(L(82, 84)), shown(L(85, 86)), shown(L(87, 88)), shown(L(89, 90))], whole=True,
      total=PaperP(4, 'spēlētājiem gan laukumā'), rownote=_paras_2023, pages=(2, 3)),
    R('I6', [one(L(94, 98), PaperP(4, 'nepiekrītat?'))], total=PaperP(4, 'nepiekrītat?'), pages=(2, 3)),
    R('II', [shown(L(102, 105))], whole=True, rownote=_part2_2023, pages=(2, 3)),
    R('III1', [shown(L(113, 116))], whole=True, rownote=_essay_2023, question=QP(4, ESSAY_2023, '1. “Personības')),
    R('III2', [shown(L(119, 122))], whole=True, rownote=_essay_2023, question=QP(4, ESSAY_2023, '2. “Ir katram')),
]


# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the nine open asks of this sitting,
# I1b, I2-I6, II, III1, III2. Live: I1a, I1c, I1d, I1e (Q1 carded per letter at
# 1 each); not touched (audited: see latvian-live-faults-2018-2026.json:
# lv-2024-hl-i-1-e's row ends with the welded price fragment "(5 ×").
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits – 100"
# (p2 y64-81) and NO answer-language rule (sl_lib gives the lt walker's own
# note); the interview with Lilija Zobens (p2 y111-128), questions in bold and
# answers, p2 to p4 y153, closing with its source address
# "(https://www.latviesi.com/...)" (p4 y153); then on p4: "I daļa (30
# punkti)" (y197), Q1 "1. Skaidrojiet vārdus un frāzes!" (y243) over a)-e),
# "(5 × 1 punkti)" at the end of e)'s line (y332); Q2-Q6 each priced "(5)";
# "II daļa (30 punkti)" (y588), the commentary, ONE task with no number; "III
# daļa (40 punkti)" (y682), the instruction "Uzrakstiet pārspriedumu par vienu
# no tēmām! (ne mazāk kā 300 vārdu)" (y709) over two titles numbered "1."
# (y734) and "2." (y768), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2), but
# III2's census text runs on into the page footer: "Mūzika ir labākais
# mierinājums noskumušam cilvēkam. (Mārtiņš Luters) Leaving Certificate
# Examination, 2024 Leaving Certificate Examination, 2024 4 Latvian – Higher
# Level Latvian – Higher Level 4" (p4 y768 + the footer at y793-805). The
# question is cut from the paper's lines here. III1's census text ends with
# the "vai" printed under it.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q1(b): the paper's "(5 × 1 punkti)" (p4 y332, on e)'s line): one mark for
#   each expression, as the live a), c)-e) cards read it; PaperP on e)'s line
#   reads the "1 punkti". The scheme prints the same at the end of e)'s gloss
#   (58).
# - Q2 "2. Kādu problēmu ... (5)" (y360), Q3 "gaitās? (5)" (y404), Q4 "par to
#   saistībā ar tekstu un savu pieredzi. (5)" (y447), Q5 "trimdā? (5)" (y491),
#   Q6 "latviskumu un latvisko idenditāti? (5)" (y535): a bare "(5)" at the end
#   of the question's own last line, PaperP.
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints "II daļa (30 punkti)" (89) but "III daļa (30
#   punkti)" (106): see the judgement calls.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; pp6-7
# blank; answers in italics):
# - Q1 (48): each expression on its line, its gloss in italics on the next,
#   49-58; b) is reprinted "b) gāzt kalnus" (51) over "pārvarēt grūtības,
#   daudz izdarīt, daudz strādāt" (52).
# - Q2 (59): one paragraph, 60-63. Q3 (64-65): one paragraph, 66-68. Q4
#   (69-70): one paragraph, 75-77 (p4). Q5 (78-79): one paragraph, 80-83. Q6
#   (84-85): one paragraph, 86-88. No mark inside any answer.
# - Part II (89-92 reprint the head, the instruction and the statement): TWO
#   paragraphs, 93-94 and 95-101 (a gap between, rendered p4).
# - Part III (106-107, p5, the head and the instruction): under title 1 (108)
#   one paragraph, 109-114; "Or" (115, in English); under title 2 (116) one
#   paragraph, 117-119; each says what the student may write about.
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I1b: one stated gloss: ONE claimable row at the paper's 1, as the live
#   a), c)-e) cards.
# - I2-I6: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - II: two paragraphs of model content, no criteria: shown, whole=True on the
#   paper's 30 (10a).
# - III1/III2: one paragraph of indicative content under each title, no
#   criteria: shown, whole=True on the paper's 40 (10a), labelled as an
#   example.
# JUDGEMENT CALLS (10f: the paper's words and prices stand; the scheme's are
# quoted on the row's note):
# - Q1(b): the paper prints "b) jāgāž milzīgi kalni" (p4 y282); the scheme
#   reprints the expression as "b) gāzt kalnus" (51), the same idiom in its
#   dictionary form, and glosses it on the next line. The exclusions file
#   reads the two as different questions ("the paper and the scheme do not
#   print the same question at this address"); they are the same ask, so it
#   is carded with the scheme's gloss and the reprint quoted.
# - III: the paper prices the essay "(40 punkti)"; the scheme heads the part
#   "III daļa (30 punkti)" (106), against "Maksimālais punktu skaits – 100"
#   (46) and 30 + 30 + 40. An SEC self-contradiction: the paper's 40 stands,
#   the scheme's head quoted on each title's row.
# - Questions: the census's text for I1b and I2-II (checked on the render; no
#   price; Q6 keeps the paper's "idenditāti", as printed); III1/III2 the
#   instruction line and the title, which also drops III2's welded footer.
# - Reading text: pp2-4 (rendered: the interview runs from p2 to p4 y153, its
#   source line, above "I daļa"). The live Q1 cards' sourceMaterial.pages
#   [2, 3, 4] AGREE with the render.
# GLYPHS: none (U+00A0 spaces in the scheme read as spaces); ā č ē ģ ī ķ ļ ņ
# š ū ž read as the render shows them in every line used. Lifted as printed:
# "kas ir vienmēr tiks dziedātas" (81), "attīsījis" (94).

ESSAY_2024 = 'Uzrakstiet pārspriedumu'


def _q1b_2024(d):
    return (f'The scheme reprints this expression as “{S(51, after="b) ").text(d)}” and glosses it on the line '
            f'under it; the paper prints “{PC(4, "b) jāgāž", after="b) ").text(d)}”.')


def _part2_2024(d):
    return ('The scheme prints these two paragraphs under the statement, with no mark inside them and no '
            'criteria for the part.')


def _essay_2024(d):
    return (f'The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            f'the part: an example, not a checklist. It heads the part “{S(106).text(d)}”; the paper prints '
            f'“{PL(4, "III daļa").text(d)}”, and the paper\'s total stands.')


Q1P_2024 = PaperP(4, 'e) kopš')

SPECS[2024] = [
    R('I1b', [one(S(52), Q1P_2024)], total=Q1P_2024, rownote=_q1b_2024, pages=(2, 3, 4)),
    R('I2', [one(L(60, 63), PaperP(4, '2. Kādu'))], total=PaperP(4, '2. Kādu'), pages=(2, 3, 4)),
    R('I3', [one(L(66, 68), PaperP(4, 'gaitās?'))], total=PaperP(4, 'gaitās?'), pages=(2, 3, 4)),
    R('I4', [one(L(75, 77), PaperP(4, 'par to saistībā'))], total=PaperP(4, 'par to saistībā'), pages=(2, 3, 4)),
    R('I5', [one(L(80, 83), PaperP(4, 'trimdā?'))], total=PaperP(4, 'trimdā?'), pages=(2, 3, 4)),
    R('I6', [one(L(86, 88), PaperP(4, 'latviskumu un latvisko'))], total=PaperP(4, 'latviskumu un latvisko'),
      pages=(2, 3, 4)),
    R('II', [shown(L(93, 94)), shown(L(95, 101))], whole=True, rownote=_part2_2024, pages=(2, 3, 4)),
    R('III1', [shown(L(109, 114))], whole=True, rownote=_essay_2024, question=QP(4, ESSAY_2024, '1. Dziesmu')),
    R('III2', [shown(L(117, 119))], whole=True, rownote=_essay_2024, question=QP(4, ESSAY_2024, '2. Mūzika')),
]


# ====================================================================== 2025
# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the thirteen open asks of this
# sitting, I1a-I1e, I2-I6, II, III1, III2. No live card in this sitting.
# Paper (rendered pp2-4): "Maksimālais punktu skaits – 100" (p2 y65) and NO
# answer-language rule (sl_lib gives the lt walker's own note); the title
# "Svešumā dažreiz pat sirsnīgāk. Kā latvieši pasaulē svin valsts svētkus"
# (p2 y94), the text in unnumbered sections with bold heads, p2 y124 to p4
# y94, closing with its source address "https://www.lsm.lv/raksts/..." (p4
# y122-134); then on p4: "I daļa (30 punkti)" (y176), Q1 "1. Skaidrojiet
# tekstā lietotos vārdus un frāzes!" (y220) over a)-e), "(5 × 1)" at the end
# of e)'s line (y313); Q2-Q6 each priced "(5)"; "II daļa (30 punkti)" (y557),
# the commentary, ONE task with no number; "III daļa (40 punkti)" (y674), the
# instruction "Uzrakstiet eseju par vienu no tēmām! (ne mazāk kā 300 vārdu)"
# (y689) over two titles numbered "1." (y715) and "2." (y748), "vai" between
# them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2); III1's
# census text ends with the "vai" printed under it.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q1: the paper prints "(5 × 1)" at the end of e)'s line (p4 y313,
#   rendered): one mark for EACH expression, so Q1 is carded per letter (the
#   brief: "unless the paper prints a mark per expression"; live 2023/2024 Q1,
#   priced "(5 × 1 punkti)" the same way, are per letter). PaperP does not read
#   a bracket with "×" and no mark word, and PY reads only a worded cell, so
#   each letter is priced from the identical cell the scheme prints at the end
#   of e)'s gloss, "gandrīz 20 gadus (5 × 1)" (70): RX(70, ...), group 1 = the
#   per-expression 1.
# - Q2 "... izraisa 18.novembris. (5)" (y348), Q3 "... multikulturālā ģimenē.
#   (5)" (y375), Q4 "viedokli, atsaucoties uz tekstu un savu pieredzi. (5)"
#   (y418), Q6 "tekstu un savu pieredzi. (5)" (y489): a bare "(5)" at the end of
#   the question's own last line, PaperP.
# - Q5: "(5)" on a line of its own under the question (p4 x482 y460), the only
#   line of p4 opening "(5)": PaperP(4, '(5)').
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints "II daļa (30)" (131) and "III daļa (40)" (148).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-7 = printed pages 4-7, "Latvian
# Marking Scheme 2025"; p3 the annotations table; p8 blank; answers in
# italics):
# - Q1 (60): each expression on its line, its gloss on the next: 62, 64, 66,
#   68, 70 ("gandrīz 20 gadus (5 × 1)"). No mark on any but that cell.
# - Q2 (71): one paragraph, 72-74, "(5)" set at the end of its last line.
# - Q3 (75): THREE paragraphs, 76-80, 81-82, 83-84 (gaps between, rendered
#   p4), "(5)" at the end of the last.
# - Q4 (89-90): one paragraph, 91-100. Q5 (101-102): one paragraph, 103-111.
#   Q6 (112-113): one paragraph, 114-126. Each ends with "(5)".
#   No mark inside any answer.
# - Part II (131-134 the head, the instruction and the statement): TWO
#   paragraphs, 135-145 and 146-147 (a gap between, rendered p6).
# - Part III (148-152, the head, the instruction and both titles), then each
#   title again as a plain head with its content under it: "Tradīcijas ir
#   sabiedrības pamats" (153) over FOUR paragraphs, 154-160, 161-162, 167-168,
#   169-170 (pp6-7); '“Nekad neuzliec vecuma limitu saviem sapņiem” (Dara
#   Torres)' (171) over FOUR paragraphs, 172-177, 178-179, 180-182, 183-185
#   (rendered p7: each opens a new line after a short one).
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I1a-I1e: one stated gloss each: ONE claimable row at 1.
# - I2, I4, I5, I6: one printed model paragraph each: ONE claimable row,
#   one(sel, price) at the paper's 5, cut before the scheme's "(5)".
# - I3: three paragraphs: shown rows, whole=True on the printed 5.
# - II: two paragraphs of model content, no criteria: shown, whole=True on the
#   paper's 30 (10a).
# - III1/III2: the paragraphs the scheme prints under each title, no
#   criteria: shown, whole=True on the paper's 40 (10a), labelled as
#   examples; the title the scheme reprints over them is a head, not a row.
# JUDGEMENT CALLS:
# - Q1 per letter, as above; if the lead rules "(5 × 1)" a whole-question
#   price, the same rows go shown on R('I1', ..., whole=True) at 5.
# - I4, I5, I6 are long paragraphs of indicative content ("Skolēni var ...")
#   but each is ONE printed paragraph: one claimable row on the convention.
#   Flip to [shown(...)], whole=True if the lead prefers.
# - The scheme's reprints match the paper word for word (Q2 ends "." on both).
# - Questions: the census's text for I1a-e and I2-II (checked on the render;
#   no price); III1/III2 the instruction line and the title.
# - Reading text: pp2-4 (rendered: the text runs from p2 to p4 y94, its
#   source address at p4 y122-134, above "I daļa"). No live card to compare.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Lifted as printed: "pieredzēm" (76), "Laine un Artūrs" (114).

ESSAY_2025 = 'Uzrakstiet eseju'
Q1P_2025 = RX(70, r'\(\d\s*×\s*(\d)\)')


def _paras_2025(d):
    return ('The scheme prints these paragraphs under the question, with no mark on any of them: shown as '
            'the scheme prints them, scored on the question\'s total.')


def _part2_2025(d):
    return ('The scheme prints these two paragraphs under the statement, with no mark inside them and no '
            'criteria for the part.')


def _essay_2025(d):
    return ('The scheme prints these paragraphs under the title, with no mark on any of them and no criteria '
            'for the part: examples, not a checklist.')


SPECS[2025] = [
    R('I1a', [one(S(62), Q1P_2025)], total=Q1P_2025, pages=(2, 3, 4)),
    R('I1b', [one(S(64), Q1P_2025)], total=Q1P_2025, pages=(2, 3, 4)),
    R('I1c', [one(S(66), Q1P_2025)], total=Q1P_2025, pages=(2, 3, 4)),
    R('I1d', [one(S(68), Q1P_2025)], total=Q1P_2025, pages=(2, 3, 4)),
    R('I1e', [one(S(70, before=' (5'), Q1P_2025)], total=Q1P_2025, pages=(2, 3, 4)),
    R('I2', [one(L(72, 74, before=' (5)'), PaperP(4, '2. Kādas'))], total=PaperP(4, '2. Kādas'), pages=(2, 3, 4)),
    R('I3', [shown(L(76, 80)), shown(L(81, 82)), shown(L(83, 84, before=' (5)'))], whole=True,
      total=PaperP(4, '3. Aprakstiet'), rownote=_paras_2025, pages=(2, 3, 4)),
    R('I4', [one(L(91, 100, before=' (5)'), PaperP(4, 'viedokli, atsaucoties'))],
      total=PaperP(4, 'viedokli, atsaucoties'), pages=(2, 3, 4)),
    R('I5', [one(L(103, 111, before=' (5)'), PaperP(4, '(5)'))], total=PaperP(4, '(5)'), pages=(2, 3, 4)),
    R('I6', [one(L(114, 126, before=' (5)'), PaperP(4, 'tekstu un savu pieredzi.'))],
      total=PaperP(4, 'tekstu un savu pieredzi.'), pages=(2, 3, 4)),
    R('II', [shown(L(135, 145)), shown(L(146, 147))], whole=True, rownote=_part2_2025, pages=(2, 3, 4)),
    R('III1', [shown(L(154, 160)), shown(L(161, 162)), shown(L(167, 168)), shown(L(169, 170))], whole=True,
      rownote=_essay_2025, question=QP(4, ESSAY_2025, '1. Tradīcijas')),
    R('III2', [shown(L(172, 177)), shown(L(178, 179)), shown(L(180, 182)), shown(L(183, 185))], whole=True,
      rownote=_essay_2025, question=QP(4, ESSAY_2025, '2. “Nekad')),
]


# ====================================================================== 2026
# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, lv-2026-hl-i-1); not
# touched (audited: see latvian-live-faults-2018-2026.json: its question text
# is the scheme's stem, not the paper's).
# Paper (rendered pp2-4): "LATVIEŠU VALODA", "Maksimālais punktu skaits – 100",
# the instruction with the rule "... Visām atbildēm jābūt latviski!" (p2
# y108-123); the title "Sarežģītais teksta uzdevums" (p2 y152), numbered
# paragraphs p2 y178 to p3, closing with its source
# "https://satori.lv/article/sarezgitais-teksta-uzdevums-diskusija,
# 28.12.2022." (p3 y710); p4 holds the questions: "Atbildiet uz visiem
# jautājumiem, ..." (y65), "I daļa (30 punkti)" (y108), Q1 "1. Skaidrojiet
# tekstā lietotos vārdus un frāzes!" (y163) over a)-e), "(5 × 1 punkti)" at
# the end of e)'s line (y281) (live); Q2-Q6 each priced "(5)"; "II daļa (30
# punkti)" (y539), the commentary, ONE task with no number; "III daļa (40
# punkti)" (y655), the instruction "Uzrakstiet eseju par vienu no tēmām! (ne
# mazāk kā 300 vārdu)" (y678) over two titles numbered "1." (y707) and "2."
# (y746), "vai" between them.
# CENSUS: every printed ask is keyed (I1a-e, I2-I6, II, III1, III2); III1's
# census text ends with the "vai" printed under it.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2 "2. Formulējiet ... (5)" (p4 y325), Q3 "3. Kas ir diskusijas ... (5)"
#   (y355), Q4 "akcentē tās nozīmi? (5)" (y399), Q5 "tā pretstats? (5)" (y443):
#   a bare "(5)" at the end of the question's own last line, PaperP.
# - Q6: "(5)" on a line of its own under the question (p4 x482 y501), the only
#   line of p4 opening "(5)": PaperP(4, '(5)').
# - II: "II daļa (30 punkti)" (PARTP); III1/III2: "III daļa (40 punkti)"
#   (PARTP). The scheme prints "II daļa (30 punktu)" (131) and "III daļa (40
#   punkti)" (144).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-7 = printed pages 4-7,
# "Leaving Certificate Latvian Marking Scheme 2026"; p3 the annotations
# table; p8 blank; answers in plain type, Part II-III in italics):
# - Q2 (72 reprint): one paragraph, 73-77. Q3 (78): one paragraph, 79-84.
# - Q4 (89-90): TWO paragraphs, 91-92 and 93-97 (a gap between, rendered p5).
# - Q5 (98-99): TWO paragraphs, 100-105 and 106-107 ("Pretstats ir ...").
# - Q6 (108-110): THREE paragraphs, 111-115 (p5), 120-123 and 124-126 (p6).
#   No mark inside any answer.
# - Part II (131-135, p7, the head and the task, reworded: see below): THREE
#   paragraphs, 136-137, 138-142, and "Skolēns pauž savu argumentētu
#   viedokli." (143) on a line of its own.
# - Part III (144-145 the head and the instruction): under title 1 (146) one
#   paragraph, 147-150; "vai" (151); under title 2 (152) one paragraph,
#   153-155; each says what the student writes about.
#   NO criteria anywhere in this scheme.
# SHAPES:
# - I2, I3: one printed model paragraph each: ONE claimable row, one(sel,
#   price) at the paper's 5.
# - I4, I5, I6: several paragraphs: shown rows, whole=True on the printed 5.
# - II: three paragraphs of model content, no criteria: shown, whole=True on
#   the paper's 30 (10a).
# - III1/III2: one paragraph of indicative content under each title, no
#   criteria: shown, whole=True on the paper's 40 (10a), labelled as an
#   example.
# JUDGEMENT CALLS (10f: the paper's words are the question; where the scheme
# rewords one, its reprint is quoted on the row's note):
# - Part II: the paper prints "Izsakiet savu viedokli par šo apgalvojumu!
#   (100 - 150 vārdu)" (p4 y568); the scheme reprints "Izsakiet savu viedokli
#   par piedāvāto apgalvojumu! (vismaz 100 vārdu)" (132). Quoted.
# - Part III: the paper prints "Uzrakstiet eseju par vienu no tēmām! ..."
#   (p4 y678); the scheme reprints "Uzrakstiet pārspriedumu par vienu no
#   tēmām! ..." (145). Quoted on both titles.
# - Part II's line 143 ("the student gives an argued opinion") is the scheme's
#   own closing line under the model, kept as a shown row as the scheme sets
#   it; move it to the note if the lead reads it as an instruction.
# - Q2-Q6: the scheme's reprints differ in spacing only ("Kas ir lasītprasme,
#   kuros", "Raksturojiet, kādu  situāciju"); not quoted.
# - Questions: the census's text for I2-II (checked on the render; no price);
#   III1/III2 the instruction line and the title.
# - Reading text: pp2-3 (rendered: the title and the text from p2 to its
#   source line at p3 y710; p4 holds only the questions). The live Q1 card's
#   sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none; ā č ē ģ ī ķ ļ ņ š ū ž read as the render shows them in every
# line used. Lifted as printed: "jaunieši lasītprasme" (73), "izdevniecīu",
# "kurs ik dienu" (81-82), "Diskusijas dalībnieka nonāk" (95), "lēnajam
# laikam.Lasot" (103), "ineresantām", "neinteresanas", "tika fragmenti"
# (125-126).

ESSAY_2026 = 'Uzrakstiet eseju'


def _paras_2026(d):
    return ('The scheme prints these paragraphs under the question, with no mark on any of them: shown as '
            'the scheme prints them, scored on the question\'s total.')


def _part2_2026(d):
    return ('The scheme prints these paragraphs under the statement, with no mark inside them and no criteria '
            f'for the part. It reprints the instruction as “{S(132).text(d)}”')


def _essay_2026(d):
    return ('The scheme prints this paragraph under the title, with no mark inside it and no criteria for '
            f'the part: an example, not a checklist. It reprints the instruction as “{S(145).text(d)}”')


SPECS[2026] = [
    R('I2', [one(L(73, 77), PaperP(4, '2. Formulējiet'))], total=PaperP(4, '2. Formulējiet'), pages=(2, 3)),
    R('I3', [one(L(79, 84), PaperP(4, '3. Kas ir'))], total=PaperP(4, '3. Kas ir'), pages=(2, 3)),
    R('I4', [shown(L(91, 92)), shown(L(93, 97))], whole=True, total=PaperP(4, 'akcentē tās'),
      rownote=_paras_2026, pages=(2, 3)),
    R('I5', [shown(L(100, 105)), shown(L(106, 107))], whole=True, total=PaperP(4, 'tā pretstats?'),
      rownote=_paras_2026, pages=(2, 3)),
    R('I6', [shown(L(111, 115)), shown(L(120, 123)), shown(L(124, 126))], whole=True, total=PaperP(4, '(5)'),
      rownote=_paras_2026, pages=(2, 3)),
    R('II', [shown(L(136, 137)), shown(L(138, 142)), shown(S(143))], whole=True, rownote=_part2_2026,
      pages=(2, 3)),
    R('III1', [shown(L(147, 150))], whole=True, rownote=_essay_2026, question=QP(4, ESSAY_2026, '1. “Mana')),
    R('III2', [shown(L(153, 155))], whole=True, rownote=_essay_2026, question=QP(4, ESSAY_2026, '2. „Turiet')),
]
