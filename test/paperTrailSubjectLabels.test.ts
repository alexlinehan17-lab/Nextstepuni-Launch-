import { describe, expect, it } from 'vitest';

import {
  paperTrailSubjectLabel,
  paperTrailSubjectMatchesProfileCycle,
  paperTrailSubjectVisibleForProfile,
} from '../components/PaperTrail';
import { PAPER_TRAIL_SUBJECTS } from '../paperTrailData';

describe('Paper Trail subject labels', () => {
  it('keeps syllabus qualifiers when stripping them would create duplicate choices', () => {
    const history = PAPER_TRAIL_SUBJECTS.filter(subject => subject.cycle === 'lc' && subject.name.startsWith('History'));
    expect(history.map(paperTrailSubjectLabel)).toEqual(['History', 'History (Early Modern)']);
  });

  it('keeps the concise label for an unambiguous subject', () => {
    const science = PAPER_TRAIL_SUBJECTS.find(subject => subject.name === 'Science');
    expect(science && paperTrailSubjectLabel(science)).toBe('Science');
  });

  it('does not pull a same-named LCA subject into a Leaving Cert profile', () => {
    const technology = PAPER_TRAIL_SUBJECTS.filter(subject => (
      subject.id === 'technology' || subject.id === 'lca-technology'
    ));
    expect(technology.map(subject => `${subject.id}|${subject.cycle}`).sort()).toEqual([
      'lca-technology|lca',
      'technology|lc',
    ]);
    expect(technology.filter(subject => (
      paperTrailSubjectVisibleForProfile(subject, false, false)
      && paperTrailSubjectMatchesProfileCycle(subject, false, false)
    )).map(subject => subject.id)).toEqual(['technology']);
    expect(technology.filter(subject => (
      paperTrailSubjectVisibleForProfile(subject, false, true)
      && paperTrailSubjectMatchesProfileCycle(subject, false, true)
    )).map(subject => subject.id)).toEqual(['lca-technology']);
  });
});
