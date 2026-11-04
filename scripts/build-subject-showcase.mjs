import { createServer } from 'vite';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const server = await createServer({ root, configFile: false, cacheDir: 'node_modules/.vite-subject-showcase', server: { middlewareMode: true, watch: null, hmr: false, ws: false }, optimizeDeps: { noDiscovery: true, include: [] }, appType: 'custom' });
try {
  const { buildSubjectShowcase } = await server.ssrLoadModule('/components/landing/subjectShowcaseSource.ts');
  const subjects = buildSubjectShowcase();
  await writeFile(new URL('../components/landing/subjectShowcase.json', import.meta.url), `${JSON.stringify(subjects, null, 2)}\n`);
  console.log(`Subject showcase: ${subjects.length} subjects; current Mark Bank, Topic Atlas and paper counts.`);
} finally { await server.close(); }
