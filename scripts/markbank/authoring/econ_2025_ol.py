#!/usr/bin/env python3
"""Economics 2025 Ordinary Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2025-ol-ev.json,
made from a visual sweep of all 32 paper pages and 47 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID).
Three cards that held one half of a jointly priced answer are withdrawn onto
the card that now carries the whole answer, through explicit progress aliases.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). The only prose written
here is guidance: tariffs, route labels and what a figure or a calculation
shows. Scheme PDF page = printed page + 1.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, emit, point, tidy  # noqa: E402

O = Sheet(2025, 'ordinary', 'LC034GLP000EV')
D = Deck(2025, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2025-OL-scheme-'
PAP = 'economics-2025-OL-paper-'


def key(s):
    return re.sub(r'\s+', '', s)


def lines_menu(start, end, pages, drop=(), occ=None):
    """Responses whose bold heading sits on its own line (no dash after it).

    The chunk is split at every line that opens with one of the bold headings
    the PDF prints on `pages`; a dropped heading (a category such as "Positive
    Effects") closes the current response without opening one.
    """
    raw = O.chunk(start, end, occ)
    # A heading at the foot of a page can arrive with the margin's bold mark
    # cells ("1st @ 8 2nd @ 4") joined on; those are tariffs, not heading words.
    heads = [re.split(r'\s+\d+(?:st|nd|rd|th)?\s*[@x]\s*\d', h)[0] for h in O.bold_heads(pages)]
    heads = [h for h in heads if len(key(h)) >= 6]
    out, current = [], None
    for line in raw.split('\n')[1:]:
        text = line.strip()
        if not text or '| P a g e' in text:
            continue
        k = key(text)
        hit = next((h for h in heads if k.startswith(key(h)) or
                    (key(h).startswith(k) and len(k) >= 12)), None)
        if hit and any(key(d) == key(hit) or key(d) == k for d in drop):
            current = None
            continue
        if hit:
            current = [text]
            out.append(current)
        elif current is not None:
            current.append(text)
    # The marks column can run into a response's line ("... increase 2nd @ 4").
    return [tidy(re.sub(r'\s*\b\d(?:st|nd|rd|th)\s*@\s*\d+\b', ' ', ' '.join(o))) for o in out]


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, per, note):
    """A required heading inside a jointly priced answer (1st x n, 2nd x m).

    One unpriced point carrying the heading's examples: a per-option price here
    would print "n marks each" for a share the scheme never fixes.
    """
    return point(rid, paras(options), None, f'{label}. {note}')


def stance(prefix, choices, topic, concept, q, parts, qtext, per, *, sa=False, stem='', figure=''):
    """A printed tick-box choice whose scheme credits each side: one card per side."""
    for suffix, word, label, options in choices:
        pick(f'{prefix}-{suffix}' if suffix else prefix, topic, concept, ref(q, parts, word, sa),
             f'{qtext} Answer for: {word.upper()}.', label, options, 1, per,
             f'One developed justification for the {word} choice, {per} marks. The scheme credits '
             f'both choices; these are its examples, not a closed list.',
             stem=stem, section='A' if sa else 'B', figure=figure)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ CSO; cheaper electricity
q1_stem = O.ask(3, 'The CSO released the following information', ' www.cso')
add('sa-q1-i', '3-0', 'what-cso-stands-for', ref(1, '(i)', sa=True),
    O.ask(3, 'What do the initials CSO stand for?', ' C Statistics O'), '2 @ 4', 8,
    [point('r-c', 'Central', 4, 'C stands for Central, 4 marks.'),
     point('r-o', 'Office', 4, 'O stands for Office, 4 marks. Statistics is completed on the paper.')],
    stem=q1_stem, **A)
pick('sa-q1-ii', '1-1', 'benefit-of-lower-electricity-prices', ref(1, '(ii)', sa=True),
     O.ask(3, 'Outline one economic benefit for Irish consumers', ' Economic benefit:'),
     'A benefit for consumers — any one',
     O.menu('(ii) Outline one economic benefit for Irish consumers', '5 | P a g e', [6]),
     1, 4, 'One developed benefit, 4 marks.', stem=q1_stem,
     figure=PAP + 'p03-q1-electricity-headline', **A)

# Q2 ─ free schoolbooks; current budget surplus
q2_stem = O.ask(4, 'As part of Budget 2025, the Minister for Education', ' Adapted from')
stance('sa-q2-a', [
    ('yes', 'yes', 'A reason the measure is efficient',
     O.menu('Indicate by means of a tick', '\nNo\n', [7])),
    ('no', 'no', 'A reason the measure is not efficient',
     O.menu('\nNo\n', '(b) OR', [7]))],
    '0-1', 'free-schoolbooks-and-scarce-resources', 2, '(a)',
    O.ask(4, 'Do you think the above measure represents an efficient use', ' Yes No'), 12,
    sa=True, stem=q2_stem, figure=PAP + 'p04-i0')
add('sa-q2-b', '3-1', 'current-budget-surplus', ref(2, '(b)', sa=True),
    O.ask(4, 'Explain the term government current budget surplus.', ' Explanation:'), '12', 12,
    [point('r-1', 'When government current revenue exceeds government current expenditure.', 12,
           'Explain the term, 12 marks. Answer either (a) or (b).')],
    stem=O.ask(4, 'The Irish government has planned for a current budget surplus', ' Explain the term'), **A)

# Q3 ─ libraries; sporting events
q3_stem = O.ask(5, 'Ireland’s newest library was opened recently', ' Adapted from')
q3a = O.ask(5, 'Outline one private benefit or social benefit', ' Private benefit Social benefit')
for suffix, word, start, end in [('private', 'private benefit', 'Private Benefit', 'Social Benefit'),
                                 ('social', 'social benefit', 'Social Benefit', '7 | P a g e')]:
    pick(f'sa-q3-a-{suffix}', '2-2', 'benefits-of-public-libraries', ref(3, '(a)', word, sa=True),
         f'{q3a} Answer for: {word.upper()}.', f'A {word} — any one',
         lines_menu(start, end, [8], drop=('Private Benefit', 'Social Benefit')),
         1, 12, f'One developed {word}, 12 marks. The paper prints a tick for private or social and '
         f'the scheme lists both; these are its examples, not a closed list.', stem=q3_stem, **A)
stance('sa-q3-b', [
    ('agree', 'agree', 'A reason to agree', O.menu('\nAgree\n', '\nDisagree\n', [9])),
    ('disagree', 'disagree', 'A reason to disagree', O.menu('\nDisagree\n', '8 | P a g e', [9]))],
    '3-5', 'hosting-international-sporting-events', 3, '(b)',
    O.ask(5, 'Indicate with a tick (✔) if you agree or disagree', ' Agree Disagree'), 12,
    sa=True, stem=O.ask(5, 'The Government should continue to support the hosting', ' Indicate'))

# Q4 ─ Budget 2025 measures
q4_stem = O.ask(6, 'Budget 2025 comes with some great news', ' (a)')
pick('sa-q4-a', '3-1', 'reasons-for-budget-2025-measures', ref(4, '(a)', sa=True),
     O.ask(6, 'Outline one reason why the government introduced the above measures.', ' Reason:'),
     'A reason for the measures — any one',
     lines_menu('(a) Outline one reason why the government introduced', '\nOR\n', [10]),
     1, 12, 'One developed reason, 12 marks. Answer either (a) or (b).', stem=q4_stem, **A)
pick('sa-q4-b', '3-1', 'opportunity-cost-of-budget-measures', ref(4, '(b)', sa=True),
     O.ask(6, 'Is there an opportunity cost of these measures', ' Yes No'),
     'An explanation of the opportunity cost — any one',
     O.menu('Place a tick (✔) in the relevant box below and explain your answer.', '9 | P a g e', [10]),
     1, 12, 'Tick YES: the scheme ticks Yes and credits no No answer. One developed explanation, '
     '12 marks for the tick and the explanation together.', stem=q4_stem, **A)

# Q5 ─ GDP
q5_stem = O.ask(7, 'Ireland’s GDP is expected to grow by 3.6%', ' Adapted from')
add('sa-q5-i', '3-0', 'what-gdp-stands-for', ref(5, '(i)', sa=True),
    O.ask(7, 'What do the initials GDP stand for?', ' G D Product'), '4', 4,
    [point('r-1', 'GROSS DOMESTIC PRODUCT', 4, 'G stands for Gross and D for Domestic; Product is '
           'completed on the paper. One 4 for the answer.')],
    stem=q5_stem, **A)
pick('sa-q5-ii', '3-5', 'advantage-of-rising-gdp', ref(5, '(ii)', sa=True),
     O.ask(7, 'Outline one advantage of an increasing GDP', ' Advantage:'),
     'An advantage for citizens — any one',
     O.menu('Outline one advantage of an increasing GDP for citizens', '10 | P a g e', [11]),
     1, 8, 'One developed advantage, 8 marks.', stem=q5_stem, **A)

# Q6 ─ vapes: one private AND one social cost, priced together
add('sa-q6-private', '2-2', 'private-and-social-costs-of-vapes', ref(6, sa=True),
    O.ask(7, 'Outline one private cost to the individual and one social cost', ' Private cost:'), '12', 12,
    [shared('r-private', 'One private cost', O.menu('Private cost\n', 'Social Cost', [12]), 8,
            'Complete BOTH headings. The scheme prices the pair as one 12: the first correct answer '
            '8 marks and the second 4, with no fixed share for either heading.'),
     shared('r-social', 'One social cost', O.menu('Social Cost', '11 | P a g e', [12]), 8,
            'One social cost to society.')],
    kind='questionTotal', stem=O.ask(7, 'It has been reported that disposable vapes', ' Adapted from'),
    figure=PAP + 'p07-i0', **A)

# Q7 ─ population aged 65 and over
q7_stem = O.ask(8, 'The graph below shows the population of people aged 65', ' Population -')
add('seca-q7-i', '3-1', 'percentage-increase-in-over-65s', ref(7, '(i)', sa=True),
    O.ask(8, 'The number of people aged 65 and over has increased by 243,700.', ' Workings:'), '4', 4,
    [point('r-answer', '41.3 %', 4,
           'Increase ÷ 2014 population × 100 = 243,700 ÷ 589,500 × 100 = 41.3%. The official working '
           'is shown in the figure.')],
    stem=q7_stem, figure=SOL + 'p13-q7i-working', **A)
pick('sa-q7-ii', '3-1', 'ageing-population-and-the-government', ref(7, '(ii)', sa=True),
     O.ask(8, 'Outline one possible economic effect which this increase', ' Economic effect:'),
     'An effect for the Government — any one',
     O.menu('(ii) Outline one possible economic effect which this increase', '12 | P a g e', [13]),
     1, 8, 'One developed effect, 8 marks.', stem=q7_stem, figure=PAP + 'p08-q7-population', **A)

# Q8 ─ monopoly: the tick in (i) and the barrier in (ii) share one 12
add('seca-q8-i-ticks', '2-0', 'monopoly-and-barriers-to-entry', ref(8, '(i)–(ii)', sa=True),
    O.ask(9, 'Identify, with a tick', ' Name of Organisation') + ' '
    + O.ask(9, 'In a monopoly market structure, there are barriers to entry.', ' Outline:'), '12', 12,
    [point('r-tick', 'An Post (mail service for letter post) ✔', None,
           '(i) Tick An Post: the mail service for letter post is the monopoly.'),
     point('r-barrier', paras([tidy(x.lstrip('• ')) for x in
                               O.chunk('Outline one such possible barrier to entry.', '13 | P a g e').split('\n•')[1:]]),
           None, '(ii) One barrier to entry; these are the scheme’s examples. The scheme prices (i) and '
           '(ii) together: the first correct answer 8 marks and the second 4.')],
    kind='questionTotal', figure=SOL + 'p14-q8i-ticks', **A)

# Q9 ─ substitutes and complements
add('seca-q9-ticks', '1-1', 'substitute-or-complement-for-a-smartwatch', ref(9, sa=True),
    O.ask(9, 'In the table below, indicate by means of a tick', ' Substitute Complement Reason'), '2 @ 6', 12,
    [point('r-iphone', 'The apple iPhone can be used along with', 6,
           'Apple iPhone 16: COMPLEMENT, with the reason (used along with the watch), 6 marks.'),
     point('r-samsung', 'The Samsung watch would be purchased', 6,
           'Samsung Galaxy Watch 7: SUBSTITUTE, with the reason (bought instead of the Apple watch), '
           '6 marks.')],
    stem=O.ask(9, 'In September 2024, Apple released', ' www.apple.com'), figure=SOL + 'p15-q9-ticks', **A)

# Q10 ─ Oasis tickets
q10_stem = O.ask(10, 'Oasis will play their first concert', ' Adapted from')
pick('sa-q10-i', '1-1', 'non-price-determinants-of-demand', ref(10, '(i)', sa=True),
     O.ask(10, 'Outline one factor, other than ticket prices', ' Outline:'),
     'A factor other than price — any one',
     O.menu('(i) Outline one factor, other than ticket prices', '(ii) The diagram below shows the supply', [16]),
     1, 8, 'One developed factor, 8 marks.', stem=q10_stem, **A)
add('sa-q10-ii', '1-2', 'fixed-supply-of-concert-tickets', ref(10, '(ii)', sa=True),
    O.ask(10, 'The diagram below shows the supply curve for tickets', ' Price S'), '4', 4,
    [point('r-1', O.run('The supply of tickets is fixed', '15 | P a g e'), 4,
           'Explain the vertical supply curve: supply is fixed at the 82,300 capacity, 4 marks.')],
    stem=q10_stem, figure=PAP + 'p10-art', **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ perfect competition; Dublin Airport
q11a_stem = O.ask(11, 'The image below shows a photo of a firm', ' www.expedia.com')
add('q11-a-i', '2-0', 'homogeneous-products', ref(11, '(a)(i)'),
    O.ask(11, 'Explain the economic term homogenous product', ' Explanation:'), '6', 6,
    [point('r-meaning', O.run('The goods produced are identical / the same.', 'Example:'), None,
           'Explain the term.'),
     point('r-example', O.run('Commodities such as wheat, crude oil, gold', '(ii) Outline two assumptions'), None,
           'Give one example; these are the scheme’s examples. The scheme gives one 6 for the '
           'explanation and the example together, with no published split.')],
    kind='questionTotal', stem=q11a_stem)
add('q11-a-ii', '2-0', 'assumptions-of-perfect-competition', ref(11, '(a)(ii)'),
    O.ask(11, 'Outline two assumptions of perfect competition', ' 1. 2.'), '10 + 4', 14,
    [anyN('r-1', 'An assumption other than homogenous products — any two', None, 2, 10,
          O.menu('(ii) Outline two assumptions of perfect competition', '16 | P a g e', [17]),
          'Two assumptions: the first correct one 10 marks and the second 4.', steps=[10, 4])],
    stem=q11a_stem)
q11b_stem = O.ask(12, 'The diagram below represents the long-run equilibrium', ' Price MC')
q11b_ask = O.ask(12, 'Write out in full what any three of the following four labels', ' MC Q')
# "Any three of the following four labels": the student chooses which three, and
# the scheme prices every label the same, so this is ONE card whose menu holds all
# four labels with a claim of three (a card per combination would put the same
# question in front of the student four times).
q11b_labels = [line.strip() for line in O.chunk(
    'Write out in full what any three of the following four labels represent.',
    '(ii) Equilibrium occurs at point E').split('\n')[1:]
    if line.strip() and not line.strip().startswith('⟨')]
c = pick('q11-b-i', '2-0', 'labels-on-the-perfect-competition-diagram', ref(11, '(b)(i)'),
         q11b_ask, 'A label written out in full — any three', q11b_labels, 3, 8,
         'Any three of the four labels written out in full, 8 marks each.',
         stem=q11b_stem, figure=PAP + 'p12-art')
c['labelKey'] = [{'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
                 {'letter': 'Q', 'meaning': 'Quantity', 'askedInThisQuestion': True},
                 {'letter': 'D = AR = MR', 'meaning': 'Demand / Average Revenue / Marginal Revenue',
                  'askedInThisQuestion': True},
                 {'letter': 'AC', 'meaning': 'Average Cost', 'askedInThisQuestion': True},
                 {'letter': 'E', 'meaning': 'long-run equilibrium, where marginal cost cuts average cost at its minimum',
                  'askedInThisQuestion': False}]
add('q11-b-ii', '2-0', 'equilibrium-price-and-output-in-perfect-competition', ref(11, '(b)(ii)'),
    O.ask(12, 'Equilibrium occurs at point E on the diagram above.', ' (iii)'), '4', 4,
    [point('r-1', 'Q1', 4, 'Drop a line from E to the quantity axis and label it Q1; read across from '
           'E to the price axis and label it P1. One 4 for both labels. The official diagram is shown '
           'in the figure.')],
    stem=q11b_stem, figure=SOL + 'p18-q11b-diagram')
pick('q11-b-iii', '2-0', 'consumer-advantage-of-perfect-competition', ref(11, '(b)(iii)'),
     O.ask(12, 'As a consumer what, in your opinion, is the main advantage', ' Advantage:'),
     'An advantage for consumers — any one',
     [tidy(x) for x in re.split(r'(?<=\.)\n', O.chunk('Low prices - firms are competitive', '17 | P a g e'))
      if x.strip()],
     1, 4, 'One developed advantage, 4 marks.', stem=q11b_stem, figure=PAP + 'p12-art')
q11c_stem = O.ask(13, 'Dublin Airport has a passenger cap', ' (i)')
pick('q11-c-i', '2-2', 'why-cap-airport-passengers', ref(11, '(c)(i)'),
     O.ask(13, 'Outline one reason why, in your opinion, a limit', ' Reason:'),
     'A reason for the cap — any one',
     O.menu('(i) Outline one reason why, in your opinion, a limit', '(ii) If this passenger cap', [19]),
     1, 10, 'One developed reason, 10 marks.', stem=q11c_stem)
add('q11-c-ii', '2-2', 'effects-of-the-airport-cap', ref(11, '(c)(ii)'),
    O.ask(13, 'If this passenger cap remains unchanged', ' Tourism into Ireland:'), '13', 13,
    [shared('r-tourism', 'Tourism into Ireland', [O.run('Tourism into Ireland\nThis could lead', 'Other airports in Ireland i.e. Cork, Shannon and Ireland West Airport\nAirlines')], 7,
            'Complete ALL THREE headings. The scheme prices the three together: the first correct '
            'effect 7 marks, the second 3 and the third 3, with no fixed share for any heading.'),
     shared('r-airports', 'Other airports in Ireland', [O.run('Other airports in Ireland i.e. Cork, Shannon and Ireland West Airport\nAirlines', 'Economic growth in Ireland\nThis')], 7,
            'The effect on other Irish airports.'),
     shared('r-growth', 'Economic growth in Ireland', [O.run('Economic growth in Ireland\nThis', '18 | P a g e')], 7,
            'The effect on economic growth.')],
    kind='questionTotal', stem=q11c_stem)

# Q12 ─ government expenditure; national income; ECB
q12_stem = O.ask(14, 'The pie chart below outlines budgeted government current', ' Total Government')
add('q12-a-i', '3-1', 'capital-share-of-government-spending', ref(12, '(a)(i)'),
    O.ask(14, 'Calculate capital expenditure as a percentage', ' Workings:'), '16', 16,
    [point('r-answer', '14.14 %', 16,
           'Capital ÷ total × 100 = €14.9bn ÷ €105.4bn × 100 = 14.14%. The scheme prints its mark '
           'split on the working: 6 for €14.9bn, 4 for €105.4bn, 2 for ×100 and 4 for the answer. '
           'The official working is shown in the figure.')],
    stem=q12_stem, figure=SOL + 'p20-q12ai-working')
add('q12-a-ii', '3-1', 'walking-and-cycling-as-capital-spending', ref(12, '(a)(ii)'),
    O.ask(14, 'Indicate with a tick (✓) whether the above is an example', ' Current Expenditure'), '5', 5,
    [point('r-1', O.run('Capital expenditure is spending by the government on items', '19 | P a g e'), 5,
           'Tick CAPITAL EXPENDITURE: the scheme ticks capital only. Explain it, 5 marks for the tick '
           'and the explanation together.')],
    stem=O.ask(14, 'In Budget 2025, the government is making €360 million', ' Adapted from'))
q12b_stem = O.ask(15, 'National Income is calculated using the following formula:', ' (i)')
add('q12-b-i', '3-0', 'national-income-components', ref(12, '(b)(i)'),
    O.ask(15, 'State what each of the letters C, G and X stand for.', ' C G X'), '3 @ 4', 12,
    [point('r-c', 'C: Consumption expenditure', 4, 'C, 4 marks.'),
     point('r-g', 'G: Government Spending', 4, 'G, 4 marks.'),
     point('r-x', 'X: Exports', 4, 'X, 4 marks. The scheme prints one 12 for the three letters.')],
    stem=q12b_stem)
add('q12-b-ii', '3-0', 'open-economy-multiplier', ref(12, '(b)(ii)'),
    'The Multiplier for an open economy is: 1 / (MPS + MPM). '
    + O.ask(15, 'Assume that MPS is 0.2 and MPM is 0.3.', ' Workings:'), '4 @ 3', 12,
    [point('r-answer', '0.2 + 0.3 = 0.5 = 2', 12,
           '1 ÷ (0.2 + 0.3) = 1 ÷ 0.5 = 2. The scheme gives 12 as 4 @ 3 across the working; the '
           'official working is shown in the figure.')],
    stem=q12b_stem, figure=SOL + 'p21-q12bii-working')
add('q12-b-iii', '3-0', 'what-an-open-economy-is', ref(12, '(b)(iii)'),
    O.ask(15, 'Explain what is meant by the economic term open economy.', ' Explanation:'), '4', 4,
    [point('r-1', O.run('An Open Economy is an economy where international trade', '20 | P a g e'), 4,
           'Explain the term, 4 marks.')],
    stem=O.ask(15, 'Ireland is a small open economy.', ' Explain'))
q12c_stem = O.ask(16, 'In October 2024, the ECB cut interest rates', ' Adapted from')
add('q12-c-i', '3-3', 'what-ecb-stands-for', ref(12, '(c)(i)'),
    O.ask(16, 'What do the initials ECB stand for?', ' E C B'), '3 @ 4', 12,
    [point('r-e', 'European', 4, 'E: European, 4 marks.'), point('r-c', 'Central', 4, 'C: Central, 4 marks.'),
     point('r-b', 'Bank', 4, 'B: Bank, 4 marks.')],
    stem=q12c_stem)
pick('q12-c-ii', '3-3', 'aims-of-the-ecb', ref(12, '(c)(ii)'),
     O.ask(16, 'Outline one aim of the ECB.', ' Outline:'), 'An aim of the ECB — any one',
     lines_menu('(ii) Outline one aim of the ECB.', '(iii) Explain the economic effect', [22]),
     1, 4, 'One aim, 4 marks.', stem=q12c_stem)
add('q12-c-iii', '3-4', 'lower-rates-savers-and-borrowers', ref(12, '(c)(iii)'),
    O.ask(16, 'Explain the economic effect these interest rate decreases', ' Savers:'), '10', 10,
    [shared('r-savers', 'Savers in Ireland', [O.run('Savers may decide to save less', 'Borrowers repaying mortgages')], 6,
            'Complete BOTH headings. The scheme prices the pair as one 10: the first correct effect '
            '6 marks and the second 4.'),
     shared('r-borrowers', 'Borrowers repaying mortgages', [O.run('Consumers will have more disposable income', '21 | P a g e')], 6,
            'The effect on borrowers repaying mortgages.')],
    kind='questionTotal', stem=q12c_stem)

# Q13 ─ skilled labour; costs; MNCs and infrastructure
q13a_stem = O.ask(17, 'Ireland remains close to full employment', ' (i)')
add('q13-a-i', '2-1', 'labour-as-a-factor-of-production', ref(13, '(a)(i)'),
    O.ask(17, 'Explain the factor of production labour.', ' Explanation:'), '7', 7,
    [point('r-1', O.run('The effort that people contribute', '(ii) State two sectors'), 7, 'Explain labour, 7 marks.')],
    stem=q13a_stem)
add('q13-a-ii', '2-1', 'sectors-short-of-skilled-labour', ref(13, '(a)(ii)'),
    O.ask(17, 'State two sectors of the Irish economy', ' 1. 2.'), '8 + 4', 12,
    [anyN('r-1', 'A sector short of skilled labour — any two', None, 2, 8,
          [s.strip() for s in O.run('Science and engineering, ICT', '(iii) Outline one economic measure')
           .rstrip('.').replace(' and transport', ', transport').split(',')],
          'Two sectors: the first correct one 8 marks and the second 4. These are the scheme’s '
          'examples, not a closed list.', steps=[8, 4])],
    stem=q13a_stem)
q13a3 = O.ask(17, 'Outline one economic measure the Irish government or employers', ' Irish government Employers')
for suffix, word, opts in [
        ('gov', 'Irish government', O.menu('\nIrish government\n', 'Responses for employers continue', [23])),
        ('emp', 'employers', O.menu('\nEmployers\n', '23 | P a g e', [24]))]:
    pick(f'q13-a-iii-{suffix}', '2-1', 'raising-the-supply-of-skilled-labour', ref(13, '(a)(iii)', word),
         f'{q13a3} Answer for: {word.upper()}.', f'A measure for {word} — any one', opts, 1, 7,
         f'One developed measure for the ticked side, 7 marks. The scheme credits both sides; these '
         f'are its examples, not a closed list.', stem=q13a_stem)
add('q13-b-i', '1-5', 'plotting-cost-and-revenue-curves', ref(13, '(b)(i)'),
    O.ask(18, 'On the graph paper provided below, draw and label:', ' Quantity (units'), '4 + 5 + 5 + 3', 17,
    [point('r-axes', 'Axes', 4, 'Complete both axes, 2 @ 2.'),
     point('r-ac', 'AC1', 5, 'Plot and label the AC curve, 5 marks.'),
     point('r-mc', 'MC1', 5, 'Plot and label the MC curve, 5 marks. The scheme margin prints MC:5 twice; '
           'one of the two is the AC curve.'),
     point('r-mr', 'MR: 3', 3, 'Draw MR as a horizontal line at €200, 3 marks. The official graph is '
           'shown in the figure.')],
    stem=O.ask(18, 'You have been given the data below for a firm.', ' On the graph'),
    figure=SOL + 'p25-q13bi-diagram')
q13b2 = O.ask(18, 'Explain the meaning of either of the following terms', ' Marginal Cost Marginal Revenue')
for cid, word, start, end in [('q13-b-ii', 'marginal cost', 'Marginal cost is the addition', 'Marginal revenue is the addition'),
                              ('q13-b-ii-mr', 'marginal revenue', 'Marginal revenue is the addition', '24 | P a g e')]:
    add(cid, '1-5', 'marginal-cost-and-marginal-revenue', ref(13, '(b)(ii)', word),
        f'{q13b2} Answer for: {word.upper()}.', '6', 6,
        [point('r-1', O.run(start, end), 6, f'Explain {word}, 6 marks. The paper prints a tick for '
               'either term and the scheme defines both.')])
q13c_stem = O.ask(19, 'A new city and reunification of Ireland', ' Adapted from')
add('q13-c-i', '4-1', 'multinationals-in-ireland', ref(13, '(c)(i)'),
    O.ask(19, 'State two other multinational companies', ' 1. 2.'), '8 + 4', 12,
    [anyN('r-1', 'A multinational operating in Ireland — any two', None, 2, 8,
          [re.sub(r'\s*\d(?:st|nd|rd|th) @ \d+$', '', x.strip())
           for x in O.chunk('Pfizer', 'Accept any MNC operating in Ireland.').split('\n') if x.strip()],
          'Two MNCs other than Apple: the first 8 marks and the second 4. The scheme accepts any MNC '
          'operating in Ireland; these are its examples.', steps=[8, 4])],
    stem=q13c_stem)
pick('q13-c', '3-1', 'public-infrastructure-for-the-apple-tax-money', ref(13, '(c)(ii)'),
     O.ask(19, 'Outline two areas of public infrastructure', ' 1. Justify:'),
     'An area of public infrastructure, justified — any two',
     lines_menu('Accept relevant infrastructure spending', '25 | P a g e', [26]),
     2, 7, 'Two areas, each justified, 7 marks each. The scheme accepts any relevant infrastructure '
     'spending.', stem=O.ask(19, 'Apple tax money ‘cannot be used', ' Adapted from'))

# Q14 ─ trade; ODA; HDI
q14a_stem = O.ask(20, 'Ireland reaps €700m Brexit bonanza', ' Adapted from')
add('q14-a-i', '4-2', 'customs-duties', ref(14, '(a)(i)'),
    O.ask(20, 'Explain the economic term customs duties.', ' Explanation:'), '6', 6,
    [point('r-1', 'A custom duty is a tax that is placed on goods imported into a country.', 6,
           'Explain the term, 6 marks.')],
    stem=q14a_stem)
add('q14-a-ii', '4-2', 'why-imports-matter', ref(14, '(a)(ii)'),
    O.ask(20, 'Outline two reasons why imports are important', ' 1. 2.'), '10 + 6', 16,
    [anyN('r-1', 'A reason imports matter — any two', None, 2, 10,
          O.menu('(ii) Outline two reasons why imports are important', '(iii) Ukraine and Moldova', [27]),
          'Two reasons: the first correct one 10 marks and the second 6.', steps=[10, 6])])
pick('q14-a-iii', '4-2', 'supporting-eu-enlargement', ref(14, '(a)(iii)'),
     O.ask(20, 'Outline one reason why Ireland is supporting', ' Reason:'),
     'A reason Ireland supports their membership — any one',
     lines_menu('Outline one reason why Ireland is supporting their membership', '26 | P a g e', [27]),
     1, 4, 'One developed reason, 4 marks.',
     stem=O.ask(20, 'Ukraine and Moldova have applied for membership', ' Outline'))
q14b_stem = O.ask(21, 'The graph below shows the amount of Overseas Development Assistance', ' Ireland Overseas')
q14b1 = O.ask(21, 'Comment on the overall trend of Irish ODA', ' Comment:')
comment = O.run('The overall amount of aid being sent by Ireland overseas has increased', 'Explanation\n')
CATEGORIES = ('Humanitarian', 'Economic Growth and Development', 'Social and Political Stability',
              'Global Benefits', 'Economic and Financial Concerns', 'Inefficiencies and Corruption',
              'Political and Strategic Issues', 'Public Opinion / Political will in Ireland',
              'More positive responses continued on the next page', 'Negative responses outlined on the next pages',
              'Positive Development', 'Negative Development')
GROUPS = {
    'positive': [('Humanitarian', 'Humanitarian\nPoverty Reduction', 'More positive responses continued', [28]),
                 ('Economic Growth and Development', 'Economic Growth and Development', 'Social and Political Stability', [29]),
                 ('Social and Political Stability', 'Social and Political Stability', 'Global Benefits', [29]),
                 ('Global Benefits', 'Global Benefits', 'Negative responses outlined', [29])],
    'negative': [('Economic and Financial Concerns', 'Economic and Financial Concerns', 'Inefficiencies and Corruption', [30]),
                 ('Inefficiencies and Corruption', 'Inefficiencies and Corruption', 'Political and Strategic Issues', [30]),
                 ('Political and Strategic Issues', 'Political and Strategic Issues', 'Public Opinion / Political will', [30]),
                 ('Public Opinion / Political will in Ireland', 'Public Opinion / Political will', '29 | P a g e', [30])],
}
for suffix, word in [('positive', 'positive development'), ('negative', 'negative development')]:
    rows = [point('r-comment', comment, None,
                  'Comment on the rising trend with figures: €868m in 2020 to €2,604m (about €2.6bn) in 2023.')]
    for i, (category, start, end, pages) in enumerate(GROUPS[suffix]):
        rows.append(point(f'r-{suffix}-{i + 1}', paras(lines_menu(start, end, pages, drop=CATEGORIES)), None,
                          f'{category}: the scheme’s examples of why the trend is a {word}. Explain one; '
                          f'the scheme gives one 16 for the comment and the explanation together, with no '
                          f'published split.'))
    add(f'q14-b-i-{suffix}', '4-0', 'trend-in-irish-overseas-aid', ref(14, '(b)(i)', word),
        f'{q14b1} Answer for: {word.upper()}.', '16', 16, rows,
        kind='questionTotal', stem=q14b_stem, figure=PAP + 'p21-q14b-oda')
add('q14-c', '4-0', 'actions-to-improve-citizens-welfare', ref(14, '(b)(ii)'),
    O.ask(21, 'Suggest two actions these governments can take', ' Action 1:'), '6 + 4', 10,
    [anyN('r-1', 'An action to improve welfare — any two', None, 2, 6,
          lines_menu('(ii) Governments of LDCs who receive this aid', '30 | P a g e', [31]),
          'Two actions: the first correct one 6 marks and the second 4.', steps=[6, 4])],
    stem=O.ask(21, 'Governments of LDCs who receive this aid', ' Suggest two'))
q14c_stem = O.ask(22, 'The data below is extracted from Ireland', ' Ireland 2003')
add('q14-c-i', '4-0', 'reading-irelands-hdi', ref(14, '(c)(i)'),
    O.ask(22, 'Based on the data in the table above, state if Ireland', ' Improved Disimproved'), '13', 13,
    [point('r-1', O.run('Ireland\'s HDI position has Improved as their HDI figure', 'Accept correct reference'), 13,
           'Tick IMPROVED: the scheme ticks Improved only. Justify with two figures: the HDI rose from '
           '0.87 in 2003 to 0.95 in 2022 (“Increased + reference to 2 figures”); improvements in the '
           'other rows are also accepted. 13 marks for the tick and the justification together.')],
    stem=q14c_stem, figure=PAP + 'p22-i0')
pick('q14-c-ii', '4-0', 'raising-a-countrys-hdi', ref(14, '(c)(ii)'),
     O.ask(22, 'Suggest one measure a country can take to help it improve its HDI score.', ' One measure:'),
     'A measure to improve HDI — any one',
     O.menu('(ii) Suggest one measure a country can take to help it improve its HDI', '31 | P a g e', [32]),
     1, 10, 'One developed measure, 10 marks.', stem=q14c_stem)

# Q15 ─ entrepreneurs; housing demand; Dublin Quays; government debt
q15a_stem = O.ask(23, 'Entrepreneurs are vital to the success', ' (i)')
add('q15-a-i-entrepreneur', '1-5', 'what-an-entrepreneur-is', ref(15, '(a)(i)'),
    O.ask(23, 'Explain the term entrepreneur.', ' Explanation:'), '10', 10,
    [point('r-1', O.run('An entrepreneur is an individual who identifies a need', '(ii) An entrepreneur must control'), 10,
           'Explain the term, 10 marks.')],
    stem=q15a_stem)
add('q15-a-ii', '1-5', 'why-entrepreneurs-control-costs', ref(15, '(a)(ii)'),
    O.ask(23, 'An entrepreneur must control their costs of production.', ' Agree Disagree'), '4', 4,
    [point('r-1', O.run('Entrepreneurs must control their costs so that they can make', '(iii) More than 570'), 4,
           'Tick AGREE: the scheme ticks Agree and prints no disagree answer. Justify it, 4 marks for '
           'the tick and the justification together.')],
    stem=q15a_stem)
pick('q15-a-iii', '3-5', 'closures-and-local-communities', ref(15, '(a)(iii)'),
     O.ask(23, 'Discuss one effect this development may have on local communities.', ' Effect:'),
     'An effect on local communities — any one',
     O.menu('Discuss one effect this development may have on local communities.', '32 | P a g e', [33]),
     1, 10, 'One developed effect, 10 marks.',
     stem=O.ask(23, 'More than 570 restaurants, cafes', ' Discuss one'))
q15b_stem = ' '.join([O.ask(24, 'It is forecasted that Ireland’s population', ' Adapted from'),
                      O.ask(24, 'The diagram below shows the market demand curve', ' Price S')])
add('q15-b-i', '1-0', 'population-growth-and-housing-demand', ref(15, '(b)(i)'),
    O.ask(24, 'The forecasted increase in population is expected', ' (ii)'), '8 + 4 + 2', 14,
    [point('r-shift', '• Demand curve shifts to the right (D1).', 8, 'Shift demand right to D1, 8 marks.'),
     point('r-quantity', '• Increase in equilibrium quantity (Q1).', 4, 'Show the new quantity Q1, 4 marks.'),
     point('r-price', '• Increase in equilibrium price (P1).', 2, 'Show the new price P1, 2 marks. The '
           'official diagram is shown in the figure.')],
    stem=q15b_stem, figure=SOL + 'p34-q15b-diagram')
add('q15-b-ii', '1-0', 'explaining-the-demand-shift', ref(15, '(b)(ii)'),
    O.ask(24, 'Explain your answer.', ' Explanation:'), '10', 10,
    [point('r-1', O.run('• The increase in population will lead to an increase in demand for housing', '33 | P a g e'), 10,
           'Explain the shift and its effect on price and quantity, 10 marks.')],
    stem=q15b_stem + ' ' + O.ask(24, 'The forecasted increase in population is expected', ' (ii)'),
    figure=PAP + 'p24-art')
stance('q15-b-iii', [
    ('pos', 'positive', 'A positive effect',
     lines_menu('Positive Effects', 'Negative Effects', [35], drop=('Positive Effects',))),
    ('neg', 'negative', 'A negative effect',
     lines_menu('Negative Effects', '34 | P a g e', [35], drop=('Negative Effects',)))],
    '2-2', 'dublin-quays-traffic-restrictions', 15, '(b)(iii)',
    O.ask(24, 'Outline one positive effect or one negative effect', ' Positive Negative'), 6,
    stem=O.ask(24, 'Restrictions were introduced limiting the movement', ' Outline one'))
q15c_stem = O.ask(25, 'The infographic below outlines government debt', ' www.cso')
add('q15-a-i', '3-1', 'benefits-of-lower-government-debt', ref(15, '(c)(i)'),
    O.ask(25, 'Outline one economic benefit for each of the following', ' Irish government:'), '14', 14,
    [shared('r-government', 'The Irish government', O.menu('Irish Government\n', 'Responses for citizens in Ireland', [36]), 8,
            'Complete BOTH headings. The scheme prices the pair as one 14: the first correct benefit '
            '8 marks and the second 6.'),
     shared('r-citizens', 'Citizens in Ireland', O.menu('Citizens in Ireland\n', '(ii) Ireland is considered', [37]), 8,
            'One benefit for citizens in Ireland.')],
    kind='questionTotal', stem=q15c_stem, figure=PAP + 'p25-i0')
add('q15-c-ii', '1-0', 'what-a-mixed-economy-is', ref(15, '(c)(ii)'),
    O.ask(25, 'Explain the meaning of the term mixed economy.', ' Explanation:'), '7', 7,
    [point('r-1', O.run('A mixed economy is one that combines elements', '36 | P a g e'), 7, 'Explain the term, 7 marks.')],
    stem=O.ask(25, 'Ireland is considered a mixed economy.', ' Explain'))

# Q16 ─ excise and VAT; inflation; climate; regional development
q16a_stem = O.ask(26, 'In Budget 2025 the government announced a €1 Increase', ' www.gov.ie')
add('q16-a-i', '3-1', 'excise-and-vat-are-indirect-taxes', ref(16, '(a)(i)'),
    O.ask(26, 'Indicate with a tick (✔) below whether excise duty and VAT', ' Direct tax'), '4', 4,
    [point('r-1', O.run('Excise duty is an indirect tax as it is levied', '(ii) Excise duty is charged'), 4,
           'Tick INDIRECT TAX: the scheme ticks indirect only. Explain it, 4 marks for the tick and '
           'the explanation together.')],
    stem=q16a_stem)
pick('q16-a-ii', '3-1', 'why-tax-alcohol-and-cigarettes', ref(16, '(a)(ii)'),
     O.ask(26, 'Explain one reason why the government places taxes', ' Explanation:'),
     'A reason for the tax — any one',
     O.menu('Explain one reason why the government places taxes', '37 | P a g e', [38]),
     1, 10, 'One developed reason, 10 marks.',
     stem=O.ask(26, 'Excise duty is charged on certain goods', ' Explain one'))
pick('q16-a-iii-excise', '3-1', 'negative-effects-of-higher-vat-on-alcohol', ref(16, '(a)(iii)'),
     O.ask(26, 'Outline one possible negative economic effect', ' Economic effect:'),
     'A negative effect — any one',
     O.menu('(iii) Outline one possible negative effect for the Irish economy', '38 | P a g e', [39]),
     1, 8, 'One developed negative effect, 8 marks.', stem=q16a_stem)
q16b_stem = O.ask(27, 'The chart below shows Ireland’s CPI annual percentage change', ' CPI - ALL')
add('q16-b-i', '3-3', 'what-cpi-stands-for', ref(16, '(b)(i)'),
    O.ask(27, 'What do the letters CPI stand for?', ' C P Index'), '3 + 2', 5,
    [point('r-c', 'Consumer', 3, 'C stands for Consumer. The scheme gives the first correct word 3 '
           'marks and the second 2.'),
     point('r-p', 'Price', 2, 'P stands for Price. Index is completed on the paper.')],
    stem=q16b_stem, figure=PAP + 'p27-art')
add('q16-b-ii', '3-3', 'trend-in-irish-inflation-2024', ref(16, '(b)(ii)'),
    O.ask(27, 'Identify the overall trend of price Inflation', ' Trend:'), '12', 12,
    [point('r-1', O.run('From May 2024 to Sep 2024 the annual percentage change in inflation decreased.', '(iii) Discuss two economic effects'), 12,
           'State the falling trend with figures: about 2.6% in May to about 0.7% in September (a fall '
           'of 1.9 points), 12 marks. The chart plots the annual RATE of inflation, so prices are '
           'still rising, only more slowly.')],
    stem=q16b_stem, figure=PAP + 'p27-art')
add('q16-a-iii', '3-3', 'effects-of-falling-inflation-on-consumers', ref(16, '(b)(iii)'),
    O.ask(27, 'Discuss two possible economic effects which falling price inflation', ' 1. 2.'), '8 + 4', 12,
    [anyN('r-1', 'An effect of falling inflation — any two', None, 2, 8,
          lines_menu('Discuss two economic effects which falling price inflation', '39 | P a g e', [40],
                     drop=('consumers.',)),
          'Two effects: the first correct one 8 marks and the second 4.', steps=[8, 4])],
    stem=q16b_stem, figure=PAP + 'p27-art')
q16c_stem = O.ask(28, 'Large cuts in carbon emissions are needed', ' UN Environment')
add('q16-b-i-ag', '0-2', 'climate-action-by-sector', ref(16, '(c)(i)'),
    ' '.join([O.ask(28, 'Identify one action that each of the following sectors', ' Agricultural Sector'),
              O.ask(28, 'Agricultural Sector', ' Action:'), O.ask(28, 'Industrial Sector', ' Action:')]),
    '6 + 6 + 6', 18,
    [heading('r-agri', 'Agricultural sector — one action',
             O.menu('Agricultural Sector\n', 'Industrial Sector\n', [41]), 6,
             'Complete BOTH sectors and the justification. One action for agriculture, 6 marks.'),
     heading('r-industry', 'Industrial sector — one action',
             O.menu('Industrial Sector\n', 'Justify your answer', [41]), 6,
             'One action for industry, 6 marks.'),
     point('r-justify', O.run('Any of the above measures will help make our economy more sustainable', '40 | P a g e'), 6,
           'Justify the actions, 6 marks.')],
    stem=q16c_stem, figure=PAP + 'p28-i0')
pick('q16-c-ii', '3-1', 'balanced-regional-development-measures', ref(16, '(c)(ii)'),
     O.ask(28, 'Suggest one measure the Irish government could take', ' Suggestion:'),
     'A measure for balanced regional development — any one',
     lines_menu('Suggest one measure the Irish government could take to help achieve this aim', '41 | P a g e', [42]),
     1, 6, 'One developed measure, 6 marks.',
     stem=O.ask(28, 'One of the aims of the Irish government is to promote Balanced', ' Suggest one'))

# The whole printed question, for the cards whose figure slot holds their solution.
for cid, fig in [('seca-q7-i', 'p08-q7i-question'), ('seca-q8-i-ticks', 'p09-q8-question'),
                 ('seca-q9-ticks', 'p09-q9-question'), ('q11-b-ii', 'p12-q11bii-question'),
                 ('q12-a-i', 'p14-q12ai-question'), ('q13-b-i', 'p18-q13bi-question'),
                 ('q15-b-i', 'p24-q15bi-question')]:
    c = next(c for c in cards if c['id'] == D.prefix + cid)
    show_before_reveal(c, None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors gave one half of a jointly priced answer its own card.
# Each half is still emitted, lifted from its own scheme block, so that
# card-corrections.json can withdraw it by ID onto the card that now carries the
# whole answer (cardAliases.ts). None of these ships.
for old, canonical, label, options, per in [
        ('sa-q6-social', 'sa-q6-private', 'One social cost', O.menu('Social Cost', '11 | P a g e', [12]), 4),
        ('sa-q8-ii', 'seca-q8-i-ticks', 'One barrier to entry',
         [tidy(x.lstrip('• ')) for x in O.chunk('Outline one such possible barrier to entry.', '13 | P a g e')
          .split('\n•')[1:]], 4),
        ('q16-b-i-ind', 'q16-b-i-ag', 'Industrial sector — one action',
         O.menu('Industrial Sector\n', 'Justify your answer', [41]), 6)]:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this part is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
