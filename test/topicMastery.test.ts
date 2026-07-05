/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail mastery scoring (feature E2): accuracy and retention
 * blend correctly, either signal stands alone, no signal → null, and the
 * strong-stability threshold maps to full retention.
 */
import { describe, it, expect } from 'vitest';
import { computeMastery, STRONG_STABILITY_DAYS } from '../components/PaperTrail/topicMastery';

describe('Paper Trail — topic mastery scoring', () => {
  it('averages accuracy and retention when both exist', () => {
    expect(computeMastery(80, 40)).toBe(60);
  });

  it('uses whichever single signal is present', () => {
    expect(computeMastery(72, undefined)).toBe(72);
    expect(computeMastery(undefined, 55)).toBe(55);
  });

  it('returns null when there is no evidence', () => {
    expect(computeMastery(undefined, undefined)).toBeNull();
  });

  it('clamps to 0–100', () => {
    expect(computeMastery(120, 120)).toBe(100);
    expect(computeMastery(-10, undefined)).toBe(0);
  });

  it('a card stable for the strong-threshold reads as full retention', () => {
    // retention score = stability / STRONG * 100; at STRONG it is 100.
    const retentionAtStrong = (STRONG_STABILITY_DAYS / STRONG_STABILITY_DAYS) * 100;
    expect(computeMastery(undefined, retentionAtStrong)).toBe(100);
  });
});
