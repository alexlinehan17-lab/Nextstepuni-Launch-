#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — publish inspected figures and write their manifest.
 *
 * Input is the catalogue produced by the figure-inspection workflow, in which an
 * agent OPENED every extracted image and wrote down what is actually in it. Only
 * figures it marked complete and non-truncated are published; anything it flagged
 * as decorative, fragmentary or cut off is left behind with the reason.
 *
 * Nothing here is typed by a model. The published name is the extractor's own
 * name, which derives from the figure's page and index in the PDF, and the hash
 * is computed from the bytes on disk. Both historical figure corruptions in this
 * repo entered through a hand-transcribed path.
 *
 * The subject is read from the file names the extractor produced, for the same
 * reason the deck build reads it from the cards: a flag that disagreed with the
 * data would file one subject's crops under another's.
 *
 *   node scripts/markbank/bind-figures.mjs <catalogue.json>
 */

import { readFileSync, writeFileSync, copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const MANIFEST = resolve(ROOT, 'components/MarkBank/figures.json');

const SUBJECT_TITLE = {
  biology: 'Biology', chemistry: 'Chemistry', physics: 'Physics',
  'agricultural-science': 'Agricultural Science',
};

const catalogue = JSON.parse(readFileSync(process.argv[2] ?? '', 'utf8'));

const manifest = existsSync(MANIFEST) ? JSON.parse(readFileSync(MANIFEST, 'utf8')) : {};
const skipped = [];
// Seeded from what is already published, so a crop cannot be republished under a
// second name by a later subject's run.
const seenHash = new Map(Object.entries(manifest).map(([id, m]) => [m.md5, id]));

for (const f of catalogue) {
  const reason =
    f.kind !== 'figure' ? 'decorative'
    : f.truncated ? 'truncated or fragmentary'
    : !f.description || f.description.length < 40 ? 'description too thin to trust'
    : null;
  if (reason) { skipped.push(`${f.file}: ${reason}`); continue; }

  // The extractor names a file <subject>-<year>-<LEVEL>-paper-p<page>-i<index>.png
  // and writes it into a <year>-<level> directory under its subject. Derive both
  // from the name, never guess.
  const stem = f.file.replace(/-p\d+-i\d+\.png$/, '');
  // The subject id may contain hyphens ("agricultural-science"), so the first
  // group cannot be [a-z]+ — that matched "agricultural", then demanded a year
  // and found "-science", and every crop for such a subject was skipped as
  // "name does not identify a subject". Non-greedy, anchored on the year.
  const parsed = /^([a-z][a-z-]*?)-(\d{4})-(hl|ol)\b/i.exec(stem);
  if (!parsed) { skipped.push(`${f.file}: name does not identify a subject, year and level`); continue; }
  const subjectId = parsed[1].toLowerCase();
  const year = parsed[2];
  const levelCode = parsed[3].toLowerCase();
  const title = SUBJECT_TITLE[subjectId];
  if (!title) { skipped.push(`${f.file}: unknown subject "${subjectId}"`); continue; }

  const src = resolve(ROOT, 'exam-papers', subjectId, 'figures', `${year}-${levelCode}`, f.file);
  if (!existsSync(src)) { skipped.push(`${f.file}: source missing at ${year}-${levelCode}/`); continue; }

  const bytes = readFileSync(src);
  const md5 = createHash('md5').update(bytes).digest('hex');
  const prev = seenHash.get(md5);
  if (prev && prev !== f.file.replace(/\.png$/, '')) {
    skipped.push(`${f.file}: identical bytes to ${prev}`);
    continue;
  }
  seenHash.set(md5, f.file.replace(/\.png$/, ''));

  const dest = resolve(ROOT, 'public/exam-figures', subjectId, 'markbank');
  mkdirSync(dest, { recursive: true });
  copyFileSync(src, resolve(dest, f.file));

  manifest[f.file.replace(/\.png$/, '')] = {
    src: `/exam-figures/${subjectId}/markbank/${f.file}`,
    md5,
    alt: f.description,
    lettersVisible: f.lettersVisible ?? [],
    labelMeanings: f.labelMeanings ?? [],
    questionRef: f.questionRef ?? '',
    year: Number(year),
    level: levelCode === 'hl' ? 'higher' : 'ordinary',
    attribution: `SEC Leaving Certificate ${title} ${year} ${levelCode === 'hl' ? 'Higher' : 'Ordinary'} Level — © State Examinations Commission`,
  };
}

writeFileSync(MANIFEST, JSON.stringify(manifest, null, 1));

const lettered = Object.values(manifest).filter(m => m.lettersVisible.length && m.labelMeanings.length);
process.stdout.write(`manifest holds ${Object.keys(manifest).length} figures (${lettered.length} lettered with scheme-stated meanings)\n`);
process.stdout.write(`skipped ${skipped.length} from this catalogue\n`);
const why = {};
for (const s of skipped) { const k = s.split(': ')[1]; why[k] = (why[k] ?? 0) + 1; }
for (const [k, n] of Object.entries(why).sort((a, b) => b[1] - a[1])) {
  process.stdout.write(`  ${n.toString().padStart(4)}  ${k}\n`);
}
