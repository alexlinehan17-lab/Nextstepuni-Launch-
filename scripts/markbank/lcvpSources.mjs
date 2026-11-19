/** LCVP main and deferred archives reuse the same SEC filenames. */
import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const sourceMaps = new Map();
const fileid = 'LC462CLP000EV.pdf';
const schemePath = year => `examiner-reports/lcvp/schemes/${year}-cl-deferred.md`;

/** Bind a completed visual census to its exact original archive bytes.
 * This validates source identity, not the correctness of authored answers. */
export function lcvpSourceMap(review, readSource = path => readFileSync(resolve(root, path))) {
  const key = `${review?.year}-cl-deferred`;
  if (!Number.isInteger(review?.year) || review.year < 2022 || review.year > 9999
      || review.level !== 'common' || review.sitting !== 'deferred' || review.language !== 'ev'
      || typeof review.visualSweep?.paper !== 'string' || !review.visualSweep.paper.trim()
      || typeof review.visualSweep?.writtenScheme !== 'string' || !review.visualSweep.writtenScheme.trim()
      || !Number.isInteger(review.manualOriginalLeaves) || review.manualOriginalLeaves < 1
      || !Array.isArray(review.tasks) || review.tasks.length === 0
      || review.manualPricedTasks !== review.tasks.length || !Array.isArray(review.sources)) {
    throw new Error(`Unreviewed LCVP deferred sitting: ${key}`);
  }
  for (const kind of ['deferredexams', 'deferredmarkingschemes']) {
    const matches = review.sources.filter(source => source.kind === kind);
    const source = matches[0];
    const expected = `paper-trail-corpus/${kind}/${review.year}/${fileid}`;
    if (matches.length !== 1 || source.year !== review.year
        || source.path !== expected || source.fileid !== fileid) {
      throw new Error(`${key}: wrong ${kind} archive identity`);
    }
    if (createHash('sha256').update(readSource(expected)).digest('hex') !== source.sha256) {
      throw new Error(`${key}: ${kind} bytes differ from visual review`);
    }
  }
  const result = new Map();
  for (const task of review.tasks) {
    if (typeof task.id !== 'string' || !task.id.startsWith(`lcvp-${key}-`)
        || task.id === `lcvp-${key}-` || result.has(task.id)
        || typeof task.questionRef !== 'string' || !task.questionRef.endsWith(' — Deferred sitting')) {
      throw new Error(`${key}: invalid deferred task ${task.id}`);
    }
    result.set(task.id, {
      year: review.year, sitting: 'deferred', lang: 'ev',
      paperFileid: fileid.replace(/\.pdf$/, '-deferred.pdf'),
      schemeFileid: fileid.replace(/\.pdf$/, '-deferred.pdf'),
      schemeTextPath: schemePath(review.year),
    });
  }
  return result;
}

export function reviewedLcvpSource(cardOrId) {
  const card = typeof cardOrId === 'string' ? undefined : cardOrId;
  const cardId = card?.id ?? cardOrId;
  if (!/^lcvp-.*-deferred-/.test(cardId)) {
    if (card && /\bdeferred\b/i.test(card.questionRef ?? '')) {
      throw new Error(`Deferred LCVP citation lacks a deferred identity: ${cardId}`);
    }
    return undefined;
  }
  const match = /^lcvp-(\d{4})-cl-deferred-.+$/.exec(cardId);
  if (!match) throw new Error(`Invalid deferred LCVP identity: ${cardId}`);
  const year = Number(match[1]);
  if (card && (card.year !== year || card.level !== 'common'
      || !card.questionRef?.endsWith(' — Deferred sitting'))) {
    throw new Error(`Deferred LCVP card metadata differs: ${cardId}`);
  }
  if (!sourceMaps.has(year)) {
    const path = resolve(root, `scripts/markbank/authoring/lcvp/${year}-cl-deferred-review.json`);
    if (!existsSync(path)) throw new Error(`Deferred LCVP card lacks reviewed sources: ${cardId}`);
    const review = JSON.parse(readFileSync(path, 'utf8'));
    if (review.year !== year) throw new Error(`Deferred LCVP review year differs: ${cardId}`);
    sourceMaps.set(year, lcvpSourceMap(review));
  }
  const source = sourceMaps.get(year).get(cardId);
  if (!source) throw new Error(`Deferred LCVP card lacks reviewed sources: ${cardId}`);
  return source;
}

/** A missing deferred transcript must never fall back to the June scheme. */
export function readLcvpDeferredScheme(source, readText = path => readFileSync(resolve(root, path), 'utf8')) {
  if (source.sitting !== 'deferred' || source.schemeTextPath !== schemePath(source.year)) {
    throw new Error('Invalid deferred LCVP scheme transcript identity');
  }
  let text;
  try { text = readText(source.schemeTextPath); }
  catch { throw new Error(`Missing deferred LCVP scheme transcript: ${source.schemeTextPath}`); }
  if (typeof text !== 'string' || !text.trim()) {
    throw new Error(`Empty deferred LCVP scheme transcript: ${source.schemeTextPath}`);
  }
  return text;
}
