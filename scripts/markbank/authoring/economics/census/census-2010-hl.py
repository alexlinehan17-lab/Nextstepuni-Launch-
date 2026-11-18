"""Write the independent 2010 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. Its cover prints the level in
capitals ("HIGHER LEVEL"), so the scheme file was built with the appenders'
cover check pointed at the file. There is no 2010 Higher Irish review, so
nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2010/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2010/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2010-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once. Section B Q5(b)(i) and (b)(ii) are each
# answered by either of the scheme's two tables, each credited with its own
# effect and explanation (the second headed "The Long run"): one route each,
# the first counted. Section B Q7(c) is a printed choice (the IMF OR the World
# Bank) whose scheme credits each with its own list: one route each, the first
# counted.
ALT = ('-long-run', '-world-bank')

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [3], [T('all', 16, 'sa-q1', '1-0')],
  'Three reasons from seven: 6 + 5 + 5.',
  'Falling prices of land for housing are The Market Economy (1-0), as 2014 HL files residential property prices.')
q(2, [2], [3], [T('all', 16, 'sa-q2', '3-1')],
  'Two measures at 8 (4 + 4) from six.',
  'Government measures to raise consumer spending (taxes, incentives, capital spending) are Fiscal Policy & the Budget (3-1); consumer spending is also National Income (3-0), as 2015 OL files it.', also=['3-0'])
q(3, [2], [4], [T('all', 16, 'sa-q3', '1-4')],
  'The working 12 (its six starred figures at 2, hidden working crop) + the explanation 4, which the scheme does not divide.',
  'Price elasticity of demand is Elasticity (1-4).')
q(4, [2], [4], [T('all', 16, 'sa-q4', '2-0')],
  'The definition 12 + two examples at 2 from seven.',
  'Non-price competition is Market Structures (2-0), as 2024 OL files price and non-price competition.')
q(5, [2], [5], [T('all', 16, 'sa-q5', '0-1')],
  'Three reasons from nine: 6 + 5 + 5.',
  'Entrepreneurship is Scarcity & Choice (0-1), as 2012 HL files it.')
q(6, [3], [6], [T('all', 17, 'sa-q6', '3-0')],
  'The working 5 (1 for each of its five items, hidden working crop) + the meaning of the figure 12.',
  'The multiplier is National Income (3-0).')
q(7, [3], [6], [T('all', 17, 'sa-q7', '3-2')],
  'Two limitations from four: 9 + 8.',
  'The Live Register is Employment & Unemployment (3-2), as 2012 HL and 2012 OL file it.')
q(8, [3], [6], [T('all', 17, 'sa-q8', '2-1')],
  'The meaning 12 + an example 5.',
  'Rent of ability is economic rent, a factor income, The Labour Market (2-1), as 2014 HL files economic rent.')
q(9, [3], [7], [T('all', 17, 'sa-q9', '1-3')],
  'Three arguments from six: 6 + 6 + 5.',
  'Water charges are Government Intervention (1-3), and as a charge on households also Fiscal Policy & the Budget (3-1), as 2015 OL files them.', also=['3-1'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [8, 9, 10],
  [T('a/i', 15, 'sb-q1-a-i', '1-0'), T('a/ii', 7, 'sb-q1-a-ii', '1-0'), T('a/iii', 8, 'sb-q1-a-iii', '1-0'),
   T('b/i', 20, 'sb-q1-b-i', '1-4'), T('b/ii', 10, 'sb-q1-b-ii', '1-4'), T('c', 15, 'sb-q1-c', '1-3')],
  'Six tasks totalling 75. a(i) [15]: the demand curve 5 points at 1 + its label 1, the supply curve the same, the equilibrium point, price and quantity 3 at 1 (hidden solution diagram, the paper’s schedule beside the ask); a(ii) [7]; a(iii) [8]: the new supply curve 5 points at 1 + the new equilibrium point, price and quantity 3 at 1 (the same diagram). b(i) 4 at 5 from nine; b(ii) 10: the minus sign 5, the value 2 and why 3, either reading (price elastic or luxury). c 3 at 5 from four.',
  'Market demand, supply and equilibrium and a shift in supply are The Market Economy (1-0); price elasticity of demand is Elasticity (1-4); actions to cut soft-drink consumption are Government Intervention (1-3), as 2017 OL files obesity measures.')
q('B2', [4], [11, 12, 13],
  [T('a/i', 15, 'sb-q2-a-i', '2-0'), T('a/ii', 10, 'sb-q2-a-ii', '2-0'), T('b/i', 8, 'sb-q2-b-i', '2-0'),
   T('b/ii', 12, 'sb-q2-b-ii', '2-0'), T('c', 30, 'sb-q2-c', '2-0')],
  'Five tasks totalling 75. a(i) 3 at 5 from four; a(ii) 2 at 5 from five. b(i) the definition 6 + an example 2 from two; b(ii) 3 at 4 from six. c the diagram 16 (ten items circled 1 + three circled 2, hidden solution diagram) + price 3 + output 3 + profits 4 and efficiency 4, each part the scheme marks (1) at 1.',
  'Monopoly, price discrimination and the comparison with perfect competition are Market Structures (2-0), as 2015 HL files monopoly and price discrimination.')
q('B3', [5], [14, 15, 16],
  [T('a', 20, 'sb-q3-a', '2-1'), T('b/i', 20, 'sb-q3-b-i', '2-1'), T('b/ii', 10, 'sb-q3-b-ii', '2-1'),
   T('c/i', 15, 'sb-q3-c-i', '3-0'), T('c/ii', 10, 'sb-q3-c-ii', '3-1')],
  'Five tasks totalling 75. a the four terms at 5. b(i) 4 at 5 from nine; b(ii) one advantage 5 from five + one disadvantage 5 from five. c(i) 3 at 5 from six; c(ii) 2 at 5 from five.',
  'Derived demand, MRP, wage drift and cyclical unemployment are The Labour Market (2-1), as 2019 HL files them; the efficiency of labour and the minimum wage are The Labour Market (2-1); the black economy is National Income (3-0), as 2012 HL files it, and measures against it Fiscal Policy & the Budget (3-1).')
q('B4', [5], [17, 18, 19],
  [T('a/i', 10, 'sb-q4-a-i', '3-1'), T('a/ii', 20, 'sb-q4-a-ii', '3-1'), T('b/i', 5, 'sb-q4-b-i', '3-1'),
   T('b/ii', 20, 'sb-q4-b-ii', '3-1'), T('c', 20, 'sb-q4-c', '3-1')],
  'Five tasks totalling 75. a(i) the two terms at 5; a(ii) 5 at 4 from nine (the paper does not say how many). b(i) 5: stating regressive 2 + explaining it 3; b(ii) 2 advantages at 5 from four + 2 disadvantages at 5 from four. c 4 at 5 from eight.',
  'Taxation revenues, the tax base, the characteristics of a good tax, the carbon tax and the national debt are Fiscal Policy & the Budget (3-1), as 2019 HL files the carbon tax.')
q('B5', [6], [20, 21, 22],
  [T('a/i', 10, 'sb-q5-a-i', '3-0'), T('a/ii', 10, 'sb-q5-a-ii', '3-0'),
   T('b/i', 10, 'sb-q5-b-i-prices', '3-0'), T('b/i', 10, 'sb-q5-b-i-long-run', '3-0'),
   T('b/ii', 10, 'sb-q5-b-ii-prices', '3-0'), T('b/ii', 10, 'sb-q5-b-ii-long-run', '3-0'),
   T('c/i', 15, 'sb-q5-c-i', '3-0'), T('c/ii', 20, 'sb-q5-c-ii', '3-0')],
  'Six tasks totalling 75. a(i) 10: 2 + 2 + 2 + 4 under the four figures of the working; a(ii) 10: 3 + 3 + 4 (hidden working crops). b(i) and b(ii) each 10, the effect 4 + its explanation 6, by either of the scheme’s two tables, each credited with its own (the second, The Long run, the opposite effect): one route each, counted once. c(i) 3 at 5 from five (the paper does not say how many); c(ii) 4 at 5 from eleven.',
  'GNP at factor cost, national income, the effect of VAT and subsidies on GNP and national income statistics are National Income (3-0).')
q('B6', [6], [23, 24, 25],
  [T('a/i', 10, 'sb-q6-a-i', '3-4'), T('a/ii', 20, 'sb-q6-a-ii', '3-4'), T('b/i', 15, 'sb-q6-b-i', '3-1'),
   T('b/ii', 10, 'sb-q6-b-ii', '3-1'), T('c', 20, 'sb-q6-c', '0-0')],
  'Five tasks totalling 75. a(i) the two terms at 5; a(ii) 2 arguments for at 5 from six + 2 against at 5 from six. b(i) 3 at 5 from nine; b(ii) 2 conflicts at 5 from six. c 4 at 5 from five.',
  'Commercial banks and nationalising them are Financial Sector (3-4), as 2014 OL files commercial banks and 2011 OL nationalised banks, and nationalisation also Government Intervention (1-3); the government’s economic aims and their conflicts are Fiscal Policy & the Budget (3-1), as 2014 HL files them; Friedman’s monetarism is Economics as a Way of Thinking (0-0), as earlier reviews file an economist’s contribution, and also Monetary Policy & Inflation (3-3).', also=['1-3', '3-3'])
q('B7', [7], [26, 27, 28, 29, 30],
  [T('a/i', 15, 'sb-q7-a-i', '4-2'), T('a/ii', 15, 'sb-q7-a-ii', '4-2'), T('b/i', 15, 'sb-q7-b-i', '4-0'),
   T('b/ii', 15, 'sb-q7-b-ii', '4-0'), T('c', 15, 'sb-q7-c-imf', '4-1'), T('c', 15, 'sb-q7-c-world-bank', '4-1')],
  'Five tasks totalling 75. a(i) 3 at 5 from eight (the paper does not say how many); a(ii) 3 at 5 from eight. b(i) 3 at 5 from thirteen (the paper does not say how many); b(ii) 3 at 5 from six. c the IMF OR the World Bank is a printed choice and the scheme credits each with its own list, 3 at 5 (from five, from three): one route each, counted once.',
  'International trade and competitiveness are International Trade & Competitiveness (4-2); developed and developing countries and promoting development are Growth & Development (4-0); the IMF and the World Bank are Globalisation (4-1), as 2017 OL files the IMF, and the World Bank’s lending to LDCs also Growth & Development (4-0).')
q('B8', [7], [31, 32, 33, 34, 35],
  [T('a/i-iv', 25, 'sb-q8-a', '3-5'), T('b/i', 10, 'sb-q8-b-i', '3-5'), T('b/ii', 15, 'sb-q8-b-ii', '3-2'),
   T('c/i', 10, 'sb-q8-c-i', '3-4'), T('c/ii', 15, 'sb-q8-c-ii', '3-4')],
  'Five cards for eight asks totalling 75. a(i)-(iv) one card, as the scheme prices the four areas together, 7 + 6 + 6 + 6, without saying which earns the 7: one ladder, one point for each area, the first correct area 7. b(i) 2 at 5 from six; b(ii) 3 at 5 from eight. c(i) 2 at 5 from six; c(ii) 3 at 5 from seven.',
  'Economic growth is Economic Growth (3-5), price levels Monetary Policy & Inflation (3-3), the current budgetary position Fiscal Policy & the Budget (3-1) and employment Employment & Unemployment (3-2), as 2016 HL files the economy’s performance; an ageing population is Economic Growth (3-5), as 2015 HL files it; emigration is Employment & Unemployment (3-2); savings are Financial Sector (3-4), as 2012 HL files them.', also=['3-3', '3-1'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (1, '1Answer six of the nine short response type questions in the spaces'): ('exam-question-selection', 'Whole-exam selection (Section A), read beside the cover’s marking grid; every printed task stays in the census.'),
 (1, 'Answer six questions from Section A and four questions from Section B. Credit will be'): ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 (2, 'Answer 1:'): ('not-a-task-selection', 'Section A Q2 answer-space label, read on "Answer 1"; not a selection.'),
 (2, 'Answer 2'): ('not-a-task-selection', 'Section A Q2 answer-space label, read on "Answer 2"; not a selection.'),
 (5, '(i) Is this tax an example of a progressive or a regressive tax? Explain your answer.'): ('answer-classification', 'Section B Q4(b)(i) progressive or regressive is the answer (regressive); one card.'),
 (5, '4. (a) “Next year, almost half of income earners will pay no income tax and 4% of income earners'): ('not-a-task-selection', 'Section B Q4(a) stem wording, read on "no"; not a selection.'),
 (6, '(c) The economist Milton Friedman was regarded as one of the major thinkers of the'): ('not-a-task-selection', 'Section B Q6(c) stem wording, read on "one of"; not a selection.'),
 (7, '(c) Write a brief account on the role of the International Monetary Fund (IMF) or the World Bank'): ('finite-route', 'Section B Q7(c) the IMF OR the World Bank: the scheme credits each with its own list, so one route each, counted once.'),
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
 'subjectId': 'economics', 'year': 2010, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 9)), 'visuallyInspectedSchemePages': list(range(1, 36)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 8 paper and 35 scheme pages (paper page 8 is blank; scheme page 1 is the SEC cover, which prints the level in capitals ("HIGHER LEVEL"), so the scheme file was built with the appenders’ cover check pointed at the file, and page 2 the support notes with the index; scheme page numbers here are the PDF’s and equal the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 54 printed asks (9 Section A + 45 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2010_hl.py). Section B Q8(a)(i)-(iv) is one card, as the scheme prices the four areas on one ladder. Section B Q5(b)(i) and (b)(ii) are one route for each of the scheme’s two tables, and Q7(c) (the IMF OR the World Bank) one route for each side the scheme credits, each counted once.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2010-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
