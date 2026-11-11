"""Write the independent 2014 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2014 Higher
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2014/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2014/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2014-hl-'
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
  'The definition 8 + one example 8 from three sample responses: one card, two rows.',
  'Opportunity cost is Scarcity & Choice (0-1); the government’s own choices are also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q(2, [2], [5], [T('i', 1, 'sa-q2-i', '1-5'), T('ii', 15, 'sa-q2-ii', '1-5')],
  'i the circled answer (YES) 1; ii the explanation 15.',
  'Marginal and average cost are Costs of Production, Revenue & Profit (1-5).')
q(3, [2], [5], [T('all', 16, 'sa-q3', '3-2')],
  'The definition 10 + one policy measure 6 from two.',
  'Structural unemployment and the policies to reduce it are Employment & Unemployment (3-2).')
q(4, [3], [6], [T('all', 16, 'sa-q4', '1-1')],
  'The explanation 12 + the example 4.',
  'Complementary goods (joint demand) are The Consumer (Demand) (1-1).')
q(5, [3], [6], [T('all', 16, 'sa-q5', '2-0')],
  'Three assumptions from five: the 1st correct answer 6, then 5 + 5.',
  'The assumptions of monopoly are Market Structures (2-0).')
q(6, [3], [6], [T('all', 17, 'sa-q6', '4-2')],
  'Two effects from five: the 1st correct answer 10, the 2nd 7.',
  'The euro’s exchange rate against the dollar is International Trade & Competitiveness (4-2).')
q(7, [3], [7], [T('all', 17, 'sa-q7', '0-1')],
  'Two ways from three: the 1st correct response 10, the 2nd 7.',
  'Enterprise as a factor of production and its return are Scarcity & Choice (0-1).')
q(8, [4], [7], [T('all', 17, 'sa-q8', '3-1')],
  'Two implications from five: the 1st correct response 11, the 2nd 6.',
  'Exiting the EU/IMF/ECB programme, fiscal discipline and the budget are Fiscal Policy & the Budget (3-1); the Troika and FDI are also Globalisation (4-1).', also=['4-1'])
q(9, [4], [8], [T('all', 17, 'sa-q9', '2-2')],
  'Two social costs and two social benefits on one ladder: the 1st correct response 5, the 2nd, 3rd and 4th 4 each: one card.',
  'Social costs and benefits of a public investment are externalities, Market Failure (2-2); weighing them is also Scarcity & Choice (0-1).', also=['0-1'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [9, 10, 11, 12],
  [T('a/i', 13, 'sb-q1-a-i', '1-1'), T('a/ii', 12, 'sb-q1-a-ii', '1-1'),
   T('b/i', 8, 'sb-q1-b-i', '1-2'), T('b/ii', 6, 'sb-q1-b-ii', '1-2'), T('b/iii', 16, 'sb-q1-b-iii', '1-2'),
   T('c/i', 12, 'sb-q1-c-i', '1-0'), T('c/ii', 8, 'sb-q1-c-ii', '1-1')],
  'Seven tasks totalling 75. a(i) the statement 4 + the explanation 9; a(ii) 2 @ 6 from four. b(i) the statement 4 + the diagram 4 (hidden solution diagram); b(ii) 6; b(iii) 2 factors @ 8, each stated and explained with its diagram (hidden solution diagrams). c(i) the diagram 8 + the explanation 4 (hidden solution diagram); c(ii) 2 points @ 4 from three.',
  'Diminishing marginal utility and consumer surplus are The Consumer (Demand) (1-1); the law of supply and shifts in supply are The Firm (Supply) (1-2); a fixed-capacity market’s demand and supply are The Market Economy (1-0).')
q('B2', [5], [13, 14, 15],
  [T('a/i', 13, 'sb-q2-a-i', '2-0'), T('a/ii', 12, 'sb-q2-a-ii', '2-0'),
   T('b/i', 18, 'sb-q2-b-i', '2-0'), T('b/ii', 12, 'sb-q2-b-ii', '2-0'), T('c', 20, 'sb-q2-c', '2-0')],
  'Five tasks totalling 75. a(i) three assumptions from six: the 1st correct answer 5, then 4 + 4; a(ii) perfect competition 6 + imperfect competition 6. b(i) the diagram 10 (hidden solution diagram) + the explanation 8; b(ii) 3 points @ 4. c the market structure 1 + four explanations at 5 + 5 + 5 + 4 from five, with reference to the Irish grocery market.',
  'Imperfect competition, its long-run equilibrium and oligopoly are Market Structures (2-0).')
q('B3', [6], [16, 17],
  [T('a/i', 15, 'sb-q3-a-i', '1-4'), T('a/ii', 15, 'sb-q3-a-ii', '1-4'), T('b', 20, 'sb-q3-b', '1-4'),
   T('c/i', 12, 'sb-q3-c-i', '1-4'), T('c/ii', 13, 'sb-q3-c-ii', '1-4')],
  'Five tasks totalling 75. a(i) the three definitions @ 5; a(ii) 3 factors @ 5 from five. b one part of three asks: the PED working 10 (hidden working crop) + inelastic 2 + the implication for government revenue 8. c(i) 12; c(ii) 13.',
  'Price and income elasticity of demand are Elasticity (1-4); the carbon tax’s yield is also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q('B4', [6], [18, 19, 20, 21, 22],
  [T('a', 20, 'sb-q4-a', '2-1'), T('b/i', 10, 'sb-q4-b-i', '0-1'), T('b/ii', 15, 'sb-q4-b-ii', '1-2'),
   T('c/i', 15, 'sb-q4-c-i', '1-0'), T('c/ii', 15, 'sb-q4-c-ii', '3-4')],
  'Five tasks totalling 75. a the four terms, each explanation 3 + example 2. b(i) 2 characteristics @ 5 from three; b(ii) 3 factors @ 5 from eight. c(i) 3 factors @ 5 from five; c(ii) one impact per category @ 5: households, the banking sector and the government, three heading rows.',
  'Derived demand, transfer earnings, supply price and economic rent are factor incomes, The Labour Market (2-1); land as a factor of production is Scarcity & Choice (0-1); where a firm locates is The Firm (Supply) (1-2); residential property prices are The Market Economy (1-0); mortgage arrears are Financial Sector (3-4).')
q('B5', [7], [23, 24, 25, 26],
  [T('a/i', 5, 'sb-q5-a-i', '3-0'), T('a/ii', 5, 'sb-q5-a-ii', '3-0'), T('a/iii', 5, 'sb-q5-a-iii', '3-0'),
   T('a/iv', 5, 'sb-q5-a-iv', '3-0'), T('b', 20, 'sb-q5-b', '4-1'),
   T('c/i', 12, 'sb-q5-c-i', '3-0'), T('c/ii', 8, 'sb-q5-c-ii', '3-0'), T('c/iii', 15, 'sb-q5-c-iii', '3-0')],
  'Eight tasks totalling 75. a(i)-(iv) each 5, the answer with its working (hidden working crops). b 4 points @ 5 from eleven. c(i) GDP 6 + GNP 6; c(ii) 8, the scheme’s one possible response; c(iii) 3 points @ 5 from six.',
  'The national income identity, the MPC, the MPM, GDP, GNP and the limits of national income statistics are National Income (3-0); multinational companies are Globalisation (4-1).')
q('B6', [7], [27, 28, 29, 30],
  [T('a/i', 20, 'sb-q6-a-i', '3-1'), T('a/ii', 10, 'sb-q6-a-ii', '3-1'), T('b', 20, 'sb-q6-b', '1-3'),
   T('c', 25, 'sb-q6-c', '3-1')],
  'Four tasks totalling 75. a(i) 4 points @ 5 from seven; a(ii) 2 conflicts @ 5 from four. b 2 arguments for @ 5 from six + 2 against @ 5 from five, both required. c four consequences from seven: the 1st correct response 7, the 2nd, 3rd and 4th 6.',
  'The government’s economic aims, their conflicts and austerity are Fiscal Policy & the Budget (3-1); privatisation is Government Intervention (1-3).')
q('B7', [8], [31, 32, 33, 34],
  [T('a/i', 10, 'sb-q7-a-i', '4-0'), T('a/ii', 15, 'sb-q7-a-ii', '4-0'), T('b/i', 15, 'sb-q7-b-i', '4-0'),
   T('b/ii', 10, 'sb-q7-b-ii', '4-0'), T('c/i', 10, 'sb-q7-c-i', '4-2'), T('c/ii', 15, 'sb-q7-c-ii', '4-2')],
  'Six tasks totalling 75. a(i) economic development 5 + economic growth 5; a(ii) 3 points @ 5 from eight. b(i) 3 points @ 5 from seven; b(ii) 2 points @ 5 from six. c(i) 2 benefits @ 5 from four; c(ii) 3 reasons @ 5 from four.',
  'Economic development, LDCs and foreign aid are Growth & Development (4-0); free trade and barriers to it are International Trade & Competitiveness (4-2); the WTO is also Globalisation (4-1).', also=['4-1'])
q('B8', [8], [35, 36, 37],
  [T('a', 20, 'sb-q8-a', '3-1'), T('b/i', 24, 'sb-q8-b-i', '3-1'), T('b/ii', 11, 'sb-q8-b-ii', '3-1'),
   T('c', 20, 'sb-q8-c', '3-1')],
  'Four tasks totalling 75. a the budget deficit 10 + the national debt 10. b(i) the four canons @ 6; b(ii) two principles from five: the 1st correct response 6, the 2nd 5. c 4 points @ 5 from six.',
  'The budget deficit, the national debt, the canons of taxation and the mix of direct and indirect taxes are Fiscal Policy & the Budget (3-1).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (2, '(i) Is this statement true? Circle the correct answer. YES / NO'): ('answer-classification', 'Section A Q2(i) yes or no is the answer (YES); one card.'),
 (5, 'No of Units Consumed 1 2 3 4 5'): ('not-a-task-selection', 'Section B Q1(a) table header, read on "No"; not a selection.'),
 (6, '(i) If the firm wishes to maximise total sales revenue, should it lower or raise the price of the'): ('answer-classification', 'Section B Q3(c)(i) lower or raise is the answer (reduce the price); one card.'),
 (6, 'Is this demand for petrol price elastic or price inelastic? Outline the implication of your answer'): ('answer-classification', 'Section B Q3(b) elastic or inelastic is the answer (inelastic); one card for the part.'),
 (7, '(b) Discuss arguments for and against the privatisation of state assets. (20)'): ('not-a-task-selection', 'Section B Q6(b) "for and against" names both sides, both required: the scheme prices 2 for and 2 against.'),
 (8, '(ii) Outline three reasons why countries might choose to impose barriers to free trade.'): ('not-a-task-selection', 'Section B Q7(c)(ii) ask wording, read on "choose"; not a selection.'),
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
 'subjectId': 'economics', 'year': 2014, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (paper pages 9-12 are blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index, and pages 38-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 54 printed asks (10 Section A + 44 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2014_hl.py). One route per printed ask: Section A Q9’s two social costs and two social benefits share one ladder, and Section B Q3(b)’s three asks are one unnumbered part.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2014-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
