/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ?starguy=1 — a strip of buttons that fire each reaction on the public bus
 * (watch aims him at the hero's first CTA), plus the topple, so every moment
 * can be screenshotted mid-motion without waiting for its trigger.
 */

import React from 'react';
import { say } from './control';

const DevHarness: React.FC = () => {
  const cta = () => document.querySelector<HTMLElement>('#top [data-hero-cta] a');
  return (
    <div className="fx-char-dev" data-fx-char="dev" aria-hidden="true">
      <button type="button" onClick={() => { const el = cta(); if (el) say({ kind: 'watch', el }); }}>watch</button>
      <button type="button" onClick={() => say({ kind: 'unwatch' })}>unwatch</button>
      <button type="button" onClick={() => say({ kind: 'nod' })}>nod</button>
      <button type="button" onClick={() => say({ kind: 'tilt' })}>tilt</button>
      <button type="button" onClick={() => say({ kind: 'cheer' })}>cheer</button>
      <button type="button" onClick={() => window.dispatchEvent(new CustomEvent('starguy-dev', { detail: { kind: 'topple' } }))}>topple</button>
    </div>
  );
};

export default DevHarness;
