import { describe, expect, it } from 'vitest';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { equalTopicAllocations, getStudyTopicOptions, recordedSubjectActivity, recordedTopicActivity, studyTopicSelection, unallocatedStudySeconds, validTopicAllocations } from '../services/studyTopicHistory';
import type { StudySessionRecord } from '../utils/strategyRegistry';
import { buildSubjectAllocation } from '../components/dashboard/dashboardAnalytics';

const spec = resolveCurriculumSpecification('Politics & Society', 2027)!;
const ids = spec.groups.slice(0, 3).map(group => group.id);
const selection = studyTopicSelection('Politics & Society', ids, '2027-06-02', 'Higher')!;
const session: StudySessionRecord = { id: 'one', date: '2026-10-03', subject: 'Politics & Society', sessionType: 'revision', plannedMinutes: 40, actualSeconds: 1801, startedAt: 0, completedAt: 1801000, pointsEarned: 0, hadReflection: false, subjectId: spec.subjectId, specificationId: spec.id, topicAllocations: equalTopicAllocations(ids, 1801) };

describe('recorded topic time', () => {
  it('splits the actual seconds once, including the remainder', () => {
    expect(session.topicAllocations?.map(item => item.seconds)).toEqual([601, 600, 600]);
    expect(validTopicAllocations(selection, session.topicAllocations!, 1801)).toBe(true);
    expect(ids.reduce((sum, id) => sum + recordedTopicActivity([session], spec, id).seconds, 0)).toBe(1801);
    expect(recordedSubjectActivity([session, session], 'Politics and Society').seconds).toBe(1801);
    expect(buildSubjectAllocation([session, session])).toEqual([{ id: spec.subjectId, label: 'Politics and Society', value: 30 }]);
  });
  it('accepts an edited split and rejects overcounting, missing topics and foreign IDs', () => {
    const edited = ids.map((topicId, index) => ({ topicId, seconds: [901, 900, 0][index] }));
    expect(validTopicAllocations(selection, edited, 1801)).toBe(true);
    expect(validTopicAllocations(selection, edited.slice(1), 1801)).toBe(false);
    expect(validTopicAllocations(selection, edited.map(item => ({ ...item, seconds: 1801 })), 1801)).toBe(false);
    expect(validTopicAllocations({ ...selection, topicIds: ['foreign'] }, [{ topicId: 'foreign', seconds: 1801 }], 1801)).toBe(false);
  });
  it('keeps subject-only history explicit and excludes other specifications', () => {
    const older = { ...session, id: 'older', subjectId: undefined, specificationId: undefined, topicAllocations: undefined };
    const different = { ...session, id: 'different', specificationId: 'other' };
    expect(recordedSubjectActivity([session, older], 'Politics and Society').seconds).toBe(3602);
    expect(unallocatedStudySeconds([session, older], 'Politics and Society')).toBe(1801);
    expect(recordedTopicActivity([older, different], spec, ids[0]).seconds).toBe(0);
    expect(older.topicAllocations).toBeUndefined();
  });
  it('rolls up group and child allocations without multiplying the subject total', () => {
    const group = spec.groups[0], child = group.topics[0];
    const allocated = { ...session, topicAllocations: [{ topicId: group.id, seconds: 901 }, { topicId: child.id, seconds: 900 }] };
    expect(recordedTopicActivity([allocated], spec, group.id).seconds).toBe(1801);
    expect(recordedTopicActivity([allocated], spec, child.id).seconds).toBe(900);
    expect(recordedSubjectActivity([allocated], spec.subjectId).seconds).toBe(1801);
  });
  it('resolves display aliases, current cohorts and supported paper levels', () => {
    expect(getStudyTopicOptions('Design & Communication Graphics', '2027-06-02', 'Higher').length).toBeGreaterThan(0);
    expect(getStudyTopicOptions('Arabic', '2027-06-02', 'Ordinary')[0].specificationId).toBe('arabic:2027');
    expect(getStudyTopicOptions('Arabic', '2027-06-02', 'Foundation')).toEqual([]);
    expect(studyTopicSelection('Arabic', ids, '2027-06-02')).toBeUndefined();
  });
});
