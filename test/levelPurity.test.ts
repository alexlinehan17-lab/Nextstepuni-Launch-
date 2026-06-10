/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Level purity (HARD RULE, user 2026-06-10): an HL exam question must NEVER
 * appear in the Ordinary-level section, and an OL question must never appear in
 * the Higher section. Concretely: a card/stem's `level` must match the level of
 * the SEC paper its question is sourced from. This guard reads the level named
 * in each entry's `source` (and `questionRef` for command-word stems) and, when
 * exactly one level is named, asserts it matches the `level` field.
 *
 * Detection is conservative — it only fires on an explicit paper-level
 * designation ("Higher Level"/"Ordinary Level", or " HL "/" OL " as in
 * "2024 HL · Q3") so it never trips on level-agnostic concept cards or content
 * words like "ordinary shares". `level: 'common'` entries are exempt (a genuine
 * single-level subject); entries naming both or neither level are skipped.
 */
import { describe, it, expect } from 'vitest';
import { RECOVERY_CARDS } from '../catchUpLaneData';
import { COMMAND_WORD_QUESTIONS } from '../commandWordData';

/** Returns 'higher' | 'ordinary' | null — the single paper level named in the text, or null if zero/both. */
function sourceLevel(text: string): 'higher' | 'ordinary' | null {
  const higher = /higher level/i.test(text) || /\bHL\b/.test(text);
  const ordinary = /ordinary level/i.test(text) || /\bOL\b/.test(text);
  if (higher && !ordinary) return 'higher';
  if (ordinary && !higher) return 'ordinary';
  return null;
}

describe('Level purity — no HL question in the OL section (and vice versa)', () => {
  it('every Catch-Up card whose source names one level has a matching level tag', () => {
    for (const c of RECOVERY_CARDS) {
      if (c.level !== 'higher' && c.level !== 'ordinary') continue;
      const named = sourceLevel(c.source);
      if (!named) continue;
      expect(named, `${c.id}: level '${c.level}' but source is ${named}-level ("${c.source.slice(0, 80)}")`).toBe(c.level);
    }
  });

  it('every Command-Word stem whose source/questionRef names one level has a matching level tag', () => {
    for (const q of COMMAND_WORD_QUESTIONS) {
      if (q.level !== 'higher' && q.level !== 'ordinary') continue;
      const named = sourceLevel(`${q.source} ${q.questionRef}`);
      if (!named) continue;
      expect(named, `${q.id}: level '${q.level}' but source/ref is ${named}-level ("${q.questionRef}")`).toBe(q.level);
    }
  });
});
