import React, { useCallback, useState, useSyncExternalStore } from 'react';
import { DARK_ARTWORK } from '../data/darkArtwork';

// A single observer serves every illustration, including private landing previews.
const listeners = new Set<() => void>();
let observer: MutationObserver | undefined;
function subscribe(listener: () => void) {
  listeners.add(listener);
  if (!observer) {
    observer = new MutationObserver(() => listeners.forEach(notify => notify()));
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  }
  return () => {
    listeners.delete(listener);
    if (!listeners.size) { observer?.disconnect(); observer = undefined; }
  };
}
const snapshot = () => document.documentElement.classList.contains('dark');
const serverSnapshot = () => false;

interface Props extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  /** For charcoal banners that remain dark in the light appearance. */
  darkSurface?: boolean;
  /** Use the existing alpha cutout on a light or tinted surface too. */
  transparentBackground?: boolean;
}

/** Original artwork in light mode, a paired transparent asset on dark surfaces.
 * Fills and ink are preserved; only the fine outside edge is supplied by CSS.
 */
export default function ThemeArtwork({ src, className = '', darkSurface = false, transparentBackground = false, onError, ...props }: Props) {
  const documentDark = useSyncExternalStore(subscribe, snapshot, serverSnapshot);
  const [element, setElement] = useState<HTMLImageElement | null>(null);
  const [failedSource, setFailedSource] = useState<string>();
  const ref = useCallback((node: HTMLImageElement | null) => setElement(node), []);
  const ownsLightPalette = Boolean(element?.closest('.account-entry, .setup-flow')) ||
    (Boolean(element?.closest('.landing-page')) && !document.documentElement.classList.contains('landing-preview-dark'));
  const dark = darkSurface || (documentDark && !ownsLightPalette);
  const pairedSource = dark || transparentBackground ? DARK_ARTWORK[src] : undefined;
  const resolvedSource = pairedSource && failedSource !== pairedSource ? pairedSource : src;
  return <img {...props} ref={ref} src={resolvedSource}
    className={`theme-filled-art ${darkSurface ? 'filled-art-on-dark' : ''} ${className}`}
    data-artwork-appearance={dark ? 'dark' : 'light'}
    onError={event => {
      if (pairedSource && resolvedSource === pairedSource) setFailedSource(pairedSource);
      else onError?.(event);
    }} />;
}
