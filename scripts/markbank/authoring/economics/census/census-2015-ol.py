"""Write the independent 2015 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2015 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2015/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2015/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2015-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: a printed choice the scheme credits with a list
# for each side (the first route of each set is the one counted).
ALT = ('-smith', '-malthus', '-ricardo')

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('i/ii/iii/iv', 16, 'sa-q1', '0-1')],
  'The four spaces (i)-(iv): the first correct response 8, the 2nd 4, the 3rd and 4th 2 each: one card.',
  'The factors of production and their examples are Scarcity & Choice (0-1).')
q(2, [2], [5], [T('i/ii/iii/iv', 16, 'sa-q2', '2-0')],
  'The four TRUE/FALSE answers: the first correct response 8, the 2nd 4, the 3rd and 4th 2 each: one card.',
  'The assumptions of perfect competition are Market Structures (2-0).')
q(3, [2], [5], [T('all', 16, 'sa-q3', '3-1')],
  '10 (5 + 5) the explanation + 6 one reason from seven.',
  'Corporation tax and its rate in the Budget are Fiscal Policy & the Budget (3-1); attracting FDI is also Globalisation (4-1).', also=['4-1'])
q(4, [3], [6], [T('all', 16, 'sa-q4', '4-2')],
  'The four words placed (Sale, Goods, Purchase, Services): the first 2 correct 6 each, the 3rd and 4th 2 each: one card.',
  'Visible exports and invisible imports are International Trade & Competitiveness (4-2).')
q(5, [3], [6], [T('a-b', 16, 'sa-q5', '4-0')],
  'One card for both asks: the scheme prices the two characteristics of (a) and the one way of (b) on one ladder, the first 2 correct responses 6 each and the 3rd 4.',
  'LDCs and how Ireland could support them are Growth & Development (4-0).')
q(6, [3], [7], [T('all', 17, 'sa-q6', '3-3')],
  'The three names: the first 2 correct 6 each (2 + 2 + 2), the 3rd 5 (2 + 2 + 1).',
  'The ECB and the CPI are Monetary Policy & Inflation (3-3); the WTO is Globalisation (4-1).', also=['4-1'])
q(7, [4], [7], [T('i', 10, 'sa-q7-i', '1-4'), T('ii', 7, 'sa-q7-ii', '1-4')],
  'i 10 (5 + 5); ii the two circled answers (rise, 28%) 4 + 3.',
  'Price elasticity of demand is Elasticity (1-4).')
q(8, [4], [7], [T('all', 17, 'sa-q8', '3-2')],
  '10 the explanation + 7 one other problem from three.',
  'Emigration and the brain drain are Employment & Unemployment (3-2).')
q(9, [4], [8], [T('a', 12, 'sa-q9-a', '1-1'), T('b', 5, 'sa-q9-b', '3-0')],
  'a 2 @ 6 from four; b 5 one cost from four.',
  'Online shopping’s benefits for consumers are The Consumer (1-1); its costs for the economy (domestic activity, tax revenue, imports as a leakage) are National Income (3-0), and imports International Trade & Competitiveness (4-2).', also=['4-2'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [9, 10, 11],
  [T('a/i', 25, 'sb-q1-a-i', '2-0'), T('a/ii', 5, 'sb-q1-a-ii', '2-0'), T('b/i', 4, 'sb-q1-b-i', '2-0'),
   T('b/ii-iii', 16, 'sb-q1-b-ii', '2-0'), T('c/i', 5, 'sb-q1-c-i', '2-0'), T('c/ii', 10, 'sb-q1-c-ii', '2-0'),
   T('c/iii', 10, 'sb-q1-c-iii', '2-0')],
  'Seven cards for eight asks, totalling 75. a(i) 5 @ 5 the five labels; a(ii) Q1 and P1, the 1st correct 3 and the 2nd 2 (hidden solution diagram). b(i) 4 the explanation (an example alone 2); b(ii) and (iii) share one 2 @ 8 (4 + 4), a characteristic with its note: one card covers both. c(i) 5; c(ii) and c(iii) each 2 @ 5 (3 + 2), one for the consumer and one for the seller: two heading rows.',
  'Imperfect competition, barriers to entry, brand loyalty and advertising are Market Structures (2-0).')
q('B2', [6], [12, 13, 14],
  [T('a/i-iii', 30, 'sb-q2-a', '1-0'), T('b/i', 10, 'sb-q2-b-i', '1-0'), T('b/ii', 6, 'sb-q2-b-ii', '1-0'),
   T('b/iii', 4, 'sb-q2-b-iii', '1-0'), T('c/i', 12, 'sb-q2-c-i', '1-3'), T('c/ii', 13, 'sb-q2-c-ii', '1-3')],
  'Six cards for eight asks, totalling 75. a(i)-(iii) share one graph priced D/C 10 (5 points at 2), S/C 10, the four labels P, Q, D/C and S/C at 1, and P1 and Q1 2 x 3: one card (hidden solution graph). b one column per development: (i) which curve 5 + 5; (ii) which way 3 + 3; (iii) why 2 + 2, with the scheme’s alternative answer accepted. c(i) 2 @ 6 (3 + 3) from three; c(ii) households 7 (4 + 3) + the government 6 (3 + 3): two heading rows.',
  'Demand, supply, equilibrium and their shifts are The Market Economy (1-0); water charges are Government Intervention (1-3), and as a charge on households also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q('B3', [7], [15, 16, 17, 18],
  [T('a/i', 6, 'sb-q3-a-i', '0-1'), T('a/ii', 16, 'sb-q3-a-ii', '1-5'), T('a/iii', 8, 'sb-q3-a-iii', '1-5'),
   T('b/i', 12, 'sb-q3-b-i', '2-1'), T('b/ii', 12, 'sb-q3-b-ii', '2-1'),
   T('c/i', 12, 'sb-q3-c-i', '0-1'), T('c/ii', 9, 'sb-q3-c-ii', '0-1')],
  'Seven tasks totalling 75. a(i) 6; a(ii) A, B, C and D each 4 (1 + 1 + 2); a(iii) the four costs at 1 + the two explanations at 2. b(i) labour 6 (4 + 2) + the national minimum wage 6: the scheme prints 7 beside the second but sets it as 4 + 2, and only 6 fits the paper’s (24); b(ii) 2 @ 6 (3 + 3) from three. c(i) 2 @ 6 (3 + 3) from four; c(ii) one action for each of the government and consumers, the 1st correct 6 (3 + 3) and the 2nd 3 (2 + 1).',
  'The entrepreneur and entrepreneurship are Scarcity & Choice (0-1); fixed, variable and total costs and profit are Costs of Production, Revenue & Profit (1-5); labour, the minimum wage and taking on workers are The Labour Market (2-1).')
q('B4', [7], [19, 20, 21],
  [T('a', 21, 'sb-q4-a', '3-4'), T('b/i', 8, 'sb-q4-b-i', '3-1'), T('b/ii', 6, 'sb-q4-b-ii', '3-4'),
   T('b/iii', 16, 'sb-q4-b-iii', '3-4'), T('c/i', 16, 'sb-q4-c-i', '3-4'),
   T('c/ii', 8, 'sb-q4-c-ii-marx', '0-0'), T('c/ii', 8, 'sb-q4-c-ii-smith', '0-0'),
   T('c/ii', 8, 'sb-q4-c-ii-malthus', '0-0'), T('c/ii', 8, 'sb-q4-c-ii-ricardo', '0-0')],
  'Six tasks totalling 75. a 2 @ 7 the two terms + 7 one other function from two. b(i) 8; b(ii) 6; b(iii) 2 @ 8 (4 + 4) from seven. c(i) any two of three motives @ 8; c(ii) 8, the name 2 + the statement 3 + the explanation 3: the scheme lists each economist’s own, so one route per economist, counted once.',
  'Money and savings are Financial Sector (3-4); DIRT is Fiscal Policy & the Budget (3-1), as 2018 OL files it; Keynes’s motives for holding money are Financial Sector (3-4); economists’ contributions are Economics as a Way of Thinking (0-0).')
q('B5', [8], [22, 23, 24],
  [T('a/i', 6, 'sb-q5-a-i', '4-2'), T('a/ii', 10, 'sb-q5-a-ii', '4-2'), T('a/iii', 10, 'sb-q5-a-iii', '4-2'),
   T('b/i', 5, 'sb-q5-b-i', '4-2'), T('b/ii', 6, 'sb-q5-b-ii', '4-2'), T('b/iii', 14, 'sb-q5-b-iii', '4-2'),
   T('c/i-iii', 24, 'sb-q5-c', '4-2')],
  'Seven cards for nine asks, totalling 75. a(i) 6 (3 + 3); a(ii) the working 6 (2 + 2 + 2) + the surplus and its reason 2 + 2; a(iii) 10, the raised marks beside each figure (1 + 1 + 2, 1 + 1 + 2) and the deficit 2. b(i) 5; b(ii) the answer 3 + the explanation 3; b(iii) 2 @ 7 (4 + 3) from six. c(i)-(iii) share one ladder, the 1st correct answer 12 (6 + 6) and the 2nd and 3rd 6 (3 + 3): one card covers the three.',
  'The balance of trade, embargoes, exports and the exchange rate are International Trade & Competitiveness (4-2); employment is also Employment & Unemployment (3-2).', also=['3-2'])
q('B6', [9], [25, 26, 27],
  [T('a/i', 5, 'sb-q6-a-i', '3-1'), T('a/ii', 10, 'sb-q6-a-ii', '3-1'), T('a/iii', 10, 'sb-q6-a-iii', '3-1'),
   T('b/i', 6, 'sb-q6-b-i', '3-1'), T('b/ii', 6, 'sb-q6-b-ii', '3-1'), T('b/iii', 12, 'sb-q6-b-iii', '3-1'),
   T('c/i', 6, 'sb-q6-c-i', '1-3'), T('c/ii', 10, 'sb-q6-c-ii', '1-3'), T('c/iii', 10, 'sb-q6-c-iii', '2-2')],
  'Nine tasks totalling 75. a(i) 5, the three marked figures at 1 and the answer 2; a(ii) 2 @ 5; a(iii) 2 @ 5, one each side from seven. b(i) 6; b(ii) the answer 3 + the explanation 3; b(iii) any two of three, each the statement 3 + the explanation 3. c(i) 6 (3 + 3) from five; c(ii) 2 @ 5 (3 + 2) from five; c(iii) 2 @ 5 (3 + 2) from four.',
  'The current budget, income tax and the USC are Fiscal Policy & the Budget (3-1); measures against smoking and their benefits for individuals are Government Intervention (1-3), and the benefits for society Market Failure (2-2), as a demerit good’s external costs.')
q('B7', [9], [28, 29, 30],
  [T('a/i', 6, 'sb-q7-a-i', '3-1'), T('a/ii', 14, 'sb-q7-a-ii', '3-1'), T('a/iii', 6, 'sb-q7-a-iii', '0-1'),
   T('b/i', 7, 'sb-q7-b-i', '3-5'), T('b/ii', 18, 'sb-q7-b-ii', '3-5'),
   T('c/i', 12, 'sb-q7-c-i', '4-1'), T('c/ii', 12, 'sb-q7-c-ii', '4-1')],
  'Seven tasks totalling 75. a(i) the answer 3 + the explanation 3; a(ii) 2 @ 7 (4 + 3) from six; a(iii) 6 (3 + 3) the opportunity cost with its example. b(i) 7; b(ii) 3 @ 6 (3 + 3), one each for citizens, businesses and the government’s finances: three heading rows. c(i) 2 @ 6 (3 + 3) from eight; c(ii) 2 @ 6 (3 + 3) from three.',
  'Capital spending on social housing is Fiscal Policy & the Budget (3-1), and social housing Government Intervention (1-3); opportunity cost is Scarcity & Choice (0-1); economic growth is Economic Growth (3-5); EU membership is Globalisation (4-1).', also=['1-3'])
q('B8', [10], [31, 32, 33],
  [T('a/i', 11, 'sb-q8-a-i', '3-0'), T('a/ii', 8, 'sb-q8-a-ii', '3-0'), T('a/iii', 6, 'sb-q8-a-iii', '4-2'),
   T('b/i', 5, 'sb-q8-b-i', '3-0'), T('b/ii', 15, 'sb-q8-b-ii', '3-0'), T('b/iii', 10, 'sb-q8-b-iii', '3-0'),
   T('c/i', 12, 'sb-q8-c-i', '3-0'), T('c/ii', 8, 'sb-q8-c-ii', '3-0')],
  'Eight tasks totalling 75. a(i) line 1 4 (2 + 2), line 2 3, line 3 4 (2 + 2); a(ii) 2 @ 4 (2 + 2), households and firms; a(iii) the answer 3 + the explanation 3. b(i) 5 (the scheme prints 4 + 1 under its one sentence); b(ii) 3 @ 5 the three letters; b(iii) 2 @ 5 (3 + 2) from four. c(i) 6 (3 + 3) for each of MPM and MPS; c(ii) 8, the four starred figures at 2.',
  'The circular flow, national income, its formula, consumer spending and the multiplier are National Income (3-0); an open economy is International Trade & Competitiveness (4-2).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 12': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 13)},
}
PAGE_SEL = {
 (2, '(Write True or False after each sentence.)'): ('answer-classification', 'Section A Q2 TRUE or FALSE is the answer for each sentence; one card, four answers.'),
 (2, '1. Insert the factor of production or an appropriate example of the factor of production into the four spaces'): ('not-a-task-selection', 'Section A Q1 a factor or an example is what each printed space asks for; one card, four spaces.'),
 (2, 'SENTENCE TRUE or FALSE'): ('answer-classification', 'Section A Q2 table header; the TRUE or FALSE answers are the four tasks of one card.'),
 (3, '(b) Outline one way Ireland (the Irish Government or Irish citizens) could support LDCs.'): ('not-a-task-selection', 'Section A Q5(b) either may act; one menu, not a selection.'),
 (3, '4. Choose the correct words from the list below to complete the following two statements:'): ('answer-classification', 'Section A Q4 the four words placed are the answer; one card.'),
 (5, '(b) There are no barriers to entry in Imperfect Competition.'): ('not-a-task-selection', 'Section B Q1(b) stimulus, read on "no"; not a selection.'),
 (6, '(b) The demand curve for Smartphones OR the supply curve for Smartphones may shift to the right'): ('answer-classification', 'Section B Q2(b) demand or supply, right or left is the answer for each development; one card a question, a row a development.'),
 (6, '(i) State whether the demand curve or the supply curve will shift'): ('answer-classification', 'Section B Q2(b)(i) demand or supply is the answer for each development; one card, two rows.'),
 (6, '(ii) State whether the curve you mention will shift to the right or the left'): ('answer-classification', 'Section B Q2(b)(ii) right or left is the answer for each development; one card, two rows.'),
 (6, 'or to the left due to the following:'): ('answer-classification', 'Section B Q2(b) stem, read on "or"; the direction is the answer.'),
 (7, '(ii) Name one other economist who contributed to economic thought and outline one of this'): ('finite-route', 'Section B Q4(c)(ii) any one economist: the scheme lists each economist’s own contribution, so one route per economist, counted once.'),
 (7, 'Explain any two of the above motives.'): ('finite-route', 'Section B Q4(c)(i) any two of three motives: one card claimed twice at 8.'),
 (8, '(ii) Is the export of beef from Ireland a visible export or an invisible export?'): ('answer-classification', 'Section B Q5(b)(ii) visible or invisible is the answer (visible); one card.'),
 (8, 'Trade and state if it is a surplus or deficit. (Show your workings.)'): ('answer-classification', 'Section B Q5(a)(iii) surplus or deficit is the answer (a deficit); one card.'),
 (8, 'Visible Exports Visible Imports Balance of Trade Surplus or Deficit'): ('not-a-task-selection', 'Section B Q5(a) table header, read on "or"; not a selection.'),
 (9, '(i) Does this spending on social housing represent current expenditure or capital expenditure by'): ('answer-classification', 'Section B Q7(a)(i) current or capital is the answer (capital); one card.'),
 (9, '(ii) Is income tax a direct or indirect tax? Explain your answer.'): ('answer-classification', 'Section B Q6(b)(ii) direct or indirect is the answer (direct); one card.'),
 (9, 'on any two of the following:'): ('finite-route', 'Section B Q6(b)(iii) any two of three: one card claimed twice at 6.'),
 (10, '8. (a) The diagram below represents the Circular Flow of Income in an economy without government or'): ('not-a-task-selection', 'Section B Q8(a) stimulus, read on "or"; not a selection.'),
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
 'subjectId': 'economics', 'year': 2015, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 36 scheme pages (paper pages 11-12 are blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index, and pages 34-36 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 80 printed asks (18 Section A + 62 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2015_ol.py). Four cards cover more than one printed ask because the scheme prices them together: Section A Q5(a)-(b), Section B Q1(b)(ii)-(iii), Q2(a)(i)-(iii) and Q5(c)(i)-(iii). Section B Q4(c)(ii) is one route per economist. Section B Q3(b)(i) prices the national minimum wage 6: the scheme prints 7 beside it but sets it as 4 + 2, and only 6 fits the paper’s (24).',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2015-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
