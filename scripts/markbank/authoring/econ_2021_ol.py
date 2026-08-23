#!/usr/bin/env python3
"""Economics 2021 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.

Two parts here answer a question about two DIFFERENT subjects under one heading
— one economic effect of Brexit on the consumer and on the firm, one benefit of
perfect competition to the consumer and to society — and the scheme lists both
sets together. Each side is carded on its own, which is the rule for parallel
accounts, so a student picking "one effect on the consumer" is not offered the
firm's.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, card, load, point, tidy  # noqa: E402

P = Paper(2021, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Evidence of Data', 'Deduct')

P.menu('reasons why MNC’s locate in Ireland', 'econ-2021-ol-q11-b-iii',
       'economics-4-1', 'why-mncs-locate-in-ireland',
       'Outline two reasons why multinational companies locate in Ireland.',
       'A reason MNCs locate in Ireland — any two',
       'Two reasons, 7 marks each, split 3 for the reason and 4 for developing it.',
       drop=SCAFFOLD)

P.menu('outdoor flower market in Stoneybatter', 'econ-2021-ol-q12-b',
       'economics-2-0', 'assumptions-of-perfect-competition',
       'This firm operates in perfect competition where there are many homogeneous products. '
       'Discuss three main assumptions of this type of market structure.',
       'An assumption of perfect competition — any three',
       'Three assumptions, 5 marks each.',
       claim=3, per=5, drop=SCAFFOLD,
       stem='Set on a photograph of the outdoor flower market in Stoneybatter, Dublin, given as '
            'an example of perfect competition.')

P.menu('impact the introduction of a new mortgage lender', 'econ-2021-ol-q13-b-i',
       'economics-3-4', 'effect-of-a-new-mortgage-lender',
       'Outline the impact the introduction of a new mortgage lender in Ireland will have on '
       'consumers applying for a mortgage and on interest rates.',
       'An impact of a new lender — either one',
       'The scheme answers this in two halves — what it does for the borrower, and what it does '
       'to the rate — and pays 7 for each.',
       claim=2, per=7, drop=SCAFFOLD)

P.menu('one measure the Irish government could use to achieve', 'econ-2021-ol-q13-c-ii',
       'economics-0-2', 'measures-for-sustainable-objectives',
       'Outline one measure the Irish government could use to achieve its objectives on care for '
       'the environment and sustainable development.',
       'A measure the government could take — any one',
       'One measure, 8 marks.',
       claim=1, per=8, drop=SCAFFOLD)

P.menu('reasons why the Irish Government may intervene', 'econ-2021-ol-q13-c-iii',
       'economics-1-3', 'why-government-intervenes',
       'Outline two reasons why the Irish Government may intervene in an economy.',
       'A reason for government intervention — any two',
       'Two reasons, 5 marks each.',
       drop=SCAFFOLD)

P.menu('one social benefit and one economic benefit resulting from the introduction of the sugar tax',
       'econ-2021-ol-q14-a-i', 'economics-2-2', 'benefits-of-the-sugar-tax',
       'Explain one social benefit and one economic benefit resulting from the introduction of '
       'the sugar tax in Ireland.',
       'A benefit of the sugar tax — any two',
       'Two benefits, 10 marks each. The scheme lists the social benefits first and the economic '
       'ones after, and the question wants one of each.',
       drop=SCAFFOLD)

P.menu('Discuss one economic effect Brexit will have on each of the following',
       'econ-2021-ol-q15-a-i', 'economics-4-2', 'effects-of-brexit-on-consumers-and-firms',
       'Discuss one economic effect Brexit will have on the Irish consumer and one on the Irish '
       'firm.',
       'An economic effect of Brexit — any two',
       'Two effects, 8 marks each. The scheme lists the consumer effects first and the firm '
       'effects after, and the question wants one of each.',
       drop=SCAFFOLD)

P.menu('Irish exports to the UK have grown by 16%', 'econ-2021-ol-q15-a-ii',
       'economics-4-2', 'benefits-of-exports-to-ireland',
       'Irish exports to the UK have grown by 16% despite the uncertainty surrounding Brexit. '
       'Outline one benefit of this for the Irish economy.',
       'A benefit of rising exports — any one',
       'One benefit, 8 marks.',
       # The scheme's list here runs straight into the next question with no
       # marker of any kind, so the tail is bounded by count: five named
       # benefits, then the examiner's data-evidence note.
       claim=1, per=8, drop=SCAFFOLD, cap=5)

P.menu('one advantage or one disadvantage of Globalisation', 'econ-2021-ol-q11-b-i-neg',
       'economics-4-1', 'disadvantages-of-globalisation',
       'Outline one disadvantage of globalisation.',
       'A disadvantage of globalisation — any one',
       'One disadvantage, 5 marks.',
       ref='2021 OL Q11(b)(i) — disadvantage',
       claim=1, per=5,
       drop=SCAFFOLD + ('Improvements in fair trade', 'New experiences',
                        'Improved government relations', 'Possible disadvantages'),
       notes='The part lets a student answer with EITHER an advantage or a disadvantage and the '
             'scheme heads the two lists separately, so each side is its own card.')

P.menu('one advantage or one disadvantage of Globalisation', 'econ-2021-ol-q11-b-i-pos',
       'economics-4-1', 'advantages-of-globalisation',
       'Outline one advantage of globalisation.',
       'An advantage of globalisation — any one',
       'One advantage, 5 marks.',
       ref='2021 OL Q11(b)(i) — advantage',
       claim=1, per=5, drop=SCAFFOLD, stop='Possible disadvantages')


# ── Two figure cards ────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2021-ol-q12-a-i', 2021, 'ordinary', 'economics-2-0', 'labelling-perfect-competition',
    '2021 OL Q12(a)(i)',
    'The diagram shows the long run equilibrium of a firm in perfect competition. Write out in '
    'full what each of the four labels represents.',
    'fixed', 20,
    [point('r-mc', 'Marginal Cost', 5, 'MC — the steeply rising curve.'),
     point('r-ac', 'Average Cost', 5, 'AC — the U-shaped curve whose minimum is point B.'),
     point('r-ar', 'Average Revenue', 5, 'AR — part of the horizontal line D = AR = MR.'),
     point('r-mr', 'Marginal Revenue', 5, 'MR — the same horizontal line: for a price taker '
                                          'demand, average revenue and marginal revenue coincide.')],
    '', tariff_kind='fixed',
    figure_key='economics-2021-OL-paper-p13-i0',
    label_key=[{'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
               {'letter': 'AC', 'meaning': 'Average Cost', 'askedInThisQuestion': True},
               {'letter': 'AR', 'meaning': 'Average Revenue', 'askedInThisQuestion': True},
               {'letter': 'MR', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': True}]))

P.cards.append(card(
    'econ-2021-ol-sa-q6-a', 2021, 'ordinary', 'economics-3-0', 'reading-the-circular-flow',
    '2021 OL Section A Q6(a)',
    'The diagram represents the circular flow of income in an open economy without the '
    'government. State what the flows numbered 1 to 3 represent.',
    'fixed', 15,
    [point('r-1', 'Incomes for supplying the factors of production', 9,
           'Flow 1 — the outer arc running from Firms back to Households.'),
     point('r-2', 'Savings', 3, 'Flow 2 — Households to Financial Institutions. A leakage.'),
     point('r-3', 'Exports', 3, 'Flow 3 — Foreign Markets to Firms. An injection.')],
    'The three unlabelled flows are the ones a student has to supply; the rest of the diagram '
    'names its own.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-OL-paper-p06-art',
    label_key=[{'letter': '1', 'meaning': 'Incomes for supplying the factors of production',
                'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'Savings', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'Exports', 'askedInThisQuestion': True}]))


# ── Section B, second pass ──────────────────────────────────────────────────
P.menu('Monetary policy and delivering price stability', 'econ-2021-ol-q13-a-iii',
       'economics-3-3', 'monetary-policy-and-price-stability',
       'Monetary policy and delivering price stability is a concern for everyone. Explain one of '
       'the terms in bold in the statement above.',
       'One of the two terms — either one',
       'One term, 8 marks. The part offers a choice of the two, so either earns the marks.',
       ref='2021 OL Q13(a)(iii)', claim=1, per=8,
       drop=('Possible responses', 'Suggested responses'))

P.menu('general prices of goods and services rose in Ireland',
       # the plain id is taken by an earlier card on this paper
       'econ-2021-ol-q13-c-iii-types',
       'economics-3-3', 'types-of-inflation-ol',
       'The general prices of goods and services rose in Ireland during 2000 to 2007. Explain one '
       'type of inflation that could account for this.',
       'A type of inflation — any one',
       'One type, 7 marks. The scheme names demand-pull, cost-push and imported inflation.',
       ref='2021 OL Q13(c)(iii)', claim=1, per=7,
       drop=('Possible responses', 'Suggested responses'))


# ── Section B, third pass: the remaining open parts ─────────────────────────
# Everything below is sliced straight out of the scheme with block(), because
# econ_parts cannot separate these: single printed answers whose mark cell
# interrupts the question, parallel accounts under one heading, and answers the
# extractor welds to the cue. as_option() strips the page furniture and stops a
# slice where the next part begins, exactly as the menu path does.
BODY = tidy(load(2021, 'ordinary'))


def sl(start, end=None, occ=None):
    """One marking point, sliced from the scheme and cleaned of furniture."""
    return as_option(block(BODY, start, end, occ))


P.cards.append(card(
    'econ-2021-ol-q11-a-ii', 2021, 'ordinary', 'economics-4-0', 'what-improved-irelands-hdi',
    '2021 OL Q11(a)(ii)',
    'Explain what might have caused this change in Ireland’s position on the HDI '
    'between 2019 and 2020.',
    '1 @ 8', 8,
    [anyN('r-1', 'A cause of the improvement — either one', 8, 1, 8,
          [sl('Life expectancy has increased', 'Mean years of schooling has increased'),
           sl('Mean years of schooling has increased', '(b) (i) Outline one advantage')],
          'One cause, 8 marks: 4 for the cause and 4 for developing it.')],
    'The paper asks this off the answers to (i) — rank, life expectancy and mean years of '
    'schooling all improved — and the scheme credits either driver of the change.',
    stem='Set on HDI tables for Ireland: ranked 3rd in 2019 and 2nd in 2020, with life '
         'expectancy at birth up from 82.1 to 82.3 years and mean years of schooling up '
         'from 12.5 to 12.7.'))

P.cards.append(card(
    'econ-2021-ol-q11-b-ii', 2021, 'ordinary', 'economics-4-1', 'mncs-operating-in-ireland',
    '2021 OL Q11(b)(ii)',
    'Name two multinational companies (MNCs) that operate in Ireland.',
    '2 @ 3', 6,
    [anyN('r-1', 'An MNC operating in Ireland — any two', 6, 2, 3,
          [n.strip() for n in
           sl('Apple / Google', '(iii) Outline two reasons why MNC').split('/') if n.strip()],
          'Two companies, 3 marks each.')],
    'The scheme prints its accepted companies as one slash-separated run; split here on the '
    'scheme’s own separators so each name is offered on its own.'))

P.cards.append(card(
    'econ-2021-ol-q11-c-i', 2021, 'ordinary', 'economics-3-5', 'what-economic-growth-is',
    '2021 OL Q11(c)(i)',
    'Foreign Direct Investment (FDI) has been a key contributor to Ireland’s economic growth. '
    'Explain the term economic growth.',
    'fixed', 10,
    [point('r-1', sl('It is the rise in GNP/output', '(ii) Explain your understanding'), 10,
           'Any one of the three wordings — rise in GNP per head over time, or increased '
           'productive capacity — earns the 10.')],
    '', tariff_kind='fixed'))

# econ_excluded records Q11(c)(ii) as "the definition welded to the cue and
# only an examples line after" — a reading taken off the extractor's view of
# the part. The scheme itself prints the explanation as a clean paragraph ⟨10⟩
# and the accepted products as a slash-run ⟨2 @ 5⟩, so the part is carded after
# all; the econ_excluded line is now stale.
P.cards.append(card(
    'econ-2021-ol-q11-c-ii', 2021, 'ordinary', 'economics-4-0', 'the-fair-trade-movement',
    '2021 OL Q11(c)(ii)',
    'Explain your understanding of the Fair‐Trade Movement. Give two examples of fair‐trade '
    'products that you can buy.',
    'fixed', 20,
    [point('r-expl', sl('Fair Trade is a trading partnership', 'Examples:'), 10,
           'The explanation, 10 marks.'),
     anyN('r-ex', 'A fair-trade product — any two', 10, 2, 5,
          [n.strip() for n in sl('Bananas/Coffee', 'Question 12').split('/') if n.strip()],
          'Two products, 5 marks each.')],
    'The scheme prints its accepted products as one slash-separated run; split here on the '
    'scheme’s own separators so each is offered on its own.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q12-c-i-consumer', 2021, 'ordinary', 'economics-2-0',
    'perfect-competition-benefits-consumer',
    '2021 OL Q12(c)(i) — the consumer',
    'Outline one benefit of perfect competition as a market for the consumer.',
    '1 @ 8', 8,
    [anyN('r-1', 'A benefit to the consumer — any one', 8, 1, 8,
          [sl('Low prices: the firm sells', '• Normal profit: the firm earns'),
           sl('Normal profit: the firm earns', 'The economy in general')],
          'One benefit, 8 marks: 4 for the point and 4 for development.')],
    'The part asks for one benefit for the consumer and one for the economy in general, and '
    'the scheme heads the two lists separately, so each side is its own card.'))

P.cards.append(card(
    'econ-2021-ol-q12-c-i-economy', 2021, 'ordinary', 'economics-2-0',
    'perfect-competition-benefits-economy',
    '2021 OL Q12(c)(i) — the economy in general',
    'Outline one benefit of perfect competition as a market for the economy in general.',
    '1 @ 8', 8,
    [anyN('r-1', 'A benefit to the economy — any one', 8, 1, 8,
          [sl('No advertising: all the goods', '• Efficiency is encouraged'),
           sl('Efficiency is encouraged', '(ii) Firms in perfect competition')],
          'One benefit, 8 marks: 4 for the point and 4 for development.')],
    'The other half of the part; the consumer’s benefits are their own card.'))

P.cards.append(card(
    'econ-2021-ol-q12-c-ii', 2021, 'ordinary', 'economics-2-0', 'snps-attract-new-entrants',
    '2021 OL Q12(c)(ii)',
    'Firms in perfect competition may earn super normal profits in the short run. Outline what '
    'might happen to the number of firms in the industry in the long run. Give a reason for '
    'your answer.',
    'fixed', 8,
    [point('r-1', sl('Other firms will be aware of the SNPs', 'Question 13'), 8,
           '4 for what happens — more firms enter — and 4 for the reason: perfect knowledge '
           'and no barriers to entry.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q13-a-i', 2021, 'ordinary', 'economics-2-1', 'what-the-minimum-wage-is',
    '2021 OL Q13(a)(i)',
    'The Irish government is accused of resisting EU changes to the minimum wage. Outline what '
    'is meant by the term minimum wage.',
    'fixed', 8,
    [point('r-1', sl('The lowest wage employers must by law', '(ii) A government may use'), 8,
           'One definition, 8 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q13-a-ii', 2021, 'ordinary', 'economics-3-1', 'what-fiscal-policy-is',
    '2021 OL Q13(a)(ii)',
    'A government may use fiscal policy in its budget to help achieve its economic aims. '
    'Explain what is meant by fiscal policy.',
    'fixed', 8,
    [point('r-1', sl('Fiscal Policy: Any actions taken', '(iii) Monetary policy'), 8,
           'One definition, 8 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q13-b-ii', 2021, 'ordinary', 'economics-3-4', 'why-the-central-bank-fines-firms',
    '2021 OL Q13(b)(ii)',
    'The Central Bank of Ireland imposed a fine of €4.1 million on Davy Stockbrokers. Outline '
    'one reason why the Central Bank of Ireland imposes fines like this on financial '
    'institutions.',
    'fixed', 7,
    [point('r-1', sl('Central Bank may fine regulated entities', '(c) (i) State the term'), 7,
           'One reason, 7 marks: regulation to ensure financial stability, consumer protection '
           'and market integrity.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q13-c-i', 2021, 'ordinary', 'economics-3-3', 'what-deflation-is',
    '2021 OL Q13(c)(i)',
    'State the term used to describe when the price of goods and services are falling in a '
    'country.',
    'fixed', 5,
    [point('r-1', sl('Deflation.', '(ii) The diagram below shows the changing inflation'), 5,
           'The term, 5 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    # econ-2021-ol-q14-a-i is taken: the sugar-tax card shipped under that id and
    # its citation was corrected to Q16(b)(i) in econ_refs.py. The id here is
    # suffixed rather than reused, because a card id is a review-history key.
    'econ-2021-ol-q14-a-i-capital', 2021, 'ordinary', 'economics-3-1',
    'current-versus-capital-expenditure',
    '2021 OL Q14(a)(i)',
    'Is the above an example of current or capital government expenditure? Explain your answer.',
    'fixed', 14,
    [point('r-verdict', sl('Capital expenditure.', 'This is a once off'), 7, 'The verdict, 7.'),
     point('r-why', sl('This is a once off/long term', '(ii) The spending by the government'), 7,
           'The explanation, 7 — a once-off, long-term item citizens benefit from for years.')],
    'The scheme prints ⟨7⟩ against the verdict and ⟨7⟩ against the explanation; the third ⟨7⟩ '
    'on the page is part (ii)’s tariff, printed a row early.',
    stem='The ESB and Bord na Móna are pleased to announce that agreement has been reached on '
         'the €160m Oweninny Project (wind farm technology) in North County Mayo.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q14-a-ii', 2021, 'ordinary', 'economics-0-1', 'what-opportunity-cost-is',
    '2021 OL Q14(a)(ii)',
    'The spending by the government on the Oweninny Project is €160 million and this involves '
    'an opportunity cost. Explain the term opportunity cost.',
    'fixed', 7,
    [point('r-1', sl('The cost of foregone alternatives', '(b) (i) Define the term mixed'), 7,
           'One definition applied to the windfarm, 7 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q14-b-i', 2021, 'ordinary', 'economics-1-0', 'what-a-mixed-economy-is',
    '2021 OL Q14(b)(i)',
    # The paper's part marker is kept in the question: "Define the term mixed
    # economy" is five words, one short of the six-word run econ_refcheck needs
    # to place a card, and HAND_CHECKED lives in econ_refs.py. The paper prints
    # the marker as part of the line, so quoting it keeps the citation checked.
    '(i) Define the term mixed economy.',
    'fixed', 8,
    [point('r-1', sl('An economy that incorporates elements',
                     '(ii) Outline one measure the Irish government'), 8,
           'One definition, 8 marks: both central planning and private enterprise play a role '
           'in allocating resources.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q14-c-ii', 2021, 'ordinary', 'economics-3-1', 'vat-is-an-indirect-tax',
    '2021 OL Q14(c)(ii)',
    'Is Value Added Tax a direct tax or an indirect tax? Explain your answer.',
    'fixed', 10,
    [point('r-verdict', sl('Indirect Tax.', 'It is a tax on spending'), 5, 'The verdict, 5.'),
     point('r-why', sl('It is a tax on spending',
                       '(iii) Outline two reasons why the Irish Government'), 5,
           'The explanation, 5 — a tax on spending, not on income.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    # econ-2021-ol-q15-a-i is taken: the Brexit-effects card shipped under that
    # id and its citation was corrected to Q16(c)(i) in econ_refs.py.
    'econ-2021-ol-q15-a-i-supply', 2021, 'ordinary', 'economics-1-2', 'the-law-of-supply',
    '2021 OL Q15(a)(i)',
    'State the law of supply. Give an example to support your answer.',
    'fixed', 8,
    [point('r-1', sl('The Law of Supply states that as prices rise',
                     'Any appropriate example', occ=0), 8,
           'The scheme closes the list "Any appropriate example." — the 8 covers the statement '
           'supported with an example.')],
    '', stem='The first notable increase in hand sanitiser sales occurred during the '
             '2009–2010 Swine Flu outbreak.',
    tariff_kind='fixed'))

P.cards.append(card(
    # econ-2021-ol-q15-a-ii is likewise taken, corrected to Q16(c)(ii).
    'econ-2021-ol-q15-a-ii-sanitiser', 2021, 'ordinary', 'economics-1-2', 'law-of-supply-applied',
    '2021 OL Q15(a)(ii)',
    'Does the law of supply apply to hand sanitiser in 2021? Explain your answer.',
    'fixed', 7,
    [point('r-1', sl('Yes. The Law of Supply', '(b) Nike'), 7,
           'Yes, with the law restated and applied to 2021: as the price consumers were '
           'willing to pay rose, supply rose.')],
    '', stem='The first notable increase in hand sanitiser sales occurred during the '
             '2009–2010 Swine Flu outbreak.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q15-b-ii', 2021, 'ordinary', 'economics-1-2', 'input-costs-shift-supply',
    '2021 OL Q15(b)(ii)',
    'The cost of cotton which is a raw material used in the production of Nike Clothing '
    'increases. Would this impact on the demand curve or the supply curve? Explain your answer.',
    'fixed', 15,
    [point('r-verdict', sl('Supply curve.', 'An increase in the price of cotton'), 8,
           'The verdict, 8.'),
     point('r-why', sl('An increase in the price of cotton', '(iii) Many consumers'), 7,
           'The explanation, 7 — a higher input cost shifts supply to the left.')],
    '', stem='Nike is famous for its ‘Just do it’ advertising campaign.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q15-b-iii', 2021, 'ordinary', 'economics-1-1', 'what-consumer-loyalty-is',
    '2021 OL Q15(b)(iii)',
    'Many consumers are loyal to the Nike brand. Explain what is meant by the term consumer '
    'loyalty.',
    'fixed', 10,
    [point('r-1', sl('A consumer may become strongly attached', '(c) (i) All economic goods'), 10,
           'One explanation, 10 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q15-c-i', 2021, 'ordinary', 'economics-0-1', 'the-concept-of-scarcity',
    '2021 OL Q15(c)(i)',
    'All economic goods are scarce and this affects how we make spending decisions. Explain '
    'the concept of scarcity.',
    'fixed', 10,
    [point('r-1', sl('Scarcity means that resources are limited', '(ii) Explain how scarcity'),
           10, '7 for the concept, 3 for development.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q15-c-ii', 2021, 'ordinary', 'economics-0-1', 'scarcity-and-consumer-choice',
    '2021 OL Q15(c)(ii)',
    'Explain how scarcity can affect my decision making as a consumer.',
    '1 @ 5', 5,
    [anyN('r-1', 'How scarcity shapes the choice — either one', 5, 1, 5,
          [sl('The scarcer a good / service', 'Because of scarcity'),
           sl('Because of scarcity a consumer', '(iii) Since the UK left the EU')],
          'One explanation, 5 marks.')],
    'The scheme prints the two accounts as consecutive paragraphs; each is its own option.'))

P.cards.append(card(
    'econ-2021-ol-q15-c-iii', 2021, 'ordinary', 'economics-4-2', 'what-a-tariff-is',
    '2021 OL Q15(c)(iii)',
    'Since the UK left the EU, EU consumers, buying goods online from the UK, now pay tariffs. '
    'Explain what is meant by the term tariff.',
    'fixed', 10,
    [point('r-1', sl('A tax on imported goods from abroad.', 'Question 16'), 10,
           '7 for the definition, 3 for development.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-q16-a', 2021, 'ordinary', 'economics-0-0', 'factors-of-production',
    '2021 OL Q16(a)',
    'Complete the table below explaining, using examples, the factors of production, other '
    'than capital, required for the sale of fizzy drinks. One factor of production has been '
    'completed for you.',
    '3 @ 8', 24,
    [point('r-land', sl('Land is anything supplied by nature', 'Labour is the human effort'), 8,
           'Land, with an example — the ground the factory is built on, or the raw materials.'),
     point('r-labour', sl('Labour is the human effort', 'Enterprise is the factor'), 8,
           'Labour, with an example — the workers who produce the fizzy drinks.'),
     point('r-enterprise', sl('Enterprise is the factor',
                              '(b) The Irish government raised over €33 million'), 8,
           'Enterprise, with an example — the owner or shareholder who takes the risks.')],
    'The Capital row is completed on the paper as the worked example; each remaining factor '
    'is paid 8 for a definition with an example.',
    tariff_kind='fixed',
    figure_key='economics-2021-OL-paper-p25-i0'))

P.cards.append(card(
    'econ-2021-ol-q16-b-ii', 2021, 'ordinary', 'economics-2-2', 'what-market-failure-is',
    '2021 OL Q16(b)(ii)',
    'Explain, giving an example, what is meant by the term Market Failure.',
    '1 @ 7', 7,
    [anyN('r-1', 'What market failure is — any one account', 7, 1, 7,
          [sl('Market failure happens', 'Complete market failure'),
           sl('Complete market failure', 'Partial failure occurs'),
           sl('Partial failure occurs', '(c) On 1st January 2020')],
          'One account with an example, 7 marks: 4 + 3.')],
    'The scheme accepts the general account or either named form — complete or partial '
    'failure — each with its example.',
    stem='The Irish government raised over €33 million in sugar tax in 2019.'))

P.emit()
