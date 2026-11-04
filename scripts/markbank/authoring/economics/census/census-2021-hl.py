"""Write the independent 2021 HL EV census draft from the full visual sweep (review 2026-10-12).

No earlier review exists for this paper. The route set is the shipped deck's
(origin/main), with two consolidations and five tariff corrections. Q12(a)(ii)
prints 2 @ 8 (5 + 3) and 2 @ 5 (2 + 3) beside the one ask for two positive AND
two negative impacts without tying either price to a side, and Q16(b)(ii) prints
one 10 (2 @ 5) cell for one social AND one economic reason: each becomes one
task, and the second card resolves by alias. Q11(a)(ii), Q11(b)(ii) and Q15(a)
take the marks the scheme prints for the answer as well as its explanation.
There is no 2021 Higher Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2021/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2021/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2021-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [4], [T('a', 7, 'seca-q1-a', '4-2'), T('b', 8, 'sa-q1-b', '4-2')],
  'a 7 trade balance €237m surplus (the paper asks for 2015-2019 and the scheme sums all five years). b 2 @ 4 from the scheme’s three headed reasons (the earlier card carried two).',
  'The balance of trade and why a surplus is an aim are International Trade & Competitiveness (4-2).')
q(2, [4], [4], [T('all', 15, 'sa-q2', '0-0')],
  'Four objective ticks priced 4 + 4, 4 + 3 without naming which row earns which: one card, unpriced rows (hidden completed table, whole printed question shown).',
  'Positive and normative statements are Economics as a Way of Thinking (0-0).')
q(3, [4, 5], [5], [T('a', 5, 'sa-q3-a', '2-0'), T('b', 10, 'sa-q3-b', '2-0')],
  'a 5 (2 + 3) one reason from three. b 2 @ 5 (2 + 3) from the scheme’s three headed conditions (the earlier card carried two).',
  'Price discrimination, why consumers accept it and the conditions for it, is Market Structures (2-0), as 2023 and 2024 HL file it; the earlier cards filed it under The Consumer.')
q(4, [5, 6], [6], [T('a', 7, 'sa-q4-a', '2-2'), T('b', 8, 'sa-q4-b', '2-2'), T('c', 8, 'sa-q4-c', '2-2')],
  'a 7 (4 + 3) demerit goods. Answer (b) OR (c), each 8 (4 + 4): two carded routes.',
  'Demerit goods, their purchase and taxing them are Market Failure (2-2).')
q(5, [7], [7], [T('a', 7, 'sa-q5-a', '3-4'), T('b', 8, 'sa-q5-b', '3-4')],
  'a 7 consumer protection. b 2 @ 4 from the scheme’s six headed duties (the earlier card carried five).',
  'Central Bank regulation and duties are the Financial Sector (3-4).')
q(6, [8, 9], [8, 9], [T('a', 7, 'sa-q6-a', '4-0'), T('b', 8, 'sa-q6-b', '4-0'), T('c', 8, 'sa-q6-c', '4-0')],
  'a 7 (4 + 3) HDI against GDP. Answer (b) OR (c), each 8 (4 + 4): one policy from four headings, or one way Ireland could assist from four (the earlier cards carried three and a mis-split four).',
  'The HDI and policies to raise it are Growth & Development (4-0).')
q(7, [10, 11], [9, 10], [T('a', 9, 'seca-q7-a', '3-1'), T('b', 6, 'sa-q7-b', '3-1'), T('c', 6, 'sa-q7-c', '3-1')],
  'a comparison 5 (three alternatives) + reason 4. Answer (b) OR (c), each 6: b 2 @ 3 from six headed disadvantages; c 6 opportunity cost of servicing the debt.',
  'Gross debt per person, a budget surplus and the national debt are Fiscal Policy & the Budget (3-1).')
q(8, [12], [11], [T('a', 7, 'seca-q8-a', '1-1'), T('b', 8, 'seca-q8-b', '1-1')],
  'a 7 price of Z €6 (the ratio is printed as fractions; crop of the printed ratios). b 8 (2 @ 4) the equi-marginal principle.',
  'The equi-marginal principle of consumer behaviour is The Consumer (1-1), as 2023 HL files it; the earlier cards filed it under Elasticity.')
q(9, [13], [11], [T('a', 9, 'seca-q9-a', '2-0'), T('b', 6, 'seca-q9-b', '2-0')],
  'a 3 @ 3 oligopoly, monopoly, monopolistic competition. b one 6 for a reason for each of the three, no published split.',
  'Identifying market structures is Market Structures (2-0).')
q(10, [14], [12], [T('a', 8, 'sa-q10-a', '3-3'), T('b', 7, 'sa-q10-b', '3-3')],
  'a 8 the post-2008 cuts. b 7: the scheme credits MAINTAIN or DECREASE (one cell, two either/or responses), carded as one card whose menu holds both stances.',
  'ECB interest rates are Monetary Policy & Inflation (3-3).')
q(11, [15, 16, 17, 18], [13, 14, 15],
  [T('a/i', 7, 'q11-a-i', '2-0'), T('a/ii', 8, 'q11-a-ii', '2-0'), T('b/i', 16, 'q11-b-i', '2-0'),
   T('b/ii', 10, 'q11-b-ii', '2-0'), T('b/iii', 8, 'q11-b-iii', '2-0'), T('c/i', 8, 'q11-c-i', '1-5'),
   T('c/ii', 18, 'q11-c-ii', '1-5')],
  'Seven tasks totalling 75. a(i) 7 HHI 4262; a(ii) 8 (3 + 5) the objective answer highly concentrated 3 and the explanation 5 (the earlier card carried the 5 only). b(i) 16 four labels; b(ii) 2 for No + 2 @ 4 reasons (the earlier card carried the 8 only); b(iii) 2 @ 4 from four headings (the earlier card carried three). c(i) 8; c(ii) 3 @ 6 (2 + 4) from eight headed economies (the earlier card carried seven).',
  'Concentration and oligopoly are Market Structures (2-0); internal economies of scale are Costs of Production, Revenue & Profit (1-5).')
q(12, [19, 20, 21], [16, 17, 18, 19, 20, 21],
  [T('a/i', 4, 'q12-a-i', '4-1'), T('a/ii', 26, 'q12-a-ii-pos', '4-1'), T('b/i', 14, 'q12-b-i', '3-1'),
   T('b/ii', 7, 'q12-b-ii', '4-2'), T('c/i', 12, 'q12-c-i', '4-2'), T('c/ii', 12, 'q12-c-ii', '4-1')],
  'Six tasks totalling 75. a(i) 4 three alternative definitions; a(ii) 2 @ 8 (5 + 3) and 2 @ 5 (2 + 3) printed beside the one ask for two positive AND two negative impacts, not tied to either side: one 26-mark card over the scheme’s five positive and eight negative headings, the old negative card resolving by alias. b(i) 2 @ 7 (3 + 4) from five; b(ii) 7 (3 + 4) from three. c(i) 2 @ 6 from four; c(ii) 2 @ 6 from six.',
  'Globalisation and EU membership are Globalisation (4-1); the 12.5% corporation tax rate is Fiscal Policy & the Budget (3-1); the Commission’s tax aim and Brexit are International Trade & Competitiveness (4-2).')
q(13, [22, 23, 24, 25], [22, 23, 24],
  [T('a/i', 8, 'q13-a-i', '1-0'), T('a/ii', 12, 'q13-a-ii', '1-0'), T('b/i', 10, 'q13-b-i', '2-2'),
   T('b/ii', 6, 'q13-b-ii', '2-2'), T('b/iii', 6, 'q13-b-iii', '1-3'), T('c/i', 15, 'q13-c-i', '1-4'),
   T('c/ii', 8, 'q13-c-ii', '1-4'), T('c/iii', 10, 'q13-c-iii', '1-4')],
  'Eight tasks totalling 75. a(i) 8 at 1 per labelled point on the completed diagram (hidden solution, whole printed (a)(i) shown); a(ii) 12 (3 @ 4), the three printed steps. b(i) 2 @ 5 (2 + 3) from three bullets; b(ii) 6 (3 + 3) one from four headings; b(iii) 6 (2 @ 3) one advantage with an example from six. c(i) 15 PED −1.63; c(ii) 8 (4 + 4) elastic and a reason; c(iii) 10 objective decrease and its explanation.',
  'Excess demand is The Market Economy (1-0); information failure is Market Failure (2-2); regulation is Government Intervention (1-3); the PED calculation is Elasticity (1-4), which the earlier card filed under The Consumer.')
q(14, [26, 27, 28, 29], [25, 26, 27, 28],
  [T('a/i', 12, 'q14-a-i', '3-3'), T('a/ii', 12, 'q14-a-ii', '3-3'), T('b/i', 14, 'q14-b-i', '3-3'),
   T('b/ii', 7, 'q14-b-ii', '3-3'), T('c/i', 6, 'q14-c-i', '4-2'), T('c/ii', 12, 'q14-c-ii', '4-2'),
   T('c/iii', 12, 'q14-c-iii', '4-2')],
  'Seven tasks totalling 75. a(i) 1 @ 6 then 2 @ 3 from four printed trends; a(ii) 2 @ 6 (3 + 3) from four. b(i) 2 @ 7 (3 + 4) from four; b(ii) 7 (3 + 4) one from three. c(i) 6 (3 + 3); c(ii) 2 @ 6 from four; c(iii) 2 @ 6 from eight.',
  'Inflation, its trend and its control are Monetary Policy & Inflation (3-3), where the earlier trend card was filed under Fiscal Policy; comparative advantage and competitiveness are International Trade & Competitiveness (4-2).')
q(15, [30, 31, 32, 33], [29, 30, 31],
  [T('a', 21, 'q15-a', '3-0'), T('b/i', 8, 'q15-b-i', '3-0'), T('b/ii', 8, 'q15-b-ii', '3-5'),
   T('b/iii', 8, 'q15-b-iii-percap', '3-0'), T('c/i', 8, 'q15-c-i', '3-0'), T('c/ii', 8, 'q15-c-ii', '3-0'),
   T('c/iii', 14, 'q15-c-iii', '3-0')],
  'Seven tasks totalling 75. a 7 + 7 + 7 for GNI and its justification, without naming which element earns which (the earlier card carried 7 for one justification). b(i) 8 (4 + 4); b(ii) 8 (4 + 4) 2007 to 2009 and why; b(iii) 8 (4 + 4) one of the scheme’s alternative accounts. c(i) 8; c(ii) 8 multiplier 1.43 (hidden working); c(iii) 2 @ 7 (3 + 4) from four headings (the earlier card carried three).',
  'GDP and GNI, recession, per capita measures and the multiplier are National Income (3-0); reading recession years off the chart is Economic Growth (3-5).')
q(16, [34, 35, 36, 37], [32, 33, 34, 35],
  [T('a/i', 7, 'q16-a-i-trend', '3-2'), T('a/ii', 9, 'q16-a-ii-derived', '2-1'), T('a/iii', 10, 'q15-b-iii', '3-2'),
   T('b/i', 9, 'q16-b-i', '2-1'), T('b/ii', 10, 'q16-b-ii-social', '2-1'), T('c/i', 12, 'q16-a-i', '2-2'),
   T('c/ii', 12, 'q16-a-ii', '1-3'), T('c/iii', 6, 'q16-c-iii', '3-1')],
  'Eight tasks totalling 75. a(i) 7 the rise and the collapse; a(ii) 9 derived demand; a(iii) 2 @ 5 (2 + 3) from three. b(i) 9 11.48% (two routes); b(ii) one 10 (2 @ 5) (2 + 3) cell for one social AND one economic reason: one card with two required headings at 5, the old economic card resolving by alias. c(i) 2 @ 6 (3 + 3) from five; c(ii) 2 @ 6 (3 + 3) from seven; c(iii) 6 (2 @ 3). Several IDs carry q15/q16(a) prefixes; their citations are Q16(a)(iii) and Q16(c).',
  'Air passengers and employment are Employment & Unemployment (3-2); derived demand and the minimum wage are The Labour Market (2-1); homelessness is Market Failure (2-2) and measures against it Government Intervention (1-3); a cost-benefit analysis of public spending is Fiscal Policy & the Budget (3-1).')

SEL = {
 'Answer 3 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 3 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (b)/(c) alternatives.'),
}
PAGE_SEL = {
 (3, 'Identify whether it is a surplus or a deficit.'): ('answer-classification', 'Q1(a) the computed balance decides the answer (a surplus); one card.'),
 (4, 'Select, using a tick () whether each of the following statements are normative statements or'): ('answer-classification', 'Q2 four objective ticks; one card with the completed table hidden until reveal.'),
 (14, 'increase, decrease, or maintain the current interest rate of 0%. Justify your choice.'): ('finite-route', 'Q10(b) the scheme credits maintain OR decrease at 7; one card whose menu holds both stances.'),
 (16, '(ii) Would you consider this market to be competitive, moderately concentrated, or'): ('answer-classification', 'Q11(a)(ii) the HHI of 4262 decides the answer (highly concentrated, 3 marks); one card.'),
 (24, 'Apple AirPods is elastic or inelastic. Give a reason for your answer.'): ('answer-classification', 'Q13(c)(ii) the PED of −1.63 decides the answer (elastic); one card.'),
 (25, 'product should it, increase, decrease or maintain the same price?'): ('answer-classification', 'Q13(c)(iii) elastic demand decides the answer (decrease price); one card.'),
 (28, '(ii) Continued capital investment in the National Broadband Plan in Ireland is one of the'): ('not-a-task-selection', 'Q14(c)(ii) stimulus ("is one of the" recommendations), not a selection.'),
 (29, '(iii) Choose two other areas the Irish Government should focus on to increase its'): ('finite-route', 'Q14(c)(iii) choose two areas: an any-two menu at 2 @ 6, one card.'),
 (29, 'Justify your choice in each case.'): ('finite-route', 'Q14(c)(iii) each chosen area is justified within its 6.'),
 (30, 'Gross Domestic Product (GDP) or Gross National Income (GNI)?'): ('answer-classification', 'Q15(a) the scheme’s answer is GNI (7 + 7 + 7 with its justification); one card.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 40: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# The shipped routes (origin/main) and the changes this census makes to them.
SHIPPED = {
 'q11-a-i': 7, 'q11-a-ii': 5, 'q11-b-i': 16, 'q11-b-ii': 8, 'q11-b-iii': 8, 'q11-c-i': 8, 'q11-c-ii': 18,
 'q12-a-i': 4, 'q12-a-ii-neg': 10, 'q12-a-ii-pos': 16, 'q12-b-i': 14, 'q12-b-ii': 7, 'q12-c-i': 12,
 'q12-c-ii': 12, 'q13-a-i': 8, 'q13-a-ii': 12, 'q13-b-i': 10, 'q13-b-ii': 6, 'q13-b-iii': 6, 'q13-c-i': 15,
 'q13-c-ii': 8, 'q13-c-iii': 10, 'q14-a-i': 12, 'q14-a-ii': 12, 'q14-b-i': 14, 'q14-b-ii': 7, 'q14-c-i': 6,
 'q14-c-ii': 12, 'q14-c-iii': 12, 'q15-a': 7, 'q15-b-i': 8, 'q15-b-ii': 8, 'q15-b-iii': 10,
 'q15-b-iii-percap': 8, 'q15-c-i': 8, 'q15-c-ii': 8, 'q15-c-iii': 14, 'q16-a-i': 12, 'q16-a-i-trend': 7,
 'q16-a-ii': 12, 'q16-a-ii-derived': 9, 'q16-b-i': 9, 'q16-b-ii-economic': 5, 'q16-b-ii-social': 5,
 'q16-c-iii': 6, 'sa-q1-b': 8, 'sa-q10-a': 8, 'sa-q10-b': 7, 'sa-q2': 15, 'sa-q3-a': 5, 'sa-q3-b': 10,
 'sa-q4-a': 7, 'sa-q4-b': 8, 'sa-q4-c': 8, 'sa-q5-a': 7, 'sa-q5-b': 8, 'sa-q6-a': 7, 'sa-q6-b': 8,
 'sa-q6-c': 8, 'sa-q7-b': 6, 'sa-q7-c': 6, 'seca-q1-a': 7, 'seca-q7-a': 9, 'seca-q8-a': 7, 'seca-q8-b': 8,
 'seca-q9-a': 9, 'seca-q9-b': 6,
}
ALIASED = {'q12-a-ii-neg': 'q12-a-ii-pos', 'q16-b-ii-economic': 'q16-b-ii-social'}
REMARKED = {'q11-a-ii': 8, 'q11-b-ii': 10, 'q15-a': 21, 'q12-a-ii-pos': 26, 'q16-b-ii-social': 10}
tasks = [t for x in Q for t in x['tasks']]
got = {t['cardId'][len(P):]: t['marks'] for t in tasks}
want = {k: REMARKED.get(k, v) for k, v in SHIPPED.items() if k not in ALIASED}
assert got == want, (set(got.items()) ^ set(want.items()))
for x in Q:
    n, total = int(x['n']), sum(t['marks'] for t in x['tasks'])
    if n > 10:
        assert total == 75, (n, total)
    else:
        once = sum(t['marks'] for t in x['tasks'] if not (n in (4, 6, 7) and t['key'] == 'c'))
        assert once == 15, (n, once)
draft = {
 'subjectId': 'economics', 'year': 2021, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-10-12 from a paired visual sweep of all 40 paper and 40 scheme pages (scheme PDF page = printed page + 1; PDF pages 36-40 are the research-project rubric and back cover). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified. Against the shipped deck: Q12(a)(ii) and Q16(b)(ii) each print one tariff across two headings and are now one task each (the second card resolves by alias); Q11(a)(ii), Q11(b)(ii) and Q15(a) take the marks printed for the objective answer as well as the explanation; menus are restored to the scheme’s full headed lists; six demonstrably wrong topics are corrected. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2021_hl.py; the Section A script is retired). Choose-N rule checked: Q14(c)(iii) "choose two" is one any-two card; no printed choose-N-of-M item pool.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2021-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
