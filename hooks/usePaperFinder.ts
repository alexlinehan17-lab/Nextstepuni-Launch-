/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail persistence — recents (with per-side last page), last level and
 * language filters. Owns the `paperTrail` namespace on progress/{uid} with
 * additive merge writes; seeds once per uid from useFreshProgress so saves
 * survive tool re-entry (the getDoc-on-mount staleness fix).
 *
 * Design notes from adversarial review:
 *  - Recents identity is the composite key (subject|year|level|lang|fileid) —
 *    SEC fileids repeat across years and collide between papers and schemes.
 *  - Page-position updates mutate a ref and debounce the Firestore write
 *    WITHOUT re-rendering: a render per page-turn would cascade into the
 *    open Viewer and steal focus/scroll.
 *  - The unmount flush only fires when a debounced write is actually pending
 *    AND the state was seeded — otherwise backing out before the seed read
 *    resolves would wipe saved recents with the EMPTY state.
 *  - Firestore rejects explicit `undefined` values (ignoreUndefinedProperties
 *    is not set app-wide), so persisted objects are stripped first.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { reportSaveError } from '../utils/logError';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import {
  type PaperLang,
  type PaperLevel,
  type PaperTrailState,
  type RecentPaper,
} from '../types/paperTrail';

const EMPTY: PaperTrailState = { recents: [] };
const MAX_RECENTS = 8;
const PAGE_WRITE_DEBOUNCE_MS = 1500;

/** Deep-strip `undefined` values (Firestore rejects them). */
const stripUndefined = <T,>(v: T): T => JSON.parse(JSON.stringify(v)) as T;

export function usePaperFinder(uid?: string) {
  const { updateDemoProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const [state, setState] = useState<PaperTrailState>(EMPTY);
  const { doc: progressDoc, loaded } = useFreshProgress(uid);
  const seededRef = useRef<string | null>(null);
  const stateRef = useRef(state);
  const pageTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Reset on account switch so the previous user's recents never bleed over.
  useEffect(() => {
    if (seededRef.current !== null && seededRef.current !== (uid ?? '')) {
      seededRef.current = null;
      stateRef.current = EMPTY;
      setState(EMPTY);
    }
  }, [uid]);

  useEffect(() => {
    if (!loaded || seededRef.current === (uid ?? '')) return;
    seededRef.current = uid ?? '';
    const saved = progressDoc?.paperTrail as Partial<PaperTrailState> | undefined;
    if (saved && Array.isArray(saved.recents)) {
      // Drop pre-composite-key entries from any earlier schema.
      const recents = saved.recents.filter(r => typeof (r as RecentPaper).key === 'string');
      stateRef.current = { ...EMPTY, ...saved, recents };
      setState(stateRef.current);
    }
  }, [loaded, progressDoc, uid]);

  const write = useCallback(
    (next: PaperTrailState) => {
      if (!uid) return;
      if (isDemo) {
        updateDemoProgress(current => ({ ...current, paperTrail: stripUndefined(next) }));
        return;
      }
      setDoc(doc(db, 'progress', uid), { paperTrail: stripUndefined(next) }, { merge: true }).catch(
        e => reportSaveError('PaperTrail.persist', e),
      );
    },
    [uid, isDemo, updateDemoProgress],
  );

  const persist = useCallback(
    (next: PaperTrailState) => {
      stateRef.current = next;
      setState(next);
      write(next);
    },
    [write],
  );

  /** Record (or refresh) a recent; merges page positions of an existing entry
   *  so re-opening a paper never resets the saved reading position. */
  const recordRecent = useCallback(
    (r: Omit<RecentPaper, 'at' | 'paperPage' | 'schemePage'> & { page?: number }) => {
      const cur = stateRef.current;
      const existing = cur.recents.find(x => x.key === r.key);
      const { page: _page, ...rest } = r;
      const entry: RecentPaper = {
        ...rest,
        paperPage: existing?.paperPage ?? (r.kind === 'paper' ? (r.page ?? 1) : 1),
        schemePage: existing?.schemePage ?? (r.kind === 'scheme' ? (r.page ?? 1) : 1),
        at: Date.now(),
      };
      const others = cur.recents.filter(x => x.key !== r.key);
      persist({ ...cur, recents: [entry, ...others].slice(0, MAX_RECENTS) });
    },
    [persist],
  );

  /** Debounced, render-free page-position update for a recents entry. */
  const updatePage = useCallback(
    (key: string, page: number, side: 'paper' | 'scheme') => {
      const cur = stateRef.current;
      const next: PaperTrailState = {
        ...cur,
        recents: cur.recents.map(x =>
          x.key === key
            ? { ...x, kind: side, ...(side === 'paper' ? { paperPage: page } : { schemePage: page }) }
            : x,
        ),
      };
      // Mutate the ref only — no setState, no re-render of the open Viewer.
      stateRef.current = next;
      if (!uid) return;
      if (pageTimer.current) clearTimeout(pageTimer.current);
      pageTimer.current = setTimeout(() => {
        pageTimer.current = null;
        write(stateRef.current);
      }, PAGE_WRITE_DEBOUNCE_MS);
    },
    [uid, write],
  );

  // Flush a pending debounced write on unmount — only if seeded and dirty.
  useEffect(
    () => () => {
      if (pageTimer.current) {
        clearTimeout(pageTimer.current);
        pageTimer.current = null;
        if (seededRef.current === (uid ?? '')) write(stateRef.current);
      }
    },
    [uid, write],
  );

  const setFilters = useCallback(
    (patch: { lastLevel?: PaperLevel; lastLang?: PaperLang }) => {
      persist({ ...stateRef.current, ...patch });
    },
    [persist],
  );

  // Publish the latest per-side positions only when leaving the reader. Page
  // turns themselves remain render-free, but Continue sees the position just read.
  const finishReading = useCallback(() => setState(stateRef.current), []);

  return { state, isLoaded: loaded, recordRecent, updatePage, setFilters, finishReading };
}
