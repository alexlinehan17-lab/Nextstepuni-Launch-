// usage: node scripts/markbank/agricultural-science-audit/claimtry.mjs <repo root> <scheme.md> "<claim>" ... -> OK/NO per claim, by the rule build-deck applies
import { readFileSync } from 'node:fs';
const [root, md, ...claims] = process.argv.slice(2);
const { comparableScheme, claimMatches } = await import(root + '/scripts/markbank/schemeText.mjs');
const s = comparableScheme(readFileSync(md, 'utf8'));
for (const c of claims) console.log(claimMatches(s, c) ? 'OK ' : 'NO ', c);
