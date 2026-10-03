import { describe, expect, test } from 'vitest';
import { fieldNotesData } from '@/components/dashboard/fieldNotesData';
import type { StudySessionRecord } from '@/studySessionData';

const record = (date: string, actualSeconds = 1500): StudySessionRecord => ({
  id: `${date}-${actualSeconds}`,
  date,
  actualSeconds,
  subject: 'Geography',
  sessionType: 'practice',
  plannedMinutes: 25,
  startedAt: 0,
  completedAt: 0,
  pointsEarned: 0,
  hadReflection: false,
});

describe('Home Field notes uses recorded study', () => {
  test('counts the current Monday-to-Sunday week, excludes future and invalid records, and sums seconds before rounding', () => {
    const result = fieldNotesData(
      [
        record('2026-09-20'),
        record('2026-09-21', 59),
        record('2026-09-21', 61),
        record('2026-09-23', 3600),
        record('2026-09-24'),
        record('2026-09-22', -60),
        record('2026-09-22', NaN),
      ],
      new Date(2026, 8, 23, 12),
    );
    expect(result.minutes).toBe(62);
    expect(result.sessions).toBe(3);
    expect(result.activeDays).toBe(2);
    expect(result.days.map((day) => day.key)).toEqual([
      '2026-09-21',
      '2026-09-22',
      '2026-09-23',
      '2026-09-24',
      '2026-09-25',
      '2026-09-26',
      '2026-09-27',
    ]);
    expect(result.days[0].minutes).toBe(2);
    expect(result.days[3]).toMatchObject({ future: true, minutes: 0, sessions: 0 });
  });
  test('continues yesterday’s streak across daylight saving and breaks at a missing study day', () => {
    const history = ['2026-10-23', '2026-10-24', '2026-10-25'].map((date) => record(date));
    expect(fieldNotesData(history, new Date(2026, 9, 26, 9)).streak).toBe(3);
    expect(fieldNotesData(history, new Date(2026, 9, 27, 9)).streak).toBe(0);
  });
  test('a new student starts at zero without example study data', () => {
    const result = fieldNotesData([], new Date(2026, 8, 27));
    expect(result).toMatchObject({ minutes: 0, sessions: 0, activeDays: 0, streak: 0 });
    expect(result.days.every((day) => day.seconds === 0)).toBe(true);
  });
});
