/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The word "guesswork" inside the display line. The real word stays in the
 * DOM — it is what screen readers read and what the canvas is measured
 * against — and once the field is ready it is painted transparent while the
 * canvas shows in its place. Plain text under prefers-reduced-motion, under
 * ?static=1, with ?gpu=none, and wherever neither WebGPU nor WebGL 2 exists.
 * The three module (guessworkField.ts, plus three/webgpu) is fetched only
 * once the line comes within 600px of the viewport.
 */

import React, { useEffect, useRef, useState } from 'react';
import { useReducedMotion } from '../../Motion';
import { isStatic } from '../fx/env';
import type { GuessworkField } from './guessworkField';

const hasWebGL2 = (): boolean => {
  try { return !!document.createElement('canvas').getContext('webgl2'); } catch { return false; }
};

export const GuessworkWord: React.FC<{ word: string; onTouch?: () => void; onReady?: (backend: 'webgpu' | 'webgl') => void }> = ({ word, onTouch, onReady }) => {
  const reduce = useReducedMotion();
  const host = useRef<HTMLSpanElement>(null);
  const text = useRef<HTMLSpanElement>(null);
  const probe = useRef<HTMLSpanElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const hit = useRef<HTMLSpanElement>(null);
  const [on, setOn] = useState(false);

  useEffect(() => {
    if (reduce || isStatic()) return;
    const gpu = new URLSearchParams(window.location.search).get('gpu');
    if (gpu === 'none') return;
    const webgpu = gpu !== 'webgl' && 'gpu' in navigator && !!(navigator as { gpu?: unknown }).gpu;
    if (!webgpu && !hasWebGL2()) return;
    const el = host.current;
    if (!el) return;
    let field: GuessworkField | null = null;
    let cancelled = false;
    const io = new IntersectionObserver(entries => {
      if (!entries.some(e => e.isIntersecting)) return;
      io.disconnect();
      import('./guessworkField')
        .then(mod => {
          if (cancelled || !canvas.current || !text.current || !probe.current || !hit.current) return null;
          return mod.createGuessworkField({
            canvas: canvas.current, host: el, text: text.current, probe: probe.current, hit: hit.current,
            forceWebGL: !webgpu,
            onReady: backend => { if (!cancelled) { setOn(true); onReady?.(backend); } },
            onTouch,
          });
        })
        .then(f => { if (f) { if (cancelled) f.destroy(); else field = f; } })
        .catch(err => { console.warn('guesswork: falling back to plain text', err); });
    }, { rootMargin: '600px 0px' });
    io.observe(el);
    return () => { cancelled = true; io.disconnect(); field?.destroy(); };
  // The callbacks are stable for the life of the section, so only the motion preference re-runs this.
  }, [reduce]);

  return (
    <span ref={host} className="fxi-guess" data-canvas={on ? 'on' : 'off'}>
      <span ref={text} className="fxi-guess-text">{word}</span>
      <span ref={probe} aria-hidden="true" style={{ display: 'inline-block', width: 0, height: 0 }} />
      <canvas ref={canvas} aria-hidden="true" hidden={!on} />
      {/* Keep the heading's inline text layout while giving the word a hit area. */}
      <span ref={hit} className="fxi-guess-hit" aria-hidden="true" />
    </span>
  );
};

export default GuessworkWord;
