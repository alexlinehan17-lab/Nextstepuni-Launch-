#!/usr/bin/env python3
"""Economics 2014 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2014-hl-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2014
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The scheme reprints each question above its answer, so a
slice always starts after the reprinted wording. A stem stops before any
printed table: the table is the crop beside the typed ask. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.

This scheme's bullets are drawn in SymbolMT, whose text layer reports each as
the letter "x" at the start of a line. A response is therefore never sliced
across one: a bulleted list is cut at its bullets (`xb`), and a response whose
bullets belong together is read where the scheme file holds it without them
(its column rendering), so every slice still traces.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import TAIL, Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, as_option, emit, point, tidy  # noqa: E402

H = Old(2014, 'higher', 'LC034ALP000EV')
D = OldDeck(2014, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2014-HL-scheme-'
PAP = 'economics-2014-HL-paper-'
XB = re.compile(r'(?:^|\n)x ')


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def xb(start, end, occ=None):
    """The scheme's SymbolMT bullet list between two anchors, cut at each bullet."""
    raw = H.chunk(start, end, occ)
    out = []
    for piece in XB.split(raw):
        piece = TAIL.sub('', as_option(tidy(piece))).strip()
        if piece:
            out.append(H.traced(piece))
    return out


def joined(start, end, occ=None):
    """A response whose SymbolMT bullets belong together, read as one: the bullets
    joined where the scheme file prints them without the bullet letters."""
    return H.traced(' '.join(xb(start, end, occ)))


def headed(start, end, firsts, occ=None):
    """Headed responses, each named by its head: "<head> — <response>", a
    response printed as SymbolMT bullets read with its bullets joined."""
    out = []
    for head, opt in zip(firsts, H.split(start, end, firsts, occ)):
        body = opt[len(head):].strip()
        bullets = ' '.join(b.strip() for b in re.split(r'(?:^|\s)x\s', body) if b.strip())
        out.append(f'{H.traced(head)} — {H.traced(bullets)}' if bullets else H.traced(head))
    return out


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def defined(head, start, end):
    """A defined term as the scheme heads it: "<term> — <definition>"."""
    return f'{H.traced(head)} — {H.opt(start, end)}'


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ opportunity cost
add('sa-q1', '0-1', 'opportunity-cost-for-the-government', ref('A', 1),
    H.q(2, 'Define the term ‘opportunity cost’.', ' Definition:'), '8 + 8', 16,
    [point('r-definition', H.opt('Opportunity cost is the cost of forgone alternatives', '\nState one example'), 8,
           'The definition, 8 marks.'),
     heading('r-example', 'An example facing the government — any one',
             xb('Spending on a new hospital the opportunity cost', 'Definition: 8 marks'), 8,
             'One example, 8 marks: these are the scheme’s sample responses, not a closed list.')],
    **A)

# Q2 ─ marginal and average cost
q2 = H.q(2, 'If the marginal cost (MC) is less than average cost (AC)', ' (i)')
add('sa-q2-i', '1-5', 'when-mc-is-below-ac', ref('A', 2, '(i)'),
    H.q(2, 'Is this statement true? Circle the correct answer.', ' (ii)'), '1', 1,
    [point('r-1', H.traced('YES'), 1, 'The circled answer, 1 mark: the scheme circles YES.')], stem=q2, **A)
add('sa-q2-ii', '1-5', 'why-ac-falls', ref('A', 2, '(ii)'), H.q(2, 'Explain the reason for your answer:', ' _'), '15', 15,
    [point('r-1', H.opt('If the additional cost of producing one extra unit', '\nCircle correct answer'), 15,
           'The explanation, 15 marks.')], stem=q2, **A)

# Q3 ─ structural unemployment
add('sa-q3', '3-2', 'structural-unemployment', ref('A', 3),
    H.q(2, 'Define the term ‘structural unemployment’', ' Definition:'), '10 + 6', 16,
    [point('r-definition', H.opt('Structural unemployment arises from a change', '\nOne policy response'), 10,
           'The definition, 10 marks.'),
     heading('r-policy', 'One policy response — any one', xb('A retraining scheme so that long-term', 'Definition: 10 marks'), 6,
             'One policy measure, 6 marks.')],
    **A)

# Q4 ─ complementary goods
add('sa-q4', '1-1', 'complementary-goods', ref('A', 4),
    H.q(3, 'Explain the meaning of the term ‘complementary goods’', ' Explanation:'), '12 + 4', 16,
    [point('r-explanation', H.opt('Goods which are consumed together', '\nExample:'), 12, 'The explanation, 12 marks.'),
     point('r-example', H.opt('Computer consoles and software/games', '\nExplanation: 12'), 4,
           'An example, 4 marks: the scheme gives two.')],
    **A)

# Q5 ─ monopoly
add('sa-q5', '2-0', 'assumptions-of-monopoly', ref('A', 5),
    H.q(3, 'State three assumptions/characteristics underlying the theory of monopoly.', ' (i)'), '6 + 5 + 5', 16,
    [anyN('r-1', 'An assumption — any three', 16, 3, 6, xb('There is only one firm in the industry', '3 assumptions:'),
          'Three assumptions: the 1st correct answer 6 marks, the 2nd and 3rd 5 each.', steps=[6, 5, 5])],
    **A)

# Q6 ─ a stronger euro against the dollar
add('sa-q6', '4-2', 'a-stronger-euro-against-the-dollar', ref('A', 6),
    H.q(3, 'Outline two possible economic effects for the Irish Economy of the euro', ' (i)'), '10 + 7', 17,
    [anyN('r-1', 'An effect — any two', 17, 2, 10,
          H.split('Import prices are cheaper', '1st correct answer: 10',
                  ['Import prices are cheaper', 'Export Prices Dearer', 'Falling Employment',
                   'Effect on tourism revenue in Ireland', 'Foreign Direct Investment / Irish investment in US']),
          'Two effects: the 1st correct answer 10 marks, the 2nd 7.', steps=[10, 7])],
    **A)

# Q7 ─ the return to enterprise
add('sa-q7', '0-1', 'the-return-to-enterprise', ref('A', 7),
    H.q(3, 'Outline two ways in which the return to the factor of production enterprise', ' (i)'), '10 + 7', 17,
    [anyN('r-1', 'A way — any two', 17, 2, 10,
          H.split('It can earn a loss', '1st correct response: 10', ['It can earn a loss', 'Returns can vary', 'Return is residual']),
          'Two ways: the 1st correct response 10 marks, the 2nd 7.', steps=[10, 7])],
    **A)

# Q8 ─ exiting the bailout
add('sa-q8', '3-1', 'exiting-the-bailout', ref('A', 8),
    H.q(4, 'Outline two possible economic implications for the Irish economy', ' (i)'), '11 + 6', 17,
    [anyN('r-1', 'An implication — any two', 17, 2, 11,
          headed('Increased consumer confidence', '1st correct response: 11',
                 ['Increased consumer confidence', 'Increased economic sovereignty',
                  'More difficult for government to maintain fiscal discipline', 'Increased governance by outside agencies',
                  'Improved global perception of Irish economy']),
          'Two implications: the 1st correct response 11 marks, the 2nd 6. ' + H.traced('The expected responses given are not exhaustive.'),
          steps=[11, 6])],
    stem=H.q(4, 'Ireland recently emerged from the EU/IMF/ECB', ' Outline two'), **A)

# Q9 ─ the pylons' social costs and benefits
add('sa-q9', '2-2', 'social-costs-and-benefits-of-pylons', ref('A', 9),
    H.q(4, 'Outline two possible social costs and two possible social benefits', ' Social Costs:'), '5 + 4 + 4 + 4', 17,
    [anyN('r-1', 'Two social costs and two social benefits', 17, 4, 5,
          side('Social Costs', H.split('Visual intrusion on the landscape', 'Social Benefits could include:',
                                       ['Visual intrusion on the landscape', 'Possible health implications',
                                        'Potential damage to wildlife habitats', 'Decline in land and house prices']))
          + side('Social Benefits', H.split('Improved infrastructure / secure supply of electricity', '1st correct response: 5',
                                            ['Improved infrastructure / secure supply of electricity',
                                             'Opportunities within the renewable energy sector',
                                             'Increased capacity of renewable energy'])),
          'Two costs and two benefits, on one ladder: the 1st correct response 5 marks, the 2nd, 3rd and 4th 4 each.',
          steps=[5, 4, 4, 4])],
    **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ utility; the law of supply; the concert
q1a_table = PAP + 'p05-q1a-table'
add('sb-q1-a-i', '1-1', 'diminishing-marginal-utility', ref('B', 1, '(a)(i)'),
    H.q(5, 'State and explain the law illustrated in the above table.', ' (ii)'), '4 + 9', 13,
    [point('r-statement', H.traced('This table illustrates the Law of Diminishing Marginal Utility.'), 4, 'The statement, 4 marks.'),
     point('r-explanation', H.opt('This law states that as a consumer consumes more units', '\nStatement: 4 marks'), 9,
           'The explanation, 9 marks.')],
    figure=q1a_table, **B)
pick('sb-q1-a-ii', '1-1', 'assumptions-of-diminishing-utility', ref('B', 1, '(a)(ii)'),
     H.q(5, 'Outline two assumptions underlying this law.', ' (25)'), 'An assumption — any two',
     H.split('Applies after ‘the origin’', '2 Assumptions: 6 marks',
             ['Applies after ‘the origin’', 'Consumer tastes do not change', 'Consumer incomes do not change',
              'No time lapse between the consumption of successive units']),
     2, 6, 'Two assumptions, 6 marks each.', **B)
q1b_i = H.q(5, 'State the ‘Law of Supply’, and illustrate with a labelled diagram.', ' (ii)')
add('sb-q1-b-i', '1-2', 'the-law-of-supply', ref('B', 1, '(b)(i)'), q1b_i, '4 + 4', 8,
    [point('r-statement', H.opt('The law of supply states that there is a positive relationship', '\nStatement: 4 marks'), 4,
           'The statement, 4 marks.'),
     ask_row('r-diagram', q1b_i[q1b_i.index('illustrate'):].rstrip('.'), 4,
             'The diagram, 4 marks: a rising supply curve against P and Q, as the figure shows.')],
    kind='fixed', figure=SOL + 'p10-q1bi-diagram', **B)
add('sb-q1-b-ii', '1-2', 'technical-progress-and-supply', ref('B', 1, '(b)(ii)'),
    H.q(5, 'Explain how technical progress affects the supply curve.', ' (iii)'), '6', 6,
    [point('r-1', H.opt('Technical progress, such as the introduction of a labour saving device', '\nExplanation: 6 marks'), 6,
           'The explanation, 6 marks.')], **B)
pick('sb-q1-b-iii', '1-2', 'what-shifts-supply', ref('B', 1, '(b)(iii)'),
     H.q(5, 'Outline, with the aid of labelled diagrams, two other factors', ' (30)'), 'A factor, with its diagram — any two',
     H.split('Cost of inputs\nIf there', 'Increase in quantity supplied Decrease',
             ['Cost of inputs', 'Number of sellers in the market', 'Changes in Taxation/Subsidy',
              'Changes in the price of related goods in production', 'Changes in expectations', 'Changes in unplanned factors']),
     2, 8, H.traced('2 factors stated, explained with correctly labelled diagram: 8 marks each') + '. The scheme’s two '
     'diagrams, an increase and a decrease in supply, are shown with the answer.', figure=SOL + 'p11-q1biii-diagrams', **B)
q1c = H.q(5, 'Macklemore announces a concert in Ireland', ' (i)')
q1c_i = H.q(5, 'Draw one labelled diagram, showing a market demand curve', ' (ii)')
add('sb-q1-c-i', '1-0', 'the-sold-out-concert', ref('B', 1, '(c)(i)'), q1c_i, '8 + 4', 12,
    [ask_row('r-diagram', q1c_i[:q1c_i.index(' Explain')].rstrip('.'), 8,
             'The diagram, 8 marks: a vertical supply curve at 80,000 and a demand curve crossing it at €65, as the figure shows.'),
     point('r-explanation', joined('Supply of Macklemore tickets is fixed', 'Correct diagram: 8 marks'), 4,
           'The explanation, 4 marks.')],
    kind='fixed', stem=q1c, figure=SOL + 'p12-q1ci-diagram', **B)
pick('sb-q1-c-ii', '1-1', 'consumer-surplus-and-ticket-prices', ref('B', 1, '(c)(ii)'),
     H.q(5, 'Explain, using the concept of Consumer Surplus', ' (20)'), 'A point of explanation — any two',
     H.split('Consumer surplus\nConsumer surplus is', '2 points of explanation: 4 marks',
             ['Consumer surplus', 'The concert promoter can extract consumer surplus by offering something extra', 'Example']),
     2, 4, 'Two points of explanation, 4 marks each.', stem=q1c, **B)

# Q2 ─ imperfect competition; the grocery market
add('sb-q2-a-i', '2-0', 'assumptions-of-imperfect-competition', ref('B', 2, '(a)(i)'),
    H.q(5, 'State and explain three assumptions underlying the theory of imperfect competition.', ' (ii)'), '5 + 4 + 4', 13,
    [anyN('r-1', 'An assumption — any three', 13, 3, 5,
          H.split('There are many buyers\nAn individual', '3 Assumptions: 5 marks',
                  ['There are many buyers', 'There are many sellers in the industry', 'Product differentiation exists',
                   'Freedom of entry and exit', 'Reasonable knowledge', 'Each firm attempts to maximise profits']),
          'Three assumptions: the 1st correct answer 5 marks, the 2nd and 3rd 4 each.', steps=[5, 4, 4])],
    kind='fixed', **B)
add('sb-q2-a-ii', '2-0', 'demand-curves-of-the-two-firms', ref('B', 2, '(a)(ii)'),
    H.q(5, 'Explain why a firm’s demand curve under imperfect competition differs', ' (25)'), '6 + 6', 12,
    [point('r-perfect', defined('Perfect competition', 'The demand curve facing a perfectly competitive firm', '\n6 marks'), 6,
           'The perfectly competitive firm’s demand curve, 6 marks.'),
     point('r-imperfect', defined('Imperfect competition', 'The demand curve facing a firm in imperfect competition', '\n6 marks'), 6,
           'The imperfectly competitive firm’s demand curve, 6 marks.')], **B)
q2b_i = H.q(5, 'Explain, with the aid of a diagram, the long run equilibrium', ' (ii)')
add('sb-q2-b-i', '2-0', 'long-run-equilibrium-in-imperfect-competition', ref('B', 2, '(b)(i)'), q2b_i, '10 + 8', 18,
    [ask_row('r-diagram', q2b_i[:q2b_i.index(', the long run')], 10,
             'The diagram, 10 marks: MC cutting MR at X, the price P2 and output Q2 read off the AR curve at C, where AC is '
             'tangent to AR above its lowest point W, as the figure shows.'),
     point('r-explanation', joined('Equilibrium / profit maximisation occurs (at point X)', 'Correct Diagram: 10 marks'), 8,
           'The explanation of the long-run equilibrium, 8 marks.')],
    kind='fixed', figure=SOL + 'p14-q2bi-diagram', **B)
pick('sb-q2-b-ii', '2-0', 'why-imperfect-competition-is-inefficient', ref('B', 2, '(b)(ii)'),
     H.q(5, 'With reference to your diagram in (b) (i) explain why the firm', ' (30)'), 'A point of information — any three',
     H.split('An imperfectly competitive firm does not produce', '3 points of information: 4 marks',
             ['An imperfectly competitive firm does not produce', 'They are not producing at the lowest point',
              'Price exceeds the marginal cost', 'Because it is not producing at the lowest point']),
     3, 4, 'Three points of information, 4 marks each: the scheme’s one possible response, read by its sentences.', **B)
add('sb-q2-c', '2-0', 'the-irish-grocery-market', ref('B', 2, '(c)'),
    H.q(5, 'Suggest a market structure which most closely reflects this situation.', ' (20)'), '1 + 5 + 5 + 5 + 4', 20,
    [point('r-structure', H.traced('Oligopoly'), 1, H.traced('Choice of market structure: 1 mark') + '.'),
     anyN('r-explanation', 'An explanation — any four', 19, 4, 5,
          H.split('The Irish grocery market is dominated by a few large sellers', 'Choice of market structure',
                  ['The Irish grocery market is dominated by a few large sellers', 'Barriers to entry exist',
                   'Mutual interdependence between the large retailers',
                   'The products sold are close substitutes / product differentiation', 'Non price competition']),
          'Four explanations: the 1st, 2nd and 3rd correct responses 5 marks each, the 4th 4. '
          + H.traced('Reference must be made to the Irish grocery market') + '.', steps=[5, 5, 5, 4])],
    kind='fixed', stem=H.q(5, '“A few large retailers', ' Suggest'), **B)

# Q3 ─ elasticity
ped = H.split('Elastic demand\nThe percentage', 'Each definition: 5 marks',
              ['Elastic demand', 'Inelastic Demand', 'Unitary Elastic Demand'])
add('sb-q3-a-i', '1-4', 'categories-of-ped', ref('B', 3, '(a)(i)'),
    H.q(6, 'Define the categories of Price Elasticity of Demand (PED)', ' (ii)'), '3 x 5', 15,
    [point(f'r-{h.split()[0].lower()}', f'{H.traced(h)} — {H.traced(o[len(h):].strip())}', 5, f'{h}, 5 marks.')
     for h, o in zip(('Elastic demand', 'Inelastic Demand', 'Unitary Elastic Demand'), ped)], **B)
pick('sb-q3-a-ii', '1-4', 'what-shapes-ped', ref('B', 3, '(a)(ii)'),
     H.q(6, 'State three factors that affect PED and explain how each factor affects it.', ' (30)'), 'A factor — any three',
     H.split('The amount and availability of close substitutes', '3 factors: 5 marks',
             ['The amount and availability of close substitutes', 'The proportion of income which is spent on the good',
              'The length of time allowed for adjustment to price changes', 'The durability of the good',
              'Number of alternative uses the good has']),
     3, 5, 'Three factors, 5 marks each.', **B)
add('sb-q3-b', '1-4', 'the-ped-of-petrol', ref('B', 3, '(b)'),
    H.q(6, 'A consumer/motorist buys 20 litres of petrol', ' (20)'), '10 + 2 + 8', 20,
    [point('r-ped', 'PED — ' + H.traced('- 0.846 (- 0.85)'), 10,
           'The PED, 10 marks. The figure shows the working as printed: −1 over 10c times €1.60 + €1.70 (€3.30) over 20 + 19 (39).'),
     point('r-inelastic', H.traced('Demand for petrol is inelastic.'), 2, 'Inelastic, 2 marks.'),
     point('r-implication', H.opt('An increase in the price of petrol will yield an increase', '\n8 marks'), 8,
           'The implication for government revenue, 8 marks.')],
    figure=SOL + 'p17-q3b-working', **B)
q3c = H.q(6, 'A firm is considering a change to its product', ' (i)')
add('sb-q3-c-i', '1-4', 'ped-and-total-revenue', ref('B', 3, '(c)(i)'),
    H.q(6, 'If the firm wishes to maximise total sales revenue', ' The market research'), '12', 12,
    [point('r-1', H.opt('This good is a price elastic good because its absolute value', '\n12 marks'), 12,
           'The answer with its reason, 12 marks: reduce the price.')], stem=q3c, **B)
add('sb-q3-c-ii', '1-4', 'yed-in-a-recession', ref('B', 3, '(c)(ii)'),
    H.q(6, 'In the case of an economy which is expected to remain in recession', ' (25)'), '13', 13,
    [point('r-1', H.opt('This good could be considered by consumers to be a luxury good', '\n13 marks'), 13,
           'The likely impact with its reason, 13 marks. ' + H.traced('Other acceptable answers marked on their merits') + '.')],
    stem=f"{H.q(6, 'A firm is considering a change to its product', ' Use this information')} "
         f"{H.q(6, 'The market research also reveals Income Elasticity', ' (ii)')}", **B)

# Q4 ─ factor incomes; land and location; property and mortgage arrears
terms = (('Derived demand', 'Is where a factor of production is demanded', '\nAn example of derived'),
         ('Transfer Earnings', 'Can be defined as the earnings of a factor', '\nAppropriate example.'),
         ('Supply Price', 'Is the minimum payment necessary to bring a factor', '\nAppropriate example.'),
         ('Economic Rent', 'This is any payment to a factor of production above', '\nAppropriate example.'))
add('sb-q4-a', '2-1', 'factor-incomes-and-derived-demand', ref('B', 4, '(a)'),
    H.q(6, 'Explain, with the aid of an example, each of the following terms:', ' (20)'), '4 x (3 + 2)', 20,
    [point(f"r-{t.split()[0].lower()}", defined(t, s, e), 3, f'{t} explained, 3 marks.') for t, s, e in terms]
    + [anyN('r-examples', 'An example of each term', 8, 4, 2,
            [defined('Derived demand', 'An example of derived demand is the demand for land', '\nTransfer Earnings')]
            + [f"{H.traced(t)} — {H.traced('Appropriate example.')}" for t, _, _ in terms[1:]],
            H.traced('Explanation: 3 marks each/example: 2 marks each = 20 marks') + '. The scheme prints an example for '
            'derived demand and asks for an appropriate example of each of the others.')],
    kind='fixed', **B)
pick('sb-q4-b-i', '0-1', 'characteristics-of-land', ref('B', 4, '(b)(i)'),
     H.q(6, 'Outline two economic characteristics of ‘land’.', ' (ii)'), 'A characteristic — any two',
     H.split('Land is fixed in supply\nAn increase', '2 characteristics: 5 marks',
             ['Land is fixed in supply', 'Land has no cost of production to society as a whole', 'Land is a non-specific factor']),
     2, 5, 'Two characteristics, 5 marks each.', **B)
pick('sb-q4-b-ii', '1-2', 'where-a-firm-locates', ref('B', 4, '(b)(ii)'),
     H.q(6, 'Discuss three economic factors which influence a firm’s decision', ' (25)'), 'A factor — any three',
     H.split('Closeness to similar firms', '3 factors: 5 marks',
             ['Closeness to similar firms', 'Availability of a skilled workforce', 'Proximity to market / raw materials',
              'Well developed infrastructure', 'Government Incentives', 'Commercial Property Prices', 'Social Infrastructure',
              'Planning Laws']),
     3, 5, 'Three factors, 5 marks each.', **B)
pick('sb-q4-c-i', '1-0', 'why-house-prices-fell', ref('B', 4, '(c)(i)'),
     H.q(6, 'State and explain three factors that caused the price of residential property', ' (ii)'), 'A factor — any three',
     H.split('Property market collapse', '3 factors: 5 marks',
             ['Property market collapse', 'The Banking Crisis', 'Economic recession / Weaker demand in housing market',
              'Emigration', 'Speculation in housing']),
     3, 5, 'Three factors, 5 marks each.', **B)
groups = (('households', 'Households', ['Lack of consumer confidence', 'Reduced creditworthiness',
                                        'Less houses for sale / depressed property market', 'Social housing requirement'],
           'The banking sector\nDebt'),
          ('banks', 'The banking sector', ['Debt write-down deals', 'Subject to more regulation and legislation',
                                           'Unemployment in the Banking Sector', 'Collapse in share prices of bank stocks'],
           'Irish Government\nReduced'),
          ('government', 'Irish Government', ['Reduced Tax Revenue for Government', 'More debt write-offs / Guarantor for the Irish banks',
                                              'Increased demand for Social and Affordable Housing',
                                              'New measures introduced by government to deal with banking/housing crisis'],
           'One possible economic impact per category'))
add('sb-q4-c-ii', '3-4', 'the-impact-of-mortgage-arrears', ref('B', 4, '(c)(ii)'),
    H.q(6, 'Discuss one possible economic impact of mortgage arrears on each of following:', ' (30)'), '3 x 5', 15,
    [heading(f'r-{rid}', H.traced(label) + ' — any one', H.split(firsts[0], end, firsts), 5,
             f'One impact on {label[0].lower() + label[1:] if label != "Irish Government" else "the Irish Government"}, 5 marks.')
     for rid, label, firsts, end in groups],
    kind='fixed', stem=H.q(6, 'Mortgage arrears (i.e. the inability', ' Discuss one'), **B)

# Q5 ─ national income; multinationals; GDP and GNP
q5a = ' '.join([H.q(7, 'The following table shows the level of National Income (Y)', ' Y C I'),
                H.q(7, 'Use this data to calculate the following:', ' (i)')])
q5a_table = PAP + 'p07-q5a-table'
for part, concept, ask, nxt, answer, label, note in (
        ('i', 'consumption-from-the-identity', 'The level of Consumption in 2013', ' (ii)', 'C = 50,000', '', 'Consumption in 2013'),
        ('ii', 'the-mpc', 'The Marginal Propensity to Consume (MPC)', ' (iii)', '0.6 (60%)', 'MPC — ', 'The MPC'),
        ('iii', 'imports-from-the-identity', 'The level of Imports in 2014', ' (iv)', 'M = 125,000', '', 'Imports in 2014'),
        ('iv', 'the-mpm', 'The Marginal Propensity to Import (MPM).', ' (20)', '0.5 (50%)', 'MPM — ', 'The MPM')):
    add(f'sb-q5-a-{part}', '3-0', concept, ref('B', 5, f'(a)({part})'), H.q(7, ask, nxt), '5', 5,
        [point('r-1', label + H.traced(answer), 5, f'{note}, 5 marks. The figure shows the working as printed.')],
        stem=q5a, figure=SOL + f'p23-q5a{part}-working', **B)
    beside_ask(cards[-1], q5a_table)
pick('sb-q5-b', '4-1', 'what-multinationals-bring', ref('B', 5, '(b)'),
     H.q(7, 'Discuss the economic benefits Multinational Companies (MNCs) can bring', ' (20)'), 'A benefit — any four',
     H.split('Employment / improved standard of living / economic growth', '4 points of information: 5 marks',
             ['Employment / improved standard of living / economic growth', 'Balance of Payments Benefits',
              'Investment in Research & Development and Education', 'Increased Government Revenue for the economy',
              'Increased demand for Commercial Property', 'Promotes regional development', 'New technology introduced',
              'Benefits to indigenous companies', 'Improved reputation for future FDI', 'Indigenous MNCs encourage more FDI',
              'Development of a "silicon valley"']),
     4, 5, 'Four points of information, 5 marks each.', stem=H.q(7, '“Ireland heads Forbes’ list', ' Discuss the'), **B)
q5c = H.q(7, 'Economists use Gross Domestic Product (GDP)', ' (i)')
add('sb-q5-c-i', '3-0', 'gdp-and-gnp', ref('B', 5, '(c)(i)'), H.q(7, 'Define each of the underlined terms.', ' (ii)'), '6 + 6', 12,
    [point('r-gdp', H.opt('Gross Domestic Product can be defined as the total output', '\n6 marks'), 6, 'GDP, 6 marks.'),
     point('r-gnp', H.opt('Gross National Product is defined as the total output', '\n6 marks'), 6, 'GNP, 6 marks.')],
    stem=q5c, **B)
add('sb-q5-c-ii', '3-0', 'gnp-or-gdp-for-ireland', ref('B', 5, '(c)(ii)'),
    H.q(7, 'Which of these terms do you consider to be a more useful measure', ' (iii)'), '8', 8,
    [point('r-1', xb('Although GDP is used for comparison with other EU countries', '\n8 marks')[0], 8,
           'The choice with its explanation, 8 marks. The scheme prints one possible response, shown in full in the '
           'figure; this is its conclusion.')],
    stem=q5c, figure=SOL + 'p25-q5cii-response', **B)
pick('sb-q5-c-iii', '3-0', 'limits-of-national-income-statistics', ref('B', 5, '(c)(iii)'),
     H.q(7, 'Discuss three limitations of national income statistics.', ' (35)'), 'A limitation — any three',
     H.split('Population distortions', '3 points of information: 5 marks',
             ['Population distortions', 'Constant prices and current prices / Inflation',
              'Hidden social costs attached to increases in national income', 'Distribution of national income and poverty',
              'Shadow economy transactions not measured', 'Nature of the goods produced']),
     3, 5, 'Three points of information, 5 marks each.', stem=q5c, **B)

# Q6 ─ economic aims; privatisation; austerity
pick('sb-q6-a-i', '3-1', 'the-governments-economic-aims', ref('B', 6, '(a)(i)'),
     H.q(7, 'State and explain four current economic aims/objectives', ' (ii)'), 'An aim — any four',
     H.split('To reduce unemployment\nUnemployment', '4 points of information: 5 marks',
             ['To reduce unemployment', 'To reduce the national debt/sustainable public finances', 'Achievement of economic growth',
              'Boost exports / improve competitiveness / attracting investment', 'Broaden the tax base / greater tax revenue certainty',
              'Sustainable economic development', 'Balanced regional development']),
     4, 5, 'Four points of information, 5 marks each.', **B)
pick('sb-q6-a-ii', '3-1', 'conflicting-aims', ref('B', 6, '(a)(ii)'),
     H.q(7, 'Outline two possible conflicts that could arise', ' (30)'), 'A conflict — any two',
     H.split('Sustainable government finances vs. economic growth', 'Economic Growth vs. just social policy',
             ['Sustainable government finances vs. economic growth', 'Sustainable government finances vs. regional development',
              'Full employment vs. equality'])
     + [H.traced('Economic Growth vs. just social policy')],
     2, 5, 'Two conflicts, 5 marks each. ' + H.traced('Other acceptable answers marked on their merits.'), **B)
add('sb-q6-b', '1-3', 'privatising-state-assets', ref('B', 6, '(b)'),
    H.q(7, 'Discuss arguments for and against the privatisation of state assets.', ' (20)'), '2 x 5 + 2 x 5', 20,
    [anyN('r-for', 'An argument for — any two', 10, 2, 5,
          H.split('Revenue for government\nThe government', '2 arguments for',
                  ['Revenue for government', 'More competition', 'Enterprise culture', 'Access to finance',
                   'Greater incentives for innovation', 'Shedding of loss making companies']),
          H.traced('2 arguments for: 5 marks each') + '.'),
     anyN('r-against', 'An argument against — any two', 10, 2, 5,
          H.split('Increased Prices/ falling standards of service', '2 arguments against',
                  ['Increased Prices/ falling standards of service', 'Loss of jobs and reduced job security',
                   'Loss of a State Resource / loss of annual profits', 'Foreign Ownership', 'Loss of essential public services']),
          H.traced('2 arguments against: 5 marks each') + '.')],
    kind='fixed', **B)
add('sb-q6-c', '3-1', 'consequences-of-austerity', ref('B', 6, '(c)'),
    H.q(7, 'Outline four possible economic consequences for the Irish economy', ' (25)'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'A consequence — any four', 25, 4, 7,
          H.split('Increased unemployment / emigration', '1st correct response: 7',
                  ['Increased unemployment / emigration', 'Loss of business confidence / lack of investment',
                   'Reduction in aggregate demand / spending / lack of economic growth',
                   'Fall in living standards / increased Taxation', 'Increased indebtedness', 'Role of the government increases',
                   'More regional inequality']),
          'Four consequences: the 1st correct response 7 marks, the 2nd, 3rd and 4th 6 each.', steps=[7, 6, 6, 6])],
    kind='fixed', stem=H.q(7, 'In The Irish Times (November 2013)', ' Outline four'), **B)

# Q7 ─ development; foreign aid; free trade
add('sb-q7-a-i', '4-0', 'development-against-growth', ref('B', 7, '(a)(i)'),
    H.q(8, 'Distinguish between the terms ‘economic development’ and ‘economic growth’', ' (ii)'), '5 + 5', 10,
    [point('r-development', defined('Economic Development', 'Occurs where an increase in the level of income', '\n5 marks'), 5,
           'Economic development, 5 marks.'),
     point('r-growth', defined('Economic Growth', 'It can be defined as an increase in GNP per head', '\n5 marks'), 5,
           'Economic growth, 5 marks.')], **B)
pick('sb-q7-a-ii', '4-0', 'characteristics-of-ldcs', ref('B', 7, '(a)(ii)'),
     H.q(8, 'Outline three characteristics of LDCs.', ' (25)'), 'A characteristic — any three',
     H.split('High population growth rates in LDCs', '3 points of information: 5 marks',
             ['High population growth rates in LDCs', 'Famine in LDCs / low life expectancy', 'High foreign debts / lack of capital',
              'High percentage of the population engaged', 'Poor infrastructure in LDCs', 'Poor levels of education / literacy in LDCs',
              'Exploitation by multinationals', 'Political corruption / less stable political institutions']),
     3, 5, 'Three points of information, 5 marks each. ' + H.traced('Other acceptable answers marked on their merits') + '.', **B)
pick('sb-q7-b-i', '4-0', 'types-of-foreign-aid', ref('B', 7, '(b)(i)'),
     H.q(8, 'Describe three types of foreign aid available to LDCs.', ' (ii)'), 'A type of aid — any three',
     H.split('Direct financial aid by governments\nThis', '3 points of information: 5 marks',
             ['Direct financial aid by governments', 'Financial aid through voluntary agencies',
              'Aid (other than financial aid) by foreign citizens', 'Restructuring of national debts',
              'Multinationals setting up in LDCs', 'Improve trade terms with LDCs', 'Assist LDCs with skills and technologies']),
     3, 5, 'Three points of information, 5 marks each.', **B)
pick('sb-q7-b-ii', '4-0', 'when-aid-fails', ref('B', 7, '(b)(ii)'),
     H.q(8, 'Discuss why foreign aid may not always result in economic growth in LDCs.', ' (25)'), 'A reason — any two',
     H.split('Unfair distribution of benefits / Widening poverty gap', '2 points of information: 5 marks',
             ['Unfair distribution of benefits / Widening poverty gap', 'Costs to the environment',
              'Rapid population growth / standard of living', 'Culture of dependency rather than improvement of local economy',
              'Food aid dependency/ reduced incentive for production', 'High profile projects']),
     2, 5, 'Two points of information, 5 marks each.', **B)
q7c = H.q(8, '“The World Trade Organisation (WTO)', ' (i)')
pick('sb-q7-c-i', '4-2', 'benefits-of-free-trade', ref('B', 7, '(c)(i)'),
     H.q(8, 'Outline two economic benefits claimed for ‘free trade’.', ' (ii)'), 'A benefit — any two',
     H.split('Greater choice of commodities / higher standard of living', '2 economic benefits: 5 marks',
             ['Greater choice of commodities / higher standard of living', 'More competitive prices of goods and services',
              'Strengthens home economy / boosts employment / investment opportunities',
              'Companies benefit from economies of large scale production']),
     2, 5, 'Two benefits, 5 marks each.', stem=q7c, **B)
pick('sb-q7-c-ii', '4-2', 'why-countries-protect', ref('B', 7, '(c)(ii)'),
     H.q(8, 'Outline three reasons why countries might choose to impose barriers', ' (25)'), 'A reason — any three',
     H.split('Protect infant industry', '3 reasons: 5 marks',
             ['Protect infant industry', 'Prevent dumping', 'Protect employment on the domestic / home market',
              'Encourage the domestic production of vital goods / national security']),
     3, 5, 'Three reasons, 5 marks each. ' + H.traced('Other acceptable answers marked on their merits') + '.', stem=q7c, **B)

# Q8 ─ the deficit and the debt; taxation
add('sb-q8-a', '3-1', 'the-deficit-and-the-debt', ref('B', 8, '(a)'),
    H.q(8, 'Explain the relationship between a government Budget Deficit and the National Debt.', ' (20)'), '10 + 10', 20,
    [point('r-deficit', H.opt('A government budget deficit exists when total government expenditure', '\n10 marks'), 10,
           'The budget deficit, 10 marks.'),
     point('r-debt', H.opt('National debt is the total amount (cumulative)', '\n10 marks'), 10,
           'The national debt and the relationship, 10 marks.')], **B)
q8b = H.q(8, '“The Irish Tax system has evolved over time', ' (i)')
canons = H.split('Equity\nThe ability', '4 points of information: 6 marks', ['Equity', 'Economy', 'Certainty', 'Convenience'])
add('sb-q8-b-i', '3-1', 'the-canons-of-taxation', ref('B', 8, '(b)(i)'),
    H.q(8, 'Discuss Adam Smiths\' four Canons of Taxation', ' (ii)'), '4 x 6', 24,
    [point(f'r-{h.lower()}', f'{H.traced(h)} — {H.traced(o[len(h):].strip())}', 6, f'{h}, 6 marks.')
     for h, o in zip(('Equity', 'Economy', 'Certainty', 'Convenience'), canons)],
    stem=q8b, **B)
add('sb-q8-b-ii', '3-1', 'principles-of-a-modern-tax-system', ref('B', 8, '(b)(ii)'),
    H.q(8, 'Outline two other principles which could be considered in a modern tax system.', ' (35)'), '6 + 5', 11,
    [anyN('r-1', 'A principle, justified — any two', 11, 2, 6,
          H.split('A tax system should have a limited disincentive effect on work', 'Tax evasion should not be possible',
                  ['A tax system should have a limited disincentive effect on work', 'A tax system should have a limited disincentive effect on investing',
                   'Taxes should have a stabilising impact on the economy', 'Tax rates should be consistent with national economic objectives'])
          + [H.traced('Tax evasion should not be possible')],
          'Two principles: the 1st correct response 6 marks, the 2nd 5. ' + H.traced('Other acceptable answers marked on their merits') + '.',
          steps=[6, 5])],
    kind='fixed', stem=q8b, **B)
pick('sb-q8-c', '3-1', 'from-direct-to-indirect-tax', ref('B', 8, '(c)'),
     H.q(8, 'Outline possible economic consequences of the Irish Government shifting', ' (20)'), 'A consequence — any four',
     H.split('Encourages enterprise, investment, employment', '4 points of information: 5 marks',
             ['Encourages enterprise, investment, employment', 'Moving from direct to indirect can make the tax system more regressive',
              'Evasion is more difficult with indirect tax', 'Revenue collected is not as certain with indirect tax',
              'Indirect taxes can be inflationary', 'May lead to a growth in the ‘shadow economy’']),
     4, 5, 'Four points of information, 5 marks each.', **B)

if __name__ == '__main__':
    emit(cards)
