/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import type { TopicMasteryMap } from '../types';
import {
  migrateTopicMastery,
  mergeTopicMasteryV2,
  projectTopicMastery,
  upsertCanonicalMastery,
} from '../services/topicMasteryMigration';

const legacy: TopicMasteryMap = {
  Biology: {
    'Unit One: The Study of Life': { confidence: 'solid', updatedAt: 10, source: 'manual' },
    'My own revision topic': { confidence: 'shaky', updatedAt: 11, source: 'manual' },
  },
};

describe('topic mastery v2 migration', () => {
  it('maps exact cohort topics and retains custom topics without loss', () => {
    const migrated = migrateTopicMastery(legacy, '2026-06-05');
    expect(Object.values(migrated.topics)).toEqual(expect.arrayContaining([
      expect.objectContaining({ specificationId: 'biology:legacy-current', topicName: 'Unit One: The Study of Life' }),
    ]));
    expect(migrated.unresolved.Biology['My own revision topic']).toEqual(legacy.Biology['My own revision topic']);
    expect(projectTopicMastery(migrated)).toEqual(legacy);
  });

  it('does not incorrectly carry an outgoing label into a redeveloped cohort', () => {
    const migrated = migrateTopicMastery(legacy, '2027-06-05');
    expect(Object.keys(migrated.topics)).toHaveLength(0);
    expect(projectTopicMastery(migrated)).toEqual(legacy);
  });

  it('stores canonical updates by stable specification and topic ids', () => {
    const updated = upsertCanonicalMastery(
      migrateTopicMastery(undefined, '2027-06-05'),
      'Biology',
      'Scientific knowledge',
      { confidence: 'solid', updatedAt: 20, source: 'manual' },
      '2027-06-05',
    );
    const entry = Object.values(updated.topics)[0];
    expect(entry).toMatchObject({ specificationId: 'biology:2027', topicId: 'bio-u1', confidence: 'solid' });
  });

  it('reconciles later legacy writes and keeps the newest record', () => {
    const original = migrateTopicMastery(legacy, '2026-06-05');
    const later = migrateTopicMastery({ Biology: {
      'Unit One: The Study of Life': { confidence: 'shaky', updatedAt: 30, source: 'debrief' },
    } }, '2026-06-05');
    const merged = mergeTopicMasteryV2(original, later);
    expect(Object.values(merged.topics)[0].confidence).toBe('shaky');
    expect(merged.unresolved.Biology['My own revision topic']).toBeDefined();
  });
});
