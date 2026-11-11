import { useCallback, useEffect, useRef } from 'react';
import { useSoundMuted } from '../components/approved-ui-runtime';

/** The approved bloom cues for study transitions, sharing the student's mute setting. */
export function useStudyTransitionSound() {
  const muted = useSoundMuted();
  const mutedRef = useRef(muted);
  mutedRef.current = muted;
  const tracks = useRef<HTMLAudioElement[]>([]);
  const playback = useRef(0);
  const prepared = useRef(false);
  const stop = useCallback(() => {
    playback.current += 1;
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
  // Unlock both HTML audio elements in the Start gesture. The countdown can
  // then use the same cue at zero without requiring another student action.
  const prepare = useCallback(() => {
    if (prepared.current || mutedRef.current || !tracks.current.length) return;
    prepared.current = true;
    const token = playback.current;
    tracks.current.forEach(track => {
      track.volume = 0;
      const ready = () => { if (playback.current === token) { track.pause(); track.currentTime = 0; track.volume = .6; } };
      try { void track.play()?.then(ready, ready); } catch { ready(); }
    });
  }, []);
  const play = useCallback((direction: 'pause' | 'return') => {
    stop();
    if (mutedRef.current) return;
    const track = tracks.current[direction === 'pause' ? 0 : 1];
    if (track) track.volume = .6;
    // A denied or unavailable audio device must never hold up the transition.
    try { void track?.play()?.catch(() => {}); } catch { /* no audio device */ }
  }, [stop]);
  return { play, muted, prepare };
}
