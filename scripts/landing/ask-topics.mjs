/** Build the landing search from the same question tags Paper Trail displays.
 * Run: node scripts/landing/ask-topics.mjs
 * The small public index keeps the full curriculum/crosswalk out of the landing bundle.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const bundle = await build({
  entryPoints: [path.join(root, 'scripts/landing/askTopicIndex.ts')],
  bundle: true, format: 'esm', platform: 'node', write: false, logLevel: 'silent',
});
const { buildAskTopicIndex } = await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString('base64')}`);
const dir = path.join(root, 'public/assets/landing/ask');
const index = JSON.parse(fs.readFileSync(path.join(dir, 'index.json'), 'utf8'));
const result = buildAskTopicIndex(index, (year, fileid) => {
  const anchors = new Map();
  // Hosted anchors take precedence for paper positions, as in the viewer.
  for (const base of ['scripts/paper-trail/answers', 'public/paper-anchors']) {
    const file = path.join(root, base, String(year), `${fileid}.json`);
    if (!fs.existsSync(file)) continue;
    for (const q of JSON.parse(fs.readFileSync(file, 'utf8')).q ?? []) {
      if (Number.isInteger(q.pP) && q.pP > 0) anchors.set(q.n, q.pP);
    }
  }
  return anchors;
});
fs.writeFileSync(path.join(dir, 'topics.json'), `${JSON.stringify(result)}\n`);
console.log(`Topic search: ${result.papers.length} papers, ${result.q.length} tagged questions, ${Object.keys(result.topics).length} topic identities.`);
