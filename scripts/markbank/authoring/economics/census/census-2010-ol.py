"""Write the independent 2010 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2010 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2010/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2010/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2010-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: none on this paper (no printed stance or
# either-or choice is credited with a list for each side).
ALT = ()

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [4], [T('i/ii', 16, 'sa-q1', '4-1')],
  'One card for the two names, the paper numbering them (i)-(ii): each name 8, the scheme printing 4 + 2 + 2 beside its three words.',
  'The IMF and the WTO are Globalisation (4-1), as 2017 OL files them.')
q(2, [2], [4], [T('all', 16, 'sa-q2', '4-0')],
  'One organisation 8 from six + one measure 8 from seven: one card, two rows.',
  'Aid to LDCs and measures to help them are Growth & Development (4-0), as 2013 OL files aid to LDCs.')
q(3, [2], [5], [T('i/ii/iii', 16, 'sa-q3', '2-0')],
  'One card for the three statements, the paper numbering them (i)-(iii): the 1st correct answer 8, the 2nd and 3rd 4 each.',
  'Product differentiation, homogeneous goods and control over price are Market Structures (2-0).')
q(4, [2], [5], [T('all', 16, 'sa-q4', '0-1')],
  'The explanation (either of two) and an example, priced 16 together without a split: one questionTotal card.',
  'Opportunity cost is Scarcity & Choice (0-1), as 2012 OL files it.')
q(5, [2], [5], [T('all', 16, 'sa-q5', '3-1')],
  'Two effects from eight at 8: one card.',
  'The current budget deficit is Fiscal Policy & the Budget (3-1); rising unemployment is also Employment & Unemployment (3-2).', also=['3-2'])
q(6, [3], [6], [T('all', 17, 'sa-q6', '3-5')],
  'Two advantages from seven: the 1st correct 10, the 2nd 7.',
  'The advantages of more people in third-level education (a better educated workforce, productivity, FDI) are Economic Growth (3-5), as 2017 OL files the advantages of education.')
q(7, [3], [6], [T('all', 17, 'sa-q7', '1-1')],
  'The four items placed as substitutes or complements: the 1st correct 5, the 2nd, 3rd and 4th 4 each: one card, the item table as the crop.',
  'Substitute and complementary goods are The Consumer (Demand) (1-1), as 2013 OL files them.')
q(8, [3], [7], [T('all', 17, 'sa-q8', '0-1')],
  'The explanation 10 + one reason 7 from nine: one card, two rows.',
  'Entrepreneurship is Scarcity & Choice (0-1), as 2012 OL files the entrepreneur.')
q(9, [3], [8], [T('all', 17, 'sa-q9', '4-2')],
  'Two effects from seven, priced 17 together without a split: one questionTotal card.',
  'Cross-border shopping is International Trade & Competitiveness (4-2), as 2017 OL files it; its effect on tax revenue is also Fiscal Policy & the Budget (3-1), and on jobs Employment & Unemployment (3-2).', also=['3-1', '3-2'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [9, 10, 11],
  [T('a/i', 12, 'sb-q1-a-i', '2-0'), T('a/ii', 9, 'sb-q1-a-ii', '2-0'), T('b', 24, 'sb-q1-b', '2-0'),
   T('c/i', 10, 'sb-q1-c-i', '2-0'), T('c/ii', 10, 'sb-q1-c-ii', '1-1'), T('c/iii', 10, 'sb-q1-c-iii', '3-2')],
  'Six tasks totalling 75. a(i) the three lines at 4 (2 + 2); a(ii) P1 and C1, the 1st correct 5 and the 2nd 4 (hidden solution diagram, the paper’s diagram beside the ask). b the three barriers, each explained with an example, the 1st correct explanation 12 and the 2nd and 3rd 6 (the scheme’s table of explanations and examples as the hidden solution). c(i) 2 at 5 (3 + 2) from five; c(ii) 2 at 5 from three; c(iii) 2 at 5 from four.',
  'Monopoly, its equilibrium and barriers to entry are Market Structures (2-0), as 2011 OL files them; the falling demand for letter-post is The Consumer (Demand) (1-1); the closure of rural post offices and its effects on jobs and communities are Employment & Unemployment (3-2), as 2019 OL files them.')
q('B2', [5], [12, 13, 14],
  [T('a/i', 7, 'sb-q2-a-i', '1-1'), T('a/ii', 8, 'sb-q2-a-ii', '1-1'), T('a/iii', 10, 'sb-q2-a-iii', '1-1'),
   T('b/i', 6, 'sb-q2-b-i', '1-0'), T('b/ii', 6, 'sb-q2-b-ii', '1-0'), T('b/iii', 8, 'sb-q2-b-iii', '1-0'),
   T('c/i', 10, 'sb-q2-c-i', '1-1'), T('c/ii', 10, 'sb-q2-c-ii', '1-0'), T('c/iii', 10, 'sb-q2-c-iii', '1-2')],
  'Nine tasks totalling 75. a(i) 7, the scheme printing 5 and 2 beneath the two halves of its sentence; a(ii) the good 5 from three + the explanation 3 from three; a(iii) the three marginal utilities at 2, the point 2 and its explanation 2 (hidden solution table, the paper’s table beside the ask). b(i) 6, either explanation; b(ii) 6; b(iii) 2 at 4 from four. c(i) 2 at 5 (3 + 2) from five; c(ii) 2 at 5 from five; c(iii) 2 at 5 from four.',
  'Marginal utility and diminishing marginal utility are The Consumer (Demand) (1-1); a fixed supply of seats and a black market for tickets are The Market Economy (1-0), as 2012 OL files a fixed supply of tickets; the falling demand for hotel accommodation is The Consumer (Demand) (1-1), its effects for the hotel industry The Market Economy (1-0), and the industry’s measures to reverse it The Firm (Supply) (1-2), as 2011 OL files Irish Rail’s actions to raise demand; tourism is also International Trade & Competitiveness (4-2).', also=['4-2'])
q('B3', [6], [15, 16, 17],
  [T('a', 20, 'sb-q3-a', '1-1'), T('b/i', 6, 'sb-q3-b-i', '1-0'), T('b/ii', 6, 'sb-q3-b-ii', '1-0'),
   T('b/iii', 18, 'sb-q3-b-iii', '1-2'), T('c/i', 12, 'sb-q3-c-i', '1-4'), T('c/ii', 13, 'sb-q3-c-ii', '1-4')],
  'Six tasks totalling 75. a 4 at 5 (2 + 3) from eight. b(i) the two lines at 3; b(ii) P1 3 + Q1 3; b(iii) the new labelled supply curve 6 (3 + 3), its explanation 8, P2 2 and Q2 2 (hidden solution diagram for (ii) and (iii), the paper’s diagram beside the ask). c(i) the answer 8 + the two halves of its explanation 2 + 2; c(ii) one answer for each good, the 1st correct 8 (6 + 2) and the 2nd 5 (3 + 2).',
  'The determinants of demand are The Consumer (Demand) (1-1); market demand, supply and equilibrium are The Market Economy (1-0); a subsidy shifting supply is The Firm (Supply) (1-2), and the subsidy also Government Intervention (1-3); price elasticity of demand, luxuries and necessities are Elasticity (1-4).', also=['1-3'])
q('B4', [7], [18, 19, 20],
  [T('a/i', 12, 'sb-q4-a-i', '3-0'), T('a/ii', 13, 'sb-q4-a-ii', '3-0'), T('b/i', 12, 'sb-q4-b-i', '3-0'),
   T('b/ii', 8, 'sb-q4-b-ii', '3-0'), T('c/i', 10, 'sb-q4-c-i', '3-2'), T('c/ii', 10, 'sb-q4-c-ii', '3-2'),
   T('c/iii', 10, 'sb-q4-c-iii', '3-2')],
  'Seven tasks totalling 75. a(i) the four lines at 3 (lines 1 and 2 at 2 + 1); a(ii) households and firms 5 (either), households and foreign markets 4, firms and foreign markets 4. b(i) the working 10 (five underlined components at 2) + the answer 2 (hidden solution working); b(ii) 8. c(i) each term 5, its two halves at 3 and 2; c(ii) 2 at 5 (2 + 3) from six; c(iii) one effect each on the labour market and on the demand for state services at 5 (2 + 3).',
  'The circular flow, national income with trade and the multiplier are National Income (3-0); emigration and immigration, their causes and effects are Employment & Unemployment (3-2).')
q('B5', [8], [21, 22],
  [T('a/i-iii', 20, 'sb-q5-a', '3-1'), T('b/i', 20, 'sb-q5-b-i', '3-1'), T('b/ii', 5, 'sb-q5-b-ii', '3-1'),
   T('c/i', 10, 'sb-q5-c-i', '1-3'), T('c/ii', 10, 'sb-q5-c-ii', '3-1'), T('c/iii', 10, 'sb-q5-c-iii', '3-1')],
  'Six cards for eight asks totalling 75. a(i)-(iii) one card, the scheme printing (7 marks +7 marks +6 marks) beneath its three terms without saying which earns which: one ladder, one explanation per term. b(i) each canon 5; b(ii) one principle 5 from four. c(i), (ii) and (iii) each 2 at 5 from the scheme’s points for that proposal (3 x 10).',
  'Direct tax, capital spending, the national debt, the canons of taxation, the retirement age and a household property tax are Fiscal Policy & the Budget (3-1), as 2012 OL files the household charge; third-level fees are Government Intervention (1-3), as 2011 OL files them; the retirement age’s effect on jobs is also The Labour Market (2-1), as 2015 HL files it.', also=['2-1'])
q('B6', [8], [23, 24, 25],
  [T('a/i-iii', 20, 'sb-q6-a', '3-4'), T('b/i', 6, 'sb-q6-b-i', '3-4'), T('b/ii', 10, 'sb-q6-b-ii', '3-4'),
   T('b/iii', 4, 'sb-q6-b-iii', '3-4'), T('c/i', 10, 'sb-q6-c-i', '3-3'), T('c/ii', 15, 'sb-q6-c-ii', '3-3'),
   T('c/iii', 10, 'sb-q6-c-iii', '3-4')],
  'Seven cards for nine asks totalling 75. a(i)-(iii) one card, the scheme printing (7 marks +7 marks + 6 marks) beneath its three terms without saying which earns which: one ladder, one explanation per term. b(i) 2 banks at 3 from four; b(ii) 2 at 5 (3 + 2) from six; b(iii) 4 (2 + 2) from five; the paper prints b as “(i) ... (i) ... (ii)”, an SEC misprint, and the scheme and the reader number them (i)-(iii). c(i) 10; c(ii) one effect each on borrowers, savers and the Irish economy at 5 (3 + 2); c(iii) 2 at 5 (3 + 2) from eight.',
  'Barter, interest rates, creditworthiness, commercial banks and the Central Bank’s functions are Financial Sector (3-4), as 2017 OL files money, barter and interest rates; the ECB and a rise in its interest rate are Monetary Policy & Inflation (3-3).')
q('B7', [9], [26, 27, 28, 29],
  [T('a/i', 6, 'sb-q7-a-i', '3-0'), T('a/ii', 4, 'sb-q7-a-ii', '3-3'), T('a/iii', 15, 'sb-q7-a-iii', '3-3'),
   T('b/i', 8, 'sb-q7-b-i', '3-4'), T('b/ii', 4, 'sb-q7-b-ii', '3-4'), T('b/iii', 8, 'sb-q7-b-iii', '3-0'),
   T('c/i', 10, 'sb-q7-c-i', '3-0'), T('c/ii', 10, 'sb-q7-c-ii', '3-0'), T('c/iii', 10, 'sb-q7-c-iii', '3-0')],
  'Nine tasks totalling 75. a(i) 6; a(ii) 4; a(iii) one effect each on social welfare recipients, savers and employees at 5 (3 + 2). b(i) 8; b(ii) 4 (2 + 2) from four; b(iii) 2 at 4 (2 + 2) from five. c(i) the explanation 4 + one other example 6, either of two; c(ii) 2 at 5 (3 + 2) from six; c(iii) 2 at 5 from seven.',
  'The CSO is National Income (3-0), as 2016 OL files it; deflation and its effects are Monetary Policy & Inflation (3-3); savings and why they rise are Financial Sector (3-4), as 2017 OL files savings; spending rather than saving is National Income (3-0); the black economy and cigarette smuggling are National Income (3-0), as earlier reviews file the black economy, and the lost tax revenue also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q('B8', [9], [30, 31, 32],
  [T('a/i', 7, 'sb-q8-a-i', '4-2'), T('a/ii', 18, 'sb-q8-a-ii', '4-2'), T('b/i', 7, 'sb-q8-b-i', '4-2'),
   T('b/ii', 6, 'sb-q8-b-ii', '4-2'), T('b/iii', 12, 'sb-q8-b-iii', '4-2'), T('c/i-iii', 25, 'sb-q8-c', '4-2')],
  'Six cards for eight asks totalling 75. a(i) an open economy 5 + economic growth 2; a(ii) three reasons from five, the 1st correct 10 and the 2nd and 3rd 4. b(i) 7, the scheme printing 5 and 2 beneath the two halves of its sentence; b(ii) 2 examples at 3 from three; b(iii) two reasons from eight, the 1st correct 8 and the 2nd 4. c(i)-(iii) one card, the scheme pricing one effect per group on one ladder: the 1st correct 11 (6 + 5), the 2nd and 3rd 7 (4 + 3).',
  'The open economy, exports, invisible imports, restricting imports and the euro’s exchange rate against sterling are International Trade & Competitiveness (4-2); economic growth is also Economic Growth (3-5), and employment within Ireland Employment & Unemployment (3-2).', also=['3-5', '3-2'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer four questions. 5': ('exam-question-selection', 'Whole-exam selection (Section B, cover; read with the examiner box’s "5"); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces Q. Mark': ('exam-question-selection', 'Whole-exam selection (Section A, cover; read with the examiner box’s heads); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B. Credit will be': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 9': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 10)},
}
PAGE_SEL = {
 (2, '(iii) Firm has complete control over price or'): ('not-a-task-selection', 'Section A Q3(iii) statement, read on "or"; not a selection.'),
 (2, '3. Name the market structure (Perfect Competition, Imperfect Competition or Monopoly) to which each'): ('answer-classification', 'Section A Q3 the market structure is the answer for each statement; one card, three answers.'),
 (3, '7. The following items are either substitutes or complements for Mobile Phones. From the list below,'): ('answer-classification', 'Section A Q7 substitute or complement is the answer for each item; one card, four answers.'),
 (5, 'No. of seats'): ('not-a-task-selection', 'Section B Q2(b) diagram axis label, read on "of"; not a selection.'),
 (5, 'marginal utility sets in and explain your choice.'): ('not-a-task-selection', 'Section B Q2(a)(iii) "explain your choice" asks for the reason behind the answer; not a selection.'),
 (6, '3. (a) State and explain four factors which affect the demand for a good or service.'): ('not-a-task-selection', 'Section B Q3(a) "a good or service", read on "or"; not a selection.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

tasks = [t for x in Q for t in x['tasks']]
for x in Q:
    total = sum(t['marks'] for t in x['tasks'] if not t['cardId'].endswith(ALT))
    want = 75 if x['n'].startswith('B') else (16 if int(x['n']) <= 5 else 17)
    assert total == want, (x['n'], total, want)
draft = {
 'subjectId': 'economics', 'year': 2010, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 34)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 33 scheme pages (paper pages 10-12 are blank; scheme pages 1-3 are the SEC cover, a blank page and the title page with the index and support notes, and page 33 the back cover; scheme page numbers here are the PDF’s, one ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part; its cover prints the level in capitals, ORDINARY LEVEL, so its scheme file was built with the appenders’ cover check pointed at the file). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 74 printed asks (12 Section A + 62 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2010_ol.py). Section A Q1(i)-(ii) and Q3(i)-(iii), and Section B Q5(a)(i)-(iii), Q6(a)(i)-(iii) and Q8(c)(i)-(iii) are one card each, as the scheme prices them together. Section B Q6(b) is printed “(i) Name ... (i) Discuss ... (ii) Outline ...”, an SEC misprint; the scheme numbers the three parts (i)-(iii) and so does the reader, so the cards cite (b)(i)-(iii). Section A Q4 and Q9 print one total over their answer without dividing it, so each is a questionTotal card. No printed choice is credited with a list for each side.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2010-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
