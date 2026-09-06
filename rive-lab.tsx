/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Rive Lab — proves the @rive-app/react-canvas runtime end-to-end before
 * Rua's own .riv exists: loads Rive's public demo file (vehicles.riv,
 * state machine "bumpy", trigger "bump"), and previews the layered
 * master SVG (docs/design/rua-master.svg) that gets imported into the
 * Rive editor for rigging. When rua.riv lands in public/assets/rua/,
 * this page is where it gets smoke-tested first.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import { useRive, useStateMachineInput } from '@rive-app/react-canvas';
import './index.css';

const DEMO_RIV = 'https://cdn.rive.app/animations/vehicles.riv';

const DemoCard: React.FC = () => {
  const { rive, RiveComponent } = useRive({
    src: DEMO_RIV,
    stateMachines: 'bumpy',
    autoplay: true,
  });
  const bump = useStateMachineInput(rive, 'bumpy', 'bump');
  return (
    <div style={{ border: '1.5px solid #383838', borderRadius: 16, overflow: 'hidden' }}>
      <div style={{ height: 300, cursor: 'pointer' }} onClick={() => bump?.fire()}>
        <RiveComponent style={{ width: '100%', height: '100%' }} />
      </div>
      <p style={{ margin: 0, padding: '10px 14px', fontSize: 12.5, color: '#5A5550', borderTop: '1.5px solid #E7E5E4' }}>
        Rive public demo — state machine <code>bumpy</code>. Click to fire the <code>bump</code> trigger.
        {rive ? ' Runtime loaded ✓' : ' Loading…'}
      </p>
    </div>
  );
};

const Lab: React.FC = () => (
  <div style={{ maxWidth: 960, margin: '0 auto', padding: '48px 24px 120px', background: '#fff', fontFamily: 'DM Sans, sans-serif' }}>
    <p style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.18em', textTransform: 'uppercase', color: '#A0968D' }}>NextStepUni · Rive Lab</p>
    <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 34, margin: '6px 0 6px', color: '#1A1A1A' }}>Rua goes interactive</h1>
    <p style={{ fontSize: 14, color: '#5A5550', maxWidth: 680, margin: '0 0 28px' }}>
      Left: the Rive runtime running a public demo file with a live state machine — the exact
      wiring Rua will use. Right: the layered master SVG that gets imported into the Rive editor
      for rigging (each part is a named group).
    </p>
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
      <DemoCard />
      <div style={{ border: '1.5px solid #383838', borderRadius: 16, overflow: 'hidden' }}>
        <img src="/docs/design/rua-master.svg" alt="Rua master vector" style={{ width: '100%', height: 300, objectFit: 'contain', display: 'block' }} />
        <p style={{ margin: 0, padding: '10px 14px', fontSize: 12.5, color: '#5A5550', borderTop: '1.5px solid #E7E5E4' }}>
          rua-master.svg — rig-ready layers: tail, wings, legs, body, head, bib, belly, beak, eyes (sclera/pupil/spark/lid).
        </p>
      </div>
    </div>
    <h2 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 20, margin: '36px 0 8px', color: '#1A1A1A' }}>Planned state machine</h2>
    <p style={{ fontSize: 13.5, color: '#5A5550', maxWidth: 680, margin: 0, lineHeight: 1.6 }}>
      One artboard, one state machine (<code>rua</code>): an <em>idle</em> loop (breath + blink every few
      seconds) as the default state; triggers <code>wave</code>, <code>cheer</code>, <code>point</code> that
      play once and return to idle; booleans <code>rest</code> (settles her into sleep) and{' '}
      <code>read</code>; a number input <code>look</code> (−1..1) panning the pupils. The component keeps
      today's pose API and maps poses onto these inputs.
    </p>
  </div>
);

const root = document.getElementById('root');
if (root) createRoot(root).render(<Lab />);
