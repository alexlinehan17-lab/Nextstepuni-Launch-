import { describe, expect, it } from 'vitest';
import { CAREERS } from '../careerPathsData';
import { buildPossibilities, scoreCareer } from '../components/possibleLifeModel';

describe('possible life model', () => {
  it('returns three unique, deliberately varied possibilities', () => {
    const possibilities = buildPossibilities(['creative', 'social', 'flexible']);
    expect(possibilities).toHaveLength(3);
    expect(new Set(possibilities.map((career) => career.id)).size).toBe(3);
    expect(new Set(possibilities.map((career) => career.field)).size).toBeGreaterThan(1);
  });

  it('keeps a Future Finder match in the set without turning it into a ranking', () => {
    const matched = CAREERS.at(-1)!;
    const possibilities = buildPossibilities(['secure', 'useful', 'challenging'], [matched.id]);
    expect(possibilities.some((career) => career.id === matched.id)).toBe(true);
  });

  it('scores relevant priority signals deterministically', () => {
    const career = CAREERS[0];
    expect(scoreCareer(career, ['social', 'useful'])).toBe(scoreCareer(career, ['social', 'useful']));
  });
});
