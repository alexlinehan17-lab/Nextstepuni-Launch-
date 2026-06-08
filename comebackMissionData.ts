/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * comebackMissionData.ts — typed, evidence-graded study techniques for the
 * Comeback Engine's weekly missions ("Schedule the Evidence").
 *
 * The old missions were all one shape ("Do one HL/OL {subject} past paper
 * question") with no guidance on WHAT to practise or WHY it works. This library
 * types each mission by technique and carries a one-line, sourced "why this beats
 * rereading" rationale, so students learn the hierarchy of study moves — not just
 * a task list.
 *
 * Grounded in:
 *  - Dunlosky, J. et al. (2013), "Improving Students' Learning With Effective
 *    Learning Techniques", Psychological Science in the Public Interest 14(1):
 *    of ten common techniques, only practice testing (retrieval) and distributed
 *    (spaced) practice earned a HIGH-utility rating; rereading, highlighting and
 *    summarising — the strategies students default to — rated LOW.
 *  - Roediger & Karpicke (2006) / Karpicke & Roediger (2008): retrieval beats
 *    restudy for long-term retention, and the advantage GROWS with delay.
 *  - Cepeda, N. J. et al. (2006), Psychological Bulletin 132(3): the best spacing
 *    gap widens with time-to-test (direction is firm; the "~10–20%" ratio is the
 *    common practitioner interpretation, used here only to scale the gap).
 *  - Rohrer, Dedrick & Stershic (2015), J. Educational Psychology 107(3):
 *    interleaving (mixing problem types) beats blocking on delayed tests — and it
 *    feels harder, which is exactly why students avoid it.
 */

export type TechniqueType = 'retrieval' | 'spaced-review' | 'interleaved';

export interface MissionTechnique {
  /** Short chip label shown on the mission card. */
  label: string;
  /** Dunlosky utility tier — every technique here is HIGH-utility by design. */
  utility: 'high';
  /** One-line "why this beats rereading", in a student's voice. */
  why: string;
  /** Inline citation for the rationale. */
  source: string;
}

export const MISSION_TECHNIQUES: Record<TechniqueType, MissionTechnique> = {
  retrieval: {
    label: 'Active recall',
    utility: 'high',
    why: 'Close the book and pull it from memory before you check. Testing yourself beats re-reading — and the gap only grows the longer it is until the exam.',
    source: 'Dunlosky 2013; Roediger & Karpicke 2006',
  },
  'spaced-review': {
    label: 'Spaced review',
    utility: 'high',
    why: 'Come back to this after a gap instead of cramming it now. The same effort, spread out, sticks far longer.',
    source: 'Dunlosky 2013; Cepeda 2006',
  },
  interleaved: {
    label: 'Mixed practice',
    utility: 'high',
    why: 'Mix two topics in one sitting instead of doing all of one. It feels harder and slower — that harder feeling is the point; it’s what makes it stick.',
    source: 'Rohrer, Dedrick & Stershic 2015',
  },
};

/**
 * The passive strategies students default to — named explicitly so they learn
 * the hierarchy, not just the task. Surfaced in the fluency-trap reveal.
 */
export const LOW_UTILITY_STRATEGIES = {
  names: ['re-reading notes', 'highlighting', 'copying out summaries'],
  note: 'Re-reading and highlighting feel productive, but they’re the lowest-utility moves in the research — they build the feeling of knowing without the recall to back it up.',
  source: 'Dunlosky et al. 2013',
};

/**
 * Spacing gap (in days) for a spaced-review mission, scaled to time-to-exam.
 * Cepeda et al.: the best gap widens with the retention interval, so the review
 * gap should open up when the exam is far and tighten as it nears. We use ~15%
 * of time-to-test, clamped to a sensible 2–21 day band for a weekly planner.
 * `daysUntilExam` of 999 means "no exam date set" → a neutral fortnightly gap.
 */
export function spacingGapDays(daysUntilExam: number): number {
  if (daysUntilExam >= 900) return 14;
  const gap = Math.round(daysUntilExam * 0.15);
  return Math.max(2, Math.min(21, gap));
}
