"""Write the independent 2019 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas
numbers it. Every tariff is the scheme's printed cell; its Summary of Mark
Allocations (scheme p5) agrees with every one. The Ordinary scheme reprints
each question above its answer, so the pairing confirms itself. There is no
2019 Ordinary Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2019/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2019/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2019-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [6], [T('all', 16, 'sa-q1', '4-1')],
  '8 @ 2 over the eight words of the three names (EU 2, ECB 3, WTO 3): one card, a row per abbreviation at 2 a word.',
  'The EU and the WTO are Globalisation (4-1); the ECB is Monetary Policy & Inflation (3-3).', also=['3-3'])
q(2, [2], [6], [T('i', 12, 'sa-q2-i', '2-0'), T('ii', 4, 'sa-q2-ii', '2-0')],
  'i 2 @ 6, the two labels (the scheme’s answer box prints 6 beside each); ii 2 @ 2, P1 and Q1 (hidden solution diagram).',
  'Long-run equilibrium in perfect competition is Market Structures (2-0).')
q(3, [2], [7], [T('all', 16, 'sa-q3', '0-1')],
  'One example for each of the four factors, priced 1 @ 8, 1 @ 4 and 2 @ 2 in the order they are credited: one card, the four factor rows claimed at 8, 4, 2, 2.',
  'The factors of production are Scarcity & Choice (0-1), as 2021-2023 OL file the same table.')
q(4, [3], [7], [T('all', 16, 'sa-q4', '0-0')],
  'Any three of four ideas, 1 @ 8 and 2 @ 4: one card, the four matches claimed at 8, 4, 4.',
  'Economists and their ideas are Economics as a Way of Thinking (0-0).')
q(5, [3], [7], [T('i', 9, 'sa-q5-i', '3-0'), T('ii', 7, 'sa-q5-ii', '3-0')],
  'i 9 (3 x 3) Gross National Product; ii 7 the percentage increase, 5% (the working is printed as a fraction; hidden crop).',
  'GNP and its growth rate are National Income (3-0).')
q(6, [3], [8], [T('all', 17, 'sa-q6', '3-0')],
  'Four items (Taxation, Investment Expenditure, Exports, Imports) placed as injections or leakages, 1 @ 8 and 3 @ 3: one card, the four placements claimed at 8, 3, 3, 3 (hidden completed table).',
  'Injections and leakages of the circular flow are National Income (3-0).')
q(7, [4], [8], [T('i', 8, 'sa-q7-i', '3-1'), T('ii', 9, 'sa-q7-ii', '3-1')],
  'i 8 (4 + 2 + 2) Universal Social Charge; ii 9 one benefit from four.',
  'The USC rate in the Budget is Fiscal Policy & the Budget (3-1).')
q(8, [4], [8], [T('a', 7, 'sa-q8-a', '0-1'), T('b', 10, 'sa-q8-b', '0-2')],
  'a 7 scarcity of resources (two accepted statements); b 2 @ 5 from four. The (i)/(ii) under (b) are ruled answer slots.',
  'Scarcity of resources is Scarcity & Choice (0-1); wasting resources is Sustainability (0-2).')
q(9, [4], [9], [T('all', 17, 'sa-q9', '1-5')],
  'One ladder across (a) and (b), 1 @ 5 and 3 @ 4 over the four elements (each cost’s definition and example), not tied to a part: one card for the question, the four elements claimed at 5, 4, 4, 4.',
  'Fixed and variable costs are Costs of Production, Revenue & Profit (1-5).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [10, 11, 12],
  [T('a/i', 20, 'sb-q1-a-i', '2-0'), T('a/ii', 10, 'sb-q1-a-ii', '2-0'), T('b/i', 9, 'sb-q1-b-i', '2-0'),
   T('b/ii-iii', 12, 'sb-q1-b-ii', '2-0'), T('c', 24, 'sb-q1-c', '2-0')],
  'Five cards for six asks, totalling 75. a(i) 5 @ 4 the five labels; a(ii) 5 + 5 P1 and Q1 (hidden solution diagram). b(i) 1 @ 9; b(ii) and (iii) share one 2 @ 6, a characteristic with its note, so one card covers both. c 2 @ 9 advantages from four and 1 @ 6 disadvantage from four.',
  'Imperfect competition and entry into the waste-collection market are Market Structures (2-0).')
q('B2', [6], [13, 14, 15],
  [T('a/i', 11, 'sb-q2-a-i', '1-0'), T('a/ii', 11, 'sb-q2-a-ii', '1-0'), T('a/iii', 8, 'sb-q2-a-iii', '1-0'),
   T('b/i', 8, 'sb-q2-b-i', '1-0'), T('b/ii', 8, 'sb-q2-b-ii', '1-0'), T('b/iii', 4, 'sb-q2-b-iii', '1-0'),
   T('c/i', 6, 'sb-q2-c-i', '1-3'), T('c/ii', 7, 'sb-q2-c-ii', '1-1'), T('c/iii', 12, 'sb-q2-c-iii', '1-3')],
  'Nine tasks totalling 75. a(i) 11 (5 @ 2) + 1 the demand curve and its D/C label; a(ii) 11 (5 @ 2) + 1 the supply curve and its S/C label; a(iii) 6 (3 + 3) P1 and Q1 + 1 + 1 the P and Q axis labels (the scheme’s summary and its graph notes agree; hidden solution graph). b 2 @ 10 (4 + 4 + 2), one column per situation: (i) which curve 4 + 4; (ii) which way 4 + 4; (iii) why 2 + 2. c(i) 6 (4 + 2) from four; c(ii) 7 (5 + 2); c(iii) 2 @ 6 (4 + 2) from six.',
  'Demand, supply and equilibrium are The Market Economy (1-0); the electric-vehicle grant and other measures are Government Intervention (1-3); its effect on demand is The Consumer (Demand) (1-1).')
q('B3', [7], [16, 17, 18],
  [T('a', 21, 'sb-q3-a', '2-1'), T('b/i', 6, 'sb-q3-b-i', '2-1'), T('b/ii', 12, 'sb-q3-b-ii', '2-1'),
   T('b/iii', 12, 'sb-q3-b-iii', '2-1'), T('c/i', 12, 'sb-q3-c-i', '2-1'), T('c/ii', 12, 'sb-q3-c-ii', '2-1')],
  'Six tasks totalling 75. a any three of four terms, 1 @ 11 and 2 @ 5. b(i) 6; b(ii) 2 @ 6 (3 + 3) from four; b(iii) 2 @ 6 (3 + 3) from eight. c(i) 2 @ 6 (4 + 2), one effect for firms and one for the economy, two heading rows; c(ii) 2 @ 6 (4 + 2) from six.',
  'Labour, its demand and supply, participation and skills shortages are The Labour Market (2-1).')
q('B4', [7], [19, 20, 21],
  [T('a', 21, 'sb-q4-a', '4-2'), T('b/i', 7, 'sb-q4-b-i', '4-2'), T('b/ii', 9, 'sb-q4-b-ii', '4-2'),
   T('b/iii', 14, 'sb-q4-b-iii', '4-2'), T('c/i', 6, 'sb-q4-c-i', '0-1'),
   T('c/ii', 6, 'sb-q4-c-ii-yes', '3-1'), T('c/ii', 6, 'sb-q4-c-ii-no', '3-1'), T('c/iii', 12, 'sb-q4-c-iii', '3-1')],
  'Eight routes; 75 with the (c)(ii) stance counted once. a any three of four terms, 1 @ 11 and 2 @ 5. b(i) 4 beside the answer (an invisible import) and 3 beside its reason; b(ii) 9; b(iii) 2 x 7 (4 + 3) from seven. c(i) 6; c(ii) 6, the scheme credits YES and NO with different content, so two stance routes; c(iii) 2 @ 6 (4 + 2) from six.',
  'Trade, the balance of trade and its terms are International Trade & Competitiveness (4-2); opportunity cost is Scarcity & Choice (0-1); the Rainy Day Fund and other uses of the €500m are Fiscal Policy & the Budget (3-1).')
q('B5', [8], [22, 23, 24],
  [T('a', 21, 'sb-q5-a', '3-4'), T('b', 24, 'sb-q5-b', '3-3'),
   T('c/i', 12, 'sb-q5-c-i', '1-5'), T('c/ii', 18, 'sb-q5-c-ii', '3-2')],
  'Four tasks totalling 75. a 3 @ 7 (4 + 3), one advantage for each of students, the university and banks: three heading rows. b 3 @ 8 (4 + 4), households, firms and the government: three heading rows. c(i) 2 @ 6 (3 + 3) the two printed reasons; c(ii) 3 @ 6 (3 + 3), customers, employees and the local community: three heading rows.',
  'Non-cash payment is Financial Sector (3-4); interest rates are Monetary Policy & Inflation (3-3); closing post offices to cut costs is Costs of Production, Revenue & Profit (1-5), and its effects on jobs and communities Employment & Unemployment (3-2).')
q('B6', [8], [25, 26, 27, 28],
  [T('a/i', 7, 'sb-q6-a-i', '3-1'), T('a/ii', 14, 'sb-q6-a-ii', '3-1'), T('b/i', 8, 'sb-q6-b-i', '3-1'),
   T('b/ii', 6, 'sb-q6-b-ii', '3-1'), T('b/iii', 16, 'sb-q6-b-iii', '3-1'), T('c', 24, 'sb-q6-c', '3-1')],
  'Six tasks totalling 75. a(i) 5 + 2 the definition and one example from two; a(ii) 2 @ 7 (3 + 4) from six. b(i) 8; b(ii) 3 the answer (indirect) + 3 its explanation; b(iii) 2 @ 8 (4 + 4) from six. c 4 @ 6 (3 + 3), an argument for and one against any two of three measures, each listed under its measure: one card with a for row and an against row, each claimed twice, every option named by its measure.',
  'Tax evasion, the role of taxation, VAT and Budget measures are Fiscal Policy & the Budget (3-1).')
q('B7', [9], [29, 30, 31, 32],
  [T('a/i', 9, 'sb-q7-a-i', '3-0'), T('a/ii', 5, 'sb-q7-a-ii', '3-0'), T('a/iii', 10, 'sb-q7-a-iii', '3-0'),
   T('b/i', 12, 'sb-q7-b-i', '4-1'), T('b/ii', 12, 'sb-q7-b-ii', '4-1'), T('b/iii', 6, 'sb-q7-b-iii', '4-1'),
   T('c/i', 10, 'sb-q7-c-i', '3-0'), T('c/ii', 8, 'sb-q7-c-ii', '3-0'), T('c/iii', 3, 'sb-q7-c-iii', '3-0')],
  'Nine tasks totalling 75. a(i) 9 (3 x 3) Central Statistics Office; a(ii) 5 one method from three; a(iii) 2 @ 5 (3 + 2) from four. b(i) 2 @ 6, the two terms; b(ii) 2 @ 6 (3 + 3) from four; b(iii) 1 @ 6 (3 + 3) from seven. c(i) 2 @ 5, MPS and MPM; c(ii) 8 the multiplier, 2 (printed as a fraction; hidden crop); c(iii) 3.',
  'National income and the multiplier are National Income (3-0); multinational companies are Globalisation (4-1).')
q('B8', [10], [33, 34, 35, 36],
  [T('a', 21, 'sb-q8-a', '3-2'), T('b/i', 6, 'sb-q8-b-i', '3-5'), T('b/ii', 16, 'sb-q8-b-ii', '3-5'),
   T('b/iii', 8, 'sb-q8-b-iii', '3-5'), T('c/i', 12, 'sb-q8-c-i', '3-5'), T('c/ii', 12, 'sb-q8-c-ii', '3-5')],
  'Six tasks totalling 75. a any three of four terms, 1 @ 11 and 2 @ 5. b(i) 6 (two accepted statements); b(ii) 2 @ 8 (5 + 3), one advantage for households and one for firms: two heading rows; b(iii) 8 (5 + 3) one example and reason from four. c(i) 2 @ 6 (4 + 2) from four; c(ii) 2 @ 6 (4 + 2) from six.',
  'Full employment and emigration are Employment & Unemployment (3-2); infrastructure, broadband and rural decline are Economic Growth (3-5).',
  also=['3-3'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 'There is no examination material on this page': ('not-a-task-selection', 'Blank back page.'),
}
PAGE_SEL = {
 (3, '4. Name the economist associated with any three of the following economic ideas/concepts'): ('finite-route', 'Section A Q4 any three of four ideas: one card, the four matches claimed at 8, 4, 4.'),
 (3, '6. The items listed below are examples of injections or leakages as they relate to the'): ('answer-classification', 'Section A Q6 each item is an injection or a leakage; one card, the four placements.'),
 (5, '(b) Free entry and exit is one of the characteristics of an imperfectly competitive market.'): ('not-a-task-selection', 'Section B Q1(b) stimulus, read on "one of"; not a selection.'),
 (6, '(b) The demand curve for sandwiches or the supply curve for sandwiches may shift to the'): ('answer-classification', 'Section B Q2(b) which curve shifts, and which way, is the answer (one column per situation).'),
 (6, '(i) State whether the demand curve or supply curve will shift.'): ('answer-classification', 'Section B Q2(b)(i) Supply Curve / Demand Curve, one per situation at 4.'),
 (6, '(ii) State whether the curve you mention will shift to the right or the left.'): ('answer-classification', 'Section B Q2(b)(ii) Left / Right, one per situation at 4.'),
 (6, 'right or the left due to the following:'): ('answer-classification', 'Section B Q2(b) stem continued: the shift direction is the answer.'),
 (7, '(i) Is this an example of an invisible import or an invisible export for the Irish economy?'): ('answer-classification', 'Section B Q4(b)(i) the scheme’s answer is an invisible import (4) with its reason (3); one card.'),
 (7, '3. (a) Explain any three of the following terms:'): ('finite-route', 'Section B Q3(a) any three of four terms: one card at 11, 5, 5.'),
 (7, '4. (a) Explain any three of the following terms:'): ('finite-route', 'Section B Q4(a) any three of four terms: one card at 11, 5, 5.'),
 (8, '(ii) Is VAT an example of a direct tax or an indirect tax? Explain your answer.'): ('answer-classification', 'Section B Q6(b)(ii) the scheme’s answer is indirect (3) with its explanation (3); one card.'),
 (8, 'any two of the following government measures announced in Budget 2019:'): ('finite-route', 'Section B Q6(c) any two of three measures: one card, a for row and an against row each claimed twice.'),
 (9, '(ii) Explain any one of the three methods used to calculate national income.'): ('finite-route', 'Section B Q7(a)(ii) any one of three methods: one card, a menu of the three.'),
 (10, '8. (a) Explain any three of the following terms:'): ('finite-route', 'Section B Q8(a) any three of four terms: one card at 11, 5, 5.'),
 (10, 'should invest in, and explain one reason for your choice.'): ('finite-route', 'Section B Q8(b)(iii) one example of four with its reason: one card.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

tasks = [t for x in Q for t in x['tasks']]
for x in Q:
    total = sum(t['marks'] for t in x['tasks'] if not t['cardId'].endswith('-no'))
    want = 75 if x['n'].startswith('B') else (16 if int(x['n']) <= 5 else 17)
    assert total == want, (x['n'], total, want)
draft = {
 'subjectId': 'economics', 'year': 2019, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (scheme pages 1-5 are the cover, notes, index and the Summary of Mark Allocations, which agrees with every tariff here; scheme pages 37-40 and paper pages 11-12 are blank). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 67 printed asks ({sum(len(x["tasks"]) for x in Q if not x["n"].startswith("B"))} Section A + {sum(len(x["tasks"]) for x in Q if x["n"].startswith("B"))} Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2019_ol.py). Choose-N rule checked: Section A Q4, Section B Q3(a), Q4(a), Q7(a)(ii), Q8(a), Q8(b)(iii) and Q6(c) are each one card; Q4(c)(ii) is two stance routes because the scheme credits YES and NO with different content.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2019-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
