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
  // The eager manifest: every subject the app reads, with its one heading list and which Atlas subject shows each
  // group. The asks themselves stay in data/atlasModel/<subject>.json and load when the subject opens.
  const { MODEL_SUBJECTS } = await server.ssrLoadModule('/scripts/atlas-model/askTopics.ts');
  const { atlasSubjectFor } = await server.ssrLoadModule('/scripts/atlas-model/checks.ts');
  const { readFile } = await import('node:fs/promises');
  const subjects = [];
  for (const subjectId of [...MODEL_SUBJECTS].sort()) {
    const file = JSON.parse(await readFile(new URL(`../../data/atlasModel/${subjectId}.json`, import.meta.url), 'utf8'));
    const home = atlasSubjectFor(subjectId) ?? subjectId;
    const used = file.groups.map(g => new Set(file.questions.filter(q => q[5].some(([, t]) => t.some(i => g.topics.includes(i)))).map(q => q[0])));
    const groups = file.groups.map((g, i) => ({ ...g, atlasId: [...used[i]].sort()[0] ?? home }));
    subjects.push({ subjectId, atlasIds: [...new Set([home, ...groups.map(g => g.atlasId)])], headingSource: file.headingSource, groups, topics: file.topics });
  }
  await writeFile(new URL('../../data/atlasModel/headings.json', import.meta.url), `${JSON.stringify({ v: 1, subjects })}\n`);
  console.log(`headings.json: ${subjects.length} subjects the app reads (${subjects.map(s => s.subjectId).join(', ')}).`);
} finally { await server.close(); }
