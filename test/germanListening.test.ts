/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * German listening cards (scripts/markbank/authoring/de_listen.py): every one
 * carries its own year's SEC recording, and the one answer the scheme prices
 * in components with a priced alternative under it pays as the scheme says.
 */

import { describe, expect, it } from 'vitest';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '../components/MarkBank/cards/german/ordinary';
import recordings from '../data/germanAudio.json';
import { isPointCard, optionGroupMarks, type SecCard } from '../types/markBank';

const listening = [...GERMAN_HIGHER, ...GERMAN_ORDINARY].filter(card => /^L[1-4]$/.test(card.section));

describe('German listening cards', () => {
  it('carry the SEC recording of their own year', () => {
    const wrong = listening.filter((card: SecCard) => {
      const recording = recordings.find(r => r.year === card.year);
      return !recording || card.audioMaterial?.playbackUrl !== recording.source.playbackUrl;
    }).map(card => card.id);
    expect(listening.length).toBeGreaterThan(0);
    expect(wrong).toEqual([]);
  });

  it('pays "allow: in summer (1 mark only)" in place of the month, never beside it', () => {
    // 2025 Ordinary L4 Q1(i): "21st (1) to 29th (1) June (2 marks)" over
    // "allow: in summer (1 mark only)", the ask worth 4.
    const card = listening.find(c => c.id === 'de-2025-ol-l4-1-i');
    expect(card && isPointCard(card)).toBe(true);
    if (!card || !isPointCard(card)) return;
    const group = card.rows[0].group!;
    expect(group.options).toEqual(['21st', 'to 29th', 'June', 'in summer']);
    const g = { claimMax: group.claimMax, optionMarks: group.optionMarks!, optionOf: group.optionOf };
    expect(optionGroupMarks(g, [3])).toBe(1);
    expect(optionGroupMarks(g, [0, 1])).toBe(2);
    expect(optionGroupMarks(g, [2, 3])).toBe(2);
    expect(optionGroupMarks(g, [0, 1, 2, 3])).toBe(card.totalMarks);
    expect(card.totalMarks).toBe(4);
  });
});
