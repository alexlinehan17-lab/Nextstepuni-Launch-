/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type SubjectModuleContent } from './subjectModuleData';

export const BUSINESS_CONTENT: Record<string, SubjectModuleContent> = {
  // ─────────────────────────────────────────────────────────────────────────
  // ACCOUNTING  (Higher Level)
  // ─────────────────────────────────────────────────────────────────────────
  accounting: {
    subjectId: 'accounting',
    subjectName: 'Accounting',
    moduleNumber: '15',
    moduleTitle: 'Mastering Accounting',
    moduleSubtitle: 'Your Complete Accounting Exam Guide',
    moduleDescription:
      'Understand the Accounting exam inside and out — the layout, mark allocation, and the specific presentation standards that separate top marks from average.',
    themeName: 'gray',
    finishButtonText: 'Balance the Books',
    sections: [
      // ── Section 1: How Accounting Actually Works ─────────────────────
      {
        title: 'How Accounting Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Leaving Certificate Accounting Higher Level exam is a **single paper** lasting **3 hours** and worth a total of **400 marks**. That is your entire result decided in one sitting, so understanding exactly how the paper is laid out is non-negotiable. There are no coursework elements, no orals, and no practicals — just this one paper and the skill you bring into the exam hall.',
          'The paper is split into [[three sections]]. **Section 1** contains short questions worth **120 marks** in total — you answer **four** out of six questions, each carrying 30 marks. These are designed to be completed relatively quickly and test breadth across the syllabus. **Section 2** has three compulsory long questions worth **60 marks each** (180 marks total). **Section 3** is one extended question worth **100 marks** — this is the big one, typically a full set of final accounts.',
          'The time pressure in Accounting is real. With 3 hours and 400 marks, you have roughly **27 seconds per mark**. That means a 100-mark question deserves about 45 minutes. Students who do not plan their time carefully run out before they reach the high-value Section 3 question, and that is where the biggest single block of marks sits.',
          'One thing that catches students off guard: [[presentation marks]] are awarded throughout the paper. The examiner is not just checking your figures — they are looking at whether your accounts are properly formatted, labelled, and laid out. Sloppy presentation loses marks even when your calculations are correct.',
        ],
        highlights: [
          {
            term: 'three sections',
            description:
              'Section 1 (120 marks, 4 short Qs), Section 2 (180 marks, 3 compulsory long Qs), Section 3 (100 marks, 1 extended Q).',
          },
          {
            term: 'presentation marks',
            description:
              'Marks awarded for correct formatting, headings, proper account layout, and double underlines on totals — not just the right numbers.',
          },
        ],
      },
      // ── Section 2: What the Examiner Rewards ────────────────────────
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Accounting examiners mark with a very specific eye. The first thing to understand is that [[correct layout]] carries its own marks in virtually every question. If you write the correct answer but present it as a list of numbers rather than a properly formatted account, you lose marks. Final accounts must have the correct headings, sub-totals, and the balance sheet must balance — format is not optional, it is examinable.',
          'The marking scheme rewards **workings**. If your final figure is wrong but your workings show a correct method, you pick up **method marks**. This is huge. Always show the steps you took to reach your answer, even in the short questions. The examiner cannot award partial credit for a wrong number if there is nothing to mark.',
          'In long questions, the examiner is looking for [[accuracy chains]]. This means one correct figure feeds into the next calculation. If your opening figure is wrong but every subsequent step is handled correctly, you still earn marks for the later steps. The marking scheme is designed to avoid penalising you twice for the same error — but only if your workings are visible.',
          'For ratio analysis and interpretation questions, examiners want you to **calculate, name the ratio, and comment**. A bare number with no label or interpretation gets minimal credit. Always state what the ratio tells you about the business and, where possible, compare it to an ideal or the previous year.',
        ],
        highlights: [
          {
            term: 'correct layout',
            description:
              'Proper headings (e.g. "Trading, Profit and Loss Account for year ended..."), double underlines, correct positioning of items, and balancing figures.',
          },
          {
            term: 'accuracy chains',
            description:
              'A marking principle where subsequent correct steps still earn marks even if an earlier figure was wrong — as long as your workings are shown.',
          },
        ],
      },
      // ── Section 3: Where Your Marks Are ────────────────────────────
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The **Section 3 question** is worth **100 marks** — that is **25% of the entire paper** in a single question. It almost always involves preparing a full set of [[final accounts]]: a Trading, Profit and Loss Account and a Balance Sheet. Some years it focuses on a sole trader, other years on a company or a manufacturing account. This question is your biggest opportunity and your biggest risk.',
          'In Section 2, the three compulsory questions (60 marks each) typically cover distinct areas. One usually involves **cash flow statements** or **club accounts**, another focuses on **published accounts** or **company accounts**, and the third often deals with **farm accounts**, **departmental accounts**, or **correction of errors and suspense**. Knowing this pattern helps you prioritise your revision.',
          'Section 1 is your [[quick wins]] zone. Each of the four short questions you answer is worth 30 marks, and they tend to test isolated skills — bank reconciliations, depreciation calculations, simple ratio work, or VAT. These are marks you can secure quickly if you have drilled the fundamentals. Do not rush them, but recognise that they are designed to reward breadth of knowledge.',
          'Here is the strategic point most students miss: **Section 1 and Section 3 together account for 220 of 400 marks** — over half the paper. If you nail the short questions and the final accounts, you are already well above the halfway line before Section 2 even comes into play.',
        ],
        highlights: [
          {
            term: 'final accounts',
            description:
              'A Trading, Profit and Loss Account plus Balance Sheet — the centrepiece of the Accounting exam, worth 100 marks in Section 3.',
          },
          {
            term: 'quick wins',
            description:
              'Section 1 short questions (120 marks total) test discrete skills and can be completed relatively quickly with solid fundamentals.',
          },
        ],
      },
      // ── Section 4: What Costs You Marks ─────────────────────────────
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mark-killer in Accounting is **poor time management**. Students spend too long perfecting Section 2 and then have 20 minutes left for a 100-mark question. You must allocate time proportionally: roughly 25 minutes for Section 1, 75 minutes for Section 2 (25 each), and 45 minutes for Section 3, with a few minutes for review.',
          'The second biggest pitfall is [[missing presentation marks]]. Students who write their balance sheet as a running list, skip headings, or forget to double-underline totals throw away marks that require zero calculation skill. Presentation marks are essentially free if you practise proper layouts — but invisible if you do not know they exist.',
          'Many students also lose marks by **not showing workings**. If a question asks you to calculate gross profit and you just write a figure, the examiner can only mark it right or wrong. If you show "Sales minus Cost of Goods Sold = Gross Profit" and your COS is slightly off, you still earn method marks for the correct process.',
          'Finally, watch out for [[adjustment traps]]. In final accounts, adjustments like closing stock, depreciation, prepayments, and accruals are where the detail marks sit. Students who skip or mishandle adjustments lose marks across multiple lines of the account — one missed adjustment can cost you 8-12 marks because it affects several totals downstream.',
        ],
        highlights: [
          {
            term: 'missing presentation marks',
            description:
              'Marks lost by skipping headings, labels, double underlines, and proper account formatting — these are marks that need no calculation.',
          },
          {
            term: 'adjustment traps',
            description:
              'Adjustments like closing stock, depreciation, accruals, and prepayments that ripple through the accounts — missing one affects multiple totals.',
          },
        ],
      },
      // ── Section 5: How to Study Accounting ──────────────────────────
      {
        title: 'How to Study Accounting',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Accounting is a **doing subject** — you cannot learn it by reading notes. The single most effective study method is [[active practice]]: sit down with a past paper question, cover up the solution, and work through it yourself. Time yourself. Check your answer against the marking scheme. Repeat. Students who do this regularly outperform those who just read over model answers every single time.',
          'Build your revision around **question types, not chapters**. Create a rotation that cycles through final accounts, cash flow statements, club accounts, published accounts, farm accounts, and correction of errors. Do at least two full past-paper questions per week from November onward. By exam time, you want to have completed every Section 3 question from the last 8-10 years.',
          'For Section 1, create a [[formula bank]] — a single A4 sheet with every formula you need: depreciation methods, ratios (current ratio, acid test, ROCE, gross profit percentage, net profit percentage), break-even calculations, and VAT rules. Test yourself on these weekly. Section 1 questions are predictable, and a student who knows every formula cold can pick up 120 marks with confidence.',
          'One underrated technique: practise your **layouts from memory**. Draw out a blank Trading, Profit and Loss Account template and a Balance Sheet template until you can produce them with correct headings and structure without looking. On exam day, this automatic recall frees your brain to focus on the actual numbers and adjustments rather than stressing about format.',
        ],
        highlights: [
          {
            term: 'active practice',
            description:
              'Working through past paper questions under timed conditions and checking against marking schemes — the core study method for Accounting.',
          },
          {
            term: 'formula bank',
            description:
              'A single-page summary of every formula, ratio, and rule needed for Section 1 — tested weekly until automatic.',
          },
        ],
        bullets: [
          'Complete every Section 3 final accounts question from the last 8-10 years',
          'Time yourself strictly: 45 minutes for 100-mark questions, 25 minutes for 60-mark questions',
          'Practise account layouts from memory until headings and format are automatic',
          'Build and test your formula bank weekly — cover ratios, depreciation, break-even, and VAT',
          'Always show workings, even in practice — build the habit before the exam',
        ],
      },
      // ── Section 6: Your Accounting Action Plan ──────────────────────
      {
        title: 'Your Accounting Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Here is your roadmap. **This week**, gather past papers from the last 10 years and the corresponding marking schemes from the SEC website. Organise them by question type: final accounts, cash flow, club accounts, published accounts, farm accounts, and correction of errors. This becomes your practice library.',
          'Start with [[Section 3 mastery]]. Do one full final accounts question per week under timed conditions (45 minutes). After completing it, go through the marking scheme line by line and note every mark you missed. Focus on adjustments and presentation. Once you can consistently score 80+ out of 100, you have secured a quarter of the paper.',
          'Simultaneously, drill Section 1 using your formula bank. Set a timer for 25 minutes and attempt four short questions. Your goal is to reach the point where Section 1 feels routine — these 120 marks should be your [[safe foundation]]. Combined with a strong Section 3, that puts you at 220 out of 400 before you even look at Section 2.',
        ],
        highlights: [
          {
            term: 'Section 3 mastery',
            description:
              'The ability to complete a full set of final accounts with correct layout and adjustments in 45 minutes — worth 100 marks (25% of the paper).',
          },
          {
            term: 'safe foundation',
            description:
              'Section 1 (120 marks) plus Section 3 (100 marks) = 220 marks secured before tackling Section 2.',
          },
        ],
        commitmentText:
          'I will complete one full Section 3 past paper question under timed conditions this week and mark it against the SEC marking scheme.',
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────────────────
  // BUSINESS  (Higher Level)
  // ─────────────────────────────────────────────────────────────────────────
  business: {
    subjectId: 'business',
    subjectName: 'Business',
    moduleNumber: '16',
    moduleTitle: 'Mastering Business',
    moduleSubtitle: 'Your Complete Business Exam Guide',
    moduleDescription:
      'Everything you need to crack the Business exam — from the ABQ to action words and the answer structures that examiners actually reward.',
    themeName: 'orange',
    finishButtonText: 'Close the Deal',
    sections: [
      // ── Section 1: How Business Actually Works ──────────────────────
      {
        title: 'How Business Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Leaving Certificate Business Higher Level exam is a **single paper** lasting **3 hours** and worth **400 marks**. It is split into [[three sections]] with very different demands, and understanding what each section asks of you is the first step toward a top grade.',
          '**Section 1** is short questions, worth **80 marks (20%)** of the total. You answer 10 out of 15 questions, each worth 8 marks. These test definitions, brief explanations, and quick recall across the entire syllabus. Section 1 is your warm-up — it should take no more than 30 minutes.',
          '**Section 2** is the [[Applied Business Question (ABQ)]], worth **80 marks (20%)**. This is a case study — a scenario about a real or fictional business — followed by three sub-questions (typically A, B, and C). The ABQ draws from **Units 3, 4, and 5** of the syllabus: Management Activities, Managing People (HR), and Enterprise and Marketing. You must link your answers directly back to the text — this is what separates the ABQ from a regular long question.',
          '**Section 3** is the long questions section, worth **240 marks (60%)**. You choose **4 from 7** questions, each worth **60 marks**. These questions can come from any unit on the syllabus and typically have sub-parts (a), (b), and sometimes (c). This is where the bulk of your marks are, and it rewards students who have studied broadly rather than gambling on specific topics.',
        ],
        highlights: [
          {
            term: 'three sections',
            description:
              'Section 1 (80 marks, short Qs), Section 2 (80 marks, ABQ case study), Section 3 (240 marks, 4 from 7 long Qs).',
          },
          {
            term: 'Applied Business Question (ABQ)',
            description:
              'A case study question worth 80 marks (20%) based on Units 3-5 (Management, HR, Enterprise, Marketing) requiring direct links to the text.',
          },
        ],
      },
      // ── Section 2: What the Examiner Rewards ────────────────────────
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Business examiners are trained to look for **structured answers**. The two answer frameworks you need are [[SEE]] and [[SEEE]]. **SEE** stands for **State, Explain, Example** — you name the concept, explain what it means, and give a relevant example. **SEEE** adds an extra E for **Elaborate** or **Evaluate**, which means you take it further by discussing advantages, disadvantages, or implications.',
          'For the ABQ in Section 2, the framework shifts to **State, Explain, Link**. The "Link" is the critical difference: you must connect your answer directly to the case study using **quotes or paraphrases** from the text. An ABQ answer without linking to the scenario is an incomplete answer, no matter how good your theory is. Examiners are specifically instructed to reward text-based linking.',
          '**Action words** in the question are your instructions. "Illustrate" means give an example. "Evaluate" means weigh up pros and cons. "Distinguish" means show the differences between two things. "Outline" requires less depth than "Discuss." Students who ignore action words give the wrong type of answer and lose marks even when their knowledge is correct.',
          'In Section 3, each 60-mark question typically has sub-parts that build in complexity. Part (a) might be a definition or list worth 10-15 marks, part (b) asks for explanation worth 20-25 marks, and part (c) demands evaluation or application worth 20-25 marks. The examiner rewards **depth over breadth** — three well-developed points score higher than six shallow ones.',
        ],
        highlights: [
          {
            term: 'SEE',
            description:
              'State, Explain, Example — the standard answer structure for Business long questions. Name the concept, explain it, illustrate with an example.',
          },
          {
            term: 'SEEE',
            description:
              'State, Explain, Example, Elaborate/Evaluate — an extended structure for higher-order questions requiring analysis or judgement.',
          },
        ],
      },
      // ── Section 3: Where Your Marks Are ────────────────────────────
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'Section 3 is worth **240 marks — 60% of the entire paper**. This is where your grade is made. With four questions at 60 marks each, every long question you answer well is worth 15% of your final result. Students who prepare thoroughly for Section 3 give themselves the strongest possible foundation.',
          'The [[ABQ]] is your other high-value target at **80 marks (20%)**. Because the ABQ always draws from Units 3-5 (Management, Human Resources, Enterprise, and Marketing), these units deserve extra study time. If you know Units 3-5 deeply and can apply them to a case study, you have already covered the ABQ and at least 2-3 of the Section 3 long questions.',
          'Within Section 3, certain topics appear with [[high frequency]]. Management and leadership styles, motivation theories (Maslow, McGregor, Herzberg), marketing concepts (the 4 Ps, market research, product life cycle), sources of finance, business planning, and industrial relations are perennial favourites. Examining the last 10 years of papers reveals that these topics appear in some form almost every year.',
          'Section 1 is worth 80 marks (20%), and it is the most mark-efficient section per minute spent. Ten questions at 8 marks each, drawn from across the syllabus — students who revise broadly and know their definitions can pick up these marks quickly, freeing up more time for the heavier sections.',
        ],
        highlights: [
          {
            term: 'ABQ',
            description:
              'The Applied Business Question — 80 marks (20%) drawn from Units 3-5. High-value because the topics overlap with Section 3.',
          },
          {
            term: 'high frequency',
            description:
              'Topics like leadership styles, motivation theories, the 4 Ps, sources of finance, and industrial relations that appear almost every year.',
          },
        ],
      },
      // ── Section 4: What Costs You Marks ────────────────────────────
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common mark-killer in Business is [[failing to link]] in the ABQ. Students write excellent theory but forget to tie it back to the case study. The examiner literally looks for references to the text — quotes, names, figures from the scenario. If your answer could apply to any business, you have not linked it. Every ABQ point should contain at least one direct reference to the passage.',
          'The second major pitfall is **ignoring the action word**. If the question says "Evaluate," you need to weigh up advantages and disadvantages. If it says "Illustrate," you need a concrete example. If it says "Distinguish," you must show clear differences. Writing a general explanation when the question demands evaluation loses marks because you are answering a different question.',
          'Time management trips up a surprising number of students. A common mistake is spending 50 minutes on the ABQ (meant to take about 35-40 minutes) and then rushing the final long question. With 4 long questions to answer in Section 3, you need approximately **30 minutes per question**. Going even 10 minutes over on one question steals marks from another.',
          'Finally, many students only write [[surface-level answers]] — they state and explain but never give examples, or they list five points with one line each instead of developing three points properly. The marking scheme rewards depth. Two fully developed SEE points (State, Explain, Example) will almost always score higher than four points that only state and briefly explain.',
        ],
        highlights: [
          {
            term: 'failing to link',
            description:
              'The most common ABQ mistake — writing good theory without connecting it to the specific case study text, names, and details.',
          },
          {
            term: 'surface-level answers',
            description:
              'Listing many undeveloped points instead of fully developing fewer points with the SEE/SEEE structure. Depth beats breadth.',
          },
        ],
      },
      // ── Section 5: How to Study Business ───────────────────────────
      {
        title: 'How to Study Business',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Business is one of those subjects where the right study technique makes an outsized difference. The foundation of your preparation should be building a [[concept bank]] — a structured set of notes organised by topic, where each concept is written in SEE format: the term, a clear explanation, and a concrete example. When you revise, you are not just re-reading; you are practising the exact format you will use in the exam.',
          'For the ABQ, the best preparation is [[practice under exam conditions]]. Get a past ABQ, read the case study, and write your answers in 35 minutes. Then compare your answers to the marking scheme. Specifically check: did you link to the text? Did you use quotes? Did you address what the question actually asked? This feedback loop is where your marks improve fastest.',
          'For Section 3, create a topic map of the 7 units and track which topics you have covered. Aim to prepare at least 6 of the 7 typical long-question areas so you have choice on exam day. The core areas to prioritise are: management and leadership, people in business and industrial relations, marketing, enterprise and business planning, managing change, and insurance and business law.',
          'Use **past marking schemes** as your revision partner. The SEC marking schemes show exactly what examiners accept and how marks are allocated point by point. Reading them teaches you the language and level of detail that earns full marks. Many students study notes but never look at how marks are actually awarded — do not make that mistake.',
        ],
        highlights: [
          {
            term: 'concept bank',
            description:
              'A structured set of notes organised by topic with each concept written in SEE format (State, Explain, Example) for direct exam use.',
          },
          {
            term: 'practice under exam conditions',
            description:
              'Timed ABQ practice (35 minutes) followed by comparison against the marking scheme — the fastest way to improve ABQ scores.',
          },
        ],
        bullets: [
          'Build your concept bank in SEE format — every key term should have a State, Explain, and Example ready',
          'Complete at least one full ABQ under timed conditions per week from January onward',
          'Study the SEC marking schemes — they reveal exactly what earns marks and what does not',
          'Prioritise Units 3-5 (Management, HR, Enterprise, Marketing) as they feed both the ABQ and Section 3',
          'Practise action word recognition — know what "illustrate", "evaluate", "outline", and "discuss" each require',
        ],
      },
      // ── Section 6: Your Business Action Plan ───────────────────────
      {
        title: 'Your Business Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start today by downloading the last 10 years of Business Higher Level papers and marking schemes from the SEC website. Create a spreadsheet or list tracking which topics appeared in Section 3 each year — you will quickly see the [[repeating patterns]]. This tells you exactly what to prioritise.',
          'Over the next two weeks, build your concept bank for Units 3-5 first. Write out every key theory in SEE format: management styles, motivation theories, the 4 Ps, market research methods, sources of finance, and business planning elements. Then begin your ABQ training — one timed practice per week, marked against the scheme.',
          'For Section 3, commit to answering **two full long questions per week** under timed conditions (30 minutes each). After marking, identify your [[weak spots]] and return to them the following week. By the time the exam arrives, you want to have practised every major topic type at least twice and feel confident choosing any 4 from 7.',
        ],
        highlights: [
          {
            term: 'repeating patterns',
            description:
              'A topic frequency analysis of past Section 3 questions — reveals which areas appear almost every year and where to focus revision.',
          },
          {
            term: 'weak spots',
            description:
              'Topics where you consistently lose marks in practice — these are your highest-return revision targets.',
          },
        ],
        commitmentText:
          'I will download the last 5 years of Business HL marking schemes and complete one full ABQ under timed conditions this week.',
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────────────────
  // ECONOMICS  (Higher Level)
  // ─────────────────────────────────────────────────────────────────────────
  economics: {
    subjectId: 'economics',
    subjectName: 'Economics',
    moduleNumber: '17',
    moduleTitle: 'Mastering Economics',
    moduleSubtitle: 'Your Complete Economics Exam Guide',
    moduleDescription:
      'Decode the Economics exam — understand how Section A and B work, where the easy marks are, and how to write answers that hit every marking point.',
    themeName: 'teal',
    finishButtonText: 'Cash In',
    sections: [
      // ── Section 1: How Economics Actually Works ─────────────────────
      {
        title: 'How Economics Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Leaving Certificate Economics Higher Level exam is a **single paper** lasting **2 hours and 30 minutes**, worth a total of **400 marks**. It is divided into [[two sections]], and the balance between them is something every student needs to understand from day one.',
          '**Section A** contains short questions worth **100 marks (25%)**. You answer **5 out of 9** questions, each worth **20 marks**. These are relatively concise — definitions, brief calculations, short explanations, or labelling a diagram. Section A is designed to test breadth across both microeconomics and macroeconomics, and it should take about 30-35 minutes.',
          '**Section B** is where your grade is really decided. It contains long questions worth **300 marks (75%)**. You choose **4 from 7** questions, each worth **75 marks**. These are multi-part essay-style questions that demand definitions, explanations, analysis, and often [[diagrams]]. Each question typically has 3-4 sub-parts that build in complexity.',
          'The time constraint is tighter than many students expect. With 150 minutes for 400 marks, you have about **22 seconds per mark**. After spending 30-35 minutes on Section A, you have roughly **28-30 minutes per long question**. Going over time on one question directly cannibalises another, so disciplined pacing is essential.',
        ],
        highlights: [
          {
            term: 'two sections',
            description:
              'Section A (100 marks, 5 from 9 short Qs) and Section B (300 marks, 4 from 7 long Qs worth 75 marks each).',
          },
          {
            term: 'diagrams',
            description:
              'Economic diagrams (supply/demand, cost curves, market structures) are essential in Section B — questions frequently carry specific marks for labelled diagrams.',
          },
        ],
      },
      // ── Section 2: What the Examiner Rewards ────────────────────────
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Economics examiners reward precision. The first thing they look for is [[accurate definitions]]. Almost every long question starts with a definition sub-part, and the marking scheme often gives full marks only for specific, textbook-quality definitions. "Demand" is not just "wanting something" — it is "the quantity of a good or service that consumers are willing and able to buy at a given price in a given time period." That level of precision is what earns full marks.',
          'The second thing examiners reward is **diagrammatic support**. In Economics, diagrams are not decorations — they carry their own marks. A question about market equilibrium expects a correctly drawn and fully labelled supply-and-demand diagram. A question on monopoly expects an MR/MC/AR/AC diagram with the profit-maximising output clearly shown. If the marking scheme allocates marks for a diagram and you skip it, those marks are gone.',
          'For longer sub-parts, the examiner looks for [[structured economic reasoning]]. This means stating the concept, explaining the underlying economic logic, and tracing through the effects step by step. For example, if asked about the impact of an increase in income tax, you should trace through: disposable income falls, consumer spending decreases, aggregate demand contracts, firms may reduce output, unemployment may rise. That chain of logic is what distinguishes a H1 answer from a H3.',
          'Examiners also value **real-world application**. While the marking scheme does not always explicitly require it, references to current economic conditions, Irish economic policy, EU regulations, or recent events in the economy demonstrate understanding beyond rote learning and frequently earn additional credit.',
        ],
        highlights: [
          {
            term: 'accurate definitions',
            description:
              'Textbook-quality definitions with all key elements — Economics examiners mark definitions strictly and give full marks only for precise wording.',
          },
          {
            term: 'structured economic reasoning',
            description:
              'Step-by-step logical chains showing cause and effect through economic concepts — the hallmark of high-grade answers.',
          },
        ],
      },
      // ── Section 3: Where Your Marks Are ────────────────────────────
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'Section B dominates — it is worth **300 of 400 marks (75%)**. Each of the four long questions you answer is worth **75 marks**, meaning each one represents nearly **19% of your total result**. Performing well on just one extra long question can jump you an entire grade. This is where your revision energy should be concentrated.',
          'Within Section B, certain topic areas appear with [[predictable regularity]]. On the micro side: demand and supply, elasticity, market structures (perfect competition, monopoly, imperfect competition), costs and revenue curves, and factors of production are staples. On the macro side: national income, fiscal and monetary policy, inflation, unemployment, international trade and the balance of payments, and economic growth are near-guaranteed appearances.',
          'Section A is your [[efficiency zone]]. With 5 questions at 20 marks each, these are designed to be answered quickly. They often involve labelling diagrams, writing short definitions, performing simple calculations (like elasticity or national income components), or explaining a concept in a few lines. A well-prepared student can secure 80-90 of these 100 marks in under 30 minutes.',
          'Here is the strategic insight: **if you score 90 in Section A and average 60 out of 75 on your four long questions, that gives you 330 out of 400 — a comfortable H1.** The path to a top grade is not about knowing everything; it is about being excellent at the high-frequency topics and disciplined on time.',
        ],
        highlights: [
          {
            term: 'predictable regularity',
            description:
              'Core topics like supply/demand, market structures, fiscal/monetary policy, and international trade appear almost every year in Section B.',
          },
          {
            term: 'efficiency zone',
            description:
              'Section A (100 marks) — quick questions where a well-prepared student can bank marks fast and save time for the higher-value Section B.',
          },
        ],
      },
      // ── Section 4: What Costs You Marks ────────────────────────────
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most damaging mistake in Economics is [[skipping diagrams]]. Students who write excellent prose but omit the diagram are leaving marks on the table. Many long-question sub-parts allocate 10-15 marks specifically for a correctly drawn and labelled diagram. You cannot talk your way into those marks — you must draw the diagram. Supply and demand, cost curves, market structure diagrams, and the Keynesian Cross are all commonly required.',
          'The second big pitfall is **vague definitions**. Economics is a precision subject. Defining inflation as "prices going up" earns maybe 2 out of 5 marks. Defining it as "a persistent and sustained increase in the general price level of goods and services in an economy over time" earns full marks. The difference is knowing the key qualifiers — persistent, sustained, general price level — that the marking scheme looks for.',
          'Many students also fall into the [[one-sided analysis]] trap. When a question asks you to "evaluate" or "discuss" a policy, it expects you to consider both sides. Students who write passionately about why minimum wage increases are great without mentioning potential unemployment effects or business cost impacts are not answering the question fully. Always address advantages and disadvantages when the action word demands it.',
          'Time pressure causes the fourth major issue. With only about 28 minutes per long question, students who write extended answers on their favourite topics run out of time on later questions. An unfinished question is devastating — even a brief, structured answer to every part scores far higher than a perfect answer to three parts and a blank fourth question.',
        ],
        highlights: [
          {
            term: 'skipping diagrams',
            description:
              'The most common high-cost mistake — diagrams carry their own marks (often 10-15 per question) and cannot be replaced by written explanation.',
          },
          {
            term: 'one-sided analysis',
            description:
              'Only presenting advantages or only disadvantages when the question asks for evaluation or discussion — loses marks for incomplete analysis.',
          },
        ],
      },
      // ── Section 5: How to Study Economics ───────────────────────────
      {
        title: 'How to Study Economics',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Economics rewards a structured approach. Start by building a [[definition bank]] — a comprehensive list of every key economic term with its full, precise definition. There are roughly 80-100 core definitions across the syllabus. Test yourself on these regularly using flashcards or active recall. Getting definitions right is the easiest way to pick up marks across both sections.',
          'Next, master your [[diagram library]]. You need to be able to draw, from memory, approximately 15-20 key diagrams: basic supply and demand, shifts in supply and demand, price ceiling and floor, individual firm under perfect competition (short-run and long-run), monopoly profit maximisation, kinked demand curve, cost curves (MC, AC, AVC), the circular flow of income, and the Keynesian Cross. Practise each one until you can draw it quickly with correct labels.',
          'For Section B preparation, use **past papers aggressively**. Work through every question from the last 10 years by topic. You will notice that question structures repeat — the way elasticity is examined, the way market structures are tested, the way fiscal policy is asked about all follow recognisable patterns. Familiarity with these patterns lets you plan your answer instantly in the exam.',
          'Finally, keep a **current affairs file** with 2-3 real-world examples per major topic. For inflation: recent ECB interest rate decisions and Irish CPI trends. For unemployment: Irish labour market data and government policy responses. For international trade: Brexit effects on Irish exports, EU single market developments. These examples add depth and demonstrate genuine understanding.',
        ],
        highlights: [
          {
            term: 'definition bank',
            description:
              'A complete collection of 80-100 precise economic definitions — the foundation for marks in both Section A and Section B opening sub-parts.',
          },
          {
            term: 'diagram library',
            description:
              '15-20 key diagrams memorised and practised until they can be drawn quickly with correct curves, axes, labels, and equilibrium points.',
          },
        ],
        bullets: [
          'Build a definition bank of 80-100 key terms and test yourself weekly using active recall',
          'Practise drawing all 15-20 core diagrams from memory with correct labels and annotations',
          'Work through every Section B question from the last 10 years, organised by topic',
          'Collect 2-3 real-world examples per major topic for current affairs application',
          'Time yourself strictly: 30-35 minutes for Section A, 28-30 minutes per Section B question',
        ],
      },
      // ── Section 6: Your Economics Action Plan ──────────────────────
      {
        title: 'Your Economics Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Begin this week by downloading the last 10 years of Economics HL papers and marking schemes. Create a [[topic frequency table]] — list every Section B topic and tally how often it appears. This reveals your must-know areas and lets you allocate study time intelligently. You will find that about 8-10 core topics cover the vast majority of questions.',
          'Over the next fortnight, start two parallel tracks. Track one: build your definition bank and diagram library, spending 20 minutes per day on active recall. Track two: begin working through past Section B questions by topic, starting with the highest-frequency areas — supply and demand, market structures, and fiscal/monetary policy.',
          'Set a weekly target of completing **two full long questions under timed conditions** (28 minutes each) and marking them against the SEC scheme. For each question, ask yourself: did I include a diagram? Were my definitions precise? Did I trace through the [[economic logic]] step by step? These three checkpoints alone will drive consistent improvement.',
        ],
        highlights: [
          {
            term: 'topic frequency table',
            description:
              'A tally of Section B topics from the last 10 years — reveals the 8-10 core areas that appear almost every year.',
          },
          {
            term: 'economic logic',
            description:
              'The cause-and-effect chain that shows how one economic change leads to subsequent effects — the key skill that earns high marks.',
          },
        ],
        commitmentText:
          'I will create my definition bank for one major topic (e.g. supply and demand) and draw all related diagrams from memory this week.',
      },
    ],
  },
};
