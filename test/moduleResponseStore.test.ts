import { beforeEach, describe, expect, test, vi } from 'vitest';
const mocks = vi.hoisted(() => ({ getDoc: vi.fn(), setDoc: vi.fn(), auth: { currentUser: { uid: 'student-a' } as { uid: string } | null } }));
vi.mock('@/firebase', () => ({ db: {}, auth: mocks.auth }));
vi.mock('firebase/firestore', () => ({ doc: (...parts: unknown[]) => parts, getDoc: mocks.getDoc, setDoc: mocks.setDoc, FieldPath: class { constructor(public parts: unknown, ...rest: unknown[]) { this.parts = [parts, ...rest]; } } }));
import { changeModuleResponse, flushModuleResponses, forgetModuleResponseMemory, loadModuleResponses, moduleResponseEntry, responseStorageKey } from '@/services/moduleResponseStore';
const snapshot = (value: Record<string, unknown>) => ({ exists: () => true, data: () => value });
function deferred<T>() { let resolve!: (value: T) => void; const promise = new Promise<T>(done => { resolve = done; }); return { promise, resolve }; }
describe('module draft persistence', () => {
  beforeEach(() => { forgetModuleResponseMemory(); localStorage.clear(); mocks.auth.currentUser = { uid: 'student-a' }; mocks.getDoc.mockReset(); mocks.setDoc.mockReset(); mocks.setDoc.mockResolvedValue(undefined); });
  test('does not replace a new edit with a slow initial account read, even after the edit has saved', async () => {
    const read = deferred<ReturnType<typeof snapshot>>(); mocks.getDoc.mockReturnValue(read.promise);
    const entry = moduleResponseEntry('student-a', 'lesson'); const loading = loadModuleResponses(entry);
    changeModuleResponse(entry, 'plan', 'new plan'); await flushModuleResponses(entry);
    read.resolve(snapshot({ lesson: { plan: 'old plan', other: 'keep this' } })); await loading;
    expect(entry.snapshot.values).toEqual({ plan: 'new plan', other: 'keep this' });
  });
  test('serialises edits while a write is pending and replaces only the edited exercise', async () => {
    const first = deferred<void>(); mocks.setDoc.mockReturnValueOnce(first.promise);
    const entry = moduleResponseEntry('student-a', 'lesson');
    changeModuleResponse(entry, 'plan', { oldItem: true }); const saving = flushModuleResponses(entry);
    changeModuleResponse(entry, 'plan', { newItem: true });
    expect(mocks.setDoc).toHaveBeenCalledTimes(1); first.resolve(); await saving;
    expect(mocks.setDoc).toHaveBeenCalledTimes(2);
    expect(mocks.setDoc.mock.calls[1][1]).toEqual({ lesson: { plan: { newItem: true } } });
    expect(mocks.setDoc.mock.calls[1][2].mergeFields[0].parts).toEqual(['lesson', 'plan']);
    expect(entry.snapshot.status).toBe('saved');
  });
  test('retains failed edits for retry and reports the failure', async () => {
    mocks.setDoc.mockRejectedValueOnce(new Error('offline'));
    const entry = moduleResponseEntry('student-a', 'lesson'); changeModuleResponse(entry, 'plan', 'keep me');
    await flushModuleResponses(entry); expect(entry.snapshot.status).toBe('error');
    expect(JSON.parse(localStorage.getItem(responseStorageKey('student-a', 'lesson'))!).dirty.plan).toBe('keep me');
    await flushModuleResponses(entry); expect(entry.snapshot.status).toBe('saved');
  });
  test('isolates accounts and never sends a pending draft using another account’s credentials', async () => {
    const first = moduleResponseEntry('student-a', 'lesson'); changeModuleResponse(first, 'private', 'a only');
    mocks.auth.currentUser = { uid: 'student-b' };
    const second = moduleResponseEntry('student-b', 'lesson'); expect(second.snapshot.values).toEqual({});
    await flushModuleResponses(first); expect(mocks.setDoc).not.toHaveBeenCalled();
  });
  test('does not repopulate device storage after sign-out while a write is finishing', async () => {
    const pending = deferred<void>(); mocks.setDoc.mockReturnValue(pending.promise);
    const entry = moduleResponseEntry('student-a', 'lesson'); changeModuleResponse(entry, 'private', 'clear me'); const saving = flushModuleResponses(entry);
    window.dispatchEvent(new Event('nextstepuni:session-cleared')); localStorage.clear(); pending.resolve(); await saving;
    expect(localStorage.length).toBe(0); expect(moduleResponseEntry('student-a', 'lesson').snapshot.values).toEqual({});
  });
});
