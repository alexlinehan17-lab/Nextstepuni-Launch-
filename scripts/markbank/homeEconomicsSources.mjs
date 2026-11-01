/** Deferred Home Economics has two question booklets, one reviewed scheme. */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
let sources;

export function homeEconomicsSourceMap(review, readSource = path => readFileSync(resolve(root, path))) {
  const key = `${review.year}-hl-deferred`;
  if (review.level !== 'higher' || review.sitting !== 'deferred' || review.language !== 'ev'
      || !review.visualSweep || !review.status.includes('all-source-pages-visually-reviewed')) {
    throw new Error(`Unreviewed Home Economics sitting: ${key}`);
  }
  for (const [kind, component, folder] of [['a', '014', 'deferredexams'], ['bc', '039', 'deferredexams'], ['scheme', '000', 'deferredmarkingschemes']]) {
    const source = review.sources[kind];
    const fileid = `LC098ALP${component}EV.pdf`;
    const expected = `paper-trail-corpus/${folder}/${review.year}/${fileid}`;
    if (source?.path !== expected || source.fileid !== fileid) throw new Error(`${key}: wrong ${kind} archive identity`);
    if (createHash('sha256').update(readSource(expected)).digest('hex') !== source.sha256) {
      throw new Error(`${key}: ${kind} bytes differ from visual review`);
    }
  }
  const result = new Map();
  for (const task of review.tasks) {
    if (!task.id.startsWith(`he-${key}-s${task.section.toLowerCase()}-`) || task.status !== 'carded'
        || !['A', 'B', 'C'].includes(task.section) || result.has(task.id)
        || !task.questionRef.endsWith(' — Deferred sitting')) throw new Error(`${key}: invalid deferred task ${task.id}`);
    result.set(task.id, {
      sitting: 'deferred', lang: 'ev',
      paperFileid: review.sources[task.section === 'A' ? 'a' : 'bc'].fileid.replace(/\.pdf$/, '-deferred.pdf'),
      schemeFileid: review.sources.scheme.fileid.replace(/\.pdf$/, '-deferred.pdf'),
    });
  }
  return result;
}

export function reviewedHomeEconomicsSource(cardId) {
  if (!/^he-\d{4}-(?:hl|ol)-deferred-/.test(cardId)) return undefined;
  if (!sources) {
    const review = JSON.parse(readFileSync(resolve(root, 'scripts/markbank/authoring/home-economics/2023-hl-deferred-review.json')));
    sources = homeEconomicsSourceMap(review);
  }
  const source = sources.get(cardId);
  if (!source) throw new Error(`Deferred Home Economics card lacks reviewed sources: ${cardId}`);
  return source;
}
