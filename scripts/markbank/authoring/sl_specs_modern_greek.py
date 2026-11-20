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


# ====================================================================== 2017
# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): "ΝΕΑ ΕΛΛΗΝΙΚΑ" / "Μέγιστη δυνατή βαθμολογία 100
# Βαθμοί" (p2 y59-84); the article "Το πνεύμα της προσφοράς" (p2 y135), nine
# numbered paragraphs to the byline "(διασκευασμένο άρθρο του Παναγιώτη
# Μποκοβού ... Νοέμβριος 2004)" (p3 y381); "ΕΡΩΤΗΣΕΙΣ" (p3 y450) and the rule
# "Να απαντήσετε και στις 3 ομάδες ερωτήσεων. Οι απαντήσεις να δοθούν στα νέα
# Ελληνικά." (p3 y473); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 100]" (p3
# y554-583), Q1's instruction ABOVE its bare "1." with "(5 βαθμοί)" at its
# right (p3 y623) and five bulleted expressions (y663-747); Q2-Q6 "(5
# βαθμοί)" each (p4 y72-266); "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (p4
# y319-343), ONE unnumbered task, the expression on its own two lines (y365-
# 419); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (p4 y485-510), the
# instruction (y535-548), "1ο θέμα:" (y581) over its title (y615-630), "2ο
# θέμα:" (y671) over a quotation (y692-713) and a task (y733-753).
# PRICES: S2 the group head's "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 /
# 100]" (PARTP, 40). The scheme prints the same heads (107, 128). No other
# figure on the paper or the scheme for these asks (rendered).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 2-4; no
# criteria, no percentages, no notes):
# - S2 (106-111 reprint the head, the task and the expression, word for word
#   but for a comma): a model commentary in a shaded box over the page break,
#   three printed paragraphs: 112-115 ("Δύο είναι οι βασικοί τύποι ... κοντά
#   στο συνάνθρωπο τους."), 120-123 ("Ο άλλος τύπος της συμπεριφοράς ... τις
#   ανθρώπινες επαφές.") and 124-126 ("Η εποχή μας χαρακτηρίζεται ...
#   κάποιας μορφής όφελος."); each new paragraph opens a fresh line after a
#   short closing line (rendered p4 y703, p5 y147).
# - S3Q1 (131-133 reprint "1ο θέμα:" and the title): the bold-italic heading
#   "Πιθανές περιοχές ανάπτυξης :" (134), then five paragraphs set apart by
#   space (rendered p5 y408-636): 135-139, 140-141, 142-144, 145, 146-149.
# - S3Q2 (150-152 and 157-158 reprint "2ο θέμα:", the quotation and the task
#   over the page break): the same heading (159), then five paragraphs
#   (rendered p6 y186-500, each closing on a short line): 160-163, 164-167,
#   168-170, 171-172, 173-176.
# SHAPES:
# - S2: 10a, the three paragraphs as three shown rows, whole=True on the
#   paper's 30; the reading text travels with it (pages=(2, 3), source='text').
# - S3Q1, S3Q2: 10a, one shown row per printed paragraph, whole=True on the
#   paper's 40; the heading over them is quoted in the rownote.
# JUDGEMENT CALLS:
# - "Πιθανές περιοχές ανάπτυξης :" is printed once under EACH title (rendered
#   p5 y388, p6 y167), so it is that title's own heading: quoted on each card
#   (rownote), never a row.
# - Questions: S2 the census text (the task and the expression, checked
#   against p4 y365-419); S3Q1/S3Q2 the group's instruction (p4 y535-548) put
#   before the census title (title 2 with its printed task, y733-753).
# - The scheme's reprint of S2's task drops the paper's comma after "έκφραση"
#   (108): punctuation only, not quoted.
# - Reading text pp2-3 (rendered: title p2 y135, the article to its byline p3
#   y381; questions from p3 y450). The live cards' sourceMaterial.pages
#   [2, 3] agree.
# GLYPHS (code points read from the text layer, render checked): the PAPER's
# S3Q1 title opens "Mε" with a LATIN M (U+004D; p4 y615); the scheme's reprint
# (132) has the Greek Μ (U+039C). The paper's own typing: kept in the
# question as printed, flagged for the lead. No Latin letter inside any
# lifted scheme row.

ESSAY_2017 = prerun(4, 'Να επιλέξετε', 'περίπου')
HEAD_2017 = quote(S(134), lead='The scheme heads it')

SPECS[2017] = [
    R('S2', [shown(L(112, 115)), shown(L(120, 123)), shown(L(124, 126))], whole=True,
      pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(135, 139)), shown(L(140, 141)), shown(L(142, 144)), shown(S(145)),
               shown(L(146, 149))], whole=True, rownote=HEAD_2017, question=ESSAY_2017),
    R('S3Q2', [shown(L(160, 163)), shown(L(164, 167)), shown(L(168, 170)), shown(L(171, 172)),
               shown(L(173, 176))], whole=True, rownote=quote(S(159), lead='The scheme heads it'),
      question=ESSAY_2017),
]


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): the article "Επικοινωνία μέσω διαδικτύου: νεανικές
# τάσεις στη γραπτή γλώσσα" runs pp2-3, eleven numbered paragraphs to the
# byline "ΝΑΣΟΣ ΚΑΤΣΩΧΗΣ,24grammata.com/ Λόγος , 20 /04/2011, 840 λέξεις,
# ..." (p3 y631-643); "ΕΡΩΤΗΣΕΙΣ" (p3 y663) and the rule (p3 y693); p4:
# "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 100]" (y58-88), Q1 "1." over
# five bulleted expressions with ONE "(5 βαθμοί)" at the right of the last
# (y213); Q2-Q6 "(5 βαθμοί)" each (y238-390); "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 /
# 100]" (y430-446), one unnumbered task of four lines (y474-513); "ΟΜΑΔΑ 3η"
# / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (y557-581), the instruction (y605-618), "1ο
# θέμα:" (y642) over its title (y665), "2ο θέμα:" (y701) over its title
# (y724-745).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (107, 125); nothing else priced for them.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 2-4; no
# criteria, no notes):
# - S2 (106-110 reprint the head and the task's first three lines; the
#   paper's fourth line, "Να αναπτύξετε τις απόψεις σας σε ένα κείμενο 100
#   περίπου λέξεων.", is not reprinted): ONE bold-italic paragraph of model
#   commentary, 111-119 ("Οι νέοι άνθρωποι , έφηβοι ... μεγαλύτερης
#   ηλικίας.").
# - S3Q1 (128-129 reprint "1ο θέμα:" and the title): five paragraphs set
#   apart by space (rendered p5 y221-647): 130-141, 142-147, 148-151,
#   152-153, 154-155. No heading.
# - S3Q2 (156-158 reprint "2ο θέμα:" and the title): three paragraphs on p6
#   (rendered: each opens a fresh line after a short closing line, y74-356):
#   163-172, 173-176, 177 ("Επιζητά ό άνθρωπος την αρμονία;").
# SHAPES:
# - S2: 10a, the paragraph as one shown row, whole=True on the paper's 30;
#   pages=(2, 3), source='text'.
# - S3Q1, S3Q2: 10a, one shown row per printed paragraph, whole=True on the
#   paper's 40.
# JUDGEMENT CALLS:
# - S3Q2's closing one-line question (177) is printed as a paragraph of its
#   own (rendered p6 y356, after "της ψυχής του;" closes the line above): its
#   own row.
# - The scheme's partial reprint of S2's task is an omission, not a
#   rewording: not quoted.
# - Questions: S2 the census text (the four printed lines, checked on p4);
#   S3Q1/S3Q2 the group's instruction (p4 y605-618) before the census title.
# - Reading text pp2-3 (rendered: title p2, the article to its byline p3
#   y643; questions from p3 y663). The live cards' pages [2, 3] agree.
# GLYPHS: none (no Latin letter inside a Greek word in any lifted line; the
# scheme's own typos, "έχε γίνει" (130), "Ποτέ πριν ο άνθρωποι" (131-132),
# are lifted as printed).

ESSAY_2018 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2018] = [
    R('S2', [shown(L(111, 119))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(130, 141)), shown(L(142, 147)), shown(L(148, 151)), shown(L(152, 153)),
               shown(L(154, 155))], whole=True, question=ESSAY_2018),
    R('S3Q2', [shown(L(163, 172)), shown(L(173, 176)), shown(S(177))], whole=True, question=ESSAY_2018),
]


# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): the article runs pp2-3 to its byline "Προβόπουλος
# Ηλίας, Φιλελεύθερος, 03-11-2018, 841 Λέξεις" (p3 y517); "ΕΡΩΤΗΣΕΙΣ" (p3
# y546), the rule (p3 y580); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 100]"
# (p3 y606-634), Q1 "1." over five bulleted expressions with one "(5
# βαθμοί)" at the right of the last (p3 y768); p4: Q2-Q6 "(5 βαθμοί)" each
# (y59-244); "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (y314-342), one unnumbered
# task of three lines (y369-402); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]"
# (y486-516), the instruction (y543-556), "1ο θέμα:" (y591) over its title
# (y614), "2ο θέμα:" (y657) over its title and task (y680-724).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (103, 120); nothing else priced for them.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 2-4; no
# criteria, no notes):
# - S2 (102-106 reprint the head and the task, word for word): ONE justified
#   bold-italic paragraph of model commentary over the page break, 107-111 and
#   116-118 ("Το διαδίκτυο μπορεί επίσης ... πολλές αναμνήσεις και πόνο.").
#   One paragraph: p4's last line (y752, "... τον πολιτισμό του.") is set
#   full-justified to the right margin, so the paragraph runs on to p5.
# - S3Q1 (123-124 reprint "1ο θέμα:" and the title): two paragraphs, an
#   indented block (rendered p5 y322-541): 125-131 and 132-135.
# - S3Q2 (136-139 reprint "2ο θέμα:" and the title with its task): six
#   paragraphs over the page break, each opening at x57 with its later lines
#   at x64 (rendered p5 y739 to p6 y455): 140-141 + 146-147, 148-153,
#   154-156, 157-160, 161-162, 163-164.
# SHAPES:
# - S2: 10a, the paragraph as one shown row (its two halves joined over the
#   page break), whole=True on the paper's 30; pages=(2, 3), source='text'.
# - S3Q1, S3Q2: 10a, one shown row per printed paragraph, whole=True on the
#   paper's 40.
# JUDGEMENT CALLS:
# - S2 kept as one paragraph across the page break (justified last line on
#   p4, no paragraph start on p5).
# - Questions: S2 the census text (checked on p4 y369-402); S3Q1/S3Q2 the
#   group's instruction (p4 y543-556) before the census title (title 2 with
#   its printed task line).
# - The scheme reprints title 1 without the paper's full stop (124) and title
#   2 with "( έτος χάσματος)" for "(έτος χάσματος)" (137): spacing and
#   punctuation only, not quoted.
# - Reading text pp2-3 (rendered: the article to its byline p3 y517;
#   questions from p3 y546). The live cards' pages [2, 3] agree.
# GLYPHS: none (no Latin letter inside a Greek word in any lifted line; "gap
# year" is the scheme's own English, as the paper prints it).

ESSAY_2019 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2019] = [
    R('S2', [shown(J(L(107, 111), L(116, 118)))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(125, 131)), shown(L(132, 135))], whole=True, question=ESSAY_2019),
    R('S3Q2', [shown(J(L(140, 141), L(146, 147))), shown(L(148, 153)), shown(L(154, 156)),
               shown(L(157, 160)), shown(L(161, 162)), shown(L(163, 164))], whole=True,
      question=ESSAY_2019),
]


# ====================================================================== 2021
# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# SIIQ1, SIIQ2 (the essay titles of Part II). Live: SIQ1-SIQ6 (6 cards); not
# touched (audited: see modern-greek-live-faults-2017-2026.json).
# A TWO-PART sitting (the SEC's 2021 reduction, no commentary): the rule
# "Να απαντήσετε και στα 2 δύο μέρη: Πρώτο μέρος και δεύτερο μέρος." / "Όλες
# οι απαντήσεις πρέπει να γραφούν στα νέα Ελληνικά." and "Μέγιστη
# βαθμολογία 70 βαθμοί" (p2 y59-103); "Μέρος πρώτο" + "(30 μονάδες)" (p2
# y132), the article "Η ανεργία του μέλλοντος" (p2 y213 to its byline "ΑΡΙΣΤΟΣ
# ΔΟΞΙΑΔΗΣ, ΠΟΛΙΤΙΚΗ ,18.04.2017, ..." p3 y479), Q1-Q6 (p3 y519 to p4 y263);
# "Μέρος δεύτερο" + "(40 μονάδες)" (p4 y351), the instruction "Να γράψετε
# ένα δοκίμιο ( το λιγότερο 300λέξεων ) επιλέγοντας ένα από τα δύο θέματα
# που" / "ακολουθούν." (y380-395), "1ο θέμα:" (y430) over title 1 (y453),
# "Ή" on a line of its own (y497), "2ο θέμα:" (y540) over title 2 (y563-578).
# PRICES: SIIQ1/SIIQ2 the part head's "(40 μονάδες)" (PARTP, 40). The scheme
# heads the same essay group "ΟΜΑΔΑ 2η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 70]" (118-
# 119): the same 40.
# WHAT THE SCHEME PRINTS (rendered scheme pp5-7 = printed pages 3-5; no
# criteria, no notes):
# - The instruction REWORDED (120-121): "Να επιλέξετε ένα από τα δύο θέματα
#   και να αναπτύξετε τις απόψεις σας σε ένα κείμενο 300 περίπου λέξεων."
#   where the paper prints "Να γράψετε ένα δοκίμιο ( το λιγότερο 300λέξεων )
#   επιλέγοντας ένα από τα δύο θέματα που ακολουθούν." (the paper asks for AT
#   LEAST 300 words, the scheme for about 300).
# - SIIQ1 (122-123 reprint "1ο θέμα:" and the title): a model essay in bold,
#   lines double-spaced, each paragraph opening a fresh line after a short
#   closing line (rendered p5 y536 to p6 y624): 124-129, 130-132, 133 ("Πιο
#   συγκεκριμένα :", a line of its own at the foot of p5), 138-140, 141-142
#   (closing "Για παράδειγμα:" on the same line), 143-144, 145-147, 148-154,
#   155-161, 162-163.
# - SIIQ2 (168-170 reprint "2ο θέμα:" and the title): two paragraphs
#   (rendered p7 y184-448): 171-177 and 178-183.
# SHAPES: SIIQ1, SIIQ2: 10a, one shown row per printed paragraph, whole=True
# on the paper's 40; the scheme's reworded instruction quoted in the rownote
# (the paper's words stand in the question). No reading text (Part II is the
# essay; sl_lib files it as Part III).
# JUDGEMENT CALLS:
# - SIIQ1's "Πιο συγκεκριμένα :" (133) is printed as a line of its own, in the
#   model's own bold type, introducing the paragraphs that follow: kept as a
#   shown row (the model's words, not a heading the scheme sets over the
#   answer). "Για παράδειγμα:" (142) ends its paragraph's printed line and
#   stays inside that row.
# - Questions: the paper's instruction (p4 y380-395) and the title's own
#   printed line(s); the census's title 1 carries the "Ή" printed between the
#   titles (y497), which is not part of it (QP takes the joiner off).
# - The scheme reprints title 2 with two spaces after "Thunberg" (169):
#   spacing only, not quoted.
# GLYPHS: SIIQ1's row 124 prints "(TN)" for the abbreviation of "τεχνητή
#   νοημοσύνη" with LATIN T and N (U+0054, U+004E; rendered identical): the
#   scheme's own typing, lifted as printed, flagged for the lead.

ESSAY_2021 = Run('Να γράψετε ένα δοκίμιο', 'ακολουθούν.')
INSTR_2021 = quote(L(120, 121), lead='The scheme reprints the instruction as')

SPECS[2021] = [
    # "Πιο συγκεκριμένα :" (133) is a lead-in heading for the points under it: in the note, not a row (lead)
    # r-4 ends before "Για παράδειγμα:", the lead-in to the next four rows (second reader): in the note
    R('SIIQ1', [shown(L(124, 129)), shown(L(130, 132)), shown(L(138, 140)),
                shown(L(141, 142, before=' Για παράδειγμα:')), shown(L(143, 144)), shown(L(145, 147)),
                shown(L(148, 154)), shown(L(155, 161)), shown(L(162, 163))], whole=True,
      rownote=both(INSTR_2021, lambda d: (f'The scheme leads the points after its second paragraph with '
                                          f'“{S(133).text(d)}” and the four examples after its fourth with '
                                          f'“{S(142, after="μας. ").text(d)}”.')),
      question=QP(4, ESSAY_2021, 'Η τεχνητή νοημοσύνη')),
    R('SIIQ2', [shown(L(171, 177)), shown(L(178, 183))], whole=True, rownote=INSTR_2021,
      question=QP(4, ESSAY_2021, Run('Η Greta Thunberg', 'επειδή δεν σου'))),
]


# ====================================================================== 2022
# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# S2Q1, S2Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# A TWO-GROUP sitting (the SEC's 2022 reduction): GROUP 2 IS THE ESSAY, not
# the commentary. Paper (rendered pp2-4): the article runs pp2-3 to its source
# lines "Σάββας Σαββόπουλος, https://www.athensvoice.gr/..." / "(820 λέξεις,
# κείμενο ελαφρά τροποποιημένο ...)" (p3 y658-682); p4: "ΕΡΩΤΗΣΕΙΣ" (y59),
# "Να απαντήσετε και στις 2 ομάδες ερωτήσεων. ..." (y86); "ΟΜΑΔΑ 1η" /
# "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 70]" (y111-140), Q1 "(5 × 1)" (y211), Q2-Q6
# "(5)" each (y340-481); "ΟΜΑΔΑ 2η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 70]" (y541-570),
# the instruction (y597-610), and the two titles numbered "1." (y657-676)
# and "2." (y730) -- no "1ο θέμα" heads this sitting.
# PRICES: S2Q1/S2Q2 the group head's "[40 / 70]" (PARTP, 40). The scheme
# prints the same "[40 / 70]" twice (103, 108).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 2-3; pp6-7
# blank, no image on any page): at the foot of p4 "ΟΜΑΔΑ 2η" / "[40 / 70]"
# (102-103); on p5 "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 70]" (108), the instruction
# (109-110) and the two titles (111-112, 113), and NOTHING after them: no
# model, no indicative points, no criteria.
# SHAPES: S2Q1, S2Q2: R4, unprinted(), UNPRINTED_ANSWER at the paper's 40,
# the note quoting what the scheme prints for the task (its instruction and
# that title).
# JUDGEMENT CALLS:
# - Not 10a: the scheme's block is only the reprinted task (rendered p5:
#   three short blocks, then blank to the page number "3").
# - Questions: the group's instruction (p4 y597-610) before the title's own
#   printed lines (title 1 runs over two lines, y659-676; the census's
#   text is the same words).
# - No reading text (the essay; sl_lib attaches none to section 2 here).
# GLYPHS: none.

# the paper sets this instruction in no-break spaces (U+00A0): the anchor carries one
ESSAY_2022 = prerun(4, 'Να\xa0επιλέξετε', 'περίπου')

SPECS[2022] = [
    R('S2Q1', [unprinted(quote(L(109, 110), L(111, 112),
                               lead='Under “ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ” the scheme prints only the instruction and '
                                    'the title, and no answer'))],
      question=ESSAY_2022),
    R('S2Q2', [unprinted(quote(L(109, 110), S(113),
                               lead='Under “ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ” the scheme prints only the instruction and '
                                    'the title, and no answer'))],
      question=ESSAY_2022),
]


# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): the article "Οι αθλητές που νίκησαν τις
# καταιγίδες" (p2 y59) runs pp2-3 to its source lines "https://maritimes.gr/
# ..." / "Πέτρος Κασιμάτης, (κείμενο διασκευασμένο ...)" (p3 y709-721); p4:
# "ΕΡΩΤΗΣΕΙΣ" (y59), the rule (y76); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30
# / 100]" (y102-130), Q1 "(5 × 1)" (y250), Q2-Q6 "(5)" each (y301-412);
# "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]" (y453-481), one unnumbered task of
# three lines (y508-542); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (y572-601),
# the instruction (y629-642), "1ο θέμα:" (y677) / title (y700), "2ο θέμα:"
# (y721) / title (y744).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (92, 105); nothing else priced for them.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 2-3; no
# criteria, no notes):
# - S2 (91-95 reprint the head and the task, word for word): ONE bold
#   paragraph of model commentary, 96-103 ("Όπως γνωρίζουμε από την Οδύσσεια
#   ... έμεινε σταθερή στο στόχο της.").
# - S3Q1 (108-109 reprint "1ο θέμα:" and the title): ONE paragraph over the
#   page break, 110-116 and 121-127 (p4 ends mid-sentence, "Την εποχή μας
#   που όλα δείχνουν να" / p5 "γίνονται γρήγορα ...").
# - S3Q2 (128-129 reprint "2ο θέμα:" and the title): eight paragraphs set
#   apart by space (rendered p5 y304-755): 130-132, 133-136, 137-141,
#   142-143, 144-146, 147-150, 151-152, 153-157.
# SHAPES:
# - S2: 10a, one shown row, whole=True on the paper's 30; pages=(2, 3),
#   source='text'.
# - S3Q1: 10a, one shown row (the paragraph's halves joined over the page
#   break), whole=True on the paper's 40.
# - S3Q2: 10a, eight shown rows, whole=True on the paper's 40.
# JUDGEMENT CALLS:
# - S3Q2's 144-146 is one paragraph (line gaps 4 within it, 10 before 147;
#   rendered p5 y540-570).
# - Questions: S2 the census text (checked on p4 y508-542); S3Q1/S3Q2 the
#   group's instruction (p4 y629-642) before the census title.
# - Reading text pp2-3 (rendered: the article to its source lines p3 y721;
#   questions from p4 y59). The live cards' pages [2, 3] agree.
# GLYPHS (code points, glyph ids read with get_texttrace, render checked):
#   S3Q2's first row opens "Oι φίλοι" with a LATIN O (U+004F, line 130) and
#   its second row has "μοίρασmα" with a LATIN m (U+006D, line 135). Both are
#   Latin glyphs of the scheme's Calibri-Bold (O = glyph 75, where the same
#   font's Greek Ο is glyph 579; m = glyph 373), drawn as Latin (the m is
#   visibly a Latin m on the render): the scheme's own typing, lifted as
#   printed, flagged for the lead (never hand-mapped).

ESSAY_2023 = prerun(4, 'Να επιλέξετε', 'λέξεων.')

SPECS[2023] = [
    R('S2', [shown(L(96, 103))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(J(L(110, 116), L(121, 127)))], whole=True, question=ESSAY_2023),
    R('S3Q2', [shown(L(130, 132)), shown(L(133, 136)), shown(L(137, 141)), shown(L(142, 143)),
               shown(L(144, 146)), shown(L(147, 150)), shown(L(151, 152)), shown(L(153, 157))],
      whole=True, question=ESSAY_2023),
]


# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): "Μέγιστη δυνατή βαθμολογία 100 Βαθμοί" (p2 y59);
# the article "Κλιματική αλλαγή : το υπαρξιακό countdown & η ψυχολογία της
# κλιματικής αδράνειας" (p2 y114) runs pp2-3 to its source lines "(κείμενο
# ελαφρά διασκευασμένο ..., Σπύρος Καλημέρης ,2..." / "https://kalimeris
# therapist.com" (p3 y745-755); p4: "ΕΡΩΤΗΣΕΙΣ" (y59), the rule (y79);
# "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ [30 / 100]" (y103-130), Q1 "(5 × 1)"
# (y280), Q2-Q6 "(5)" each (y320-481); "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 / 100]"
# (y500-527), the task: a sentence to comment on (y552) and the instruction
# "Σε μια παράγραφο 100 - 150 περίπου λέξεων να σχολιάσετε το νόημα της
# προηγούμενης φράσης." (y572); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]"
# (y597-612), the instruction on ONE line (y625), "1ο θέμα:" (y650) / title
# (y672-685), "2ο θέμα:" (y711) / a quotation signed "Γιώργος Σεφέρης (Νόμπελ
# Λογοτεχνίας, 1963)" (y732-752).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (126, 145); nothing else priced for them.
# WHAT THE SCHEME PRINTS (rendered scheme pp5-7 = printed pages 3-5; no
# criteria, no notes):
# - S2 (125-130): the head, the sentence, and the instruction REWORDED:
#   "Σε μια παράγραφο 100 περίπου λέξεων να σχολιάσετε το νόημα της
#   προηγούμενης" / "φράσης." (129-130) where the paper asks for "100 - 150
#   περίπου λέξεων". Then ONE justified bold paragraph of model commentary
#   over the page break, 131-136 and 141-143 ("Η φράση "Οι άνθρωποι ..." ...
#   προσωπικού χαρακτήρα και δράσης."); p5's "... στις αποφάσεις μας." (y704)
#   is a justified inner line, not a paragraph end (rendered).
# - S3Q1 (148-150 reprint "1ο θέμα:" and the title): three paragraphs set
#   apart by space (rendered p6 y360 to p7 y118): 151-159, 160-164,
#   165-167 + 172-174 (over the page break, mid-sentence).
# - S3Q2 (175-177 reprint "2ο θέμα:" and the quotation with its signature):
#   seven paragraphs set apart by space (rendered p7 y272-686): 178-181, 182
#   ("Ας αναλύσουμε τα βασικά στοιχεία αυτής της άποψης:"), 183-186
#   (opening with the run-in label "Σύνδεση Παρελθόντος και Μέλλοντος:"),
#   187-190, 191-193, 194-196, 197-199.
# SHAPES:
# - S2: 10a, one shown row, whole=True on the paper's 30, the scheme's
#   reworded instruction quoted in the rownote (the paper's words stand);
#   pages=(2, 3), source='text'.
# - S3Q1, S3Q2: 10a, one shown row per printed paragraph, whole=True on the
#   paper's 40.
# JUDGEMENT CALLS:
# - S3Q2's 182 is a sentence of the model essay printed as a paragraph of its
#   own (set apart by space), not a heading over the answer: its own row.
#   The run-in "Σύνδεση Παρελθόντος και Μέλλοντος:" opens its paragraph's
#   line in the same type and stays inside that row.
# - Questions: S2 the census text (both printed lines, p4 y552-572); S3Q1/
#   S3Q2 the group's one-line instruction (p4 y625) before the census title.
# - Reading text pp2-3 (rendered: the article to its source lines p3 y755;
#   questions from p4 y59). The live cards' pages [2, 3] agree.
# GLYPHS: none (no Latin letter inside a Greek word in any lifted line; the
# scheme's own slips, "η δικαιοσύνες" (155), lifted as printed).

ESSAY_2024 = pre(4, 'Να επιλέξετε')

SPECS[2024] = [
    R('S2', [shown(J(L(131, 136), L(141, 143)))], whole=True,
      rownote=quote(L(129, 130), lead='The scheme reprints the instruction as'), pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(151, 159)), shown(L(160, 164)), shown(J(L(165, 167), L(172, 174)))], whole=True,
      question=ESSAY_2024),
    R('S3Q2', [shown(L(178, 181)), shown(S(182)), shown(L(183, 186)), shown(L(187, 190)), shown(L(191, 193)),
               shown(L(194, 196)), shown(L(197, 199))], whole=True, question=ESSAY_2024),
]


# ====================================================================== 2025
# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): the interview "ΑΠΟΨΕΙΣ ΜΑΘΗΤΩΝ ΓΙΑ ΤΗΝ ΕΚΠΑΙΔΕΥΣΗ
# ΤΟΥΣ" (p2 y59) runs pp2-3 to its byline "Των Νάσιας Αναστασιάδη, ... (1000
# λέξεις) ΤΟ ΒΗΜΑ, 22-10-2023" (p3 y759-769); p4: "ΕΡΩΤΗΣΕΙΣ" (y59), the rule
# (y88); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ ΕΡΜΗΝΕΙΑ ... [30 / 100]" (y121-139), Q1
# five expressions lettered a)-e) under one "(5 × 1)" (y275), Q2-Q6 "(5)"
# each (y303-494); "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ ... [30 / 100]" (y522-538), the
# question to comment on (y560) and the instruction "Σε μια παράγραφο 100
# -150 λέξεων ..." (y582); "ΟΜΑΔΑ 3η" / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ ... [40 / 100]"
# (y615-630), the instruction "... σε ένα κείμενο" / "τουλάχιστον 300
# λέξεων." (y651-665), "1ο θέμα:" (y694) / title (y715), "2ο θέμα:" (y744) /
# a quotation "(Ηράκλειτος)." (y765).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (139, 166); nothing else priced for them.
# WHAT THE SCHEME PRINTS (rendered scheme pp6-9 = printed pages 6-9; p3 the
# SEC's annotation key; no criteria, no notes):
# - S2 (138-141 reprint the head and the task, word for word): the bold
#   heading "Για παράδειγμα:" (142), then a model commentary in TWO justified
#   paragraphs: 143-151 + 156-160 (over the page break; p7 y162 "...
#   προκλήσεις του." closes it short) and 161-164 ("Ακόμα, μαθαίνουμε ... η
#   συναισθηματική μας κατάσταση."; its line y206 "... την εξέλιξη μας." is a
#   justified inner line reaching the margin, x1 523, so 163 does not open a
#   paragraph).
# - S3Q1 (169-170 reprint "1ο θέμα:" and the title): "Για παράδειγμα:" (171),
#   then five ragged-right paragraphs, each closing on a line the next word
#   would have fitted (rendered p7 y512 to p8 y294): 172-176, 177-183,
#   188-192, 193-195, 196-198.
# - S3Q2 (199-200 reprint "2ο θέμα:" and the quotation, "Ηράκλειτος." for the
#   paper's "(Ηράκλειτος).": punctuation only): "Για παράδειγμα:" (201), then
#   six justified paragraphs (rendered p8 y404 to p9 y338; each closes on a
#   short line): 202-206, 207-212, 213-216, 217-218 + 223-224 (over the page
#   break; 219 is the page number "8"), 225-232, 233-235.
# SHAPES:
# - S2: 10a, the two paragraphs as two shown rows, whole=True on the paper's
#   30, the heading quoted in the rownote; pages=(2, 3), source='text'.
# - S3Q1, S3Q2: 10a, one shown row per printed paragraph, whole=True on the
#   paper's 40, each title's own "Για παράδειγμα:" quoted in its rownote.
# JUDGEMENT CALLS:
# - "Για παράδειγμα:" is printed on a line of its own in bold over each model
#   (once per task, under each title separately): a heading, quoted, never a
#   row.
# - S3Q2's 213 "... της ατομικής έκφρασης." reaches the margin justified
#   (x1 523): the paragraph runs on to 216.
# - Questions: S2 the census text (both printed lines, p4 y560-582); S3Q1/
#   S3Q2 the group's instruction (p4 y651-665) before the census title.
# - Reading text pp2-3 (rendered: the interview to its byline p3 y769;
#   questions from p4 y59). The live cards' pages [2, 3] agree.
# GLYPHS: none (no Latin letter inside a Greek word in any lifted line).

ESSAY_2025 = prerun(4, 'Να επιλέξετε', 'τουλάχιστον')

SPECS[2025] = [
    R('S2', [shown(J(L(143, 151), L(156, 160))), shown(L(161, 164))], whole=True,
      rownote=quote(S(142), lead='The scheme heads it'), pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(172, 176)), shown(L(177, 183)), shown(L(188, 192)), shown(L(193, 195)),
               shown(L(196, 198))], whole=True, rownote=quote(S(171), lead='The scheme heads it'),
      question=ESSAY_2025),
    R('S3Q2', [shown(L(202, 206)), shown(L(207, 212)), shown(L(213, 216)), shown(J(L(217, 218), L(223, 224))),
               shown(L(225, 232)), shown(L(233, 235))], whole=True,
      rownote=quote(S(201), lead='The scheme heads it'), question=ESSAY_2025),
]


# ====================================================================== 2026
# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# S2, S3Q1, S3Q2. Live: S1Q1-S1Q6 (6 cards); not touched (audited: see
# modern-greek-live-faults-2017-2026.json).
# Paper (rendered pp2-4): "Μέγιστη δυνατή βαθμολογία 100 Βαθμοί" (p2 y59);
# the article runs pp2-3 to its source line "(κείμενο διασκευασμένο για τις
# ανάγκες της εξέτασης) , Στέλιος Κερασίδης,08-02-2024, Pcychology.gr" (p3
# y762); p4: "ΕΡΩΤΗΣΕΙΣ" (y59), the rule (y80); "ΟΜΑΔΑ 1η" / "ΚΑΤΑΝΟΗΣΗ ΚΑΙ
# ΕΡΜΗΝΕΙΑ [30 / 100]" (y100-121), Q1 "1." set as a cell of its own beside
# its instruction (y148), five expressions lettered a)-e) under one "(5 ×
# 1)" (y246), Q2-Q6 "(5)" each (y270-417); "ΟΜΑΔΑ 2η" / "ΣΧΟΛΙΑΣΜΟΣ [30 /
# 100]" (y436-464), one unnumbered task of three lines (y491-525); "ΟΜΑΔΑ 3η"
# / "ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ [40 / 100]" (y552-578), the instruction (y599-614), "1ο
# θέμα:" (y633) / title (y655-670), "2ο θέμα:" (y689) / three lines of
# Cavafy signed "(Κ.Καβάφης,1913)" (y711-734).
# PRICES: S2 "[30 / 100]" (PARTP, 30); S3Q1/S3Q2 "[40 / 100]" (PARTP, 40).
# The scheme prints the same heads (116, 128); nothing else priced for these
# asks (its "(5)" and "(5X1)" stand only under Q1-Q6).
# WHAT THE SCHEME PRINTS (rendered scheme pp6-7 = printed pages 6-7; no
# criteria, no notes):
# - S2 (115-119 reprint the head and the task, word for word): ONE paragraph
#   of model commentary, 120-126 ("Αν και αναγνωρίζουμε ... του κόσμου γύρω
#   μας.").
# - S3Q1 (131-133 reprint "1ο θέμα:" and the title): three paragraphs set
#   apart by space (rendered p6 y518-757): 134-138, 139-143, 144-147.
# - S3Q2 (152-155 reprint "2ο θέμα:" and the three lines): TWO paragraphs
#   set apart by space (rendered p7): 156-168 and 169-177. Line 165 ("... το
#   ενδεχόμενο αυτό.") fills its line and 166 ("Εκείνο, όμως, ...") follows
#   with no space between: one paragraph (the only space on the page falls
#   before 169).
# SHAPES:
# - S2: 10a, one shown row, whole=True on the paper's 30; pages=(2, 3),
#   source='text'.
# - S3Q1, S3Q2: 10a, one shown row per printed paragraph, whole=True on the
#   paper's 40.
# JUDGEMENT CALLS:
# - Questions: S2 the census text (checked on p4 y491-525); S3Q1/S3Q2 the
#   group's instruction (p4 y599-614) before the census title (title 2 its
#   three printed lines with the signature, as printed).
# - Reading text pp2-3 (rendered: the article to its source line p3 y762;
#   questions from p4 y59). The live cards' pages [2, 3] agree.
# GLYPHS: none (no Latin letter inside a Greek word in any lifted line).

ESSAY_2026 = prerun(4, 'Να επιλέξετε', 'περίπου')

SPECS[2026] = [
    R('S2', [shown(L(120, 126))], whole=True, pages=(2, 3), source='text'),
    R('S3Q1', [shown(L(134, 138)), shown(L(139, 143)), shown(L(144, 147))], whole=True,
      question=ESSAY_2026),
    R('S3Q2', [shown(L(156, 168)), shown(L(169, 177))], whole=True, question=ESSAY_2026),
]
