import { describe, expect, it } from 'vitest';
import { buildRecoveryPlan } from '../components/comeback/recoveryPlan';
import type { StudentSubjectProfile } from '../components/subjectData';

const profile: StudentSubjectProfile = {
  subjects: [
    { subjectName: 'Biology', level: 'higher', currentGrade: 'H5', targetGrade: 'H2' },
    { subjectName: 'English', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
  ],
  examStartDate: '2027-06-01',
  restDays: ['Sunday'],
  defaultBlockDuration: 45,
  createdAt: '2026-01-01',
  updatedAt: '2026-01-01',
};

describe('buildRecoveryPlan', () => {
  it('keeps the week small, respects rest days and focuses on at most two subjects', () => {
    const plan = buildRecoveryPlan({
      profile,
      priorities: [
        { subjectName: 'Biology', currentGrade: 'H5', targetGrade: 'H2', isMaths: false, currentPoints: 56, targetPoints: 88, pointsGain: 32, difficultyMultiplier: 1, efficiencyMultiplier: 1, priorityScore: 4 },
        { subjectName: 'English', currentGrade: 'H4', targetGrade: 'H2', isMaths: false, currentPoints: 66, targetPoints: 88, pointsGain: 22, difficultyMultiplier: 1, efficiencyMultiplier: 1, priorityScore: 2 },
      ],
      masteryEntries: [],
      timetableCompletions: {},
      reason: 'overloaded',
      capacity: 5,
      curriculumLevel: 'senior',
      now: new Date(2026, 7, 9, 12), // Sunday
    });

    expect(plan.actions).toHaveLength(5);
    expect(new Set(plan.actions.map(action => action.subject)).size).toBeLessThanOrEqual(2);
    expect(plan.actions.every(action => action.dayLabel !== 'Sun 9')).toBe(true);
    expect(plan.signals.find(signal => signal.id === 'capacity')?.detail).toContain('5 focused blocks');
  });
});
