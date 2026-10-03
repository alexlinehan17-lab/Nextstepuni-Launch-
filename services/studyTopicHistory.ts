/** @license SPDX-License-Identifier: Apache-2.0 */
import {
  CURRICULUM_SPECIFICATIONS, examinationYearFromDate,
  resolveCurriculumSpecification, resolveSubjectId, specificationContainsId,
  type CanonicalCurriculumSpecification,
} from '../curriculumRegistry';
import type { CurriculumLevel } from '../curriculum';
import type { StudySessionRecord } from '../utils/strategyRegistry';
import type { StudyTopicAllocation, StudyTopicSelection } from '../types/studyTopics';

export interface StudyTopicOption {
  id: string;
  name: string;
  groupId: string;
  groupName: string;
  specificationId: string;
  kind: 'area' | 'topic';
}

export function sameStudySubject(a: string, b: string): boolean {
  const first = resolveSubjectId(a), second = resolveSubjectId(b);
  return first && second ? first === second : a.trim().toLowerCase() === b.trim().toLowerCase();
}

export function getStudyTopicOptions(subject: string, examDate?: string | null, level?: string): StudyTopicOption[] {
  const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
  if (!spec || spec.status !== 'verified' || (level && !spec.levels.includes(level.toLowerCase() as CurriculumLevel))) return [];
  return spec.groups.flatMap(group => [
    { id: group.id, name: group.title, groupId: group.id, groupName: group.title, specificationId: spec.id, kind: 'area' as const },
    ...group.topics.filter(topic => !topic.levels || !level || topic.levels.includes(level.toLowerCase() as CurriculumLevel)).map(topic => ({
      id: topic.id, name: topic.title, groupId: group.id, groupName: group.title, specificationId: spec.id, kind: 'topic' as const,
    })),
  ]);
}

export function studyTopicSelection(subject: string, topicIds: string[], examDate?: string | null, level?: string): StudyTopicSelection | undefined {
  const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
  if (!spec || spec.status !== 'verified') return undefined;
  const allowed = new Set(getStudyTopicOptions(subject, examDate, level).map(topic => topic.id));
  const ids = [...new Set(topicIds)];
  if (ids.some(id => !allowed.has(id))) return undefined;
  return { subjectId: spec.subjectId, specificationId: spec.id, topicIds: ids };
}

export function equalTopicAllocations(topicIds: string[], actualSeconds: number): StudyTopicAllocation[] {
  const ids = [...new Set(topicIds)];
  if (!ids.length) return [];
  const total = Math.max(0, Math.floor(actualSeconds));
  const base = Math.floor(total / ids.length), remainder = total % ids.length;
  return ids.map((topicId, index) => ({ topicId, seconds: base + (index < remainder ? 1 : 0) }));
}

/** Every selected topic appears exactly once, and the pool is the actual clock time. */
export function validTopicAllocations(selection: StudyTopicSelection, allocations: StudyTopicAllocation[], actualSeconds: number): boolean {
  const spec = CURRICULUM_SPECIFICATIONS.find(item => item.id === selection.specificationId && item.subjectId === selection.subjectId);
  const selected = new Set(selection.topicIds);
  if (!spec || selected.size !== selection.topicIds.length || selection.topicIds.some(id => !specificationContainsId(spec, id))) return false;
  if (!selected.size) return allocations.length === 0;
  return allocations.length === selected.size
    && new Set(allocations.map(item => item.topicId)).size === selected.size
    && allocations.every(item => selected.has(item.topicId) && Number.isInteger(item.seconds) && item.seconds >= 0)
    && allocations.reduce((sum, item) => sum + item.seconds, 0) === actualSeconds;
}

/** Validate before writing a session, its reflection or its points. */
export function sessionTopicAllocations(selection: StudyTopicSelection | undefined, actualSeconds: number, allocations?: StudyTopicAllocation[]): StudyTopicAllocation[] {
  const next = allocations ?? equalTopicAllocations(selection?.topicIds ?? [], actualSeconds);
  if (selection && !validTopicAllocations(selection, next, actualSeconds)) {
    throw new Error('Topic time must add up to the recorded session.');
  }
  if (!selection && next.length) throw new Error('Select topics before allocating time.');
  return next;
}

export function uniqueStudySessions(sessions: StudySessionRecord[]): StudySessionRecord[] {
  const byId = new Map<string, StudySessionRecord>();
  for (const session of sessions) {
    if (!byId.has(session.id) || session.completedAt > byId.get(session.id)!.completedAt) byId.set(session.id, session);
  }
  return [...byId.values()];
}

export function recordedSubjectActivity(sessions: StudySessionRecord[], subject: string) {
  const records = uniqueStudySessions(sessions).filter(session => sameStudySubject(session.subjectId ?? session.subject, subject));
  return { records, count: records.length, seconds: records.reduce((sum, record) => sum + Math.max(0, record.actualSeconds), 0) };
}

export function canonicalNodeIds(spec: CanonicalCurriculumSpecification, nodeId: string): string[] {
  const group = spec.groups.find(item => item.id === nodeId);
  return group ? [group.id, ...group.topics.map(topic => topic.id)] : [nodeId];
}

export function recordedTopicActivity(sessions: StudySessionRecord[], spec: CanonicalCurriculumSpecification, nodeId: string) {
  const nodes = new Set(canonicalNodeIds(spec, nodeId));
  const subject = recordedSubjectActivity(sessions, spec.subjectId);
  const records = subject.records.flatMap(session => {
    if (session.specificationId !== spec.id || !session.topicAllocations?.length) return [];
    const selection = { subjectId: spec.subjectId, specificationId: spec.id, topicIds: session.topicAllocations.map(item => item.topicId) };
    if (!validTopicAllocations(selection, session.topicAllocations, session.actualSeconds)) return [];
    const seconds = session.topicAllocations.filter(item => nodes.has(item.topicId)).reduce((sum, item) => sum + item.seconds, 0);
    return seconds > 0 ? [{ session, seconds }] : [];
  });
  return { records: records.sort((a, b) => b.session.completedAt - a.session.completedAt), count: records.length, seconds: records.reduce((sum, record) => sum + record.seconds, 0) };
}

export function unallocatedStudySeconds(sessions: StudySessionRecord[], subject: string): number {
  return recordedSubjectActivity(sessions, subject).records.reduce((sum, session) => {
    const selection = { subjectId: session.subjectId ?? '', specificationId: session.specificationId ?? '', topicIds: session.topicAllocations?.map(item => item.topicId) ?? [] };
    return sum + (selection.topicIds.length && validTopicAllocations(selection, session.topicAllocations ?? [], session.actualSeconds) ? 0 : Math.max(0, session.actualSeconds));
  }, 0);
}
