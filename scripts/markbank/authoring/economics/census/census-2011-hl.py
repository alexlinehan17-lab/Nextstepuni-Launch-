"""Write the independent 2011 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2011 Higher
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2011/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2011/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2011-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once. Section B Q5(b)(ii) is a printed choice
# (four arguments in favour OR four against) whose scheme credits each side
# with its own column: one route each, the first counted.
ALT = ('-against',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '3-3')],
  'Four steps from five at 4.',
  'Constructing the CPI is Monetary Policy & Inflation (3-3).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '1-0')],
  '16 (12 + 4): the definition 12 and the two examples 4 between them, 2 each, from five (read in printed order, as 2014 HL prices its explanation 12 and example 4).',
  'A mixed economy is The Market Economy (1-0), as earlier reviews file economic systems.')
q(3, [2], [6], [T('i/ii/iii/iv', 16, 'sa-q3', '2-0')],
  'One card for the four statements, 4 each: the paper numbers them (i)-(iv), and the card covers all four.',
  'Perfect competition, imperfect competition and monopoly are Market Structures (2-0).')
q(4, [2], [6], [T('all', 16, 'sa-q4', '3-1')],
  'Three areas from nine: 10 + 4 + 2.',
  'The NTMA and the national debt are Fiscal Policy & the Budget (3-1).')
q(5, [2], [6], [T('all', 16, 'sa-q5', '2-1')],
  '16 (12 + 4): the definition 12 and the two factors 4 between them, 2 each, from four (read as Q2 is).',
  'Occupational mobility of labour is The Labour Market (2-1).')
q(6, [3], [7], [T('all', 17, 'sa-q6', '4-2')],
  'Two effects from five: 9 + 8.',
  'A falling euro against the dollar is International Trade & Competitiveness (4-2).')
q(7, [3], [7], [T('all', 17, 'sa-q7', '4-1')],
  'Three reasons from five: 10 + 5 + 2.',
  'Multinationals re-locating to Southeast Asia are Globalisation (4-1).')
q(8, [3], [8], [T('all', 17, 'sa-q8', '1-4')],
  '17 (8 + 5 + 2 + 2), read in printed order: the formula and working 8 (hidden working crop), the answer 5, complement 2, the negative CED 2.',
  'Cross elasticity of demand is Elasticity (1-4).')
q(9, [3], [8], [T('all', 17, 'sa-q9', '3-4')],
  'Two reasons from four and two actions from six on one ladder: 5 + 4 + 4 + 4.',
  'Mortgage arrears and what lenders can do are Financial Sector (3-4).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [9, 10, 11],
  [T('a/i', 6, 'sb-q1-a-i', '1-1'), T('a/ii', 14, 'sb-q1-a-ii', '1-1'), T('b/i', 16, 'sb-q1-b-i', '1-1'),
   T('b/ii', 14, 'sb-q1-b-ii', '1-1'), T('c/i', 12, 'sb-q1-c-i', '1-1'), T('c/ii', 13, 'sb-q1-c-ii', '1-1')],
  'Six tasks totalling 75. a(i) the two definitions 6, which the scheme does not divide: questionTotal, unpriced rows; a(ii) each consumer’s diagram 3 (its axes and D/C at 1), the market diagram 5 (its axes at 1 and the cumulative D/C 3) and the explanation 3 (hidden solution diagrams). b(i) a movement along 8 and a shift 8, each with its diagram (hidden solution diagrams); b(ii) 2 at 7 from six. c(i) 2 at 6 from four; c(ii) 13 (9 + 4), the working 9 and the answer 4 in printed order (hidden working crop).',
  'Individual and market demand, movements along and shifts in demand, diminishing marginal utility and the equi-marginal principle are The Consumer (Demand) (1-1).')
q('B2', [4], [12, 13, 14, 15],
  [T('a/i', 15, 'sb-q2-a-i', '2-0'), T('a/ii', 10, 'sb-q2-a-ii', '2-0'), T('b/i-ii', 25, 'sb-q2-b', '2-0'),
   T('c/i-ii', 25, 'sb-q2-c', '2-0')],
  'Four cards for six asks totalling 75. a(i) 3 at 5 from six; a(ii) 2 at 5 from four. b(i)-(ii) one card, as the scheme prices one diagram for both: the diagram 9 (its nine elements at 1, hidden solution diagram), the shape 8 and the equilibrium 8, neither divided. c(i)-(ii) one card, as the scheme prices the two reasons and two benefits on one ladder: 7 + 6 + 6 + 6.',
  'Oligopoly, the kinked demand curve and price and non-price competition are Market Structures (2-0).')
q('B3', [5], [16, 17, 18, 19],
  [T('a/i', 5, 'sb-q3-a-i', '2-1'), T('a/ii', 10, 'sb-q3-a-ii', '2-1'), T('a/iii', 10, 'sb-q3-a-iii', '2-1'),
   T('b/i', 15, 'sb-q3-b-i', '3-5'), T('b/ii', 15, 'sb-q3-b-ii', '3-5'), T('c', 20, 'sb-q3-c', '2-2')],
  'Six tasks totalling 75. a(i) 5; a(ii) 2 at 5 from seven; a(iii) 2 at 5 from three. b(i) 3 at 5 from six; b(ii) 3 at 5 from eight. c 2 advantages at 5 from seven + 2 disadvantages at 5 from seven.',
  'Marginal revenue productivity is The Labour Market (2-1); investment and what influences it are Economic Growth (3-5) and also National Income (3-0); public transport against new roads is externalities, Market Failure (2-2), as 2014 HL files a public investment’s social costs and benefits.', also=['3-0'])
q('B4', [5], [20, 21, 22],
  [T('a/i', 12, 'sb-q4-a-i', '1-5'), T('a/ii', 18, 'sb-q4-a-ii', '1-5'), T('b/i', 15, 'sb-q4-b-i', '4-2'),
   T('b/ii', 15, 'sb-q4-b-ii', '1-2'), T('c', 15, 'sb-q4-c', '2-2')],
  'Five tasks totalling 75. a(i) the three calculations 12, which the scheme does not divide: questionTotal, unpriced rows (the paper’s table beside the ask, hidden working crop); a(ii) the diagram 12 and the explanation 6 (hidden solution diagram). b(i) 3 at 5 from six; b(ii) 3 at 5 from six. c two private costs from eight and two social costs from five on one ladder: 4 + 4 + 4 + 3.',
  'Marginal and average cost, profit and the short-run AC curve are Costs of Production, Revenue & Profit (1-5); falling costs and competitiveness are International Trade & Competitiveness (4-2); restrictions on business growth are The Firm (Supply) (1-2); the private and social costs of an oil spill are externalities, Market Failure (2-2).')
q('B5', [6], [23, 24, 25],
  [T('a/i', 10, 'sb-q5-a-i', '3-1'), T('a/ii', 20, 'sb-q5-a-ii', '3-1'), T('b/i', 5, 'sb-q5-b-i', '1-3'),
   T('b/ii', 20, 'sb-q5-b-ii-favour', '1-3'), T('b/ii', 20, 'sb-q5-b-ii-against', '1-3'), T('c', 20, 'sb-q5-c', '3-1')],
  'Five tasks totalling 75. a(i) 10; a(ii) 4 at 5 from eight. b(i) 5; b(ii) four arguments in favour OR four against is a printed choice and the scheme credits each with its own column, 4 at 5: one route each, counted once. c four measures from five: 7 + 7 + 3 + 3.',
  'Fiscal policy, reducing the deficit and the public sector wage bill are Fiscal Policy & the Budget (3-1); privatisation is Government Intervention (1-3), as earlier reviews file it.')
q('B6', [6], [26, 27, 28],
  [T('a/i', 20, 'sb-q6-a-i', '3-4'), T('a/ii', 8, 'sb-q6-a-ii', '3-3'), T('a/iii', 7, 'sb-q6-a-iii', '3-4'),
   T('b', 20, 'sb-q6-b', '3-4'), T('c', 20, 'sb-q6-c', '3-3')],
  'Five tasks totalling 75. a(i) the four functions at 5; a(ii) 8; a(iii) 7. b 4 at 5 from six. c 4 at 5 from nine.',
  'The functions of money, the lender of last resort and bank regulation are Financial Sector (3-4); monetary policy and rising interest rates are Monetary Policy & Inflation (3-3).')
q('B7', [7], [29, 30, 31],
  [T('a/i', 14, 'sb-q7-a-i', '3-0'), T('a/ii', 16, 'sb-q7-a-ii', '3-0'), T('b/i', 8, 'sb-q7-b-i', '3-0'),
   T('b/ii', 8, 'sb-q7-b-ii', '3-0'), T('b/iii', 9, 'sb-q7-b-iii', '3-0'), T('c', 20, 'sb-q7-c', '3-5')],
  'Six tasks totalling 75. a(i) GDP 7 + GNP 7; a(ii) 16 over three reasons for an ask of two: 8 each. b(i) 8; b(ii) 8 by either method (hidden working crop); b(iii) 9 over three points the scheme does not divide: questionTotal, unpriced rows. c 4 at 5 from eleven, positive and negative.',
  'GDP, GNP and the multiplier are National Income (3-0); the effects of faster economic growth are Economic Growth (3-5).')
q('B8', [7], [32, 33, 34, 35],
  [T('a', 20, 'sb-q8-a', '3-5'), T('b', 25, 'sb-q8-b', '3-2'), T('c/i', 10, 'sb-q8-c-i', '3-2'), T('c/ii', 20, 'sb-q8-c-ii', '3-1')],
  'Four tasks totalling 75. a 4 at 5 from eight, at least one for government and one for business. b the compulsory point 4 + 3 other points at 7 from five. c(i) 2 at 5 from eight; c(ii) 4 at 5 from ten, positive and negative.',
  'The census and its uses are Economic Growth (3-5), as 2016 OL and 2017 OL file it; net outward migration and measures to reduce unemployment are Employment & Unemployment (3-2); the EU/IMF financial support is Fiscal Policy & the Budget (3-1).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (1, 'Answer four questions. 5'): ('exam-question-selection', 'Whole-exam selection (Section B), read beside the cover’s marking grid; every printed task stays in the census.'),
 (1, 'Answer six of the nine short response type questions in the spaces Q. Mark'): ('exam-question-selection', 'Whole-exam selection (Section A), read beside the cover’s marking grid; every printed task stays in the census.'),
 (2, '3. Name the market structure (Perfect Competition, Imperfect Competition or Monopoly) to which'): ('answer-classification', 'Section A Q3 the market structure is the answer for each statement; one card, four answers.'),
 (3, 'Is Good A a substitute for, or a complement to,'): ('answer-classification', 'Section A Q8 substitute or complement is the answer (a complement); one card.'),
 (3, 'payments) of 90 days or more. Outline two economic reasons for this development and two actions'): ('not-a-task-selection', 'Section A Q9 ask wording, read on "or"; not a selection.'),
 (5, '(b) ‘The cost of doing business in Ireland is falling. However, some costs continue to increase or'): ('not-a-task-selection', 'Section B Q4(b) stem wording, read on "or"; not a selection.'),
 (6, '(ii) Outline four economic arguments in favour of privatisation OR outline four economic'): ('finite-route', 'Section B Q5(b)(ii) four arguments in favour OR four against: the scheme credits each with its own column, so one route each, counted once.'),
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
 'subjectId': 'economics', 'year': 2011, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 9)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 8 paper and 40 scheme pages (paper page 8 is blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the support notes with the index, and pages 36-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 55 printed asks (12 Section A + 43 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2011_hl.py). Section A Q3(i)-(iv), Section B Q2(b)(i)-(ii) and Q2(c)(i)-(ii) are one card each, as the scheme prices them together; Section B Q5(b)(ii) (in favour OR against) is one route for each side the scheme credits, counted once.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2011-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
