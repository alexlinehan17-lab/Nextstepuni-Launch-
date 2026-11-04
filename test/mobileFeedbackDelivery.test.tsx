import React, { useState } from 'react';
import { beforeEach, afterEach, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { KnowledgeTree } from '../components/KnowledgeTree';
import FeedbackModal from '../components/FeedbackModal';
import AdminFeedbackInbox from '../components/AdminFeedbackInbox';
import { submitAnonymousFeedback } from '../functions/src/anonymousFeedback';
import { useSettings } from '../hooks/useSettings';

// Exercise the real phone entry point, callable handler and inbox together.
// Only authentication and Firestore transport are replaced by an in-memory store.
const storage = vi.hoisted(() => ({ records: new Map<string, Record<string, unknown>>() }));
const firestorePath = await vi.hoisted(async () => {
  const { createRequire } = await import('node:module');
  const { dirname, resolve } = await import('node:path');
  const require = createRequire(resolve(process.cwd(), 'functions/package.json'));
  const root = resolve(dirname(require.resolve('firebase-admin')), '..');
  return resolve(root, require(resolve(root, 'package.json')).exports['./firestore'].import);
});
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
vi.mock('../functions/src/security', () => ({ CALLABLE_OPTIONS: {}, assertUnrevokedAuth: vi.fn() }));
vi.mock(firestorePath, () => ({
  FieldValue: { serverTimestamp: () => ({ toDate: () => new Date('2026-10-08T12:00:00Z') }) },
  Timestamp: { fromDate: (date: Date) => date },
  getFirestore: () => ({
    collection: (name: string) => ({ doc: (id = 'generated-id') => ({
      path: `${name}/${id}`,
      get: async () => ({ data: () => ({ school: 'test-school' }) }),
    }) }),
    runTransaction: async (run: (transaction: unknown) => Promise<void>) => run({
      get: async ({ path }: { path: string }) => ({ exists: storage.records.has(path), data: () => storage.records.get(path) }),
      set: ({ path }: { path: string }, value: Record<string, unknown>) => storage.records.set(path, value),
      create: ({ path }: { path: string }, value: Record<string, unknown>) => storage.records.set(path, value),
    }),
  }),
}));
vi.mock('firebase/functions', () => ({
  getFunctions: () => ({}),
  httpsCallable: (_functions: unknown, name: string) => async (data: unknown) => {
    expect(name).toBe('submitAnonymousFeedback');
    const result = await submitAnonymousFeedback.run({
      data, auth: { uid: 'test-student', token: {} },
    } as Parameters<typeof submitAnonymousFeedback.run>[0]);
    return { data: result };
  },
}));
vi.mock('firebase/firestore', () => {
  type MemoryQuery = { path: string; filters: { field?: string; value?: unknown }[] };
  const docs = ({ path, filters }: MemoryQuery) => [...storage.records.entries()]
    .filter(([key, value]) => key.startsWith(`${path}/`) && filters.every(filter => !filter.field || value[filter.field] === filter.value))
    .map(([id, value]) => ({ id, data: () => value }));
  return {
    collection: (_db: unknown, path: string) => path,
    query: (path: string, ...filters: MemoryQuery['filters']) => ({ path, filters }),
    where: (field: string, _op: string, value: unknown) => ({ field, value }),
    orderBy: () => ({}), limit: () => ({}), startAfter: () => ({}),
    getDocs: async (query: MemoryQuery) => ({ docs: docs(query) }),
    getCountFromServer: async (query: MemoryQuery) => ({ data: () => ({ count: docs(query).length }) }),
    doc: vi.fn(), getDoc: vi.fn(), setDoc: vi.fn(), updateDoc: vi.fn(), serverTimestamp: vi.fn(),
  };
});

const noop = () => {};
function PhoneHome() {
  const [open, setOpen] = useState(false);
  const { settings, updateSetting } = useSettings();
  return <>
    <KnowledgeTree uid="test-student" userName="Sample Student" allCourses={[]} userProgress={{}} categoryTitles={{} as never}
      settings={settings} updateSetting={updateSetting} completedCount={0} totalCount={0}
      onSelectCategory={noop} onGoToModules={noop} onGoToInnovationZone={noop} onGoToDashboard={noop}
      onGoToLearningPaths={noop} onGoToJourney={noop} onSelectModule={noop} onLogout={noop}
      onOpenSettings={noop} onOpenPassport={noop} onOpenFeedback={() => setOpen(true)} />
    <FeedbackModal open={open} onClose={() => setOpen(false)} context={{ surface: 'tree' }} />
  </>;
}

beforeEach(() => {
  storage.records.clear();
  localStorage.clear();
  localStorage.setItem('nsu-coachmarks:test-student', '1');
  window.scrollTo = vi.fn();
});
afterEach(() => vi.restoreAllMocks());

test.each([
  ['iPhone', 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X)', 'ios'],
  ['Android', 'Mozilla/5.0 (Linux; Android 15; Pixel 9)', 'android'],
])('%s Home feedback is saved anonymously and appears in the admin New inbox', async (_device, userAgent, platform) => {
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue(userAgent);
  const student = render(<PhoneHome />);
  const trigger = screen.getByRole('button', { name: 'Feedback' });
  trigger.focus();
  fireEvent.click(trigger);
  expect(screen.getByRole('dialog', { name: 'Help us improve' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('radio', { name: 'Something isn’t working' }));
  const message = `The study timer on ${platform} does not keep my chosen duration.`;
  fireEvent.change(screen.getByRole('textbox'), { target: { value: message } });
  fireEvent.click(screen.getByRole('button', { name: 'Send anonymously' }));
  expect(await screen.findByText('Sent without account details.')).toBeInTheDocument();
  const saved = storage.records.get('anonymousFeedback/generated-id');
  expect(saved).toMatchObject({ message, platform, category: 'broken', status: 'new', context: { surface: 'tree' } });
  for (const key of ['uid', 'name', 'email', 'school']) expect(saved).not.toHaveProperty(key);
  fireEvent.click(screen.getAllByRole('button', { name: 'Close' })[0]);
  await waitFor(() => expect(trigger).toHaveFocus());
  student.unmount();
  render(<AdminFeedbackInbox />);
  expect(await screen.findByText(message)).toBeInTheDocument();
  expect(screen.getByText(platform)).toBeInTheDocument();
  expect(screen.getByRole('tab', { name: /^New\s*1$/ })).toHaveAttribute('aria-selected', 'true');
});
