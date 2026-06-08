/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards Catch-Up Lane recovery content: every card must map to a real
 * curriculum subject + subtopic id (the picker filters on these), be
 * well-formed, and have a unique id.
 */
import { describe, it, expect } from 'vitest';
import { RECOVERY_CARDS } from '../catchUpLaneData';
import { CURRICULUM } from '../curriculum';

const validTopicIds = new Set(CURRICULUM.flatMap((s) => s.strands.flatMap((st) => st.subtopics.map((t) => t.id))));
const validSubjectIds = new Set(CURRICULUM.map((s) => s.id));

describe('Catch-Up Lane recovery cards', () => {
  it('every card maps to a real curriculum subject + subtopic', () => {
    for (const c of RECOVERY_CARDS) {
      expect(validSubjectIds.has(c.subjectId), `${c.id}: unknown subjectId "${c.subjectId}"`).toBe(true);
      expect(validTopicIds.has(c.topicId), `${c.id}: topicId "${c.topicId}" not in curriculum`).toBe(true);
    }
  });

  it('every card is well-formed', () => {
    for (const c of RECOVERY_CARDS) {
      expect(c.gist.trim().length, `${c.id}: empty gist`).toBeGreaterThan(0);
      expect(c.oneMove.label.trim().length && c.oneMove.text.trim().length, `${c.id}: empty oneMove`).toBeTruthy();
      expect(c.check.prompt.trim().length, `${c.id}: empty prompt`).toBeGreaterThan(0);
      expect(c.check.modelAnswer.trim().length, `${c.id}: empty modelAnswer`).toBeGreaterThan(0);
      expect(c.check.needed.length, `${c.id}: <2 needed points`).toBeGreaterThanOrEqual(2);
      expect(c.source.trim().length, `${c.id}: missing source`).toBeGreaterThan(0);
      expect(c.marksWeight, `${c.id}: bad marksWeight`).toBeGreaterThan(0);
    }
  });

  it('all card ids are unique', () => {
    const ids = RECOVERY_CARDS.map((c) => c.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('covers the four target subjects', () => {
    const subs = new Set(RECOVERY_CARDS.map((c) => c.subjectId));
    for (const s of ['biology', 'english', 'mathematics', 'geography']) {
      expect(subs.has(s), `no cards for ${s}`).toBe(true);
    }
  });
});
