/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert Business exam questions for the Exam Strategiser.
 * 2025 Higher Level. Source: SEC paper + marking scheme.
 *
 * All entries authored to the new schema (per-prompt `debrief` + question-
 * level `biggestMistake`) per /CLAUDE.md § "Strategiser content quality
 * rules". Examiner sources: 2025 marking scheme primarily; 2015 Chief
 * Examiner's Report for cross-cutting behavioural patterns.
 */

import { type ExamQuestion } from '../../types/examStrategiser';

export const businessQuestions: ExamQuestion[] = [
  // ── Section 1 Q7 — Gearing + Debt/Equity Ratio ────────────────────
  {
    id: 'business-2025-hl-s1-q7',
    subject: 'business',
    taskType: 'business-section-1-short',
    year: 2025,
    paper: 'Section 1',
    section: 'Section 1 — Short Response',
    questionNumber: '7',
    level: 'higher',
    marks: 10,
    totalPaperMarks: 400,
    totalPaperMinutes: 180,
    commandWords: ['Explain', 'Calculate'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: '(a) ' },
          { text: 'Explain the term Gearing', annotation: { type: 'command', note: 'Definition + concept. Mark scheme: 3 marks for the core definition, 2 marks for elaboration (e.g. lowly vs highly geared, or what the ratio measures).' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'The following are the figures relating to Korn Ltd for 2024:' },
        ],
      },
      {
        type: 'list-item',
        content: [{ text: 'Authorised Share Capital — €900,000' }],
      },
      {
        type: 'list-item',
        content: [
          { text: 'Issued Share Capital', annotation: { type: 'keyword', note: 'This is the equity figure to use, not Authorised. Authorised (€900,000) is the maximum the company is allowed to issue; only Issued (€550,000) is actual equity. Mixing them is the most common error on this question type.' } },
          { text: ' — €550,000' },
        ],
      },
      {
        type: 'list-item',
        content: [{ text: 'Long Term Loan — €300,000' }],
      },
      {
        type: 'list-item',
        content: [
          { text: 'Reserves/Retained Earnings', annotation: { type: 'keyword', note: 'Reserves count as equity. Equity = Issued Share Capital + Reserves = €550,000 + €50,000 = €600,000.' } },
          { text: ' — €50,000' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(b) ' },
          { text: 'Calculate the Debt/Equity Ratio', annotation: { type: 'command', note: 'Mark scheme: 5 marks awarded as 5×1 — one mark for each of: identifying Debt, identifying Equity, substituting, calculating, and expressing as a ratio.' } },
          { text: '. ' },
          { text: 'Show your workings', annotation: { type: 'trap', note: 'NOT decorative. The 5 marks are split across 5 procedural steps. Stating "0.5:1" without showing Debt ÷ Equity caps you at the final-answer mark only.' } },
          { text: '. ' },
          { text: '(10)', annotation: { type: 'marks-allocation', note: 'Mark scheme: (a) 3+2 (b) 5@1m. Spend ~4.5 mins.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q7-equity',
        type: 'multiple-choice',
        prompt: 'For the Debt/Equity ratio, which capital figure goes in Equity?',
        options: [
          'Authorised Share Capital (€900,000)',
          'Issued Share Capital + Reserves (€600,000)',
          'Authorised Share Capital + Reserves (€950,000)',
          'Issued Share Capital only (€550,000)',
        ],
        correctAnswer: 'Issued Share Capital + Reserves (€600,000)',
        debrief: {
          strategicPrinciple: '"Issued" is what the company actually has; "Authorised" is just the cap on what it could issue. Reserves are equity.',
          commonWrongAnswer: {
            answer: 'Authorised Share Capital (€900,000)',
            reason: 'Students see "Share Capital" and pick the bigger number, missing the Issued/Authorised distinction the question deliberately tests by listing both.',
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Q7 support notes p.14' },
          },
        },
      },
      {
        id: 'q7-workings',
        type: 'multiple-choice',
        prompt: 'You write "0.5:1" as your answer with no working shown. What\'s the maximum mark out of 5?',
        options: ['5/5', '4/5', '1/5', '0/5'],
        correctAnswer: '1/5',
        debrief: {
          strategicPrinciple: 'The 5 marks for part (b) are explicitly split across 5 procedural steps — not one mark for the answer.',
          commonWrongAnswer: {
            answer: '5/5 — "the answer is right"',
            reason: "Students treat 'show your workings' as a polite suggestion. The Section 1 Q7 marking template `5@1m` treats each step (Debt identified, Equity identified, substitution, calculation, ratio) as a separately-counted mark.",
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Section 1 marking grid p.5' },
          },
        },
      },
      {
        id: 'q7-time',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend on this 10-mark question?',
        correctAnswer: 5,
        hint: '400 marks ÷ 180 mins ≈ 0.45 mins/mark.',
      },
    ],
    biggestMistake: {
      title: 'Skipping the substitution line',
      body: 'In Section 1 calculation questions, the marking grid treats each procedural step as a separately-counted mark. The 2025 scheme awards Q7(b) as `5@1m`: identifying Debt, identifying Equity, substitution, calculation, ratio. Students write "0.5:1" with the formula `D/E` underneath and assume the marker will fill in the gaps. The marker awards what is on the page, not what is implied. Show every line.',
      source: { year: 2025, type: 'marking-scheme', pageRef: 'Q7 marking grid p.5; support notes p.14' },
    },
  },

  // ── Section 2 — Applied Business Question (Inis Bia) ──────────────
  {
    id: 'business-2025-hl-s2-abq',
    subject: 'business',
    taskType: 'business-abq',
    year: 2025,
    paper: 'Section 2',
    section: 'Section 2 — Applied Business Question (Inis Bia)',
    questionNumber: 'ABQ',
    level: 'higher',
    marks: 80,
    totalPaperMarks: 400,
    totalPaperMinutes: 180,
    commandWords: ['Outline', 'Evaluate', 'Recommend', 'Describe'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Inis Bia was founded by Trisha Owens in 2020. Trisha was a chef and noticed a change in consumer tastes; she set up healthy readymade meals after redundancy. The business expanded nationally. Challenges followed: a major customer went into liquidation owing money; vegetable supplier changes caused inconsistency, costing a UK contract; Trisha struggled to keep accurate records. To facilitate expansion, Trisha appointed Michael Walsh as Human Resources manager. He introduced a buddy system, HR check-ins, and a 3-year loyalty payment.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(A) Skills (20 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Outline the entrepreneurial skills/characteristics displayed by Trisha. ' },
          { text: 'Refer to the text in your answer', annotation: { type: 'command', note: 'Mark scheme: 4@5 (2+2+1) — Name (2) + Explain (2) + LINK (1). Four skills required, each with a direct quote from the case.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(B) Management Control (30 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Evaluate the effectiveness', annotation: { type: 'command', note: 'Mark scheme: 4@7 (1+2+1+3) — Name (1) + Explain (2) + Link (1) + EVALUATE (3). Evaluation is the heaviest single component. Naming and explaining the control type without judging whether it worked at Inis Bia caps you at 4/7 per type.' } },
          { text: ' of the types of management control in place at Inis Bia. (ii) ' },
          { text: 'Recommend', annotation: { type: 'keyword', note: 'Worth 2 marks. Pick ONE control type and propose a specific improvement (e.g. for credit control: credit checks, interest payments, limits on credit sales).' } },
          { text: ' how one type of control could be improved.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(C) HRM Functions (30 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Describe the functions of human resource management (HRM) at Inis Bia. Refer to the text in your answer. ' },
          { text: '(80)', annotation: { type: 'marks-allocation', note: '20% of the entire paper. ~36 mins. P 30 / C 30 / L 30 / M 10 not enforced — instead each part has its own structural grid (see annotations on each sub-part).' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'abq-link-rule',
        type: 'multiple-choice',
        prompt: 'You write a perfect 3-paragraph explanation of "Innovation" as an entrepreneurial skill but don\'t quote anything from the case. What\'s the maximum mark out of 5 for that skill?',
        options: ['5/5', '4/5', '3/5', '0/5 — "no link awarded without relevant theory" cuts both ways'],
        correctAnswer: '4/5',
        debrief: {
          strategicPrinciple: 'The 5 marks per skill split as Name (2) + Explain (2) + LINK (1). Strong theory still earns the Name + Explain marks, but the link mark requires a direct case quote — "Separate links are required in each section."',
          commonWrongAnswer: {
            answer: '5/5 — "the explanation is good enough"',
            reason: 'Students underestimate how mechanical the ABQ marking is. Each skill is its own 5-mark sub-grid, and the link mark is 1 of 5 — non-substitutable.',
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Section 2 marking note p.6 and support notes p.18-19' },
          },
        },
      },
      {
        id: 'abq-comprehension-trap',
        type: 'multiple-choice',
        prompt: 'You quote the case extensively, paraphrase what Trisha did, but don\'t invoke any business theory. Mark out of 80?',
        options: ['Around 60', 'Around 40', 'Around 20', 'Close to 0'],
        correctAnswer: 'Close to 0',
        debrief: {
          strategicPrinciple: 'The ABQ is theory + linked quote, in that order. The 2015 Chief Examiner\'s Report explicitly flags case-summary as one of two failure modes that score little or nothing.',
          commonWrongAnswer: {
            answer: 'Around 40 — "I covered the case in detail"',
            reason: 'Students treat the ABQ as a comprehension piece, especially under time pressure. The 2025 marking scheme is explicit: "No link awarded without relevant theory." A perfect quote with no business term scores 0 for that point.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.15' },
          },
        },
      },
      {
        id: 'abq-evaluate',
        type: 'multiple-choice',
        prompt: "In Part (B)(i), the marking grid is `4@7 (1+2+1+3)`. Which component is worth the most marks per control type?",
        options: ['Naming the control type', 'Explaining the theory', 'Linking to the case', 'Evaluating effectiveness'],
        correctAnswer: 'Evaluating effectiveness',
        debrief: {
          strategicPrinciple: 'Evaluation is 3 of the 7 marks per control type — more than naming, explaining, and linking combined. Stopping at "this is quality control, here\'s the link" forfeits nearly half the available marks per type.',
          commonWrongAnswer: {
            answer: 'Explaining the theory',
            reason: 'Students lean toward the part they\'ve studied most — definitions of control types. They write rich explanations and run out of time before judging whether each control actually worked at Inis Bia.',
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Section 2 grid p.6' },
          },
        },
      },
      {
        id: 'abq-time',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend on the ABQ?',
        correctAnswer: 36,
        hint: '80 marks × 0.45 mins/mark.',
      },
    ],
    biggestMistake: {
      title: 'Treating links as decorative',
      body: 'The single largest mark loss across the ABQ comes from broken links — either business theory written with no case quote, or case material rewritten with no theory. The 2025 marking scheme is explicit that "no link awarded without relevant theory" and "separate links are required in each section." A separate, direct quote per point is the only structure that scores. Plan one clearly-marked quote per skill / control / function before writing.',
      source: { year: 2025, type: 'marking-scheme', pageRef: 'Section 2 marking note p.6' },
    },
  },

  // ── Section 3 Q1 — People in Business ──────────────────────────────
  {
    id: 'business-2025-hl-s3-q1',
    subject: 'business',
    taskType: 'business-people-in-business',
    year: 2025,
    paper: 'Section 3',
    section: 'Section 3 Part 1 — People in Business',
    questionNumber: '1',
    level: 'higher',
    marks: 60,
    totalPaperMarks: 400,
    totalPaperMinutes: 180,
    commandWords: ['Illustrate', 'Explain', 'Define', 'List'],
    questionText: [
      {
        type: 'subpart-label',
        content: [{ text: '(A) Contract Elements (20 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Illustrate', annotation: { type: 'command', note: '"Illustrate" requires Explain + Example. Mark scheme: 4@5 (4+1)(4+1)(3+2)(3+2). First two elements: 4m explain + 1m example. Last two: 3m explain + 2m example. Skipping the example caps you per element.' } },
          { text: ' your understanding of the following essential elements of a valid contract: ' },
          { text: 'Consideration, Capacity to Contract, Consent to Contract, Legality of form', annotation: { type: 'keyword', note: 'All FOUR required. Doing 3 caps at 15/20.' } },
          { text: '. (20)' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(B) Industrial Action (20 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Explain, ' },
          { text: 'using examples', annotation: { type: 'command', note: 'Mark scheme: 4@5 (2+2+1) — Name (2) + Explain (2) + Example (1). FOUR types required. Examples not optional.' } },
          { text: ', the different types of industrial action. (20)' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(C) Discrimination (20 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Define discrimination', annotation: { type: 'command', note: 'Worth 8 marks for the definition alone. Must reference the comparison ("less favourable treatment than another person") and the protected grounds.' } },
          { text: ' as set out in the Employment Equality Act 1998/2015. (ii) ' },
          { text: 'List four grounds', annotation: { type: 'trap', note: 'Marking grid: 8 marks (3, 3, 1, 1). First two grounds named earn 3 each; next two earn only 1 each. Listing more than 4 wastes time. EXPLAINING the grounds wastes marks — the cue is "List", not "outline".' } },
          { text: ' other than gender and sexual orientation on which discrimination is outlawed. ' },
          { text: '(60)', annotation: { type: 'marks-allocation', note: '~27 mins total. Allocate ~9 mins per 20-mark sub-part.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q1-illustrate',
        type: 'multiple-choice',
        prompt: '"Illustrate" each contract element. What does that command word require?',
        options: [
          'A precise definition only',
          'Explain + give an example',
          'List the elements',
          'Discuss the element\'s history',
        ],
        correctAnswer: 'Explain + give an example',
        debrief: {
          strategicPrinciple: '"Illustrate" = Explain + Example. The marking grid is `(4+1)` per element — explanation worth 3-4 marks, example worth 1-2. Skipping the example caps you per element.',
          commonWrongAnswer: {
            answer: 'A precise definition only',
            reason: 'Students treat "Illustrate" as a synonym for "Define". The 2015 Chief Examiner Report calls out the recurring HL pattern: strong definitions followed by inadequate answers to the actual question that uses them.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.16-17' },
          },
        },
      },
      {
        id: 'q1-list',
        type: 'multiple-choice',
        prompt: 'For Q1(C)(ii) "List four grounds", you write paragraphs explaining each ground in detail. What happens?',
        options: [
          "You earn extra marks for thoroughness",
          'No effect — same mark as a list',
          'The cue is "List" — explanation earns nothing extra; you waste time you needed for other parts',
          'You\'re penalised for not following instructions',
        ],
        correctAnswer: 'The cue is "List" — explanation earns nothing extra; you waste time you needed for other parts',
        debrief: {
          strategicPrinciple: '"List" rewards brevity only. The marking grid is `(3, 3, 1, 1)` — first two grounds at 3m, next two at 1m. The grounds named are the entire score; explanation is unscored.',
          commonWrongAnswer: {
            answer: 'No effect — same mark as a list',
            reason: 'Students assume more = better. The 2015 Chief Examiner Report identified this exact behaviour: "some candidates wrote paragraphs to explain the protected grounds rather than just naming the grounds, as was required."',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.17' },
          },
        },
      },
      {
        id: 'q1-list-grounds',
        type: 'short-text',
        prompt: 'Excluding gender and sexual orientation, name four grounds protected under the Employment Equality Act.',
        hint: 'Civil status, family status, disability, religion, race, age, membership of the Traveller community.',
      },
    ],
    biggestMistake: {
      title: 'Ignoring the question cue',
      body: 'Q1 is the Section 3 question that punishes cue-mismatches most heavily because it spans three different cues across its three parts: "Illustrate" (A), "Explain using examples" (B), "List" (C). Students who default to one register — usually thorough explanation — overshoot on (C) and underdeliver on (A). The 2025 marking grids reward the cue, not the volume.',
      source: { year: 2025, type: 'marking-scheme', pageRef: 'Q1 grid p.7' },
    },
  },

  // ── Section 3 Q8 — Business in Action (P&G) ────────────────────────
  {
    id: 'business-2025-hl-s3-q8',
    subject: 'business',
    taskType: 'business-business-in-action',
    year: 2025,
    paper: 'Section 3',
    section: 'Section 3 Part 2 — Business in Action (Proctor & Gamble)',
    questionNumber: '8',
    level: 'higher',
    marks: 60,
    totalPaperMarks: 400,
    totalPaperMinutes: 180,
    commandWords: ['Explain', 'Illustrate', 'Describe'],
    questionText: [
      {
        type: 'subpart-label',
        content: [{ text: '(A) Product portfolio + Market segmentation (20 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Explain the term ' },
          { text: 'product portfolio', annotation: { type: 'keyword', note: '6 marks (3+3). Definition + elaboration. "A collection/range of all products and services a company offers."' } },
          { text: '. (ii) ' },
          { text: 'Illustrate', annotation: { type: 'command', note: 'Mark scheme: 2@7 (2+3+2) — Method named (2) + Explain (3) + Reference (2). TWO methods required — not four.' } },
          { text: ' the different methods of market segmentation used by businesses such as Proctor and Gamble.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(B) Market Research Reasons (15 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Describe', annotation: { type: 'command', note: 'Mark scheme: 3@5 (3+2) — Name (3) + Explain (2). THREE reasons required at 5m each.' } },
          { text: ' the reasons why a business conducts market research.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(C) Breakeven Chart (25 marks)' }],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Forecast Output: 200,000 units. Selling Price: €10/unit. Fixed Costs: €600,000. Variable Costs: €5/unit.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Illustrate ' },
          { text: 'by means of a breakeven chart', annotation: { type: 'trap', note: 'Without a chart drawn, the marking scheme caps you at 12/25. Chart breakdown: Title 2m, Axes 1+1m, Fixed Costs line 3m, Total Costs line 3m, Total Revenue line 3m, BEP marked 4m, Profit 4m, Margin of Safety 4m.' } },
          { text: ': (i) Breakeven point. (ii) Margin of safety at the forecast output. (iii) Profit at the forecast output. ' },
          { text: '(60)', annotation: { type: 'marks-allocation', note: '~27 mins total. Note unequal split: A=20m, B=15m, C=25m. The breakeven chart alone is 25m — give it ~11 mins.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q8-chart-or-calc',
        type: 'multiple-choice',
        prompt: 'You do the breakeven calculations perfectly (BEP=120k units, MoS=80k, profit=€400k) but don\'t draw the chart. Maximum mark out of 25?',
        options: ['25/25', '20/25', '12/25', '4/25'],
        correctAnswer: '12/25',
        debrief: {
          strategicPrinciple: 'The 2025 marking grid for Q8(C) lists two paths explicitly: WITH chart = up to 25 marks; calculations only = max 12 marks (BEP 4 + Profit 4 + MoS 4). The chart carries 13 of the 25 marks.',
          commonWrongAnswer: {
            answer: '25/25 — "the maths is right"',
            reason: 'Students who run short on time skip the chart and rely on numerical answers. The chart isn\'t a presentation flourish — it\'s explicitly the majority of the marks.',
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Q8(C) grid p.11; support notes p.51' },
          },
        },
      },
      {
        id: 'q8-chart-labels',
        type: 'multiple-choice',
        prompt: 'You draw a perfect breakeven chart but forget to add a title. Marks lost?',
        options: ['0', '1', '2', '4'],
        correctAnswer: '2',
        debrief: {
          strategicPrinciple: 'The chart is graded line-by-line. Title = 2m. Each axis label = 1m. FC, TC, TR lines = 3m each. Each marked point (BEP, profit, MoS) = 4m. Missing one component costs that exact number of marks.',
          commonWrongAnswer: {
            answer: '0 — the chart is otherwise correct',
            reason: 'Students treat title and axis labels as decoration. The marking is granular and unforgiving — same trap pattern as Geography\'s "diagram without labels = 0" rule.',
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Q8(C) grid p.11' },
          },
        },
      },
      {
        id: 'q8-segmentation-count',
        type: 'multiple-choice',
        prompt: '(A)(ii) "Illustrate the different methods of market segmentation". How many methods does the marking grid expect?',
        options: ['One', 'Two', 'Three', 'Four'],
        correctAnswer: 'Two',
        debrief: {
          strategicPrinciple: 'Mark scheme: 2@7 — exactly two methods, each at 7 marks. Listing four methods at 3 marks each is wasted breadth at the cost of depth on each.',
          commonWrongAnswer: {
            answer: 'Four',
            reason: 'Students assume "different methods" implies an exhaustive list. The grid weights two well-developed methods over four shallow ones — two examples at 7 marks each (Method named 2 + Explain 3 + Reference 2).',
            source: { year: 2025, type: 'marking-scheme', pageRef: 'Q8(A)(ii) grid p.11' },
          },
        },
      },
      {
        id: 'q8-bep',
        type: 'number',
        prompt: 'Quick check — what\'s the breakeven point in units? (FC=€600,000, Selling Price=€10, Variable Cost=€5/unit)',
        correctAnswer: 120000,
        hint: 'BEP = Fixed Costs ÷ Contribution per unit. Contribution per unit = Selling Price − Variable Cost.',
      },
    ],
    biggestMistake: {
      title: 'Treating the chart as optional',
      body: 'The single biggest mark loss on Q8(C) is skipping the breakeven chart in favour of "just the calculations." The 2025 marking scheme explicitly caps calculations-only at 12 of 25 marks (48%). The chart\'s marking grid awards 2 marks for the title, 1 mark per axis label, 3 marks per cost/revenue line, 4 marks per marked point. A student who gets every number right but draws nothing is automatically below pass mark on this sub-part.',
      source: { year: 2025, type: 'marking-scheme', pageRef: 'Q8(C) grid p.11; support notes p.51' },
    },
  },
];
