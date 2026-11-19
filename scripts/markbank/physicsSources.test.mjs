import assert from 'node:assert/strict';
import test from 'node:test';
import { existsSync, readFileSync } from 'node:fs';
import { reviewedPhysicsSourceMetadata, physicsSourceMap } from './physicsSources.mjs';

test('same-year main and deferred cards cannot resolve to the same source', () => {
  assert.equal(reviewedPhysicsSourceMetadata('phys-2022-hl-q12-b-ii'), undefined);
  assert.deepEqual(reviewedPhysicsSourceMetadata('phys-2022-hl-deferred-q12-b-ii'), {
    sitting: 'deferred', lang: 'ev', paperFileid: 'LC021ALP000EV-deferred.pdf',
    schemeFileid: 'LC021ALP000EV-deferred.pdf',
  });
});

test('unreviewed deferred tasks fail instead of falling back to a main Q number', () => {
  assert.throws(() => reviewedPhysicsSourceMetadata('phys-2022-hl-deferred-missing'), /lacks reviewed sources/);
  assert.throws(() => reviewedPhysicsSourceMetadata('phys-2022-ol-deferred-q1-i'), /lacks reviewed sources/);
});

const audit = JSON.parse(readFileSync(new URL('./authored/physics-review-audit.json', import.meta.url)));
const reviews = Object.values(audit.sittings).filter(review => review.sitting === 'deferred');
test('all available deferred Physics original bytes match their reviewed hashes', {
  skip: !reviews.every(review => Object.values(review.sources).every(source => existsSync(source.path))),
}, () => {
  assert.equal(physicsSourceMap(audit).size, reviews.reduce((sum, review) => sum + review.tasks.length, 0));
});
