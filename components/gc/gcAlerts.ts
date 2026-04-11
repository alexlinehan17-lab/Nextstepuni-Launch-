/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { GCStudentFullData } from './gcTypes';

// ── Types ──────────────────────────────────────────────────

export type AlertSeverity = 'urgent' | 'watch' | 'nudge';

export interface EarlyWarningAlert {
  id: string;            // unique key: `${type}-${studentUid}`
  type: string;          // signal type for dismiss tracking
  severity: AlertSeverity;
  studentUid: string;
  studentName: string;
  studentAvatar: string;
  title: string;
  description: string;
  metric: number;        // numeric value for "resurface if worse" logic
}

export interface DismissedAlert {
  dismissedAt: number;
  metricAtDismissal: number;
}

// ── Helpers ────────────────────────────────────────────────

const DAY_MS = 24 * 60 * 60 * 1000;

function getLastActiveDate(student: GCStudentFullData): string | null {
  if (!student.timetableCompletions) return null;
  const keys = Object.keys(student.timetableCompletions);
  if (keys.length === 0) return null;
  keys.sort((a, b) => b.localeCompare(a));
  return keys[0];
}

function daysSinceDate(dateStr: string): number {
  return Math.floor((Date.now() - new Date(dateStr).getTime()) / DAY_MS);
}

// ── Signal Generators ──────────────────────────────────────

function engagementDropoff(s: GCStudentFullData): EarlyWarningAlert | null {
  const lastDate = getLastActiveDate(s);
  if (!lastDate) return null;

  const daysSince = daysSinceDate(lastDate);
  if (daysSince < 5) return null;

  // Only flag students who were previously active (had activity at some point)
  const totalDays = Object.keys(s.timetableCompletions || {}).length;
  if (totalDays < 3) return null;

  return {
    id: `engagement-dropoff-${s.user.uid}`,
    type: 'engagement-dropoff',
    severity: daysSince >= 7 ? 'urgent' : 'watch',
    studentUid: s.user.uid,
    studentName: s.user.name,
    studentAvatar: s.user.avatar,
    title: daysSince >= 7 ? 'Inactive for over a week' : `Inactive ${daysSince} days`,
    description: `Was previously active (${totalDays} active days), last seen ${lastDate}.`,
    metric: daysSince,
  };
}

function streakBroken(s: GCStudentFullData): EarlyWarningAlert | null {
  const streak = s.streak;
  if (!streak) return null;

  // Only flag if they had a meaningful streak (7+) and now lost it
  if (streak.longestStreak < 7 || streak.currentStreak > 0) return null;

  // Check last active date to see if it was recent enough to matter
  const lastDate = getLastActiveDate(s);
  if (!lastDate) return null;
  const daysSince = daysSinceDate(lastDate);
  if (daysSince > 14) return null; // too old to flag

  return {
    id: `streak-broken-${s.user.uid}`,
    type: 'streak-broken',
    severity: 'watch',
    studentUid: s.user.uid,
    studentName: s.user.name,
    studentAvatar: s.user.avatar,
    title: `Lost ${streak.longestStreak}-day streak`,
    description: `Had built a strong habit, now inactive for ${daysSince} days.`,
    metric: streak.longestStreak,
  };
}

function studyTimeDropping(s: GCStudentFullData): EarlyWarningAlert | null {
  // Need study sessions from progress doc — check timetableCompletions as proxy
  const completions = s.timetableCompletions;
  if (!completions) return null;

  const now = new Date();
  const _todayKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;

  let thisWeekBlocks = 0;
  let lastWeekBlocks = 0;

  for (const [dateKey, blocks] of Object.entries(completions)) {
    const days = daysSinceDate(dateKey);
    const count = Array.isArray(blocks) ? blocks.length : 0;
    if (days <= 7) thisWeekBlocks += count;
    else if (days <= 14) lastWeekBlocks += count;
  }

  if (lastWeekBlocks < 5) return null; // need enough baseline
  const dropPct = Math.round(((lastWeekBlocks - thisWeekBlocks) / lastWeekBlocks) * 100);
  if (dropPct < 50) return null;

  return {
    id: `study-dropping-${s.user.uid}`,
    type: 'study-dropping',
    severity: 'watch',
    studentUid: s.user.uid,
    studentName: s.user.name,
    studentAvatar: s.user.avatar,
    title: `Activity down ${dropPct}%`,
    description: `${thisWeekBlocks} blocks this week vs ${lastWeekBlocks} last week.`,
    metric: dropPct,
  };
}

function stalledProgress(s: GCStudentFullData): EarlyWarningAlert | null {
  // Check if student was making progress but has stopped
  const completions = s.timetableCompletions;
  if (!completions) return null;

  const dateKeys = Object.keys(completions).sort((a, b) => b.localeCompare(a));
  if (dateKeys.length < 5) return null;

  const lastDate = dateKeys[0];
  const daysSince = daysSinceDate(lastDate);

  // Not stalled if active within 14 days
  if (daysSince < 14) return null;

  // Only flag if they had meaningful engagement before
  if (dateKeys.length < 10) return null;

  return {
    id: `stalled-${s.user.uid}`,
    type: 'stalled',
    severity: 'watch',
    studentUid: s.user.uid,
    studentName: s.user.name,
    studentAvatar: s.user.avatar,
    title: 'Progress stalled',
    description: `No new activity in ${daysSince} days despite ${dateKeys.length} previous active days.`,
    metric: daysSince,
  };
}

function _noReflections(s: GCStudentFullData): EarlyWarningAlert | null {
  // Check study sessions from the progress data
  // We access studySessions via the raw progress doc - but GCStudentFullData
  // doesn't have studySessions directly. We can infer from points data.
  // For now, check if the student has enough engagement but no reflection-based points
  const points = s.points;
  if (!points) return null;

  // We can't directly access studySessions from GCStudentFullData,
  // so this signal focuses on students who are active but might benefit from reflection
  // Skip for now - we'll address this in a future iteration
  return null;
}

// ── Main Alert Generator ──────────────────────────────────

export function generateAlerts(
  students: GCStudentFullData[],
  dismissedAlerts: Record<string, DismissedAlert>,
): EarlyWarningAlert[] {
  const allAlerts: EarlyWarningAlert[] = [];

  for (const student of students) {
    const signals = [
      engagementDropoff(student),
      streakBroken(student),
      studyTimeDropping(student),
      stalledProgress(student),
    ];

    for (const alert of signals) {
      if (!alert) continue;

      // Check if dismissed — resurface if situation has worsened
      const dismissed = dismissedAlerts[alert.id];
      if (dismissed) {
        // For metrics where higher = worse (daysSince, stressedCount, dropPct)
        if (alert.metric <= dismissed.metricAtDismissal) continue;
        // Situation worsened — resurface
      }

      allAlerts.push(alert);
    }
  }

  // Sort: urgent first, then watch, then nudge
  const severityOrder: Record<AlertSeverity, number> = { urgent: 0, watch: 1, nudge: 2 };
  allAlerts.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);

  return allAlerts;
}
