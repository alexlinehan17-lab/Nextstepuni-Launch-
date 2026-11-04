// usage: node scripts/markbank/agricultural-science-audit/claimtest.mjs <repo root> <scheme.md> <claims.json>  -> prints MISS lines
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const [root, md, file] = process.argv.slice(2);
const { comparableScheme, claimMatches } = await import(resolve(root, 'scripts/markbank/schemeText.mjs'));
const s = comparableScheme(readFileSync(md, 'utf8'));
let miss = 0;
for (const c of JSON.parse(readFileSync(file, 'utf8'))) if (!claimMatches(s, c)) { miss++; console.log('MISS', c); }
console.log(miss, 'missing');
