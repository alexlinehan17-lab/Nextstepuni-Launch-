/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A window into the real app: the actual running app in a same-origin
 * iframe, laid out at desktop size and scaled to fit. Same origin means the
 * landing page can reach into the document (to drive a scripted cursor or
 * deep-link a view) without the app knowing it is being watched.
 */

import React, { useCallback, useRef, useState } from 'react';
import { ScaledSurface } from './ScaledSurface';
import { L } from '../theme';

export interface LookingGlassHandle { doc: () => Document | null; win: () => Window | null }

export const LookingGlass: React.FC<{
  /** App URL to load, e.g. "/?demo=1&view=paper-trail". */
  src: string;
  width?: number;
  height?: number;
  title: string;
  className?: string;
  onReady?: (handle: LookingGlassHandle) => void;
  /** Mount the iframe only when this is true (keeps hidden tabs cheap). */
  active?: boolean;
}> = ({ src, width = 1280, height = 800, title, className = '', onReady, active = true }) => {
  const frameRef = useRef<HTMLIFrameElement>(null);
  const [loaded, setLoaded] = useState(false);
  const handleLoad = useCallback(() => {
    setLoaded(true);
    onReady?.({ doc: () => frameRef.current?.contentDocument ?? null, win: () => frameRef.current?.contentWindow ?? null });
  }, [onReady]);
  return (
    <ScaledSurface width={width} height={height} className={className}>
      {active && (
        <iframe
          ref={frameRef}
          src={src}
          title={title}
          width={width}
          height={height}
          onLoad={handleLoad}
          style={{ border: 0, display: 'block', width, height, background: L.paper, opacity: loaded ? 1 : 0, transition: 'opacity 240ms ease' }}
        />
      )}
    </ScaledSurface>
  );
};

export default LookingGlass;
