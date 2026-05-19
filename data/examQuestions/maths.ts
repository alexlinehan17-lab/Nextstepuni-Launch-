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
    taskType: 'maths-section-a-algebra',
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
        debrief: {
          strategicPrinciple: "Identifying command words is the first step before writing — each one sets up a separately-marked item. This question has TWO: 'Solve' (part a) and 'Show that...justify each step' (part b). Spotting them before answering anchors your time budget per command.",
          commonWrongAnswer: {
            answer: '1',
            reason: "Students count only 'Solve' and miss 'Show that' / 'Justify each step' as a single composite command. The marking scheme treats each separately-credited demand as its own item — and 'justify each step' adds a procedural-justification mark on top of the show-that derivation.",
          },
        },
      },
      {
        id: 'time-allocation',
        prompt: 'Roughly how many minutes should this question take?',
        type: 'number',
        correctAnswer: 12,
        hint: '25 marks out of 300 on a 150-minute paper.',
        debrief: {
          strategicPrinciple: 'HL Maths runs at half a minute per mark (150 min / 300 marks). 25 marks → ~12-13 minutes.',
          commonWrongAnswer: {
            answer: '25',
            reason: 'Students conflate "marks" with "minutes" on the first read. The 2015 Maths CER noted top HL candidates "made a determined effort to complete the entire examination paper" and "persevere in solving problems even when, because of errors, the numerical values were not user-friendly" (p.20) — but that perseverance only works if the time budget is correct. 25 marks at 0.5 min/mark = 12.5 minutes.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.20' },
          },
        },
      },
      {
        id: 'sum-roots-rule',
        prompt: 'Which rule gives the sum of the roots most efficiently?',
        type: 'short-text',
        hint: 'Relates the coefficients of a quadratic to its roots.',
        debrief: {
          strategicPrinciple: "For a quadratic ax² + bx + c = 0, sum of roots = −b/a, product = c/a (Vieta's formulas). 'Show that the sum is 2.5' becomes a one-line proof using the coefficients of part (a) — not a re-derivation from the solved roots.",
          commonWrongAnswer: {
            answer: 'Solve the equation and add the roots',
            reason: 'Students re-solve part (a) and sum the answers — works, but uses 4-5 lines for a result Vieta gives in one. The 2015 Maths CER noted top HL candidates "showed a good depth of understanding of the whole syllabus, along with an ability to be both flexible and accurate in their work, and to bring knowledge and skills from a number of different strands to bear on a given question" (p.27) — recognising when −b/a applies is exactly that strand-bridging move.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.27' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Re-deriving when Vieta gives the answer in one line',
      body: "Q1(b) asks you to 'show that' the sum of roots equals 2.5. The lazy path re-solves part (a) and sums; the elegant path uses sum of roots = −b/a directly — a one-line proof from the coefficients. The 2015 Maths CER consistently noted that top HL candidates 'showed a good depth of understanding of the whole syllabus, along with an ability to be both flexible and accurate in their work' (p.27) — the flexibility is recognising when a less-obvious formula gives a tighter proof. Plus: 'Justify each step' requires naming the rule ('by Vieta's formulas') — a bare algebraic line without justification loses procedural marks.",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.27' },
    },
  },
  {
    id: 'maths-2025-ord-p1-q3',
    taskType: 'maths-section-a-algebra',
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
        debrief: {
          strategicPrinciple: 'OL Maths runs at half a minute per mark. 30 marks gets 15 minutes — across all three sub-parts, not per part.',
          commonWrongAnswer: {
            answer: '5',
            reason: 'Students see 10 marks per sub-part and budget 5 minutes per sub-part. Multiplying gives 15 minutes for the question, but it also signals they are budgeting per-part rather than per-question, which under-runs on the harder sub-part and over-runs on the easier one.',
          },
        },
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
        debrief: {
          strategicPrinciple: 'Maths marking schemes award credit per visible procedural step, not just for the final answer. The wording "Use calculations to support" makes the requirement explicit — without the per-bar calculation, the marker has no procedure to credit.',
          commonWrongAnswer: {
            answer: 'You can just tick the correct box and skip the working',
            reason: 'Students treat "Use calculations to support your answer" as polite framing rather than a marking-scheme cue. The 2015 Chief Examiner Report noted that "marks are generally not awarded for an incorrect answer without any supporting work" — and the inverse: a correct conclusion without working is capped at the final-answer mark only.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.31' },
          },
        },
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
        debrief: {
          strategicPrinciple: 'Dividing or multiplying an inequality by a negative flips the sign. Reaching −4x ≥ −12 is High Partial Credit; the flip is what unlocks full credit. The 2015 Maths CER flagged that OL candidates "struggled noticeably with questions that involved any significant amount of algebra" — this is exactly the kind of procedural rule that gets skipped under time pressure.',
          commonWrongAnswer: {
            answer: 'It stays the same: x ≥ 3',
            reason: 'Students follow the procedural muscle memory from positive-coefficient inequalities. The flip is a rule learned but easily forgotten — and the wrong direction passes a sanity check (x ≥ 3 is a reasonable-looking solution), so there is no internal signal to catch it.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.17' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Treating "Use calculations" as optional framing',
      body: 'All three parts of Q3 turn on showing visible procedural work. (a) explicitly demands calculations; (b) requires the inequality-flip step to be visible; (c)(ii) requires consistent use of YOUR k and t from (c)(i). The 2015 Maths CER is explicit: marks are awarded for procedures that would lead to a solution even when the final answer is wrong — and conversely, a correct answer without supporting work is generally not credited beyond the final-answer mark. Every line you write is a separately-marked component.',
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.31' },
    },
  },
  {
    id: 'maths-2025-ord-p1-q4',
    taskType: 'maths-section-a-calculus',
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
        debrief: {
          strategicPrinciple: 'OL Maths runs at half a minute per mark. 30 marks gets 15 minutes, distributed across sub-parts roughly in mark proportion: (a) 5 marks → 2.5 mins, (b) 10 marks → 5 mins, (c) 15 marks → 7.5 mins.',
          commonWrongAnswer: {
            answer: '10',
            reason: 'Students treat 30 marks as "about 10 minutes" from rough memory, under-budgeting and leaving themselves no margin on the heavier (c) sub-part. The per-mark rule keeps the proportion right between sub-parts.',
          },
        },
      },
      {
        id: 'q4b-substitute',
        prompt: "Part (b) asks for f′(x), then 'Hence, find the slope of the tangent at (2, −4)'. Once you have f′(x), what do you substitute x = 2 into?",
        type: 'multiple-choice',
        options: ['f(x)', 'f′(x)', 'Both f(x) and f′(x)', 'Neither — graph it'],
        correctAnswer: 'f′(x)',
        debrief: {
          strategicPrinciple: "The slope of a tangent is the value of the derivative at the point. 'Hence' means use the f′(x) you just computed — substitute x = 2 into f′(x), not f(x). The marking scheme awards zero credit for substituting into f.",
          commonWrongAnswer: {
            answer: 'f(x)',
            reason: 'Students see the point (2, −4) and substitute x = 2 into the function that gave them the y-coordinate — natural reflex. The 2015 Maths CER documented this exact confusion at HL: candidates "did not know that solving f′(x) = 0 would yield the x-coordinates of the turning point of the function. In many instances, candidates sought to solve f″(x) = 0 instead, which illustrated a lack of comprehension of the concept of a turning point and its relationship to the derivative." Same family of error: applying the wrong order of derivative.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
          },
        },
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
        debrief: {
          strategicPrinciple: "'Give a reason' is a command word — each command earns marks separately. The marking-scheme convention treats every command in a question as a separately-credited item: labelled sub-parts, named answers, AND reasons.",
          commonWrongAnswer: {
            answer: 'Optional — the matching in (c)(i) gets all the credit',
            reason: 'Students read "give a reason" as flavour text — the matching already feels like the answer. A one-line sentence ("P is a turning point" or "the slope of the tangent at P is zero") is the entire requirement. The 2015 Maths CER noted that strong OL candidates wrote a clear conclusion alongside their calculation — "some candidates wrote the equation, substituted, calculated — and then forgot to write the conclusion. This loses marks" (p.22).',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.22' },
          },
        },
      },
    ],
    biggestMistake: {
      title: "Substituting into f instead of f′ — and skipping 'give a reason'",
      body: 'Q4 spans three sub-parts but two errors carry most of the lost marks. (b) tests whether you substitute into f′(x) or f(x) — the marking scheme is explicit that substituting into f earns zero. (c)(ii) tests whether you write the one-line reason — skipping it drops a level of credit. The 2015 Maths CER documented the f vs f′ confusion at HL (p.21); at OL the pattern is the same, often amplified by "I\'ll just compute and move on." Both are 30-second writes that lock in the marks.',
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
    },
  },
  {
    id: 'maths-2025-ord-p1-q7',
    taskType: 'maths-section-b-functions-graphing',
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
        debrief: {
          strategicPrinciple: 'OL Maths runs at half a minute per mark. 50 marks → 25 minutes — a sixth of the paper on one question. Going past 25 means another sub-part later runs short.',
          commonWrongAnswer: {
            answer: '10',
            reason: 'Students see "10 marks → 5 mins" from earlier per-part allocations and round the 50-mark whole-question budget down by reflex. The per-mark rule scales linearly: 50 × 0.5 = 25 minutes.',
          },
        },
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
        debrief: {
          strategicPrinciple: "'During which... increased by the greatest amount' specifies a CHANGE over a time period, not a level at a moment. The biggest change is May (€1.20) → June (€6.00) = +€4.80, so the answer is May.",
          commonWrongAnswer: {
            answer: 'March (highest value reached)',
            reason: 'Students read "greatest amount" and pick the month with the highest value. The phrase "during which... increased" picks out a delta, not an absolute. The 2015 Maths CER documented that strong OL candidates "presented the relevant formula, substituted correctly, did the calculation, and gave the answer... as required" — clean reading first. Mid-band candidates skim the question and substitute the first interpretation that fits.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.23' },
          },
        },
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
        debrief: {
          strategicPrinciple: 'Percentage error = error / true value × 100. So true value = error / percentage. The arithmetic is a division (1.50 ÷ 0.163 ≈ €9.20), not a multiplication (which returns €0.24 — clearly not a share value).',
          commonWrongAnswer: {
            answer: '1·50 × 0·163',
            reason: 'Students see a percentage and reach for multiplication — the rote pattern from "find X% of Y" questions. The 2015 Maths CER noted OL candidates "struggled noticeably with questions that involved any significant amount of algebra" (p.17); rearranging error/value = percentage to solve for value is exactly this kind of algebraic step. A sanity check (€0.24 for a share value? €9.20 fits the graph?) would catch it.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.17' },
          },
        },
      },
      {
        id: 'q7e-natural',
        prompt: 'Q7(e)(ii): solving for when Company B falls below €2 gives n = 24·06… Because n ∈ ℕ and the value must fall BELOW €2, n is:',
        type: 'multiple-choice',
        options: ['24', '25', '24·06', 'Either 24 or 25'],
        correctAnswer: '25',
        debrief: {
          strategicPrinciple: 'n ∈ ℕ + "falls below €2" = round UP, not down. At n = 24, the value still equals €2; the next natural number, n = 25, is the first that pushes below. The marking scheme applies a star (Full Credit −1) for n = 24.',
          commonWrongAnswer: {
            answer: '24',
            reason: 'Students compute 24.06… and round down by reflex — truncation feels safer than rounding up. But the question requires the value to fall BELOW €2, so boundary cases don\'t count. The 2015 Maths CER documented a related pattern at HL — candidates "did not test the resulting roots" on squared equations, "assuming instead that both solutions would satisfy the original equation" (p.21). Same family: not checking whether the candidate solution actually satisfies the question\'s constraint.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
          },
        },
      },
    ],
    biggestMistake: {
      title: "Misreading 'during which' and rounding the wrong direction",
      body: "Q7's marks are scattered across five sub-parts and each one rewards a single careful parse: (a)(ii) wants the month a CHANGE happened, not the highest value; (b) wants both a calculation AND a plot; (c) wants division by the percentage (not multiplication); (e)(ii) wants the next natural number, not the truncated one. The 2015 Maths CER noted top OL candidates 'presented the relevant formula, substituted correctly, did the calculation, and gave the answer correct to two decimal places with the relevant unit' (p.23) — clean reading, clean execution. Q7 is where 'I'll skim and substitute' costs you the band.",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.23' },
    },
  },
  {
    id: 'maths-2025-ord-p1-q8',
    taskType: 'maths-section-b-functions-graphing',
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
        debrief: {
          strategicPrinciple: 'OL Maths runs at half a minute per mark. 50 marks → 25 minutes. Q8 has three sub-parts at 20+15+15 — budget proportionally to keep the chain moving.',
          commonWrongAnswer: {
            answer: '15',
            reason: 'Students under-budget the big questions because they feel intimidating. 50 marks × 0.5 min/mark = 25 mins — that\'s a sixth of the paper on this single question.',
          },
        },
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
        debrief: {
          strategicPrinciple: "'AND explain what it means' is a separately marked item. Marking-scheme convention treats every command in a question as separately credited — the calculation gets one mark band, the explanation gets another. Skipping the sentence drops a level of credit.",
          commonWrongAnswer: {
            answer: '0 marks — the number is the answer',
            reason: 'Students write "−4" and move on, treating "explain" as polite framing. The 2015 Maths CER noted that strong OL candidates wrote a clear conclusion alongside their calculation — some candidates "wrote the equation, substituted, calculated — and then forgot to write the conclusion. This loses marks" (p.22). Same pattern: the explanation is the conclusion the marker is looking for.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.22' },
          },
        },
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
        debrief: {
          strategicPrinciple: "Maximum/minimum of a function ⇒ derivative equals zero. Find Q′(x), set Q′(x) = 0, solve for x. Then substitute that x back into Q(x) — not Q′(x) — for the maximum value.",
          commonWrongAnswer: {
            answer: 'Substitute x = 0',
            reason: 'Students see "maximum" and substitute the first available x (often a boundary like 0 or 7). The 2015 Maths CER documented this confusion at HL: candidates "sought to solve f″(x) = 0 instead, which illustrated a lack of comprehension of the concept of a turning point and its relationship to the derivative" (p.21). Same family: misapplying the derivative-to-extremum link.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
          },
        },
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
        debrief: {
          strategicPrinciple: 'R(x) + 3 puts the +3 OUTSIDE the function — every y-value increases by 3, a vertical shift up. R(x + 3) would put the +3 INSIDE the function input and shift the graph LEFT by 3 (because R is now evaluated 3 units earlier).',
          commonWrongAnswer: {
            answer: 'Shifting it down by 3',
            reason: 'Students see "+ 3" and reach for whichever direction first comes to mind. The rule (+ outside = up, + inside = left) is procedural but easily skipped under time pressure. The 2015 Maths CER noted OL candidates "struggled noticeably with questions that involved any significant amount of algebra" (p.17) — graph transformations are exactly this kind of rule-based algebra that gets dropped when the question feels visual.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.17' },
          },
        },
      },
    ],
    biggestMistake: {
      title: "Reading 'explain' and 'hence' as polite framing",
      body: "Q8 has three sub-parts and each one rewards reading the command word literally. (a)(i) demands BOTH a number AND a one-sentence explanation — the explanation carries marks. (b)(i)/(ii) chain via 'hence' — find Q′(x), set it to zero, then substitute back into Q(x) (not Q′(x)). (c)(ii) tests whether you can distinguish R(x) + 3 (vertical shift up) from R(x + 3) (horizontal shift left). The 2015 Maths CER noted strong OL candidates 'presented the relevant formula, substituted correctly, did the calculation, and gave the answer correct to two decimal places with the relevant unit, as required' (p.23). Q8 is full of 'as required' moments.",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.23' },
    },
  },
  {
    id: 'maths-2025-ord-p2-q7',
    taskType: 'maths-section-b-probability',
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
        debrief: {
          strategicPrinciple: "For 'at least 1' questions, the complement (1 − P(none)) is one calculation; the direct sum is three. Both score full marks if correct — the complement just has fewer steps to slip on.",
          commonWrongAnswer: {
            answer: 'Direct sum P(WW) + P(WL) + P(LW)',
            reason: "Reads 'at least 1' as 'count all win-bearing outcomes' — mathematically valid, but three multiplications plus an addition instead of one subtraction. The 2015 Maths CER noted top OL candidates 'presented the relevant formula, substituted correctly, did the calculation, and gave the answer correct to two decimal places with the relevant unit' — clean order, fewer error points.",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.23' },
          },
        },
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
        debrief: {
          strategicPrinciple: "When the question specifies 'first loss is the third game,' the sequence W, W, L is fixed — multiply along that single path. Combinations would apply for 'exactly one loss in three games', where the loss could fall anywhere.",
          commonWrongAnswer: {
            answer: 'Use ³C₁ × 0·22',
            reason: "Students hear 'three games' and reach for combinatorial machinery — a rote pattern from Bernoulli trials. The 2015 Maths CER flagged this exact failure mode on OL counting questions: candidates 'simply worked with a factorial (6!), while others worked with ⁿPᵣ, neither of which displays any appreciable level of understanding' — deploying ⁿCᵣ/ⁿPᵣ without parsing what the question is actually counting.",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
          },
        },
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
        debrief: {
          strategicPrinciple: "The volume formula uses radius, not diameter. Halving the diameter is a one-second operation, but it's the single most-skipped step on sphere questions — and the answer is off by a factor of 8 (since r³ scales cubically).",
          commonWrongAnswer: {
            answer: 'Substitute 18 directly as r',
            reason: "Students see a number and substitute. The diameter value is sitting right there next to the formula — the cognitive shortcut is to plug it in. A sanity check (does 5832 sound like the volume of a child's football?) would catch it, but most OL candidates don't run the check.",
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Substituting the first number you see without checking what it is',
      body: "Q7 is four small procedures — each one tests whether you read what the question actually asks before reaching for the formula. (a)(iii) tests 'at least 1' vs 'exactly 1'. (b)(ii) tests 'first loss is the third game' (sequence) vs 'one loss in three games' (combination). (c)(i) tests diameter vs radius. The 2015 Maths CER consistently identified this as the OL/HL behavioural difference: top OL candidates 'presented the relevant formula, substituted correctly, did the calculation, and gave the answer correct to two decimal places with the relevant unit' (p.23). Mid-band candidates substitute the first number they see.",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.23' },
    },
  },
  {
    id: 'maths-2025-ord-p2-q8',
    taskType: 'maths-section-b-statistics',
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
        debrief: {
          strategicPrinciple: "Calculations + Conclusion + Reason. The (c)(iii) marking rule explicitly applies Full Credit −1 if either conclusion OR reason is missing or incorrect. The calculation alone caps you below full marks.",
          commonWrongAnswer: {
            answer: 'Just the calculation',
            reason: 'Students compute the confidence interval [9.5, 16.5] and stop, treating "state your conclusion, and give a reason" as polite framing. The OL marking convention treats each command word as a separately credited item — three commands = three items.',
          },
        },
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
        debrief: {
          strategicPrinciple: 'Correlation coefficient r is bounded: −1 ≤ r ≤ 1. Any value outside that range is mathematically impossible. The range itself is the reason "r = 5" is wrong, not just that 5 feels large.',
          commonWrongAnswer: {
            answer: 'r must be a whole number',
            reason: 'Students invent a constraint to rule out 5 without recalling the actual bound. The 2015 Maths CER noted OL candidates "struggled noticeably with questions that involved any significant amount of algebra" (p.17) — the [−1, 1] bound is a procedural fact, easily forgotten under pressure.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.17' },
          },
        },
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
        debrief: {
          strategicPrinciple: 'OL margin of error at 5% significance is 1/√n. HL uses 1·96·√(p̂(1−p̂)/n). Don\'t import the HL formula onto an OL paper — the OL marking scheme expects 1/√n exactly.',
          commonWrongAnswer: {
            answer: '1·96 × √(p̂(1−p̂)/n)',
            reason: 'Students conflate OL and HL formulae. The 2015 Maths CER documented that cohort migration was reshaping grade distributions — many candidates "would previously have done OL are now doing HL" (p.27), and the reverse pattern (OL candidates exposed to HL material) leads them to reach for the more sophisticated formula. The marker awards on the OL convention only.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.27' },
          },
        },
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
        debrief: {
          strategicPrinciple: "'Show that' means the answer is given; demonstrate the working that produces it. Stating '3.5%' is not the answer — the working IS the answer. Without the derivation (ME = 1/√815 = 0.03503… = 3.5%), the marker has nothing to credit.",
          commonWrongAnswer: {
            answer: 'Just write 3·5% as the answer',
            reason: "Students treat 'show that' as confirmation, not derivation. The 2015 Maths CER is explicit: 'marks are generally not awarded for an incorrect answer without any supporting work, whereas if candidates show a procedure which would lead to a solution, then they may get credit for this' (p.31). 'Show that' inverts the rule — the correct answer alone gets no credit because the marking scheme is testing whether you can derive it.",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.31' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Stopping at the calculation — and importing the HL formula',
      body: "Q8 is statistics-heavy: pie chart, correlation, hypothesis test. Two failure modes carry most of the lost marks. (c)(iii) explicitly requires THREE items — calculation, conclusion, reason; the marking scheme applies a star if conclusion or reason is missing. (c)(i) tests the OL margin-of-error formula (1/√n), which mixed-cohort candidates often substitute the HL formula for. The 2015 Maths CER: 'Marks are generally not awarded for an incorrect answer without any supporting work, whereas if candidates show a procedure which would lead to a solution, then they may get credit for this' (p.31) — and conversely, a correct answer without the demanded conclusion + reason is capped at the calculation mark only.",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.31' },
    },
  },
  {
    id: 'maths-2025-ord-p2-q9',
    taskType: 'maths-section-b-geometry',
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
        debrief: {
          strategicPrinciple: "Lengths scale by k; areas scale by k². Doubling a triangle's side quadruples its area. For enlargements: bigger area / smaller area = k², not k. Volumes scale by k³ — same logic.",
          commonWrongAnswer: {
            answer: 'k',
            reason: "Students apply the scale factor uniformly to everything — lengths AND areas — without distinguishing dimension. The 2015 Maths CER pinpointed this exact pattern as the defining OL P2 weakness: 'Many candidates struggled with the construction of the centre of enlargement and the subsequent determination and application of scale factor' (p.22) — enlargements were the lowest-mean OL P2 question at 46%.",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.22' },
          },
        },
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
        debrief: {
          strategicPrinciple: "'Maximum' + 'needs at least' = floor, not round. 11.6 means 12 participants would each get 58 cm — short of the 60 cm constraint. So 11 is the actual maximum.",
          commonWrongAnswer: {
            answer: 'Because rounding 11·6 gives 12',
            reason: "Students round to nearest by reflex. The 2015 Maths CER documented a related failure mode at HL — candidates 'did not test the resulting roots, assuming instead that both solutions would satisfy the original equation' (p.21). Same family of error: not checking whether the rounded answer actually satisfies the question's constraint (60 cm per person).",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
          },
        },
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
        debrief: {
          strategicPrinciple: 'Centroid = intersection of MEDIANS (vertex to midpoint of opposite side). The other three: circumcentre = perpendicular bisectors, incentre = angle bisectors, orthocentre = altitudes. Four named centres; the centroid is the only one that\'s a balance point.',
          commonWrongAnswer: {
            answer: 'Perpendicular bisectors of the sides',
            reason: "Students learn the four triangle centres as a set and confuse the constructions. Both centroid and circumcentre involve lines drawn from sides — easy to swap under pressure. The 2015 Maths CER noted OL candidates 'struggled with the construction of the centre of enlargement' (p.22); construction-of-named-points more broadly remains a recurring OL weak spot.",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.22' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'k² for areas — the most-failed enlargement rule',
      body: "Q9 turns on three named procedural rules: centroid = medians (not perpendicular bisectors); areas scale by k² (not k); 'maximum needing at least' = floor (not round). The 2015 Maths CER pinpointed this exact category as the lowest-mean OL P2 question at 46%: 'Many candidates struggled with the construction of the centre of enlargement and the subsequent determination and application of scale factor' (p.22). Each rule is a single line of work, but each carries a sub-part's worth of marks.",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.22' },
    },
  },
  {
    id: 'maths-2025-ord-p2-q10',
    taskType: 'maths-section-b-trigonometry',
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
        debrief: {
          strategicPrinciple: 'Two sides + included angle, want AREA → ½ ab sin C. (Cosine rule finds a missing side; sine rule finds missing angles in non-right triangles; Pythagoras only works for right-angled triangles.) Formula choice turns on what is given and what is wanted.',
          commonWrongAnswer: {
            answer: 'Cosine rule',
            reason: 'Students see "triangle + included angle" in their formula bank and reach for cosine rule by reflex — but cosine rule returns a side, not an area. The 2015 Maths CER noted OL candidates "struggled noticeably with questions that involved any significant amount of algebra" (p.17); choosing among trig formulae is exactly this kind of structural decision that gets skipped under time pressure.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.17' },
          },
        },
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
        debrief: {
          strategicPrinciple: 'Routes have order: A→B→C→A and A→C→B→A are DIFFERENT sequences of swims. Order matters → permutation (ⁿPᵣ), not combination (ⁿCᵣ). ⁵P₂ = 5×4 = 20.',
          commonWrongAnswer: {
            answer: 'Same route — combination (⁵C₂ = 10)',
            reason: 'Students see "pick 2 from 5" and reach for combinations — the rote pattern. The 2015 Maths CER flagged this exact failure mode at OL on a parallel counting question: candidates "simply worked with a factorial (6!), while others worked with ⁿPᵣ, neither of which displays any appreciable level of understanding" (p.21) — deploying counting machinery without parsing whether order matters.',
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
          },
        },
      },
      {
        id: 'q10-decompose',
        type: 'short-text',
        prompt: 'How does ABCDEF decompose into shapes you can find areas of?',
        hint: 'Two triangles plus a rectangle.',
        debrief: {
          strategicPrinciple: "ABCDEF = two congruent triangles (ABC, DEF) + rectangle ACDF in the middle. The 'hence' in (iv) is the cue — use the |AC| you just found as one side of the rectangle. Decomposition turns a 'six-sided shape' into three formula applications you already know.",
          commonWrongAnswer: {
            answer: 'Treat it as one shape and search for a hexagon formula',
            reason: "Students look for a single polygon-area formula instead of decomposing. The decomposition is the strategic move; once you see two triangles + a rectangle, the formula choice is just 2 × ½ab sin C + length × width. The 2015 Maths CER noted that strong OL candidates 'presented the relevant formula, substituted correctly, did the calculation, and gave the answer correct to two decimal places with the relevant unit' (p.23) — clean decomposition is what makes the formula choice trivial.",
            source: { year: 2015, type: 'chief-examiner', pageRef: 'p.23' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Combinations vs permutations, and the wrong trig formula for area',
      body: "Q10 spans trig and counting; each sub-part has a single high-value choice. (a)(ii) chooses between ½ ab sin C (for area) and cosine rule (for sides) — pick the one matching what you need to find. (a)(iv) uses 'hence' to chain (iii)'s |AC| into a decomposition (two triangles + rectangle). (b)(ii) is 5! (not 6! — A is fixed). (b)(iii) is ⁵P₂ (not ⁵C₂ — routes have order). The 2015 Maths CER documented this exact OL counting-confusion pattern: 'Many students simply worked with a factorial (6!), while others worked with ⁿPᵣ, neither of which displays any appreciable level of understanding' (p.21).",
      source: { year: 2015, type: 'chief-examiner', pageRef: 'p.21' },
    },
  },
];
