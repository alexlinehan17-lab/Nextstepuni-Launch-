/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Asked in the study room, never on launch: the first time a student runs a
 * timed session, offer one notification for when the time is up. Their answer
 * is kept (settings), so the room asks once; the switch in Your setup and
 * Settings changes it later.
 */

import React, { useEffect, useState } from 'react';
import { Bell, Check } from 'lucide-react';
import { useSharedStudySession } from '../../contexts/StudySessionContext';
import { useStudyNotifications } from '../../hooks/useStudyNotifications';

const CONFIRMATION_MS = 6000;

const clockTime = (at: number) => new Date(at).toLocaleTimeString('en-IE', { hour: 'numeric', minute: '2-digit' });

export default function StudyNotifyOffer() {
  const session = useSharedStudySession();
  const notify = useStudyNotifications();
  const [answer, setAnswer] = useState<'asking' | 'on' | 'blocked' | 'done'>('asking');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (answer !== 'on') return;
    const timer = window.setTimeout(() => setAnswer('done'), CONFIRMATION_MS);
    return () => window.clearTimeout(timer);
  }, [answer]);

  if (!session || session.openEnded || answer === 'done') return null;
  if (session.phase !== 'active' && session.phase !== 'paused') return null;
  if (answer === 'asking' && !notify.shouldOffer) return null;

  if (answer === 'on') {
    return (
      <p className="ss-notify-status" role="status">
        <Check size={15} aria-hidden="true" />
        {session.endsAt ? `We’ll let you know at ${clockTime(session.endsAt)}.` : 'We’ll let you know when your time is up.'}
      </p>
    );
  }

  if (answer === 'blocked') {
    return (
      <div className="ss-notify" role="status">
        <p>{notify.hint}</p>
        <div className="ss-notify-actions">
          <button type="button" className="ss-notify-yes" onClick={() => setAnswer('done')}>OK</button>
        </div>
      </div>
    );
  }

  const enable = async () => {
    if (busy) return;
    setBusy(true);
    try {
      setAnswer(await notify.turnOn() === 'granted' ? 'on' : 'blocked');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="ss-notify" role="group" aria-labelledby="ss-notify-question">
      <p id="ss-notify-question">Switching to your notes or another app? We can tell you when your {session.plannedMinutes + session.extendedMinutes} minutes are up.</p>
      <div className="ss-notify-actions">
        <button type="button" className="ss-notify-yes" onClick={enable} disabled={busy}>
          <Bell size={16} aria-hidden="true" />Notify me when time’s up
        </button>
        <button type="button" className="ss-notify-no" onClick={() => { notify.turnOff(); setAnswer('done'); }}>Not now</button>
      </div>
    </div>
  );
}
