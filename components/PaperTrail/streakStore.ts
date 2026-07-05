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
/** Earn one streak freeze for every N practised days, capped so a stockpile
 *  can't paper over long absences. Freezes auto-protect a missed day — no guilt,
 *  no manual juggling. */
const FREEZE_EARN_EVERY = 5;
const FREEZE_MAX = 2;

interface StreakData {
  /** local YYYY-MM-DD → count of practice actions that day. */
  days: Record<string, number>;
  /** cards-per-day target. */
  goal: number;
  /** Days auto-covered by a freeze (count as active for the streak). */
  frozen?: string[];
}

const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

const read = (uid?: string): StreakData => {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    const v = raw ? (JSON.parse(raw) as Partial<StreakData>) : {};
    return { days: v.days ?? {}, goal: v.goal ?? DEFAULT_GOAL, frozen: v.frozen ?? [] };
  } catch {
    return { days: {}, goal: DEFAULT_GOAL, frozen: [] };
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

/** Inverse of dayIndex: a day index back to its YYYY-MM-DD key. */
export function indexToKey(index: number): string {
  const d = new Date(index * DAY);
  const p = (x: number) => String(x).padStart(2, '0');
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())}`;
}

/** Which missed days to auto-freeze to keep the current run alive to today —
 *  only when the available freezes fully cover the gap (otherwise the streak
 *  breaks and the freezes are preserved). Pure. */
export function frozenBridge(active: number[], frozen: number[], available: number, today: number): number[] {
  const set = new Set([...active, ...frozen]);
  let lastActive = -Infinity;
  for (const i of set) if (i <= today && i > lastActive) lastActive = i;
  if (!Number.isFinite(lastActive)) return [];
  const gapStart = lastActive + 1;
  const gapEnd = today - 1; // cover up to yesterday; today can still be practised
  const gap = gapEnd - gapStart + 1;
  if (gap <= 0 || gap > available) return [];
  const out: number[] = [];
  for (let d = gapStart; d <= gapEnd; d++) out.push(d);
  return out;
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
  /** Freezes ready to protect a future missed day. */
  freezes: number;
  /** True when a freeze is currently holding the streak (missed but protected). */
  protectedNow: boolean;
}

const freezesAvailable = (v: StreakData): number => {
  const earned = Math.floor(Object.keys(v.days).length / FREEZE_EARN_EVERY);
  return Math.max(0, Math.min(FREEZE_MAX, earned - (v.frozen?.length ?? 0)));
};

/** Auto-apply freezes to bridge missed days up to today. Mutates `v`; returns
 *  true if anything changed (so the caller can persist). */
const reconcile = (v: StreakData, now: number): boolean => {
  const today = dayIndex(dayKey(now));
  const active = Object.keys(v.days).map(dayIndex);
  const frozen = (v.frozen ?? []).map(dayIndex);
  const add = frozenBridge(active, frozen, freezesAvailable(v), today);
  if (!add.length) return false;
  v.frozen = [...(v.frozen ?? []), ...add.map(indexToKey)];
  return true;
};

const summarise = (v: StreakData, now: number): StreakSummary => {
  const today = dayKey(now);
  const active = Object.keys(v.days).map(dayIndex);
  const frozen = (v.frozen ?? []).map(dayIndex);
  const { current, longest } = computeStreak([...active, ...frozen], dayIndex(today));
  const todayCount = v.days[today] ?? 0;
  const yesterdayFrozen = frozen.includes(dayIndex(today) - 1);
  return {
    current,
    longest,
    todayCount,
    goal: v.goal,
    goalMet: todayCount >= v.goal,
    activeToday: todayCount > 0,
    freezes: freezesAvailable(v),
    protectedNow: current > 0 && todayCount === 0 && yesterdayFrozen,
  };
};

export function getStreak(uid: string | undefined, now: number): StreakSummary {
  const v = read(uid);
  if (reconcile(v, now)) write(uid, v);
  return summarise(v, now);
}

/** Log one (or more) practice actions for today; returns the fresh summary. */
export function recordActivity(uid: string | undefined, now: number, inc = 1): StreakSummary {
  const v = read(uid);
  const today = dayKey(now);
  v.days[today] = (v.days[today] ?? 0) + inc;
  reconcile(v, now);
  write(uid, v);
  return summarise(v, now);
}

export function setGoal(uid: string | undefined, goal: number, now: number): StreakSummary {
  const v = read(uid);
  v.goal = Math.max(1, Math.round(goal));
  write(uid, v);
  return summarise(v, now);
}
