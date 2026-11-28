/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 8a: the counsellor's dashboard in the agreed look keeps its working. The four places switch
 * pages on a phone; the Overview's rows open the same student; the Students search and each of the
 * nine status filters keep exactly the students today's filter keeps; the status guide lists every
 * status the code can produce; Broadcast still needs a message before it sends, and sends the same
 * payload; Export builds the same files from the same students; cohort tags are set and cleared from a
 * row's menu; the row menu flags, resets and deletes through the same handlers.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { GCOverview, STATUS_GUIDE } from '../components/gc/GCOverview';
import GCHandInGrid from '../components/gc/GCHandInGrid';
import GCExportModal from '../components/gc/GCExportModal';
import { mapProgressDocToStudent } from '../components/GCDashboard';
import { getStudentStatus, getVisibleCourses } from '../components/gc/gcUtils';
import { getTags, _resetCohortCacheForTests } from '../components/gc/cohortTags';
import { STATUS_CONFIG } from '../utils/studentStatus';
import { STAFF_BROADCASTS } from '../data/staffEncouragement';
import type { GCStudentFullData, StudentStatus } from '../components/gc/gcTypes';
import type { SessionUser } from '../utils/authUtils';
import type { EarlyWarningAlert } from '../components/gc/gcAlerts';
import type { FlagData, FlagPriority } from '../hooks/useGCFlags';

vi.mock('firebase/firestore', () => ({
  doc: vi.fn(() => ({})),
  getDoc: vi.fn(async () => ({ exists: () => false, data: () => ({}) })),
  setDoc: vi.fn(async () => undefined),
  collection: vi.fn(), query: vi.fn(), where: vi.fn(), limit: vi.fn(),
  getDocs: vi.fn(async () => ({ docs: [] })),
}));
const callable = vi.fn(async () => ({ data: { success: true, delivered: 1 } }));
vi.mock('firebase/functions', () => ({ getFunctions: vi.fn(() => ({})), httpsCallable: vi.fn(() => callable) }));
const csv = vi.hoisted(() => ({
  generateStudentProgressCSV: vi.fn(() => 'progress'),
  generateAttendanceCSV: vi.fn(() => 'attendance'),
  generateSubjectHealthCSV: vi.fn(() => 'health'),
  generateStudentDetailCSV: vi.fn(() => 'detail'),
  downloadCSV: vi.fn(),
}));
vi.mock('../utils/exportCsv', () => csv);
const pdf = vi.hoisted(() => ({ generateReport: vi.fn(async () => undefined) }));
vi.mock('../utils/exportPdf', () => pdf);
const studentCsv = vi.hoisted(() => vi.fn(() => 'name,progress'));
vi.mock('../components/gc/gcUtils', async importOriginal => ({ ...(await importOriginal<Record<string, unknown>>()), generateStudentCSV: studentCsv }));

const DAY = 86400000;
const keyDaysAgo = (n: number) => { const d = new Date(Date.now() - n * DAY); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
const isoDaysAgo = (n: number) => new Date(Date.now() - n * DAY).toISOString();

function student(uid: string, name: string, createdDaysAgo: number, blockDaysAgo: number[], yearGroup: SessionUser['yearGroup'] = '6th'): GCStudentFullData {
  const user = { uid, name, avatar: 'star-crew:maker', email: `${uid}@example.org`, school: 's1', role: 'student', createdAt: isoDaysAgo(createdDaysAgo), yearGroup } as unknown as SessionUser;
  const timetableCompletions: Record<string, string[]> = {};
  for (const n of blockDaysAgo) timetableCompletions[keyDaysAgo(n)] = ['b1'];
  return mapProgressDocToStudent(user, { timetableCompletions });
}

const STUDENTS: GCStudentFullData[] = [
  student('nia', 'Niamh New', 2, []),
  student('ian', 'Ian Inactive', 40, []),
  student('ruth', 'Ruth Risk', 90, [20, 21, 22]),
  student('dara', 'Dara Drift', 90, [10, 11]),
  student('tom', 'Tom Thrive', 90, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
  student('ali', 'Alan Again', 90, [2], '3rd'),
];

function flagsApi(initial: Record<string, FlagPriority> = { ruth: 'high' }) {
  const flags: Record<string, FlagData> = {};
  for (const [uid, priority] of Object.entries(initial)) flags[uid] = { priority, flaggedAt: 1 } as FlagData;
  return {
    flags,
    flagStudent: vi.fn(async () => undefined),
    unflagStudent: vi.fn(async () => undefined),
    updateFlagPriority: vi.fn(async () => undefined),
    isFlagged: (uid: string) => uid in flags,
    getFlagData: (uid: string) => flags[uid] ?? null,
    flaggedStudentUids: Object.keys(flags),
  };
}

const statusOf = (s: GCStudentFullData) => getStudentStatus(s, getVisibleCourses(s, []));

/** Today's filter, written out from the code before area 8a (GCOverview.tsx at 240be654). */
function todaysFilter(filter: string, flagged: Set<string>): string[] {
  return STUDENTS.filter(s => {
    const st = statusOf(s);
    if (filter === 'flagged') return flagged.has(s.user.uid);
    if (filter === 'needs-attention') return st === 'drifting' || st === 'at-risk' || flagged.has(s.user.uid);
    if (filter !== 'all') return st === filter;
    return true;
  }).map(s => s.user.name).sort();
}

function setWidth(width: number) {
  window.matchMedia = ((query: string) => {
    const min = /min-width:\s*(\d+)px/.exec(query);
    return { matches: min ? width >= Number(min[1]) : false, media: query, onchange: null, addEventListener: () => {}, removeEventListener: () => {}, addListener: () => {}, removeListener: () => {}, dispatchEvent: () => false };
  }) as unknown as typeof window.matchMedia;
}

beforeEach(() => { setWidth(390); callable.mockClear(); _resetCohortCacheForTests(); });
afterEach(() => cleanup());

const renderOverview = (props: Partial<React.ComponentProps<typeof GCOverview>> = {}) => {
  const onSelectStudent = vi.fn();
  const gcFlags = flagsApi();
  const view = render(<GCOverview studentData={STUDENTS} allCourses={[]} school="s1" onSelectStudent={onSelectStudent} gcFlags={gcFlags} {...props} />);
  return { ...view, onSelectStudent, gcFlags };
};

describe('the fixtures', () => {
  test('cover at least four different statuses', () => {
    expect(new Set(STUDENTS.map(statusOf)).size).toBeGreaterThanOrEqual(4);
  });
});

describe('Students on a phone (area 8a)', () => {
  const shownNames = () => screen.getAllByRole('button', { name: /^View / }).map(b => (b.getAttribute('aria-label') ?? '').replace(/^View /, '').split(',')[0]).sort();

  test('each of the nine status filters keeps the same students as today', async () => {
    renderOverview({ place: 'students' });
    const flagged = new Set(['ruth']);
    const filters: [string, string][] = [
      ['All', 'all'], ['Needs attention', 'needs-attention'], ['Thriving', 'thriving'], ['Active', 'active'], ['New', 'new'],
      ['Drifting', 'drifting'], ['At risk', 'at-risk'], ['Inactive', 'inactive'], ['Flagged', 'flagged'],
    ];
    for (const [label, key] of filters) {
      fireEvent.click(screen.getByRole('button', { name: /^Filter and sort students/ }));
      const sheet = await screen.findByRole('dialog', { name: 'Filter students' });
      fireEvent.click(within(sheet).getByRole('radio', { name: new RegExp(`^${label} `) }));
      const expected = todaysFilter(key, flagged);
      // The button says how many will show before it is pressed.
      fireEvent.click(within(sheet).getByRole('button', { name: new RegExp(`^Show ${expected.length} student`) }));
      await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Filter students' })).toBeNull());
      if (expected.length === 0) expect(screen.getByText('No students match your filters.')).toBeInTheDocument();
      else expect(shownNames()).toEqual(expected);
    }
  });

  test('search keeps the same students as today, and a row opens that student', () => {
    const { onSelectStudent } = renderOverview({ place: 'students' });
    fireEvent.change(screen.getByRole('searchbox', { name: 'Search students' }), { target: { value: 'ra' } });
    expect(shownNames()).toEqual(STUDENTS.filter(s => s.user.name.toLowerCase().includes('ra')).map(s => s.user.name).sort());
    fireEvent.click(screen.getByRole('button', { name: /^View Dara Drift/ }));
    expect(onSelectStudent).toHaveBeenCalledWith('dara');
  });

  test('the status guide lists every status the code can produce, in its words', async () => {
    renderOverview({ place: 'students' });
    fireEvent.click(screen.getByRole('button', { name: 'Status guide' }));
    const sheet = await screen.findByRole('dialog', { name: 'Status guide' });
    const all = Object.keys(STATUS_CONFIG) as StudentStatus[];
    expect(STATUS_GUIDE.map(g => g.status).sort()).toEqual([...all].sort());
    for (const g of STATUS_GUIDE) expect(within(sheet).getByText(g.desc)).toBeInTheDocument();
  });

  test('Export list downloads today\'s CSV of the students in view', () => {
    URL.createObjectURL = vi.fn(() => 'blob:x');
    URL.revokeObjectURL = vi.fn();
    renderOverview({ place: 'students' });
    fireEvent.click(screen.getByRole('button', { name: 'Export list' }));
    expect(studentCsv).toHaveBeenCalledWith(STUDENTS, []);
  });
});

describe('the Overview on a phone (area 8a)', () => {
  test('a warning row and an attention row open the same student as today', () => {
    const alert: EarlyWarningAlert = { id: 'a1', studentUid: 'ruth', studentName: 'Ruth Risk', studentAvatar: 'star-crew:maker', severity: 'urgent', title: 'Inactive for over a week', description: 'Was previously active', metric: 1 } as EarlyWarningAlert;
    const { onSelectStudent } = renderOverview({ alerts: [alert] });
    fireEvent.click(screen.getByRole('button', { name: /^View Ruth Risk: Urgent, Inactive for over a week/ }));
    expect(onSelectStudent).toHaveBeenLastCalledWith('ruth');
    fireEvent.click(screen.getByRole('button', { name: /^View Dara Drift, status: Drifting/ }));
    expect(onSelectStudent).toHaveBeenLastCalledWith('dara');
  });

  test('"See all" opens the Students place', () => {
    const onOpenStudents = vi.fn();
    renderOverview({ onOpenStudents });
    fireEvent.click(screen.getByRole('button', { name: /^See all 6 students/ }));
    expect(onOpenStudents).toHaveBeenCalled();
  });

  test('Broadcast waits for a message, then sends the same payload as today', async () => {
    renderOverview();
    fireEvent.click(screen.getByRole('button', { name: 'Broadcast' }));
    const sheet = await screen.findByRole('dialog', { name: 'Broadcast message' });
    fireEvent.click(within(sheet).getByRole('button', { name: /^Send to 6/ }));
    expect(callable).not.toHaveBeenCalled();
    fireEvent.click(within(sheet).getByRole('radio', { name: STAFF_BROADCASTS[1].text }));
    await act(async () => { fireEvent.click(within(sheet).getByRole('button', { name: /^Send to 6/ })); });
    expect(callable).toHaveBeenCalledWith({ studentUids: STUDENTS.map(s => s.user.uid), kind: 'broadcast', messageId: STAFF_BROADCASTS[1].id });
  });

  test('Broadcast to one year sends to that year only', async () => {
    renderOverview();
    fireEvent.click(screen.getByRole('button', { name: 'Broadcast' }));
    const sheet = await screen.findByRole('dialog', { name: 'Broadcast message' });
    fireEvent.click(within(sheet).getByRole('button', { name: /^3rd Year/ }));
    fireEvent.click(within(sheet).getByRole('radio', { name: STAFF_BROADCASTS[0].text }));
    await act(async () => { fireEvent.click(within(sheet).getByRole('button', { name: /^Send to 1/ })); });
    expect(callable).toHaveBeenCalledWith({ studentUids: ['ali'], kind: 'broadcast', messageId: STAFF_BROADCASTS[0].id });
  });
});

describe('Export (area 8a)', () => {
  test('builds the same files from the same students as today', async () => {
    const onClose = vi.fn();
    render(<GCExportModal isOpen onClose={onClose} studentData={STUDENTS} allCourses={[]} school="s1" />);
    const sheet = await screen.findByRole('dialog', { name: 'Export data' });
    fireEvent.click(within(sheet).getByRole('button', { name: 'Export CSV' }));
    expect(csv.generateStudentProgressCSV).toHaveBeenCalledWith(STUDENTS, []);
    expect(csv.generateAttendanceCSV).toHaveBeenCalledWith(STUDENTS);
    expect(csv.generateSubjectHealthCSV).toHaveBeenCalledWith(STUDENTS);
    const day = new Date().toISOString().split('T')[0];
    expect(csv.downloadCSV.mock.calls.map(c => c[1])).toEqual([`progress-summary-${day}.csv`, `attendance-${day}.csv`, `subject-health-${day}.csv`]);
    await act(async () => { fireEvent.click(within(sheet).getByRole('button', { name: 'Export PDF' })); });
    expect(pdf.generateReport).toHaveBeenCalledWith({ school: 's1', students: STUDENTS, allCourses: [], includeProgress: true, includeAttendance: true, includeSubjectHealth: true, individualStudent: undefined });
  });
});

describe('Practice (area 8a)', () => {
  test('a cohort tag is set and cleared from a row\'s menu on a phone', async () => {
    render(<GCHandInGrid students={STUDENTS} allCourses={[]} school="s1" onSelectStudent={vi.fn()} />);
    const open = () => fireEvent.click(screen.getByRole('button', { name: 'Cohort tags for Dara Drift' }));
    open();
    fireEvent.click(await screen.findByRole('menuitemcheckbox', { name: 'DEIS' }));
    await waitFor(() => expect(getTags('s1', 'dara')).toEqual(['DEIS']));
    expect(screen.getByRole('menuitemcheckbox', { name: 'DEIS' })).toHaveAttribute('aria-checked', 'true');
    fireEvent.click(screen.getByRole('menuitemcheckbox', { name: 'DEIS' }));
    await waitFor(() => expect(getTags('s1', 'dara')).toEqual([]));
  });

  test('on a laptop each tag is a button that takes an ink outline when on', () => {
    setWidth(1280);
    render(<GCHandInGrid students={STUDENTS} allCourses={[]} school="s1" onSelectStudent={vi.fn()} />);
    const row = screen.getByRole('button', { name: 'Dara Drift' }).closest('[role="row"]') as HTMLElement;
    const priority = within(row).getByRole('button', { name: 'Priority' });
    expect(priority).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(priority);
    expect(getTags('s1', 'dara')).toEqual(['Priority']);
    expect(within(row).getByRole('button', { name: 'Priority' })).toHaveAttribute('aria-pressed', 'true');
  });
});

describe('All students on a laptop (area 8a)', () => {
  test('the row menu flags, resets and deletes through today\'s handlers', async () => {
    setWidth(1280);
    const onResetPassword = vi.fn();
    const onDeleteStudent = vi.fn();
    const { gcFlags } = renderOverview({ onResetPassword, onDeleteStudent });
    fireEvent.click(screen.getByRole('button', { name: 'Actions for Dara Drift' }));
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Flagged, high priority' }));
    expect(gcFlags.flagStudent).toHaveBeenCalledWith('dara', 'high');
    fireEvent.click(screen.getByRole('button', { name: 'Actions for Ruth Risk' }));
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Flagged, normal priority' }));
    expect(gcFlags.updateFlagPriority).toHaveBeenCalledWith('ruth', 'normal');
    fireEvent.click(screen.getByRole('button', { name: 'Actions for Ruth Risk' }));
    fireEvent.click(await screen.findByRole('menuitem', { name: 'Remove flag' }));
    expect(gcFlags.unflagStudent).toHaveBeenCalledWith('ruth');
    fireEvent.click(screen.getByRole('button', { name: 'Actions for Tom Thrive' }));
    fireEvent.click(await screen.findByRole('menuitem', { name: 'Reset password' }));
    expect(onResetPassword).toHaveBeenCalledWith('tom');
    fireEvent.click(screen.getByRole('button', { name: 'Actions for Tom Thrive' }));
    fireEvent.click(await screen.findByRole('menuitem', { name: 'Delete account' }));
    expect(onDeleteStudent).toHaveBeenCalledWith(STUDENTS[4].user);
  });

  test('each status filter button keeps the same students as today', () => {
    setWidth(1280);
    renderOverview();
    const table = screen.getByRole('table', { name: 'All students' });
    for (const [label, key] of [['Drifting', 'drifting'], ['At risk', 'at-risk'], ['Flagged', 'flagged'], ['Needs attention', 'needs-attention'], ['All', 'all']] as const) {
      fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${label} \\d`) }));
      const names = within(table).queryAllByRole('row').slice(1).map(r => within(r).getAllByRole('button')[0].textContent ?? '').sort();
      expect(names).toEqual(todaysFilter(key, new Set(['ruth'])));
    }
  });
});
