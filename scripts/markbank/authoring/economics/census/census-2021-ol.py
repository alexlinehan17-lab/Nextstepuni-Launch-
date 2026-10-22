"""Write the independent 2021 OL EV census draft from the full visual sweep (review 2026-10-12).

No earlier full review exists for this paper (only the targeted Q3 boundary
review, whose whole-question 15 is kept). The route set is the shipped deck's
(origin/main) plus one task: Q14(b)(ii) prints a separate 1 @ 8 cell for each of
its two objectives, and the shipped card carried both lists as one any-one menu
at 8, so Maintaining State Services becomes its own card. Three tariffs are
corrected to the printed cells: Q6(b) and Q9(b) 10 -> 15, Q12(b) 15 -> 21.
There is no 2021 Ordinary Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2021/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2021/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2021-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [4], [T('i', 12, 'sa-q1-i', '3-1'), T('ii', 3, 'sa-q1-ii', '3-1')],
  '(i) 3 @ 4 Education 8.9 of 89.6 = 9.93%. (ii) 1 @ 2 then 1 @ 1, two examples from the scheme’s slash-separated list.',
  'Government expenditure by department is Fiscal Policy & the Budget (3-1).')
q(2, [4], [4], [T('all', 15, 'sa-q2', '0-0')],
  'Two objective ticks priced 1 @ 9, 1 @ 6 (first correct 9, second 6): one card, unpriced rows (hidden completed table, whole printed question shown).',
  'Positive and normative statements are Economics as a Way of Thinking (0-0).')
q(3, [4], [5], [T('i+ii', 15, 'sa-q3-i', '1-4')],
  'The targeted boundary review kept: 6 @ 2 working, 1 @ 2 the answer −4.71 and 1 @ 1, printed before (ii); one 15-mark card for the calculation and the elastic answer (hidden working, whole printed question shown).',
  'Price elasticity of demand is Elasticity (1-4).')
q(4, [5], [5], [T('all', 15, 'sa-q4', '1-1')],
  '6 @ 2 the two marginal utilities 13 and 9 with workings, 1 @ 3 the point diminishing marginal utility sets in (hidden completed table, whole printed question shown).',
  'Marginal utility is The Consumer (1-1).')
q(5, [5], [5], [T('all', 15, 'sa-q5', '1-1')],
  '1 @ 9 a substitute named, 1 @ 6 the explanation (three wordings).',
  'Substitute goods are The Consumer (1-1).')
q(6, [6], [6], [T('a', 15, 'sa-q6-a', '3-0'), T('b', 15, 'sa-q6-b', '4-2')],
  'Answer (a) OR (b). a 1 @ 9, 2 @ 3 for the three flows (first correct 9), unpriced rows. b 1 @ 9 explanation + 1 @ 6 example (the earlier card carried 10).',
  'The circular flow is National Income (3-0); invisible exports are International Trade & Competitiveness (4-2).')
q(7, [7], [6], [T('all', 15, 'sa-q7', '3-1')],
  '5 @ 3 the budget calculation and the verdict surplus.',
  'The budgetary position is Fiscal Policy & the Budget (3-1).')
q(8, [7], [7], [T('all', 15, 'sa-q8', '1-1')],
  '9 demand shift to the left on the diagram + 6 (3 + 3) explanation (hidden completed diagram, whole printed question shown).',
  'A shift in demand is The Consumer (1-1).')
q(9, [8], [7], [T('a', 15, 'sa-q9-a', '0-2'), T('b', 15, 'sa-q9-b', '0-2')],
  'Answer (a) OR (b). a 1 @ 9, 2 @ 3 for the three pillars (first correct 9), unpriced rows. b 1 @ 9 then 1 @ 6 for two examples from four plus any acceptable response (the earlier card carried 10).',
  'The pillars of sustainability and sustainable choices are Sustainability (0-2).')
q(10, [9], [8], [T('a', 15, 'sa-q10-a', '2-1'), T('b', 15, 'sa-q10-b', '2-1')],
  'Answer (a) OR (b). a 1 @ 9, 1 @ 6 for the two terms (first correct 9), unpriced rows. b 1 @ 15 (9 + 6) one reason from eight (the earlier card carried six).',
  'Public and private sector pay and wage differentials are The Labour Market (2-1).')
q(11, [10, 11, 12], [9, 10, 11],
  [T('a/i', 12, 'q11-a-i', '4-0'), T('a/ii', 8, 'q11-a-ii', '4-0'), T('b/i/advantage', 5, 'q11-b-i-pos', '4-1'),
   T('b/i/disadvantage', 5, 'q11-b-i-neg', '4-1'), T('b/ii', 6, 'q11-b-ii', '4-1'), T('b/iii', 14, 'q11-b-iii', '4-1'),
   T('c/i', 10, 'q11-c-i', '3-5'), T('c/ii', 20, 'q11-c-ii', '4-0')],
  'Eight routes; 75 with one route for b(i). a(i) 4 @ 3, the four cells +1, +0.2 years, +0.2, Yes; a(ii) 1 @ 8 (4 + 4) one of two causes. b(i) one advantage OR one disadvantage at 5, a printed choice whose scheme lists eight advantages and four disadvantages: two routes (the earlier cards carried three of each); b(ii) 2 @ 3; b(iii) 2 @ 7 (3 + 4) from seven (the earlier card carried six). c(i) 10; c(ii) 10 explanation + 2 @ 5 products.',
  'The HDI and Fair Trade are Growth & Development (4-0); globalisation and MNCs are Globalisation (4-1); economic growth is Economic Growth (3-5).')
q(12, [13, 14, 15], [12, 13],
  [T('a/i', 20, 'q12-a-i', '2-0'), T('a/ii', 10, 'q12-a-ii', '2-0'), T('b', 21, 'q12-b', '2-0'),
   T('c/i/consumer', 8, 'q12-c-i-consumer', '2-0'), T('c/i/economy', 8, 'q12-c-i-economy', '2-0'),
   T('c/ii', 8, 'q12-c-ii', '2-0')],
  'Six tasks totalling 75. a(i) 4 @ 5 the four labels; a(ii) 2 @ 4, 1 @ 2 for P1, Q1 and C1, the order the scheme prints beside the cell (hidden completed diagram, whole printed (a) shown). b 1 @ 9 (6 + 3) then 2 @ 6 (3 + 3) for three assumptions from eight (the earlier card carried 3 @ 5). c(i) the consumer and the economy are separately printed 1 @ 8 cells: two cards; c(ii) 1 @ 8 (4 + 4).',
  'Perfect competition is Market Structures (2-0).')
q(13, [16, 17, 18], [14, 15, 16],
  [T('a/i', 8, 'q13-a-i', '2-1'), T('a/ii', 8, 'q13-a-ii', '3-1'), T('a/iii', 8, 'q13-a-iii', '3-3'),
   T('b/i', 14, 'q13-b-i', '3-4'), T('b/ii', 7, 'q13-b-ii', '3-4'), T('c/i', 5, 'q13-c-i', '3-3'),
   T('c/ii', 18, 'q13-c-ii-cpi', '3-3'), T('c/iii', 7, 'q13-c-iii-types', '3-3')],
  'Eight tasks totalling 75. a(i) 8; a(ii) 8; a(iii) 8 (4 + 4) either term in bold. b(i) one 2 @ 7 (4 + 3) cell for an impact on consumers AND on interest rates: one card with two required headings at 7 (the earlier card was an any-two menu); b(ii) 7. c(i) 5 deflation; c(ii) 3 @ 6 the three readings; c(iii) 7 one cause from four.',
  'The minimum wage is The Labour Market (2-1); fiscal policy is Fiscal Policy & the Budget (3-1); monetary policy, deflation and inflation are Monetary Policy & Inflation (3-3); mortgage lenders and the Central Bank are the Financial Sector (3-4).')
q(14, [19, 20, 21], [17, 18, 19],
  [T('a/i', 14, 'q14-a-i-capital', '3-1'), T('a/ii', 7, 'q14-a-ii', '0-1'), T('b/i', 8, 'q14-b-i', '1-0'),
   T('b/ii/environment', 8, 'q13-c-ii', '0-2'), T('b/ii/state-services', 8, 'q14-b-ii-services', '3-1'),
   T('c/i', 10, 'q14-c-i', '3-1'), T('c/ii', 10, 'q14-c-ii', '3-1'), T('c/iii', 10, 'q13-c-iii', '1-3')],
  'Eight tasks totalling 75. a(i) 7 capital + 7 explanation; a(ii) 7 (the scheme prints three 7s down (a) and totals it 21). b(i) 8; b(ii) one measure for EACH objective, each a separately printed 1 @ 8 cell: Care for the Environment (five measures) and Maintaining State Services (four), two cards; the earlier single card at 8 now carries the environment and a new card the state services. c(i) 2 @ 5 Ireland and Germany; c(ii) 5 indirect + 5 explanation; c(iii) 2 @ 5 (2 + 3) from seven (the earlier card carried six). Two IDs carry q13 prefixes; their citations are Q14.',
  'Capital expenditure, state services and taxes are Fiscal Policy & the Budget (3-1); opportunity cost is Scarcity & Choice (0-1); the mixed economy is The Market Economy (1-0); environmental measures are Sustainability (0-2); intervention is Government Intervention (1-3).')
q(15, [22, 23, 24], [20, 21],
  [T('a/i', 8, 'q15-a-i-supply', '1-2'), T('a/ii', 7, 'q15-a-ii-sanitiser', '1-2'), T('b/i', 10, 'q15-b-i', '1-1'),
   T('b/ii', 15, 'q15-b-ii', '1-2'), T('b/iii', 10, 'q15-b-iii', '1-1'), T('c/i', 10, 'q15-c-i', '0-1'),
   T('c/ii', 5, 'q15-c-ii', '0-1'), T('c/iii', 10, 'q15-c-iii', '4-2')],
  'Eight tasks totalling 75. a(i) 8 the law of supply with an example; a(ii) 7 Yes and its explanation, no published split. b(i) 10 Diagram B; b(ii) 8 supply curve + 7 explanation; b(iii) 10. c(i) 10 (7 + 3); c(ii) 5 one of two accounts; c(iii) 10 (7 + 3).',
  'The law of supply and input costs are The Firm (Supply) (1-2); demand and consumer loyalty are The Consumer (1-1); scarcity is Scarcity & Choice (0-1); tariffs are International Trade & Competitiveness (4-2).')
q(16, [25, 26], [22, 23, 24],
  [T('a', 24, 'q16-a', '0-1'), T('b/i', 20, 'q14-a-i', '2-2'), T('b/ii', 7, 'q16-b-ii', '2-2'),
   T('c/i', 16, 'q15-a-i', '4-2'), T('c/ii', 8, 'q15-a-ii', '4-2')],
  'Five tasks totalling 75. a 3 @ 8 land, labour and enterprise rows. b(i) one 2 @ 10 (6 + 4) cell for one social AND one economic benefit: one card with two required headings at 10 (the earlier card was an any-two menu); b(ii) 7 (4 + 3) one of three accounts. c(i) one 2 @ 8 (4 + 4) cell for an effect on consumers AND on businesses: one card with two required headings at 8; c(ii) 1 @ 8 (4 + 4) from five. Several IDs carry q14/q15 prefixes; their citations are Q16.',
  'The factors of production are Scarcity & Choice (0-1), as 2022 and 2023 OL file the same table (the earlier card filed it under Economics as a Way of Thinking); the sugar tax and market failure are Market Failure (2-2); Brexit and exports are International Trade & Competitiveness (4-2).')

SEL = {
 'Answer 3 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 3 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer (a) or (b)': ('finite-route', 'Printed alternative pair; (a) and (b) are separate carded tasks, counted once in the question total.'),
 'Answer either (a) or (b)': ('finite-route', 'Printed alternative pair; (a) and (b) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (a)/(b) alternatives.'),
}
PAGE_SEL = {
 (4, '(ii) Indicate if the demand for Kerosene is price elastic or price inelastic.'): ('answer-classification', 'Q3(ii) the PED of −4.71 decides the answer (elastic); kept within the one Q3 card.'),
 (7, 'Indicate if it is a surplus or a deficit.'): ('answer-classification', 'Q7 the computed position decides the answer (a surplus of €1.4bn); one card.'),
 (8, 'sustainable choices.'): ('not-a-task-selection', 'Q9(b) wrapped ask ("more environmentally sustainable choices"), not a selection.'),
 (11, '(b) (i) Outline one advantage or one disadvantage of globalisation.'): ('finite-route', 'Q11(b)(i) advantage OR disadvantage, ticked; the scheme lists both, two routes at 5.'),
 (16, 'Explain one of the terms in bold in the statement above.'): ('finite-route', 'Q13(a)(iii) either term (monetary policy or price stability) at 8: one card whose menu holds both.'),
 (19, '(a) (i) Is the above an example of current or capital government expenditure?'): ('answer-classification', 'Q14(a)(i) the scheme answer is capital expenditure; one card.'),
 (21, '(ii) Is Value Added Tax a direct tax or an indirect tax?'): ('answer-classification', 'Q14(c)(ii) the scheme answer is indirect; one card.'),
 (23, 'Demand curve or supply curve:'): ('answer-classification', 'Q15(b)(ii) answer line; the scheme answer is the supply curve.'),
 (23, 'Diagram A: OR Diagram B:'): ('answer-classification', 'Q15(b)(i) tick line; the scheme answer is Diagram B.'),
 (23, 'increases. Would this impact on the demand curve or the supply curve?'): ('answer-classification', 'Q15(b)(ii) the scheme answer is the supply curve (8) with its explanation (7); one card.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 28: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# The shipped routes (origin/main) and the changes this census makes to them.
SHIPPED = {
 'q11-a-i': 12, 'q11-a-ii': 8, 'q11-b-i-neg': 5, 'q11-b-i-pos': 5, 'q11-b-ii': 6, 'q11-b-iii': 14, 'q11-c-i': 10,
 'q11-c-ii': 20, 'q12-a-i': 20, 'q12-a-ii': 10, 'q12-b': 15, 'q12-c-i-consumer': 8, 'q12-c-i-economy': 8,
 'q12-c-ii': 8, 'q13-a-i': 8, 'q13-a-ii': 8, 'q13-a-iii': 8, 'q13-b-i': 14, 'q13-b-ii': 7, 'q13-c-i': 5,
 'q13-c-ii': 8, 'q13-c-ii-cpi': 18, 'q13-c-iii': 10, 'q13-c-iii-types': 7, 'q14-a-i': 20, 'q14-a-i-capital': 14,
 'q14-a-ii': 7, 'q14-b-i': 8, 'q14-c-i': 10, 'q14-c-ii': 10, 'q15-a-i': 16, 'q15-a-i-supply': 8, 'q15-a-ii': 8,
 'q15-a-ii-sanitiser': 7, 'q15-b-i': 10, 'q15-b-ii': 15, 'q15-b-iii': 10, 'q15-c-i': 10, 'q15-c-ii': 5,
 'q15-c-iii': 10, 'q16-a': 24, 'q16-b-ii': 7, 'sa-q1-i': 12, 'sa-q1-ii': 3, 'sa-q10-a': 15, 'sa-q10-b': 15,
 'sa-q2': 15, 'sa-q3-i': 15, 'sa-q4': 15, 'sa-q5': 15, 'sa-q6-a': 15, 'sa-q6-b': 10, 'sa-q7': 15, 'sa-q8': 15,
 'sa-q9-a': 15, 'sa-q9-b': 10,
}
REMARKED = {'sa-q6-b': 15, 'sa-q9-b': 15, 'q12-b': 21}
ADDED = {'q14-b-ii-services': 8}
tasks = [t for x in Q for t in x['tasks']]
got = {t['cardId'][len(P):]: t['marks'] for t in tasks}
want = {**{k: REMARKED.get(k, v) for k, v in SHIPPED.items()}, **ADDED}
assert got == want, (set(got.items()) ^ set(want.items()))
for x in Q:
    n = int(x['n'])
    alternative = lambda t: (n <= 10 and t['key'] == 'b') or t['key'] == 'b/i/disadvantage'
    once = sum(t['marks'] for t in x['tasks'] if not alternative(t))
    assert once == (75 if n > 10 else 15), (n, once)
draft = {
 'subjectId': 'economics', 'year': 2021, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 29)), 'visuallyInspectedSchemePages': list(range(1, 29)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-10-12 from a paired visual sweep of all 28 paper and 28 scheme pages (scheme PDF page = printed page + 1; PDF pages 25-28 are the research-project rubric and back cover). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified. Against the shipped deck: one task added (Q14(b)(ii) Maintaining State Services, a separately printed 1 @ 8 cell the earlier single card merged with Care for the Environment); Q6(b) and Q9(b) 10 -> 15 and Q12(b) 15 -> 21 at their printed cells; Q13(b)(i), Q16(b)(i) and Q16(c)(i) each print one cell for two required headings and become heading cards; menus restored to the scheme’s full lists; the Q3 whole-question boundary review kept. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2021_ol.py; the Section A script is retired). Choose-N rule checked: no printed choose-N-of-M item pool.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2021-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
