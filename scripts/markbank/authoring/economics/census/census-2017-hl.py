"""Write the independent 2017 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; its Summary of Mark Allocations
(scheme pp5-40, printed 3-37; the 2017 scheme prints no summary table) is read part by part. There is no 2017 Higher Irish review, so
nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2017/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2017/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2017-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

ALT = ('-bad',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '3-1')],
  '2 at 8 marks each: two opportunity costs from six.',
  'Restoring public sector pay and its opportunity costs are Fiscal Policy & the Budget (3-1), opportunity cost Scarcity & Choice (0-1).', also=['0-1'])
q(2, [2], [5], [T('all', 16, 'sa-q2', '2-1')],
  '6 + 4 + 3 + 3, 1st correct response 6, 2nd 4, 3rd and 4th 3 each: one card, the four ticks claimed at 6, 4, 3, 3.',
  'The labour force, quasi-rent and capital widening are The Labour Market (2-1) and factor markets; bond prices and interest are Financial Sector (3-4).', also=['3-4'])
q(3, [2], [5], [T('a', 12, 'sa-q3-a', '3-1'), T('b', 4, 'sa-q3-b', '3-1')],
  'a 2 explanations at 5 + 2 examples at 1; b 4.',
  'Direct and indirect taxation and their equity are Fiscal Policy & the Budget (3-1).')
q(4, [3], [6], [T('all', 16, 'sa-q4', '3-4')],
  '6 + 5 + 5: three limitations from six, claimed at 6, 5, 5. The (i)-(iii) are ruled answer slots.',
  'Banks’ power to create credit is Financial Sector (3-4).')
q(5, [3], [6], [T('all', 16, 'sa-q5', '4-2')],
  '2 at 8 marks each: two consequences from eight. The (i)/(ii) are ruled answer slots.',
  'A fall in sterling against the euro is International Trade & Competitiveness (4-2).')
q(6, [3], [6], [T('a', 6, 'sa-q6-a', '2-0'), T('b', 11, 'sa-q6-b', '2-0')],
  'a Diagram: MR, AR (D), MC at 2 each (hidden solution diagram); b Explanation 11 graded over the printed points (unpriced rows).',
  'Long-run equilibrium in monopoly is Market Structures (2-0).')
q(7, [4], [7], [T('a', 12, 'sa-q7-a', '1-4'), T('b', 5, 'sa-q7-b', '1-4')],
  'a workings 8 (8 items at 1, printed as a fraction; hidden crop) + correct answer 4; b complement 2 + reason 3.',
  'Cross price elasticity of demand is Elasticity (1-4).')
q(8, [4], [7], [T('all', 17, 'sa-q8', '3-1')],
  '2 conflicts explained, 12 + 5, first correct response 12: one card, the two conflicts claimed at 12 then 5.',
  'Conflicting government policy objectives are Fiscal Policy & the Budget (3-1); growth is Economic Growth (3-5), the balance of payments International Trade & Competitiveness (4-2).', also=['3-5', '4-2'])
q(9, [4], [8], [T('all', 17, 'sa-q9', '3-1')],
  '2 points explained, 9 + 8, first correct response 9, one advantage and one disadvantage: one card, claimed at 9 then 8.',
  'Reintroducing third-level fees is Fiscal Policy & the Budget (3-1).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [9, 10, 11, 12],
  [T('a', 25, 'sb-q1-a', '1-0'), T('b/i', 10, 'sb-q1-b-i', '1-0'), T('b/ii', 10, 'sb-q1-b-ii', '1-0'),
   T('b/iii', 10, 'sb-q1-b-iii', '1-0'), T('c/i', 10, 'sb-q1-c-i', '1-3'), T('c/ii', 10, 'sb-q1-c-ii', '1-3')],
  'Six tasks totalling 75. a any two of three pairs: 1st correct response 7, remaining three 6 each, over four definitions: one menu of the six, claimed at 7, 6, 6, 6. b(i)-(iii) diagram 5 (1 each) + explanation 5 (shift, price, quantity 1 each + the reason 2); hidden solution diagrams. c(i) diagram 10, eight labels at 1 + €715 2 (hidden solution diagram); c(ii) 2 at 5 (2 + 3) from five.',
  'The laws of demand and supply and market equilibrium are The Market Economy (1-0); consumer and producer surplus and derived and joint demand are The Consumer (1-1); a rent control is Government Intervention (1-3).', also=['1-1'])
q('B2', [5], [13, 14, 15],
  [T('a/i', 17, 'sb-q2-a-i', '2-0'), T('a/ii', 18, 'sb-q2-a-ii', '2-0'),
   T('b/i', 8, 'sb-q2-b-i', '2-0'), T('b/ii', 12, 'sb-q2-b-ii', '2-0'),
   T('c/i', 10, 'sb-q2-c-i', '2-0'), T('c/ii', 10, 'sb-q2-c-ii', '2-0')],
  'Six tasks totalling 75. a(i) short-run diagram 9 at 1 + long-run diagram 8 (AC 2 at a tangent to AR 2, then P2, C2, Q2 and the equilibrium point 1 each); hidden solution diagrams. a(ii) three headings at 6. b(i) 8 (4 + 4) the answer and its explanation; b(ii) 12 (4 + 4 + 4) over the printed explanation (unpriced rows). c(i) 4 + 2 reasons at 3; c(ii) 4 + 6 graded.',
  'Perfect and imperfect competition are Market Structures (2-0).')
q('B3', [6], [16, 17, 18],
  [T('a/i', 5, 'sb-q3-a-i', '1-5'), T('a/ii', 5, 'sb-q3-a-ii', '1-5'), T('a/iii', 4, 'sb-q3-a-iii', '1-5'),
   T('a/iv', 16, 'sb-q3-a-iv', '1-5'), T('b/i', 10, 'sb-q3-b-i', '1-5'), T('b/ii', 10, 'sb-q3-b-ii', '1-5'),
   T('c/i', 15, 'sb-q3-c-i', '2-1'), T('c/ii', 10, 'sb-q3-c-ii', '2-1')],
  'Eight tasks totalling 75. a(i) 5; a(ii) 5; a(iii) 4; a(iv) points on AC 6, on MC 6, labels 4 at 1 (hidden solution graph). b(i) 10; b(ii) 2 at 5 (2 + 3) from four. c(i) diagram 5 + explanation 5 + one other point 5 from two; hidden solution diagram. c(ii) 2 at 5 (2 + 3) from three.',
  'Fixed, variable, average and marginal cost and the marginal efficiency of capital are Costs of Production, Revenue & Profit (1-5); the marginal revenue product of labour and public sector wages are The Labour Market (2-1).')
q('B4', [6], [19, 20, 21, 22],
  [T('a/i', 12, 'sb-q4-a-i', '3-0'), T('a/ii', 8, 'sb-q4-a-ii', '3-0'),
   T('b/i', 23, 'sb-q4-b-i', '3-0'), T('b/ii', 12, 'sb-q4-b-ii', '3-1'),
   T('c/i', 15, 'sb-q4-c-i', '3-0'), T('c/ii', 5, 'sb-q4-c-ii', '3-0')],
  'Six tasks totalling 75. a(i) 2 at 6 the income and expenditure methods; a(ii) 8 graded (unpriced rows). b(i) diagram 13 (5 sectors at 1, 8 flows at 1 for the two halves of each, component and direction) + explanation 10 (5 bullets at 2); hidden solution diagram. b(ii) 6 + 6, one cell each. c(i) 3 points at 5 (2 + 3) from five; c(ii) 1 at 5 (2 + 3) from three.',
  'National income, its measurement and the circular flow are National Income (3-0); Budget 2017 capital spending and the USC are also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q('B5', [7], [23, 24, 25, 26],
  [T('a/i', 12, 'sb-q5-a-i', '4-2'), T('a/ii', 18, 'sb-q5-a-ii', '4-2'),
   T('b/i', 10, 'sb-q5-b-i', '4-2'), T('b/ii', 15, 'sb-q5-b-ii', '4-2'),
   T('c/i', 5, 'sb-q5-c-i', '4-2'), T('c/ii', 5, 'sb-q5-c-ii', '4-2'), T('c/iii', 10, 'sb-q5-c-iii', '4-2')],
  'Seven tasks totalling 75. a(i) absolute advantage 4 + comparative advantage 8 graded; a(ii) 3 at 6 (3 + 3) from seven. b(i) 2 points at 5 (2 + 3) from six; b(ii) 3 at 5 (2 + 3) over the for and against columns, at least one of each: one menu. c(i) 5; c(ii) 5 97.9; c(iii) 2 at 5 (2 + 3) from four.',
  'Absolute and comparative advantage, protectionism and the terms of trade are International Trade & Competitiveness (4-2).')
q('B6', [7], [27, 28, 29, 30, 31],
  [T('a/i', 8, 'sb-q6-a-i', '3-3'), T('a/ii', 12, 'sb-q6-a-ii', '3-3'),
   T('b/i', 10, 'sb-q6-b-i', '3-3'), T('b/ii', 10, 'sb-q6-b-ii-good', '3-3'), T('b/ii', 10, 'sb-q6-b-ii-bad', '3-3'),
   T('b/iii', 10, 'sb-q6-b-iii', '3-3'), T('c/i', 15, 'sb-q6-c-i', '1-0'), T('c/ii', 10, 'sb-q6-c-ii', '1-0')],
  'Seven tasks, eight routes; 75 with the (b)(ii) stance counted once. a(i) 8 graded over six steps (unpriced rows); a(ii) 3 at 4 (2 + 2) from seven. b(i) 2 at 5; b(ii) 1 effect on households and 1 on firms at 5 (2 + 3): the scheme lists a good table and a bad table, so two stance routes, each two heading rows; b(iii) 2 points at 5 (2 + 3) from three. c(i) 3 at 5 (2 + 3) from eight; c(ii) 2 at 5 (2 + 3) from eight.',
  'The CPI, inflation and the ECB are Monetary Policy & Inflation (3-3); residential property prices are The Market Economy (1-0).')
q('B7', [8], [32, 33, 34, 35, 36],
  [T('a', 20, 'sb-q7-a', '3-1'), T('b/i', 5, 'sb-q7-b-i', '1-3'), T('b/ii', 25, 'sb-q7-b-ii', '1-3'),
   T('c', 25, 'sb-q7-c', '0-0')],
  'Four tasks totalling 75. a 4 at 5 the four terms. b(i) 5; b(ii) 4 at 5 (2 + 3) over the for and against lists, at least one of each, + 5 for any valid Irish example: one menu and one example menu. c any three of five economists, 2 contributions each, 1st correct response 5 (3 + 2) and every other 4 (2 + 2): one menu of the five economists’ printed contributions, each economist claimed with both of its contributions at 9 (5 + 4) first, then 8.',
  'The national debt, fiscal policy, the budget deficit and tax avoidance are Fiscal Policy & the Budget (3-1); privatisation is Government Intervention (1-3); economists’ contributions are Economics as a Way of Thinking (0-0).')
q('B8', [8], [37, 38, 39],
  [T('a/i', 10, 'sb-q8-a-i', '3-2'), T('a/ii', 5, 'sb-q8-a-ii', '3-2'), T('a/iii', 15, 'sb-q8-a-iii', '3-2'),
   T('b', 25, 'sb-q8-b', '3-5'), T('c', 20, 'sb-q8-c', '1-3')],
  'Five tasks totalling 75. a(i) 2 at 5; a(ii) 5 net migration -28,558; a(iii) 3 at 5 (2 + 3) over the push and pull columns. b 4 points, 7 (4 + 3) + 6 + 6 + 6: one menu claimed at 7, 6, 6, 6. c 4 points at 5 (2 + 3), at least one social and one economic: one menu.',
  'Natural increase, migration and emigration are Employment & Unemployment (3-2); the consequences of a growing population are Economic Growth (3-5); social housing is Government Intervention (1-3) and Fiscal Policy & the Budget (3-1).', also=['3-1'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (2, '2. Indicate by means of a tick (\uf0fc) which of the following statements is TRUE or FALSE.'): ('answer-classification', 'Section A Q2 four objective ticks; one card claimed at 6, 4, 3, 3.'),
 (4, '(b) Is Good A a substitute or a complement to Good B? Explain your answer.'): ('answer-classification', 'Section A Q7(b) the scheme’s answer is a complement (2) with its reason (3); one card.'),
 (5, '1. (a) In the case of any two of the following distinguish between the concepts.'): ('finite-route', 'Section B Q1(a) any two of three pairs: one card, the six definitions as one menu claimed at 7, 6, 6, 6.'),
 (7, '(ii) Discuss the economic arguments for and against a government introducing trade'): ('not-a-task-selection', 'Section B Q5(b)(ii) "for and against" names both sides of one discussion; one menu of both columns.'),
 (7, '(ii) The Irish inflation rate was at, or close to, 0% between 2013 and 2016.'): ('not-a-task-selection', 'Section B Q6(b)(ii) stimulus, read on "or"; not a selection.'),
 (7, 'Is such a low rate of inflation good or bad for (a) households and (b) firms?'): ('answer-classification', 'Section B Q6(b)(ii) good or bad is the answer; the scheme credits each with its own table, so two stance routes.'),
 (8, '(c) Outline the key contributions to economic thought by any three of the following economists:'): ('finite-route', 'Section B Q7(c) any three of five economists: one card, a menu of the five economists claimed three times at 9, 8, 8.'),
 (8, '(ii) State and explain the economic arguments for and against privatisation using any Irish'): ('not-a-task-selection', 'Section B Q7(b)(ii) "for and against" names both sides of one discussion; one menu, with any Irish example.'),
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
 'subjectId': 'economics', 'year': 2017, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 9)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 8 paper and 40 scheme pages (scheme pages 1-4 are the covers, the note on published schemes, the title page and the notes and index; page 40 is the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 61 printed asks (12 Section A + 49 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2017_hl.py). Printed choices are one card each: Section B Q1(a) any two of three pairs and Q7(c) any three of five economists. The stance route is Section B Q6(b)(ii), good or bad, each credited with its own table.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2017-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
