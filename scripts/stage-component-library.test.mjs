import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Readable } from 'node:stream';
import { stageLibrary, validateManifest } from './stage-component-library.mjs';

const bytes = Buffer.from('<html>components</html>');
const entry = path => ({
  path,
  size: bytes.length,
  sha256: createHash('sha256').update(bytes).digest('hex'),
});
const manifest = files => ({
  schemaVersion: 1,
  bucket: 'nextstepuni-app.firebasestorage.app',
  prefix: 'private-builds/component-library/test-release',
  files,
});

test('stages an allowlisted gallery after verifying size and checksum', async () => {
  const destination = join(tmpdir(), `component-library-test-${process.pid}`);
  const release = manifest([entry('index.html'), entry('burst.json'), entry('assets/gallery-abc123.js'), entry('images/previews/example.webp'), entry('logos/example.svg')]);
  const count = await stageLibrary(release, destination, async () => Readable.from(bytes));
  assert.equal(count, 5);
  assert.equal(await readFile(join(destination, 'index.html'), 'utf8'), bytes.toString());
});

test('rejects traversal, source maps, source files and duplicate paths', () => {
  for (const path of ['../index.html', '/index.html', 'assets/../../index.html', 'assets/gallery.js.map', 'logos/example.exe', 'src/button.tsx']) {
    assert.throws(() => validateManifest(manifest([entry('index.html'), entry(path)])), /path/);
  }
  assert.throws(() => validateManifest(manifest([entry('index.html'), entry('index.html')])), /path/);
});

test('rejects an invalid checksum and a manifest without the gallery document', () => {
  assert.throws(() => validateManifest(manifest([{ ...entry('index.html'), sha256: 'bad' }])), /checksum/);
  assert.throws(() => validateManifest(manifest([entry('assets/gallery.js')])), /Incomplete/);
});

test('removes the staged directory when downloaded content fails verification', async () => {
  const destination = join(tmpdir(), `component-library-bad-test-${process.pid}`);
  const release = manifest([entry('index.html')]);
  await assert.rejects(() => stageLibrary(release, destination, async () => Readable.from('changed')), /verification/);
  await assert.rejects(() => readFile(join(destination, 'index.html')));
});
