import { useCallback, useEffect, useRef } from 'react';
import { useSoundMuted } from '../components/approved-ui-runtime';

/** The approved bloom cues, played only by a student's transition action. */
export function useStudyTransitionSound() {
  const muted = useSoundMuted();
  const mutedRef = useRef(muted);
  mutedRef.current = muted;
  const tracks = useRef<HTMLAudioElement[]>([]);
  const stop = useCallback(() => {
    tracks.current.forEach(track => { track.pause(); track.currentTime = 0; });
  }, []);
  useEffect(() => {
    tracks.current = ['pause', 'return'].map(direction => {
      const track = new Audio(`/sounds/study-bloom-${direction}.wav`);
      track.preload = 'auto';
      track.volume = .6;
      return track;
    });
    window.addEventListener('pagehide', stop);
    const onVisibility = () => { if (document.hidden) stop(); };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      stop(); tracks.current = [];
      window.removeEventListener('pagehide', stop);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, [stop]);
  useEffect(() => { if (muted) stop(); }, [muted, stop]);
  const play = useCallback((direction: 'pause' | 'return') => {
    stop();
    if (mutedRef.current) return;
    const track = tracks.current[direction === 'pause' ? 0 : 1];
    // A denied or unavailable audio device must never hold up the transition.
    try { void track?.play()?.catch(() => {}); } catch { /* no audio device */ }
  }, [stop]);
  return { play, muted };
}
