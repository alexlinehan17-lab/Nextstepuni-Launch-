/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Registration is the one screen every student must get through, and a wrong
 * join code gives them no diagnostic beyond "that code is not correct" — six
 * of which locks them out for fifteen minutes. So the matching rule has to
 * accept everything a student can plausibly type from a printed handout.
 */
import { describe, expect, test } from 'vitest';

import { SCHOOL_JOIN_CODES, normaliseJoinCode } from '@/functions/src/schoolJoinPolicy';

const matches = (typed: string, school: string) =>
  normaliseJoinCode(typed) === normaliseJoinCode(SCHOOL_JOIN_CODES[school]);

describe('school join codes', () => {
  test('every school in the picker has a code', () => {
    expect(Object.keys(SCHOOL_JOIN_CODES).sort()).toEqual(
      ['joeys', 'larkin', 'marino', 'mountcarmel', 'oconnells', 'pwc', 'rosmini'],
    );
  });

  test('the shipped codes are plain alphanumeric', () => {
    for (const [school, code] of Object.entries(SCHOOL_JOIN_CODES)) {
      expect(code, `${school} code must survive a phone keyboard`).toMatch(/^[A-Za-z0-9]+$/);
    }
  });

  test('accepts the curly apostrophe a phone substitutes', () => {
    // The bug: iOS/Android smart punctuation types ’ where the code held '.
    expect(matches("Joey’s02", 'joeys')).toBe(true);
    expect(matches("Joey's02", 'joeys')).toBe(true);
    expect(matches("O’Connell’s04", 'oconnells')).toBe(true);
    expect(matches("O'Connell's04", 'oconnells')).toBe(true);
  });

  test('accepts spacing a student cannot see', () => {
    expect(matches('Mount Carmel05', 'mountcarmel')).toBe(true);
    expect(matches('MountCarmel05', 'mountcarmel')).toBe(true);
    expect(matches('  mount  carmel 05 ', 'mountcarmel')).toBe(true);
  });

  test('accepts any casing', () => {
    expect(matches('MARINO01', 'marino')).toBe(true);
    expect(matches('marino01', 'marino')).toBe(true);
    expect(matches('pwc07', 'pwc')).toBe(true);
  });

  test('no student is stranded by the reissue — old handouts still work', () => {
    // The codes previously printed for schools, typed exactly as published.
    const PREVIOUSLY_PUBLISHED: Record<string, string> = {
      marino: 'Marino01',
      joeys: "Joey's02",
      larkin: 'Larkin03',
      oconnells: "O'Connell's04",
      mountcarmel: 'Mount Carmel05',
      rosmini: 'Rosmini06',
      pwc: 'PwC07',
    };
    for (const [school, oldCode] of Object.entries(PREVIOUSLY_PUBLISHED)) {
      expect(matches(oldCode, school), `${school}'s old printed code must still work`).toBe(true);
    }
  });

  test('still rejects a genuinely wrong code', () => {
    expect(matches('Marino02', 'marino')).toBe(false);
    expect(matches('Larkin03', 'marino')).toBe(false);
    expect(matches('', 'marino')).toBe(false);
    // Punctuation is folded away, not treated as a wildcard.
    expect(matches('!!!!', 'marino')).toBe(false);
  });

  test('no two schools share a code', () => {
    const folded = Object.values(SCHOOL_JOIN_CODES).map(normaliseJoinCode);
    expect(new Set(folded).size).toBe(folded.length);
  });
});
