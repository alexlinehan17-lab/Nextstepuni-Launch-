/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Why did this card's provenance check fail?
 *
 *     node scripts/markbank/provdiag.mjs <subject> <card-id>
 *
 * provcheck.mjs tells you a claim is untraceable; this tells you WHERE it stops
 * matching. It binary-searches the longest prefix of the normalised claim that
 * IS in the scheme, then prints what the scheme has next. That is usually the
 * whole diagnosis: a claim that dies at a column boundary is a table the
 * markdown flattened, one that dies mid-formula is stacked notation, and one
 * that dies at a word is a genuine wording difference.
 */
import { readFileSync } from 'node:fs';
import { comparableScheme, normalise } from './schemeText.mjs';
const subj = process.argv[2];
const want = process.argv[3];
const cards = JSON.parse(readFileSync(`scripts/markbank/authored/${subj}.json`,'utf8'));
const c = cards.find(x => x.id === want);
const stem = `${c.year}-${c.level === 'higher' ? 'hl' : 'ol'}`;
const scheme = comparableScheme(readFileSync(`examiner-reports/${subj}/schemes/${stem}.md`,'utf8'));
console.log('card', c.id, '| scheme', stem);
for (const r of c.rows) {
  const claims = [...(r.group?.options ?? [])];
  if (r.kind !== 'anyN') claims.push(r.verbatim);
  for (const claim of claims) {
    const n = normalise(claim);
    if (scheme.includes(n)) continue;
    console.log('\nFAILS:', JSON.stringify(claim));
    console.log('  normalised:', n);
    // longest prefix that IS present
    let lo = 0, hi = n.length;
    while (lo < hi) { const mid = Math.ceil((lo+hi)/2); if (scheme.includes(n.slice(0,mid))) lo = mid; else hi = mid-1; }
    console.log(`  longest matching prefix (${lo}/${n.length}):`, n.slice(0, lo));
    console.log('  first unmatched chars:', JSON.stringify(n.slice(lo, lo+24)));
    const i = scheme.indexOf(n.slice(0, lo));
    if (i >= 0) console.log('  scheme continues:', JSON.stringify(scheme.slice(i+lo, i+lo+40)));
  }
}
