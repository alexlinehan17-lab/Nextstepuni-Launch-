import React from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { PERSONAL_STAR_CREW, DEFAULT_PERSONAL_STAR_CREW_ID, getPersonalStarCrew } from '../data/personalStarCrew';
import StarCrewArtwork from './StarCrewArtwork';
import { RadioGroup, RadioGroupItem } from './account-ui-runtime';
import './account-ui-runtime.css';
import './account-controls.css';

export default function AccountCrewPicker({ value, onChange, disabled = false }: {
  value: string; onChange: (avatar: string) => void; disabled?: boolean;
}) {
  const reduced = useReducedMotion();
  const selected = getPersonalStarCrew(value) ?? getPersonalStarCrew(DEFAULT_PERSONAL_STAR_CREW_ID)!;
  return <div className="account-crew-choice">
    <div className="account-crew-feature" aria-live="polite" aria-atomic="true">
      <AnimatePresence mode="wait" initial={false}><motion.div key={selected.id}
        initial={{ opacity: 0, y: reduced ? 0 : 10, scale: reduced ? 1 : .95 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: reduced ? 0 : -8 }} transition={{ duration: reduced ? 0 : .22 }}>
        <StarCrewArtwork artwork={selected} className="account-crew-illustration" loading="eager" fallback={null} />
      </motion.div></AnimatePresence>
      <span><strong>{selected.name}</strong><small>You can change this any time.</small></span>
    </div>
    <div className="nsu-kobra account-crew-controls"><RadioGroup value={selected.id} onValueChange={onChange} disabled={disabled} aria-label="Choose your Star Crew character" className="account-crew-grid">
      {PERSONAL_STAR_CREW.map(crew => <label key={crew.id} data-selected={selected.id === crew.id} data-account-sound="save">
        <StarCrewArtwork artwork={crew} className="account-crew-illustration" loading="eager" fallback={null} />
        <span>{crew.name.replace(/^The /, '')}</span><RadioGroupItem value={crew.id} />
      </label>)}
    </RadioGroup></div>
  </div>;
}
