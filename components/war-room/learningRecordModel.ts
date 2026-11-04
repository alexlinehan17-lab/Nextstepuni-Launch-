import { getStudyTopicOptions, recordedSubjectActivity } from '../../services/studyTopicHistory';
import type { useTopicMastery } from '../../hooks/useTopicMastery';
import type { StudentSubject } from '../subjectData';
import type { StudySessionRecord } from '../../utils/strategyRegistry';

export function subjectLearningDetails(subject: StudentSubject, examDate: string | null | undefined, sessions: StudySessionRecord[], mastery: ReturnType<typeof useTopicMastery>) {
  const options = getStudyTopicOptions(subject.subjectName, examDate, subject.level);
  const canonical = mastery.getCanonicalSubjectTopics(subject.subjectName);
  const topics = options.map(option => ({ option, entry: canonical[option.id] }));
  const latest = topics.filter(topic => (topic.entry?.updatedAt ?? 0) > 0).sort((a, b) => b.entry!.updatedAt - a.entry!.updatedAt)[0];
  return { activity: recordedSubjectActivity(sessions, subject.subjectName), options, latest };
}

export const confidenceLabel = (value?: string) => value === 'solid' ? 'Solid' : value === 'shaky' ? 'Shaky' : value === 'not-started' ? 'Not started' : 'Not recorded';
export const levelLabel = (level: string) => `${level.charAt(0).toUpperCase()}${level.slice(1)} level`;

/** Short display for large totals; exact seconds remain in the subject record. */
export function compactStudyTime(seconds: number) {
  const total = Math.floor(Math.max(0, seconds));
  const hours = Math.floor(total / 3600), minutes = Math.floor(total % 3600 / 60);
  return hours ? `${hours.toLocaleString('en-IE')} hr${minutes ? ` ${minutes} min` : ''}` : total < 60 && total ? `${total} sec` : `${minutes} min`;
}
