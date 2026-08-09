import { describe, expect, it } from 'vitest';
import {
  allocateSessions,
  computeSubjectPriorities,
  computeWeeklyStudyTarget,
  generateWeeklyTimetable,
  type SubjectPriority,
} from '../components/timetableAlgorithm';
import type { StudentSubject } from '../components/subjectData';

const priorities: SubjectPriority[] = [
  ['Biology', 8],
  ['Mathematics', 7],
  ['English', 6],
  ['Chemistry', 5],
  ['History', 4],
  ['Geography', 3],
  ['French', 2],
].map(([subjectName, priorityScore]) => ({
  subjectName: subjectName as string,
  currentGrade: 'H5',
  targetGrade: 'H2',
  isMaths: subjectName === 'Mathematics',
  currentPoints: 56,
  targetPoints: 88,
  pointsGain: 32,
  difficultyMultiplier: 1,
  efficiencyMultiplier: 1,
  priorityScore: priorityScore as number,
}));

describe('weekly study workload', () => {
  it('ramps gradually and stays inside the six-to-twelve-hour envelope', () => {
    const targets = [30, 20, 12, 6, 3].map(computeWeeklyStudyTarget);
    expect(targets.map(target => target.targetHours)).toEqual([6, 6.75, 8.25, 10, 12]);
    expect(targets.every((target, index) => index === 0 || target.targetMinutes >= targets[index - 1].targetMinutes)).toBe(true);
  });

  it('translates hours into the correct number of focused blocks', () => {
    const foundation = allocateSessions(priorities, 30, undefined, 45);
    const examPrep = allocateSessions(priorities, 3, undefined, 45);
    expect(foundation.reduce((sum, item) => sum + item.sessions, 0)).toBe(8);
    expect(examPrep.reduce((sum, item) => sum + item.sessions, 0)).toBe(16);
  });

  it('uses every block when all subjects are already at target', () => {
    const atTarget = priorities.map(priority => ({ ...priority, priorityScore: 0, pointsGain: 0 }));
    const allocation = allocateSessions(atTarget, 30, undefined, 45);
    expect(allocation.reduce((sum, item) => sum + item.sessions, 0)).toBe(8);
  });
});

describe('best-six CAO optimisation', () => {
  const subject = (subjectName: string, currentGrade: StudentSubject['currentGrade'], targetGrade: StudentSubject['targetGrade']): StudentSubject => ({
    subjectName,
    level: 'higher',
    currentGrade,
    targetGrade,
  });

  it('does not divert extra sessions to a target that cannot enter the current best six', () => {
    const studentSubjects = [
      subject('English', 'H2', 'H1'),
      subject('Irish', 'H2', 'H1'),
      subject('Biology', 'H2', 'H1'),
      subject('Chemistry', 'H2', 'H1'),
      subject('Business', 'H2', 'H1'),
      subject('Geography', 'H2', 'H1'),
      subject('Art', 'H7', 'H4'),
    ];
    const result = computeSubjectPriorities(studentSubjects);
    const art = result.find(item => item.subjectName === 'Art');
    expect(art?.pointsGain).toBe(29);
    expect(art?.bestSixPointsGain).toBe(0);
    expect(art?.priorityScore).toBe(0);

    const allocation = allocateSessions(result, 30, undefined, 45);
    expect(allocation.find(item => item.subjectName === 'Art')?.sessions).toBe(1);
  });

  it('recognises the Higher Maths bonus only to the extent that it changes best-six points', () => {
    const studentSubjects = [
      subject('Mathematics', 'H7', 'H6'),
      subject('English', 'H5', 'H3'),
      subject('Irish', 'H5', 'H3'),
      subject('Biology', 'H5', 'H3'),
      subject('Chemistry', 'H5', 'H3'),
      subject('Business', 'H5', 'H3'),
      subject('Geography', 'H5', 'H3'),
    ];
    const maths = computeSubjectPriorities(studentSubjects).find(item => item.subjectName === 'Mathematics');
    expect(maths?.pointsGain).toBe(34);
    expect(maths?.bestSixPointsGain).toBe(15);
    expect(maths?.targetGradeSteps).toBe(1);
  });

  it('ramps total hours without allowing one subject to consume the timetable', () => {
    const studentSubjects = [
      subject('Mathematics', 'H6', 'H2'),
      subject('English', 'H4', 'H2'),
      subject('Irish', 'H5', 'H3'),
      subject('Biology', 'H6', 'H2'),
      subject('Chemistry', 'H4', 'H2'),
      subject('Business', 'H3', 'H1'),
      subject('Geography', 'H2', 'H1'),
    ];
    const result = computeSubjectPriorities(studentSubjects);
    const foundation = allocateSessions(result, 30, undefined, 45);
    const examPrep = allocateSessions(result, 3, undefined, 45);
    expect(foundation.reduce((sum, item) => sum + item.sessions * 45, 0) / 60).toBe(6);
    expect(examPrep.reduce((sum, item) => sum + item.sessions * 45, 0) / 60).toBe(12);
    expect(Math.max(...examPrep.map(item => item.sessions))).toBeLessThanOrEqual(
      Math.min(...examPrep.map(item => item.sessions)) * 3,
    );
    const building = allocateSessions(result, 12, undefined, 45);
    const mathsSessions = building.find(item => item.subjectName === 'Mathematics')?.sessions ?? 0;
    expect(mathsSessions).toBe(Math.max(...building.map(item => item.sessions)));
  });
});

describe('weekly day placement', () => {
  it('balances an ordinary week instead of creating one-block and four-block days', () => {
    const allocations = allocateSessions(priorities, 3, undefined, 45);
    const timetable = generateWeeklyTimetable(allocations, 3, 0, [], 45);
    const loads = timetable.map(day => day.blocks.length);
    expect(loads.reduce((sum, load) => sum + load, 0)).toBe(16);
    expect(Math.max(...loads) - Math.min(...loads)).toBeLessThanOrEqual(1);
  });

  it('keeps rest days empty and balances the remaining active days', () => {
    const allocations = allocateSessions(priorities, 20, undefined, 45);
    const timetable = generateWeeklyTimetable(allocations, 20, 0, ['Wednesday', 'Sunday'], 45);
    expect(timetable[2].blocks).toHaveLength(0);
    expect(timetable[6].blocks).toHaveLength(0);
    const activeLoads = timetable.filter((_, index) => index !== 2 && index !== 6).map(day => day.blocks.length);
    expect(Math.max(...activeLoads) - Math.min(...activeLoads)).toBeLessThanOrEqual(1);
  });

  it('spaces a subject across days when the week has room', () => {
    const allocations = allocateSessions(priorities, 30, undefined, 45);
    const timetable = generateWeeklyTimetable(allocations, 30, 0, [], 45);
    for (const day of timetable) {
      const subjectNames = day.blocks.map(block => block.subjectName);
      expect(new Set(subjectNames).size).toBe(subjectNames.length);
    }
  });
});
