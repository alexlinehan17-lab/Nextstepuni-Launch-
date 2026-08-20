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

const src = readFileSync(resolve(__dirname, '..', 'components/worldPalette.ts'), 'utf8');

const worlds = [...src.matchAll(
  /'([a-z-]+)':\s*\{[^}]*?mid: '(#[0-9a-fA-F]{6})',(?:\s*midText: '(#[0-9a-fA-F]{6})',)?[^}]*?deep: '(#[0-9a-fA-F]{6})',\s*deepDark: '(#[0-9a-fA-F]{6})'/g,
)].map(m => ({ key: m[1], mid: m[2], midText: m[3], deep: m[4], deepDark: m[5] }));

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

/* The RAISED card, not the page canvas. It is the lighter of the two dark
   surfaces these tones appear on, so it is the worst case for contrast — testing
   against #18181b passed tones that then failed at 4.49:1 on this one. */
const DARK_CARD = '#202020';

describe('module world ink', () => {
  it('finds all five worlds', () => {
    expect(worlds.map(w => w.key)).toEqual([
      'architecture-mindset', 'science-growth', 'learning-cheat-codes',
      'subject-specific-science', 'exam-zone',
    ]);
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
      const tone = w.midText ?? w.mid;
      const r = ratio(tone, DARK_CARD);
      expect(r, `${w.key} mid tone is ${r.toFixed(2)}:1`).toBeGreaterThanOrEqual(4.5);
    }
  });


  it('keeps the saturated mid for fills, so white labels on it are unchanged', () => {
    // midText is a TEXT swap only. Lightening the fill while the button label
    // stays white took those buttons from 3.6:1 to 2.4:1.
    const palette = readFileSync(resolve(__dirname, '..', 'components/worldPalette.ts'), 'utf8');
    expect(palette).toMatch(/midText: \(t: Pick<WorldTones, 'mid' \| 'midText'>\)/);
    expect(palette).not.toContain('mid: (t:');
  });


  it('inverts the world CTA in dark instead of darkening it', () => {
    // Darkening the fill to `deep` gives the label 7-11:1 but leaves the button
    // only 1.4-2.2:1 clear of the card behind it, so it reads as a tinted hole
    // rather than a raised action. The pale tone sits ~11:1 clear of the card.
    const palette = readFileSync(resolve(__dirname, '..', 'components/worldPalette.ts'), 'utf8');
    expect(palette).toContain("background: t.deepDark, color: 'var(--ink-on-accent)'");
    expect(palette).toContain('background: t.mid');

    const CARD_L = '#FFFFFF';
    for (const w of worlds) {
      // Light is untouched: the saturated mid with a white label.
      expect(ratio(w.mid, CARD_L)).toBeGreaterThan(1.5);
      // Dark: the pale fill must clear the card AND take dark ink.
      expect(ratio(w.deepDark, DARK_CARD),
        `${w.key} CTA fill only ${ratio(w.deepDark, DARK_CARD).toFixed(2)}:1 from the card`).toBeGreaterThanOrEqual(4.5);
      expect(ratio('#1A1A1A', w.deepDark),
        `${w.key} CTA label only ${ratio('#1A1A1A', w.deepDark).toFixed(2)}:1`).toBeGreaterThanOrEqual(4.5);
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
      'architecture-mindset': '#1e3a5f', 'science-growth': '#7c4a14',
      'learning-cheat-codes': '#115e4f', 'subject-specific-science': '#8a2860',
      'exam-zone': '#7f1d1d',
    };
    for (const w of worlds) expect(w.deep).toBe(authored[w.key]);
  });
  it('is the only copy of the palette', () => {
    // It lived in ModulesView and ModuleShowcase at once, and fixing one left
    // every module title on the category screen at about 1.2:1.
    const others = ['components/ModulesView.tsx', 'components/ModuleShowcase.tsx']
      .filter(f => /#1e3a5f|#115e4f|#8a2860/.test(
        readFileSync(resolve(__dirname, '..', f), 'utf8')));
    expect(others, `world hexes duplicated in: ${others.join(', ')}`).toEqual([]);
  });
});
