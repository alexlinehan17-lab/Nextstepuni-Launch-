/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic-tag ↔ anchor numbering contract. Every tagged question must be
 * joinable to a paper anchor by `n` — either the committed answer-map sidecar
 * (scripts/paper-trail/answers) or the hosted paper-anchors fallback
 * (public/paper-anchors). A tag numbered against a different question run
 * renders the Topic Atlas card's honest fallback at best (split-spec Biology
 * Paper 2 shipped months of "can't be shown as a crop yet" this way) and a
 * WRONG crop at worst, so a fully unjoinable paper fails the build.
 */
import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

const ROOT = path.resolve(__dirname, '..');
const TAGS = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'data/paperTrail/paperTopicTags.json'), 'utf8'),
) as { subjectId: string; year: number; fileid: string; q: { n: string }[] }[];

const anchorNs = (year: number, fileid: string): Set<string> | null => {
  const out = new Set<string>();
  for (const p of [
    path.join(ROOT, 'scripts/paper-trail/answers', String(year), `${fileid}.json`),
    path.join(ROOT, 'public/paper-anchors', String(year), `${fileid}.json`),
  ]) {
    if (!fs.existsSync(p)) continue;
    try {
      const m = JSON.parse(fs.readFileSync(p, 'utf8')) as { q?: { n: string }[] };
      for (const q of m.q ?? []) out.add(q.n);
    } catch {
      // unreadable candidate — the other source may still cover it
    }
  }
  return out.size ? out : null;
};

describe('topic tags join their paper anchors', () => {
  it('dictionary runtime expands exactly to the committed full audit artifact', () => {
    expect(PAPER_TOPIC_TAGS).toEqual(TAGS);
  });

  it('no tagged paper is fully unjoinable by question number', () => {
    const broken: string[] = [];
    let anchored = 0;
    for (const t of TAGS) {
      const ns = anchorNs(t.year, t.fileid);
      if (!ns) continue; // no anchor source at all — vault already falls back honestly
      anchored++;
      if (!t.q.some(q => ns.has(q.n))) {
        broken.push(`${t.subjectId} ${t.year} ${t.fileid}: tags ${t.q.map(q => q.n).join(',')} vs anchors ${[...ns].join(',')}`);
      }
    }
    expect(anchored).toBeGreaterThan(1000); // the join is real, not vacuous
    expect(broken, broken.slice(0, 5).join('\n')).toEqual([]);
  });
});
