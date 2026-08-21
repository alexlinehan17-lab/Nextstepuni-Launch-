/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Apply suggest-verbatim.mjs's candidates to the authored cards.
 *
 *     node scripts/markbank/suggest-verbatim.mjs <subject> > /tmp/s.tsv
 *     node scripts/markbank/apply-verbatim.mjs <subject> /tmp/s.tsv
 *
 * Re-checks the safety rule here rather than trusting the file: a replacement
 * is written only if the new text contains EVERY word of the old, in order, and
 * only if it actually traces to the scheme. So the card can only gain the
 * alternatives the SEC printed and the author dropped -- never lose meaning.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { normalise } from './schemeText.mjs';

const subj = process.argv[2];
const path = `scripts/markbank/authored/${subj}.json`;
const cards = JSON.parse(readFileSync(path, 'utf8'));
const byId = new Map(cards.map((c) => [c.id, c]));
const cache = new Map();
const schemeFor = (c) => {
  const stem = `${c.year}-${c.level === 'higher' ? 'hl' : 'ol'}`;
  const f = `examiner-reports/${subj}/schemes/${stem}.md`;
  if (!cache.has(f)) cache.set(f, normalise(readFileSync(f, 'utf8')));
  return cache.get(f);
};
const words = (s) => (String(s).toLowerCase().match(/[a-z0-9]+/g) ?? []);
function covers(text, claim) {
  const t = words(text), c = words(claim);
  let i = 0;
  for (const w of c) { i = t.indexOf(w, i); if (i === -1) return false; i++; }
  return true;
}

/**
 * Is every word the candidate ADDS an alternative the SEC printed behind a "/"?
 *
 * `covers` alone is not enough. The scheme markdown interleaves table columns,
 * so "Decrease in dopamine levels or decrease in serotonin levels" also appears,
 * word for word in order, inside "Decrease in dopamine levels or decrease in
 * stroke or multiple sclerosis or other or serotonin levels" -- two columns
 * shuffled together, which means nothing.
 *
 * So walk the candidate against the claim. A word that does not match the next
 * expected one is allowed ONLY while we are inside an alternative, which a "/"
 * opens and the next matching word closes. That keeps "absorbs/stops/blocks",
 * "energy/heat" and "contain gaps / contain specific wavelengths", and rejects
 * every shuffle, because a shuffle has no slash.
 */
function addsOnlyAlternatives(cand, claim) {
  const want = words(claim);
  let wi = 0, inAlt = false;
  for (const tok of String(cand).split(/\s+/)) {
    if (!tok) continue;
    if (tok === '/' || tok === '//') { inAlt = true; continue; }
    const parts = tok.split('/');
    for (let p = 0; p < parts.length; p++) {
      if (p > 0) inAlt = true;
      // Split the part the same way words() splits the claim: "electron(s)" is
      // TWO words there, so joining it here would never match.
      for (const w of (parts[p].toLowerCase().match(/[a-z0-9]+/g) ?? [])) {
        if (wi < want.length && w === want[wi]) { wi++; inAlt = false; continue; }
        if (!inAlt) return false;
      }
    }
    if (tok.endsWith('/')) inAlt = true;
  }
  return wi === want.length;
}

let applied = 0, rejected = 0;
for (const line of readFileSync(process.argv[3], 'utf8').split('\n')) {
  if (!line.trim()) continue;
  const [id, rowId, claimJson, candJson] = line.split('\t');
  if (!candJson || candJson === 'NO CANDIDATE') continue;
  const claim = JSON.parse(claimJson), cand = JSON.parse(candJson);
  const c = byId.get(id);
  if (!c) { rejected++; continue; }
  const row = c.rows.find((r) => r.id === rowId);
  if (!row) { rejected++; continue; }
  if (!covers(cand, claim)) { console.log(`REJECT ${id} ${rowId}: candidate drops words`); rejected++; continue; }
  if (!addsOnlyAlternatives(cand, claim)) {
    console.log(`REJECT ${id} ${rowId}: adds text that is not a "/" alternative — likely interleaved columns`);
    rejected++; continue;
  }
  const scheme = schemeFor(c);
  if (!scheme.includes(normalise(cand))) { console.log(`REJECT ${id} ${rowId}: candidate not in scheme`); rejected++; continue; }
  if (row.kind === 'anyN' && row.group) {
    const i = row.group.options.indexOf(claim);
    if (i === -1) { rejected++; continue; }
    row.group.options[i] = cand;
  } else if (String(row.verbatim).split(/\s[—-]\s/).pop() === claim) {
    row.verbatim = String(row.verbatim).replace(claim, cand);
  } else { rejected++; continue; }
  applied++;
  console.log(`applied ${id} ${rowId}`);
}
writeFileSync(path, JSON.stringify(cards, null, 1) + '\n');
console.log(`\n${applied} applied, ${rejected} rejected`);
