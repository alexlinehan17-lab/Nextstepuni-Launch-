/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useDeckSound — tiny procedural Web Audio cues for the card decks (no audio
 * files). Synthesises gentle blips for swipe / save / skip / tap / complete.
 * The AudioContext is created lazily and resumed on the first user gesture
 * (swipe/tap), satisfying browser autoplay rules. Silently no-ops if Web Audio
 * is unavailable. Sound can be muted via setEnabled(false).
 */

import { useRef, useCallback } from 'react';

type Tone = 'swipe' | 'save' | 'skip' | 'tap' | 'complete';

export function useDeckSound() {
  const ctxRef = useRef<AudioContext | null>(null);
  const enabledRef = useRef(true);

  const getCtx = useCallback((): AudioContext | null => {
    if (typeof window === 'undefined') return null;
    if (!ctxRef.current) {
      const AC = window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!AC) return null;
      try { ctxRef.current = new AC(); } catch { return null; }
    }
    if (ctxRef.current && ctxRef.current.state === 'suspended') ctxRef.current.resume().catch(() => {});
    return ctxRef.current;
  }, []);

  const blip = useCallback(
    (c: AudioContext, freq: number, durSec: number, type: OscillatorType, gain = 0.07, slideTo?: number) => {
      const o = c.createOscillator();
      const g = c.createGain();
      o.type = type;
      o.frequency.setValueAtTime(freq, c.currentTime);
      if (slideTo) o.frequency.exponentialRampToValueAtTime(slideTo, c.currentTime + durSec);
      g.gain.setValueAtTime(0.0001, c.currentTime);
      g.gain.exponentialRampToValueAtTime(gain, c.currentTime + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + durSec);
      o.connect(g);
      g.connect(c.destination);
      o.start();
      o.stop(c.currentTime + durSec + 0.03);
    },
    [],
  );

  const play = useCallback(
    (tone: Tone) => {
      if (!enabledRef.current) return;
      const c = getCtx();
      if (!c) return;
      try {
        if (tone === 'swipe') blip(c, 300, 0.18, 'sine', 0.05, 500);
        else if (tone === 'save') {
          blip(c, 523, 0.12, 'sine', 0.06);
          window.setTimeout(() => { const c2 = getCtx(); if (c2) blip(c2, 784, 0.16, 'sine', 0.06); }, 85);
        } else if (tone === 'skip') blip(c, 240, 0.12, 'sine', 0.035, 170);
        else if (tone === 'tap') blip(c, 460, 0.06, 'triangle', 0.035);
        else if (tone === 'complete') {
          [523, 659, 784, 1047].forEach((f, i) =>
            window.setTimeout(() => { const cc = getCtx(); if (cc) blip(cc, f, 0.22, 'sine', 0.055); }, i * 110),
          );
        }
      } catch { /* ignore audio errors */ }
    },
    [getCtx, blip],
  );

  const setEnabled = useCallback((v: boolean) => { enabledRef.current = v; }, []);

  return { play, setEnabled };
}
