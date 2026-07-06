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
const MS24 = (p: string) => ({ label: `SEC Business HL marking scheme 2024, ${p}` });
const CER15 = (p: string) => ({ label: `Chief Examiner's Report, Business 2015, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Business OL marking scheme 2025, ${p}` });

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
      id: 'b1-e',
      label: 'Script E',
      persona: 'Paraphrases the case — never quotes it',
      attempts: [
        {
          id: 'b1-e-1',
          text: 'Adaptability: an entrepreneur adjusts their plans when circumstances change, finding new ways to keep the business running. Nora shows adaptability because when the weather turned against her she found another way to keep earning instead of giving up.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'Named (2) and explained (2) — but the “link” is the candidate’s own summary of what happened, not a phrase lifted from the case. The scheme wants a direct quote (here, “filmed a set of online balance-training tutorials”), so the link mark is lost. 4/5 — the near-miss that feels like a full answer.',
        },
        {
          id: 'b1-e-2',
          text: 'Initiative: acting without being prompted, creating opportunities rather than waiting for them. Nora shows initiative because she came up with a clever new way to make money during the storms.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'Same trap: sound theory, but “a clever new way to make money during the storms” paraphrases the case rather than quoting it. A direct phrase — e.g. she “filmed a set of online balance-training tutorials from her garage” — would have banked the mark. 4/5.',
        },
      ],
      embodies: {
        behaviour: 'Gestures at the case in their own words instead of quoting a direct phrase — the link mark needs an actual quote or phrase from the text.',
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
    'Case and question authored for this exercise. The illustrative grid — Name + Explain + Link + Evaluate — is one year’s ABQ evaluate template (SEC 2025 HL, where it carried a heavy 3-of-7 evaluate mark). The year-stable convention, not the exact split, is the point: the ABQ always includes an Evaluate task with its own separately-awarded judgement mark, and the exact weighting and which part it sits in are set per-question each year.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the control', marks: 1 },
      { id: 'explain', label: 'Explain the theory', marks: 2 },
      { id: 'link', label: 'Link to the case', marks: 1 },
      { id: 'eval', label: 'Evaluate: judgement + justification', marks: 3 },
    ],
    shorthand: '(1+2+1+3), evaluate separately awarded',
    ruleNote:
      'The Evaluate task carries its own mark, separate from Name/Explain/Link — and a verdict with no justification scores nothing for it. The exact weighting varies year to year (heavy in some ABQs, lighter in others), but the rule is constant: don’t stop after the link, and always justify the judgement.',
    cite: MS25('p.6 (2025 ABQ evaluate template; the separately-awarded evaluate mark is the year-stable convention)'),
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
          keyNote: 'Name, theory and case link are all here — and then it stops. The question asked for an evaluation, and no judgement was offered, so the separately-awarded evaluate mark scores zero. 4/7 — the answer did everything except the thing the cue asked for.',
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
      'On “Evaluate” cues the verdict alone is worth nothing — pair it with evidence or a criterion. The ABQ always carries an Evaluate task with its own separately-awarded judgement mark; don’t stop after Name/Explain/Link.',
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

// ═══════════════ Ordinary Level ═══════════════

// ─────────────── O1 · The asymmetric two-point grid ───────────────

const O1: GridSession = {
  mode: 'grid',
  id: 'biz-ol-asymmetric',
  subject: 'business',
  level: 'ordinary',
  title: 'The first point is worth double',
  cue: 'Explain two (OL)',
  question: 'An Ordinary Level “explain two” question is worth 15 marks, marked 10 (7+3) for the first point and 5 (4+1) for the second — each split into stating the point plus developing it. A candidate names and develops one point fully, then just names a second without developing it.',
  questionNote:
    'Scenario authored for this exercise. The signature OL Business grid is asymmetric: two-point questions pay 10 (7 state + 3 develop) for the first point and 5 (4 + 1) for the second, so one developed point caps at 10/15.',
  grid: {
    perPoint: [
      { id: 'p1state', label: 'Point 1 — stated', marks: 7 },
      { id: 'p1dev', label: 'Point 1 — developed', marks: 3 },
      { id: 'p2state', label: 'Point 2 — stated', marks: 4 },
      { id: 'p2dev', label: 'Point 2 — developed', marks: 1 },
    ],
    shorthand: '10 (7+3) + 5 (4+1)',
    ruleNote:
      'The first point carries 10 marks, the second only 5 — and each has a “develop it” tranche (3 and 1). One fully developed point caps at 10/15; two named-but-undeveloped points score 11/15; you need both stated AND developed to reach 15.',
    cite: MSOL('p.5 (asymmetric two-point grid)'),
  },
  scripts: [
    {
      id: 'o1-a',
      label: 'Script A',
      persona: 'One point developed, one just named',
      attempts: [
        {
          id: 'o1-a-1',
          text: 'Point 1: stated clearly and then developed with a reason and an example. Point 2: named only, with no development.',
          key: { p1state: 7, p1dev: 3, p2state: 4, p2dev: 0 },
          keyNote: '14 of 15 — the first point is complete (10), and the second is named (4) but the 1-mark development tranche is missed. Even here the asymmetry matters: developing the first point mattered far more than the second. Develop both to reach 15.',
        },
      ],
      embodies: {
        behaviour: 'Develops one point but leaves the second undeveloped — forfeiting its development tranche.',
        cite: MSOL('p.5'),
      },
    },
    {
      id: 'o1-b',
      label: 'Script B',
      persona: 'One point only',
      attempts: [
        {
          id: 'o1-b-1',
          text: 'One point, stated and fully developed. No second point attempted.',
          key: { p1state: 7, p1dev: 3, p2state: 0, p2dev: 0 },
          keyNote: 'Capped at 10 of 15 — a single point, however good, can only reach the first point’s 10 marks. The OL brevity trap, made concrete: give the second point, even briefly, to unlock the other 5.',
        },
      ],
      embodies: {
        behaviour: 'Gives only one point where two are required — the documented OL brevity trap.',
        cite: CER15('p.20'),
      },
    },
  ],
  takeaway: {
    id: 'codex-o1',
    rule: 'At OL, give both points — and develop each.',
    detail:
      'Ordinary Level two-point questions pay 10 (7+3) for the first and 5 (4+1) for the second, each with a “develop it” tranche. One point caps at 10/15; naming without developing forfeits the 3- and 1-mark tranches. Always give both points and develop both.',
    cite: MSOL('p.5'),
  },
};

// ─────────────────────── B7 · The example is a mark ───────────────────────

const B7: GridSession = {
  mode: 'grid',
  id: 'biz-example-mark',
  subject: 'business',
  level: 'higher',
  title: 'The example is a mark',
  cue: 'Explain, using examples',
  question:
    'Explain, using examples, two different types of industrial action a trade union might take.',
  questionNote:
    'Question authored for this exercise; marked on the SEC 2025 HL Section 3 template Q1(B) — 4@5 (2+2+1), Name + Explain + Example — shortened to two points here.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the item', marks: 2 },
      { id: 'explain', label: 'Explain the theory', marks: 2 },
      { id: 'example', label: 'Concrete example', marks: 1 },
    ],
    shorthand: '2@5 (2+2+1)',
    ruleNote:
      'On an “Explain, using examples” or “Illustrate” cue the Example is its own discrete mark — a flawless explanation with no concrete instance still forfeits it. Note the difference from the ABQ: here the mark buys YOUR own real-world example, not a quote lifted from a case. The cue tells you whether the 5th mark is an example (Illustrate / “using examples”) or a second layer of explanation (Discuss).',
    cite: MS25('p.7 (Q1(B) “Explain, using examples” grid — Name, explain, example)'),
  },
  scripts: [
    {
      id: 'b7-a',
      label: 'Script A',
      persona: 'Textbook definitions, no instances',
      attempts: [
        {
          id: 'b7-a-1',
          text: 'A strike is where employees withdraw their labour completely and refuse to work in order to put pressure on the employer to concede to their demands.',
          key: { name: 2, explain: 2, example: 0 },
          keyNote: 'Named (2) and explained (2) — but the cue asked for an example and none is given. A single instance (e.g. a one-day national bus strike) banks the last mark. 4/5.',
        },
        {
          id: 'b7-a-2',
          text: 'A work-to-rule is where employees do only the exact duties in their contract and nothing beyond them, slowing output without formally stopping work.',
          key: { name: 2, explain: 2, example: 0 },
          keyNote: 'Same near-miss: correct type, correct theory, no example. Across four such points the habit quietly leaks four marks. 4/5.',
        },
      ],
      embodies: {
        behaviour: 'Answers an “Explain, using examples” cue with definitions only — the cue-word requirement the report says is “often not addressed adequately.”',
        cite: CER15('p.20'),
      },
    },
    {
      id: 'b7-b',
      label: 'Script B',
      persona: 'Has the example — skips the theory',
      attempts: [
        {
          id: 'b7-b-1',
          text: 'An overtime ban — for example, nurses refusing to work any extra shifts beyond their rostered hours during a pay dispute.',
          key: { name: 2, explain: 0, example: 1 },
          keyNote: 'Named (2) with a real example (1), but the theory — what an overtime ban actually is and how it pressures the employer — is missing. The explain mark still has to be earned separately. 3/5.',
        },
      ],
    },
    {
      id: 'b7-c',
      label: 'Script C',
      persona: 'Name, theory, instance',
      attempts: [
        {
          id: 'b7-c-1',
          text: 'A strike: employees collectively withdraw their labour to pressure the employer into meeting their demands — for example, a one-day national stoppage by public-transport drivers over pay.',
          key: { name: 2, explain: 2, example: 1 },
          keyNote: 'Name, theory and a concrete instance — the full 2+2+1. 5/5.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b7',
    rule: 'Example cues buy an example mark.',
    detail:
      'When the cue is “Illustrate” or “Explain using examples”, one discrete mark per point is reserved for a concrete instance — and it’s your own real-world example, not a case quote. Learn the theory, then always attach a named example.',
    cite: MS25('p.7'),
  },
};

// ─────────────────────── B8 · Two of each, or half marks ───────────────────────

const B8: GridSession = {
  mode: 'grid',
  id: 'biz-two-of-each',
  subject: 'business',
  level: 'higher',
  title: 'Two of each, or half marks',
  cue: 'Discuss advantages and disadvantages',
  question:
    'Discuss the advantages and disadvantages of an acquisition (takeover) as a method of business expansion.',
  questionNote:
    'Question authored for this exercise; marked on the SEC 2025 HL Q7(A) template — 4@5 (2+3), Name + Explain, with the scheme’s explicit “2 of each required” instruction.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the point', marks: 2 },
      { id: 'explain', label: 'Explain / develop it', marks: 3 },
    ],
    shorthand: '4@5 (2+3) — 2 of each required',
    ruleNote:
      'When the cue names two sides — “advantages and disadvantages” — the scheme credits at most two of each: its note reads “2 of each required.” Four brilliant advantages score only two of them; the other two are worth nothing until you cross to the other side of the argument. A one-sided answer caps at 10 of 20.',
    cite: MS25('p.10 (Q7(A) “advantages and disadvantages” grid — “2 of each required”)'),
  },
  scripts: [
    {
      id: 'b8-a',
      label: 'Script A',
      persona: 'Four points — all on one side',
      attempts: [
        {
          id: 'b8-a-1',
          text: 'Advantage — Speed of growth: a takeover lets the buyer gain market share instantly rather than building capacity from scratch, developed with the reduced time-to-market this brings.',
          key: { name: 2, explain: 3 },
          keyNote: 'A valid, developed advantage. First of the two advantages the scheme will count. 5/5.',
        },
        {
          id: 'b8-a-2',
          text: 'Advantage — Access to resources: the acquirer gains the target’s premises, staff, patents and customer base in one move, developed with the example of buying an established brand.',
          key: { name: 2, explain: 3 },
          keyNote: 'Second developed advantage — also counted. 5/5. So far 10/20.',
        },
        {
          id: 'b8-a-3',
          text: 'Advantage — Economies of scale: the larger combined firm can spread fixed costs over more output and negotiate better with suppliers.',
          key: { name: 0, explain: 0 },
          keyNote: 'A perfectly good third advantage — worth nothing. The scheme counts only two advantages, and no disadvantage has been given. 0/5.',
        },
        {
          id: 'b8-a-4',
          text: 'Advantage — Eliminates a competitor: buying a rival removes it from the market and strengthens the acquirer’s position.',
          key: { name: 0, explain: 0 },
          keyNote: 'Fourth advantage, same fate. 0/5. Total 10/20 — a one-sided answer marked at exactly half.',
        },
      ],
      embodies: {
        behaviour: 'Argues only one side where the scheme requires “2 of each” — advantages and disadvantages.',
        cite: MS25('p.10'),
      },
    },
    {
      id: 'b8-b',
      label: 'Script B',
      persona: 'Three-one split',
      attempts: [
        {
          id: 'b8-b-1',
          text: 'Advantage — Speed of growth: instant market share instead of organic expansion, developed with reduced time-to-market.',
          key: { name: 2, explain: 3 },
          keyNote: 'Counted advantage one. 5/5.',
        },
        {
          id: 'b8-b-2',
          text: 'Advantage — Access to resources: premises, staff and customers acquired in one move.',
          key: { name: 2, explain: 3 },
          keyNote: 'Counted advantage two. 5/5.',
        },
        {
          id: 'b8-b-3',
          text: 'Advantage — Economies of scale: fixed costs spread over greater output.',
          key: { name: 0, explain: 0 },
          keyNote: 'A third advantage — over the cap of two, so it scores nothing. 0/5.',
        },
        {
          id: 'b8-b-4',
          text: 'Disadvantage — Culture clash: merging two workforces with different norms can cause conflict and lost productivity, developed with the risk of key staff leaving.',
          key: { name: 2, explain: 3 },
          keyNote: 'The first disadvantage — and the moment the answer starts scoring again. 5/5. Total 15/20: crossing sides even once unlocked five marks the third advantage never could.',
        },
      ],
    },
    {
      id: 'b8-c',
      label: 'Script C',
      persona: 'Balanced — two each',
      attempts: [
        {
          id: 'b8-c-1',
          text: 'Advantage — Speed of growth: instant market share, developed with reduced time-to-market.',
          key: { name: 2, explain: 3 },
          keyNote: 'Advantage one. 5/5.',
        },
        {
          id: 'b8-c-2',
          text: 'Advantage — Access to resources: premises, staff, patents and customers in one move.',
          key: { name: 2, explain: 3 },
          keyNote: 'Advantage two. 5/5.',
        },
        {
          id: 'b8-c-3',
          text: 'Disadvantage — Culture clash: merging workforces can cause conflict and lost output, developed with the risk of key staff leaving.',
          key: { name: 2, explain: 3 },
          keyNote: 'Disadvantage one. 5/5.',
        },
        {
          id: 'b8-c-4',
          text: 'Disadvantage — High cost / overpayment: the acquirer may overpay and take on the target’s hidden debts, developed with the strain on cash flow.',
          key: { name: 2, explain: 3 },
          keyNote: 'Disadvantage two. Full 20/20 — two developed points on each side, exactly what “2 of each required” pays for.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b8',
    rule: 'Discuss both sides — each side is capped.',
    detail:
      'When a “Discuss” cue names advantages and disadvantages, the scheme credits “2 of each” — a one-sided answer caps at half marks no matter how many points you pile on one side. Split your four points two-and-two.',
    cite: MS25('p.10'),
  },
};

// ─────────────────────── B9 · The format is marked ───────────────────────

const B9: GridSession = {
  mode: 'grid',
  id: 'biz-format-marks',
  subject: 'business',
  level: 'higher',
  title: 'The format is marked',
  cue: 'Calculate and state',
  question:
    'Calculate the Balance of Trade and state whether it is a surplus or a deficit. Show your workings. (Visible exports €72bn; visible imports €34bn.)',
  questionNote:
    'Figures and question modelled on the SEC 2024 HL Q2(A) Balance of Trade / Balance of Payments item. The scheme marks it: “formula 1 mark and each correct figure 1 mark, € sign 1 mark, surplus/deficit 1 mark.”',
  grid: {
    perPoint: [
      { id: 'formula', label: 'State the formula (Exports − Imports)', marks: 1 },
      { id: 'figures', label: 'Substitute the correct figures', marks: 1 },
      { id: 'euro', label: 'Include the € sign', marks: 1 },
      { id: 'verdict', label: 'State surplus or deficit', marks: 1 },
    ],
    shorthand: 'formula 1 · figures 1 · € sign 1 · surplus/deficit 1',
    ruleNote:
      'Two of the four marks are pure presentation: the € sign is a mark, and stating “surplus” or “deficit” is a mark. “State whether your answer is a surplus or a deficit” is not a courtesy — it is on the grid. Correct arithmetic with a bare number and no verdict throws away half the marks.',
    cite: MS24('p.8 (Q2(A) BoT/BoP grid — “€ sign 1 mark, surplus/deficit 1 mark”)'),
  },
  scripts: [
    {
      id: 'b9-a',
      label: 'Script A',
      persona: 'Right number, nothing else',
      attempts: [
        {
          id: 'b9-a-1',
          text: '72 − 34 = 38.',
          key: { formula: 1, figures: 1, euro: 0, verdict: 0 },
          keyNote: 'The formula is implied and the figures are right — but there is no € sign and no surplus/deficit verdict, each of which is a separate mark. 2/4 for a numerically correct answer.',
        },
      ],
      embodies: {
        behaviour: 'Omits the currency sign and the surplus/deficit verdict — each of which the scheme marks separately.',
        cite: MS24('p.8'),
      },
    },
    {
      id: 'b9-b',
      label: 'Script B',
      persona: 'Currency, but no verdict',
      attempts: [
        {
          id: 'b9-b-1',
          text: '€72bn − €34bn = €38bn.',
          key: { formula: 1, figures: 1, euro: 1, verdict: 0 },
          keyNote: 'Now the € sign is there (1). But the question explicitly asked whether it is a surplus or a deficit, and that word is missing — the last mark is still on the table. 3/4.',
        },
      ],
    },
    {
      id: 'b9-c',
      label: 'Script C',
      persona: 'Formula, figures, format, verdict',
      attempts: [
        {
          id: 'b9-c-1',
          text: 'Balance of Trade = Visible Exports − Visible Imports = €72bn − €34bn = €38bn surplus.',
          key: { formula: 1, figures: 1, euro: 1, verdict: 1 },
          keyNote: 'Formula, figures, currency and the surplus verdict — the full 4/4. The two “format” marks cost nothing but attention.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b9',
    rule: 'In financial answers, the format carries marks.',
    detail:
      'On BoT/BoP and similar computations the € sign and the surplus/deficit verdict are each their own mark. Write the formula, keep the currency sign on every figure, and end with the word the question asked for — surplus or deficit.',
    cite: MS24('p.8'),
  },
};

// ─────────────────────── B10 · Own figure allowed ───────────────────────

const B10: GridSession = {
  mode: 'grid',
  id: 'biz-own-figure',
  subject: 'business',
  level: 'higher',
  title: 'Own figure allowed',
  cue: 'Calculate (multi-step)',
  question:
    'Calculate the Balance of Payments and state whether it is a surplus or a deficit. Show your workings. (Total exports: visible €72bn + invisible €93bn; total imports: visible €34bn + invisible €84bn.)',
  questionNote:
    'Figures modelled on the SEC 2024 HL Q2(A) Balance of Payments item, whose worked solution is annotated “Own Figure Allowed” on the later steps — a wrong subtotal carried consistently forward still earns the downstream marks.',
  grid: {
    perPoint: [
      { id: 'formula', label: 'Correct BoP formula', marks: 1 },
      { id: 'subtotal', label: 'Correct export/import subtotals', marks: 1 },
      { id: 'result', label: 'Final subtraction using own subtotals', marks: 1 },
      { id: 'verdict', label: 'Surplus/deficit consistent with own result', marks: 1 },
    ],
    shorthand: 'formula 1 · subtotals 1 · result 1 · verdict 1 — “Own Figure Allowed”',
    ruleNote:
      'The scheme prints “Own Figure Allowed” beside the closing steps: a candidate who mis-adds a subtotal but carries that wrong figure consistently into the final subtraction still earns the result and verdict marks. One slip costs one mark — not the whole answer — but only if the workings are shown and internally consistent.',
    cite: MS24('p.38 (Q2(A) BoP worked solution — “Own Figure Allowed”)'),
  },
  scripts: [
    {
      id: 'b10-a',
      label: 'Script A',
      persona: 'One slip, carried honestly',
      attempts: [
        {
          id: 'b10-a-1',
          text: 'BoP = Total Exports − Total Imports. Total exports = 72 + 93 = €165bn. Total imports = 34 + 84 = €128bn. BoP = €165bn − €128bn = €37bn surplus.',
          key: { formula: 1, subtotal: 0, result: 1, verdict: 1 },
          keyNote: 'The imports subtotal is wrong (34 + 84 = 118, not 128), so the subtotal mark is lost. But €165bn − €128bn = €37bn is correct arithmetic on the candidate’s OWN figure, and the surplus verdict is consistent — so both downstream marks stand. 3/4: one slip, one mark.',
        },
      ],
      embodies: {
        behaviour: 'Makes a single subtotal error but carries it consistently — the exact case the “Own Figure Allowed” annotation is written for.',
        cite: MS24('p.38'),
      },
    },
    {
      id: 'b10-b',
      label: 'Script B',
      persona: 'Bare wrong answer, no workings',
      attempts: [
        {
          id: 'b10-b-1',
          text: '€37bn',
          key: { formula: 0, subtotal: 0, result: 0, verdict: 0 },
          keyNote: 'The same wrong final figure as Script A — but with no formula, no subtotals and no surplus/deficit word, there is nothing for “Own Figure Allowed” to attach to. 0/4. The rule rescues shown workings, never a bare number.',
        },
      ],
      embodies: {
        behaviour: 'Gives a bare final figure with no workings — “Own Figure Allowed” cannot apply without a shown, consistent method.',
        cite: MS24('p.38'),
      },
    },
    {
      id: 'b10-c',
      label: 'Script C',
      persona: 'Clean throughout',
      attempts: [
        {
          id: 'b10-c-1',
          text: 'BoP = Total Exports − Total Imports = €165bn − €118bn = €47bn surplus. (Exports 72 + 93 = 165; imports 34 + 84 = 118.)',
          key: { formula: 1, subtotal: 1, result: 1, verdict: 1 },
          keyNote: 'Correct subtotals, correct result, surplus stated. 4/4 — and had a slip crept in, the shown method would still have protected three of the four marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b10',
    rule: 'Own figure allowed — so show your method.',
    detail:
      'SEC financial questions carry an “Own Figure Allowed” rule: one arithmetic slip carried consistently forward costs a single mark, not the answer. It only works if your workings are on the page — a bare wrong number earns nothing.',
    cite: MS24('p.38'),
  },
};

// ─────────────────────── B11 · The link is not an afterthought ───────────────────────

const B11: GridSession = {
  mode: 'grid',
  id: 'biz-link-weight',
  subject: 'business',
  level: 'higher',
  title: 'The link is not an afterthought',
  cue: 'Describe (ABQ, refer to text)',
  caseText:
    'At Corrib Foods, staff turnover fell after the HR manager, Deirdre, rebuilt the induction programme and introduced a structured annual appraisal where every employee sets goals with their line manager. The company also runs a monthly training budget of €4,000 that Deirdre allocates against skills gaps identified in those appraisals.',
  question:
    'Describe two human resource management (HRM) functions carried out at Corrib Foods. Refer to the text in your answer.',
  questionNote:
    'Case and question authored for this exercise. The grid is the SEC 2025 HL ABQ Part (C) template — 5@6 (2+2+2), Name + Explain + Link, where the Link is weighted 2 of 6 — tied for the heaviest sub-mark. Shortened to two points here.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the HRM function', marks: 2 },
      { id: 'explain', label: 'Explain the theory', marks: 2 },
      { id: 'link', label: 'Link: direct case quote/phrase', marks: 2 },
    ],
    shorthand: '2@6 (2+2+2) — link weighted 2',
    ruleNote:
      'In Part (A) the case link is 1 of 5 — cheap enough to treat as a bonus. But in the “Describe HRM functions” part it is 2 of 6, tied with Name and Explain for the heaviest sub-mark. The link’s weight scales with the part, so skipping it here — where students habitually treat it as an add-on — costs the most.',
    cite: MS25('p.6 (ABQ Part (C) grid — 5@6 (2+2+2) Name, Explain, Link)'),
  },
  scripts: [
    {
      id: 'b11-a',
      label: 'Script A',
      persona: 'Theory-perfect, case-blind',
      attempts: [
        {
          id: 'b11-a-1',
          text: 'Training and development: HRM ensures employees have the skills to do their jobs by identifying skills gaps and providing courses, which improves performance and motivation.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'Named and explained (4) — but no phrase from the case. Here that costs 2, not 1: the link is the heaviest mark in this part. 4/6.',
        },
        {
          id: 'b11-a-2',
          text: 'Performance appraisal: HRM formally reviews each employee’s performance against objectives so that strengths are recognised and development needs are planned.',
          key: { name: 2, explain: 2, link: 0 },
          keyNote: 'Same shortfall. Two no-link points here leak four marks — the price of treating the link as optional in the part where it is worth most. 4/6.',
        },
      ],
      embodies: {
        behaviour: 'Treats the case link as a low-value add-on in the ABQ part where it is weighted heaviest (2 of 6).',
        cite: MS25('p.6'),
      },
    },
    {
      id: 'b11-b',
      label: 'Script B',
      persona: 'Names and links — thin theory',
      attempts: [
        {
          id: 'b11-b-1',
          text: 'Training and development: Deirdre “allocates [a monthly training budget] against skills gaps identified in those appraisals” at Corrib Foods.',
          key: { name: 2, explain: 0, link: 2 },
          keyNote: 'A named function (2) with a strong, direct case link (2) — but no general theory of what the training-and-development function is or why it matters. The explain mark is separate and unearned. 4/6.',
        },
      ],
    },
    {
      id: 'b11-c',
      label: 'Script C',
      persona: 'Name, theory, heavy link',
      attempts: [
        {
          id: 'b11-c-1',
          text: 'Training and development: HRM closes skills gaps by funding relevant learning so staff can perform and grow. At Corrib Foods the €4,000 monthly budget is “allocated against skills gaps identified in those appraisals”.',
          key: { name: 2, explain: 2, link: 2 },
          keyNote: 'Name (2) + theory (2) + a direct case phrase (2). Full 6/6 — and the link, done properly, was the single most valuable move.',
        },
        {
          id: 'b11-c-2',
          text: 'Performance appraisal: HRM reviews performance against agreed objectives to plan development. At Corrib Foods “every employee sets goals with their line manager” at a “structured annual appraisal”.',
          key: { name: 2, explain: 2, link: 2 },
          keyNote: 'A different function, a different quote, theory tied to it. 6/6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-b11',
    rule: 'The link’s weight scales with the ABQ part.',
    detail:
      'The case link is 1 of 5 in Part (A) but 2 of 6 in the “Describe HRM functions” part — tied for the heaviest sub-mark. Never treat the link as a throwaway; check what it’s worth in the part you’re answering and quote the case every time.',
    cite: MS25('p.6'),
  },
};

// ─────────────── O2 · The labels are the diagram (OL) ───────────────

const O2: GridSession = {
  mode: 'grid',
  id: 'biz-ol-diagram-labels',
  subject: 'business',
  level: 'ordinary',
  title: 'The labels are the diagram',
  cue: 'Draw and label',
  question:
    'Draw and label a Product Life Cycle diagram. (Each script below describes what a candidate actually put on the page.)',
  questionNote:
    'Scenario authored for this exercise; the grid is the SEC 2025 OL Q8(E) Product Life Cycle template, item for item: Title 1m, Sales axis 1m, Time axis 1m, Curved line 2m, Labels (in order) 5 × 2m = 15m.',
  grid: {
    perPoint: [
      { id: 'title', label: 'Chart title', marks: 1 },
      { id: 'sales', label: 'Sales axis labelled', marks: 1 },
      { id: 'time', label: 'Time axis labelled', marks: 1 },
      { id: 'curve', label: 'Curved line drawn', marks: 2 },
      { id: 'l1', label: 'Stage label 1 (Introduction)', marks: 2 },
      { id: 'l2', label: 'Stage label 2 (Growth)', marks: 2 },
      { id: 'l3', label: 'Stage label 3 (Maturity)', marks: 2 },
      { id: 'l4', label: 'Stage label 4 (Saturation)', marks: 2 },
      { id: 'l5', label: 'Stage label 5 (Decline)', marks: 2 },
    ],
    shorthand: 'Title 1 · Sales 1 · Time 1 · Curve 2 · Labels (in order) 5×2 = 15m',
    ruleNote:
      'The five stage-labels, in the correct order, are 10 of the 15 marks. A beautifully drawn, correctly shaped curve with both axes named but no stage labels caps at 5/15. At OL the labels — and their order — are where a diagram’s marks actually live.',
    cite: MSOL('p.40 (Q8(E) PLC grid — “Labels (in order) 5 × 2m”)'),
  },
  scripts: [
    {
      id: 'o2-a',
      label: 'Script A',
      persona: 'Perfect curve, no labels',
      attempts: [
        {
          id: 'o2-a-1',
          text: 'The page shows a neatly drawn, correctly shaped product life cycle curve with a title and both axes labelled “Sales” and “Time”. None of the five stages is labelled along the curve.',
          key: { title: 1, sales: 1, time: 1, curve: 2, l1: 0, l2: 0, l3: 0, l4: 0, l5: 0 },
          keyNote: 'Title, axes and curve are all there (5m) — and then the answer stops. The five stage-labels are 10 of the 15 marks, and none was written. 5/15 for a diagram that “looks right”.',
        },
      ],
      embodies: {
        behaviour: 'Draws the chart but omits the labels, which carry the majority of the marks — the universal chart failure the report flags at OL.',
        cite: CER15('p.21'),
      },
    },
    {
      id: 'o2-b',
      label: 'Script B',
      persona: 'Labels done, furniture forgotten',
      attempts: [
        {
          id: 'o2-b-1',
          text: 'The page shows the curve with all five stages labelled in order — Introduction, Growth, Maturity, Saturation, Decline — but there is no title on the diagram and neither axis is labelled.',
          key: { title: 0, sales: 0, time: 0, curve: 2, l1: 2, l2: 2, l3: 2, l4: 2, l5: 2 },
          keyNote: 'The curve and all five ordered labels earn 12 — but the missing title and two axis labels quietly drop 3. 12/15.',
        },
      ],
    },
    {
      id: 'o2-c',
      label: 'Script C',
      persona: 'Titled, axed, curved, labelled',
      attempts: [
        {
          id: 'o2-c-1',
          text: 'The page shows a titled PLC diagram with “Sales” and “Time” axes, a correctly shaped curve, and all five stages labelled in order along it.',
          key: { title: 1, sales: 1, time: 1, curve: 2, l1: 2, l2: 2, l3: 2, l4: 2, l5: 2 },
          keyNote: '15/15. The labels a student thinks of as finishing touches were two-thirds of the marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-o2',
    rule: 'On OL diagrams, the labels are most of the marks.',
    detail:
      'The Product Life Cycle grid pays 10 of 15 marks for the five stage-labels in order, and only 3 for title and axes. Draw the curve, name both axes, and label every stage in sequence — the labels are the diagram’s real content.',
    cite: MSOL('p.40'),
  },
};

// ─────────────── O3 · The document is a checklist (OL) ───────────────

const O3: GridSession = {
  mode: 'grid',
  id: 'biz-ol-agm-document',
  subject: 'business',
  level: 'ordinary',
  title: 'The document is a checklist',
  cue: 'Draft (business document)',
  question:
    'Draft a Notice and Agenda for the Annual General Meeting (AGM) of a company. (Each script below describes what a candidate put on the page.)',
  questionNote:
    'Scenario authored for this exercise; the grid is the SEC 2025 OL Q6(C) AGM template — Notice 4 × 1m, Agenda 5 × 2m (“must contain at least five items”), Signed 1m = 15m.',
  grid: {
    perPoint: [
      { id: 'notice', label: 'Notice — 4 required elements', marks: 4 },
      { id: 'a1', label: 'Agenda item 1', marks: 2 },
      { id: 'a2', label: 'Agenda item 2', marks: 2 },
      { id: 'a3', label: 'Agenda item 3', marks: 2 },
      { id: 'a4', label: 'Agenda item 4', marks: 2 },
      { id: 'a5', label: 'Agenda item 5', marks: 2 },
      { id: 'signed', label: 'Signed by the secretary', marks: 1 },
    ],
    shorthand: 'Notice 4 · Agenda 5×2 · Signed 1 = 15m',
    ruleNote:
      'A business document is marked as a checklist of prescribed components. The agenda alone is 10 of the 15 marks and “must contain at least five items” — fewer than five directly caps the agenda score. The notice elements and the secretary’s signature each carry their own marks too, so the “furniture” is not optional.',
    cite: MSOL('p.6 (Q6(C) AGM grid — Notice 4@1m, Agenda 5@2m, Signed 1m)'),
  },
  scripts: [
    {
      id: 'o3-a',
      label: 'Script A',
      persona: 'Good notice, short agenda',
      attempts: [
        {
          id: 'o3-a-1',
          text: 'A correct notice (date, time, venue and purpose of the AGM), then an agenda with three items — minutes of the last meeting, chairperson’s address, and any other business — signed by the secretary.',
          key: { notice: 4, a1: 2, a2: 2, a3: 2, a4: 0, a5: 0, signed: 1 },
          keyNote: 'Notice (4) and signature (1) are there, but the agenda has only three of the required five items, so two 2-mark slots are empty. 11/15 — the missing agenda items are the cheapest marks on the page.',
        },
      ],
      embodies: {
        behaviour: 'Supplies fewer than the five agenda items the scheme requires — the agenda “must contain at least five items”.',
        cite: MSOL('p.6'),
      },
    },
    {
      id: 'o3-b',
      label: 'Script B',
      persona: 'Full agenda, no wrapper',
      attempts: [
        {
          id: 'o3-b-1',
          text: 'Five clear agenda items — minutes, chairperson’s address, directors’ report, election of directors, and any other business — but with no notice (no date, time or venue) at the top and no secretary’s signature at the bottom.',
          key: { notice: 0, a1: 2, a2: 2, a3: 2, a4: 2, a5: 2, signed: 0 },
          keyNote: 'The full five-item agenda earns 10 — but the missing notice and signature are marked components too, and both are gone. 10/15.',
        },
      ],
    },
    {
      id: 'o3-c',
      label: 'Script C',
      persona: 'Every component present',
      attempts: [
        {
          id: 'o3-c-1',
          text: 'A complete notice (date, time, venue, purpose), a five-item agenda (minutes, chairperson’s address, directors’ report, election of directors, AOB), signed by the secretary.',
          key: { notice: 4, a1: 2, a2: 2, a3: 2, a4: 2, a5: 2, signed: 1 },
          keyNote: '15/15 — every prescribed component of the document present and correct.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-o3',
    rule: 'Business documents are marked component-by-component.',
    detail:
      'An AGM answer is a checklist: a full notice, at least five agenda items, and the secretary’s signature each carry marks, with the agenda worth 10 of 15. Give all five agenda items and don’t drop the notice or the signature.',
    cite: MSOL('p.6'),
  },
};

// ─────────────── O4 · Three points, three equal fifths (OL) ───────────────

const O4: GridSession = {
  mode: 'grid',
  id: 'biz-ol-three-point',
  subject: 'business',
  level: 'ordinary',
  title: 'Three points, three equal fifths',
  cue: 'Outline three (OL)',
  question:
    'An Ordinary Level “outline three” question is worth 15 marks, marked at 5 marks each (4m to state the point + 1m to develop it) — a symmetric grid, unlike the asymmetric two-point one. A candidate gives only two of the three points required.',
  questionNote:
    'Scenario authored for this exercise; the grid is the SEC 2025 OL Q5(C) template — “Outline three skills: @ 5 marks each (4m + 1m)”. Where a two-point question is asymmetric (10 / 5), a three-point question is symmetric — every point is worth the same 5.',
  grid: {
    perPoint: [
      { id: 'state', label: 'State the point', marks: 4 },
      { id: 'develop', label: 'Develop it', marks: 1 },
    ],
    shorthand: '3 @ 5 each (4+1) — symmetric',
    ruleNote:
      'When three points are required the grid is symmetric: each point is worth 5 (4 to state, 1 to develop). There is no cheap point to skip — omitting the third costs a full 5 marks (33%), not the small 5-mark tail of the asymmetric two-point grid. Give all three, and add the development line to each.',
    cite: MSOL('p.6 (Q5(C) “Outline three” grid — “@ 5 marks each (4m + 1m)”)'),
  },
  scripts: [
    {
      id: 'o4-a',
      label: 'Script A',
      persona: 'Two of three, both developed',
      attempts: [
        {
          id: 'o4-a-1',
          text: 'Point 1: stated and developed with a reason.',
          key: { state: 4, develop: 1 },
          keyNote: 'A complete point. 5/5.',
        },
        {
          id: 'o4-a-2',
          text: 'Point 2: stated and developed with a reason.',
          key: { state: 4, develop: 1 },
          keyNote: 'A second complete point. 5/5 — but the third point was never attempted, and on a symmetric grid that is a full 5 marks gone. 10/15.',
        },
      ],
      embodies: {
        behaviour: 'Gives only two points where three are required — the OL brevity trap, made expensive by the symmetric grid.',
        cite: CER15('p.20'),
      },
    },
    {
      id: 'o4-b',
      label: 'Script B',
      persona: 'Three named, none developed',
      attempts: [
        {
          id: 'o4-b-1',
          text: 'Point 1: named, no development.',
          key: { state: 4, develop: 0 },
          keyNote: 'Stated (4) but not developed — the 1-mark tail is lost.',
        },
        {
          id: 'o4-b-2',
          text: 'Point 2: named, no development.',
          key: { state: 4, develop: 0 },
          keyNote: 'Same again. 4/5.',
        },
        {
          id: 'o4-b-3',
          text: 'Point 3: named, no development.',
          key: { state: 4, develop: 0 },
          keyNote: 'Three named points beat two developed ones here (12 vs 10) — but a develop line on each would have banked the last three marks. 12/15.',
        },
      ],
    },
    {
      id: 'o4-c',
      label: 'Script C',
      persona: 'Three, each developed',
      attempts: [
        {
          id: 'o4-c-1',
          text: 'Point 1: stated and developed.',
          key: { state: 4, develop: 1 },
          keyNote: 'Named (4) and developed (1) — full 5. Each of the three points is worth the same 5, so all three must be attempted.',
        },
        {
          id: 'o4-c-2',
          text: 'Point 2: stated and developed.',
          key: { state: 4, develop: 1 },
          keyNote: 'A second point, named (4) and developed (1) — another full 5. Symmetric marking: no point is a cheap tail.',
        },
        {
          id: 'o4-c-3',
          text: 'Point 3: stated and developed.',
          key: { state: 4, develop: 1 },
          keyNote: 'All three points stated and developed. 15/15.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-o4',
    rule: 'Three-point OL grids are symmetric.',
    detail:
      'Unlike the asymmetric two-point grid (10 / 5), an “outline three” question pays 5 for every point (4 + 1). There is no cheap point to drop — skip one and you lose a full third of the marks. Give all three and develop each.',
    cite: MSOL('p.6'),
  },
};

export const BUSINESS_CHAIR: ChairSubject = {
  id: 'business',
  label: 'Business',
  tagline: 'Grids, cues and links — where Business marks are actually won.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, O1, O2, O3, O4],
  sources: [
    { label: 'SEC Business HL marking scheme 2025 (examiner-reports/business/2025-marking-scheme)' },
    { label: 'SEC Business HL marking scheme 2024 (examiner-reports/business/2024-marking-scheme)' },
    { label: 'SEC Business OL marking scheme 2025 (examiner-reports/business/2025-ol-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Business 2015 (examiner-reports/business/2015-chief-examiner)' },
  ],
  coverageNote:
    'Higher Level sessions are verified against the 2025 and 2024 HL schemes; the Ordinary Level sessions are verified against the 2025 OL scheme (note: OL has no ABQ, and uses asymmetric two-point / symmetric three-point grids). The BoT/BoP “€ sign”, “surplus/deficit” and “Own Figure Allowed” rules are drawn from the 2024 HL scheme, where that question appears.',
};
