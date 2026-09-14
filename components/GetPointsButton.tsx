import React, { useEffect, useRef, useState } from 'react';
import { Coins, LoaderCircle } from 'lucide-react';
import { useOptionalProgress } from '../contexts/ProgressContext';
import { useToast } from './Toast';
import { creditDrawerPoints, DRAWER_POINTS_CREDIT } from '../services/progressRepository';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { awaitWriteOrTimeout } from '../utils/firestoreWrite';

export default function GetPointsButton({ uid, expanded }: { uid?: string; expanded: boolean }) {
  const progress = useOptionalProgress();
  const { showToast } = useToast();
  const [saving, setSaving] = useState(false);
  const inFlight = useRef(false);
  const currentUid = useRef(uid);
  useEffect(() => {
    currentUid.current = uid;
    return () => { currentUid.current = undefined; };
  }, [uid]);

  // The balance and the authenticated account must belong to the same user.
  if (!uid || !progress?.progressLoaded || progress.progressDataUid !== uid) return null;

  const addPoints = async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setSaving(true);
    const refresh = () => { if (currentUid.current === uid) progress.reloadProgress(); };
    const reportFailure = () => {
      if (currentUid.current !== uid) return;
      refresh();
      showToast('Could not add JP. Please try again.', 'error');
    };
    try {
      if (uid === DEMO_STUDENT_UID) {
        progress.updateDemoProgress(current => ({
          ...current,
          pointsData: {
            ...current.pointsData,
            totalEarned: (current.pointsData?.totalEarned ?? 0) + DRAWER_POINTS_CREDIT,
          },
        }));
        showToast('100 JP added to your bank.', 'success');
        return;
      }

      const write = creditDrawerPoints(uid);
      const outcome = await awaitWriteOrTimeout(write, 'GetPointsButton.credit');
      if (currentUid.current !== uid) return;
      if (outcome === 'failed') { reportFailure(); return; }
      refresh();
      if (outcome === 'pending') {
        showToast('100 JP queued. They’ll sync when you’re online.', 'info');
        // A queued write can still be rejected when the connection returns.
        void write.then(refresh, reportFailure);
      } else {
        showToast('100 JP added to your bank.', 'success');
      }
    } catch {
      reportFailure();
    } finally {
      inFlight.current = false;
      if (currentUid.current) setSaving(false);
    }
  };

  const Icon = saving ? LoaderCircle : Coins;
  return (
    <button
      type="button"
      onClick={() => { void addPoints(); }}
      disabled={saving}
      aria-label="GET POINTS"
      aria-busy={saving}
      title="Add 100 JP to your bank"
      className="relative flex items-center gap-3 px-2.5 py-2.5 rounded-xl text-left hover:bg-[#F3EEE7] dark:hover:bg-zinc-800 transition-colors disabled:opacity-50 disabled:cursor-wait"
    >
      <span className="shrink-0 flex items-center justify-center w-[18px]">
        <Icon size={18} strokeWidth={1.6} aria-hidden="true" className={`text-[#C35319] dark:text-orange-400 ${saving ? 'animate-spin motion-reduce:animate-none' : ''}`} />
      </span>
      <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${expanded ? 'opacity-100' : 'opacity-0'}`}>
        GET POINTS
      </span>
    </button>
  );
}
