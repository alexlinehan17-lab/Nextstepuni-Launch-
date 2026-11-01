/** Resolve deferred Physics cards from their reviewed source pair, never a Q-number match. */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
let sources;

export function reviewedPhysicsSource(cardId) {
  if (!/^phys-\d{4}-(?:hl|ol)-deferred-/.test(cardId)) return undefined;
  if (!sources) {
    sources = new Map();
    const audit = JSON.parse(readFileSync(resolve(root, 'scripts/markbank/authored/physics-review-audit.json')));
    for (const [key, review] of Object.entries(audit.sittings)) {
      if (review.sitting !== 'deferred') continue;
      if (!/^\d{4}-(?:hl|ol)-deferred$/.test(key) || review.status !== 'reviewed') {
        throw new Error(`Unreviewed Physics sitting: ${key}`);
      }
      const [year, level] = key.split('-');
      const fileid = `LC021${level === 'hl' ? 'A' : 'G'}LP000EV.pdf`;
      for (const [kind, folder] of [['paper', 'deferredexams'], ['scheme', 'deferredmarkingschemes']]) {
        const source = review.sources[kind];
        const expected = `paper-trail-corpus/${folder}/${year}/${source.fileid}`;
        if (source.path !== expected || source.fileid !== fileid) {
          throw new Error(`${key}: wrong ${kind} archive identity`);
        }
        const bytes = readFileSync(resolve(root, expected));
        if (createHash('sha256').update(bytes).digest('hex') !== source.sha256) {
          throw new Error(`${key}: ${kind} bytes differ from visual review`);
        }
      }
      const source = {
        sitting: 'deferred', lang: 'ev',
        paperFileid: review.sources.paper.fileid.replace(/\.pdf$/, '-deferred.pdf'),
        schemeFileid: review.sources.scheme.fileid.replace(/\.pdf$/, '-deferred.pdf'),
      };
      for (const task of review.tasks) {
        if (!task.id.startsWith(`phys-${key}-`) || task.status !== 'carded' || sources.has(task.id)) {
          throw new Error(`${key}: invalid deferred task ${task.id}`);
        }
        sources.set(task.id, source);
      }
    }
  }
  const source = sources.get(cardId);
  if (!source) throw new Error(`Deferred Physics card lacks reviewed sources: ${cardId}`);
  return source;
}
