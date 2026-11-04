"""Write the independent 2022 OL EV census draft from the full visual sweep (re-review 2026-10-12).

Route set: the earlier review's, except Q3, Q8 and Q14(b). Each prints ONE
"1st x n, 2nd x m" tariff beside its stem across two printed parts (9/6, 9/6 and
10/7), the layout 2023 OL Q9 and 2024 OL Q1 already carry as one task with
unpriced rows, so each becomes one task and the (ii) card resolves by alias.
The 2022 Ordinary Irish review mirrors those three route changes only.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2022/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2022/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2022-ol-'
old = json.loads((W / 'scripts/markbank/authoring/reviews/economics-2022-ol-ev.json').read_text())
atlas = json.loads((W / 'data/examTopics/economics-sec-topic-reviews.json').read_text())
OLD_NODES = {q['n']: q['canonicalNodeIds'] for q in atlas['questions']
             if q['year'] == 2022 and q['level'] == 'ordinary' and q['lang'] == 'ev'}
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(OLD_NODES.get(str(n), []) + [t['topicId'] for t in tasks]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [5], [T('i', 9, 'sa-q1-i', '3-5'), T('ii', 6, 'sa-q1-ii', '3-5')],
  '(i) 6 + 3 printed beside the two-row table: 2022 highest, 2020 lowest, one card with unpriced rows. (ii) 6 economic growth.',
  'Forecast growth and its definition are Economic Growth (3-5).')
q(2, [4], [5], [T('i', 9, 'sa-q2-i', '0-0'), T('ii', 6, 'sa-q2-ii', '0-0')],
  '(i) 9 Central Statistics Office. (ii) 6 one use of census data (five bullets).',
  'The CSO and the use of census data are Economics as a Way of Thinking (0-0).')
q(3, [4], [6], [T('i+ii', 15, 'sa-q3-i', '1-1')],
  'One tariff, 1st x 9 (6+3) and 2nd x 6 (3+3), prints beside the Q3 stem across (i) and (ii): one 15-mark card with unpriced rows (a reason for online shopping AND a disadvantage for local retailers); the old (ii) card resolves by alias.',
  'Consumer behaviour online is The Consumer (1-1); the effect on retailers is also Costs of Production, Revenue & Profit (1-5).')
q(4, [5], [6], [T('all', 15, 'seca-q4-ticks', '1-1')],
  'Four objective ticks (Samsung and Pixel substitutes, case and plug complements), 1st x 9 then 3 x 2: one card, unpriced rows (hidden completed table, whole printed question shown).',
  'Substitute and complementary goods are The Consumer (1-1).')
q(5, [5], [7], [T('a', 15, 'sa-q5-a', '2-1'), T('b', 15, 'sa-q5-b', '2-1')],
  'Answer (a) OR (b), each two advantages 1st x 9 (6+3), 2nd x 6 (3+3): economy (seven bullets) or employees (three).',
  'The minimum wage is The Labour Market (2-1).')
q(6, [6], [8], [T('i', 9, 'seca-q6-i', '3-2'), T('ii', 6, 'sa-q6-ii', '3-2')],
  '(i) 6 + 3 March and April 2021, unpriced pair. (ii) 6 the lockdown.',
  'Unemployment and its rise are Employment & Unemployment (3-2).')
q(7, [7], [9], [T('a/i', 5, 'sa-q7-a-i', '1-5'), T('a/ii', 10, 'seca-q7-a-ii-ticks', '1-5'), T('b/i', 10, 'sa-q7-b-i', '1-5'), T('b/ii', 5, 'sa-q7-b-ii', '1-5')],
  'Answer (a) OR (b). a(i) 5 fixed costs; a(ii) 4+4+1+1 four objective ticks (hidden completed table, whole printed question shown). b(i) 10 (5 x 2) €3,550; b(ii) 5 (2+2+1) €1,450 (hidden working; the whole printed (b) with its table shown).',
  'Fixed and variable costs, total cost and profit are Costs of Production, Revenue & Profit (1-5).')
q(8, [8], [10], [T('i+ii', 15, 'sa-q8-i', '2-2')],
  'One tariff, 1st x 9 (6+3) and 2nd x 6 (3+3), prints beside the Q8 stem across (i) and (ii): one 15-mark card with unpriced rows (a positive externality AND an opportunity cost); the old (ii) card resolves by alias.',
  'Positive externalities are Market Failure (2-2); the opportunity cost of public spending is Scarcity & Choice (0-1).')
q(9, [8], [11], [T('i', 13, 'seca-q9-i', '1-4'), T('ii', 2, 'sa-q9-ii', '1-4')],
  '(i) 13 PED = −1 (hidden working, whole printed question shown). (ii) 2 objective UNIT ELASTIC.',
  'Price elasticity of demand is Elasticity (1-4).')
q(10, [9], [12], [T('a', 15, 'sa-q10-a', '3-1'), T('b', 15, 'sa-q10-b', '3-1')],
  'Answer (a) OR (b), each 9+3+3: compare 2018 €5.32bn with 2024 €3.51bn, or define the national debt (two wordings).',
  'The national debt and its interest are Fiscal Policy & the Budget (3-1).')
q(11, [10, 11, 12], [13, 14, 15],
  [T('a/i', 12, 'q11-a-i', '2-0'), T('a/ii', 12, 'q11-a-ii', '2-0'), T('b/i', 21, 'q11-b-i', '2-0'),
   T('b/ii', 9, 'q11-b-ii', '2-0'), T('c/i', 9, 'q11-c-i', '2-0'), T('c/ii', 8, 'q11-c-ii', '2-0'),
   T('c/iii', 4, 'q11-c-iii', '1-3')],
  'Seven tasks totalling 75. a(i) 9 + 3 YouTube and Vimeo, unpriced pair; a(ii) 1 x 8, 1 x 4. b(i) 3 x 7 Price, Marginal Cost, Marginal Revenue; b(ii) 4 + 4 + 1 for Q1, P1, C1 (hidden solution, whole printed (b) shown). c(i) 5 + 4 explanation and example; c(ii) 2 x 4 (2+2); c(iii) 4 (2+2).',
  'Monopoly and the streaming market are Market Structures (2-0); intervening against a dominant firm is Government Intervention (1-3).')
q(12, [13, 14, 15], [16, 17, 18],
  [T('a/i-iii', 28, 'q12-a-i', '1-0'), T('b/i', 8, 'q12-b-i', '1-1'), T('b/ii', 8, 'q12-b-ii', '1-1'),
   T('b/iii', 12, 'q12-b-iii', '1-0'), T('c/i', 5, 'q12-c-i', '0-2'), T('c/ii', 14, 'q12-c-ii', '0-2')],
  'Six tasks totalling 75. a(i)-(iii) one diagram, 28 (14 x 2) with the equilibrium labels inside it (hidden solution, whole printed (a) shown); the old supply-only card resolves by alias. b(i) 8; b(ii) 8 demand right to D2; b(iii) 6 + 6 P2 and Q2 (hidden solution, whole printed (b) shown). c(i) 5 (3+2) two wordings; c(ii) 2 x 7 (4+3).',
  'Demand, supply and equilibrium are The Market Economy (1-0); the demand shift is The Consumer (1-1); a sustainable business is Sustainability (0-2).')
q(13, [16, 17, 18], [19, 20, 21],
  [T('a/i', 16, 'q13-a-i-percentage', '3-1'), T('a/ii/current', 9, 'q13-a-ii-expenditure', '3-1'),
   T('a/ii/capital', 9, 'q13-a-ii-capital', '3-1'), T('b/i', 12, 'q13-b-i', '3-0'), T('b/ii', 12, 'q13-b-ii', '3-0'),
   T('b/iii', 6, 'q13-b-iii', '3-0'), T('c/i', 10, 'q13-c-i', '1-1'), T('c/ii', 10, 'q13-c-ii', '1-1')],
  'Eight routes; 75 with one route for a(ii). a(i) 16 86.61% (hidden working, whole printed question shown); a(ii) current OR capital, each 6 + 3 definition and example, two routes. b(i) 12 for I, X, M, no split; b(ii) 12 multiplier 2 (hidden working, whole printed (ii) shown); b(iii) 6 (the scheme line that national income doubles is flagged). c(i) 10 (6+4); c(ii) 1st x 6, 2nd x 4 explanation and example, unpriced pair.',
  'Government expenditure is Fiscal Policy & the Budget (3-1); national income and the multiplier are National Income (3-0); consumer spending and rational behaviour are The Consumer (1-1).')
q(14, [19, 20, 21], [22, 23, 24, 25],
  [T('a/i', 24, 'q14-a-i', '0-1'), T('a/ii', 3, 'q14-a-ii-scarce', '0-1'), T('a/iii', 7, 'q14-a-iii-water', '0-2'),
   T('b/i+ii', 17, 'q14-b-i', '1-3'), T('c/i', 16, 'q13-a-i', '4-0'), T('c/ii', 8, 'q13-a-ii', '4-0')],
  'Six tasks totalling 75. a(i) 4 x 6 (4+2) one row per factor (hidden completed table, whole printed question shown); a(ii) 3 (three wordings); a(iii) 7. b one tariff, 1st x 10 (6+4) and 2nd x 7 (4+3), prints beside the stem across (i) and (ii): one 17-mark card with unpriced rows; the old (ii) card resolves by alias. c(i) 2 x 8 (4+4); c(ii) 2 x 4 (2+2) (these two IDs carry q13 prefixes; citations are Q14(c)).',
  'The factors of production and scarcity are Scarcity & Choice (0-1); water use is Sustainability (0-2); water charges are Government Intervention (1-3); less developed nations and aid are Growth & Development (4-0).')
q(15, [22, 23, 24], [26, 27, 28],
  [T('a/i', 10, 'q15-a-i-trend', '3-1'), T('a/ii', 9, 'q15-a-ii', '3-1'), T('b/i', 12, 'q15-b-i', '4-1'),
   T('b/ii', 8, 'q14-a-ii', '4-1'), T('b/iii', 8, 'q14-a-iii', '4-1'), T('c/i', 12, 'q15-c-i', '4-2'),
   T('c/ii', 16, 'q14-b-ii', '4-2')],
  'Seven tasks totalling 75. a(i) 10 (6+4) trend with figures (the scheme writes €4m/€12m for a millions axis); a(ii) 9 (6+3), the scheme marks two linked concepts, revenue 6 and the services it pays for 3. b(i) 2 x 6 names; b(ii) and b(iii) 2 x 4 (2+2). c(i) US 6 AND UK 6; c(ii) 2 x 8 (4+4). Several IDs carry q14 prefixes; citations are Q15.',
  'Corporation tax is Fiscal Policy & the Budget (3-1); multinationals are Globalisation (4-1); exports are International Trade & Competitiveness (4-2).')
q(16, [25, 26, 27], [29, 30, 31, 32],
  [T('a/i', 12, 'q15-a-i', '1-3'), T('a/ii', 7, 'q16-a-ii-smoking', '1-3'), T('a/iii/social', 4, 'q15-a-iii-social', '2-2'),
   T('a/iii/private', 4, 'q15-a-iii-private', '2-2'), T('b/i', 8, 'q16-b-i', '3-3'), T('b/ii', 16, 'q16-a-ii', '3-3'),
   T('c/i', 8, 'q16-c-i', '3-1'), T('c/ii', 8, 'q16-c-ii', '3-0'), T('c/iii', 8, 'q16-c-iii', '3-0')],
  'Nine tasks totalling 75. a(i) 2 x 6 (3+3); a(ii) 7 (4+3); a(iii) one social AND one private benefit, separate 1 x 4 (2+2) cells, two cards. b(i) 8 (6+2) two wordings; b(ii) 2 x 8 (4+4). c(i) 8 indirect tax and example; c(ii) 8 hidden economy and example (the English scheme prints this 8 beside the example; the Irish scheme places an 8 beside each of (i), (ii), (iii)); c(iii) 8.',
  'Minimum pricing and cigarette measures are Government Intervention (1-3); social and private benefits are Market Failure (2-2); inflation is Monetary Policy & Inflation (3-3); indirect tax is Fiscal Policy & the Budget (3-1); the hidden economy is National Income (3-0).')

SEL = {
 'Answer 3 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 3 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer either (a) or (b)': ('finite-route', 'Printed alternative pair; (a) and (b) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (a)/(b) alternatives.'),
}
PAGE_SEL = {
 (8, '(An externality refers to the external costs (or external benefits) that accrue to other individuals or'): ('not-a-task-selection', 'Q8 stem definition ("costs or benefits"), not a selection.'),
 (8, 'to society as a result of production or consumption.) Adapted from ourworldindata.org'): ('not-a-task-selection', 'Q8 stem definition, continued.'),
 (8, '(ii) Indicate if the demand is price elastic, price inelastic or unit elastic.'): ('answer-classification', 'Q9(ii) the PED of −1 decides the answer (unit elastic); one card.'),
 (16, '(ii) Explain current or capital government expenditure, using a relevant example to'): ('finite-route', 'Q13(a)(ii) current OR capital; the scheme writes both, two routes at 9.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 32: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# Every route equals the earlier review's except the three consolidations.
tup = lambda qs: sorted((x['n'], t['key'], t['cardId'], t['marks'], t['topicId']) for x in qs for t in x['tasks'])
new, prev = set(tup(Q)), set(tup(old['questions']))
expect_new = {('3', 'i+ii', P + 'sa-q3-i', 15, 'economics-1-1'), ('8', 'i+ii', P + 'sa-q8-i', 15, 'economics-2-2'),
              ('14', 'b/i+ii', P + 'q14-b-i', 17, 'economics-1-3')}
expect_old = {('3', 'i', P + 'sa-q3-i', 9, 'economics-1-1'), ('3', 'ii', P + 'sa-q3-ii', 6, 'economics-1-5'),
              ('8', 'i', P + 'sa-q8-i', 9, 'economics-2-2'), ('8', 'ii', P + 'sa-q8-ii', 6, 'economics-0-1'),
              ('14', 'b/i', P + 'q14-b-i', 10, 'economics-1-3'), ('14', 'b/ii', P + 'q14-b-ii-water', 7, 'economics-1-3')}
# A re-run after recording finds the review already carries the change.
if new != prev and (new - prev != expect_new or prev - new != expect_old):
    raise SystemExit(f'unexpected route change: +{new - prev} -{prev - new}')
for x, o in zip(Q, old['questions']):
    assert x['paperPages'] == o['paperPages'], x['n']
    assert x['schemePages'] == o['schemePages'], x['n']
    assert x['canonicalNodeIds'] == OLD_NODES[x['n']], (x['n'], x['canonicalNodeIds'])
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2022, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 33)), 'visuallyInspectedSchemePages': list(range(1, 37)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Re-review 2026-10-12 from a fresh paired visual sweep of all 32 paper and 36 scheme pages (scheme PDF page = printed page + 1; PDF pages 33-36 are the research-project rubric and back cover). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified. Three route changes against the earlier census: Q3, Q8 and Q14(b) each print one first/second tariff across two parts and are now one task each with unpriced rows (the layout 2023 OL Q9 and 2024 OL Q1 already carry); the (ii) cards resolve by alias, and the 2022 Ordinary Irish review mirrors those three changes only. Every stem and ask is now sliced from the paper and every menu from the scheme (econ_2022_ol.py; the Section A script and the correction module are retired). Choose-N rule checked: no printed choose-N-of-M item pool on this paper.',
 'externalClarifications': old.get('externalClarifications', []),
 'curriculumSource': old.get('curriculumSource', 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf'),
}
for k in ('targetedIrishEvidence',):
    if k in old: draft[k] = old[k]
out = W / 'scripts/markbank/authoring/drafts/economics-2022-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
