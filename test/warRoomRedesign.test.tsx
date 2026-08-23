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
      getCanonicalSubjectTopics: vi.fn(() => ({})),
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

    expect(await screen.findByRole('heading', { name: 'What matters now' })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: 'Focus' })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByRole('heading', { name: 'Geography' })).toBeInTheDocument();
    expect(screen.getByText('Start here')).toBeInTheDocument();

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

    expect(await screen.findByText('Highest impact')).toBeInTheDocument();
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

    fireEvent.click(await screen.findByRole('tab', { name: 'Review' }));
    expect(await screen.findByRole('heading', { name: 'Coverage and confidence' })).toBeInTheDocument();

    const geography = screen.getByRole('button', { name: /Geography/ });
    fireEvent.click(geography);
    const selectedGeography = screen.getByRole('button', { name: /^Geography/, pressed: true });
    expect(selectedGeography).toHaveAttribute('aria-pressed', 'true');
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

    fireEvent.click(screen.getByRole('tab', { name: 'Results' }));
    expect(await screen.findByRole('heading', { name: 'Mock trajectory' })).toBeInTheDocument();
    expect(screen.getByText('No mock results yet')).toBeInTheDocument();
    expect(screen.queryByText('Track your mock exam trajectory')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: 'Time plan' }));
    expect(await screen.findByRole('heading', { name: 'A manageable week, repeated' })).toBeInTheDocument();
    expect(screen.queryByText('Exam runway')).not.toBeInTheDocument();
    expect(screen.queryByText('Weekly capacity')).not.toBeInTheDocument();
  });

  test('defaults Single and Full mock dates to the local Irish calendar day', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-06-03T00:30:00+01:00'));
    renderWarRoom();

    fireEvent.click(screen.getByRole('tab', { name: 'Review' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Results' }));
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

    fireEvent.click(screen.getByRole('tab', { name: 'Review' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Results' }));
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

    fireEvent.click(screen.getByRole('tab', { name: 'Review' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Results' }));
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

    fireEvent.click(screen.getByRole('tab', { name: 'Review' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Results' }));
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
    fireEvent.click(screen.getByRole('tab', { name: 'Review' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Results' }));

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

    const context = screen.getByRole('list', { name: 'Strategy context' });
    expect(within(context).getByText((_, element) => (
      element?.tagName === 'LI' && element.textContent === '1 day to exams'
    ))).toBeInTheDocument();

    await act(async () => {
      vi.advanceTimersByTime(31_000);
    });

    expect(within(context).getByText((_, element) => (
      element?.tagName === 'LI' && element.textContent === '0 days to exams'
    ))).toBeInTheDocument();
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

  test('supports keyboard navigation from Focus into every Review view', async () => {
    renderWarRoom();

    const focusTab = await screen.findByRole('tab', { name: 'Focus' });
    focusTab.focus();
    fireEvent.keyDown(focusTab, { key: 'ArrowRight' });

    expect(screen.getByRole('tab', { name: 'Review' })).toHaveAttribute('aria-selected', 'true');
    expect(await screen.findByRole('heading', { name: 'Coverage and confidence' })).toBeInTheDocument();

    const subjectsTab = screen.getByRole('tab', { name: 'Subjects' });
    expect(subjectsTab).toHaveAttribute('aria-selected', 'true');
    subjectsTab.focus();
    fireEvent.keyDown(subjectsTab, { key: 'ArrowRight' });

    const resultsTab = screen.getByRole('tab', { name: 'Results' });
    expect(resultsTab).toHaveFocus();
    expect(resultsTab).toHaveAttribute('aria-selected', 'true');
    expect(await screen.findByRole('heading', { name: 'Mock trajectory' })).toBeInTheDocument();

    fireEvent.keyDown(resultsTab, { key: 'ArrowRight' });

    const timeTab = screen.getByRole('tab', { name: 'Time plan' });
    expect(timeTab).toHaveFocus();
    expect(timeTab).toHaveAttribute('aria-selected', 'true');
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

    expect(await screen.findByRole('heading', { name: 'What matters now' })).toBeInTheDocument();
    expect(screen.queryByText(/days to exams/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/current points/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: 'Review' }));
    expect(await screen.findByRole('heading', { name: 'Coverage and confidence' })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: 'Time plan' })).not.toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: 'Results' })).not.toBeInTheDocument();
  });

  test('reconciles the active review and selected subject after settings edits', async () => {
    const profile = createDevStudentProfile(NOW);
    const { rerender } = render(
      <WarRoom uid="" profile={profile} timetableCompletions={{}} />,
    );

    fireEvent.click(await screen.findByRole('tab', { name: 'Review' }));
    fireEvent.click(await screen.findByRole('tab', { name: 'Time plan' }));
    expect(await screen.findByRole('heading', { name: 'Where the time goes' })).toBeInTheDocument();

    const updatedProfile = {
      ...profile,
      examStartDate: null,
      subjects: profile.subjects.slice(1).map(({ subjectName, level }) => ({ subjectName, level })),
    };
    rerender(<WarRoom uid="" profile={updatedProfile} timetableCompletions={{}} />);

    expect(await screen.findByRole('heading', { name: 'Coverage and confidence' })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: 'Time plan' })).not.toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: 'Results' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Geography' })).toHaveAttribute('aria-pressed', 'true');
  });
});
