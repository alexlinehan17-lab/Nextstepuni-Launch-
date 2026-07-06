/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Business (Higher Level) marking sessions.
 *
 * Questions, cases and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or real candidate scripts.
 * The marking grids, mark values and credit rules are the real ones, cited to:
 *  - SEC Business HL marking scheme 2025 (examiner-reports/business/2025-*)
 *  - Chief Examiner's Report, Business 2015 (examiner-reports/business/2015-*)
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession } from './types';

const MS25 = (p: string) => ({ label: `SEC Business HL marking scheme 2025, ${p}` });
const CER15 = (p: string) => ({ label: `Chief Examiner's Report, Business 2015, ${p}` });

// ─────────────────────────── B1 · Theory + Link ───────────────────────────

const B1: GridSession = {
  mode: 'grid',
  id: 'biz-theory-link',
  subject: 'business',
  level: 'higher',
  title: 'Theory + link, or nothing',
  cue: 'Outline (ABQ)',
  caseText:
    'Nora runs Sáile Surf School on the Sligo coast. To buy her first vans and boards she took out a loan secured against her own house. Last winter, after studying a season of booking data, she dropped group lessons and moved to small-pod coaching, even though group lessons were her best-known product. When storms closed the beach for three weeks, she filmed a set of online balance-training tutorials from her garage and sold them to clients who couldn’t get in the water.',
  question: 'Outline two entrepreneurial skills shown by Nora. Refer to the text above in your answer.',
  questionNote:
    'Case and question authored for this exercise. The marking grid is the SEC 2025 HL ABQ Part (A) template — 4@5 (2+2+1), Name + Explain + Link — shortened to two points here.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the skill', marks: 2 },
      { id: 'explain', label: 'Explain the theory', marks: 2 },
      { id: 'link', label: 'Link: quote/phrase from the case', marks: 1 },
    ],
    shorthand: '2@5 (2+2+1)',
    ruleNote:
      'Links must be a direct, relevant quote or phrase from the case, and each point needs its own separate link. The scheme is blunt: “No link awarded without relevant theory.” The reverse also holds — theory with no case link loses the link mark every time.',
    cite: MS25('p.6 (ABQ Part (A) grid and link rule)'),
  },
  scripts: [
    {
      id: 'b1-a',
      label: 'Script A',
      persona: 'Knows the theory cold — never opens the case',
      attempts: [
        {
          id: 'b1-a-1',
          text: 'Risk-taking: an entrepreneur is willing to commit their own resources to a venture where there is a real chance of loss. Entrepreneurs take calculated risks rather than gambles, weighing the potential loss against the potential reward before acting.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'Perfect theory — named and explained. But there is no quote or phrase from the case, so the link mark is gone. 4/5.',
        },
        {
          id: 'b1-a-2',
          text: 'Decision-making: an entrepreneur must be able to choose between alternative courses of action, often with incomplete information, and commit to the chosen course. Good decision-makers gather what evidence they can before deciding.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'Same pattern: textbook-complete, case-absent. 4/5. Across a real 80-mark ABQ this habit costs a full grade band.',
        },
      ],
      embodies: {
        behaviour: 'Writes business theory without any reference to the case — the first of the two ABQ failure modes the Chief Examiner names.',
        cite: CER15('p.15'),
      },
    },
    {
      id: 'b1-b',
      label: 'Script B',
      persona: 'Treats the case as a comprehension exercise',
      attempts: [
        {
          id: 'b1-b-1',
          text: 'Nora runs a surf school on the Sligo coast. She took out a loan against her own house to buy vans and boards, which shows she is a good businesswoman.',
          key: { name: 0, explain: 0, link: 0 },
          keyNote: 'This retells the case. No entrepreneurial skill is named, no theory is explained — and without theory, the quoted material earns no link mark either. 0/5.',
        },
        {
          id: 'b1-b-2',
          text: 'When the beach closed for three weeks she made online tutorials in her garage and sold them to her clients, so she kept making money even in the storms.',
          key: { name: 0, explain: 0, link: 0 },
          keyNote: 'Again pure retelling. The examiner can see the candidate read the case — but reading is not the skill being examined. 0/5.',
        },
      ],
      embodies: {
        behaviour: 'Treats the ABQ as a comprehension piece and rewrites chunks of the case — the second documented ABQ failure mode.',
        cite: CER15('p.15'),
      },
    },
    {
      id: 'b1-c',
      label: 'Script C',
      persona: 'One good quote — recycled for both points',
      attempts: [
        {
          id: 'b1-c-1',
          text: 'Risk-taking: willingness to commit personal resources where loss is possible. Nora shows this when she “took out a loan secured against her own house” — her home is on the line if the business fails.',
          key: { name: 2, explain: 2, link: 1 },
          keyNote: 'Name, theory, and a direct case phrase tied to that theory. Full 5/5.',
        },
        {
          id: 'b1-c-2',
          text: 'Initiative: acting without being prompted, creating opportunities rather than waiting for them. Nora shows initiative because she “took out a loan secured against her own house”.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'The theory is fine, but the same quote has been reused — the scheme requires separate links for each point, and this quote evidences risk, not initiative. Link mark lost. 4/5.',
        },
      ],
      embodies: {
        behaviour: 'Reuses one case quote across multiple points — separate links are required in each section.',
        cite: MS25('p.6'),
      },
    },
    {
      id: 'b1-d',
      label: 'Script D',
      persona: 'The examiner’s friend',
      attempts: [
        {
          id: 'b1-d-1',
          text: 'Risk-taking: an entrepreneur commits their own resources knowing they may lose them. Nora “took out a loan secured against her own house” — she has put her personal assets at risk for the venture.',
          key: { name: 2, explain: 2, link: 1 },
          keyNote: 'Name (2) + theory (2) + a separate, relevant case phrase (1). 5/5.',
        },
        {
          id: 'b1-d-2',
          text: 'Decision-making: choosing between alternatives using available evidence and committing to the choice. After “studying a season of booking data”, Nora dropped her best-known product for small-pod coaching — an evidence-based decision with real trade-offs.',
          key: { name: 2, explain: 2, link: 1 },
          keyNote: 'A different skill, a different quote, theory tied to the evidence. 5/5.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b1',
    rule: 'Theory and link are non-substitutable.',
    detail:
      'On the ABQ, a point only pays when named theory and a separate direct case phrase appear together — perfect theory with no link, or perfect quoting with no theory, both leave marks on the table.',
    cite: MS25('p.6'),
  },
};

// ─────────────────────────── B2 · List means list ───────────────────────────

const B2: GridSession = {
  mode: 'grid',
  id: 'biz-list-rule',
  subject: 'business',
  level: 'higher',
  title: 'List means list',
  cue: 'List',
  question:
    'List four grounds, other than gender, under which discrimination is outlawed under the Employment Equality Acts.',
  questionNote:
    'Question authored for this exercise; the SEC 2025 HL paper asked a “List four grounds” question marked on this exact grid. Valid grounds under the Acts include civil status, family status, sexual orientation, religion, age, disability, race, and membership of the Traveller community.',
  grid: {
    perPoint: [
      { id: 'g1', label: '1st valid ground', marks: 3 },
      { id: 'g2', label: '2nd valid ground', marks: 3 },
      { id: 'g3', label: '3rd valid ground', marks: 1 },
      { id: 'g4', label: '4th valid ground', marks: 1 },
    ],
    shorthand: '8 marks (3, 3, 1, 1)',
    ruleNote:
      'The first two valid grounds named earn 3 marks each; the next two earn 1 each. Explanation earns nothing extra on a “List” cue, and naming fewer than four caps your total no matter how well you write.',
    cite: MS25('p.8 (Q1(C)(ii) grid)'),
  },
  scripts: [
    {
      id: 'b2-a',
      label: 'Script A',
      persona: 'Writes beautifully — about two grounds',
      attempts: [
        {
          id: 'b2-a-1',
          text: 'One ground is age: an employer cannot treat a worker less favourably because they are older or younger than others, for example passing over an older applicant for training. Another is disability: employers must not discriminate against people with disabilities and should provide reasonable accommodation, such as accessible workstations, so that they can do their jobs fully.',
          key: { g1: 3, g2: 3, g3: 0, g4: 0 },
          keyNote: 'Two valid grounds (age, disability) = 3 + 3. The paragraphs of explanation earn nothing — the cue is “List”. Two more names would have beaten all this prose. 6/8.',
        },
      ],
      embodies: {
        behaviour: 'Wrote paragraphs to explain the protected grounds rather than just naming them, as the question required.',
        cite: CER15('p.17'),
      },
    },
    {
      id: 'b2-b',
      label: 'Script B',
      persona: 'Stops one short',
      attempts: [
        {
          id: 'b2-b-1',
          text: '1. Age  2. Race  3. Religion',
          key: { g1: 3, g2: 3, g3: 1, g4: 0 },
          keyNote: 'Three valid grounds: 3 + 3 + 1 = 7. The fourth slot is only worth 1 mark — but it is the cheapest mark on the paper, and it was left behind. 7/8.',
        },
      ],
    },
    {
      id: 'b2-c',
      label: 'Script C',
      persona: 'The clean lister',
      attempts: [
        {
          id: 'b2-c-1',
          text: '1. Age  2. Disability  3. Religion  4. Membership of the Traveller community',
          key: { g1: 3, g2: 3, g3: 1, g4: 1 },
          keyNote: 'Four valid grounds, no wasted words. Full 8/8 in under a minute — exactly what the grid pays for.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b2',
    rule: 'The cue sets the currency.',
    detail:
      '“List” pays for names and nothing else — explanation is unpaid labour. Match the length of your answer to the cue and the mark allocation, not to how much you know.',
    cite: MS25('p.8'),
  },
};

// ─────────────────────── B3 · Precision beats vibes ───────────────────────

const B3: GridSession = {
  mode: 'grid',
  id: 'biz-precision',
  subject: 'business',
  level: 'higher',
  title: 'Precision beats vibes',
  cue: 'Explain',
  question: 'Explain the insurance principles of utmost good faith and insurable interest.',
  questionNote:
    'Question authored for this exercise; marked on the SEC 2025 short-response template for two developed points — (3+2)(3+2), core statement + development.',
  grid: {
    perPoint: [
      { id: 'core', label: 'Core statement (precise)', marks: 3 },
      { id: 'dev', label: 'Development / example', marks: 2 },
    ],
    shorthand: '(3+2) (3+2)',
    ruleNote:
      'Each principle earns 3 for a precise core statement and 2 for development. Near-synonyms don’t count as the principle: the 2015 report singles out “telling the truth” offered for utmost good faith, where “disclosing all material facts” was required.',
    cite: MS25('p.4 (Section 1 (3+2)(3+2) template)'),
  },
  scripts: [
    {
      id: 'b3-a',
      label: 'Script A',
      persona: 'Close — but paraphrasing',
      attempts: [
        {
          id: 'b3-a-1',
          text: 'Utmost good faith means you must always tell the truth to the insurance company when you are filling in the forms.',
          key: { core: 0, dev: 0 },
          keyNote: '“Telling the truth” is not the principle — utmost good faith requires disclosing ALL material facts, asked or not. A truthful form that omits a material fact still breaches it. The Chief Examiner flagged this exact paraphrase. 0/5.',
        },
        {
          id: 'b3-a-2',
          text: 'Insurable interest means you must benefit from the item insured existing and suffer financially by its loss — for example, you can insure your own house but not your neighbour’s.',
          key: { core: 3, dev: 2 },
          keyNote: 'Precise core plus a clarifying example. 5/5.',
        },
      ],
      embodies: {
        behaviour: 'Explains utmost good faith as “telling the truth” rather than disclosing all material facts — precision of language is required.',
        cite: CER15('p.19'),
      },
    },
    {
      id: 'b3-b',
      label: 'Script B',
      persona: 'Names it, never develops it',
      attempts: [
        {
          id: 'b3-b-1',
          text: 'Utmost good faith: all material facts must be disclosed to the insurer.',
          key: { core: 3, dev: 0 },
          keyNote: 'The core is precise — 3 marks. But there is no development or example, so the 2 development marks are gone.',
        },
        {
          id: 'b3-b-2',
          text: 'Insurable interest: you must have a financial interest in what you insure.',
          key: { core: 3, dev: 0 },
          keyNote: 'Same again: right, but bare. 3/5. One-line answers on “Explain” cues leave the development marks behind every time.',
        },
      ],
      embodies: {
        behaviour: 'Gives one valid but undeveloped point where developed points are required — the brevity pattern the report calls a significant barrier.',
        cite: CER15('p.20'),
      },
    },
    {
      id: 'b3-c',
      label: 'Script C',
      persona: 'Precise and developed',
      attempts: [
        {
          id: 'b3-c-1',
          text: 'Utmost good faith: the insured must disclose all material facts to the insurer, whether asked or not — e.g. telling a home insurer about prior flooding, since it affects the risk being priced.',
          key: { core: 3, dev: 2 },
          keyNote: 'Precise core, developed with a material-fact example. 5/5.',
        },
        {
          id: 'b3-c-2',
          text: 'Insurable interest: the insured must stand to benefit from the item’s existence and suffer financially from its loss — which is why you can insure your own car but not a stranger’s.',
          key: { core: 3, dev: 2 },
          keyNote: '5/5. Ten marks here takes four sentences — but they have to be the right four sentences.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b3',
    rule: 'Near-synonyms are not the principle.',
    detail:
      'Business definitions are marked on precise language — “telling the truth” isn’t utmost good faith, and “production” isn’t the marketing-mix “product”. Learn the exact phrase, then add one line of development.',
    cite: CER15('p.19'),
  },
};

// ─────────────────────── B4 · Evaluate means judge ───────────────────────

const B4: GridSession = {
  mode: 'grid',
  id: 'biz-evaluate',
  subject: 'business',
  level: 'higher',
  title: 'Evaluate means judge',
  cue: 'Evaluate',
  caseText:
    'Bean & Board is a small café that holds daily stock of coffee beans, milk and pastries. Last summer it threw away unsold pastries most evenings. Since January it has used an ordering app that suggests order sizes from the previous fortnight’s sales, and end-of-day waste has fallen sharply.',
  question: 'Evaluate the effectiveness of stock control in Bean & Board. Refer to the case in your answer.',
  questionNote:
    'Case and question authored for this exercise. The grid is the SEC 2025 HL ABQ Part (B)(i) template — 4@7 (1+2+1+3), Name + Explain + Link + Evaluate — shortened to one point here.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the control', marks: 1 },
      { id: 'explain', label: 'Explain the theory', marks: 2 },
      { id: 'link', label: 'Link to the case', marks: 1 },
      { id: 'eval', label: 'Evaluate: judgement + justification', marks: 3 },
    ],
    shorthand: '1@7 (1+2+1+3)',
    ruleNote:
      'Evaluation is the single most heavily weighted component in this grid — 3 of the 7 marks. A verdict with no justification, or an answer that stops after the link, hands back almost half the marks.',
    cite: MS25('p.6 (ABQ Part (B)(i) grid)'),
  },
  scripts: [
    {
      id: 'b4-a',
      label: 'Script A',
      persona: 'Does everything — except the job',
      attempts: [
        {
          id: 'b4-a-1',
          text: 'Stock control means holding the right level of stock: enough to meet demand without tying up cash or creating waste. Bean & Board “threw away unsold pastries most evenings” last summer, and now uses an ordering app based on the previous fortnight’s sales.',
          key: { name: 1, explain: 2, link: 1, eval: 0 },
          keyNote: 'Name, theory and case link are all here — and then it stops. The question asked for an evaluation, and no judgement was offered. The heaviest component (3 marks) scores zero. 4/7.',
        },
      ],
      embodies: {
        behaviour: 'Names, explains and links but never evaluates — the report notes some candidates “do not evaluate at all”.',
        cite: CER15('p.17'),
      },
    },
    {
      id: 'b4-b',
      label: 'Script B',
      persona: 'Verdict without evidence',
      attempts: [
        {
          id: 'b4-b-1',
          text: 'Stock control means managing stock levels so the business doesn’t over- or under-order. Bean & Board uses an ordering app for its daily stock. In my opinion the stock control is very effective and works really well for the café.',
          key: { name: 1, explain: 2, link: 1, eval: 0 },
          keyNote: '“Very effective” is a verdict, but nothing justifies it — no outcome, no evidence, no criterion. The report calls these evaluations “very superficial”. 4/7.',
        },
      ],
      embodies: {
        behaviour: 'Offers a superficial evaluation — a judgement with no justification.',
        cite: CER15('p.17'),
      },
    },
    {
      id: 'b4-c',
      label: 'Script C',
      persona: 'Judge and justify',
      attempts: [
        {
          id: 'b4-c-1',
          text: 'Stock control means holding the right stock levels: enough to meet demand without waste or tied-up cash. Bean & Board’s app orders from the “previous fortnight’s sales”. It is effective: the case states end-of-day waste “has fallen sharply” since January, so the control is demonstrably reducing the exact cost — binned pastries — that it was introduced to cut.',
          key: { name: 1, explain: 2, link: 1, eval: 3 },
          keyNote: 'A judgement (“it is effective”) justified with a measurable outcome from the case. That is what the 3 evaluation marks buy. 7/7.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b4',
    rule: 'Evaluation = judgement + justification.',
    detail:
      'On “Evaluate” cues the verdict alone is worth nothing — pair it with evidence or a criterion. In the ABQ grid, evaluation is the heaviest single component at 3 of 7 marks.',
    cite: MS25('p.6'),
  },
};

// ─────────────────────── B5 · Show your workings ───────────────────────

const B5: GridSession = {
  mode: 'grid',
  id: 'biz-workings',
  subject: 'business',
  level: 'higher',
  title: 'Show your workings',
  cue: 'Calculate',
  question:
    'From the following figures, calculate the Debt/Equity ratio and express your answer as X : 1. Long-term loan €400,000; Authorised share capital €1,000,000; Issued share capital €700,000; Retained earnings (reserves) €100,000.',
  questionNote:
    'Figures authored for this exercise; marked on the SEC 2025 Q7 ratio template — five distinct marking points at 1 mark each, one per step of the working.',
  grid: {
    perPoint: [
      { id: 'debt', label: 'Identify Debt (€400,000)', marks: 1 },
      { id: 'equity', label: 'Identify Equity = Issued + Reserves (€800,000)', marks: 1 },
      { id: 'sub', label: 'Substitute into the ratio', marks: 1 },
      { id: 'calc', label: 'Calculate the result (0.5)', marks: 1 },
      { id: 'ratio', label: 'Express as a ratio (0.5 : 1)', marks: 1 },
    ],
    shorthand: '5 @ 1m',
    ruleNote:
      'Each procedural step is its own marking point. A bare final answer — even a correct one — collects only the mark for the step it shows. The scheme enforces “show your workings” through the grid, not through a polite instruction.',
    cite: MS25('p.5 (Q7 Debt/Equity grid)'),
  },
  scripts: [
    {
      id: 'b5-a',
      label: 'Script A',
      persona: 'Mental maths, empty page',
      attempts: [
        {
          id: 'b5-a-1',
          text: '0.5 : 1',
          key: { debt: 0, equity: 0, sub: 0, calc: 0, ratio: 1 },
          keyNote: 'The answer is right — and worth 1 of the 5 marks. Identifying the figures, substituting and calculating were each their own marking point, and none of them appear. 1/5.',
        },
      ],
      embodies: {
        behaviour: 'States the final ratio without working — the grid caps this at 1 mark.',
        cite: MS25('p.5'),
      },
    },
    {
      id: 'b5-b',
      label: 'Script B',
      persona: 'Full working — wrong capital',
      attempts: [
        {
          id: 'b5-b-1',
          text: 'Debt = €400,000. Equity = Authorised capital + Reserves = €1,000,000 + €100,000 = €1,100,000. Debt/Equity = 400,000 ÷ 1,100,000 = 0.36. Ratio = 0.36 : 1.',
          key: { debt: 1, equity: 0, sub: 1, calc: 1, ratio: 1 },
          keyNote: 'One wrong choice — Authorised instead of Issued capital — loses exactly one marking point; the rest of the working is consistent and earns its steps. Authorised capital is only the ceiling on what COULD be issued; equity is Issued + Reserves. 4/5.',
        },
      ],
      embodies: {
        behaviour: 'Uses Authorised rather than Issued share capital in the equity figure — a documented misconception on this exact ratio.',
        cite: MS25('p.5'),
      },
    },
    {
      id: 'b5-c',
      label: 'Script C',
      persona: 'Five steps, five marks',
      attempts: [
        {
          id: 'b5-c-1',
          text: 'Debt = long-term loan = €400,000. Equity = Issued share capital + Reserves = €700,000 + €100,000 = €800,000. Debt/Equity = 400,000 ÷ 800,000 = 0.5. Ratio = 0.5 : 1.',
          key: { debt: 1, equity: 1, sub: 1, calc: 1, ratio: 1 },
          keyNote: 'Every marking point visible on the page. 5/5 — and if a slip had crept in, the shown steps would still have earned theirs.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b5',
    rule: 'In calculation grids, each step is its own mark.',
    detail:
      'Write the figures you chose, the substitution, the arithmetic and the final format — a bare answer earns one mark out of five, and a shown working protects you when one step goes wrong.',
    cite: MS25('p.5'),
  },
};

// ─────────────────────── B6 · The chart IS the marks ───────────────────────

const B6: GridSession = {
  mode: 'grid',
  id: 'biz-chart',
  subject: 'business',
  level: 'higher',
  title: 'The chart IS the marks',
  cue: 'Illustrate (chart)',
  question:
    'Using the information in a breakeven question, illustrate the breakeven point, the profit at forecast output, and the margin of safety on a fully labelled breakeven chart. (Each script below describes what a candidate actually put on the page.)',
  questionNote:
    'Scenario authored for this exercise; the grid is the SEC 2025 Q8(C) breakeven-chart grid, item for item, including the calculations-only cap.',
  grid: {
    perPoint: [
      { id: 'title', label: 'Chart title', marks: 2 },
      { id: 'xaxis', label: 'Output axis labelled', marks: 1 },
      { id: 'yaxis', label: 'Costs/revenue axis labelled', marks: 1 },
      { id: 'fc', label: 'Fixed costs line', marks: 3 },
      { id: 'tc', label: 'Total costs line', marks: 3 },
      { id: 'tr', label: 'Total revenue line', marks: 3 },
      { id: 'bep', label: 'Breakeven point marked', marks: 4 },
      { id: 'profit', label: 'Profit at forecast output marked', marks: 4 },
      { id: 'mos', label: 'Margin of safety marked', marks: 4 },
    ],
    shorthand: '25m (chart) — or calculations only: max 12m',
    ruleNote:
      'If no chart is drawn, only the three calculations can score: breakeven point 4, profit 4, margin of safety 4 — a hard cap of 12 of the 25 marks. Within the chart, the title is worth 2 and each axis label 1: the “furniture” alone is 4 marks.',
    cite: MS25('p.11 (Q8(C) grid)'),
  },
  scripts: [
    {
      id: 'b6-a',
      label: 'Script A',
      persona: 'Perfect calculations, no chart',
      attempts: [
        {
          id: 'b6-a-1',
          text: 'The page shows three correct calculations, clearly laid out: the breakeven point in units, the profit at forecast output, and the margin of safety. No chart is drawn anywhere in the answer.',
          key: { title: 0, xaxis: 0, yaxis: 0, fc: 0, tc: 0, tr: 0, bep: 4, profit: 4, mos: 4 },
          keyNote: 'Flawless arithmetic — capped at 12/25. The question asked for a chart, and 13 of the 25 marks only exist on the chart. Most students who skip the chart have no idea the cap is this severe.',
        },
      ],
      embodies: {
        behaviour: 'Does “calculations only” on a chart question — the scheme caps this at 12 of 25 marks.',
        cite: MS25('p.11'),
      },
    },
    {
      id: 'b6-b',
      label: 'Script B',
      persona: 'Drew the chart, skipped the furniture',
      attempts: [
        {
          id: 'b6-b-1',
          text: 'The page shows a neat chart with fixed costs, total costs and total revenue lines all correctly drawn, and the breakeven point marked where the lines cross. There is no chart title, neither axis is labelled, and neither the profit at forecast output nor the margin of safety is marked.',
          key: { title: 0, xaxis: 0, yaxis: 0, fc: 3, tc: 3, tr: 3, bep: 4, profit: 0, mos: 0 },
          keyNote: 'The three lines and the breakeven point earn well (13m) — but the missing title and axis labels quietly drop 4 marks, and the unmarked profit and margin of safety drop 8 more. 13/25 for a chart that “looks right”.',
        },
      ],
      embodies: {
        behaviour: 'Loses marks for failing to label and title the chart — flagged across chart questions at both levels.',
        cite: CER15('p.18'),
      },
    },
    {
      id: 'b6-c',
      label: 'Script C',
      persona: 'The full chart',
      attempts: [
        {
          id: 'b6-c-1',
          text: 'The page shows a titled breakeven chart with both axes labelled; fixed costs, total costs and total revenue lines drawn; the breakeven point, the profit at forecast output and the margin of safety all clearly marked on the chart.',
          key: { title: 2, xaxis: 1, yaxis: 1, fc: 3, tc: 3, tr: 3, bep: 4, profit: 4, mos: 4 },
          keyNote: '25/25. Note how the marks distribute: the title and labels a student thinks of as decoration are worth as much as a whole costs line.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b6',
    rule: 'On chart questions, the chart carries the majority of the marks.',
    detail:
      'Calculations alone cap at 12/25 on the breakeven grid, and title + axis labels are 4 marks of pure discipline. Draw the chart, label everything, mark every required point.',
    cite: MS25('p.11'),
  },
};

export const BUSINESS_CHAIR: ChairSubject = {
  id: 'business',
  label: 'Business',
  tagline: 'Grids, cues and links — where Business marks are actually won.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [B1, B2, B3, B4, B5, B6],
  sources: [
    { label: 'SEC Business HL marking scheme 2025 (examiner-reports/business/2025-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Business 2015 (examiner-reports/business/2015-chief-examiner)' },
  ],
  coverageNote:
    'Higher Level sessions are verified against the 2025 HL marking scheme. Ordinary Level shares the same question cues and grid logic; OL-specific sessions (verified against an OL scheme) are being added.',
};
