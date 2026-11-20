/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Mark Bank's "In the Topic Atlas" line (single model, M4): it opens the card's Atlas question under the card's
 * heading, and names the printed question only when the Atlas number is a printed one. Agricultural Science's Atlas
 * numbers each part 1001, 1002…, which must never reach a student as "Question 1004".
 */
import { beforeAll, describe, expect, it } from 'vitest';
import { atlasLinkForCard, loadAtlasModel } from '../components/PaperTrail/atlasModel';

beforeAll(() => Promise.all([loadAtlasModel('biology'), loadAtlasModel('agricultural-science')]));

describe('atlasLinkForCard', () => {
  it('names a printed question number and opens its Atlas question', () => {
    const link = atlasLinkForCard('bio-2024-hl-q1-a')!;
    expect(link.question).toBe('2024 Higher Question 1');
    const params = new URL(link.href, 'https://example.test').searchParams;
    expect(params.get('subject')).toBe('biology');
    expect(params.get('topic')).toBe(link.heading.id);
    expect(params.get('q')).toBe('1');
  });

  it('does not name an Atlas-only number as a printed question', () => {
    const link = atlasLinkForCard('agsci-2026-hl-q2aii')!;
    expect(link.question).toBe('2026 Higher');
    expect(new URL(link.href, 'https://example.test').searchParams.get('q')).toBe('1004');
  });
});
