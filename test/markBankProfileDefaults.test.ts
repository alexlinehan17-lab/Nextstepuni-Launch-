import { describe, expect, it } from 'vitest';

import { profileDeckChoice } from '../components/MarkBank/MarkBank';

describe('Mark Bank profile defaults', () => {
  it('opens on the first supported subject and saved level in the student profile', () => {
    expect(profileDeckChoice([
      { subjectName: 'English', level: 'higher' },
      { subjectName: 'Chemistry', level: 'ordinary' },
    ])).toEqual({ subjectId: 'chemistry', level: 'ordinary' });
  });

  it('understands common profile aliases without inventing an unavailable deck', () => {
    expect(profileDeckChoice([{ subjectName: 'Maths', level: 'Higher' }]))
      .toEqual({ subjectId: 'maths', level: 'higher' });
    expect(profileDeckChoice([{ subjectName: 'English', level: 'Higher' }])).toBeNull();
  });
});

