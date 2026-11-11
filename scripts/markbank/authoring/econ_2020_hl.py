#!/usr/bin/env python3
"""Economics 2020 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2020-hl-ev.json, made
from a visual sweep of all 12 paper pages and 44 scheme pages before any 2020
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The only prose written here is guidance: tariffs, route
labels and what a figure or a calculation shows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import show_before_reveal  # noqa: E402
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2020, 'higher', 'LC034ALP000EV')
D = OldDeck(2020, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2020-HL-scheme-'
PAP = 'economics-2020-HL-paper-'
bl = H.bullets


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def side(label, options):
    """Options listed under one of the scheme's own side headings ("For", "Against"),
    each named by it: "<heading> — <response>". Both halves trace."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ substitution and income effects
add('sa-q1', '1-1', 'substitution-and-income-effects', ref('A', 1),
    H.q(2, 'A fall in the price of a consumer product', ' Substitution effect'), '1st @ 10, 2nd @ 6', 16,
    [anyN('r-1', 'Each effect explained', 16, 2, 10,
          H.split('Substitution effect: consumers will demand more', '2. Citizens in some',
                  ['Substitution effect', 'Income effect']),
          'Both effects: the first correct explanation 10 marks, the second 6.', steps=[10, 6])],
    kind='fixed', **A)

# Q2 ─ economic development and its social costs
add('sa-q2', '4-0', 'economic-development-and-social-costs', ref('A', 2),
    H.q(2, 'Citizens in some Less Developed Countries', ' Explanation'), '1 @ 8 and 2 @ 4', 16,
    [point('r-development', H.opt('Economic development refers to', 'Possible social costs'), 8,
           'The explanation of economic development, 8 marks.'),
     anyN('r-costs', 'A social cost — any two', 8, 2, 4,
          H.split('Damage to environment:', '4 | P a g e',
                  ['Damage to environment', 'Population movement', 'Loss of traditional cultural values',
                   'Quality of life issues']),
          'Two social costs, 4 marks each.')], **A)

# Q3 ─ unemployment from automation
q3 = H.q(3, 'Up to 800 million global workers', ' (Source')
add('sa-q3-a', '3-2', 'structural-unemployment-from-automation', ref('A', 3, '(a)'),
    H.q(3, 'Name the type of unemployment these workers will experience.', ' Type of'), '4 + 4', 8,
    [point('r-type', H.traced(H.chunk('Structural / Technological Unemployment', ' ⟨')), 4, 'The type, 4 marks.'),
     point('r-explanation', H.opt('Is a form of unemployment caused by a mismatch', 'Technological unemployment may'), 4,
           'The explanation, 4 marks. The scheme also accepts its explanation of technological unemployment.',
           accepts=[H.opt('Technological unemployment may be caused', '(b) Outline one policy')])],
    stem=q3, **A)
pick('sa-q3-b', '3-2', 'policy-for-structural-unemployment', ref('A', 3, '(b)'),
     H.q(3, 'Outline one policy response that the Irish government could take', ' Government policy'),
     'A government policy — any one',
     bl('• The government must provide retraining', '4. (i) Complete the diagram'),
     1, 8, 'One policy, 8 marks (4 + 4).', stem=q3, **A)

# Q4 ─ a shift in the beef market's equilibrium
q4 = H.q(3, 'The following diagram represents a change in equilibrium', ' Price')
q4i = H.q(3, 'Complete the above diagram by labelling', ' (ii)')
add('sa-q4-i', '1-0', 'labelling-a-shift-in-equilibrium', ref('A', 4, '(i)'), q4i, '8', 8,
    [ask_row('r-1', q4i, 8, 'The four labels on the completed diagram, 8 marks. The scheme prices them as one 8; '
             'its completed diagram is shown with the answer.')],
    stem=q4, figure=SOL + 'p06-q4i-diagram', **A)
beside_ask(cards[-1], PAP + 'p03-q4-diagram')
add('sa-q4-ii', '1-0', 'what-shifts-supply-to-the-right', ref('A', 4, '(ii)'),
    H.q(3, 'Indicate by means of a tick', ' Explanation:'), '4 + 4', 8,
    [point('r-tick', H.cell('(b) An increase in a subsidy', upto='beef farmers.'), 4, 'The tick, 4 marks.'),
     point('r-explanation', H.opt('An increase is a subsidy for beef farmers', '5 | P a g e'), 4,
           'The explanation, 4 marks.')],
    stem=q4, figure=PAP + 'p03-q4-diagram', **A)

# Q5 ─ PTSB branch closures
q5 = H.q(4, 'Permanent Trustee Savings Bank (PTSB)', ' (Source')
pick('sa-q5-a', '3-4', 'why-bank-branches-close', ref('A', 5, '(a)'),
     H.q(4, 'Outline one possible reason for the closure', ' (b)'), 'A reason for the closures — any one',
     H.split('Decrease costs\nPTSB wants', '(b) Outline two economic effects',
             ['Decrease costs', 'Increase in the use of online', 'Advances in technology',
              'Offset reduction in income to the bank']),
     1, 8, 'One reason, 8 marks.', stem=q5, **A)
pick('sa-q5-b', '3-4', 'effects-of-bank-branch-closures', ref('A', 5, '(b)'),
     H.q(4, 'Outline two economic effects of these closures', ' (i)'), 'An economic effect — any two',
     H.split('Rise in unemployment in the banking sector', '6 | P a g e',
             ['Rise in unemployment in the banking sector', 'Loss of banking services to the local community',
              'Fall in demand for other goods and services']),
     2, 4, 'Two effects, 4 marks each.', stem=q5, **A)

# Q6 ─ Keynes and fiscal policy
q6 = H.q(4, 'John Maynard Keynes supported the use of fiscal policy', ' (i)')
add('sa-q6-i', '3-1', 'fiscal-policy', ref('A', 6, '(i)'),
    H.q(4, 'Define the term fiscal policy:', ' ___'), '9', 9,
    [point('r-1', H.opt('Fiscal policy refers to those actions', 'Is any change in government'), 9,
           'The definition, 9 marks. The scheme also accepts its second statement.',
           accepts=[H.opt('Is any change in government spending and taxation', '(ii) Do you agree')])],
    stem=q6, **A)
q6ii = ' '.join([H.q(4, 'Do you agree with Keynes support of government intervention', ' Yes'),
                 H.q(4, 'Yes / No. Place a circle around your choice', ' Reason 1')])
for word, mark, start, end, firsts in (
        ('yes', 'Yes.', 'Achieve sustainable economic growth:', 'No.\nAnti laissez',
         ['Achieve sustainable economic growth', 'Help create employment', 'Redistribution of wealth',
          'Provision of essential services', 'Protection of consumers']),
        ('no', 'No.', 'Anti laissez faire:', '7 | P a g e',
         ['Anti laissez faire', 'Funding by borrowing / increased taxation', 'Costly / inefficient state services',
          'Discourage private enterprise'])):
    add(f'sa-q6-ii-{word}', '3-1', 'keynes-and-government-intervention', ref('A', 6, '(ii)', word),
        f'{q6ii} Justify the choice: {word.upper()}.', '2 + 2 x 3', 8,
        [point('r-choice', H.traced(mark), 2, f'Circling {word.upper()}, 2 marks.'),
         anyN('r-reasons', f'A reason for answering {word.upper()} — any two', 6, 2, 3,
              H.split(start, end, firsts), 'Two reasons, 3 marks each. The scheme credits YES and NO, each with its own list.')],
        kind='fixed', stem=q6, **A)

# Q7 ─ regulating the gig economy: one ladder over (a) and (b)
add('sa-q7', '2-1', 'regulating-the-gig-economy', ref('A', 7),
    ' '.join([H.q(5, 'Outline two arguments in favour of increased regulation', ' (i)'),
              H.q(5, 'Outline one argument against increased regulation', ' ___')]),
    '1st x 9 & 2 x 4', 17,
    [anyN('r-1', 'Two arguments in favour and one against', 17, 3, 9,
          H.split('Protection of employee rights:', '1st x 9',
                  ['Protection of employee rights', 'Certainty to the employee’s standard of living',
                   'Quality of service', 'Prevent the growth of the shadow economy'])
          + H.split('Disincentive to work:', '8 | P a g e',
                    ['Disincentive to work', 'Cost increases', 'Reduced flexibility for employees / employers']),
          'Two arguments in favour (the first four listed) and one against (the last three). The scheme prices the '
          'three on one ladder across (a) and (b): the first credited 9 marks, the other two 4 each.', steps=[9, 4, 4])],
    kind='fixed', stem=H.q(5, 'The continuing rise of the ‘gig economy’', ' (a)'), **A)

# Q8 ─ decline in towns and rural areas: one ladder over (a) and (b)
add('sa-q8', '3-5', 'decline-of-towns-and-rural-areas', ref('A', 8),
    ' '.join([H.q(5, 'Explain two economic effects of this decline', ' (i)'),
              H.q(5, 'Outline one measure which the government could take to address', ' ___')]),
    '1st x 9 & 2 x 4', 17,
    [anyN('r-1', 'Two economic effects and one measure', 17, 3, 9,
          H.split('Regional variations in employment levels:', '(b) Outline one measure',
                  ['Regional variations in employment levels', 'Falling population in some areas',
                   'Pressure on Irish transport networks', 'Under-utilisation of local infrastructure'])
          + H.split('Business incentives to locate in certain regions', '9 | P a g e',
                    ['Business incentives to locate in certain regions', 'Improve / maintain the infrastructure',
                     'Provide grants for local communities', 'Improve / maintain local services']),
          'Two effects (the first four listed) and one measure (the last four). The scheme prices the three on one '
          'ladder across (a) and (b): the first credited 9 marks, the other two 4 each.', steps=[9, 4, 4])],
    kind='fixed', stem=H.q(5, 'Some citizens are concerned with the decline', ' (a)'), **A)

# Q9 ─ the kinked demand curve of an oligopoly
q9 = H.q(6, 'The diagram below represents the long', ' (i)')
q9_fig = PAP + 'p06-q9-diagram'
add('sa-q9-i', '2-0', 'labelling-an-oligopoly-diagram', ref('A', 9, '(i)'),
    ' '.join([H.q(6, 'Write in full the label (not abbreviation)', ' Price'),
              H.q(6, 'Use the answer box provided.', ' 1')]),
    '3 x 3', 9,
    [point(f'r-{n}', f'{n} — ' + H.cell(label, whole=True), 3, f'Line {n}, 3 marks.')
     for n, label in ((1, 'Marginal Cost'), (2, 'Demand/ Average Revenue'), (3, 'Marginal Revenue'))],
    stem=q9, figure=q9_fig, **A)
add('sa-q9-ii', '2-0', 'equilibrium-of-an-oligopoly', ref('A', 9, '(ii)'),
    H.q(6, 'Show on the diagram the equilibrium point (E)', ' (iii)'), 'P1 = 1, Q1 = 1, E = 1', 3,
    [point(f'r-{x.lower()}', H.traced(f'{x} = 1').split(' = ')[0], 1, f'{x}, 1 mark.') for x in ('P1', 'Q1', 'E')],
    stem=q9, figure=SOL + 'p11-q9-diagram', **A)
beside_ask(cards[-1], q9_fig)
add('sa-q9-iii', '2-0', 'price-rigidity', ref('A', 9, '(iii)'),
    H.q(6, 'With reference to the diagram explain the term price rigidity.', ' ___'), '5', 5,
    [point('r-1', H.opt('Price rigidity, in the diagram above', '10 | P a g e'), 5, 'The explanation, 5 marks.')],
    stem=q9, figure=q9_fig, **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ utility; the alcohol advertising ban; rail
q1a = ' '.join([H.q(7, 'The table below illustrates the Law of Diminishing Marginal Utility.', ' No.'),
                ])
q1a_fig = PAP + 'p07-q1a-table'
add('sb-q1-a-i', '1-1', 'law-of-diminishing-marginal-utility', ref('B', 1, '(a)(i)'),
    H.q(7, 'Explain the Law of Diminishing Marginal Utility.', ' (ii)'), '9', 9,
    [point('r-1', H.opt('The law of diminishing marginal ⟨9⟩', '(ii) Calculate the marginal utility'), 9,
           'The explanation, 9 marks.')], stem=q1a, **B)
add('sb-q1-a-ii', '1-1', 'calculating-marginal-utility', ref('B', 1, '(a)(ii)'),
    H.q(7, 'Using the table above calculate the marginal utility', ' (iii)'), '4', 4,
    [point('r-1', H.traced('25 - 10 = 15, 37 – 25 = 12, 47 – 37 = 10, 54 – 47 = 7'), 4,
           'The four marginal utilities, A 15, B 12, C 10 and D 7, 4 marks: the scheme’s workings.')],
    stem=q1a, figure=q1a_fig, **B)
add('sb-q1-a-iii', '1-1', 'where-diminishing-marginal-utility-sets-in', ref('B', 1, '(a)(iii)'),
    H.q(7, 'State at what point diminishing marginal utility sets in', ' (iv)'), '4', 4,
    [point('r-1', H.opt('The law of diminishing marginal utility sets in after', '(iv) State and explain two'), 4,
           'The point and its explanation, 4 marks.')],
    stem=q1a, figure=q1a_fig, **B)
pick('sb-q1-a-iv', '1-1', 'assumptions-of-diminishing-marginal-utility', ref('B', 1, '(a)(iv)'),
     H.q(7, 'State and explain two assumptions underlying this law.', ' [25]'), 'An assumption — any two',
     H.split('Consumer’s income / taste doesn’t change', '11 | P a g e',
             ['Consumer’s income / taste doesn’t change', 'A certain minimum quantity',
              'No time has elapsed between the consumption']),
     2, 4, 'Two assumptions, 4 marks each.', stem=q1a, **B)
q1b = H.q(7, 'The Public Health (Alcohol) Act 2018', ' (Source')
add('sb-q1-b-i', '1-0', 'advertising-ban-and-the-alcohol-market', ref('B', 1, '(b)(i)'),
    H.q(7, 'Explain, with the aid of a labelled diagram, the likely impact', ' (ii)'), '5 + 5', 10,
    [point('r-diagram', H.opt('D1, D2, S1, Indication of lower equilibrium price', 'As there are now less'), 5,
           'The diagram, 5 marks: 1 for each element the scheme names. The completed diagram is in the figure.'),
     point('r-explanation', H.opt('As there are now less eligible places', '(ii) Discuss three other'), 5,
           'The explanation, 5 marks.')],
    stem=q1b, figure=SOL + 'p13-q1bi-diagram', **B)
# The split's tail trim takes a closing "21." for the next item's numeral, so the
# age-restriction measure is sliced on its own.
q1b_measures = H.split('Taxes: increase taxes such as excise', '12 | P a g e',
             ['Taxes:', 'Regulate availability', 'Introduce limits to the amount of alcohol', 'Age restrictions',
              'Sale points', 'Consumer awareness', 'Increase minimum pricing', 'Introduce harsher penalties',
              'Ban drinks industry sponsorship'])
q1b_measures[3] = H.opt('Age restrictions: raise the legal age', 'Sale points:')
pick('sb-q1-b-ii', '1-3', 'reducing-alcohol-consumption', ref('B', 1, '(b)(ii)'),
     H.q(7, 'Discuss three other possible measures which could be introduced', ' [25]'), 'A measure — any three',
     q1b_measures, 3, 5, 'Three measures, 5 marks each.', stem=q1b, **B)
q1c = H.q(7, 'Iarnród Éireann (Irish Rail) has warned', ' (Source')
pick('sb-q1-c-i', '1-1', 'rising-demand-for-rail', ref('B', 1, '(c)(i)'),
     H.q(7, 'State and explain one reason why the demand for train services', ' (ii)'), 'A reason — any one',
     H.split('Recovery in the Irish economy / increases in employment', '(i) Discuss the case for',
             ['Recovery in the Irish economy', 'Housing crisis', 'Lack of regional development',
              'Changes in population', 'More consumers availing of the Taxsaver']),
     1, 7, 'One reason, 7 marks.', stem=q1c, **B)
pick('sb-q1-c-ii', '3-5', 'investing-in-the-railways', ref('B', 1, '(c)(ii)'),
     H.q(7, 'Discuss the case for and against increased investment', ' [25]'), 'A point for or against — any three',
     side('For', H.split('Facilitates geographic mobility:', '13 | P a g e',
                         ['Facilitates geographic mobility', 'Balanced regional development', 'Less road traffic congestion',
                          'Relatively environmentally friendly', 'Improved infrastructure', 'Social benefit',
                          'Cost effective for the state']))
     + side('Against', H.split('Very capital intensive:', '14 | P a g e',
                               ['Very capital intensive', 'It is very long-term investment', 'Opportunity cost',
                                'Cost to the taxpayer', 'Unfair to those not serviced'])),
     3, 6, 'Three points across the case for and the case against, 6 marks each. The scheme prices the three '
     'together, 3 x 6, without a split between the sides.', stem=q1c, **B)

# Q2 ─ imperfect competition; non-price competition
q2 = H.q(8, 'Bord Bia has reported that the number of microbreweries', ' (Source')
pick('sb-q2-a-i', '2-0', 'why-microbrewing-is-imperfectly-competitive', ref('B', 2, '(a)(i)'),
     H.q(8, 'Explain one reason why the above industry is imperfectly competitive.', ' (ii)'), 'A reason — any one',
     bl('• There are many small firms who operate independently and can influence', '(ii) State and explain three other'),
     1, 5, 'One reason, 5 marks.', stem=q2, **B)
pick('sb-q2-a-ii', '2-0', 'characteristics-of-imperfect-competition', ref('B', 2, '(a)(ii)'),
     H.q(8, 'State and explain three other key characteristics', ' [20]'), 'A characteristic — any three',
     bl('• There are many small firms who operate independently and can change', '15 | P a g e'),
     3, 5, 'Three characteristics other than your answer to (i), 5 marks each.', stem=q2, **B)
cells = H.chunk('D=AR MR MC AC Equilibrium P1 C1 Q1 accurately', ' ⟨').split()
elements = [*cells[:4], H.cell('Correct Equilibrium point - E'), *cells[5:8], H.cell('SNP accurately shown')]
explanation = [H.opt(a, b) for a, b in (
    ('Occurs at point E where', '• MC = MR'), ('MC = MR [and MC is rising].', '2. Price / Output'),
    ('The firm produces Q1.', '• and sells'), ('and sells it at P1.', '3. Cost'),
    ('The cost is shown at C1 (point Y).', '4. SNP'), ('The firm is earning SNP (P1,C1,Y,X)', '• because'),
    ('because AR > AC .', '5. Inefficiency'), ('The firm is not producing at the lowest point', '• It is thus'),
    ('It is thus inefficient/wasteful of resources.', '16 | P a g e'))]
add('sb-q2-b-i', '2-0', 'short-run-equilibrium-in-imperfect-competition', ref('B', 2, '(b)(i)'),
    H.q(8, 'Explain, with the aid of a labelled diagram, the equilibrium position', ' (ii)'),
    'Diagram 9 + explanation 9', 18,
    [anyN('r-diagram', 'The diagram — each correctly labelled element', 9, 9, 1, elements,
          'The diagram, 9 marks: 1 for each of the nine elements in the scheme’s table. The completed diagram is in '
          'the figure.'),
     anyN('r-explanation', 'The explanation — each point', 9, 9, 1, explanation,
          'The explanation, 9 marks: 1 for each of the nine points, under equilibrium, price and output, cost, '
          'supernormal profit and inefficiency.')],
    kind='fixed', stem=q2, figure=SOL + 'p17-q2bi-diagram', **B)
q2bii = H.q(8, 'With the aid of a labelled diagram, explain the impact which the entry', ' [30]')
add('sb-q2-b-ii', '2-0', 'entry-of-new-firms-in-imperfect-competition', ref('B', 2, '(b)(ii)'), q2bii,
    '6 + 6', 12,
    [ask_row('r-diagram', q2bii[:q2bii.index(',')], 6,
             'The diagram, 6 marks. The scheme prices it as one 6 and prints the completed diagram, shown with the '
             'answer.'),
     point('r-explanation', H.opt('As more and more firms enter the industry:', '17 | P a g e'), 6,
           'The explanation, 6 marks.')],
    stem=q2, figure=SOL + 'p18-q2bii-diagram', **B)
q2c = H.q(8, 'Firms in some industries tend to engage in non', ' (i)')
# "Explain the underlined term." twice on this paper (here and Q8(c)(i)): the
# sentence holding the underlined term is read as part of the ask.
add('sb-q2-c-i', '2-0', 'non-price-competition', ref('B', 2, '(c)(i)'),
    f"{q2c} {H.q(8, 'Explain the underlined term.', ' (ii)')}",
    '6', 6, [point('r-1', H.opt('Non-price competition is a situation whereby', '(ii) Outline two examples'), 6,
                   'The explanation, 6 marks.')], **B)
add('sb-q2-c-ii', '2-0', 'effective-non-price-measures', ref('B', 2, '(c)(ii)'),
    H.q(8, 'Outline two examples of effective non', ' (iii)'), '2 x 3 + 5', 11,
    [anyN('r-examples', 'A non-price measure — any two', 6, 2, 3,
          [x.strip() for x in bl('• Clubcards/Loyalty cards', 'These measures can be considered')]
          if False else [H.traced(x) for x in ('Clubcards/Loyalty cards/Money-off vouchers.', 'Free car park', 'Coupons',
                                              '24hr opening hours', 'Free gifts/giveaways', 'Buy one get one free',
                                              'Convenient location', 'Advertising, promotion and branding')],
          'Two examples, 3 marks each.'),
     point('r-why', H.opt('These measures can be considered as effective', '(iii) Is non-price competition'), 5,
           'Why they are effective, 5 marks.')],
    kind='fixed', stem=q2c, **B)
q2ciii = H.q(8, 'Is non‐price competition beneficial to consumers?', ' [25]')
for word, start, end, firsts in (
        ('yes', 'It allows for price stability', 'No - not as beneficial',
         ['It allows for price stability', 'Consumer Loyalty is rewarded', 'Informative advertising',
          'A more diverse shopping experience']),
        ('no', 'Can get goods at cheaper prices:', '18 | P a g e',
         ['Can get goods at cheaper prices', 'Higher disposable income', 'More choice'])):
    pick(f'sb-q2-c-iii-{word}', '2-0', 'is-non-price-competition-good-for-consumers', ref('B', 2, '(c)(iii)', word),
         f'{q2ciii} Justify the choice: {word.upper()}.', f'A reason for answering {word.upper()} — any two',
         H.split(start, end, firsts), 2, 4,
         'Two reasons, 4 marks each. The scheme credits YES and NO, each with its own list.', stem=q2c, **B)

# Q3 ─ full employment; MNCs; the gender pay gap
q3a = H.q(8, 'The Irish economist Alan McQuaid said', ' (Source')
add('sb-q3-a-i', '3-2', 'full-employment', ref('B', 3, '(a)(i)'), H.q(8, 'Define the underlined term.', ' (ii)'), '8', 8,
    [point('r-1', H.opt('Full employment refers to the scenario', '(ii) Discuss the possible economic'), 8,
           'The definition, 8 marks.')], stem=q3a, **B)
pick('sb-q3-a-ii', '3-2', 'benefits-and-challenges-of-full-employment', ref('B', 3, '(a)(ii)'),
     H.q(8, 'Discuss the possible economic benefits and challenges', ' [26]'),
     'A benefit or a challenge — any three',
     side('Possible economic benefits', H.split('Increased standard of living for citizens:', 'Possible challenges may include',
                                              ['Increased standard of living for citizens', 'Fall in social welfare bill',
                                               'Increased aggregate demand', 'Increased investment',
                                               'An increase in confidence', 'Reduces inequality']))
     + side('Possible challenges', H.split('Possible skilled labour shortages:', '19 | P a g e',
                                       ['Possible skilled labour shortages', 'Possible wage demands',
                                        'Pressure on the state infrastructure', 'Loss of service', 'Inflationary pressures',
                                        'Negative Balance of Payments Impact'])),
     3, 6, 'Three points across the benefits and the challenges, 6 marks each (3 + 3). The scheme prices the three '
     'together, 3 x 6, without a split between them.', stem=q3a, **B)
pick('sb-q3-b', '4-1', 'risks-if-mncs-relocate', ref('B', 3, '(b)'),
     H.q(8, 'Discuss four possible economic risks for the Irish economy', ' [24]'), 'An economic risk — any four',
     H.split('Taxation revenues: multinationals', '20 | P a g e',
             ['Taxation revenues', 'Loss of employment', 'Effects on economic growth', 'Increased difficulty in attracting FDI',
              'Loss of skills in the workforce', 'Effect on regional development']),
     4, 6, 'Four risks, 6 marks each (3 + 3).', stem=H.q(8, 'Ireland is an attractive location for many', ' Discuss'), **B)
q3c = H.q(8, 'Despite being better educated overall', ' (Source')
add('sb-q3-c', '2-1', 'the-gender-pay-gap', ref('B', 3, '(c)'),
    ' '.join([H.q(8, 'Outline two reasons why gender pay inequality', ' (ii)'),
              H.q(8, 'Discuss two measures the Irish government could take', ' [25]')]),
    '1st: 8, 2nd: 7, 2 x 5', 25,
    [anyN('r-1', 'Two reasons and two measures', 25, 4, 8,
          H.split('Discrimination in the workplace:', '21 | P a g e',
                  ['Discrimination in the workplace', 'Lack of enforcement by State agencies',
                   'Balancing work and family responsibilities', '‘Glass ceiling’', 'Different jobs, different sectors',
                   'Undervaluing of women’s work and skills', 'Gender role of women / tradition'])
          + H.split('Awareness - raising Campaign:', '22 | P a g e',
                    ['Awareness - raising Campaign', 'Collective Agreements', 'Labour Inspections',
                     'Audits by companies', 'Make pay systems transparent', 'Gender Equality Studies',
                     'Implement / enforce existing laws', 'Education on gender stereotyping']),
          'Two reasons for the gap (the first seven listed, (i)) and two government measures (the last eight, (ii)). '
          'The scheme prices the four on one ladder across (i) and (ii): the first credited 8 marks, the second 7, '
          'the other two 5 each.', steps=[8, 7, 5, 5])],
    kind='fixed', stem=q3c, **B)

# Q4 ─ costs; merger and competition
q4 = H.q(9, 'The cost of doing business in Ireland', ' (Source')
add('sb-q4-a-i', '1-5', 'staying-open-at-a-loss', ref('B', 4, '(a)(i)'),
    H.q(9, 'In the short‐run firms may stay in the industry', ' (ii)'), '5', 5,
    [point('r-1', H.opt('If a firm’s total revenue is greater than its total variable costs', '(ii) State and explain three'),
           5, 'The explanation, 5 marks.')], stem=q4, **B)
pick('sb-q4-a-ii', '1-5', 'why-control-costs', ref('B', 4, '(a)(ii)'),
     H.q(9, 'State and explain three reasons why it is important for a business', ' [20]'), 'A reason — any three',
     H.split('Lower prices / increased demand / profits increase:', '23 | P a g e',
             ['Lower prices / increased demand', 'Increased competitiveness', 'Better use of scarce resources',
              'Survival of business']),
     3, 5, 'Three reasons, 5 marks each.', stem=q4, **B)
q4b = H.q(9, 'The table below shows cost data of a firm.', ' Output')
values = [f'{H.traced(lab)} — {H.traced(v)}' for lab, v in (
    ('MC1', '10'), ('MC2', '7'), ('MC3', '9'), ('MC4', '16'), ('MC5', '28'),
    ('ATC1', '20'), ('ATC2', '13.5'), ('ATC3', '12'), ('ATC4', '13'), ('ATC5', '16'))]
add('sb-q4-b-i', '1-5', 'marginal-and-average-total-cost', ref('B', 4, '(b)(i)'),
    H.q(9, 'Calculate the marginal cost and average total cost at each unit of output.', ' (ii)'), '10 (10 x 1)', 10,
    [anyN('r-1', 'Each cost', 10, 10, 1, values,
          'The five marginal costs and five average total costs, 1 mark each. The completed table is in the figure.')],
    kind='fixed', stem=q4b, figure=SOL + 'p25-q4bi-table', **B)
beside_ask(cards[-1], PAP + 'p09-q4b-table')
q4bii = H.q(9, 'Draw one graph showing marginal cost and average total cost and explain', ' [25]')
add('sb-q4-b-ii', '1-5', 'marginal-and-average-cost-curves', ref('B', 4, '(b)(ii)'), q4bii, '10 (10 x 1) + 5', 15,
    [ask_row('r-graph', H.q(9, 'Draw one graph showing marginal cost and average total cost', ' and explain'), 10,
             'The graph, 10 marks (10 x 1): the scheme’s plotted graph is shown with the answer.'),
     point('r-explanation', H.opt('When the marginal cost is lower than the average cost', '24 | P a g e'), 5,
           'The relationship between the curves, 5 marks.')],
    stem=q4b, figure=SOL + 'p25-q4bii-graph', **B)
beside_ask(cards[-1], PAP + 'p09-q4b-table')
q4c = H.q(9, 'Fiat Chrysler and Peugeot are engaged in merger talks', ' (Source')
add('sb-q4-c-i', '1-5', 'internal-economies-of-scale', ref('B', 4, '(c)(i)'), H.q(9, 'Define internal economies of scale.', ' (ii)'),
    '10', 10, [point('r-1', H.opt('Internal economies of scale refer to', '(ii) Outline three internal'), 10,
                     'The definition, 10 marks.')], stem=q4c, **B)
pick('sb-q4-c-ii', '1-5', 'merger-economies-of-scale', ref('B', 4, '(c)(ii)'),
     H.q(9, 'Outline three internal economies of scale which Fiat', ' (iii)'), 'An internal economy of scale — any three',
     H.split('Managerial economies / labour economies:', '(iii) Outline two reasons',
             ['Managerial economies', 'Purchasing economies', 'Technical economies', 'Economies in use of raw materials',
              'Economies in distribution', 'Marketing economies']),
     3, 4, 'Three economies of scale, 4 marks each.', stem=q4c, **B)
pick('sb-q4-c-iii', '1-3', 'blocking-a-merger', ref('B', 4, '(c)(iii)'),
     H.q(9, 'Outline two reasons why the EU’s competition enforcer', ' [30]'), 'A reason — any two',
     H.split('Exploitation of consumers:', '25 | P a g e',
             ['Exploitation of consumers', 'Higher prices', 'Reduced research and development',
              'Reduced quantity and choice for consumers']),
     2, 4, 'Two reasons, 4 marks each (2 + 2).', stem=q4c, **B)

# Q5 ─ enterprise; marginal revenue product; elasticity
q5a = H.q(10, 'An American survey has ranked Ireland', ' (Source')
add('sb-q5-a-i', '0-1', 'enterprise', ref('B', 5, '(a)(i)'), H.q(10, 'Define the factor of production enterprise.', ' (ii)'),
    '9', 9, [point('r-1', H.opt('Enterprise is the factor which helps', '(ii) Discuss four economic'), 9,
                   'The definition, 9 marks.')], stem=q5a, **B)
pick('sb-q5-a-ii', '0-1', 'why-entrepreneurship-matters', ref('B', 5, '(a)(ii)'),
     H.q(10, 'Discuss four economic reasons why entrepreneurship', ' [25]'), 'A reason — any four',
     H.split('Creates employment: entrepreneurs', '26 | P a g e',
             ['Creates employment', 'Organises production', 'Decides what prices to be charged',
              'Decides what commodities will be produced', 'Encourages further investment',
              'Provides an outlet for savers funds', 'Generates revenue for the government', 'May increase exports',
              'Creates income and wealth within the country']),
     4, 4, 'Four reasons, 4 marks each (2 + 2).', stem=q5a, **B)
q5b = H.q(10, 'The table below shows possible employment levels', ' Units')
q5b_fig = PAP + 'p10-q5b-table'
mp = [H.traced(f'MP{n}: {a}') for n, a in ((2, '25 – 10 = 15'), (3, '45 – 25 = 20'), (4, '60 – 45 = 15'),
                                         (5, '70 – 60 = 10'), (6, '77 – 70 = 7'), (7, '82 – 77 = 5'))]
mrp = [H.traced(f'MRP{n}: {a}') for n, a in ((2, '15 x 20 = 300'), (3, '20 x 20 = 400'), (4, '15 x 20 = 300'),
                                           (5, '10 x 20 = 200'), (6, '7 x 20 = 140'), (7, '5 x 20 = 100'))]
add('sb-q5-b-i', '2-1', 'marginal-revenue-product-of-labour', ref('B', 5, '(b)(i)'),
    H.q(10, 'Calculate the marginal product and marginal revenue product', ' (ii)'), '6 x 2 + 6 x 1', 18,
    [anyN('r-mp', 'Each marginal product', 12, 6, 2, mp, 'The six marginal products, 2 marks each.'),
     anyN('r-mrp', 'Each marginal revenue product', 6, 6, 1, mrp, 'The six marginal revenue products, 1 mark each.')],
    kind='fixed', stem=q5b, figure=q5b_fig, **B)
add('sb-q5-b-ii', '2-1', 'diminishing-marginal-returns', ref('B', 5, '(b)(ii)'),
    H.q(10, 'State at what point the law of diminishing marginal returns', ' (iii)'), '6', 6,
    [point('r-1', H.opt('The law of diminishing marginal returns sets in after', '(iii) How many workers'), 6,
           'The point and its explanation, 6 marks.')], stem=q5b, figure=q5b_fig, **B)
add('sb-q5-b-iii', '2-1', 'how-many-workers-to-employ', ref('B', 5, '(b)(iii)'),
    H.q(10, 'How many workers should be employed in the above firm?', ' [30]'), '6', 6,
    [point('r-1', H.opt('This firm should employ 6 employees.', '27 | P a g e'), 6,
           'The number and its reason, 6 marks.')], stem=q5b, figure=q5b_fig, **B)
q5c = H.q(10, 'An Irish firm which sells its product in both the EU and US', ' EU')
q5c_fig = PAP + 'p10-q5c-table'
add('sb-q5-c-i', '1-4', 'normal-or-inferior-good', ref('B', 5, '(c)(i)'),
    H.q(10, 'Explain whether you consider this good to be normal or inferior?', ' (ii)'), '7', 7,
    [point('r-1', H.opt('This good is a normal good.', '(ii) Suggest one reason'), 7, 'The answer and its reason, 7 marks.')],
    stem=q5c, figure=q5c_fig, **B)
add('sb-q5-c-ii', '1-4', 'why-price-elasticity-differs', ref('B', 5, '(c)(ii)'),
    H.q(10, 'Suggest one reason for the difference in the price elasticity', ' (iii)'), '7', 7,
    [anyN('r-1', 'A reason — any one', 7, 1, 7,
          [o.lstrip('• ').strip() for o in bl('• The good may have greater brand loyalty', '(iii) If the firm wishes')],
          'One reason, 7 marks. The scheme first states the difference: '
          + H.opt('The good has a lower price elasticity of demand', '• The good may have greater brand') + '')],
    kind='fixed', stem=q5c, figure=q5c_fig, **B)
add('sb-q5-c-iii', '1-4', 'where-to-charge-a-higher-price', ref('B', 5, '(c)(iii)'),
    H.q(10, 'If the firm wishes to maximise total sales revenue', ' [20]'), '6', 6,
    [point('r-1', H.opt('In the European market.', '28 | P a g e'), 6, 'The market and the reason, 6 marks.')],
    stem=q5c, figure=q5c_fig, **B)

# Q6 ─ trade protection; the EU; export markets
q6a = H.q(11, 'In October 2019 the World Trade Organisation', ' (Source')
add('sb-q6-a-i', '4-2', 'tariffs-and-subsidies', ref('B', 6, '(a)(i)'), H.q(11, 'Explain the terms tariffs and subsidies.', ' (ii)'),
    '2 x 6', 12,
    [point('r-tariffs', H.opt('Tariffs refer to taxes placed upon imports', 'Subsidies are payments'), 6, 'Tariffs, 6 marks.'),
     point('r-subsidies', H.opt('Subsidies are payments from the government', '(ii) Explain why the European'), 6,
           'Subsidies, 6 marks.')], stem=q6a, **B)
pick('sb-q6-a-ii', '4-2', 'why-the-eu-subsidises-airbus', ref('B', 6, '(a)(ii)'),
     H.q(11, 'Explain why the EU would give subsidies', ' (iii)'), 'A reason — any one',
     H.split('European employment:', '(iii) Discuss the arguments',
             ['European employment', 'European economic growth', 'Research and development', 'Encourage European']),
     1, 6, 'One reason, 6 marks (3 + 3).', stem=q6a, **B)
pick('sb-q6-a-iii', '4-2', 'arguments-against-protectionism', ref('B', 6, '(a)(iii)'),
     H.q(11, 'Discuss the arguments against trade protectionism.', ' [30]'), 'An argument against protectionism — any three',
     H.split('Firms may become over dependent on the protection:', '29 | P a g e',
             ['Firms may become over dependent', 'May lead to retaliation', 'Inequality:', 'Reduction in world output',
              'Employment levels']),
     3, 4, 'Three arguments, 4 marks each.', stem=q6a, **B)
q6b = H.q(11, 'As a member of the EU, Irish businesses enjoy free access', ' (i)')
add('sb-q6-b-i', '4-2', 'free-trade-area-and-common-market', ref('B', 6, '(b)(i)'),
    H.q(11, 'Distinguish between a free trade area and a common market', ' (ii)'), '7 + 6', 13,
    [point('r-fta', H.opt('A Free Trade Area means that member countries', 'A common market:'), 7, 'A free trade area, 7 marks.'),
     point('r-cm', H.opt('A common market: member countries agree', '(ii) Discuss three economic'), 6, 'A common market, 6 marks.')],
    stem=q6b, **B)
pick('sb-q6-b-ii', '4-2', 'benefits-of-eu-membership', ref('B', 6, '(b)(ii)'),
     H.q(11, 'Discuss three economic benefits to Ireland from continued EU membership.', ' [25]'), 'A benefit — any three',
     H.split('Free Trade Area / larger market / trade expansion:', '30 | P a g e',
             ['Free Trade Area / larger market', 'Capital Funding', 'Freedom movement of capital', 'Foreign Direct Investment',
              'EU legislation and policies']),
     3, 4, 'Three benefits, 4 marks each.', stem=q6b, **B)
q6c = H.q(11, 'Irish beef exports to China are set to grow', ' (Source')
pick('sb-q6-c-i', '4-2', 'advantages-of-new-export-markets', ref('B', 6, '(c)(i)'),
     H.q(11, 'Outline the economic advantages of growing new export markets', ' (ii)'), 'An advantage — any two',
     H.split('Access to larger markets/ Increased sales and profits:', '(ii) Discuss two possible difficulties',
             ['Access to larger markets', 'Economies of scale:', 'Diversifying risk / Brexit', 'Easier to access finance']),
     2, 5, 'Two advantages, 5 marks each.', stem=q6c, **B)
pick('sb-q6-c-ii', '4-2', 'difficulties-entering-the-chinese-market', ref('B', 6, '(c)(ii)'),
     H.q(11, 'Discuss two possible difficulties which Irish exporting companies', ' [20]'), 'A difficulty — any two',
     H.split('Transport costs: these increase', '32 | P a g e',
             ['Transport costs', 'Labour costs', 'Exchange rate risks', 'Language skills', 'Bureaucracy in other countries',
              'Level of costs', 'Competitiveness:', 'Accessing credit', 'Capacity of the firm']),
     2, 5, 'Two difficulties, 5 marks each.', stem=q6c, **B)

# Q7 ─ the carbon tax; government spending; an empty home tax
q7a = H.q(11, 'In Budget 2020 the government increased the rate of carbon tax', ' (Source')
add('sb-q7-a-i', '3-1', 'the-carbon-tax-as-a-regressive-tax', ref('B', 7, '(a)(i)'),
    H.q(11, 'Why do some people consider the carbon tax to be a regressive tax?', ' (ii)'), '7', 7,
    [point('r-1', H.opt('The carbon tax can be considered regressive', 'Takes a higher percentage'), 7,
           'The explanation, 7 marks. The scheme also accepts its shorter statement.',
           accepts=[H.opt('Takes a higher percentage of income from low income', '(ii) Outline the possible positive')])],
    stem=q7a, **B)
pick('sb-q7-a-ii', '3-1', 'consequences-of-the-carbon-tax-rise', ref('B', 7, '(a)(ii)'),
     H.q(11, 'Outline the possible positive and negative economic consequences', ' [25]'),
     'A positive or negative consequence — any three',
     side('Positive', H.split('Less consumption of demerit goods:', '33 | P a g e',
                              ['Less consumption of demerit goods', 'Closer to achieving EU targets', 'Additional tax revenue',
                               'Changing consumer mindsets', 'Evasion impossible', 'No disincentive to work']))
     + side('Negative', H.split('Higher household costs:', '34 | P a g e',
                                ['Higher household costs', 'Higher business costs', 'Falling international competitiveness',
                                 'Pressure on public transport', 'Will increase inflation'])),
     3, 6, 'Three consequences across the positive and the negative, 6 marks each. The scheme prices the three '
     'together, 3 x 6, without a split between them.', stem=q7a, **B)
q7b = H.q(11, 'In Budget 2020 the government gave the green light', ' (Source')
add('sb-q7-b-i', '3-1', 'current-and-capital-spending', ref('B', 7, '(b)(i)'),
    H.q(11, 'Identify one example of current government expenditure', ' (ii)'), '8 (2 x 4)', 8,
    [point('r-current', H.opt('Current government expenditure: expenditure for An Garda', 'Capital government expenditure:'), 4,
           'The current example and why, 4 marks.'),
     point('r-capital', H.opt('Capital government expenditure: expenditure for construction', '(ii) Discuss the social'), 4,
           'The capital example and why, 4 marks.')], stem=q7b, **B)
pick('sb-q7-b-ii', '3-1', 'benefits-of-garda-spending', ref('B', 7, '(b)(ii)'),
     H.q(11, 'Discuss the social benefits and economic benefits of increased spending', ' (iii)'), 'A benefit — any three',
     H.split('Injection into the circular flow of income:', 'Must have one social',
             ['Injection into the circular flow of income', 'More employment/more spending',
              'More legitimate businesses', 'Less crime']),
     3, 4, 'Three benefits, 4 marks each (3 x 4). ' + H.opt('Must have one social /economic benefit.', '(iii) Outline one'),
     stem=q7b, **B)
add('sb-q7-b-iii', '3-1', 'toll-roads', ref('B', 7, '(b)(iii)'),
    H.q(11, 'Outline one argument for and one argument against making new sections', ' [30]'), '5 + 5 (3 + 2)', 10,
    [heading('r-for', H.traced('For') + ' — any one',
             H.split('Higher quality: the use of toll funds', 'Against\nOther motor taxes',
                     ['Higher quality', 'Financing construction / maintenance', 'More efficient transport']), 5,
             'One argument for, 5 marks (3 + 2).'),
     heading('r-against', H.traced('Against') + ' — any one',
             H.split('Other motor taxes: road-users', '35 | P a g e', ['Other motor taxes', 'Regressive:', 'Firms face higher costs']), 5,
             'One argument against, 5 marks (3 + 2).')],
    kind='fixed', stem=q7b, **B)
q7c = H.q(11, 'An empty home tax is needed to tackle the homelessness crisis', ' (i)')
q7ci = H.q(11, 'In your opinion, is this empty home tax a good idea?', ' (ii)')
for word, start, end, firsts in (
        ('yes', 'Encourage people to sell the vacant property:', 'No\nExtra tax unfair',
         ['Encourage people to sell the vacant property', 'Misallocation of resources', 'Maye ease the housing crisis']),
        ('no', 'Extra tax unfair on top of LPT:', '(ii) Suggest three alternative',
         ['Extra tax unfair on top of LPT', 'Nanny state / interference'])):
    pick(f'sb-q7-c-i-{word}', '3-1', 'an-empty-home-tax', ref('B', 7, '(c)(i)', word),
         f'{q7ci} Justify the choice: {word.upper()}.', f'A reason for answering {word.upper()} — any one',
         H.split(start, end, firsts), 1, 8,
         'One reason, 8 marks. The scheme credits YES and NO, each with its own list.', stem=q7c, **B)
pick('sb-q7-c-ii', '3-1', 'reducing-homelessness', ref('B', 7, '(c)(ii)'),
     H.q(11, 'Suggest three alternative measures the government could take', ' [20]'), 'A measure — any three',
     H.split('Social housing: the more social housing', '36 | P a g e',
             ['Social housing', 'Modular housing', 'Build up, not out', 'Rezone land', 'Reduce tax / charges',
              'Increase the levy on land hoarders', 'Increased provision of emergency accommodation',
              'Rent freeze in Rent Pressure Zones']),
     3, 4, 'Three measures, 4 marks each.', stem=q7c, **B)

# Q8 ─ national income terms and data; the national debt
add('sb-q8-a', '3-0', 'transfer-payments-benefits-in-kind-and-nfi', ref('B', 8, '(a)'),
    H.q(12, 'Explain the following economic terms, giving an appropriate example', ' [21]'), '7 + 7 + 7 (5 + 2)', 21,
    [point('r-transfer', H.opt('Transfer Payments: payments for which', 'Benefits-in-kind:'), 7,
           'Transfer payments with an example, 7 marks (5 + 2).'),
     point('r-bik', H.opt('Benefits-in-kind: payment in any non-monetary form', 'Net Factor Income from the Rest'), 7,
           'Benefits-in-kind with an example, 7 marks (5 + 2).'),
     point('r-nfi', H.opt('Net Factor Income from the Rest of the World: All income', '37 | P a g e')
           .replace('Ireland2 minus1', 'Ireland² minus¹').replace('origin2.', 'origin².'), 7,
           'Net factor income with an example, 7 marks (5 + 2). The small raised figures are the scheme’s own, as it '
           'prints them.')], **B)
q8b = ' '.join([H.q(12, 'The following table shows National Income (Y)', ' Y'),
                H.q(12, 'Use this data to answer the following:', ' (i)')])
q8b_fig = PAP + 'p12-q8b-table'
for cid, concept, parts, ask, answer, note in (
        ('sb-q8-b-i', 'government-spending-from-the-identity', '(b)(i)', H.q(12, 'Calculate the level of government spending in 2018.', ' (ii)'),
         H.traced('G = 60,000'), 'G, 5 marks, with the scheme’s working: 200,000 = 70,000 + 50,000 + G + 80,000 – 60,000.'),
        ('sb-q8-b-ii', 'national-income-from-the-identity', '(b)(ii)', H.q(12, 'Calculate the level of National Income in 2019.', ' (iii)'),
         H.traced('Y = 250,000'), 'Y, 5 marks, with the scheme’s working: Y = 105,000 + 55,000 + 65,000 + 90,000 – 65,000.')):
    add(cid, '3-0', concept, ref('B', 8, parts), ask, '5', 5, [point('r-1', answer, 5, note)], stem=q8b, figure=q8b_fig, **B)
add('sb-q8-b-iii', '3-0', 'marginal-propensity-to-import', ref('B', 8, '(b)(iii)'),
    H.q(12, 'Define marginal propensity to import (MPM).', ' (iv)'), '5', 5,
    [point('r-1', H.opt('The marginal propensity to import is the proportion', '(iv) Calculate the Marginal'), 5,
           'The definition, 5 marks.')], stem=q8b, figure=q8b_fig, **B)
add('sb-q8-b-iv', '3-0', 'calculating-the-mpm', ref('B', 8, '(b)(iv)'),
    H.q(12, 'Calculate the marginal propensity to import (MPM).', ' (v)'), '5', 5,
    [point('r-1', H.traced('0.1'), 5, 'The MPM, 5 marks. The scheme sets the working as a fraction, the change in imports '
           'over the change in income; the figure shows it as printed.')],
    stem=q8b, figure=SOL + 'p39-q8biv-working', **B)
beside_ask(cards[-1], q8b_fig)
add('sb-q8-b-v', '3-0', 'the-multiplier', ref('B', 8, '(b)(v)'),
    H.q(12, 'Calculate the value of the multiplier and explain', ' [30]'), '5 + 5', 10,
    [point('r-multiplier', H.traced('Multiplier = 2.5'), 5,
           'The multiplier, 5 marks. The scheme sets the MPC and the multiplier as fractions; the figure shows them as printed.'),
     point('r-meaning', H.opt('This figure means that any injection into the economy', '38 | P a g e'), 5,
           'Its economic meaning, 5 marks.')],
    stem=q8b, figure=SOL + 'p39-q8bv-working', **B)
beside_ask(cards[-1], q8b_fig)
q8c = H.q(12, 'Ireland’s national debt reached €206 billion', ' (Source')
add('sb-q8-c-i', '3-1', 'the-national-debt', ref('B', 8, '(c)(i)'),
    f"{q8c} {H.q(12, 'Explain the underlined term.', ' (ii)')}", '6', 6,
    [point('r-1', H.opt('National debt is the total/cumulative amount', '(ii) Name the agency'), 6, 'The explanation, 6 marks.')],
    **B)
add('sb-q8-c-ii', '3-1', 'the-ntma', ref('B', 8, '(c)(ii)'),
    H.q(12, 'Name the agency responsible for managing Ireland’s national debt.', ' (iii)'), '6 (3 + 3)', 6,
    [point('r-name', H.opt('The National Treasury Management Agency NTMA', 'Its core function'), 3, 'The agency, 3 marks.'),
     anyN('r-function', 'One other function — any one', 3, 1, 3,
          [o.lstrip('• ').strip() for o in bl('• Borrowing on behalf of the Irish Government', '(iii) Outline three risks')],
          'One other function, 3 marks. The scheme states the agency’s core function as: '
          + H.opt('Its core function is borrowing for the exchequer', 'Amongst its duties'))],
    kind='fixed', stem=q8c, **B)
pick('sb-q8-c-iii', '3-1', 'risks-of-the-national-debt', ref('B', 8, '(c)(iii)'),
     H.q(12, 'Outline three risks to the Irish economy arising', ' [24]'), 'A risk — any three',
     H.split('Opportunity costs involved / loss of public services:', '39 | P a g e',
             ['Opportunity costs involved', 'Increased burden on current and future taxpayers', 'Annual interest repayments',
              'Loss of economic sovereignty', 'Circular flow of income']),
     3, 4, 'Three risks, 4 marks each (2 + 2).', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
