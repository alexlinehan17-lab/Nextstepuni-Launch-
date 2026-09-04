/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Avatar Lab — the living showroom for Rua the Robin, the app's guide.
 * Renders every pose straight from the production component
 * (components/ui/Rua.tsx), so this page is always true to what ships.
 * `npx vite`, then open /avatar-lab.html.
 *
 * Decision log: candidates (Robin / Wren / evolved Blob) were auditioned
 * here on 2026-09-04; Alex picked the Robin.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import Rua, { type RuaPose } from './components/ui/Rua';
import './index.css';

const POSES: Array<{ pose: RuaPose; label: string; use: string }> = [
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
    <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 34, margin: '6px 0 6px', color: '#1A1A1A' }}>Rua the Robin</h1>
    <p style={{ fontSize: 14, color: '#5A5550', maxWidth: 640, margin: '0 0 32px' }}>
      The bird that lands beside you while you work. Every pose below renders from the production
      component — what you see here is exactly what ships.
    </p>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 18 }}>
      {POSES.map(({ pose, label, use }) => (
        <div key={pose} style={{ textAlign: 'center' }}>
          <div style={{ background: '#fff', border: '1.5px solid #383838', borderRadius: 16, padding: 14, overflow: pose === 'peek' ? 'hidden' : undefined, height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Rua pose={pose} size={128} />
          </div>
          <p style={{ fontSize: 12.5, fontWeight: 700, color: '#1A1A1A', margin: '8px 0 2px' }}>{label}</p>
          <p style={{ fontSize: 11, color: '#78716C', margin: 0, lineHeight: 1.4 }}>{use}</p>
        </div>
      ))}
    </div>
    <div style={{ marginTop: 40, display: 'flex', alignItems: 'end', gap: 22 }}>
      <div style={{ textAlign: 'center' }}>
        <Rua pose="perch" size={24} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>24</p>
      </div>
      <div style={{ textAlign: 'center' }}>
        <Rua pose="perch" size={48} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>48</p>
      </div>
      <div style={{ textAlign: 'center' }}>
        <Rua pose="perch" size={96} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>96</p>
      </div>
      <div style={{ textAlign: 'center' }}>
        <Rua pose="perch" size={192} />
        <p style={{ fontSize: 10, color: '#A8A29E' }}>192</p>
      </div>
    </div>
  </div>
);

const root = document.getElementById('root');
if (root) createRoot(root).render(<Lab />);
