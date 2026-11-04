import { useEffect } from 'react';

export const PREVIEW_READY = 'landing-preview-ready';
export const PREVIEW_PLAYBACK = 'landing-preview-playback';

/** Commit alongside the real content, inside its Suspense boundary. An iframe
 * load event also fires for blocked documents and cannot prove it is ready. */
export default function PreviewReady() {
  useEffect(() => {
    window.parent.postMessage({ type: PREVIEW_READY }, window.location.origin);
  }, []);
  return null;
}
