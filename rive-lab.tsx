/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Starguy Lab — smoke-tests the Rive rig of the website's one character.
 * Drop the exported file at public/assets/landing/starguy.riv (artboard the
 * PNG's own proportions, state machine "Traveller", inputs speed 0–100,
 * land, step) and this page shows it beside the untouched PNG with the
 * three inputs on sliders. Until the file exists it shows the PNG fallback,
 * which is exactly what the landing page renders too. Dev only: served by
 * Vite, ignored by the single-input production build.
 */

import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { useMotionValue } from 'framer-motion';
import { StarguyFigure, STARGUY_RIV } from './components/landing/starguy/StarguyFigure';
import './index.css';

const Lab: React.FC = () => {
  const speed = useMotionValue(0);
  const [speedUi, setSpeedUi] = useState(0);
  const [land, setLand] = useState(false);
  const [step, setStep] = useState(0);
  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: '48px 24px 120px', background: '#fff', fontFamily: 'DM Sans, sans-serif', color: '#1A1A1A' }}>
      <p style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.18em', textTransform: 'uppercase', color: '#B84A0C' }}>NextStepUni · Starguy Lab</p>
      <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 34, margin: '6px 0 6px' }}>Starguy, alive</h1>
      <p style={{ fontSize: 14, color: '#5F5A55', maxWidth: 680, margin: '0 0 28px', lineHeight: 1.5 }}>
        Left: the PNG as it is. Right: <code>{STARGUY_RIV}</code> through the Rive runtime with the state machine
        inputs the landing page drives. If the file is missing the right side falls back to the PNG — nothing changes his appearance.
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div style={{ border: '1.5px solid #1A1A1A', borderRadius: 16, padding: 24 }}>
          <img src="/assets/landing/starguy.png" alt="Starguy, the PNG" style={{ width: 240, height: 'auto', display: 'block', margin: '0 auto' }} />
          <p style={{ margin: '14px 0 0', fontSize: 12.5, color: '#5F5A55', textAlign: 'center' }}>The drawing. It does not change.</p>
        </div>
        <div style={{ border: '1.5px solid #1A1A1A', borderRadius: 16, padding: 24 }}>
          <div style={{ width: 240, margin: '0 auto' }}><StarguyFigure speed={speed} land={land} step={step} /></div>
          <p style={{ margin: '14px 0 0', fontSize: 12.5, color: '#5F5A55', textAlign: 'center' }}>The rig, or the PNG until it lands.</p>
        </div>
      </div>
      <div style={{ marginTop: 28, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, fontSize: 13 }}>
        <label>speed · {speedUi}<br /><input type="range" min={0} max={100} value={speedUi} onChange={e => { const v = Number(e.target.value); setSpeedUi(v); speed.set(v); }} style={{ width: '100%' }} /></label>
        <label><input type="checkbox" checked={land} onChange={e => setLand(e.target.checked)} /> land (true at the footer)</label>
        <button type="button" onClick={() => setStep(n => n + 1)} style={{ minHeight: 36, borderRadius: 6, border: '1.5px solid #1A1A1A', background: '#fff', fontWeight: 700, boxShadow: '2px 2px 0 #1A1A1A' }}>fire step ({step})</button>
      </div>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(<React.StrictMode><Lab /></React.StrictMode>);
