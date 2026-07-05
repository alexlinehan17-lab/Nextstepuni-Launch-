/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * AI mark-scheme feedback (feature E11) — SCAFFOLD ONLY, INERT.
 *
 * The proposed feature: a student types an answer and it is marked against the
 * real SEC marking scheme, mark by mark. This is the one capability where a
 * model is clearly better than self-marking (cf. Save My Exams "Smart Mark").
 *
 * IMPORTANT — compliance posture (see compliance/AI_GOVERNANCE_SCHEDULE.md §6.1):
 *   • This file contains NO LLM SDK, NO model call, NO API key, and sends NO
 *     data off-platform. `requestAnswerMarking` throws unconditionally.
 *   • The real implementation is a governed SERVER endpoint (a Cloud Function,
 *     added at activation) — never a client-side model call — grounded strictly
 *     in the official scheme, with a refusal policy, safety check, logging and
 *     rate limits per §6 of the governance schedule.
 *   • `AI_MARKING_LIVE` is false; the UI stays hidden until governance sign-off.
 *
 * The `tallyMarking` helper below is pure arithmetic (no AI) and unit-tested.
 */

/** Master switch — false until governance sign-off + a governed endpoint exist. */
export const AI_MARKING_LIVE = false;

/** One awardable point from the official marking scheme. */
export interface SchemePoint {
  text: string;
  marks: number;
}

export interface MarkedPoint extends SchemePoint {
  awarded: boolean;
  /** Short, scheme-grounded note on why the mark was/wasn't given. */
  note?: string;
}

export interface MarkingRequest {
  /** Which question (subject/year/level/n) the answer is for. */
  questionRef: string;
  studentAnswer: string;
  /** The official scheme points to mark against (never invented). */
  scheme?: SchemePoint[];
}

export interface MarkingResult {
  points: MarkedPoint[];
  awarded: number;
  max: number;
  /** Plain-language, scheme-grounded summary of where marks were gained/lost. */
  summary: string;
}

/** Pure: total the awarded vs available marks across the marked points. */
export function tallyMarking(points: MarkedPoint[]): { awarded: number; max: number } {
  return points.reduce(
    (a, p) => ({ awarded: a.awarded + (p.awarded ? p.marks : 0), max: a.max + p.marks }),
    { awarded: 0, max: 0 },
  );
}

/**
 * INERT. Always throws — there is no client-side model call, by design. When the
 * feature is activated this is replaced by a call to a governed server endpoint
 * (see the governance schedule). Kept as a typed seam so the UI can be built and
 * reviewed without any AI ever executing.
 */
export async function requestAnswerMarking(_req: MarkingRequest): Promise<MarkingResult> {
  throw new Error('AI marking is not enabled — see compliance/AI_GOVERNANCE_SCHEDULE.md §6.1.');
}
