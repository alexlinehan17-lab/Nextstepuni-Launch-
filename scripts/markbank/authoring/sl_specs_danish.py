#!/usr/bin/env python3
"""Reviewed specs for the Danish classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/danish/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def _titles(*sels):
    """A question printed as a stem over titles: each printed line (or cut)
    on a line of its own."""
    return lambda d, _q: '\n'.join(s.text(d) for s in sels)


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2010 HL ===
# The SEC published no marking scheme for 2010 (SOURCES.md item 5: not in the
# archive listing; no scheme on disk). Every ask is carded with the paper's own
# price and the fixed line NO_SCHEME_PUBLISHED, unscored (R4), by the lead.
# Paper (rendered pp2-4): the text runs pp2-3 (paragraphs 1-8, to y380 on p3);
# Opgave I "(maksimum 30 point)": Q1 prints five unlettered expressions under
# "(5 x 1 point)" (one ask in the census), Q2-Q6 "(5 point)" each; Opgave II
# "(maksimum 30 point)" (p4), the commentary; Opgave III "(maksimum 40 point)",
# one essay task with its two titles as dashes (one ask in the census).
SPECS[2010] = [
    NoScheme('I1', pages=(2, 3)),
    NoScheme('I2', pages=(2, 3)),
    NoScheme('I3', pages=(2, 3)),
    NoScheme('I4', pages=(2, 3)),
    NoScheme('I5', pages=(2, 3)),
    NoScheme('I6', pages=(2, 3)),
    NoScheme('II1', total=PARTP(), pages=(2, 3)),
    NoScheme('III1', total=PARTP()),
]


# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1 and III1. Live: I1-I6 (6 cards); not touched (audited: see the LIVE
# FAULTS list, danish-live-faults-2011-2017.json).
# Paper (rendered pp2-4): "DANSK (maksimum 100 point)" (p2); the text "Lykke er
# - at være dansk" runs pp2-3 (title p2 y178, paragraphs 1-10 to p3 y320);
# "Opgaver" (p3 y372), the rule "Alle spørgsmål skal besvares med dine egne ord
# og på dansk" (p3 y398, bold italic, no full stop); "Opgave I (maksimum 30
# point)" (p3 y424); Q1 five unlettered "Forklar ordet ..." lines under one
# "(maks. 5 x 1 point)" (p3 y518); Q2-Q6 "(maks. 5 point)" each; "Opgave II
# (maksimum 30 point)" on one line (p4 y91), a quotation from paragraph 6 and
# "Kommenter dette synspunkt med minimum 100 ord." (bold); "Opgave III
# (maksimum 40 point)" on one line (p4 y271), "Skriv et essay på cirka 300 ord
# om ét af disse to emner:" and two titles set as DASHES (p4 y326, y353-367),
# not numbered: the census counts one ask, III1 (as the 2010 sitting).
# PRICES:
# - II1: the head's own "(maksimum 30 point)" (PARTP; the census reads only
#   Opgave I's total this sitting, so PARTP reads the head's own line). The
#   scheme prints the same head "Opgave II (maksimum 30 point)" (line 34).
# - III1: "(maksimum 40 point)" (PARTP, head's own line); scheme line 38.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; p1 cover, p2 blank, pp5-8
# blank):
# - Opgave II (34): one paragraph, 35-37, "Svaret forventes at indfange det
#   dialektiske ved lykken i citatet: ... ikke være godt." (what the answer is
#   expected to capture).
# - Opgave III (38): one paragraph, 39-41, "Svaret forventes at forholde sig
#   eksplicit til begreberne materiel og åndelig/sjælelig lykke. ... en
#   personlig stillingtagen til emnet."
# - Criteria (p4, 46-53): "Note: I del 2 og del 3 vil de følgende elementer
#   blive anvendt som vurderingskriterier." -- for Parts 2 AND 3. 1. Målstyring
#   "– 30 %" (47-48), 2. Sammenhæng "– 30%" (49-50), 3. Sprogligt herredømme
#   "– 30%" (51-52), 4. Sprogregler "– 10%" (53): all four printed (rendered
#   p4), 100 %.
# SHAPES:
# - II1: graded (10b) on the four criteria: 30/30/30/10 % of 30 = 9/9/9/3,
#   whole numbers. Head: the part's own paragraph (35-37), the scheme's answer
#   for this part; the criteria's lead line quoted (it names the parts).
# - III1: graded (10b): 30/30/30/10 % of 40 = 12/12/12/4. Head: Part III's own
#   paragraph (39-41); the lead line quoted.
# JUDGEMENT CALLS:
# - Part III's paragraph names no title, but its words address the first
#   ("begreberne materiel og åndelig/sjælelig lykke"; title 1 "Forholdet mellem
#   åndelig og materiel lykkeopfattelse"). The census keys ONE ask over both
#   dashed titles (no number on either), so the one card carries both titles
#   and the paragraph as printed; the note says the scheme names no title.
#   If the lead wants a split, it needs a coordinator ruling (titles unnumbered).
# - III1's question is cut from the paper's lines (stem, then each title on a
#   line of its own: QL), so the dashes the paper sets as separate cells do
#   not run into the text.
# - II1's question is cut from the paper's own lines (quotation and task).
# - Reading text pp2-3 (rendered). II1 quotes paragraph 6, so the text
#   travels with it: pages=(2, 3). The live Part I cards of 2011 carry NO
#   sourceMaterial at all (flagged, P).
# GLYPHS: none. æ ø å read cleanly in every line used (paper and scheme), and
# the scheme's "competent" (52) is printed so (English word on the render).

CRIT_2011 = crit((47, 48), (49, 50), (51, 52), 53)
LEAD_2011 = quote(S(46), lead='The scheme prints')


def _no_title_2011(d):
    return 'The scheme prints this paragraph under “Opgave III” and names neither title.'


SPECS[2011] = [
    R('II1', [graded(L(35, 37), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, Run('”Er vi overlykkelige', 'kræfter og overskud.”'), 'Kommenter dette synspunkt'),
      pages=(2, 3)),
    R('III1', [graded(L(39, 41), PARTP(), CRIT_2011)], rownote=both(LEAD_2011, _no_title_2011),
      question=QL(4, 'Skriv et essay på cirka 300 ord', 'Forholdet mellem åndelig',
                  Run('"De fleste mennesker', '(Abraham Lincoln'))),
]


# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1 and III1. Live: I1-I6 (6 cards); not touched (audited: see
# danish-live-faults-2011-2017.json).
# Paper (rendered pp2-4): the instruction and the rule "Alle svar skal skrives
# på dansk." (p2 y107-122), "Maksimum 100 point" (p2 y150); the article "Hvor
# meget betyder det ydre?" runs pp2-3 (paragraphs 1-6, p2 y232 to p3 y506);
# "Opgave I" with "(maksimum 30 point)" in its right-hand cell (p3 y548); Q1
# five unlettered "Forklar betydningen ..." lines over one "(maks. 5x1 point)"
# (p3 y644); Q2-Q6 "(maks. 5 point)" each; "Opgave II" / "(maksimum 30 point)"
# (p4 y368), a quotation and "Diskuter dette synspunkt med ca. 100 ord."
# (y437); "Opgave III" / "(maksimum 40 point)" (p4 y534), "Skriv et essay på
# cirka 300 ord om ét af disse to emner:" and two DASHED titles joined by
# "ELLER" (p4 y589-644), not numbered: the census counts one ask, III1.
# PRICES:
# - II1: "(maksimum 30 point)" (PARTP; the census reads the head cell). The
#   scheme heads the part "Part II Total 30 marks" (line 43).
# - III1: "(maksimum 40 point)" (PARTP); scheme "Part III Total 40 marks" (53).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; p1 cover, p2 blank):
# - Part II (43): a descriptive line, 44, "Kommentar på ca. 100 ord som viser
#   klar forståelse af tekstens vigtigste pointer."; then "Diskussionen kan
#   f.eks. drejes i følgende retninger:" (45) over two directions, "a.
#   Udviklingen er harmløs ... skabe sig en karriere," (46-47) and "b.
#   Udskillelse af grimme mennesker kan føre til decideret diskrimination og
#   had." (the "b." is set at the END of line 47, rendered p3; its words are
#   line 48).
# - Part III (53, p4): a descriptive line, 54-55, "Et velskrevet eassay på ca.
#   300 ord, relevant i forhold til hver sit emne, ... rimeligt flydende.";
#   then "For eksempel: Menneskelige relationer bygger på meget andet end
#   udseendet ... ikke i nogen klub på internettet." (56-58).
# - Criteria (p4, 59-66): "Note: I del 2 og del 3 vil de følgende elementer
#   blive anvendt som vurderingskriterier." -- Parts 2 AND 3. Målstyring
#   "– 30 %" (60-61), Sammenhæng "– 30%" (62-63), Sprogligt herredømme
#   "– 30%" (64-65), Sprogregler "– 10%" (66): all four printed, 100 %.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the part's descriptive line (44);
#   the two directions quoted under the scheme's own heading (45) as
#   examples, not a checklist (10a); the criteria's lead quoted.
# - III1: graded (10b), 12/12/12/4 of 40. Head: the descriptive line (54-55);
#   the paragraph quoted under the scheme's own "For eksempel:" as an example
#   (10a); lead quoted.
# JUDGEMENT CALLS:
# - Direction a. is cut before ", b." on line 47 and b. is line 48 (the SEC
#   set the letter at the end of the line above its words; rendered p3).
# - III1 carries both dashed titles (one ask). The scheme's example concerns
#   the first title ("Dybde og overflade i menneskelige relationer"); its
#   descriptive line says "relevant i forhold til hver sit emne" (both).
# - III1's question: the stem and each title on a line of its own, the
#   paper's dashes and "ELLER" left out (the second dash is printed inside
#   the title's own cell, "- I vores ...", so it is cut after "- ").
# - II1's question is cut from the paper's lines (the census glues the head
#   cell's "(maksimum 30 point)" in front).
# - Reading text pp2-3 (rendered: p2 holds the rule, the title and paragraphs
#   1-3; p3 paragraphs 3-6 to y506). The live Part I cards carry
#   sourceMaterial.pages [3]: the render does not agree (flagged, P).
# GLYPHS: none. Scheme line 54 prints "eassay" (rendered p4 identically: the
#   SEC's typing), lifted as printed; flagged for the lead.

CRIT_2012 = crit((60, 61), (62, 63), (64, 65), 66)
LEAD_2012 = quote(S(59), lead='The scheme prints')


SPECS[2012] = [
    R('II1', [graded(S(44), PARTP(), CRIT_2012)],
      rownote=both(examples(S(45), J(S(46, after='a. '), S(47, before=', b.')), S(48)), LEAD_2012),
      question=QP(4, Run('”Pæne mennesker', 'også fakta'), 'Diskuter dette synspunkt'),
      pages=(2, 3)),
    R('III1', [graded(L(54, 55), PARTP(), CRIT_2012)],
      rownote=both(examples(S(56, before=' Menneskelige'), L(56, 58, after='For eksempel: ')), LEAD_2012),
      question=_titles(PL(4, 'Skriv et essay'), PL(4, 'Dybde og overflade'),
                       PC(4, '- I vores moderne', after='- '))),
]


# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1-I6 (6 cards); not touched (audited: see
# danish-live-faults-2011-2017.json).
# Paper (rendered pp2-4): the instruction and the rule "Alle svar skal skrives
# på dansk." (p2 y65-81), "(Maksimum 100 point)" (p2 y122); the article
# "Kapitalisme-kritik helt ude i skoven" runs pp2-3 (title p2 y148, the text to
# p3 y438, the editing note p3 y487); "Opgave I" / "(30 point)" (p3
# y587-605); Q1 five unlettered lines over "(5 × 1 point)" (p3 y755); Q2-Q6
# "(5 point)" each (p4); "Opgave II" / "(30 point)" (p4 y451), a quotation
# and the task (y478-532); "Opgave III" / "(40 point)" (p4 y607), "Skriv et
# essay på cirka 300 ord om ét af disse to emner:" over two NUMBERED titles,
# "1. Personlige værdier ..." and "2. " Selvom vi rejser ..."" with "Ralph
# Waldo Emerson" (italic) set at its right, joined by "ELLER" (p4 y685-751):
# the census counts two asks, III1 and III2 (coordinator ruling B).
# PRICES:
# - II1: "(30 point)" (PARTP; the census reads the head cell). Scheme "Part II
#   Total 30 marks" (87).
# - III1/III2: "(40 point)" (PARTP). Scheme "Part III Total 40 marks" (95).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; p2 the standard note, pp5-6
# blank):
# - Criteria FIRST (p4 top, 79-86): "Note: I del 2 og del 3 vil de følgende
#   elementer blive anvendt som vurderingskriterier." -- Parts 2 AND 3.
#   Målstyring "– 30 %" (80-81), Sammenhæng "– 30%" (82-83), Sprogligt
#   herredømme "– 30%" (84-85), Sprogregler "– 10%" (86): 100 %.
# - Part II (87): a descriptive line, 88, "Kommentar på ca. 100 ord som viser
#   klar forståelse af tekstens vigtigste pointer."; then one paragraph,
#   89-94, opening with its own heading run into the line, "Diskussionen kan
#   f.eks. drejes i følgende retninger: Det moderne, vestlige liv er det
#   bedste af alle, ... en ny og bedre måde at leve på."
# - Part III (95): title 1 reprinted in bold as a heading (96, "Personlige
#   værdier og kompetencer i en verden under forandring"); a descriptive line,
#   97-98, "Et velskrevet essay på ca. 300 ord, relevant i forhold til hver
#   sit emne, ... rimeligt flydende."; a paragraph of content for title 1,
#   99-104 ("Menneskets forhold til det omgivende samfund ... kræver
#   fleksibilitet af mennesket."); "ELLER" (105); title 2 reprinted in bold
#   (106-107) and NOTHING under it (rendered p4 ends there; p5 blank).
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30. Head: the descriptive line (88); the
#   paragraph quoted under its own heading as examples (10a); lead quoted.
# - III1: graded (10b), 12/12/12/4 of 40. Head: the descriptive line (97-98);
#   the title-1 paragraph quoted under the scheme's own heading (the bold
#   title, 96) as examples (10a); lead quoted.
# - III2: graded (10b), 12/12/12/4 of 40: the criteria serve "del 3" as a
#   whole. Head: the same descriptive line (97-98), whose words cover both
#   titles ("relevant i forhold til hver sit emne"); the note says the scheme
#   reprints the second title and prints nothing under it.
# JUDGEMENT CALLS:
# - The descriptive line 97-98 is printed under title 1's bold heading, but it
#   names "hver sit emne" (each topic): read as serving both titles, so it
#   heads III2 too. If the lead reads it as title 1's alone, III2's head has
#   no printed line of its own: then III2 would be unprinted() at 40 with the
#   criteria quoted, since the criteria (not an answer) are all it has.
# - II1's question is cut from the paper's lines (the census glues the head
#   cell's "(30 point)" in front). The paper opens the quotation with ” and
#   prints no closing mark (rendered p4): kept as printed.
# - III1/III2 questions: the stem, then the title (number taken off); III2
#   keeps its attribution "Ralph Waldo Emerson" (a cell of the title's last
#   line). The census glues "ELLER" to III1.
# - Reading text pp2-3 (rendered). II1 travels with it. The live Part I
#   cards carry sourceMaterial.pages [3]: the render does not agree (p2 holds
#   the rule, title and most of the text; flagged, P).
# GLYPHS: none in the lines used.

CRIT_2014 = crit((80, 81), (82, 83), (84, 85), 86)
LEAD_2014 = quote(S(79), lead='The scheme prints')
ESSAY_2014 = 'Skriv et essay på cirka 300 ord'


def _nothing_2014(d):
    return f'The scheme reprints the second title as “{L(106, 107).text(d)}” and prints nothing under it.'


SPECS[2014] = [
    R('II1', [graded(S(88), PARTP(), CRIT_2014)],
      rownote=both(examples(S(89, before=' Det moderne'), L(89, 94, after='retninger: ')), LEAD_2014),
      question=QP(4, Run('”De unge i vores', 'livsformer.'), Run('Hvorfor tror du', 'Forklar din mening')),
      pages=(2, 3)),
    R('III1', [graded(L(97, 98), PARTP(), CRIT_2014)],
      rownote=both(examples(S(96), L(99, 104)), LEAD_2014),
      question=QP(4, ESSAY_2014, '1. Personlige værdier')),
    R('III2', [graded(L(97, 98), PARTP(), CRIT_2014)],
      rownote=both(LEAD_2014, _nothing_2014),
      question=QP(4, ESSAY_2014, Run('2. " Selvom', 'Ralph Waldo Emerson'))),
]


# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# I1, II1, III1. Live: I2-I6 (5 cards); not touched (audited: see
# danish-live-faults-2011-2017.json).
# Paper (rendered pp2-4): the instruction and the rule "Alle svar skal skrives
# på dansk." (p2 y64-78), "(Maksimum 100 point)" (p2 y91); the article "Ud med
# smid-væk-kulturen: Alt fra bamser til brødristere repareres" runs pp2-3
# (title p2 y140, the text to the byline p3 y520 and the editing note p3
# y545); "Opgave I" / "(maksimum 30 point)" (p3 y619); Q1 prints FIVE
# UNLETTERED "Forklar betydningen af ordet ..." lines, four on p3 (y668-741)
# and the fifth on p4 (y63), and under them "(maks. 5×1 point)" on a line of
# its own (p4 y78); Q2-Q6 "(maks. 5 point)" each; "Opgave II" / "(maksimum 30
# point)" (p4 y461); "Opgave III" / "(maksimum 40 point)" (p4 y593), "Skriv et
# essay på cirka 300 ord om ét af disse to emner:" over two DASHED titles
# joined by "ELLER" (p4 y667-755): one ask, III1.
# PRICES:
# - I1: the census reads NO price (tariff None; Q1 runs over the page break),
#   but the paper PRINTS one: "(maks. 5×1 point)" (p4 y78), 1 point for each
#   expression. Each row is priced from that printed line (PaperP reads its
#   "1 point"); the card's 5 is read from the scheme's reprint "(5 × 1 point)"
#   (line 55, RX), the same figure: no sl_lib reader takes the count "5" of a
#   paper's "5×1" (PaperP reads the "1 point"; PY refuses "maks."). Not 10i:
#   the exclusion's "neither document states a tariff" is wrong.
# - II1: "(maksimum 30 point)" (PARTP). Scheme "Opgave II Total 30 marks" (83).
# - III1: "(maksimum 40 point)" (PARTP). Scheme "Opgave III Total 40 marks" (92).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; p1 cover, p2 the standard
# note, pp5-6 blank):
# - Q1 (50-55): five lines "Enhver rimelig forklaring (e.g. “...”)", one per
#   expression, in the paper's order, then "(5 × 1 point)". Paired by words:
#   englebamse / "et sovedyr som ligner en bjørn med vinger på ryggen" (50);
#   uldtrøje / "beklædning til overkroppen, lavet af uld" (51); genbrug / "at
#   genanvende tingene eller materialerne" (52); fortørnede / "vrede,
#   skuffede" (53); vendepunkt / "at bevæge sig i en anden retning end den
#   hidtidige" (54).
# - Opgave II (83, p4): a descriptive line, 84, "Kommentar på ca. 100 ord som
#   viser evne til at sætte temaet ind i et større perspektiv."; then two
#   alternative paragraphs, 85-87 ("F.eks. kan man tage det approach, at den
#   høje skilsmisserate ...") and 88-91 ("Eller man kan sige, at
#   skilsmisserate og smid-væk-kultur ikke har noget med hinanden at gøre,
#   ...").
# - Opgave III (92): the two titles reprinted with their dashes and "Eller"
#   (93-95), a stray dash (96, rendered p4), then ONE descriptive line, 97-98,
#   "Et velskrevet essay på ca. 300 ord, relevant i forhold til hver sit
#   emne, ... rimeligt flydende."
# - NO criteria anywhere this sitting (rendered pp3-4; the 2011-2014 "Note: I
#   del 2 og del 3 ..." block is not printed).
# SHAPES:
# - I1: one card (one ask), a row per expression, each one(gloss) at the
#   paper's 1 point, adding to 5; each row led by its expression (the
#   paper's word, cut from its line) so the pairing shows.
# - II1: the two paragraphs shown, priced as a whole on the paper's 30 (10a,
#   questionTotal); the descriptive line quoted as its head.
# - III1: only a descriptive line and no criteria: R4 (unprinted) at the
#   paper's 40, the note quoting the line (ruling 4).
# JUDGEMENT CALLS:
# - Q1 rows keep the scheme's whole line, "Enhver rimelig forklaring (e.g.
#   “...”)": the scheme's answer is the direction AND its example (as the live
#   2012/2014/2016 Q1 cards quote it).
# - I1's question: the five printed lines, one per line (QL), the fifth from
#   p4; the census text holds them run together.
# - II1 is shown, not graded: no criteria are printed for 2015.
# - II1's question is cut from the paper's lines (the census glues the head
#   cell's "(maksimum 30 point)" in front).
# - III1's question: stem and both titles, one per line, dashes and "ELLER"
#   left out; title 2 keeps "(Sokrates)" (italic, same printed line).
# - Reading text pp2-3 (rendered). The live Part I cards (I2-I6) carry
#   sourceMaterial.pages [3]: the render does not agree (flagged, P).
# GLYPHS: the scheme's cover and note headings (lines 4, 6, 9-11, 15, 35) are
# a shifted font map ("&RLPLVL~QQD6FU~GXLWKH6WiLW" for "Coimisiún na
# Scrúduithe Stáit": ASCII letters read 29 code points low, '&' U+0026 for
# 'C' U+0043, 'R' U+0052 for 'o' U+006F; 'ú' read as '~' U+007E). Cover and
# boilerplate only: no line used here is affected; æ ø å read cleanly in
# lines 50-98 (checked against the render).

Q1P_2015 = PaperP(4, '(maks. 5×1 point)')
Q1T_2015 = RX(55, r'\((\d)\s*×\s*1\s*point\)')


def _word(page, opening):
    """The expression a Q1 line prints between its quotation marks."""
    return PC(page, opening, after='ordet ”', before='”')


SPECS[2015] = [
    R('I1', [one(S(50, after='1. '), Q1P_2015, lead=_word(3, '1. Forklar betydningen af ordet ”englebamse”')),
             one(S(51), Q1P_2015, lead=_word(3, 'Forklar betydningen af ordet ”uldtrøje”')),
             one(S(52), Q1P_2015, lead=_word(3, 'Forklar betydningen af ordet ” genbrug”')),
             one(S(53), Q1P_2015, lead=_word(3, 'Forklar betydningen af ordet ” fortørnede”')),
             one(S(54), Q1P_2015, lead=_word(4, 'Forklar betydningen af ordet ” vendepunkt”'))],
      total=Q1T_2015,
      question=QL(3, '1. Forklar betydningen af ordet ”englebamse”',
                  'Forklar betydningen af ordet ”uldtrøje”', 'Forklar betydningen af ordet ” genbrug”',
                  'Forklar betydningen af ordet ” fortørnede”',
                  (4, 'Forklar betydningen af ordet ” vendepunkt”')),
      pages=(2, 3)),
    R('II1', [shown(L(85, 87)), shown(L(88, 91))], whole=True,
      rownote=quote(S(84), lead='The scheme heads it'),
      question=QP(4, Run('Ud fra din læsning', 'om det på ca. 100 ord.')),
      pages=(2, 3)),
    R('III1', [unprinted(quote(L(97, 98), lead='Under the two titles the scheme prints only'))],
      question=_titles(PL(4, 'Skriv et essay'), PL(4, 'Rigdom og velfærd'), PL(4, '”Den er rigest'))),
]


# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1 and III1. Live: I1-I6 (6 cards); not touched (audited: see
# danish-live-faults-2011-2017.json).
# Paper (rendered pp2-4): the instruction and the rule "Alle svar skal skrives
# på dansk." (p2 y78-92), "(Maksimum 100 point)" (p2 y105); the article "Dyrk
# din by – og spis den" runs pp2-3 (title p2 y130, the text to p3 y590, the
# editing note p3 y614); p4 holds all the questions: "Opgave I" / "(maksimum
# 30 point)" (p4 y77), Q1 five unlettered lines over "(5 × 1 point)" (y200),
# Q2-Q6 "(5 point)" each; "Opgave II" / "(maksimum 30 point)" (p4 y472), a
# quotation run into the task (y496-584); "Opgave III" / "(maksimum 40
# point)" (p4 y633), "Skriv et essay på cirka 300 ord om ét af disse to
# emner:" over two DASHED titles joined by "ELLER", the second with its
# attribution "Fintan O’Toole i The Irish Times, 22. februar 2016" set right
# under it (p4 y682-759): one ask, III1.
# PRICES:
# - II1: "(maksimum 30 point)" (PARTP). Scheme "Opgave II Total 30 marks" (91).
# - III1: "(maksimum 40 point)" (PARTP). Scheme "Part III Total 40 marks" (98).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; p2 the standard note, pp5-6
# blank):
# - Opgave II (91, p4): a descriptive line, 92, "Kommentar på ca. 100 ord som
#   viser evne til at sætte temaet ind i et større perspektiv."; then two
#   alternative paragraphs, 93-95 ("F.eks. kan man tage det approach, at
#   byhaverne blot er en poppet by-trend, ...") and 96-97 ("Eller man kan gå
#   med teksten ... byhaverne er den nye tids kapitalisme.").
# - Part III (98): both titles reprinted with their dashes and "eller"
#   (99-103), the second in OTHER words than the paper's (see 10f below),
#   then ONE descriptive line, 104-105, "Et velskrevet essay på ca. 300 ord,
#   relevant i forhold til hver sit emne, ... rimeligt flydende."
# - NO criteria anywhere this sitting (rendered pp3-4).
# SHAPES:
# - II1: the two paragraphs shown, priced as a whole on the paper's 30 (10a,
#   questionTotal); the descriptive line quoted as its head.
# - III1: only a descriptive line and no criteria: R4 (unprinted) at the
#   paper's 40, the note quoting the line (ruling 4).
# JUDGEMENT CALLS:
# - 10f, paper and scheme disagree on title 2: the paper prints "”Verden kan
#   blive et temmelig dårligt sted at være, hvis vi ikke arbejder sammen på at
#   gøre den mere lige, mere demokratisk og mere bæredygtig.”" (p4 y731-746);
#   the scheme reprints "... arbejder sammen på at skabe mere lighed, mere
#   demokrati og mere bæredygtighed i den.”" (101-102). The paper wins on the
#   question; the scheme's words are quoted on the row.
# - III1's question: stem and both titles, one per line (dashes and "ELLER"
#   left out); title 2 keeps its attribution, joined on its line (as 2014's
#   "Ralph Waldo Emerson").
# - II1's question is cut from the paper's lines (the census glues the head
#   cell's "(maksimum 30 point)" in front).
# - Reading text pp2-3 (rendered; p4 is questions only). The live Part I
#   cards carry sourceMaterial.pages [4], the QUESTIONS page: the render does
#   not agree (flagged, P).
# GLYPHS: none in the lines used. The scheme prints "byhavekulturens" etc.
# cleanly; "EU’s  grænseværdier" (95) has a double space on the render, read
# as one.

SPECS[2016] = [
    R('II1', [shown(L(93, 95)), shown(L(96, 97))], whole=True,
      rownote=quote(S(92), lead='The scheme heads it'),
      question=QP(4, Run('”Måske er det en modreaktion', 'dette emne på ca. 100 ord.')),
      pages=(2, 3)),
    R('III1', [unprinted(both(quote(L(104, 105), lead='Under the two titles the scheme prints only'),
                              quote(L(101, 102, after='- ”', before='”'), lead='It reprints the second title as')))],
      question=_titles(PL(4, 'Skriv et essay'), PL(4, 'Det gode menneske'),
                       J(PL(4, '”Verden kan blive'), PL(4, 'den mere lige'), PL(4, 'Fintan O’Toole')))),
]


# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the five open asks of this sitting,
# I1, I5, I6, II1, III1. Live: I2-I4 (3 cards); not touched (audited: see
# danish-live-faults-2011-2017.json).
# Paper (rendered pp2-4; it reprints 2014's article and Part I questions):
# the rule "Alle svar skal skrives på dansk." and "Maksimum 100 point" (p2
# y116); the article runs pp2-3 (to "naboer.«" p3 y600, the editing note p3
# y626); "Opgave I" / "(maksimum 30 point)" (p3 y671); Q1 prints FIVE
# UNLETTERED "Forklar betydningen af ..." lines, three on p3 (y699-768) and two
# on p4 (y82-116), and "(maks. 5 × 1 point)" at the right of the fifth (p4
# y116, a cell of its own); Q2-Q6 "(maks. 5 point)" each, Q5's and Q6's at
# the right of their LAST lines (p4 y353, y459); "Opgave II" / "(maksimum 30
# point)" (p4 y505); "Opgave III" / "(maksimum 40 point)" (p4 y639), "Skriv et
# essay på cirka 300 ord om ét af disse to emner:" over title 1 set as
# "-Personlige værdier ..." (y696), "eller" (y721) and title 2 with NO dash, a
# quotation and a task over three lines (y742-772): one ask, III1.
# PRICES:
# - I1: the census reads NO price (tariff None; it also keeps only the first
#   expression as the text), but the paper PRINTS "(maks. 5 × 1 point)" (p4
#   y116): 1 point per expression. Rows priced from that printed cell
#   (PaperP reads its "1 point"); the card's 5 read from the scheme's reprint
#   "(5 x 1 point)" (line 56, RX), the same figure (no sl_lib reader takes
#   the "5" of a paper's "5 × 1": PaperP reads "1 point", PY refuses "maks.").
# - I5, I6: the census reads NO price (tariff None), but the paper PRINTS
#   "(maks. 5 point)" at the right of each question's last line (p4 y353,
#   y459; rendered). PaperP cannot single them out (three p4 cells open
#   "(maks. 5 point)", y210/y353/y459) and PY's cell pattern refuses "maks.",
#   so each is priced from the scheme's own "(5 point)" under its answer
#   (SP(83), SP(87)), the same 5. If the lead extends PY to take "(maks. N
#   point)", PY(4, 353) / PY(4, 459) are the paper's cells. Not 10i: the
#   exclusion's "neither document states a tariff" is wrong.
# - II1: "(maksimum 30 point)" (PARTP); scheme "Opgave II (Total 30 point)" (88).
# - III1: "(maksimum 40 point)" (PARTP); scheme "Opgave III (Total 40 point)" (97).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; p2 the standard note, pp5-6
# blank):
# - Q1 (48-56): five "Enhver rimelig forklaring (e.g. ”...”)" entries in the
#   paper's order, the second and fourth wrapped (49-51, 53-54), then "(5 x 1
#   point)". Paired by words: bjælkehus / "et gammeldags hus opført af
#   træbjælker" (48); værdier / "Værdier er kulturelt bestemte opfattelser
#   ..." (49-51); "et stort og vildt spring ud over kanten" / "et valg, der
#   medfører en radikal forandring i livsstil" (52); nøjsomhed / "livsstil,
#   hvor man klarer sig med eller er tilfreds med lidt" (53-54); "tæskede mig
#   selv" / "at bebrejde eller kritisere sig selv" (55).
# - Q5 (80-83): one paragraph, "Ligesom de amerikanske ”Preppers” forbereder
#   familien sig ... bliver selvforsynende.", "(5 point)".
# - Q6 (84-87): one paragraph, "Den moderne livsstil er præget af trends, ...
#   tage afstand fra.", "(5 point)".
# - Opgave II (88): a descriptive line, 89-90, "En kommentar på ca. 100 ord,
#   som viser evne til at forstå Hjelskovs syn på det moderne samfund."; then
#   one paragraph, 91-96, "Hjelskov baserer bl.a. sin påstand på sin datters
#   veninde, ... den autentiske livsstil."
# - Opgave III (97): both titles reprinted (98-102), then ONE descriptive
#   line, 103-105, "Et velskrevet essay på ca. 300 ord, relevant i forhold
#   til hver sit emne, ... rimeligt flydende sprog."
# - NO criteria anywhere this sitting (rendered pp3-4).
# SHAPES:
# - I1: one card (one ask), a row per expression, each one(gloss) at the
#   paper's 1 point, adding to 5; each row led by its expression.
# - I5, I6: one printed paragraph each = one row at the printed 5 (the shape
#   of this sitting's live I2-I4 and of 2014's I5/I6).
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a,
#   questionTotal); the descriptive line quoted as its head.
# - III1: only a descriptive line and no criteria: R4 (unprinted) at the
#   paper's 40, the note quoting the line (ruling 4).
# JUDGEMENT CALLS:
# - Q1 rows keep the scheme's whole entry, "Enhver rimelig forklaring (e.g.
#   ”...”)", the wrapped ones joined (49-51, 53-54).
# - I1's question: the five printed lines, one per line (QL); the census
#   keeps only the first. I5's and I6's questions are cut from the paper's
#   lines (Run): the census keeps only each one's FIRST text line ("... hvis
#   de", "... for at give"), not the task sentence.
# - I5 and I6 one claimable row each, not shown: each answer is one stated
#   reading of the quotation, as the live I2-I4 of this sitting. If the lead
#   prefers self-assessment for these, flip to shown, whole=True.
# - II1's question is cut from the paper's lines (the census glues the head
#   cell's "(maksimum 30 point)" in front).
# - III1's question: stem, title 1 (its dash, printed against the word, cut
#   off), title 2's three lines joined; "eller" left out.
# - Reading text pp2-3 (rendered; p2 holds the title and the first half). The
#   live I2-I4 carry sourceMaterial.pages [3]: the render does not agree
#   (flagged, P).
# GLYPHS: none in the lines used (æ ø å clean; the scheme spells the author
# "Hjelskov", the paper "Hejlskov": the SEC's typing, kept in the rows).

Q1P_2017 = PaperP(4, '(maks. 5 × 1 point)')
Q1T_2017 = RX(56, r'\((\d)\s*x\s*1\s*point\)')


def _word(page, opening):
    """The expression a Q1 line prints between its quotation marks."""
    return PC(page, opening, after='”', before='”')


SPECS[2017] = [
    R('I1', [one(S(48, after='1. '), Q1P_2017, lead=_word(3, '1. Forklar betydningen af ordet ”bjælkehus”')),
             one(L(49, 51), Q1P_2017, lead=_word(3, 'Forklar betydningen af ordet ”værdier”')),
             one(S(52), Q1P_2017, lead=_word(3, 'Forklar betydningen af ordene ”et stort')),
             one(L(53, 54), Q1P_2017, lead=_word(4, 'Forklar betydningen af ordet ”nøjsomhed”')),
             one(S(55), Q1P_2017, lead=_word(4, 'Forklar betydningen af ordene ” tæskede'))],
      total=Q1T_2017,
      question=QL(3, '1. Forklar betydningen af ordet ”bjælkehus”',
                  'Forklar betydningen af ordet ”værdier”', 'Forklar betydningen af ordene ”et stort',
                  (4, 'Forklar betydningen af ordet ”nøjsomhed”'), (4, 'Forklar betydningen af ordene ” tæskede')),
      pages=(2, 3)),
    R('I5', [one(L(80, 82, after='5. '), SP(83))], total=SP(83),
      question=QP(4, Run('5. ”Det påvirker', 'som Andrea Hejlskov gør sig')), pages=(2, 3)),
    R('I6', [one(L(84, 86, after='6. '), SP(87))], total=SP(87),
      question=QP(4, Run('6. ”Vi er helt sikkert', 'ser pænere ud.”')), pages=(2, 3)),
    R('II1', [shown(L(91, 96))], whole=True,
      rownote=quote(L(89, 90), lead='The scheme heads it'),
      question=QP(4, Run('”De unge i vores', 'bedste af alle'), Run('Hvorfor tror du', 'konklusion?')),
      pages=(2, 3)),
    R('III1', [unprinted(quote(L(103, 105), lead='Under the two titles the scheme prints only'))],
      question=_titles(PL(4, 'Skriv et essay'), PC(4, '-Personlige', after='-'),
                       J(PL(4, '”Min holdning'), PL(4, 'Diskuter dette synspunkt'), PL(4, 'medier.')))),
]


def specs(year):
    return SPECS.get(year, [])
