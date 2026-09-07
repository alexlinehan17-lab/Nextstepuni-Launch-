/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Starguy, alive. The same drawing — not a redraw — placed in Rive as a
 * raster image (public/assets/landing/starguy.riv). Its state machine
 * "Traveller" is one 1D blend on the number input `speed` (0–100): at rest
 * the `idle` breath (a 1% scale swell over 2.4s), at a fast flick the `walk`
 * stride (an 8px lift and a ±1.5° lean about the star, 0.8s). Between them
 * the runtime crossfades, so his stride grows with his speed down the page.
 *
 * The file also carries a one-shot `land` squash timeline and `land`/`step`
 * inputs, but its graph does not route to that timeline yet, so the landing
 * squash is done here, on the wrapper, when a hop arrives. Both inputs are
 * still fed to the rig; when the graph gains those transitions the wrapper
 * squash is the only thing to remove.
 *
 * Until the file exists, or if it fails to load, this renders the PNG exactly
 * as before, so nothing on the page changes appearance; the .riv only adds
 * motion. The lite runtime (no text, no audio) is enough for an image, and
 * its wasm is served from our own bundle rather than a CDN.
 */

import React, { useEffect, useState } from 'react';
import { Alignment, Fit, Layout, RuntimeLoader, useRive, useStateMachineInput } from '@rive-app/react-canvas-lite';
import { animate, useMotionValue, useMotionValueEvent, type MotionValue } from 'framer-motion';
import { MotionSpan } from '../../Motion';
import { Starguy } from '../primitives';

export const STARGUY_RIV = '/assets/landing/starguy.riv';
export const STARGUY_STATE_MACHINE = 'Traveller';
/** The PNG's own proportions; the Rive artboard is authored to match. */
export const STARGUY_RATIO = '1030 / 1193';
/** Where he stands: the star, as a fraction of the drawing (the rig's origin too). */
const STAR_ORIGIN = '62% 86%';
/** The traveller's hop lasts this long; the squash lands as it ends. */
const HOP_MS = 450;

RuntimeLoader.setWasmUrl(new URL('@rive-app/canvas-lite/rive.wasm', import.meta.url).href);

let rivKnown: boolean | null = null;
const rivExists = async (): Promise<boolean> => {
  if (rivKnown !== null) return rivKnown;
  try {
    // A dev server answers unknown paths with its HTML shell and a 200, so a
    // 200 alone is not proof: the file must also be a binary, not a page.
    const r = await fetch(STARGUY_RIV, { method: 'HEAD' });
    rivKnown = r.ok && !/text\/html/i.test(r.headers.get('content-type') ?? '');
  } catch { rivKnown = false; }
  return rivKnown;
};

const Rig: React.FC<{ speed?: MotionValue<number>; land?: boolean; step?: number; onFail: () => void }> = ({ speed, land = false, step = 0, onFail }) => {
  const { rive, RiveComponent } = useRive({
    src: STARGUY_RIV,
    stateMachine: STARGUY_STATE_MACHINE,
    autoplay: true,
    layout: new Layout({ fit: Fit.Contain, alignment: Alignment.BottomCenter }),
    onLoadError: onFail,
  });
  const speedInput = useStateMachineInput(rive, STARGUY_STATE_MACHINE, 'speed');
  const landInput = useStateMachineInput(rive, STARGUY_STATE_MACHINE, 'land');
  const stepInput = useStateMachineInput(rive, STARGUY_STATE_MACHINE, 'step');
  useMotionValueEvent(speed ?? (null as never), 'change', v => { if (speedInput) speedInput.value = v; });
  useEffect(() => { if (landInput) landInput.value = land; }, [land, landInput]);
  useEffect(() => { if (step > 0) stepInput?.fire(); }, [step, stepInput]);
  return <RiveComponent style={{ width: '100%', aspectRatio: STARGUY_RATIO, display: 'block' }} />;
};

/**
 * The figure the traveller (and any slot) renders. `speed` is a MotionValue
 * so a scroll-linked value can drive the stride without re-rendering. Each
 * `step` (a hop to a new place) ends in a small squash-and-recover about the
 * star, the same 0.45s the rig's own land timeline describes.
 */
export const StarguyFigure: React.FC<{ speed?: MotionValue<number>; land?: boolean; step?: number; className?: string; style?: React.CSSProperties }> = ({ speed, land, step = 0, className = '', style }) => {
  const [mode, setMode] = useState<'checking' | 'rive' | 'png'>('checking');
  const scaleX = useMotionValue(1);
  const scaleY = useMotionValue(1);
  useEffect(() => { let on = true; rivExists().then(ok => { if (on) setMode(ok ? 'rive' : 'png'); }); return () => { on = false; }; }, []);
  useEffect(() => {
    if (step <= 0) return;
    const id = window.setTimeout(() => {
      animate(scaleX, [1, 1.04, 0.99, 1], { duration: 0.45, times: [0, 0.26, 0.67, 1], ease: 'easeOut' });
      animate(scaleY, [1, 0.94, 1.02, 1], { duration: 0.45, times: [0, 0.26, 0.67, 1], ease: 'easeOut' });
    }, HOP_MS);
    return () => window.clearTimeout(id);
  }, [step, scaleX, scaleY]);
  return (
    <MotionSpan className={className} style={{ display: 'block', scaleX, scaleY, transformOrigin: STAR_ORIGIN, ...style }}>
      {mode === 'rive'
        ? <Rig speed={speed} land={land} step={step} onFail={() => setMode('png')} />
        : <Starguy size={0} style={{ width: '100%', height: 'auto' }} />}
    </MotionSpan>
  );
};

export default StarguyFigure;
