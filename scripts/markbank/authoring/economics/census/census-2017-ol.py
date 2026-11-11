"""Write the independent 2017 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2017 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2017/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2017/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2017-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: a printed choice the scheme credits with a list
# for each side (the first route of each set is the one counted).
ALT = ('-no',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '3-1')],
  '4 x 4 the four matches (A 5, B 4, C 1, D 2): one card, a row per tax.',
  'VAT, DIRT, PAYE and customs duty are taxes: Fiscal Policy & the Budget (3-1).')
q(2, [2], [5], [T('i', 10, 'sa-q2-i', '1-5'), T('ii', 6, 'sa-q2-ii', '1-5')],
  'i 3 + 3 + 4 the quantity axis, the costs axis and the fixed-cost line at €3,000 (hidden solution graph); ii 6 the explanation and an example, printed as one 6: questionTotal, unpriced rows.',
  'Fixed costs are Costs of Production, Revenue & Profit (1-5).')
q(3, [3], [6], [T('all', 16, 'sa-q3', '4-2')],
  '2 x 8 one effect on retailers from three and one on the government’s finances from four: two heading rows.',
  'Cross-border shopping is International Trade & Competitiveness (4-2); its effect on the government’s finances (VAT, excise duty, social welfare) is Fiscal Policy & the Budget (3-1).', also=['3-1'])
q(4, [3], [6], [T('all', 16, 'sa-q4', '4-2')],
  '4 x 4 the four ticks, a row each.',
  'Visible and invisible exports and imports are International Trade & Competitiveness (4-2).')
q(5, [3], [6], [T('all', 16, 'sa-q5', '4-1')],
  '5 + 6 + 5 the three names (IMF 5, ECB 6, WTO 5), a row each.',
  'The IMF and the WTO are Globalisation (4-1); the ECB is Monetary Policy & Inflation (3-3).', also=['3-3'])
q(6, [3], [7], [T('all', 17, 'sa-q6', '0-1')],
  '7 opportunity cost and 2 x 5 two advantages from five: one card, a row for the term and a two-claim row.',
  'Opportunity cost is Scarcity & Choice (0-1); spending on third-level education is Fiscal Policy & the Budget (3-1), and its advantages (a better educated workforce, productivity, FDI) are also Economic Growth (3-5).', also=['3-1', '3-5'])
q(7, [4], [7], [T('i', 7, 'sa-q7-i', '1-1'), T('ii', 10, 'sa-q7-ii', '1-1')],
  'i 7 the new demand curve D1 drawn and labelled (hidden solution diagram); ii 2 x 5 two reasons from five.',
  'A shift in the demand for new cars is The Consumer (1-1).')
q(8, [4], [8], [T('all', 17, 'sa-q8', '1-3')],
  '10 + 7 one advantage from six and one disadvantage from four, priced on one ladder by order: the first correct response 10, the second 7.',
  'New taxes on disposable packaging are Government Intervention (1-3), as taxes also Fiscal Policy & the Budget (3-1), and as a measure against waste Sustainability (0-2).', also=['3-1', '0-2'])
q(9, [4], [8], [T('i', 12, 'sa-q9-i', '2-0'), T('ii', 5, 'sa-q9-ii', '2-0')],
  'i 4 + 4 + 4 the three labels; ii 5 No, with the reason (AR = AC).',
  'Long-run equilibrium in perfect competition is Market Structures (2-0).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [9, 10, 11],
  [T('a/i', 24, 'sb-q1-a-i', '2-0'), T('a/ii', 6, 'sb-q1-a-ii', '2-0'), T('b/i-ii', 21, 'sb-q1-b', '2-0'),
   T('c/i', 8, 'sb-q1-c-i', '1-3'), T('c/ii', 16, 'sb-q1-c-ii', '1-3')],
  'Five cards for six asks, totalling 75. a(i) 6 @ 4 the six labels; a(ii) 6 for P1 and C1 together (hidden solution diagram): questionTotal, unpriced rows. b(i) and (ii) share one 3 x 7, a barrier with its note, so one card covers both: three from six. c(i) 1 x 8 from four; c(ii) 2 x 8 from four.',
  'Monopoly and barriers to entry are Market Structures (2-0); state companies and their losses are Government Intervention (1-3).')
q('B2', [6], [12, 13, 14],
  [T('a/i', 10, 'sb-q2-a-i', '0-1'), T('a/ii', 10, 'sb-q2-a-ii', '1-1'), T('b/i-iii', 30, 'sb-q2-b', '1-0'),
   T('c/i', 12, 'sb-q2-c-i', '1-4'), T('c/ii', 13, 'sb-q2-c-ii', '1-4')],
  'Five cards for seven asks, totalling 75. a(i) 2 x 5 any two of three characteristics; a(ii) 2 x 5 any two of three terms. b(i)-(iii) share one graph priced D 10 (5 points at 2), S 10 (5 points at 2), the four labels P, Q, D/C and S/C 4 on one line, and P1 and Q1 2 x 3: the labels line spans (i) and (ii) and the scheme prints no Summary of Mark Allocations to split it, so one card covers the three (hidden solution graph). c(i) 6 x 2 the six symbols; c(ii) 5 the answer + 8 the reason.',
  'Economic goods and their characteristics are Scarcity & Choice (0-1); normal, substitute and complementary goods are The Consumer (1-1); market demand, supply and equilibrium are The Market Economy (1-0); income elasticity of demand is Elasticity (1-4).')
q('B3', [7], [15, 16, 17],
  [T('a', 20, 'sb-q3-a', '0-1'), T('b/i', 14, 'sb-q3-b-i', '2-1'), T('b/ii', 8, 'sb-q3-b-ii', '2-1'),
   T('b/iii', 8, 'sb-q3-b-iii', '2-1'), T('c/i', 12, 'sb-q3-c-i', '2-1'), T('c/ii', 13, 'sb-q3-c-ii', '3-2')],
  'Six tasks totalling 75. a 4 x 5 the four factors. b(i) 2 x 7 (4 + 3) public and private sector with an example of each; b(ii) 1 x 8 (4 + 4) from five; b(iii) 1 x 8 (4 + 4) from six. c(i) 2 x 6 (3 + 3) from seven; c(ii) 7 (4 + 3) + 6 (3 + 3) by order, two measures from five.',
  'The factors of production are Scarcity & Choice (0-1); public and private sector pay and wage differentials are The Labour Market (2-1); a wage increase’s inflation is also Monetary Policy & Inflation (3-3); emigrants returning are Employment & Unemployment (3-2).', also=['3-3'])
q('B4', [7], [18, 19, 20],
  [T('a/i', 10, 'sb-q4-a-i', '3-4'), T('a/ii', 5, 'sb-q4-a-ii', '3-4'), T('a/iii', 10, 'sb-q4-a-iii', '3-4'),
   T('b/i', 12, 'sb-q4-b-i', '3-4'), T('b/ii', 14, 'sb-q4-b-ii', '3-4'),
   T('c/i', 8, 'sb-q4-c-i', '3-3'), T('c/ii', 16, 'sb-q4-c-ii', '3-3')],
  'Seven tasks totalling 75. a(i) 2 x 5 money and barter; a(ii) 1 x 5 from three; a(iii) 2 x 5 from four. b(i) 2 x 6 interest rate and savings; b(ii) 2 x 7 (4 + 3) from seven. c(i) 8; c(ii) 2 x 8 (4 + 4) any two of three developments, each with its statement and explanation.',
  'Money, barter, interest rates and savings are Financial Sector (3-4); price inflation is Monetary Policy & Inflation (3-3).')
q('B5', [8], [21, 22, 23],
  [T('a/i', 5, 'sb-q5-a-i', '3-0'), T('a/ii', 10, 'sb-q5-a-ii', '3-0'), T('a/iii', 6, 'sb-q5-a-iii', '3-0'),
   T('b/i', 5, 'sb-q5-b-i', '4-2'), T('b/ii', 15, 'sb-q5-b-ii', '3-0'), T('b/iii', 10, 'sb-q5-b-iii', '3-0'),
   T('c/i', 8, 'sb-q5-c-i', '3-5'), T('c/ii', 16, 'sb-q5-c-ii', '3-5')],
  'Eight tasks totalling 75. a(i) 5; a(ii) 10 (2 + 3 + 3 + 2, printed beside the 1, the 0.15, the 0.25 and the 2.5); a(iii) 6 (2 + 2 + 2, beside the €10 million, the 2.5 and the €25 million). b(i) 5; b(ii) 3 x 5 the three lines; b(iii) 2 x 5 any two of three pairs. c(i) 8; c(ii) 2 x 8 (4 + 4) from six.',
  'The multiplier and the circular flow of income are National Income (3-0); an open economy is International Trade & Competitiveness (4-2); economic growth is Economic Growth (3-5).')
q('B6', [9], [24, 25, 26, 27],
  [T('a/i', 5, 'sb-q6-a-i', '3-1'), T('a/ii', 10, 'sb-q6-a-ii', '3-1'), T('a/iii', 10, 'sb-q6-a-iii', '3-1'),
   T('b', 24, 'sb-q6-b', '3-1'), T('c/i', 16, 'sb-q6-c-i', '3-1'),
   T('c/ii', 10, 'sb-q6-c-ii-yes', '3-1'), T('c/ii', 10, 'sb-q6-c-ii-no', '3-1')],
  'Six tasks totalling 75. a(i) 5 (1 + 1 + 1 + 2, printed beside the two figures, the minus sign and the €2,697m); a(ii) 2 x 5 one example each side from seven; a(iii) 2 x 5 (3 + 2) the two effects. b 4 x 6, one argument for and one against any two of three measures: one card, a two-claim row a side. c(i) 2 x 8 (4 + 4) from four; c(ii) 2 x 5 (3 + 2): YES and NO each with its own list, so one route per side, counted once.',
  'The current budget, its income and spending, Budget 2017 measures and taxation rates are Fiscal Policy & the Budget (3-1); falling unemployment is Employment & Unemployment (3-2).', also=['3-2'])
q('B7', [9], [28, 29, 30],
  [T('a/i', 9, 'sb-q7-a-i', '4-2'), T('a/ii', 8, 'sb-q7-a-ii', '4-2'), T('a/iii', 8, 'sb-q7-a-iii', '4-2'),
   T('b/i', 8, 'sb-q7-b-i', '3-1'), T('b/ii', 16, 'sb-q7-b-ii', '4-1'),
   T('c/i', 6, 'sb-q7-c-i', '4-1'), T('c/ii', 20, 'sb-q7-c-ii', '4-2')],
  'Seven tasks totalling 75. a(i) 9; a(ii) 8 the balance and deficit, printed as one 8: questionTotal, unpriced rows; a(iii) 8 (1 + 1 + 1, 1 + 1 + 1 and 2, printed beside each figure and the surplus). b(i) 8; b(ii) 2 x 8 (4 + 4) from nine. c(i) 6; c(ii) 2 x 10 (4 + 6) any two of three areas.',
  'The balance of trade and Brexit are International Trade & Competitiveness (4-2); corporation tax is Fiscal Policy & the Budget (3-1); where a multinational locates and the EU are Globalisation (4-1).')
q('B8', [10], [31, 32, 33],
  [T('a/i', 9, 'sb-q8-a-i', '3-0'), T('a/ii', 5, 'sb-q8-a-ii', '3-5'), T('a/iii', 16, 'sb-q8-a-iii', '3-5'),
   T('b', 20, 'sb-q8-b', '1-3'), T('c/i', 9, 'sb-q8-c-i', '1-3'), T('c/ii', 16, 'sb-q8-c-ii', '3-5')],
  'Six tasks totalling 75. a(i) 9; a(ii) 5; a(iii) 2 x 8 (4 + 4) any two of three areas. b 2 x 10 (5 + 5) from seven. c(i) 9; c(ii) 2 x 8 (4 + 4) from four.',
  'The CSO is National Income (3-0), as 2018 OL files it; the census and a growing population are Economic Growth (3-5), as are its effect on the labour market (The Labour Market, 2-1) and state services (Fiscal Policy & the Budget, 3-1); obesity measures and privatisation are Government Intervention (1-3); rural broadband’s advantages are Economic Growth (3-5).', also=['2-1', '3-1'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 10': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 11)},
}
PAGE_SEL = {
 (2, '(One explanation has no match.)'): ('not-a-task-selection', 'Section A Q1 instruction, read on "One"; one card, four matches.'),
 (3, '4. Indicate by means of a tick () the category to which each good or service belongs:'): ('answer-classification', 'Section A Q4 each item’s category is the answer; one card, four ticks.'),
 (4, '(ii) Is the firm earning supernormal profit? Yes / No.'): ('answer-classification', 'Section A Q9(ii) yes or no is the answer (No, as AR = AC); one card.'),
 (4, 'Circle your choice and explain your answer.'): ('answer-classification', 'Section A Q9(ii) the circled answer and its reason; one card.'),
 (6, '(i) Explain any two of the underlined terms, with reference to the Apple iPhone 7.'): ('finite-route', 'Section B Q2(a)(i) any two of three characteristics: one card claimed twice at 5.'),
 (6, '(ii) Explain any two of the following economic terms:'): ('finite-route', 'Section B Q2(a)(ii) any two of three terms: one card claimed twice at 5.'),
 (7, '(ii) State one economic effect which any two of the following developments may have on the'): ('finite-route', 'Section B Q4(c)(ii) any two of three developments: one card claimed twice at 8.'),
 (7, 'deciding whether to save or not. (26 marks)'): ('not-a-task-selection', 'Section B Q4(b)(ii) ask wording, read on "or"; not a selection.'),
 (8, '(c) One of the aims of government is to achieve economic growth.'): ('not-a-task-selection', 'Section B Q5(c) stimulus, read on "One"; not a selection.'),
 (8, 'any two of the following:'): ('finite-route', 'Section B Q5(b)(iii) any two of three pairs: one card claimed twice at 5.'),
 (9, '(b) Outline one economic argument in favour of and one economic argument against any two of'): ('finite-route', 'Section B Q6(b) any two of three Budget 2017 measures, one argument for and one against each: one card, two claims a side at 6.'),
 (9, '(ii) Using the above data, calculate the Balance of Trade and state if it is a surplus or deficit.'): ('answer-classification', 'Section B Q7(a)(ii) surplus or deficit is the answer (a deficit); one card.'),
 (9, 'Trade and state if it is a surplus or deficit. Show your workings. (25 marks)'): ('answer-classification', 'Section B Q7(a)(iii) surplus or deficit is the answer (a surplus); one card.'),
 (9, 'any two of the following:'): ('finite-route', 'Section B Q7(c)(ii) any two of three areas: one card claimed twice at 10.'),
 (10, 'may have on any two of the following:'): ('finite-route', 'Section B Q8(a)(iii) any two of three areas: one card claimed twice at 8.'),
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
 'subjectId': 'economics', 'year': 2017, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 36 scheme pages (scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index; scheme pages 34-35 are blank and 36 the back cover, as paper pages 11-12 are blank; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 65 printed asks (12 Section A + 53 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2017_ol.py). Two cards cover more than one printed ask because the scheme prices them together: Section B Q1(b)(i)-(ii), a barrier with its note at 7, and Q2(b)(i)-(iii), one graph whose labels line spans the parts. The stance route is Section B Q6(c)(ii), YES or NO, each credited with its own list.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2017-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
