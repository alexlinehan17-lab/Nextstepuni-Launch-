import { describe, expect, it } from 'vitest';
import { suggestEmailCorrection } from '../utils/emailTypo';

describe('suggestEmailCorrection', () => {
  it.each([
    // Typos seen on real NextStepUni signups.
    ['aoife@marinocollge.ie', 'aoife@marinocollege.ie'],
    ['aoife@gmail.comdeedw', 'aoife@gmail.com'],
    // Common slips.
    ['aoife@gmial.com', 'aoife@gmail.com'],
    ['aoife@gmail.co', 'aoife@gmail.com'],
    ['aoife@gmail.con', 'aoife@gmail.com'],
    ['aoife@gmailcom', 'aoife@gmail.com'],
    ['aoife@gmail.com.', 'aoife@gmail.com'],
    ['aoife@hotmial.com', 'aoife@hotmail.com'],
    ['aoife@outlok.ie', 'aoife@outlook.ie'],
    ['aoife@icloud.co', 'aoife@icloud.com'],
    ['aoife@oconnelschool.ie', 'aoife@oconnellschool.ie'],
    ['aoife@marinocolege.ei', 'aoife@marinocollege.ie'],
  ])('suggests a fix for %s', (typed, expected) => {
    expect(suggestEmailCorrection(typed)).toBe(expected);
  });

  it.each([
    'aoife@gmail.com',
    'aoife@marinocollege.ie',
    'aoife@hotmail.co.uk',
    'aoife@mail.com',
    'aoife@ymail.com',
    'aoife@me.com',
    'aoife@marino.cdetb.ie',
    'aoife@marino.ie',
    'aoife@ucc.ie',
    'aoife@example.com',
    'aoife',
    '@gmail.com',
    'aoife@g',
    '',
  ])('leaves %s alone', (typed) => {
    expect(suggestEmailCorrection(typed)).toBeNull();
  });

  it('keeps the local part exactly as typed and ignores surrounding spaces', () => {
    expect(suggestEmailCorrection('  Aoife.Byrne@GMIAL.com ')).toBe('Aoife.Byrne@gmail.com');
  });
});
