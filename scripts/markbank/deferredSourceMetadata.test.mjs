import assert from 'node:assert/strict';
import test from 'node:test';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { physicsSourceMap, physicsSourceMetadataMap } from './physicsSources.mjs';
import { homeEconomicsSourceMap, homeEconomicsSourceMetadataMap } from './homeEconomicsSources.mjs';

const physics = JSON.parse(readFileSync(new URL('./authored/physics-review-audit.json', import.meta.url)));
const home = JSON.parse(readFileSync(new URL('./authoring/home-economics/2023-hl-deferred-review.json', import.meta.url)));
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const bytesFor = path => Buffer.from(`test fixture for ${path}`);
const deferredPhysics = audit => Object.values(audit.sittings).filter(r => r.sitting === 'deferred');
const subjects = [
  { name: 'Physics', original: physics, reviews: deferredPhysics, metadata: physicsSourceMetadataMap, strict: physicsSourceMap },
  { name: 'Home Economics', original: home, reviews: review => [review], metadata: homeEconomicsSourceMetadataMap, strict: homeEconomicsSourceMap },
];

for (const subject of subjects) {
  test(`${subject.name}: metadata retains every reviewed task without reading PDFs`, () => {
    const result = subject.metadata(subject.original);
    const ids = subject.reviews(subject.original).flatMap(review => review.tasks.map(task => task.id));
    assert.deepEqual([...result.keys()].sort(), ids.sort());
    assert.ok([...result.values()].every(source => source.sitting === 'deferred' && source.lang === 'ev'));
  });

  test(`${subject.name}: strict authoring still rejects missing and changed originals`, () => {
    assert.throws(() => subject.strict(subject.original, () => { throw new Error('missing original'); }), /missing original/);
    assert.throws(() => subject.strict(subject.original, () => Buffer.from('wrong original')), /bytes differ/);
    const fixture = structuredClone(subject.original);
    for (const review of subject.reviews(fixture)) {
      for (const source of Object.values(review.sources)) source.sha256 = digest(bytesFor(source.path));
    }
    assert.deepEqual(subject.strict(fixture, bytesFor), subject.metadata(fixture));
  });

  test(`${subject.name}: metadata rejects wrong archive, unreviewed tasks and invalid hashes`, () => {
    for (const mutate of [
      review => { Object.values(review.sources)[0].path = 'paper-trail-corpus/exampapers/wrong.pdf'; },
      review => { Object.values(review.sources)[0].sha256 = 'not-a-hash'; },
      review => { review.tasks[0].status = 'unreviewed'; },
      review => { review.tasks.push(structuredClone(review.tasks[0])); },
    ]) {
      const bad = structuredClone(subject.original);
      mutate(subject.reviews(bad)[0]);
      assert.throws(() => subject.metadata(bad), /archive identity|source hash|invalid deferred task/);
    }
  });
}

for (const [moduleName, strictName, metadataName, reviews] of [
  ['physicsSources.mjs', 'reviewedPhysicsSource', 'reviewedPhysicsSourceMetadata', deferredPhysics(physics)],
  ['homeEconomicsSources.mjs', 'reviewedHomeEconomicsSource', 'reviewedHomeEconomicsSourceMetadata', [home]],
]) {
  test(`${moduleName}: metadata cannot bypass strict checks and failed reads cannot poison its cache`, () => {
    const cardId = reviews[0].tasks[0].id;
    // Separate process: intercept only this module's review/PDF reads, without
    // touching real source files or sharing patched builtins with other tests.
    const script = String.raw`
      import assert from 'node:assert/strict';
      import fs from 'node:fs';
      import { createHash } from 'node:crypto';
      import { syncBuiltinESMExports } from 'node:module';
      const read = fs.readFileSync;
      let pdfReads = 0;
      let failOnce = true;
      const bytesFor = path => Buffer.from('fixture:' + path);
      fs.readFileSync = (path, ...args) => {
        const name = String(path);
        if (name.includes('/paper-trail-corpus/')) {
          pdfReads++;
          if (failOnce) { failOnce = false; throw new Error('temporary original read failure'); }
          return bytesFor(name.slice(name.indexOf('paper-trail-corpus/')));
        }
        if (name.endsWith('physics-review-audit.json') || /home-economics\/202[23]-hl-deferred-review\.json$/.test(name)) {
          const document = JSON.parse(read(path, ...args));
          const reviews = document.sittings ? Object.values(document.sittings).filter(r => r.sitting === 'deferred') : [document];
          for (const review of reviews) for (const source of Object.values(review.sources)) {
            source.sha256 = createHash('sha256').update(bytesFor(source.path)).digest('hex');
          }
          return JSON.stringify(document);
        }
        return read(path, ...args);
      };
      syncBuiltinESMExports();
      const module = await import(${JSON.stringify(new URL(moduleName, import.meta.url).href)});
      const metadata = module[${JSON.stringify(metadataName)}](${JSON.stringify(cardId)});
      assert.equal(pdfReads, 0);
      assert.throws(() => module[${JSON.stringify(strictName)}](${JSON.stringify(cardId)}), /temporary original read failure/);
      assert.deepEqual(module[${JSON.stringify(strictName)}](${JSON.stringify(cardId)}), metadata);
      const readsAfterSuccess = pdfReads;
      assert.ok(readsAfterSuccess > 1);
      assert.deepEqual(module[${JSON.stringify(strictName)}](${JSON.stringify(cardId)}), metadata);
      assert.equal(pdfReads, readsAfterSuccess);
    `;
    const child = spawnSync(process.execPath, ['--input-type=module', '--eval', script], { encoding: 'utf8' });
    assert.equal(child.status, 0, child.stderr || child.stdout);
  });
}
