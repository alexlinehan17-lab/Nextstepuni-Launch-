/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Vault feed primitives — siblingsFor / topicsForSubject / questionsForTopics.
 * These drive the "every question on a topic, newest first" feed, so their
 * contracts are load-bearing: a regression here silently reorders, drops, or
 * double-counts questions in front of students. Tested as INVARIANTS against
 * the real committed tags so the pins hold as the tag corpus grows.
 */

import { describe, it, expect } from 'vitest';
import {
  siblingsFor,
  topicsForSubject,
  questionsForTopics,
  taggedSubjects,
} from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

// A real subject + a couple of its busiest topics to drive the invariants.
const subjects = taggedSubjects();
const sampleSubject = subjects.find(s => topicsForSubject(s).length > 0)!;
const sampleTopics = topicsForSubject(sampleSubject).slice(0, 3);

describe('Topic Vault feed primitives', () => {
  it('there is real tag data to test against', () => {
    expect(subjects.length).toBeGreaterThan(0);
    expect(sampleTopics.length).toBeGreaterThan(0);
  });

  it('siblingsFor returns newest-year-first', () => {
    for (const t of sampleTopics) {
      const sibs = siblingsFor(sampleSubject, t.subtopicId);
      for (let i = 1; i < sibs.length; i++) {
        expect(sibs[i - 1].year, `${t.subtopicId} out of year order`).toBeGreaterThanOrEqual(sibs[i].year);
      }
    }
  });

  it('every sibling actually carries the requested topic (primary or secondary)', () => {
    const key = (s: { level: string; lang: string; year: number; fileid: string }) =>
      `${s.level}|${s.lang}|${s.year}|${s.fileid}`;
    const bySlice = new Map<string, (typeof PAPER_TOPIC_TAGS)[number]>();
    for (const p of PAPER_TOPIC_TAGS) bySlice.set(key(p), p);
    for (const t of sampleTopics) {
      for (const s of siblingsFor(sampleSubject, t.subtopicId)) {
        const paper = bySlice.get(key(s))!;
        const q = paper.q.find(x => x.n === s.n)!;
        expect(q.primary === t.subtopicId || q.secondary === t.subtopicId, `${t.subtopicId} mismatched`).toBe(true);
      }
    }
  });

  it("topicsForSubject count == siblingsFor length (the docs promise they line up)", () => {
    for (const t of sampleTopics) {
      expect(siblingsFor(sampleSubject, t.subtopicId).length, `${t.subtopicId} count drift`).toBe(t.count);
    }
  });

  it('topicsForSubject is busiest-first', () => {
    const all = topicsForSubject(sampleSubject);
    for (let i = 1; i < all.length; i++) {
      expect(all[i - 1].count).toBeGreaterThanOrEqual(all[i].count);
    }
  });

  it('questionsForTopics dedups by paper+question across overlapping topics', () => {
    const ids = sampleTopics.map(t => t.subtopicId);
    const out = questionsForTopics(sampleSubject, ids);
    const keys = out.map(q => `${q.level}|${q.lang}|${q.year}|${q.fileid}|${q.n}`);
    expect(new Set(keys).size).toBe(keys.length);
  });

  it('unknown subject / topic yields an empty feed, never throws', () => {
    expect(siblingsFor('not-a-subject', 'nope')).toEqual([]);
    expect(topicsForSubject('not-a-subject')).toEqual([]);
    expect(questionsForTopics('not-a-subject', null)).toEqual([]);
  });
});
