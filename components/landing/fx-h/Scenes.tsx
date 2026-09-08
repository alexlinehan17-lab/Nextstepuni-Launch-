/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scenes that soak through each other. Every chapter stands on its own
 * full-bleed drawing in the page's materials — ruled answer-book lines,
 * the SEC cover tints, contour lines, a week grid, CAO boxes, graph paper,
 * a compass and a road (scripts/landing/scenes-svg.mjs) — and between two
 * chapters the next scene bleeds up through the last like ink in fibre,
 * scrubbed by the scroll (bleed.ts). Mounted beside <Chapters /> in main;
 * positions itself behind the chapters (fx-h.css, z-index −1) and reads the
 * chapters off the DOM, so a seventh article is a seventh scene.
 *
 * Without WebGL2, under prefers-reduced-motion, under ?static=1, and on
 * phones (battery), the scenes are still there, cut at the chapter
 * boundaries by the page's ink blots. ?scenes=static forces that;
 * ?scenes=0 removes the scenes altogether (for measuring).
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { isStatic } from '../fx/env';
import { Bleed } from './bleed';
import { bleedSpan, measureLayout, mixAt, sameLayout, sceneUrl, type Layout } from './layout';
import './fx-h.css';

type Mode = 'bleed' | 'static' | 'off';

const decideMode = (): Mode => {
  if (typeof window === 'undefined') return 'off';
  const want = new URLSearchParams(window.location.search).get('scenes');
  if (want === '0') return 'off';
  if (want === 'static' || isStatic()) return 'static';
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return 'static';
  if (window.matchMedia('(hover: none) and (pointer: coarse)').matches || window.innerWidth < 768) return 'static';
  return 'bleed';
};

/** Where the chapters are, kept current through font swaps, image loads, resizes and a chapter arriving. */
const useLayout = (enabled: boolean): Layout | null => {
  const [layout, setLayout] = useState<Layout | null>(null);
  useEffect(() => {
    if (!enabled) return;
    let raf = 0;
    const measure = (): void => {
      raf = 0;
      const next = measureLayout(window.innerHeight);
      setLayout(prev => (sameLayout(prev, next) ? prev : next));
    };
    const schedule = (): void => { if (!raf) raf = requestAnimationFrame(measure); };
    schedule();
    document.fonts?.ready.then(schedule).catch(() => undefined);
    window.addEventListener('resize', schedule);
    window.addEventListener('load', schedule);
    const section = document.getElementById('chapters');
    const ro = typeof ResizeObserver !== 'undefined' && section ? new ResizeObserver(schedule) : null;
    if (section) ro?.observe(section);
    const mo = section ? new MutationObserver(schedule) : null;
    if (section) mo?.observe(section, { childList: true, subtree: true });
    return () => {
      if (raf) cancelAnimationFrame(raf);
      window.removeEventListener('resize', schedule);
      window.removeEventListener('load', schedule);
      ro?.disconnect();
      mo?.disconnect();
    };
  }, [enabled]);
  return layout;
};

/** How far a scene runs on under the next one's blot cut. */
const UNDER = 260;

/** The still scenes: one div per chapter, the tile repeating down it. */
const StaticScenes: React.FC<{ layout: Layout }> = ({ layout }) => {
  const { sectionTop, sectionBottom, mainTop, bands, boundaries } = layout;
  const n = bands.length;
  return (
    <div className="fxh-track" aria-hidden="true" style={{ top: sectionTop - mainTop, height: sectionBottom - sectionTop }}>
      {bands.map((band, i) => {
        // The first fills from the section's top; each next one starts a blot's depth above its rule and runs under the one after.
        const start = i === 0 ? sectionTop : boundaries[i] - 120;
        const end = i === n - 1 ? sectionBottom : boundaries[i + 1] + UNDER;
        const cut = i > 0 ? ` fxh-scene--cut fxh-scene--blot-${((i - 1) % 3) + 1}` : '';
        return (
          <div
            key={band.id}
            className={`fxh-scene${cut}`}
            style={{ top: start - sectionTop, height: end - start, backgroundImage: `url(${sceneUrl(band.scene)})` }}
          />
        );
      })}
    </div>
  );
};

/** The bleed: a sticky canvas riding a track that spans the chapters and the bleeds in and out of them. */
const BleedScenes: React.FC<{ layout: Layout | null; onFail: () => void }> = ({ layout, onFail }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const layoutRef = useRef<Layout | null>(layout);
  layoutRef.current = layout;
  const redraw = useRef<() => void>(() => undefined);
  const [box, setBox] = useState<{ top: number; height: number }>({ top: 0, height: 0 });

  useEffect(() => {
    if (!layout) return;
    const H = window.innerHeight;
    const S = bleedSpan(layout, H);
    // Far enough above and below the chapters that the canvas is already at the window's top when the first bleed starts, and still there when the last ends.
    const top = layout.boundaries[0] - S - H / 2;
    const bottom = layout.boundaries[layout.boundaries.length - 1] + S + H / 2;
    setBox({ top: top - layout.mainTop, height: bottom - top });
    redraw.current();
  }, [layout]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const engine = new Bleed(canvas);
    if (!engine.ok) { engine.destroy(); onFail(); return; }
    let raf = 0;
    const frame = (): void => {
      raf = 0;
      const L = layoutRef.current;
      if (!L) return;
      const rect = canvas.getBoundingClientRect();
      const H = rect.height || window.innerHeight;
      if (rect.bottom <= 0 || rect.top >= window.innerHeight) return;
      const sy = window.scrollY;
      const mix = mixAt(L, sy + H / 2, bleedSpan(L, H));
      engine.render({ pageTop: rect.top + sy, a: mix.a, b: mix.b, p: mix.p, seed: mix.seed });
    };
    const schedule = (): void => { if (!raf) raf = requestAnimationFrame(frame); };
    redraw.current = schedule;
    engine.onReady = schedule;
    const resize = (): void => {
      engine.resize(canvas.clientWidth, canvas.clientHeight, Math.min(window.devicePixelRatio || 1, 2));
      schedule();
    };
    const lost = (e: Event): void => { e.preventDefault(); onFail(); };
    resize();
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', resize);
    canvas.addEventListener('webglcontextlost', lost);
    return () => {
      if (raf) cancelAnimationFrame(raf);
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', resize);
      canvas.removeEventListener('webglcontextlost', lost);
      redraw.current = () => undefined;
      engine.destroy();
    };
  }, [onFail]);

  return (
    <div className="fxh-track" aria-hidden="true" style={{ top: box.top, height: box.height }}>
      <canvas ref={canvasRef} className="fxh-canvas" />
    </div>
  );
};

const Scenes: React.FC = () => {
  const [mode, setMode] = useState<Mode>('off');
  useEffect(() => { setMode(decideMode()); }, []);
  const layout = useLayout(mode !== 'off');
  const fail = useCallback(() => setMode('static'), []);
  if (mode === 'off') return null;
  if (mode === 'bleed') return <BleedScenes layout={layout} onFail={fail} />;
  return layout ? <StaticScenes layout={layout} /> : null;
};

export default Scenes;
