/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Each module world is colour-coded, and the Modules screen draws every eyebrow,
 * counter and progress ring from that world's `deep` tone — often at 60-80%
 * alpha via a hex suffix (`${deep}AA`).
 *
 * Those tones are authored to sit on a light card. On the dark one they measured
 * between 1.54:1 and 2.31:1, so the navy, red and magenta worlds were
 * effectively unreadable. `deepDark` is the same hue raised in luminance. The
 * point is that the worlds stay *distinguishable* — flattening them all to white
 * would have been readable but would have destroyed the colour coding.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const src = readFileSync(resolve(__dirname, '..', 'components/ModulesView.tsx'), 'utf8');

const worlds = [...src.matchAll(
  /worldKey: '([a-z]+)'[\s\S]*?mid: '(#[0-9a-fA-F]{6})',(?:\s*midDark: '(#[0-9a-fA-F]{6})',)?[\s\S]*?deep: '(#[0-9a-fA-F]{6})',\s*deepDark: '(#[0-9a-fA-F]{6})',/g,
)].map(m => ({ key: m[1], mid: m[2], midDark: m[3], deep: m[4], deepDark: m[5] }));

const srgb = (hex: string) => [1, 3, 5].map(i => {
  const v = parseInt(hex.slice(i, i + 2), 16) / 255;
  return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
});
const lum = (hex: string) => { const [r, g, b] = srgb(hex); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const ratio = (a: string, b: string) => {
  const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
};
/** Flatten `hex` at `alpha` over `bg`, the way a hex-suffixed colour renders. */
const over = (hex: string, alpha: number, bg: string) => {
  const mix = (i: number) => Math.round(
    alpha * parseInt(hex.slice(i, i + 2), 16) + (1 - alpha) * parseInt(bg.slice(i, i + 2), 16),
  );
  return '#' + [1, 3, 5].map(i => mix(i).toString(16).padStart(2, '0')).join('');
};

const DARK_CARD = '#18181b';

describe('module world ink', () => {
  it('finds all five worlds', () => {
    expect(worlds.map(w => w.key)).toEqual(['mind', 'growth', 'learn', 'decode', 'exam']);
  });

  it('clears AA on the dark card even at the lowest alpha the screen uses', () => {
    // 0x99 = 60%, the faintest suffix applied to `deep` on this screen.
    for (const w of worlds) {
      const r = ratio(over(w.deepDark, 0.6, DARK_CARD), DARK_CARD);
      expect(r, `${w.key} deepDark at 60% is ${r.toFixed(2)}:1`).toBeGreaterThanOrEqual(4.5);
    }
  });

  it('clears AA for the small mono numerals', () => {
    for (const w of worlds) {
      const tone = w.midDark ?? w.mid;
      const r = ratio(tone, DARK_CARD);
      expect(r, `${w.key} mid tone is ${r.toFixed(2)}:1`).toBeGreaterThanOrEqual(4.5);
    }
  });

  it('keeps the worlds distinguishable rather than collapsing them to white', () => {
    const inks = worlds.map(w => w.deepDark);
    expect(new Set(inks).size).toBe(worlds.length);
    for (const ink of inks) {
      // Anything this close to white has lost its hue and its world identity.
      expect(ratio(ink, '#ffffff'), `${ink} is indistinguishable from white`).toBeGreaterThan(1.15);
    }
  });

  it('leaves the light-mode tones untouched', () => {
    const authored: Record<string, string> = {
      mind: '#1e3a5f', growth: '#7c4a14', learn: '#115e4f', decode: '#8a2860', exam: '#7f1d1d',
    };
    for (const w of worlds) expect(w.deep).toBe(authored[w.key]);
  });
});
