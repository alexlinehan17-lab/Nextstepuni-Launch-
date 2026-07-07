/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic-tag ↔ curriculum integrity. The Topic Vault resolves every tag's
 * subtopic id against curriculum.ts; an orphaned id would silently drop
 * questions from the vault (or label them with a raw id). This pins the
 * contract so taxonomy restructuring can't strand the 5,306+ tags.
 */

import { describe, it, expect } from 'vitest';
import { CURRICULUM } from '../curriculum';
import { PAPER_TOPIC_TAGS, TOPIC_LABELS } from '../data/paperTrail/topicTags';

const curriculumIds = new Set(
  CURRICULUM.flatMap(s => s.strands.flatMap(st => st.subtopics.map(t => t.id))),
);

describe('topic-tag integrity', () => {
  it('every tag id resolves to a curriculum subtopic', () => {
    const orphans = new Set<string>();
    for (const p of PAPER_TOPIC_TAGS) {
      for (const q of p.q) {
        if (!curriculumIds.has(q.primary)) orphans.add(q.primary);
        if (q.secondary && !curriculumIds.has(q.secondary)) orphans.add(q.secondary);
      }
    }
    expect([...orphans]).toEqual([]);
  });

  it('every tag id has a display label', () => {
    const unlabeled = new Set<string>();
    for (const p of PAPER_TOPIC_TAGS) {
      for (const q of p.q) {
        if (!TOPIC_LABELS[q.primary]) unlabeled.add(q.primary);
        if (q.secondary && !TOPIC_LABELS[q.secondary]) unlabeled.add(q.secondary);
      }
    }
    expect([...unlabeled]).toEqual([]);
  });

  it('curriculum labels are well-formed (balanced parens, no stray whitespace)', () => {
    const bad: string[] = [];
    for (const s of CURRICULUM) {
      for (const st of s.strands) {
        for (const t of st.subtopics) {
          const open = (t.name.match(/\(/g) ?? []).length;
          const close = (t.name.match(/\)/g) ?? []).length;
          if (open !== close || t.name !== t.name.trim() || t.name.includes('  ')) {
            bad.push(`${t.id}: ${t.name}`);
          }
        }
      }
    }
    expect(bad).toEqual([]);
  });
});
