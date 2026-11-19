import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { HOSTED_ANSWER_OVERRIDES, hostedAnswersUrl, preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import sources from '../scripts/markbank/authoring/russian-reviewed-sources.json';

// Exact original filenames: EV through 2018, bilingual BV from 2019.
const repaired = [
  [2010, 'LC099ALP000EV.pdf'], [2010, 'LC099ALPA00EV.pdf'],
  [2017, 'LC099GLP000EV.pdf'], [2017, 'LC099GLPA00EV.pdf'],
  [2018, 'LC099ALP000EV.pdf'], [2018, 'LC099ALPA00EV.pdf'],
  [2019, 'LC099ALP000BV.pdf'], [2019, 'LC099ALPA00BV.pdf'],
  [2020, 'LC099ALP000BV.pdf'], [2020, 'LC099ALPA00BV.pdf'],
  [2021, 'LC099ALP000BV.pdf'], [2021, 'LC099ALPA00BV.pdf'],
] as const;

describe('reviewed Russian hosted answer-map routes', () => {
  it.each(repaired)('uses the committed original map for %i/%s', (year, fileid) => {
    const key = `russian|${year}|${fileid}`;
    expect(HOSTED_ANSWER_OVERRIDES.has(key)).toBe(true);
    expect(preferredAnswersUrl('russian', year, fileid, 'https://storage.invalid/stale-map'))
      .toBe(hostedAnswersUrl(year, fileid));
    const authored = readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/${year}/${fileid}.json`), 'utf8');
    const hosted = readFileSync(resolve(__dirname, `../public/paper-answers/${year}/${fileid}.json`), 'utf8');
    expect(hosted).toBe(authored);
    const map = JSON.parse(hosted);
    expect(map.paperFileid).toBe(fileid);
    const bound = sources.filter(source => source.year === year && source.paperFileid === fileid);
    expect(bound.length).toBeGreaterThan(0);
    const level = fileid.startsWith('LC099GL') ? 'ordinary' : 'higher';
    expect(bound.every(source => source.level === level && source.schemeFileid === map.schemeFileid)).toBe(true);
    expect(map.q.length).toBeGreaterThan(0);
  });

  it('does not route an unreviewed component through a guessed hosted map', () => {
    const storage = 'https://storage.invalid/unreviewed';
    expect(preferredAnswersUrl('russian', 2021, 'LC099ALP999BV.pdf', storage)).toBe(storage);
  });

  it('does not apply Russian map preferences to another subject', () => {
    const storage = 'https://storage.invalid/other-subject';
    expect(preferredAnswersUrl('german', 2021, 'LC099ALP000BV.pdf', storage)).toBe(storage);
  });
});
