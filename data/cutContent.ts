/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Cut Content Log ────────────────────────────────────────────────────────
//
// Tracked record of module content that was REMOVED or REFRAMED during the
// pre-accreditation review (ahead of the meeting with Brian MacCraith / DCU).
//
// Governing rule (agreed 2026-06): we only state or advise something the
// peer-reviewed literature actually supports. Any claim that could not be
// verified against a real, locatable source is reframed to non-prescriptive
// language or cut outright — a citation is NEVER invented to keep it.
//
// Every cut or reframe is logged here so there is a transparent audit trail of
// exactly what changed and why. This list is surfaced in-app via the
// "Cut Content" page (home sidebar, admin/owner reference — not student-facing
// guidance).
//
// When cutting or reframing content, append an entry below. Keep `original`
// as the verbatim text that was removed so it can be reviewed in context.

export type CutAction = 'removed' | 'reframed';

export interface CutContentEntry {
  /** Stable unique id (e.g. `${moduleId}-001`). */
  id: string;
  /** Human-readable module/course this came from (title preferred). */
  module: string;
  /** The lesson / section / sub-module the content was cut from. */
  section: string;
  /** Whether the content was removed entirely or reframed to non-prescriptive. */
  action: CutAction;
  /** Verbatim original text that was removed. */
  original: string;
  /** If reframed, the replacement text now shown to students. */
  reframedTo?: string;
  /** Why it was cut — e.g. "No peer-reviewed source supports this advice." */
  reason: string;
  /** ISO date the cut was made. */
  date: string;
  /**
   * True when this was only reframed because a primary source is paywalled /
   * unconfirmable — the original wording can be RESTORED verbatim once the PDF
   * is supplied. These surface in their own "Awaiting references" section.
   */
  awaitingSource?: boolean;
  /** The specific paper to dig out to restore the original (shown in the awaiting section). */
  neededSource?: string;
}

export const CUT_CONTENT: CutContentEntry[] = [
  {
    id: 'mastering-active-recall-001',
    module: 'Mastering Active Recall',
    section: "Step 3 — The 'I Know This' Trap",
    action: 'reframed',
    original:
      'Students who stopped testing themselves after one correct answer could only remember about 35% of the material a week later. Students who kept testing themselves on everything remembered about 80% — more than double.',
    reframedTo:
      'In a well-known study, students who kept testing themselves on material remembered far more a week later than students who stopped as soon as they got it right once — even though both groups felt just as sure they knew it.',
    reason:
      'The specific figures (35% / 80%) come from Karpicke & Roediger (2008, Science), which is paywalled with no open-access copy, so the exact numbers could not be verified against the primary source. Reframed to the qualitative finding, which the abstract fully supports. Citation retained (doi:10.1126/science.1152408). Exact figures can be restored if the PDF is supplied.',
    date: '2026-06-23',
    awaitingSource: true,
    neededSource: 'Karpicke, J. D., & Roediger, H. L. (2008). The critical importance of retrieval for learning. Science. doi:10.1126/science.1152408',
  },
  {
    id: 'mastering-active-recall-002',
    module: 'Mastering Active Recall',
    section: 'Step 5 — The Anxiety Myth',
    action: 'reframed',
    original:
      'An incredible 92% of students said it helped them learn, and 72% said it made them less nervous for big exams.',
    reframedTo:
      'The large majority said it helped them learn, and most said it actually made them less nervous for big exams.',
    reason:
      'The 92%/72% figures trace to Agarwal et al. (2014, JARMAC), which is paywalled and not indexed in open databases. The percentages are corroborated by multiple secondary sources but could not be confirmed against the primary full text, so they were reframed to a qualitative claim the paper supports. Citation retained (doi:10.1016/j.jarmac.2014.07.002).',
    date: '2026-06-23',
    awaitingSource: true,
    neededSource: "Agarwal, P. K., D'Antonio, L., Roediger, H. L., McDermott, K. B., & McDaniel, M. A. (2014). Classroom-based programs of retrieval practice reduce middle school and high school students' test anxiety. Journal of Applied Research in Memory and Cognition. doi:10.1016/j.jarmac.2014.07.002",
  },
  {
    id: 'mastering-active-recall-003',
    module: 'Mastering Active Recall',
    section: 'Step 6 — Your Recall Toolkit (micro-commitment)',
    action: 'reframed',
    original:
      'For your next study session, try the 20/80 rule. Spend 20% of your time consuming information (reading, watching) and 80% of your time actively recalling it (self-quizzing, explaining it out loud).',
    reframedTo:
      'For your next study session, flip the balance: spend most of your time actively recalling (self-quizzing, explaining out loud) rather than re-reading or watching.',
    reason:
      'The specific 20/80 ratio is a popularisation with no peer-reviewed empirical basis. The underlying principle (weight study time toward retrieval over restudy) is well supported (Roediger & Karpicke 2006; Karpicke & Roediger 2008), so the advice was reframed to drop the false-precision ratio.',
    date: '2026-06-23',
  },
  {
    id: 'mastering-active-recall-004',
    module: 'Mastering Active Recall',
    section: 'Step 6 — Your Recall Toolkit (Rule 1 card)',
    action: 'reframed',
    original:
      "If It Feels Hard, It's Working — That feeling of struggle when you're trying to remember something? That IS learning happening. If it feels easy, it's probably not doing much.",
    reframedTo:
      "A Bit of Struggle Is the Point — When recalling something takes real effort, but you can still manage it, that effort is what builds lasting memory ('desirable difficulties'). If it feels completely effortless, it's probably not doing much.",
    reason:
      "The original overstated the science — not all difficulty aids learning, only 'desirable difficulties' (effortful but ultimately successful retrieval). Reframed to the precise concept, supported by Soderstrom & Bjork (2015, doi:10.1177/1745691615569000).",
    date: '2026-06-23',
  },
  {
    id: 'spaced-repetition-001',
    module: 'Spaced Repetition',
    section: 'Step 1 — The Forgetting Curve',
    action: 'reframed',
    original:
      'Without reviewing, you can lose over 50% of new information within an hour, and up to 80% within a day.',
    reframedTo:
      'Without reviewing, a large share of new information slips away within the first day or two — classic studies of the forgetting curve, since replicated, show memory dropping sharply soon after learning.',
    reason:
      "The specific figures overstate the evidence — the replicated Ebbinghaus forgetting curve (Murre & Dros 2015, doi:10.1371/journal.pone.0120644) shows a sharp early drop but not ~80% loss within 24 hours. Reframed to a defensible qualitative claim citing the replication.",
    date: '2026-06-23',
  },
  {
    id: 'spaced-repetition-002',
    module: 'Spaced Repetition',
    section: 'Step 2 — The Cramming Paradox',
    action: 'reframed',
    original: 'Spaced Practice can triple how long you remember something.',
    reframedTo: 'Spaced Practice can dramatically increase how long you remember something.',
    reason:
      'The "triple" multiplier is not supported as a general figure. The spacing effect itself is robustly evidenced (Cepeda et al. 2006, doi:10.1037/0033-2909.132.3.354), but effect sizes vary widely by interval, so the specific number was reframed to a qualitative claim.',
    date: '2026-06-23',
  },
  {
    id: 'how-memory-works-001',
    module: 'How Your Memory Works',
    section: 'Step 6 — Your Action Plan (micro-commitment)',
    action: 'reframed',
    original:
      "This single act of 'sleep hygiene' has a bigger impact on your memory than an extra hour of cramming.",
    reframedTo:
      "This single act of 'sleep hygiene' protects the deep sleep your memory relies on to lock in what you studied.",
    reason:
      'The original made a direct quantitative comparison ("bigger impact than an extra hour of cramming") that is not established by any specific study. The underlying point — sleep is essential for memory consolidation — is well supported (Diekelmann & Born 2010, doi:10.1038/nrn2762), so the claim was reframed to drop the unsupported comparison.',
    date: '2026-06-23',
  },
  {
    id: 'elaborative-interrogation-001',
    module: 'Elaborative Interrogation',
    section: 'Step 1 — The "Why" Engine',
    action: 'reframed',
    original:
      'Students who asked "Why?" remembered 72% of material. Passive readers remembered only 37%. … the "Why?" group remembered almost double what the passive readers did (72% vs 37%).',
    reframedTo:
      'In classic experiments, students who asked "Why?" remembered far more than passive readers — one simple question can come close to doubling how much sticks.',
    reason:
      'The specific 72%/37% figures could not be tied to a verifiable primary source. The elaborative-interrogation effect (the "why" question roughly doubling retention vs passive reading) is well evidenced (Stein & Bransford 1979, doi:10.1016/s0022-5371(79)90481-x; Pressley et al. 1987, doi:10.1037/0278-7393.13.2.291; reviewed in Dunlosky et al. 2013), so the claim was reframed to the supported qualitative version. The on-screen demo bars are illustrative only (no numbers shown).',
    date: '2026-06-23',
  },
  {
    id: 'cognitive-endurance-001',
    module: 'Cognitive Endurance',
    section: 'Step 3 — Fueling the Engine',
    action: 'reframed',
    original:
      'Swishing a sports drink around your mouth for 10 seconds tricks your brain into thinking fuel is on the way. This can give you a real mental boost in the final, gruelling hour of a long exam.',
    reframedTo:
      'Swishing a sports drink around your mouth for about 10 seconds activates reward areas in your brain. In endurance exercise this reliably lowers how hard the effort feels; it may give a similar lift in the final, gruelling hour of a long exam, though the evidence for mental tasks is less settled.',
    reason:
      'The carbohydrate mouth-rinse effect is established for endurance/physical performance and perceived effort (Chambers, Bridge & Jones 2009, doi:10.1113/jphysiol.2008.164285), but its benefit for sustained cognitive/exam performance is not well established. Reframed to state the evidenced mechanism and flag the uncertainty for mental tasks rather than promising "a real mental boost".',
    date: '2026-06-23',
  },
  {
    id: 'cognitive-endurance-002',
    module: 'Cognitive Endurance',
    section: 'Step 6 — The Recovery Protocol',
    action: 'reframed',
    original:
      'In the crucial break between two exams on the same day, a 20-minute NSDR session is the single most effective way to recharge for the afternoon paper.',
    reframedTo:
      'In the crucial break between two exams on the same day, a 20-minute NSDR session is one of the best ways to recharge for the afternoon paper.',
    reason:
      'The "single most effective" superlative is not supported — the peer-reviewed evidence base for NSDR / yoga nidra as a recovery tool is still limited. Reframed to a non-superlative recommendation. (Brief structured breathing has stronger support: Balban et al. 2023, doi:10.1016/j.xcrm.2022.100895.)',
    date: '2026-06-23',
  },
];
