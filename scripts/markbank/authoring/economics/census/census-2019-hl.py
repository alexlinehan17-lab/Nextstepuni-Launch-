"""Write the independent 2019 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again. The Atlas numbers the Section B
questions B1-B8, so they are keyed that way here. Every tariff is the scheme's
printed cell; the scheme's own Summary of Mark Allocations (scheme p5) agrees
with every one. There is no 2019 Higher Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2019/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2019/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2019-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [6], [T('a', 6, 'sa-q1-a', '1-1'), T('b', 10, 'sa-q1-b', '1-1')],
  'a 6 (3 + 3) the equi-marginal principle. b 10 MU of the 7th orange = 5 utils (the working is printed as fractions; hidden crop).',
  'The equi-marginal principle of consumer behaviour is The Consumer (1-1).')
q(2, [2], [6], [T('all', 16, 'sa-q2', '2-1')],
  'Four TRUE/FALSE ticks at 4 @ 4, one card with a row per statement (completed table hidden until reveal).',
  'Derived demand for labour, the Live Register, cyclical unemployment and the backward-bending labour supply curve are The Labour Market (2-1).')
q(3, [2], [6], [T('all', 16, 'sa-q3', '4-0')],
  '2 @ 8 graded: economic development and economic growth, two required headings at 8.',
  'Development against growth is Growth & Development (4-0).')
q(4, [3], [7], [T('all', 16, 'sa-q4', '0-0')],
  '2 @ 8: any two of the scheme’s six headed contributions. The (i)/(ii) are ruled answer slots, not parts.',
  'The contributions of an economist to economic thought are Economics as a Way of Thinking (0-0).')
q(5, [3], [7], [T('i', 8, 'sa-q5-i', '2-0'), T('ii', 3, 'sa-q5-ii', '2-0'), T('iii', 5, 'sa-q5-iii', '2-0')],
  'i 4 @ 2 the four labels; ii 3 @ 1 P1, C1, Q1; iii 2 (normal profit only) + 3 (AR = AC). 16.',
  'Long-run equilibrium in imperfect competition is Market Structures (2-0).')
q(6, [3], [8], [T('all', 17, 'sa-q6', '4-2')],
  'One cell 11 + 6 beside the two definitions without naming which earns which: one card, unpriced rows.',
  'A free trade area against a customs union is International Trade & Competitiveness (4-2).')
q(7, [4], [8], [T('a', 9, 'sa-q7-a', '3-1'), T('b', 8, 'sa-q7-b', '3-1')],
  'a 5 + 4 beside the two ticks (70% debt-to-GDP, 6% unemployment) without naming which earns which: one card for (a)(i)-(ii), unpriced rows. b 4 + 4 one trend explanation per indicator.',
  'The debt-to-GDP ratio and the unemployment rate as indicators of the economy’s position are read here as Fiscal Policy & the Budget (3-1).')
q(8, [4], [8], [T('all', 17, 'sa-q8', '3-1')],
  'Advantages 1 @ 9 then 1 @ 4 (graded) from five headings; disadvantage 4 from two. 17. The (i)/(ii) are ruled answer slots.',
  'Raising the threshold for the higher income tax rate is Fiscal Policy & the Budget (3-1).')
q(9, [5], [9], [T('a', 13, 'sa-q9-a', '2-1'), T('b', 4, 'sa-q9-b', '2-1')],
  'a 1 @ 9 then 1 @ 4 (graded) from six headings; b 4 one measure from seven. 17. The (i)/(ii) are ruled answer slots.',
  'Older workers, the labour force and extended working lives are The Labour Market (2-1); the scheme’s reasons include income tax revenue and pension spending, so the question is also Fiscal Policy & the Budget (3-1).',
  also=['3-1'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [6], [10, 11, 12, 13],
  [T('a/i', 10, 'sb-q1-a-i', '1-1'), T('a/ii', 15, 'sb-q1-a-ii', '1-1'),
   T('b/i', 10, 'sb-q1-b-i', '1-0'), T('b/ii', 10, 'sb-q1-b-ii', '1-0'), T('b/iii', 10, 'sb-q1-b-iii', '1-0'),
   T('c/i', 12, 'sb-q1-c-i', '1-3'), T('c/ii', 8, 'sb-q1-c-ii', '1-3')],
  'Seven tasks totalling 75. a(i) 5 + 5 the two definitions; a(ii) 3 @ 5 (2 + 3) from six bullets. b(i)-(iii) each diagram 5 (D1, S1, S2, price, quantity at 1 each) + explanation 5 (the reason 2, shift, price and quantity 1 each); hidden solution diagrams. c(i) 12 graded off the printed diagram; c(ii) 2 x 4 (2 + 2) from six.',
  'Individual and market demand are The Consumer (1-1); shifts in market equilibrium are The Market Economy (1-0); rent control as a price ceiling is Government Intervention (1-3).')
q('B2', [7], [14, 15, 16],
  [T('a/i', 15, 'sb-q2-a-i', '2-0'), T('a/ii', 5, 'sb-q2-a-ii', '2-0'),
   T('b/i', 20, 'sb-q2-b-i', '2-0'), T('b/ii', 10, 'sb-q2-b-ii', '2-0'),
   T('c/i', 17, 'sb-q2-c-i', '2-0'), T('c/ii', 8, 'sb-q2-c-ii', '1-3')],
  'Six tasks totalling 75. a(i) 3 @ 5 (2 + 3) from five; a(ii) 5 graded. b(i) diagram 11 (11 @ 1) + explanation 9 (9 @ 1, the nine printed bullets); hidden solution diagram. b(ii) 5 + 5 (2 + 3) monopoly and perfect competition. c(i) 1 @ 9 then 2 @ 4 from six, an example required in each; c(ii) 2 x 4 from four.',
  'Monopoly, price discrimination and large-scale firms are Market Structures (2-0); regulation of anti-competitive behaviour is Government Intervention (1-3).')
q('B3', [7], [17, 18, 19],
  [T('a/i', 5, 'sb-q3-a-i', '1-4'), T('a/ii', 20, 'sb-q3-a-ii', '1-4'),
   T('b/i', 10, 'sb-q3-b-i', '1-4'), T('b/ii', 16, 'sb-q3-b-ii', '1-4'), T('b/iii', 4, 'sb-q3-b-iii', '1-4'),
   T('c/i', 16, 'sb-q3-c-i', '1-4'), T('c/ii', 4, 'sb-q3-c-ii', '1-4')],
  'Seven tasks totalling 75. a(i) 5; a(ii) 2 @ 6 then 2 @ 4 from eight, an example required in each. b(i) 5 + 5 (2 + 3) for each consumer group; b(ii) diagrams 2 @ 6 (2 + 2 + 2) + explanations 2 + 2 (hidden solution diagrams); b(iii) 2 @ 2. c(i) calculation 12 (CED +2.43, working printed as fractions, hidden crop) + explanation 4 graded; c(ii) 4 graded.',
  'Price, cross and the uses of elasticity are Elasticity (1-4).')
q('B4', [8], [20, 21, 22],
  [T('a/i', 20, 'sb-q4-a-i', '1-5'), T('a/ii', 10, 'sb-q4-a-ii', '2-1'),
   T('b/i', 7, 'sb-q4-b-i', '1-5'), T('b/ii', 6, 'sb-q4-b-ii', '1-5'), T('b/iii', 3, 'sb-q4-b-iii', '1-5'),
   T('b/iv', 4, 'sb-q4-b-iv', '1-5'), T('c/i', 15, 'sb-q4-c-i', '2-1'), T('c/ii', 10, 'sb-q4-c-ii', '2-1')],
  'Eight tasks totalling 75. a(i) any two of three pairs: the scheme prices four definitions 2 @ 6 and 2 @ 4 without tying either price to a pair or term: one menu of its six definitions, claim 4, steps 6, 6, 4, 4 (the 2021 HL Q12(a)(ii) layout); a(ii) 2 @ 5 (2 + 3) from six. b(i) 7 ATC 400; b(ii) 6 TC 900; b(iii) 3 MC 450; b(iv) 4 two units (MC = MR = 100). c(i) 3 @ 5 (2 + 3) from six; c(ii) 2 @ 5 (2 + 3) from six.',
  'Average and marginal cost and the cost table are Costs of Production, Revenue & Profit (1-5); the marginal revenue product of labour and skills shortages are The Labour Market (2-1).')
q('B5', [9], [23, 24, 25, 26],
  [T('a/i', 10, 'sb-q5-a-i', '3-4'), T('a/ii', 20, 'sb-q5-a-ii', '3-4'), T('b', 20, 'sb-q5-b', '3-3'),
   T('c/i', 6, 'sb-q5-c-i', '3-1'), T('c/ii', 7, 'sb-q5-c-ii', '3-1'), T('c/iii', 12, 'sb-q5-c-iii', '3-1')],
  'Six tasks totalling 75. a(i) 2 @ 5 (2 + 3) from seven; a(ii) 4 @ 5 (2 + 3) beside the four printed lists (advantages and disadvantages, for the banking industry and for consumers), the four heads the ask names: one heading row each at 5. b 4 @ 4 (2 + 2) from six, + 4 printed beneath it beside the scheme’s note that answers must be linked to the current economic climate. c(i) 6; c(ii) 7; c(iii) 2 @ 6 (3 + 3) from five.',
  'Money and electronic money are Financial Sector (3-4); the ECB interest rate is Monetary Policy & Inflation (3-3); the budget surplus, the national debt and government objectives are Fiscal Policy & the Budget (3-1).')
q('B6', [9], [27, 28, 29],
  [T('a/i', 8, 'sb-q6-a-i', '3-3'), T('a/ii', 8, 'sb-q6-a-ii', '3-3'), T('a/iii', 9, 'sb-q6-a-iii', '3-3'),
   T('b/i', 10, 'sb-q6-b-i', '3-3'), T('b/ii', 12, 'sb-q6-b-ii', '3-3'), T('b/iii', 8, 'sb-q6-b-iii', '3-3'),
   T('c', 20, 'sb-q6-c', '4-2')],
  'Seven tasks totalling 75. a(i) 8 graded over seven printed steps (unpriced rows); a(ii) 2 @ 4 nominal and real wage; a(iii) 9 graded over the three printed answers (unpriced rows). b(i) 5 + 5 (2 + 3) demand-pull and cost-push; b(ii) 3 @ 4 (2 + 2) from seven; b(iii) 8 graded over four printed steps (unpriced rows). c 4 @ 5 (2 + 3) from eight.',
  'Price indices, real wages, inflation and deflation are Monetary Policy & Inflation (3-3); international competitiveness is International Trade & Competitiveness (4-2).')
q('B7', [10], [30, 31, 32],
  [T('a/i', 14, 'sb-q7-a-i', '3-0'), T('a/ii', 16, 'sb-q7-a-ii', '3-0'),
   T('b/i', 5, 'sb-q7-b-i', '3-0'), T('b/ii', 5, 'sb-q7-b-ii', '3-0'), T('b/iii', 9, 'sb-q7-b-iii', '3-0'),
   T('b/iv', 6, 'sb-q7-b-iv', '3-0'), T('c/i', 5, 'sb-q7-c-i', '3-0'), T('c/ii', 15, 'sb-q7-c-ii', '3-0')],
  'Eight tasks totalling 75. a(i) 2 @ 7 graded from five; a(ii) 2 @ 8 graded from nine. b(i) 5; b(ii) 5 MPS 0.4; b(iii) calculation 5 (multiplier 1.25, printed as fractions, hidden crop) + explanation 4; b(iv) 6 €40bn. c(i) 5; c(ii) 3 @ 5 (2 + 3) from five.',
  'National income statistics, the multiplier and the shadow economy are National Income (3-0).')
q('B8', [11], [33, 34, 35],
  [T('a/i', 10, 'sb-q8-a-i', '3-1'), T('a/ii', 15, 'sb-q8-a-ii-yes', '3-1'), T('a/ii', 15, 'sb-q8-a-ii-no', '3-1'),
   T('b/i', 15, 'sb-q8-b-i', '3-1'), T('b/ii', 15, 'sb-q8-b-ii', '3-1'),
   T('c/i', 6, 'sb-q8-c-i', '3-1'), T('c/ii', 14, 'sb-q8-c-ii', '3-1')],
  'Seven routes; 75 with the (a)(ii) stance counted once. a(i) 5 + 5 (4 + 1) each tax with an example; a(ii) 3 @ 5 (2 + 3): the scheme credits YES and NO with different lists, so two stance routes. b(i) 3 @ 5 (2 + 3) from five; b(ii) 3 @ 5 (2 + 3) from four. c(i) 6 graded; c(ii) 2 @ 7 (4 + 3) from eight.',
  'Progressive and regressive taxes, carbon tax, overspending, corporation tax and a just social policy are Fiscal Policy & the Budget (3-1).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 'There is no examination material on this page': ('not-a-task-selection', 'Blank back page.'),
}
PAGE_SEL = {
 (2, '2. Indicate by means of a tick () whether each of the following statements is TRUE or FALSE.'): ('answer-classification', 'Section A Q2 four objective ticks; one card, a row per statement at 4.'),
 (3, '(iii) State whether or not the firm is earning supernormal profits. Give a reason for your'): ('answer-classification', 'Section A Q5(iii) the scheme’s answer is normal profit only (2) with its reason (3); one card.'),
 (5, '(b) Suggest one measure which the government or firms could take to support extended'): ('not-a-task-selection', 'Section A Q9(b) "government or firms" names who may act, not a choice of routes; one menu.'),
 (7, '(ii) Outline four factors that affect the PED for a good or service, providing examples'): ('not-a-task-selection', 'Section B Q3(a)(ii) "four factors": a count, read by the DIRECTIVE pattern on "four"; one menu.'),
 (8, '(ii) Outline measures which the government and / or firms could take to address'): ('not-a-task-selection', 'Section B Q4(c)(ii) "government and / or firms" names who may act; one menu.'),
 (8, '4. (a) (i) In the case of any two of the following three pairs, distinguish between the'): ('finite-route', 'Section B Q4(a)(i) any two of three pairs: one card, the six definitions as one menu claimed four times at 6, 6, 4, 4.'),
 (11, '(i) One of the government’s objectives is to achieve a just social policy.'): ('not-a-task-selection', 'Section B Q8(c)(i) stimulus, read on "one of"; not a selection.'),
 (11, '(ii) Ireland’s corporation tax rate of 12.5% is one of the lowest in the EU.'): ('not-a-task-selection', 'Section B Q8(b)(ii) stimulus, read on "one of"; not a selection.'),
 (11, '(ii) Outline measures which the government and/or firms could consider to address'): ('not-a-task-selection', 'Section B Q8(c)(ii) "government and/or firms" names who may act; one menu.'),
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
 'subjectId': 'economics', 'year': 2019, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 36 scheme pages (scheme pages 1-5 are the cover, notes, index and the Summary of Mark Allocations, which agrees with every tariff here; paper page 12 is blank). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if not x["n"].startswith("B"))} Section A + {sum(len(x["tasks"]) for x in Q if x["n"].startswith("B"))} Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2019_hl.py). Choose-N rule checked: Section B Q4(a)(i) "any two of the following three pairs" is one card; Q8(a)(ii) is two stance routes because the scheme credits each side with its own list.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2019-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
