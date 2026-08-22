#!/usr/bin/env node
/**
 * Gate candidate marking points against a scheme using the build's own rule.
 *
 * The authoring scripts are Python and the provenance rule is JavaScript. The
 * temptation is to re-implement normalise() on the Python side; provcheck.mjs
 * shows where that ends — it drifted from build-deck.mjs and reported 114
 * shipped Agricultural Science claims as untraceable when every one of them
 * was fine. So Python proposes and this disposes, importing the same
 * comparableScheme/claimMatches the build and the deck test import.
 *
 *   echo '{"scheme":"examiner-reports/agricultural-science/schemes/2021-hl.md",
 *          "claims":["Buttercup","Thistle"]}' | node verify-claims.mjs
 *   -> {"ok":["Buttercup","Thistle"],"bad":[]}
 */
import { readFileSync } from 'node:fs';
import { comparableScheme, claimMatches } from '../schemeText.mjs';

const input = JSON.parse(readFileSync(0, 'utf8'));
const scheme = comparableScheme(readFileSync(input.scheme, 'utf8'));
const ok = [];
const bad = [];
for (const claim of input.claims) (claimMatches(scheme, claim) ? ok : bad).push(claim);
process.stdout.write(JSON.stringify({ ok, bad }));
