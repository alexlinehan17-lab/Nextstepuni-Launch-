/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Why did this card's provenance check fail, and what does the scheme say?
 *
 *     node scripts/markbank/provdiag.mjs <subject> <card-id>
 *
 * provcheck.mjs tells you a claim is untraceable; this tells you WHERE it stops
 * matching and prints the SEC's own wording at that point, so the fix is usually
 * obvious: a claim that dies at a column boundary is a table the markdown
 * flattened, one that dies mid-formula is stacked notation, and one that dies at
 * a word is a wording difference — most often the card picked one of the
 * scheme's slash-separated alternatives ("absorbs/stops/blocks").
 *
 * The raw context is recovered by normalising the scheme WHILE recording, for
 * every surviving character, the offset it came from — so a position in the
 * normalised text can be mapped back to the sentence it belongs to.
 */
import { readFileSync } from 'node:fs';
import { normalise } from './schemeText.mjs';

const subj = process.argv[2];
const want = process.argv[3];
const cards = JSON.parse(readFileSync(`scripts/markbank/authored/${subj}.json`, 'utf8'));
const c = cards.find((x) => x.id === want);
if (!c) { console.error(`no card ${want} in ${subj}`); process.exit(1); }

const stem = `${c.year}-${c.level === 'higher' ? 'hl' : 'ol'}`;
const raw = readFileSync(`examiner-reports/${subj}/schemes/${stem}.md`, 'utf8');

/** Normalised scheme plus, per normalised character, its offset in `raw`. */
const flat = [];
const at = [];
for (let i = 0; i < raw.length; i++) {
  const n = normalise(raw[i]);
  for (const ch of n) { flat.push(ch); at.push(i); }
}
const scheme = flat.join('');

const claimsOf = (r) => r.kind === 'anyN' && r.group ? r.group.options
                                                    : [String(r.verbatim).split(/\s[—-]\s/).pop()];
console.log(`card ${c.id} | scheme ${stem}\n`);
for (const r of c.rows ?? []) {
  for (const claim of claimsOf(r)) {
    const n = normalise(claim);
    if (scheme.includes(n)) continue;
    console.log(`FAILS (row ${r.id}): ${JSON.stringify(claim)}`);
    let lo = 0, hi = n.length;
    while (lo < hi) {
      const mid = Math.ceil((lo + hi) / 2);
      if (scheme.includes(n.slice(0, mid))) lo = mid; else hi = mid - 1;
    }
    console.log(`  matches the first ${lo}/${n.length} characters, then stops`);
    const i = scheme.indexOf(n.slice(0, lo));
    if (i >= 0) {
      const from = at[Math.max(0, i - 40)] ?? 0;
      const to = at[Math.min(at.length - 1, i + lo + 120)] ?? raw.length;
      console.log('  SCHEME SAYS: ' + JSON.stringify(raw.slice(from, to).replace(/\s+/g, ' ')));
    }
    console.log();
  }
}
