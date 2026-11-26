/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A tap on a phone fires :hover and the look stays behind. Every hand-written
 * :hover rule is guarded by the same media query Tailwind's
 * future.hoverOnlyWhenSupported uses (design/postcss-hover-only.js).
 */
import postcss from 'postcss';
import { describe, expect, it } from 'vitest';
import hoverOnlyWhenSupported, { HOVER_QUERY } from '../design/postcss-hover-only.js';

/** PostCSS keeps the source's own spacing; compare the rules, not the spaces round the braces. */
const squash = (css: string) => css.replace(/\s*([{};])\s*/g, '$1').replace(/;}/g, '}').trim();
const run = (css: string) => squash(postcss([hoverOnlyWhenSupported()]).process(css, { from: undefined }).css);

describe('hover looks only where hover exists', () => {
  it('uses the media query Tailwind uses for hoverOnlyWhenSupported', () => {
    expect(HOVER_QUERY).toBe('(hover: hover) and (pointer: fine)');
  });

  it('wraps a hover rule in the hover media query', () => {
    expect(run('.a:hover { color: red; }')).toBe(`@media ${HOVER_QUERY}{.a:hover{color: red}}`);
  });

  it('splits a selector list so the non-hover half still applies everywhere', () => {
    expect(run('.a:hover, .a:focus-visible { color: red; }'))
      .toBe(`.a:focus-visible{color: red}@media ${HOVER_QUERY}{.a:hover{color: red}}`);
  });

  it('keeps the rule inside the media query it was already in', () => {
    expect(run('@media (max-width: 700px) { .a:hover { color: red; } }'))
      .toBe(`@media (max-width: 700px){@media ${HOVER_QUERY}{.a:hover{color: red}}}`);
  });

  it('leaves guarded rules, keyframes and rules without :hover alone', () => {
    expect(run('@media (hover: hover) { .a:hover { color: red; } }')).toBe('@media (hover: hover){.a:hover{color: red}}');
    expect(run('.a:focus { color: red; }')).toBe('.a:focus{color: red}');
    expect(run('@keyframes k { from { opacity: 0; } to { opacity: 1; } }')).toBe('@keyframes k{from{opacity: 0}to{opacity: 1}}');
  });
});
