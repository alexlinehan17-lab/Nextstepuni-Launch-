"""Write the independent 2014 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2014 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2014/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2014/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2014-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: Section B Q4(c) asks for ANY TWO of three
# budget measures, and the scheme lists each measure's own arguments, so each
# measure is a route; the first two are the ones counted.
ALT = ('-tobacco',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '0-1')],
  'The three words placed (SOCIAL; RESOURCES / FACTORS OF PRODUCTION / INPUTS; WANTS): the first correct response 8, the 2nd and 3rd 4 each: one card.',
  'Economics as the study of scarce resources and infinite wants is Scarcity & Choice (0-1).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '4-2')],
  'The four ticks: the first correct response 10, the 2nd, 3rd and 4th 2 each: one card.',
  'Visible and invisible exports and imports are International Trade & Competitiveness (4-2).')
q(3, [2], [5], [T('all', 16, 'sa-q3', '1-1')],
  'The two bracketed words (INCREASING, FALL): the first correct response 12, the 2nd 4.',
  'Diminishing marginal utility is The Consumer (Demand) (1-1).')
q(4, [3], [5], [T('all', 16, 'sa-q4', '3-1')],
  'One effect each for retailers and the government’s finances: the 1st correct response 10, the 2nd 6.',
  'Public sector pay and the government’s finances are Fiscal Policy & the Budget (3-1).')
q(5, [3], [6], [T('all', 16, 'sa-q5', '3-0')],
  'The working, 5 correct components at 3, and the answer 1 (€3,300m).',
  'National income from C + I + G + X – M is National Income (3-0).')
q(6, [3], [6], [T('all', 17, 'sa-q6', '2-1')],
  'The three ticks (TRUE, FALSE, FALSE): the 1st and 2nd correct responses 7 each, the 3rd 3: one card.',
  'A trade union’s minimum wage and the supply of labour are The Labour Market (2-1).')
q(7, [4], [7], [T('all', 17, 'sa-q7', '3-1')],
  'One effect each for businesses and homeowners: the 1st correct response 11, the 2nd 6.',
  'A tax relief scheme announced in the Budget is Fiscal Policy & the Budget (3-1).')
q(8, [4], [7], [T('all', 17, 'sa-q8', '0-0')],
  'The four matches (A 3, B 1, C 4, D 2): the 1st correct response 8, the 2nd, 3rd and 4th 3 each: one card.',
  'Economists and their ideas are Economics as a Way of Thinking (0-0).')
q(9, [4], [8], [T('all', 17, 'sa-q9', '1-4')],
  'The four symbols left blank (ΔQ, P1, P2, Q2): the 1st correct response 8, the 2nd, 3rd and 4th 3 each: one card.',
  'The PED formula is Elasticity (1-4).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [9, 10, 11],
  [T('a/i', 20, 'sb-q1-a-i', '2-0'), T('a/ii', 10, 'sb-q1-a-ii', '2-0'), T('b/i', 7, 'sb-q1-b-i', '2-0'),
   T('b/ii-iii', 14, 'sb-q1-b-ii', '2-0'), T('c/i', 12, 'sb-q1-c-i', '2-0'), T('c/ii', 12, 'sb-q1-c-ii', '2-0')],
  'Six cards for seven asks, totalling 75. a(i) 5 @ 4 the five labels; a(ii) P1 and C1, the 1st correct 6 and the 2nd 4 (hidden solution diagram). b(i) 7; b(ii) and (iii) share one 2 x 7, a barrier with its note: one card covers both. c(i) 2 @ 6 from two; c(ii) 2 @ 6 from three.',
  'Monopoly, barriers to entry and competition for a statutory monopoly are Market Structures (2-0).')
q('B2', [6], [12, 13, 14],
  [T('a/i', 14, 'sb-q2-a-i', '0-1'), T('a/ii', 7, 'sb-q2-a-ii', '0-1'), T('b/i', 6, 'sb-q2-b-i', '1-1'),
   T('b/ii', 12, 'sb-q2-b-ii', '1-1'), T('b/iii', 6, 'sb-q2-b-iii', '0-2'), T('c/i', 6, 'sb-q2-c-i', '1-3'),
   T('c/ii', 12, 'sb-q2-c-ii', '1-3'), T('c/iii', 12, 'sb-q2-c-iii', '2-2')],
  'Eight tasks totalling 75. a(i) any two of three terms @ 7; a(ii) 7 (No, it is not transferable). b(i) 6; b(ii) 2 @ 6 from four; b(iii) 6 one advantage from three. c(i) 6 one measure from eight; c(ii) 2 x 6 from five; c(iii) 2 x 6 from four.',
  'Economic goods are Scarcity & Choice (0-1); the law of demand and a shift in demand are The Consumer (Demand) (1-1); the advantages of electric cars are Sustainability (0-2); measures against alcohol abuse and their benefits for individuals are Government Intervention (1-3), and the benefits for society Market Failure (2-2), as a demerit good’s external costs.')
q('B3', [7], [15, 16, 17],
  [T('a/i', 8, 'sb-q3-a-i', '1-0'), T('a/ii', 8, 'sb-q3-a-ii', '1-0'), T('a/iii', 4, 'sb-q3-a-iii', '1-0'),
   T('b/i', 5, 'sb-q3-b-i', '4-0'), T('b/ii', 10, 'sb-q3-b-ii', '4-0'), T('b/iii', 10, 'sb-q3-b-iii', '4-0'),
   T('c/i', 9, 'sb-q3-c-i', '3-0'), T('c/ii', 21, 'sb-q3-c-ii', '3-5')],
  'Eight tasks totalling 75. a(i) 2 explanations @ 4; a(ii) 2 examples @ 4; a(iii) 4 one advantage from five. b(i) 5; b(ii) 2 @ 5 from eight; b(iii) 2 @ 5 from four. c(i) 9 (GNP / GDP); c(ii) 3 @ 7, one benefit each for citizens, retailers and the government’s finances: three heading rows.',
  'Centrally planned and mixed economic systems are The Market Economy (1-0); economic growth in LDCs and helping them are Growth & Development (4-0); the measure of the economy’s size is National Income (3-0); the benefits of economic growth are Economic Growth (3-5).')
q('B4', [7], [18, 19, 20, 21],
  [T('a/i', 6, 'sb-q4-a-i', '3-1'), T('a/ii', 12, 'sb-q4-a-ii', '3-1'), T('a/iii', 12, 'sb-q4-a-iii', '3-1'),
   T('b/i', 9, 'sb-q4-b-i', '3-1'), T('b/ii', 12, 'sb-q4-b-ii', '3-1'),
   T('c', 12, 'sb-q4-c-jobseekers', '3-1'), T('c', 12, 'sb-q4-c-dirt', '3-1'), T('c', 12, 'sb-q4-c-tobacco', '3-1')],
  'Six tasks totalling 75. a(i) 6; a(ii) 2 explanations @ 6, each tax indirect; a(iii) 2 @ 6 from four. b(i) two examples from six, the 1st 5 and the 2nd 4; b(ii) 2 @ 6 from six. c any two of three measures, each one argument in favour and one against, the 1st correct response 8 and the 2nd 4: the scheme lists each measure’s own arguments, so one route per measure, two counted.',
  'VAT, the airport travel tax, austerity and the Budget 2014 measures are Fiscal Policy & the Budget (3-1); Jobseekers Allowance is also Employment & Unemployment (3-2), DIRT the Financial Sector (3-4) and tobacco duty Government Intervention (1-3).', also=['3-2', '3-4', '1-3'])
q('B5', [8], [22, 23, 24],
  [T('a/i', 13, 'sb-q5-a-i', '1-5'), T('a/ii', 12, 'sb-q5-a-ii', '1-5'), T('b/i', 5, 'sb-q5-b-i', '0-1'),
   T('b/ii', 10, 'sb-q5-b-ii', '0-1'), T('b/iii', 10, 'sb-q5-b-iii', '0-1'), T('c/i', 15, 'sb-q5-c-i', '0-1'),
   T('c/ii', 10, 'sb-q5-c-ii', '1-2')],
  'Seven tasks totalling 75. a(i) fixed costs 5 + variable costs 4 + one example of each 2 + 2; a(ii) two reasons from five, the 1st 8 and the 2nd 4. b(i) 5; b(ii) and b(iii) two from four and from five, the 1st 6 and the 2nd 4. c(i) the three factors @ 5; c(ii) two factors from seven, the 1st 6 and the 2nd 4.',
  'Fixed and variable costs are Costs of Production, Revenue & Profit (1-5); the entrepreneur and the factors of production are Scarcity & Choice (0-1); where a business locates is The Firm (Supply) (1-2).')
q('B6', [8], [25, 26, 27],
  [T('a/i', 7, 'sb-q6-a-i', '3-4'), T('a/ii', 7, 'sb-q6-a-ii', '3-4'), T('a/iii', 7, 'sb-q6-a-iii', '3-3'),
   T('b/i', 9, 'sb-q6-b-i', '3-3'), T('b/ii', 6, 'sb-q6-b-ii', '3-3'), T('b/iii', 15, 'sb-q6-b-iii', '3-3'),
   T('c/i', 10, 'sb-q6-c-i', '3-4'), T('c/ii', 10, 'sb-q6-c-ii', '3-4'), T('c/iii', 4, 'sb-q6-c-iii', '3-4')],
  'Nine tasks totalling 75. a the three terms @ 7. b(i) 9; b(ii) 6; b(iii) 3 @ 5 from six. c(i) two functions from five and c(ii) two effects from six, each the 1st 6 and the 2nd 4; c(iii) 4 one reason from three.',
  'Barter, money, commercial banks and credit unions are Financial Sector (3-4); price inflation, the ECB and interest rates are Monetary Policy & Inflation (3-3).')
q('B7', [9], [28, 29, 30],
  [T('a/i', 7, 'sb-q7-a-i', '4-2'), T('a/ii', 8, 'sb-q7-a-ii', '4-2'), T('a/iii', 10, 'sb-q7-a-iii', '4-2'),
   T('b/i', 6, 'sb-q7-b-i', '4-2'), T('b/ii', 16, 'sb-q7-b-ii', '4-2'), T('b/iii', 8, 'sb-q7-b-iii', '4-2'),
   T('c/i', 5, 'sb-q7-c-i', '4-1'), T('c/ii', 15, 'sb-q7-c-ii', '4-1')],
  'Eight tasks totalling 75. a(i) 7; a(ii) 2 definitions @ 4; a(iii) 2 @ 5 from six. b(i) 6; b(ii) 2 @ 8 from six; b(iii) 2 @ 4 from four. c(i) 5; c(ii) 3 @ 5 from the positive and negative columns.',
  'The WTO, tariffs, quotas, protection, the open economy and exports are International Trade & Competitiveness (4-2); the WTO is also Globalisation (4-1); the EU and its enlargement are Globalisation (4-1).')
q('B8', [9], [31, 32, 33, 34],
  [T('a/i', 10, 'sb-q8-a-i', '3-2'), T('a/ii', 10, 'sb-q8-a-ii', '3-2'), T('a/iii', 10, 'sb-q8-a-iii', '3-2'),
   T('b/i', 10, 'sb-q8-b-i', '3-2'), T('b/ii', 15, 'sb-q8-b-ii', '3-2'), T('c/i', 12, 'sb-q8-c-i', '3-1'),
   T('c/ii', 8, 'sb-q8-c-ii', '3-1')],
  'Seven tasks totalling 75. a(i) 2 explanations @ 5; a(ii) two reasons from five, the 1st 6 and the 2nd 4; a(iii) one positive and one negative effect @ 5: two heading rows. b(i) 10; b(ii) one effect each on retailers, the government’s finances and the Balance of Trade, the 1st correct response 7 and the 2nd and 3rd 4. c(i) two aims from six, the 1st 8 and the 2nd 4; c(ii) 2 measures @ 4 from four.',
  'Emigration, immigration, the CSO and a fall in unemployment are Employment & Unemployment (3-2); the government’s economic aims and the measures to achieve them are Fiscal Policy & the Budget (3-1).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 9': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 10)},
}
PAGE_SEL = {
 (2, '2. Indicate by means of a tick (\uf0fc) the category to which each good or service belongs:'): ('answer-classification', 'Section A Q2 the ticked category is the answer for each statement; one card, four answers.'),
 (2, '3. Choose the correct word from the bracketed words to complete the following statement:'): ('answer-classification', 'Section A Q3 the bracketed choices are the answers (INCREASING, FALL); one card.'),
 (3, 'Tick (\uf0fc) True or False after each of the following statements:'): ('answer-classification', 'Section A Q6 TRUE or FALSE is the answer for each statement; one card, three answers.'),
 (6, '(i) Explain any two of the underlined terms.'): ('finite-route', 'Section B Q2(a)(i) any two of three terms: one card claimed twice at 7.'),
 (7, '(c) In recent years Ireland has been in recession and has experienced little or no economic growth.'): ('not-a-task-selection', 'Section B Q3(c) stimulus, read on "or"; not a selection.'),
 (7, '(ii) Are the taxes underlined above direct taxes or indirect taxes? Explain your answers.'): ('answer-classification', 'Section B Q4(a)(ii) direct or indirect is the answer (both indirect); one card.'),
 (7, 'ANY TWO of the following government measures announced in Budget 2014:'): ('finite-route', 'Section B Q4(c) any two of three measures: the scheme lists each measure’s own arguments, so one route per measure, two counted.'),
 (8, '(c) Businesses need factors of production to produce output or provide a service.'): ('not-a-task-selection', 'Section B Q5(c) stimulus, read on "or"; not a selection.'),
 (3, 'Page 3 of 9 OVER'): ('not-a-task-selection', 'Page footer, read on "of"; not a selection.'),
 (9, '(c) Increasing employment is one of the economic aims of the Irish government.'): ('not-a-task-selection', 'Section B Q8(c) stimulus, read on "one"; not a selection.'),
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
 'subjectId': 'economics', 'year': 2014, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 36 scheme pages (paper pages 10-12 are blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index, and pages 35-36 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 69 printed asks (9 Section A + 60 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2014_ol.py). Section B Q1(b)(ii)-(iii) is one card, as the scheme prices a barrier with its note. Section B Q4(c) any two of three budget measures is one route per measure, two counted.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2014-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
