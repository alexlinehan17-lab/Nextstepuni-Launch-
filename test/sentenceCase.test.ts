/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, it } from 'vitest';
import { sentenceCase } from '@/utils/sentenceCase';

describe('sentenceCase', () => {
  it('turns the six reasons into the agreed board’s words', () => {
    expect(['My Own Path', 'For My People', 'A Career I Love', 'Keep Learning', 'Prove Them Wrong', 'Keep My Options Open'].map(sentenceCase))
      .toEqual(['My own path', 'For my people', 'A career I love', 'Keep learning', 'Prove them wrong', 'Keep my options open']);
  });
  it('leaves words already in sentence case, "I" and acronyms alone', () => {
    expect(sentenceCase('Find your direction')).toBe('Find your direction');
    expect(sentenceCase('Show what I can do')).toBe('Show what I can do');
    expect(sentenceCase('Get Into A CAO Course')).toBe('Get into a CAO course');
    expect(sentenceCase('What I’m Into')).toBe('What I’m into');
  });
});
