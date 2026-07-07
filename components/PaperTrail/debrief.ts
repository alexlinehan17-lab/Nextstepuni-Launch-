/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Sunday Debrief (F11) — an auto-written weekly recap, composed entirely
 * from the student's own local stores: self-marks this week, focused minutes,
 * calibration state and streaks, plus one concrete focus for next week. Pure
 * template composition — no generation, no network, every number traceable to
 * a store. Shown once per week (dismiss persists per ISO week).
 */

import { allMarks } from './attemptStore';
import { loadGrove } from './focusStore';
import { getStreak } from './streakStore';
import { computeProgress } from './progressStats';
import { topicLabel } from './topics';
import { loadChair, overallCalibration, pct, topMisses } from '../ExaminersChair/store';

const WEEK_MS = 7 * 86_400_000;

export interface Debrief {
  headline: string;
  /** 2–4 plain sentences, each earned by real data. */
  lines: string[];
  /** One concrete focus for next week, or null when there's no signal. */
  focus: string | null;
  /** Self-marks made this week (the card hides itself under 1). */
  weekMarks: number;
}

/** ISO-ish week key (UTC), e.g. "2026-w27" — used for once-per-week dismissal. */
export const weekKey = (now: number) => {
  const d = new Date(now);
  const jan1 = Date.UTC(d.getUTCFullYear(), 0, 1);
  const week = Math.floor((now - jan1) / WEEK_MS);
  return `${d.getUTCFullYear()}-w${week}`;
};

const SEEN_KEY = 'pt:debrief-seen:';

export const debriefSeen = (uid: string | undefined, now: number): boolean => {
  try {
    return localStorage.getItem(SEEN_KEY + (uid || 'anon')) === weekKey(now);
  } catch {
    return true;
  }
};
export const markDebriefSeen = (uid: string | undefined, now: number): void => {
  try {
    localStorage.setItem(SEEN_KEY + (uid || 'anon'), weekKey(now));
  } catch { /* private mode — degrade */ }
};

/** Compose the week's recap, or null when the week has no real signal. */
export function composeDebrief(uid: string | undefined, now: number): Debrief | null {
  const since = now - WEEK_MS;

  const weekMarksList = allMarks(uid).filter(m => m.ts >= since);
  const weekMarks = weekMarksList.length;
  const weekAvg = weekMarks
    ? Math.round(weekMarksList.reduce((a, m) => a + (m.max ? (m.score / m.max) * 100 : m.score), 0) / weekMarks)
    : 0;
  const focusMinutes = loadGrove(uid).filter(r => r.ts >= since).reduce((a, r) => a + r.minutes, 0);
  const streak = getStreak(uid, now);
  const chair = loadChair(uid);
  const chairWeek = Object.values(chair.results).filter(r => r.completedAt >= since).length;
  const cal = overallCalibration(chair);

  if (weekMarks === 0 && focusMinutes === 0 && chairWeek === 0) return null;

  const lines: string[] = [];
  if (weekMarks > 0) {
    lines.push(
      `You self-marked ${weekMarks} question${weekMarks === 1 ? '' : 's'} this week at ${weekAvg}% average accuracy.`,
    );
  }
  if (focusMinutes > 0) {
    lines.push(`${focusMinutes} focused minutes went into the grove.`);
  }
  if (chairWeek > 0 && cal !== null) {
    lines.push(
      `${chairWeek} marking session${chairWeek === 1 ? '' : 's'} in the Examiner's Chair — your eye now agrees with the examiner ${pct(cal)} of the time.`,
    );
  }
  if (streak.current >= 3) {
    lines.push(`Your practice streak stands at ${streak.current} days.`);
  }

  // One concrete focus for next week: the top calibration blind spot when one
  // exists, else the weakest measured topic.
  const miss = topMisses(chair, 1)[0];
  const p = computeProgress(uid, now);
  const weak = p.weakestTopics.find(t => t.count >= 2 && t.avg < 66);
  const focus = miss
    ? `Next week: re-mark your “${miss.label}” blind spot in the Examiner's Chair.`
    : weak
      ? `Next week: drill ${topicLabel(weak.subtopicId)} — your weakest measured topic (${weak.avg}%).`
      : null;

  const headline =
    weekMarks >= 10 ? 'A serious week of work.'
    : weekMarks > 0 ? 'The week, in your own numbers.'
    : 'You kept the desk warm this week.';

  return { headline, lines, focus, weekMarks };
}
