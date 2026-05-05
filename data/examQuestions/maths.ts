/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Placeholder Maths questions — used to verify Exam Strategiser rendering.
 * Real Leaving Cert questions to be authored in subsequent prompts.
 */

import { type ExamQuestion } from '../../types/examStrategiser';

export const mathsQuestions: ExamQuestion[] = [
  {
    id: 'maths-placeholder-2024-p1-q1',
    subject: 'maths',
    year: 2024,
    paper: 'Paper 1',
    section: 'Algebra',
    questionNumber: '1',
    level: 'higher',
    marks: 25,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['Solve', 'Show'],
    questionText: [
      {
        type: 'subpart-label',
        content: [{ text: '(a)' }],
      },
      {
        type: 'paragraph',
        content: [
          {
            text: 'Solve',
            annotation: {
              type: 'command',
              note: 'Solve = find the value(s) of the unknown. Always present the final answer clearly, e.g. "x = 3 or x = -2", not buried in a line of working.',
            },
          },
          { text: ' the equation ' },
        ],
      },
      {
        type: 'formula',
        content: [{ text: '2x² − 5x − 3 = 0' }],
      },
      {
        type: 'spacer',
        content: [{ text: '' }],
      },
      {
        type: 'subpart-label',
        content: [{ text: '(b)' }],
      },
      {
        type: 'paragraph',
        content: [
          {
            text: 'Show that',
            annotation: {
              type: 'command',
              note: '"Show that" = prove the result step-by-step. The final answer is given to you — markers want the working, not the answer. No working = no marks.',
            },
          },
          { text: ' the sum of the roots of the equation in part (a) is ' },
          {
            text: '2.5',
            annotation: {
              type: 'keyword',
              note: 'The result is given. Use the relationship between coefficients and roots: sum of roots = -b/a. Avoid solving from scratch — examiners reward the elegant route.',
            },
          },
          { text: '. ' },
          {
            text: 'Justify each step',
            annotation: {
              type: 'trap',
              note: '"Justify each step" means name the rule you are using (e.g. "by Vieta\'s formulas"). A bare line of algebra without justification loses procedural marks.',
            },
          },
          { text: '.' },
        ],
      },
      {
        type: 'spacer',
        content: [{ text: '' }],
      },
      {
        type: 'paragraph',
        content: [
          {
            text: '(25 marks)',
            annotation: {
              type: 'marks-allocation',
              note: '25 out of 300 marks on a 150-minute paper = ~12 minutes. This is meant to be a quick win — do not over-engineer it.',
            },
          },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'command-words',
        prompt: 'How many command words does this question contain?',
        type: 'multiple-choice',
        options: ['1', '2', '3', '4'],
        correctAnswer: '2',
        hint: 'Look at the start of part (a) and part (b).',
      },
      {
        id: 'time-allocation',
        prompt: 'Roughly how many minutes should this question take?',
        type: 'number',
        correctAnswer: 12,
        hint: '25 marks out of 300 on a 150-minute paper.',
      },
      {
        id: 'sum-roots-rule',
        prompt: 'Which rule gives the sum of the roots most efficiently?',
        type: 'short-text',
        hint: 'Relates the coefficients of a quadratic to its roots.',
      },
    ],
    topAnswerIncludes: [
      'The two roots of part (a) presented clearly: x = 3 or x = -1/2',
      'For part (b), use of -b/a (or Vieta\'s) rather than re-solving',
      'Each step labelled with the rule applied',
      'Final result restated to confirm what was asked',
    ],
    commonTraps: [
      'Solving part (b) from scratch instead of using sum-of-roots',
      'Skipping justification — markers cannot award procedural marks for unjustified steps',
    ],
  },
  {
    id: 'maths-2025-ord-p1-q3',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 1',
    section: 'A',
    questionNumber: '3',
    level: 'ordinary',
    marks: 30,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['Solve', 'Use calculations', 'Write down', 'Use'],
    questionText: [
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Best value comparison' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Rickie is buying protein bars. The cost of a single protein bar is €3·30. A shop has the following offers:' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Offer A: 3 bars for the price of 2 bars. Offer B: 12-pack of the same bar for €29·99.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Which offer is ' },
          { text: 'cheaper', annotation: { type: 'keyword', note: 'You must compare like-for-like — cost per bar is the cleanest unit. Offer A: (2×3.30)/3 = €2·20/bar. Offer B: 29.99/12 = €2·50/bar.' } },
          { text: ' per bar? ' },
          { text: 'Use calculations to support your answer.', annotation: { type: 'command', note: 'Ticking the box without working only gets you Low Partial Credit. The calculation IS where most of the marks live.' } },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Inequality' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Solve', annotation: { type: 'command', note: 'Treat as an equation — but watch the sign when dividing or multiplying by a negative.' } },
          { text: ' the inequality for x ∈ ℝ:  2x + 4 ≥ 6x − 8' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Working leads to ' },
          { text: '−4x ≥ −12', annotation: { type: 'trap', note: 'Dividing by −4 FLIPS the inequality: x ≤ 3, NOT x ≥ 3. The marking scheme awards High Partial Credit just for reaching −4x ≥ −12 — full credit needs the flip.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Factor pairs and quadratic expansion' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'k × t = 12, where k, t ∈ ℤ. (i) ' },
          { text: 'Write down', annotation: { type: 'command', note: 'Low-effort command — pick ANY valid integer pair: (1,12), (2,6), (3,4), (4,3), (6,2), (12,1) all work.' } },
          { text: ' a possible value of k and the corresponding value of t.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) ' },
          { text: 'Use', annotation: { type: 'command', note: 'You must use YOUR k and t from (i). (x+k)(x+t) = x² + (k+t)x + kt — so b = k + t. k=6, t=2 → b=8. k=3, t=4 → b=7. Either is correct, depending on (i).' } },
          { text: ' your values for k and t from (c)(i) to find b in: (x + k)(x + t) = x² + bx + 12' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q3-time',
        prompt: 'Q3 is worth 30 marks on a 300-mark, 150-minute paper. How many minutes should you spend?',
        type: 'number',
        correctAnswer: 15,
        hint: 'Marks ÷ 2 = minutes (300 marks / 150 minutes).',
      },
      {
        id: 'q3a-calc',
        prompt: "In part (a), what does 'Use calculations to support your answer' mean for your marks?",
        type: 'multiple-choice',
        options: [
          'You can just tick the correct box and skip the working',
          'The working is required for full marks — ticking alone gets only Low Partial Credit',
          'Calculations are optional unless you get the answer wrong',
          'You only need calculations if you choose Offer B',
        ],
        correctAnswer: 'The working is required for full marks — ticking alone gets only Low Partial Credit',
      },
      {
        id: 'q3b-flip',
        prompt: 'In part (b), once you reach −4x ≥ −12, what happens to the inequality sign when you divide both sides by −4?',
        type: 'multiple-choice',
        options: [
          'It stays the same: x ≥ 3',
          'It flips: x ≤ 3',
          'You can write either — both are correct',
          'You should leave it as −4x ≥ −12',
        ],
        correctAnswer: 'It flips: x ≤ 3',
      },
    ],
    topAnswerIncludes: [
      'Part (a): Like-for-like comparison (cost per bar) with both calculations shown — Offer A: €6·60/3 = €2·20, Offer B: €29·99/12 = €2·50. Tick Offer A.',
      'Part (b): Transposes correctly, isolates x, FLIPS the inequality when dividing by −4, ends at x ≤ 3.',
      'Part (c)(i): Any valid integer pair where k × t = 12.',
      'Part (c)(ii): Uses the EXACT values from (c)(i) — b = k + t (so b = 8 if you picked k=6,t=2; b=7 if k=3,t=4).',
    ],
    commonTraps: [
      "Ticking 'Offer A' in (a) without showing the per-bar comparison — Low Partial Credit only.",
      'Forgetting to flip the inequality sign when dividing by a negative — easily costs you a level of credit.',
      'In (c)(ii), using values different to those given in (c)(i) — answer must be consistent.',
      'Treating ≥ like > and excluding x = 3 from the solution.',
    ],
  },
  {
    id: 'maths-2025-ord-p1-q4',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 1',
    section: 'A',
    questionNumber: '4',
    level: 'ordinary',
    marks: 30,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['Solve', 'Find', 'Hence', 'Write', 'give a reason'],
    questionText: [
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: '5 marks → 2·5 mins' } },
          { text: ' Linear equation' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Solve', annotation: { type: 'command', note: 'Three independently-marked steps: distribute, transpose, solve.' } },
          { text: ' the following equation in a ∈ ℝ:  5(a − 3) = 2a + 7' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Differentiation and slope of tangent' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'f(x) = x³ − 3x² + 4x − 8, where x ∈ ℝ.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Find', annotation: { type: 'command', note: 'Differentiate term-by-term. f′(x) = 3x² − 6x + 4.' } },
          { text: ' f′(x), the derivative of f(x). ' },
          { text: 'Hence', annotation: { type: 'command', note: '"Hence" means USE what you just found. Slope of the tangent at (2, −4) = f′(2), NOT f(2).' } },
          { text: ', find the slope of the tangent to f(x) at the point (2, −4).' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'The most common error: ' },
          { text: 'substituting x = 2 into f(x) instead of f′(x)', annotation: { type: 'trap', note: 'The marking scheme is explicit: "zero credit for substituting 2 into f". The slope of a tangent ALWAYS comes from the derivative.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: '15 marks → 7·5 mins' } },
          { text: ' Reading derivatives from a graph' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'A cubic g(x) is shown. P sits at a local maximum (top of the curve), Q is on the descending part between P and the trough, R is on the ascending part after the trough.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Match each of P, Q, R to the correct derivative description: g′(x) < 0, g′(x) = 0, g′(x) > 0.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) For the point matched to g′(x) = 0, ' },
          { text: 'give a reason', annotation: { type: 'command', note: 'Easy mark, easily missed. One sentence is enough: "P is a turning point" OR "the slope of the tangent at P is zero".' } },
          { text: ' for your answer.' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q4-time',
        prompt: 'Q4 is worth 30 marks. How many minutes should you spend on it?',
        type: 'number',
        correctAnswer: 15,
      },
      {
        id: 'q4b-substitute',
        prompt: "Part (b) asks for f′(x), then 'Hence, find the slope of the tangent at (2, −4)'. Once you have f′(x), what do you substitute x = 2 into?",
        type: 'multiple-choice',
        options: ['f(x)', 'f′(x)', 'Both f(x) and f′(x)', 'Neither — graph it'],
        correctAnswer: 'f′(x)',
      },
      {
        id: 'q4c-reason',
        prompt: "Part (c)(ii) asks you to 'give a reason'. How important is writing the reason?",
        type: 'multiple-choice',
        options: [
          'Optional — the matching in (c)(i) gets all the credit',
          "It's one of the four marked items in this part — skipping it drops a level of credit",
          'It is worth most of part (c)',
          "Reasons aren't marked at Ordinary Level",
        ],
        correctAnswer: "It's one of the four marked items in this part — skipping it drops a level of credit",
      },
    ],
    topAnswerIncludes: [
      'Part (a): Three clean steps — distribute (5a − 15 = 2a + 7), transpose (3a = 22), solve (a = 22/3).',
      'Part (b): f′(x) = 3x² − 6x + 4. Then f′(2) = 12 − 12 + 4 = 4. Slope = 4.',
      'Part (c)(i): Q matches g′(x) < 0; P matches g′(x) = 0; R matches g′(x) > 0.',
      'Part (c)(ii): One-line reason — "P is a turning point" or "the slope of the tangent at P is zero".',
    ],
    commonTraps: [
      'Substituting x = 2 into f(x) instead of f′(x) in part (b) — zero credit per the marking scheme.',
      'Distributing the 5 incorrectly in (a) — writing 5a − 3 instead of 5a − 15.',
      'Skipping the reason in (c)(ii) — costs a level of credit even with (c)(i) perfect.',
      'Mixing up Q and R — Q is on the descending side (negative slope), R on the ascending side.',
    ],
  },
  {
    id: 'maths-2025-ord-p1-q7',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 1',
    section: 'B',
    questionNumber: '7',
    level: 'ordinary',
    marks: 50,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['estimate', 'identify', 'plot', 'find', 'complete', 'draw', 'fill in'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Context: a graph shows the value of one share for Company A, in euro, on the 1st of each month from January to July. Approximate values from the graph: Jan €4·00, Feb €5·00, Mar €7·30, Apr €2·30, May €1·20, Jun €6·00, Jul €8·00.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Reading the graph' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'estimate', annotation: { type: 'command', note: 'Read directly from the graph — not a calculation. Answer: €7·30 (1st March).' } },
          { text: ' the value of one share on 1st March.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Use the graph to identify the month ' },
          { text: 'during which', annotation: { type: 'keyword', note: 'NOT "in which the value is highest". This asks for the month during which the value INCREASED the most. Biggest jump is May (€1·20) to June (€6·00) = +€4·80 — answer is May.' } },
          { text: ' the value of one share increased by ' },
          { text: 'the greatest amount', annotation: { type: 'trap', note: 'Easy to misread as "highest value" (March) or "highest endpoint" (July). Answer is the start month of the biggest increase: May.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: '5 marks → 2·5 mins' } },
          { text: ' Plot a calculated point' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'On 1st August the value of one share was 15% lower than 1st July. ' },
          { text: 'Estimate the value AND plot the point.', annotation: { type: 'command', note: 'TWO requirements: calculation AND plot. €8·00 × 0·85 = €6·80, then plot at (Aug, 6·80). High Partial Credit for the value alone — full credit needs the plot.' } },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Percentage error' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Liam predicts the value of one share. The error in his prediction is €1·50, which is a percentage error of 16·3%. Find the value of one share (to the nearest cent).' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Common mistake: ' },
          { text: 'doing 1·50 × 0·163 instead of 1·50 ÷ 0·163', annotation: { type: 'trap', note: 'Percentage error = error / true value × 100. So 1·50 / true value = 0·163 → true value = 1·50 / 0·163 ≈ €9·20.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(d)', annotation: { type: 'marks-allocation', note: '15 marks → 7·5 mins' } },
          { text: ' Exponential model for Company B' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'P(m) = 2 × 1·29ᵐ where m is months since 1st January, 0 ≤ m ≤ 6. Given values: P(0)=2, P(2)=3·33, P(6)=9·22.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Complete the table for m = 1, 3, 4, 5. (ii) Draw P(m) on the same diagram as Company A. (iii) The two curves cross only once — ' },
          { text: 'in which month must this have happened', annotation: { type: 'keyword', note: 'A is a piecewise line, B is a smooth exponential curve. They cross only once — early on, around March. Read off the graph.' } },
          { text: '?' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(e)', annotation: { type: 'marks-allocation', note: '10 marks → 5 mins' } },
          { text: ' Linear decline after peak' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'After 1st July (peak), Company B declines linearly at 30 cent/month. Q(n) = ___ − 0·3n where n is months after the peak.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Fill in the missing number', annotation: { type: 'command', note: 'The missing number is the share value AT the peak — P(6) = 9·22.' } },
          { text: ' to complete Q(n).' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Find how many months until Company B falls below its 1st January value (€2). ' },
          { text: 'Remember n ∈ ℕ', annotation: { type: 'trap', note: 'Solving 2 = 9·22 − 0·3n gives n = 24·06… Because we need the value to fall BELOW €2, and n is a natural number, ROUND UP to n = 25, NOT 24. The marking scheme applies a star (Full Credit −1) for n = 24.' } },
          { text: '.' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q7-time',
        prompt: 'Q7 is worth 50 marks. How many minutes should you spend?',
        type: 'number',
        correctAnswer: 25,
      },
      {
        id: 'q7a-greatest',
        prompt: "Q7(a)(ii) asks for the month 'during which' the value increased by the greatest amount. The answer is:",
        type: 'multiple-choice',
        options: [
          'March (highest value reached)',
          'May (start of the biggest jump, May→June)',
          'July (highest endpoint of the period)',
          'June (end of the biggest jump)',
        ],
        correctAnswer: 'May (start of the biggest jump, May→June)',
      },
      {
        id: 'q7c-error',
        prompt: 'Q7(c): the prediction error is €1·50 = 16·3% of the true value. To find the true value, you do:',
        type: 'multiple-choice',
        options: [
          '1·50 × 0·163',
          '1·50 ÷ 0·163',
          '16·3 ÷ 1·50',
          '0·163 − 1·50',
        ],
        correctAnswer: '1·50 ÷ 0·163',
      },
      {
        id: 'q7e-natural',
        prompt: 'Q7(e)(ii): solving for when Company B falls below €2 gives n = 24·06… Because n ∈ ℕ and the value must fall BELOW €2, n is:',
        type: 'multiple-choice',
        options: ['24', '25', '24·06', 'Either 24 or 25'],
        correctAnswer: '25',
      },
    ],
    topAnswerIncludes: [
      'Part (a)(i): €7·30 read straight from the graph at March.',
      'Part (a)(ii): May — recognised that "during which" means the month in which the biggest INCREASE happens (May→June, +€4·80).',
      'Part (b): Both 8 × 0·85 = €6·80 AND the point plotted on the graph.',
      'Part (c): Recognises error/true value = percentage error → true value = 1·50 / 0·163 ≈ €9·20.',
      'Part (d)(i): Table values P(1) = 2·58, P(3) = 4·29, P(4) = 5·54, P(5) = 7·14.',
      'Part (d)(iii): Identifies the single crossing point from the graph (around March).',
      'Part (e)(i): The missing number is 9·22 (the peak P(6)).',
      'Part (e)(ii): Solves 2 = 9·22 − 0·3n → n = 24·06… → ROUNDS UP to n = 25.',
    ],
    commonTraps: [
      "Reading 'during which the value increased by the greatest amount' as 'in which month was the value highest' — answers March instead of May.",
      'In (b): writing €6·80 but forgetting to plot the point — High Partial Credit instead of full marks.',
      'In (c): doing 1·50 × 0·163 = €0·24 instead of 1·50 ÷ 0·163 = €9·20.',
      'In (e)(i): writing the slope (−0·3) again instead of the peak value (9·22).',
      'In (e)(ii): rounding DOWN to n = 24 — Full Credit −1 in the marking scheme (boundary case where value would equal €2, not fall below).',
    ],
  },
  {
    id: 'maths-2025-ord-p1-q8',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 1',
    section: 'B',
    questionNumber: '8',
    level: 'ordinary',
    marks: 50,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['Find', 'explain', 'Complete', 'Draw', 'estimate', 'Hence'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: "Context: a company's first-year profit is modelled by P(x) = −1·5x² + 10·5x − 4, where P(x) is in millions of euro and x is the number of phones in tens of thousands, 0 ≤ x ≤ 7." },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: '20 marks total → 10 mins' } },
          { text: ' First-year profit model' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Find P(0) AND explain what it means in the context', annotation: { type: 'command', note: 'TWO requirements: a number AND a sentence. P(0) = −4. Explanation: producing zero phones gives a loss of €4 million. Both halves carry marks (Scale 5C).' } },
          { text: ' of the question. (5 marks)' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Complete the table for P(x) at x = 0, 2, 3, 4, 6, 7 (values 5 and 11 given for x = 1 and x = 5). (iii) Draw the graph of P(x) for 0 ≤ x ≤ 7.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iv) Use your graph to estimate the range of x for which the profit is ' },
          { text: 'at least €6 million', annotation: { type: 'keyword', note: '"At least" = ≥, so the answer is the closed interval. Read off the graph: 1·2 ≤ x ≤ 5·8.' } },
          { text: '. ' },
          { text: 'Show your work on the graph.', annotation: { type: 'command', note: 'Draw the horizontal line at y = 6 and mark where it crosses your curve. Without this work, the marking scheme caps you at High Partial Credit.' } },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: '15 marks → 7·5 mins' } },
          { text: ' Second-year profit — calculus' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Q(x) = −1·5x² + 9·6x − 3·5 (millions of €), 0 ≤ x ≤ 7.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Find Q′(x), and hence find the value of x', annotation: { type: 'command', note: '"Hence" = use what you just found. Q′(x) = −3x + 9·6. Set Q′(x) = 0 to find the maximum: x = 3·2.' } },
          { text: ' which gives the maximum value of Q(x). ' },
          { text: '(ii) Hence, find the maximum value of Q(x).', annotation: { type: 'command', note: 'Substitute x = 3·2 back into Q(x), NOT Q′(x). Q(3·2) = −1·5(3·2)² + 9·6(3·2) − 3·5 = €11·86 million.' } },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: '15 marks → 7·5 mins' } },
          { text: ' Third-year — graph translation' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'A graph of R(x) is given (downward parabola, peak ≈ 9·5 around x = 3, roots near x = 0·5 and x = 5·5). With €3 million additional funding, the new profit is R(x) + 3.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Estimate R(2) from the graph (≈ 8) and find R(2) + 3 = 11.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Draw the graph of y = R(x) + 3. ' },
          { text: 'This is a vertical shift', annotation: { type: 'trap', note: 'R(x) + 3 means EVERY y-value goes UP by 3. Same shape, lifted 3 units. NOT a left/right shift, NOT a stretch. Plot key points (peak, roots, y-intercept) shifted up by 3 and join smoothly.' } },
          { text: '.' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q8-time',
        prompt: 'Q8 is worth 50 marks. How many minutes should you spend?',
        type: 'number',
        correctAnswer: 25,
      },
      {
        id: 'q8a-explain',
        prompt: "Q8(a)(i) says 'Find P(0) AND explain what it means in the context'. What is the explanation worth out of 5 marks?",
        type: 'multiple-choice',
        options: [
          '0 marks — the number is the answer',
          '1–2 marks (Low Partial Credit if explanation is in shape)',
          'Half (~3 marks)',
          'All 5 marks',
        ],
        correctAnswer: '1–2 marks (Low Partial Credit if explanation is in shape)',
      },
      {
        id: 'q8b-max',
        prompt: "Q8(b)(i) says 'Find Q′(x), and hence find the value of x which gives the maximum value of Q(x).' Once you have Q′(x), what's the next step?",
        type: 'multiple-choice',
        options: [
          'Substitute x = 0',
          'Set Q′(x) = 0 and solve for x',
          'Square it',
          'Find Q′(7)',
        ],
        correctAnswer: 'Set Q′(x) = 0 and solve for x',
      },
      {
        id: 'q8c-translation',
        prompt: 'Q8(c)(ii) asks for the graph of y = R(x) + 3. This transforms R(x) by:',
        type: 'multiple-choice',
        options: [
          'Shifting it up by 3',
          'Shifting it down by 3',
          'Shifting it right by 3',
          'Shifting it left by 3',
        ],
        correctAnswer: 'Shifting it up by 3',
      },
    ],
    topAnswerIncludes: [
      'Part (a)(i): P(0) = −4 AND a sentence explaining it as a loss of €4 million if zero phones are produced.',
      'Part (a)(ii): Correct values P(0) = −4, P(2) = 11, P(3) = 14, P(4) = 14, P(6) = 5, P(7) = −4.',
      'Part (a)(iv): Horizontal line at y = 6 drawn on the graph, both intersection points marked, answer 1·2 ≤ x ≤ 5·8.',
      'Part (b)(i): Q′(x) = −3x + 9·6, sets to zero, x = 3·2.',
      'Part (b)(ii): Substitutes x = 3·2 into Q(x) (not Q′(x)) — maximum = €11·86 million.',
      'Part (c)(i): R(2) ≈ 8, R(2) + 3 = 11.',
      'Part (c)(ii): Same parabola shape lifted vertically by 3 units (peak from ≈9·5 to ≈12·5; roots and y-intercept all shift up by 3).',
    ],
    commonTraps: [
      'Part (a)(i): finding P(0) = −4 but skipping the explanation — drops a level of credit.',
      'Part (a)(iv): writing 1·2 ≤ x ≤ 5·8 with no graph work — capped at High Partial Credit.',
      'Part (b)(i): forgetting to set Q′(x) = 0; just leaving Q′(x) = −3x + 9·6 as the final answer.',
      'Part (b)(ii): substituting x = 3·2 into Q′(x) instead of Q(x) — gives 0 instead of the maximum.',
      'Part (c)(ii): translating left or right by 3, or stretching vertically by 3, instead of shifting up.',
    ],
  },
  {
    id: 'maths-2025-ord-p2-q7',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 2',
    section: 'B',
    questionNumber: '7',
    level: 'ordinary',
    marks: 50,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['complete', 'work out', 'find', 'correct to', 'in terms of'],
    questionText: [
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: 'Tree diagram + at-least-1 calc' } },
          { text: ' Tennis tree diagram (Seán)' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Seán is playing two tennis matches. He either wins or loses each match. P(win match 1) = 0·6, P(win match 2) = 0·7. The outcomes of the two matches are ' },
          { text: 'independent', annotation: { type: 'keyword', note: '"Independent" tells you to MULTIPLY along branches — no conditional probability needed.' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Tree diagram (described): match 1 splits into W₁ (0·6) and L₁ (?). Each of those splits into W₂ and L₂. Given leaf outcomes: P(WW) = 0·42, P(LL) = 0·12. Missing branch probabilities: P(L₁) = ?, P(L₂|W₁) = ?, P(W₂|L₁) = ?. Missing leaf outcomes: P(WL) = ?, P(LW) = ?.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iii) From the tree diagram, find the probability that Seán wins ' },
          { text: 'at least 1 match', annotation: { type: 'trap', note: '"At least 1" means 1 OR 2 wins. Cleanest: 1 − P(no wins) = 1 − 0·12 = 0·88. Direct sum 0·42 + 0·18 + 0·28 also works but more arithmetic.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: 'Independent service games (Sarah)' } },
          { text: ' Repeated independent trials' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Sarah plays tennis. Each time she plays a service game, P(win) = 0·78. Winning each service game is independent.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Probability of losing the next service game?', annotation: { type: 'command', note: 'One-step: P(loss) = 1 − P(win) = 1 − 0·78 = 0·22. Don\'t overthink.' } },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Probability that the ' },
          { text: 'first service game that Sarah loses is her third service game', annotation: { type: 'trap', note: '"First loss is the third game" means W, W, L in that order — multiply 0·78 × 0·78 × 0·22. Don\'t add. Don\'t use combinations.' } },
          { text: '? Give your answer ' },
          { text: 'correct to 3 decimal places', annotation: { type: 'command', note: 'Rounding penalty (Full Credit −1) if missing or wrong. Final answer 0·134.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: 'Sphere volume (football)' } },
          { text: ' Volume of a sphere' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) A child\'s football is a sphere with ' },
          { text: 'diameter 18 cm', annotation: { type: 'keyword', note: 'DIAMETER, not radius. Halve it to r = 9 before substituting into V = (4/3)πr³. Common error: using 18 as r.' } },
          { text: '. Find the volume, ' },
          { text: 'in terms of π', annotation: { type: 'command', note: 'Do NOT evaluate π. Leave the answer as 972π. If you write 3053·6 instead, Full Credit −1 (apply a *).' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) An adult\'s football is a sphere with volume 5424·6 cm³. Find the radius, ' },
          { text: 'correct to 1 decimal place', annotation: { type: 'command', note: 'r = ³√(5424·6 × 3 / (4π)) = 10·9 cm. Watch the cube root — common slip is forgetting it and stopping at r³.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(d)', annotation: { type: 'marks-allocation', note: 'Expected goals (E(X) = Σ x·P(x))' } },
          { text: ' Expected value' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Expected Goals (xG) measures the probability that a shot results in a goal. A team had 15 shots; the statistician assigned probabilities as follows: 6 shots at 10%, 5 shots at 20%, 3 shots at 40%, 1 shot at 70%.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Use the table to ' },
          { text: 'work out the Expected Goals', annotation: { type: 'command', note: 'Expected value: E(X) = Σ x·P(x). 6(0·1) + 5(0·2) + 3(0·4) + 1(0·7) = 3·5.' } },
          { text: ' for the team — i.e. the expected number of goals scored from these 15 shots.' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q7-at-least-1',
        type: 'multiple-choice',
        prompt: "For 'at least 1 match', what's the cleanest first move?",
        options: [
          'Direct sum P(WW) + P(WL) + P(LW)',
          '1 − P(no wins) = 1 − P(LL)',
          'Add 0·6 + 0·7',
          'Multiply 0·6 × 0·7',
        ],
        correctAnswer: '1 − P(no wins) = 1 − P(LL)',
      },
      {
        id: 'q7-third-loss',
        type: 'multiple-choice',
        prompt: "The 'first loss is the third game' question. What does the order tell you?",
        options: [
          'Add the probabilities',
          'Multiply in order: W, W, L → 0·78 × 0·78 × 0·22',
          'Use ³C₁ × 0·22',
          'It doesn\'t matter — just compute P(L)',
        ],
        correctAnswer: 'Multiply in order: W, W, L → 0·78 × 0·78 × 0·22',
      },
      {
        id: 'q7-diameter',
        type: 'multiple-choice',
        prompt: 'Diameter is 18 cm. First step before using V = (4/3)πr³?',
        options: [
          'Substitute 18 directly as r',
          'Halve it: r = 9',
          'Square it',
          'Cube it',
        ],
        correctAnswer: 'Halve it: r = 9',
      },
    ],
    topAnswerIncludes: [
      'Tree completed: P(L₁) = 0·4, P(L₂|W₁) = 0·3, P(W₂|L₁) = 0·7; P(WL) = 0·18, P(LW) = 0·28',
      'P(at least 1 win) = 1 − 0·12 = 0·88',
      'P(loss next service game) = 1 − 0·78 = 0·22',
      'P(W,W,L) = 0·78 × 0·78 × 0·22 = 0·134 (3 d.p.)',
      'V = (4/3)π(9)³ = 972π cm³ (in terms of π — do not evaluate)',
      'r = ³√(5424·6 × 3 / (4π)) ≈ 10·9 cm (1 d.p.)',
      'E(X) = 6(0·1) + 5(0·2) + 3(0·4) + 1(0·7) = 3·5 expected goals',
    ],
    commonTraps: [
      "'At least 1' read as 'exactly 1' — student computes only WL + LW and forgets WW",
      "Adding 0·78 + 0·78 + 0·22 instead of multiplying for 'first loss = third game'",
      'Using diameter 18 as the radius in the volume formula',
      "Evaluating π in (c)(i) when 'in terms of π' is explicitly stated → Full Credit −1",
      'Forgetting the cube root in (c)(ii) and reporting r³ ≈ 1295',
      'Not rounding (b)(ii) to 3 d.p. → Full Credit −1',
      "(d): treating the 'Number of shots' row as probabilities, or only summing one row",
    ],
  },
  {
    id: 'maths-2025-ord-p2-q8',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 2',
    section: 'B',
    questionNumber: '8',
    level: 'ordinary',
    marks: 50,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['complete', 'work out', 'show that', 'explain', 'test the claim'],
    questionText: [
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: 'Pie chart from a frequency table' } },
          { text: ' New car sales 2023 — pie chart' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'A table shows new private car sales in 2023 by fuel type, with counts (to nearest hundred), percentages (2 d.p.) and pie-chart angles. Petrol: 38 700 cars, 32·96%, 119°. Diesel: 25 900 cars, ?, ?. Fully Electric: 22 500 cars, 19·17%, ?. Hybrid: 30 300 cars, ?, 93°. Total: 117 400, 100%, 360°.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Complete the table by working out the ' },
          { text: 'two missing percentages', annotation: { type: 'command', note: '% = (count / total) × 100. Diesel: 25 900/117 400 × 100 = 22·06%. Hybrid: 30 300/117 400 × 100 = 25·81%.' } },
          { text: ' (Diesel, Hybrid) and the ' },
          { text: 'two missing angles', annotation: { type: 'command', note: 'angle = (count / total) × 360. Diesel: 79°. Fully Electric: 69°.' } },
          { text: ' (Diesel, Fully Electric). Percentages to 2 d.p., angles to nearest degree.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Complete the pie chart for Diesel, Fully Electric and Hybrid. ' },
          { text: 'Label each sector clearly with the fuel type', annotation: { type: 'command', note: 'Labelling is REQUIRED for full credit. Pie chart not fully labelled → Full Credit −1.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: 'Correlation interpretation' } },
          { text: ' Reading a scatter plot' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'A scatter plot relates engine size (x) to fuel efficiency (y) for several cars. Points trend downward from upper-left to lower-right with a clear, tight pattern.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Pick the description that best fits the correlation between engine size and fuel efficiency: Strong positive / Strong negative / Weak positive / Weak negative. ' },
          { text: 'Explain your choice', annotation: { type: 'command', note: 'TWO-PART answer: (a) tick the box, (b) write a sentence relating engine size to fuel efficiency. Both required.' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Tom says r = 5. Explain why this ' },
          { text: 'cannot be correct', annotation: { type: 'keyword', note: 'r is bounded: −1 ≤ r ≤ 1. State the range. "It\'s wrong" alone is not an explanation.' } },
          { text: '.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: 'Hypothesis test by confidence interval' } },
          { text: ' Sample of new cars 2024' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'A random sample of 815 new cars from 2024.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) ' },
          { text: 'Show that', annotation: { type: 'command', note: '"Show that" = the answer is given (3·5%); demonstrate the working. You must derive it, not just state it.' } },
          { text: ' the ' },
          { text: 'margin of error for a population proportion', annotation: { type: 'keyword', note: 'At 5% level of significance, ME = 1/√n. Don\'t use the HL formula 1·96·√(p̂(1−p̂)/n) — OL formula is just 1/√n.' } },
          { text: ' is 3·5%, correct to 1 d.p.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) 106 of the 815 new cars in the sample were electric. Find the percentage, ' },
          { text: 'correct to the nearest percent', annotation: { type: 'command', note: '106/815 × 100 = 13·006...% → 13% (nearest percent).' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iii) In 2023, 19·2% of new cars were electric. A reporter claimed 2024 is different. Use (c)(i) and (c)(ii) to ' },
          { text: 'test the claim', annotation: { type: 'command', note: 'Hypothesis test by confidence interval: build CI from p̂ ± ME, then check whether 19·2% falls inside.' } },
          { text: ' that 2024 differs from 2023, ' },
          { text: 'at the 5% level of significance', annotation: { type: 'keyword', note: 'Confirms ME = 1/√n. Confidence level = 95% (1 − 0·05).' } },
          { text: '. ' },
          { text: 'Show calculations, state your conclusion, and give a reason', annotation: { type: 'trap', note: 'THREE things required for full credit. Marking scheme: "Apply a * if either conclusion OR reason missing OR incorrect" → Full Credit −1. Don\'t stop at the calculation.' } },
          { text: '.' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q8-three-things',
        type: 'short-text',
        prompt: 'What three things does (c)(iii) require for full marks?',
        hint: 'Calculations, conclusion, reason.',
      },
      {
        id: 'q8-r-bound',
        type: 'multiple-choice',
        prompt: 'Why is r = 5 impossible?',
        options: [
          'r must be a whole number',
          'r must be positive',
          'r must satisfy −1 ≤ r ≤ 1',
          'r must be less than 1·96',
        ],
        correctAnswer: 'r must satisfy −1 ≤ r ≤ 1',
      },
      {
        id: 'q8-me-formula',
        type: 'multiple-choice',
        prompt: 'OL margin of error for a population proportion at 5% significance:',
        options: [
          '1/√n',
          '1·96 × √(p̂(1−p̂)/n)',
          '√n',
          '1·96/√n',
        ],
        correctAnswer: '1/√n',
      },
      {
        id: 'q8-show-that',
        type: 'multiple-choice',
        prompt: "'Show that ME = 3·5%' — what does it require?",
        options: [
          'Just write 3·5% as the answer',
          'Demonstrate the calculation that produces 3·5%',
          'Verify by substituting 3·5% back',
          'It\'s optional working',
        ],
        correctAnswer: 'Demonstrate the calculation that produces 3·5%',
      },
    ],
    topAnswerIncludes: [
      'Diesel: 22·06%, 79°. Hybrid: 25·81%. Fully Electric: 69°',
      'Pie chart with three new sectors drawn AND labelled (Diesel, Fully Electric, Hybrid)',
      '(b)(i): Strong negative — "cars with greater engine size are less fuel efficient"',
      '(b)(ii): "r cannot be greater than 1" / "r must lie between −1 and +1"',
      '(c)(i): ME = 1/√815 = 0·035028... = 3·5% (1 d.p.)',
      '(c)(ii): 106/815 × 100 = 13% (nearest percent)',
      '(c)(iii) calculations: 13 ± 3·5 → CI is [9·5%, 16·5%]',
      '(c)(iii) conclusion: "Reject the claim that 2024 is the same as 2023" / "There is evidence the proportion changed"',
      '(c)(iii) reason: "19·2% lies outside the CI [9·5%, 16·5%]"',
    ],
    commonTraps: [
      'Drawing pie chart sectors but not labelling them → Full Credit −1',
      "(b)(i) saying 'weak negative' when the trend is clearly strong",
      "(b)(ii) writing '5 is wrong' without giving the [−1, 1] range",
      '(c)(i) using the HL formula 1·96·√(p̂(1−p̂)/n) — OL formula is just 1/√n',
      "(c)(i) stating 3·5% without showing the derivation — fails 'Show that'",
      '(c)(iii) STOPPING at the calculation 13 ± 3·5 = [9·5, 16·5] without conclusion or reason',
      '(c)(iii) writing the conclusion but not the reason → Full Credit −1',
      '(c)(iii) comparing 13% to its own CI instead of comparing 19·2% (the 2023 value) to the 2024 CI',
    ],
  },
  {
    id: 'maths-2025-ord-p2-q9',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 2',
    section: 'B',
    questionNumber: '9',
    level: 'ordinary',
    marks: 50,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['construct', 'show', 'find', 'work out'],
    questionText: [
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: 'Construction of midpoint + centroid' } },
          { text: ' Construct the centroid' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Clodagh is making a wooden table. Triangle ABC is a scaled diagram of the table-top, supported by one leg attached to the centroid.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) On the diagram, ' },
          { text: 'construct the midpoint of [AB]', annotation: { type: 'command', note: '"Construct" = compass arcs from A and B with equal radius (> half |AB|), intersecting above and below; line through intersections crosses [AB] at the midpoint. Measurement is acceptable as backup but compass is the proper method. LABEL the point D or lose marks.' } },
          { text: '. Label the point D.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Hence, ' },
          { text: 'construct the centroid', annotation: { type: 'keyword', note: 'Centroid = INTERSECTION OF MEDIANS (lines from each vertex to the midpoint of the opposite side). At least 2 medians required. Centroid sits 2/3 along each median from the vertex. Don\'t confuse with circumcentre (perpendicular bisectors).' } },
          { text: ' of triangle ABC. Label this point O. (D and/or O not labelled → Full Credit −1.)' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: 'Enlargements: lengths × k, areas × k²' } },
          { text: ' Scale factor and enlargements' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Finn is making two triangular tables; the bigger top is an enlargement of the smaller. Scale factor k.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Longest side of bigger table = 45 cm; longest side of smaller = 36 cm. ' },
          { text: 'Show', annotation: { type: 'command', note: '"Show that" — the answer 1·25 is given. Demonstrate the calculation: k = 45/36 = 1·25.' } },
          { text: ' the scale factor k = 1·25.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Shortest side of smaller = 25·5 cm. ' },
          { text: 'Find the length of the shortest side of the bigger table-top', annotation: { type: 'command', note: 'Lengths scale by k. 25·5 × 1·25 = 31·875 → 31·9 cm (1 d.p.).' } },
          { text: ', correct to 1 d.p.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iii) Area of bigger table = 724 cm². Use k = 1·25 to find the ' },
          { text: 'area of the smaller table-top', annotation: { type: 'trap', note: 'AREAS scale by k², NOT k. Bigger = k² × smaller, so smaller = bigger / k² = 724 / 1·5625 = 463 cm². Most students multiply or divide by k once and get the wrong answer.' } },
          { text: ' (nearest cm²).' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(c)', annotation: { type: 'marks-allocation', note: 'Sectors and arc length' } },
          { text: ' Cookery demonstration table' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'A demonstration table is a sector of a circle, radius 160 cm, central angle 250°. The table has Teacher, Demonstration and Work Sections; the Work Section is a band of width 40 cm running along the outer edge.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) The shaded ' },
          { text: 'Work Section', annotation: { type: 'keyword', note: 'NOT a sector — it\'s an annular sector (sector minus smaller sector). Outer radius 160, inner radius 160 − 40 = 120. Both share the 250° angle. Area = (250/360) × π(160² − 120²).' } },
          { text: ' has width 40 cm. Find its area, nearest cm².' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Each participant needs ' },
          { text: 'at least 60 cm along the outer circumference', annotation: { type: 'keyword', note: 'Outer arc length = (250/360) × 2π(160) = 698·13 cm. Use OUTER radius (160), not inner.' } },
          { text: ' of the Work Section. ' },
          { text: 'Find the maximum number of participants', annotation: { type: 'trap', note: '698·13 / 60 = 11·6. FLOOR to 11, do NOT round to 12. "Maximum" with a "needs at least" constraint = floor function. Marking scheme: "Apply a * for answer given as 12."' } },
          { text: '.' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q9-area-scale',
        type: 'multiple-choice',
        prompt: 'Lengths scale by k. Areas scale by:',
        options: ['k', 'k²', 'k³', '√k'],
        correctAnswer: 'k²',
      },
      {
        id: 'q9-floor',
        type: 'multiple-choice',
        prompt: "Why is 'maximum number of participants' a floor, not a round?",
        options: [
          'Because rounding 11·6 gives 12',
          '"Needs at least 60 cm" means each must have ≥60 cm — 12 participants would only have 58 cm each',
          'It doesn\'t matter — both give the same answer',
          'Floor and round are the same for positive numbers',
        ],
        correctAnswer: '"Needs at least 60 cm" means each must have ≥60 cm — 12 participants would only have 58 cm each',
      },
      {
        id: 'q9-centroid',
        type: 'multiple-choice',
        prompt: 'Centroid is the intersection of:',
        options: [
          'Perpendicular bisectors of the sides',
          'Angle bisectors',
          'Medians (vertex to midpoint of opposite side)',
          'Altitudes',
        ],
        correctAnswer: 'Medians (vertex to midpoint of opposite side)',
      },
    ],
    topAnswerIncludes: [
      '(a)(i): compass arcs from A and B (equal radius) intersecting above/below [AB]; line through intersections crosses [AB] at midpoint D',
      '(a)(ii): at least two medians drawn (vertex to midpoint of opposite side); intersection labelled O',
      '(b)(i): k = 45/36 = 1·25 (shown as a calculation)',
      '(b)(ii): 25·5 × 1·25 = 31·9 cm (1 d.p.)',
      '(b)(iii): 724 / 1·5625 = 463 cm² (nearest cm²)',
      '(c)(i): (250/360) × π(160² − 120²) = (250/360) × π(11 200) = 24 435 cm² (nearest cm²)',
      '(c)(ii): outer arc = (250/360) × 2π(160) = 698·13 cm → 698·13 / 60 = 11·63... → 11 participants (FLOOR)',
    ],
    commonTraps: [
      'Measuring with a ruler instead of constructing with compass arcs',
      'Not labelling D and/or O → Full Credit −1',
      "Drawing perpendicular bisectors instead of medians (that's the circumcentre, not the centroid)",
      'k² area trap — multiplying by k once (724 × 1·25 = 905) or dividing by k once (724 / 1·25 = 579·2)',
      '(c)(i) calculating the full sector at 160 only (forgetting to subtract the inner sector)',
      '(c)(ii) using inner circumference 2π(120) instead of outer 2π(160)',
      "(c)(ii) rounding 11·6 UP to 12 — must FLOOR for 'maximum needing at least'",
    ],
  },
  {
    id: 'maths-2025-ord-p2-q10',
    subject: 'maths',
    year: 2025,
    paper: 'Paper 2',
    section: 'B',
    questionNumber: '10',
    level: 'ordinary',
    marks: 50,
    totalPaperMarks: 300,
    totalPaperMinutes: 150,
    commandWords: ['find', 'work out', 'use the cosine rule', 'hence'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Aoibhe is a member of a sea-swimming club. The club has six markers in the water: A, B, C, D, E, F.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(a)', annotation: { type: 'marks-allocation', note: 'Polygon perimeter, area, cosine rule' } },
          { text: ' Six-sided swimming course' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'ABCDEF is a six-sided shape with AF parallel to CD and AF perpendicular to AC. |AB| = |CD| = |EF| = |FA| = 200 m, and |BC| = |DE| = 150 m.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Aoibhe swims A → B → C → D → E → F → A. Find the ' },
          { text: 'total distance Aoibhe swims', annotation: { type: 'command', note: '"Total distance" = perimeter (sum of all six sides). 4×200 + 2×150 = 1100 m. Don\'t forget any sides.' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) Angle ABC = 110°. ' },
          { text: 'Work out the area', annotation: { type: 'command', note: 'Two sides AND the included angle → use ½ ab sin C. Don\'t reach for cosine rule or Pythagoras here.' } },
          { text: ', nearest m², of ' },
          { text: 'triangle ABC', annotation: { type: 'keyword', note: 'JUST the triangle, not the whole polygon. Read the question.' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iii) Aoibhe swims straight A to C. ' },
          { text: 'Use the cosine rule', annotation: { type: 'command', note: 'Method specified — must use cosine rule, not sine rule or Pythagoras. Two sides + included angle (BC, AB, ABC=110°): c² = a² + b² − 2ab·cos(C). |AC|² = 150² + 200² − 2(150)(200)·cos 110° → |AC| ≈ 288 m.' } },
          { text: ' to work out the distance from A to C, nearest metre.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iv) ' },
          { text: 'Hence, or otherwise', annotation: { type: 'keyword', note: '"Hence" = use the previous part (|AC| now known). Polygon decomposes into TWO congruent triangles (ABC and DEF) PLUS rectangle ACDF. Area = 2 × 14 095 + 200 × 288 = 85 790 m².' } },
          { text: ', work out the total area enclosed by the six markers.' },
        ],
      },
      {
        type: 'subpart-label',
        content: [
          { text: '(b)', annotation: { type: 'marks-allocation', note: 'Permutations (factorials, ⁵P₂)' } },
          { text: ' Counting routes' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Point A is the start and end for all swims.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(i) Aoibhe wants to swim from A, visiting each of B, C, D, E, F ' },
          { text: 'once and only once', annotation: { type: 'keyword', note: 'Permutation of 5 items — every marker visited exactly once, ORDER MATTERS.' } },
          { text: ', and finishing at A. (e.g. A → E → C → F → D → B → A.) Give another example.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(ii) ' },
          { text: 'Work out how many such routes are possible', annotation: { type: 'command', note: '5 markers in any order between A and A → 5! = 120 routes. Don\'t compute 6! — A is fixed at start and end, only the 5 middle markers permute.' } },
          { text: '.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: '(iii) On a particular day Aoibhe wants to start at A, swim to ' },
          { text: 'two markers other than A', annotation: { type: 'trap', note: 'Pick 2 of 5 markers WITH ORDER MATTERING (A→E→B→A is different from A→B→E→A). PERMUTATION, not combination: ⁵P₂ = 5×4 = 20, NOT ⁵C₂ = 10.' } },
          { text: ', and return to A (e.g. A → E → B → A). How many such routes are possible?' },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q10-formula',
        type: 'multiple-choice',
        prompt: 'Two sides and the included angle, want the area. Which formula?',
        options: ['Sine rule', 'Cosine rule', '½ ab sin C', 'Pythagoras'],
        correctAnswer: '½ ab sin C',
      },
      {
        id: 'q10-perm-comb',
        type: 'multiple-choice',
        prompt: '(b)(iii): Is A → B → C → A the same route as A → C → B → A? Permutation or combination?',
        options: [
          'Same route — combination (⁵C₂ = 10)',
          'Different route — permutation (⁵P₂ = 20)',
          'Same — order doesn\'t matter for round trips',
          'Different — but multiply ⁵C₂ by 2',
        ],
        correctAnswer: 'Different route — permutation (⁵P₂ = 20)',
      },
      {
        id: 'q10-decompose',
        type: 'short-text',
        prompt: 'How does ABCDEF decompose into shapes you can find areas of?',
        hint: 'Two triangles plus a rectangle.',
      },
    ],
    topAnswerIncludes: [
      '(a)(i): 4×200 + 2×150 = 1100 m',
      '(a)(ii): ½(150)(200) sin 110° = 14 095 m² (nearest m²)',
      '(a)(iii): |AC|² = 150² + 200² − 2(150)(200) cos 110° = 83 021 → |AC| = 288 m',
      '(a)(iv): 2 × 14 095 + 200 × 288 = 85 790 m² (two triangles + rectangle ACDF)',
      '(b)(i): any valid permutation, e.g. A → B → C → D → E → F → A',
      '(b)(ii): 5! = 120 routes',
      '(b)(iii): ⁵P₂ = 5 × 4 = 20 routes',
    ],
    commonTraps: [
      '(a)(i) forgetting two of the six sides',
      '(a)(ii) using cosine rule when ½ ab sin C is intended',
      '(a)(iii) using a non-included angle in the cosine rule',
      '(a)(iv) treating the polygon as one triangle, or two triangles only (missing the rectangle)',
      '(b)(ii) computing 6! — A is fixed at start and end, only 5 middle markers permute',
      '(b)(iii) using ⁵C₂ = 10 instead of ⁵P₂ = 20 — order matters',
      '(b)(iii) multiplying ⁵C₂ by 2 — ⁵P₂ already accounts for order',
    ],
  },
];
