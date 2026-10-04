import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { ArrowUpRight, X } from 'lucide-react';
import { useReducedMotion } from '../Motion';
import { useModal } from '../../hooks/useModal';
import StudySnoozer from './StudySnoozer';
import StudySoundToggle from './StudySoundToggle';
import { animateStudyChange, studyControlOrigin } from './studyMotion';
import { formatStudyTime } from './StudySessionFinish';
import './study-crew.css';

export default function StudyBreak({ subject, elapsedSeconds, onResume, onLeave, sound }: {
  subject: string;
  elapsedSeconds: number;
  onResume: (event: React.MouseEvent<HTMLButtonElement>) => void;
  onLeave: () => void;
  sound?: { muted: boolean; play: (direction: 'pause' | 'return') => void };
}) {
  const [open, setOpen] = useState(false);
  const [moving, setMoving] = useState<'opening' | 'closing' | null>(null);
  const [inhale, setInhale] = useState(true);
  const rest = useRef<HTMLDivElement>(null), guide = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const restMascot = useRef<SVGSVGElement>(null), guideMascot = useRef<SVGSVGElement>(null);
  const core = useRef<HTMLDivElement>(null), character = useRef<HTMLDivElement>(null);
  const busy = useRef(false), origin = useRef({ x: 0, y: 0 });
  const wasOpen = useRef(false);
  const reduced = useReducedMotion();

  const close = () => {
    if (busy.current || !open) return;
    busy.current = true;
    sound?.play('return');
    setMoving('closing');
  };
  useModal(open, close, guide, { closeDisabled: Boolean(moving) });
  useEffect(() => {
    if (open) wasOpen.current = true;
    else if (wasOpen.current) {
      wasOpen.current = false;
      trigger.current?.focus({ preventScroll: true });
    }
  }, [open]);

  useLayoutEffect(() => {
    if (!moving || !rest.current || !guide.current) return;
    const returning = moving === 'closing';
    const from = returning ? guide.current : rest.current;
    const to = returning ? rest.current : guide.current;
    const fromMascot = returning ? guideMascot.current : restMascot.current;
    const toMascot = returning ? restMascot.current : guideMascot.current;
    if (!returning) guide.current.querySelector<HTMLButtonElement>('.study-breathe-return')?.focus({ preventScroll: true });
    return animateStudyChange({ from, to, origin: origin.current, reduced: Boolean(reduced), returning,
      mascot: fromMascot && toMascot ? { from: fromMascot, to: toMascot } : undefined,
      onFinish: () => { busy.current = false; setMoving(null); if (returning) setOpen(false); },
    });
  }, [moving, reduced]);

  useEffect(() => {
    if (!open || moving) return;
    setInhale(true);
    const epoch = performance.now();
    const animations: Animation[] = [];
    if (!reduced) {
      const cycle = (element: HTMLElement | null, start: string, peak: string) => {
        if (!element?.animate) return;
        element.style.transform = '';
        animations.push(element.animate([
          { offset: 0, transform: start, easing: 'cubic-bezier(.4,0,.2,1)' },
          { offset: .4, transform: peak, easing: 'cubic-bezier(.4,0,.2,1)' },
          { offset: 1, transform: start },
        ], { duration: 10000, iterations: Infinity }));
      };
      cycle(core.current, 'scale(.86)', 'scale(1.04)');
      cycle(character.current, 'translateY(4px)', 'translateY(-6px)');
    }
    const timer = window.setInterval(() => setInhale((performance.now() - epoch) % 10000 < 4000), 100);
    return () => {
      window.clearInterval(timer);
      // Preserve the current geometry while the guide fades away.
      [core.current, character.current].forEach(element => { if (element) element.style.transform = getComputedStyle(element).transform; });
      animations.forEach(animation => animation.cancel());
    };
  }, [open, moving, reduced]);

  return <section className="study-break-experience">
    <div ref={rest} className="study-break" inert={open} aria-hidden={open}>
      {sound && <div className="study-break-tools"><StudySoundToggle muted={sound.muted} /></div>}
      <p className="study-crew-eyebrow" data-study-arrive>A little room to breathe</p>
      <div className="study-break-art" data-study-arrive><StudySnoozer artworkRef={restMascot} /></div>
      <h1 id="study-break-title" data-study-arrive>Even stars take a moment.</h1>
      <p data-study-arrive>Look away. Stretch a little. Come back when you’re ready.</p>
      <div className="study-break-context" data-study-arrive><strong>{subject}</strong><span>{formatStudyTime(elapsedSeconds)} studied · Timer paused</span></div>
      <button type="button" className="crew-primary" data-study-arrive onClick={onResume}>Back to study<ArrowUpRight size={21} aria-hidden="true" /></button>
      <button ref={trigger} type="button" className="crew-link study-breathe-toggle" data-study-arrive aria-haspopup="dialog" aria-expanded={open} onClick={event => {
        if (busy.current) return;
        busy.current = true;
        origin.current = studyControlOrigin(event.currentTarget);
        sound?.play('pause'); setInhale(true); setOpen(true); setMoving('opening');
      }}>Take a few slow breaths</button>
      <p className="study-breath-prompt" data-study-arrive>Your place is right here.</p>
      <button type="button" className="crew-link study-break-leave" data-study-arrive onClick={onLeave}>Finish for now</button>
    </div>
    {open && <div ref={guide} className="study-breathe-guide" role="dialog" aria-modal="true" aria-labelledby="study-breathe-title" aria-describedby="study-breathe-detail" tabIndex={-1}>
      <header className="study-breathe-top">
        <p className="study-breathe-kicker">A little room to breathe</p>
        <div className="study-room-tools">{sound && <StudySoundToggle muted={sound.muted} />}<button type="button" className="study-breathe-close" aria-label="Close breathing guide" onClick={close} disabled={Boolean(moving)}><X size={17} aria-hidden="true" /></button></div>
      </header>
      <div className="study-breathe-content">
        <h2 id="study-breathe-title" data-study-arrive>Take a moment.</h2>
        <div className="study-breathe-circle" data-study-arrive>
          <div ref={core} className="study-breathe-core" aria-hidden="true" />
          <div ref={character} className="study-breathe-character"><StudySnoozer artworkRef={guideMascot} /></div>
        </div>
        <div className="study-breathe-guidance" key={inhale ? 'inhale' : 'exhale'} data-study-arrive>
          <p className="study-breathe-phase">{inhale ? 'Breathe in' : 'Breathe out'}<span aria-hidden="true">.</span></p>
          <p id="study-breathe-detail">{inhale ? 'Slowly. There’s no rush.' : 'Let your shoulders soften.'}</p>
        </div>
      </div>
      <footer className="study-breathe-footer" data-study-arrive>
        <button type="button" className="crew-primary study-breathe-return" onClick={close} disabled={Boolean(moving)}>Back to your break<ArrowUpRight size={19} aria-hidden="true" /></button>
        <p>Your place is right here.</p>
      </footer>
    </div>}
  </section>;
}
