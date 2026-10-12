/**
 * Check that every quoted marking point is found in the scheme text, by the rule
 * the deck build applies (claimMatches over the glyph-repaired comparable scheme).
 *
 *   python3 scripts/markbank/authoring/maths/review_2020_hl_p1.py /tmp/q.json   # dump the quotes
 *   node scripts/markbank/authoring/maths/check_quotes.mjs examiner-reports/maths/schemes/2020-hl.md /tmp/q.json
 *
 * The label before " — " is the scheme part a point comes from, not quoted text.
 */
import { readFileSync } from 'node:fs';
import { comparableScheme, claimMatches } from '../../schemeText.mjs';
const [schemeFile, quotesFile] = process.argv.slice(2);
const scheme = comparableScheme(readFileSync(schemeFile, 'utf8'));
const quotes = JSON.parse(readFileSync(quotesFile, 'utf8'));
let bad = 0;
for (const [id, list] of Object.entries(quotes)) for (const q of list) {
  const claim = String(q).split(/\s[—-]\s/).pop();
  if (!claimMatches(scheme, claim)) { bad++; console.log('MISS', id, JSON.stringify(q)); }
}
console.log(bad ? `${bad} missing` : 'all quotes found');
