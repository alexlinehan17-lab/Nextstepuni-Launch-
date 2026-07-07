/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Marker's Licence (Trusted Marker loop) — how much a student's self-marks
 * can be trusted, earned in The Examiner's Chair. Calibration there is measured
 * against real SEC marking keys; here it becomes the credibility badge on every
 * self-marked question. Purely local, read-only over the chair store.
 */

import { calibrationBand, loadChair, overallCalibration } from '../ExaminersChair/store';

export interface MarkerLicence {
  /** Mean agreement with the examiner's key, 0–100. */
  pct: number;
  /** Human band, e.g. "Sharp eye". */
  band: string;
  /** Marking sessions completed in The Examiner's Chair. */
  sessions: number;
}

/** The licence, or null until it's earned (3+ completed marking sessions —
 * fewer is a guess, not a calibration). */
export function markerLicence(uid?: string): MarkerLicence | null {
  const chair = loadChair(uid);
  const sessions = Object.keys(chair.results).length;
  const cal = overallCalibration(chair);
  if (cal === null || sessions < 3) return null;
  return { pct: Math.round(cal * 100), band: calibrationBand(cal), sessions };
}
