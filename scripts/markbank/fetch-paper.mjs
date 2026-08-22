#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — download an SEC paper or marking scheme from Paper Trail.
 *
 * The corpus this project already ships is the source of truth for every PDF the
 * Mark Bank is built from, so a card's figures and its marking points come from
 * the same bytes a student can open in the app. Fetching by hand went wrong
 * twice: once by taking `papers[0]` and getting the answerbook rather than the
 * question paper, and once by guessing a storage path. Both are resolved here.
 *
 * The output name matters. `extract-figures.py` derives a figure's published key
 * from the file name, and the deck's cards reference that key, so a paper saved
 * under a different name yields figures no card can find. Pass the name the
 * cards expect: <subject>-<year>-<HL|OL>-paper<n>.pdf.
 *
 *   node scripts/markbank/fetch-paper.mjs biology 2022 higher "Section C" \
 *        /tmp/biopapers/biology-2022-HL-paper2.pdf
 *
 * With no label it lists what that subject/year/level actually holds, which is
 * the quickest way to find the label to pass.
 *
 * --scheme fetches the MARKING SCHEME for that sitting instead of the paper.
 * One scheme usually covers every paper of a sitting, so the label may be any of
 * them and the same file comes back; where a subject splits its schemes, the
 * label picks between them.
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { paperIndex } from './paperIndex.mjs';

const BUCKET = 'nextstepuni-app.firebasestorage.app';

const argv = process.argv.slice(2);
const wantScheme = argv.includes('--scheme');
const [subject, yearArg, level, label, out] = argv.filter((a) => a !== '--scheme');
if (!subject || !yearArg || !level) {
  process.stderr.write('usage: fetch-paper.mjs <subject> <year> <higher|ordinary> [label] [outfile]\n');
  process.exit(2);
}
const year = Number(yearArg);

const subjectPapers = paperIndex[subject];
if (!subjectPapers) {
  process.stderr.write(`unknown subject "${subject}" — have: ${Object.keys(paperIndex).join(', ')}\n`);
  process.exit(1);
}

// `ev` is the English-language edition; the Irish one carries the same figures
// but different question text, and mixing the two produced cards whose stem did
// not match their own paper.
const release = Object.values(subjectPapers).find(
  (r) => r.year === year && r.level === level && r.lang === 'ev',
);
if (!release) {
  process.stderr.write(`no ${subject} ${year} ${level} (ev) in the index\n`);
  process.exit(1);
}

if (!label) {
  for (const p of release.papers) {
    process.stdout.write(`${p.label}${p.scheme ? `  [scheme ${p.scheme.f}]` : ''}\n`);
  }
  process.exit(0);
}

const paper = release.papers.find((p) => p.label === label);
if (!paper) {
  process.stderr.write(`no paper labelled "${label}" — have: ${release.papers.map((p) => p.label).join(' | ')}\n`);
  process.exit(1);
}

const doc = wantScheme ? paper.scheme : paper.doc;
if (!doc) {
  process.stderr.write(`no ${wantScheme ? 'scheme' : 'paper'} for "${label}"\n`);
  process.exit(1);
}
const path = `papers/lc/${subject}/${year}/${wantScheme ? 'scheme' : 'paper'}/${doc.f}`;
const url = `https://firebasestorage.googleapis.com/v0/b/${BUCKET}/o/${encodeURIComponent(path)}?alt=media`;
const res = await fetch(url);
if (!res.ok) {
  process.stderr.write(`${res.status} fetching ${path}\n`);
  process.exit(1);
}
const bytes = Buffer.from(await res.arrayBuffer());

const dest = out ?? `${subject}-${year}-${level === 'higher' ? 'HL' : 'OL'}${wantScheme ? '-scheme' : ''}.pdf`;
mkdirSync(dirname(dest), { recursive: true });
writeFileSync(dest, bytes);
process.stdout.write(`${dest} (${(bytes.length / 1024).toFixed(0)} kB)\n`);
