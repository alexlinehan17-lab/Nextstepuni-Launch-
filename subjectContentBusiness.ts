/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type SubjectModuleContent } from './subjectModuleData';
import { SUBJECT_BUSINESS_REFERENCE_LIST } from './data/references/subjectBusiness';

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
          'The paper is split into [[three sections]]. **Section 1 — Financial Accounting** is worth **120 marks**: you either answer the single **120-mark Q1** (a full set of final accounts — the sole trader, company, or manufacturing account) **or** answer **any two of Q2–Q4 at 60 marks each**. **Section 2 — Financial Accounting** is worth **200 marks**: you answer **two of Q5–Q7, each worth 100 marks** (areas like interpretation of accounts, cash flow or abridged accounts, or correction of errors and suspense). **Section 3 — Management Accounting** is worth **80 marks**: you answer **one of Q8–Q9** (budgeting, costing, or flexible budgets).',
          'The time pressure in Accounting is real. With 3 hours and 400 marks, you have roughly **27 seconds per mark** (about 0.45 minutes). That means the 120-mark Q1 deserves around 54 minutes and a 100-mark Section 2 question about 45 minutes. Students who do not plan their time carefully run out before they finish the high-value Section 1 and Section 2 questions, and that is where the biggest blocks of marks sit.',
          'One thing that catches students off guard: [[presentation marks]] are awarded throughout the paper. The examiner is not just checking your figures — they are looking at whether your accounts are properly formatted, labelled, and laid out. Sloppy presentation loses marks even when your calculations are correct.',
        ],
        highlights: [
          {
            term: 'three sections',
            description:
              'Section 1 — Financial Accounting (120 marks: Q1 alone, or any two of Q2–Q4 at 60 each), Section 2 — Financial Accounting (200 marks: two of Q5–Q7 at 100 each), Section 3 — Management Accounting (80 marks: one of Q8–Q9).',
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
          'The single biggest question on the paper is **Section 1 Q1**, worth **120 marks** — that is **30% of the entire paper** in one question. It almost always involves preparing a full set of [[final accounts]]: a Trading, Profit and Loss Account and a Balance Sheet, for a sole trader, a company, or a manufacturing business. This question is your biggest opportunity and your biggest risk. (If you prefer, you can instead answer any two of Q2–Q4 at 60 marks each — but Q1 is where most of the final-accounts practice pays off.)',
          'Section 2 is where the second-largest block of marks lives — **200 marks**, from which you answer **two of Q5–Q7 at 100 marks each**. These questions typically cover distinct areas: **interpretation of accounts (ratios)**, **cash flow statements** or **abridged accounts**, and **correction of errors and suspense**. (Published accounts sits in Section 1 as Q2.) Knowing this pattern helps you prioritise your revision — securing two strong 100-mark answers here is half the paper on its own.',
          'Section 3 is **Management Accounting**, worth **80 marks** — you answer **one of Q8–Q9**. This is where **budgeting** (production, purchases, cash, and budgeted trading & P&L), **costing**, **flexible budgets**, and break-even / marginal-costing analysis are tested. It is a smaller block than Sections 1 and 2, but a well-drilled student can bank it reliably because the question types are predictable.',
          'Here is the strategic point most students miss: **Section 1 (120 marks) and Section 2 (200 marks) together account for 320 of 400 marks** — four-fifths of the paper. If you can produce a clean set of final accounts and two strong Section 2 answers, you are already deep into the paper before Section 3 even comes into play.',
        ],
        highlights: [
          {
            term: 'final accounts',
            description:
              'A Trading, Profit and Loss Account plus Balance Sheet — the centrepiece of the Accounting exam, worth 120 marks as Section 1 Q1.',
          },
        ],
      },
      // ── Section 4: What Costs You Marks ─────────────────────────────
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mark-killer in Accounting is **poor time management**. Students spend too long perfecting one question and then run short on another. Allocate time in proportion to the marks — roughly **0.45 minutes per mark**: about **54 minutes for the 120-mark Section 1 Q1**, about **90 minutes for Section 2** (roughly 45 minutes for each 100-mark question), and about **36 minutes for the 80-mark Section 3**, with a few minutes left for review.',
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
          'Build your revision around **question types, not chapters**. Create a rotation that cycles through final accounts, interpretation of accounts (ratios), cash flow statements, published accounts, correction of errors, and the management-accounting topics (budgeting, costing, flexible budgets). Do at least two full past-paper questions per week from November onward. By exam time, you want to have completed every full-accounts Section 1 Q1 from the last 8-10 years.',
          'Build a [[formula bank]] — a single A4 sheet with every formula you need: depreciation methods, ratios (current ratio, acid test, ROCE, gross profit percentage, net profit percentage), break-even and marginal-costing calculations, and VAT rules. Test yourself on these weekly. The ratio and management-accounting questions are predictable, and a student who knows every formula cold can pick up marks with confidence.',
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
              'A single-page summary of every formula, ratio, and rule needed for ratios and management accounting — tested weekly until automatic.',
          },
        ],
        bullets: [
          'Complete every full-accounts Section 1 Q1 from the last 8-10 years',
          'Time yourself strictly: about 54 minutes for the 120-mark Q1, 45 minutes for each 100-mark Section 2 question, 36 minutes for the 80-mark Section 3',
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
          'Here is your roadmap. **This week**, gather past papers from the last 10 years and the corresponding marking schemes from the SEC website. Organise them by question type: final accounts, interpretation of accounts, cash flow, published accounts, correction of errors, and management accounting (budgeting, costing, flexible budgets). This becomes your practice library.',
          'Start with [[final accounts mastery]]. Do one full final accounts question (Section 1 Q1) per week under timed conditions (about 54 minutes). After completing it, go through the marking scheme line by line and note every mark you missed. Focus on adjustments and presentation. Once you can consistently score highly on the 120-mark Q1, you have secured nearly a third of the paper.',
          'Simultaneously, drill your Section 2 answers (interpretation of accounts, cash flow, correction of errors) and your management-accounting questions using your formula bank. Two strong 100-mark Section 2 answers plus a clean Q1 are your [[safe foundation]] — that puts you at 320 out of 400 before you even look at Section 3.',
        ],
        highlights: [
          {
            term: 'final accounts mastery',
            description:
              'The ability to complete a full set of final accounts with correct layout and adjustments in about 54 minutes — worth 120 marks (30% of the paper) as Section 1 Q1.',
          },
          {
            term: 'safe foundation',
            description:
              'Section 1 (120 marks) plus Section 2 (200 marks) = 320 marks in play before tackling Section 3.',
          },
        ],
        commitmentText:
          'I will complete one full final accounts question (Section 1 Q1) under timed conditions this week and mark it against the SEC marking scheme.',
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
          'The Leaving Certificate Business Higher Level exam is a **single paper** lasting **3 hours** and worth **400 marks**. It is split into [[three sections]] with very different demands, and understanding what each section asks of you is the first step toward a top grade.{{cite:1}}',
          '**Section 1** is short questions, worth **80 marks (20%)** of the total. You answer **8 short questions, each worth 10 marks**.{{cite:1}} These test definitions, brief explanations, and quick recall across the entire syllabus. Section 1 is your warm-up — it should take no more than 30 minutes.',
          '**Section 2** is the [[Applied Business Question (ABQ)]], worth **80 marks (20%)**. This is a case study — a scenario about a real or fictional business — followed by three sub-questions (A, B, and C). The 2025 ABQ drew from **Units 2, 3, and 4** of the syllabus: Enterprise, Management, and Human Resources.{{cite:1}} You must link your answers directly back to the text — every point needs a relevant quote or phrase from the ABQ, or it earns no marks.{{cite:1}}',
          '**Section 3** is the long questions section, worth **240 marks (60%)**. You answer **4 questions, each worth 60 marks** — at least one from Part 1 (People in Business / Business Environment) and one from Part 2.{{cite:1}} These questions can come from any unit on the syllabus and typically have sub-parts (a), (b), and sometimes (c). This is where the bulk of your marks are, and it rewards students who have studied broadly rather than gambling on specific topics.',
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
              'A case study question worth 80 marks (20%). The 2025 ABQ drew from Units 2-4 (Enterprise, Management, HR) and required direct links to the text.',
          },
        ],
      },
      // ── Section 2: What the Examiner Rewards ────────────────────────
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Business examiners are trained to look for **structured answers**. The two answer frameworks you need are [[SEE]] and [[SEEE]]. **SEE** stands for **State, Explain, Example** — you name the concept, explain what it means, and give a relevant example. **SEEE** adds an extra E for **Elaborate** or **Evaluate**, which means you take it further by discussing advantages, disadvantages, or implications. The marking scheme uses exactly this "Name, Explain, Example" pattern when allocating marks.{{cite:1}}',
          'For the ABQ in Section 2, the framework shifts to **State, Explain, Link** (the scheme calls it Name, Explain, Link). The "Link" is the critical difference: you must connect your answer directly to the case study using a **direct quote or phrase** from the text. The marking scheme states that no link mark is awarded without relevant theory, and that a separate link is required in each part.{{cite:1}}',
          '**Action words** in the question are your instructions. "Illustrate" means give an example. "Evaluate" means weigh up pros and cons. "Distinguish" means show the differences between two things. "Outline" requires less depth than "Discuss." Students who ignore action words give the wrong type of answer and lose marks even when their knowledge is correct.{{cite:2}}',
          'In Section 3, each 60-mark question typically has sub-parts that build in complexity. Part (a) might be a definition or list, part (b) asks for explanation, and part (c) demands evaluation or application. The examiner rewards **depth over breadth** — fully developed points score higher than a longer list of one-word or undeveloped ones.{{cite:2}}',
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
          'Section 3 is worth **240 marks — 60% of the entire paper**.{{cite:1}} This is where your grade is made. With four questions at 60 marks each, every long question you answer well is worth 15% of your final result. Students who prepare thoroughly for Section 3 give themselves the strongest possible foundation.',
          'The [[ABQ]] is your other high-value target at **80 marks (20%)**. Because the ABQ draws heavily on the management, enterprise, and HR units (Units 2-4 in 2025), these units deserve extra study time.{{cite:1}} If you know them deeply and can apply them to a case study, you have already covered the ABQ and several of the Section 3 long questions.',
          'Within Section 3, certain topics appear with [[high frequency]]. Management and leadership styles, motivation theories (Maslow, McGregor, Herzberg), marketing concepts (the 4 Ps, market research, product life cycle), sources of finance, business planning, and industrial relations are perennial favourites. Examining the last 10 years of papers reveals that these topics appear in some form almost every year.',
          'Section 1 is worth 80 marks (20%), and it is the most mark-efficient section per minute spent. Eight questions at 10 marks each, drawn from across the syllabus — students who revise broadly and know their definitions can pick up these marks quickly, freeing up more time for the heavier sections.{{cite:1}}',
        ],
        highlights: [
          {
            term: 'ABQ',
            description:
              'The Applied Business Question — 80 marks (20%), drawing on the enterprise, management and HR units (Units 2-4 in 2025). High-value because the topics overlap with Section 3.',
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
          'The most common mark-killer in Business is [[failing to link]] in the ABQ. Students write excellent theory but forget to tie it back to the case study. The examiner literally looks for references to the text — a direct quote, name, or figure from the scenario — and awards no link mark without it. If your answer could apply to any business, you have not linked it. Every ABQ point should contain at least one direct reference to the passage.{{cite:1}}',
          'The second major pitfall is **ignoring the action word**. If the question says "Evaluate," you need to weigh up advantages and disadvantages. If it says "Illustrate," you need a concrete example. If it says "Distinguish," you must show clear differences. Writing a general explanation when the question demands evaluation loses marks because you are answering a different question.{{cite:2}}',
          'Time management trips up a surprising number of students. A common mistake is spending 50 minutes on the ABQ (meant to take about 35-40 minutes) and then rushing the final long question. With 4 long questions to answer in Section 3, you need approximately **30 minutes per question**. Going even 10 minutes over on one question steals marks from another.',
          'Finally, many students only write [[surface-level answers]] — they state and explain but never give examples, or they list many points with one line each instead of developing fewer points properly. The marking scheme rewards depth: fully developed SEE points (State, Explain, Example) score higher than a longer list of one-word or briefly-stated points.{{cite:2}}',
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
          'Use **past marking schemes** as your revision partner. The SEC marking schemes show exactly what examiners accept and how marks are allocated point by point.{{cite:1}} Reading them teaches you the language and level of detail that earns full marks. Many students study notes but never look at how marks are actually awarded — do not make that mistake.',
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
          'Prioritise the enterprise, management and HR units (Units 2-4 in 2025) as they feed both the ABQ and Section 3',
          'Practise action word recognition — know what "illustrate", "evaluate", "outline", and "discuss" each require',
        ],
      },
      // ── Section 6: Your Business Action Plan ───────────────────────
      {
        title: 'Your Business Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start today by downloading the last 10 years of Business Higher Level papers and marking schemes from the SEC website. Create a spreadsheet or list tracking which topics appeared in Section 3 each year — you will quickly see the [[repeating patterns]]. This tells you exactly what to prioritise.',
          'Over the next two weeks, build your concept bank for the enterprise, management and HR units first (the ABQ\'s home ground — Units 2-4 in 2025). Write out every key theory in SEE format: management styles, motivation theories, sources of finance, and business planning elements, then the marketing topics for Section 3. Then begin your ABQ training — one timed practice per week, marked against the scheme.{{cite:1}}',
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
    references: SUBJECT_BUSINESS_REFERENCE_LIST,
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
      'Decode the Economics exam — understand how the written paper and the Student Research Project work, how Section A and B are marked, and how to write answers that hit every marking point.',
    themeName: 'teal',
    finishButtonText: 'Cash In',
    sections: [
      // ── Section 1: How Economics Actually Works ─────────────────────
      {
        title: 'How Economics Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Certificate Economics has **two assessment components**: a **written examination worth 80%** of your grade and a **Student Research Project (SRP) worth 20%**. Many students forget the SRP entirely and treat the subject as one exam — but a fifth of your result is decided before you ever sit the paper, so both components need a plan from day one.',
          'The written paper lasts **two and a half hours** and is divided into [[two sections]] — Section A (short-answer questions) and Section B (extended-response questions). Understanding how each is marked, and how the SRP is graded, is the first step toward a top grade.',
          '**Section A** is worth **75 marks**. It is a set of short questions built around stimulus material — a news extract, a CSO table, a chart, or a diagram — followed by short parts that test definitions, brief calculations, short explanations, or reading a diagram. Some questions offer an internal choice (e.g. "answer either (b) or (c)"). Section A is designed to test breadth across the five strands of the specification.',
          '**Section B** is the extended-response section — six themed long questions (**Q11–Q16**), each threading a real-world stimulus (CSO data, news headlines) through several parts. These parts mix developed-point answers, calculations, and [[diagrams]], and build in complexity. This is where most of the written-paper marks sit, so disciplined pacing across the two and a half hours is essential.',
        ],
        highlights: [
          {
            term: 'two sections',
            description:
              'Section A (75 marks, stimulus-based short questions across the five strands) and Section B (six themed extended-response long questions, Q11–Q16). The written paper is 80% of the grade; the Student Research Project is the other 20%.',
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
          'Section B — the six themed long questions (Q11–Q16) — is where most of the written-paper marks are decided. These extended-response questions carry far more marks than the short Section A questions, so performing well across your Section B answers is what jumps you a grade. This is where the bulk of your revision energy should be concentrated.',
          'Within Section B, certain topic areas appear with [[predictable regularity]]. On the micro side: demand and supply, elasticity, market structures (perfect competition, monopoly, imperfect competition), costs and revenue curves, and factors of production are staples. On the macro side: national income, fiscal and monetary policy, inflation, unemployment, international trade and the balance of payments, and economic growth are near-guaranteed appearances.',
          'Section A (**75 marks**) is your [[efficiency zone]]. Its stimulus-based short questions are designed to be answered quickly — reading a chart or diagram, writing short definitions, performing simple calculations (like a savings rate or an export percentage), or explaining a concept in a few lines. A well-prepared student can bank a strong share of these 75 marks efficiently and save time for the higher-value Section B questions.',
          'Here is the strategic insight: because the written paper is **80% of your grade** and the Student Research Project is the other **20%**, the top grades come from being strong on **both** components — excellent on the high-frequency Section B topics, efficient in Section A, and deliberate about the SRP rather than treating it as an afterthought. The path to a top grade is not about knowing everything; it is about depth on the topics that recur and discipline across both components.',
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
              'Section A (75 marks) — stimulus-based short questions where a well-prepared student can bank marks fast and save time for the higher-value Section B.',
          },
        ],
      },
      // ── Section 4: What Costs You Marks ────────────────────────────
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most damaging mistake in Economics is [[skipping diagrams]] — and, just as costly, drawing them **unlabelled**. Diagrams are not decoration: they are broken into named, itemised marks, and the labels and axes are separately marked. On the 2025 paper a full supply-and-demand graph was worth 17 marks (2 for the axes, 6 for each curve, plus the equilibrium point and price/quantity labels); a monopoly long-run-equilibrium diagram was worth 12 marks; a minimum-wage labour-market diagram 6 marks. Cues like "Label your diagram fully" and "Do not use abbreviations" are enforced mark-by-mark — writing "MC" where "Marginal cost" is demanded scores nothing for that item. You cannot talk your way into these marks — you must draw and fully label the diagram. Supply and demand, cost curves, market-structure diagrams (including the kinked-demand curve), and the LRAC construction are all commonly required.',
          'The second big pitfall is **vague definitions**. Economics is a precision subject. Defining inflation as "prices going up" earns maybe 2 out of 5 marks. Defining it as "a persistent and sustained increase in the general price level of goods and services in an economy over time" earns full marks. The difference is knowing the key qualifiers — persistent, sustained, general price level — that the marking scheme looks for.',
          'Many students also fall into the [[one-sided analysis]] trap. When a question asks you to "evaluate" or "discuss" a policy, it expects you to consider both sides. Students who write passionately about why minimum wage increases are great without mentioning potential unemployment effects or business cost impacts are not answering the question fully. Always address advantages and disadvantages when the action word demands it.',
          'Time pressure causes the fourth major issue. With only two and a half hours for the whole paper, students who write extended answers on their favourite topics run out of time on later questions. An unfinished question is devastating — even a brief, structured answer to every part scores far higher than a perfect answer to some parts and a blank on the rest. Remember, too, that over-supplying points earns nothing: a part marked "two factors" counts only the first two, so a third point wastes time it can never buy back.',
        ],
        highlights: [
          {
            term: 'skipping diagrams',
            description:
              'The most common high-cost mistake — diagrams carry their own itemised marks (e.g. 17 for a full supply-and-demand graph, 12 for a monopoly diagram in 2025), with labels and axes separately marked, and cannot be replaced by written explanation.',
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
          'Next, master your [[diagram library]]. You need to be able to draw, from memory, the key diagrams the paper keeps returning to: basic supply and demand and shifts in supply and demand, individual firm under perfect competition (short-run and long-run), monopoly profit maximisation, the minimum-wage / price-control labour-market diagram, the kinked-demand curve, cost curves (MC, AC, AVC), and the long-run average cost (LRAC) construction. Practise each one until you can draw it quickly with **every curve, axis, and equilibrium point fully labelled** — because the labels are separately marked.',
          'For Section B preparation, use **past papers aggressively** — but note the syllabus change. The current Economics specification (with its 80% written paper plus 20% Student Research Project) has been examined only from **2021 onward**, so work through the papers from **2021 to the present** by topic. Papers from before 2021 sit under the old syllabus with a different paper structure, so they are not a reliable guide to the current exam. Across the current papers you will notice question structures repeat — the way elasticity is examined, the way market structures are tested, the way fiscal policy is asked about all follow recognisable patterns.',
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
          'Build a definition bank of key terms and test yourself weekly using active recall',
          'Practise drawing the core diagrams from memory with every curve, axis, and label complete',
          'Work through every Section B question from 2021 onward (the current specification), organised by topic',
          'Collect 2-3 real-world examples per major topic for current affairs application',
          'Do not forget the Student Research Project — it is 20% of your grade and marked on analysis and evaluation supported by data',
          'Time yourself against the full two-and-a-half-hour paper, in proportion to each part’s marks',
        ],
      },
      // ── Section 6: Your Economics Action Plan ──────────────────────
      {
        title: 'Your Economics Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Begin this week by downloading the Economics HL papers and marking schemes **from 2021 onward** — the years examined under the current specification. (Older papers use a different paper structure, so building a frequency table from them would mislead your priorities.) Create a [[topic frequency table]] — list every Section B topic and tally how often it appears across the current papers. This reveals your must-know areas and lets you allocate study time intelligently.',
          'Over the next fortnight, start two parallel tracks. Track one: build your definition bank and diagram library, spending 20 minutes per day on active recall. Track two: begin working through past Section B questions by topic, starting with the highest-frequency areas — supply and demand, market structures, and fiscal/monetary policy. And set aside dedicated time for the **Student Research Project** — worth 20% of your grade — planning your line of inquiry and data sources early rather than leaving it to the end.',
          'Set a weekly target of completing **two full long questions under timed conditions** — pacing yourself in proportion to each part’s marks — and marking them against the SEC scheme. For each question, ask yourself: did I include a fully labelled diagram? Were my definitions precise, using the key phrases the scheme looks for? Did I trace through the [[economic logic]] step by step? These three checkpoints alone will drive consistent improvement.',
        ],
        highlights: [
          {
            term: 'topic frequency table',
            description:
              'A tally of Section B topics across the current-specification papers (2021 onward) — reveals the core areas that recur and where to focus revision.',
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
