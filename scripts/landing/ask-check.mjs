/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ask the papers — look at what ask-index.mjs wrote before trusting it:
 * per-paper question counts (a split that failed shows as 0–3 or 40+),
 * the longest questions (a leaked extract shows as a wall of prose) and a
 * random sample per subject.
 *
 * Usage: node scripts/landing/ask-check.mjs [subject ...] [--sample=N] [--longest=N]
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const DIR = path.join(ROOT, 'public', 'assets', 'landing', 'ask');
const arg = (name, fallback) => { const a = process.argv.find(x => x.startsWith(`--${name}=`)); return a ? +a.slice(name.length + 3) : fallback; };
const only = process.argv.slice(2).filter(a => !a.startsWith('--'));
const SAMPLE = arg('sample', 4), LONGEST = arg('longest', 3);
const index = JSON.parse(fs.readFileSync(path.join(DIR, 'index.json'), 'utf8'));
let seed = 7;
const rand = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
for (const s of index.subjects) {
  if (only.length && !only.includes(s.id)) continue;
  const d = JSON.parse(fs.readFileSync(path.join(DIR, s.file), 'utf8'));
  console.log(`\n=== ${d.name}: ${d.papers.length} papers, ${d.q.length} questions, ${(s.bytes / 1024).toFixed(0)} KB`);
  const counts = d.papers.map((p, i) => `${p.y}${p.l}${p.p ? ' ' + p.p : ''}:${d.q.filter(q => q[0] === i).length}`);
  console.log('  per paper: ' + counts.join('  '));
  const byLen = d.q.map((q, i) => [q[3].length, i]).sort((a, b) => b[0] - a[0]).slice(0, LONGEST);
  for (const [len, i] of byLen) { const q = d.q[i], p = d.papers[q[0]]; console.log(`  LONG ${len} ${p.y} ${p.l} ${p.p} ${q[1]} p${q[2]}: ${q[3].slice(0, 220)}…`); }
  for (let k = 0; k < SAMPLE; k++) { const i = Math.floor(rand() * d.q.length); const q = d.q[i], p = d.papers[q[0]]; console.log(`  ${p.y} ${p.l} ${p.p} ${q[1]} p${q[2]}: ${q[3].slice(0, 200)}${q[3].length > 200 ? '…' : ''}`); }
}
