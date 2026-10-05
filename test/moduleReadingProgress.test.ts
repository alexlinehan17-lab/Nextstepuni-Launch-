import { describe, expect, test } from 'vitest';
import { readSectionIds, readingCheckpoint, resumeSection } from '@/utils/moduleReadingProgress';
const sections = [{ id: 'first' }, { id: 'second' }, { id: 'third' }];
describe('independent reading checkpoints', () => {
  test('opening a later page neither completes it nor the pages skipped', () => {
    const opened = readingCheckpoint({ unlockedSection: 0 }, sections, 'full', 2, false);
    expect(opened.unlockedSection).toBe(0);
    expect(resumeSection(opened, sections, 'full')).toBe(2);
    const finished = readingCheckpoint(opened, sections, 'full', 2, true);
    expect([...readSectionIds(finished, sections, 'full')]).toEqual(['third']);
    expect(finished.unlockedSection).toBe(1);
  });
  test('out-of-order reading counts each section once', () => {
    let progress = readingCheckpoint({ unlockedSection: 0 }, sections, 'full', 2, true);
    progress = readingCheckpoint(progress, sections, 'full', 2, true);
    expect(progress.unlockedSection).toBe(1);
    progress = readingCheckpoint(progress, sections, 'full', 0, true);
    progress = readingCheckpoint(progress, sections, 'full', 1, true);
    expect(progress.unlockedSection).toBe(3);
    expect(readSectionIds(progress, sections, 'full').size).toBe(3);
  });
  test('preserves historical reading and distinguishes Essentials from the full lesson', () => {
    expect([...readSectionIds({ unlockedSection: 2 }, sections, 'full')]).toEqual(['first', 'second']);
    const short = [{ id: 'short' }];
    const progress = readingCheckpoint({ unlockedSection: 0 }, short, 'essentials', 0, true, 3);
    expect(progress.unlockedSection).toBe(3);
    expect(readSectionIds(progress, sections, 'full').size).toBe(0);
    expect(readSectionIds(progress, short, 'essentials').size).toBe(1);
  });
});
