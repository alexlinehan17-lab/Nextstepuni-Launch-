import React, { useRef, useState } from 'react';
import { useReducedMotion } from 'framer-motion';
import './welcome-character.css';

/** A small, bounded interaction: drag the character, then let it settle home. */
export function WelcomeCharacter() {
  const reducedMotion = useReducedMotion();
  const stage = useRef<HTMLDivElement>(null);
  const drag = useRef<{ id: number; x: number; y: number } | null>(null);
  const didDrag = useRef(false);
  const [hop, setHop] = useState(0);

  const resetPosition = () => {
    drag.current = null;
    stage.current?.classList.remove('welcome-character-dragging');
    stage.current?.style.setProperty('--character-x', '0px');
    stage.current?.style.setProperty('--character-y', '0px');
    stage.current?.style.setProperty('--character-turn', '0deg');
  };

  const release = (event: React.PointerEvent<HTMLButtonElement>) => {
    if (drag.current?.id !== event.pointerId) return;
    resetPosition();
    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId);
    }
  };

  return (
    <div ref={stage} className="welcome-character-stage">
      <div className="welcome-character-papers" aria-hidden="true"><i /><i /><i /></div>
      <div className="welcome-character-position">
        <div className={hop && !reducedMotion ? 'welcome-character-hop' : undefined} onAnimationEnd={() => setHop(0)}>
          <button
            type="button"
            className="welcome-character"
            aria-label="Play with the star character"
            onPointerDown={event => {
              if (reducedMotion || !event.isPrimary || event.button !== 0 || drag.current) return;
              didDrag.current = false;
              drag.current = { id: event.pointerId, x: event.clientX, y: event.clientY };
              event.currentTarget.setPointerCapture(event.pointerId);
              stage.current?.classList.add('welcome-character-dragging');
            }}
            onPointerMove={event => {
              const origin = drag.current;
              if (!origin || origin.id !== event.pointerId) return;
              if (reducedMotion) { resetPosition(); return; }
              const maxX = Math.min(65, event.currentTarget.clientWidth * .22);
              const x = Math.max(-maxX, Math.min(maxX, (event.clientX - origin.x) * .7));
              const y = Math.max(-60, Math.min(45, (event.clientY - origin.y) * .7));
              if (Math.abs(x) + Math.abs(y) > 5) didDrag.current = true;
              stage.current?.style.setProperty('--character-x', `${x}px`);
              stage.current?.style.setProperty('--character-y', `${y}px`);
              stage.current?.style.setProperty('--character-turn', `${x / 9}deg`);
            }}
            onPointerUp={release}
            onPointerCancel={release}
            onLostPointerCapture={resetPosition}
            onClick={event => {
              // A drag ends with a click too; only taps and keyboard activation hop.
              if (!reducedMotion && (!didDrag.current || event.detail === 0)) setHop(value => value + 1);
              didDrag.current = false;
            }}
          >
            <img src="/icons/onboarding/star-person.png" alt="" draggable={false} width={300} height={300} />
          </button>
        </div>
      </div>
    </div>
  );
}
