#!/usr/bin/env node
/**
 * Fold stdin through the Mark Bank's own glyph folding and write it back.
 *
 * The SEC's PDFs typeset "letters" with a single Ʃ glyph and "ti" with Ɵ, and
 * test/markBankSchemes.test.ts holds every scheme file to being extractor
 * output with those folded away. Text appended by append-scheme-blocks.py has
 * to meet the same bar, and the fold has to be the SAME fold — so this imports
 * the table rather than restating it, for the reason verify-claims.mjs imports
 * claimMatches rather than reimplementing it.
 */
import { readFileSync } from 'node:fs';
import { LIGATURES } from '../schemeText.mjs';

// Ligatures only. foldDigits also rewrites subscripts, superscripts and the
// Mathematical Alphanumeric block, and folding those in the appended text cost
// a Chemistry card whose marking point matched the unfolded form. The file-level
// rule this has to satisfy is about ligatures alone; everything else is already
// handled at comparison time by normalise(), where it belongs.
const text = readFileSync(0, 'utf8');
process.stdout.write(text.replace(/[ƟŦƩﬀﬁﬂﬃﬄﬅﬆ]/g, (c) => LIGATURES[c] ?? c));
