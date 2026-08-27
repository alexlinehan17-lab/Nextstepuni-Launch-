/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Timetable subject chips carry one ink — white — on a deepened version of the
 * subject's own colour. Two properties have to hold together, and they pull
 * against each other: every fill must be dark enough for white text (or the
 * label is unreadable), and the fills must stay far enough apart (or the chip
 * stops identifying the subject at a glance, which is its whole job).
 *
 * These drive off the component's real SUBJECT_HEX export rather than a copy,
 * so recolouring or adding a subject is covered automatically.
 */
import { describe, expect, it } from 'vitest';

import { subjectFill, SUBJECT_HEX } from '@/components/SpacedRepetitionTimetable';

const AA = 4.5;

function contrastWithWhite(hex: string): number {
  const lin = (v: number) => (v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
  const [r, g, b] = [1, 3, 5].map(i => lin(parseInt(hex.slice(i, i + 2), 16) / 255));
  return 1.05 / (0.2126 * r + 0.7152 * g + 0.0722 * b + 0.05);
}

function rgb(hex: string): [number, number, number] {
  return [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16)) as [number, number, number];
}

function rgbDistance(a: string, b: string): number {
  const [r1, g1, b1] = rgb(a), [r2, g2, b2] = rgb(b);
  return Math.hypot(r1 - r2, g1 - g2, b1 - b2);
}

function hue(hex: string): number {
  const [r, g, b] = rgb(hex).map(v => v / 255);
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  if (max === min) return -1;
  const d = max - min;
  const h = max === r ? ((g - b) / d + (g < b ? 6 : 0))
    : max === g ? (b - r) / d + 2
      : (r - g) / d + 4;
  return (h / 6) * 360;
}

const PALETTE = Object.entries(SUBJECT_HEX);

describe('subjectFill', () => {
  it('covers the whole palette', () => {
    // Guards the guard: if SUBJECT_HEX stopped being exported or came back
    // empty, every assertion below would vacuously pass.
    expect(PALETTE.length).toBeGreaterThan(25);
  });

  it('makes white text clear AA on every subject', () => {
    const failures = PALETTE
      .map(([name, raw]) => [name, subjectFill(raw)] as const)
      .filter(([, fill]) => contrastWithWhite(fill) < AA)
      .map(([name, fill]) => `${name}: ${fill} at ${contrastWithWhite(fill).toFixed(2)}:1`);
    expect(failures).toEqual([]);
  });

  it('keeps subjects visually distinct from one another', () => {
    // The regression this guards: deepening every subject to the SAME contrast
    // lands them all on one luminance, collapsing pairs that differed only in
    // lightness (Japanese/Music came out 4 RGB units apart under a flat target).
    // 12 is below the palette's own tightest pair (the greys, ~7.5 raw) scaled
    // for the deepening, and well above the collapse a flat target produced.
    const tooClose: string[] = [];
    for (let i = 0; i < PALETTE.length; i++) {
      for (let j = i + 1; j < PALETTE.length; j++) {
        const [nameA, rawA] = PALETTE[i], [nameB, rawB] = PALETTE[j];
        if (rawA === rawB) continue; // genuinely share a colour in the palette
        const before = rgbDistance(rawA, rawB);
        const after = rgbDistance(subjectFill(rawA), subjectFill(rawB));
        // Only a pair the deepening pushed together is a regression; pairs that
        // were already close in the source palette are not this function's doing.
        if (after < 12 && after < before) tooClose.push(`${nameA}/${nameB}: ${before.toFixed(0)} -> ${after.toFixed(0)}`);
      }
    }
    expect(tooClose).toEqual([]);
  });

  it('preserves the hue, so a subject stays its own colour', () => {
    const drifted = PALETTE
      .filter(([, raw]) => hue(raw) !== -1)
      .map(([name, raw]) => [name, Math.abs(hue(subjectFill(raw)) - hue(raw))] as const)
      .filter(([, delta]) => delta > 8)
      .map(([name, delta]) => `${name}: ${delta.toFixed(1)}°`);
    expect(drifted).toEqual([]);
  });

  it('leaves a colour that already meets its target untouched', () => {
    // Technology is the darkest blue in the palette and already clears AA.
    expect(subjectFill('#2563eb')).toBe('#2563eb');
  });

  it('actually darkens the light subjects rather than passing them through', () => {
    // The failure this catches: a subjectFill that returned its input would
    // satisfy hue-preservation and distinctness, and only this test would fail.
    expect(subjectFill('#eab308')).not.toBe('#eab308');
    expect(contrastWithWhite('#eab308')).toBeLessThan(AA);
    expect(contrastWithWhite(subjectFill('#eab308'))).toBeGreaterThanOrEqual(AA);
  });

  it('returns a valid 6-digit hex, and is stable across calls', () => {
    expect(subjectFill('#84cc16')).toMatch(/^#[0-9a-f]{6}$/i);
    expect(subjectFill('#84cc16')).toBe(subjectFill('#84cc16'));
  });

  it('terminates on the extremes without hanging', () => {
    expect(subjectFill('#000000')).toMatch(/^#[0-9a-f]{6}$/i);
    expect(contrastWithWhite(subjectFill('#ffffff'))).toBeGreaterThanOrEqual(AA);
  });
});
