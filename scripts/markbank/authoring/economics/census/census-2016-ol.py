"""Write the independent 2016 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2016 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2016/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2016/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2016-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: a printed choice the scheme credits with a list
# for each side (the first route of each set is the one counted).
ALT = ('-against',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '0-1')],
  '8 + 4 + 4 the three blanks (NATURE, GOODS, RENT), the first correct response 8: one card.',
  'Land as a factor of production and its return are Scarcity & Choice (0-1).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '4-2')],
  '8 + 4 + 2 + 2 the four ticks, the first correct response 8: one card.',
  'Tariffs, quotas, embargoes and subsidies are International Trade & Competitiveness (4-2).')
q(3, [2], [6], [T('a', 12, 'sa-q3-a', '1-1'), T('b', 4, 'sa-q3-b', '1-1')],
  'a 4 + 4 + 4 the three blank figures; b 4 the explanation.',
  'Total and marginal utility are The Consumer (1-1).')
q(4, [3], [6], [T('a', 10, 'sa-q4-a', '1-5'), T('b', 3, 'sa-q4-b', '1-5'), T('c', 3, 'sa-q4-c', '1-5')],
  'a 5 x 2 the four costs and their total; b 3 x 1 the sales, the cost and the profit; c 3 x 1 the cost, the output and the average cost.',
  'Total cost, profit and average cost are Costs of Production, Revenue & Profit (1-5).')
q(5, [3], [7], [T('all', 16, 'sa-q5', '0-0')],
  '8 + 4 + 2 + 2 the four matches (A 3, B 4, C 2, D 1), the first correct response 8: one card.',
  'Economists and their ideas are Economics as a Way of Thinking (0-0).')
q(6, [3], [7, 8], [T('a-b', 17, 'sa-q6', '3-1')],
  'One card for both asks: the scheme prices the reason of (a) and the measure of (b) on one ladder, 10 for the first correct response and 7 for the second, so neither part has a price of its own.',
  'Homelessness and measures against it are Fiscal Policy & the Budget (3-1), as 2018 OL files them, and as intervention in the housing market Government Intervention (1-3).', also=['1-3'])
q(7, [4], [8], [T('a', 10, 'sa-q7-a', '2-0'), T('b', 7, 'sa-q7-b', '1-3')],
  'a 10 the explanation; b 7 one reason from four.',
  'Branding is product differentiation, Market Structures (2-0); plain packaging is Government Intervention (1-3).')
q(8, [4], [8], [T('a', 5, 'sa-q8-a', '3-0'), T('b', 12, 'sa-q8-b', '3-0')],
  'a 5 the explanation; b 8 + 4 one effect on the government and one on businesses, the first correct response 8.',
  'The black economy is National Income (3-0), as the shadow economy is filed; its effect on tax revenue is also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q(9, [4], [9], [T('all', 17, 'sa-q9', '1-4')],
  '8 + 3 + 3 + 3 the four symbols the paper leaves blank (the paper prints Y1 and Q2), the first correct response 8.',
  'Income elasticity of demand is Elasticity (1-4).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [10, 11, 12],
  [T('a/i', 24, 'sb-q1-a-i', '2-0'), T('a/ii', 6, 'sb-q1-a-ii', '2-0'), T('b/i', 4, 'sb-q1-b-i', '2-0'),
   T('b/ii-iii', 16, 'sb-q1-b-ii', '2-0'), T('c/i', 5, 'sb-q1-c-i', '1-3'), T('c/ii', 10, 'sb-q1-c-ii', '1-3'),
   T('c/iii', 10, 'sb-q1-c-iii', '1-3')],
  'Seven cards for eight asks, totalling 75. a(i) 6 @ 4 the six labels; a(ii) 3 + 3 P1 and Q1 (hidden solution diagram). b(i) 4; b(ii) and (iii) share one 2 x 8 (state 4 + explain 4), a characteristic with its note, under the scheme’s "(ii) & (iii)" head: one card covers both. c(i) 5 (2 + 3) from four; c(ii) 2 x 5 (2 + 3) from nine; c(iii) 2 x 5 (2 + 3) from seven.',
  'Perfect competition is Market Structures (2-0); the alcohol advertising ban and other measures are Government Intervention (1-3).')
q('B2', [6], [13, 14, 15],
  [T('a/i', 6, 'sb-q2-a-i', '1-0'), T('a/ii', 4, 'sb-q2-a-ii', '1-0'), T('a/iii', 10, 'sb-q2-a-iii', '0-2'),
   T('a/iv', 5, 'sb-q2-a-iv', '1-3'), T('b/i', 8, 'sb-q2-b-i', '1-0'), T('b/ii', 6, 'sb-q2-b-ii', '1-0'),
   T('b/iii', 6, 'sb-q2-b-iii', '1-0'), T('c/i', 10, 'sb-q2-c-i', '3-4'), T('c/ii', 10, 'sb-q2-c-ii', '3-4'),
   T('c/iii', 10, 'sb-q2-c-iii', '3-4')],
  'Ten tasks totalling 75. a(i) 3 x 2 the three lines; a(ii) 2 + 2 P1 and Q1 (the scheme’s item table prices each; hidden solution diagram); a(iii) 2 x 5 (2 + 3) from four; a(iv) 5 (2 + 3) from seven. b one column per factor: (i) which curve 4 + 4; (ii) which way 3 + 3; (iii) why 3 + 3. c(i) 2 x 5 (2 + 3) from six; c(ii) 2 x 5 from seven; c(iii) 2 x 5 from five.',
  'Demand, supply and their shifts are The Market Economy (1-0); the advantages of electric cars are Sustainability (0-2), the measures to encourage them Government Intervention (1-3); commercial and electronic banking are Financial Sector (3-4).')
q('B3', [7], [16, 17, 18],
  [T('a/i', 12, 'sb-q3-a-i', '0-1'), T('a/ii', 12, 'sb-q3-a-ii', '0-1'),
   T('b/i', 7, 'sb-q3-b-i', '2-1'), T('b/ii', 10, 'sb-q3-b-ii', '2-1'), T('b/iii', 10, 'sb-q3-b-iii', '2-1'),
   T('c/i', 12, 'sb-q3-c-i', '4-2'), T('c/ii', 12, 'sb-q3-c-ii', '4-2')],
  'Seven tasks totalling 75. a(i) 3 + 3 each for labour and capital; a(ii) 2 x 6 (3 + 3) from five. b(i) 7 (4 + 3); b(ii) 2 x 5 (2 + 3) from five; b(iii) 2 x 5 (2 + 3) from six. c(i) 2 x 6 (3 + 3) from four; c(ii) 2 x 6 (3 + 3) from five.',
  'The factors of production and the entrepreneur are Scarcity & Choice (0-1); the national minimum wage is The Labour Market (2-1); international conferences and their visitors are International Trade & Competitiveness (4-2), as tourist numbers are filed.')
q('B4', [7], [19, 20, 21],
  [T('a/i', 5, 'sb-q4-a-i', '3-0'), T('a/ii', 5, 'sb-q4-a-ii', '3-5'), T('a/iii', 5, 'sb-q4-a-iii', '3-5'),
   T('a/iv', 10, 'sb-q4-a-iv', '3-5'), T('b/i', 5, 'sb-q4-b-i', '1-0'), T('b/ii', 10, 'sb-q4-b-ii', '3-5'),
   T('b/iii', 10, 'sb-q4-b-iii', '1-0'), T('c/i', 5, 'sb-q4-c-i', '4-0'), T('c/ii', 10, 'sb-q4-c-ii', '4-0'),
   T('c/iii', 10, 'sb-q4-c-iii', '4-0')],
  'Ten tasks totalling 75. a(i) 5; a(ii) 5; a(iii) 5 one item from four; a(iv) 2 x 5 (3 + 2), one use for businesses from three and one for the government from five: two heading rows. b(i) 5; b(ii) 2 x 5 (3 + 2) from five; b(iii) 2 x 5 (3 + 2) from four. c(i) 5 (3 + 2); c(ii) 2 x 5 (3 + 2) from nine; c(iii) 2 x 5 (3 + 2) from five.',
  'The CSO is National Income (3-0), as 2017 and 2018 OL file it; the census, its uses and a changing population are Economic Growth (3-5), and the census data’s uses also Economics as a Way of Thinking (0-0); a centrally planned economy is The Market Economy (1-0); LDCs and their difficulties are Growth & Development (4-0).', also=['0-0'])
q('B5', [8], [22, 23, 24, 25],
  [T('a/i', 10, 'sb-q5-a-i', '3-1'), T('a/ii', 10, 'sb-q5-a-ii', '3-1'),
   T('a/iii', 10, 'sb-q5-a-iii-for', '1-3'), T('a/iii', 10, 'sb-q5-a-iii-against', '1-3'),
   T('b/i', 5, 'sb-q5-b-i', '3-1'), T('b/ii', 15, 'sb-q5-b-ii', '3-1'),
   T('c/i', 6, 'sb-q5-c-i', '3-2'), T('c/ii', 14, 'sb-q5-c-ii', '3-2'), T('c/iii', 5, 'sb-q5-c-iii', '3-2')],
  'Eight tasks totalling 75. a(i) direct and indirect taxes, each 3 the explanation + 2 an example; a(ii) 2 x 5 (2 + 3) from eight; a(iii) 2 x 5 (2 + 3) for OR against: the scheme credits each side with its own list, so one route per side, counted once. b(i) 5; b(ii) 3 x 5 (state 2 + explain 3), one effect each for employees, imports and employment: three heading rows. c(i) 6; c(ii) 2 x 7 (4 + 3) from seven; c(iii) 5 (3 + 2) from six.',
  'Direct and indirect taxes, the uses of tax revenue and the USC are Fiscal Policy & the Budget (3-1); a sugar tax is Government Intervention (1-3); unemployment and youth unemployment are Employment & Unemployment (3-2).')
q('B6', [8], [26, 27, 28, 29],
  [T('a/i', 10, 'sb-q6-a-i', '4-2'), T('a/ii', 10, 'sb-q6-a-ii', '4-2'),
   T('b/i', 10, 'sb-q6-b-i', '4-2'), T('b/ii', 10, 'sb-q6-b-ii', '4-2'), T('b/iii', 5, 'sb-q6-b-iii', '4-2'),
   T('c/i', 6, 'sb-q6-c-i', '4-1'), T('c/ii', 6, 'sb-q6-c-ii', '4-1'), T('c/iii', 6, 'sb-q6-c-iii', '4-1'),
   T('c/iv', 12, 'sb-q6-c-iv', '4-1')],
  'Nine tasks totalling 75. a(i) 5 + 5 visible and invisible imports; a(ii) 2 x 5 (2 + 3) from five. b(i) 2 x 5 (2 + 3) from six; b(ii) 2 x 5 (2 + 3) from four; b(iii) 5 (2 + 3) from four. c(i) 6; c(ii) 6 one MNC from the scheme’s list; c(iii) 6 (3 + 3) from six; c(iv) 2 x 6 (3 + 3) from four.',
  'Imports and tourism are International Trade & Competitiveness (4-2); multinational companies are Globalisation (4-1).')
q('B7', [9], [30, 31, 32],
  [T('a/i', 5, 'sb-q7-a-i', '3-0'), T('a/ii', 10, 'sb-q7-a-ii', '3-0'), T('a/iii', 10, 'sb-q7-a-iii', '3-0'),
   T('b/i', 10, 'sb-q7-b-i', '3-0'), T('b/ii', 10, 'sb-q7-b-ii', '3-0'),
   T('c/i', 10, 'sb-q7-c-i', '3-0'), T('c/ii', 10, 'sb-q7-c-ii', '3-5'), T('c/iii', 10, 'sb-q7-c-iii', '3-5')],
  'Eight tasks totalling 75. a(i) 5; a(ii) 2 x 5 the income and output methods; a(iii) 2 x 5 (3 + 2) from six. b(i) 5 x 2 the five letters; b(ii) 10 €3,250m. c(i) 4 + 6 the EU and GDP; c(ii) 2 x 5 (3 + 2) from six; c(iii) 2 x 5 (3 + 2) from six.',
  'National income, its methods, statistics and identity and GDP are National Income (3-0); the EU is also Globalisation (4-1); the advantages and costs of growth are Economic Growth (3-5).', also=['4-1'])
q('B8', [9], [33, 34, 35, 36],
  [T('a/i', 5, 'sb-q8-a-i', '3-1'), T('a/ii', 10, 'sb-q8-a-ii', '3-1'), T('a/iii', 10, 'sb-q8-a-iii', '3-1'),
   T('b/i', 6, 'sb-q8-b-i', '3-1'), T('b/ii', 12, 'sb-q8-b-ii', '3-1'), T('b/iii', 8, 'sb-q8-b-iii', '3-1'),
   T('c', 24, 'sb-q8-c', '0-2')],
  'Seven tasks totalling 75. a(i) 5; a(ii) 2 x 5 (3 + 2) from seven; a(iii) 2 x 5 (3 + 2) from nine. b(i) 6; b(ii) 6 (3 + 3) one advantage from seven and 6 (3 + 3) one disadvantage from seven: two heading rows; b(iii) 4 any acceptable infrastructure + 4 the reason. c 3 x 8 (4 + 4) one measure each for any three of four groups: one card.',
  'The national debt, the government’s economic aims and public infrastructure spending are Fiscal Policy & the Budget (3-1); infrastructure is also Economic Growth (3-5); protecting the environment is Sustainability (0-2) and, by the government’s taxes, grants and subsidies, Government Intervention (1-3), as 2016 HL files it.', also=['3-5', '1-3'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 12': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 13)},
}
PAGE_SEL = {
 (2, 'Any payment or assistance given by'): ('not-a-task-selection', 'Section A Q2 table row, read on "or"; not a selection.'),
 (2, 'goods or services.'): ('not-a-task-selection', 'Section A Q2 table row, read on "or"; not a selection.'),
 (5, '(b) One of the characteristics of perfect competition is that perfect knowledge exists.'): ('not-a-task-selection', 'Section B Q1(b) stimulus, read on "One"; not a selection.'),
 (6, '(b) The following factors cause either a demand curve or a supply curve to shift to the right or'): ('answer-classification', 'Section B Q2(b) demand or supply, right or left is the answer for each factor; one card a question, a row a factor.'),
 (6, '(i) state whether the demand curve or supply curve will shift'): ('answer-classification', 'Section B Q2(b)(i) demand or supply is the answer for each factor; one card, two rows.'),
 (6, '(ii) state whether the curve you mention will shift to the right or the left'): ('answer-classification', 'Section B Q2(b)(ii) right or left is the answer for each factor; one card, two rows.'),
 (7, '(b) China is no longer a centrally planned economy but it is not yet a free enterprise economy. China'): ('not-a-task-selection', 'Section B Q4(b) stimulus, read on "or"; not a selection.'),
 (7, '(ii) State two measures that either the Irish government or local government/authorities'): ('not-a-task-selection', 'Section B Q3(c)(ii) either body may take the measures; one menu, not a selection.'),
 (8, 'Discuss two arguments for or against the introduction of a sugar tax.'): ('answer-classification', 'Section B Q5(a)(iii) for or against: the scheme credits each side with its own list, so two stance routes.'),
 (9, '(c) Suggest one measure which any three of the following could take to protect the environment:'): ('finite-route', 'Section B Q8(c) any three of four groups: one card claimed three times at 8.'),
 (9, '8. (a) Reducing Ireland’s national debt is one of the Irish government’s economic aims.'): ('not-a-task-selection', 'Section B Q8(a) stimulus, read on "one"; not a selection.'),
 (9, 'one reason for your choice.'): ('not-a-task-selection', 'Section B Q8(b)(iii) ask wording, read on "one"; not a selection.'),
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
 'subjectId': 'economics', 'year': 2016, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (paper pages 10-12 are blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index, and pages 37-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 82 printed asks (15 Section A + 67 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2016_ol.py). Two cards cover more than one printed ask because the scheme prices them together: Section A Q6(a)-(b), one ladder, and Section B Q1(b)(ii)-(iii), a characteristic with its note under one head. The stance route is Section B Q5(a)(iii), for or against, each credited with its own list. Section B Q8(c) any three of four groups is one card.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2016-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
