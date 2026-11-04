"""Write the independent 2025 OL EV census draft from the full visual sweep."""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2025/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2025/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2025-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})
q(1, [3], [6], [T('i', 8, 'sa-q1-i', '3-0'), T('ii', 4, 'sa-q1-ii', '1-1')],
  'i 2@4 Central and Office (Statistics given). ii 4 one benefit of lower electricity prices from five.',
  'The CSO and official statistics belong with national income measurement (NCCA 4.1). Benefits of lower prices to consumers are the consumer (NCCA 2.2).')
q(2, [4], [7], [T('a/yes', 12, 'sa-q2-a-yes', '0-1'), T('a/no', 12, 'sa-q2-a-no', '0-1'), T('b', 12, 'sa-q2-b', '3-1')],
  'Answer (a) or (b). a printed Yes/No tick, the scheme lists both: two routes 12 each. b 12 current budget surplus definition.',
  'Efficient use of scarce resources is scarcity and choice (NCCA 1.2). The current budget surplus is fiscal policy (NCCA 4.2).')
q(3, [5], [8, 9], [T('a/private', 12, 'sa-q3-a-private', '2-2'), T('a/social', 12, 'sa-q3-a-social', '2-2'),
                   T('b/agree', 12, 'sa-q3-b-agree', '3-5'), T('b/disagree', 12, 'sa-q3-b-disagree', '3-5')],
  'Answer (a) or (b). a printed private OR social benefit tick, both lists in the scheme: two routes 12 each. b Agree/Disagree: two routes 12 each.',
  'Private and social benefits of libraries are externalities (NCCA 3.3). Benefits and costs of hosting events are growth outcomes (NCCA 4.6).')
q(4, [6], [10], [T('a', 12, 'sa-q4-a', '3-1'), T('b', 12, 'sa-q4-b', '3-1')],
  'Answer (a) or (b). a 12 one reason from four. b 12 objective tick (the scheme ticks Yes) plus explanation, one card.',
  'Tax-band changes, USC cuts and cost-of-living payments are fiscal policy (NCCA 4.2).')
q(5, [7], [11], [T('i', 4, 'sa-q5-i', '3-0'), T('ii', 8, 'sa-q5-ii', '3-5')],
  'i 4 Gross Domestic (Product given). ii 8 one advantage of rising GDP from six.',
  'GDP is national income (NCCA 4.1); the advantages of growth are economic growth (NCCA 4.6).')
q(6, [7], [12], [T('all', 12, 'sa-q6-private', '2-2')],
  'One 12 cell, 1st x 8 and 2nd x 4, for one private cost AND one social cost: both required, no fixed share for either heading, so one card (the old social-cost card resolves by alias).',
  'Private and social costs of vaping are externalities and market failure (NCCA 3.3).')
q(7, [8], [13], [T('i', 4, 'seca-q7-i', '3-1'), T('ii', 8, 'sa-q7-ii', '3-1')],
  'i 4 = 41.3% (fraction working, hidden solution crop). ii 8 one effect for the Government from six.',
  'The fiscal cost of an ageing population (pensions, health spending, tax revenue) is fiscal policy (NCCA 4.2).')
q(8, [9], [14], [T('i-ii', 12, 'seca-q8-i-ticks', '2-0')],
  'The scheme prints one 1st x 8 / 2nd x 4 cell beside (i) and nothing beside (ii): the tick (An Post) and one barrier to entry share one 12, so one card (the old barrier card resolves by alias; the old tick card carried 12 for the tick alone).',
  'Monopoly and barriers to entry are market structures (NCCA 3.1).')
q(9, [9], [15], [T('all', 12, 'seca-q9-ticks', '1-1')],
  '2 @ 6: iPhone 16 complement and Samsung Galaxy Watch 7 substitute, each with its reason (objective classifications).',
  'Substitutes and complements are the consumer and demand (NCCA 2.2).')
q(10, [10], [16], [T('i', 8, 'sa-q10-i', '1-1'), T('ii', 4, 'sa-q10-ii', '1-2')],
  'i 8 one factor other than price from five. ii 4 the vertical supply curve at the 82,300 capacity.',
  'Determinants of demand are the consumer (NCCA 2.2). Fixed supply is the firm and supply (NCCA 2.3).')
q(11, [11, 12, 13], [17, 18, 19],
  [T('a/i', 6, 'q11-a-i', '2-0'), T('a/ii', 14, 'q11-a-ii', '2-0'),
   T('b/i', 24, 'q11-b-i', '2-0'),
   T('b/ii', 4, 'q11-b-ii', '2-0'), T('b/iii', 4, 'q11-b-iii', '2-0'),
   T('c/i', 10, 'q11-c-i', '2-2'), T('c/ii', 13, 'q11-c-ii', '2-2')],
  'Seven tasks totalling 75. a(i) one 6 cell for meaning and example. a(ii) 1st x 10, 2nd x 4. b(i) "any three of the following four labels", 3 @ 8: the student chooses which three and the scheme prices every label alike, so one card whose menu lists all four labels with a claim of three (coordinator rule 2026-10-12; the three branch-only combination cards from the first pass are retired, never on main). b(ii) 4 for Q1 and P1 (hidden solution diagram). b(iii) 4 (the old card priced it 8). c(i) 10 (the old card priced it 8). c(ii) 1st x 7, 2nd x 3, 3rd x 3 across three required headings, one card.',
  'Perfect competition, homogeneous products, its diagram and its consumer advantages are market structures (NCCA 3.1). A passenger cap and its effects are government intervention against negative externalities (NCCA 3.3).')
q(12, [14, 15, 16], [20, 21, 22],
  [T('a/i', 16, 'q12-a-i', '3-1'), T('a/ii', 5, 'q12-a-ii', '3-1'), T('b/i', 12, 'q12-b-i', '3-0'),
   T('b/ii', 12, 'q12-b-ii', '3-0'), T('b/iii', 4, 'q12-b-iii', '3-0'), T('c/i', 12, 'q12-c-i', '3-3'),
   T('c/ii', 4, 'q12-c-ii', '3-3'), T('c/iii', 10, 'q12-c-iii', '3-4')],
  'Eight tasks totalling 75. a(i) 16 = 14.14% with the scheme marks printed on the working (hidden solution crop). a(ii) 5 objective tick (capital) plus explanation. b(i) 12 for C, G and X. b(ii) 12 = 4 @ 3, multiplier 2. b(iii) 4. c(i) 3 @ 4 European Central Bank. c(ii) 4. c(iii) 1st x 6, 2nd x 4 across savers AND borrowers, one card.',
  'Government expenditure is fiscal policy (NCCA 4.2). National income, the multiplier and the open economy are NCCA 4.1. The ECB is monetary policy (NCCA 4.4); interest-rate effects on savers and borrowers are the financial sector (NCCA 4.5).')
q(13, [17, 18, 19], [23, 24, 25, 26],
  [T('a/i', 7, 'q13-a-i', '2-1'), T('a/ii', 12, 'q13-a-ii', '2-1'),
   T('a/iii/government', 7, 'q13-a-iii-gov', '2-1'), T('a/iii/employers', 7, 'q13-a-iii-emp', '2-1'),
   T('b/i', 17, 'q13-b-i', '1-5'), T('b/ii/mc', 6, 'q13-b-ii', '1-5'), T('b/ii/mr', 6, 'q13-b-ii-mr', '1-5'),
   T('c/i', 12, 'q13-c-i', '4-1'), T('c/ii', 14, 'q13-c', '3-1')],
  'Nine routes; 75 with one route per tick. a(i) 7. a(ii) 1st @ 8, 2nd @ 4. a(iii) government OR employers tick, both lists: two routes 7 each. b(i) 17 = axes 2 @ 2, AC 5, MC 5, MR 3 (hidden solution graph). b(ii) marginal cost OR marginal revenue tick: two routes 6 each (the old card keeps its ID as the MC route). c(i) 1st @ 8, 2nd @ 4 two MNCs (missing before). c(ii) 2 @ 7 (the old card cited Q13(c)).',
  'Labour and skills shortages are the labour market (NCCA 3.2). Cost and revenue curves are NCCA 2.3 (deck 2.6). MNCs are globalisation (NCCA 5.2). Infrastructure spending is fiscal policy (NCCA 4.2).')
q(14, [20, 21, 22], [27, 28, 29, 30, 31, 32],
  [T('a/i', 6, 'q14-a-i', '4-2'), T('a/ii', 16, 'q14-a-ii', '4-2'), T('a/iii', 4, 'q14-a-iii', '4-2'),
   T('b/i/positive', 16, 'q14-b-i-positive', '4-0'), T('b/i/negative', 16, 'q14-b-i-negative', '4-0'),
   T('b/ii', 10, 'q14-c', '4-0'), T('c/i', 13, 'q14-c-i', '4-0'), T('c/ii', 10, 'q14-c-ii', '4-0')],
  'Eight routes; 75 with one route for (b)(i). a(i) 6. a(ii) 1st @ 10, 2nd @ 6. a(iii) 4. b(i) one 16 cell for the trend comment and a positive OR negative development, both lists in the scheme: two routes 16 each (missing before). b(ii) 1st @ 6, 2nd @ 4 (the old card cited Q14(b)). c(i) 13 objective tick (improved) plus two figures. c(ii) 10.',
  'Customs duties, imports and EU enlargement are international trade (NCCA 5.3). Overseas aid, welfare in LDCs and the HDI are growth and development (NCCA 5.1).')
q(15, [23, 24, 25], [33, 34, 35, 36, 37],
  [T('a/i', 10, 'q15-a-i-entrepreneur', '1-5'), T('a/ii', 4, 'q15-a-ii', '1-5'), T('a/iii', 10, 'q15-a-iii', '3-5'),
   T('b/i', 14, 'q15-b-i', '1-0'), T('b/ii', 10, 'q15-b-ii', '1-0'),
   T('b/iii/positive', 6, 'q15-b-iii-pos', '2-2'), T('b/iii/negative', 6, 'q15-b-iii-neg', '2-2'),
   T('c/i', 14, 'q15-a-i', '3-1'), T('c/ii', 7, 'q15-c-ii', '1-0')],
  'Nine routes; 75 with one route for (b)(iii). a(i) 10. a(ii) 4 objective tick (the scheme ticks Agree and prints no disagree answer), one card. a(iii) 10. b(i) 8 + 4 + 2 (hidden solution diagram). b(ii) 10. b(iii) positive OR negative tick: two routes 6 each. c(i) 1st @ 8, 2nd @ 6 across government AND citizens, one card. c(ii) 7.',
  'Entrepreneurs and their costs are the firm (NCCA 2.3, deck 2.6). Closures and local communities are growth outcomes (NCCA 4.6). Housing demand is the market economy (NCCA 2.1). Traffic restrictions address negative externalities (NCCA 3.3). Debt reduction is fiscal policy (NCCA 4.2); a mixed economy is the market economy (NCCA 2.1).')
q(16, [26, 27, 28], [38, 39, 40, 41, 42],
  [T('a/i', 4, 'q16-a-i', '3-1'), T('a/ii', 10, 'q16-a-ii', '3-1'), T('a/iii', 8, 'q16-a-iii-excise', '3-1'),
   T('b/i', 5, 'q16-b-i', '3-3'), T('b/ii', 12, 'q16-b-ii', '3-3'), T('b/iii', 12, 'q16-a-iii', '3-3'),
   T('c/i', 18, 'q16-b-i-ag', '0-2'), T('c/ii', 6, 'q16-c-ii', '3-1')],
  'Eight tasks totalling 75. a(i) 4 objective tick (indirect). a(ii) 10. a(iii) 8 (the paper asks about VAT). b(i) 1st @ 3, 2nd @ 2 Consumer and Price. b(ii) 12. b(iii) 1st @ 8, 2nd @ 4. c(i) 2 @ 6 for one agricultural AND one industrial action plus a 6 justification, one 18 card (the old industrial-only card resolves by alias; the justification was missing). c(ii) 6.',
  'Excise duty and VAT are fiscal policy (NCCA 4.2). CPI and falling inflation are the price level (NCCA 4.4). Climate action by sector is sustainability (NCCA 1.3). Balanced regional development is fiscal policy (NCCA 4.2).')

SEL = {
 'Answer 4 out of 6 quesƟons.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 8 out of 10 quesƟons from this secƟon.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 8 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'QuesƟons 2, 3 and 4 contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (a) OR (b); every alternative is its own carded task.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer (a) or (b)': ('finite-route', 'Printed alternative pair; (a) and (b) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (a)/(b) alternatives.'),
 'Agree Disagree': ('finite-route', 'Printed two-box stance; the scheme lists both sides (or ticks one, recorded per question), each stance carded accordingly.'),
}
PAGE_SEL = {
 (4, 'Yes No'): ('finite-route', 'Q2(a) Yes/No: the scheme lists both sides, two routes.'),
 (5, '(a) Outline one private benefit or social benefit of the increased use of public libraries.'): ('finite-route', 'Q3(a) private OR social benefit: both lists in the scheme, two routes.'),
 (5, 'Indicate with a tick (✔) if you agree or disagree with this statement. Justify your answer.'): ('finite-route', 'Q3(b) agree/disagree routes.'),
 (6, 'Yes No'): ('answer-classification', 'Q4(b) the scheme ticks Yes only; one card.'),
 (9, '(i) Identify, with a tick (✔), which one of the following firms exist in a monopoly market'): ('answer-classification', 'Q8(i) one correct tick (An Post).'),
 (9, 'In the table below, indicate by means of a tick (✔) which of the following are either a substitute to'): ('answer-classification', 'Q9 each item has one correct box.'),
 (9, 'or a complement for the Apple Watch series 10. Explain the reason for your choice in each case.'): ('answer-classification', 'Q9 each item has one correct box.'),
 (10, '82,300 No. of Tickets'): ('not-a-task-selection', 'Axis label text in the Q10 diagram.'),
 (12, '(i) Write out in full what any three of the following four labels represent.'): ('finite-route', 'Q11(b)(i) choose any three of four labels, all priced 8: one card with a claim-three menu of all four.'),
 (13, 'passengers that can pass through the airport in any given year). This passenger cap was'): ('not-a-task-selection', 'Stem wording ("any given year"), not a selection.'),
 (14, 'Indicate with a tick () whether the above is an example of current or capital'): ('answer-classification', 'Q12(a)(ii) the scheme ticks capital only; one card.'),
 (17, '(iii) Outline one economic measure the Irish government or employers could take to'): ('finite-route', 'Q13(a)(iii) government OR employers: both lists, two routes.'),
 (18, '(ii) Explain the meaning of either of the following terms:'): ('finite-route', 'Q13(b)(ii) marginal cost OR marginal revenue: two routes.'),
 (18, 'marginal cost or marginal revenue.'): ('finite-route', 'Q13(b)(ii) the two printed terms.'),
 (19, 'Justify your choice in each case.'): ('not-a-task-selection', 'Instruction to justify each of two open areas; not a selection.'),
 (21, 'In your opinion, is this trend a positive development or a negative development?'): ('finite-route', 'Q14(b)(i) positive OR negative: both lists, two routes.'),
 (21, 'Is this trend a Positive development or a Negative development'): ('finite-route', 'Q14(b)(i) the printed tick boxes.'),
 (22, "(i) Based on the data in the table above, state if Ireland's HDI position has improved or"): ('answer-classification', 'Q14(c)(i) the scheme ticks Improved only; one card.'),
 (23, 'Agree Disagree'): ('answer-classification', 'Q15(a)(ii) the scheme ticks Agree and prints no disagree answer; one card.'),
 (23, 'Do you agree or disagree with this statement?'): ('answer-classification', 'Q15(a)(ii) Agree only in the scheme.'),
 (23, 'Indicate your choice with a tick () in the corresponding box below.'): ('answer-classification', 'Q15(a)(ii) tick box with one credited answer.'),
 (24, 'Outline one positive effect or one negative effect of the above measure for those'): ('finite-route', 'Q15(b)(iii) positive OR negative: both lists, two routes.'),
 (24, 'people who live in Dublin. Indicate your choice with a tick () in the corresponding'): ('finite-route', 'Q15(b)(iii) the printed tick boxes.'),
 (26, 'tax or an indirect tax. Explain your choice.'): ('answer-classification', 'Q16(a)(i) the scheme ticks indirect only; one card.'),
 (28, '(ii) One of the aims of the Irish government is to promote Balanced Regional'): ('not-a-task-selection', 'Stem wording ("One of the aims"), not a selection.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 32: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2025, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-11',
 'visuallyInspectedPaperPages': list(range(1, 33)), 'visuallyInspectedSchemePages': list(range(1, 48)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Census from the paired visual sweep of all 32 paper and 47 scheme pages, checked against the 68 cards the earlier extractors shipped. {len(tasks)} routes ({sum(1 for x in Q if int(x["n"]) <= 10 for _ in x["tasks"])} Section A + {sum(1 for x in Q if int(x["n"]) > 10 for _ in x["tasks"])} Section B), {len(sels)} raw directive lines classified. Three cards that held one part of a jointly priced answer are withdrawn with progress aliases (Q6 social cost, Q8(ii) barrier, Q16(c)(i) industrial action); four routes are added (the Q13(b)(ii) marginal revenue route, Q13(c)(i), and the two Q14(b)(i) routes). Q11(b)(i) "any three of four labels" is one card with a claim-three menu of all four labels. Q11(b)(iii) and Q11(c)(i) tariffs corrected to 4 and 10. Scheme PDF pp43-46 student research project descriptors, p47 back cover: no written-paper asks.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2025-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
