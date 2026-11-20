"""Card the SEC's 2022 Ordinary Level deferred Business sitting.

Sources (deferredexams/2022 and deferredmarkingschemes/2022, filed by Paper Trail as "<fileid>-deferred"):
Section 1 and Answerbook LC033GLP032EV (36 pages), Section 2 LC033GLP033EV (12 pages), marking scheme
LC033GLP000EV (32 pages). Every page was rendered and read on 2026-11-19: the Section 1 booklet's cover,
instructions, the fifteen short questions on pages 3-8 (Q5's increase/decrease table, Q10's controller and
facilitator grid, Q12's tax matching table, Q13's Head2Toe sales table), the Section 2 answerbook instructions,
two graph-paper pages (10, 11), ruled answer pages and the back cover; the Section 2 booklet's cover, Questions
1-9 on pages 2-10 with their extracts and images (Q3's IDA Ireland FDI infographic, which prints its figures
only as an image; Q6's and Q9's underlined terms; Q8's cash flow forecast and balance sheet extract), page 11 with
no examination material and the back cover; the scheme's cover, p2 note on deferred marking schemes, p3 notes,
the allocation tables (Section 1 p4, Section 2 pp5-7) and the solutions (Section 1 pp8-10, Section 2 pp11-30;
31-32 blank).

Choice is not a route (collapse-choices.py, collapse-choose-one.py): Section 2 Q3(C) (one of four printed EU
institutions), Q5(E) (Maslow or McGregor), Q6(A) (one of the two underlined terms), Q6(B)(ii) (two of the three
sources) and Q9(A) (two of the three underlined terms) are each one card with every printed option; the scheme
marks every option alike and each files under one topic.

The scheme's printed page numbers run one ahead of the PDF's; cards cite PDF pages.
Run from the repo root; reproduce.py runs it in the chain.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deferred_lib import Sitting, response, comps, points, seq, unequal  # noqa: E402

D = Sitting(2022, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV')
L, S = D.lift, D.sch
W = lambda page, *s, **k: L(1, page, *s, **k)
P = lambda page, *s, **k: L(2, page, *s, **k)


def per(label, items, marks):
    return [response(i, f'{label} ({r})', [('answer', 'Answer', m)]) for i, (r, m) in enumerate(zip(items, marks), 1)]


# ---------------------------------------------------------------- Section 1 (answer five of fifteen; 15 marks each)
D.add(1, 'q1', 'Q1', W(3, 'What do the following letters stand for? Write each answer in the space provided.') + '\n' + W(3, 'ATM', 'AGM', 'AOB'),
      15, 'business-2-12', 'business-abbreviations', 3, [4, 8], 'Each abbreviation in full: 5 marks.',
      [response(i, f'{t} in full', [('answer', 'Words written in full', 5)]) for i, t in enumerate(['ATM', 'AGM', 'AOB'], 1)],
      expected=D.expected(8, 'ATM –Automated Teller Machine', 'AGM – Annual General Meeting', 'AOB – Any Other Business'))
D.add(1, 'q2', 'Q2', W(3, 'Write TRUE or FALSE after each of the following statements.') + '\n' + W(
    3, '(i) A sole trader has unlimited liability.', '(ii) Insurable interest means that you cannot profit from insurance.',
    '(iii) A dividend is the share of the profits received by a company shareholder.', '(iv) A recession leads to an increase in employment.',
    '(v) An e-mail cannot have more than 140 characters.'),
      15, 'business-5-14', 'business-statements-true-false', 3, [4, 8], 'Five statements at 3 marks each.',
      per('Statement', ['i', 'ii', 'iii', 'iv', 'v'], [3] * 5),
      expected=D.expected(8, '(i) TRUE', '(ii) FALSE', '(iii)TRUE', '(iv)FALSE', '(v) FALSE'),
      extra=['business-3-17', 'business-5-15', 'business-2-12'])
D.add(1, 'q3', 'Q3', W(3, 'List three ways a contract can be terminated.'), 15, 'business-0-12', 'contract-termination-ways', 3, [4, 8],
      'Three ways at 5 marks each.', [response(i, f'Way {i}', [('answer', 'Way', 5)]) for i in (1, 2, 3)],
      expected=D.expected(8, 'Performance', 'Agreement', 'Frustration', 'Breach'))
D.add(1, 'q4', 'Q4', W(4, 'Explain the term minutes of a meeting.'), 15, 'business-2-12', 'minutes-of-a-meeting', 4, [4, 8],
      'Explain the term for 15 marks (8 + 7).', [comps('Minutes of a meeting', (8, 7))],
      expected=D.split([(8, 'This is an account of a meeting', ' 15m 8 + 7 5.')], ['This is an account of a meeting written by the secretary.']))
D.add(1, 'q5', 'Q5', W(4, 'If the Euro (€) increases in value against the UK (£) Sterling, indicate whether each of the following would be expected to increase or decrease.')
      + '\n' + W(4, '(i) Number of UK visitors coming to Ireland.', '(ii) Imports to Ireland from the UK.'), 15, 'business-6-13',
      'exchange-rate-effects', 4, [4, 8], '(i) 8 marks and (ii) 7 marks.', per('Effect', ['i', 'ii'], [8, 7]),
      expected=D.expected(8, '(i) Decrease', '(ii) Increase'))
D.add(1, 'q6', 'Q6', W(4, 'Explain the term visible export and give an example of one Irish visible export.'), 15, 'business-6-13',
      'visible-export', 4, [4, 8], 'Explanation 10 marks (5 + 5) and example 5 marks.',
      [comps('Visible export', (5, 5), ['Explanation', 'Explanation'], 1), comps('Example', (5,), ['Example'], 2)],
      expected=D.split([(8, 'Visible exports are physical goods', ' 15m 5 + 5 5 7.')], ['Visible exports are physical goods', 'Examples:']))
D.add(1, 'q7', 'Q7', W(5, 'Complete each of the following sentences by inserting one of these terms:') + '\n' + W(
    5, 'NET PROFIT COST OF SALES DIVIDENDS PAID VARIABLE COSTS', '(Note: One of the terms does not apply to any of the sentences.)')
      + '\n' + W(5, '(i) Fixed Costs +', '= Total Costs.', '(ii) Gross Profit ─ Expenses =', '(iii) Sales ─', '= Gross Profit.', sep=' '),
      15, 'business-3-19', 'cost-and-profit-terms', 5, [4, 8], 'Three sentences at 5 marks each.', per('Sentence', ['i', 'ii', 'iii'], [5, 5, 5]),
      expected=D.expected(8, '(i) Variable Costs', '(ii) Net Profit', '(ii) Cost of Sales'),
      guidance=['The scheme numbers its third answer “(ii)”; it completes sentence (iii).'])
D.cards[-1]['questionText'] = (W(5, 'Complete each of the following sentences by inserting one of these terms:') + '\n'
                               + W(5, 'NET PROFIT COST OF SALES DIVIDENDS PAID VARIABLE COSTS') + '\n'
                               + W(5, '(Note: One of the terms does not apply to any of the sentences.)') + '\n\n'
                               + W(5, '(i) Fixed Costs +') + ' ________ ' + W(5, '= Total Costs.') + '\n'
                               + W(5, '(ii) Gross Profit ─ Expenses =') + ' ________.\n'
                               + W(5, '(iii) Sales ─') + ' ________ ' + W(5, '= Gross Profit.'))
D.add(1, 'q8', 'Q8', W(5, 'Explain the term franchising and state one example of a franchise.'), 15, 'business-5-14', 'franchising', 5, [4, 8],
      'Explanation 10 marks (5 + 5) and example 5 marks.',
      [comps('Franchising', (5, 5), ['Explanation', 'Explanation'], 1), comps('Example', (5,), ['Example'], 2)],
      expected=D.split([(8, 'This is the granting of a licence', ' 15m 10 (5 + 5) 5')], ['This is the granting of a licence', 'Example:']))
D.add(1, 'q9', 'Q9', W(5, 'Describe two entrepreneurial skills important in setting up a business.'), 15, 'business-1-5', 'entrepreneurial-skills', 5, [4, 9],
      'Two skills: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Skill', [(4, 4), (4, 3)]),
      expected=D.split([(9, 'Innovative/Creative', ' Accept other appropriate responses.')],
                       ['Innovative/Creative', 'Proactive', 'Decisive', 'People skills', 'Time management', 'Stress skills']))
D.add(1, 'q10', 'Q10', W(6, 'Complete the following table which refers to quotes from management by placing a tick (\uf0fc) in the correct box for each statement.').replace('\uf0fc', '✓')
      + '\n' + W(6, '‘All decisions must be approved by the manager.’', '‘Are there any problems I can help you with?’',
                 '‘Have that work finished by 5.00pm or else.’', '‘Do as I say and don’t ask questions.’',
                 '‘There is a development course coming up in which you may be interested.’'),
      15, 'business-3-21', 'controller-or-facilitator', 6, [4, 9], 'Five quotes at 3 marks each.', per('Quote', ['i', 'ii', 'iii', 'iv', 'v'], [3] * 5),
      expected=D.expected(9, '(i) Controller', '(ii) Facilitator', '(iii) Controller', '(iv) Controller', '(v) Facilitator'),
      guidance=['The paper prints a tick box for Controller or Facilitator beside each quote (its tick is a Wingdings glyph in the text layer, shown as ✓); the scheme numbers the quotes (i)-(v) in print order.'])
D.add(1, 'q11', 'Q11', W(6, 'Outline two advantages of effective stock control in a business.'), 15, 'business-2-13', 'stock-control-advantages', 6, [4, 9],
      'Two advantages: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Advantage', [(4, 4), (4, 3)]),
      expected=D.split([(9, 'Increased customer satisfaction', ' 15m 8m (4 + 4)')],
                       ['Increased customer satisfaction', 'Reduced costs', 'Increased efficiency', 'Identifies stock losses',
                        'Working capital will be used efficiently', 'Less wastage']))
D.add(1, 'q12', 'Q12', W(7, 'In the following table, Column 1 is a list of business terms and Column 2 is a list of explanations.') + '\n\n' + W(
    7, '1 Capital Acquisitions Tax', '2 DIRT', '3 Customs Duty', '4 Corporation Tax', '5 Local Property Tax',
    'A A tax on company profit.', 'B A tax paid on imported goods.', 'C A tax paid on gifts and inheritance.',
    'D A tax paid on the interest earned on savings.', 'E A tax paid on the sale of assets.', 'F A tax calculated on the value of your home.')
      + '\n\n' + W(7, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant business term below. One explanation has no match.'),
      15, 'business-3-18', 'tax-terms-matching', 7, [4, 9], 'Five matches at 3 marks each.', per('Term', ['1', '2', '3', '4', '5'], [3] * 5),
      expected={'page': 9, 'items': [{'id': f'e{n}', 'text': f'{n} — {x}'} for n, x in
                                     enumerate(S(9, 'Business Term 1 2 3 4 5 Explanation C D B A F').split()[-5:], 1)]},
      guidance=['Answer key (scheme grid “Business Term 1 2 3 4 5 Explanation C D B A F”): 1 C; 2 D; 3 B; 4 A; 5 F. Explanation E is unused.'])
D.add(1, 'q13', 'Q13', W(7, 'Draw a bar chart to illustrate the following information for Head2Toe Ltd.', 'Use the graph paper on page 10 of this booklet.')
      + '\n\n' + W(7, 'Sales in Munster (per county) €’000', 'County: Clare Cork Kerry Limerick Tipperary Waterford', 'Sales: 20 50 35 40 30 25'),
      15, 'business-2-12', 'sales-bar-chart', 7, [4, 9], 'Six accurate bars at 2 marks each, the X axis (County) 1, the Y axis (€/sales) 1 and the title 1.',
      [response(1, 'Bar chart', [('title', 'Title', 1), ('x-axis', 'X axis (County)', 1), ('y-axis', 'Y axis (€/sales)', 1),
                                 *[(f'bar-{k.lower()}', f'{k}: {v}', 2) for k, v in
                                   zip(['Clare', 'Cork', 'Kerry', 'Limerick', 'Tipperary', 'Waterford'], [20, 50, 35, 40, 30, 25])]])],
      expected=D.expected(9, 'Title 1m', 'X axis (County) 1m', 'Y axis (€/sales) 1 m', '6 bars @ 2 m'),
      guidance=['The scheme draws its model chart as an image on page 9 (read from the rendered page: “Head2Toe Ltd / Sales in Munster”, six bars by county, Sales (€’000) against County) and prices it “'
                + S(4, 'Bar chart with 6 accurate bars @ 2 mark each') + '”; the bar labels on this card are the paper’s own figures.'])
D.add(1, 'q14', 'Q14', W(8, 'Outline two benefits of teamwork for a business.'), 15, 'business-3-20', 'teamwork-benefits', 8, [4, 10],
      'Two benefits: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Benefit', [(4, 4), (4, 3)]),
      expected=D.split([(10, 'Improved decision-making:', ' 15m 8m (4 + 4)')],
                       ['Improved decision-making:', 'Better staff morale:', 'Improved staff relations:', 'Workload is shared:',
                        'Improved communication:', 'Work is completed faster:', 'Generates creative ideas:', 'Reduced Staff absenteeism:']))
D.add(1, 'q15', 'Q15', W(8, 'Write the correct word after each sentence below:', 'Strength Weakness Opportunity Threat') + '\n' + W(
    8, '(i) High level of staff turnover.', '(ii) The shop has been offered the premises next door.', '(iii) Another similar shop has opened on the same street.',
    '(iv) The shop provides high quality customer service.'),
      15, 'business-2-13', 'swot-words', 8, [4, 10], '(i), (ii) and (iii) at 4 marks each and (iv) 3 marks.',
      per('Sentence', ['i', 'ii', 'iii', 'iv'], [4, 4, 4, 3]),
      expected=D.expected(10, '(i) Weakness', '(ii) Opportunity', '(iii) Threat', '(iv) Strength'))

# ---------------------------------------------------------------- Section 2 (answer three of nine; 75 marks each)
suits = P(2, 'SUITS LTD SALE NOW ON ALL Suits €200 Includes free shirt with every suit purchased', 'After seeing this advertisement, Patrick visited Suits Ltd. He selected a suit and then asked the sales assistant to include a white shirt. When paying for the suit, the sales assistant charged Patrick €250. She said the suit Patrick chose was not on sale. On arriving home, he discovered that the shirt had not been included. When he returned to the shop to ask for the shirt, the assistant said he would have to pay for it.')
ellen = P(2, 'Ellen Dunne is employed in a food processing company. She and her colleagues are in a dispute with their employer and are on a ‘go-slow’. They are all members of a trade union.')
D.add(2, 'q1a', 'Q1(A)', suits + '\n\n' + P(2, 'Explain how Suits Ltd has broken the terms of the Consumer Protection Act 2007.'), 15, 'business-0-13',
      'consumer-protection-act-breaches', 2, [5, 11], 'Two points: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Point', [(4, 4), (4, 3)]),
      expected=D.split([(11, 'It is illegal for a business to make misleading claims', ' 15m 8m (4 + 4)')],
                       ['It is illegal for a business to make misleading claims about goods and services:', 'It is illegal for a business to make false/misleading claims about prices:',
                        'The Act requires information in advertisements to be fair and accurate.']))
D.add(2, 'q1b', 'Q1(B)', suits + '\n\n' + P(2, 'Outline one approach for solving the above problem between the retailer and Patrick.'), 10, 'business-0-13',
      'consumer-dispute-approach', 2, [5, 11], 'One approach at 10 marks (5 + 5).', [comps('Approach', (5, 5))],
      expected=D.split([(11, 'Negotiation The process', ' 10m 5 + 5')], ['Negotiation', 'CAI (Consumer Association of Ireland)', 'Small claims court']))
D.add(2, 'q1c', 'Q1(C)', P(2, 'Outline two functions of the Competition and Consumer Protection Commission (CCPC).'), 15, 'business-0-13',
      'ccpc-functions', 2, [5, 11], 'Two functions: 10 marks (7 + 3) and 5 marks (4 + 1).', unequal('Function', [(7, 3), (4, 1)]),
      expected=D.split([(11, 'Provides information to consumers', ' 15m 10m (7 + 3)')],
                       ['Provides information to consumers', 'Provides information to businesses', 'Can take enforcement actions',
                        'Advises policy makers', 'Publishes a consumer protection list', 'Examines mergers and acquisitions']))
D.add(2, 'q1di', 'Q1(D)(i)', ellen + '\n\n' + P(2, 'Outline two causes of an industrial dispute.'), 15, 'business-0-14', 'industrial-dispute-causes', 2, [5, 12],
      'Two causes: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Cause', [(4, 4), (4, 3)]),
      expected=D.split([(12, 'Working conditions –', ' (ii) Explain the term')],
                       ['Working conditions –', 'Pay rates –', 'New work practices –', 'Discrimination –', 'Demarcation issues –', 'Pensions -',
                        'Holiday entitlements', 'Dismissal –', 'Redundancies –']))
D.add(2, 'q1dii', 'Q1(D)(ii)', ellen + '\n\n' + P(2, 'Explain the term go-slow.'), 5, 'business-0-14', 'go-slow', 2, [5, 12],
      'Explain the term for 5 marks (3 + 2).', [comps('Go-slow', (3, 2))],
      expected=D.split([(12, 'A go-slow is a protest', ' 20m 8m')], ['A go-slow is a protest by workers']))
D.add(2, 'q1e', 'Q1(E)', ellen + '\n\n' + P(2, 'Outline two functions of a trade union.'), 15, 'business-0-14', 'trade-union-functions', 2, [5, 12],
      'Two functions: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Function', [(4, 4), (4, 3)]),
      expected=D.split([(12, 'Securing a fair wage', ' 15m 8m (4 + 4)')],
                       ['Securing a fair wage', 'Securing fair/improved working conditions', 'Negotiating on behalf of its members',
                        'Seeking opportunities for promotion', 'Providing for training']))

farm = P(3, 'We should buy our fruit and vegetables from local sources, according to the organisation One Change.', 'John Byrne is a famer who sells organically grown vegetables and free-range eggs in his shop on his farm. On Saturdays he sells his produce at local farmer’s markets and supplies local restaurants each week.')
ethics = P(3, 'Good ethics are essential in modern business.')
D.add(2, 'q2ai', 'Q2(A)(i)', farm + '\n\n' + P(3, 'From the information above,', '(i) Name the sector of the economy in which farming operates.', sep=' '), 5,
      'business-5-13', 'farming-sector-named', 3, [5, 13], 'Name the sector: 5 marks.', [comps('Sector', (5,), ['Name'])],
      expected=D.expected(13, 'Primary'))
D.add(2, 'q2aii', 'Q2(A)(ii)', farm + '\n\n' + P(3, '(ii) Explain two reasons why this sector is important in Ireland.'), 15, 'business-5-13',
      'primary-sector-importance', 3, [5, 13], 'Two reasons: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Reason', [(4, 4), (4, 3)]),
      expected=D.split([(13, 'Agriculture – providing food', ' 20m 5 8m')], ['Agriculture –', 'Employment –', 'Exports / Balance of Payments –', 'Capital expenditure –']))
D.add(2, 'q2b', 'Q2(B)', farm + '\n\n' + P(3, 'Identify one issue facing this sector in Ireland.'), 10, 'business-5-13', 'primary-sector-issue', 3, [5, 13],
      'One issue at 10 marks (5 + 5).', [comps('Issue', (5, 5))],
      expected=D.split([(13, 'EU payments –', ' 10m 5 + 5')], ['EU payments –', 'Small farm sizes –', 'Diversification –', 'Climate change –', 'Depletion of fishing stock –']))
D.add(2, 'q2c', 'Q2(C)', P(3, 'Name and explain one other sector of the economy, giving an example in your answer.'), 15, 'business-5-13',
      'other-economic-sector', 3, [5, 13], 'Name 4 marks, explanation 7 marks (4 + 3) and example 4 marks.',
      [comps('Sector', (4,), ['Name'], 1), comps('Explanation', (4, 3), None, 2), comps('Example', (4,), ['Example'], 3)],
      expected=D.split([(13, 'Secondary Sector:', ' Accept other appropriate answers.')], ['Secondary Sector:', 'Tertiary Sector:']))
D.add(2, 'q2d', 'Q2(D)', ethics + '\n\n' + P(3, 'Explain the term Business Ethics.'), 10, 'business-5-17', 'business-ethics-term', 3, [5, 14],
      'Explain the term for 10 marks (5 + 5).', [comps('Business ethics', (5, 5))],
      expected=D.split([(14, 'Having moral principles.', ' 10m 5 + 5')], ['Having moral principles.']))
for key, roman, who, start, end, heads in [
        ('q2ei', 'i', 'its employees', 'Fair wages –', ' (ii) its customers',
         ['Fair wages –', 'Working conditions –', 'Health and Safety –', 'Treat everyone equally –', 'Work patterns –', 'Code of ethics –']),
        ('q2eii', 'ii', 'its customers.', 'Fair price –', ' 20m 10m',
         ['Fair price –', 'Quality products and services –', 'Do not mislead –', 'Do not target vulnerable people –', 'After sales policy -', 'Code of ethics –'])]:
    D.add(2, key, f'Q2(E)({roman})', ethics + '\n\n' + P(3, 'Explain how a business can be ethical towards:') + '\n' + P(3, f'({roman}) {who}'), 10,
          'business-5-17', f"ethical-towards-{'employees' if roman == 'i' else 'customers'}", 3, [5, 14], 'Explain for 10 marks (5 + 5).',
          [comps('Ethical behaviour', (5, 5))], expected=D.split([(14, start, end)], heads))

fdi = P(4, 'FDI stands for Foreign Direct Investment (multinational companies setting up in Ireland) and CAPEX stands for Capital Expenditure (investing in large projects.)')
D.add(2, 'q3a', 'Q3(A)', fdi + '\n\n' + P(4, 'Using the information above outline two benefits to Ireland of FDI.'), 15, 'business-6-15', 'fdi-benefits', 4, [5, 15],
      'Two benefits: 8 marks (5 + 3) and 7 marks (5 + 2).', unequal('Benefit', [(5, 3), (5, 2)]),
      expected=D.split([(15, 'Employment – creating jobs', ' 15m 8m (5 + 3)')], ['Employment –', 'Capital expenditure –', 'Exports –', 'Buy Irish goods –', 'Other points']),
      guidance=['The paper prints the IDA Ireland figures as an image (page 4); “' + S(15, 'Must give reference to information provided for full marks.') + '”'])
D.add(2, 'q3b', 'Q3(B)', P(4, 'Explain two reasons why a multinational company might set up a manufacturing plant in Ireland.'), 15, 'business-6-15',
      'multinationals-locating-in-ireland', 4, [5, 15], 'Two reasons: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Reason', [(4, 4), (4, 3)]),
      expected=D.split([(15, 'Access to EU markets:', ' 15m 8m (4 + 4)')],
                       ['Access to EU markets:', 'Low Corporation Tax (12.5%):', 'English speaking member of the Eurozone:', 'Highly skilled workforce:',
                        'Access to Govt. Grants/ incentives to locate here.', 'Track Record:']))
D.add(2, 'q3c', 'Q3(C)', P(4, 'EU INSTITUTIONS Council of the European Union European Commission European Parliament European Court of Auditors') + '\n\n'
      + P(4, 'Explain the role of any one of the EU institutions listed above.'), 15, 'business-6-14', 'eu-institution-role', 4, [5, 16],
      'The chosen institution: 10 marks (7 + 3) and 5 marks (4 + 1).', unequal('Role', [(7, 3), (4, 1)]),
      expected=D.split([(16, 'Council of the European Union Made up', ' 15m 10m')],
                       ['Council of the European Union', 'European Commission', 'European Parliament', 'European Court of Auditors']),
      guidance=['A printed choice of one of four institutions: one card, every institution marked alike.'])
D.add(2, 'q3d', 'Q3(D)', P(4, 'List five countries of the EU.'), 15, 'business-6-14', 'eu-member-countries', 4, [5, 17],
      'Five countries at 3 marks each.', [response(i, f'Country {i}', [('answer', 'Country', 3)]) for i in range(1, 6)],
      expected=D.split([(17, 'Ireland, Austria', ' 15m 5 @ 3m each')], ['Ireland, Austria, Belgium']))
D.add(2, 'q3e', 'Q3(E)', P(4, 'Outline two advantages of the euro to Irish households.'), 15, 'business-6-14', 'euro-advantages-households', 4, [5, 17],
      'Two advantages: 10 marks (7 + 3) and 5 marks (4 + 1).', unequal('Advantage', [(7, 3), (4, 1)]),
      expected=D.split([(17, 'Exchange rate costs –', ' 15m 10m (7 + 3)')],
                       ['Exchange rate costs –', 'Transparency of prices –', 'Greater choice -', 'Price stability in EU –', 'Availability of credit -']))

mary = P(5, 'Mary works as a secretary for Murray Construction for the last eight years. She recently informed her employer that she was pregnant and would be going on maternity leave in 8 weeks’ time. Murray Construction informed Mary that taking maternity leave was not acceptable for their business and terminated her employment with immediate effect.')
michael = P(5, 'Michael bought an electric tooth brush in his local pharmacy. He brought the tooth brush home. At home he plugged it in to try it, he immediately could smell burning. He was afraid to use it. He returned to the pharmacy with the product to complain.')
D.add(2, 'q4ai', 'Q4(A)(i)', mary + '\n\n' + P(5, '(i) Outline two reasons for unfair dismissal (other than pregnancy).'), 10, 'business-0-14',
      'unfair-dismissal-reasons', 5, [6, 18], 'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)),
      expected=D.split([(18, 'Political or religious beliefs', ' (ii) Outline two reasons for fair dismissal.')],
                       ['Political or religious beliefs or opinions.', 'Membership of a trade union', 'Unfair selection for redundancy.', 'Race –',
                        'Membership of the travelling community.']))
D.add(2, 'q4aii', 'Q4(A)(ii)', mary + '\n\n' + P(5, '(ii) Outline two reasons for fair dismissal.'), 10, 'business-0-14', 'fair-dismissal-reasons', 5, [6, 18],
      'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)),
      expected=D.split([(18, 'Employee misconduct –', ' 20m 2 @ 5m')],
                       ['Employee misconduct –', 'Employee incapable', 'Not showing the competence', 'The employee is not properly qualified', 'Redundancy,']))
D.add(2, 'q4b', 'Q4(B)', mary + '\n\n' + P(5, 'Explain what Mary’s rights are in this situation under the Employment Equality Act 1998-2015.'), 15, 'business-0-14',
      'employment-equality-rights', 5, [6, 18], 'Two points: 10 marks (7 + 3) and 5 marks (4 + 1).', unequal('Right', [(7, 3), (4, 1)]),
      expected=D.split([(18, 'Mary can bring her case to the WRC', ' 15m 10m (7 + 3)')],
                       ['Mary can bring her case to the WRC', 'The complaint may be dealt with by mediation or adjudication.', 'If unhappy with the WRC decision,',
                        'Mary is entitled to be reinstated', 'Mary is entitled to financial compensation.']))
D.add(2, 'q4c', 'Q4(C)', P(5, 'Explain the role of the shop steward in the work place.'), 15, 'business-0-14', 'shop-steward-role', 5, [6, 18],
      'Two points: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Point', [(4, 4), (4, 3)]),
      expected=D.split([(18, 'The shop steward is the contact person', ' 15m 8m (4 + 4)')],
                       ['The shop steward is the contact person', 'The shop steward will liaise', 'Will recruit new members', 'Will ensure that employees contracts']))
D.add(2, 'q4d', 'Q4(D)', michael + '\n\n' + P(5, 'Name the act that protects Michael in this case.'), 10, 'business-0-13', 'sale-of-goods-act-named', 5, [6, 18],
      'Name the Act: 10 marks (the scheme’s table prices it at 5 words @ 2 marks each).', [comps('The Act', (2, 2, 2, 2, 2), [f'Word {k}' for k in range(1, 6)])],
      expected=D.expected(18, 'The Sale of Goods and Supply of Services Act 1980.'),
      guidance=['The scheme’s table prints “' + S(6, '5 words @ 2 marks each') + '”; its solution prints the Act at 10.'])
D.add(2, 'q4e', 'Q4(E)', michael + '\n\n' + P(5, 'Explain three forms of redress available to Michael.'), 15, 'business-0-13', 'consumer-redress-forms', 5, [6, 18],
      'Three forms at 5 marks each (3 + 2).', points('Form of redress', 3, (3, 2)),
      expected=D.split([(18, 'Michael is entitled to a full refund', ' 15m 3 @ 5m')],
                       ['Michael is entitled to a full refund', 'Michael is entitled to a replacement', 'Michael is entitled to the toothbrush being repaired']))

jim = P(6, 'Jim operates a retail supermarket business. He employs four sales assistants. He is finding it difficult to compete with the large retail supermarket chains. Jim thinks that his employees are lazy and feels he is giving the same instructions over and over again. He does not trust them. There is a need to motivate his employees and communicate better with them.')
D.add(2, 'q5a', 'Q5(A)', jim + '\n\n' + P(6, 'Name and explain the leadership style Jim currently operates.'), 10, 'business-2-11', 'autocratic-leadership', 6, [6, 19],
      'Name 3 marks and explanation 7 marks (4 + 3).', [comps('Style', (3,), ['Name'], 1), comps('Explanation', (4, 3), None, 2)],
      expected=D.split([(19, 'Autocratic An autocratic leader', ' Accept other appropriate answers.')], ['Autocratic', 'An autocratic leader']))
D.add(2, 'q5b', 'Q5(B)', jim + '\n\n' + P(6, 'Describe two responsibilities of an employer to their employees.'), 15, 'business-3-20', 'employer-responsibilities', 6, [6, 19],
      'Two responsibilities: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Responsibility', [(4, 4), (4, 3)]),
      expected=D.split([(19, 'Provide a written contract', ' 15m 8m (4 + 4)')],
                       ['Provide a written contract –', 'Pay wages as agreed –', 'Provide safe working conditions –', 'Comply with employment law –',
                        'Allow them to join a trade union']))
D.add(2, 'q5c', 'Q5(C)', jim + '\n\n' + P(6, 'Outline three barriers to communication in this business.'), 15, 'business-2-12', 'communication-barriers', 6, [6, 19],
      'Three barriers at 5 marks each (3 + 2).', points('Barrier', 3, (3, 2)),
      expected=D.split([(19, 'Language used may not be appropriate', ' 15m 3 @ 5m')],
                       ['Language used may not be appropriate', 'Wrong medium chosen –', 'Not listening or concentrating.', 'Relationships –', 'Timing –',
                        'Use of irrelevant material –', 'Lack of feedback', 'Interference/technology breakdown.']))
D.add(2, 'q5d', 'Q5(D)', jim + '\n\n' + P(6, 'Explain two methods of communication with employees which Jim should consider.'), 15, 'business-2-12',
      'communication-methods-employees', 6, [6, 19], 'Two methods: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Method', [(4, 4), (4, 3)]),
      expected=D.split([(19, 'Oral/Verbal:', ' 15m 8m (4 + 4)')], ['Oral/Verbal:', 'Written:', 'Visual:', 'Accept two types from:']))
D.add(2, 'q5e', 'Q5(E)', jim + '\n\n' + P(6, 'Outline the motivational theory of either Maslow or McGregor.'), 20, 'business-2-11', 'maslow-or-mcgregor', 6, [6, 20],
      'Four points at 5 marks each (3 + 2).', points('Point', 4, (3, 2)),
      expected=D.split([(20, 'Maslow Physical Needs', ' 20m 4 @ 5m')],
                       ['Maslow', 'Physical Needs –', 'Safety/Security Needs –', 'Social Needs –', 'Esteem Needs –', 'Self-actualisation Needs –',
                        'McGregor Theory X', 'Characteristics/Implications of a Theory X Manager may include:', 'McGregor Theory Y']),
      guidance=['A printed choice of either theory: one card, both marked alike (4 @ 5 marks).'])

peter = P(7, 'Peter Roche, who is employed in a medical company, intends to set up his own business. It will produce pillow covers for hospitals using a medical textile which will reduce the risk of infections. He will use batch production to make the new products for what he sees as a niche market. He has obtained a grant for the premises. He hopes to lease a delivery van and to get a bank overdraft.')
D.add(2, 'q6a', 'Q6(A)', peter + '\n\n' + P(7, 'Explain one of the underlined terms above.'), 10, 'business-4-15', 'batch-production-or-niche-market', 7, [6, 21],
      'One term at 10 marks (5 + 5).', [comps('Term', (5, 5))],
      expected=D.split([(21, 'Batch production Manufacturing', ' 10m 5 + 5')], ['Batch production', 'Niche market']),
      guidance=['The paper underlines “batch production” and “niche market” (page 7). A printed choice of one: one card, both marked alike.'],
      extra=['business-4-16'])
sources = P(7, 'Peter will use three sources of finance – grant, leasing and bank overdraft.')
D.add(2, 'q6bi', 'Q6(B)(i)', peter + '\n\n' + sources + '\n' + P(7, '(i) State whether each of the three sources of finance is short-term, medium-term or long-term.'), 6,
      'business-3-16', 'finance-source-terms', 7, [6, 21], 'Three sources at 2 marks each.',
      [response(i, s, [('answer', 'Term', 2)]) for i, s in enumerate(['Grant', 'Leasing', 'Bank overdraft'], 1)],
      expected=D.expected(21, 'Grant – long term', 'Leasing – medium term', 'Bank overdraft – short term'))
D.add(2, 'q6bii', 'Q6(B)(ii)', peter + '\n\n' + sources + '\n' + P(7, '(ii) Explain two of the three sources of finance which Peter will use.'), 14,
      'business-3-16', 'finance-sources-explained', 7, [6, 21], 'Two sources at 7 marks each (4 + 3).', points('Source', 2, (4, 3)),
      expected=D.split([(21, 'Grant: Usually once off', ' 20m 6m')], ['Grant:', 'Leasing:', 'Bank overdraft:']),
      guidance=['A printed choice of two of the three sources: one card, every source marked alike.'])
D.add(2, 'q6c', 'Q6(C)', peter + '\n\n' + P(7, 'Explain two difficulties, other than sources of finance, that Peter could experience when setting up his own business.'), 20,
      'business-4-15', 'start-up-difficulties', 7, [6, 22], 'Two difficulties at 10 marks each (5 + 5).', points('Difficulty', 2, (5, 5)),
      expected=D.split([(22, 'Competition – market may be saturated', ' 20m 10m (5 + 5)')],
                       ['Competition –', 'Customers –', 'Advertising –', 'Business structure /organisation –', 'Business knowledge –', 'Regulations –',
                        'Source of a site –', 'Start-up costs –']))
D.add(2, 'q6d', 'Q6(D)', P(7, 'Outline two taxes that Peter would be expected to pay.'), 10, 'business-3-18', 'business-taxes', 7, [6, 22],
      'Two taxes at 5 marks each (3 + 2).', points('Tax', 2, (3, 2)),
      expected=D.split([(22, 'VAT – on goods and services', ' 10m 2 @ 5m')],
                       ['VAT –', 'Income Tax (PAYE) –', 'Corporation Tax –', 'Motor Tax –', 'Property Tax –', 'Capital Gains Tax –', 'DIRT –', 'Employers PRSI']))
D.add(2, 'q6e', 'Q6(E)', P(7, 'Explain two types of insurance you would expect Peter’s business to have.'), 15, 'business-3-17', 'business-insurance-types', 7, [6, 22],
      'Two types: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Insurance', [(4, 4), (4, 3)]),
      expected=D.split([(22, 'Motor insurance – to cover', ' 15m 8m (4 + 4)')],
                       ['Motor insurance –', 'Buildings & Contents Insurance –', 'Public Liability Insurance –', 'Employers Liability Insurance –',
                        'Goods in Transit Insurance –', 'Plate Glass Window Insurance –', 'Product Liability Insurance –']))

devonport = P(8, 'Devonport Design Ltd, Ross Business Park, Sligo, designs electronic products for its customers. It needs new hardware and software. It is looking for a Sales Manager with a marketing degree and a minimum of three years management experience in sales, including online selling.')
D.add(2, 'q7a', 'Q7(A)', P(8, 'What do the following letters stand for: ICT and www?'), 10, 'business-2-12', 'ict-and-www', 8, [7, 23],
      'Each at 5 marks.', [response(i, f'{t} in full', [('answer', 'Words written in full', 5)]) for i, t in enumerate(['ICT', 'www'], 1)],
      expected=D.expected(23, 'Information and Communication Technology', 'World Wide Web'))
D.add(2, 'q7b', 'Q7(B)', devonport + '\n\n' + P(8, 'Explain the term hardware.'), 10, 'business-2-12', 'hardware-term', 8, [7, 23],
      'Explain the term for 10 marks (5 + 5).', [comps('Hardware', (5, 5))],
      expected=D.split([(23, 'Hardware: The physical aspects', ' 10m 5 + 5')], ['Hardware:']))
D.add(2, 'q7c', 'Q7(C)', P(8, 'Excluding social media, explain two ways in which a business uses modern technology.'), 20, 'business-2-12',
      'modern-technology-uses', 8, [7, 23], 'Two ways at 10 marks each (5 + 5).', points('Way', 2, (5, 5)),
      expected=D.split([(23, 'Self-service checkouts', ' Any appropriate technology accepted')],
                       ['Self-service checkouts –', 'Speedy stock ordering', 'Touch screen orders –', 'Video conferencing –', 'Email –', 'Apps –',
                        'Websites for online sales', 'Software for quick decision making –', 'Payroll software –']))
LETTER = [('senders-address', 'Sender’s Address', 2), ('date', 'Date', 2), ('receivers-address', 'Receiver’s Address', 2), ('reference', 'Reference', 2),
          ('opening-salutation', 'Opening Salutation', 1), ('opening-paragraph', 'Opening paragraph', 2), ('contents', 'Contents', 6),
          ('closing-salutation', 'Closing Salutation', 1), ('signature', 'Signature', 2)]
D.add(2, 'q7d', 'Q7(D)', devonport + '\n\n' + P(8, 'Brian Horan, who lives at 32 High Street, Sligo, worked for five years for a company which sold books online. He has an honours degree in marketing and a diploma in ICT. He applies for the position of Sales Manager.',
                                                'Draft Brian\'s letter of application, using today’s date, to Ms Rita Lynch, Human Resource Manager of Devonport Design Ltd.', sep=' '),
      20, 'business-2-12', 'letter-of-application', 8, [7, 24], 'The scheme’s nine elements: ' + '; '.join(f'{l} {m}' for _, l, m in LETTER) + '.',
      [response(1, 'Letter of application', LETTER)],
      expected=D.split([(24, '32 High Street Sligo', ' 20m Sender’s Address')],
                       ['32 High Street Sligo Co Sligo', '07/07/22', 'Ms Rita Lynch', 'Re: Sales Manager Position', 'Dear Ms Lynch',
                        'I refer to your advertisement', 'Yours sincerely', 'Brian Horan Brian Horan']),
      guidance=['The scheme prints “' + S(24, 'Contents 6m (3 + 3)') + '”.'],
      extra=['business-3-20'])
D.add(2, 'q7e', 'Q7(E)', P(8, 'Outline two functions of a Human Resource Manager.'), 15, 'business-3-20', 'hr-manager-functions', 8, [7, 25],
      'Two functions: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Function', [(4, 4), (4, 3)]),
      expected=D.split([(25, '(i) Training and Development', ' 15m 8m (4 + 4)')],
                       ['Training and Development', 'Recruitment', 'Employer/Employee Relations', 'Manpower planning', 'Performance appraisal', 'Pay and Rewards'],
                       drop=['(ii)', '(iii)', '(iv)', '(v)', '(vi)']))

laura = P(9, 'Laura Jones owns a cleaning business in a large town. Her customers include offices, schools and shops. She prepares her own financial records. She has a deposit account and a current account. She prepares a Cash Flow Forecast for her business.')
cff = P(9, 'Laura Cleaning Ltd CASH FLOW FORECAST May-July 2022', '2022 May June July € € €', 'Total Receipts 36,000 40,000 31,000', 'Total Payments 33,000 36,000 39,000',
        'Net Cash (Receipts – Payments) 3,000 4,000 – 8,000', 'Opening Cash 2,000 5,000 9,000', 'Closing Cash 5,000 9,000 1,000')
bs = P(9, 'Laura prepared the following extract from her Balance Sheet:') + '\n' + P(9, 'Balance Sheet extract € €', 'Current Assets: Debtors 24,000', 'Closing Stock 24,000 48,000',
                                                                                 'Current Liabilities: Creditors 19,000', 'Bank Overdraft 5,000 24,000')
D.add(2, 'q8a', 'Q8(A)', laura + '\n\n' + P(9, 'Explain the term fixed assets and state one example.'), 10, 'business-3-19', 'fixed-assets', 9, [7, 26],
      'Explanation 5 marks (3 + 2) and example 5 marks.', [comps('Fixed assets', (3, 2), ['Explanation', 'Explanation'], 1), comps('Example', (5,), ['Example'], 2)],
      expected=D.split([(26, 'Permanent items', ' 10m 5m (3 + 2)')], ['Permanent items (lasting longer than one year) owned by the business.', 'Examples:']))
D.add(2, 'q8b', 'Q8(B)', laura + '\n\n' + P(9, 'Explain the difference between a Current Account and a Deposit Account.'), 15, 'business-3-16',
      'current-versus-deposit-account', 9, [7, 26], 'Two comparisons: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Comparison', [(4, 4), (4, 3)]),
      expected=D.split([(26, 'Current accounts:', ' 15m 8m (4 + 4)')], ['Current accounts:', 'Deposit accounts:']))
D.add(2, 'q8c', 'Q8(C)', laura + '\n\n' + P(9, 'Outline two reasons why Laura might prepare a Cash Flow Forecast.'), 10, 'business-3-16', 'cash-flow-forecast-reasons', 9, [7, 26],
      'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)),
      expected=D.split([(26, 'To compare cash flow forecast', ' 10m 2 @ 5m')],
                       ['To compare cash flow forecast', 'To get a loan –', 'To predict inflows and outflows of cash –', 'To show months when there could be possible shortages',
                        'To show months with excess cash –']))
D.add(2, 'q8di', 'Q8(D)(i)', laura + '\n\n' + cff + '\n\n' + P(9, '(i) Does Laura Cleaning Ltd have a better cashflow position in June or July?'), 5, 'business-3-16',
      'better-cashflow-month', 9, [7, 27], 'The answer: 5 marks.', [comps('Month', (5,), ['Answer'])], expected=D.expected(27, '(i) June'))
D.add(2, 'q8dii', 'Q8(D)(ii)', laura + '\n\n' + cff + '\n\n' + P(9, '(ii) Outline two possible reasons for your answer.'), 15, 'business-3-16',
      'cashflow-month-reasons', 9, [7, 27], 'Two reasons: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Reason', [(4, 4), (4, 3)]),
      expected=D.split([(27, 'Total Receipts higher in June', ' 20m 5 8m')],
                       ['Total Receipts higher in June than in July,', 'Total Payments higher in July than June,', 'Laura still must pay her bills']))
for key, roman, name, prompt, formula, work, answer in [
        ('q8ei', 'i', 'Working capital ratio', '(i) Calculate the Working Capital Ratio (current ratio) for the year. Show all your workings.',
         'Current Assets : Current Liabilities', '24,000 + 24,000 : 19,000 + 5,000 €48,000 : €24,000', '= 2:1'),
        ('q8eii', 'ii', 'Acid test ratio', '(ii) Calculate the Acid Test Ratio for the year. Show all your workings.',
         '(Current Assets – Closing Stock) : Current Liabilities', '48,000 – 24,000 : 24,000 €24,000 : €24,000', '= 1:1')]:
    D.add(2, key, f'Q8(E)({roman})', laura + '\n\n' + bs + '\n\n' + P(9, prompt), 10, 'business-3-19', f"{name.lower().replace(' ', '-')}-calculation", 9, [7, 27],
          'Formula 2 marks, workings 6 marks and answer 2 marks.',
          [response(1, name, [('formula', 'Formula', 2), ('workings', 'Workings', 6), ('answer', 'Answer', 2)])],
          expected=D.expected(27, formula, work, answer),
          guidance=['The scheme’s table prints “' + S(7, '2 Formulae @ 2 marks each 2 workings @ 6 marks each 2 answers @ 2 marks each') + '” for (E).'])

patches = P(10, 'Patches Ltd manufactures children’s clothing which is sold under a brand name. Up until 2019 it operated as a partnership, but then changed to a private company limited by shares (Ltd). As well as selling children’s clothing, the company is now diversifying into other products. After doing some market research, it has just produced a new baby car seat.')
D.add(2, 'q9a', 'Q9(A)', patches + '\n\n' + P(10, 'Explain two of the underlined terms.'), 10, 'business-5-14', 'ownership-and-diversification-terms', 10, [7, 28],
      'Two terms at 5 marks each (3 + 2).', points('Term', 2, (3, 2)),
      expected=D.split([(28, 'Partnership A Partnership exists', ' 10m 2 @ 5m')], ['Partnership', 'Private Ltd Company', 'Diversifying']),
      guidance=['The paper underlines “partnership”, “private company limited by shares (Ltd)” and “diversifying” (page 10). A printed choice of two of the three: one card, every term marked alike.'],
      extra=['business-4-18'])
D.add(2, 'q9b', 'Q9(B)', patches + '\n\n' + P(10, 'Outline two reasons why market research is needed before developing a new product.'), 15, 'business-4-16',
      'market-research-reasons', 10, [7, 28], 'Two reasons: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Reason', [(4, 4), (4, 3)]),
      expected=D.split([(28, 'To find out if is there a demand', ' 15m 8m (4 + 4)')],
                       ['To find out if is there a demand for the product.', 'To find out if there is room in the market', 'To find out the size of the market',
                        'To find out more about competitors', 'To find out what customers want', 'To help determine the appropriate price',
                        'To find out the target market', 'To predict what customers will want', 'To find out the best type of promotion']))
D.add(2, 'q9c', 'Q9(C)', patches + '\n\n' + P(10, 'Outline two benefits of using a brand name.'), 15, 'business-4-17', 'brand-name-benefits', 10, [7, 29],
      'Two benefits: 8 marks (5 + 3) and 7 marks (5 + 2).', unequal('Benefit', [(5, 3), (5, 2)]),
      expected=D.split([(29, 'Product is more recognisable', ' 15m 8m (5 + 3)')],
                       ['Product is more recognisable/helps identify product.', 'Makes product stand out', 'Easier to introduce new products.',
                        'Recognised all over the world.', 'Creates brand loyalty.', 'Enables supplier to charge a higher price', 'Aids marketing']))
D.add(2, 'q9d', 'Q9(D)', patches + '\n\n' + P(10, 'Explain two factors that Patches Ltd might consider when setting the price of the new baby car seat.'), 15, 'business-4-17',
      'pricing-factors', 10, [7, 29], 'Two factors: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Factor', [(4, 4), (4, 3)]),
      expected=D.split([(29, 'Cost of production', ' 15m 8m (4 + 4)')],
                       ['Cost of production / research & development:', 'The target market:', 'Competition:', 'Type of product:', 'Economic conditions/demand:',
                        'Break-even point:']))
D.add(2, 'q9ei', 'Q9(E)(i)', patches + '\n\n' + P(10, '(i) Choose one suitable advertising medium to bring the new baby car seat to the attention of consumers.'), 5,
      'business-4-17', 'advertising-medium-choice', 10, [7, 30], 'One medium: 5 marks.', [comps('Medium', (5,), ['Medium'])],
      expected=D.expected(30, 'Television, newspapers, magazines', 'Accept any appropriate answer such as those in part (ii).'))
D.add(2, 'q9eii', 'Q9(E)(ii)', patches + '\n\n' + P(10, '(ii) Outline two reasons for your choice.'), 15, 'business-4-17', 'advertising-medium-reasons', 10, [7, 30],
      'Two reasons: 8 marks (4 + 4) and 7 marks (4 + 3).', unequal('Reason', [(4, 4), (4, 3)]),
      expected=D.split([(30, 'Television: large national market.', ' 20m 5 8m')],
                       ['Television:', 'Press:', 'Internet/Social media:', 'Radio:', 'Internet:', 'Cinema:', 'Posters and billboards:', 'Direct mail/flyers:']))

# ---------------------------------------------------------------- the sitting
for q in range(1, 16):
    D.atlas(1, q, 'p1', f'Every part of the 2022 Ordinary deferred Section 1 Question {q} was visually checked against the deferred booklet and scheme.')
for q in range(1, 10):
    D.atlas(2, q, 'p2', f'Every part of the 2022 Ordinary deferred Section 2 Question {q} was visually checked against the deferred booklet and scheme.')
D.emit({**{(1, str(q)): 15 for q in range(1, 16)}, **{(2, str(q)): 75 for q in range(1, 10)}},
       {1: 'No finite printed answer menu occurs in Section 1 (answer five of fifteen). True/False labels, the controller/facilitator ticks, '
           'the word bank, the tax matching grid and the SWOT words are required answers for every row. Skills, advantages and benefits '
           'in the support notes are open examples.',
        2: 'Printed choices are kept as one card each (choice is not a route): Q3(C) one of four EU institutions, Q5(E) Maslow or '
           'McGregor, Q6(A) one of two underlined terms, Q6(B)(ii) two of three sources, Q9(A) two of three underlined terms; the '
           'scheme marks every option alike and each files under one topic. Other lists in the support notes are open examples.'},
       {1: list(range(1, 37)), 2: list(range(1, 13)), 'scheme': list(range(1, 33))})
