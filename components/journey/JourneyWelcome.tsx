import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { ArrowUpRight, X } from 'lucide-react';
import { useModal } from '../../hooks/useModal';
import CrewIllustration from '../CrewIllustration';
import './journey-welcome.css';

/** Mounted only after this student's saved progress has loaded. */
export default function JourneyWelcome({ hasSeenWelcome, onDismissWelcome }: {
  hasSeenWelcome: boolean;
  onDismissWelcome: () => void;
}) {
  const [open, setOpen] = useState(!hasSeenWelcome);
  const dialogRef = useRef<HTMLDivElement>(null);
  const reduceMotion = useReducedMotion();
  const close = () => {
    setOpen(false);
    if (!hasSeenWelcome) onDismissWelcome();
  };
  useModal(open, close, dialogRef);
  useEffect(() => {
    if (!open) return;
    const overflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = overflow; };
  }, [open]);

  return <>
    <button type="button" className="journey-welcome-help" onClick={() => setOpen(true)} aria-label="How Journey works">
      <span aria-hidden="true">?</span><span>How it works</span>
    </button>
    {createPortal(<AnimatePresence>
      {open && <motion.div
        className="journey-welcome-overlay" data-lenis-prevent
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        transition={{ duration: reduceMotion ? 0 : 0.18 }}
        onClick={event => { if (event.target === event.currentTarget) close(); }}
      >
        <motion.div
          ref={dialogRef} role="dialog" aria-modal="true" tabIndex={-1}
          aria-labelledby="journey-welcome-title" aria-describedby="journey-welcome-description"
          className="journey-welcome"
          initial={{ opacity: 0, y: reduceMotion ? 0 : 18, scale: reduceMotion ? 1 : 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: reduceMotion ? 0 : 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <header className="journey-welcome-header">
            <span className="journey-welcome-brand">nextstepuni</span>
            <button type="button" aria-label="Close Journey introduction" onClick={close}><X size={20} /></button>
          </header>
          <div className="journey-welcome-body">
            <div className="journey-welcome-story">
              <p className="journey-welcome-eyebrow">Welcome to Journey Mode</p>
              <h2 id="journey-welcome-title">Your effort.<br />A world of<br />your own.</h2>
              <p id="journey-welcome-description">A little island that grows with the work you put in. A place to make your progress visible, one small step at a time.</p>
              <div className="journey-welcome-art" aria-hidden="true">
                <CrewIllustration character="star-crew:stargazer" />
                <span>Small steps.<br />New horizons.</span>
              </div>
            </div>
            <div className="journey-welcome-guide">
              <p className="journey-welcome-eyebrow">Here’s how it works</p>
              <ol>
                <li><span className="journey-welcome-number">01</span><div><h3>Study. Earn. Grow.</h3><p>Complete study sessions and lessons to earn Journey Points (JP). Your balance is at the top of your island.</p></div></li>
                <li><span className="journey-welcome-number">02</span><div><h3>Build a place that’s yours.</h3><p>Open <strong>Build your island</strong>, choose a tile and tap an open corner. Preview it, then confirm to use your points.</p></div></li>
                <li><span className="journey-welcome-number">03</span><div><h3>See what’s out there.</h3><p>Growing your island reveals hidden stories and mythic stickers. Collect your discoveries in your <strong>Fieldbook</strong>.</p></div></li>
              </ol>
              <p className="journey-welcome-note">No rush. No upkeep.<br />Your island will be here when you come back.</p>
              <button type="button" className="journey-welcome-start" onClick={close}>Explore my island <ArrowUpRight size={22} aria-hidden="true" /></button>
              <p className="journey-welcome-reminder">Revisit this guide any time with “How it works”.</p>
            </div>
          </div>
        </motion.div>
      </motion.div>}
    </AnimatePresence>, document.body)}
  </>;
}
