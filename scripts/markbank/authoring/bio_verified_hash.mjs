/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The content hash of the cards a Biology review verified (left untouched),
 * in the current deck and in the deck at the review's baseline commit; the two
 * must agree, and the hash is what markBankBiologyReview.test.ts pins.
 *   node scripts/markbank/authoring/bio_verified_hash.mjs 2023-ol
 */
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const sitting = process.argv[2];
const audit = JSON.parse(fs.readFileSync(path.join(ROOT, 'scripts/markbank/authored/biology-review-audit.json'), 'utf8'));
const review = audit.sittings[sitting]?.review;
if (!review) throw new Error(`${sitting}: no reviewed sitting with a baseline`);
const deck = `components/MarkBank/cards/biology/${sitting.endsWith('-hl') ? 'higher' : 'ordinary'}.ts`;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bio-vh-'));
const before = path.join(tmp, 'before.ts');
fs.writeFileSync(before, execFileSync('git', ['show', `${review.baselineCommit}:${deck}`], { cwd: ROOT, maxBuffer: 1 << 30 }));
const after = path.join(tmp, 'after.ts');
fs.copyFileSync(path.join(ROOT, deck), after);
for (const [label, file] of [['baseline', before], ['current', after]]) {
  const { CARDS } = await import(pathToFileURL(file).href);
  const byId = new Map(CARDS.map(c => [c.id, c]));
  const cards = review.verified.map(id => byId.get(id)).sort((a, b) => a.id.localeCompare(b.id));
  console.log(label, cards.length, createHash('sha256').update(JSON.stringify(cards)).digest('hex'));
}
fs.rmSync(tmp, { recursive: true, force: true });
