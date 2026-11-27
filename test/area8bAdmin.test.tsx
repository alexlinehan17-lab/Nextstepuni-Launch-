/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 8b: the Admin dashboard in the agreed look keeps its working. The five places switch pages on a
 * phone and every page of today's eight tabs is still reachable (Year groups behind the Schools switch,
 * First run from Overview's second row, School access from the account menu); Log out in the account
 * menu signs out; the Schools / Year groups switch shows today's figures; the Students search narrows
 * the list already loaded by name and reads nothing new; one student opened shows the same figures;
 * delete still needs its password and calls the same function with the same argument; a failed delete
 * says so in the app's message, not a browser alert; the dashboard opens dark whatever the account's
 * settings record says, and logging out gives the page back as it was.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';

type Desc = { name: string };
const db = vi.hoisted(() => ({
  users: [] as Array<Record<string, unknown>>,
  progress: {} as Record<string, Record<string, unknown>>,
  reads: [] as string[],
}));
vi.mock('firebase/firestore', () => ({
  collection: vi.fn((_db: unknown, name: string) => ({ name })),
  doc: vi.fn((_db: unknown, name: string, id: string) => ({ name, id })),
  query: vi.fn((col: Desc) => ({ name: col.name })),
  where: vi.fn(), orderBy: vi.fn(), limit: vi.fn(), startAfter: vi.fn(), documentId: vi.fn(),
  serverTimestamp: vi.fn(), updateDoc: vi.fn(async () => undefined),
  getCountFromServer: vi.fn(async (q: Desc) => { db.reads.push(`count:${q.name}`); return { data: () => ({ count: 0 }) }; }),
  getDocs: vi.fn(async (q: Desc) => {
    db.reads.push(`docs:${q.name}`);
    if (q.name === 'users') return { docs: db.users.map(user => ({ id: user.uid, data: () => user })) };
    if (q.name === 'progress') return { docs: Object.entries(db.progress).map(([id, data]) => ({ id, data: () => data })) };
    return { docs: [] };
  }),
}));
const callable = vi.hoisted(() => vi.fn(async () => ({ data: { success: true } })));
const httpsCallable = vi.hoisted(() => vi.fn(() => callable));
vi.mock('firebase/functions', () => ({ getFunctions: vi.fn(() => ({})), httpsCallable }));
const reauth = vi.hoisted(() => vi.fn(async () => undefined));
vi.mock('../utils/reauthenticate', () => ({ reauthMethodFor: () => 'password', reauthenticateCurrentUser: reauth }));
vi.mock('../firebase', () => ({ default: {}, db: {}, auth: { currentUser: { uid: 'admin-uid', providerData: [{ providerId: 'password' }] } } }));

import { AdminDashboard } from '../components/AdminDashboard';
import { SCHOOLS } from '../schoolData';
import type { CourseData } from '../components/Library';

const COURSES = [
  { id: 'c1', category: 'architecture-mindset', sectionsCount: 4, title: 'One' },
  { id: 'c2', category: 'science-growth', sectionsCount: 2, title: 'Two' },
] as unknown as CourseData[];
const SCHOOL_A = SCHOOLS[0].id;
const SCHOOL_B = SCHOOLS[1].id;

function seed() {
  db.users = [
    { uid: 'u1', name: 'Aoife Testwell', school: SCHOOL_A, yearGroup: '6th', avatar: 'star-crew:maker' },
    { uid: 'u2', name: 'Cian Fakenham', school: SCHOOL_A, yearGroup: '6th', avatar: 'star-crew:maker' },
    { uid: 'u3', name: 'Niamh Example', school: SCHOOL_A, yearGroup: '5th', avatar: 'star-crew:maker' },
    { uid: 'u4', name: 'Oisín Specimen', school: SCHOOL_B, yearGroup: '6th', avatar: 'star-crew:maker' },
    { uid: 'staff', name: 'A Counsellor', school: SCHOOL_A, role: 'gc' },
  ];
  db.progress = {
    u1: { c1: { unlockedSection: 4 }, c2: { unlockedSection: 1 } }, // 100% and 50%: overall 75, started 2, complete 1
    u2: { c1: { unlockedSection: 1 } }, // 25% and 0: overall 12.5
    u3: {},
    u4: { c2: { unlockedSection: 2 } }, // 0 and 100: overall 50
  };
  db.reads = [];
}

function setWidth(width: number) {
  window.matchMedia = ((query: string) => {
    const min = Number(/min-width:\s*(\d+)/.exec(query)?.[1] ?? 0);
    return { matches: width >= min, media: query, addEventListener: () => {}, removeEventListener: () => {}, addListener: () => {}, removeListener: () => {}, onchange: null, dispatchEvent: () => false };
  }) as unknown as typeof window.matchMedia;
}

async function open(width = 390, onLogout = vi.fn()) {
  setWidth(width);
  const view = render(<AdminDashboard allCourses={COURSES} onLogout={onLogout} />);
  await screen.findByText(/students? (are|is) yet to get started|Every student in this view has started learning/);
  return { ...view, onLogout };
}

const places = () => screen.getByRole('navigation', { name: 'Admin dashboard' });

beforeEach(() => {
  seed();
  localStorage.clear();
  document.documentElement.classList.remove('dark');
  window.scrollTo = vi.fn() as unknown as typeof window.scrollTo;
  callable.mockClear(); httpsCallable.mockClear(); reauth.mockClear();
});
afterEach(() => { cleanup(); document.documentElement.classList.remove('dark'); });

describe('the five places on a phone', () => {
  test('switch pages, and every page of today\'s eight tabs is still reachable', async () => {
    await open();
    expect(within(places()).getAllByRole('button').map(b => b.textContent)).toEqual(['Overview', 'Students', 'Schools', 'Programme', 'Feedback']);
    expect(screen.getByRole('heading', { level: 1, name: 'What needs attention today' })).toBeInTheDocument();

    fireEvent.click(within(places()).getByRole('button', { name: 'Students' }));
    expect(screen.getByRole('heading', { level: 1, name: 'Students' })).toBeInTheDocument();

    fireEvent.click(within(places()).getByRole('button', { name: 'Schools' }));
    expect(screen.getByRole('heading', { level: 1, name: 'Schools' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: 'Year groups' }));
    expect(screen.getByRole('button', { name: 'Open students in 6th Year' })).toBeInTheDocument();
    expect(within(places()).getByRole('button', { name: 'Schools' })).toHaveAttribute('aria-current', 'page');

    fireEvent.click(within(places()).getByRole('button', { name: 'Programme' }));
    expect(screen.getByRole('heading', { level: 1, name: 'Programme evidence' })).toBeInTheDocument();

    fireEvent.click(within(places()).getByRole('button', { name: 'Feedback' }));
    expect(screen.getByRole('heading', { level: 1, name: 'Feedback inbox' })).toBeInTheDocument();

    // First run: the second row on Overview, with Back.
    fireEvent.click(within(places()).getByRole('button', { name: 'Overview' }));
    fireEvent.click(screen.getByRole('button', { name: /Are students getting in\?/ }));
    expect(screen.getByRole('heading', { level: 1, name: 'Are students getting in?' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Refresh funnel counts' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Back to Overview' }));
    expect(screen.getByRole('heading', { level: 1, name: 'What needs attention today' })).toBeInTheDocument();

    // School access: from the account menu, with Back.
    fireEvent.click(screen.getByRole('button', { name: 'Your account' }));
    fireEvent.click(await screen.findByRole('menuitem', { name: /School access/ }));
    expect(await screen.findByRole('heading', { level: 1, name: 'School logins' })).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: 'Set password' })).toHaveLength(SCHOOLS.length * 2);
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByRole('heading', { level: 1, name: 'What needs attention today' })).toBeInTheDocument();
  });

  test('Log out in the account menu signs out', async () => {
    const { onLogout } = await open();
    fireEvent.click(screen.getByRole('button', { name: 'Your account' }));
    fireEvent.click(await screen.findByRole('menuitem', { name: /Log out/ }));
    expect(onLogout).toHaveBeenCalledTimes(1);
  });

  test('on a laptop the sidebar lists the five places and School access, and Log out sits in the menu under your name', async () => {
    const { onLogout } = await open(1280);
    const side = screen.getByRole('complementary', { name: 'Admin dashboard' });
    expect(within(side).getAllByRole('button').map(b => b.textContent).slice(0, 6)).toEqual(['Overview', 'Students', 'Schools', 'Programme', 'Feedback', 'School access']);
    fireEvent.click(within(side).getByRole('button', { name: 'School access' }));
    expect(screen.getByRole('heading', { level: 1, name: 'School logins' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Your account: Admin' }));
    fireEvent.click(await screen.findByRole('menuitem', { name: 'Log out' }));
    expect(onLogout).toHaveBeenCalledTimes(1);
  });
});

describe('figures', () => {
  test('Schools and Year groups show today\'s figures: students, the share started, the average progress', async () => {
    await open();
    fireEvent.click(within(places()).getByRole('button', { name: 'Schools' }));
    const a = screen.getByRole('button', { name: `Open students in ${SCHOOLS[0].name}` });
    // u1 75, u2 12.5, u3 0: three students, two started (67%), average 29.
    expect(a).toHaveTextContent('3 students · 67% started');
    expect(a).toHaveTextContent('29%');
    fireEvent.click(screen.getByRole('radio', { name: 'Year groups' }));
    const sixth = screen.getByRole('button', { name: 'Open students in 6th Year' });
    // u1 75, u2 12.5, u4 50: three, all started, average 46.
    expect(sixth).toHaveTextContent('3 students · 100% started');
    expect(sixth).toHaveTextContent('46%');
  });

  test('on a laptop the full table keeps every column, Completed a course included', async () => {
    await open(1280);
    fireEvent.click(within(screen.getByRole('complementary', { name: 'Admin dashboard' })).getByRole('button', { name: 'Schools' }));
    const row = screen.getByRole('button', { name: `Open students in ${SCHOOLS[0].name}` }).closest('[role=row]') as HTMLElement;
    expect(within(row).getAllByRole('cell').map(cell => cell.textContent)).toEqual([SCHOOLS[0].name, '3', '267%', '29%', '1', 'Students']);
  });
});

describe('students', () => {
  test('the search narrows the list already loaded, by name, and reads nothing new', async () => {
    await open();
    fireEvent.click(within(places()).getByRole('button', { name: 'Students' }));
    expect(screen.getAllByRole('button', { name: /^View / })).toHaveLength(4);
    const readsBefore = db.reads.length;
    fireEvent.change(screen.getByRole('searchbox', { name: 'Search students' }), { target: { value: 'oisín' } });
    expect(screen.getAllByRole('button', { name: /^View / }).map(b => b.getAttribute('aria-label'))).toEqual(['View Oisín Specimen']);
    fireEvent.change(screen.getByRole('searchbox', { name: 'Search students' }), { target: { value: 'zzz' } });
    expect(screen.getByText('No matching students')).toBeInTheDocument();
    expect(db.reads.length).toBe(readsBefore);
  });

  test('opening a student shows the same figures as today\'s card', async () => {
    await open();
    fireEvent.click(within(places()).getByRole('button', { name: 'Students' }));
    fireEvent.click(screen.getByRole('button', { name: 'View Aoife Testwell' }));
    expect(screen.getByRole('heading', { level: 1, name: 'Aoife Testwell' })).toBeInTheDocument();
    const figures = document.querySelector('.adm-fa') as HTMLElement;
    expect(figures.textContent).toBe('Overall75%Started2Complete1');
    const areas = [...document.querySelectorAll('.adm-ahead')].map(el => el.textContent);
    expect(areas.slice(0, 2)).toEqual(['The Architecture of your Mindset100%', 'The Science of Growth50%']);
    expect(areas).toHaveLength(5);
    fireEvent.click(screen.getByRole('button', { name: 'Back to Students' }));
    expect(screen.getByRole('heading', { level: 1, name: 'Students' })).toBeInTheDocument();
  });
});

describe('delete', () => {
  test('still needs the password, then calls the same function with the same argument', async () => {
    await open(1280);
    fireEvent.click(within(screen.getByRole('complementary', { name: 'Admin dashboard' })).getByRole('button', { name: 'Students' }));
    fireEvent.click(screen.getByRole('button', { name: 'Delete Cian Fakenham' }));
    const dialog = await screen.findByRole('alertdialog', { name: 'Delete student account' });
    expect(dialog).toHaveTextContent('Delete Cian Fakenham and all associated progress and profile data? This action cannot be undone.');
    const remove = within(dialog).getByRole('button', { name: 'Delete account' });
    expect(remove).toHaveAttribute('aria-disabled', 'true');
    fireEvent.click(remove);
    expect(reauth).not.toHaveBeenCalled();
    expect(callable).not.toHaveBeenCalled();
    expect(within(dialog).getByLabelText('Re-enter your password')).toHaveFocus();
    fireEvent.change(within(dialog).getByLabelText('Re-enter your password'), { target: { value: 'secret-pass' } });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Delete account' }));
    await waitFor(() => expect(callable).toHaveBeenCalledTimes(1));
    expect(reauth).toHaveBeenCalledWith(expect.anything(), 'secret-pass');
    expect(httpsCallable).toHaveBeenCalledWith(expect.anything(), 'requestAccountDeletion');
    expect(callable).toHaveBeenCalledWith({ uid: 'u2' });
    await waitFor(() => expect(screen.queryByRole('button', { name: 'Delete Cian Fakenham' })).toBeNull());
  });

  test('Cancel sends nothing; a failed delete says so in the app\'s message, never a browser alert', async () => {
    const alert = vi.spyOn(window, 'alert').mockImplementation(() => {});
    await open(1280);
    fireEvent.click(within(screen.getByRole('complementary', { name: 'Admin dashboard' })).getByRole('button', { name: 'Students' }));
    fireEvent.click(screen.getByRole('button', { name: 'Delete Aoife Testwell' }));
    let dialog = await screen.findByRole('alertdialog', { name: 'Delete student account' });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Cancel' }));
    await waitFor(() => expect(screen.queryByRole('alertdialog')).toBeNull());
    expect(callable).not.toHaveBeenCalled();

    callable.mockRejectedValueOnce(new Error('denied'));
    fireEvent.click(screen.getByRole('button', { name: 'Delete Aoife Testwell' }));
    dialog = await screen.findByRole('alertdialog', { name: 'Delete student account' });
    fireEvent.change(within(dialog).getByLabelText('Re-enter your password'), { target: { value: 'secret-pass' } });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Delete account' }));
    expect(await screen.findAllByText('Failed to delete student. You may not have permission.')).not.toHaveLength(0);
    expect(alert).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Delete Aoife Testwell' })).toBeInTheDocument();
    alert.mockRestore();
  });
});

describe('dark by default', () => {
  test.each([
    ['no settings record', null],
    ['a saved darkMode: false (useSettings writes that default; the account has no switch)', { darkMode: false }],
    ['a saved darkMode: true', { darkMode: true }],
  ])('opens dark with %s, holds it while open, and logging out gives the page back', async (_case, saved) => {
    if (saved) localStorage.setItem('nextstep-settings:admin-uid', JSON.stringify(saved));
    const before = JSON.stringify(localStorage);
    const view = await open();
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    // The app's own settings effect may clear the class: the dashboard keeps it on while open.
    act(() => { document.documentElement.classList.remove('dark'); });
    await waitFor(() => expect(document.documentElement.classList.contains('dark')).toBe(true));
    view.unmount();
    expect(document.documentElement.classList.contains('dark')).toBe(false);
    expect(JSON.stringify(localStorage)).toBe(before);
  });

  test('a page that was already dark stays dark after logging out', async () => {
    document.documentElement.classList.add('dark');
    const view = await open();
    view.unmount();
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });
});
