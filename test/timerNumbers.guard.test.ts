/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Timers count in the pixel-style numbers (Departure Mono).
 *
 * Alex chose the study timer "Rule" with pixel-style numbers on 24 Nov 2026.
 * A later drawing set the study room's big countdown in the plain typeface,
 * the build followed the drawing, and he caught it in the built app on 26 Nov
 * 2026: "I thought we were doing the kind of pixelated text for the study
 * timer? Why are we straying from what we chose, we shouldn't do that."
 *
 * This guard holds the choice: every rule that sets a typeface on the study
 * room's countdown, on the small timer over the app, or on the set-up
 * screen's readout must name the pixel-style face.
 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { expect, test } from 'vitest';

const read = (path: string) => readFileSync(resolve(__dirname, '..', path), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');

/** The bodies of every rule whose selector names `className` and which sets a typeface. */
function typefaceRules(css: string, className: string): string[] {
  const rules = [...css.matchAll(/([^{}]+)\{([^{}]*)\}/g)];
  return rules
    .filter(([, selector]) => new RegExp(`\\.${className}(?![\\w-])`).test(selector))
    .map(([, , body]) => body)
    .filter(body => /(^|[;\s])font(-family)?\s*:/.test(body));
}

test('the study room counts down in the pixel-style numbers', () => {
  const rules = typefaceRules(read('components/study/study-room.css'), 'ss-timer-digits');
  expect(rules.length).toBeGreaterThan(0);
  for (const body of rules) expect(body).toContain('Departure Mono');
});

test('the small timer over the app counts in the pixel-style numbers', () => {
  const rules = typefaceRules(read('components/study/study-mini-timer.css'), 'study-mini-digits');
  expect(rules.length).toBeGreaterThan(0);
  for (const body of rules) expect(body).toContain('Departure Mono');
});

test('the readout style every counter shares is the pixel-style face', () => {
  const rules = typefaceRules(read('index.css'), 't-readout');
  expect(rules.length).toBeGreaterThan(0);
  for (const body of rules) expect(body).toContain('Departure Mono');
});
