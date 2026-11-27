import React, { useRef, useState } from 'react';
import type { CardFigure } from '../../types/markBank';
import { figureUrl } from '../../utils/figureUrl';
import { Button } from '../ui/Button';

/** Preserve the SEC's typeset equations, diagrams and working at their natural
 * proportions. Tall solutions must never shrink to a fixed-height thumbnail. */
const MathematicsWorkedSolution: React.FC<{ figure: CardFigure }> = ({ figure }) => {
  const dialog = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const [zoomed, setZoomed] = useState(false);
  const src = figureUrl(figure.src);
  const close = () => dialog.current?.close();
  return (
    <div className="mb-maths-worked">
      <h3>Worked solution</h3>
      <p>Follow the working, then compare your answer with the credit notes.</p>
      <Button ref={trigger} size="sm" className="mb-maths-expand" onClick={() => {
        setZoomed(false);
        dialog.current?.showModal();
      }}>Enlarge worked solution</Button>
      {figure.sourceNote && <p className="mb-maths-source-note">{figure.sourceNote}</p>}
      <figure>
        <img src={src} alt={figure.alt} />
        <figcaption>{figure.attribution}</figcaption>
      </figure>
      <dialog ref={dialog} className="mb-maths-solution-dialog frame-dialog-native" aria-label="Worked solution and credit notes"
        onClose={() => trigger.current?.focus()}>
        <div className="mb-maths-solution-toolbar">
          <strong>Worked solution</strong>
          <Button size="sm" aria-pressed={zoomed} onClick={() => setZoomed(!zoomed)}>
            {zoomed ? 'Fit to screen' : 'Zoom in'}
          </Button>
          <Button size="sm" onClick={close}>Close solution</Button>
          {zoomed && <small>Scroll across and down to follow the working.</small>}
        </div>
        <div className="mb-maths-solution-scroll" tabIndex={0} aria-label="Solution image; scroll to read all working">
          {figure.sourceNote && <p className="mb-maths-source-note">{figure.sourceNote}</p>}
          <img src={src} alt={figure.alt} className={zoomed ? 'is-zoomed' : ''} />
        </div>
      </dialog>
    </div>
  );
};

export default MathematicsWorkedSolution;
