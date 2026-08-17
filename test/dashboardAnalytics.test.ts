import { describe, expect, test } from 'vitest';
import type { StudyReflection, TopicMasteryV2 } from '@/types';
import type { DebriefEntry } from '@/components/StudyDebrief';
import type { StudySessionRecord } from '@/utils/strategyRegistry';
import {
  buildActivityBuckets,
  buildMasterySummary,
  buildStrategyUsage,
  collectConfidenceObservations,
  filterSessions,
  getRangeBounds,
} from '@/components/dashboard/dashboardAnalytics';

const NOW = new Date(2026, 7, 14, 12); // Friday 14 August 2026

function session(overrides: Partial<StudySessionRecord> = {}): StudySessionRecord {
  const completedAt = new Date(2026, 7, 14, 12).getTime();
  return {
    id: 'session-1',
    date: '2026-08-14',
    subject: 'Biology',
    sessionType: 'practice',
    plannedMinutes: 25,
    actualSeconds: 1_500,
    startedAt: completedAt - 1_500_000,
    completedAt,
    pointsEarned: 20,
    hadReflection: true,
    ...overrides,
  };
}

describe('student dashboard analytics', () => {
  test('uses calendar week, month and year boundaries', () => {
    expect(getRangeBounds('week', NOW).start).toEqual(new Date(2026, 7, 10));
    expect(getRangeBounds('week', NOW).end).toEqual(new Date(2026, 7, 17));
    expect(getRangeBounds('month', NOW).start).toEqual(new Date(2026, 7, 1));
    expect(getRangeBounds('month', NOW).end).toEqual(new Date(2026, 8, 1));
    expect(getRangeBounds('year', NOW).start).toEqual(new Date(2026, 0, 1));
    expect(getRangeBounds('year', NOW).end).toEqual(new Date(2027, 0, 1));
  });

  test('updates the matching activity bar and supports sessions/minutes from one source', () => {
    const records = [
      session(),
      session({ id: 'session-2', actualSeconds: 600, completedAt: new Date(2026, 7, 14, 18).getTime() }),
      session({ id: 'session-3', date: '2026-08-12', subject: 'English', completedAt: new Date(2026, 7, 12, 18).getTime() }),
    ];
    const buckets = buildActivityBuckets(records, 'week', 'all', NOW);
    const friday = buckets.find(bucket => bucket.key === '2026-08-14');
    expect(friday).toMatchObject({ sessions: 2, minutes: 35 });
    expect(buckets.reduce((sum, bucket) => sum + bucket.sessions, 0)).toBe(3);
    expect(filterSessions(records, 'week', 'Biology', NOW)).toHaveLength(2);
  });

  test('stores one canonical confidence point when a session and its reflection overlap', () => {
    const completedAt = new Date(2026, 7, 14, 12).getTime();
    const records = [session({ confidenceAfter: 4, confidenceLabel: 'good', completedAt })];
    const reflections: StudyReflection[] = [{
      dateKey: '2026-08-14',
      blockId: 'reflection-1',
      subjectName: 'Biology',
      sessionType: 'practice',
      reflection: 'Good',
      pointsEarned: 10,
      timestamp: completedAt - 30_000,
      confidenceAfter: 4,
      confidenceLabel: 'good',
      reflectionMode: 'quick',
    }];
    const observations = collectConfidenceObservations(records, [], reflections);
    expect(observations).toHaveLength(1);
    expect(observations[0]).toMatchObject({ subject: 'Biology', score: 4, label: 'good' });
    expect(observations[0].id).toBe('session-session-1');
  });

  test('keeps historic debrief confidence and technique data useful', () => {
    const debrief: DebriefEntry = {
      id: 'old-1',
      date: '2026-08-13',
      subject: 'English',
      sessionType: 'revision',
      durationMinutes: 30,
      hardestTopic: 'Comparative study',
      strategy: 'active-recall',
      confidenceBefore: 2,
      confidenceAfter: 3,
      whatWorked: '',
    };
    expect(collectConfidenceObservations([], [debrief], [])[0]).toMatchObject({ score: 3, label: 'okay' });
    expect(buildStrategyUsage([], [debrief], 'week', 'all', NOW)).toEqual([
      { id: 'Active Recall', label: 'Active Recall', value: 1 },
    ]);
  });

  test('filters canonical and unresolved topic readiness by subject', () => {
    const mastery: TopicMasteryV2 = {
      schemaVersion: 2,
      topics: {
        'bio::cells': {
          subjectId: 'biology', subjectName: 'Biology', specificationId: 'bio', topicId: 'cells', topicName: 'Cells',
          confidence: 'solid', updatedAt: 1, source: 'manual',
        },
        'eng::poetry': {
          subjectId: 'english', subjectName: 'English', specificationId: 'eng', topicId: 'poetry', topicName: 'Poetry',
          confidence: 'shaky', updatedAt: 1, source: 'manual',
        },
      },
      unresolved: {
        Biology: {
          Genetics: { confidence: 'not-started', updatedAt: 1, source: 'import' },
        },
      },
    };
    expect(buildMasterySummary(mastery, 'Biology')).toEqual({ notStarted: 1, shaky: 0, solid: 1, total: 2 });
    expect(buildMasterySummary(mastery, 'all')).toEqual({ notStarted: 1, shaky: 1, solid: 1, total: 3 });
  });
});
