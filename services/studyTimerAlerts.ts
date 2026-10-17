/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * What the study timer should be telling the device, worked out from the
 * running session alone. Pure, so the lifecycle is tested without a device:
 *
 *   start, resume, keep going  schedule (or reschedule) "time's up"
 *   pause, end early, discard  cancel it
 *   the countdown runs out     leave it alone: it is firing, or has fired
 *   save, sign-out             cancel it and clear it from the screen
 *
 * hooks/useStudyTimerAlerts carries these out through services/notifications
 * and the iOS Live Activity.
 */

import { NOTICE_IDS, type LocalNotice } from './notifications';

export interface StudyTimerSnapshot {
  phase: 'idle' | 'active' | 'paused' | 'complete';
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  openEnded: boolean;
  /** Wall-clock end of a running countdown; null otherwise. */
  endsAt: number | null;
  /** Wall-clock start, shifted forward by paused time (count-up anchor). */
  startedAt: number;
  plannedMinutes: number;
  extendedMinutes: number;
  elapsedSeconds: number;
  totalDuration: number;
}

export const SESSION_TYPE_LABEL: Record<StudyTimerSnapshot['sessionType'], string> = {
  'new-learning': 'New Learning',
  practice: 'Practice',
  revision: 'Revision',
};

/** The countdown reached zero (not an early finish, not open-ended). */
export const ranOut = (s: StudyTimerSnapshot): boolean =>
  s.phase === 'complete' && !s.openEnded && s.totalDuration > 0 && s.elapsedSeconds >= s.totalDuration;

const minutesLabel = (minutes: number) => `${minutes} minute${minutes === 1 ? '' : 's'}`;

/** Short, warm and specific. No emojis. */
export function studyTimerCopy(s: Pick<StudyTimerSnapshot, 'subject' | 'plannedMinutes' | 'extendedMinutes'>): { title: string; body: string } {
  if (s.extendedMinutes > 0) {
    return {
      title: `Extra time done: ${s.subject}`,
      body: `That’s ${minutesLabel(s.plannedMinutes + s.extendedMinutes)} of ${s.subject} in total. Tap to log it and collect your bonus.`,
    };
  }
  return {
    title: `Time’s up: ${s.subject}`,
    body: `That’s ${minutesLabel(s.plannedMinutes)} of ${s.subject} done. Tap to log it, or keep going.`,
  };
}

/** The "time's up" notification this session wants, if any. */
export function studyTimerNotice(
  s: StudyTimerSnapshot,
  options: { enabled: boolean; roomOpen: boolean },
): LocalNotice | null {
  if (!options.enabled || s.phase !== 'active' || s.openEnded || !s.endsAt) return null;
  return {
    id: NOTICE_IDS.studyTimer,
    ...studyTimerCopy(s),
    at: s.endsAt,
    route: 'study-session',
    // In the study room the timer itself says "Time's up"; a banner on top
    // would be a second alert. Anywhere else in the app it is the alert.
    showInForeground: !options.roomOpen,
  };
}

export type NoticeStep =
  | { action: 'schedule'; notice: LocalNotice; key: string }
  | { action: 'cancel' }
  | { action: 'keep' };

export const noticeKey = (n: LocalNotice) =>
  [n.id, Math.round(n.at / 1000), n.title, n.body, n.showInForeground ? 'fg' : 'bg'].join('|');

/**
 * What to do next, given the key of what was last scheduled: undefined when
 * nothing is known yet (a launch, or another student before), null when it was
 * cancelled.
 */
export function planStudyNotice(
  previous: string | null | undefined,
  s: StudyTimerSnapshot,
  options: { enabled: boolean; roomOpen: boolean },
): NoticeStep {
  const notice = studyTimerNotice(s, options);
  if (notice) {
    const key = noticeKey(notice);
    return key === previous ? { action: 'keep' } : { action: 'schedule', notice, key };
  }
  // The clock flips to "complete" within half a second either side of the
  // scheduled time (it rounds to whole seconds), and the student may be
  // anywhere: let the notification fire.
  if (ranOut(s)) return { action: 'keep' };
  return previous === null ? { action: 'keep' } : { action: 'cancel' };
}

// ── Live Activity (iOS lock screen and Dynamic Island) ─────

export interface StudyActivityState {
  subject: string;
  /** "25 min · Practice", "Open-ended · Revision", "25 + 10 min · Practice" */
  detail: string;
  phase: 'running' | 'paused' | 'done';
  countsDown: boolean;
  /** Wall-clock start (ms), shifted by pauses: the count-up anchor. */
  startedAt: number;
  /** Wall-clock end (ms) of a running countdown. */
  endsAt: number | null;
  /** Frozen display while paused: seconds left (countdown) or studied (count-up). */
  pausedSeconds: number;
  /** The countdown's full length (0 when open-ended), for the progress bar. */
  totalSeconds: number;
  /** Shown in the done state. */
  doneLabel: string;
}

export function studyActivityState(s: StudyTimerSnapshot): StudyActivityState | null {
  if (s.phase === 'idle' || !s.subject) return null;
  const length = s.openEnded
    ? 'Open-ended'
    : s.extendedMinutes > 0 ? `${s.plannedMinutes} + ${s.extendedMinutes} min` : `${s.plannedMinutes} min`;
  const remaining = Math.max(0, s.totalDuration - s.elapsedSeconds);
  return {
    subject: s.subject,
    detail: `${length} · ${SESSION_TYPE_LABEL[s.sessionType]}`,
    phase: s.phase === 'active' ? 'running' : s.phase === 'paused' ? 'paused' : 'done',
    countsDown: !s.openEnded,
    startedAt: s.startedAt,
    endsAt: s.phase === 'active' && !s.openEnded ? s.endsAt : null,
    pausedSeconds: s.phase === 'paused' ? (s.openEnded ? s.elapsedSeconds : remaining) : 0,
    totalSeconds: s.openEnded ? 0 : s.totalDuration,
    doneLabel: ranOut(s) ? 'Time’s up' : 'Ready to log',
  };
}

/** Changes only when what the lock screen shows changes (not every tick). */
export const activityKey = (state: StudyActivityState | null) =>
  state ? JSON.stringify({ ...state, startedAt: Math.round(state.startedAt / 1000), endsAt: state.endsAt && Math.round(state.endsAt / 1000) }) : 'none';
