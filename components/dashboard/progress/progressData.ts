import { STRATEGY_REGISTRY, type StudySessionRecord } from '../../../utils/strategyRegistry';
import type { DebriefEntry } from '../../StudyDebrief';
import { filterSessions, getRangeBounds, parseDateKey, type DashboardRange, type ConfidenceObservation } from '../dashboardAnalytics';

/** An empty selection means the entire record, including historical subjects. */
export function selectSubjects<T extends { subject: string }>(records: T[], selected: string[]): T[] {
  return selected.length ? records.filter(record => selected.includes(record.subject)) : records;
}

export const subjectColours = ['#398a80', '#527fb6', '#eb692a', '#b08a35', '#bd6f89', '#9575bc', '#819199'];
export function subjectColour(subject: string, universe: string[]) {
  const index = Math.max(0, universe.indexOf(subject));
  return subjectColours[index] ?? `hsl(${Math.round(index * 137.508) % 360} 48% 48%)`;
}

export function confidenceChartData(observations: ConfidenceObservation[], subjects: string[]) {
  const rows = new Map<number, Record<string, number>>();
  for (const observation of [...observations].sort((a, b) => a.timestamp - b.timestamp)) {
    const index = subjects.indexOf(observation.subject);
    if (index < 0) continue;
    const row = rows.get(observation.timestamp) ?? { timestamp: observation.timestamp };
    row[`s${index}`] = observation.score;
    rows.set(observation.timestamp, row);
  }
  return [...rows.values()];
}

export interface MethodEntry {
  id: string;
  subject: string;
  date: string;
  minutes: number;
  sessionType: StudySessionRecord['sessionType'];
  evidence: 'prompt' | 'reported';
}
export interface MethodRecord {
  id: string;
  name: string;
  description: string;
  entries: MethodEntry[];
}
const legacyMethods: Record<string, { id: string; name: string }> = {
  'active-recall': { id: 'mastering-active-recall-protocol', name: 'Active Recall' },
  'past-papers': { id: 'past-papers', name: 'Past papers' },
  're-reading': { id: 're-reading', name: 'Re-reading notes' },
  summarising: { id: 'summarising', name: 'Summarising' },
  teaching: { id: 'teaching', name: 'Teaching / explaining' },
  videos: { id: 'videos', name: 'Videos / resources' },
  flashcards: { id: 'flashcards', name: 'Flashcards' },
  other: { id: 'other', name: 'Other' },
};
/** Keep prompt exposure separate from self-reported use, including legacy records. */
export function buildMethodJournal(sessions: StudySessionRecord[], debriefs: DebriefEntry[], range: DashboardRange, now = new Date()): MethodRecord[] {
  const records = new Map<string, MethodRecord>();
  const add = (id: string, name: string, description: string, entry: MethodEntry) => {
    const method = records.get(id) ?? { id, name, description, entries: [] };
    method.entries.push(entry);
    records.set(id, method);
  };
  for (const session of filterSessions(sessions, range, 'all', now)) {
    for (const id of new Set(session.strategiesShown ?? [])) {
      const definition = STRATEGY_REGISTRY.find(method => method.moduleId === id);
      if (!definition) continue;
      add(id, definition.strategyName, definition.description, {
        id: `session:${session.id}:${id}`, subject: session.subject, date: session.date,
        minutes: Math.round(Math.max(0, session.actualSeconds) / 60), sessionType: session.sessionType, evidence: 'prompt',
      });
    }
  }
  const bounds = getRangeBounds(range, now);
  for (const debrief of debriefs) {
    const date = parseDateKey(debrief.date);
    if (!date || date < bounds.start || date >= bounds.end || !debrief.strategy) continue;
    const legacy = legacyMethods[debrief.strategy];
    const definition = STRATEGY_REGISTRY.find(method => method.moduleId === (legacy?.id ?? debrief.strategy));
    const id = definition?.moduleId ?? legacy?.id ?? debrief.strategy;
    add(id, definition?.strategyName ?? legacy?.name ?? debrief.strategy, definition?.description ?? 'A method you recorded in your study debrief.', {
      id: `debrief:${debrief.id}`, subject: debrief.subject, date: debrief.date,
      minutes: Math.max(0, debrief.durationMinutes), sessionType: debrief.sessionType, evidence: 'reported',
    });
  }
  return [...records.values()].map(method => ({ ...method, entries: method.entries.sort((a, b) => b.date.localeCompare(a.date)) }))
    .sort((a, b) => b.entries.length - a.entries.length || a.name.localeCompare(b.name));
}
