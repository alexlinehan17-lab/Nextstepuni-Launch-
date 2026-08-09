/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useTopicMastery } from '../hooks/useTopicMastery';
import { useMockResults } from '../hooks/useMockResults';
import { type StudentSubjectProfile } from '../components/subjectData';
import { type CAOCourse, hydrateCourses } from '../components/futureFinderData';
import { computeSubjectPriorities, type SubjectPriority } from '../components/timetableAlgorithm';
import { LC_SUBJECTS, getPointsForGrade, type Grade } from '../components/subjectData';

// ─── Types ──────────────────────────────────────────────────

interface InnovationDataContextValue {
  // Topic mastery (shared by WarRoom, SyllabusXRay, SpacedRepTimetable)
  topicMastery: ReturnType<typeof useTopicMastery>;

  // Mock results (shared by WarRoom, CAOSimulator, PointsPassport)
  mockResults: ReturnType<typeof useMockResults>;

  // Future Finder picks (shared by WarRoom, ComebackEngine, CAOSimulator)
  futureFinderPicks: CAOCourse[];
  futureFinderLoading: boolean;

  // Computed: current CAO points from profile
  currentCAOPoints: number;

  // Computed: subject priorities (with topic mastery factored in)
  subjectPriorities: SubjectPriority[];
}

// ─── Context ────────────────────────────────────────────────

const InnovationDataContext = createContext<InnovationDataContextValue | null>(null);

export const useInnovationData = (): InnovationDataContextValue => {
  const ctx = useContext(InnovationDataContext);
  if (!ctx) throw new Error('useInnovationData must be used within InnovationDataProvider');
  return ctx;
};

// ─── Provider ───────────────────────────────────────────────

interface InnovationDataProviderProps {
  children: React.ReactNode;
  uid?: string;
  subjectProfile: StudentSubjectProfile | null;
}

export const InnovationDataProvider: React.FC<InnovationDataProviderProps> = ({
  children, uid, subjectProfile,
}) => {
  // Shared hooks — called once here instead of in each tool
  const topicMastery = useTopicMastery(uid, subjectProfile?.examStartDate);
  const mockResults = useMockResults(uid);

  // Future Finder picks — loaded from Firestore once
  const [futureFinderPicks, setFutureFinderPicks] = useState<CAOCourse[]>([]);
  const [futureFinderLoading, setFutureFinderLoading] = useState(true);

  useEffect(() => {
    if (!uid) { setFutureFinderPicks([]); setFutureFinderLoading(false); return; }
    let cancelled = false;
    setFutureFinderLoading(true);
    getDoc(doc(db, 'progress', uid)).then(snap => {
      if (cancelled) return;
      const data = snap.data();
      // Union both Future Finder namespaces. The live senior tool writes
      // `futureFinderRevamped`; only the retired tile writes `futureFinder`.
      // Reading the legacy field alone meant War Room's target course, the CAO
      // Simulator's gap panel, the Comeback anchor and the Career Paths seed
      // all pointed at a list the student had abandoned — or at nothing.
      // Preference order: explicit bookmarks → the algorithm's ranking → legacy.
      const revamped = data?.futureFinderRevamped as { picks?: string[]; topMatches?: string[] } | undefined;
      const codes = revamped?.picks?.length
        ? revamped.picks
        : revamped?.topMatches?.length
          ? revamped.topMatches
          : (data?.futureFinder?.topPicks ?? []);
      setFutureFinderPicks(codes.length ? hydrateCourses(codes).slice(0, 5) : []);
      setFutureFinderLoading(false);
    }).catch(() => {
      if (!cancelled) setFutureFinderLoading(false);
    });
    return () => { cancelled = true; };
  }, [uid]);

  // Computed: current CAO points (best 6 from current grades)
  const currentCAOPoints = useMemo(() => {
    if (!subjectProfile) return 0;
    const points = subjectProfile.subjects.map(s => {
      const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths ?? false;
      return getPointsForGrade(s.currentGrade as Grade, isMaths);
    }).sort((a, b) => b - a);
    return points.slice(0, 6).reduce((sum, p) => sum + p, 0);
  }, [subjectProfile]);

  // Computed: subject priorities WITH topic mastery factored in
  const subjectPriorities = useMemo(() => {
    if (!subjectProfile) return [];
    return computeSubjectPriorities(subjectProfile.subjects, topicMastery.mastery, subjectProfile.examStartDate);
  }, [subjectProfile, topicMastery.mastery]);

  const value: InnovationDataContextValue = {
    topicMastery,
    mockResults,
    futureFinderPicks,
    futureFinderLoading,
    currentCAOPoints,
    subjectPriorities,
  };

  return <InnovationDataContext.Provider value={value}>{children}</InnovationDataContext.Provider>;
};

export default InnovationDataContext;
