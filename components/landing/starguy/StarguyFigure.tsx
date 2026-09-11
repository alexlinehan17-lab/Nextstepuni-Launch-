/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Starguy, alive. The same drawing — not a redraw — placed in Rive as two
 * raster layers cut from the one PNG (public/assets/landing/starguy.riv):
 * the body, and the head on its own node pivoted at the neck. A root group
 * pivots at the star.
 *
 * Motion comes from two places in the file. The state machine "Traveller"
 * is one 1D blend on the number input `speed` (0–100): at rest the `idle`
 * breath (a 1% scale swell over 2.4s), at a fast flick the `walk` stride
 * (an 8px lift and a ±1.5° lean about the star, 0.8s). Everything else is
 * data-bound: the file's view model carries five numbers that drive node
 * properties directly, with no state-machine graph in between —
 *
 *   numberProperty1  head rotation, degrees          (look left/right)
 *   numberProperty2  head local Y, px, base −670.98  (nod up/down)
 *   numberProperty3  root rotation, degrees          (lean with motion)
 *   numberProperty4  root scale X, percent           (squash / stretch)
 *   numberProperty5  root scale Y, percent
 *
 * (The editor would not rename the properties, so the mapping lives here.)
 *
 * Until the file exists, or if it fails to load, this renders the PNG exactly
 * as before, so nothing on the page changes appearance; the .riv only adds
 * motion. The lite runtime (no text, no audio) is enough, and its wasm is
 * served from our own bundle rather than a CDN.
 */

import React, { useEffect, useRef, useState } from 'react';
import {
  Alignment, Fit, Layout, RuntimeLoader, useRive, useStateMachineInput,
  useViewModel, useViewModelInstance, useViewModelInstanceNumber,
} from '@rive-app/react-canvas-lite';
import { useMotionValueEvent, type MotionValue } from 'framer-motion';
import { Starguy } from '../primitives';

export const STARGUY_RIV = '/assets/landing/starguy.riv';
export const STARGUY_STATE_MACHINE = 'Traveller';
/** The PNG's own proportions; the Rive artboard is authored to match. */
export const STARGUY_RATIO = '1030 / 1193';

/** The head node's resting local Y inside the body node, in artboard px. */
const HEAD_BASE_Y = -670.98;
/** How far the head turns toward the pointer at full look, degrees. */
const LOOK_TURN = 7;
/** How far the head lifts or drops at full look, px. */
const LOOK_NOD = 5;

const VM = {
  headTurn: 'numberProperty1',
  headY: 'numberProperty2',
  lean: 'numberProperty3',
  scaleX: 'numberProperty4',
  scaleY: 'numberProperty5',
} as const;

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

/**
 * Everything that moves him, as MotionValues so scroll- and pointer-linked
 * values drive the rig without React re-renders. All optional; a missing
 * value leaves that part at rest.
 */
export interface StarguySignals {
  /** Stride: 0 at rest, 100 at a fast flick. */
  speed?: MotionValue<number>;
  /** Where he looks, −1…1 across and −1 (up)…1 (down). */
  lookX?: MotionValue<number>;
  lookY?: MotionValue<number>;
  /** Whole-body lean about the star, degrees; positive tips the head to the right. */
  lean?: MotionValue<number>;
  /** Squash (1) through rest (0) to stretch (−1), about the star. */
  squash?: MotionValue<number>;
}

const useBoundNumber = (path: string, instance: ReturnType<typeof useViewModelInstance>) => {
  const { setValue } = useViewModelInstanceNumber(path, instance);
  const ref = useRef(setValue);
  ref.current = setValue;
  return ref;
};

const useDrive = (value: MotionValue<number> | undefined, apply: (v: number) => void) => {
  const applyRef = useRef(apply);
  applyRef.current = apply;
  useMotionValueEvent(value ?? (null as never), 'change', v => applyRef.current(v));
  // Push the current value once the rig is ready, so a value set before load lands.
  useEffect(() => { if (value) applyRef.current(value.get()); });
};

const Rig: React.FC<StarguySignals & { onFail: () => void }> = ({ speed, lookX, lookY, lean, squash, onFail }) => {
  const { rive, RiveComponent } = useRive({
    src: STARGUY_RIV,
    stateMachine: STARGUY_STATE_MACHINE,
    autoplay: true,
    autoBind: true,
    layout: new Layout({ fit: Fit.Contain, alignment: Alignment.BottomCenter }),
    onLoadError: onFail,
  });
  const speedInput = useStateMachineInput(rive, STARGUY_STATE_MACHINE, 'speed');
  const viewModel = useViewModel(rive, { useDefault: true });
  const instance = useViewModelInstance(viewModel, { useDefault: true, rive });
  const headTurn = useBoundNumber(VM.headTurn, instance);
  const headY = useBoundNumber(VM.headY, instance);
  const leanDeg = useBoundNumber(VM.lean, instance);
  const scaleX = useBoundNumber(VM.scaleX, instance);
  const scaleY = useBoundNumber(VM.scaleY, instance);

  useMotionValueEvent(speed ?? (null as never), 'change', v => { if (speedInput) speedInput.value = v; });
  useEffect(() => { if (speedInput && speed) speedInput.value = speed.get(); }, [speedInput, speed]);
  useDrive(lookX, v => headTurn.current(clamp(v, -1, 1) * LOOK_TURN));
  useDrive(lookY, v => headY.current(HEAD_BASE_Y + clamp(v, -1, 1) * LOOK_NOD));
  useDrive(lean, v => leanDeg.current(clamp(v, -12, 12)));
  useDrive(squash, v => {
    const s = clamp(v, -1, 1);
    // Volume roughly conserved: squash widens, stretch narrows.
    scaleX.current(100 + s * 5);
    scaleY.current(100 - s * 7);
  });
  return <RiveComponent style={{ width: '100%', aspectRatio: STARGUY_RATIO, display: 'block' }} />;
};

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

/**
 * The figure the traveller (and any slot) renders. Signals are MotionValues
 * so the traveller's springs and the pointer drive the rig directly.
 */
export const StarguyFigure: React.FC<StarguySignals & { className?: string; style?: React.CSSProperties }> = ({ className = '', style, ...signals }) => {
  const [mode, setMode] = useState<'checking' | 'rive' | 'png'>('checking');
  useEffect(() => { let on = true; rivExists().then(ok => { if (on) setMode(ok ? 'rive' : 'png'); }); return () => { on = false; }; }, []);
  return (
    <span className={className} style={{ display: 'block', ...style }}>
      {mode === 'rive'
        ? <Rig {...signals} onFail={() => setMode('png')} />
        : <Starguy size={0} style={{ width: '100%', height: 'auto' }} />}
    </span>
  );
};

export default StarguyFigure;
