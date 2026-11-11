#!/usr/bin/env node
/** Explicit original-PDF gate; the portable runtime suite never needs a corpus.
 * This only verifies archive identity, not a visual review or authored answers. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { lcvpSourceMap } from '../lcvpSources.mjs';
import { resolveIndexedPaperFileid } from '../paperIndex.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const inventory = JSON.parse(readFileSync(resolve(root, 'scripts/markbank/authoring/lcvp/local-source-inventory-20261109.json'), 'utf8'));
const proof = [];
for (const year of [2022, 2023]) {
  // An in-memory binding probe, never persisted as an authoring/source review.
  const review = {
    year, level: 'common', sitting: 'deferred', language: 'ev',
    visualSweep: { paper: 'Binding probe only', writtenScheme: 'Binding probe only' },
    manualOriginalLeaves: 1, manualPricedTasks: 1,
    sources: inventory.filter(source => source.year === year && source.kind.startsWith('deferred')),
    tasks: [{ id: `lcvp-${year}-cl-deferred-binding-probe`, questionRef: `${year} binding probe — Deferred sitting` }],
  };
  const source = lcvpSourceMap(review).get(review.tasks[0].id);
  assert.equal(resolveIndexedPaperFileid('lcvp', year, 'common', source), 'LC462CLP000EV-deferred');
  for (const kind of ['deferredexams', 'deferredmarkingschemes']) {
    const readJune = path => readFileSync(resolve(root, path.replace(`/${kind}/`, `/${kind === 'deferredexams' ? 'exampapers' : 'markingschemes'}/`)));
    assert.throws(() => lcvpSourceMap(review, readJune), /bytes differ from visual review/);
  }
  assert.throws(() => resolveIndexedPaperFileid('lcvp', year, 'common', { ...source, schemeFileid: 'LC462CLP000EV.pdf' }), /No unique indexed question\/scheme pair/);
  proof.push({ year, sources: review.sources.map(({ kind, path, sha256 }) => ({ kind, path, sha256 })), separatePairResolved: true, bothJuneSubstitutionsRejected: true, mixedPairRejected: true });
}
process.stdout.write(JSON.stringify({ passed: true, scope: 'Archive binding only; no visual-review, task-coverage or completion claim', proof }, null, 2) + '\n');
