import { type UnifiedMockResult } from '../types';
import { type ProgressDocument } from './progressRepository';

type LegacyMock = {
  id?: string;
  label?: string;
  date?: string;
  grades?: UnifiedMockResult['entries'];
  subject?: string;
  grade?: string;
  level?: string;
  totalPoints?: number;
  timestamp?: number;
};

const today = () => new Date().toISOString().split('T')[0];

function legacyToUnified(mock: LegacyMock, source: 'points-passport' | 'war-room', index: number): UnifiedMockResult {
  const entries = mock.grades
    ?? (mock.subject
      ? [{ subjectName: mock.subject, grade: mock.grade ?? '', level: mock.level ?? 'higher' }]
      : []);
  const timestamp = mock.timestamp ?? 0;
  return {
    id: mock.id ?? `${source}-${timestamp}-${index}`,
    label: mock.label ?? 'Mock Exam',
    date: mock.date ?? today(),
    entries,
    totalPoints: mock.totalPoints ?? 0,
    timestamp,
  };
}

function resultKey(result: UnifiedMockResult): string {
  if (result.id) return result.id;
  return `${result.label}|${result.date}|${result.entries.map(entry => `${entry.subjectName}:${entry.grade}:${entry.level}`).join(',')}`;
}

/**
 * Read every historical mock-results namespace without dropping records.
 * `unifiedMockResults` is the canonical field; `mockResults` remains a
 * transition mirror while older deployed clients are still in circulation.
 */
export function reconcileMockResults(data: ProgressDocument | null | undefined): UnifiedMockResult[] {
  if (!data) return [];

  const candidates: UnifiedMockResult[] = [
    ...(data.unifiedMockResults ?? []),
    ...(data.mockResults ?? []),
    ...((data.pointsPassport?.mockResults ?? []).map((mock, index) => legacyToUnified(mock, 'points-passport', index))),
    ...((data.warRoom?.mockResults ?? []).map((mock, index) => legacyToUnified(mock, 'war-room', index))),
  ];

  const byKey = new Map<string, UnifiedMockResult>();
  for (const result of candidates) {
    const key = resultKey(result);
    const existing = byKey.get(key);
    if (!existing) {
      byKey.set(key, result);
      continue;
    }
    // A transitional client may have appended one subject to one namespace
    // while another client retained the rest. Union by subject instead of
    // choosing one copy, so reconciliation can never discard an entered grade.
    const entries = [...existing.entries];
    const subjects = new Set(entries.map(entry => entry.subjectName));
    for (const entry of result.entries) {
      if (!subjects.has(entry.subjectName)) entries.push(entry);
    }
    byKey.set(key, {
      ...existing,
      entries,
      totalPoints: Math.max(existing.totalPoints, result.totalPoints),
      timestamp: Math.max(existing.timestamp, result.timestamp),
    });
  }

  return [...byKey.values()].sort((a, b) => b.timestamp - a.timestamp);
}

export function mockResultsStoragePatch(results: UnifiedMockResult[]) {
  return {
    unifiedMockResults: results,
    // Temporary compatibility mirror for already-installed app versions.
    mockResults: results,
  };
}
