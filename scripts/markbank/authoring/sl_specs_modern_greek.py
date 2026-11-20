#!/usr/bin/env python3
"""Reviewed specs for the Modern Greek examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/modern-greek/schemes/<year>-hl.md.
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
# Drafted (small-languages lane, 20 Nov): the three open asks of this
# sitting, S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (mgr-2010-hl-1-1 .. -1-6); not
# touched (audited: modern-greek-live-faults-2010-2016.json).
# Paper (rendered pp2-4; the text layer sets most spaces as U+00A0, so the
# openings below are single words or carry "\xa0"): the rule "Να απαντήσετε
# και στις 3 ομάδες ερωτήσεων. Οι απαντήσεις να δοθούν στα νέα Ελληνικά."
# (p2 y102); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ (30/100)" over the
# article (p2 y128-157); the article "Η ΣΥΓΧΡΟΝΗ ΚΑΤΑΝΑΛΩΤΙΚΗ ΚΟΙΝΩΝΙΑ" (p2
# y212), four numbered paragraphs, to its source line "... εκδ. Σαββάλας"
# (p3 y448); "ΟΜΑΔΑ 1η (30/100)" again over the questions (p3 y497), Q1-Q6
# "(5 βαθμοί)" each (live); "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ (30/100)" (p4 y357), ONE
# unnumbered task (p4 y383-413); "ΟΜΑΔΑ 3η ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ (40/100)" (p4
# y478), the instruction (y517-533) and two titles "1ο θέμα:" / "2ο θέμα:".
# PRICES: S2 the group head's "(30/100)" (PARTP, the walker reads 30);
# S3Q1/S3Q2 "(40/100)" (PARTP, 40). The scheme prints the same heads (78-79,
# 85-86). No other price is printed for any of the three.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3):
# - S2 (78-82 reprint the head and the task, word for word): one italic
#   sentence of model commentary, 83-84 ("Δημιουργείται μια ψευδαίσθηση ...
#   χρονικό διάστημα"), no mark inside it.
# - S3 (85-88 reprint the head and the instruction; 93-94 and 100-101 each
#   title, word for word): under title 1 five bullets, 95-99 ("Η φιλία" ...
#   "κλπ"); under title 2 four bullets, 102-105.
# - Criteria (p4, 106-115): "ΣΗΜΕΙΩΣΗ:" (106, a heading) then "Στη 2η και
#   3η ομάδα ερωτήσεων τα ακόλουθα στοιχεία συνυπολογίζονται στη
#   βαθμολογία:" (107-108) -- for groups 2 AND 3 -- then four numbered
#   criteria printing "(30%)" (110), "(30%)" (112), "(30%)" (114), "(10%)"
#   (115): 100 %.
# SHAPES:
# - S2: graded (10b), 30/30/30/10 % of the printed 30 = 9/9/9/3. No
#   descriptive line is printed for the group, so the head is the criteria's
#   own lead (107-108), as Latvian 2010; the model sentence quoted as
#   examples, not a checklist (10a), as Latvian/Estonian Part II.
# - S3Q1/S3Q2: graded (10b), 12/12/12/4 of 40, head the criteria's lead;
#   each title's own bullets quoted as examples (10a), "κλπ" included as the
#   scheme prints it (the list's own last bullet).
# JUDGEMENT CALLS:
# - Each essay card's question is the instruction printed over both titles
#   and the title (prerun: the run of the instruction's two printed lines,
#   then the census title); "1ο θέμα:" is the title's number, cited Section 3
#   Q1/Q2 as the census keys it.
# - S2's question is the census text, checked against p4 (the task as
#   printed, no price; "( 2η παράγραφος)" spaced as printed).
# - Reading text: pp2-3 (rendered: title p2 y212, paragraphs 1-4 and the
#   source line on p3 to y448; p3 y497 on holds only questions). S2 carries
#   pages=(2, 3) and source='text': sl_lib attaches sourceMaterial only to
#   sections 'I'/'II' or source='text', and the Modern Greek keys are
#   '1'/'2'/'3', so without it the S1/S2 cards carry NO reading text (lead:
#   runtime gap, flagged). The live S1 cards' sourceMaterial.pages [2, 3]
#   AGREE with the render.
# GLYPHS: none in the lines used (paper and scheme: Greek letters, tonos and
# punctuation only; checked on the render). Lifted as printed: "πως" for
# "πώς" (task), "τα περιεχόμενο" (task), "μόνον ότι  δε μπορεί" (102).

CRIT_2010 = crit((109, 110), (111, 112), (113, 114), 115)
HEAD_2010 = L(107, 108)
ESSAY_2010 = prerun(4, 'Να\xa0διαλέξεις', 'περίπου')

SPECS[2010] = [
    R('S2', [graded(HEAD_2010, PARTP(), CRIT_2010)],
      rownote=examples(None, L(83, 84)), pages=(2, 3), source='text'),
    R('S3Q1', [graded(HEAD_2010, PARTP(), CRIT_2010)],
      rownote=examples(None, S(95), S(96), S(97), S(98), S(99)),
      question=ESSAY_2010),
    R('S3Q2', [graded(HEAD_2010, PARTP(), CRIT_2010)],
      rownote=examples(None, S(102), S(103), S(104), S(105)),
      question=ESSAY_2010),
]


# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this
# sitting, S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (mgr-2011-hl-1-1 .. -1-6); not
# touched (audited: modern-greek-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Να απαντήσετε και στις 3 ομάδες
# ερωτήσεων. Οι απαντήσεις να δοθούν στα νέα Ελληνικά." (p2 y89); the article
# "Η ΜΟΛΥΝΣΗ ΤΟΥ ΠΕΡΙΒΑΛΛΟΝΤΟΣ" (p2 y124-159), nine numbered paragraphs, to
# its source line "... 12ου Ενιαίου Λυκείου Περιστερίου" (p3 y168);
# "Ερωτήσεις: (οι απαντήσεις να δοθούν στα Νεοελληνικά ...)" (p3 y208);
# "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ (συνολική βαθμολογία 30 βαθμοί , 6 Χ
# 5 )" (p3 y264-277), Q1-Q6 (live); "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ (βαθμολογία 30
# βαθμοί)" (p4 y93), ONE unnumbered task (y136-162); "ΟΜΑΔΑ 3η ΕΚΘΕΣΗ
# ΔΟΚΙΜΙΟ (βαθμολογία 40 βαθμοί)" (p4 y252), the instruction (y293-307) and
# the titles "1ο θέμα:" (y346) / "2ο θέμα:" (y416). Every page carries the
# footer "Page N of 4" (y811).
# PRICES: S2 the group head's "(βαθμολογία 30 βαθμοί)" (PARTP, the walker
# reads 30); S3Q1/S3Q2 "(βαθμολογία 40 βαθμοί)" (PARTP, 40). The scheme
# prints the same heads (53, 60).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 2-3):
# - S2 (53-56 reprint the head and the task, word for word): one paragraph
#   of model commentary, 57-59 ("Το πρόβλημα της μόλυνσης δημιουργήθηκε ...
#   τα πάντα"), no mark inside it.
# - S3 (60-68 reprint the head, the instruction and both titles, word for
#   word, typos included): no model, no points under either title.
# - Criteria (p5, 73-81): "ΣΗΜΕΙΩΣΗ:" (73, a heading) then "Στη 2η και 3η
#   ομάδα ερωτήσεων τα ακόλουθα στοιχεία συνυπολογίζονται στη βαθμολογία:"
#   (74) -- for groups 2 AND 3 -- then four numbered criteria printing
#   "(30%)" (76), "(30%)" (78), "(30%)" (80), "(10%)" (81): 100 %.
# SHAPES:
# - S2: graded (10b), 9/9/9/3 of the printed 30; head the criteria's lead
#   (74, no descriptive line printed); the model paragraph quoted as
#   examples, not a checklist (10a).
# - S3Q1/S3Q2: graded (10b), 12/12/12/4 of 40; head the criteria's lead. The
#   scheme prints the criteria for the essay and nothing else, so no R4 line.
# JUDGEMENT CALLS:
# - S3Q2's census text runs on into the page footer "Page 4 of 4" (p4
#   y811): its question is cut from the paper's own lines (the instruction,
#   then the title's two printed lines, "... στον ηλεκρονικό κόσμο" / "μας;").
#   S3Q1: the instruction, then the census title (checked against p4 y376).
# - S2's question is the census text, checked against p4 y136-162 (no price,
#   no footer).
# - Reading text: pp2-3 (rendered: title p2 y124, paragraphs 1-7 on p2, 8-9
#   and the source line on p3 to y168; p3 y208 on holds only questions):
#   S2 pages=(2, 3), source='text' (see the 2010 note on the runtime gap).
#   The live S1 cards' sourceMaterial.pages [2, 3] AGREE.
# GLYPHS: none in the lines used. Lifted as printed: "πιστευετε" (no tonos)
# and "ηλεκρονικό" (title 2, paper and scheme alike), "τη τελευταία φράση"
# (task).

CRIT_2011 = crit((75, 76), (77, 78), (79, 80), 81)
HEAD_2011 = S(74)
INSTR_2011 = Run('Να επιλέξετε', 'περίπου')

SPECS[2011] = [
    R('S2', [graded(HEAD_2011, PARTP(), CRIT_2011)],
      rownote=examples(None, L(57, 59)), pages=(2, 3), source='text'),
    R('S3Q1', [graded(HEAD_2011, PARTP(), CRIT_2011)],
      question=prerun(4, 'Να επιλέξετε', 'περίπου')),
    R('S3Q2', [graded(HEAD_2011, PARTP(), CRIT_2011)],
      question=QP(4, INSTR_2011, Run('Τι πιστευετε', 'μας;'))),
]


# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this
# sitting, S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (mgr-2012-hl-1-1 .. -1-6); not
# touched (audited: modern-greek-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the article "ΓΙΑΤΙ ΜΑΣ ΣΥΝΕΠΑΙΡΝΕΙ ΤΟ
# ΠΟΔΟΣΦΑΙΡΟ;" (p2 y177), six numbered paragraphs, to its source line
# "Δημήτρης Δημητράκος, εφημερίδα. ΤΟ ΒΗΜΑ, 05/07/1998" (p3 y399);
# "ΕΡΩΤΗΣΕΙΣ" and the rule (p3 y426-467); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ
# ΕΡΜΗΝΕΙΑ [30 / 100]" (p3 y492-522), Q1-Q6 "(5 βαθμοί)" each (live);
# "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (p4 y310-337), ONE unnumbered task
# (y374-422); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (p4 y504-530), the
# instruction (y555-568) and the titles "1ο θέμα:" (y599) / "2οθέμα:" (y665,
# printed with no space; the walker's THEME reads it).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints "(30/100)" (69) and "(40/100)" (82).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 2-3; no
# criteria, no notes anywhere in this scheme):
# - S2 (68-72): the head and a REWORDED reprint of the task: the quoted
#   phrase lacks the paper's "να πάει κόντρα δηλαδή" ("Κανένας δεν τολμά να
#   αντιπαρατεθεί ή να περιφρονήσει ανοιχτά αυτόν τον μοντέρνο Θεό.", 71-72).
#   Then ONE paragraph of model commentary, 73-77 ("Το ποδόσφαιρο ενώνει
#   τους ανθρώπους, ... τις διαφωνίες τους."), no mark inside it.
# - S3Q1 (85-87 reprint the title, "μυαλό , σε": spacing only): one
#   paragraph, 88-89 ("Ο αθλητισμός και η φροντίδα ... του πνεύματος.").
# - S3Q2 (90-91): the scheme reprints the title REWORDED, "Στη σύγχρονη
#   κοινωνία τους το κάθε τι είναι επικεντρωμένο στο εδώ και το τώρα." where
#   the paper prints "κοινωνία μας" and "εδώ και τώρα"; then one paragraph,
#   92-97 ("Μεγάλο μέρος της κοινωνίας μας ... ή να περιμένουν.").
# SHAPES (10a: a model the scheme prices only as a whole, no criteria):
# - S2: the paragraph, one shown row, whole=True on the printed 30.
# - S3Q1, S3Q2: the paragraph, one shown row, whole=True on the printed 40.
# JUDGEMENT CALLS:
# - The paper's words stand in the question; the scheme's reworded reprints
#   of S2's phrase and S3Q2's title are quoted on the row (10f).
# - Essay questions: the instruction printed over both titles, then the
#   census title (prerun; titles checked against p4 y621-688).
# - Reading text: pp2-3 (rendered: title p2 y177, paragraphs 1-4 on p2, 4
#   cont.-6 and the source line on p3 to y399): S2 pages=(2, 3),
#   source='text'. The live S1 cards' sourceMaterial.pages [2, 3] AGREE.
# GLYPHS: none in the lines used. Lifted as printed: "πως" (task),
# "χρόνο, κόπο, υπομονή και όνειρα" (93, "όνειρα" twice in the sentence),
# "για ότι" (95).

ESSAY_2012 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2012] = [
    R('S2', [shown(L(73, 77))], whole=True,
      rownote=quote(L(71, 72), lead='The scheme reprints the phrase as'),
      pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(88, 89))], whole=True, question=ESSAY_2012),
    R('S3Q2', [shown(L(92, 97))], whole=True,
      rownote=quote(S(91), lead='The scheme reprints the title as'),
      question=ESSAY_2012),
]


# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this
# sitting, S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (mgr-2013-hl-1-1 .. -1-6); not
# touched (audited: modern-greek-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the article "Κοινωνία σε κρίση, πολίτες σε δράση"
# (p2 y121), nine numbered paragraphs, to its byline "Ισμαηλίδου Έλλη,
# Πουλιόπουλος Γιώργος, Το Βήμα , 18/12/2011" and "(κείμενο διασκευασμένο
# ... 790 λέξεις)" (p3 y531-544); "ΕΡΩΤΗΣΕΙΣ" and the rule (p3 y571-598);
# "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 100]" (p3 y623-638), Q1-Q6
# "(5 βαθμοί)" each (live); "ΟΜΑΔΑ 2η ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (p4 y394), ONE
# unnumbered task (y433-473); "ΟΜΑΔΑ 3η ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (p4 y581),
# the instruction (y606-619) and the titles "1ο θέμα:" (y650) / "2ο θέμα:"
# (y711).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (92, 100).
# WHAT THE SCHEME PRINTS (rendered scheme p4 = printed page 2; no criteria,
# no notes anywhere in this scheme):
# - S2 (92-95): the head and the task, REWORDED: "... πως καταλαβαίνετε την
#   έκφραση:" (93) where the paper prints "... την φράση:" (p4 y433); the
#   quotation itself word for word. Then ONE paragraph of model commentary,
#   96-99 ("Η προσφορά των μεμονωμένων ατόμων ... κοινωνικών εξεγέρσεων.
#   Κλπ…."), no mark inside it.
# - S3Q1 (103-104 reprint the title, word for word): one paragraph, 105-108
#   ("Από τη συνεργασία και την αλληλεγγύη ... του ιδιώτ . Kλπ……").
# - S3Q2 (109-110 reprint the title, "σου - ένα": dash only): one paragraph,
#   111-113 ("Το ταξίδι της ζωής του καθενός ... γεμάτης όνειρα. Κλπ…..").
# SHAPES (10a: a model the scheme prices only as a whole, no criteria):
# - S2: the paragraph, one shown row, whole=True on the printed 30.
# - S3Q1, S3Q2: the paragraph, one shown row, whole=True on the printed 40.
# JUDGEMENT CALLS:
# - Each paragraph ends with the scheme's own "Κλπ…." ("etc."): kept, as it
#   is printed inside the paragraph and says the model is open-ended.
# - S2: the paper's words stand in the question; the scheme's reworded line
#   93 is quoted on the row (10f).
# - Essay questions: the instruction printed over both titles, then the
#   census title (prerun; the paper prints "Η  αξία" with two spaces, the
#   census and the scheme one).
# - Reading text: pp2-3 (rendered: title p2 y121, paragraphs 1-6 on p2, 6
#   cont.-9 and the byline on p3 to y544): S2 pages=(2, 3), source='text'.
#   The live S1 cards' sourceMaterial.pages [2, 3] AGREE.
# GLYPHS (scheme, S3Q1's row; glyph ids read with get_texttrace, font
# Calibri,BoldItalic): line 107 "ανaγκη" carries a LATIN a (U+0061, glyph
# 258; the font's α is glyph 626, ά 627) and line 108 "Kλπ" a LATIN K
# (U+004B, glyph 60; Κ is glyph 574). Real Latin glyphs, the SEC's own
# typing (rendered at 400 dpi: indistinguishable in this italic), not a font
# map: lifted as printed and flagged for the lead. Also as printed: "ιδιώτ ."
# (108, the word cut short, rendered so).

ESSAY_2013 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2013] = [
    R('S2', [shown(L(96, 99))], whole=True,
      rownote=quote(S(93), lead='The scheme reprints the task as'),
      pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(105, 108))], whole=True, question=ESSAY_2013),
    R('S3Q2', [shown(L(111, 113))], whole=True, question=ESSAY_2013),
]


# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this
# sitting, S1Q2-S1Q6, S2, S3Q1, S3Q2. Live: S1Q1 (mgr-2014-hl-1-1); not
# touched (audited: modern-greek-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the article "ΣΕ ΚΡΙΣΗ ΤΑΥΤΟΤΗΤΑΣ Η ΕΥΡΩΠΑΪΚΗ
# ΜΕΣΑΙΑ ΤΑΞΗ" (p2 y184), eight numbered paragraphs, to "(κείμενο ελαφρά
# διασκευασμένο ...) 710 λέξεις" / "Newsit.gr, 12/11/2013 , 9:30, Πηγή
# EURO2DAY" (p3 y645-660); "ΕΡΩΤΗΣΕΙΣ" and the rule (p3 y701-743); p4:
# "ΟΜΑΔΑ 1η" (y72) / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ" with "[30 / 100]" at the right
# (y102); Q1 "1) ..." with "(5 βαθμοί)" (y144) over five bullets (live);
# Q2-Q6 "2)" to "6)" (y243-371) with NO price; "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ
# [30 / 100]" (y421-448), ONE unnumbered task (y468-521); "ΟΜΑΔΑ 3η" /
# "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (y562-588), the instruction (y613-626), the
# titles "1ο θέμα:" (y657) / "2ο θέμα:" (y703), title 2 a quotation signed
# "Ralph Waldo Emerson" (y755).
# PRICES:
# - S1Q2-S1Q6: NO price on the paper (rendered p4: no bracketed number and
#   no "βαθμ" anywhere from "2)" to "6)") and none on the scheme (rendered
#   pp3-4: lines 59-114 print no number but the questions' own). The paper
#   prints "[30 / 100]" for ΟΜΑΔΑ 1η and "(5 βαθμοί)" for Q1 alone, so five
#   unpriced asks share what is left: CARD-STANDARD 10i, never split (not a
#   REM: two or more asks). Unpriced(PL(4, 'ΟΜΑΔΑ 1η'), PARTP()) -> label
#   "ΟΜΑΔΑ 1η", total 30 (the walker reads the group head's 30).
# - S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40). The
#   scheme prints the same heads (116, 135).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 2-4; no
# criteria, no notes anywhere in this scheme):
# - Q2 (59-60 reprint): one italic paragraph, 61-65.
# - Q3 (66 reprint): one italic paragraph, 67-77.
# - Q4 (78-80): the question REWORDED, "... δημιουργούν κάποιου είδους
#   κρίση για αυτούς;" where the paper prints "... δημιουργούν κάποια κρίση
#   για αυτούς;"; then one italic paragraph, 85-100, opening the next page
#   (81-84 are the page number and the page marker, before it).
# - Q5 (101 reprint): one italic paragraph, 102-106.
# - Q6 (107 reprint): one italic paragraph, 108-114.
# - S2 (115-120 reprint the head and the task, word for word): one italic
#   paragraph of model commentary, 125-133, no mark inside it.
# - S3Q1 (138-139 reprint the title): two bullets, 140 ("Ta χαρακτηριστικά
#   του επαγγέλματος") and 141-144 ("H θετική προσφορά ... (επιβεβαίωση ...
#   της κοινωνίας)").
# - S3Q2 (145-148 reprint the title and its signature, with an extra comma
#   "μέσα μας , γιατί": punctuation only): one paragraph, 149-155.
# SHAPES:
# - S1Q2-S1Q6: 10i (unpriced): the paragraph as one shown row, no marks.
# - S2: the paragraph, one shown row, whole=True on the printed 30 (10a).
# - S3Q1: the two bullets, two shown rows, whole=True on 40 (10a).
# - S3Q2: the paragraph, one shown row, whole=True on 40 (10a).
# JUDGEMENT CALLS:
# - S1Q4: the paper's words stand in the question; the scheme's reworded
#   reprint is quoted on the row (10f).
# - Questions: S1Q2-S1Q6 and S2 are the census text, checked against p4
#   (no price, wrapped lines joined, "πολιτικών , των" spaced as printed).
#   Essays: the instruction, then the census title (title 2 with its printed
#   signature "Ralph Waldo Emerson", which the paper sets under it).
# - Reading text: pp2-3 (rendered: title p2 y184, paragraphs 1-4 on p2, 4
#   cont.-8 and the source lines on p3 to y660; p4 holds only questions):
#   pages=(2, 3), source='text' on S1Q2-S1Q6 and S2 (see the 2010 note on
#   the runtime gap). The live S1Q1 card's sourceMaterial.pages [2, 3] AGREE.
# GLYPHS (scheme, S3Q1's rows; glyph ids read with get_texttrace, font
# TimesNewRoman,BoldItalic): line 140 "Ta" is LATIN T + a (U+0054 glyph 55,
# U+0061 glyph 68; the font's Τ is glyph 521, α glyph 302) and line 141 "H"
# a LATIN H (U+0048 glyph 43; Η is glyph 510). Real Latin glyphs, the SEC's
# own typing (identical on the render), not a font map: lifted as printed,
# flagged for the lead. Latin words the paper itself prints (Mac, Twitter,
# Amazon, Bauman) are names. Also as printed: "διαδικτύωσης" (103), "γι
# 'αυτό" (99), "Ιντερνέτ" (87).

U1_2014 = Unpriced(PL(4, 'ΟΜΑΔΑ 1η'), PARTP())
ESSAY_2014 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2014] = [
    R('S1Q2', [shown(L(61, 65))], unpriced=U1_2014, pages=(2, 3), source='text'),
    R('S1Q3', [shown(L(67, 77))], unpriced=U1_2014, pages=(2, 3), source='text'),
    R('S1Q4', [shown(L(85, 100))], unpriced=U1_2014,
      rownote=quote(L(78, 80, after='4. '), lead='The scheme reprints the question as'),
      pages=(2, 3), source='text'),
    R('S1Q5', [shown(L(102, 106))], unpriced=U1_2014, pages=(2, 3), source='text'),
    R('S1Q6', [shown(L(108, 114))], unpriced=U1_2014, pages=(2, 3), source='text'),
    R('S2', [shown(L(125, 133))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(S(140)), shown(L(141, 144))], whole=True, question=ESSAY_2014),
    R('S3Q2', [shown(L(149, 155))], whole=True, question=ESSAY_2014),
]


# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): all nine asks of this sitting,
# S1Q1-S1Q6, S2, S3Q1, S3Q2. No live card (the old reader refused the whole
# scheme as unreadable).
# Paper (rendered pp2-4; clean text layer): the article "Πώς μετριέται η
# ευτυχία;" (p2 y150), six numbered paragraphs, to "840 λέξεις (κείμενο
# διασκευασμένο ...) Ασπασία Δασκαλοπούλου 13.10.2014 , εφημερίδα ,ΤΟ ΒΗΜΑ"
# (p3 y545-558); "ΕΡΩΤΗΣΕΙΣ" and the rule (p3 y581-623); "ΟΜΑΔΑ 1η" /
# "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 100]" (p3 y648-677); Q1 "1) ..." with "(5
# βαθμοί)" (p3 y720) over five bullets (p3 y733 - p4 y104); Q2-Q6 "2)" to
# "6)", each "(5 βαθμοί)" at the right (p4 y150, 193, 240, 284, 328);
# "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (p4 y366-393), ONE unnumbered task
# (y419-471); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (p4 y514-540), the
# instruction (y565-578), the titles "1ο θέμα:" (y609) / "2ο θέμα:" (y669).
# PRICES: S1Q1-S1Q6 each the paper's own "(5 βαθμοί)" (PP: the walker reads
# 5 for each); S1Q1's covers the five expressions together (no per-
# expression mark on paper or scheme). S2 "[30 / 100]" (PARTP, 30);
# S3Q1/S3Q2 "[40 / 100]" (PARTP, 40). The scheme prints "(5 βαθμοί)" on Q1
# only (54) and the same group heads (52, 120, 137).
# THE SCHEME'S TEXT LAYER was mangled (two broken ToUnicode maps) and has been
# repaired into examiner-reports/modern-greek/schemes/2015-hl.md. Every row
# below was read against the rendered scheme (pp3-6, and 300-400 dpi crops
# of every word the check below flagged): see GLYPHS.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-6 = printed pages 2-5; no
# criteria, no notes):
# - Q1 (53-54 reprint the stem with "(5 βαθμοί)"): a two-column table, the
#   expression on the left as the paper prints it, its gloss in bold on the
#   right (55-59): "οικονομική πρόοδος, καλοπέραση" / "καθορίσουμε,
#   διακρίνουμε, καταλάβουμε" / "να διαλέξεις" / "δημιουργείς, τραβάς" /
#   "έχει παρατηρήσει". No split of the 5.
# - Q2-Q6 (each reprints its question, no price): ONE bold paragraph each,
#   Q2 62-73, Q3 76-98 (over the page break, 85-88 the page number and
#   marker), Q4 101-104, Q5 107-113, Q6 115-118. No mark inside any.
# - S2 (119-128 reprint the head and the task, "την ευτυχία, που": an extra
#   comma only): ONE bold paragraph of model commentary, 129-135.
# - S3Q1 (140-142 reprint the title): FOUR bold paragraphs, set apart by
#   space on the render: 143-149, 150-155, 156-160, 161-162.
# - S3Q2 (167-168 reprint the title): two runs of bold text, 169-172 ("Ο
#   άνθρωπος ... ικανοποιημένος .") and 173-177 ("Ο Σωκράτης ... πλούσιο."),
#   the second opening a new line after a short line (rendered p6).
# SHAPES:
# - S1Q1: one shown row per gloss (the scheme prints no split), whole=True
#   on the printed 5 (questionTotal), each row led by its expression as the
#   paper prints it (lead: "For “...”"), as Croatian 2015 and Czech 2015 Q1.
# - S1Q2-S1Q6: one printed paragraph each -> ONE claimable row, one(sel,
#   PP()) at the paper's 5 (lane convention).
# - S2: the paragraph, one shown row, whole=True on 30 (10a).
# - S3Q1: four shown rows, one per printed paragraph, whole=True on 40.
# - S3Q2: two shown rows, whole=True on 40.
# JUDGEMENT CALLS:
# - S3Q2: the scheme sets no space between its two runs, but breaks the
#   line after "ικανοποιημένος ." (rendered p6, the line ends at about two
#   thirds of the measure) and opens "Ο Σωκράτης" on a new line: read as two
#   paragraphs, two shown rows. If the lead reads one paragraph: one shown
#   row L(169, 177).
# - S1Q1's question: the printed stem's two lines and the five printed
#   expressions, one per line, their bullets taken off (_q1; QL keeps a
#   printed marker, which is a letter elsewhere and a bare bullet here).
#   S1Q2-S1Q6, S2: the census text, checked against p4 (no price; wrapped
#   lines joined). Essays: the instruction, then the census title.
# - Reading text: pp2-3 (rendered: title p2 y150, paragraphs 1-4 on p2, 4
#   cont.-6 and the source lines on p3 to y558): pages=(2, 3), source='text'
#   on S1Q1-S1Q6 and S2 (see the 2010 note on the runtime gap). No live card
#   of this sitting to compare.
# GLYPHS (the repaired .md, checked 20 Nov): NO wrong letter found in any
# lifted row. (1) Q2-Q5's rows repeat the article: word-diffed against this
# sitting's paper (clean text layer) they agree letter for letter; the only
# differences are two commas the paper prints and the scheme does not
# ("περίπτωση," p2 y540, "Ένα," p2 y715), and the render of the scheme
# confirms the scheme has neither. (2) Every other word of every lifted row
# (Q1 glosses, Q6, S2, S3Q1, S3Q2; 72 Greek words found in no other Modern
# Greek paper or scheme, plus "tablet") is a correctly accented Greek word
# (or that one printed English word), and those rows were
# read line by line against 200 dpi crops of scheme pp3-6: every letter and
# tonos agrees. Every character of the rows is U+0386-U+03CE Greek, ASCII
# or «» punctuation; the one Latin word is "tablet" (149), printed so.
# Lifted as printed: "σ αυτήν" (71, no apostrophe, as the paper p2 y540),
# "τη κοινή" (154), "συναισθήματα αξίες" (132, no comma).

import re as _re


def _q1(page, stem, *items):
    """Q1's printed stem and its printed expressions, one per line, each
    without its bullet."""
    ql = QL(page, stem, *items)

    def q(d, _census=None):
        lines = ql(d).split('\n')
        return '\n'.join([lines[0]] + [_re.sub(r'^[•●]\s*', '', x) for x in lines[1:]])
    return q


def _expr(page, opening):
    """An expression as the paper prints it under Q1, its bullet and its
    printed trailing comma taken off."""
    return PC(page, opening, after='• ', before=',') if opening != '• έχει' else PC(page, opening, after='• ')


ESSAY_2015 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2015] = [
    R('S1Q1', [shown(S(55, after='οικονομική ευημερία, '), lead=_expr(3, '• οικονομική')),
               shown(S(56, after='προβλέψουμε, '), lead=_expr(3, '• προβλέψουμε')),
               shown(S(57, after='να επιλέξεις, '), lead=_expr(4, '• να επιλέξεις')),
               shown(S(58, after='φτιάχνεις, '), lead=_expr(4, '• φτιάχνεις')),
               shown(S(59, after='έχει εντοπίσει '), lead=_expr(4, '• έχει'))],
      whole=True, total=PP(),
      note=('The paper prices Question 1 only as a whole, beside its stem; the scheme glosses each '
            'expression and prints no split.'),
      question=_q1(3, Run('1)', 'που'), '• οικονομική', '• προβλέψουμε', (4, '• να'), (4, '• φτιάχνεις'),
                   (4, '• έχει')),
      pages=(2, 3), source='text'),
    R('S1Q2', [one(L(62, 73), PP())], total=PP(), pages=(2, 3), source='text'),
    R('S1Q3', [one(J(L(76, 84), L(89, 98)), PP())], total=PP(), pages=(2, 3), source='text'),
    R('S1Q4', [one(L(101, 104), PP())], total=PP(), pages=(2, 3), source='text'),
    R('S1Q5', [one(L(107, 113), PP())], total=PP(), pages=(2, 3), source='text'),
    R('S1Q6', [one(L(115, 118), PP())], total=PP(), pages=(2, 3), source='text'),
    R('S2', [shown(L(129, 135))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(143, 149)), shown(L(150, 155)), shown(L(156, 160)), shown(L(161, 162))],
      whole=True, question=ESSAY_2015),
    R('S3Q2', [shown(L(169, 172)), shown(L(173, 177))], whole=True, question=ESSAY_2015),
]


# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): all nine asks of this sitting,
# S1Q1-S1Q6, S2, S3Q1, S3Q2. No live card (the old reader refused the six
# comprehension asks as unpriced and the writing tasks as models).
# Paper (rendered pp2-4): the rule "Να απαντήσετε και στις 3 ομάδες." /
# "Όλες οι απαντήσεις να δοθούν στα νέα ελληνικά." (p2 y122-147); "ΟΜΑΔΑ 1η"
# (p2 y170) / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ" with "[30 / 100]" at the right (p2
# x459 y197) heads the ARTICLE, "Διαβάστε το κείμενο που ακολουθεί." (y223),
# "Ο ρόλος της μουσικής στη ζωή μας" (y247), seven numbered paragraphs to
# "(830 λέξεις)Γράφει η Σοφία Π. Μιχαλοπούλου, 19/09/2015, ISOTIMOS.COM" (p3
# y717); p4: "ΕΡΩΤΗΣΕΙΣ" (y74), Q1 "1." over five underlined expressions,
# each a bullet (y96-221), Q2-Q6 "2." to "6." (y243-383); "ΟΜΑΔΑ 2η" /
# "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (y423-448), ONE unnumbered task (y472-523); "ΟΜΑΔΑ
# 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (y571-597), the instruction (y624-637),
# the titles "1ο θέμα:" (y667) / "2ο θέμα:" (y709), title 2 a quotation
# signed "Fintan O’ Toole: The Irish Times, 22.02.2016" (y758).
# PRICES:
# - S1Q1-S1Q6: NO price on the paper (rendered p4: no bracketed number and
#   no "βαθμ" from "1." to "6.") nor on the scheme (rendered pp3-4, lines
#   50-106: none). The only figure is the group's "[30 / 100]", printed on
#   p2 before the article. CARD-STANDARD 10i for all six (never split):
#   Unpriced(PL(2, 'ΟΜΑΔΑ 1η'), PaperP(2, '[30 / 100]')) -> "ΟΜΑΔΑ 1η", 30.
#   PARTP cannot read it: the walker opens the questions at "ΕΡΩΤΗΣΕΙΣ" (p4)
#   and never sees the p2 head (its section totals for 2016 are {2: 30,
#   3: 40}), so the total is read from the paper's printed cell (PaperP).
# - S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40). The
#   scheme prints the same heads (49, 112, 122).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; no
# criteria, no notes):
# - Q1 (50 reprints the stem): a two-column table, the expression on the
#   left, its gloss in bold on the right (51-55): "βασικό, αρχικό" /
#   "δείχνω, φανερώνω, παρουσιάζω" / "επιρροή, επίπτωση" /
#   "χρησιμοποιούνται" / "διώχνει, μειώνει". The second expression is
#   reprinted "Εκφράζω" where the paper prints "Εκφράζει" (p4 y147); the fifth
#   "Καταπολεμά" for the paper's "καταπολεμά" (case only).
# - Q2 (56 reprint): one bold-italic paragraph, 57-63.
# - Q3 (64 reprint): one paragraph, 65-69.
# - Q4 (70-71 reprint, "πως ... πως" for the paper's "πώς ... πώς": accents
#   only): one paragraph over the page break, 72-74 and 79-82 (75-78 the page
#   number and marker).
# - Q5 (83-85): the question REWORDED, "Να εξηγήσετε γιατί συμφωνείτε ή
#   γιατί διαφωνείτε." where the paper prints "Να εξηγήσετε για τι
#   συμφωνείτε ή γιατί διαφωνείτε."; then a requirement line, "Αποδεκτή
#   οποιαδήποτε άποψη αρκεί να στηρίζεται σε επιχειρήματα" (86), the heading
#   "Για παράδειγμα :" (87) and two sample answers each under its own
#   heading: "εάν συμφωνώ:" (88) over 89-91, "εάν διαφωνώ:" (92) over 93-98.
# - Q6 (99-100 reprint): one paragraph, 101-106; "Η αυτο-" ends line 102 and
#   "έκφραση" opens 103 (the paper's own compound "αυτο-έκφραση", p3 y646).
# - S2 (111-116 reprint the head and the task, word for word): one paragraph
#   of model commentary, 117-120.
# - S3Q1 (125-126 reprint the title): one paragraph, 127-131.
# - S3Q2 (132-135 reprint the title and signature, "O Toole" and
#   "22-02-2016": punctuation only): one paragraph, 136-142.
# SHAPES:
# - S1Q1: 10i, one shown row per gloss, each led by its expression as the
#   paper prints it ("For “...”").
# - S1Q2-S1Q4, S1Q6: 10i, the paragraph as one shown row.
# - S1Q5: 10i, three shown rows: the requirement line, then each sample
#   answer led by its own heading ("For “εάν συμφωνώ”"); "Για παράδειγμα :"
#   is a heading and goes in the rownote.
# - S2: the paragraph, one shown row, whole=True on 30 (10a).
# - S3Q1, S3Q2: the paragraph, one shown row, whole=True on 40 (10a).
# JUDGEMENT CALLS:
# - S1Q5's requirement line (86) is the scheme's own statement of what is
#   accepted, not a heading: a row, as Bulgarian 2010 Q6.
# - The paper's words stand in S1Q1's and S1Q5's questions; the scheme's
#   "Εκφράζω" and its reworded S1Q5 are quoted (10f).
# - S1Q6: the compound broken at its own hyphen over 102/103 is joined with
#   no space (Join(..., sep='')), "αυτο-έκφραση" as the paper prints it.
# - Questions: S1Q1 the stem and the five expressions, one per line (QL);
#   S1Q2-S1Q6 and S2 the census text, checked against p4; essays the
#   instruction, then the census title (title 2 with its printed signature).
# - Reading text: pp2-3 (rendered: the group head and the title on p2, the
#   text to the byline p3 y717; p4 holds only questions): pages=(2, 3),
#   source='text' on S1Q1-S1Q6 and S2 (see the 2010 note on the runtime
#   gap). No live card of this sitting to compare.
# RUNTIME (lead): this sitting does not build as sl_lib stands. The paper
# prints its rule in lower case, "Όλες οι απαντήσεις να δοθούν στα νέα
# ελληνικά." (p2 y147), and RULE_WORDS['modern-greek'] asks for "Ελληνικ", so
# rule_note raises "the paper prints no answer-language rule". Checked with
# that one pattern widened in memory to r'[Εε]λληνικ|Νεοελληνικ' (nothing
# written): the note then quotes the p2 sentence on page 2.
# GLYPHS (glyph ids read with get_texttrace): the PAPER's S1Q5 opens "O
# συγγραφέας" with a LATIN O (U+004F, Calibri glyph 75; the font's Ο is glyph
# 579): the SEC's own typing, kept in the question as printed, flagged. The
# SCHEME's S3Q1 row has "Tέλος" (line 130) with a LATIN T (U+0054,
# Calibri,BoldItalic glyph 100; Τ is glyph 584) and S3Q2's row "Mόνο" (line
# 137) a LATIN M (U+004D, glyph 68 of the subset Calibri-BoldItalic, which
# carries no Greek Μ). Real Latin glyphs, identical on the render, the SEC's
# typing, not a font map: lifted as printed, flagged for the lead.

U1_2016 = Unpriced(PL(2, 'ΟΜΑΔΑ 1η'), PaperP(2, '[30 / 100]'))
ESSAY_2016 = prerun(4, 'Να επιλέξετε', 'περίπου')


def _q1_2016(d):
    return (f'The scheme reprints the second expression, “{PL(4, "Εκφράζει").text(d)}” on the paper, '
            f'as “{S(52, after="• ", before=" δείχνω").text(d)}”.')


def _q5_2016(d):
    return (f'The scheme reprints the question as “{L(83, 85, after="5. ").text(d)}” Its two sample '
            f'answers stand under the heading “{S(87).text(d)}”.')


SPECS[2016] = [
    R('S1Q1', [shown(S(51, after='Πρωταρχικό '), lead=PL(4, 'Πρωταρχικό')),
               shown(S(52, after='Εκφράζω '), lead=PL(4, 'Εκφράζει')),
               shown(S(53, after='Επίδραση '), lead=PL(4, 'Επίδραση')),
               shown(S(54, after='Λαμβάνονται '), lead=PL(4, 'Λαμβάνονται')),
               shown(S(55, after='Καταπολεμά '), lead=PL(4, 'καταπολεμά'))],
      unpriced=U1_2016, rownote=_q1_2016,
      question=QL(4, '1.', 'Πρωταρχικό', 'Εκφράζει', 'Επίδραση', 'Λαμβάνονται', 'καταπολεμά'),
      pages=(2, 3), source='text'),
    R('S1Q2', [shown(L(57, 63))], unpriced=U1_2016, pages=(2, 3), source='text'),
    R('S1Q3', [shown(L(65, 69))], unpriced=U1_2016, pages=(2, 3), source='text'),
    R('S1Q4', [shown(J(L(72, 74), L(79, 82)))], unpriced=U1_2016, pages=(2, 3), source='text'),
    R('S1Q5', [shown(S(86)),
               shown(L(89, 91), lead=S(88, before=':')),
               shown(L(93, 98), lead=S(92, before=':'))],
      unpriced=U1_2016, rownote=_q5_2016, pages=(2, 3), source='text'),
    R('S1Q6', [shown(Join(L(101, 102), L(103, 106), sep=''))], unpriced=U1_2016,
      pages=(2, 3), source='text'),
    R('S2', [shown(L(117, 120))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(127, 131))], whole=True, question=ESSAY_2016),
    R('S3Q2', [shown(L(136, 142))], whole=True, question=ESSAY_2016),
]
