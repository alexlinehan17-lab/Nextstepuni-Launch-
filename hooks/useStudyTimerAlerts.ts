/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Keeps the device in step with the running study session: the "time's up"
 * notification is scheduled, moved or cancelled as the session starts, pauses,
 * resumes, keeps going and ends (services/studyTimerAlerts has the rules).
 *
 * Runs inside the StudySessionEngine, which is keyed by uid, so signing out or a
 * different student signing in unmounts it and cancels what it scheduled. Its
 * first pass also cancels anything left over from before a relaunch.
 */

import { useEffect, useRef } from 'react';
import type { useStudySession } from './useStudySession';
import { useStudyNotifications } from './useStudyNotifications';
import { cancelLocalNotice, NOTICE_IDS, scheduleLocalNotice } from '../services/notifications';
import { planStudyNotice, ranOut, type StudyTimerSnapshot } from '../services/studyTimerAlerts';

type StudySession = ReturnType<typeof useStudySession>;

export function studyTimerSnapshot(session: StudySession): StudyTimerSnapshot {
  return {
    phase: session.phase,
    subject: session.subject,
    sessionType: session.sessionType,
    openEnded: session.openEnded,
    endsAt: session.endsAt,
    startedAt: session.startedAt,
    plannedMinutes: session.plannedMinutes,
    extendedMinutes: session.extendedMinutes,
    elapsedSeconds: session.elapsedSeconds,
    totalDuration: session.totalDuration,
  };
}

export function useStudyTimerAlerts(session: StudySession, { uid, roomOpen }: { uid: string | undefined; roomOpen: boolean }) {
  const { enabled } = useStudyNotifications();
  const snapshot = studyTimerSnapshot(session);
  const finished = ranOut(snapshot);
  /** Key of what was last scheduled: undefined unknown, null cancelled. */
  const scheduled = useRef<string | null | undefined>(undefined);

  useEffect(() => {
    if (!uid) return;
    const step = planStudyNotice(scheduled.current, snapshot, { enabled, roomOpen });
    if (step.action === 'schedule') {
      scheduled.current = step.key;
      void scheduleLocalNotice(step.notice);
    } else if (step.action === 'cancel') {
      scheduled.current = null;
      void cancelLocalNotice(NOTICE_IDS.studyTimer);
    }
    // Only what the notification depends on: not the clock's every tick.
  }, [uid, enabled, roomOpen, snapshot.phase, snapshot.subject, snapshot.openEnded, snapshot.endsAt, snapshot.plannedMinutes, snapshot.extendedMinutes, finished]);

  useEffect(() => () => {
    if (!uid) return;
    scheduled.current = undefined;
    void cancelLocalNotice(NOTICE_IDS.studyTimer);
  }, [uid]);
}
