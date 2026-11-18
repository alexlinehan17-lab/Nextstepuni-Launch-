"""Write the independent 2016 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2016 Higher
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2016/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2016/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2016-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once beyond the first (none on this paper: the
# Section B Q8(a) areas are four parts of one ask, each counted).
ALT = ()

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('a', 9, 'sa-q1-a', '2-0'), T('b/i', 3, 'sa-q1-b-i', '2-0'), T('b/ii', 4, 'sa-q1-b-ii', '2-0')],
  'a 3 x 3 the three labelled lines; b(i) 3 the shaded supernormal profit (hidden solution diagram); b(ii) 4.',
  'Short-run equilibrium and supernormal profit in perfect competition are Market Structures (2-0).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '1-5')],
  '10 the definition and 6 any suitable example explained: one card, two rows.',
  'The law of diminishing marginal returns is Costs of Production, Revenue & Profit (1-5).')
q(3, [2], [6], [T('all', 16, 'sa-q3', '2-1')],
  '2 x 8 two ways from eight, under the scheme’s occupational and geographical mobility heads.',
  'The mobility of labour is The Labour Market (2-1); reducing unemployment is Employment & Unemployment (3-2).', also=['3-2'])
q(4, [3], [6], [T('all', 16, 'sa-q4', '1-5')],
  '10 the explanation and 6 one example from six, which must refer to the aircraft industry.',
  'Economies of scale are Costs of Production, Revenue & Profit (1-5).')
q(5, [3], [7], [T('a', 10, 'sa-q5-a', '3-2'), T('b', 6, 'sa-q5-b', '3-2')],
  'a 2 x 5 (2 + 3) two effects from eight; b 6 one policy from eight.',
  'Youth unemployment and policies against it are Employment & Unemployment (3-2).')
q(6, [3], [8], [T('i', 9, 'sa-q6-i', '1-4'), T('ii', 8, 'sa-q6-ii', '1-4')],
  'i 9, the scheme’s raised 1 beside each of nine items of the working; ii 4 the + sign (a normal good) + 4 the 6.67 (a luxury good).',
  'Income elasticity of demand is Elasticity (1-4).')
q(7, [4], [8], [T('a', 9, 'sa-q7-a', '3-3'), T('b', 8, 'sa-q7-b', '3-3')],
  'a 9, 3 each beside the money supply, interest rates and the availability of credit; b 2 x 4 two benefits from seven.',
  'Monetary policy and price stability are Monetary Policy & Inflation (3-3).')
q(8, [4], [9], [T('a-b', 17, 'sa-q8', '1-3')],
  'One card for both asks: the scheme prices the two effects of (a) and the one method of (b) on one ladder, 7 (4 + 3) for the first correct response and 5 (3 + 2) for each other, so neither part has a price of its own.',
  'A levy on insurance premiums and measures against flooding are Government Intervention (1-3); the levy is also a tax (Fiscal Policy & the Budget, 3-1), and climate measures Sustainability (0-2).', also=['3-1', '0-2'])
q(9, [4], [10], [T('all', 17, 'sa-q9', '2-1')],
  '7 (4 + 3) + 5 (3 + 2) + 5 (3 + 2) any three impacts from fourteen, positive or negative, the first correct response 7.',
  'The national minimum wage is The Labour Market (2-1).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [11, 12, 13],
  [T('a/i', 20, 'sb-q1-a-i', '1-2'), T('a/ii', 15, 'sb-q1-a-ii', '1-2'),
   T('b/i', 6, 'sb-q1-b-i', '1-4'), T('b/ii', 6, 'sb-q1-b-ii', '1-4'), T('b/iii', 6, 'sb-q1-b-iii', '1-4'),
   T('b/iv', 6, 'sb-q1-b-iv', '1-4'), T('c', 16, 'sb-q1-c', '1-0')],
  'Seven tasks totalling 75. a(i) 4 x 5 (2 + 3) four factors from six; a(ii) movement 8 (diagram 3 + explanation 5) and shift 7 (diagram 2 + explanation 5) (hidden solution diagrams). b(i)-(iv) each TRUE/FALSE 2 + explanation 4. c 12 the diagram + 4 the explanation (hidden solution diagram).',
  'The supply of a good and its curve are The Firm (Supply) (1-2); cross, price and income elasticity are Elasticity (1-4); a ticket shortage from demand and supply is The Market Economy (1-0).')
q('B2', [5], [14, 15, 16, 17],
  [T('a/i', 7, 'sb-q2-a-i', '2-0'), T('a/ii', 10, 'sb-q2-a-ii', '2-0'), T('a/iii', 18, 'sb-q2-a-iii', '2-0'),
   T('b/i', 15, 'sb-q2-b-i', '2-0'), T('b/ii', 10, 'sb-q2-b-ii', '2-0'), T('c', 15, 'sb-q2-c', '2-0')],
  'Six tasks totalling 75. a(i) 7 oligopoly with its reason, printed as one 7: questionTotal, unpriced rows; a(ii) 2 x 5 (2 + 3) from seven; a(iii) the diagram 5 (P, Q, AB, BC, P1 at 1 each), the overall curve 3, AB 5 and BC 5 (hidden solution diagram). b(i) 3 x 5 (2 + 3) from five; b(ii) 2 x 5 (2 + 3) from five. c 3 x 5 (2 + 3) from twelve, under the scheme’s small-firm and large-firm heads.',
  'Oligopoly, the kinked demand curve, market entry and the size of firms are Market Structures (2-0); economies of scale are also Costs of Production, Revenue & Profit (1-5).', also=['1-5'])
q('B3', [6], [18, 19, 20],
  [T('a/i-iv', 20, 'sb-q3-a', '2-1'), T('b/i', 20, 'sb-q3-b-i', '2-1'), T('b/ii', 15, 'sb-q3-b-ii', '2-1'),
   T('c', 20, 'sb-q3-c', '2-1')],
  'Four cards for seven asks, totalling 75. a(i)-(iv) share one ladder, the 1st correct response 8 and the 2nd, 3rd and 4th 4 each, so no term has a price of its own: one card covers the four. b(i) 4 x 5 (2 + 3) from six; b(ii) two challenges 7 (4 + 3) and a policy for each 8 (4 + 4), under the scheme’s excess supply and excess demand heads. c 4 x 5 (2 + 3) from nine.',
  'The participation rate, real wages, productivity, derived demand, the supply of labour and wage differences are The Labour Market (2-1); the labour market’s challenges include unemployment (Employment & Unemployment, 3-2).', also=['3-2'])
q('B4', [6], [21, 22, 23, 24],
  [T('a/i', 10, 'sb-q4-a-i', '1-5'), T('a/ii', 5, 'sb-q4-a-ii', '1-5'),
   T('b/i', 10, 'sb-q4-b-i', '1-5'), T('b/ii', 8, 'sb-q4-b-ii', '1-5'), T('b/iii', 12, 'sb-q4-b-iii', '1-5'),
   T('c/i', 15, 'sb-q4-c-i', '4-2'), T('c/ii', 15, 'sb-q4-c-ii', '4-2')],
  'Seven tasks totalling 75. a(i) 10 (5 + 5) the short run and the long run; a(ii) 5. b(i) 2 x 5; b(ii) 4 + 4 the MR and MC columns; b(iii) the graph 5 (price, quantity, MR, MC and the profit-maximising output at 1 each), the output 3 and the explanation 4 (hidden solution graph). c(i) 3 x 5 (2 + 3) from nine; c(ii) 3 x 5 (2 + 3) from eight.',
  'Production periods, marginal revenue and cost and profit maximisation are Costs of Production, Revenue & Profit (1-5); competitiveness is International Trade & Competitiveness (4-2).')
q('B5', [7], [25, 26, 27],
  [T('a/i', 5, 'sb-q5-a-i', '3-2'), T('a/ii', 20, 'sb-q5-a-ii', '3-2'),
   T('b/i', 6, 'sb-q5-b-i', '3-0'), T('b/ii', 6, 'sb-q5-b-ii', '3-0'), T('b/iii', 8, 'sb-q5-b-iii', '3-0'),
   T('b/iv', 10, 'sb-q5-b-iv', '3-0'), T('c', 20, 'sb-q5-c', '3-0')],
  'Seven tasks totalling 75. a(i) 5; a(ii) 2 x 5 (2 + 3) benefits and 2 x 5 (2 + 3) challenges. b(i) 6; b(ii) 6; b(iii) the starred working 4 (1 each, by either method) + the answer 4; b(iv) 10, 2 beside each of five figures of the working. c 2 x 10 (4 + 6) any two of three.',
  'Full employment is Employment & Unemployment (3-2); the MPS, the multiplier, the injection needed and GDP are National Income (3-0).')
q('B6', [7], [28, 29, 30, 31],
  [T('a/i', 5, 'sb-q6-a-i', '4-2'), T('a/ii', 20, 'sb-q6-a-ii', '4-2'),
   T('b/i', 17, 'sb-q6-b-i', '4-2'), T('b/ii', 7, 'sb-q6-b-ii', '4-2'), T('b/iii', 6, 'sb-q6-b-iii', '4-2'),
   T('c', 20, 'sb-q6-c', '4-2')],
  'Six tasks totalling 75. a(i) 5; a(ii) 4 x 5 (2 + 3) from five. b(i) 7 + 7 + 3 the current, capital and financial accounts; b(ii) 7; b(iii) 6 (3 + 3) one problem from seven. c 2 x 5 (2 + 3) benefits and 2 x 5 (2 + 3) challenges.',
  'Exchange rates, the balance of payments and SMEs in foreign markets are International Trade & Competitiveness (4-2); trading abroad is also Globalisation (4-1).', also=['4-1'])
q('B7', [8], [32, 33, 34, 35],
  [T('a', 20, 'sb-q7-a', '3-1'), T('b/i', 16, 'sb-q7-b-i', '3-1'), T('b/ii', 14, 'sb-q7-b-ii', '3-1'),
   T('c', 25, 'sb-q7-c', '0-2')],
  'Four tasks totalling 75. a 2 x 10 (5 + 5) any two of three pairs: one card. b(i) 2 x 8 (3 + 5) from seven; b(ii) 2 x 7 (3 + 4) from five. c 4 points, 7 (4 + 3) for the first correct response and 6 (3 + 3) for each other, from five.',
  'Income and wealth, progressive and regressive taxes, the impact and incidence of a tax and policies against inequality are Fiscal Policy & the Budget (3-1); protecting the environment is Sustainability (0-2) and, by taxes, subsidies and regulation, Government Intervention (1-3).', also=['1-3'])
q('B8', [8], [36, 37, 38, 39],
  [T('a', 5, 'sb-q8-a-growth', '3-5'), T('a', 5, 'sb-q8-a-prices', '3-3'), T('a', 5, 'sb-q8-a-unemployment', '3-2'),
   T('a', 5, 'sb-q8-a-interest', '3-3'), T('b/i', 21, 'sb-q8-b-i', '3-1'), T('b/ii', 14, 'sb-q8-b-ii', '3-1'),
   T('c', 20, 'sb-q8-c', '3-5')],
  'Seven cards for four asks, totalling 75. a 4 x 5, one card for each printed area, each 2 (approximate figure) + 3 (trend 1 + comment 2) with no row the scheme ties them to: questionTotal, unpriced rows. b(i) 3 x 7 (3 + 4), at least one under each of the budget deficit and gross debt heads; b(ii) 2 x 7 (3 + 4) from four. c 4 x 5 (2 + 3), at least one positive and one negative.',
  'Economic growth is Economic Growth (3-5), the price level and interest rates Monetary Policy & Inflation (3-3), unemployment Employment & Unemployment (3-2); the budget deficit, gross debt and their costs are Fiscal Policy & the Budget (3-1); an urbanising population is Economic Growth (3-5), as population change is filed.')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 12': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 13)},
}
PAGE_SEL = {
 (5, '(b) Read the following statements and indicate if they are TRUE or FALSE.'): ('answer-classification', 'Section B Q1(b) TRUE or FALSE is the answer for each of four statements; one card each, the answer 2 and its explanation 4.'),
 (5, '1. (a) (i) Outline four factors that determine the supply of a good or service.'): ('not-a-task-selection', 'Section B Q1(a)(i) ask wording, read on "or"; not a selection.'),
 (7, '(c) Explain how Ireland’s Gross Domestic Product (GDP) could be affected by any two of the'): ('finite-route', 'Section B Q5(c) any two of three developments: one card claimed twice at 10.'),
 (8, '7. (a) In the case of any two of the following three pairs, distinguish between the two concepts.'): ('finite-route', 'Section B Q7(a) any two of three pairs: one card claimed twice at 10.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

tasks = [t for x in Q for t in x['tasks']]
for x in Q:
    total = sum(t['marks'] for t in x['tasks'] if not ALT or not t['cardId'].endswith(ALT))
    want = 75 if x['n'].startswith('B') else (16 if int(x['n']) <= 5 else 17)
    assert total == want, (x['n'], total, want)
draft = {
 'subjectId': 'economics', 'year': 2016, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (paper pages 9-12 are blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index, and page 40 the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 63 printed asks (15 Section A + 48 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2016_hl.py). Two cards cover more than one printed ask because the scheme prices them on one ladder: Section A Q8(a)-(b) and Section B Q3(a)(i)-(iv). Section B Q8(a) is one card per printed area. Printed choices are one card each: Section B Q5(c) and Q7(a), any two of three.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2016-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
