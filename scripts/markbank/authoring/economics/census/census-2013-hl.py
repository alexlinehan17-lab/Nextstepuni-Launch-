"""Write the independent 2013 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2013 Higher
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2013/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2013/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2013-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: Section B Q6(a)(i) is answered by either of
# the scheme's two alternatives (the reserve ratio, or a bank's balance
# sheets), each credited with its own points; the first is the one counted.
ALT = ('-balance-sheet',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '0-1')],
  'Any 2 points at 8 from the scheme’s one answer: one card, its sentences claimed twice.',
  'Scarcity, unlimited wants and choice are Scarcity & Choice (0-1).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '1-5')],
  'The definition 8 + any 2 reasons at 4 (2 + 2) from four.',
  'The marginal efficiency of capital is Costs of Production, Revenue & Profit (1-5), as 2017 HL files it.')
q(3, [2], [5], [T('all', 16, 'sa-q3', '1-4')],
  'The four ticks at 4: one card.',
  'Price elasticity of demand is Elasticity (1-4).')
q(4, [2], [6], [T('a', 8, 'sa-q4-a', '2-0'), T('b', 8, 'sa-q4-b', '2-0')],
  'a 8; b any 2 points at 4 from three.',
  'Collusion and price wars in oligopoly are Market Structures (2-0).')
q(5, [2], [6], [T('all', 16, 'sa-q5', '4-2')],
  'Three mechanisms from six: 6 + 5 + 5.',
  'Trade barriers are International Trade & Competitiveness (4-2).')
q(6, [3], [6], [T('all', 17, 'sa-q6', '3-0')],
  '7 + 6 + 4 for the scheme’s one answer, which it does not divide into points: questionTotal, unpriced rows.',
  'The paradox of thrift and the circular flow are National Income (3-0).')
q(7, [3], [7], [T('all', 17, 'sa-q7', '0-0')],
  'Four contributions from ten: 5 + 4 + 4 + 4.',
  'Adam Smith’s contributions are Economics as a Way of Thinking (0-0).')
q(8, [3], [7], [T('all', 17, 'sa-q8', '3-0')],
  'The definition 9 + the APC 8: the three starred figures at 2 and the two bold figures at 1 (hidden working crop).',
  'The average propensity to consume is National Income (3-0).')
q(9, [3], [8], [T('a-b', 17, 'sa-q9', '1-3')],
  'One card for both asks: the scheme prices the private and social cost of (a) and the advantage and disadvantage of (b) on one ladder, the 1st correct answer 5 and the next 3 at 4.',
  'A minimum price for alcohol is Government Intervention (1-3); the private and social costs of alcohol abuse are also Market Failure (2-2).', also=['2-2'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [9, 10, 11],
  [T('a/i', 11, 'sb-q1-a-i', '1-1'), T('a/ii', 14, 'sb-q1-a-ii', '1-1'), T('b/i', 10, 'sb-q1-b-i', '1-0'),
   T('b/ii', 10, 'sb-q1-b-ii', '1-0'), T('b/iii', 10, 'sb-q1-b-iii', '1-0'), T('c/i', 10, 'sb-q1-c-i', '1-1'),
   T('c/ii', 10, 'sb-q1-c-ii', '1-1')],
  'Seven tasks totalling 75. a(i) the 1st correct response 7 (4 + 3) and the 2nd 4 (2 + 2); a(ii) 2 at 7 (4 + 3) from four. b each 10: the diagram 5 (its elements at 1) + the shift 1 + the reason 2 + the new price 1 + the new quantity 1 (hidden solution diagrams). c(i) 2 explanations at 5; c(ii) 2 explanations at 3 + the conclusion 4.',
  'Effective demand, the exceptions to the law of demand and the substitution and income effects are The Consumer (Demand) (1-1); shifts in a market’s demand and supply are The Market Economy (1-0); derived demand is also The Labour Market (2-1).', also=['2-1'])
q('B2', [4], [12, 13, 14, 15],
  [T('a/i', 15, 'sb-q2-a-i', '2-0'), T('a/ii', 10, 'sb-q2-a-ii', '2-0'), T('b', 25, 'sb-q2-b', '2-0'),
   T('c/i', 7, 'sb-q2-c-i', '2-0'), T('c/ii', 6, 'sb-q2-c-ii', '2-0'), T('c/iii', 12, 'sb-q2-c-iii', '2-0')],
  'Six tasks totalling 75. a(i) 3 at 5 (2 + 3) from eight; a(ii) 2 at 5 (2 + 3) from eight. b the diagram 10 points at 1 + the explanation 15 under the scheme’s five numbered heads (hidden solution diagram). c(i) 7; c(ii) the explanation 3 + the example 3; c(iii) 2 at 6 (3 + 3) from five.',
  'Barriers to entry, monopoly and competitive advertising are Market Structures (2-0).')
q('B3', [5], [16, 17, 18, 19],
  [T('a', 25, 'sb-q3-a', '2-1'), T('b', 25, 'sb-q3-b', '2-1'), T('c/i', 10, 'sb-q3-c-i', '2-1'),
   T('c/ii', 5, 'sb-q3-c-ii', '2-1'), T('d', 10, 'sb-q3-d', '0-0')],
  'Five tasks totalling 75. a four influences from nine, the first 3 at 7 (4 + 3) and the 4th 4 (2 + 2). b each market its diagram 5 (hidden solution diagrams) + its explanation, 7 (4 + 3) for the free market and 8 (4 + 4) with the minimum wage. c(i) 2 at 5 (2 + 3) from seven; c(ii) 5 (2 + 3) from eight. d 10 (6 + 4).',
  'A firm’s demand for labour, wage determination, a minimum wage and the gender pay gap are The Labour Market (2-1); Marx’s theory of exploitation is Economics as a Way of Thinking (0-0).')
q('B4', [5], [20, 21, 22],
  [T('a/i', 20, 'sb-q4-a-i', '3-1'), T('a/ii', 10, 'sb-q4-a-ii', '3-1'), T('b/i', 12, 'sb-q4-b-i', '3-1'),
   T('b/ii', 18, 'sb-q4-b-ii', '3-1'), T('c', 15, 'sb-q4-c', '3-1')],
  'Five tasks totalling 75. a(i) 4 at 5 (2 + 3) from eight; a(ii) 2 at 5 (2 + 3) from five. b(i) 2 at 6 (3 + 3) from six; b(ii) 3 at 6 (3 + 3) from six. c two arguments from four, the 1st 10 (5 + 5) and the 2nd 5 (2 + 3).',
  'The current budget deficit, the budget and income inequality, excise duties, motor tax and capital expenditure are Fiscal Policy & the Budget (3-1); taxes to curb smoking and drinking are also Government Intervention (1-3).', also=['1-3'])
q('B5', [6], [23, 24, 25],
  [T('a', 15, 'sb-q5-a', '3-0'), T('b/i', 18, 'sb-q5-b-i', '3-0'), T('b/ii', 5, 'sb-q5-b-ii', '3-0'),
   T('b/iii', 12, 'sb-q5-b-iii', '3-0'), T('c/i', 13, 'sb-q5-c-i', '3-0'), T('c/ii', 12, 'sb-q5-c-ii', '3-1')],
  'Six tasks totalling 75. a the three terms at 5. b(i) the diagram 18: the 5 sectors at 2 and the 8 flows at 1 (hidden solution diagram); b(ii) 5, the answer 2 + the explanation 3; b(iii) 3 at 4 (2 + 2) from six. c(i) 4 + 9; c(ii) two points from five, the 1st 8 (4 + 4) and the 2nd 4 (2 + 2).',
  'National income terms, the circular flow, injections, consumption and the multiplier are National Income (3-0); a Keynesian stimulus plan is Fiscal Policy & the Budget (3-1).')
q('B6', [6], [26, 27, 28, 29, 30],
  [T('a/i', 20, 'sb-q6-a-i-reserve-ratio', '3-4'), T('a/i', 20, 'sb-q6-a-i-balance-sheet', '3-4'),
   T('a/ii', 10, 'sb-q6-a-ii', '3-4'), T('b/i', 8, 'sb-q6-b-i', '3-3'), T('b/ii', 12, 'sb-q6-b-ii', '3-3'),
   T('c/i', 5, 'sb-q6-c-i', '3-3'), T('c/ii', 10, 'sb-q6-c-ii', '3-3'), T('c/iii', 10, 'sb-q6-c-iii', '3-3')],
  'Seven tasks totalling 75. a(i) 20 by either of the scheme’s alternatives, each credited with its own points: A, the four steps at 4 + the numerical example’s four starred figures at 1; B, the two balance sheets 4 + 6 + the explanation 5 at 2 (hidden solution crop): one route each, counted once. a(ii) 2 at 5 (2 + 3) from five. b(i) 2 at 4 (2 + 2) from five; b(ii) 2 at 6 (3 + 3) from nine. c(i) 5; c(ii) 2 at 5 (2 + 3) from five; c(iii) 2 at 5 (2 + 3) from seven.',
  'Credit creation and the banks’ ability to lend are Financial Sector (3-4); quantitative easing, interest rates and the CPI are Monetary Policy & Inflation (3-3).')
q('B7', [7], [31, 32, 33],
  [T('a/i', 6, 'sb-q7-a-i', '4-2'), T('a/ii', 12, 'sb-q7-a-ii', '4-2'), T('a/iii', 12, 'sb-q7-a-iii', '4-2'),
   T('b', 25, 'sb-q7-b', '4-2'), T('c', 20, 'sb-q7-c', '4-2')],
  'Five tasks totalling 75. a(i) 6; a(ii) 2 at 6 (3 + 3) from four; a(iii) 2 at 6 (3 + 3) from four. b 5 points at 5 (2 + 3) from six. c 4 points at 5 (2 + 3) from nine.',
  'The balance of payments, the euro’s exchange rate and the challenges on international markets are International Trade & Competitiveness (4-2); foreign firms in Ireland are also Globalisation (4-1).', also=['4-1'])
q('B8', [7], [34, 35, 36, 37],
  [T('a/i', 15, 'sb-q8-a-i', '3-2'), T('a/ii', 15, 'sb-q8-a-ii', '3-2'), T('b/i', 18, 'sb-q8-b-i', '3-1'),
   T('b/ii', 12, 'sb-q8-b-ii', '3-1'), T('c', 15, 'sb-q8-c', '3-5')],
  'Five tasks totalling 75. a(i) 3 at 5 (2 + 3) from seven; a(ii) 3 at 5 (2 + 3) from nine. b(i) 3 at 6 (3 + 3) from six; b(ii) 2 at 6 (3 + 3) from five. c 3 at 5 (2 + 3) from six.',
  'Youth unemployment and the measures against it are Employment & Unemployment (3-2); the national debt is Fiscal Policy & the Budget (3-1); an ageing population is Economic Growth (3-5), as 2015 HL files it, and its pressures on pensions and the labour supply Fiscal Policy & the Budget (3-1) and The Labour Market (2-1).', also=['2-1'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (2, '1. The fundamental economic problem is one of ‘scarcity’. Explain this concept.'): ('not-a-task-selection', 'Section A Q1 ask wording, read on "one"; not a selection.'),
 (2, 'likely to be elastic or inelastic. (Tick \uf0fc the correct box.)'): ('answer-classification', 'Section A Q3 elastic or inelastic is the answer for each statement; one card, four answers.'),
 (4, '(ii) If the price of an inferior product falls (all other things being equal) will more or less of'): ('answer-classification', 'Section B Q1(c)(ii) more or less is the answer, by the substitution and income effects; one card.'),
 (6, '(ii) Are transfer payments an injection into, or a leakage from the Circular Flow of Income?'): ('answer-classification', 'Section B Q5(b)(ii) injection or leakage is the answer (an injection); one card.'),
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
 'subjectId': 'economics', 'year': 2013, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 9)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 8 paper and 40 scheme pages (paper page 8 is blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the support notes with the index, and pages 38-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 57 printed asks (11 Section A + 46 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2013_hl.py). Section A Q9(a)-(b) is one card, as the scheme prices its four answers on one ladder. Section B Q6(a)(i) is one route for each of the scheme’s two alternatives, counted once.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2013-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
