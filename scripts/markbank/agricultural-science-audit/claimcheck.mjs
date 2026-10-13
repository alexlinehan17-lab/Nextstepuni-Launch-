// usage: node scripts/markbank/agricultural-science-audit/claimcheck.mjs <repo root> <cards.json> -> prints untraceable claims per card (mirrors build-deck provenance)
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
const [root, cardsPath] = process.argv.slice(2);
const { comparableScheme, claimMatches } = await import(resolve(root, 'scripts/markbank/schemeText.mjs'));
const cards = JSON.parse(readFileSync(cardsPath, 'utf8'));
const cache = new Map();
let bad = 0;
for (const c of cards) {
  const f = resolve(root, 'examiner-reports/agricultural-science/schemes', `${c.year}-${c.level === 'higher' ? 'hl' : 'ol'}.md`);
  if (!cache.has(f)) cache.set(f, comparableScheme(existsSync(f) ? readFileSync(f, 'utf8') : ''));
  const s = cache.get(f);
  for (const r of [c.rows, ...(c.answerVariants ?? []).map(v => v.rows)].flat()) {
    const claims = r.kind === 'anyN' && r.group ? r.group.options : [String(r.verbatim).split(/\s[—-]\s/).pop()];
    for (const claim of claims) if (!claimMatches(s, claim)) { bad++; console.log(`${c.id} ${r.id}: ${claim}`); }
  }
}
console.log(`${bad} untraceable claim(s) across ${cards.length} cards`);
