import { doc, FieldPath, getDoc, setDoc } from 'firebase/firestore';
import { auth, db } from '../firebase';
import { DEMO_STUDENT_UID } from '../data/devStudent';

export type ResponseSaveStatus = 'loading' | 'saving' | 'saved' | 'device' | 'error';
export interface ResponseSnapshot { values: Record<string, any>; loaded: boolean; status: ResponseSaveStatus }
interface Entry {
  uid: string | null;
  moduleId: string;
  snapshot: ResponseSnapshot;
  listeners: Set<() => void>;
  dirty: Record<string, any>;
  edited: Record<string, any>;
  timer?: ReturnType<typeof setTimeout>;
  inFlight?: Promise<void>;
  load?: Promise<void>;
  disposed?: boolean;
}
const entries = new Map<string, Entry>();
const accountReads = new Map<string, Promise<Record<string, any>>>();
export const responseStorageKey = (uid: string, moduleId: string) => `nextstepuni:response-draft:${uid}:${moduleId}`;
function publish(entry: Entry, patch: Partial<ResponseSnapshot>) {
  if (entry.disposed) return;
  entry.snapshot = { ...entry.snapshot, ...patch };
  entry.listeners.forEach(listener => listener());
}
function remember(entry: Entry) {
  if (!entry.uid || entry.disposed) return;
  try { localStorage.setItem(responseStorageKey(entry.uid, entry.moduleId), JSON.stringify({ values: entry.snapshot.values, dirty: entry.dirty })); }
  catch { if (entry.uid === DEMO_STUDENT_UID) publish(entry, { status: 'error' }); }
}
function readAccount(uid: string) {
  if (!accountReads.has(uid)) accountReads.set(uid, getDoc(doc(db, 'responses', uid))
    .then(snapshot => snapshot.exists() ? snapshot.data() : {})
    .catch(error => { accountReads.delete(uid); throw error; }));
  return accountReads.get(uid)!;
}
export function moduleResponseEntry(uid: string | null, moduleId: string): Entry {
  const identity = `${uid ?? 'guest'}:${moduleId}`;
  const existing = entries.get(identity);
  if (existing) return existing;
  const entry: Entry = { uid, moduleId, snapshot: { values: {}, loaded: !uid || uid === DEMO_STUDENT_UID, status: uid === DEMO_STUDENT_UID ? 'device' : uid ? 'loading' : 'device' }, listeners: new Set(), dirty: {}, edited: {} };
  if (uid) try {
    const recovery = JSON.parse(localStorage.getItem(responseStorageKey(uid, moduleId)) ?? 'null');
    if (recovery?.values && typeof recovery.values === 'object') entry.snapshot.values = recovery.values;
    if (recovery?.dirty && typeof recovery.dirty === 'object') entry.dirty = recovery.dirty;
  } catch { /* A corrupt device draft must never replace account data. */ }
  entries.set(identity, entry);
  return entry;
}
export function subscribeModuleResponses(entry: Entry, listener: () => void) {
  entry.listeners.add(listener);
  return () => { entry.listeners.delete(listener); };
}
export async function loadModuleResponses(entry: Entry, force = false): Promise<void> {
  if ((!force && entry.snapshot.loaded) || !entry.uid || entry.uid === DEMO_STUDENT_UID || entry.disposed) return;
  if (entry.load) return entry.load;
  const timeout = setTimeout(() => { if (!entry.snapshot.loaded) publish(entry, { loaded: true, status: 'error' }); }, 5000);
  entry.load = (async () => {
    try {
      const data = await readAccount(entry.uid!);
      const values = { ...(data[entry.moduleId] ?? {}), ...entry.dirty, ...entry.edited };
      publish(entry, { values, loaded: true, status: Object.keys(entry.dirty).length ? 'saving' : 'saved' });
      remember(entry);
      if (Object.keys(entry.dirty).length) void flushModuleResponses(entry);
    } catch { publish(entry, { loaded: true, status: 'error' }); }
    finally { clearTimeout(timeout); entry.load = undefined; }
  })();
  return entry.load;
}
export function changeModuleResponse(entry: Entry, key: string, value: any) {
  entry.dirty[key] = value;
  entry.edited[key] = value;
  publish(entry, { values: { ...entry.snapshot.values, [key]: value }, status: entry.uid && entry.uid !== DEMO_STUDENT_UID ? 'saving' : 'device' });
  remember(entry);
  if (entry.timer) clearTimeout(entry.timer);
  entry.timer = setTimeout(() => { void flushModuleResponses(entry); }, 700);
}
export async function flushModuleResponses(entry: Entry): Promise<void> {
  if (entry.disposed) return;
  if (entry.timer) { clearTimeout(entry.timer); entry.timer = undefined; }
  if (!entry.uid || entry.uid === DEMO_STUDENT_UID) return;
  if (entry.inFlight) { await entry.inFlight; if (entry.snapshot.status !== 'error' && Object.keys(entry.dirty).length) return flushModuleResponses(entry); return; }
  if (!Object.keys(entry.dirty).length) return;
  if (auth.currentUser?.uid !== entry.uid) { publish(entry, { status: 'error' }); return; }
  const patch = { ...entry.dirty };
  entry.dirty = {};
  publish(entry, { status: 'saving' });
  entry.inFlight = (async () => {
    try {
      // merge:true merges response leaves; a stale form cannot overwrite
      // another exercise's answers. Writes are serialised per form.
      await setDoc(doc(db, 'responses', entry.uid!), { [entry.moduleId]: patch }, { mergeFields: Object.keys(patch).map(key => new FieldPath(entry.moduleId, key)) });
      accountReads.delete(entry.uid!);
      publish(entry, { status: Object.keys(entry.dirty).length ? 'saving' : 'saved' });
    } catch {
      entry.dirty = { ...patch, ...entry.dirty };
      publish(entry, { status: 'error' });
    } finally { remember(entry); entry.inFlight = undefined; }
  })();
  await entry.inFlight;
  if (entry.snapshot.status !== 'error' && Object.keys(entry.dirty).length) await flushModuleResponses(entry);
}
export function forgetModuleResponseMemory() { entries.forEach(entry => { entry.disposed = true; if (entry.timer) clearTimeout(entry.timer); }); entries.clear(); accountReads.clear(); }
if (typeof window !== 'undefined') window.addEventListener('nextstepuni:session-cleared', forgetModuleResponseMemory);
