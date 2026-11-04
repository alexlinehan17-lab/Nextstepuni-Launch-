/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Year islands: the classmates in a student's own school AND year group, read
 * from the /islandPublic projection (functions/src/islandProjection.ts), plus
 * the student's own "Show my island to my year" choice.
 *
 * Nothing is fetched until the Your year panel first opens, so opening Journey
 * costs no classmate reads. The query filters on BOTH school and yearGroup with
 * the values from the student's own users doc, read fresh here: those are the
 * exact values firestore.rules compares, and a query that does not match them
 * is denied as a whole.
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import { collection, doc, getDoc, getDocs, limit, query, setDoc, where } from 'firebase/firestore';
import { db } from '../firebase';
import { useOptionalProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { logError } from '../utils/logError';
import { awaitWriteOrTimeout, saveInBackground } from '../utils/firestoreWrite';
import {
  ISLAND_VISIBILITY_FIELD,
  isPeerYearGroup,
  type IslandVisibility,
  type PeerYearGroup,
} from '../functions/src/islandProjection';
import { byName, parseYearIsland, type YearIsland } from '../components/journey/year/yearIslands';

/** Well above any real year group; bounds the read if something goes wrong. */
const MAX_CLASSMATES = 300;

export type YearIslandsStatus = 'idle' | 'loading' | 'ready' | 'no-school' | 'no-year' | 'graduated' | 'error';
export interface YearCohort { school: string; yearGroup: PeerYearGroup }

export function useYearIslands(uid: string, { enabled }: { enabled: boolean }) {
  const progress = useOptionalProgress();
  const profileYear = useRef<unknown>(undefined);
  profileYear.current = (progress?.rawProgressDoc?.subjectProfile as { yearGroup?: unknown } | undefined)?.yearGroup;
  const [status, setStatus] = useState<YearIslandsStatus>('idle');
  const [classmates, setClassmates] = useState<YearIsland[]>([]);
  const [cohort, setCohort] = useState<YearCohort | null>(null);
  const [visibility, setVisibilityState] = useState<IslandVisibility>('year');
  // The switch stays disabled until the student's real choice has been read.
  const [visibilityKnown, setVisibilityKnown] = useState(false);
  const [visibilityError, setVisibilityError] = useState('');
  const [sample, setSample] = useState(false);
  const [loadKey, setLoadKey] = useState(0);
  const loaded = useRef<number | null>(null);

  useEffect(() => {
    if (!enabled || loaded.current === loadKey) return;
    loaded.current = loadKey;
    let active = true, settled = false;
    setStatus('loading');
    (async () => {
      if (uid === DEMO_STUDENT_UID) {
        const { sampleYearIslands, SAMPLE_COHORT } = await import('../data/sampleYearIslands');
        // Review states for the dev harness: ?classmates=none | slow | error.
        const review = new URLSearchParams(window.location.search).get('classmates');
        if (review === 'slow') await new Promise(resolve => setTimeout(resolve, 120_000));
        if (review === 'error') throw new Error('Sample year islands: review error state');
        if (!active) return;
        setSample(true);
        setVisibilityKnown(true);
        setCohort(SAMPLE_COHORT);
        setClassmates(review === 'none' ? [] : sampleYearIslands().sort(byName));
        setStatus('ready');
        return;
      }
      const self = (await getDoc(doc(db, 'users', uid))).data() ?? {};
      if (!active) return;
      setVisibilityState(self[ISLAND_VISIBILITY_FIELD] === 'hidden' ? 'hidden' : 'year');
      setVisibilityKnown(true);
      const school = typeof self.school === 'string' ? self.school : '';
      if (!school) { setStatus('no-school'); return; }
      let yearGroup: unknown = self.yearGroup;
      if (yearGroup === 'graduated') { setStatus('graduated'); return; }
      // Older accounts recorded their year only in onboarding's subject
      // profile. Copy it to the users doc, where the rules (and the staff
      // dashboard) read it, rather than send the student off to set it again.
      if (!yearGroup && isPeerYearGroup(profileYear.current)) {
        yearGroup = profileYear.current;
        // The rules check the query against the SERVER copy, so wait (briefly:
        // a write never settles offline) for the copy to land before querying.
        const saved = await awaitWriteOrTimeout(setDoc(doc(db, 'users', uid), { yearGroup }, { merge: true }), 'useYearIslands.yearGroup');
        if (!active) return;
        if (saved === 'failed') { setStatus('no-year'); return; }
      }
      if (!isPeerYearGroup(yearGroup)) { setStatus('no-year'); return; }
      setCohort({ school, yearGroup });
      const snapshot = await getDocs(query(
        collection(db, 'islandPublic'),
        where('school', '==', school),
        where('yearGroup', '==', yearGroup),
        limit(MAX_CLASSMATES),
      ));
      if (!active) return;
      setClassmates(snapshot.docs
        .filter(snap => snap.id !== uid)
        .map(snap => parseYearIsland(snap.id, snap.data()))
        .filter((island): island is YearIsland => island !== null)
        .sort(byName));
      setStatus('ready');
    })()
      .catch(err => {
        logError('useYearIslands.load', err);
        if (active) setStatus('error');
      })
      .finally(() => { settled = true; });
    return () => {
      active = false;
      // Closed mid-load: load again next time rather than stay "loading".
      if (!settled) loaded.current = null;
    };
  }, [enabled, loadKey, uid]);

  const reload = useCallback(() => setLoadKey(key => key + 1), []);

  /**
   * Optimistic, like every write in this app: the switch moves at once, the
   * write flushes whenever the connection allows, and only a real rejection
   * puts the switch back (utils/firestoreWrite.ts explains why never to await).
   */
  const setVisibility = useCallback((next: IslandVisibility) => {
    setVisibilityState(next);
    setVisibilityError('');
    if (uid === DEMO_STUDENT_UID) return;
    const previous: IslandVisibility = next === 'year' ? 'hidden' : 'year';
    saveInBackground(
      setDoc(doc(db, 'users', uid), { [ISLAND_VISIBILITY_FIELD]: next }, { merge: true }),
      'useYearIslands.visibility',
      () => {
        setVisibilityState(current => (current === next ? previous : current));
        setVisibilityError('That change did not save. Check your connection and try again.');
      },
      { silent: true },
    );
  }, [uid]);

  return { status, classmates, cohort, visibility, visibilityKnown, setVisibility, visibilityError, sample, reload };
}
