/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The running study session lives above the views, so a student can minimise
 * the timer and keep it counting while they use Mark Bank, Paper Trail or the
 * Topic Atlas. There is exactly one useStudySession per signed-in student: the
 * study room and the mini timer both read this provider. Reload safety stays in
 * the hook (services/studySessionStore).
 *
 * The hook runs in an engine keyed by uid, so a different student signing in
 * on the same tab (sign-out does not reload) starts clean, without remounting
 * the app beneath the provider.
 */

import React, { createContext, memo, useContext, useLayoutEffect, useState } from 'react';
import { useStudySession } from '../hooks/useStudySession';
import type { UserProgress } from '../types';
import type { CourseData } from '../components/Library';

export type StudySessionState = ReturnType<typeof useStudySession>;

interface Scope { session: StudySessionState | null }

const StudySessionContext = createContext<Scope | null>(null);

interface EngineProps {
  uid: string | undefined;
  userProgress: UserProgress;
  allCourses: CourseData[];
  onSession: (session: StudySessionState) => void;
}

// Memoised: it re-renders on its own clock ticks, not on every publish.
const StudySessionEngine = memo(function StudySessionEngine({ uid, userProgress, allCourses, onSession }: EngineProps) {
  const session = useStudySession(uid, userProgress, allCourses);
  useLayoutEffect(() => { onSession(session); });
  return null;
});

export function StudySessionProvider({ uid, userProgress, allCourses, children }: {
  uid: string | undefined;
  userProgress: UserProgress;
  allCourses: CourseData[];
  children: React.ReactNode;
}) {
  const [session, setSession] = useState<StudySessionState | null>(null);
  return (
    <StudySessionContext.Provider value={{ session }}>
      <StudySessionEngine key={uid ?? 'signed-out'} uid={uid} userProgress={userProgress} allCourses={allCourses} onSession={setSession} />
      {children}
    </StudySessionContext.Provider>
  );
}

/** The provider's scope, or null when rendered outside one. */
export const useStudySessionScope = (): Scope | null => useContext(StudySessionContext);

/** The shared running session, or null (no provider, or its first frame). */
export const useSharedStudySession = (): StudySessionState | null => useContext(StudySessionContext)?.session ?? null;
