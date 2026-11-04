import { describe, expect, it } from 'vitest';
import { PERSONAL_STAR_CREW } from '@/data/personalStarCrew';
import { pickLoadingCrew, resolveLoadingCrew } from '@/utils/loadingCrew';
import { getToolLoadingLabel } from '@/utils/loadingLabels';

describe('loading crew eligibility', () => {
  it.each([undefined, 'Charlie', 'star-crew:skater'])('never draws Hugger for %s', avatar => {
    const seen = new Set(Array.from({ length: 100 }, (_, i) => pickLoadingCrew(avatar, i / 100).id));
    expect(seen).toEqual(new Set(PERSONAL_STAR_CREW.filter(crew => crew.id !== 'star-crew:hugger').map(crew => crew.id)));
  });
  it('allows the complete pool only for a person who selected Hugger', () => {
    const seen = new Set(Array.from({ length: 100 }, (_, i) => pickLoadingCrew('star-crew:hugger', i / 100).id));
    expect(seen).toEqual(new Set(PERSONAL_STAR_CREW.map(crew => crew.id)));
    expect(resolveLoadingCrew('personal', 'star-crew:hugger', 0).id).toBe('star-crew:hugger');
    expect(resolveLoadingCrew('personal', 'star-crew:reader', .99).id).toBe('star-crew:reader');
  });
  it('uses an eligible crew member for a missing or legacy personal avatar', () => {
    for (const avatar of [undefined, 'Charlie', 'star-person', 'star-crew:missing']) {
      const crew = resolveLoadingCrew('personal', avatar, .8);
      expect(crew.id).toMatch(/^star-crew:/);
      expect(crew.id).not.toBe('star-crew:hugger');
    }
  });
});

describe('nested tool loading copy', () => {
  it('uses the destination name consistently for aliases and curricula', () => {
    expect(getToolLoadingLabel('planner')).toBe('Opening your planner');
    expect(getToolLoadingLabel('cao-simulator')).toBe(getToolLoadingLabel('points-passport'));
    expect(getToolLoadingLabel('syllabus-xray')).toBe(getToolLoadingLabel('war-room'));
    expect(getToolLoadingLabel('career-paths')).toBe(getToolLoadingLabel('your-possible-life'));
    expect(getToolLoadingLabel('future-finder', 'junior')).toBe('Opening Subject Explorer');
    expect(getToolLoadingLabel('future-finder', 'senior')).toBe('Opening Future Finder');
  });
  it.each([undefined, null, 'unknown', '__proto__', 'constructor'])('does not render arbitrary URL content: %s', tool => {
    expect(getToolLoadingLabel(tool)).toBe('Opening Launchpad');
  });
});
