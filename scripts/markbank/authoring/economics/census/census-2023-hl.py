"""Write the independent 2023 HL EV census draft from the full visual sweep (re-review 2026-10-12).

Route set: the earlier review's, except Q16(a). The scheme prints four cells for
Q16(a)(i)-(ii): 4 and 4 beside the two definitions, 7 beside the diagram and 8
beside the explanation, so (i) individual/market demand (4 + 4) and (ii) the
car-market diagram and explanation (7 + 8) are separately priced printed parts
and are two tasks. The 2023 Higher Irish review mirrors that route change only.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2023/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2023/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2023-hl-'
old = json.loads((W / 'scripts/markbank/authoring/reviews/economics-2023-hl-ev.json').read_text())
atlas = json.loads((W / 'data/examTopics/economics-sec-topic-reviews.json').read_text())
OLD_NODES = {q['n']: q['canonicalNodeIds'] for q in atlas['questions']
             if q['year'] == 2023 and q['level'] == 'higher' and q['lang'] == 'ev'}
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + OLD_NODES.get(str(n), [])))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [5], [T('a', 6, 'sa-q1-a', '1-2'), T('b', 6, 'sa-q1-b', '2-0')],
  'a diagram 3 (vertical supply) + explanation 3 (three bullets), one card. b 2 @ 3 from six headed conditions.',
  'Fixed-capacity ticket supply is The Firm (Supply) (1-2); price discrimination is Market Structures (2-0).')
q(2, [4], [6, 7], [T('a', 6, 'sa-q2-a', '1-4'), T('b', 6, 'sa-q2-b', '1-4'), T('c', 6, 'sa-q2-c-adv', '3-1')],
  'a objective tick PRICE INELASTIC 1 + explanation 5. Answer (b) 2 @ 3 (four bullets) OR (c) 2 @ 3 required headings Advantage AND Disadvantage, one card; the old disadvantage card resolves by alias.',
  'Price elasticity of petrol and its uses are Elasticity (1-4); the excise-duty decision is Fiscal Policy & the Budget (3-1) and Government Intervention (1-3).')
q(3, [5], [8], [T('a', 6, 'sa-q3-a', '1-1'), T('b', 6, 'sa-q3-b', '1-1'), T('c', 6, 'seca-q3-c', '1-1')],
  'a 6 three utility cells and workings (hidden solution, whole printed question shown). Answer (b) 6 (third unit; MU 40 to 35) OR (c) 6 objective No (180 against 360); the formula is shown as a data crop.',
  'Total and marginal utility and the equi-marginal principle are The Consumer (1-1).')
q(4, [6], [9], [T('a', 6, 'sa-q4-a', '1-5'), T('b', 6, 'sa-q4-b', '1-5'), T('c', 6, 'sa-q4-c', '1-5')],
  'a 6 four cost cells (hidden solution, whole printed question shown). Answer (b) 6 objective DISAGREE (cover average variable costs) OR (c) 6 MC/AC relationships.',
  'Average and marginal cost and the short-run shutdown condition are Costs of Production, Revenue & Profit (1-5).')
q(5, [7], [10], [T('a', 6, 'sa-q5-a', '0-1'), T('b', 6, 'sa-q5-b', '0-1')],
  'a one 6 cell for three objective letters (C efficient, A inefficient, B impossible). b one 6 cell justifying all three.',
  'The production possibilities frontier is Scarcity & Choice (0-1).')
q(6, [8], [11], [T('a', 6, 'seca-q6-a', '3-1'), T('b', 6, 'sa-q6-b', '3-1')],
  'a 6 three objective ticks (VAT indirect, PAYE direct, customs and excise indirect). b one 6 cell for three canons from six bullets, no per-canon split.',
  'Direct and indirect taxes and the canons of taxation are Fiscal Policy & the Budget (3-1).')
q(7, [9], [12], [T('a', 6, 'sa-q7-a', '1-0'), T('b', 6, 'sa-q7-b', '1-3')],
  'a diagram 3 (supply left S to S1) + explanation 3 (hidden solution, whole printed question shown); the scheme bullets say S1 to S2 against its own diagram. b one 6 cell for two reasons, no split.',
  'The rental supply shift is The Market Economy (1-0); the vacant property tax is Government Intervention (1-3).')
q(8, [10], [13], [T('a', 6, 'sa-q8-a', '3-3'), T('b', 6, 'sa-q8-b', '3-3')],
  'a 6 justify the rate rises (inflation). b 6 objective YES with one of four explanations.',
  'ECB interest rates and Eurozone monetary policy are Monetary Policy & Inflation (3-3).')
q(9, [11], [13], [T('a', 6, 'sa-q9-a', '1-5'), T('b', 6, 'sa-q9-b', '1-5')],
  'a 6 law of diminishing marginal returns. b one 6 cell for two cost advantages, no split.',
  'Diminishing returns and the cost advantages of specialisation are Costs of Production, Revenue & Profit (1-5); specialisation is also Scarcity & Choice (0-1).')
q(10, [12], [14], [T('B', 6, 'sa-q10', '3-0'), T('C', 6, 'sa-q10-c', '3-0')],
  'A (GNP €323bn) is completed on the paper and is not a task. B 6 GNI = 323 + 1.7 - 0.5 = €324.2bn and C 6 modified GNI = 324.2 - 89 = €235.2bn, 2 @ 6.',
  'GNI and modified GNI are National Income (3-0).')
q(11, [13, 14, 15, 16], [15, 16, 17, 18],
  [T('a/i', 8, 'q11-a-i', '3-5'), T('a/ii', 10, 'q11-a-ii', '3-5'), T('a/iii', 10, 'q11-a-iii-neg', '3-1'),
   T('b/i', 6, 'q11-b-i', '2-1'), T('b/ii', 9, 'q11-b-ii', '2-1'), T('b/iii', 9, 'q11-b-iii', '2-1'),
   T('c/i', 5, 'q11-c-i', '4-0'), T('c/ii', 9, 'q11-c-ii', '3-1'), T('c/iii', 9, 'q11-c-iii', '3-1')],
  'Nine tasks totalling 75. a(i) 8 = 7.59% (-1 for %; hidden working, whole printed question shown); a(ii) 2 x 5; a(iii) required Negative 5 AND Positive 5, one card (the old positive card resolves by alias). b(i) 6; b(ii) and b(iii) 1st @ 5 2nd @ 4. c(i) objective NEGATIVELY 1 + explanation 4; c(ii) 1st @ 5 2nd @ 4; c(iii) 1st @ 5 2nd @ 4, one disadvantage of EACH policy.',
  'Population change is Economic Growth (3-5); population and government finances and inequality policies are Fiscal Policy & the Budget (3-1); labour and its mobility are The Labour Market (2-1); the HDI is Growth & Development (4-0).')
q(12, [17, 18, 19, 20], [19, 20, 21, 22],
  [T('a/i', 12, 'q12-a-i', '2-0'), T('a/ii', 4, 'q12-a-ii', '2-0'), T('a/iii', 17, 'q12-a-iii', '2-0'),
   T('b/i', 9, 'q12-b-i', '2-0'), T('b/ii', 5, 'q12-b-ii', '2-0'), T('b/iii', 10, 'q12-b-iii-adv', '2-0'),
   T('c', 18, 'q12-c', '1-3')],
  'Seven tasks totalling 75. a(i) 3 @ 4 (eight); a(ii) 4 (four); a(iii) diagram 9 (one per label) + explanation 8, one card. b(i) 9 HHI 3,172 (hidden working, whole printed question shown); b(ii) 5 objective HIGHLY CONCENTRATED + reason; b(iii) required Advantage AND Disadvantage priced 1st @ 6 2nd @ 4 across the pair, one card (the old disadvantage card resolves by alias). c 18 = 1st @ 8, 2 @ 5 across the For/Against table: three arguments, one card.',
  'Perfect competition, the HHI and concentration are Market Structures (2-0); the windfall tax is Government Intervention (1-3).')
q(13, [21, 22, 23, 24], [23, 24, 25, 26],
  [T('a/i', 13, 'q13-a-i', '3-0'), T('a/ii', 12, 'q13-a-ii', '3-0'), T('a/iii', 8, 'q13-a-iii', '3-0'),
   T('b/i', 6, 'q13-b-i-mps', '3-0'), T('b/ii', 8, 'q13-b-ii-multiplier', '3-0'), T('b/iii', 8, 'q13-b-iii', '3-0'),
   T('c/i', 12, 'q13-b-i', '4-1'), T('c/ii', 8, 'q13-b-ii', '4-2')],
  'Eight tasks totalling 75. a(i) 13 @ 1 circular-flow labels (hidden solution); a(ii) injections 2 + examples 2 @ 2, leakages 2 + examples 2 @ 2; a(iii) 2 @ 4. b(i) 6 (3 @ 2) MPS 0.3; b(ii) 8 (4 @ 2) multiplier 2; b(iii) 8 injection €125m. c(i) 1st @ 7 2nd @ 5; c(ii) 2 @ 4. (The c-part IDs carry b suffixes from the earlier extractor; citations are Q13(c).)',
  'The circular flow, the hidden economy and the multiplier are National Income (3-0); reliance on MNCs is Globalisation (4-1); competitiveness is International Trade & Competitiveness (4-2).')
q(14, [25, 26, 27, 28], [27, 28, 29, 30],
  [T('a/i', 8, 'q14-a-i', '3-2'), T('a/ii', 4, 'q14-a-ii', '3-2'), T('a/iii', 14, 'q14-a-iii', '3-2'),
   T('b/i', 6, 'q14-b-i', '3-2'), T('b/ii', 8, 'q14-b-ii', '3-1'), T('b/iii', 12, 'q14-b-iii', '0-1'),
   T('c/i', 7, 'q14-c-i', '4-2'), T('c/ii', 8, 'q15-b-ii', '4-2'), T('c/iii', 8, 'q15-b-iii', '4-2')],
  'Nine tasks totalling 75. a(i) 8 (4 + 4) one trend with figures, three scheme alternatives; a(ii) 4 awarded to all who attempted (the question should have named the Labour Force Survey); a(iii) 2 @ 7. b(i) 6 (4 + 2); b(ii) 2 @ 4; b(iii) 3 @ 4 required headings private benefit, external benefit, who bore the cost. c(i) 7; c(ii) and c(iii) 2 @ 4 (IDs carry q15 prefixes; citations are Q14(c)).',
  'Unemployment and full employment are Employment & Unemployment (3-2); government objectives are Fiscal Policy & the Budget (3-1); the PUP cost-benefit is Scarcity & Choice (0-1), its external benefit Market Failure (2-2); trade protection is International Trade & Competitiveness (4-2).')
q(15, [29, 30, 31, 32], [31, 32, 33, 34],
  [T('a/i', 6, 'q15-a-i', '3-3'), T('a/ii', 8, 'q15-a-ii', '3-3'), T('a/iii', 19, 'q15-a-iii', '3-3'),
   T('b/i', 8, 'q15-b-i', '3-3'), T('b/ii', 6, 'q15-b-ii-depreciation', '4-2'),
   T('b/iii/yes', 8, 'q15-b-iii-euro', '4-2'), T('b/iii/no', 8, 'q15-b-iii-euro-no', '4-2'),
   T('c/i', 7, 'q15-c-i', '1-3'), T('c/ii', 7, 'q15-c-ii', '1-3'), T('c/iii', 6, 'q15-c-iii', '1-3')],
  'Ten routes; 75 with one route for b(iii). a(i) one 6 cell for trend + consumer effect; a(ii) 4 + 4; a(iii) 19 composite index 112.2 (hidden worksheet, whole printed question shown). b(i) 8; b(ii) 6 objective DEPRECIATION; b(iii) printed Yes/No, the scheme writes both: two routes 8 each. c(i) 7; c(ii) 7; c(iii) 6 objective NO.',
  'Electricity prices, inflation, the price index and monetary policy are Monetary Policy & Inflation (3-3); exchange rates are International Trade & Competitiveness (4-2); the €600 credit is Government Intervention (1-3).')
q(16, [33, 34, 35, 36], [35, 36, 37, 38, 39],
  [T('a/i', 8, 'q16-a-i', '1-0'), T('a/ii', 15, 'q16-a-ii', '1-0'), T('a/iii', 5, 'q16-a-iii', '2-2'),
   T('b/i', 5, 'q16-b-i', '2-2'), T('b/ii', 8, 'q16-b-ii', '0-2'), T('b/iii', 10, 'q16-b-iii', '0-2'),
   T('c/i', 12, 'q16-c-i-for', '0-2'), T('c/ii', 12, 'q16-c-ii', '0-2')],
  'Eight tasks totalling 75. a(i) individual demand 4 + market demand 4 (the two 4s sit beside the definitions, the 7 beside the diagram and the 8 beside the explanation; the earlier census joined (i) and (ii) at 23). a(ii) diagram 7 + explanation 8 (hidden solution). a(iii) 5 objective YES. b(i) 5 objective YES; b(ii) 2 @ 4; b(iii) 1st @ 6 2nd @ 4. c(i) required For AND Against priced 1st @ 7 2nd @ 5 across the pair, one card (the old against card resolves by alias); c(ii) 1st @ 7 2nd @ 5.',
  'Individual and market demand and the car-market shift are The Market Economy (1-0), individual demand also The Consumer (1-1); government and market failure are Market Failure (2-2); the circular economy, food waste, the national herd and deposit return are Sustainability (0-2).')

SEL = {
 'Answer 4 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Questions two, three and four contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (b) OR (c); every alternative is its own carded task.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (b)/(c) alternatives.'),
}
PAGE_SEL = {
 (4, '(a) Select, using a tick () if petrol is considered to have price elastic demand or price inelastic'): ('answer-classification', 'Q2(a) the scheme ticks price inelastic only; one card.'),
 (6, 'Agree: Disagree:'): ('answer-classification', 'Q4(b) the scheme ticks Disagree only; one card.'),
 (6, 'agree or disagree with this statement?'): ('answer-classification', 'Q4(b) objective Disagree.'),
 (7, '(b) Justify each of your choices you made in (a) above.'): ('not-a-task-selection', 'Q5(b) justify the letters chosen in (a), not a selection.'),
 (7, 'Choose one letter for each A, B or C'): ('answer-classification', 'Q5(a) each production point has one correct letter; one card.'),
 (7, 'Identify from the diagram above which option (A, B or C) represents,'): ('answer-classification', 'Q5(a) fixed letters C, A, B.'),
 (8, 'taxation or indirect taxation.'): ('answer-classification', 'Q6(a) each tax has one correct box; one card.'),
 (10, 'in Ireland? Yes: No:'): ('answer-classification', 'Q8(b) the scheme answers Yes only; one card.'),
 (14, '(b) Labour is one of the factors of production.'): ('not-a-task-selection', 'Stem sentence ("one of the factors"), not a selection.'),
 (15, 'positively or negatively affect Ireland’s HDI score?'): ('answer-classification', 'Q11(c)(i) the scheme answers Negatively only; one card.'),
 (17, '(ii) Identify one reason why the market for Irish milk can no longer be considered'): ('not-a-task-selection', 'Q11/12 "identify one reason" is an open response, not a printed pool.'),
 (17, 'faced with an abundance of choice from low‐fat milk to super milk to lactose free'): ('not-a-task-selection', 'Stem wording ("choice"), not a selection.'),
 (19, '(ii) Would you consider this market to be competitive, moderately concentrated, or'): ('answer-classification', 'Q12(b)(ii) the HHI decides the answer (highly concentrated); one card.'),
 (31, '(ii) Does the prevailing trend on the graph below indicate appreciation or depreciation of'): ('answer-classification', 'Q15(b)(ii) the chart decides the answer (depreciation); one card.'),
 (31, 'appreciating? Yes: No: Justify your answer.'): ('finite-route', 'Q15(b)(iii) Yes/No; the scheme writes both sides, two routes.'),
 (32, 'Yes: No:'): ('answer-classification', 'Q15(c)(iii) the scheme answers No only; one card.'),
 (33, 'Yes: No:'): ('answer-classification', 'Q16(a)(iii) the scheme answers Yes only; one card.'),
 (34, 'Outline two of the challenges the economy will face supporting the transition to the'): ('not-a-task-selection', 'Q16(b)(ii) "two of the challenges" is an open response, not a printed pool.'),
 (34, 'Yes: No:'): ('answer-classification', 'Q16(b)(i) the scheme answers Yes only; one card.'),
 (36, 'a drink will pay a small deposit for the plastic bottle or can container. Customers will'): ('not-a-task-selection', 'Stem wording ("or"), not a selection.'),
 (36, 'get their money back when they return the container to a retailer or other collection'): ('not-a-task-selection', 'Stem wording ("or"), not a selection.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 40: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# Every route equals the earlier review's except the Q16(a) split.
tup = lambda qs: sorted((x['n'], t['key'], t['cardId'], t['marks'], t['topicId']) for x in qs for t in x['tasks'])
new, prev = set(tup(Q)), set(tup(old['questions']))
expect_new = {('16', 'a/i', P + 'q16-a-i', 8, 'economics-1-0'), ('16', 'a/ii', P + 'q16-a-ii', 15, 'economics-1-0')}
expect_old = {('16', 'a/i+ii', P + 'q16-a-ii', 23, 'economics-1-0')}
# A re-run after recording finds the review already carries the change.
if new != prev and (new - prev != expect_new or prev - new != expect_old):
    raise SystemExit(f'unexpected route change: +{new - prev} -{prev - new}')
for x, o in zip(Q, old['questions']):
    assert x['paperPages'] == o['paperPages'], x['n']
tasks = [t for x in Q for t in x['tasks']]
targeted = dict(old['targetedIrishEvidence'])
targeted['reason'] = ('Identical cost table/choices on paper p6 and explicit 6/6/6 allocation on scheme p9 resolve '
                      'displaced English Q4 tariffs; paper p33 and scheme p35 show the same 4, 4, 7, 8 cells for '
                      'Q16(a)(i)-(ii) without the stray English 3.')
draft = {
 'subjectId': 'economics', 'year': 2023, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 45)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Re-review 2026-10-12 from a fresh paired visual sweep of all 40 paper and 44 scheme pages (scheme PDF page = printed page + 2). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified. One route change against the earlier census: Q16(a)(i) (4 + 4) is its own task, no longer joined to the Q16(a)(ii) diagram (7 + 8); the 2023 Higher Irish review mirrors that change only. Every stem and ask is now sliced from the paper and every menu from the scheme (econ_2023_hl.py; the Section A script and the correction module are retired). Four split required-heading cards stay consolidated with progress aliases. Q10 A is completed on the paper. Scheme pp40-44 student research project descriptors: no written-paper asks. Choose-N rule checked: no printed choose-N-of-M item pool on this paper.',
 'targetedIrishEvidence': targeted,
 'externalClarifications': [],
 'curriculumSource': old.get('curriculumSource', 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf'),
}
out = W / 'scripts/markbank/authoring/drafts/economics-2023-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']), x['canonicalNodeIds'])
