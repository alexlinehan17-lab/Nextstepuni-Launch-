import { describe, expect, it } from 'vitest';
import { createDirectionProfile, getNorthStarDisplayText, hasStudentAuthoredNorthStar, normaliseDirectionProfile } from '../services/directionProfile';
import type { NorthStar } from '../types';

const northStar: NorthStar = {
  category: 'options-freedom',
  statement: 'Get enough points so I have choices',
  visionBoard: ['real-choices', 'see-world', 'freedom-no'],
  createdAt: '2026-08-09T00:00:00.000Z',
  updatedAt: '2026-08-09T00:00:00.000Z',
  authoredByStudent: false,
};

describe('direction profile', () => {
  it('turns onboarding selections into living vision items', () => {
    const profile = createDirectionProfile(northStar, '2026-08-09T01:00:00.000Z');
    expect(profile.version).toBe(2);
    expect(profile.visionItems.map(item => item.id)).toEqual(northStar.visionBoard);
    expect(profile.visionItems.every(item => item.state === 'curious')).toBe(true);
  });

  it('does not claim system category copy was authored by the student', () => {
    expect(hasStudentAuthoredNorthStar(northStar)).toBe(false);
    expect(getNorthStarDisplayText(northStar)).toContain('Get enough points');
  });

  it('preserves saved states while adding newly selected cards', () => {
    const existing = createDirectionProfile({ ...northStar, visionBoard: ['real-choices'] });
    existing.visionItems[0].state = 'current-target';
    const result = normaliseDirectionProfile(existing, northStar);
    expect(result.visionItems.find(item => item.id === 'real-choices')?.state).toBe('current-target');
    expect(result.visionItems.some(item => item.id === 'see-world')).toBe(true);
  });
});
