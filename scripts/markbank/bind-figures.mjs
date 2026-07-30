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
 *   node scripts/markbank/bind-figures.mjs <catalogue.json>
 */

import { readFileSync, writeFileSync, copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const SRC = resolve(ROOT, 'exam-papers/biology/figures');
const DEST = resolve(ROOT, 'public/exam-figures/biology/markbank');
const MANIFEST = resolve(ROOT, 'components/MarkBank/figures.json');

const catalogue = JSON.parse(readFileSync(process.argv[2] ?? '', 'utf8'));
mkdirSync(DEST, { recursive: true });

const manifest = {};
const skipped = [];
const seenHash = new Map();

for (const f of catalogue) {
  const reason =
    f.kind !== 'figure' ? 'decorative'
    : f.truncated ? 'truncated or fragmentary'
    : !f.description || f.description.length < 40 ? 'description too thin to trust'
    : null;
  if (reason) { skipped.push(`${f.file}: ${reason}`); continue; }

  // The extractor names a file <paper>-p<page>-i<index>.png; the directory it
  // lives in is that same paper. Derive both, never guess.
  const dir = f.file.replace(/-p\d+-i\d+\.png$/, '').replace(/^biology-/, '').toLowerCase();
  const src = resolve(SRC, dir, f.file);
  if (!existsSync(src)) { skipped.push(`${f.file}: source missing at ${dir}/`); continue; }

  const bytes = readFileSync(src);
  const md5 = createHash('md5').update(bytes).digest('hex');
  const prev = seenHash.get(md5);
  if (prev) { skipped.push(`${f.file}: identical bytes to ${prev}`); continue; }
  seenHash.set(md5, f.file);

  const id = f.file.replace(/\.png$/, '');
  copyFileSync(src, resolve(DEST, f.file));

  const [, year, level] = /^(\d{4})-(hl|ol)/.exec(dir) ?? [];
  manifest[id] = {
    src: `/exam-figures/biology/markbank/${f.file}`,
    md5,
    alt: f.description,
    lettersVisible: f.lettersVisible ?? [],
    labelMeanings: f.labelMeanings ?? [],
    questionRef: f.questionRef ?? '',
    year: year ? Number(year) : null,
    level: level === 'hl' ? 'higher' : level === 'ol' ? 'ordinary' : null,
    attribution: `SEC Leaving Certificate Biology ${year ?? ''} ${level === 'hl' ? 'Higher' : 'Ordinary'} Level — © State Examinations Commission`,
  };
}

writeFileSync(MANIFEST, JSON.stringify(manifest, null, 1));

const lettered = Object.values(manifest).filter(m => m.lettersVisible.length && m.labelMeanings.length);
process.stdout.write(`published ${Object.keys(manifest).length} figures (${lettered.length} lettered with scheme-stated meanings)\n`);
process.stdout.write(`skipped ${skipped.length}\n`);
const why = {};
for (const s of skipped) { const k = s.split(': ')[1]; why[k] = (why[k] ?? 0) + 1; }
for (const [k, n] of Object.entries(why).sort((a, b) => b[1] - a[1])) {
  process.stdout.write(`  ${n.toString().padStart(4)}  ${k}\n`);
}
