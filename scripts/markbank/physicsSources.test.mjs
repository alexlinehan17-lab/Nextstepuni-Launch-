import assert from 'node:assert/strict';
import test from 'node:test';
import { reviewedPhysicsSource } from './physicsSources.mjs';

test('same-year main and deferred cards cannot resolve to the same source', () => {
  assert.equal(reviewedPhysicsSource('phys-2022-hl-q12-b-ii'), undefined);
  assert.deepEqual(reviewedPhysicsSource('phys-2022-hl-deferred-q12-b-ii'), {
    sitting: 'deferred', lang: 'ev', paperFileid: 'LC021ALP000EV-deferred.pdf',
    schemeFileid: 'LC021ALP000EV-deferred.pdf',
  });
});

test('unreviewed deferred tasks fail instead of falling back to a main Q number', () => {
  assert.throws(() => reviewedPhysicsSource('phys-2022-hl-deferred-missing'), /lacks reviewed sources/);
  assert.throws(() => reviewedPhysicsSource('phys-2022-ol-deferred-q1-i'), /lacks reviewed sources/);
});
