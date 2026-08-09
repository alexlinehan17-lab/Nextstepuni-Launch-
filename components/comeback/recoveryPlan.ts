import type { StudentSubjectProfile } from '../subjectData';
import type { SubjectPriority } from '../timetableAlgorithm';
import type { CanonicalTopicMasteryEntry } from '../../types';

export type RecoveryReason = 'missed-time' | 'overloaded' | 'unsure' | 'motivation' | 'other';
export type RecoveryCapacity = 3 | 5 | 7;

export interface RecoverySignal {
  id: string;
  label: string;
  detail: string;
  tone: 'attention' | 'steady' | 'positive';
}

export interface RecoveryAction {
  id: string;
  dateKey: string;
  dayLabel: string;
  subject: string;
  topic?: string;
  sessionType: 'practice' | 'revision' | 'new-learning';
  durationMinutes: number;
  reason: string;
  destination: 'mark-bank' | 'planner';
  done: boolean;
}

export interface RecoveryPlan {
  version: 2;
  createdAt: string;
  reason: RecoveryReason;
  capacity: RecoveryCapacity;
  signals: RecoverySignal[];
  priorities: string[];
  actions: RecoveryAction[];
  legacyAnchor?: string;
}

interface BuildRecoveryPlanInput {
  profile: StudentSubjectProfile;
  priorities: SubjectPriority[];
  masteryEntries: CanonicalTopicMasteryEntry[];
  timetableCompletions: Record<string, string[]>;
  reason: RecoveryReason;
  capacity: RecoveryCapacity;
  curriculumLevel: 'junior' | 'senior';
  now?: Date;
  legacyAnchor?: string;
}

const DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const SHORT_DAY = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const dateKey = (date: Date) => {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
};

const recentCompletionCount = (completions: Record<string, string[]>, now: Date) => {
  let count = 0;
  for (let offset = 0; offset < 7; offset += 1) {
    const day = new Date(now);
    day.setDate(now.getDate() - offset);
    count += completions[dateKey(day)]?.length ?? 0;
  }
  return count;
};

const nextAvailableDates = (now: Date, restDays: string[], count: number) => {
  const dates: Date[] = [];
  const perDay = new Map<string, number>();
  const cursor = new Date(now);
  let guard = 0;

  while (dates.length < count && guard < 21) {
    const dayName = DAY_NAMES[cursor.getDay()];
    const key = dateKey(cursor);
    const used = perDay.get(key) ?? 0;
    if (!restDays.includes(dayName) && used < 2) {
      dates.push(new Date(cursor));
      perDay.set(key, used + 1);
    }
    if ((perDay.get(key) ?? 0) >= 2 || restDays.includes(dayName)) {
      cursor.setDate(cursor.getDate() + 1);
    }
    guard += 1;
  }
  return dates;
};

/**
 * Produces a deliberately small recovery week. It does not invent a second
 * timetable: each action launches an existing execution surface, while this
 * plan explains why that action has been selected.
 */
export function buildRecoveryPlan({
  profile,
  priorities,
  masteryEntries,
  timetableCompletions,
  reason,
  capacity,
  curriculumLevel,
  now = new Date(),
  legacyAnchor,
}: BuildRecoveryPlanInput): RecoveryPlan {
  const studentSubjects = new Set(profile.subjects.map(subject => subject.subjectName));
  const subjectMastery = new Map<string, CanonicalTopicMasteryEntry[]>();
  for (const entry of masteryEntries) {
    if (!studentSubjects.has(entry.subjectName)) continue;
    const list = subjectMastery.get(entry.subjectName) ?? [];
    list.push(entry);
    subjectMastery.set(entry.subjectName, list);
  }

  const ranked = profile.subjects
    .map(subject => {
      const priority = priorities.find(item => item.subjectName === subject.subjectName)?.priorityScore ?? 0.2;
      const topics = subjectMastery.get(subject.subjectName) ?? [];
      const shaky = topics.filter(topic => topic.confidence === 'shaky').length;
      const notStarted = topics.filter(topic => topic.confidence === 'not-started').length;
      return { subject, topics, shaky, notStarted, score: priority + shaky * 0.35 + notStarted * 0.08 };
    })
    .sort((a, b) => b.score - a.score || a.subject.subjectName.localeCompare(b.subject.subjectName));

  const selected = ranked.slice(0, Math.min(2, ranked.length));
  const completedLastWeek = recentCompletionCount(timetableCompletions, now);
  const shakyTotal = ranked.reduce((sum, item) => sum + item.shaky, 0);
  const signals: RecoverySignal[] = [
    {
      id: 'pace',
      label: 'Recent rhythm',
      detail: completedLastWeek === 0
        ? 'No timetable blocks were recorded in the last seven days.'
        : `${completedLastWeek} timetable block${completedLastWeek === 1 ? '' : 's'} completed in the last seven days.`,
      tone: completedLastWeek >= 5 ? 'positive' : completedLastWeek >= 2 ? 'steady' : 'attention',
    },
    {
      id: 'mastery',
      label: 'Knowledge gaps',
      detail: shakyTotal > 0
        ? `${shakyTotal} topic${shakyTotal === 1 ? '' : 's'} currently marked shaky across your subjects.`
        : 'No shaky topics recorded yet, so grade gaps and coverage drive this plan.',
      tone: shakyTotal > 0 ? 'attention' : 'steady',
    },
    {
      id: 'capacity',
      label: 'Realistic capacity',
      detail: `${capacity} focused blocks across the next seven days — no catch-up marathon.`,
      tone: 'positive',
    },
  ];

  const dates = nextAvailableDates(now, profile.restDays ?? [], capacity);
  const actions: RecoveryAction[] = dates.map((date, index) => {
    const rankedSubject = selected[index % Math.max(1, selected.length)] ?? ranked[index % Math.max(1, ranked.length)];
    const subjectName = rankedSubject?.subject.subjectName ?? 'General study';
    const weakTopics = rankedSubject?.topics
      .filter(topic => topic.confidence === 'shaky' || topic.confidence === 'not-started')
      .sort((a, b) => (a.confidence === 'shaky' ? -1 : 1) - (b.confidence === 'shaky' ? -1 : 1));
    const topic = weakTopics?.[index % Math.max(1, weakTopics.length)]?.topicName;
    const sessionType: RecoveryAction['sessionType'] = topic
      ? (index % 3 === 2 ? 'revision' : 'practice')
      : (index % 2 === 0 ? 'practice' : 'revision');
    const destination = curriculumLevel === 'senior' && sessionType === 'practice' ? 'mark-bank' : 'planner';

    return {
      id: `recovery-${dateKey(date)}-${index}-${subjectName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`,
      dateKey: dateKey(date),
      dayLabel: `${SHORT_DAY[date.getDay()]} ${date.getDate()}`,
      subject: subjectName,
      topic,
      sessionType,
      durationMinutes: Math.min(45, Math.max(25, profile.defaultBlockDuration ?? 45)),
      reason: topic
        ? `${topic} is an identified knowledge gap in one of your highest-priority subjects.`
        : `${subjectName} currently offers one of the strongest returns on your available study time.`,
      destination,
      done: false,
    };
  });

  return {
    version: 2,
    createdAt: now.toISOString(),
    reason,
    capacity,
    signals,
    priorities: selected.map(item => item.subject.subjectName),
    actions,
    legacyAnchor,
  };
}
