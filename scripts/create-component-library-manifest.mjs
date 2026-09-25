import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { readdir, stat, writeFile } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import { validateManifest } from './stage-component-library.mjs';

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else if (entry.isFile()) files.push(path);
  }
  return files;
}

async function checksum(path) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(path)) hash.update(chunk);
  return hash.digest('hex');
}

const release = resolve(process.argv[2] || '');
const output = resolve(process.argv[3] || 'deployment/component-library.json');
if (!process.argv[2]) throw new Error('Pass the compiled component library directory');

const files = [];
for (const path of (await walk(release)).sort()) {
  const details = await stat(path);
  files.push({
    path: relative(release, path).split(sep).join('/'),
    size: details.size,
    sha256: await checksum(path),
  });
}

const releaseHash = createHash('sha256')
  .update(JSON.stringify(files))
  .digest('hex');
const manifest = {
  schemaVersion: 1,
  bucket: 'nextstepuni-app.firebasestorage.app',
  prefix: `private-builds/component-library/20260925-${releaseHash}`,
  files,
};
validateManifest(manifest);
await writeFile(output, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`Wrote ${files.length} verified component library entries (${releaseHash}).`);
