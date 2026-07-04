/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — practice streak + daily goal (feature B3). Records the days a
 * student actually practised (graded a review card, or self-marked a question)
 * and how many cards they did each day, so home can show a streak and a
 * "N of your daily goal" ring. Pure day-run maths (`computeStreak`) is unit-
 * tested; the clock is always injected so the store stays deterministic.
 */

const PREFIX = 'pt:streak:';
const DAY = 86_400_000;
const DEFAULT_GOAL = 10;

interface StreakData {
  /** local YYYY-MM-DD → count of practice actions that day. */
  days: Record<string, number>;
  /** cards-per-day target. */
  goal: number;
}

const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

const read = (uid?: string): StreakData => {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    const v = raw ? (JSON.parse(raw) as Partial<StreakData>) : {};
    return { days: v.days ?? {}, goal: v.goal ?? DEFAULT_GOAL };
  } catch {
    return { days: {}, goal: DEFAULT_GOAL };
  }
};
const write = (uid: string | undefined, v: StreakData) => {
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(v));
  } catch {
    /* quota / private mode — degrade silently */
  }
};

/** Local calendar day for an epoch, as YYYY-MM-DD. */
export function dayKey(now: number): string {
  const d = new Date(now);
  const p = (x: number) => String(x).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

/** A dayKey → an integer day index (UTC-anchored so day differences are exact
 *  regardless of DST — we only ever compare gaps of whole days). */
export function dayIndex(key: string): number {
  const [y, m, d] = key.split('-').map(Number);
  return Math.floor(Date.UTC(y, m - 1, d) / DAY);
}

// ─── pure streak maths ──────────────────────────────────────

export interface StreakCounts {
  /** Consecutive practised days ending today (or yesterday, if today is not yet
   *  practised — so the streak is not shown as broken mid-morning). */
  current: number;
  /** Longest consecutive run ever. */
  longest: number;
}

/** Given the set of practised day-indices and today's index, the current and
 *  longest streaks. Robust to unsorted / duplicate input. */
export function computeStreak(activeIndices: number[], todayIndex: number): StreakCounts {
  const set = new Set(activeIndices);
  if (set.size === 0) return { current: 0, longest: 0 };

  // Longest run anywhere.
  let longest = 0;
  for (const i of set) {
    if (set.has(i - 1)) continue; // only start counting at a run's beginning
    let len = 1;
    while (set.has(i + len)) len++;
    longest = Math.max(longest, len);
  }

  // Current run: anchor at today if practised, else yesterday, else 0.
  let anchor = set.has(todayIndex) ? todayIndex : set.has(todayIndex - 1) ? todayIndex - 1 : null;
  let current = 0;
  if (anchor !== null) {
    while (set.has(anchor)) {
      current++;
      anchor--;
    }
  }
  return { current, longest };
}

// ─── public summary ─────────────────────────────────────────

export interface StreakSummary {
  current: number;
  longest: number;
  /** Practice actions logged today. */
  todayCount: number;
  goal: number;
  goalMet: boolean;
  activeToday: boolean;
}

const summarise = (v: StreakData, now: number): StreakSummary => {
  const today = dayKey(now);
  const indices = Object.keys(v.days).map(dayIndex);
  const { current, longest } = computeStreak(indices, dayIndex(today));
  const todayCount = v.days[today] ?? 0;
  return { current, longest, todayCount, goal: v.goal, goalMet: todayCount >= v.goal, activeToday: todayCount > 0 };
};

export function getStreak(uid: string | undefined, now: number): StreakSummary {
  return summarise(read(uid), now);
}

/** Log one (or more) practice actions for today; returns the fresh summary. */
export function recordActivity(uid: string | undefined, now: number, inc = 1): StreakSummary {
  const v = read(uid);
  const today = dayKey(now);
  v.days[today] = (v.days[today] ?? 0) + inc;
  write(uid, v);
  return summarise(v, now);
}

export function setGoal(uid: string | undefined, goal: number, now: number): StreakSummary {
  const v = read(uid);
  v.goal = Math.max(1, Math.round(goal));
  write(uid, v);
  return summarise(v, now);
}
