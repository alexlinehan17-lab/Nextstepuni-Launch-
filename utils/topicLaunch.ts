import type { StudyTopicSelection } from '../types/studyTopics';

// Navigation carries no learning records. A launch is an in-memory suggestion,
// scoped to the signed-in student and cleared after the destination mounts.
const study = new Map<string, StudyTopicSelection>();
const practice = new Map<string, { subjectId: string; subtopicId: string; level?: string }>();
export function queueTopicStudy(uid: string, selection: StudyTopicSelection) { study.set(uid, { ...selection, topicIds: [...selection.topicIds] }); }
export function peekTopicStudy(uid?: string) { return uid ? study.get(uid) : undefined; }
export function clearTopicStudy(uid?: string) { if (uid) study.delete(uid); }
export function queueTopicPractice(uid: string, subjectId: string, subtopicId: string, level?: string) { practice.set(uid, { subjectId, subtopicId, ...(level ? { level } : {}) }); }
export function peekTopicPractice(uid?: string) { return uid ? practice.get(uid) : undefined; }
export function clearTopicPractice(uid?: string) { if (uid) practice.delete(uid); }
