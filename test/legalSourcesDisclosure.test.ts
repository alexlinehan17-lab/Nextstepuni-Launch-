/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Google Play rejected NextStepUni in August 2026 under the Misleading Claims
 * policy: the app carries information published by Irish public bodies (SEC
 * marking schemes and Chief Examiner reports, CAO/SUSI/HEA guidance) and the
 * listing had neither links to those original sources nor a statement that the
 * app does not represent a government entity.
 *
 * These are the two things the reviewer looked for. Losing either one from the
 * legal copy would re-trigger the rejection, and nothing else in the suite
 * would notice, so they are pinned here.
 */
import { describe, it, expect } from 'vitest';
import { TERMS_OF_USE, LEGAL_URL_RE } from '../components/legal/legalContent';

const terms = TERMS_OF_USE.flatMap(s => s.body).join('\n');

describe('government-information disclosure (Google Play Misleading Claims)', () => {
  it('states plainly that the app does not represent a government entity', () => {
    expect(terms).toMatch(/not affiliated with, endorsed by, or acting on behalf of/i);
    expect(terms).toMatch(/State Examinations Commission/);
    expect(terms).toMatch(/any other government body or public agency/i);
  });

  it('links the original source for every public body whose material it carries', () => {
    for (const host of [
      'https://www.examinations.ie',   // SEC — papers, marking schemes, CE reports
      'https://www.cao.ie',            // CAO — applications, points, deadlines
      'https://www.susi.ie',           // SUSI — student grants
      'https://hea.ie',                // HEA — higher education data
      'https://www.qualifax.ie',       // Qualifax — national course database
      'https://www.citizensinformation.ie',
      'https://www.gov.ie',
    ]) {
      expect(terms).toContain(host);
    }
  });

  it('writes those sources as bare URLs, so both renderers can linkify them', () => {
    LEGAL_URL_RE.lastIndex = 0;
    const found = terms.match(LEGAL_URL_RE) ?? [];
    expect(found.length).toBeGreaterThanOrEqual(7);
    // Trailing punctuation would break the href the renderers build.
    for (const url of found) expect(url).not.toMatch(/[.,)]$/);
  });

  it('keeps the pattern stateless between callers', () => {
    // Global regexes carry lastIndex. Both renderers reset it before use; if a
    // future edit drops that reset, alternating calls start missing matches.
    LEGAL_URL_RE.lastIndex = 0;
    const first = 'see https://www.cao.ie today'.match(LEGAL_URL_RE);
    LEGAL_URL_RE.lastIndex = 0;
    const second = 'see https://www.cao.ie today'.match(LEGAL_URL_RE);
    expect(first).toEqual(second);
  });
});
