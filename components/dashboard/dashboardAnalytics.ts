/**
 * Pure analytics transforms for the student dashboard.
 *
 * Keeping the aggregation outside React makes every chart deterministic,
 * testable and honest about what has actually been recorded.
 */

import type { DebriefEntry } from '../StudyDebrief';
import type { StudyConfidenceLabel, StudyReflection, TopicMasteryV2, UnifiedMockResult } from '../../types';
import { STRATEGY_REGISTRY, type StudySessionRecord } from '../../utils/strategyRegistry';

export type DashboardRange = 'week' | 'month' | 'year';
export type ActivityMetric = 'sessions' | 'minutes';

export const CONFIDENCE_SCORE: Record<StudyConfidenceLabel, number> = {
  lost: 1,
  shaky: 2,
  okay: 3,
  good: 4,
  confident: 5,
};

export const CONFIDENCE_LABELS = ['Lost', 'Shaky', 'Okay', 'Good', 'Confident'] as const;

export interface RangeBounds {
  start: Date;
  end: Date;
  label: string;
}

export interface ActivityBucket {
  key: string;
  label: string;
  accessibleLabel: string;
  start: number;
  end: number;
  sessions: number;
  minutes: number;
}

export interface ConfidenceObservation {
  id: string;
  subject: string;
  timestamp: number;
  dateKey: string;
  score: number;
  label: StudyConfidenceLabel;
}

export interface RankedValue {
  id: string;
  label: string;
  value: number;
}

export interface RhythmDay {
  key: string;
  date: Date;
  sessions: number;
  minutes: number;
  isFuture: boolean;
}

export interface MasterySummary {
  notStarted: number;
  shaky: number;
  solid: number;
  total: number;
}

const DAY_MS = 86_400_000;

export function startOfLocalDay(value: Date): Date {
  return new Date(value.getFullYear(), value.getMonth(), value.getDate());
}

export function toLocalDateKey(value: Date): string {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, '0');
  const day = String(value.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export function parseDateKey(value: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return null;
  const parsed = new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function formatDayMonth(value: Date): string {
  return value.toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
}

export function getRangeBounds(range: DashboardRange, now = new Date()): RangeBounds {
  const today = startOfLocalDay(now);

  if (range === 'week') {
    const mondayOffset = (today.getDay() + 6) % 7;
    const start = new Date(today);
    start.setDate(today.getDate() - mondayOffset);
    const end = new Date(start);
    end.setDate(start.getDate() + 7);
    const finalDay = new Date(end.getTime() - DAY_MS);
    return {
      start,
      end,
      label: `${formatDayMonth(start)} – ${formatDayMonth(finalDay)}`,
    };
  }

  if (range === 'month') {
    const start = new Date(today.getFullYear(), today.getMonth(), 1);
    const end = new Date(today.getFullYear(), today.getMonth() + 1, 1);
    return {
      start,
      end,
      label: start.toLocaleDateString('en-IE', { month: 'long', year: 'numeric' }),
    };
  }

  const start = new Date(today.getFullYear(), 0, 1);
  const end = new Date(today.getFullYear() + 1, 0, 1);
  return { start, end, label: String(today.getFullYear()) };
}

function sessionTimestamp(session: StudySessionRecord): number | null {
  if (Number.isFinite(session.completedAt)) return session.completedAt;
  const parsed = parseDateKey(session.date);
  return parsed?.getTime() ?? null;
}

export function sessionIsInRange(session: StudySessionRecord, bounds: RangeBounds): boolean {
  const timestamp = sessionTimestamp(session);
  return timestamp !== null && timestamp >= bounds.start.getTime() && timestamp < bounds.end.getTime();
}

export function filterSessions(
  sessions: StudySessionRecord[],
  range: DashboardRange,
  subject = 'all',
  now = new Date(),
): StudySessionRecord[] {
  const bounds = getRangeBounds(range, now);
  return sessions.filter(session => (
    sessionIsInRange(session, bounds)
    && (subject === 'all' || session.subject === subject)
  ));
}

export function buildActivityBuckets(
  sessions: StudySessionRecord[],
  range: DashboardRange,
  subject = 'all',
  now = new Date(),
): ActivityBucket[] {
  const bounds = getRangeBounds(range, now);
  const buckets: ActivityBucket[] = [];

  if (range === 'year') {
    for (let month = 0; month < 12; month += 1) {
      const start = new Date(bounds.start.getFullYear(), month, 1);
      const end = new Date(bounds.start.getFullYear(), month + 1, 1);
      buckets.push({
        key: `${bounds.start.getFullYear()}-${String(month + 1).padStart(2, '0')}`,
        label: start.toLocaleDateString('en-IE', { month: 'short' }),
        accessibleLabel: start.toLocaleDateString('en-IE', { month: 'long', year: 'numeric' }),
        start: start.getTime(),
        end: end.getTime(),
        sessions: 0,
        minutes: 0,
      });
    }
  } else {
    const cursor = new Date(bounds.start);
    while (cursor < bounds.end) {
      const start = new Date(cursor);
      const end = new Date(cursor);
      end.setDate(end.getDate() + 1);
      buckets.push({
        key: toLocalDateKey(start),
        label: range === 'week'
          ? start.toLocaleDateString('en-IE', { weekday: 'short' })
          : String(start.getDate()),
        accessibleLabel: start.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' }),
        start: start.getTime(),
        end: end.getTime(),
        sessions: 0,
        minutes: 0,
      });
      cursor.setDate(cursor.getDate() + 1);
    }
  }

  for (const session of sessions) {
    if (subject !== 'all' && session.subject !== subject) continue;
    const timestamp = sessionTimestamp(session);
    if (timestamp === null || timestamp < bounds.start.getTime() || timestamp >= bounds.end.getTime()) continue;
    const bucket = buckets.find(item => timestamp >= item.start && timestamp < item.end);
    if (!bucket) continue;
    bucket.sessions += 1;
    bucket.minutes += Math.max(0, session.actualSeconds) / 60;
  }

  return buckets.map(bucket => ({ ...bucket, minutes: Math.round(bucket.minutes) }));
}

function confidenceLabelFromScore(score: number): StudyConfidenceLabel {
  if (score <= 1) return 'lost';
  if (score === 2) return 'shaky';
  if (score === 3) return 'okay';
  if (score === 4) return 'good';
  return 'confident';
}

function normaliseConfidenceLabel(value: unknown): StudyConfidenceLabel | null {
  if (typeof value !== 'string') return null;
  const clean = value.trim().toLowerCase() as StudyConfidenceLabel;
  return Object.hasOwn(CONFIDENCE_SCORE, clean) ? clean : null;
}

export function collectConfidenceObservations(
  sessions: StudySessionRecord[],
  debriefs: DebriefEntry[],
  reflections: StudyReflection[],
): ConfidenceObservation[] {
  const observations: ConfidenceObservation[] = [];

  for (const reflection of reflections) {
    const inferredLabel = normaliseConfidenceLabel(reflection.confidenceLabel)
      ?? normaliseConfidenceLabel(reflection.reflection);
    const inferredScore = reflection.confidenceAfter
      ?? (inferredLabel ? CONFIDENCE_SCORE[inferredLabel] : undefined);
    if (!inferredLabel || !inferredScore || inferredScore < 1 || inferredScore > 5) continue;
    observations.push({
      id: `reflection-${reflection.timestamp}`,
      subject: reflection.subjectName,
      timestamp: reflection.timestamp,
      dateKey: reflection.dateKey,
      score: inferredScore,
      label: inferredLabel,
    });
  }

  for (const debrief of debriefs) {
    if (!Number.isFinite(debrief.confidenceAfter)) continue;
    const parsed = parseDateKey(debrief.date);
    if (!parsed) continue;
    parsed.setHours(12);
    const score = Math.max(1, Math.min(5, Math.round(debrief.confidenceAfter)));
    observations.push({
      id: `debrief-${debrief.id}`,
      subject: debrief.subject,
      timestamp: parsed.getTime(),
      dateKey: debrief.date,
      score,
      label: confidenceLabelFromScore(score),
    });
  }

  for (const session of sessions) {
    const score = session.confidenceAfter
      ?? (session.confidenceLabel ? CONFIDENCE_SCORE[session.confidenceLabel] : undefined);
    const timestamp = sessionTimestamp(session);
    if (!score || timestamp === null || score < 1 || score > 5) continue;
    observations.push({
      id: `session-${session.id}`,
      subject: session.subject,
      timestamp,
      dateKey: session.date,
      score,
      label: session.confidenceLabel ?? confidenceLabelFromScore(score),
    });
  }

  // Session documents are the canonical source. Collapse an older reflection
  // recorded within five minutes of the same session so the chart never
  // double-counts one debrief during the schema transition.
  const deduplicated = new Map<string, ConfidenceObservation>();
  for (const observation of observations) {
    const fiveMinuteWindow = Math.round(observation.timestamp / 300_000);
    const key = `${observation.subject}|${observation.dateKey}|${fiveMinuteWindow}`;
    const existing = deduplicated.get(key);
    if (!existing || observation.id.startsWith('session-')) deduplicated.set(key, observation);
  }

  return [...deduplicated.values()].sort((a, b) => a.timestamp - b.timestamp);
}

export function confidenceInRange(
  observations: ConfidenceObservation[],
  range: DashboardRange,
  subject = 'all',
  now = new Date(),
): ConfidenceObservation[] {
  const bounds = getRangeBounds(range, now);
  return observations.filter(item => (
    item.timestamp >= bounds.start.getTime()
    && item.timestamp < bounds.end.getTime()
    && (subject === 'all' || item.subject === subject)
  ));
}

export function buildSubjectAllocation(sessions: StudySessionRecord[]): RankedValue[] {
  const totals = new Map<string, number>();
  for (const session of sessions) {
    totals.set(session.subject, (totals.get(session.subject) ?? 0) + Math.max(0, session.actualSeconds) / 60);
  }
  return [...totals.entries()]
    .map(([label, value]) => ({ id: label, label, value: Math.round(value) }))
    .sort((a, b) => b.value - a.value);
}

const LEGACY_STRATEGY_LABELS: Record<string, string> = {
  'past-papers': 'Past papers',
  'active-recall': 'Active Recall',
  're-reading': 'Re-reading notes',
  summarising: 'Summarising',
  teaching: 'Teaching / explaining',
  videos: 'Videos / resources',
  flashcards: 'Flashcards',
  other: 'Other',
};

export function buildStrategyUsage(
  sessions: StudySessionRecord[],
  debriefs: DebriefEntry[],
  range: DashboardRange,
  subject = 'all',
  now = new Date(),
): RankedValue[] {
  const totals = new Map<string, number>();
  const registry = new Map(STRATEGY_REGISTRY.map(item => [item.moduleId, item.strategyName]));
  const filteredSessions = filterSessions(sessions, range, subject, now);

  for (const session of filteredSessions) {
    for (const strategyId of new Set(session.strategiesShown ?? [])) {
      const label = registry.get(strategyId);
      if (label) totals.set(label, (totals.get(label) ?? 0) + 1);
    }
  }

  const bounds = getRangeBounds(range, now);
  for (const debrief of debriefs) {
    const parsed = parseDateKey(debrief.date);
    if (!parsed || parsed < bounds.start || parsed >= bounds.end) continue;
    if (subject !== 'all' && debrief.subject !== subject) continue;
    const label = LEGACY_STRATEGY_LABELS[debrief.strategy] ?? debrief.strategy;
    if (label) totals.set(label, (totals.get(label) ?? 0) + 1);
  }

  return [...totals.entries()]
    .map(([label, value]) => ({ id: label, label, value }))
    .sort((a, b) => b.value - a.value);
}

export function buildSessionMix(sessions: StudySessionRecord[]): RankedValue[] {
  const labels: Record<StudySessionRecord['sessionType'], string> = {
    'new-learning': 'New learning',
    practice: 'Practice',
    revision: 'Revision',
  };
  const totals: Record<StudySessionRecord['sessionType'], number> = {
    'new-learning': 0,
    practice: 0,
    revision: 0,
  };
  for (const session of sessions) totals[session.sessionType] += 1;
  return (Object.keys(totals) as StudySessionRecord['sessionType'][]).map(id => ({
    id,
    label: labels[id],
    value: totals[id],
  }));
}

export function buildStudyRhythm(
  sessions: StudySessionRecord[],
  now = new Date(),
  weeks = 13,
): RhythmDay[][] {
  const today = startOfLocalDay(now);
  const currentMonday = new Date(today);
  currentMonday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
  const start = new Date(currentMonday);
  start.setDate(currentMonday.getDate() - ((weeks - 1) * 7));

  const totals = new Map<string, { sessions: number; minutes: number }>();
  for (const session of sessions) {
    const current = totals.get(session.date) ?? { sessions: 0, minutes: 0 };
    current.sessions += 1;
    current.minutes += Math.max(0, session.actualSeconds) / 60;
    totals.set(session.date, current);
  }

  return Array.from({ length: weeks }, (_, weekIndex) => (
    Array.from({ length: 7 }, (_unused, dayIndex) => {
      const date = new Date(start);
      date.setDate(start.getDate() + (weekIndex * 7) + dayIndex);
      const key = toLocalDateKey(date);
      const value = totals.get(key) ?? { sessions: 0, minutes: 0 };
      return {
        key,
        date,
        sessions: value.sessions,
        minutes: Math.round(value.minutes),
        isFuture: date > today,
      };
    })
  ));
}

export function buildMasterySummary(topicMastery: TopicMasteryV2 | undefined, subject = 'all'): MasterySummary {
  const summary: MasterySummary = { notStarted: 0, shaky: 0, solid: 0, total: 0 };
  if (!topicMastery) return summary;

  const add = (confidence: 'not-started' | 'shaky' | 'solid') => {
    if (confidence === 'not-started') summary.notStarted += 1;
    else summary[confidence] += 1;
    summary.total += 1;
  };

  for (const entry of Object.values(topicMastery.topics)) {
    if (subject !== 'all' && entry.subjectName !== subject) continue;
    add(entry.confidence);
  }
  for (const [subjectName, topics] of Object.entries(topicMastery.unresolved)) {
    if (subject !== 'all' && subjectName !== subject) continue;
    for (const entry of Object.values(topics)) add(entry.confidence);
  }
  return summary;
}

export function buildMockSeries(mocks: UnifiedMockResult[]): UnifiedMockResult[] {
  return [...mocks]
    .filter(mock => Number.isFinite(mock.totalPoints) && mock.date && Number.isFinite(new Date(`${mock.date}T12:00:00`).getTime()))
    .sort((a, b) => a.date.localeCompare(b.date));
}

export function averageConfidence(observations: ConfidenceObservation[]): number | null {
  if (observations.length === 0) return null;
  return observations.reduce((sum, item) => sum + item.score, 0) / observations.length;
}
