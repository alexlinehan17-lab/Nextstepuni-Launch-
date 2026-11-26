/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Rule (c-study, agreed 24 Nov 2026: "Yep - Best one I agree"): one tick
 * per minute (or half-minute), a taller one every five. Inked ticks are your
 * time, hairline ticks the rest, and one orange tick is now. It draws what the
 * session already knows; it measures nothing itself.
 */
import React from 'react';
import './study-marks.css';

export interface StudyRuleMarks {
  /** Number of intervals: the rule draws ticks 0..ticks. */
  ticks: number;
  /** Every `major`-th tick is tall. */
  major: number;
  /** Every tick not divisible by `half` is short (half-minute ticks), or 0. */
  half?: number;
  /** Ticks from `inkFrom` (rounded up) to `inkTo` are inked; none when inkTo < 0. */
  inkFrom: number;
  inkTo: number;
  /** Where the orange tick stands, in ticks. */
  now: number;
}

/** The Your session box: an hour of minutes, the chosen length inked. */
export function cardMarks(minutes: number): StudyRuleMarks {
  return { ticks: 60, major: 5, inkFrom: 0, inkTo: minutes > 0 ? Math.min(60, minutes) : -1, now: 0 };
}

/** The room: the session's length in half-minutes, minutes or five minutes;
 *  the time to come is inked and the orange tick travels with the clock. An
 *  open-ended session is drawn against the hour it is in. */
export function roomMarks(totalSeconds: number, elapsedSeconds: number, openEnded: boolean): StudyRuleMarks {
  const total = openEnded ? Math.max(3600, Math.ceil(Math.max(1, elapsedSeconds) / 3600) * 3600) : Math.max(60, totalSeconds);
  const unit = total / 60 <= 30 ? 30 : total / 60 <= 75 ? 60 : 300;
  const ticks = Math.max(1, Math.round(total / unit));
  const now = Math.min(ticks, Math.max(0, elapsedSeconds) / unit);
  return { ticks, major: unit === 30 ? 10 : unit === 60 ? 5 : 3, half: unit === 30 ? 2 : 0, inkFrom: now, inkTo: ticks, now };
}

export default function StudyRule({ marks, size, className = '' }: { marks: StudyRuleMarks; size: 'card' | 'room'; className?: string }) {
  const { ticks, major, half = 0, inkFrom, inkTo, now } = marks;
  const first = Math.ceil(inkFrom - 1e-6);
  return (
    <span className={`study-rule study-rule--${size} ${className}`.trim()} aria-hidden="true">
      {Array.from({ length: ticks + 1 }, (_, index) => {
        const kind = index % major === 0 ? ' study-rule-major' : half && index % half !== 0 ? ' study-rule-half' : '';
        const ink = inkTo >= 0 && index >= first && index <= inkTo ? ' study-rule-ink' : '';
        return <i key={index} className={`${kind}${ink}`.trim() || undefined} style={{ left: `${(index / ticks) * 100}%` }} />;
      })}
      <b style={{ left: `${(Math.min(now, ticks) / ticks) * 100}%` }} />
    </span>
  );
}
