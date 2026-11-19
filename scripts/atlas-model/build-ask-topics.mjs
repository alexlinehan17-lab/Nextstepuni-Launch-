// Write data/atlasModel/<subject>.json, the one topic record per ask that the Mark Bank and the Topic Atlas both read.
// Usage: node scripts/atlas-model/build-ask-topics.mjs [subject…]   (default: every subject with a filing)
// Generated: never edit the JSON by hand. test/atlasModelChecks.test.ts re-derives it and fails when it lags.
import { createServer } from 'vite';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../../', import.meta.url));
const server = await createServer({ root, configFile: false, cacheDir: 'node_modules/.vite-atlas-model', server: { middlewareMode: true, watch: null, hmr: false, ws: false }, optimizeDeps: { noDiscovery: true, include: [] }, appType: 'custom', logLevel: 'error' });
try {
  const { deriveAskTopics, FILED_SUBJECTS } = await server.ssrLoadModule('/scripts/atlas-model/askTopics.ts');
  for (const subjectId of process.argv.slice(2).length ? process.argv.slice(2) : FILED_SUBJECTS) {
    const { file, problems } = await deriveAskTopics(subjectId);
    if (problems.length) { console.error(problems.slice(0, 20).join('\n')); throw new Error(`${subjectId}: ${problems.length} cards have no topic record`); }
    await writeFile(new URL(`../../data/atlasModel/${subjectId}.json`, import.meta.url), `${JSON.stringify(file)}\n`);
    const asks = file.questions.reduce((n, q) => n + q[5].length, 0);
    const multi = file.questions.filter(q => new Set(q[5].flatMap(a => a[1])).size > 1).length;
    console.log(`${subjectId}: ${asks + file.unplaced.length} asks (${file.unplaced.length} not yet in the Atlas) in ${file.questions.length} printed questions (${multi} with parts under more than one heading), ${file.topics.length} headings.`);
  }
} finally { await server.close(); }
