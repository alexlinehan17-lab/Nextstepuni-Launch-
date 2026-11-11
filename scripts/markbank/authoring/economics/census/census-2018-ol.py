"""Write the independent 2018 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; its Summary of Mark Allocations
(scheme p5, printed 3) agrees with every one. There is no 2018 Ordinary Irish review, so
nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2018/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2018/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2018-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: a printed choice the scheme credits with a list
# for each side (the first route of each set is the one counted).
ALT = ('-malthus', '-ricardo', '-marx', '-keynes', '-friedman')

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [6], [T('all', 16, 'sa-q1', '3-0')],
  '9 (3+3+3), (2+1+1), (1+1+1) over the three names, a word at a time: one card, a row per abbreviation (GNP 9, CPI 4, CSO 3).',
  'GNP and the CSO are National Income (3-0); the CPI is Monetary Policy & Inflation (3-3).', also=['3-3'])
q(2, [2], [6], [T('i', 12, 'sa-q2-i', '2-0'), T('ii', 4, 'sa-q2-ii', '2-0')],
  'i 3 x 4 the three labels (the scheme’s answer box prints 4 beside each); ii 1 x 4 one barrier from six.',
  'Long-run equilibrium in monopoly and barriers to entry are Market Structures (2-0).')
q(3, [2], [7], [T('i/ii/iii/iv', 16, 'sa-q3', '1-2')],
  '2 x 6 & 2 x 2 over the four TRUE/FALSE answers, not tied to a sentence: one card for (i)-(iv), the four claimed at 6, 6, 2, 2.',
  'The factors that influence a firm’s supply are The Firm (Supply) (1-2).')
q(4, [3], [7, 8], [T('i', 10, 'sa-q4-i', '0-0'), T('ii', 6, 'sa-q4-ii-smith', '0-0'), T('ii', 6, 'sa-q4-ii-malthus', '0-0'),
                   T('ii', 6, 'sa-q4-ii-ricardo', '0-0'), T('ii', 6, 'sa-q4-ii-marx', '0-0'),
                   T('ii', 6, 'sa-q4-ii-keynes', '0-0'), T('ii', 6, 'sa-q4-ii-friedman', '0-0')],
  'i 10 naming an economist from the scheme’s six; ii 6 one contribution: the scheme lists each economist’s own contributions, so one route per economist, counted once.',
  'Economists and their contributions are Economics as a Way of Thinking (0-0).')
q(5, [3], [9], [T('all', 16, 'sa-q5', '1-1')],
  '4 @ 4: the four placements (bus and train substitutes, windscreen wipers and diesel complements), one row each.',
  'Substitute and complementary goods are The Consumer (1-1).')
q(6, [3], [9], [T('i', 8, 'sa-q6-i', '3-1'), T('ii', 9, 'sa-q6-ii', '3-1')],
  'i 8 Deposit Interest Retention Tax; ii 9 one benefit from five.',
  'DIRT and its rate in the Budget are Fiscal Policy & the Budget (3-1).')
q(7, [3], [9], [T('i', 8, 'sa-q7-i', '3-3'), T('ii', 9, 'sa-q7-ii', '3-3')],
  'i 8 price inflation; ii 9 one advantage from seven.',
  'Price inflation is Monetary Policy & Inflation (3-3).')
q(8, [4], [10], [T('i', 8, 'sa-q8-i', '3-0'), T('ii', 9, 'sa-q8-ii', '3-0')],
  'i 8 imports as a leakage; ii 3 x 3 the three numbered lines.',
  'The circular flow of income is National Income (3-0).')
q(9, [4], [10], [T('all', 17, 'sa-q9', '0-1')],
  '1 x 9 & 2 x 4 over the three terms placed (scarce resources, opportunity cost, price): one card claimed at 9, 4, 4.',
  'Economic goods, scarce resources and opportunity cost are Scarcity & Choice (0-1).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [11, 12],
  [T('a/i', 20, 'sb-q1-a-i', '2-0'), T('a/ii', 10, 'sb-q1-a-ii', '2-0'),
   T('b/i', 7, 'sb-q1-b-i', '2-0'), T('b/ii', 7, 'sb-q1-b-ii', '2-0'), T('b/iii', 7, 'sb-q1-b-iii', '2-0'),
   T('c', 24, 'sb-q1-c', '2-0')],
  'Six tasks totalling 75. a(i) 5 @ 4 the five labels; a(ii) 5 + 5 P1 and Q1 (hidden solution diagram). b 3 @ 7, one card each. c 3 x 8, two advantages for consumers from three and one challenge for producers from three: two heading rows.',
  'Perfect competition and increased competition among airlines are Market Structures (2-0).')
q('B2', [6], [13, 14, 15],
  [T('a/i', 10, 'sb-q2-a-i', '1-1'), T('a/ii', 12, 'sb-q2-a-ii', '1-1'), T('a/iii', 3, 'sb-q2-a-iii', '1-1'),
   T('b/i', 7, 'sb-q2-b-i', '1-1'), T('b/ii', 6, 'sb-q2-b-ii', '1-1'), T('b/iii', 12, 'sb-q2-b-iii', '1-1'),
   T('c/i', 10, 'sb-q2-c-i', '1-3'), T('c/ii', 15, 'sb-q2-c-ii', '1-3')],
  'Eight tasks totalling 75. a(i) 5 + 5; a(ii) 3 @ 4 A 40, B 20, C 10 (the scheme’s workings); a(iii) 1 + 2. b(i) 7; b(ii) 6; b(iii) 2 @ 6 (3 + 3) from four. c(i) 2 @ 5 from five; c(ii) 3 @ 5, two advantages from three and one disadvantage from two: two heading rows.',
  'Utility, marginal utility and demand are The Consumer (1-1); the sugar tax is Government Intervention (1-3), and as a tax introduced in the Budget also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q('B3', [7], [16, 17],
  [T('a', 24, 'sb-q3-a', '0-1'), T('b/i', 12, 'sb-q3-b-i', '1-5'), T('b/ii', 6, 'sb-q3-b-ii', '1-5'),
   T('b/iii', 12, 'sb-q3-b-iii', '1-5'), T('c', 21, 'sb-q3-c', '2-1')],
  'Five tasks totalling 75. a 3 x 8 (3 + 2 + 3), each factor with its explanation and return. b(i) 3 @ 4 A €2,000, B €3,000, C €4,000; b(ii) 6 €1,400; b(iii) 2 @ 6 (4 + 2) fixed and variable costs with an example. c 3 x 7 (4 + 3), one effect each for employees, businesses and consumers, each from its printed positives and negatives: three heading rows.',
  'The factors of production and their returns are Scarcity & Choice (0-1); total revenue, profit and fixed and variable costs are Costs of Production, Revenue & Profit (1-5); the minimum wage is The Labour Market (2-1), a government-set wage floor (Government Intervention, 1-3) whose effects include job losses (Employment & Unemployment, 3-2).', also=['1-3', '3-2'])
q('B4', [7], [18, 19, 20],
  [T('a', 21, 'sb-q4-a', '3-4'), T('b/i', 12, 'sb-q4-b-i', '3-4'), T('b/ii', 12, 'sb-q4-b-ii', '3-4'),
   T('c/i', 12, 'sb-q4-c-i', '3-4'), T('c/ii', 18, 'sb-q4-c-ii', '3-4')],
  'Five tasks totalling 75. a any three of four functions, 3 x 7 (2 + 5). b(i) 2 @ 6 (3 + 3) from five; b(ii) 2 @ 6 (3 + 3), one advantage from six and one disadvantage from three: two heading rows. c(i) 2 @ 6 two methods from six; c(ii) 3 @ 6 banks, businesses and consumers: three heading rows.',
  'Money, savings and non-cash payment are Financial Sector (3-4).')
q('B5', [8], [21, 22, 23, 24],
  [T('a/i', 6, 'sb-q5-a-i', '3-1'), T('a/ii', 6, 'sb-q5-a-ii', '3-1'), T('a/iii', 12, 'sb-q5-a-iii', '3-1'),
   T('b/i', 9, 'sb-q5-b-i', '3-1'), T('b/ii', 9, 'sb-q5-b-ii', '3-1'), T('b/iii', 12, 'sb-q5-b-iii', '3-1'),
   T('c/i', 7, 'sb-q5-c-i', '0-1'), T('c/ii', 14, 'sb-q5-c-ii', '3-1')],
  'Eight tasks totalling 75. a(i) 6 (3 + 3) and a(ii) 6 (3 + 3) printed beside the answer and its explanation together: questionTotal, unpriced rows; a(iii) 2 @ 6 (3 + 3), one advantage from four and one disadvantage from five: two heading rows. b(i) and (ii) share one 6 x 3 over six cells, three names and three direct/indirect answers, a row each; b(iii) 2 @ 6 direct and indirect taxes. c(i) 7; c(ii) 2 x 7 (4 + 3) from seven.',
  'The budget deficit, the national debt, taxes and spending on education are Fiscal Policy & the Budget (3-1); opportunity cost is Scarcity & Choice (0-1); the economic advantages of education spending (a better workforce, productivity, growth) are also Economic Growth (3-5).', also=['3-5'])
q('B6', [9], [25, 26, 27, 28, 29],
  [T('a/i', 10, 'sb-q6-a-i', '3-0'), T('a/ii', 10, 'sb-q6-a-ii', '3-0'),
   T('b/i', 10, 'sb-q6-b-i', '4-1'), T('b/ii', 10, 'sb-q6-b-ii', '4-1'), T('b/iii', 5, 'sb-q6-b-iii', '4-1'),
   T('c/i', 10, 'sb-q6-c-i', '4-0'), T('c/ii', 10, 'sb-q6-c-ii', '4-0'), T('c/iii', 10, 'sb-q6-c-iii', '4-0')],
  'Eight tasks totalling 75. a(i) 10 (5 x 2) the five letters; a(ii) 10 €3,700m. b(i) 2 x 5 the two terms; b(ii) 2 x 5 (3 + 2) from five; b(iii) 1 x 5 (3 + 2) from five. c(i) 2 x 5 from nine; c(ii) 2 x 5 from six; c(iii) 2 x 5 from seven.',
  'The national income identity is National Income (3-0); multinationals are Globalisation (4-1), economic growth Economic Growth (3-5); LDCs and aid are Growth & Development (4-0).', also=['3-5'])
q('B7', [9], [30, 31, 32],
  [T('a/i', 6, 'sb-q7-a-i', '4-2'), T('a/ii', 18, 'sb-q7-a-ii', '4-2'),
   T('b/i', 12, 'sb-q7-b-i', '4-2'), T('b/ii', 6, 'sb-q7-b-ii', '4-2'), T('b/iii', 12, 'sb-q7-b-iii', '4-2'),
   T('c/i', 8, 'sb-q7-c-i', '4-2'), T('c/ii', 6, 'sb-q7-c-ii', '4-2'), T('c/iii', 7, 'sb-q7-c-iii', '4-2')],
  'Eight tasks totalling 75. a(i) 6; a(ii) 3 x 6 (3 + 3) from eight. b(i) 2 x 6 visible exports and imports; b(ii) 2 x 3 an example of each; b(iii) 2 x 6 from five. c(i) 8; c(ii) 2 x 3 tariffs and quotas; c(iii) 1 x 7 (4 + 3) from eight.',
  'An open economy, visible trade, the balance of trade and Brexit are International Trade & Competitiveness (4-2); Brexit, the UK leaving the EU, is also Globalisation (4-1), as EU membership is filed.', also=['4-1'])
q('B8', [10], [33, 34, 35],
  [T('a/i', 3, 'sb-q8-a-i', '3-2'), T('a/ii', 27, 'sb-q8-a-ii', '3-2'), T('b', 24, 'sb-q8-b', '2-1'),
   T('c/i', 7, 'sb-q8-c-i', '3-1'), T('c/ii', 14, 'sb-q8-c-ii', '3-1')],
  'Five tasks totalling 75. a(i) 3; a(ii) 3 x 9 (5 + 4) retailers, government finances and the balance of trade: three heading rows. b 4 x 6, two advantages for employees from three and two for the government from four: two heading rows. c(i) 1 x 7 from seven; c(ii) 2 x 7 (4 + 3) from nine.',
  'Measuring unemployment and rising employment are Employment & Unemployment (3-2); extending the retirement age is The Labour Market (2-1), its effect on the pension bill Fiscal Policy & the Budget (3-1); homelessness measures are Fiscal Policy & the Budget (3-1) and, as intervention in the housing market (social housing, rent regulation, subsidies), Government Intervention (1-3).', also=['3-1', '1-3'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
}
PAGE_SEL = {
 (2, 'SENTENCE TRUE or FALSE'): ('answer-classification', 'Section A Q3 table header; the TRUE or FALSE answers are the four tasks of one card.'),
 (2, 'Write True or False after each of the following sentences.'): ('answer-classification', 'Section A Q3 four TRUE/FALSE answers, claimed at 6, 6, 2, 2.'),
 (3, '5. The following items are either substitute goods or complementary goods for cars.'): ('answer-classification', 'Section A Q5 each item is a substitute or a complement; one card, four placements.'),
 (4, '9. Use three of the five terms below to complete the explanation for economic goods.'): ('finite-route', 'Section A Q9 three of five terms: one card, the three placed terms claimed at 9, 4, 4.'),
 (6, '(ii) State whether the shift in demand from D1 to D2 above represents an increase or'): ('answer-classification', 'Section B Q2(b)(ii) increase or decrease is the answer (an increase); one card.'),
 (7, '4. (a) State and explain any three functions of money. (21 marks)'): ('finite-route', 'Section B Q4(a) any three of four functions: one card claimed three times at 7.'),
 (8, '(i) Is the government planning a budget deficit or budget surplus? Explain your answer.'): ('answer-classification', 'Section B Q5(a)(i) deficit or surplus is the answer (a deficit); one card.'),
 (8, '(ii) State whether each tax is an example of a direct tax or an indirect tax.'): ('answer-classification', 'Section B Q5(b)(ii) direct or indirect is the answer for each tax; one card, three rows.'),
 (8, '\uf0b7 a tax on goods or services.'): ('not-a-task-selection', 'Section B Q5(b) stem bullet, read on "or"; not a selection.'),
 (10, '8. (a) ‘Ireland’s unemployment rate is expected to be 6 % or lower by the end of the year.’'): ('not-a-task-selection', 'Section B Q8(a) stimulus, read on "or"; not a selection.'),
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
 'subjectId': 'economics', 'year': 2018, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 36 scheme pages (scheme pages 1-5 are the SEC cover, the note on published schemes, the title page, the notes and index and the Summary of Mark Allocations, which agrees with every tariff here; scheme page 36 and paper pages 11-12 are blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 70 printed asks (17 Section A + 53 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2018_ol.py). Section A Q4(ii) is one route per economist because the scheme lists each economist’s own contributions; Section A Q3 and Q9 are one card each, claimed at the printed steps.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2018-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
