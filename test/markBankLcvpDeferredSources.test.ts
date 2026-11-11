import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { lcvpSourceMap, reviewedLcvpSource, readLcvpDeferredScheme } from '../scripts/markbank/lcvpSources.mjs';
import { resolveIndexedPaperFileid } from '../scripts/markbank/paperIndex.mjs';
import inventory from '../scripts/markbank/authoring/lcvp/local-source-inventory-20261109.json';

// Portable contract fixtures use synthetic bytes. The explicit original-source
// CLI checks the actual PDFs; neither fixture is a published visual review.
const readFixture = (path: string) => Buffer.from(`Synthetic binding fixture: ${path}`);
const fixture = (year: number) => ({
  year, level: 'common', sitting: 'deferred', language: 'ev',
  visualSweep: { paper: 'Test fixture only', writtenScheme: 'Test fixture only' },
  manualOriginalLeaves: 1, manualPricedTasks: 1,
  sources: inventory.filter(source => source.year === year && source.kind.startsWith('deferred'))
    .map(source => ({ ...source, sha256: createHash('sha256').update(readFixture(source.path)).digest('hex') })),
  tasks: [{ id: `lcvp-${year}-cl-deferred-test`, questionRef: `${year} CL Section B Q1 — Deferred sitting` }],
});
const sourceMap = (review: ReturnType<typeof fixture>) => lcvpSourceMap(review, readFixture);

describe('LCVP deferred archive binding', () => {
  it.each([2022, 2023])('resolves the separate %i deferred pair despite identical SEC filenames', year => {
    const review = fixture(year);
    const source = sourceMap(review).get(review.tasks[0].id)!;
    expect(source.paperFileid).toBe('LC462CLP000EV-deferred.pdf');
    expect(source.schemeFileid).toBe('LC462CLP000EV-deferred.pdf');
    expect(source.schemeTextPath).toBe(`examiner-reports/lcvp/schemes/${year}-cl-deferred.md`);
    expect(resolveIndexedPaperFileid('lcvp', year, 'common', source)).toBe('LC462CLP000EV-deferred');
    const main = { ...source, paperFileid: 'LC462CLP000EV.pdf', schemeFileid: 'LC462CLP000EV.pdf' };
    expect(resolveIndexedPaperFileid('lcvp', year, 'common', main)).toBe('LC462CLP000EV');
    expect(() => resolveIndexedPaperFileid('lcvp', year, 'common', { ...source, schemeFileid: main.schemeFileid }))
      .toThrow(/No unique indexed question\/scheme pair/);
  });

  it.each(['deferredexams', 'deferredmarkingschemes'])('rejects June %s bytes with the same filename', kind => {
    const review = fixture(2022);
    const readWrongArchive = (path: string) => readFixture(path.replace(`/${kind}/`, `/${kind === 'deferredexams' ? 'exampapers' : 'markingschemes'}/`));
    expect(() => lcvpSourceMap(review, readWrongArchive)).toThrow(/bytes differ from visual review/);
  });

  it.each(['deferredexams', 'deferredmarkingschemes'])('rejects a %s path redirected into the main archive', kind => {
    const review = fixture(2022);
    review.sources.find(source => source.kind === kind)!.path = `paper-trail-corpus/exampapers/2022/LC462CLP000EV.pdf`;
    expect(() => sourceMap(review)).toThrow(/archive identity/);
  });

  it('rejects wrong years, levels, languages, incomplete visual census and duplicate tasks', () => {
    const mutations: Array<(review: ReturnType<typeof fixture>) => void> = [
      review => { review.year = 2023; },
      review => { review.level = 'higher'; },
      review => { review.sitting = 'main'; },
      review => { review.language = 'iv'; },
      review => { review.visualSweep.paper = ''; },
      review => { review.visualSweep.writtenScheme = ''; },
      review => { review.manualOriginalLeaves = 0; },
      review => { review.manualPricedTasks = 2; },
      review => { review.sources.push(review.sources[0]); },
      review => { review.sources[0].year = 2023; },
      review => { review.tasks[0].id = 'lcvp-2022-cl-main-test'; },
      review => { review.tasks[0].questionRef = '2022 CL Section B Q1'; },
      review => { review.tasks.push(review.tasks[0]); review.manualPricedTasks = 2; },
    ];
    for (const mutate of mutations) {
      const review = fixture(2022); mutate(review);
      expect(() => sourceMap(review)).toThrow();
    }
  });

  it('does not bind unreviewed deferred IDs or disturb current main cards', () => {
    expect(reviewedLcvpSource('lcvp-2022-cl-a1')).toBeUndefined();
    expect(() => reviewedLcvpSource('lcvp-2099-cl-deferred-a1')).toThrow(/lacks reviewed sources/);
    expect(() => reviewedLcvpSource('lcvp-2022-hl-deferred-a1')).toThrow(/Invalid deferred LCVP identity/);
  });

  it('rejects deferred citations on main IDs and inconsistent card year, level or citation', () => {
    const card = { id: 'lcvp-2022-cl-deferred-test', year: 2022, level: 'common', questionRef: '2022 CL Section B Q1 — Deferred sitting' };
    expect(() => reviewedLcvpSource({ ...card, id: 'lcvp-2022-cl-test' })).toThrow(/lacks a deferred identity/);
    for (const mutation of [{ year: 2023 }, { level: 'higher' }, { questionRef: '2022 CL Section B Q1' }]) {
      expect(() => reviewedLcvpSource({ ...card, ...mutation })).toThrow(/metadata differs/);
    }
  });

  it('reads only the separate deferred transcript and fails when it is absent or empty', () => {
    const review = fixture(2022);
    const source = sourceMap(review).get(review.tasks[0].id)!;
    const paths: string[] = [];
    expect(readLcvpDeferredScheme(source, (path: string) => { paths.push(path); return 'Deferred scheme fixture'; }))
      .toBe('Deferred scheme fixture');
    expect(paths).toEqual(['examiner-reports/lcvp/schemes/2022-cl-deferred.md']);
    expect(() => readLcvpDeferredScheme(source, () => { throw new Error('ENOENT'); })).toThrow(/Missing deferred LCVP/);
    expect(() => readLcvpDeferredScheme(source, () => ' \n')).toThrow(/Empty deferred LCVP/);
    expect(() => readLcvpDeferredScheme({ ...source, schemeTextPath: 'examiner-reports/lcvp/schemes/2022-cl.md' }))
      .toThrow(/transcript identity/);
  });
});
