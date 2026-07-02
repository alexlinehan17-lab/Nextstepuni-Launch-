/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic-tag pipeline — turn classifier/verifier output into committed wave files.
 *
 * Input: a JSON object { subjectId: [ {key, primary, secondary?} ... ] } at the
 * path given as argv[2] (default _wave_tags.json). Joins each tag to its stem
 * metadata (out/<subject>-stems.json) to recover fileid/level/paper/year/lang,
 * validates every id against curriculum.ts, groups by paper, and writes
 * tags/<subject>.json. Run build-tags.mjs afterwards.
 *
 * Usage:  node scripts/paper-trail/topic-tags/apply-wave.mjs [wave_tags.json]
 */
import fs from 'fs';
import path from 'path';

const IN = process.argv[2] || '_wave_tags.json';
const OUT_DIR = 'scripts/paper-trail/topic-tags/out';
const TAGS_DIR = 'scripts/paper-trail/topic-tags/tags';
fs.mkdirSync(TAGS_DIR, { recursive: true });

// valid curriculum ids
const ct = fs.readFileSync('curriculum.ts', 'utf8');
const cs = ct.indexOf('CURRICULUM: CurriculumSubject[] =');
const ca = ct.indexOf('[', ct.indexOf('=', cs));
let cd = 0, ce = -1;
for (let i = ca; i < ct.length; i++) {
  if (ct[i] === '[') cd++;
  else if (ct[i] === ']') { cd--; if (!cd) { ce = i; break; } }
}
const CUR = JSON.parse(ct.slice(ca, ce + 1).replace(/,\s*([\]}])/g, '$1'));
const validIds = new Set();
for (const s of CUR) for (const st of s.strands) for (const sub of st.subtopics) validIds.add(sub.id);

const paperKeyOf = l => (/\b(two|2|ii)\b/i.test(l) ? 'p2' : /\b(one|1|i)\b/i.test(l) ? 'p1' : 'single');

const bySubject = JSON.parse(fs.readFileSync(IN, 'utf8'));
let grand = 0;
for (const [subjectId, tags] of Object.entries(bySubject)) {
  const stems = JSON.parse(fs.readFileSync(path.join(OUT_DIR, `${subjectId}-stems.json`), 'utf8'));
  const meta = Object.fromEntries(stems.map(s => [s.key, s]));
  const papers = {};
  let dropped = 0, seen = new Set();
  for (const tg of tags) {
    const m = meta[tg.key];
    if (!m) { dropped++; continue; }
    if (seen.has(tg.key)) continue; // de-dupe overlapping chunk output
    seen.add(tg.key);
    if (!validIds.has(tg.primary)) { dropped++; continue; }
    const secondary = tg.secondary && validIds.has(tg.secondary) ? tg.secondary : undefined;
    const id = `${m.year}|${m.level}|${m.lang}|${m.f}`;
    if (!papers[id]) papers[id] = { subjectId, level: m.level, lang: m.lang, year: m.year, fileid: m.f, paperKey: paperKeyOf(m.paper), q: [] };
    const q = { n: String(m.n), primary: tg.primary };
    if (secondary) q.secondary = secondary;
    papers[id].q.push(q);
  }
  const arr = Object.values(papers).sort((a, b) => b.year - a.year || a.level.localeCompare(b.level) || a.paperKey.localeCompare(b.paperKey));
  for (const p of arr) p.q.sort((a, b) => Number(a.n) - Number(b.n));
  const nq = arr.reduce((a, p) => a + p.q.length, 0);
  fs.writeFileSync(path.join(TAGS_DIR, `${subjectId}.json`), JSON.stringify(arr, null, 1));
  grand += nq;
  console.log(`${subjectId}: ${arr.length} papers, ${nq} questions${dropped ? `, dropped ${dropped}` : ''}`);
}
console.log(`TOTAL ${grand} questions across ${Object.keys(bySubject).length} subjects`);
