import { describe, expect, it } from 'vitest';

import { builtDecks, levelsForSubject, loadCards } from '../components/MarkBank/deck';
import { readChoice, writeChoice } from '../components/MarkBank/store';
import { profileDeckChoice } from '../components/MarkBank/MarkBank';

describe('Mark Bank profile defaults', () => {
  it('opens on the first supported subject and saved level in the student profile', () => {
    expect(profileDeckChoice([
      { subjectName: 'English', level: 'higher' },
      { subjectName: 'Chemistry', level: 'ordinary' },
    ])).toEqual({ subjectId: 'english', level: 'higher' });
  });

  it('opens and remembers Foundation Mathematics without offering that level on other subjects', async () => {
    expect(profileDeckChoice([{ subjectName: 'Mathematics', level: 'Foundation' }]))
      .toEqual({ subjectId: 'maths', level: 'foundation' });
    expect(levelsForSubject('maths')).toEqual(['higher', 'ordinary', 'foundation']);
    expect(levelsForSubject('biology')).toEqual(['higher', 'ordinary']);
    expect(builtDecks()).toContainEqual({ subjectId: 'maths', level: 'foundation', label: 'Mathematics Foundation' });
    expect(await loadCards('maths', 'foundation')).toHaveLength(326);
    writeChoice('foundation-default-test', { subjectId: 'maths', level: 'foundation' });
    expect(readChoice('foundation-default-test')).toEqual({ subjectId: 'maths', level: 'foundation' });
    localStorage.removeItem('mb:choice:foundation-default-test');
  });

  it('understands common profile aliases and newly available decks', () => {
    expect(profileDeckChoice([{ subjectName: 'Maths', level: 'Higher' }]))
      .toEqual({ subjectId: 'maths', level: 'higher' });
    expect(profileDeckChoice([{ subjectName: 'English', level: 'Higher' }]))
      .toEqual({ subjectId: 'english', level: 'higher' });
  });
});
