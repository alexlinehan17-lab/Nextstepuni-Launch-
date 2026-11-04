"""Write the independent 2024 OL EV census draft from the full visual sweep.

2024 OL was a half-finished batch from the Codex pause; this census is counted
from the paper and scheme afresh. The route set is the one the 2024 Ordinary
Irish review mirrors task for task (econ_review.validate_equivalences), so every
(key, card, marks, topic) tuple must equal the earlier review's; the sweep
confirmed each one. Boundary and topic reasons are re-written from this sweep.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2024/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2024/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2024-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})
q(1, [3], [5, 6], [T('i+ii', 12, 'sa-q1-i', '0-2')],
  '(i) one reason oceans and seas are a valuable resource (five headed) and (ii) one way individuals can protect them (eight bullets) are priced together, 1st @ 8 then 2nd @ 4, so one card with two unpriced rows; the old (ii)-only card resolves by alias.',
  'Marine resources and their protection are Sustainability (0-2).')
q(2, [4], [6, 7], [T('a', 12, 'sa-q2-a', '2-0'), T('b', 12, 'sa-q2-b', '1-1')],
  'Answer (a) OR (b). a objective tick NON-PRICE competition plus explanation, 1st @ 8 then 2nd @ 4, one card. b 12 one benefit of the coupons from six headed.',
  'Price and non-price competition are Market Structures (2-0); a benefit to shoppers is The Consumer (1-1).')
q(3, [5], [8], [T('a', 12, 'seca-q3-a-ticks', '2-0'), T('b', 12, 'sa-q3-b', '2-0')],
  'Answer (a) OR (b). a two objective true/false ticks (1 False, 2 True), 1st @ 8 then 2nd @ 4, one card. b two reasons 1st @ 8 then 2nd @ 4 from five headed.',
  'Monopolistic competition and competitive advertising are Market Structures (2-0).')
q(4, [6], [9], [T('a', 12, 'sa-q4-a', '1-1'), T('b', 12, 'sa-q4-b', '3-4')],
  'Answer (a) OR (b). a 12 one reason families do not save (five headed). b 12 one measure financial institutions could take (four headed).',
  'Household saving is The Consumer (1-1); what banks could do to encourage saving is the Financial Sector (3-4).')
q(5, [6], [10], [T('table', 12, 'seca-q5-ticks', '4-2')],
  '2 @ 6: beef to Germany is an objective visible EXPORT and Irish tourists in French hotels an objective invisible IMPORT, each tick with its reason, one card.',
  'Visible and invisible trade are International Trade & Competitiveness (4-2).')
q(6, [7], [10], [T('two-effects', 12, 'sa-q6', '0-2')],
  'Two effects on consumers 1st @ 8 then 2nd @ 4 from five headed, one card.',
  'The Deposit Return Scheme is Sustainability (0-2).')
q(7, [7], [11], [T('table', 12, 'seca-q7-ticks', '0-0')],
  'Two objective classifications (plastic bag levy POSITIVE, pension NORMATIVE), 1st @ 8 then 2nd @ 4, one card.',
  'Positive and normative statements are Economics as a Way of Thinking (0-0).')
q(8, [8], [11], [T('i+ii', 12, 'sa-q8-i', '3-0')],
  '(i) lowest inequality Slovakia and (ii) highest USA read off the Gini chart, priced together 1st @ 8 then 2nd @ 4, one card; the old (ii)-only card resolves by alias.',
  'Income distribution measured by the Gini coefficient is National Income (3-0).')
q(9, [8], [11], [T('four-blanks', 12, 'sa-q9', '3-0')],
  'Four blanks (Gross, Product; Gross, National) priced 1st @ 4, 2nd @ 4, 3rd @ 2, 4th @ 2 without naming the field for each price: one card, four unpriced rows. All four are required; no choice.',
  'GDP and GNI are National Income (3-0).')
q(10, [9], [12], [T('diagram+reason', 12, 'sa-q10', '1-0')],
  'Objective tick DIAGRAM A (demand shifts right) 8 + explanation of the higher price and quantity 4, one card.',
  'A shift in demand and the new equilibrium are The Market Economy (1-0).')
q(11, [10, 11, 12], [13, 14, 15, 16, 17],
  [T('a/i', 12, 'q11-a-i', '3-3'), T('a/ii', 5, 'q11-a-ii', '1-5'), T('a/iii', 5, 'q11-a-iii', '1-3'),
   T('b/i', 24, 'q11-b-i', '2-0'), T('b/ii', 3, 'q11-b-ii', '2-0'), T('b/iii', 4, 'q11-b-iii', '2-0'),
   T('c/i', 6, 'q11-c-i', '2-0'), T('c/ii', 16, 'q12-c-ii', '0-2')],
  'Eight tasks totalling 75. a(i) Flogas highest and Electric Ireland lowest, 1st @ 8 then 2nd @ 4. a(ii) 5 (six headed); a(iii) 5 (six headed). b(i) 3 x 8: all three labels written out in full (no choice). b(ii) 3 for Q1 and P1 (hidden solution diagram, whole printed question shown). b(iii) 4 for an example and a reason together. c(i) 6 objective tick LESS competitive plus explanation (four headed). c(ii) 2 @ 8 from eleven headed (the ID carries a q12 prefix from the earlier extractor; the citation is Q11(c)(ii)).',
  'Electricity price rises and inflation are Monetary Policy & Inflation (3-3); their effect on firms is Costs of Production, Revenue & Profit (1-5); the €450 credit is Government Intervention (1-3); oligopoly is Market Structures (2-0); household energy use is Sustainability (0-2).')
q(12, [13, 14, 15], [18, 19, 20, 21],
  [T('a/i', 18, 'q12-a-i', '3-2'), T('a/ii', 7, 'q12-a-ii', '3-2'), T('b/i', 4, 'q12-b-i', '0-1'),
   T('b/ii', 10, 'q12-b-ii', '2-1'), T('b/iii', 10, 'q12-b-iii', '2-1'), T('c/i', 6, 'q12-c-i', '3-2'),
   T('c/ii', 10, 'q12-c-ii-unemployment', '3-2'), T('c/iii', 10, 'q12-c-iii', '3-2')],
  'Eight tasks totalling 75. a(i) 18 (6 @ 3) = 2.73% (-1 for %). a(ii) 7 (six headed). b(i) 4, two wordings of scarcity. b(ii) 10 (five headed); b(iii) 10 (seven headed). c(i) 6 trend with figures; c(ii) 10 (two bullets); c(iii) 10 (six bullets).',
  'Employment, unemployment and the unemployment trend are Employment & Unemployment (3-2); scarcity is Scarcity & Choice (0-1); skills shortages and the supply of skilled labour are The Labour Market (2-1).')
q(13, [16, 17, 18], [22, 23, 24, 25, 26],
  [T('a/i', 12, 'q13-a-i', '1-5'), T('a/ii', 16, 'q13-a-ii', '1-5'), T('b/i', 13, 'q13-b-i', '3-3'),
   T('b/ii', 10, 'q13-b-ii', '3-3'), T('c/i', 10, 'q13-c-i', '3-3'),
   T('c/ii/yes', 10, 'q13-c-ii-yes', '0-2'), T('c/ii/no', 10, 'q13-c-ii-no', '0-2'), T('c/iii', 4, 'q13-c-iii', '3-3')],
  'Eight routes; 75 with one route for c(ii). a(i) 12 = axes 2 @ 2, FC 3, VC 5 (hidden solution graph, whole printed question shown). a(ii) 2 @ 8 fixed and variable costs, each explained with an example. b(i) Switzerland lowest and Turkey highest, 1st @ 8 then 2nd @ 5. b(ii) 10 (four headed). c(i) 10 cost-push. c(ii) printed Yes/No tick, the scheme lists both: two routes 10 each. c(iii) 4 (six headed).',
  'Fixed and variable costs are Costs of Production, Revenue & Profit (1-5); food price and cost-push inflation and the ECB are Monetary Policy & Inflation (3-3); environmentally friendly materials are Sustainability (0-2).')
q(14, [19, 20, 21], [27, 28, 29, 30, 31, 32],
  [T('a/i/total', 12, 'q14-a-i', '3-1'), T('a/i/education', 8, 'q14-a-i-education', '3-1'),
   T('a/ii', 4, 'q14-a-ii-eu', '4-1'), T('a/iii', 4, 'q14-a-iii', '3-1'), T('b/i', 7, 'q14-b-i', '3-1'),
   T('b/ii', 7, 'q14-b-ii', '3-1'), T('b/iii/agree', 7, 'q14-b-iii-agree', '3-1'),
   T('b/iii/disagree', 7, 'q14-b-iii-disagree', '3-1'), T('c/i', 16, 'q14-c-i', '4-2'),
   T('c/ii', 10, 'q14-a-ii', '4-2')],
  'Ten routes; 75 with one route for b(iii). a(i) two independently priced calculations: total 12 (5 @ 1 + 7) = €44.22 billion and Education share 8 (3 @ 1 + 5) = 21.78%. a(ii) 4 (eight headed); a(iii) 4. b(i) 7 (five headed); b(ii) 7 objective tick INDIRECT plus explanation; b(iii) printed Agree/Disagree tick, the scheme lists both: two routes 7 each. c(i) 16 = working 4 @ 3 (€62bn) + SURPLUS and explanation 4. c(ii) 1 @ 6 then 1 @ 4 (the ID carries an a-ii suffix from the earlier extractor; the citation is Q14(c)(ii)).',
  'Government spending, the national debt and VAT are Fiscal Policy & the Budget (3-1); the EU budget is Globalisation (4-1); the balance of trade and exports are International Trade & Competitiveness (4-2).')
q(15, [22, 23, 24], [33, 34, 35],
  [T('a', 20, 'q15-a', '0-1'), T('b/i', 15, 'q15-b-i', '1-0'), T('b/ii', 9, 'q15-b-ii', '1-0'),
   T('b/iii', 6, 'q15-b-iii', '1-1'), T('c/i', 20, 'q15-c-i', '1-4'), T('c/ii', 5, 'q15-c-ii', '1-4')],
  'Six tasks totalling 75. a 20 = 3 @ 5 and 1 @ 3, 1 @ 2 across five required blanks (Capital, Labour, Enterprise named; Enterprise and Land explained), one card (hidden solution table, whole printed question shown). b(i) 15 (3 @ 5) supply shifts left (hidden solution diagram); b(ii) 9 explanation; b(iii) 6 substitute good (four wordings). c(i) 20 (10 @ 2) PED = -1.71 (-2 for the sign); c(ii) 5 price elastic with explanation.',
  'Factors of production are Scarcity & Choice (0-1); a supply shift is The Market Economy (1-0); substitute goods are The Consumer (1-1); price elasticity is Elasticity (1-4).')
q(16, [25, 26, 27], [36, 37, 38, 39, 40, 41, 42],
  [T('a/i', 9, 'q16-a-i', '3-5'), T('a/ii', 9, 'q16-a-ii', '2-1'), T('a/iii', 9, 'q16-a-iii', '3-1'),
   T('b/i', 10, 'q16-b-i', '3-1'), T('b/ii/both', 18, 'q16-b-ii-adv', '3-1'),
   T('c/i/positive', 10, 'q16-c-i-pos', '3-4'), T('c/i/negative', 10, 'q16-c-i-neg', '3-4'),
   T('c/ii', 10, 'q16-c-ii', '3-4')],
  'Eight routes; 75 with one route for c(i). a(i)-(iii) 9 each (nine, five and five headed). b(i) 10 (three headed). b(ii) required headings advantage 9 + disadvantage 9, one card (the old disadvantage card resolves by alias). c(i) printed Positive/Negative tick, the scheme ticks both and lists each side: two routes 10 each. c(ii) 10 (four headed).',
  'World population growth is Economic Growth (3-5); older workers are The Labour Market (2-1); ageing and corporation tax are Fiscal Policy & the Budget (3-1); mortgage rules and a new mortgage lender are the Financial Sector (3-4).')

SEL = {
 'Answer 4 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Questions two, three and four contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (a) OR (b); every alternative is its own carded task.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'OR': ('finite-route', 'Separator between the printed (a)/(b) alternatives.'),
}
PAGE_SEL = {
 (4, 'using price competition or non‐price competition. Explain your answer.'): ('answer-classification', 'Q2(a) the scheme ticks non-price competition only; one card.'),
 (5, 'whether you regard each statement below to be true or false.'): ('answer-classification', 'Q3(a) each statement has one correct box (False, True); one card.'),
 (6, 'Indicate by means of a tick (✔) which of the following are either an import into or an export from the'): ('answer-classification', 'Q5 each item has one correct box (export, import); one card.'),
 (6, 'Irish economy. Explain the reason for your choice in each case.'): ('answer-classification', 'Q5 tail of the import/export instruction.'),
 (9, 'Indicate, by means of a tick (✔), whether Diagram A or Diagram B shows its new market equilibrium'): ('answer-classification', 'Q10 the scheme ticks Diagram A only; one card.'),
 (11, 'choice.'): ('not-a-task-selection', 'Q11(b)(iii) "explain a reason for your choice" of an open oligopoly example, not a printed pool.'),
 (12, '(i) In your opinion, is the Irish energy market more competitive or less competitive as a'): ('answer-classification', 'Q11(c)(i) the scheme ticks Less Competitive only; one card.'),
 (12, 'your choice.'): ('answer-classification', 'Q11(c)(i) tail of the tick instruction.'),
 (18, 'Yes No'): ('finite-route', 'Q13(c)(ii) Yes/No boxes; the scheme lists both sides, two routes.'),
 (18, 'below and explain your choice.'): ('finite-route', 'Q13(c)(ii) tail of the Yes/No instruction.'),
 (20, '(ii) Indicate with a tick (✔) below whether VAT is an example of a direct tax or an indirect tax.'): ('answer-classification', 'Q14(b)(ii) the scheme ticks indirect tax only; one card.'),
 (20, 'Explain your choice.'): ('answer-classification', 'Q14(b)(ii) tail of the direct/indirect instruction.'),
 (20, 'Do you agree with the tourism and hospitality industry having a 13.5% VAT rate?'): ('finite-route', 'Q14(b)(iii) agree/disagree; the scheme lists both, two routes.'),
 (20, 'Please tick (✔) your choice.'): ('finite-route', 'Q14(b)(iii) stance tick boxes.'),
 (20, 'Agree Disagree'): ('finite-route', 'Q14(b)(iii) printed stance boxes.'),
 (21, 'Indicate with a tick (✔) whether it was a surplus or a deficit.'): ('answer-classification', 'Q14(c)(i) the balance is objectively a surplus; one card.'),
 (21, 'Answer: Surplus: or Deficit:'): ('answer-classification', 'Q14(c)(i) answer boxes for the objective surplus.'),
 (22, 'Complete the table by either naming or explaining each factor of production.'): ('required-headings', 'Q15(a) every blank cell is required; "naming or explaining" describes which cell is blank, not a choice.'),
 (24, '(ii) Indicate if the demand for a bar of chocolate is price elastic or price inelastic.'): ('answer-classification', 'Q15(c)(ii) the PED of -1.71 is objectively price elastic; one card.'),
 (27, 'has a positive or negative effect on first‐time home buyers / the Irish housing market.'): ('finite-route', 'Q16(c)(i) positive OR negative; the scheme ticks and lists both, two routes.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 32: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# The route tuples must equal the earlier review's, which the Irish review mirrors.
old = json.loads((W / 'scripts/markbank/authoring/reviews/economics-2024-ol-ev.json').read_text())
tup = lambda qs: sorted((x['n'], t['key'], t['cardId'], t['marks'], t['topicId']) for x in qs for t in x['tasks'])
if tup(Q) != tup(old['questions']):
    raise SystemExit('route tuples differ from the reviewed (Irish-mirrored) set')
for x, o in zip(Q, old['questions']):
    assert x['paperPages'] == o['paperPages'], x['n']
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2024, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 33)), 'visuallyInspectedSchemePages': list(range(1, 47)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Re-review 2026-10-12, closing the batch left half-finished at the Codex pause: a fresh paired visual sweep of all 32 paper and 46 scheme pages (scheme PDF page = printed page), counted from the paper and scheme rather than from the earlier cards. {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified; the route set equals the earlier review and the Irish review that mirrors it. Every stem and ask is now sliced from the paper and every menu from the scheme\'s own bullets (econ_2024_ol.py; the Section A script and the correction module are retired). Three split answers stay consolidated with progress aliases (Q1(ii), Q8(ii), Q16(b)(ii) disadvantage). Scheme pp43-45 student research project descriptors and p46 back cover: no written-paper asks. Choose-N rule checked: no printed choose-N-of-M item pool on this paper.',
 'externalClarifications': old.get('externalClarifications', []),
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2024-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
