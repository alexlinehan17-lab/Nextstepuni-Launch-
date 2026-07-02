/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic-tag pipeline — reconstruct verified tags from a workflow's journal.
 *
 * Robust to a large/truncated final workflow return: reads every `result` entry
 * in the given workflow run dir(s), collects classify `tags` + verify
 * `corrections`, attributes each tag to a subject via its subtopic id (each
 * subject's ids are listed in out/<subject>-taxonomy.txt), applies corrections,
 * de-dupes, and writes _wave_tags.json in the shape apply-wave.mjs expects.
 *
 * Usage: node scripts/paper-trail/topic-tags/reconstruct-from-journal.mjs <wfDir> [wfDir...]
 */
import fs from 'fs';
import path from 'path';

const dirs = process.argv.slice(2);
if (!dirs.length) {
  console.error('usage: reconstruct-from-journal.mjs <wfDir> [wfDir...]');
  process.exit(1);
}

// id -> subjectId, from every taxonomy file we generated
const OUT = 'scripts/paper-trail/topic-tags/out';
const idToSubject = {};
for (const fn of fs.readdirSync(OUT).filter(f => f.endsWith('-taxonomy.txt'))) {
  const subject = fn.replace('-taxonomy.txt', '');
  for (const line of fs.readFileSync(path.join(OUT, fn), 'utf8').split('\n')) {
    const m = line.match(/^\s+(\S+)\s{2,}/);
    if (m) idToSubject[m[1]] = subject;
  }
}

const classify = []; // {key, primary, secondary}
const corrections = {}; // key -> correct id
for (const d of dirs) {
  const jl = path.join(d, 'journal.jsonl');
  if (!fs.existsSync(jl)) { console.error('no journal', d); continue; }
  for (const line of fs.readFileSync(jl, 'utf8').trim().split('\n')) {
    let o;
    try { o = JSON.parse(line); } catch { continue; }
    if (o.type !== 'result' || !o.result) continue;
    if (Array.isArray(o.result.tags)) for (const t of o.result.tags) classify.push(t);
    if (Array.isArray(o.result.corrections)) for (const c of o.result.corrections) corrections[c.key] = c.correct;
  }
}

const bySubject = {};
const seen = new Set();
let corrected = 0, orphan = 0;
for (const t of classify) {
  if (seen.has(t.key)) continue;
  seen.add(t.key);
  let primary = t.primary;
  if (corrections[t.key]) { primary = corrections[t.key]; corrected++; }
  const subject = idToSubject[primary];
  if (!subject) { orphan++; continue; } // unknown id → drop (apply-wave also validates)
  (bySubject[subject] ||= []).push({ key: t.key, primary, secondary: t.secondary || null });
}
fs.writeFileSync('_wave_tags.json', JSON.stringify(bySubject));
const counts = Object.fromEntries(Object.entries(bySubject).map(([k, v]) => [k, v.length]));
console.log('subjects:', counts);
console.log(`total ${seen.size} unique questions, ${corrected} corrected by verifier, ${orphan} dropped (bad id)`);
