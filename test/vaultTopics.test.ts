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
  frequencyFor,
  topicsForPaper,
  browseTopicIdsForQuestion,
  paperKeyOf,
} from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

// A real subject + a couple of its busiest topics to drive the invariants.
const subjects = taggedSubjects();
const sampleSubject = subjects.find(s => topicsForSubject(s).length > 0)!;
const sampleTopics = topicsForSubject(sampleSubject).slice(0, 3);

describe('Topic Vault feed primitives', () => {
  it('keeps written and aural paper identities separate', () => {
    expect(paperKeyOf('Exam Paper')).toBe('single');
    expect(paperKeyOf('Aural Paper')).toBe('aural');
    expect(paperKeyOf('Listening Comprehension')).toBe('aural');
  });

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

  it('every sibling actually carries the requested canonical or exam topic', () => {
    for (const t of sampleTopics) {
      for (const s of siblingsFor(sampleSubject, t.subtopicId)) {
        const paper = topicsForPaper(s.subjectId, s.year, s.level, s.lang, s.fileid)!;
        const q = paper.q.find(x => x.n === s.n)!;
        expect(
          q.primary === t.subtopicId ||
          q.secondary === t.subtopicId ||
          browseTopicIdsForQuestion(paper, q).includes(t.subtopicId),
          `${t.subtopicId} mismatched`,
        ).toBe(true);
      }
    }
  });

  it('topicsForSubject count equals distinct printed siblings, not translated editions', () => {
    for (const t of sampleTopics) {
      const printed = new Set(
        siblingsFor(sampleSubject, t.subtopicId)
          .map(s => `${s.level}|${s.year}|${s.paperKey}|${s.n}`),
      );
      expect(printed.size, `${t.subtopicId} count drift`).toBe(t.count);
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
    const keys = out.map(q => `${q.level}|${q.year}|${q.paperKey}|${q.n}`);
    expect(new Set(keys).size).toBe(keys.length);
  });

  it('unknown subject / topic yields an empty feed, never throws', () => {
    expect(siblingsFor('not-a-subject', 'nope')).toEqual([]);
    expect(topicsForSubject('not-a-subject')).toEqual([]);
    expect(questionsForTopics('not-a-subject', null)).toEqual([]);
  });

  // A real (subject, level, paperKey, subtopic) slice to drive frequency.
  const sampleTag = PAPER_TOPIC_TAGS.find(p => p.q.length > 0)!;
  const sampleSub = sampleTag.q[0].primary;

  it('frequencyFor is honest: yearsWith ⊆ tagged years, distinct, newest-first', () => {
    const f = frequencyFor(sampleTag.subjectId, sampleTag.level, sampleTag.paperKey, sampleSub);
    expect(f.yearsWith.length).toBeLessThanOrEqual(f.totalYears);
    expect(new Set(f.yearsWith).size).toBe(f.yearsWith.length); // distinct
    for (let i = 1; i < f.yearsWith.length; i++) {
      expect(f.yearsWith[i - 1]).toBeGreaterThan(f.yearsWith[i]); // strictly descending
    }
    // The sample's own year must be among the hits for its own subtopic.
    expect(f.yearsWith).toContain(sampleTag.year);
    expect(f.totalYears).toBeGreaterThan(0);
  });

  it('frequencyFor on an unexamined subtopic reports 0 hits but a real denominator', () => {
    const f = frequencyFor(sampleTag.subjectId, sampleTag.level, sampleTag.paperKey, 'not-a-subtopic');
    expect(f.yearsWith).toEqual([]);
    expect(f.totalYears).toBeGreaterThan(0); // the pool still exists
  });

  it('topicsForPaper resolves a real paper and returns null for an unknown one', () => {
    const got = topicsForPaper(sampleTag.subjectId, sampleTag.year, sampleTag.level, sampleTag.lang, sampleTag.fileid);
    expect(got).not.toBeNull();
    expect(got!.q.length).toBe(sampleTag.q.length);
    expect(topicsForPaper('nope', 1900, 'higher', 'ev', 'nope.pdf')).toBeNull();
  });
});
