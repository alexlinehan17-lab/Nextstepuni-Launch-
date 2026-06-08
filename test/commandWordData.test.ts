/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards Command-Word Reflex stems: the command word must be tappable (appear as
 * a consecutive run of word-tokens in the stem — mirrors the component's
 * cmdIndices, incl. multi-word cues), the subject must be real, both levels must
 * be present, and ids unique.
 */
import { describe, it, expect } from 'vitest';
import { COMMAND_WORD_QUESTIONS } from '../commandWordData';
import { CURRICULUM } from '../curriculum';

const validSubjectIds = new Set(CURRICULUM.map((s) => s.id));
const norm = (s: string) => s.replace(/[^a-zA-Z]/g, '').toLowerCase();

/** True if the command word resolves to a consecutive run of stem word-tokens. */
function anchorResolves(stem: string, cmd: string): boolean {
  const cmdWords = cmd.toLowerCase().split(/\s+/).map((w) => w.replace(/[^a-z]/g, '')).filter(Boolean);
  if (cmdWords.length === 0) return false;
  const words = stem.split(/(\s+)/).filter((t) => !/^\s+$/.test(t)).map(norm);
  for (let p = 0; p + cmdWords.length <= words.length; p++) {
    if (cmdWords.every((w, k) => words[p + k] === w)) return true;
  }
  return false;
}

describe('Command-Word Reflex stems', () => {
  it('every command word is tappable (a token-run in its stem)', () => {
    for (const q of COMMAND_WORD_QUESTIONS) {
      expect(anchorResolves(q.stem, q.commandWord), `${q.id}: "${q.commandWord}" is not a tappable run in the stem`).toBe(true);
    }
  });

  it('every stem maps to a real curriculum subject + is well-formed', () => {
    for (const q of COMMAND_WORD_QUESTIONS) {
      expect(validSubjectIds.has(q.subjectId), `${q.id}: unknown subjectId "${q.subjectId}"`).toBe(true);
      expect(q.stem.trim() && q.demand.trim() && q.trap.trim() && q.source.trim(), `${q.id}: empty field`).toBeTruthy();
      expect(q.marks, `${q.id}: bad marks`).toBeGreaterThan(0);
    }
  });

  it('both Higher and Ordinary levels are represented', () => {
    const levels = new Set(COMMAND_WORD_QUESTIONS.map((q) => q.level));
    expect(levels.has('higher')).toBe(true);
    expect(levels.has('ordinary')).toBe(true);
  });

  it('all ids are unique', () => {
    const ids = COMMAND_WORD_QUESTIONS.map((q) => q.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});
