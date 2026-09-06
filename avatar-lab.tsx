/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Avatar Lab — the living showroom for Puifín the Puffin, the app's guide.
 * Renders every pose straight from the production component
 * (components/ui/Puifin.tsx), so this page is always true to what ships.
 * `npx vite`, then open /avatar-lab.html.
 *
 * Decision log: a hand-drawn SVG robin and a 3D vinyl-toy robin were both
 * rejected ("too SVG esque", "no character"). Alex chose the puffin from a
 * four-concept pitch (fox/squirrel/puffin/hedgehog) and named him Puifín;
 * the flat vibrant-toon renders come from docs/design/puifin_poses.py.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import Puifin, { type PuifinPose } from './components/ui/Puifin';
import './index.css';

const POSES: Array<{ pose: PuifinPose; label: string; use: string }> = [
  { pose: 'perch', label: 'Perch', use: 'default idle — guide bubbles, quiet company' },
  { pose: 'wave', label: 'Wave', use: 'greetings — onboarding welcome' },
  { pose: 'fly', label: 'Fly', use: '"next step" transitions, launches' },
  { pose: 'cheer', label: 'Cheer', use: 'completions, round summaries, streak days' },
  { pose: 'rest', label: 'Rest', use: 'rest days, all-done states' },
  { pose: 'think', label: 'Think', use: 'empty states, prompts to reflect' },
  { pose: 'read', label: 'Read', use: 'study surfaces, reading company' },
  { pose: 'point', label: 'Point', use: 'directing attention to one thing' },
  { pose: 'peek', label: 'Peek', use: 'edge-of-card appearances (overflow-hidden container)' },
  { pose: 'nod', label: 'Nod', use: 'gentle encouragement, caught-up states' },
];

const Lab: React.FC = () => (
  <div style={{ maxWidth: 900, margin: '0 auto', padding: '48px 24px 120px', background: '#fff', fontFamily: 'DM Sans, sans-serif' }}>
    <p style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.18em', textTransform: 'uppercase', color: '#A0968D' }}>NextStepUni · Avatar Lab</p>
    <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 34, margin: '6px 0 6px', color: '#1A1A1A' }}>Puifín the Puffin</h1>
    <p style={{ fontSize: 14, color: '#5A5550', maxWidth: 640, margin: '0 0 32px' }}>
      The Irish seabird that waddles alongside your study — modelled in Blender, rendered flat and vibrant.
      Every pose below comes through the production component: exactly what ships. Nod and
      peek reuse the perch render (CSS rock / container crop).
    </p>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 18 }}>
      {POSES.map(({ pose, label, use }) => (
        <div key={pose} style={{ textAlign: 'center' }}>
          <div style={{ background: '#fff', border: '1.5px solid #383838', borderRadius: 16, padding: 14, overflow: pose === 'peek' ? 'hidden' : undefined, height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Puifin pose={pose} size={128} />
          </div>
          <p style={{ fontSize: 12.5, fontWeight: 700, color: '#1A1A1A', margin: '8px 0 2px' }}>{label}</p>
          <p style={{ fontSize: 11, color: '#78716C', margin: 0, lineHeight: 1.4 }}>{use}</p>
        </div>
      ))}
    </div>
    <h2 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 22, margin: '44px 0 4px', color: '#1A1A1A' }}>Animations</h2>
    <p style={{ fontSize: 13, color: '#5A5550', margin: '0 0 18px' }}>
      Rendered frame sequences from the same Blender build, played as stepped sprite strips.
      Perch blinks every few seconds; wave plays twice then settles; fly flaps continuously.
    </p>
    <div style={{ display: 'flex', gap: 18 }}>
      {(['perch', 'wave', 'fly'] as PuifinPose[]).map((pose) => (
        <div key={`anim-${pose}`} style={{ textAlign: 'center' }}>
          <div style={{ background: '#fff', border: '1.5px solid #383838', borderRadius: 16, padding: 14, height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Puifin pose={pose} size={128} />
          </div>
          <p style={{ fontSize: 12.5, fontWeight: 700, color: '#1A1A1A', margin: '8px 0 2px' }}>
            {pose === 'perch' ? 'Blink (idle)' : pose === 'wave' ? 'Wave ×2, then rest' : 'Flap (loop)'}
          </p>
        </div>
      ))}
    </div>
    <div style={{ marginTop: 40, display: 'flex', alignItems: 'end', gap: 22 }}>
      <div style={{ textAlign: 'center' }}>
        <Puifin pose="perch" size={24} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>24</p>
      </div>
      <div style={{ textAlign: 'center' }}>
        <Puifin pose="perch" size={48} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>48</p>
      </div>
      <div style={{ textAlign: 'center' }}>
        <Puifin pose="perch" size={96} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>96</p>
      </div>
      <div style={{ textAlign: 'center' }}>
        <Puifin pose="perch" size={192} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>192</p>
      </div>
    </div>
  </div>
);

const root = document.getElementById('root');
if (root) createRoot(root).render(<Lab />);
