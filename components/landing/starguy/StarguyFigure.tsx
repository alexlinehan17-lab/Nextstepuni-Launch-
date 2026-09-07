/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Starguy, alive. The same drawing — not a redraw — rigged in Rive as a
 * raster mesh (public/assets/landing/starguy.riv, state machine "Traveller",
 * inputs: speed 0–100, land, step). Until that file exists, or if it fails to
 * load, this renders the PNG exactly as before, so nothing on the page
 * changes appearance; the .riv only adds motion. The lite runtime (no text,
 * no audio) is enough for an image mesh, and its wasm is served from our
 * own bundle rather than a CDN.
 */

import React, { useEffect, useState } from 'react';
import { Alignment, Fit, Layout, RuntimeLoader, useRive, useStateMachineInput } from '@rive-app/react-canvas-lite';
import { useMotionValueEvent, type MotionValue } from 'framer-motion';
import { Starguy } from '../primitives';

export const STARGUY_RIV = '/assets/landing/starguy.riv';
export const STARGUY_STATE_MACHINE = 'Traveller';
/** The PNG's own proportions; the Rive artboard is authored to match. */
export const STARGUY_RATIO = '1030 / 1193';

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
    stateMachines: STARGUY_STATE_MACHINE,
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
 * so a scroll-linked value can drive the stride without re-rendering.
 */
export const StarguyFigure: React.FC<{ speed?: MotionValue<number>; land?: boolean; step?: number; className?: string; style?: React.CSSProperties }> = ({ speed, land, step, className = '', style }) => {
  const [mode, setMode] = useState<'checking' | 'rive' | 'png'>('checking');
  useEffect(() => { let on = true; rivExists().then(ok => { if (on) setMode(ok ? 'rive' : 'png'); }); return () => { on = false; }; }, []);
  if (mode === 'rive') {
    return (
      <span className={className} style={{ display: 'block', ...style }}>
        <Rig speed={speed} land={land} step={step} onFail={() => setMode('png')} />
      </span>
    );
  }
  return <Starguy size={0} className={className} style={{ width: '100%', height: 'auto', ...style }} />;
};

export default StarguyFigure;
