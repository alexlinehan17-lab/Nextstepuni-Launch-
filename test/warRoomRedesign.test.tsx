/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';

vi.mock('framer-motion', async importOriginal => {
  const actual = await importOriginal<Record<string, unknown>>();
  return {
    ...actual,
    AnimatePresence: ({ children }: { children: React.ReactNode }) => children,
  };
});

const innovationState = vi.hoisted(() => ({
  mastery: {} as Record<string, Record<string, {
    confidence: 'not-started' | 'shaky' | 'solid';
    updatedAt: number;
    source: 'manual' | 'debrief' | 'import';
  }>>,
  mocks: [] as Array<{
    id: string;
    label: string;
    date: string;
    entries: Array<{ subjectName: string; grade: string; level: string }>;
    totalPoints: number;
    timestamp: number;
  }>,
  canonical: {} as Record<string, Record<string, { confidence: 'not-started' | 'shaky' | 'solid'; updatedAt: number; source: 'manual' | 'debrief' | 'import' }>>,
  importSyllabusTopics: vi.fn(),
  setTopicConfidence: vi.fn(),
  addMockResult: vi.fn(),
  removeMockResult: vi.fn(),
}));

const firestoreState = vi.hoisted(() => ({
  sessions: [] as Array<Record<string, unknown>>,
  progress: {} as Record<string, unknown>,
}));

vi.mock('firebase/firestore', () => ({
  collection: vi.fn(() => ({})),
  doc: vi.fn(() => ({})),
  getDocs: vi.fn(async () => ({
    docs: firestoreState.sessions.map(data => ({ data: () => data })),
  })),
  getDoc: vi.fn(async () => ({ data: () => firestoreState.progress })),
}));

vi.mock('@/contexts/InnovationDataContext', () => ({
  useInnovationData: () => ({
    topicMastery: {
      mastery: innovationState.mastery,
      canonicalMastery: { schemaVersion: 2, topics: {}, unresolved: {} },
      isLoaded: true,
      importSyllabusTopics: innovationState.importSyllabusTopics,
      getSubjectTopics: (subject: string) => innovationState.mastery[subject] ?? {},
      getCanonicalSubjectTopics: (subject: string) => innovationState.canonical[subject] ?? {},
      getTopicConfidence: (subject: string, topic: string) => (
        innovationState.mastery[subject]?.[topic]?.confidence ?? 'not-started'
      ),
      setTopicConfidence: innovationState.setTopicConfidence,
      bulkUpdate: vi.fn(),
    },
    mockResults: {
      mocks: innovationState.mocks,
      isLoaded: true,
      addMockResult: innovationState.addMockResult,
      removeMockResult: innovationState.removeMockResult,
      getLatestBySubject: vi.fn(() => null),
    },
    futureFinderPicks: [{
      id: 'target-course',
      title: 'Computer Science',
      institution: 'University College Dublin',
      typicalPoints: 500,
    }],
  }),
}));

import WarRoom, { type WarRoomStudyBlock } from '@/components/WarRoom';
import { getStudyTopicOptions } from '@/services/studyTopicHistory';
import { createDevStudentProfile } from '@/data/devStudent';
import { DAYS_OF_WEEK, getBlockId } from '@/components/subjectData';
import {
  allocateSessions,
  computeSubjectPriorities,
  computeWeeksUntilExam,
  generateWeeklyTimetable,
  type SubjectSM2State,
} from '@/components/timetableAlgorithm';

const NOW = new Date('2026-08-10T12:00:00.000Z');
const TODAY_BLOCK: WarRoomStudyBlock = {
  subject: 'Geography',
  sessionType: 'new-learning',
  durationMinutes: 45,
  dateKey: '2026-08-10',
  blockId: 'Geography|new-learning|0',
};

const renderWarRoom = ({
  uid = '',
  timetableCompletions = {},
  todayBlocks = [TODAY_BLOCK],
  onStudyNow = vi.fn<(block: WarRoomStudyBlock) => void>(),
}: {
  uid?: string;
  timetableCompletions?: Record<string, string[]>;
  todayBlocks?: WarRoomStudyBlock[];
  onStudyNow?: (block: WarRoomStudyBlock) => void;
} = {}) => {
  render(
    <WarRoom
      uid={uid}
      profile={createDevStudentProfile(NOW)}
      timetableCompletions={timetableCompletions}
      todayBlocks={todayBlocks}
      onStudyNow={onStudyNow}
    />,
  );
  return { onStudyNow };
};

describe('War Room minimalist workspace', () => {
  beforeEach(() => {
    innovationState.mastery = {};
    innovationState.canonical = {};
    innovationState.mocks = [];
    firestoreState.sessions = [];
    firestoreState.progress = {};
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  test('defaults to one clear focus, limits the queue, and launches the exact scheduled block', async () => {
    const onStudyNow = vi.fn();
    renderWarRoom({ onStudyNow });

    expect(await screen.findByRole('region', { name: 'War Room strategy workspace' })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: 'Today' })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByRole('heading', { name: 'Geography' })).toBeInTheDocument();

    const studyActions = screen.getAllByRole('button', { name: 'Start a 45-minute session' });
    expect(studyActions).toHaveLength(1);

    const queue = screen.getByRole('list', { name: 'Weekly subject queue' });
    expect(within(queue).getAllByRole('listitem')).toHaveLength(3);

    expect(screen.queryByRole('heading', { name: 'Exam runway' })).not.toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Points position' })).not.toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Ranked next priorities' })).not.toBeInTheDocument();
    expect(screen.queryByText(/study patterns/i)).not.toBeInTheDocument();

    fireEvent.click(studyActions[0]);
    expect(onStudyNow).toHaveBeenCalledTimes(1);
    expect(onStudyNow).toHaveBeenCalledWith(TODAY_BLOCK);
  });

  test('keeps supporting evidence hidden until the student requests it', async () => {
    innovationState.mastery = {
      Geography: {
        'Physical environments': { confidence: 'not-started', updatedAt: 1, source: 'manual' },
        'Regional geography': { confidence: 'shaky', updatedAt: 2, source: 'manual' },
      },
    };
    innovationState.mocks = [{
      id: 'mock-1',
      label: 'February Mocks',
      date: '2026-02-12',
      entries: [{ subjectName: 'Geography', grade: 'H5', level: 'higher' }],
      totalPoints: 56,
      timestamp: 1,
    }];

    renderWarRoom();

    expect(await screen.findByRole('heading', { name: 'Geography' })).toBeInTheDocument();
    const disclosure = screen.getByRole('button', { name: 'Why this subject?' });
    expect(disclosure).toHaveAttribute('aria-expanded', 'false');
    expect(screen.queryByText('25% weighted coverage across 2 topics.')).not.toBeInTheDocument();

    fireEvent.click(disclosure);

    expect(disclosure).toHaveAttribute('aria-expanded', 'true');
    expect(await screen.findByText('25% weighted coverage across 2 topics.')).toBeInTheDocument();
    expect(screen.getByText('H5 → H2')).toBeInTheDocument();
  });

  test('keeps Review functional and sends the selected subject topic actions', async () => {
    innovationState.mastery = {
      Geography: {
        'Physical environments': { confidence: 'shaky', updatedAt: 1, source: 'manual' },
      },
    };

    renderWarRoom();

    fireEvent.click(await screen.findByRole('tab', { name: 'Subjects' }));
    const geographyCard = screen.getByRole('article', { name: 'Geography subject card' });
    fireEvent.click(within(geographyCard).getByRole('button', { name: 'Browse topics' }));
    expect(await screen.findByRole('heading', { name: 'Coverage and confidence' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'For 2027 exam candidates only' })).toBeInTheDocument();
    expect(screen.getByText(/first examined in 2028/)).toBeInTheDocument();
    expect(screen.queryByText(/exam frequency/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/marks per hour/i)).not.toBeInTheDocument();

    const topicControl = await screen.findByRole('button', { name: /Physical environments: shaky/i });
    fireEvent.click(topicControl);
    fireEvent.click(screen.getByRole('button', { name: 'Reset Physical environments to not started' }));

    expect(innovationState.setTopicConfidence).toHaveBeenNthCalledWith(
      1,
      'Geography',
      'Physical environments',
      'solid',
      'manual',
    );
    expect(innovationState.setTopicConfidence).toHaveBeenNthCalledWith(
      2,
      'Geography',
      'Physical environments',
      'not-started',
      'manual',
    );

    fireEvent.click(screen.getByRole('button', { name: 'Back to subjects' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));
    expect(await screen.findByRole('heading', { name: 'Mock trajectory' })).toBeInTheDocument();
    expect(screen.getByText('No mock results yet')).toBeInTheDocument();
    expect(screen.queryByText('Track your mock exam trajectory')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Back to learning record' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Time plan' }));
    expect(await screen.findByRole('heading', { name: 'A manageable week, repeated' })).toBeInTheDocument();
    expect(screen.queryByText('Exam runway')).not.toBeInTheDocument();
    expect(screen.queryByText('Weekly capacity')).not.toBeInTheDocument();
  });

  test('defaults Single and Full mock dates to the local Irish calendar day', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-06-03T00:30:00+01:00'));
    renderWarRoom();

    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));
    fireEvent.click(screen.getByRole('button', { name: 'Single result' }));

    expect(screen.getByLabelText('Date')).toHaveValue('2026-06-03');
    expect(screen.getByLabelText('Date')).toHaveAttribute('max', '2026-06-03');

    fireEvent.click(screen.getByRole('button', { name: /Cancel/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Full mock' }));

    const fullMockDate = screen.getByLabelText('Date');
    expect(fullMockDate).toHaveValue('2026-06-03');
    expect(fullMockDate).toHaveAttribute('max', '2026-06-03');

    fireEvent.change(fullMockDate, { target: { value: '2026-06-04' } });
    expect(screen.getByRole('button', { name: 'Save full mock' })).toBeDisabled();
  });

  test('validates and saves one exact single-result payload', () => {
    renderWarRoom();

    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));
    fireEvent.click(screen.getByRole('button', { name: 'Single result' }));

    fireEvent.change(screen.getByLabelText('Subject'), { target: { value: 'Geography' } });
    fireEvent.change(screen.getByLabelText('Grade'), { target: { value: 'H5' } });
    fireEvent.change(screen.getByLabelText('Label (optional)'), { target: { value: 'Mock 1' } });

    const date = screen.getByLabelText('Date');
    const save = screen.getByRole('button', { name: 'Save result' });
    fireEvent.change(date, { target: { value: '' } });

    expect(save).toBeDisabled();
    fireEvent.click(save);
    expect(innovationState.addMockResult).not.toHaveBeenCalled();

    fireEvent.change(date, { target: { value: '2026-08-09' } });
    expect(save).toBeEnabled();
    fireEvent.click(save);

    expect(innovationState.addMockResult).toHaveBeenCalledTimes(1);
    expect(innovationState.addMockResult).toHaveBeenCalledWith({
      label: 'Mock 1',
      date: '2026-08-09',
      entries: [{ subjectName: 'Geography', grade: 'H5', level: 'higher' }],
      totalPoints: 56,
      resultKind: 'single',
    });
  });

  test('applies the Higher Maths CAO bonus to a single-result payload', () => {
    renderWarRoom();

    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));
    fireEvent.click(screen.getByRole('button', { name: 'Single result' }));

    fireEvent.change(screen.getByLabelText('Subject'), { target: { value: 'Mathematics' } });
    fireEvent.change(screen.getByLabelText('Grade'), { target: { value: 'H6' } });
    fireEvent.change(screen.getByLabelText('Date'), { target: { value: '2026-08-09' } });

    expect(screen.getByRole('option', { name: 'H6 (71 pts)' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save result' }));

    expect(innovationState.addMockResult).toHaveBeenCalledTimes(1);
    expect(innovationState.addMockResult).toHaveBeenCalledWith({
      label: 'Single Result',
      date: '2026-08-09',
      entries: [{ subjectName: 'Mathematics', grade: 'H6', level: 'higher' }],
      totalPoints: 71,
      resultKind: 'single',
    });
  });

  test('reconciles an open single-result form when settings remove its subject', async () => {
    const profile = createDevStudentProfile(NOW);
    const { rerender } = render(
      <WarRoom uid="" profile={profile} timetableCompletions={{}} />,
    );

    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));
    fireEvent.click(screen.getByRole('button', { name: 'Single result' }));

    expect(screen.getByLabelText('Subject')).toHaveValue('Politics & Society');
    fireEvent.change(screen.getByLabelText('Grade'), { target: { value: 'H5' } });

    const updatedProfile = {
      ...profile,
      subjects: profile.subjects.slice(1),
    };
    rerender(<WarRoom uid="" profile={updatedProfile} timetableCompletions={{}} />);

    await waitFor(() => {
      expect(screen.getByLabelText('Subject')).toHaveValue('Geography');
      expect(screen.getByLabelText('Grade')).toHaveValue('');
    });
  });

  test('ignores historical results for subjects no longer in Settings', () => {
    innovationState.mocks = [{
      id: 'removed-subject-mock',
      label: 'Old mock',
      date: '2025-12-01',
      entries: [{ subjectName: 'Biology', grade: 'H3', level: 'higher' }],
      totalPoints: 77,
      timestamp: 1,
    }];

    renderWarRoom();
    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));

    expect(screen.getByText('No mock results yet')).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Performance over time' })).not.toBeInTheDocument();
  });

  test('counts this Monday-to-Sunday completion and ignores the previous week', () => {
    vi.useFakeTimers();
    vi.setSystemTime(NOW);

    renderWarRoom({
      timetableCompletions: {
        '2026-08-10': ['Geography|new-learning|0'],
        '2026-08-03': ['Mathematics|practice|0'],
      },
    });

    expect(screen.getByRole('progressbar', { name: 'Geography weekly sessions' }))
      .toHaveAttribute('aria-valuenow', '1');
    expect(screen.getByRole('progressbar', { name: 'Weekly queue progress' }))
      .toHaveAttribute('aria-valuenow', '1');
  });

  test('uses local calendar days and refreshes the countdown across midnight', async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-06-02T23:59:30+01:00'));
    const profile = {
      ...createDevStudentProfile(NOW),
      examStartDate: '2026-06-03',
    };

    render(<WarRoom uid="" profile={profile} timetableCompletions={{}} />);

    const context = screen.getByRole('group', { name: 'Exam countdown' });
    expect(within(context).getByText('1')).toBeInTheDocument();
    expect(within(context).getByText('day to your exams')).toBeInTheDocument();

    await act(async () => {
      vi.advanceTimersByTime(31_000);
    });

    expect(within(context).getByText('0')).toBeInTheDocument();
    expect(within(context).getByText('days to your exams')).toBeInTheDocument();
  });

  test('does not count an early-ended study record as a completed weekly session', async () => {
    const now = new Date();
    const todayKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    firestoreState.sessions = [
      {
        id: 'early-geography',
        date: todayKey,
        subject: 'Geography',
        sessionType: 'new-learning',
        plannedMinutes: 45,
        actualSeconds: 60,
        startedAt: 1,
        completedAt: 2,
        pointsEarned: 0,
        hadReflection: false,
      },
      {
        id: 'complete-mathematics',
        date: todayKey,
        subject: 'Mathematics',
        sessionType: 'practice',
        plannedMinutes: 45,
        actualSeconds: 2700,
        startedAt: 1,
        completedAt: 2,
        pointsEarned: 20,
        hadReflection: true,
      },
    ];

    renderWarRoom({ uid: 'student-1' });

    expect(await screen.findByRole('progressbar', { name: 'Geography weekly sessions' }))
      .toHaveAttribute('aria-valuenow', '0');
    expect(screen.getByRole('progressbar', { name: 'Weekly queue progress' }))
      .toHaveAttribute('aria-valuenow', '1');
  });

  test('derives the launch payload from the same mastery, SM-2, and rest-day plan as the Planner', async () => {
    const now = new Date();
    const jsDay = now.getDay();
    const todayIndex = jsDay === 0 ? 6 : jsDay - 1;
    const todayName = DAYS_OF_WEEK[todayIndex];
    const otherRestDays = DAYS_OF_WEEK.filter(day => day !== todayName).slice(0, 3);
    const profile = {
      ...createDevStudentProfile(now),
      restDays: [...otherRestDays, todayName],
    };
    const sm2States: SubjectSM2State[] = profile.subjects.map((subject, index) => ({
      subjectName: subject.subjectName,
      easeFactor: index === 0 ? 1.4 : 2.5,
      interval: index === 0 ? 1 : 14,
      repetitions: index === 0 ? 0 : 3,
      nextReviewDate: TODAY_BLOCK.dateKey,
      lastQuality: index === 0 ? 2 : 4,
    }));
    innovationState.mastery = {
      Geography: {
        'Physical environments': { confidence: 'shaky', updatedAt: 1, source: 'manual' },
      },
    };
    firestoreState.progress = { sm2States };
    const onStudyNow = vi.fn();

    render(
      <WarRoom
        uid="student-parity"
        profile={profile}
        timetableCompletions={{}}
        skippedSessions={[]}
        onStudyNow={onStudyNow}
      />,
    );

    fireEvent.click(await screen.findByRole('button', { name: /Start a \d+-minute session/ }));

    const weeksUntilExam = computeWeeksUntilExam(profile.examStartDate!);
    const priorities = computeSubjectPriorities(profile.subjects, innovationState.mastery, profile.examStartDate);
    const allocations = allocateSessions(priorities, weeksUntilExam, sm2States, profile.defaultBlockDuration);
    const timetable = generateWeeklyTimetable(
      allocations,
      weeksUntilExam,
      0,
      profile.restDays.slice(0, 3),
      profile.defaultBlockDuration,
      sm2States,
      innovationState.mastery,
    );
    const dateKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    const expectedPayloads = timetable[todayIndex].blocks.map((block, blockIndex) => ({
      subject: block.subjectName,
      sessionType: block.sessionType,
      durationMinutes: block.durationMinutes,
      dateKey,
      blockId: getBlockId(block, blockIndex),
    }));

    expect(onStudyNow).toHaveBeenCalledTimes(1);
    expect(expectedPayloads).toContainEqual(onStudyNow.mock.calls[0][0]);
  });

  test('supports keyboard navigation through every Kobra workspace tab', async () => {
    renderWarRoom();
    const today = await screen.findByRole('tab', { name: 'Today' });
    today.focus();
    fireEvent.keyDown(today, { key: 'ArrowRight' });
    const subjects = screen.getByRole('tab', { name: 'Subjects' });
    await waitFor(() => expect(subjects).toHaveFocus());
    expect(subjects).toHaveAttribute('aria-selected', 'true');
    expect(await screen.findByRole('heading', { name: /Your subjects.*Your next moves/ })).toBeInTheDocument();
    fireEvent.keyDown(subjects, { key: 'ArrowRight' });
    const record = screen.getByRole('tab', { name: 'Learning record' });
    await waitFor(() => expect(record).toHaveFocus());
    expect(record).toHaveAttribute('aria-selected', 'true');
    expect(await screen.findByRole('heading', { name: /The small steps.*On record/ })).toBeInTheDocument();
    fireEvent.keyDown(record, { key: 'ArrowRight' });
    const time = screen.getByRole('tab', { name: 'Time plan' });
    await waitFor(() => expect(time).toHaveFocus());
    expect(time).toHaveAttribute('aria-selected', 'true');
    expect(await screen.findByRole('heading', { name: 'Where the time goes' })).toBeInTheDocument();
  });

  test('stays useful when an exam date and Leaving Cert grades are not available', async () => {
    const baseProfile = createDevStudentProfile(NOW);
    const profile = {
      ...baseProfile,
      examStartDate: null,
      subjects: baseProfile.subjects.map(({ subjectName, level }) => ({ subjectName, level })),
    };

    render(
      <WarRoom
        uid=""
        profile={profile}
        timetableCompletions={{}}
      />,
    );

    expect(await screen.findByRole('region', { name: 'War Room strategy workspace' })).toBeInTheDocument();
    expect(screen.queryByText(/days to exams/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/current points/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: 'Subjects' }));
    expect(await screen.findByRole('heading', { name: /Your subjects.*Your next moves/ })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: 'Time plan' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Results and grades' })).not.toBeInTheDocument();
  });

  test('reconciles the active review and selected subject after settings edits', async () => {
    const profile = createDevStudentProfile(NOW);
    const { rerender } = render(
      <WarRoom uid="" profile={profile} timetableCompletions={{}} />,
    );

    fireEvent.click(await screen.findByRole('tab', { name: 'Subjects' }));
    fireEvent.click(await screen.findByRole('tab', { name: 'Time plan' }));
    expect(await screen.findByRole('heading', { name: 'Where the time goes' })).toBeInTheDocument();

    const updatedProfile = {
      ...profile,
      examStartDate: null,
      subjects: profile.subjects.slice(1).map(({ subjectName, level }) => ({ subjectName, level })),
    };
    rerender(<WarRoom uid="" profile={updatedProfile} timetableCompletions={{}} />);

    expect(await screen.findByRole('heading', { name: /Your subjects.*Your next moves/ })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: 'Time plan' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Results and grades' })).not.toBeInTheDocument();
    expect(screen.getByRole('article', { name: 'Geography subject card' })).toBeInTheDocument();
    expect(screen.queryByRole('article', { name: 'Politics & Society subject card' })).not.toBeInTheDocument();
  });
  test('uses exact saved time, deduplicates records and keeps early sessions visible', async () => {
    const early = { id: 'early', date: '2026-08-10', subject: 'Geography', sessionType: 'revision', plannedMinutes: 45, actualSeconds: 60, startedAt: 1, completedAt: 2, pointsEarned: 0, hadReflection: false };
    firestoreState.sessions = [early, { ...early }, { ...early, id: 'maths', subject: 'Maths', actualSeconds: 2700, completedAt: 3 }];
    renderWarRoom({ uid: 'saved-records' });
    fireEvent.click(await screen.findByRole('tab', { name: 'Subjects' }));
    const geography = screen.getByRole('article', { name: 'Geography subject card' });
    expect(within(geography).getByText('1 minute')).toBeInTheDocument();
    const maths = screen.getByRole('article', { name: 'Mathematics subject card' });
    expect(within(maths).getByText('45 minutes')).toBeInTheDocument();
    fireEvent.change(screen.getByRole('searchbox', { name: 'Find a subject' }), { target: { value: 'geo' } });
    expect(screen.getAllByRole('article')).toHaveLength(1);
    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    expect(screen.getByLabelText('46 minutes')).toHaveTextContent('46 min');
    expect(screen.getByText('recorded study / 2 saved sessions')).toBeInTheDocument();
    const rows = document.querySelectorAll('.wr-history-row');
    expect(rows[0]).toHaveTextContent('Maths');
    expect(rows[1]).toHaveTextContent('Geography');
  });

  test('opens the real Signature record, carries its topic selection and restores focus', async () => {
    const onStudyTopic = vi.fn();
    const profile = createDevStudentProfile(NOW);
    render(<WarRoom uid="" profile={profile} timetableCompletions={{}} todayBlocks={[]} onStudyTopic={onStudyTopic} />);
    fireEvent.click(await screen.findByRole('tab', { name: 'Subjects' }));
    const card = screen.getByRole('article', { name: 'Geography subject card' });
    const trigger = within(card).getByRole('button', { name: 'Learning record' });
    trigger.focus();
    fireEvent.click(trigger);
    const dialog = await screen.findByRole('dialog', { name: 'The subject, on record.' }, { timeout: 15000 });
    const topic = getStudyTopicOptions('Geography', profile.examStartDate, 'higher').find(item => item.kind === 'topic')!;
    fireEvent.change(within(dialog).getByLabelText('Look at'), { target: { value: topic.id } });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Start studying' }));
    expect(onStudyTopic).toHaveBeenCalledWith({ subjectId: 'geography', specificationId: topic.specificationId, topicIds: [topic.id] });
    fireEvent.keyDown(document, { key: 'Escape' });
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    await waitFor(() => expect(trigger).toHaveFocus());
  }, 20000);

  test('records confidence with the canonical curriculum ID in the ledger', async () => {
    const profile = createDevStudentProfile(NOW);
    render(<WarRoom uid="" profile={profile} timetableCompletions={{}} />);
    fireEvent.click(await screen.findByRole('tab', { name: 'Learning record' }));
    const topic = getStudyTopicOptions(profile.subjects[0].subjectName, profile.examStartDate, profile.subjects[0].level).find(item => item.kind === 'topic')!;
    fireEvent.click(screen.getByRole('button', { name: 'Solid' }));
    expect(innovationState.setTopicConfidence).toHaveBeenCalledWith(profile.subjects[0].subjectName, topic.name, 'solid', 'manual', topic.id);
    expect(await screen.findByText('scored questions')).toBeInTheDocument();
  });

  test('does not carry loaded records or open cards between accounts', async () => {
    const profile = createDevStudentProfile(NOW);
    firestoreState.sessions = [{ id: 'previous', date: '2026-08-10', subject: 'Geography', sessionType: 'revision', plannedMinutes: 45, actualSeconds: 7200, startedAt: 1, completedAt: 2, pointsEarned: 0, hadReflection: false }];
    const { rerender } = render(<WarRoom uid="previous" profile={profile} timetableCompletions={{}} todayBlocks={[TODAY_BLOCK]} />);
    expect(await screen.findByLabelText('120 minutes')).toHaveTextContent('2 hr');
    fireEvent.click(screen.getByRole('tab', { name: 'Learning record' }));
    fireEvent.click(screen.getByRole('button', { name: 'Results and grades' }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    firestoreState.sessions = [];
    rerender(<WarRoom uid="next" profile={profile} timetableCompletions={{}} todayBlocks={[TODAY_BLOCK]} />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('120 minutes')).not.toBeInTheDocument();
    expect(await screen.findByLabelText('0 minutes')).toHaveTextContent('0 min');
  });

  test('keeps an empty day honest and opens subject choices', async () => {
    renderWarRoom({ todayBlocks: [] });
    expect(await screen.findByText('No sessions left in today’s plan.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Start a \d+-minute session/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Choose a subject' }));
    expect(screen.getByRole('tab', { name: 'Subjects' })).toHaveAttribute('aria-selected', 'true');
  });

  test('shows the latest canonical topic confidence without guessing from display labels', async () => {
    const profile = createDevStudentProfile(NOW);
    const topic = getStudyTopicOptions('Geography', profile.examStartDate, 'higher').find(item => item.kind === 'topic')!;
    innovationState.mastery = { Geography: { [topic.name]: { confidence: 'solid', updatedAt: 100, source: 'manual' } } };
    const { rerender } = render(<WarRoom uid="" profile={profile} timetableCompletions={{}} initialMode="review" initialReviewPanel="subjects" />);
    const card = screen.getByRole('article', { name: 'Geography subject card' });
    expect(within(card).getByText('Not recorded')).toBeInTheDocument();
    innovationState.canonical = { Geography: { [topic.id]: { confidence: 'shaky', updatedAt: 200, source: 'manual' } } };
    rerender(<WarRoom uid="" profile={profile} timetableCompletions={{}} initialMode="review" initialReviewPanel="subjects" />);
    expect(within(card).getByText('Shaky')).toBeInTheDocument();
    expect(within(card).getByText(topic.name)).toBeInTheDocument();
    expect(within(card).queryByText('Solid')).not.toBeInTheDocument();
  });

  test('retains records for subjects without a verified curriculum instead of opening an empty card', async () => {
    const profile = { ...createDevStudentProfile(NOW), subjects: [{ subjectName: 'Study skills', level: 'higher' as const }] };
    firestoreState.sessions = [{ id: 'unmapped', date: '2026-08-10', subject: 'Study skills', sessionType: 'revision', plannedMinutes: 45, actualSeconds: 125, startedAt: 1, completedAt: 2, pointsEarned: 0, hadReflection: false }];
    render(<WarRoom uid="unmapped" profile={profile} timetableCompletions={{}} initialMode="review" />);
    const card = await screen.findByRole('article', { name: 'Study skills subject card' });
    fireEvent.click(within(card).getByRole('button', { name: 'Learning record' }));
    const dialog = screen.getByRole('dialog', { name: 'The subject, on record.' });
    expect(within(dialog).getAllByText('2 min 5 sec')).toHaveLength(2);
    expect(within(dialog).getByText(/verified topic map is not available/)).toBeInTheDocument();
  });

  test('pages the dated record without dropping older sessions', async () => {
    const profile = createDevStudentProfile(NOW);
    firestoreState.sessions = Array.from({ length: 15 }, (_, index) => ({ id: `history-${index}`, date: '2026-08-10', subject: 'Geography', sessionType: 'revision', plannedMinutes: 45, actualSeconds: 60, startedAt: 1, completedAt: index + 2, pointsEarned: 0, hadReflection: false }));
    render(<WarRoom uid="history" profile={profile} timetableCompletions={{}} />);
    fireEvent.click(await screen.findByRole('tab', { name: 'Learning record' }));
    expect(document.querySelectorAll('.wr-history-row')).toHaveLength(10);
    expect(screen.getByText('recorded study / 15 saved sessions')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Show more sessions (5 remaining)' }));
    expect(document.querySelectorAll('.wr-history-row')).toHaveLength(15);
    expect(screen.queryByRole('button', { name: /Show more sessions/ })).not.toBeInTheDocument();
  });

});
