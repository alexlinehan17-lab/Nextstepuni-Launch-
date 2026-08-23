import { type UnifiedMockResult, type UnifiedMockResultKind } from '../types';
import { computeBestSixTotal } from '../components/pointsScenarioStore';
import type { Grade } from '../components/subjectData';
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

function isGrade(value: string): value is Grade {
  return /^(H|O)[1-8]$/.test(value);
}

function recomputeFullMockTotal(entries: UnifiedMockResult['entries']): number {
  return computeBestSixTotal(entries.flatMap(entry => (
    isGrade(entry.grade) ? [{ subjectName: entry.subjectName, grade: entry.grade }] : []
  )));
}

export function resolveMockResultKind(
  result: Pick<UnifiedMockResult, 'entries' | 'resultKind'>,
): UnifiedMockResultKind {
  return result.resultKind ?? (result.entries.length > 1 ? 'full' : 'single');
}

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
    resultKind: entries.length > 1 ? 'full' : 'single',
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
  ].map(result => ({ ...result, resultKind: resolveMockResultKind(result) }));

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
    let entriesChanged = false;
    for (const entry of result.entries) {
      if (!subjects.has(entry.subjectName)) {
        entries.push(entry);
        subjects.add(entry.subjectName);
        entriesChanged = true;
      }
    }
    const resultKind = existing.resultKind === 'full' || result.resultKind === 'full'
      ? 'full'
      : 'single';
    byKey.set(key, {
      ...existing,
      entries,
      totalPoints: resultKind === 'full' && entriesChanged
        ? recomputeFullMockTotal(entries)
        : Math.max(existing.totalPoints, result.totalPoints),
      timestamp: Math.max(existing.timestamp, result.timestamp),
      resultKind,
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

/**
 * Once a deletion is made, clear the retired namespaces as well as writing the
 * canonical list. Otherwise reconciliation can restore a deleted legacy item
 * on the next load.
 */
export function mockResultsDeletionPatch(results: UnifiedMockResult[]) {
  return {
    ...mockResultsStoragePatch(results),
    pointsPassport: { mockResults: [] },
    warRoom: { mockResults: [] },
  };
}
