import React, { createContext, useContext, useState } from 'react';
import { createDemoStudentProfile, createDemoStudySessions, createDemoTopicMastery, createDemoMockResults, createDemoTimetableCompletions } from '../../data/devStudent';
import { canonicalMasteryForSpecification, projectTopicMastery, upsertCanonicalMastery } from '../../services/topicMasteryMigration';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../../curriculumRegistry';
import type { useTopicMastery } from '../../hooks/useTopicMastery';
import type { useMockResults } from '../../hooks/useMockResults';
import type { UnifiedMockResult } from '../../types';

// The review builds the real product component with the existing demo seed.
// Provider aliases below are scoped to the portable build, with no persistence.
const now = new Date();
export const profile = createDemoStudentProfile(now);
const names = profile.subjects.map(subject => subject.subjectName);
export const sessions = createDemoStudySessions(now, names);
export const completions = createDemoTimetableCompletions(now);
const Context = createContext<{ topicMastery: ReturnType<typeof useTopicMastery>; mockResults: ReturnType<typeof useMockResults>; futureFinderPicks: []; } | null>(null);

export function ReviewProvider({ children }: { children: React.ReactNode }) {
  const [canonical, setCanonical] = useState(() => createDemoTopicMastery(profile, now));
  const [mocks, setMocks] = useState(() => createDemoMockResults(now, names));
  const mastery = projectTopicMastery(canonical);
  const topicMastery: ReturnType<typeof useTopicMastery> = {
    canonicalMastery: canonical, mastery, isLoaded: true,
    setTopicConfidence: (subject, topic, confidence, source = 'manual', id) => setCanonical(value => upsertCanonicalMastery(value, subject, topic, { confidence, source, updatedAt: Date.now() }, profile.examStartDate, id)),
    importSyllabusTopics: () => {}, bulkUpdate: () => {},
    getSubjectTopics: subject => mastery[subject] ?? {},
    getTopicConfidence: (subject, topic) => mastery[subject]?.[topic]?.confidence ?? 'not-started',
    getCanonicalSubjectTopics: subject => {
      const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(profile.examStartDate));
      return spec ? canonicalMasteryForSpecification(canonical, spec.id) : {};
    },
  };
  const mockResults: ReturnType<typeof useMockResults> = {
    mocks, isLoaded: true,
    addMockResult: mock => setMocks(value => [...value, { ...mock, id: `review-${Date.now()}`, timestamp: Date.now() } as UnifiedMockResult]),
    removeMockResult: id => setMocks(value => value.filter(mock => mock.id !== id)),
    getLatestBySubject: subject => {
      const mock = mocks.filter(item => item.entries.some(entry => entry.subjectName === subject)).sort((a, b) => b.timestamp - a.timestamp)[0];
      const entry = mock?.entries.find(item => item.subjectName === subject);
      return mock && entry ? { mock, entry } : null;
    },
  };
  return <Context.Provider value={{ topicMastery, mockResults, futureFinderPicks: [] }}>{children}</Context.Provider>;
}
export function useInnovationData() {
  const value = useContext(Context);
  if (!value) throw new Error('The review provider is missing.');
  return value;
}
export const useOptionalProgress = () => ({ studySessions: sessions, studyDebriefs: [], rawProgressDoc: { sm2States: [] } });
