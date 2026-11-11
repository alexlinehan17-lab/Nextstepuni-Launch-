"""Write the independent 2011 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2011 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2011/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2011/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2011-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once. Section B Q2(c)(i) (one advantage OR one
# disadvantage) and Q7(c)(ii) (agree or disagree with Keynes) are printed
# choices whose scheme credits each side with its own column: one route each,
# the first counted.
ALT = ('-disadvantage', '-disagree')

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [4], [T('i/ii/iii', 16, 'sa-q1', '3-1')],
  'One card for the three names, the paper numbering them (i)-(iii): each missing word at its printed price, 2 + 2, 3 + 3, 3 + 3.',
  'NAMA, the ECB and the IMF are Fiscal Policy & the Budget (3-1), as the EU/IMF programme is filed in earlier reviews; the ECB is also Monetary Policy & Inflation (3-3).', also=['3-3'])
q(2, [2], [4], [T('i/ii/iii', 16, 'sa-q2', '1-0')],
  'One card for the three statements, the paper numbering them (i)-(iii): the 1st correct answer 8, the 2nd and 3rd 4 each.',
  'Free enterprise, mixed and centrally planned economies are The Market Economy (1-0).')
q(3, [2], [4], [T('all', 16, 'sa-q3', '1-3')],
  'One advantage from four and one disadvantage from four on one ladder: 12 + 4.',
  'Third-level fees are Government Intervention (1-3), as 2012 HL files students paying towards their education.')
q(4, [2], [5], [T('a', 13, 'sa-q4-a', '2-0'), T('b', 3, 'sa-q4-b', '2-0')],
  'a the five labels at their printed prices (2, 3, 3, 3, 2); b Q1 3 (hidden solution diagram).',
  'The long-run equilibrium of a firm in perfect competition is Market Structures (2-0).')
q(5, [3], [5], [T('all', 16, 'sa-q5', '4-2')],
  'The four matches the paper leaves open: the 1st and 2nd correct 6 each, the 3rd and 4th 2 each.',
  'Barriers to trade are International Trade & Competitiveness (4-2).')
q(6, [3], [5], [T('all', 17, 'sa-q6', '0-1')],
  'The explanation, any two of its four points at 4; the two circled goods, the 1st correct 5 and the 2nd 4.',
  'An economic good is Scarcity & Choice (0-1).')
q(7, [3], [6], [T('i/ii/iii/iv', 17, 'sa-q7', '1-1')],
  'One card for the four sentences, the paper numbering them (i)-(iv): 6 + 6 + 3 + 2.',
  'The factors influencing consumer demand are The Consumer (Demand) (1-1).')
q(8, [3], [6], [T('all', 17, 'sa-q8', '3-1')],
  'Three aims from thirteen: 9 + 4 + 4.',
  'The government’s economic aims are Fiscal Policy & the Budget (3-1).')
q(9, [3], [6], [T('all', 17, 'sa-q9', '3-0')],
  'The three figures at 3, the two signs at 2 and the answer 4 (hidden working crop).',
  'National income with exports and imports is National Income (3-0).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [7, 8, 9, 10],
  [T('a/i', 22, 'sb-q1-a-i', '2-0'), T('a/ii', 8, 'sb-q1-a-ii', '2-0'), T('b/i-ii', 21, 'sb-q1-b', '2-0'),
   T('c/i', 6, 'sb-q1-c-i', '1-3'), T('c/ii', 6, 'sb-q1-c-ii', '1-3'), T('c/iii', 12, 'sb-q1-c-iii', '1-3')],
  'Six cards for seven asks totalling 75. a(i) the six labels at their printed prices (4, 4, 4, 4, 3, 3); a(ii) P1 and C1 4 each (hidden solution diagram, the paper’s diagram beside the ask). b(i)-(ii) one card, as the scheme prices each barrier stated and explained: 11 + 5 + 5 from nine. c(i) 6 (either definition); c(ii) 6; c(iii) one way for each of any two groups at 6, from each group’s positive and negative effects.',
  'Monopoly, its equilibrium and barriers to entry are Market Structures (2-0); privatisation is Government Intervention (1-3), as earlier reviews file it.')
q('B2', [5], [11, 12, 13],
  [T('a/i-iii', 25, 'sb-q2-a', '1-0'), T('b/i-iii', 20, 'sb-q2-b', '1-0'), T('c/i', 6, 'sb-q2-c-i-advantage', '1-0'),
   T('c/i', 6, 'sb-q2-c-i-disadvantage', '1-0'), T('c/ii', 12, 'sb-q2-c-ii', '1-2'), T('c/iii', 12, 'sb-q2-c-iii', '2-2')],
  'Five cards for eight asks totalling 75. a(i)-(iii) one card, the scheme pricing one diagram: each curve’s four points at 2, the four labels at 1, PE and QE 3 + 2 (hidden solution graph, the paper’s table beside the ask). b(i)-(iii) one card, the three answers for each of the two statements: the curve 3, the direction 3 and the explanation 2 + 2. c(i) one advantage OR one disadvantage is a printed choice and the scheme credits each with its own column, 6: one route each, counted once; c(ii) 2 at 6 from five; c(iii) 2 at 6 from eight.',
  'Demand, supply and shifts in the umbrella market and the new motorways are The Market Economy (1-0); Irish Rail’s actions to raise demand are The Firm (Supply) (1-2); the advantages of public transport are externalities, Market Failure (2-2), as 2011 HL files public transport.')
q('B3', [6], [14, 15, 16],
  [T('a/i', 6, 'sb-q3-a-i', '0-1'), T('a/ii', 10, 'sb-q3-a-ii', '1-5'), T('a/iii', 9, 'sb-q3-a-iii', '1-5'),
   T('b/i', 9, 'sb-q3-b-i', '3-1'), T('b/ii', 16, 'sb-q3-b-ii', '2-1'), T('c/i', 5, 'sb-q3-c-i', '2-1'),
   T('c/ii', 10, 'sb-q3-c-ii', '2-1'), T('c/iii', 10, 'sb-q3-c-iii', '2-1')],
  'Eight tasks totalling 75. a(i) 6; a(ii) each definition 5 (4 + 1); a(iii) each cost 3. b(i) the public sector 3 + an example 2, the private sector 2 + an example 2; b(ii) two effects at 4 for businesses from five and two for government finance from five. c(i) 5; c(ii) 2 at 5 from five; c(iii) 2 at 5 from five.',
  'Capital as a factor of production is Scarcity & Choice (0-1); fixed and variable costs are Costs of Production, Revenue & Profit (1-5); the public and private sectors are Fiscal Policy & the Budget (3-1); falling wages and the minimum wage are The Labour Market (2-1), and the national minimum wage also Government Intervention (1-3).', also=['1-3'])
q('B4', [6], [17, 18, 19],
  [T('a/i', 14, 'sb-q4-a-i', '4-2'), T('a/ii', 7, 'sb-q4-a-ii', '4-2'), T('a/iii', 4, 'sb-q4-a-iii', '4-2'),
   T('b/i', 5, 'sb-q4-b-i', '4-2'), T('b/ii', 15, 'sb-q4-b-ii', '4-2'), T('c/i', 6, 'sb-q4-c-i', '4-2'),
   T('c/ii', 12, 'sb-q4-c-ii', '4-2'), T('c/iii', 12, 'sb-q4-c-iii', '4-2')],
  'Eight tasks totalling 75. a(i) each explanation 5 (3 + 2) + an example 2; a(ii) 7 (hidden working crop, the paper’s table beside the ask); a(iii) deficit 2 + why 2. b(i) 5; b(ii) 3 at 5 from eight. c(i) 6; c(ii) 2 at 6 from four; c(iii) 2 at 6 from six.',
  'Visible and invisible trade, the balance of trade, the small open economy and tourism are International Trade & Competitiveness (4-2).')
q('B5', [7], [20, 21, 22],
  [T('a/i', 13, 'sb-q5-a-i', '3-1'), T('a/ii', 12, 'sb-q5-a-ii', '3-1'), T('b/i', 10, 'sb-q5-b-i', '3-1'),
   T('b/ii', 10, 'sb-q5-b-ii', '3-1'), T('c/i', 6, 'sb-q5-c-i', '3-1'), T('c/ii', 6, 'sb-q5-c-ii', '3-0'),
   T('c/iii', 6, 'sb-q5-c-iii', '3-1'), T('c/iv', 12, 'sb-q5-c-iv', '3-1')],
  'Eight tasks totalling 75. a(i) the current budget deficit 5 + current income 4 + current spending 4; a(ii) two income examples at 3 from eight + two spending examples at 3 from seven. b(i) 2 at 5 from five; b(ii) 2 at 5 from four. c(i) 6; c(ii) 6; c(iii) 6 from four; c(iv) 2 at 6 from seven.',
  'The current budget, water charges and the national debt are Fiscal Policy & the Budget (3-1); GDP is National Income (3-0).')
q('B6', [7], [23, 24, 25],
  [T('a/i', 6, 'sb-q6-a-i', '3-0'), T('a/ii', 12, 'sb-q6-a-ii', '3-0'), T('a/iii', 7, 'sb-q6-a-iii', '3-0'),
   T('b/i', 12, 'sb-q6-b-i', '1-0'), T('b/ii', 5, 'sb-q6-b-ii', '1-0'), T('b/iii', 8, 'sb-q6-b-iii', '1-0'),
   T('c/i', 12, 'sb-q6-c-i', '3-1'), T('c/ii', 8, 'sb-q6-c-ii', '3-1'), T('c/iii', 5, 'sb-q6-c-iii', '3-1')],
  'Nine tasks totalling 75. a(i) 6; a(ii) 2 at 6 from six; a(iii) the working 1 + 1 + 1 + 1 and the answer 3. b(i) 2 at 6 from six; b(ii) 5 from three; b(iii) 2 at 4 from three. c(i) infrastructure 6 (its explanation 3 and an example 3, as the scheme prices its examples) + opportunity cost 6; c(ii) 2 at 4 from seven; c(iii) 5 from four.',
  'National income, injections and the multiplier are National Income (3-0); falling demand for houses and ghost estates are The Market Economy (1-0), as earlier reviews file residential property prices; infrastructure spending and its opportunity cost are Fiscal Policy & the Budget (3-1), and opportunity cost also Scarcity & Choice (0-1).', also=['0-1'])
q('B7', [8], [26, 27, 28],
  [T('a/i', 10, 'sb-q7-a-i', '3-4'), T('a/ii', 10, 'sb-q7-a-ii', '3-4'), T('a/iii', 5, 'sb-q7-a-iii', '3-4'),
   T('b/i', 7, 'sb-q7-b-i', '3-4'), T('b/ii', 18, 'sb-q7-b-ii', '3-4'), T('c/i', 18, 'sb-q7-c-i', '3-4'),
   T('c/ii', 7, 'sb-q7-c-ii-agree', '0-0'), T('c/ii', 7, 'sb-q7-c-ii-disagree', '0-0')],
  'Six tasks totalling 75. a(i) currency 5 + store of wealth 5; a(ii) 2 at 5 from three; a(iii) 5 from three. b(i) nationalised 5 + a bank 2; b(ii) one effect for each of the three groups at 6. c(i) the three motives at 6; c(ii) agree or disagree is a printed choice and the scheme credits each with its own column: Yes / No 1 + a reason 6: one route each, counted once.',
  'Money, currency, nationalised banks and Keynes’s motives for holding money are Financial Sector (3-4); Keynes and government involvement are Economics as a Way of Thinking (0-0), and government involvement also Government Intervention (1-3).', also=['1-3'])
q('B8', [8], [29, 30, 31, 32],
  [T('a/i', 9, 'sb-q8-a-i', '3-0'), T('a/ii', 4, 'sb-q8-a-ii', '3-5'), T('a/iii', 12, 'sb-q8-a-iii', '3-5'),
   T('b/i', 8, 'sb-q8-b-i', '3-1'), T('b/ii', 12, 'sb-q8-b-ii', '2-1'), T('c/i', 6, 'sb-q8-c-i', '4-0'),
   T('c/ii', 12, 'sb-q8-c-ii', '4-0'), T('c/iii', 12, 'sb-q8-c-iii', '4-0')],
  'Eight tasks totalling 75. a(i) the three words of CSO at 3; a(ii) 4; a(iii) one use for each of the three groups at 4. b(i) 8 from three; b(ii) one effect for each of the two at 6. c(i) 6, 4 + 2 on a ladder; c(ii) 2 at 6 from five; c(iii) 2 at 6 from six.',
  'The CSO is National Income (3-0), as 2016 OL files it; the census and its uses are Economic Growth (3-5); the retirement age is Fiscal Policy & the Budget (3-1) and its effects The Labour Market (2-1), as 2015 HL files them; economic development and aid to LDCs are Growth & Development (4-0).', also=['3-1'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (2, '2. Name the economic system (Free Enterprise, Mixed Economy or Centrally Planned) to which'): ('answer-classification', 'Section A Q2 the economic system is the answer for each statement; one card, three answers.'),
 (2, 'Answer six of the nine short response type questions in the spaces provided:'): ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 (3, '8. One of the economic aims of the Irish Government at present is to reduce Government Current'): ('not-a-task-selection', 'Section A Q8 stem wording, read on "One"; not a selection.'),
 (3, 'Circle only two of these:'): ('finite-route', 'Section A Q6 two of the four goods listed: one card, the two economic goods claimed at 5 and 4.'),
 (3, 'SENTENCE TRUE or FALSE'): ('answer-classification', 'Section A Q7 table head: true or false is the answer for each sentence.'),
 (3, 'Write TRUE or FALSE after each of the following sentences.'): ('answer-classification', 'Section A Q7 true or false is the answer for each sentence; one card, four answers.'),
 (4, '(iii) State and explain one way any two of the following may be affected by the possible'): ('finite-route', 'Section B Q1(c)(iii) any two of three groups: one card claimed twice at 6.'),
 (5, '(b) The demand curve for umbrellas OR the supply curve for umbrellas may shift to the right or to'): ('answer-classification', 'Section B Q2(b) demand or supply, right or left is the answer for each statement; one card.'),
 (5, '(i) Outline one possible economic advantage OR one possible economic disadvantage of'): ('finite-route', 'Section B Q2(c)(i) one advantage OR one disadvantage: the scheme credits each with its own column, so one route each, counted once.'),
 (5, '(i) state whether the demand curve or supply curve will shift;'): ('answer-classification', 'Section B Q2(b)(i) demand or supply curve is the answer; one card with (ii)-(iii).'),
 (5, '(ii) state whether the curve you mention will shift to the right or the left;'): ('answer-classification', 'Section B Q2(b)(ii) right or left is the answer; one card with (i) and (iii).'),
 (6, '(iii) State whether each of the three underlined costs above is an example of a fixed cost or a'): ('answer-classification', 'Section B Q3(a)(iii) fixed or variable is the answer for each cost; one card.'),
 (6, '(iii) State whether the new Balance of Trade is a surplus or deficit and explain your answer.'): ('answer-classification', 'Section B Q4(a)(iii) surplus or deficit is the answer (a deficit); one card.'),
 (6, 'Visible Exports Visible Imports Balance of Trade Surplus or Deficit'): ('not-a-task-selection', 'Section B Q4 table head, read on "or"; not a selection.'),
 (8, '(ii) Keynes favoured Government involvement/participation in an economy. Do you agree'): ('finite-route', 'Section B Q7(c)(ii) agree or disagree: the scheme credits each side with its own column, so one route each, counted once.'),
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
 'subjectId': 'economics', 'year': 2011, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 36 scheme pages (paper pages 9-12 are blank; scheme pages 1-3 are the SEC cover, a blank page and the support notes with the index, and pages 33-36 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part; its cover prints the level in capitals, ORDINARY LEVEL). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 81 printed asks (17 Section A + 64 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2011_ol.py). Section A Q1(i)-(iii), Q2(i)-(iii) and Q7(i)-(iv), and Section B Q1(b)(i)-(ii), Q2(a)(i)-(iii) and Q2(b)(i)-(iii) are one card each, as the scheme prices them together; Section B Q2(c)(i) (advantage OR disadvantage) and Q7(c)(ii) (agree or disagree) are one route for each side the scheme credits, counted once.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2011-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
