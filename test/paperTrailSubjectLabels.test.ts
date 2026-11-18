import { describe, expect, it } from 'vitest';

import {
  paperTrailSubjectLabel,
  paperTrailSubjectMatchesStudentName,
  paperTrailSubjectMatchesProfileCycle,
  paperTrailSubjectVisibleForProfile,
} from '../components/PaperTrail';
import { PAPER_TRAIL_SUBJECTS, PAPER_TRAIL_INDEX } from '../paperTrailData';

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


describe('LCA Leaving Cert Maths paper links', () => {
  it('matches the chosen Maths course to its LC papers without pulling in LC French', () => {
    const names = ['Leaving Cert Maths', 'French', 'Mathematical Applications'];
    const mine = PAPER_TRAIL_SUBJECTS.filter(subject =>
      paperTrailSubjectMatchesProfileCycle(subject, false, true, names) &&
      names.some(name => paperTrailSubjectMatchesStudentName(subject, name)));
    expect(mine.map(subject => subject.id)).toContain('mathematics');
    expect(mine.map(subject => subject.id)).toContain('lca-french');
    expect(mine.map(subject => subject.id)).not.toContain('french');
    const maths = PAPER_TRAIL_SUBJECTS.find(subject => subject.id === 'mathematics')!;
    expect(paperTrailSubjectMatchesProfileCycle(maths, false, true, ['French'])).toBe(false);
    expect(paperTrailSubjectMatchesProfileCycle(maths, true, false, names)).toBe(false);
    for (const level of ['higher', 'ordinary', 'foundation']) {
      expect(maths.levels).toContain(level);
      expect(PAPER_TRAIL_INDEX.mathematics.some(entry => entry.level === level && entry.papers.length > 0)).toBe(true);
    }
  });
});
