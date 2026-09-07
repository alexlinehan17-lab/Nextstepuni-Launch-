/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Renders a desktop-sized surface (the real app, or a real app component)
 * inside whatever width the page gives it, by laying the child out at a fixed
 * logical width and scaling it down with a transform. The height follows the
 * scaled content so the page never reserves empty space.
 */

import React, { useEffect, useRef, useState } from 'react';

export const ScaledSurface: React.FC<{
  /** Logical width the child is laid out at, e.g. 1200. */
  width: number;
  /** Logical height the child is laid out at. */
  height: number;
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
  /** Called with the current scale, for anything that has to match it (a scripted cursor). */
  onScale?: (scale: number) => void;
}> = ({ width, height, children, className = '', style, onScale }) => {
  const hostRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);
  useEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    const sync = () => {
      const s = Math.min(1, host.clientWidth / width);
      setScale(s);
      onScale?.(s);
    };
    sync();
    const ro = new ResizeObserver(sync);
    ro.observe(host);
    return () => ro.disconnect();
  }, [width, onScale]);
  return (
    <div ref={hostRef} className={className} style={{ position: 'relative', width: '100%', height: Math.round(height * scale), overflow: 'hidden', ...style }}>
      <div style={{ position: 'absolute', top: 0, left: 0, width, height, transform: `scale(${scale})`, transformOrigin: '0 0' }}>
        {children}
      </div>
    </div>
  );
};

export default ScaledSurface;
