/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only harness for the onboarding flow — mirrors atlas-dev.tsx. Lets the
 * guided setup be iterated on visually without an account: `npx vite`, then
 * open /onboarding-dev.html. Never part of the production build (single-input
 * build ignores extra root HTML files).
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import Onboarding from './components/Onboarding';
import './index.css';

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(
    <Onboarding
      userId="dev-preview"
      userName="Aoife Byrne"
      onComplete={async profile => { console.log('[onboarding-dev] complete', profile); }}
      onSkip={() => console.log('[onboarding-dev] skipped')}
    />,
  );
}
