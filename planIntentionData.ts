/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * planIntentionData.ts — content for the planner's "Intention Engine".
 *
 * Implementation intentions ("when [situation], then I will [action]") are one
 * of the most reliable findings in behaviour-change research: binding an action
 * to a concrete cue roughly doubles follow-through versus a goal alone
 * (Gollwitzer & Sheeran 2006, d ≈ 0.65 across 94 studies). The triggers below
 * are deliberately built around real after-school anchor moments for the DEIS
 * cohort — not an idealised quiet study at a desk — so the cue is something that
 * actually happens in the student's evening.
 *
 * Lifts the cue primitive out of the comeback-only flow (components/CatchUpLane/
 * Comeback.tsx) into the everyday planner.
 */

/** DEIS-grounded situational triggers — concrete anchor moments of an evening. */
export const PLAN_TRIGGERS: string[] = [
  'When I get home and drop my bag',
  'When I get off the bus',
  'When I’ve changed out of my uniform',
  'When the dinner plates are cleared',
  'When my phone hits 8pm',
  'When my younger siblings are settled',
  'When I sit down at the kitchen table',
  'When I’ve finished my evening snack',
];

/** A short, autonomy-framed "why this works" note (no productivity lecture). */
export const PLAN_WHY = {
  text: 'Tying a block to a specific moment — “when X, then I’ll do this” — makes you far more likely to actually start, because the moment itself reminds you. It’s your plan, in your words.',
  source: 'Gollwitzer & Sheeran 2006 — d ≈ 0.65 across 94 studies',
};

/** Build the default "…then I will…" line for a block, in the student's voice. */
export function defaultThen(subject: string): string {
  return `then I’ll sit down and do my ${subject} block`;
}
