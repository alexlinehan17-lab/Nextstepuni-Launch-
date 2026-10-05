import { useCallback, useMemo, useSyncExternalStore, type SetStateAction } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Snapshot { value: unknown; retain: boolean; error: boolean }
const drafts = new Map<string, { snapshot: Snapshot; listeners: Set<() => void> }>();
if (typeof window !== 'undefined') window.addEventListener('nextstepuni:session-cleared', () => { drafts.clear(); });
export function usePrivateDeviceDraft<T>(name: string, initial: T) {
  const { user } = useAuth();
  const key = `nextstepuni:private-draft:${user?.uid ?? 'guest'}:${name}`;
  const entry = useMemo(() => {
    const existing = drafts.get(key); if (existing) return existing;
    let snapshot: Snapshot = { value: initial, retain: false, error: false };
    try { const saved = JSON.parse(localStorage.getItem(key) ?? 'null'); if (saved?.retain) snapshot = { value: saved.value, retain: true, error: false }; } catch { /* Session-only remains usable. */ }
    const created = { snapshot, listeners: new Set<() => void>() }; drafts.set(key, created); return created;
  }, [key]);
  const subscribe = useCallback((listener: () => void) => { entry.listeners.add(listener); return () => { entry.listeners.delete(listener); }; }, [entry]);
  const snapshot = useSyncExternalStore(subscribe, () => entry.snapshot);
  const publish = useCallback((value: unknown, retain: boolean) => {
    let error = false;
    try { if (retain) localStorage.setItem(key, JSON.stringify({ value, retain })); else localStorage.removeItem(key); } catch { error = true; }
    entry.snapshot = { value, retain, error }; entry.listeners.forEach(listener => listener());
  }, [entry, key]);
  const update = useCallback((next: SetStateAction<T>) => publish(typeof next === 'function' ? (next as (previous: T) => T)(entry.snapshot.value as T) : next, entry.snapshot.retain), [entry, publish]);
  return { value: snapshot.value as T, update, retain: snapshot.retain, setRetain: (retain: boolean) => publish(entry.snapshot.value, retain), clear: () => publish(initial, false), error: snapshot.error };
}
