/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * collegeCompassData.ts — content + helpers for the College Compass tool.
 *
 * ───────────────────────────────────────────────────────────────────────────
 * ⚠️  CONTENT ACCURACY — READ BEFORE EACH CYCLE
 * ───────────────────────────────────────────────────────────────────────────
 * Every date, threshold, points value and euro figure below changes EVERY
 * admissions cycle. These are 2026-cycle reference values, last verified on
 * COMPASS_LAST_VERIFIED. Before each new cycle they MUST be re-checked against
 * the official handbooks (cao.ie, accesscollege.ie, susi.ie, hea.ie) — see
 * COMPASS_SOURCES. NO euro figure here is authoritative; all eligibility
 * checks are ESTIMATES ONLY and the UI must always say so.
 *
 * Dates are stored CYCLE-RELATIVE (month/day, no year) and resolved at runtime
 * by resolveCycleDate(), so the trail auto-rolls each cycle and never presents
 * an already-passed date as upcoming. See computeStopStates().
 */

// ─── Primitives ─────────────────────────────────────────────────────────────

export type CompassScheme = 'cao' | 'hear' | 'dare' | 'scholarship' | 'results';

/** Live = current 6th years (countdowns + checklist). Orientation = TY/5th
 *  years previewing the cycle ahead (no countdowns, no checklist pressure). */
export type CompassMode = 'live' | 'orientation';

/** A cycle-relative calendar anchor — month (1-12) + day, NO year. */
export interface CycleDate {
  month: number;
  day: number;
  label: string; // human label, e.g. "1 Feb" — descriptive only, not parsed
}

export interface VerifyMeta {
  sourceLabel: string;
  sourceUrl: string;
  lastChecked: string; // ISO date
}

export interface JourneyMyth {
  claim: string;
  verdict: 'true' | 'false';
  explainer: string;
}

export interface ChecklistItemDef {
  id: string;
  label: string;
  detail?: string;
}

export interface CrossLink {
  /** Must match an Innovation Zone tool id (future-finder, cao-simulator, …). */
  toolId: string;
  title: string;
  description: string;
}

export interface JourneyStop {
  id: string;
  order: number;
  title: string;
  scheme: CompassScheme;
  start: CycleDate;
  end?: CycleDate;
  /** One-line "what this stop is". */
  tagline: string;
  /** The accent "why this matters" callout. */
  whyItMatters: string;
  myths: JourneyMyth[];
  /** Rendered + persisted only in live mode (6th years). */
  checklistItems: ChecklistItemDef[];
  crossLinks: CrossLink[];
  verify: VerifyMeta;
}

export const COMPASS_LAST_VERIFIED = '2026-05-29';

// ─── Hero copy (keyed by mode) ───────────────────────────────────────────────

export const HERO_COPY: Record<CompassMode, { eyebrow: string; title: string; tagline: string }> = {
  live: {
    eyebrow: 'Your runway · Live',
    title: 'College Compass',
    tagline: 'Every CAO, HEAR, DARE and scholarship deadline of your final year — in order, with what to do next.',
  },
  orientation: {
    eyebrow: 'The year ahead · Preview',
    title: 'College Compass',
    tagline: 'A calm preview of the application year coming at you — so none of it takes you by surprise.',
  },
};

// ─── The six trail stops ─────────────────────────────────────────────────────

export const JOURNEY_STOPS: JourneyStop[] = [
  {
    id: 'doors-open',
    order: 1,
    title: 'Doors Open',
    scheme: 'cao',
    start: { month: 11, day: 5, label: '5 Nov' },
    end: { month: 1, day: 20, label: '20 Jan' },
    tagline: 'The CAO opens — apply early and save on the fee.',
    whyItMatters:
      'The CAO doesn’t decide who gets in or set "the points" — colleges do. The CAO just collects applications, ranks them by points after results, and passes on the colleges’ offers. Applying and paying before the discounted-fee deadline saves you money.',
    myths: [
      {
        claim: 'The CAO decides who gets a place and sets the points.',
        verdict: 'false',
        explainer:
          'The CAO is a clearing house. Each college sets its own entry rules and selects its students. "Points required" is just the score of the last person admitted, worked out after results.',
      },
    ],
    checklistItems: [
      { id: 'create-account', label: 'Create my CAO account at cao.ie' },
      { id: 'pay-discount', label: 'Apply + pay before the discounted-fee deadline', detail: 'The early rate is cheaper than the standard rate — verify both on cao.ie.' },
    ],
    crossLinks: [
      { toolId: 'future-finder-revamped', title: 'Not sure what to put down?', description: 'Explore courses and careers that fit who you are in Future Finder.' },
    ],
    verify: { sourceLabel: 'cao.ie — How to Apply & Important Dates', sourceUrl: 'https://www.cao.ie/apply.php', lastChecked: COMPASS_LAST_VERIFIED },
  },
  {
    id: 'lock-in',
    order: 2,
    title: 'Lock-In Day',
    scheme: 'cao',
    start: { month: 2, day: 1, label: '1 Feb (17:00)' },
    tagline: 'CAO closes at 5pm on 1 Feb — the hard gate for restricted courses.',
    whyItMatters:
      'Restricted courses — Medicine (HPAT), portfolio and audition courses, some interview routes — must be on your list by 1 February. They generally cannot be added later, not even at Change of Mind. List every course in genuine order of preference.',
    myths: [
      {
        claim: 'Listing a course lower down hurts my chances of getting it.',
        verdict: 'false',
        explainer:
          'Your order only decides which course you’re offered first. Putting a course at #8 instead of #1 never lowers your chance of being offered it — you’re offered the highest one you qualify for.',
      },
      {
        claim: 'I should only list courses I think I’ll get the points for.',
        verdict: 'false',
        explainer:
          'List in genuine order of preference, dream courses at the top. There is no penalty for aiming high — if you don’t reach one, it simply moves to your next preference.',
      },
    ],
    checklistItems: [
      { id: 'final-list', label: 'Final course list submitted in genuine order of preference' },
      { id: 'restricted-added', label: 'Any restricted courses added', detail: 'These generally can’t be added after 1 Feb.' },
      { id: 'tests-registered', label: 'Registered for HPAT / portfolio / audition if needed' },
    ],
    crossLinks: [
      { toolId: 'future-finder-revamped', title: 'Still weighing options?', description: 'Compare courses side by side in Future Finder before you lock your list.' },
    ],
    verify: { sourceLabel: 'cao.ie — Restricted-Application Courses', sourceUrl: 'https://www.cao.ie/index.php?page=restrictedcourses&bb=restrictions', lastChecked: COMPASS_LAST_VERIFIED },
  },
  {
    id: 'access-window',
    order: 3,
    title: 'The Access Window',
    scheme: 'hear',
    start: { month: 3, day: 1, label: '~1 Mar (forms)' },
    end: { month: 3, day: 10, label: '~10 Mar (documents)' },
    tagline: 'HEAR & DARE deadlines — months before the Leaving Cert, on a separate clock.',
    whyItMatters:
      'This is the trap most people miss: HEAR and DARE run on an earlier, separate timeline. You flag them on your CAO application by 1 Feb, complete the online form by around 1 March, and post documents to arrive by around 10 March. Miss it and you can’t apply — they don’t chase missing documents.',
    myths: [
      {
        claim: 'HEAR and DARE deadlines are the same as the normal CAO dates.',
        verdict: 'false',
        explainer:
          'They’re much earlier. The online forms close around 1 March and documents must arrive by around 10 March — long before the Leaving Cert and the late-cycle CAO dates.',
      },
      {
        claim: 'A diagnosis is enough to qualify for DARE.',
        verdict: 'false',
        explainer:
          'DARE needs BOTH a specialist diagnosis AND evidence (through your school) that it negatively affected your education. One without the other is not enough.',
      },
    ],
    checklistItems: [
      { id: 'flag-cao', label: 'Flagged HEAR/DARE on my CAO application by 1 Feb' },
      { id: 'hear-form', label: 'HEAR online form submitted (if applying)' },
      { id: 'dare-sif', label: 'DARE Section A — ticked YES to Q1 (if applying)' },
      { id: 'docs-posted', label: 'Supporting documents posted to arrive by the deadline' },
    ],
    crossLinks: [],
    verify: { sourceLabel: 'accesscollege.ie — HEAR & DARE', sourceUrl: 'https://accesscollege.ie', lastChecked: COMPASS_LAST_VERIFIED },
  },
  {
    id: 'money-stops',
    order: 4,
    title: 'Money Stops',
    scheme: 'scholarship',
    start: { month: 4, day: 1, label: 'SUSI ~Apr' },
    end: { month: 10, day: 10, label: 'Bursary ~Oct' },
    tagline: 'Grants and scholarships — the four things students always mix up.',
    whyItMatters:
      'SUSI is a grant, decided on household income, not grades — not a scholarship. Free Fees covers most tuition automatically (you still owe the Student Contribution). Scholarships are extra and college-specific — some automatic on results, some you must apply for separately. Sorting out which is which is half the battle.',
    myths: [
      {
        claim: 'SUSI is a scholarship for high achievers.',
        verdict: 'false',
        explainer:
          'SUSI is a means-tested government grant — decided on your household income, not your results. Scholarships are separate, usually merit-based, and run by individual colleges.',
      },
      {
        claim: 'All scholarships are automatic if you do well enough.',
        verdict: 'false',
        explainer:
          'Some entrance scholarships are automatic on your CAO/LC results, but many — and all sports scholarships — need a separate application with their own deadline, often before you even get results.',
      },
    ],
    checklistItems: [
      { id: 'susi', label: 'Apply to SUSI when it opens (~April)' },
      { id: 'scholarship-deadlines', label: 'Diarised any scholarship deadlines (sports, all-rounder…)' },
      { id: 'bursary', label: 'Checked the 1916 Bursary (~Sept) if eligible' },
    ],
    crossLinks: [],
    verify: { sourceLabel: 'susi.ie & hea.ie — grants, fees & bursaries', sourceUrl: 'https://www.susi.ie/eligibility-criteria/', lastChecked: COMPASS_LAST_VERIFIED },
  },
  {
    id: 'change-of-mind',
    order: 5,
    title: 'Change Your Mind',
    scheme: 'cao',
    start: { month: 5, day: 5, label: '~5 May' },
    end: { month: 7, day: 1, label: '1 Jul (17:00)' },
    tagline: 'The free Change of Mind window — re-order or swap courses, as often as you like.',
    whyItMatters:
      'Change of Mind is free, and your latest saved order is the one that counts. Accepting a Round 1 offer never locks you out of a higher preference in a later round — you stay in the running for everything above it automatically.',
    myths: [
      {
        claim: 'Changing my mind costs money.',
        verdict: 'false',
        explainer:
          'The Change of Mind facility (around 5 May–1 Jul) is free. The earlier Feb–Mar amendment window carries a small fee — that’s a different thing, and you usually won’t need it.',
      },
      {
        claim: 'If I accept an offer, I’m locked in and can’t move up.',
        verdict: 'false',
        explainer:
          'Accepting keeps you in the running for all your higher preferences in later rounds. You don’t lose your place by accepting a lower one in the meantime.',
      },
    ],
    checklistItems: [
      { id: 'review-order', label: 'Reviewed and updated my order of preference' },
    ],
    crossLinks: [
      { toolId: 'cao-simulator', title: 'Run the numbers', description: 'See how grade changes ripple through your CAO total in the CAO Points Simulator.' },
    ],
    verify: { sourceLabel: 'cao.ie — Change of Mind', sourceUrl: 'https://www.cao.ie/?page=aboutCOM', lastChecked: COMPASS_LAST_VERIFIED },
  },
  {
    id: 'results-offers',
    order: 6,
    title: 'Results & Offers',
    scheme: 'results',
    start: { month: 8, day: 20, label: 'Results ~Aug' },
    end: { month: 10, day: 1, label: 'Rounds ~Oct' },
    tagline: 'Results, points and CAO offers in rounds — what the numbers really mean.',
    whyItMatters:
      '"Points required" isn’t a target set in advance — it’s the score of the last person admitted that year, so it moves with demand. Your points come from your best six subjects in one sitting, plus 25 bonus points for H6 or higher in Higher Maths (only if Maths is in your best six). Ties are split by a random number — and that only matters right at the cut-off.',
    myths: [
      {
        claim: 'The points for a course are fixed and set before results.',
        verdict: 'false',
        explainer:
          'They’re set after results — the points are simply the score of the last person who got a place that year. They rise and fall every year with how many people apply.',
      },
      {
        claim: 'The random number means luck decides whether I get in.',
        verdict: 'false',
        explainer:
          'The random number only breaks ties between people on exactly the same points at the cut-off. Your points get you there; the random number is just the tiebreaker for the very last places.',
      },
      {
        claim: 'Higher Maths bonus points always count.',
        verdict: 'false',
        explainer:
          'The +25 bonus for H6 or higher in Higher Maths only counts if Maths is one of your best six subjects.',
      },
    ],
    checklistItems: [
      { id: 'results-day', label: 'Leaving Cert results day' },
      { id: 'round1', label: 'Round 1 offers — reply by the deadline' },
    ],
    crossLinks: [
      { toolId: 'points-passport', title: 'Track your trajectory', description: 'See your mock trends and grade bargains in Points Passport.' },
      { toolId: 'cao-simulator', title: 'What points do I need?', description: 'Model grade combinations in the CAO Points Simulator.' },
    ],
    verify: { sourceLabel: 'cao.ie — Points & Offers', sourceUrl: 'https://www.cao.ie/index.php?page=points', lastChecked: COMPASS_LAST_VERIFIED },
  },
];

// ─── HEAR eligibility self-check ─────────────────────────────────────────────
//
// Indicator 1 (income) is a MANDATORY gate worth 0 toward the score. The four
// scored indicators sum to a maximum of 7. Eligible at 2.5+, Priority at 5.5+
// — but ONLY if the income gate is met. 2026-cycle weightings; verify yearly.

export interface HearIndicator {
  id: string;
  label: string;
  detail: string;
  points: number;
  isIncomeGate?: boolean;
}

export const HEAR_INDICATORS: HearIndicator[] = [
  { id: 'income', label: 'Household income at or below the HEAR limit', detail: 'The mandatory indicator — the income year is two years before entry. The limit rises with family size. Verify the exact figure on accesscollege.ie.', points: 0, isIncomeGate: true },
  { id: 'area', label: 'Home address in a disadvantaged area', detail: 'Scored against the Pobal deprivation index. "Very/extremely disadvantaged" scores higher than "disadvantaged".', points: 2.5 },
  { id: 'dsp', label: 'Parent/guardian on a means-tested social welfare payment', detail: 'A means-tested DSP payment for 26+ weeks in the reference year.', points: 2 },
  { id: 'deis', label: 'Completed 5 years in a DEIS school', detail: 'Five years of second-level schooling in a DEIS school.', points: 1.5 },
  { id: 'medical-card', label: 'Family holds a Medical Card or GP Visit Card', detail: 'A current HSE Medical Card or GP Visit Card in the applicant’s name.', points: 1 },
];

export const HEAR_THRESHOLDS = { eligible: 2.5, priority: 5.5, max: 7 } as const;

export type HearOutcome = 'not-eligible' | 'eligible' | 'priority';

export function computeHearScore(selectedIds: string[]): { score: number; incomeGateMet: boolean; outcome: HearOutcome } {
  const incomeGateMet = selectedIds.includes('income');
  let score = 0;
  for (const ind of HEAR_INDICATORS) {
    if (ind.isIncomeGate) continue;
    if (selectedIds.includes(ind.id)) score += ind.points;
  }
  let outcome: HearOutcome = 'not-eligible';
  if (incomeGateMet) {
    if (score >= HEAR_THRESHOLDS.priority) outcome = 'priority';
    else if (score >= HEAR_THRESHOLDS.eligible) outcome = 'eligible';
  }
  return { score, incomeGateMet, outcome };
}

/** Automatically-priority groups (not point-scored — they confer priority on
 *  their own). Surfaced as a note in the HEAR clarifier. */
export const HEAR_PRIORITY_GROUPS: string[] = [
  'Care-experienced (in care / aftercare)',
  'Member of the Traveller or Roma community',
  'Young parent on a low income',
  'Eligible for BOTH HEAR and DARE',
];

// ─── DARE two-gate self-check ────────────────────────────────────────────────
//
// Two pillars BOTH required: Evidence of Disability (a clear specialist
// diagnosis in one of the recognised categories) AND Educational Impact
// (evidenced via the school). 2026-cycle list; verify the categories,
// professionals and report-age limits verbatim against the live handbook.

export interface DareCategory {
  id: string;
  name: string;
  appropriateProfessional: string;
  /** Years the report must be within, or null for no age limit. */
  reportAgeLimitYears: number | null;
  note?: string;
}

export const DARE_CATEGORIES: DareCategory[] = [
  { id: 'adhd', name: 'ADD / ADHD', appropriateProfessional: 'Psychiatrist or Psychologist', reportAgeLimitYears: 3 },
  { id: 'autism', name: 'Autism Spectrum Disorder', appropriateProfessional: 'Psychiatrist or Psychologist', reportAgeLimitYears: null },
  { id: 'vision', name: 'Blind / Vision Impaired', appropriateProfessional: 'Ophthalmologist or Optometrist', reportAgeLimitYears: null },
  { id: 'hearing', name: 'Deaf / Hard of Hearing', appropriateProfessional: 'Audiologist or ENT consultant', reportAgeLimitYears: null },
  { id: 'dcd', name: 'Developmental Co-ordination Disorder (Dyspraxia)', appropriateProfessional: 'Psychologist or Occupational Therapist', reportAgeLimitYears: null },
  { id: 'dyslexia', name: 'Dyslexia / Significant Literacy Difficulty', appropriateProfessional: 'Psychologist (or School Statement route)', reportAgeLimitYears: null, note: 'Literacy attainment scores must be recent — verify the cut-off date.' },
  { id: 'dyscalculia', name: 'Dyscalculia / Significant Numeracy Difficulty', appropriateProfessional: 'Psychologist', reportAgeLimitYears: null, note: 'Numeracy attainment scores must be recent — verify the cut-off date.' },
  { id: 'mental-health', name: 'Mental Health Condition', appropriateProfessional: 'Psychiatrist or Clinical Psychologist', reportAgeLimitYears: 3 },
  { id: 'neurological', name: 'Neurological Condition (incl. Brain Injury / Epilepsy)', appropriateProfessional: 'Neurologist or relevant consultant', reportAgeLimitYears: null },
  { id: 'physical', name: 'Physical Disability', appropriateProfessional: 'Relevant medical consultant', reportAgeLimitYears: null },
  { id: 'speech-language', name: 'Speech & Language Communication Disorder', appropriateProfessional: 'Speech & Language Therapist', reportAgeLimitYears: null },
  { id: 'ongoing-illness', name: 'Significant Ongoing Illness', appropriateProfessional: 'Relevant medical consultant', reportAgeLimitYears: 3 },
];

export interface DareImpactIndicator {
  id: string;
  label: string;
  /** Indicator 6 only applies to literacy/numeracy categories. */
  literacyNumeracyOnly?: boolean;
}

export const DARE_IMPACT_INDICATORS: DareImpactIndicator[] = [
  { id: 'supports', label: 'Received interventions or supports at school' },
  { id: 'attendance', label: 'Attendance or school routine was disrupted' },
  { id: 'wellbeing', label: 'School experience / well-being was affected' },
  { id: 'results', label: 'Learning and exam results were affected' },
  { id: 'other', label: 'Other significant educational impact' },
  { id: 'attainment', label: 'Attainment at or below the 10th percentile', literacyNumeracyOnly: true },
];

/** DARE rule: most need ANY 2 of indicators 1-5; literacy/numeracy applicants
 *  need indicator 6 PLUS one other. Estimate only. */
export function meetsDareImpact(selectedIndicatorIds: string[], categoryId: string | null): boolean {
  const isLitNum = categoryId === 'dyslexia' || categoryId === 'dyscalculia';
  const standardCount = selectedIndicatorIds.filter(id => id !== 'attainment').length;
  if (isLitNum) {
    return selectedIndicatorIds.includes('attainment') && standardCount >= 1;
  }
  return standardCount >= 2;
}

/** Who completes each part of the DARE Supplementary Information Form. */
export const DARE_FORM_PARTS: { id: string; part: string; who: string }[] = [
  { id: 'section-a', part: 'Section A — online form', who: 'You (the student) — tick YES to Q1' },
  { id: 'section-b', part: 'Section B — Educational Impact Statement', who: 'Your school (with the Principal’s signature & stamp)' },
  { id: 'section-c', part: 'Section C — Evidence of Disability', who: 'The appropriate specialist professional' },
];

// ─── Document pack generator ─────────────────────────────────────────────────
//
// Turns the HEAR/DARE self-checks into a concrete, personalised list of what to
// gather and post. The single biggest avoidable reason these applications fail
// is incomplete documentation — and the schemes do NOT chase missing items.
// Estimate/guide only; the live handbook is the source of truth.

interface HearDoc { text: string; posted: boolean }

/** Always needed when applying for HEAR (income is the mandatory indicator). */
export const HEAR_BASE_DOCUMENTS: HearDoc[] = [
  { text: 'Proof of your identity and current home address', posted: true },
  { text: 'Full household income evidence for the reference year (e.g. Revenue & DSP statements)', posted: true },
  { text: 'Your completed HEAR form and signed declaration', posted: true },
];

/** Extra evidence tied to specific (optional) HEAR indicators. */
export const HEAR_DOCUMENTS: Record<string, HearDoc> = {
  dsp: { text: 'A DSP statement showing the means-tested payment (26+ weeks)', posted: true },
  'medical-card': { text: 'A copy of your Medical Card or GP Visit Card, in date on the required date', posted: true },
  deis: { text: 'DEIS schooling is usually verified from official lists — check if anything is needed from you', posted: false },
  area: { text: 'Your area is assessed from your home address — no separate document to post', posted: false },
};

export const DARE_ONLINE_STEPS: string[] = [
  'Section A — complete online and tick YES to Q1 (nothing to post)',
];

export const DARE_POST_DOCUMENTS: string[] = [
  'Section B — Educational Impact Statement, completed and stamped by your school',
  'Section C — Evidence of Disability, completed by the appropriate professional',
];

export const DOCUMENT_DEADLINE_NOTE =
  'Post everything to arrive by the documents deadline (around 10 March) — number each page with your CAO number and keep proof of postage. The schemes don’t chase missing documents.';

export interface DocumentPack {
  hear: { applying: boolean; toPost: string[]; autoVerified: string[] };
  dare: { applying: boolean; online: string[]; toPost: string[]; categoryReqs: string[] };
}

/** Build the personalised document list from the self-check selections. Pure. */
export function buildDocumentPack(hearIndicators: string[], dareCategoryId?: string): DocumentPack {
  const hearApplying = hearIndicators.length > 0;
  const toPost: string[] = [];
  const autoVerified: string[] = [];
  if (hearApplying) {
    for (const d of HEAR_BASE_DOCUMENTS) (d.posted ? toPost : autoVerified).push(d.text);
    for (const id of hearIndicators) {
      const doc = HEAR_DOCUMENTS[id];
      if (doc) (doc.posted ? toPost : autoVerified).push(doc.text);
    }
  }

  const dareApplying = !!dareCategoryId;
  const categoryReqs: string[] = [];
  if (dareApplying) {
    const cat = DARE_CATEGORIES.find(c => c.id === dareCategoryId);
    if (cat) {
      categoryReqs.push(`Section C must be completed by: ${cat.appropriateProfessional}`);
      categoryReqs.push(
        cat.reportAgeLimitYears === null
          ? 'Diagnostic report: no age limit'
          : `Diagnostic report: must be less than ${cat.reportAgeLimitYears} years old`,
      );
      if (cat.note) categoryReqs.push(cat.note);
    }
  }

  return {
    hear: { applying: hearApplying, toPost, autoVerified },
    dare: {
      applying: dareApplying,
      online: dareApplying ? [...DARE_ONLINE_STEPS] : [],
      toPost: dareApplying ? [...DARE_POST_DOCUMENTS] : [],
      categoryReqs,
    },
  };
}

// ─── Money sorter ────────────────────────────────────────────────────────────

export type MoneyBucket = 'means' | 'merit' | 'automatic' | 'admission';

export const MONEY_BUCKETS: Record<MoneyBucket, { label: string; blurb: string }> = {
  means: { label: 'Means-based', blurb: 'Decided on household income, not grades. You apply.' },
  merit: { label: 'Merit — apply', blurb: 'Earned on achievement (academic, sport, all-rounder). Separate application + deadline.' },
  automatic: { label: 'Automatic', blurb: 'No application — awarded on your results, or applied to everyone.' },
  admission: { label: 'Admission route', blurb: 'Not cash — a reduced-points route that also unlocks supports.' },
};

export interface MoneyItem {
  id: string;
  name: string;
  bucket: MoneyBucket;
  isAutomatic: boolean;
  deadlineWindow: string;
  note: string;
  sourceUrl: string;
}

export const MONEY_ITEMS: MoneyItem[] = [
  { id: 'susi', name: 'SUSI Student Grant', bucket: 'means', isAutomatic: false, deadlineWindow: 'Opens ~April', note: 'Means-tested grant — household income, not grades. Maintenance + fee parts.', sourceUrl: 'https://www.susi.ie/' },
  { id: 'free-fees', name: 'Free Fees Initiative', bucket: 'automatic', isAutomatic: true, deadlineWindow: 'Automatic at enrolment', note: 'State pays tuition for most EU first-time students. You still owe the Student Contribution.', sourceUrl: 'https://hea.ie/funding-governance-performance/funding/student-finance/course-fees/' },
  { id: 'bursary-1916', name: '1916 Bursary', bucket: 'means', isAutomatic: false, deadlineWindow: 'Opens ~Sept, closes ~Oct', note: 'Means-based access bursary for priority/under-represented groups.', sourceUrl: 'https://1916bursary.ie/' },
  { id: 'saf', name: 'Student Assistance Fund', bucket: 'means', isAutomatic: false, deadlineWindow: 'Apply via college, term-time', note: 'Hardship fund for day-to-day costs — does NOT cover tuition or the contribution.', sourceUrl: 'https://hea.ie/funding-governance-performance/funding/student-finance/student-assistance-fund/' },
  { id: 'entrance-scholarships', name: 'Entrance Scholarships', bucket: 'automatic', isAutomatic: true, deadlineWindow: 'Awarded on LC/CAO results', note: 'Top points scorers (e.g. UCD, Trinity, UCC Quercus) — usually no application.', sourceUrl: 'https://careersportal.ie/scholarships/index.php' },
  { id: 'merit-scholarships', name: 'All-rounder / academic scholarships', bucket: 'merit', isAutomatic: false, deadlineWindow: 'Apply ~Feb–Jul', note: 'High achievers/all-rounders (e.g. UCD Ad Astra) — separate application.', sourceUrl: 'https://careersportal.ie/scholarships/index.php' },
  { id: 'sports-scholarships', name: 'Sports scholarships', bucket: 'merit', isAutomatic: false, deadlineWindow: 'Apply ~Mar–May', note: 'Elite athletes — separate application; may include points concessions (you still meet minimums).', sourceUrl: 'https://careersportal.ie/scholarships/index.php' },
  { id: 'hear-dare', name: 'HEAR / DARE', bucket: 'admission', isAutomatic: false, deadlineWindow: 'Via CAO ~1 Feb / ~1 Mar', note: 'Reduced-points routes — not cash, but unlock places at lower points plus supports.', sourceUrl: 'https://accesscollege.ie' },
];

// ─── The Open Door — affordability reframe (Money Stops) ─────────────────────
//
// Mistake-first: lead with the "closed door" sticker price a student fears, then
// drop the real numbers in — each labelled with what removes it (Free Fees,
// SUSI, HEAR) — to reveal the real, smaller, supported cost. Grounded in Destin
// & Oyserman (an OPEN, affordable-looking path raises low-income students' school
// effort; a closed/expensive one suppresses it) and Snyder's hope theory (show
// multiple workable routes). EVERY euro figure is an ESTIMATE for the 2026 cycle,
// source-stamped below and gated by COMPASS_LAST_VERIFIED — the UI always says so.
// NO student income is ever collected; the bands below are PUBLIC info only.
//
// Figures verified 2026-06 against the live 2026/27 cycle (primary sources):
//  - Free Fees covers tuition, not means-tested (hea.ie).
//  - Student contribution capped at €3,000; the permanent Budget 2026 cut makes the
//    STANDARD charge €2,500; a SUSI contribution grant brings it to ~€2,000 for
//    households under €120k; €0 for maintenance-grant holders (gov.ie Budget 2026; susi.ie).
//  - SUSI maintenance up to ~€7,936/yr (2026/27 Special Rate, non-adjacent; susi.ie).
//  - SUSI income thresholds (2026/27, <4 dependent children): Special Rate ~€28,600,
//    full maintenance (Band 1) ~€47,010, 100% contribution grant ~€64,315, 50% ~€71,300.
//  - Living costs ~€16,400/yr away from home (DCU Cost of Attending University 2025/26).

export interface OpenDoorLine {
  id: string;
  label: string;
  /** What it looks like through the "closed door" (the fear). */
  sticker: string;
  /** What it actually is once the relevant scheme applies. */
  open: string;
  /** The scheme that removes/reduces it. */
  removedBy: string;
  detail: string;
  source: { label: string; url: string };
}

export const OPEN_DOOR_LINES: OpenDoorLine[] = [
  {
    id: 'tuition',
    label: 'Tuition fees',
    sticker: 'thousands a year',
    open: '€0',
    removedBy: 'Free Fees',
    detail: 'The State pays undergraduate tuition for eligible EU first-time students through the Free Fees scheme — and it is NOT means-tested, so your family’s income doesn’t come into it.',
    source: { label: 'hea.ie — Free Fees', url: 'https://hea.ie/funding-governance-performance/funding/student-finance/course-fees/' },
  },
  {
    id: 'contribution',
    label: 'Student contribution',
    sticker: '€3,000 / year',
    open: '€2,500 — or as low as €0 with SUSI',
    removedBy: 'Budget 2026 + SUSI',
    detail: 'The contribution is capped at €3,000; the permanent Budget 2026 cut brings the standard charge to €2,500. A SUSI contribution grant takes it to about €2,000 for households under €120,000, and SUSI pays it in full for maintenance-grant holders.',
    source: { label: 'susi.ie — Budget 2026', url: 'https://www.susi.ie/news/budget-2026/' },
  },
  {
    id: 'living',
    label: 'Living costs',
    sticker: '~€16,400 / year away from home',
    open: 'up to ~€7,900 / year covered',
    removedBy: 'SUSI maintenance grant',
    detail: 'If your family income qualifies, SUSI pays a maintenance grant — up to about €7,936 a year living away from home (2026/27 Special Rate). The Student Assistance Fund and part-time work help with the rest, and living at home costs far less again.',
    source: { label: 'susi.ie — grant rates', url: 'https://www.susi.ie/eligibility-criteria/income/full-time-undergraduate-income-thresholds-and-grant-award-rates/' },
  },
];

/** The "second, lower door" — HEAR (a points route, not cash). */
export const OPEN_DOOR_HEAR = {
  label: 'A second, lower-points door',
  detail: 'HEAR offers reduced-points places into the very same courses for students from under-represented backgrounds — plus extra supports once you’re in. It’s a real second door beside the standard-points one, not a consolation prize.',
  source: { label: 'accesscollege.ie — HEAR', url: 'https://accesscollege.ie/hear/' },
};

/** Illustrative SUSI bands — PUBLIC info, NEVER an income self-estimate. */
export const OPEN_DOOR_SUSI_BANDS: string[] = [
  'Family income under ~€28,600? You’d likely get the higher Special Rate grant.',
  'Under ~€47,000? Likely the full maintenance grant.',
  'Under ~€64,000? SUSI likely pays your student contribution in full.',
  'Under ~€120,000? A SUSI contribution grant brings what you pay down to about €2,000 (2026/27).',
];

export const OPEN_DOOR_COPY = {
  closedHeading: 'The door a lot of people see',
  closedSub: '“College costs a fortune — that’s not for someone like me.” It’s the wall that makes people stop before they even start.',
  revealCta: 'Open the door',
  openHeading: 'The door that’s actually there',
  openSub: 'Once the supports you’re entitled to are in, the real cost is far smaller — and for many students, most of it is covered.',
  bandsHeading: 'Would a grant cover me?',
  bandsNote: 'Rough guide only — SUSI decides on your household’s reckonable income and size, not on these round numbers. Check the real thing; it takes about 10 minutes.',
  step: { label: 'Check your SUSI eligibility', url: 'https://www.susi.ie/eligibility-criteria/' },
  disclaimer: 'Every figure here is an estimate for the 2026 cycle and changes each year — your actual costs depend on your course, college and circumstances. Always confirm on susi.ie and hea.ie.',
};

// ─── Restricted-course quick check ───────────────────────────────────────────

export interface RestrictedCourseType {
  id: string;
  label: string;
  mustLockByFeb1: boolean;
  test: string;
}

export const RESTRICTED_COURSE_TYPES: RestrictedCourseType[] = [
  { id: 'medicine', label: 'Medicine', mustLockByFeb1: true, test: 'HPAT — register ~early Feb, sit ~mid-Feb' },
  { id: 'art-portfolio', label: 'Art & Design', mustLockByFeb1: true, test: 'Portfolio submission' },
  { id: 'music-performance', label: 'Music / Performance', mustLockByFeb1: true, test: 'Audition' },
  { id: 'interview-route', label: 'Some interview / mature routes', mustLockByFeb1: true, test: 'Interview or assessment' },
  { id: 'standard', label: 'Most other courses', mustLockByFeb1: false, test: 'No special test — can be added at Change of Mind' },
];

// ─── Sources (aggregated for the verify modal) ───────────────────────────────

export const COMPASS_SOURCES: { label: string; url: string }[] = [
  { label: 'CAO — applications, dates, points & offers', url: 'https://www.cao.ie' },
  { label: 'HEAR & DARE — Access College', url: 'https://accesscollege.ie' },
  { label: 'SUSI — student grant', url: 'https://www.susi.ie' },
  { label: 'HEA — fees, Student Assistance Fund & 1916 Bursary', url: 'https://hea.ie/funding-governance-performance/funding/student-finance/' },
];

export const CYCLE_NOTE =
  'Every date, threshold and figure here changes each year, and eligibility checks are estimates only — always confirm on the official source before you rely on a result. Because an admissions cycle runs from November to the following autumn, if this year’s deadlines have already passed the trail shows the next cycle’s dates.';

// ─── Cycle-relative date resolution ──────────────────────────────────────────
//
// A CAO cycle spans November (applications open) to the following October
// (final offers). We store anchors as month/day only and resolve them against
// a chosen "entry year" so the same data serves every cycle and never shows a
// passed date as upcoming.

/** Resolve a cycle-relative anchor to a real Date within a given entry year.
 *  Nov/Dec anchors belong to the year BEFORE entry; Jan-Oct to the entry year. */
export function resolveCycleDate(anchor: CycleDate, entryYear: number): Date {
  const calendarYear = anchor.month >= 11 ? entryYear - 1 : entryYear;
  return new Date(calendarYear, anchor.month - 1, anchor.day);
}

/** The entry year the trail should target for a given mode.
 *  - live (6th): the cycle currently in progress.
 *  - orientation (TY/5th): the next cycle that is fully ahead. */
export function cycleEntryYear(today: Date, mode: CompassMode): number {
  const y = today.getFullYear();
  const m = today.getMonth() + 1; // 1-12
  if (mode === 'live') {
    // Nov/Dec → this autumn opened next year's cycle; otherwise this year's.
    return m >= 11 ? y + 1 : y;
  }
  // orientation: the next cycle whose November opening is still in the future.
  return m >= 11 ? y + 2 : y + 1;
}

/** Whole days from today until a date (negative if past). Time-of-day ignored. */
export function daysUntil(date: Date, today: Date): number {
  const a = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime();
  const b = new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime();
  return Math.round((a - b) / 86400000);
}

export type StopStatus = 'past' | 'now' | 'future';

export interface StopState {
  id: string;
  start: Date;
  end: Date | null;
  status: StopStatus;
  daysUntilStart: number;
}

/** Resolve every stop's dates and status for a mode, plus the index of the
 *  "current" stop (the active one, else the next upcoming, else the last). */
export function computeStopStates(
  today: Date,
  mode: CompassMode,
): { entryYear: number; states: StopState[]; currentIndex: number } {
  const entryYear = cycleEntryYear(today, mode);
  const states: StopState[] = JOURNEY_STOPS.map(stop => {
    const start = resolveCycleDate(stop.start, entryYear);
    const end = stop.end ? resolveCycleDate(stop.end, entryYear) : null;
    const startDay = daysUntil(start, today);
    const endDay = end ? daysUntil(end, today) : startDay;
    let status: StopStatus;
    if (endDay < 0) status = 'past';
    else if (startDay <= 0 && endDay >= 0) status = 'now';
    else status = 'future';
    return { id: stop.id, start, end, status, daysUntilStart: startDay };
  });

  let currentIndex = states.findIndex(s => s.status === 'now');
  if (currentIndex === -1) currentIndex = states.findIndex(s => s.status === 'future');
  if (currentIndex === -1) currentIndex = states.length - 1;

  return { entryYear, states, currentIndex };
}

// ─── Completion model — the SINGLE source of derived truth ───────────────────
//
// Both the student-facing College Compass UI and the GC dashboard card compute
// progress through these helpers, so what the student marks and what the GC
// sees can never diverge (same input state -> same output, by construction).

export type CompassItemStatus = 'not-started' | 'in-progress' | 'done';

/** An item's status from a stored checklist map, tolerating legacy boolean `true` (= done). */
export function itemStatus(checklist: Record<string, unknown> | undefined, key: string): CompassItemStatus {
  const v = checklist?.[key];
  if (v === 'done' || v === true) return 'done';
  if (v === 'in-progress') return 'in-progress';
  return 'not-started';
}

export interface StopProgress {
  stopId: string;
  title: string;
  scheme: CompassScheme;
  /** Student hid this stop (e.g. not applying HEAR/DARE) — excluded from totals. */
  dismissed: boolean;
  total: number;
  done: number;
  inProgress: number;
  notStarted: number;
  items: { key: string; label: string; status: CompassItemStatus }[];
}

export interface CompassProgress {
  stops: StopProgress[];
  /** Totals across NON-dismissed stops only (matches what the student is working). */
  totalItems: number;
  doneItems: number;
  inProgressItems: number;
  /** 0-100, of non-dismissed items. */
  percentDone: number;
  updatedAt?: string;
}

/**
 * Derive per-stop + overall progress from a CollegeCompassState-shaped value.
 * Used identically by the student tool and the GC dashboard.
 */
export function computeCompassProgress(
  state: { checklist?: Record<string, unknown>; dismissedStops?: string[]; updatedAt?: string } | null | undefined,
): CompassProgress {
  const checklist = state?.checklist ?? {};
  const dismissed = new Set(state?.dismissedStops ?? []);
  const stops: StopProgress[] = JOURNEY_STOPS.map(stop => {
    const items = stop.checklistItems.map(it => {
      const key = `${stop.id}:${it.id}`;
      return { key, label: it.label, status: itemStatus(checklist, key) };
    });
    const done = items.filter(i => i.status === 'done').length;
    const inProgress = items.filter(i => i.status === 'in-progress').length;
    return {
      stopId: stop.id,
      title: stop.title,
      scheme: stop.scheme,
      dismissed: dismissed.has(stop.id),
      total: items.length,
      done,
      inProgress,
      notStarted: items.length - done - inProgress,
      items,
    };
  });
  const active = stops.filter(s => !s.dismissed);
  const totalItems = active.reduce((n, s) => n + s.total, 0);
  const doneItems = active.reduce((n, s) => n + s.done, 0);
  const inProgressItems = active.reduce((n, s) => n + s.inProgress, 0);
  return {
    stops,
    totalItems,
    doneItems,
    inProgressItems,
    percentDone: totalItems === 0 ? 0 : Math.round((doneItems / totalItems) * 100),
    updatedAt: state?.updatedAt,
  };
}
