import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { useLoadingCrew } from '../contexts/LoadingCrewContext';
import { getPersonalStarCrew } from '../data/personalStarCrew';
import { resolveLoadingCrew } from '../utils/loadingCrew';
import StarCrewArtwork from './StarCrewArtwork';
import './crew-loading.css';

interface LoadingSpinnerProps {
  label?: string;
  overlay?: boolean;
  variant?: 'full' | 'compact' | 'quiet';
  selection?: 'personal' | 'random';
  placement?: 'viewport' | 'panel';
  calm?: boolean;
}

/** Real waits only: no timer, fabricated progress, audio loop or forced duration. */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  label = 'Opening your space', overlay = false, variant = 'full',
  selection = 'personal', placement = 'viewport', calm = false,
}) => {
  const crewContext = useLoadingCrew();
  const [localDraw] = useState(Math.random);
  const crew = resolveLoadingCrew(selection, crewContext?.avatar, crewContext?.draw ?? localDraw);
  const spare = getPersonalStarCrew(crew.id === 'star-crew:skater' ? 'star-crew:maker' : 'star-crew:skater')!;
  const loadingSurface = (
    <div role="status" aria-live="polite" aria-atomic="true"
      data-loader-placement={placement} data-loading-crew={crew.id}
      className={[
        'theme-compat crew-loading',
        placement === 'viewport'
          ? `fixed inset-0 flex min-h-[100dvh] w-full items-center justify-center bg-[var(--surface-canvas)] px-6 text-center ${overlay ? 'z-[200]' : 'z-[80]'}`
          : 'crew-loading-panel',
      ].join(' ')}>
      <div className={`crew-loading-content crew-loading-${variant}${calm ? ' crew-loading-calm' : ''}`}>
        <div className="crew-loading-figure" aria-hidden="true">
          <StarCrewArtwork artwork={crew} className="crew-loading-art" loading="eager"
            fallback={<StarCrewArtwork artwork={spare} className="crew-loading-art" loading="eager" fallback={null} />} />
          <i className="crew-loading-shadow" />
        </div>
        <div className="crew-loading-copy">
          <p>{label}</p>
          <span className="crew-loading-dots" aria-hidden="true"><i /><i /><i /></span>
        </div>
      </div>
    </div>
  );

  // Full-screen fallbacks escape transformed route containers. Panel fallbacks
  // leave an already-mounted title/back control usable.
  return placement === 'viewport' && typeof document !== 'undefined'
    ? createPortal(loadingSurface, document.body) : loadingSurface;
};
