/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Mark Bank board (components/MarkBank), signed out. Biology,
 * Economics and Mathematics are open; the other twelve subjects show with a
 * lock. No uid means the board keeps its choices in localStorage and never
 * touches Firestore.
 */

import React, { useEffect } from 'react';
import MarkBank from '../../MarkBank/MarkBank';
import { GlassStage, type GlassLocks, type GlassProps } from './GlassStage';
import { FREE_SUBJECTS, LOCKED_SUBJECTS } from './demoProfile';

export const MARKBANK_SUBJECTS_LIVE: { id: string; label: string }[] = FREE_SUBJECTS.map(s => ({ id: s, label: s }));

const LOCKS: GlassLocks = { names: LOCKED_SUBJECTS };

const MarkBankGlass: React.FC<GlassProps> = ({ sub, active, height = 700, logicalWidth }) => {
  // The board remembers its last subject per device; the mode tabs should win.
  useEffect(() => { try { localStorage.removeItem('mb:choice:anon'); } catch { /* storage may be unavailable */ } }, [sub]);
  return (
    <GlassStage active={active} height={height} logicalWidth={logicalWidth} locks={LOCKS}>
      {active && (
        <div className="landing-glass-pad">
          <MarkBank key={sub} uid={undefined} studentSubjects={[{ subjectName: sub, level: 'higher' }]} />
        </div>
      )}
    </GlassStage>
  );
};

export default MarkBankGlass;
