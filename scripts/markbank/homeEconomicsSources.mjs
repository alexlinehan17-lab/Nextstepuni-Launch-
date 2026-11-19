/** Deferred Home Economics has two question booklets, one reviewed scheme. */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
let sources;
let metadata;

/** Committed archive/task identities can be checked without the optional PDFs. */
export function homeEconomicsSourceMetadataMap(review) {
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
    if (!/^[a-f0-9]{64}$/.test(source.sha256)) throw new Error(`${key}: invalid ${kind} source hash`);
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

/** Generators always verify the original bytes; missing originals still fail. */
export function homeEconomicsSourceMap(review, readSource = path => readFileSync(resolve(root, path))) {
  const result = homeEconomicsSourceMetadataMap(review);
  for (const kind of ['a', 'bc', 'scheme']) {
    const source = review.sources[kind];
    if (createHash('sha256').update(readSource(source.path)).digest('hex') !== source.sha256) {
      throw new Error(`${review.year}-hl-deferred: ${kind} bytes differ from visual review`);
    }
  }
  return result;
}

function loadSources(mapReview) {
  const result = new Map();
  for (const year of [2022, 2023]) {
    const review = JSON.parse(readFileSync(resolve(root, `scripts/markbank/authoring/home-economics/${year}-hl-deferred-review.json`)));
    for (const [id, source] of mapReview(review)) {
      if (result.has(id)) throw new Error(`Duplicate reviewed Home Economics task: ${id}`);
      result.set(id, source);
    }
  }
  return result;
}

const findSource = (map, cardId) => {
  const source = map.get(cardId);
  if (!source) throw new Error(`Deferred Home Economics card lacks reviewed sources: ${cardId}`);
  return source;
};

export function reviewedHomeEconomicsSource(cardId) {
  if (!/^he-\d{4}-(?:hl|ol)-deferred-/.test(cardId)) return undefined;
  sources ??= loadSources(homeEconomicsSourceMap);
  return findSource(sources, cardId);
}

export function reviewedHomeEconomicsSourceMetadata(cardId) {
  if (!/^he-\d{4}-(?:hl|ol)-deferred-/.test(cardId)) return undefined;
  metadata ??= loadSources(homeEconomicsSourceMetadataMap);
  return findSource(metadata, cardId);
}
