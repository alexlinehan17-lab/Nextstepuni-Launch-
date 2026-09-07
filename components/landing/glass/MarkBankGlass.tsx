/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Mark Bank board (components/MarkBank/MarkBank), signed out: the
 * topic board for a subject, and "Start a practice session" opens the actual
 * review session over the page. Grades stay in this browser's localStorage;
 * nothing is written anywhere else without an account.
 */

import React, { useMemo } from 'react';
import MarkBank from '../../MarkBank/MarkBank';
import { GlassStage } from './GlassStage';

export const MARKBANK_SUBJECTS_LIVE: { id: string; label: string }[] = [
  { id: 'Biology', label: 'Biology' },
  { id: 'Chemistry', label: 'Chemistry' },
  { id: 'Physics', label: 'Physics' },
  { id: 'Business', label: 'Business' },
  { id: 'Geography', label: 'Geography' },
  { id: 'Mathematics', label: 'Maths' },
];

const MarkBankGlass: React.FC<{ sub: string; active: boolean }> = ({ sub, active }) => {
  // The board remembers the last subject in localStorage; the mode tabs must win.
  const subjects = useMemo(() => {
    try { window.localStorage.removeItem('mb:choice:anon'); } catch { /* private mode */ }
    return [{ subjectName: sub, level: 'higher' }];
  }, [sub]);
  return (
    <GlassStage active={active} height={700}>
      {active && (
        <div className="landing-glass-pad">
          <MarkBank key={sub} uid={undefined} studentSubjects={subjects} />
        </div>
      )}
    </GlassStage>
  );
};

export default MarkBankGlass;
