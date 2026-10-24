"""Write the independent 2023 OL EV census draft from the full visual sweep (re-review 2026-10-12).

The route set is the one the 2023 Ordinary Irish review mirrors task for task
(econ_review.validate_equivalences), so every (key, card, marks, topic) tuple
must equal the earlier review's; the sweep confirmed each one. Boundary and
topic reasons are re-written from this sweep.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2023/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2023/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2023-ol-'
old = json.loads((W / 'scripts/markbank/authoring/reviews/economics-2023-ol-ev.json').read_text())
atlas = json.loads((W / 'data/examTopics/economics-sec-topic-reviews.json').read_text())
OLD_NODES = {q['n']: q['canonicalNodeIds'] for q in atlas['questions']
             if q['year'] == 2023 and q['level'] == 'ordinary' and q['lang'] == 'ev'}
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + OLD_NODES.get(str(n), [])))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [5], [T('i', 8, 'sa-q1-i', '3-2'), T('ii', 4, 'seca-q1-ii', '3-2')],
  '(i) 8 July 2022 (4.3%, the first month plotted). (ii) 4 one comment with figures: the scheme gives an overall trend (4.3% to 4.4%) and a month-by-month alternative.',
  'The unemployment rate and its trend are Employment & Unemployment (3-2).')
q(2, [4], [6], [T('a', 12, 'sa-q2-a', '3-4'), T('b', 12, 'sa-q2-b', '3-4')],
  'Answer (a) OR (b); the stem tariff 1st @ 8, 2nd @ 4 covers whichever is answered. a two effects on consumers of the bank exits (six bullets); b two Central Bank functions (eight bullets).',
  'Retail banking competition and the Central Bank are Financial Sector (3-4).')
q(3, [5], [7], [T('a/i', 8, 'sa-q3-a-i', '2-1'), T('a/ii', 4, 'sa-q3-a-ii', '2-1'), T('b', 12, 'sa-q3-b', '2-1')],
  'Answer (a) OR (b). a(i) 8 one area short of skills (five sectors) and a(ii) 4 one effect (six bullets) are separately priced. b two measures 1st @ 8, 2nd @ 4 (six bullets).',
  'Skills shortages and measures to address them are The Labour Market (2-1).')
q(4, [6], [8], [T('a/i', 8, 'seca-q4-a-i', '2-0'), T('a/ii', 4, 'sa-q4-a-ii', '2-0'), T('b', 12, 'sa-q4-b', '2-0')],
  'Answer (a) OR (b). a(i) 8 objective tick Iarnród Éireann (Irish Rail) and a(ii) 4 explain monopoly (three sentences of one idea), separately priced. b two characteristics 1st @ 8, 2nd @ 4 (four bullets).',
  'Monopoly identification, definition and characteristics are Market Structures (2-0).')
q(5, [7], [9], [T('whole', 12, 'sa-q5', '1-2')],
  'One 12: explain the relationship shown by the printed vertical S1 (fixed, perfectly inelastic ticket supply). No drawing is asked.',
  'Fixed-capacity ticket supply is The Firm (Supply) (1-2).')
q(6, [7], [9], [T('i', 8, 'sa-q6-i', '3-0'), T('ii', 4, 'sa-q6-ii', '3-5')],
  '(i) 2 @ 4 Domestic and Product, Gross printed. (ii) 4 one advantage of rising GDP (six bullets).',
  'GDP is National Income (3-0); the advantages of its growth are Economic Growth (3-5).')
q(7, [8], [10], [T('whole', 12, 'sa-q7', '3-1')],
  'Two reasons the government collects tax, 1st @ 8, 2nd @ 4 (five bullets).',
  'Why the government taxes is Fiscal Policy & the Budget (3-1).')
q(8, [8], [10], [T('i', 6, 'sa-q8-i', '4-0'), T('ii', 6, 'sa-q8-ii', '4-0')],
  '(i) Gross National Income is printed, so both education and life expectancy are required, priced together 1st @ 4, 2nd @ 2: not a choose-two-of-three pool. (ii) area of expenditure and explanation, 1st @ 4, 2nd @ 2. The paper says eighth; the scheme repeats second.',
  'The HDI and the spending behind it are Growth & Development (4-0).')
q(9, [9], [11], [T('i+ii', 12, 'sa-q9', '0-1')],
  'One 1st @ 8, 2nd @ 4 prints beside (i) and covers both parts: the definition and the housing-spend opportunity cost are one card with unpriced rows.',
  'Opportunity cost is Scarcity & Choice (0-1).')
q(10, [9], [11], [T('whole', 12, 'sa-q10-private', '0-1')],
  'One private AND one social benefit priced together 1st @ 8, 2nd @ 4, one card with unpriced rows; the old social-benefit card resolves by alias.',
  'Private and social benefits are Scarcity & Choice (0-1); vaping as a demerit good is also Market Failure (2-2).')
q(11, [10, 11, 12], [12, 13, 14],
  [T('a/i', 10, 'q11-a-i', '2-0'), T('a/ii', 10, 'q11-a-ii', '2-0'), T('b/i', 24, 'q11-b-i', '2-0'),
   T('b/ii', 9, 'q11-b-ii', '2-0'), T('b/iii', 2, 'q11-b-iii', '2-0'), T('c/i', 10, 'q11-c-i', '3-0'),
   T('c/ii', 10, 'q11-c-ii', '3-0')],
  'Seven tasks totalling 75. a(i) and a(ii) 1st @ 6, 2nd @ 4. b(i) 3 @ 8 average cost, average revenue / demand, quantity; b(ii) 9 = 1st @ 4, 2nd @ 4, 3rd @ 1 for Q1, P1, C1 (hidden solution, whole printed question shown); b(iii) objective No 1 + reason 1. c(i) explanation 6 + one other example 4; c(ii) required business AND government effects priced 1st @ 6, 2nd @ 4, one card.',
  'Monopolistic competition and its long-run equilibrium are Market Structures (2-0); the hidden economy is National Income (3-0), its tax effects also Fiscal Policy & the Budget (3-1).')
q(12, [13, 14, 15], [15, 16],
  [T('a/i', 16, 'q12-a-i', '3-1'), T('a/ii', 12, 'q12-a-ii', '3-1'), T('b/i', 8, 'q12-b-i', '3-1'),
   T('b/ii', 12, 'q12-b-ii', '3-1'), T('c/i', 10, 'q12-c-i', '1-3'), T('c/ii', 14, 'q12-c-ii', '0-2'),
   T('c/iii', 3, 'q12-c-iii', '0-2')],
  'Seven tasks totalling 75. a(i) 6 @ 2 + answer 4 = €95 million; a(ii) 4 @ 3 = 28.94%. b(i) 8 equity; b(ii) 1st @ 8, 2nd @ 4 two other principles. c(i) 10 one benefit of the credit; c(ii) 1st @ 10, 2nd @ 4; c(iii) one 3 for the three pillars, no split.',
  'Government revenue and the principles of taxation are Fiscal Policy & the Budget (3-1); the electricity credit is Government Intervention (1-3); household energy choices and the pillars are Sustainability (0-2).')
q(13, [16, 17, 18], [17, 18, 19],
  [T('a/i', 12, 'q13-a-i', '4-2'), T('a/ii', 10, 'q13-a-ii', '4-2'), T('b/i', 8, 'q13-b-i', '3-0'),
   T('b/ii/income', 18, 'q13-b-ii', '3-0'), T('b/ii/trade', 9, 'q13-b-ii-trade', '4-2'),
   T('c/i', 8, 'q13-c-i', '3-3'), T('c/ii', 8, 'q13-c-ii', '3-3'), T('c/iii', 2, 'q13-c-iii', '3-4')],
  'Eight tasks totalling 75. a(i) 2019 and 2016 priced 1st @ 8, 2nd @ 4, one card; a(ii) 1st @ 8, 2nd @ 2. b(i) 2 @ 4 C and G. b(ii) two separately priced calculations under one printed part: national income 18 (6 @ 3) €1,400m and balance of trade 9 (3 @ 3) €100m. c(i) 8; c(ii) 8 (savings may rise, fall or stay unchanged); c(iii) 2.',
  'Exports and the balance of trade are International Trade & Competitiveness (4-2); the national income formula is National Income (3-0); ECB rate rises are Monetary Policy & Inflation (3-3); switching to Revolut is Financial Sector (3-4).')
q(14, [19, 20, 21], [20, 21, 22],
  [T('a/i', 10, 'q14-a-i', '3-3'), T('a/ii', 12, 'q14-a-ii-reason', '3-3'), T('b/i', 18, 'q14-b-i', '1-5'),
   T('b/ii', 9, 'q14-b-ii', '1-5'), T('b/iii', 3, 'q14-b-iii', '1-2'), T('c/i', 18, 'q14-c-i', '1-5'),
   T('c/ii', 5, 'q14-c-ii', '1-5')],
  'Seven tasks totalling 75. a(i) 10 (6+4) one trend with figures, two scheme alternatives (the graph is in cent); a(ii) required reason AND consumer effect priced 1st @ 8, 2nd @ 4, one card (the old effect card resolves by alias). b(i) 3 @ 6 €6,000; b(ii) 3 @ 3 €1,500; b(iii) 3. c(i) fixed 6 + example 3, variable 6 + example 3; c(ii) 5.',
  'Petrol prices and their effects are Monetary Policy & Inflation (3-3); revenue, profit and costs are Costs of Production, Revenue & Profit (1-5); the parts shortage is The Firm (Supply) (1-2).')
q(15, [22, 23, 24], [23, 24, 25],
  [T('a/i', 20, 'q15-a-i-percentage', '1-1'), T('a/ii', 5, 'q15-a-ii', '1-3'), T('b/i', 16, 'q15-b-i', '1-1'),
   T('b/ii', 9, 'q15-b-ii', '1-1'), T('b/iii', 5, 'q15-b-iii', '1-1'), T('c/i', 12, 'q15-a-i', '1-3'),
   T('c/ii', 8, 'q15-c-ii', '0-2')],
  'Seven tasks totalling 75. a(i) 5 @ 4 = 81.32%; a(ii) 5 subsidy. b(i) 4 @ 4 the demand curve with axes (hidden solution); b(ii) shift right 6 + explanation 3; b(iii) 5. c(i) 1st @ 8, 2nd @ 4 (the ID carries an a suffix; the citation is Q15(c)(i)); c(ii) 8.',
  'Vehicle demand data and the demand curve are The Consumer (1-1); subsidies and EV incentives are Government Intervention (1-3); the social benefit of cleaner cars is Sustainability (0-2).')
q(16, [25, 26, 27], [26, 27, 28],
  [T('a/i', 24, 'q16-a-i-factors', '0-1'), T('a/ii', 6, 'q16-a-ii', '0-1'), T('b/i', 14, 'q16-a-i', '0-1'),
   T('b/ii', 7, 'q16-b-ii', '1-5'), T('c/i', 8, 'q16-c-i', '0-2'), T('c/ii', 8, 'q16-c-ii', '0-2'),
   T('c/iii', 8, 'q16-c-iii', '0-2')],
  'Seven tasks totalling 75. a(i) 6 @ 4 the six blank table cells (hidden completed table, whole printed question shown); a(ii) objective Yes 2 + explanation 4. b(i) any two of scarce, transferable and utility, 2 @ 7, one card with a claim-two menu (coordinator rule 2026-10-12: no card per combination; the ID carries an a suffix, the citation is Q16(b)(i)); b(ii) 7. c(i), c(ii), c(iii) 8 each.',
  'Factors of production, the entrepreneur and economic goods are Scarcity & Choice (0-1); economies of scale are Costs of Production, Revenue & Profit (1-5); food waste is Sustainability (0-2).')

SEL = {
 'Answer 4 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Questions two, three and four contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (a) OR (b); every alternative is its own carded task.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer either (a) or (b)': ('finite-route', 'Printed alternative pair; (a) and (b) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (a)/(b) alternatives.'),
}
PAGE_SEL = {
 (6, '(a) (i) Identify, with a tick (), which one of the following firms exist in a monopoly market'): ('answer-classification', 'Q4(a)(i) the scheme ticks Irish Rail only; one card.'),
 (8, '(i) Name two of the three areas (elements) that the Human Development Index (HDI)'): ('required-headings', 'Q8(i) GNI is printed, so the two remaining elements are both required; not a choose-two-of-three pool.'),
 (11, '(iii) Is the above firm producing efficiently? Yes: No:'): ('answer-classification', 'Q11(b)(iii) the scheme answers No only; one card.'),
 (14, '(b) (i) Equity is one of the principles of a good tax system. Explain the term equity.'): ('not-a-task-selection', 'Stem wording ("one of the principles"), not a selection.'),
 (20, 'Total Profit or Loss -€500 €500'): ('not-a-task-selection', 'Table heading ("profit or loss"), not a selection.'),
 (25, 'It is one of the fastest growing food manufacturers in Ireland.'): ('not-a-task-selection', 'Stem wording ("one of the fastest"), not a selection.'),
 (26, '(i) Explain any two of the above terms.'): ('finite-route', 'Q16(b)(i) a closed pool of three terms, any two, each priced 7: one card whose claim-two menu lists all three (coordinator rule 2026-10-12).'),
 (26, 'economy? Explain your answer. Yes: No:'): ('answer-classification', 'Q16(a)(ii) the scheme answers Yes only (2 + explanation 4); one card.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 32: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# The route tuples must equal the earlier review's, which the Irish review mirrors.
tup = lambda qs: sorted((x['n'], t['key'], t['cardId'], t['marks'], t['topicId']) for x in qs for t in x['tasks'])
if tup(Q) != tup(old['questions']):
    raise SystemExit(f'route tuples differ: +{set(tup(Q)) - set(tup(old["questions"]))} -{set(tup(old["questions"])) - set(tup(Q))}')
for x, o in zip(Q, old['questions']):
    assert x['paperPages'] == o['paperPages'], x['n']
    assert x['schemePages'] == o['schemePages'], x['n']
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2023, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 33)), 'visuallyInspectedSchemePages': list(range(1, 33)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Re-review 2026-10-12 from a fresh paired visual sweep of all 32 paper and 32 scheme pages (scheme PDF page = printed page + 2; the unnumbered annotation table is PDF page 4). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified; the route set equals the earlier review and the Irish review that mirrors it. Every stem and ask is now sliced from the paper and every menu from the scheme\'s own bullets (econ_2023_ol.py; the Section A script and the correction module are retired). Two split answers stay consolidated with progress aliases (Q10 social benefit, Q14(a)(ii) effect). Q16(b)(i) any two of three terms is one claim-two card. Scheme pp29-31 student research project descriptors and p32 back cover: no written-paper asks. Choose-N rule checked: Q16(b)(i) is the only printed choose-N-of-M pool on this paper.',
 'externalClarifications': old.get('externalClarifications', []),
 'curriculumSource': old.get('curriculumSource', 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf'),
}
if 'targetedIrishEvidence' in old:
    draft['targetedIrishEvidence'] = old['targetedIrishEvidence']
out = W / 'scripts/markbank/authoring/drafts/economics-2023-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']), x['canonicalNodeIds'])
