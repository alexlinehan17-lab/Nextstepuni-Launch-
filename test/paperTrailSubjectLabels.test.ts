import { describe, expect, it } from 'vitest';

import { paperTrailSubjectLabel } from '../components/PaperTrail';
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
});
