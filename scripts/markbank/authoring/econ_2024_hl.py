#!/usr/bin/env python3
"""Economics 2024 Higher Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2024-hl-ev.json,
made from a visual sweep of all 40 paper pages and 52 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID), and
the 83 routes are the ones the 2024 Higher Irish review mirrors task for task,
so the Irish attachment is unchanged.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). The only prose written
here is guidance: tariffs, route labels and what a figure or a calculation
shows. Scheme PDF page = printed page.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, bullets, emit, heads, point, tidy  # noqa: E402

H = Sheet(2024, 'higher', 'LC034ALP000EV')
D = Deck(2024, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2024-HL-scheme-'
PAP = 'economics-2024-HL-paper-'


def key(s):
    return re.sub(r'\s+', '', s)


def at(start, end, firsts, occ=None):
    """The scheme's responses between two anchors, split where each one begins.

    For responses the PDF does not open with a bold heading followed by a dash
    (plain paragraphs, or a bold heading ending in a colon), the first words of
    each response are named and the text is sliced from the scheme at them.
    """
    return [as_option(o) for o in heads(H.chunk(start, end, occ), firsts)]


def lines_menu(start, end, pages, drop=(), occ=None):
    """Responses whose bold heading sits on its own line (no dash after it)."""
    raw = H.chunk(start, end, occ)
    hs = [h for h in H.bold_heads(pages) if len(key(h)) >= 6]
    out, current = [], None
    for line in raw.split('\n')[1:]:
        text = line.strip()
        if not text or '| P a g e' in text:
            continue
        k = key(text)
        hit = next((h for h in hs if k.startswith(key(h)) or
                    (key(h).startswith(k) and len(k) >= 12)), None)
        if hit and any(key(d) == key(hit) or key(d) == k for d in drop):
            current = None
            continue
        if hit:
            current = [text]
            out.append(current)
        elif current is not None:
            current.append(text)
    return [tidy(' '.join(o)) for o in out]


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, note):
    """A required heading inside a jointly priced answer (1 @ 6 then 1 @ 4).

    One unpriced point carrying the heading's examples: a per-option price here
    would print "n marks each" for a share the scheme never fixes.
    """
    return point(rid, paras(options), None, f'{label}. {note}')


def stance(prefix, choices, topic, concept, q, parts, qtext, per, *, sa=False, stem='', figure=''):
    """A printed tick-box choice whose scheme credits each side: one card per side."""
    for suffix, word, label, options in choices:
        pick(f'{prefix}-{suffix}', topic, concept, ref(q, parts, word, sa),
             f'{qtext} Answer for: {word.upper()}.', label, options, 1, per,
             f'One developed justification for the {word} choice, {per} marks. The scheme credits '
             f'both choices; these are its examples, not a closed list.',
             stem=stem, section='A' if sa else 'B', figure=figure)


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1 @ 6, 1 @ 4)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ CSO balance of payments infographic
q1_stem = H.ask(3, 'The adapted infographic below displays', ' (a)')
add('seca-q1-a', '4-2', 'calculating-the-current-account-balance', ref(1, '(a)', sa=True),
    H.ask(3, 'From the data above, calculate the balance of payments', ' Workings:'), '6', 6,
    [point('r-answer', H.run('€76bn + €91bn = €167bn', '(b) Outline one advantage of having a surplus'), 6,
           'Credits: goods exports €76bn + services exports €91bn = €167bn. Debits: goods imports €38bn '
           '+ services imports €83bn = €121bn. Balance €167bn − €121bn = €46bn, a SURPLUS. The scheme '
           'gives one 6 for the workings and the verdict, with no published split.')],
    stem=q1_stem, figure=PAP + 'p03-i0', **A)
pick('sa-q1-b', '4-2', 'advantages-of-a-payments-surplus', ref(1, '(b)', sa=True),
     H.ask(3, 'Outline one advantage of having a surplus on the balance of payments.', ' Leaving'),
     'An advantage of a surplus — any one',
     H.menu('(b) Outline one advantage of having a surplus on the balance of payments.', '5 | P a g e', [5]),
     1, 6, 'One developed advantage, 6 marks. The scheme’s “injection” example says the multiplier is '
     'increased in size: an injection raises national income through the multiplier; it does not '
     'change the multiplier’s value.', **A)

# Q2 ─ full employment
q2_stem = H.ask(4, 'According to Central Statistics Office (CSO) data', ' (a)')
add('sa-q2-a', '3-2', 'what-full-employment-is', ref(2, '(a)', sa=True),
    H.ask(4, 'Explain what you understand by the term full employment.', ' Full employment:'), '6', 6,
    [point('r-1', H.run('Full employment is a situation when everyone in the labour force', 'Answer either (b) or (c)'), 6,
           'Explain the term, 6 marks: everyone in the labour force willing and able to work is employed '
           'at existing wage rates; in Ireland an unemployment rate of about 4% to 5%.')],
    stem=q2_stem, **A)
pick('sa-q2-b', '3-2', 'why-full-employment-is-an-aim', ref(2, '(b)', sa=True),
     H.ask(4, 'Explain, giving two reasons, why full employment is an economic aim', ' 1. 2.'),
     'A reason full employment is an aim — any two',
     at('(b) Explain, giving two reasons, why full employment is an economic aim', 'OR\n(c) The achievement',
        ['Increased direct/indirect tax revenue', 'Decreased social welfare payments',
         'Boosts demand / economic growth', 'Reduction in poverty']),
     2, 3, 'Two reasons, 3 marks each. Answer either (b) or (c).', stem=q2_stem, **A)
pick('sa-q2-c', '3-1', 'conflicting-economic-aims', ref(2, '(c)', sa=True),
     H.ask(4, 'Explain how any other two current economic aims', ' 1. 2.'),
     'An aim that conflicts with full employment — any two',
     H.menu('(c) The achievement of full employment is an economic aim', '6 | P a g e', [6]),
     2, 3, 'Two conflicts, 3 marks each: name the other aim and explain how it clashes with full '
           'employment. Answer either (b) or (c).',
     stem=H.ask(4, 'The achievement of full employment is an economic aim of the government.', ' Explain how'), **A)

# Q3 ─ electricity price cap; energy credits
q3_stem = H.ask(5, 'During 2022, the equilibrium megawatt price per hour', ' Adapted from')
add('sa-q3-a', '1-3', 'drawing-a-price-ceiling-and-its-excess-demand', ref(3, '(a)', sa=True),
    H.ask(5, 'Illustrate, on the diagram below, how the European Commission', ' Price MWh'), '6', 6,
    [point('r-diagram', H.run('Price MWh S\nPe', '(b) Explain your understanding of the economic term price ceiling'), 6,
           'Draw the €200 limit as a horizontal line P1 BELOW the equilibrium price Pe (€600). At P1 the '
           'quantity supplied is S1 and the quantity demanded D1; the gap from S1 to D1 is the excess '
           'demand. The official diagram is shown in the figure; the scheme gives one 6 for it.')],
    stem=q3_stem, figure=SOL + 'p07-q3a-diagram', **A)
pick('sa-q3-b', '1-3', 'price-ceiling', ref(3, '(b)', sa=True),
     H.ask(5, 'Explain your understanding of the economic term price ceiling.', ' Price ceiling:'),
     'A point of the explanation — any two',
     at('(b) Explain your understanding of the economic term price ceiling.', 'OR\n(c) In Budget 2024',
        ['A price ceiling is a maximum price', 'This price may be below the equilibrium',
         'A measure put in place to prevent']),
     2, 3, 'Two points, 3 marks each: a legal maximum price, set below the market equilibrium, to '
     'protect consumers from excessive prices. Answer either (b) or (c).', stem=q3_stem, **A)
pick('sa-q3-c', '1-3', 'reasons-for-energy-credits', ref(3, '(c)', sa=True),
     H.ask(5, 'Explain why you think the government introduced this credit.', ' Explanation:'),
     'A reason for the credit — any two',
     H.menu('(c) In Budget 2024 the government announced energy credits', '7 | P a g e', [7]),
     2, 3, 'Two reasons, 3 marks each (the scheme prices the part 2 @ 3). Answer either (b) or (c). '
     'The scheme’s last example places the measure in Budget 2023; the paper’s credit is from Budget 2024.',
     stem=H.ask(5, 'In Budget 2024 the government announced energy credits', ' Explain why'), **A)

# Q4 ─ capital deepening; demand for labour; MEC
add('seca-q4-a-ticks', '1-5', 'capital-deepening-or-widening', ref(4, '(a)', sa=True),
    H.ask(6, 'From the information given above, tick', ' Capital Widening'), '6', 6,
    [point('r-1', H.run('Capital deepening is occurring in this scenario', '(b) Outline two factors'), 6,
           'Tick CAPITAL DEEPENING: machines rise from 5 to 10 while the workforce stays at 5, so capital '
           'per worker rises from 1:1 to 2:1. Widening would add machines AND workers with the ratio '
           'unchanged. The scheme gives one 6 for the tick and the explanation.')],
    stem=H.ask(6, 'The table below shows a firm’s capital to labour ratio', ' 2022'),
    figure=SOL + 'p08-q4a-ticks', **A)
pick('sa-q4-b', '2-1', 'demand-for-labour', ref(4, '(b)', sa=True),
     H.ask(6, 'Outline two factors which may affect an individual company', ' 1. 2.'),
     'A factor affecting the demand for labour — any two',
     H.menu('(b) Outline two factors which may affect an individual company', 'OR\n⟨6⟩', [8]),
     2, 3, 'Two factors, 3 marks each. Answer either (b) or (c).', **A)
add('sa-q4-c', '1-5', 'marginal-efficiency-of-capital', ref(4, '(c)', sa=True),
    H.ask(6, 'Explain the term Marginal Efficiency of Capital (MEC).', ' Explanation:'), '6', 6,
    [point('r-1', H.run('The MEC is the extra profit earned', '8 | P a g e'), 6,
           'Explain the term, 6 marks. Answer either (b) or (c).')], **A)

# Q5 ─ concert-ticket shortage
q5_stem = H.ask(7, 'Harry Styles performed a concert at Slane Castle', ' (a)')
add('sa-q5-a', '1-0', 'why-a-sold-out-concert-shows-a-shortage', ref(5, '(a)', sa=True),
    H.ask(7, 'Using the information above, illustrate with the aid of a fully labelled diagram', ' (b)'), '8', 8,
    [point('r-diagram', '€97.10', 8,
           'Label Price/€ and Quantity. Supply S1 is a VERTICAL line at the 80,000 capacity; demand D1 '
           'slopes down and meets it at the equilibrium price P1. Draw the actual price €97.10 BELOW P1: '
           'at €97.10 the quantity demanded (Qx) exceeds 80,000, and the gap from 80,000 to Qx is the '
           'excess demand. The official diagram is shown in the figure; the scheme gives one 8 for it.')],
    stem=q5_stem, figure=SOL + 'p09-q5a-diagram', **A)
add('sa-q5-b', '1-0', 'explaining-a-ticket-shortage', ref(5, '(b)', sa=True),
    H.ask(7, 'Explain your diagram above.', ' Explanation:'), '4', 4,
    [point('r-1', H.run('The demand for tickets is downward sloping', '9 | P a g e'), 4,
           'Explain the diagram, 4 marks: demand slopes down, supply is fixed at 80,000, and €97.10 is '
           'below the equilibrium price, so there is excess demand.')],
    stem=q5_stem, figure=SOL + 'p09-q5a-diagram', **A)

# Q6 ─ short-run AC and MC
q6a_ask = H.ask(8, 'With the aid of a fully labelled diagram below', ' Explanation:')
add('sa-q6-a-diagram', '1-5', 'draw-short-run-average-and-marginal-cost', ref(6, '(a)', 'diagram', sa=True),
    q6a_ask + ' Draw the diagram.', '5', 5,
    [point('r-diagram', 'Marginal cost Average cost', 5,
           'Label the axes C/P/€ and Q, and the curves Marginal cost and Average cost. MC cuts AC at the '
           'minimum point of AC: MC is below AC while AC falls and above it while AC rises. The official '
           'diagram is shown in the figure; the scheme gives 5 for the diagram.')],
    figure=SOL + 'p10-q6a-cost-curves',
    notes='The diagram (5) and the written explanation (3) are separately priced in the scheme.', **A)
add('sa-q6-a', '1-5', 'marginal-cost-and-average-cost', ref(6, '(a)', 'explanation', sa=True),
    q6a_ask + ' Write the explanation.', '3', 3,
    [point('r-explanation', H.run('If marginal cost is less than average cost', '(b) Explain the shape'), 3,
           'The written explanation, 3 marks: what average cost does while marginal cost is below it, '
           'above it and equal to it.')],
    figure=SOL + 'p10-q6a-cost-curves', **A)
add('sa-q6-b-down', '1-5', 'shape-of-short-run-average-cost', ref(6, '(b)', sa=True),
    H.ask(8, 'Explain the shape of the short run average cost curve', ' Downward sloping part:'), '2 @ 2', 4,
    [heading('r-down', 'Downward sloping part',
             [H.run('Specialisation/division of labour:', 'OR\nGreater spread of fixed costs'),
              H.run('Greater spread of fixed costs:', 'Upward sloping part:')], 2,
             'Complete BOTH headings. The downward-sloping part: either reason, 2 marks.'),
     point('r-up', H.run('The law of diminishing marginal returns', '10 | P a g e'), 2,
           'The upward-sloping part: diminishing marginal returns, 2 marks.')], **A)

# Q7 ─ vaping
q7_stem = H.ask(9, 'The number of teenagers in Ireland who vape', ' Adapted from')
pick('sa-q7-a', '2-2', 'vaping-as-a-market-failure', ref(7, '(a)', sa=True),
     H.ask(9, 'Explain why the purchase of vape products are a form of market failure.', ' Explanation:'),
     'A way of explaining the failure — any one',
     at('(a) Explain why the purchase of vape products are a form of market failure.', '(b) Outline two ways',
        ['The purchase of demerit goods', 'Their consumption causes negative externalities',
         'Vape products are demerit goods as users', 'Their free-market price fails']),
     1, 6, 'One developed explanation, 6 marks.', stem=q7_stem, **A)
pick('sa-q7-b', '1-3', 'intervening-in-the-vaping-market', ref(7, '(b)', sa=True),
     H.ask(9, 'Outline two ways the Irish government could intervene', ' 1. 2.'),
     'A way to intervene — any two',
     H.menu('(b) Outline two ways the Irish government could intervene', '11 | P a g e', [11]),
     2, 3, 'Two ways, 3 marks each.', stem=q7_stem, **A)

# Q8 ─ price discrimination
q8_stem = H.ask(10, 'Price discrimination remains a popular pricing strategy', ' (a)')
add('sa-q8-a', '2-0', 'price-discrimination-definition-and-example', ref(8, '(a)', sa=True),
    H.ask(10, 'Explain, using an example, what you understand by the term price discrimination.',
          ' Price discrimination:'), '4 + 2', 6,
    [point('r-definition', H.run('Price discrimination is when a firm charges', 'Example:'), 4,
           'Explain the term, 4 marks.'),
     anyN('r-example', 'One example of price discrimination', 2, 1, 2,
          bullets(H.chunk('Example:', '(b) Outline two characteristics of consumers'), drop_prefix='Example:'),
          'Give one example, 2 marks; these are the scheme’s examples.')],
    stem=q8_stem, **A)
pick('sa-q8-b', '2-0', 'conditions-for-price-discrimination', ref(8, '(b)', sa=True),
     H.ask(10, 'Outline two characteristics of consumers that permit', ' 1. 2.'),
     'A characteristic of consumers — any two',
     H.menu('(b) Outline two characteristics of consumers', '12 | P a g e', [12]),
     2, 3, 'Two characteristics, 3 marks each.', stem=q8_stem, **A)

# Q9 ─ Coillte woodland; positive externality
q9a_stem = H.ask(11, 'Coillte has pledged to add a further 100,000 hectares', ' Adapted from')
q9a_ask = H.ask(11, 'Outline one opportunity cost of this pledge by Coillte', ' Opportunity cost:')
q9_cost = bullets(H.chunk('Opportunity cost:', 'Social benefit:', occ=0), drop_prefix='Opportunity cost:')
q9_benefit = bullets(H.chunk('Social benefit:', '(b) The Atlantic Technological University', occ=0),
                     drop_prefix='Social benefit:')
add('sa-q9-a-cost', '0-1', 'opportunity-cost-and-social-benefit-of-woodland', ref(9, '(a)', sa=True),
    q9a_ask, '3 + 3', 6,
    [heading('r-cost', 'Opportunity cost', q9_cost, 3, 'Complete BOTH headings. One opportunity cost, 3 marks.'),
     heading('r-benefit', 'Social benefit', q9_benefit, 3, 'One social benefit, 3 marks.')],
    stem=q9a_stem, **A)
pick('sa-q9-b', '2-2', 'positive-externalities', ref(9, '(b)', sa=True),
     H.ask(11, 'Explain what you understand by the term, positive externality.', ' Positive externality:'),
     'A way of explaining the term — any one',
     at('Explain what you understand by the term, positive externality.', '13 | P a g e',
        ['With positive externalities the benefit', 'Goods / services which give a benefit',
         'The existence of ATU will bring']),
     1, 6, 'One developed explanation, 6 marks: the benefit to society exceeds the private benefit, or '
     'a benefit reaches a third party. The ATU line is the scheme’s own illustration.',
     stem=H.ask(11, 'The Atlantic Technological University was launched', ' Explain what'), **A)

# Q10 ─ national accounts ladder; NFIA
q10_stem = H.ask(12, 'The data below has been adapted from Ireland’s National Accounts', ' Description')
add('sa-q10-a-ii', '3-0', 'from-gnp-to-gross-national-income', ref(10, '(a)(ii)', sa=True),
    H.ask(12, 'Given that Gross Domestic Product (GDP) at Current Market Prices', ' Relationships / Workings Answer'),
    '6', 6,
    [point('r-1', H.run('Gross National Product (GNP) at CMP €325bn', '(b) Explain the term net factor income'), 6,
           'GNI = GNP + EU subsidies − EU taxes = €325bn + €2bn − €0.5bn = €326.5bn. Part (i), GDP to GNP, '
           'is completed on the paper; only part (ii) is marked. The official ladder is shown in the figure.')],
    stem=q10_stem, figure=SOL + 'p14-q10aii-working', **A)
add('sa-q10-b', '3-0', 'net-factor-income-from-abroad', ref(10, '(b)', sa=True),
    H.ask(12, 'Explain the term Net factor income from abroad.', ' Explanation:'), '6', 6,
    [point('r-1', H.run('Net factor income is the income earned by Irish factors', '14 | P a g e'), 6,
           'Explain the term, 6 marks: income of Irish factors abroad sent home MINUS income of foreign '
           'factors in Ireland sent abroad.')], **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ tourism; the multiplier; organic ice cream
q11_stem = H.ask(13, 'The chart below shows the number of foreign tourists', ' Number of foreign')
add('q11-a-i', '4-2', 'percentage-increase-in-foreign-tourists', ref(11, '(a)(i)'),
    H.ask(13, 'Calculate the percentage increase in foreign tourists', ' Workings:'), '8', 8,
    [point('r-answer', '94.11% / 94% Increase', 8,
           '(737,600 − 380,000) ÷ 380,000 × 100 = 357,600 ÷ 380,000 × 100 = 94.11% (94% accepted). '
           'Divide by the EARLIER figure. Deduct 1 mark if % is omitted.')],
    stem=q11_stem, figure=PAP + 'p13-i1')
add('q11-a-ii', '3-0', 'tourism-and-the-circular-flow', ref(11, '(a)(ii)'),
    H.ask(13, 'Outline the effect of this increase in tourism', ' (iii)'), '6', 6,
    [point('r-1', H.run('Foreign tourists coming to Ireland are an invisible export', '(iii) Outline one possible disadvantage'), 6,
           'One effect, 6 marks: tourist spending is an invisible export, an injection that increases '
           'the circular flow of income.')],
    stem=q11_stem, figure=PAP + 'p13-i1')
pick('q11-a-iii', '4-2', 'disadvantages-of-tourism', ref(11, '(a)(iii)'),
     H.ask(13, 'Outline one possible disadvantage of increasing tourism numbers', ' Disadvantage:'),
     'A disadvantage of rising tourism — any one',
     H.menu('(iii) Outline one possible disadvantage of increasing tourism numbers', '15 | P a g e', [15]),
     1, 6, 'One developed disadvantage, 6 marks.', stem=q11_stem, figure=PAP + 'p13-i1')
q11b_stem = H.ask(14, 'It has been estimated that in the Irish economy', ' (i)')
q11b_ask = H.ask(14, 'Based on the information stated above and using an appropriate formula', ' Workings:')
add('q11-b-i', '3-0', 'the-multiplier-and-what-it-means', ref(11, '(b)(i)', 'calculation'),
    q11b_ask + ' Do the calculation.', '12', 12,
    [point('r-answer', 'Answer = 1.08', 12,
           'MPS = 1 − 0.6 = 0.4. Multiplier = 1 ÷ (MPT + MPM + MPS) = 1 ÷ (0.22 + 0.3 + 0.4) = 1 ÷ 0.92; '
           'or 1 ÷ (1 − (0.6 − 0.22 − 0.3)) = 1 ÷ 0.92. The scheme prints 1.08; 1 ÷ 0.92 = 1.086956…, '
           'which rounds to 1.09.')],
    stem=q11b_stem,
    notes='The calculation (12) and the economic meaning (4) are separately priced in the scheme.')
add('q11-b-i-meaning', '3-0', 'the-multiplier-and-what-it-means-explanation', ref(11, '(b)(i)', 'meaning'),
    q11b_ask + ' Write the economic meaning.', '4', 4,
    [point('r-meaning', H.run('• In this case if there is an injection of €1', '(ii) Explain briefly how a reduction'), 4,
           'Explain the meaning, 4 marks: an initial €1 injection raises national income by about €1.08 '
           '(1.09 with ordinary rounding).')],
    stem=q11b_stem)
add('q11-b-ii', '3-0', 'income-tax-and-the-multiplier', ref(11, '(b)(ii)'),
    H.ask(14, 'Explain briefly how a reduction in income tax rates', ' Explanation:'), '4', 4,
    [point('r-1', H.run('A reduction in income tax would result in less of a leakage', '16 | P a g e'), 4,
           'Explain, 4 marks: a lower income-tax rate means a smaller leakage (a lower MPT), so spending '
           'rises and the value of the multiplier rises.')])
pick('q11-b-iii', '3-0', 'uses-of-national-income-statistics', ref(11, '(b)(iii)'),
     H.ask(14, 'Outline two uses of the information provided by national income statistics.', ' 1. 2.'),
     'A use of national income statistics — any two',
     H.menu('(iii) Outline two uses of the information provided by national income statistics.', '17 | P a g e', [17]),
     2, 4, 'Two uses, 4 marks each.')
q11c_stem = H.ask(15, 'Assume the market for a brand of Irish organic ice cream', ' (i)')
for part, page, ask_start, cause, sol, concept, start, stop, crit_start, crit_end in [
        ('i', 15, 'A prolonged heatwave during the summer in Ireland.', 'heatwave', 'p18-q11ci-shift',
         'demand-shift-heatwave', '• D/C shifts to the right (D2).', 'Explanation ⟨4⟩',
         'Shift in D/C to the right / Higher P', '18 | P a g e'),
        ('ii', 15, 'An increase in lactose intolerant consumers.', 'lactose', 'p19-q11cii-shift',
         'demand-shift-consumer-tastes', '• D/C shifts to the left (D2).', 'Explanation ⟨4⟩',
         'Shift in D/C to the left / Lower P', '19 | P a g e'),
        ('iii', 16, 'Producers are receiving a subsidy for organic ice cream production.', 'subsidy',
         'p20-q11ciii-shift', 'supply-shift-subsidy', '• S/C shifts to the right (S2).', 'Explanation ⟨4 @ 1⟩',
         'Shift in S/C to the right / Lower P', '20 | P a g e')]:
    part_ask = H.ask(page, ask_start, ' Diagram')
    add(f'q11-c-{part}-diagram', '1-0', concept + '-diagram', ref(11, f'(c)({part})', 'diagram'),
        part_ask + ' Draw the diagram.', '5 @ 1', 5,
        [point('r-diagram', H.run(start, stop), 5,
               'Draw a separate, fully labelled demand and supply diagram: the shifted curve and the new '
               'equilibrium price and quantity, 5 marks at 1 each. These lines are the scheme’s account of '
               'what the diagram shows; the official diagram is in the figure.')],
        stem=q11c_stem, figure=SOL + sol,
        notes='The diagram (5) and the written explanation (4) are separately priced in the scheme.')
    criteria = [o.strip() for o in H.run(crit_start, crit_end).split(' / ')]
    add(f'q11-c-{part}', '1-0', concept, ref(11, f'(c)({part})', 'explanation'),
        part_ask + ' Write the explanation.', '4 @ 1', 4,
        [anyN('r-explanation', 'What the explanation must say — all four', 4, 4, 1, criteria,
              'Explain all four at 1 mark each: the shift and its direction, the price, the quantity and '
              'the cause.')],
        stem=q11c_stem, figure=SOL + sol)

# Q12 ─ taxation; inflation; gambling; consumer behaviour
q12_stem = H.ask(17, 'In 2022, €313m in tax revenues was overpaid', ' Adapted from')
pick('q12-a-i', '3-1', 'canons-of-taxation', ref(12, '(a)(i)'),
     H.ask(17, 'Explain two other canons/principles of taxation.', ' 1. 2.'),
     'A canon of taxation other than certainty — any two',
     at('(i) The principle of certainty is one of the canons of taxation', '21 | P a g e',
        ['Equity:', 'Economy:', 'Convenience:', 'Taxes should not be perceived', 'Taxes should assist',
         'Taxes should be consistent', 'Taxes should have a stabilising', 'Tax evasion should not']),
     2, 5, 'Two canons other than certainty, 5 marks each.',
     stem=q12_stem + ' ' + H.ask(17, 'The principle of certainty is one of the canons of taxation', ' Explain two'))
pick('q12-a-ii', '3-0', 'effects-of-the-hidden-economy', ref(12, '(a)(ii)'),
     H.ask(17, 'Outline two effects on the Irish economy of an increase', ' 1. 2.'),
     'An effect of a growing hidden economy — any two',
     at('Outline two effects on the Irish economy of an increase in activities in the hidden',
        '(iii) A new 30% tax rate',
        ['Loss of tax revenue to the government', 'Decline in legitimate business activity',
         'Increased government expenditure on enforcement', 'Increased crime levels',
         'Standards of products/services', 'Increase in employment in the hidden economy']),
     2, 5, 'Two effects, 5 marks each.',
     stem=H.ask(17, 'Revenue actively challenges all forms of hidden economic activity.', ' Adapted from'))
stance('q12-a-iii', [
    ('tax', 'tax payer', 'A consequence for the tax payer — any one',
     at('Tax payer:', 'Government:',
        ['Increased disposable income', 'Incentive to work', 'More equitable', 'Greater consumer demand',
         'Reduced pressure on wage demands', 'Improved choice for employees'])),
    ('gov', 'government', 'A consequence for the government — any one',
     at('Government:', '23 | P a g e',
        ['Less government revenue from direct taxation', 'More government revenue from indirect taxation',
         'Negative impact on balance of payments', 'Opportunity cost of initiative',
         'Government more reliant on a less stable']))],
    '3-1', 'a-middle-rate-and-the-taxpayer', 12, '(a)(iii)',
    H.ask(17, 'Outline one economic consequence for either the tax payer', ' Tax payer Government'), 4,
    stem=H.ask(17, 'A new 30% tax rate for middle-income earners', ' Adapted from'))
next(c for c in cards if c['id'] == D.prefix + 'q12-a-iii-gov')['conceptId'] = 'a-middle-rate-and-the-exchequer'
q12b_stem = H.ask(18, 'Data from the Consumer Price Index (CPI) all items', ' CPI - all items')
add('q12-b-i', '3-3', 'describing-the-trend-in-cpi-annual-change', ref(12, '(b)(i)'),
    H.ask(18, 'Outline the overall trend of the CPI annual % change', ' Outline:'), '6', 6,
    [point('r-trend', H.run('The overall trend of the CPI between March and October', '(ii) The table below shows'), 6,
           'Describe the trend with figures, 6 marks: the annual rate falls from just under 8% in March to '
           'about 5% in October 2023, a fall of almost 3 percentage points, with a small late-summer rise. '
           'The graph plots the inflation RATE, which falls but stays positive. Prices are still rising.')],
    stem=q12b_stem, figure=PAP + 'p18-art')
add('q12-b-ii', '3-3', 'weighting-simple-price-indices-into-a-composite', ref(12, '(b)(ii)'),
    H.ask(18, 'The table below shows a country’s composite price index', ' % of Price'), '19', 19,
    [point('r-answer', '119.5', 19,
           'Simple index = current price ÷ base price × 100: food 66 ÷ 60 × 100 = 110; transport '
           '45 ÷ 30 × 100 = 150; other items 96 ÷ 80 × 100 = 120. Weighted: 110 × 65% = 71.5; 150 × 20% '
           '= 30.0; 120 × 15% = 18. Price index for the current year = 71.5 + 30.0 + 18 = 119.5. The '
           'official worksheet is shown in the figure; the scheme gives 19 for the whole table, with no '
           'published split.')],
    figure=SOL + 'p24-q12bii-working')
pick('q12-b-iii', '3-3', 'effects-of-high-inflation', ref(12, '(b)(iii)'),
     H.ask(19, 'Outline two possible economic effects of high price inflation', ' 1. 2.'),
     'An effect of high price inflation — any two',
     at('(iii) Outline two possible economic effects of high price inflation', '(c) Up to €10,000',
        ['Loss of purchasing power', 'Those on fixed incomes', 'Possibility of wage demands',
         'Loss of international competitiveness', 'If tax rates are not indexed', 'Borrowers may benefit']),
     2, 3, 'Two effects, 3 marks each.')
q12c_stem = H.ask(19, 'Up to €10,000 a minute is spent in Ireland', ' Adapted from')
add('q12-c-i', '1-3', 'why-regulate-gambling', ref(12, '(c)(i)'),
    H.ask(19, 'Outline two reasons why it is important that the gambling industry', ' 1. 2.'), '4 + 2', 6,
    [steps('r-1', 'A reason to regulate gambling — any two',
           H.menu('(i) Outline two reasons why it is important that the gambling industry', '25 | P a g e', [25]),
           4, 2, 'reasons')],
    stem=q12c_stem)
pick('q12-c-ii', '2-2', 'demerit-goods', ref(12, '(c)(ii)'),
     H.ask(19, 'Cigarettes are classified as demerit goods.', ' Outline:'),
     'An effect of demerit good markets — any one',
     H.menu('(ii) Cigarettes are classified as demerit goods.', '(iii) One assumption of consumer behaviour', [26]),
     1, 4, 'One effect, 4 marks. The scheme lists benefits (employment, tax revenue) as well as harms.')
pick('q12-c-iii', '1-1', 'assumptions-of-consumer-behaviour', ref(12, '(c)(iii)'),
     H.ask(20, 'One assumption of consumer behaviour is that they have limited incomes.', ' 1. 2.'),
     'A key assumption other than limited incomes — any two',
     at('(iii) One assumption of consumer behaviour is that they have limited incomes.', '26 | P a g e',
        ['Consumers seek to get maximum utility', 'Consumers are subject to the law',
         'Most consumers will act rationally']),
     2, 5, 'Two assumptions other than limited incomes, 5 marks each.')

# Q13 ─ Census 2022; Vacant Home Tax; globalisation; corporation tax; budget surplus
q13_stem = H.ask(21, 'The infographic below is from the CSO.', ' (a)')
add('q13-a-i', '3-5', 'net-migration-as-a-share-of-population-change', ref(13, '(a)(i)'),
    H.ask(21, 'Using the data in the table below (extracted from the infographic above)', ' Population 2016'),
    '8', 8,
    [point('r-answer', '52.63%', 8,
           'Net migration ÷ total change × 100 = 190,333 ÷ 361,671 × 100 = 52.63%. Deduct 1 mark if % is '
           'omitted.')],
    stem=q13_stem, figure=PAP + 'p21-i1')
add('q13-a-ii', '3-5', 'consequences-of-a-rising-population', ref(13, '(a)(ii)'),
    H.ask(21, 'Discuss two economic consequences of an increasing population.', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'An economic consequence of a rising population — any two',
           H.menu('(ii) Discuss two economic consequences of an increasing population.',
                  '(iii) The infographic on page 21', [28]), 6, 4, 'consequences')],
    stem=q13_stem, figure=PAP + 'p21-i0')
add('q13-a-iii', '1-3', 'vacant-home-tax', ref(13, '(a)(iii)'),
    H.ask(22, 'The infographic on page 21 also highlights', ' Adapted from'), '6 + 4', 10,
    [steps('r-1', 'An advantage of the Vacant Home Tax — any two',
           H.menu('(iii) The infographic on page 21 also highlights', '28 | P a g e', [28]), 6, 4, 'advantages')],
    figure=PAP + 'p21-i0')
q13b_stem = H.ask(22, 'Globalisation is not dead.', ' Adapted from')
pick('q13-b-i', '4-1', 'what-globalisation-is', ref(13, '(b)(i)'),
     H.ask(22, 'Explain the term globalisation.', ' Globalisation:'),
     'A way of explaining the term — any one',
     at('Explain the term globalisation.', '(ii) Explain two reasons behind the growth',
        ['Globalisation is the process', 'Globalisation is the increasing', 'Globalisation is the ability',
         'Integration between countries']),
     1, 6, 'One developed explanation, 6 marks; the scheme accepts these four formulations.', stem=q13b_stem)
add('q13-b-ii', '4-1', 'growth-of-globalisation', ref(13, '(b)(ii)'),
    H.ask(22, 'Explain two reasons behind the growth of globalisation', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A reason globalisation grew — any two',
           H.menu('(ii) Explain two reasons behind the growth of globalisation', '29 | P a g e', [29]), 6, 4,
           'reasons')],
    stem=q13b_stem)
q13_positive = H.menu('Positive:\n⟨1 @ 4⟩', 'Negative:\nInequality', [30])
q13_negative = lines_menu('Negative:\nInequality', '31 | P a g e', [31], drop=('Negative:',))
add('q13-b-iii-pos', '4-1', 'positive-and-negative-impacts-of-globalisation', ref(13, '(b)(iii)'),
    H.ask(23, 'Outline one positive and one negative impact of globalisation.', ' Positive:'), '10', 10,
    [shared('r-positive', 'One positive impact', q13_positive,
            'Complete BOTH headings. The scheme prices the pair as one 10: the first correct impact 6 '
            'marks and the second 4, with no fixed share for either heading.'),
     shared('r-negative', 'One negative impact', q13_negative, 'One negative impact of globalisation.')],
    kind='questionTotal', stem=q13b_stem)
add('q13-c-i', '3-1', 'why-corporation-tax-receipts-rose', ref(13, '(c)(i)'),
    H.ask(23, 'Outline the overall trend in corporation tax receipts', ' Outline:'), '2 @ 4', 8,
    [point('r-trend', H.run('• Irelands corporation tax receipts have been increasing', 'Explanation:'), 4,
           'Outline the rising trend with data from the graph, 4 marks: €3,520m in 2011 to €22,643m in 2022, '
           'an increase of €19,123m (over 543%). The scheme’s introduction says 2011 – 2021; the paper’s '
           'graph and the scheme’s own answer run to 2022.'),
     point('r-explanation', H.run('• This increase is due to the strong performance', 'It is essential that'), 4,
           'Explain one reason for the trend, 4 marks. The scheme dates the 12.5% rate to 1998; Revenue’s '
           '2003 Statistical Report gives 1 January 2003 for the standard 12.5% rate.')],
    stem=H.ask(23, 'The diagram below shows Ireland’s Corporation Tax receipts', ' Corporation Tax Receipts'),
    figure=PAP + 'p23-i0')
add('q13-c-ii', '3-1', 'current-budget-surplus', ref(13, '(c)(ii)'),
    H.ask(24, 'Explain the term government current budget surplus.', ' Explanation:'), '7', 7,
    [point('r-1', H.run('A government current budget surplus occurs when', '32 | P a g e'), 7,
           'Explain the term, 7 marks: CURRENT revenue exceeding CURRENT expenditure.')],
    stem=H.ask(24, 'It is essential that the government uses budget surpluses wisely.', ' Adapted from'))
add('q13-c-iii-pos', '3-1', 'positive-and-negative-budget-surplus-effects', ref(13, '(c)(iii)'),
    H.ask(24, 'Outline one possible positive and one possible negative economic consequence', ' One possible positive:'),
    '3 + 3', 6,
    [heading('r-positive', 'One possible positive',
             H.menu('Positive: ⟨1 @ 3⟩', 'Negative: ⟨1 @ 3⟩', [33]), 3,
             'Complete BOTH headings. One positive consequence, 3 marks.'),
     heading('r-negative', 'One possible negative',
             H.menu('Negative: ⟨1 @ 3⟩', '33 | P a g e', [33]), 3, 'One negative consequence, 3 marks.')])

# Q14 ─ monopolistic competition; ECB rates; real interest; neobanks
pick('q14-a-i', '2-0', 'monopolistic-competition-characteristics', ref(14, '(a)(i)'),
     H.ask(25, 'Outline three characteristics (other than many sellers)', ' 1. 2. 3.'),
     'A characteristic other than many sellers — any three',
     H.menu('Outline three characteristics (other than many sellers) of a', '(ii) Firms operating under monopolistic', [34]),
     3, 5, 'Three characteristics other than many sellers, 5 marks each.',
     stem=H.ask(25, 'In the Irish economy there are many restaurants', ' Outline three'))
stance('q14-a-ii', [
    ('agree', 'agree', 'The case that resources are wasted',
     [H.run('It does not produce at the lowest point of average cost', 'DISAGREE:')]),
    ('disagree', 'disagree', 'The case that resources are not wasted',
     [H.run('If a firm invests in innovation', '34 | P a g e')])],
    '2-0', 'monopolistic-competition-wastes-resources', 14, '(a)(ii)',
    H.ask(25, 'Firms operating under monopolistic competition waste resources.', ' Agree:'), 6)
next(c for c in cards if c['id'] == D.prefix + 'q14-a-ii-disagree')['conceptId'] = 'monopolistic-competition-does-not-waste'
q14b_ask = H.ask(26, 'Explain, with the aid of a fully labelled diagram (including the axes), the long-run', ' Explanation:')
add('q14-b-i', '2-0', 'long-run-equilibrium-in-monopolistic-competition', ref(14, '(b)(i)', 'diagram'),
    q14b_ask + ' Draw the diagram.', '12 x 1', 12,
    [point('r-diagram', 'Price P C Q Qty MR AR AC MC E T A', 12,
           'Twelve labels at 1 mark each: Price axis, P, C, Q, Quantity axis, MR, AR, AC, MC, E, T (or a '
           'dot) and A. MC = MR at E sets output Q; AR is tangent to AC at T, so price P equals cost C; A '
           'marks the minimum of AC. The official diagram is shown in the figure.')],
    figure=SOL + 'p35-q14bi-equilibrium',
    notes='The diagram (12) and the written explanation (9) are separately priced in the scheme.')
add('q14-b-i-explanation', '2-0', 'long-run-equilibrium-in-monopolistic-competition-explanation',
    ref(14, '(b)(i)', 'explanation'), q14b_ask + ' Write the explanation.', '9', 9,
    [point('r-explanation', H.run('1. Equilibrium:', '35 | P a g e'), 9,
           'Explain all six features, 9 marks with no separately priced steps: equilibrium at E where '
           'MC = MR, output Q, price P, cost C, normal profit because AR = AC, and scarce resources wasted '
           'because output is short of the lowest point of AC.')],
    figure=SOL + 'p35-q14bi-equilibrium')
pick('q14-b-ii', '2-0', 'monopolistic-competition-consumer-advantage', ref(14, '(b)(ii)'),
     H.ask(26, 'Outline one possible economic advantage to consumers', ' Economic advantage:'),
     'An advantage to consumers — any one',
     H.menu('(ii) Outline one possible economic advantage to consumers', 'The President of the European Central Bank', [36]),
     1, 5, 'One developed advantage, 5 marks.')
q14c_stem = H.ask(27, 'The President of the European Central Bank (ECB)', ' Adapted from')
add('q14-c-i-spending', '3-3', 'interest-rates-spending-and-national-debt', ref(14, '(c)(i)'),
    H.ask(27, 'Explain one economic effect these interest rate increases have', ' Level of consumer spending:'),
    '2 @ 4', 8,
    [heading('r-spending', 'Level of consumer spending',
             H.menu('Level of consumer spending:', 'Cost of servicing the national debt:', [36]), 4,
             'Complete BOTH headings. The effect on consumer spending, 4 marks.'),
     heading('r-debt', 'Cost of servicing the national debt',
             H.menu('Cost of servicing the national debt:', '(ii) Calculate the real rate', [36]), 4,
             'The effect on the cost of servicing the national debt, 4 marks.')],
    stem=q14c_stem)
add('q14-c-ii', '3-3', 'calculating-the-real-rate-of-interest', ref(14, '(c)(ii)'),
    H.ask(27, 'Calculate the real rate of interest', ' Workings:'), '8', 8,
    [point('r-answer', '2.25% – 5.50% = - 3.25%', 8,
           'Real rate = nominal rate − inflation rate = 2.25% − 5.50% = −3.25%. A negative real rate: '
           'saving loses purchasing power. Deduct 1 mark if % is omitted.')],
    stem=q14c_stem)
pick('q14-c-iii', '3-4', 'why-neobanks-grew-in-ireland', ref(14, '(c)(iii)'),
     H.ask(28, 'Outline two reasons why so many Irish people have adopted', ' 1. 2.'),
     'A reason for adopting a digital-only account — any two',
     H.menu('Outline two reasons why so many Irish people have adopted', '37 | P a g e', [37]),
     2, 6, 'Two reasons, 6 marks each.',
     stem=H.ask(28, 'The number of people using the services offered by Neobanks', ' Adapted from'))

# Q15 ─ LDC debt; aid; competitiveness; the dollar; EU; obesity; data centres
q15_stem = H.ask(29, 'The chart below shows the rising debt repayment', ' Debt servicing')
add('q15-a-i', '4-0', 'percentage-rise-in-ldc-debt-servicing', ref(15, '(a)(i)'),
    H.ask(29, 'Calculate the percentage increase in debt repayment', ' Workings:'), '8', 8,
    [point('r-answer', '95.45%', 8,
           '($43bn − $22bn) ÷ $22bn × 100 = 21 ÷ 22 × 100 = 95.45%. Use 2016 as the base. Deduct 1 mark '
           'if % is omitted.')],
    stem=q15_stem, figure=PAP + 'p29-i0')
pick('q15-a-ii', '4-0', 'solving-the-ldc-debt-crisis', ref(15, '(a)(ii)'),
     H.ask(29, 'Outline one step which could be taken by governments of developed countries', ' One step:'),
     'A step developed countries could take — any one',
     H.menu('(ii) Outline one step which could be taken by the governments', '38 | P a g e', [38]),
     1, 5, 'One developed step, 5 marks.', stem=q15_stem, figure=PAP + 'p29-i0')
add('q15-a-iii', '4-0', 'limits-of-financial-aid', ref(15, '(a)(iii)'),
    H.ask(29, 'Explain two reasons why financial aid given to LDCs', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A reason aid may not help — any two',
           H.menu('(iii) Explain two reasons why financial aid given to LDCs', '39 | P a g e', [39]), 6, 4, 'reasons')])
q15b_stem = H.ask(30, 'In 2022, the IMD', ' Adapted from')
pick('q15-b-i', '4-2', 'improving-competitiveness', ref(15, '(b)(i)'),
     H.ask(30, 'Suggest two economic measures that the Irish government could implement', ' 1. 2.'),
     'A measure to improve competitiveness — any two',
     H.menu('(i) Suggest two economic measures that the Irish government could implement', '(ii) Over the past year', [40]),
     2, 4, 'Two measures, 4 marks each.', stem=q15b_stem)
add('q15-b-ii', '4-2', 'a-stronger-dollar-and-irish-trade', ref(15, '(b)(ii)'),
    H.ask(30, 'Outline the effects this increase in the value of the American Dollar', ' Ireland’s exports to the US:'),
    '2 @ 5', 10,
    [point('r-exports', H.run('Irish exports should increase', 'and\nIrelands imports'), 5,
           'Complete BOTH headings. Ireland’s exports to the US rise: cheaper in dollars, 5 marks.'),
     point('r-imports', H.run('Irish imports from the US should decrease', '(iii) If competitiveness'), 5,
           'Ireland’s imports from the US fall: dearer in euro, 5 marks.')],
    stem=H.ask(30, 'Over the past year, the American dollar', ' Outline the effects'))
add('q15-b-iii', '3-5', 'what-a-recession-is', ref(15, '(b)(iii)'),
    H.ask(30, 'If competitiveness in Ireland was to deteriorate', ' Recession:'), '4', 4,
    [point('r-1', H.run('A recession is when the economy, as measured by GDP', '40 | P a g e'), 4,
           'Explain the term, 4 marks: two consecutive quarters of negative GDP growth.')])
add('q15-c-i', '4-1', 'reasons-to-join-the-eu', ref(15, '(c)(i)'),
    H.ask(31, 'Give two reasons why countries wish to join the EU.', ' Adapted from'), '6 + 4', 10,
    [steps('r-1', 'A reason to join the EU — any two',
           H.menu('Give two reasons why countries wish to join the EU.', '41 | P a g e', [41]), 6, 4, 'reasons')],
    stem=H.ask(31, 'In 2023, Ireland celebrated its 50th anniversary', ' Give two'))
add('q15-c-ii-economic', '1-3', 'economic-and-social-measures-against-obesity', ref(15, '(c)(ii)'),
    H.ask(31, 'Explain one economic measure and one social measure', ' Economic measure:'), '10', 10,
    [shared('r-economic', 'One economic measure', H.menu('Economic measure\n⟨1 @ 4⟩', 'Social measure\n', [42]),
            'Complete BOTH headings. The scheme prices the pair as one 10: the first correct measure 6 '
            'marks and the second 4, with no fixed share for either heading.'),
     shared('r-social', 'One social measure', H.menu('Social measure\n', '(iii) Amazon secured', [42]),
            'One social measure.')],
    kind='questionTotal', stem=H.ask(31, 'According to a European Agency, Eurostat', ' Adapted from'))
add('q15-c-iii', '2-2', 'data-centres-negative-consequences', ref(15, '(c)(iii)'),
    H.ask(32, 'Discuss two possible negative consequences', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A negative consequence of data centres — any two',
           H.menu('Discuss two possible negative consequences for the Irish economy', '42 | P a g e', [42]), 6, 4,
           'consequences')],
    stem=H.ask(32, 'Amazon secured planning permission for two new data centres', ' Adapted independent.ie'))

# Q16 ─ homelessness; social housing; YED; DART+; indirect taxation
q16_stem = H.ask(33, '12,827 people living in emergency accommodation', ' Number of homeless')
add('q16-a-i', '1-3', 'why-homelessness-rose-in-ireland', ref(16, '(a)(i)'),
    H.ask(33, 'Outline two reasons for the increase in the number of homeless people', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A reason homelessness rose — any two',
           H.menu('(i) Outline two reasons for the increase in the number of homeless people', '43 | P a g e', [43]),
           6, 4, 'reasons')],
    stem=q16_stem, figure=PAP + 'p33-art')
add('q16-a-ii', '1-3', 'benefits-of-social-housing-spending', ref(16, '(a)(ii)'),
    H.ask(33, 'Discuss two benefits of increasing expenditure on social housing', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A benefit other than reducing homelessness — any two',
           H.menu('Discuss two benefits of increasing expenditure on social housing apart', '44 | P a g e', [44]),
           6, 4, 'benefits')],
    stem=H.ask(33, 'Over 7,400 new social housing units were built in 2022.', ' Discuss two'))
add('q16-b-i', '1-4', 'income-elasticity-of-demand', ref(16, '(b)(i)'),
    H.ask(34, 'Explain the term income elasticity of demand.', ' (ii)'), '8', 8,
    [point('r-1', H.run('This measures the percentage/proportionate change', '(ii) Using an appropriate formula'), 8,
           'Explain the term, 8 marks: the percentage change in quantity demanded caused by a percentage '
           'change in income.')])
q16b2_ask = H.ask(34, 'Using an appropriate formula and the figures in the table below', ' Year Average')
add('q16-b-ii', '1-4', 'income-elasticity-and-what-it-means', ref(16, '(b)(ii)', 'calculation'),
    q16b2_ask + ' Do the calculation.', '9', 9,
    [point('r-answer', '+ 0.8', 9,
           'Midpoint YED = (ΔQ ÷ ΔY) × ((Y1 + Y2) ÷ (Q1 + Q2)) = (+30 ÷ +10,000) × (90,000 ÷ 330) = '
           '+0.81818…, which the scheme gives as +0.8. The paper’s table is for 2022 and 2023; the '
           'scheme’s copy of it labels the same figures 2021 and 2022.')],
    figure=PAP + 'p34-i0',
    notes='The workings (9) and the economic meaning (4) are separately priced in the scheme.')
add('q16-b-ii-meaning', '1-4', 'income-elasticity-and-what-it-means-explanation', ref(16, '(b)(ii)', 'meaning'),
    q16b2_ask + ' Write the economic meaning.', '4', 4,
    [point('r-meaning', H.run('The good is inelastic', '(iii) Assume income elasticity'), 4,
           'Explain the sign and the size, 4 marks: positive, so a normal good; below 1, so income '
           'inelastic, a necessity.')],
    figure=PAP + 'p34-i0')
add('q16-b-iii', '1-4', 'using-yed-to-forecast-sales', ref(16, '(b)(iii)'),
    H.ask(34, 'Assume the income elasticity of demand (YED) for a PlayStation 5', ' Workings:'), '6', 6,
    [point('r-answer', 'Answer: 7,400 units', 6,
           'Change in sales = YED × change in income = 5.2 × (−5%) = −26%. 26% of 10,000 units = 2,600 '
           'units. Expected 2024 sales = 10,000 − 2,600 = 7,400 units. The paper gives 2023 sales and a '
           '2024 fall in income; the scheme’s working labels the years 2022 and 2023.')])
q16c_stem = H.ask(35, 'A major expansion to the Dublin Area Rapid Transport', ' Adapted from')
add('q16-c-i', '3-1', 'what-capital-expenditure-is', ref(16, '(c)(i)'),
    H.ask(35, 'The above expenditure is classed as capital expenditure.', ' Explain:'), '4 + 2', 6,
    [point('r-definition', H.run('Capital expenditure is spending on items not used up', 'Example - building'), 4,
           'Explain the term, 4 marks.'),
     point('r-example', H.run('Example - building a new school', '(ii) Outline one social cost'), 2,
           'An example OTHER than transport, 2 marks.')],
    stem=q16c_stem)
add('q16-c-ii-cost', '0-1', 'social-cost-and-benefit-of-dart', ref(16, '(c)(ii)'),
    H.ask(35, 'Outline one social cost and one social benefit of the proposed DART+', ' Social Cost:'), '2 @ 5', 10,
    [heading('r-cost', 'Social cost', H.menu('Social cost:\nTraffic', 'Social benefit:\nReduced emissions', [46]), 5,
             'Complete BOTH headings. One social cost, 5 marks.'),
     heading('r-benefit', 'Social benefit', H.menu('Social benefit:\nReduced emissions', '46 | P a g e', [46]), 5,
             'One social benefit, 5 marks.')],
    stem=q16c_stem)
add('q16-c-iii-advantage', '3-1', 'advantages-and-disadvantages-of-indirect-tax', ref(16, '(c)(iii)'),
    H.ask(36, 'Discuss the economic advantages and disadvantages of increasing indirect taxation.', ' 75 marks'),
    '2 @ 6', 12,
    [heading('r-advantage', 'An advantage', H.menu('Advantages:', 'Disadvantages:', [47]), 6,
             'Complete BOTH headings: two points at 6 marks each, and the scheme requires a MINIMUM of ONE '
             'advantage and one disadvantage. One advantage, 6 marks.'),
     heading('r-disadvantage', 'A disadvantage', H.menu('Disadvantages:', 'Must have a MINIMUM', [47]), 6,
             'One disadvantage, 6 marks.')],
    stem=H.ask(36, 'To fund more expenditure into the future', ' Discuss the economic'))

# The paper's own data beside the typed ask; a card whose figure slot holds its
# solution carries the whole printed question instead (see show_before_reveal).
for cid, fig in [('sa-q3-a', 'p05-q3a-question'), ('seca-q4-a-ticks', 'p06-q4a-question'),
                 ('sa-q10-a-ii', 'p12-q10a-question'), ('q12-b-ii', 'p18-q12bii-question')]:
    c = next(c for c in cards if c['id'] == D.prefix + cid)
    show_before_reveal(c, None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split eight required-heading responses into one card per
# heading. Each half is still emitted, lifted from its own heading, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('sa-q6-b-up', 'sa-q6-b-down', 'Upward sloping part',
     [H.run('The law of diminishing marginal returns', '10 | P a g e')], 2),
    ('sa-q9-a-benefit', 'sa-q9-a-cost', 'Social benefit', q9_benefit, 3),
    ('q13-b-iii-neg', 'q13-b-iii-pos', 'Negative', q13_negative, 4),
    ('q13-c-iii-neg', 'q13-c-iii-pos', 'Negative', H.menu('Negative: ⟨1 @ 3⟩', '33 | P a g e', [33]), 3),
    ('q14-c-i-debt', 'q14-c-i-spending', 'Cost of servicing the national debt',
     H.menu('Cost of servicing the national debt:', '(ii) Calculate the real rate', [36]), 4),
    ('q15-c-ii-social', 'q15-c-ii-economic', 'Social measure',
     H.menu('Social measure\n', '(iii) Amazon secured', [42]), 6),
    ('q16-c-ii-benefit', 'q16-c-ii-cost', 'Social benefit',
     H.menu('Social benefit:\nReduced emissions', '46 | P a g e', [46]), 5),
    ('q16-c-iii-disadvantage', 'q16-c-iii-advantage', 'Disadvantages',
     H.menu('Disadvantages:', 'Must have a MINIMUM', [47]), 6),
]
for old, canonical, label, options, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this heading is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
