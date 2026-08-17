import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, test } from 'vitest';

import { CAREERS } from '@/careerPathsData';
import {
  CAREER_DAY_PROFILES,
  isEntryRouteCopy,
  possibleDayFor,
  workplaceUpsideFor,
} from '@/components/possibleLifeModel';
import type { CareerCard } from '@/types/careerPaths';

const minutes = (time: string): number => {
  const [hours, mins] = time.split(':').map(Number);
  return hours * 60 + mins;
};

describe('Your Possible Life — career-specific ordinary days', () => {
  test('every offered career has an authored day and there are no stale profiles', () => {
    expect(Object.keys(CAREER_DAY_PROFILES).sort()).toEqual(
      CAREERS.map(career => career.id).sort(),
    );
  });

  test('every day is a chronological three-beat sequence with a named setting', () => {
    for (const career of CAREERS) {
      const day = possibleDayFor(career);
      expect(day.setting.trim().length, `${career.id}: setting`).toBeGreaterThan(30);
      expect(day.beats, `${career.id}: beats`).toHaveLength(3);

      const times = day.beats.map(beat => {
        expect(beat.time, `${career.id}: malformed time`).toMatch(/^\d{2}:\d{2}$/);
        expect(beat.title.trim().length, `${career.id}: beat title`).toBeGreaterThan(4);
        expect(beat.detail.trim().length, `${career.id}: beat detail`).toBeGreaterThan(25);
        return minutes(beat.time);
      });

      expect(times, `${career.id}: times out of order`).toEqual([...times].sort((a, b) => a - b));
      expect(day.workplaceReality.trim().length, `${career.id}: workplace reality`).toBeGreaterThan(35);
    }
  });

  test('no timed day or workplace reality contains an admissions or education barrier', () => {
    for (const career of CAREERS) {
      const day = possibleDayFor(career);
      const workplaceCopy = [
        day.setting,
        day.workplaceReality,
        ...day.beats.flatMap(beat => [beat.title, beat.detail]),
      ];

      for (const copy of workplaceCopy) {
        expect(isEntryRouteCopy(copy), `${career.id}: ${copy}`).toBe(false);
      }
      expect(isEntryRouteCopy(workplaceUpsideFor(career)), `${career.id}: workplace upside`).toBe(false);
    }
  });

  test('the pharmacist day describes pharmacy work, not CAO points or laboratory research', () => {
    const pharmacist = CAREERS.find(career => career.id === 'pharmacist')!;
    const copy = JSON.stringify(possibleDayFor(pharmacist));

    expect(copy).toMatch(/prescriptions/i);
    expect(copy).toMatch(/community pharmacy/i);
    expect(copy).not.toMatch(/CAO|points|laboratory researcher/i);
  });

  test('a future career without an authored profile still skips entry-only cons', () => {
    const futureCareer = {
      ...CAREERS[0],
      id: 'future-role',
      whatYouDo: ['Do the first workplace task', 'Do the second workplace task'],
      cons: ['Very high CAO points to get in', 'Night and weekend shifts are common'],
    } as CareerCard;

    expect(possibleDayFor(futureCareer).workplaceReality).toBe('Night and weekend shifts are common');
  });

  test('the day screen no longer reads its timeline or reality from the generic first con', () => {
    const source = readFileSync(resolve(process.cwd(), 'components/YourPossibleLife.tsx'), 'utf8');
    expect(source).toContain('day.beats.map');
    expect(source).toContain('day.workplaceReality');
    expect(source).not.toContain('career.cons[0]');
    expect(source).not.toContain('career.pros[0]');
  });
});
