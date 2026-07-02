/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic-tag pipeline helper — emit a subject's curriculum subtopic taxonomy as
 * a compact text block for the classifier agents (id + name, grouped by strand).
 *
 * Usage:  node scripts/paper-trail/topic-tags/gen-taxonomy.mjs <subjectId>
 * Writes: scripts/paper-trail/topic-tags/out/<subjectId>-taxonomy.txt
 */
import fs from 'fs';
import path from 'path';

const SUBJECT = process.argv[2];
if (!SUBJECT) {
  console.error('usage: gen-taxonomy.mjs <subjectId>');
  process.exit(1);
}
const ct = fs.readFileSync('curriculum.ts', 'utf8');
const cs = ct.indexOf('CURRICULUM: CurriculumSubject[] =');
const ca = ct.indexOf('[', ct.indexOf('=', cs));
let cd = 0, ce = -1;
for (let i = ca; i < ct.length; i++) {
  if (ct[i] === '[') cd++;
  else if (ct[i] === ']') { cd--; if (!cd) { ce = i; break; } }
}
const CUR = JSON.parse(ct.slice(ca, ce + 1).replace(/,\s*([\]}])/g, '$1'));
const subj = CUR.find(x => x.id === SUBJECT);
if (!subj) {
  console.error('no curriculum for', SUBJECT);
  process.exit(1);
}
let out = `${subj.name} — curriculum subtopics. Assign the SINGLE best primary id (optional secondary).\n`;
for (const st of subj.strands) {
  out += `\n${st.name}:\n`;
  for (const sub of st.subtopics) out += `  ${sub.id}  ${sub.name}\n`;
}
const dir = 'scripts/paper-trail/topic-tags/out';
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(path.join(dir, `${SUBJECT}-taxonomy.txt`), out);
console.error(`wrote ${SUBJECT} taxonomy: ${subj.strands.reduce((a, s) => a + s.subtopics.length, 0)} subtopics`);
