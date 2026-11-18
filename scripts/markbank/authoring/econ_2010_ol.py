#!/usr/bin/env python3
"""Economics 2010 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2010-ol-ev.json, made
from a visual sweep of all 12 paper pages and 33 scheme pages before any 2010
Ordinary card existed. Section B restarts at Question 1, so every citation
names its section and every id carries it (-sa-, -sb-). Question wording and
stems are sliced from the question paper; every marking point is sliced from
the scheme (econ_legacy_lib.py). The scheme's cover prints its level in
capitals ("ORDINARY LEVEL"), so its scheme file was built with the appenders'
cover check pointed at the file (visually verified as the English Ordinary
scheme). A stem stops before any printed table or diagram: that is the crop
beside the typed ask, and printed items a student must read to answer are
typed from the text layer. The only prose written here is guidance: tariffs,
route labels and what a figure or a calculation shows.

The scheme's Group / Statement / Explanation tables print each group's
statements as one cell and its explanations as the next, and their rows do
not line up: a statement is paired with the explanation that restates it, and
an explanation that restates none stands alone (`paired`).

Section B Q6(b) is printed "(i) Name ... (i) Discuss ... (ii) Outline ...", an
SEC misprint; the scheme numbers the three parts (i)-(iii), and so does the
paper reader, so the cards are cited (b)(i), (b)(ii) and (b)(iii).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point, tidy  # noqa: E402

H = Old(2010, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2010, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2010-OL-scheme-'
PAP = 'economics-2010-OL-paper-'
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
CELLS = [ln.strip() for ln in H.full_md.split('<!-- markbank:table-cells -->', 1)[1]
         .split('<!-- /markbank:table-cells -->', 1)[0].splitlines()]


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def pair(head, body):
    return f'{H.traced(head)} — {H.traced(body)}'


def se(statement):
    """A two-column row: the heading cell and the cell after it."""
    i = CELLS.index(statement)
    return f'{H.traced(statement)} — {H.traced(CELLS[i + 1])}'


def bullets_of(cell):
    """A cell's own bullets, each traced."""
    return [H.traced(p.strip()) for p in cell.split('•') if p.strip()]


def paired(statements, explanations, rows):
    """One group of a Group / Statement / Explanation table. `statements` lists
    the statement cell's statements (each traced on its own), `explanations` is
    the explanation cell; `rows` pairs (statement index, explanation index) by
    what each explanation restates. A statement index of None is an explanation
    that restates no statement; an explanation index of None, a statement the
    scheme explains nowhere."""
    ex = bullets_of(explanations)
    out = []
    for s, e in rows:
        if s is None:
            out.append(ex[e])
        elif e is None:
            out.append(H.traced(statements[s]))
        else:
            out.append(f'{H.traced(statements[s])} — {ex[e]}')
    return out


GLYPH_BULLETS = re.compile('[\uf0a7\uf0b7]')


def glyph_bullets(start, end):
    """Responses the scheme bullets with a symbol-font glyph the text layer
    reads as a private-use character: cut at each glyph, each traced."""
    return [H.traced(tidy(p)) for p in GLYPH_BULLETS.split(H.chunk(start, end)) if tidy(p)]


def lettered(start, end, letters):
    """A list the scheme letters (a), (b) ...: each item cut at the next letter,
    read without its own letter. The common cutters stop at "(a)"-"(c)" only."""
    text = tidy(H.chunk(start, end))
    at = [text.index(f'({x}) ') for x in letters]
    out = []
    for i, a in enumerate(at):
        b = at[i + 1] if i + 1 < len(at) else len(text)
        # Traced as printed; the symbol-font bullet is then set as the bullet it is
        # (the provenance gate ignores every bullet form).
        out.append(GLYPH_BULLETS.sub('•', H.traced(tidy(text[a + len(f'({letters[i]}) '):b]))))
    return out


def unpriced_menu(rid, label, claim, options, note):
    """A menu inside a questionTotal card: the scheme prices the whole answer and
    never says what one response is worth, so the group carries no per-option
    value (as the shipped Chemistry 2026 OL Q11(d)B(vi) card does). The session
    prints a group's per-option marks only when the value is a number."""
    return {"id": rid, "kind": "anyN", "verbatim": label, "marks": None, "openList": True,
            "contextNote": note, "group": {"claimMax": claim, "perOption": None, "options": options}}


def qn(page, anchor, start, end):
    """An ask the page prints more than once, read after a unique anchor before it."""
    text = H.q(page, anchor, end)
    return text[text.index(start):]


def ladder(rid, label, total, options, steps, note):
    return anyN(rid, label, total, len(steps), steps[0], options, note, steps=steps)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ the IMF and the WTO
add('sa-q1', '4-1', 'the-imf-and-the-wto', ref('A', 1, '(i)–(ii)'),
    H.q(2, 'What economic institutions do the following initials stand for?', ' (16 marks)'), '(4 + 2 + 2) x 2', 16,
    [anyN('r-imf', 'IMF — each word of its name', 8, 3, 4, [H.traced(x) for x in ('International', 'Monetary', 'Fund')],
          'IMF in full: the scheme prints ' + H.traced('4 + 2 + 2') + ' beside the name without saying which word earns the 4, '
          'so the first correct word is claimed at 4 and the other two at 2.', steps=[4, 2, 2]),
     anyN('r-wto', 'WTO — each word of its name', 8, 3, 4, [H.traced(x) for x in ('World', 'Trade', 'Organisation')],
          'WTO in full: 4 + 2 + 2 beside the name, read the same way.', steps=[4, 2, 2])],
    kind='fixed', **A)

# Q2 ─ helping less developed countries
add('sa-q2', '4-0', 'helping-less-developed-countries', ref('A', 2),
    H.q(2, 'Many Irish citizens donate financial aid to organisations', ' Organisation:'), '8 + 8', 16,
    [heading('r-organisation', 'An organisation — any one',
             [H.traced(x) for x in ('Goal', 'Concern', 'Trócaire', 'Red Cross', 'World Vision', 'Bóthar')], 8,
             'One organisation, ' + H.traced('8 marks') + ': the scheme names six and adds “etc.”'),
     heading('r-measure', 'A measure — any one',
             H.split('1. Buy goods produced in LDCs', '1 measure at 8 marks.',
                     ['Buy goods produced in LDCs', 'Put pressure on governments', 'Campaign for debt reduction.',
                      'Encourage multinationals', 'Volunteer to work in a LDC.', 'Buy Fair Trade products',
                      'Donations other than financial aid.']), 8,
             'One measure, ' + H.traced('8 marks') + '.')],
    kind='fixed', **A)

# Q3 ─ which market structure
structures = (('Product differentiation exists', 'Imperfect Competition'), ('Products are homogeneous/identical', 'Perfect Competition'),
              ('Firm has complete control over price or output', 'Monopoly'))
add('sa-q3', '2-0', 'which-market-structure', ref('A', 3, '(i)–(iii)'),
    # The three statements follow the ask, from the paper's own table rows.
    f"{H.q(2, 'Name the market structure (Perfect Competition, Imperfect Competition or Monopoly)', ' STATEMENT')} "
    f"{H.q(2, '(i) Product differentiation exists', ' (16 marks)')}", '8 + 4 + 4', 16,
    [ladder('r-1', 'Each statement named', 16, [pair(s, m) for s, m in structures], [8, 4, 4],
            'All three: ' + H.traced('1st correct answer: 8 marks. 2nd & 3rd: 2 at 4 marks each.'))],
    kind='fixed', **A)

# Q4 ─ opportunity cost
add('sa-q4', '0-1', 'opportunity-cost-and-an-example', ref('A', 4),
    H.q(2, 'Explain the term opportunity cost and give one example.', ' Explanation:'), '16', 16,
    [point('r-explanation', H.traced('The cost of foregone alternatives.'), None,
           'The explanation: the scheme accepts either of its two.',
           accepts=[H.traced('The cost of passing up the next best choice when making a decision.')]),
     point('r-example', H.traced('The opportunity cost of going to college is the money you would have earned if you took employment instead.'),
           None, 'An example: the scheme accepts any relevant one. Claim the complete answer: the scheme prices the explanation '
           'and the example ' + H.traced('16 marks') + ' together, without dividing them.')],
    kind='questionTotal', **A)

# Q5 ─ unemployment and the current budget deficit
pick('sa-q5', '3-1', 'unemployment-and-the-budget-deficit', ref('A', 5),
     H.q(2, 'State two economic effects which an increasing level of unemployment', ' Effect 1:'), 'An effect — any two',
     H.split('1. Social welfare payments will increase', '2 effects at 8 marks each.',
             ['Social welfare payments will increase', 'Increased expenditure on job promotion', 'More staff may have to be employed',
              'Reduced income tax revenue', 'Reduced corporation tax revenue', 'Reduced indirect tax revenue',
              'Increased government expenditure on medical cards', 'Government must find other sources of income']),
     2, 8, 'Two effects, ' + H.traced('2 effects at 8 marks each.')[len('2 effects at '):], **A)

# Q6 ─ more people in third-level education
add('sa-q6', '3-5', 'advantages-of-third-level-education', ref('A', 6),
    H.q(3, 'Currently more people are availing of third-level education in Ireland.', ' Advantage 1:'), '10 + 7', 17,
    [ladder('r-1', 'An advantage — any two', 17,
            H.split('1. Future employment prospects for these citizens may improve.', '1st correct answer: 10 marks.',
                    ['Future employment prospects', 'Standard of living for these citizens', 'Workforce becomes more highly skilled',
                     'More educated workforce may help attract FDI', 'More educated workforce may result in better',
                     'Towns / cities where 3rd level colleges', 'Opportunity costs: more people']),
            [10, 7], 'Two advantages: ' + H.traced('1st correct answer: 10 marks. 2nd correct answer: 7 marks.'))],
    kind='fixed', **A)

# Q7 ─ substitutes and complements for mobile phones
# The four items are one printed row of cells, which the text layer runs together; each is
# read out of that run, so the typed list keeps the cells apart.
q7_run = H.q(3, 'Mobile Credit e-mail', ' Answer:')
q7_items = [x for x in ('Mobile Credit', 'e-mail', 'Landline Telephone', 'Mobile Ringtones & Apps') if x in q7_run]
assert ' '.join(q7_items) == q7_run, q7_run
subs, comps = H.traced('Substitutes for mobile phone'), H.traced('Complements for mobile phone')
add('sa-q7', '1-1', 'substitutes-and-complements-for-phones', ref('A', 7),
    f"{H.q(3, 'The following items are either substitutes or complements for Mobile Phones.', ' Mobile Credit')} "
    f"{', '.join(q7_items)}", '5 + 4 + 4 + 4', 17,
    [ladder('r-1', 'Each item placed', 17,
            [f'{subs} — {H.traced(x)}' for x in ('e-mail', 'Landline Telephone')]
            + [f'{comps} — {H.traced(x)}' for x in ('Mobile Credit', 'Mobile Ringtones & Apps')],
            [5, 4, 4, 4], 'All four: ' + H.traced('1st correct answer: 5 marks.') + ' '
            + H.traced('2nd, 3rd & 4th correct answer: 4 marks each.'))],
    kind='fixed', figure=PAP + 'p03-q7-table', **A)

# Q8 ─ entrepreneurship
add('sa-q8', '0-1', 'why-entrepreneurship-matters', ref('A', 8),
    H.q(3, 'Entrepreneurship is important in the development of an economy.', ' Explanation:'), '10 + 7', 17,
    [point('r-explanation', H.traced('Entrepreneurship is the risk undertaken by an individual in combining the other factors into a '
                                     'production unit to produce a product or provide a service in the hope of making a profit.'), 10,
           'The explanation, 10 marks.'),
     heading('r-reason', 'A reason — any one',
             H.split('1. Creates employment', '\n⟨(17 marks)⟩',
                     ['Creates employment', 'Organises production', 'Decides what commodities will be produced', 'Decides prices to be charged',
                      'Encourages further investment', 'Provides an outlet for savers funds', 'Generates revenue for the government',
                      'May increase exports', 'Creates wealth within the country']), 7,
             'One reason, 7 marks.')],
    kind='fixed', **A)

# Q9 ─ cross-border shopping
add('sa-q9', '4-2', 'effects-of-cross-border-shopping', ref('A', 9),
    H.q(3, 'State two economic effects on the economy of the Republic of Ireland', ' Effect 1:'), '17', 17,
    [unpriced_menu('r-1', 'An effect — any two', 2,
                   H.split('1. Taxation revenue falls', '\n⟨(17 marks)⟩',
                           ['Taxation revenue falls', 'Unemployment:', 'More competitive pricing:', 'Taxation policy:', 'Increased imports',
                            'Closure of businesses', 'Pressure to change government policies']),
                   'Any two of these. Claim the complete answer: the scheme prices the two effects ' + H.traced('17 marks')
                   + ' together, without saying what one effect is worth.')],
    kind='questionTotal', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ monopoly; barriers to entry; An Post
q1 = H.q(4, 'The diagram below represents a Monopoly firm in equilibrium.', ' Monopoly Price')
q1_fig = PAP + 'p04-q1-diagram'
add('sb-q1-a-i', '2-0', 'lines-of-the-monopolist', ref('B', 1, '(a)(i)'),
    f"{H.q(4, 'Copy the diagram into your answerbook.', ' (i)')} {H.q(4, 'Clearly label each of the lines numbered 1 to 3.', ' (ii)')}",
    '3 @ 4', 12,
    [point(f'r-{n}', f'{n} — {H.traced(name)}', 4, f'Line {n}, ' + H.traced('4 marks ( 2 + 2 )') + '.')
     for n, name in (('1', 'Marginal Cost'), ('2', 'Average Cost'), ('3', 'Marginal Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'price-and-cost-of-the-monopolist', ref('B', 1, '(a)(ii)'),
    H.q(4, 'The above firm produces Q1. Show on your diagram:', ' (21 marks)'), '5 + 4', 9,
    [ladder('r-1', 'Each label shown', 9,
            [H.traced(x) for x in ('P1 the price charged for this output', 'C1 the average cost of producing this output')], [5, 4],
            'Both: ' + H.traced('1st correct response: 5 marks. 2nd correct response: 4 marks.') + ' P1 is level with the point where the '
            'line up from Q1 meets the AR line, and C1 with the point where it meets the average cost curve, as the scheme’s diagram shows.')],
    kind='fixed', stem=q1, figure=SOL + 'p09-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
barriers = (('Patents and Copyrights', 'A patent/ copyright confers the sole right on a business to a particular manufacturing process for a '
                                       'particular commodity.'),
            ('Legal monopolies / state monopolies', 'The government may grant to a company the sole right to supply a good or service so that '
                                                    'there is a legal restriction on competition.'),
            ('Economies of scale', 'Arise where the largest supplier in an industry has a significant cost advantage over competitors because '
                                   'of its large size. It is unlikely that a potential competitor would be willing to make the capital investment '
                                   'needed to enter the monopolist\'s market.'))
add('sb-q1-b', '2-0', 'barriers-to-entry-with-examples', ref('B', 1, '(b)'),
    H.q(4, 'Explain each of the following barriers to entry', ' (24 marks)'), '12 + 6 + 6', 24,
    [ladder('r-1', 'Each barrier explained, with an example', 24, [pair(b, e) for b, e in barriers], [12, 6, 6],
            'All three, each with an example: ' + H.traced('1st Correct explanation 12 marks') + ', the '
            + H.traced('2nd and 3rd at 6 marks each') + '. The scheme’s examples for each barrier are in its table, shown with the answer.')],
    kind='fixed', figure=SOL + 'p10-q1b-table', **B)
q1c = H.q(4, 'An Post is a monopoly firm in the delivery of ‘letter-post’.', ' (i)')
pick('sb-q1-c-i', '2-0', 'advantages-of-the-an-post-monopoly', ref('B', 1, '(c)(i)'),
     H.q(4, 'State and explain two advantages of this monopoly for consumers.', ' (ii)'), 'An advantage — any two',
     H.split('1. Convenience\n', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['Convenience', 'Relatively cheap cost of the service', 'Range of services provided', 'Banking services in areas where no banks operate.',
              'Social benefits']),
     2, 5, 'Two advantages, 5 marks each (3 to state it, 2 to explain it).', stem=q1c, **B)
pick('sb-q1-c-ii', '1-1', 'why-letter-post-demand-is-falling', ref('B', 1, '(c)(ii)'),
     H.q(4, 'Explain two reasons for the falling demand for letter-post.', ' (iii)'), 'A reason — any two',
     H.split('1. Change in the price of the good.', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['Change in the price of the good.', 'Change in consumer tastes / fashion.', 'Change in price of substitutes.']),
     2, 5, 'Two reasons, 5 marks each (3 + 2).', stem=q1c, **B)
pick('sb-q1-c-iii', '3-2', 'closing-rural-post-offices', ref('B', 1, '(c)(iii)'),
     H.q(4, 'Discuss two effects of the closure of small rural post offices for the local economy.', ' (30 marks)'), 'An effect — any two',
     H.split('1. Loss of essential services.', '2 at 5 marks each. State: 3 marks. Explain: 2marks.',
             ['Loss of essential services.', 'Loss of banking services.', 'Increase in rural unemployment.', 'Decline in rural communities.']),
     2, 5, 'Two effects, 5 marks each (3 + 2).', stem=q1c, **B)

# Q2 ─ marginal utility; a black market for concert tickets; hotel accommodation
q2a = H.q(5, 'As consumers consume more units of a good their marginal utility will eventually fall.', ' (i)')
add('sb-q2-a-i', '1-1', 'marginal-utility', ref('B', 2, '(a)(i)'),
    qn(5, 'their marginal utility will eventually fall.', 'Explain the underlined term.', ' (ii)'), '5 + 2', 7,
    [point('r-1', H.traced('Marginal utility is the extra utility /satisfaction gained'), 5,
           'The extra utility or satisfaction, 5 marks: the scheme prints ' + H.traced('7 marks') + ' beside the ask, and 5 marks and '
           '2 marks beneath the two halves of its sentence, read here in that order.'),
     point('r-2', H.traced('when you consume one extra unit of a good.'), 2, 'One extra unit, 2 marks.')],
    stem=q2a, **B)
add('sb-q2-a-ii', '1-1', 'a-good-whose-utility-may-not-fall', ref('B', 2, '(a)(ii)'),
    H.q(5, 'Suggest one good a person may consume which may not result in a fall', ' (iii)'), '5 + 3', 8,
    [heading('r-good', 'A good — any one', [H.traced(x) for x in ('Cigarettes', 'Alcohol', 'Medicines')], 5,
             'The good, ' + H.traced('5 marks') + ': the scheme names three and adds “etc.”'),
     heading('r-explanation', 'The explanation — any one',
             glyph_bullets('For addictive goods the consumer may get the same utility', 'Explanation: 3 marks'), 3,
             'The explanation, ' + H.traced('Explanation: 3 marks')[len('Explanation: '):] + '.')],
    kind='fixed', stem=q2a, **B)
q2a_table = PAP + 'p05-q2a-table'
add('sb-q2-a-iii', '1-1', 'when-diminishing-marginal-utility-sets-in', ref('B', 2, '(a)(iii)'),
    H.q(5, 'Complete the following table in your answerbook.', ' Number of units'), '2 + 2 + 2 + 2 + 2', 10,
    [point('r-4', f"4 — {H.traced('20')}", 2, 'The marginal utility of the 4th unit, 2 marks: 95 less 75.'),
     point('r-5', f"5 — {H.traced('15')}", 2, 'The 5th unit, 2 marks: 110 less 95.'),
     point('r-6', f"6 — {H.traced('5')}", 2, 'The 6th unit, 2 marks: 115 less 110. The scheme prints '
           + H.traced('2 marks 2 marks 2 marks') + ' beneath the three values.'),
     point('r-point', H.traced('After the 3rd unit is consumed / on the consumption of the 4th unit'), 2,
           'Where diminishing marginal utility sets in, 2 marks.'),
     point('r-why', H.traced('On the consumption of the 4th unit the consumer’s marginal utility has fallen from 40 units to 20 units.'), 2,
           'The explanation, 2 marks. The completed table is shown with the answer.')],
    kind='fixed', stem=q2a, figure=SOL + 'p12-q2aiii-table', **B)
beside_ask(cards[-1], q2a_table)
q2b = H.q(5, 'The diagram below represents the supply of seats for the Rihanna concert', ' Price S1')
q2b_fig = PAP + 'p05-q2b-diagram'
add('sb-q2-b-i', '1-0', 'a-black-market', ref('B', 2, '(b)(i)'),
    qn(5, 'a ‘black market’ may develop for the tickets. Price', 'Explain the underlined term.', ' (ii)'), '6', 6,
    [heading('r-1', 'A black market — either',
             [H.traced('An unofficial /illegal market.'), H.traced('Sellers offer tickets on this market at prices other than their face value.')],
             6, 'The explanation, 6 marks: the scheme accepts either.')],
    kind='fixed', stem=q2b, figure=q2b_fig, **B)
add('sb-q2-b-ii', '1-0', 'a-fixed-supply-of-seats', ref('B', 2, '(b)(ii)'),
    H.q(5, 'Explain the relationship between the price of tickets and the supply of seats', ' (iii)'), '6', 6,
    [point('r-1', H.traced('As the price of tickets change the supply of seats remains unchanged / fixed.'), 6, 'The relationship, 6 marks.')],
    stem=q2b, figure=q2b_fig, **B)
pick('sb-q2-b-iii', '1-0', 'effects-of-a-ticket-black-market', ref('B', 2, '(b)(iii)'),
     H.q(5, 'Discuss two effects for potential ticket buyers', ' (20 marks)'), 'An effect — any two',
     H.split('1. It is likely that tickets will sell', '2 effects at 4 marks each = 8 marks.',
             ['It is likely that tickets', 'There is a possibility', 'Additional security procedures', 'Promoters, seeing that demand']),
     2, 4, 'Two effects, ' + H.traced('4 marks each') + '.', stem=q2b, figure=q2b_fig, **B)
q2c = H.q(5, 'The demand for hotel accommodation in Ireland has been decreasing.', ' (i)')
pick('sb-q2-c-i', '1-1', 'why-hotel-demand-is-falling', ref('B', 2, '(c)(i)'),
     H.q(5, 'State and explain two possible economic reasons for this development.', ' (ii)'), 'A reason — any two',
     H.split('Drop in incomes/ holidays a luxury item', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['Drop in incomes/ holidays', 'Increase in savings.', 'Decline in foreign tourists', 'Economic recession', 'Prices of alternatives.']),
     2, 5, 'Two reasons, 5 marks each (3 to state it, 2 to explain it).', stem=q2c, **B)
pick('sb-q2-c-ii', '1-0', 'falling-demand-and-the-hotel-industry', ref('B', 2, '(c)(ii)'),
     H.q(5, 'State and explain two economic effects of this development for the hotel industry.', ' (iii)'), 'An effect — any two',
     H.split('Lower revenues/ profits:', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['Lower revenues/ profits:', 'Closures:', 'Rising Unemployment:', 'Lower prices:', 'Loss making hotels:']),
     2, 5, 'Two effects, 5 marks each (3 + 2).', stem=q2c, **B)
pick('sb-q2-c-iii', '1-2', 'reviving-hotel-demand', ref('B', 2, '(c)(iii)'),
     H.q(5, 'Suggest two economic measures which the hotel industry could take', ' (30 marks)'), 'A measure — any two',
     H.split('Reduce prices / Improve quality of services', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['Reduce prices / Improve quality', 'Advertising / Promotion.', 'Broaden the range of services', 'Target UK / Northern Irish consumers.']),
     2, 5, 'Two measures, 5 marks each (3 + 2).', stem=q2c, **B)

# Q3 ─ the determinants of demand; a subsidy for sugar beet; price elasticity
pick('sb-q3-a', '1-1', 'what-affects-demand', ref('B', 3, '(a)'),
     H.q(6, 'State and explain four factors which affect the demand for a good or service.', ' (20 marks)'), 'A factor — any four',
     H.split('1. Price of the good itself.', '4 factors at 5 marks each.',
             ['Price of the good itself.', 'Price of complementary good.', 'Prices of substitute good.', 'Income of the consumer.',
              'The consumer’s tastes / preference', 'Expectations concerning future prices', 'Government regulations.', 'Unplanned factors.']),
     4, 5, 'Four factors, 5 marks each (2 to state it, 3 to explain it).', **B)
q3b = H.q(6, 'The diagram below represents the market demand and market supply for sugar beet.', ' P 1 2 Q')
q3b_fig = PAP + 'p06-q3b-diagram'
add('sb-q3-b-i', '1-0', 'lines-of-the-sugar-beet-market', ref('B', 3, '(b)(i)'),
    f"{H.q(6, 'Copy the diagram into your answerbook.', ' (i)')} {H.q(6, 'Label each of the lines numbered 1 and 2.', ' (ii)')}",
    '2 @ 3', 6,
    [point(f'r-{n}', f'{n} — {H.traced(name)}', 3, f'Line {n}, 3 marks.') for n, name in (('1', 'SUPPLY'), ('2', 'DEMAND'))],
    stem=q3b, figure=q3b_fig, **B)
add('sb-q3-b-ii', '1-0', 'equilibrium-in-the-sugar-beet-market', ref('B', 3, '(b)(ii)'),
    H.q(6, 'Show on your diagram: • The market equilibrium price (P1)', ' (iii)'), '3 + 3', 6,
    [point('r-price', f"{H.traced('The market equilibrium price (P1) charged for sugar beet;')} — {H.traced('P1')}", 3,
           'The equilibrium price, ' + H.traced('3 marks') + '.'),
     point('r-quantity', f"{H.traced('The market equilibrium quantity (Q1) sold on the market.')} — {H.traced('Q1')}", 3,
           'The equilibrium quantity, 3 marks: P1 and Q1 read off where the demand line crosses supply line 1, as the scheme’s '
           'diagram shows.')],
    stem=q3b, figure=SOL + 'p16-q3b-diagram', **B)
beside_ask(cards[-1], q3b_fig)
add('sb-q3-b-iii', '1-2', 'a-subsidy-for-sugar-beet', ref('B', 3, '(b)(iii)'),
    H.q(6, 'If the sugar beet producers received a subsidy', ' (30 marks)'), '6 + 8 + 2 + 2', 18,
    [point('r-curve', H.traced('New Labelled Supply Curve.'), 6,
           'The new supply curve, labelled, ' + H.traced('6 marks ( 3 marks + 3 marks)') + ': drawn to the right of the old one, as '
           'the scheme’s diagram shows.'),
     point('r-why', H.traced('This subsidy would lower the costs of production for suppliers and so increase supply'), 8,
           'The explanation, 8 marks.'),
     point('r-p2', H.traced('New lower P2.'), 2, 'The new price, 2 marks.'),
     point('r-q2', H.traced('New higher quantity supplied, Q2.'), 2, 'The new quantity, 2 marks.')],
    kind='fixed', stem=q3b, figure=SOL + 'p16-q3b-diagram', **B)
beside_ask(cards[-1], q3b_fig)
q3c = H.q(6, 'Suppose the Price Elasticity of Demand (PED) for two goods was as follows:', ' (i)')
add('sb-q3-c-i', '1-4', 'the-greater-fall-in-demand', ref('B', 3, '(c)(i)'),
    H.q(6, 'Which good will experience the greatest fall in quantity demanded?', ' (ii)'), '8 + 2 + 2', 12,
    [point('r-answer', H.traced('iPhones will experience the biggest fall in quantity demanded.'), 8, 'The answer, 8 marks.'),
     point('r-iphone', H.traced('iPhone: Qd will fall by 3.8 x 10 = 38%'), 2,
           'The iPhone’s fall, 2 marks: the scheme prints 2 marks beneath each half of its explanation.'),
     point('r-petrol', H.traced('while the demand for petrol will only fall by 0.5 x 10 = 5%'), 2, 'Petrol’s fall, 2 marks.')],
    kind='fixed', stem=q3c, **B)
add('sb-q3-c-ii', '1-4', 'a-luxury-and-a-necessity', ref('B', 3, '(c)(ii)'),
    H.q(6, 'Which good would you consider a ‘luxury’ good', ' (25 marks)'), '8 + 5', 13,
    [ladder('r-1', 'Each good classed, with why — the iPhone and petrol', 13,
            side('iPhone', bullets_of(cc('• Luxury goods tend to be price elastic'))) + side('Petrol', bullets_of(cc('• Necessities tend to be'))),
            [8, 5], 'One answer for each good, one per group: the iPhone (the first two options) and petrol (the last two). '
            + H.traced('First correct answer: 8 marks. State 6 marks. Explain 2 marks.') + ' '
            + H.traced('Second correct answer: 5 marks. State 3 marks. Explain 2 marks.'))],
    kind='fixed', stem=q3c, **B)

# Q4 ─ the circular flow; national income; emigration and immigration
q4a = H.q(7, 'The diagram below represents the Circular Flow of Income in an open economy without Government.', ' (i)')
q4a_fig = PAP + 'p07-q4a-diagram'
lines4 = (('1', 'Payment / for factors of production', H.traced('3 marks: 2 marks + 1 mark (wages)')),
          ('2', 'Supply /commodities or goods & services', H.traced('3 marks: 2 marks + 1 mark')), ('3', 'Imports', '3 marks'),
          ('4', 'Exports', '3 marks'))
add('sb-q4-a-i', '3-0', 'lines-of-the-open-circular-flow', ref('B', 4, '(a)(i)'),
    H.q(7, 'State clearly what each of the lines numbered 1 to 4 represents.', ' (ii)'), '4 @ 3', 12,
    [point(f'r-{n}', f'{n} — {cc(r, whole=True)}', 3, f'Line {n}, {m}.') for n, r, m in lines4],
    stem=q4a, figure=q4a_fig, **B)
add('sb-q4-a-ii', '3-0', 'activities-around-the-open-flow', ref('B', 4, '(a)(ii)'),
    H.q(7, 'Referring to the diagram above, explain briefly the types of activities', ' (25 marks)'), '5 + 4 + 4', 13,
    [heading('r-households-firms', H.traced('Households and firms') + ' — either',
             [H.traced('Households: supply factors of production / labour (to firms) and in return receive an income.'),
              H.traced('Firms: supply commodities (goods & services) to households, who spend their income on these.')], 5,
             'Households and firms, 5 marks: the scheme accepts either.'),
     point('r-imports', f"{H.traced('Households and foreign markets')} — "
           f"{H.traced('Households: spend part of their income buying imports (from foreign markets).')}", 4,
           'Households and foreign markets, 4 marks.'),
     point('r-exports', f"{H.traced('Firms and foreign markets')} — "
           f"{H.traced('Firms export some of their goods (to foreign markets) and receive income for these.')}", 4,
           'Firms and foreign markets, 4 marks.')],
    kind='fixed', stem=q4a, figure=q4a_fig, **B)
q4b = H.q(7, 'Given: National Income as Y = C + I + G + (X - M).', ' (i)')
add('sb-q4-b-i', '3-0', 'national-income-with-trade', ref('B', 4, '(b)(i)'),
    H.q(7, 'If National Income, without imports and exports, is €1,500m', ' (ii)'), '10 + 2', 12,
    [point('r-working', H.traced('€1,500m + €70m - €100m'), 10,
           'The working, 10 marks: ' + H.traced('Each correct underlined component 2 mark = 10 marks.') + ' The scheme underlines five: '
           '€1,500m, the plus, €70m, the minus and €100m. The working is shown with the answer.'),
     point('r-answer', H.traced('€1,470m'), 2, 'The answer, 2 marks.')],
    kind='fixed', stem=q4b, figure=SOL + 'p19-q4bi-working', **B)
add('sb-q4-b-ii', '3-0', 'the-multiplier-by-example', ref('B', 4, '(b)(ii)'),
    H.q(7, 'The economist John Maynard Keynes developed the concept of the Multiplier', ' (20 marks)'), '8', 8,
    [point('r-1', H.traced('If the multiplier for an economy is 2 and there in an injection of €10m into the economy then national income '
                           'will increase by €20m.'), 8, 'The multiplier explained by an example, 8 marks.')],
    **B)
q4c = H.q(7, 'There is more emigration than immigration in Ireland at present.', ' (i)')
emig, immig = H.traced('Emigration'), H.traced('Immigration')
add('sb-q4-c-i', '3-2', 'emigration-and-immigration', ref('B', 4, '(c)(i)'),
    H.q(7, 'Explain the two underlined terms.', ' (ii)'), '3 + 2 + 3 + 2', 10,
    [point('r-emig-who', f"{emig} — {H.traced('Movement of Irish nationals')}", 3,
           'Emigration, the movement of Irish nationals, 3 marks: the scheme prints ( 3 ) and ( 2 ) beside the two halves of each '
           'explanation, ' + H.traced('5 marks') + ' for each term.'),
     point('r-emig-where', f"{emig} — {H.traced('to reside elsewhere')}", 2, 'Emigration, to reside elsewhere, 2 marks.'),
     point('r-immig-who', f"{immig} — {H.traced('Movement of foreign nationals')}", 3, 'Immigration, the movement of foreign nationals, 3 marks.'),
     point('r-immig-where', f"{immig} — {H.traced('to reside in Ireland')}", 2, 'Immigration, to reside in Ireland, 2 marks.')],
    stem=q4c, **B)
pick('sb-q4-c-ii', '3-2', 'why-emigration-exceeds-immigration', ref('B', 4, '(c)(ii)'),
     H.q(7, 'State and explain two reasons for the above situation.', ' (iii)'), 'A reason — any two',
     H.split('1. Economic recession in Ireland.', '2 reasons at 5 marks each.',
             ['Economic recession in Ireland.', 'Wage rates in Ireland.', 'Prospects for economic recovery are poor.',
              'Foreign nationals returning to their home countries.', 'Job opportunities abroad.', 'Rising levels of taxation in Ireland.']),
     2, 5, 'Two reasons, 5 marks each (2 to state it, 3 to explain it).', stem=q4c, **B)
labour = paired(['Decreases in size', 'Increased dependency ratio', 'Labour shortages may develop', 'Loss of skills'],
                cc('• With increasing emigration the size'), [(0, 0), (1, None), (2, 1), (3, None)])
add('sb-q4-c-iii', '3-2', 'emigration-labour-and-state-services', ref('B', 4, '(c)(iii)'),
    H.q(7, 'State and explain the possible economic effects which increased emigration', ' (30 marks)'), '2 x 5 (2 + 3)', 10,
    [heading('r-labour', H.traced('Irish Labour market') + ' — any one', labour, 5,
             'One effect on the Irish labour market, 5 marks (2 to state it, 3 to explain it): the scheme prints '
             + H.traced('2 x 5 marks') + ', ' + H.traced('2 x 2 marks each') + ' beneath its statements and ' + H.traced('2 x 3 marks each')
             + ' beneath its explanations. It prints four statements beside two explanations; each explanation is paired with the '
             'statement it restates, and the other two statements stand alone.'),
     point('r-services', f"{H.traced('Demand for State services')} — {H.traced('May decrease.')} — "
           f"{bullets_of(cc('• With less people living in Ireland'))[0]}", 5,
           'The effect on the demand for State services, 5 marks (2 + 3): the scheme gives one.')],
    kind='fixed', stem=q4c, **B)

# Q5 ─ taxation terms; the canons of taxation; three budget proposals
terms5 = ([f"{H.traced('Direct tax')} — {x}" for x in bullets_of(cc('• a tax on incomes'))]
          + [f"{H.traced('Government Capital Spending')} — {x}" for x in bullets_of(cc('• any outlay by government'))]
          + [f"{H.traced('National debt')} — {x}" for x in bullets_of(cc('• this is the total amount of government borrowing'))])
add('sb-q5-a', '3-1', 'direct-tax-capital-spending-and-the-national-debt', ref('B', 5, '(a)(i)–(iii)'),
    H.q(8, 'Explain the following terms: (i) Direct tax;', ' (20 marks)'), '7 + 7 + 6', 20,
    [ladder('r-1', 'Each term explained — one for each', 20, terms5, [7, 7, 6],
            'One explanation for each term, one per term: the scheme prints ' + H.traced('(7 marks +7 marks +6 marks)') + ' beneath its '
            'table without saying which term earns which, claimed here as the first two correct answers 7 each and the 3rd 6. The '
            'scheme gives two explanations of a direct tax.')],
    kind='fixed', **B)
q5b = H.q(8, 'The economist Adam Smith developed the following Canons of Taxation', ' (i)')
canon_note = H.traced('4 at 5 marks each per correct explanation')
add('sb-q5-b-i', '3-1', 'explaining-the-canons-of-taxation', ref('B', 5, '(b)(i)'),
    H.q(8, 'Explain each of the above canons of taxation.', ' (ii)'), '4 @ 5', 20,
    [heading('r-equity', 'Equity — either',
             [H.traced('The ability of each person to pay the tax must be taken into account'),
              H.traced('Takes a higher proportion of income in tax as income rises')], 5,
             'Equity, 5 marks: the scheme accepts either (' + canon_note + ').'),
     heading('r-economy', 'Economy — either',
             [H.traced('the revenue collected should exceed the costs of collection'),
              H.traced('the costs of assessment and collection should be as low as possible.')], 5,
             'Economy, 5 marks: either.'),
     point('r-certainty', H.traced('the taxpayer/collector should know how much tax to pay / is to be collected'), 5, 'Certainty, 5 marks.'),
     heading('r-convenience', 'Convenience — either',
             [H.traced('the tax should be collected in a way / manner which is convenient to the taxpayer.'),
              H.traced('the tax should be collected at a time which is convenient to the taxpayer.')], 5,
             'Convenience, 5 marks: either.')],
    kind='fixed', stem=q5b, **B)
pick('sb-q5-b-ii', '3-1', 'a-further-principle-of-taxation', ref('B', 5, '(b)(ii)'),
     H.q(8, 'In addition to these canons discuss one further principle', ' (25 marks)'), 'A principle — any one',
     [se(x) for x in ('Redistribution', 'Evasion', 'Incentive to work/save', 'Brain drain.')],
     1, 5, 'One principle, 5 marks.', stem=q5b, **B)
q5c = H.q(8, 'Discuss the possible economic effects which the following proposals', ' (i)')
for part, topic, concept, item, nxt, cell, name in (
        ('i', '1-3', 'effects-of-third-level-fees', 'Introduction of third level college fees', ';', '• Current expenditure by government will decrease',
         'third level college fees'),
        ('ii', '3-1', 'effects-of-a-later-retirement-age', 'Increase in the statutory retirement age from 65 to 68 years', ';',
         '• Government finances should improve', 'the later retirement age'),
        ('iii', '3-1', 'effects-of-a-household-property-tax', 'Introduction of a household property tax', '.', '• This should lead to an increase',
         'a household property tax')):
    pick(f'sb-q5-c-{part}', topic, concept, ref('B', 5, f'(c)({part})'), f'{q5c} {H.q(8, item, nxt)}', 'An effect — any two',
         bullets_of(cc(cell)), 2, 5,
         f'Two effects of {name}, 5 marks each: the scheme prints ' + H.traced('3 x 10 marks each: 2 distinct points at 5 marks each.')[:-1] + '.',
         **B)

# Q6 ─ money terms; commercial banks; the ECB and the Central Bank
terms6 = ([f"{H.traced('Barter')} — {x}" for x in bullets_of(cc('• Swapping of one item for another.'))]
          + [f"{H.traced('Interest rate')} — {x}" for x in bullets_of(cc('• the price of money'))]
          + [f"{H.traced('Creditworthy customer')} — {x}" for x in bullets_of(cc('• able to repay loans'))])
add('sb-q6-a', '3-4', 'barter-interest-and-creditworthiness', ref('B', 6, '(a)(i)–(iii)'),
    H.q(8, 'Explain the following terms: (i) Barter;', ' (20 marks)'), '7 + 7 + 6', 20,
    [ladder('r-1', 'Each term explained — one for each', 20, terms6, [7, 7, 6],
            'One explanation for each term, one per term: the scheme prints ' + H.traced('(7 marks +7 marks + 6 marks)') + ' beneath its '
            'table without saying which term earns which, claimed here as the first two correct answers 7 each and the 3rd 6. The '
            'scheme gives two explanations of a creditworthy customer.')],
    kind='fixed', **B)
misprint = 'The paper prints this part as “({p})” by misprint; the scheme numbers it ({s}).'
pick('sb-q6-b-i', '3-4', 'commercial-banks-in-ireland', ref('B', 6, '(b)(i)'),
     H.q(8, 'Name two commercial banks operating in Ireland.', ' (i) Discuss'), 'A commercial bank — any two',
     [H.traced(x) for x in ('Allied Irish Banks', 'Bank of Ireland', 'Permanent TSB', 'Ulster Bank')],
     2, 3, 'Two banks, ' + H.traced('3 marks each') + '.', **B)
pick('sb-q6-b-ii', '3-4', 'functions-of-commercial-banks', ref('B', 6, '(b)(ii)'),
     H.q(8, 'Discuss two main functions of commercial banks.', ' (ii)'), 'A function — any two',
     H.split('Savings Facilities\n', '2 functions at 5 marks each.',
             ['Savings Facilities', 'Lending', 'Operate cheque system/current accounts', '24 Hour Banking',
              'Computerised Transfer of Money/Automated Bill Payment', 'Foreign Exchange']),
     2, 5, 'Two functions, 5 marks each (3 to state it, 2 to explain it). ' + misprint.format(p='i', s='ii'), **B)
pick('sb-q6-b-iii', '3-4', 'why-regulate-commercial-banks', ref('B', 6, '(b)(iii)'),
     H.q(8, 'Outline one economic reason why commercial banks should be regulated.', ' (20 marks)'), 'A reason — any one',
     H.split('Protect consumers.\n', '1 reason x 4 marks.',
             ['Protect consumers.', 'Proper lending policies.', 'Banking system stability.', 'Economic stability / confidence.',
              'Less need for government intervention.']),
     1, 4, 'One reason, 4 marks (2 to state it, 2 to explain it). ' + misprint.format(p='ii', s='iii'), **B)
q6c = H.q(8, 'The ECB decides the main interest rate within the euro zone.', ' (i)')
add('sb-q6-c-i', '3-3', 'ecb-in-full', ref('B', 6, '(c)(i)'), H.q(8, 'What do the initials ECB represent?', ' (ii)'), '10', 10,
    [point('r-1', H.traced('European Central Bank'), 10, 'The name, 10 marks.')], stem=q6c, **B)
borrowers = [f"{H.traced('Higher cost of borrowing')} — {x}" for x in bullets_of(cc('• The cost of borrowing would increase'))]
savers = [f"{H.traced('Higher returns')} — {x}" for x in bullets_of(cc('• Savers would earn a higher rate of return'))]
economy = paired(['National Debt.', 'Economic growth.', 'Demand for wage increases.'], cc('• Cost of repaying interest on the National debt'),
                 [(0, 0), (None, 1), (2, 2), (None, 3)])
add('sb-q6-c-ii', '3-3', 'effects-of-higher-ecb-rates', ref('B', 6, '(c)(ii)'),
    H.q(8, 'If the ECB was to increase interest rates, state and explain the effects', ' (iii)'), '3 x 5 (3 + 2)', 15,
    [heading('r-borrowers', H.traced('Borrowers') + ' — any one', borrowers, 5,
             'One effect on borrowers, 5 marks (3 to state it, 2 to explain it).'),
     heading('r-savers', H.traced('Savers') + ' — any one', savers, 5, 'One effect on savers, 5 marks (3 + 2).'),
     heading('r-economy', H.traced('Irish Economy') + ' — any one', economy, 5,
             'One effect on the Irish economy, 5 marks (3 + 2). The scheme prints three statements (the national debt, economic growth '
             'and demand for wage increases) beside four explanations: the first and third explanations restate the national debt and '
             'wage demands and are set beside them, and the other two stand alone.')],
    kind='fixed', stem=q6c, **B)
pick('sb-q6-c-iii', '3-4', 'functions-of-the-central-bank', ref('B', 6, '(c)(iii)'),
     H.q(8, 'State and explain two functions of the Central Bank of Ireland.', ' (35 marks)'), 'A function — any two',
     lettered('(a) Prints / Issues legal tender.', '2 at 5 marks each.', 'abcdefgh'),
     2, 5, 'Two functions, 5 marks each (3 to state it, 2 to explain it).', stem=q6c, **B)

# Q7 ─ deflation; savings; smuggling and the black economy
q7 = H.q(9, 'Consumer prices fell at an annual rate of 6.6% in October 2009', ' (a)')
add('sb-q7-a-i', '3-0', 'cso-in-full', ref('B', 7, '(a)(i)'), H.q(9, 'What do the initials CSO represent?', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Central Statistics Office'), 6, 'The name, 6 marks.')], stem=q7, **B)
add('sb-q7-a-ii', '3-3', 'falling-consumer-prices', ref('B', 7, '(a)(ii)'),
    H.q(9, 'State the economic term used for the situation underlined above.', ' (iii)'), '4', 4,
    [point('r-1', H.traced('Deflation'), 4, 'The term, 4 marks.')], stem=q7, **B)
welfare = paired(['Lower cost of living', 'Improved standard of living'], cc('• The cost of living would decrease with lower prices.'),
                 [(0, 0), (1, 1), (None, 2)])
savers7 = paired(['Increased rate of return', 'Increased savings'], cc('• Savers would earn a higher real rate of return'), [(0, 0), (1, 1)])
employees = paired(['Increased disposable income/ higher standard of living.', 'Reduced wage demands.', 'Discourage spending'],
                   cc('• Deflation may discourage spending'), [(0, 1), (1, 2), (2, 0), (None, 3)])
add('sb-q7-a-iii', '3-3', 'effects-of-deflation', ref('B', 7, '(a)(iii)'),
    H.q(9, 'Discuss the effects which the above development may have for each of the following:', ' (25 marks)'), '3 x 5 (3 + 2)', 15,
    [heading('r-welfare', H.traced('Social Welfare Recipients') + ' — any one', welfare, 5,
             'One effect on people in receipt of social welfare, 5 marks (3 to state it, 2 to explain it): '
             + H.traced('3 at 5 marks each: 3 marks + 2marks.') + ' Each statement is set beside the explanation that restates it; an '
             'explanation that restates none stands alone.'),
     heading('r-savers', H.traced('Savers') + ' — any one', savers7, 5, 'One effect on savers, 5 marks (3 + 2).'),
     heading('r-employees', H.traced('Employees') + ' — any one', employees, 5, 'One effect on employees, 5 marks (3 + 2).')],
    kind='fixed', stem=q7, **B)
q7b = H.q(9, 'Savings within the Irish economy are increasing.', ' (i)')
add('sb-q7-b-i', '3-4', 'savings', ref('B', 7, '(b)(i)'),
    qn(9, 'Savings within the Irish economy are increasing.', 'Explain the underlined term.', ' (ii)'), '8', 8,
    [point('r-1', H.traced('Savings means not spending part of your income / money'), 8, 'The explanation, 8 marks.')], stem=q7b, **B)
pick('sb-q7-b-ii', '3-4', 'why-savings-are-rising', ref('B', 7, '(b)(ii)'),
     H.q(9, 'Discuss one reason for this development.', ' (iii)'), 'A reason — any one',
     H.split('Consumers behaving cautiously\n', '4 marks. State: 2 marks. Explain: 2 marks.',
             ['Consumers behaving cautiously', 'Lack of confidence in the economy', 'Postponing spending', 'More difficult to get credit']),
     1, 4, 'One reason, 4 marks (2 to state it, 2 to explain it).', stem=q7b, **B)
pick('sb-q7-b-iii', '3-0', 'why-spending-beats-saving-now', ref('B', 7, '(b)(iii)'),
     H.q(9, 'State and explain two possible economic reasons why an increase in consumer spending', ' (20 marks)'), 'A reason — any two',
     H.split('Help create jobs / prevents job losses.', '2 reasons at 4 marks each.',
             ['Help create jobs / prevents job losses.', 'Economic growth / stimulate economic activity.', 'Restore confidence in economy.',
              'Improve Government finances.', 'Investment by entrepreneurs.']),
     2, 4, 'Two reasons, 4 marks each (2 + 2).', stem=q7b, **B)
q7c = H.q(9, 'The smuggling of cigarettes into Ireland is an example of an activity', ' (i)')
add('sb-q7-c-i', '3-0', 'the-black-economy-and-an-example', ref('B', 7, '(c)(i)'),
    H.q(9, 'Explain the underlined term and give one other example of such an activity.', ' (ii)'), '4 + 6', 10,
    [point('r-explanation', H.traced('Activity which takes place which is not recorded and therefore not included in national income accounts.'),
           4, 'The explanation, 4 marks.'),
     heading('r-example', 'Another example — either',
             [H.traced('A teacher giving grinds, without declaring the income for tax purposes.'),
              H.traced('A plumber fixing a washing machine for a cash payment, and not declaring the income for tax purposes.')], 6,
             'One other example, 6 marks: the scheme gives two.')],
    kind='fixed', stem=q7c, **B)
pick('sb-q7-c-ii', '3-0', 'why-cigarettes-are-smuggled', ref('B', 7, '(c)(ii)'),
     H.q(9, 'State and explain two possible reasons for smuggling activity.', ' (iii)'), 'A reason — any two',
     H.split('High price of cigarettes in Ireland', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['High price of cigarettes', 'Inadequate security measures.', 'Ease of movement within the EU.', 'Inadequate penalties',
              'Illegal goods.', 'Market demand exists.']),
     2, 5, 'Two reasons, 5 marks each (3 to state it, 2 to explain it).', stem=q7c, **B)
pick('sb-q7-c-iii', '3-0', 'effects-of-cigarette-smuggling', ref('B', 7, '(c)(iii)'),
     H.q(9, 'Discuss two economic effects of this development for the Irish economy.', ' (30 marks)'), 'An effect — any two',
     H.split('Opportunity Costs.\n', '2 at 5 marks each. State: 3 marks. Explain: 2 marks.',
             ['Opportunity Costs.', 'Increased health care costs.', 'Decline in legitimate business activity.', 'Increased government expenditure.',
              'Loss of tax revenues.', 'Increase crime levels.', 'Standards of products']),
     2, 5, 'Two effects, 5 marks each (3 + 2).', stem=q7c, **B)

# Q8 ─ the open economy and exports; invisible imports; the euro against sterling
q8 = H.q(9, 'The Irish economy is an open economy which relies on exports', ' (a)')
add('sb-q8-a-i', '4-2', 'an-open-economy-and-economic-growth', ref('B', 8, '(a)(i)'),
    H.q(9, 'Explain each of the underlined terms.', ' (ii)'), '5 + 2', 7,
    [point('r-open', H.opt('Open economy: an economy which engages', ' 5 marks'), 5, 'An open economy, 5 marks.'),
     point('r-growth', H.traced('Economic Growth: an increase in GNP per head.'), 2, 'Economic growth, 2 marks.')],
    stem=q8, **B)
add('sb-q8-a-ii', '4-2', 'why-exports-matter', ref('B', 8, '(a)(ii)'),
    H.q(9, 'State and explain three reasons why exports are so important for the Irish economy.', ' (25 marks)'), '10 + 4 + 4', 18,
    [ladder('r-1', 'A reason — any three', 18,
            H.split('1. Job creation.', '18 marks: 1st Correct 10 marks',
                    ['Job creation.', 'Increased GNP / Economic growth', 'Increased sales / profits.', 'Earn foreign currencies.',
                     'Attract investment.']),
            [10, 4, 4], 'Three reasons: ' + H.traced('18 marks: 1st Correct 10 marks; 2nd /3rd points at 4 marks') + '.')],
    kind='fixed', stem=q8, **B)
q8b = H.q(9, 'Spending by Irish people attending sporting events abroad', ' (i)')
add('sb-q8-b-i', '4-2', 'invisible-imports', ref('B', 8, '(b)(i)'),
    qn(9, 'would be an example of an invisible import.', 'Explain the underlined term.', ' (ii)'), '5 + 2', 7,
    [point('r-1', H.traced('The purchase of foreign services'), 5,
           'The purchase of foreign services, 5 marks: the scheme prints ' + H.traced('7 marks') + ' above its sentence, and 5 marks and '
           '2 marks beneath its two halves, read here in that order.'),
     point('r-2', H.traced('by Irish consumers.'), 2, 'By Irish consumers, 2 marks.')],
    stem=q8b, **B)
pick('sb-q8-b-ii', '4-2', 'other-invisible-imports', ref('B', 8, '(b)(ii)'),
     H.q(9, 'State two other examples of invisible imports.', ' (iii)'), 'An example — any two',
     [H.traced(x) for x in ('Irish people using foreign financial services.', 'Foreign rock bands performing in Ireland.',
                            'Ryanair using maintenance crews in countries outside Ireland.')],
     2, 3, 'Two examples, 3 marks each: ' + H.traced('3 marks + 3 marks each') + '.', stem=q8b, **B)
add('sb-q8-b-iii', '4-2', 'why-restrict-imports', ref('B', 8, '(b)(iii)'),
    H.q(9, 'State and explain two reasons why some governments wish to restrict imports.', ' (25 marks)'), '8 + 4', 12,
    [ladder('r-1', 'A reason — any two', 12,
            H.split('Protect domestic industries.\nNew', '1st correct 8 marks;',
                    ['Protect domestic industries.', 'Protect domestic employment.', 'Protect against ‘Cheap Labour’ economies.',
                     'National Security.', 'To protect human rights.', 'Production of strategic goods.', 'To prevent dumping.',
                     'Protect the Balance of Payments']),
            [8, 4], 'Two reasons: ' + H.traced('1st correct 8 marks; 2nd correct 4 marks.'))],
    kind='fixed', stem=q8b, **B)
exporters = paired(['Exports dearer', 'Reduced demand/sales', 'Reduced sales revenue'], cc('• The prices of Irish exports in pound sterling'),
                   [(0, 0), (1, 1), (2, 2), (None, 3)])
imports8 = paired(['Imports cheaper', 'Increased imports', 'Decreased inflation'], cc('• The prices of UK imports in euro'),
                  [(0, 0), (1, 1), (2, 2), (None, 3)])
jobs = paired(['Decreases'], cc('• With fewer exports to the UK'), [(0, 0), (None, 1)])
add('sb-q8-c', '4-2', 'a-dearer-euro-against-sterling', ref('B', 8, '(c)(i)–(iii)'),
    f"{H.q(9, 'Discuss the economic effects of the above development on each of the following:', ' (i)')} "
    f"{H.q(9, '(i) Irish firms exporting to the UK;', ' (25 marks)')}", '11 + 7 + 7', 25,
    [ladder('r-1', 'One effect for each — exporters, imports, employment', 25,
            exporters + imports8 + jobs,
            [11, 7, 7], 'One effect for each of (i), (ii) and (iii), one per group: '
            + H.traced('1st correct answer: 11 marks. State: 6 marks. Explain: 5 marks.') + ' '
            + H.traced('2nd & 3rd correct answers: 2 x 7 marks each. State: 4 marks. Explain: 3 marks.') + ' The scheme lists four effects '
            'on Irish firms exporting to the UK, then four on Irish imports from the UK, then two on employment within Ireland, in that '
            'order here. Each statement is set beside the explanation that restates it; an explanation that restates none stands alone.')],
    kind='fixed', stem=H.q(9, 'During 2009 the euro (€) increased in value relative to the UK pound sterling (£).', ' Discuss'), **B)

# A short ask the paper prints for several parts ("Explain the underlined term.") would
# read the same on every card, and the deck refuses two cards asking one question: each
# carries its stem in its question instead, as 2013 OL does.
_asked = [' '.join(c['questionText'].split()).lower() for c in cards]
for c in cards:
    if _asked.count(' '.join(c['questionText'].split()).lower()) > 1 and c.get('stem'):
        c['questionText'], c['stem'] = f"{c['stem']} {c['questionText']}", ''

if __name__ == '__main__':
    emit(cards)
