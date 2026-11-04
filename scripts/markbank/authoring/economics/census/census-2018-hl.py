"""Write the independent 2018 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; its Summary of Mark Allocations
(scheme p5, printed 3) agrees with every one. There is no 2018 Higher Irish review, so
nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2018/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2018/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2018-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [6], [T('a', 8, 'sa-q1-a', '2-0'), T('b', 8, 'sa-q1-b', '2-0')],
  'a 8: 4 + 4, two of the three printed statements; b 2 @ 4 (2 + 2) two characteristics from seven.',
  'The perfectly competitive firm as a price taker is Market Structures (2-0).')
q(2, [2], [7], [T('all', 16, 'sa-q2', '3-3')],
  '2 @ 8 (4 + 4) two effects from nine. The (i)/(ii) are ruled answer slots.',
  'The effects of a rise in interest rates are Monetary Policy & Inflation (3-3).')
q(3, [2], [7], [T('all', 16, 'sa-q3', '4-2')],
  '12 + 4 beside the one printed explanation: one card, one row at 16.',
  'A customs union is International Trade & Competitiveness (4-2).')
q(4, [3], [7], [T('a', 10, 'sa-q4-a', '1-5'), T('b', 6, 'sa-q4-b', '1-5')],
  'a 10 the law; b 6 (2 + 4) printed beside the answer and its reason together, without saying which earns which: questionTotal, unpriced rows.',
  'The law of diminishing marginal returns is Costs of Production, Revenue & Profit (1-5).')
q(5, [3], [8], [T('all', 16, 'sa-q5', '3-0')],
  'Four TRUE/FALSE ticks, 2 @ 6 and 2 @ 2 (the scheme prints 2 x 6, 2 x 2) without tying a price to a statement: one card, the four ticks claimed at 6, 6, 2, 2.',
  'Double counting, injections, GDP and transfer payments are National Income (3-0).')
q(6, [3], [8], [T('all', 17, 'sa-q6', '3-1')],
  '1 @ 5 and 3 @ 4 over the four canons: one card, claimed at 5, 4, 4, 4.',
  'Adam Smith’s canons of taxation are Fiscal Policy & the Budget (3-1).')
q(7, [4], [8, 9], [T('a', 12, 'sa-q7-a', '3-1'), T('b', 5, 'sa-q7-b', '3-1')],
  'a 2 @ 6 (3 + 3) two policies from the printed list; b 1 x 5 one challenge from five.',
  'Policies to reduce income inequality are Fiscal Policy & the Budget (3-1).')
q(8, [4], [9], [T('all', 17, 'sa-q8', '2-1')],
  '6 + 6 + 5 (6: 3+3, 6: 3+3, 5: 3+2) over three consequences from five: one card, claimed at 6, 6, 5. The (i)-(iii) are ruled answer slots.',
  'Raising the retirement age is The Labour Market (2-1); its effects on revenue and pension spending are also Fiscal Policy & the Budget (3-1).',
  also=['3-1'])
q(9, [5], [10], [T('a', 8, 'sa-q9-a', '2-0'), T('b', 9, 'sa-q9-b', '2-0')],
  'a 8 the definition; b 3 x 3 three conditions from three. The (i)-(iii) are ruled answer slots.',
  'Price discrimination is Market Structures (2-0).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [6], [11, 12, 13],
  [T('a/i', 10, 'sb-q1-a-i', '1-1'), T('a/ii', 15, 'sb-q1-a-ii', '1-0'),
   T('b/i', 13, 'sb-q1-b-i', '1-0'), T('b/ii', 6, 'sb-q1-b-ii', '1-2'), T('b/iii', 12, 'sb-q1-b-iii', '1-1'),
   T('b/iv', 4, 'sb-q1-b-iv', '1-1'), T('c/i', 6, 'sb-q1-c-i', '1-5'), T('c/ii', 9, 'sb-q1-c-ii', '1-1')],
  'Eight tasks totalling 75. a(i) 5 + 5 movement along and shift; a(ii) diagram 9 (9 x 1, the nine labels the scheme marks) + explanation 6; hidden solution diagram. b(i) diagram 13: six labels 6 x 1, vertical S/C at 400 units 2, five points on D/C 5 x 1; hidden solution diagram. b(ii) 6; b(iii) 2 @ 6; b(iv) 2 + 2 the two areas. c(i) 6 €24,000; c(ii) 9 graded over four printed paragraphs (unpriced rows).',
  'Movements along and shifts in demand, consumer surplus and total revenue are The Consumer (1-1); equilibrium and a surplus are The Market Economy (1-0); a fixed-capacity supply curve is The Firm (Supply) (1-2); total revenue at a fixed price is Costs of Production, Revenue & Profit (1-5).')
q('B2', [7], [14, 15, 16, 17],
  [T('a/i', 6, 'sb-q2-a-i', '2-0'), T('a/ii', 24, 'sb-q2-a-ii', '2-0'),
   T('b/i', 17, 'sb-q2-b-i', '2-0'), T('b/ii', 8, 'sb-q2-b-ii', '2-0'),
   T('c/i', 10, 'sb-q2-c-i', '2-0'), T('c/ii', 10, 'sb-q2-c-ii', '1-3')],
  'Six tasks totalling 75. a(i) 6; a(ii) 4 @ 6 (3 + 3), two advantages (2 x 6) and two disadvantages (2 x 6): two heading rows. b(i) diagram 9 (9 x 1) + explanation 8 (4 @ 2) from five; hidden solution diagram. b(ii) 8 graded over three printed paragraphs (unpriced rows). c(i) 2 x 5 (2 + 3) from three; c(ii) 2 x 5 (2 + 3) from four.',
  'Oligopoly, the kinked demand curve and collusion are Market Structures (2-0); measures against anti-competitive practice are Government Intervention (1-3).')
q('B3', [7], [18, 19, 20, 21],
  [T('a/i', 5, 'sb-q3-a-i', '1-5'), T('a/ii', 8, 'sb-q3-a-ii', '1-5'), T('a/iii', 8, 'sb-q3-a-iii', '1-5'),
   T('a/iv', 4, 'sb-q3-a-iv', '1-5'), T('b/i', 5, 'sb-q3-b-i', '1-4'), T('b/ii', 10, 'sb-q3-b-ii', '1-4'),
   T('b/iii', 10, 'sb-q3-b-iii', '1-4'), T('c/i', 7, 'sb-q3-c-i', '4-2'), T('c/ii', 18, 'sb-q3-c-ii', '1-4')],
  'Nine tasks totalling 75. a(i) 5; a(ii) graph 8: seven MC points x 1 and the label 1 (hidden solution table and graph); a(iii) 2 + 2 indicating the level and 4 the explanation; a(iv) 4 €35. b(i) 5; b(ii) 10 graded over three printed paragraphs (unpriced rows); b(iii) 2 x 5 (2 + 3) from seven. c(i) 7; c(ii) 2 x 9 graded, two of the three printed explanations.',
  'Marginal cost and profit maximisation are Costs of Production, Revenue & Profit (1-5); price elasticity of supply and of demand are Elasticity (1-4); a fall in sterling’s value is International Trade & Competitiveness (4-2).')
q('B4', [8], [22, 23, 24, 25, 26],
  [T('a/i', 8, 'sb-q4-a-i', '2-1'), T('a/ii', 12, 'sb-q4-a-ii', '2-1'),
   T('b/i', 9, 'sb-q4-b-i', '1-5'), T('b/ii', 14, 'sb-q4-b-ii', '1-5'), T('b/iii', 7, 'sb-q4-b-iii', '1-5'),
   T('c/i', 10, 'sb-q4-c-i', '2-1'), T('c/ii', 10, 'sb-q4-c-ii', '2-1'), T('c/iii', 5, 'sb-q4-c-iii', '2-1')],
  'Eight tasks totalling 75. a(i) 8; a(ii) 2 x 6 (3 + 3) from four. b(i) 9; b(ii) 2 x 7 (3 + 4) from eleven; b(iii) 1 x 7 (3 + 4) one disadvantage from four. c(i) 5 + 5 occupational and geographic; c(ii) 2 x 5 (2 + 3) from seven; c(iii) 5 (2 + 3) one measure from eight.',
  'Labour productivity and the mobility of labour are The Labour Market (2-1); economies of scale are Costs of Production, Revenue & Profit (1-5), the stem’s globalisation Globalisation (4-1).',
  also=['4-1'])
q('B5', [8], [27, 28, 29, 30, 31, 32],
  [T('a/i', 10, 'sb-q5-a-i', '3-1'), T('a/ii', 10, 'sb-q5-a-ii-monetary', '3-3'), T('a/ii', 10, 'sb-q5-a-ii-fiscal', '3-1'),
   T('b/i', 5, 'sb-q5-b-i', '3-1'), T('b/ii', 15, 'sb-q5-b-ii', '3-1'), T('b/iii', 5, 'sb-q5-b-iii', '1-3'),
   T('c/i', 6, 'sb-q5-c-i', '3-1'), T('c/ii', 12, 'sb-q5-c-ii', '3-1'),
   T('c/iii', 12, 'sb-q5-c-iii-no', '3-1'), T('c/iii', 12, 'sb-q5-c-iii-yes', '3-1')],
  'Eight tasks, ten routes; 75 with the (a)(ii) and (c)(iii) choices counted once. a(i) 5 + 5 fiscal and monetary policy; a(ii) 2 x 5 (2 + 3) on monetary policy OR fiscal policy: the scheme lists each separately, so two routes. b(i) 5; b(ii) 3 x 5 from seven; b(iii) 5 (2 + 3) from four. c(i) 6; c(ii) 2 x 6 (3 + 3) from seven; c(iii) 2 x 6 (3 + 3): the scheme credits NO and YES with different lists, so two stance routes.',
  'Fiscal policy, indirect taxes and budget deficits are Fiscal Policy & the Budget (3-1); monetary policy and the Eurozone are Monetary Policy & Inflation (3-3); non-tax interventions in consumer behaviour are Government Intervention (1-3).')
q('B6', [9], [33, 34, 35, 36, 37, 38],
  [T('a/i', 15, 'sb-q6-a-i', '3-2'), T('a/ii', 15, 'sb-q6-a-ii', '3-2'),
   T('b', 25, 'sb-q6-b', '4-1'), T('c', 20, 'sb-q6-c', '4-0')],
  'Four tasks totalling 75. a(i) 3 x 5 (2 + 3) from five; a(ii) 3 x 5 (2 + 3) from nine. b 7 + 6 + 6 + 6, two points in favour and two against (1 @ 7 and 3 @ 6 in the summary), not tied to a side: one menu of both lists claimed at 7, 6, 6, 6. c 4 @ 5 (2 + 3), two benefits (2 x 5) and two challenges (2 x 5): two heading rows.',
  'Migration and its consequences are Employment & Unemployment (3-2); the Single European Market is Globalisation (4-1); development aid for LDCs is Growth & Development (4-0).')
q('B7', [9], [39, 40, 41, 42, 43],
  [T('a/i', 5, 'sb-q7-a-i', '3-5'), T('a/ii', 5, 'sb-q7-a-ii', '3-2'), T('a/iii', 5, 'sb-q7-a-iii', '3-3'),
   T('a/iv', 5, 'sb-q7-a-iv', '3-1'), T('b', 25, 'sb-q7-b', '3-4'),
   T('c/i', 18, 'sb-q7-c-i', '3-1'), T('c/ii', 12, 'sb-q7-c-ii', '3-1')],
  'Seven tasks totalling 75. a 4 x 5 (2 + 1 + 2), each area priced 5 as an approximate figure, an accurate trend and a comment, over the scheme’s heading and points for that area (unpriced rows). b 7 + 6 + 6 + 6, minimum of two for citizens and two for the banking industry, not tied to a side: one menu of both lists claimed at 7, 6, 6, 6. c(i) 3 x 6 (3 + 3) from seven; c(ii) 2 x 6 (3 + 3) from six.',
  'Growth is Economic Growth (3-5), employment Employment & Unemployment (3-2), inflation Monetary Policy & Inflation (3-3) and the national debt and capital spending Fiscal Policy & the Budget (3-1); banking regulation is Financial Sector (3-4).')
q('B8', [10], [44, 45, 46, 47, 48, 49],
  [T('a/i', 5, 'sb-q8-a-i', '3-0'), T('a/ii', 6, 'sb-q8-a-ii', '3-0'), T('a/iii', 3, 'sb-q8-a-iii', '3-0'),
   T('a/iv', 6, 'sb-q8-a-iv', '3-0'), T('b', 25, 'sb-q8-b', '4-1'),
   T('c/i', 15, 'sb-q8-c-i', '0-2'), T('c/ii', 15, 'sb-q8-c-ii', '0-2')],
  'Seven tasks totalling 75. a(i) 5 100,000; a(ii) 6 net exports 20,000; a(iii) 3 savings 50,000; a(iv) 6 the multiplier 1.25 (workings printed as fractions; hidden crop). b 7 + 6 + 6 + 6, two benefits and two challenges (1 @ 7 and 3 @ 6), not tied to a side: one menu claimed at 7, 6, 6, 6. c(i) 3 x 5 (2 + 3) from five; c(ii) 3 @ 5 (2 + 3), one measure each for individuals, firms and the government: three heading rows.',
  'The national income identity, net exports, savings and the multiplier are National Income (3-0); FDI is Globalisation (4-1); protecting the environment and carbon emissions are Sustainability (0-2).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
}
PAGE_SEL = {
 (3, '(b) Does this law apply in the short run or in the long run? Explain your answer.'): ('answer-classification', 'Section A Q4(b) short run or long run is the answer (the short run only); one card.'),
 (3, '5. Read each statement below and indicate if the statement is TRUE or FALSE.'): ('answer-classification', 'Section A Q5 four objective ticks; one card, the four claimed at 6, 6, 2, 2.'),
 (8, '(iii) Suggest one measure which could be considered to address any factor'): ('not-a-task-selection', 'Section B Q4(c)(iii) "any factor identified in (ii)" points back to the student’s own answer; one menu of measures.'),
 (8, 'the Government’s monetary policy or fiscal policy in Ireland.'): ('finite-route', 'Section B Q5(a)(ii) monetary policy OR fiscal policy: the scheme lists each separately, so two routes.'),
 (9, '(b) Discuss the economic arguments for and against Ireland being a member of the'): ('not-a-task-selection', 'Section B Q6(b) "for and against" names both sides of one discussion; one menu of both lists, two of each.'),
 (9, 'infrastructural projects) by the Irish government may conflict with any two'): ('finite-route', 'Section B Q7(c)(ii) any two other objectives: one card, a menu of six.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

tasks = [t for x in Q for t in x['tasks']]
for x in Q:
    total = sum(t['marks'] for t in x['tasks'] if not t['cardId'].endswith(('-no', '-fiscal')))
    want = 75 if x['n'].startswith('B') else (16 if int(x['n']) <= 5 else 17)
    assert total == want, (x['n'], total, want)
draft = {
 'subjectId': 'economics', 'year': 2018, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 53)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 52 scheme pages (scheme pages 1-5 are the SEC cover, the note on published schemes, the title page, the notes and index and the Summary of Mark Allocations, which agrees with every tariff here; scheme pages 50-52 and paper pages 11-12 are blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 70 printed asks (13 Section A + 57 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2018_hl.py). Descending ladders over a list (Section A Q5, Q6 and Q8; Section B Q6(b), Q7(b) and Q8(b)) are one card claimed at the printed steps. Routes: Section B Q5(a)(ii) monetary OR fiscal policy and Q5(c)(iii) NO / YES, each credited with its own list.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2018-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
