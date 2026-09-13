import { useState } from 'react';
export type StudyTimerAppearance = 'ink' | 'layers';
const readAppearance = (key: string): StudyTimerAppearance => {
  try { return localStorage.getItem(key) === 'layers' ? 'layers' : 'ink'; } catch { return 'ink'; }
};
/** A device preference scoped to the student; session recording is unchanged. */
export function useStudyTimerAppearance(uid: string) {
  const key = `nsu-study-timer:${uid}`;
  const [saved, setSaved] = useState(() => ({ key, appearance: readAppearance(key) }));
  const appearance = saved.key === key ? saved.appearance : readAppearance(key);
  const setAppearance = (next: StudyTimerAppearance) => {
    setSaved({ key, appearance: next });
    try { localStorage.setItem(key, next); } catch { /* Still usable when storage is unavailable. */ }
  };
  return [appearance, setAppearance] as const;
}
