"""Write the independent 2013 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2013 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2013/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2013/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2013-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: none on this paper (no printed stance or
# either-or choice is credited with a list for each side).
ALT = ()

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '0-1')],
  'The four spaces: 2 at 6 + 2 at 2, the first two correct 6 each: one card.',
  'The factors of production and their examples are Scarcity & Choice (0-1).')
q(2, [2], [5], [T('i/ii/iii/iv', 16, 'sa-q2', '1-2')],
  'The four TRUE/FALSE answers: 2 at 6 + 2 at 2: one card.',
  'What influences an individual firm’s supply is The Firm (Supply) (1-2).')
q(3, [2], [5], [T('all', 16, 'sa-q3', '1-1')],
  'One reason 10 from six + one effect for retailers 6 from five: one card, two rows.',
  'Consumers’ online purchasing is The Consumer (Demand) (1-1); its effects on retailers are The Firm (Supply) (1-2).', also=['1-2'])
q(4, [2], [6], [T('all', 16, 'sa-q4', '3-4')],
  'The three motives: 10 + 3 + 3, the first correct 10: one card.',
  'Keynes’s motives for holding money are Financial Sector (3-4), as 2015 OL files them.')
q(5, [2], [6], [T('all', 16, 'sa-q5', '4-0')],
  'One reason 10 from four + one effect for LDCs 6 from five: one card, two rows.',
  'Aid to LDCs and its effects are Growth & Development (4-0).')
q(6, [3], [7], [T('a', 9, 'sa-q6-a', '1-5'), T('b/i', 5, 'sa-q6-b-i', '1-5'), T('b/ii', 3, 'sa-q6-b-ii', '1-5')],
  'a the four costs placed, 1 at 3 + 3 at 2; b(i) 5 the total cost; b(ii) 3 the profit.',
  'Fixed and variable costs, total cost and profit are Costs of Production, Revenue & Profit (1-5).')
q(7, [3], [7], [T('all', 17, 'sa-q7', '1-3')],
  'One reason 11 from five + one effect 6 from four: one card, two rows.',
  'Private health insurance and the pressure on public health services are Government Intervention (1-3); state health funding is also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q(8, [3], [8], [T('a', 15, 'sa-q8-a', '2-0'), T('b', 2, 'sa-q8-b', '2-0')],
  'a the three curves at 5 (3 + 2); b 2 (1 + 1), the price and the average cost shown (hidden solution diagram).',
  'Monopoly equilibrium is Market Structures (2-0).')
q(9, [3], [8], [T('all', 17, 'sa-q9', '3-1')],
  'The explanation 7 (any one of three) + one benefit 10 from five: one card, two rows.',
  'Public infrastructure spending is Fiscal Policy & the Budget (3-1), as capital spending; a public hospital is also Government Intervention (1-3).', also=['1-3'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [9, 10, 11, 12],
  [T('a/i', 24, 'sb-q1-a-i', '2-0'), T('a/ii', 6, 'sb-q1-a-ii', '2-0'), T('b/i', 7, 'sb-q1-b-i', '2-0'),
   T('b/ii-iii', 14, 'sb-q1-b-ii', '2-0'), T('c/i', 4, 'sb-q1-c-i', '1-0'), T('c/ii', 10, 'sb-q1-c-ii', '1-0'),
   T('c/iii', 10, 'sb-q1-c-iii', '3-1')],
  'Seven cards for eight asks, totalling 75. a(i) the six labels at 4; a(ii) Q1, C1 and P1, 3 at 2 (hidden solution diagram). b(i) 7; b(ii) and (iii) share one 2 at 7 (4 + 3), a characteristic with its note: one card covers both. c(i) 4 one reason from four; c(ii) one effect per category, 2 at 5 (2 + 3): two heading rows; c(iii) 2 at 5 (2 + 3) from four.',
  'Perfect competition, its labels and characteristics are Market Structures (2-0); petrol and diesel prices and their effects are The Market Economy (1-0); the measures to reduce motorists’ costs (VAT, NCT, motor tax) are Fiscal Policy & the Budget (3-1).')
q('B2', [5], [13, 14, 15],
  [T('a/i-iii', 30, 'sb-q2-a', '1-0'), T('b/i', 10, 'sb-q2-b-i', '1-1'), T('b/ii', 15, 'sb-q2-b-ii', '1-1'),
   T('c/i', 12, 'sb-q2-c-i', '0-1'), T('c/ii', 8, 'sb-q2-c-ii', '0-1')],
  'Five cards for seven asks, totalling 75. a(i)-(iii) share one graph: D/C 10 (5 points at 2), S/C 10, the four labels at 1, and Pe and Qe 2 at 3: one card (hidden solution graph). b(i) any two of three terms at 5; b(ii) the shift 2 + its explanation 3 + two measures at 5 (2 + 3) from four. c(i) each cost 6; c(ii) the financial cost 5 + the opportunity cost 3.',
  'Demand, supply and equilibrium are The Market Economy (1-0); normal, substitute and complementary goods and a shift in demand are The Consumer (Demand) (1-1); financial and opportunity cost are Scarcity & Choice (0-1).')
q('B3', [6], [16, 17, 18, 19],
  [T('a/i', 7, 'sb-q3-a-i', '2-1'), T('a/ii', 12, 'sb-q3-a-ii', '2-1'), T('a/iii', 6, 'sb-q3-a-iii', '2-1'),
   T('b/i', 10, 'sb-q3-b-i', '3-1'), T('b/ii', 6, 'sb-q3-b-ii', '3-1'), T('b/iii', 10, 'sb-q3-b-iii', '3-1'),
   T('c/i', 12, 'sb-q3-c-i', '2-1'), T('c/ii', 12, 'sb-q3-c-ii', '2-1')],
  'Eight tasks totalling 75. a(i) 7; a(ii) 2 at 6 (3 + 3) from eight; a(iii) the definition 4 + one factor 2 from six. b(i) the public sector 5 + an example 5; b(ii) one reason at 6 (3 + 3) from three; b(iii) 2 at 5 (2 + 3) from six. c(i) 2 at 6 (3 + 3) from five; c(ii) any 2 actions at 6 (3 + 3), from any two of the three groups.',
  'Labour, wage differentials, occupational mobility and the IT skills shortage are The Labour Market (2-1); the public sector and its numbers are Fiscal Policy & the Budget (3-1), and its job losses also Employment & Unemployment (3-2).', also=['3-2'])
q('B4', [6], [20, 21, 22, 23],
  [T('a/i', 5, 'sb-q4-a-i', '1-3'), T('a/ii', 10, 'sb-q4-a-ii', '1-3'), T('a/iii', 10, 'sb-q4-a-iii', '1-3'),
   T('b/i', 5, 'sb-q4-b-i', '3-1'), T('b/ii', 10, 'sb-q4-b-ii', '1-3'), T('b/iii', 5, 'sb-q4-b-iii', '1-3'),
   T('c', 30, 'sb-q4-c', '3-1')],
  'Seven tasks totalling 75. a(i) 5; a(ii) 2 at 5 (2 + 3) from seven; a(iii) 2 at 5 (2 + 3) from seven. b(i) 5; b(ii) 2 at 5 (2 + 3) from five; b(iii) 1 at 5 (2 + 3) from five. c each of the three measures one argument in favour 5 (2 + 3) and one against 5 (2 + 3): one card, six heading rows.',
  'Privatisation is Government Intervention (1-3), as earlier reviews file it; VAT and the Budget 2013 measures are Fiscal Policy & the Budget (3-1); a sugar tax is Government Intervention (1-3).')
q('B5', [7], [24, 25, 26],
  [T('a/i', 20, 'sb-q5-a-i', '3-0'), T('a/ii', 10, 'sb-q5-a-ii', '3-0'), T('b/i', 10, 'sb-q5-b-i', '3-0'),
   T('b/ii', 10, 'sb-q5-b-ii', '3-1'), T('c/i', 5, 'sb-q5-c-i', '3-0'), T('c/ii', 10, 'sb-q5-c-ii', '3-0'),
   T('c/iii', 10, 'sb-q5-c-iii', '3-0')],
  'Seven tasks totalling 75. a(i) the five lines at 4; a(ii) the three activities 3 + 3 + 4. b(i) 2 at 5 (2 + 3) from six; b(ii) 2 at 5 (2 + 3) from six. c(i) 5 one example from two; c(ii) 2 at 5 (2 + 3) from four; c(iii) 2 at 5 (2 + 3) from five.',
  'The circular flow, consumer expenditure and the black economy are National Income (3-0), as earlier reviews file the black economy; the government’s actions to raise spending are Fiscal Policy & the Budget (3-1).')
q('B6', [8], [27, 28, 29, 30],
  [T('a/i', 4, 'sb-q6-a-i', '3-2'), T('a/ii', 8, 'sb-q6-a-ii', '3-2'), T('a/iii', 12, 'sb-q6-a-iii', '3-2'),
   T('b/i', 12, 'sb-q6-b-i', '3-5'), T('b/ii', 9, 'sb-q6-b-ii', '3-5'), T('c/i', 6, 'sb-q6-c-i', '3-2'),
   T('c/ii', 12, 'sb-q6-c-ii', '3-2'), T('c/iii', 12, 'sb-q6-c-iii', '3-2')],
  'Eight tasks totalling 75. a(i) 4; a(ii) the 1st reason 6 (4 + 2) and the 2nd 2; a(iii) the 1st effect 8 (6 + 2) and the 2nd 4 (2 + 2), negative or positive. b(i) the 1st effect 8 (6 + 2) and the 2nd 4; b(ii) one reason at 9 (6 + 3) from four. c(i) 6; c(ii) the 1st reason 8 and the 2nd 4; c(iii) one measure each for consumers and the government, the 1st 8 and the 2nd 4.',
  'Emigration, its causes and effects, and unemployment, its measurement, causes and remedies are Employment & Unemployment (3-2); an ageing population is Economic Growth (3-5), as 2015 HL files it, and the retirement age also Fiscal Policy & the Budget (3-1) and The Labour Market (2-1).', also=['3-1', '2-1'])
q('B7', [8], [31, 32, 33, 34],
  [T('a/i', 2, 'sb-q7-a-i', '4-2'), T('a/ii', 12, 'sb-q7-a-ii', '4-2'), T('a/iii', 12, 'sb-q7-a-iii', '4-2'),
   T('b/i', 12, 'sb-q7-b-i', '4-2'), T('b/ii', 12, 'sb-q7-b-ii', '4-2'), T('c/i', 9, 'sb-q7-c-i', '4-1'),
   T('c/ii', 4, 'sb-q7-c-ii', '4-1'), T('c/iii', 12, 'sb-q7-c-iii', '4-1')],
  'Eight tasks totalling 75. a(i) 2 one example from three; a(ii) and a(iii) the 1st 8 (6 + 2) and the 2nd 4 (2 + 2), from five and from eight. b(i) and b(ii) the 1st 8 (6 + 2) and the 2nd 4 (2 + 2), from seven and from five. c(i) 9; c(ii) 4 one MNC from four; c(iii) the 1st benefit 8 and the 2nd 4 from six.',
  'Imports, their benefits, restricting them and tourism are International Trade & Competitiveness (4-2); Irish multinationals are Globalisation (4-1).')
q('B8', [9], [35, 36, 37, 38],
  [T('a/i', 7, 'sb-q8-a-i', '3-1'), T('a/ii', 10, 'sb-q8-a-ii', '3-4'), T('a/iii', 8, 'sb-q8-a-iii', '3-4'),
   T('b/i', 6, 'sb-q8-b-i', '3-4'), T('b/ii', 18, 'sb-q8-b-ii', '3-4'), T('c/i', 6, 'sb-q8-c-i', '3-3'),
   T('c/ii', 12, 'sb-q8-c-ii', '3-4'), T('c/iii', 8, 'sb-q8-c-iii', '4-1')],
  'Eight tasks totalling 75. a(i) 7; a(ii) 2 at 5 (2 + 3) from nine; a(iii) one advantage 4 + one disadvantage 4: two heading rows. b(i) one reason at 6 (3 + 3) from three; b(ii) one effect per group at 6 (3 + 3): three heading rows. c(i) 6; c(ii) durable 4 + two other characteristics at 4 from five; c(iii) one advantage 4 + one disadvantage 4: two heading rows.',
  'DIRT is Fiscal Policy & the Budget (3-1), as 2015 OL files it; savings, the banks and the characteristics of money are Financial Sector (3-4); the ECB is Monetary Policy & Inflation (3-3); the euro’s advantages and disadvantages for Ireland are Globalisation (4-1), and its interest rates also Monetary Policy & Inflation (3-3).', also=['3-3'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 9': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 10)},
}
PAGE_SEL = {
 (2, 'SENTENCE TRUE or FALSE'): ('answer-classification', 'Section A Q2 table header; the TRUE or FALSE answers are the four tasks of one card.'),
 (2, 'Write True or False after each of the following sentences.'): ('answer-classification', 'Section A Q2 TRUE or FALSE is the answer for each sentence; one card, four answers.'),
 (4, '(b) One of the characteristics of Perfect Competition is that all goods produced are'): ('not-a-task-selection', 'Section B Q1(b) stimulus, read on "One"; not a selection.'),
 (5, '(b) (i) Explain any two of the following economic terms:'): ('finite-route', 'Section B Q2(b)(i) any two of three terms: one card claimed twice at 5.'),
 (6, '(ii) Outline one action which any two of the following could take to reduce this skills'): ('finite-route', 'Section B Q3(c)(ii) one action for any two of three groups: one card claimed twice at 6.'),
 (8, 'choose to visit Ireland in 2013.'): ('not-a-task-selection', 'Section B Q7(b)(i) ask wording, read on "choose"; not a selection.'),
 (9, '(b) ‘Allied Irish Bank (AIB) closed 44 of its bank branches in October 2012 and aims to shut one'): ('not-a-task-selection', 'Section B Q8(b) stimulus, read on "one"; not a selection.'),
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
 'subjectId': 'economics', 'year': 2013, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (paper pages 10-12 are blank; scheme pages 1-4 are the SEC cover (in Irish, Gnáthleibhéal, although the scheme is the English one), the note on published schemes, the title page and the support notes with the index, and pages 39-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 76 printed asks (15 Section A + 61 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2013_ol.py). Three cards cover more than one printed ask because the scheme prices them together: Section A Q2(i)-(iv), Section B Q1(b)(ii)-(iii) and Q2(a)(i)-(iii).',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2013-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
