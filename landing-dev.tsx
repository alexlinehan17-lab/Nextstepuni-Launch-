/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only harness for the marketing landing page — mirrors onboarding-dev.tsx.
 * `npx vite`, then open /landing-dev.html. Never part of the production build:
 * the single-input Vite build ignores extra root HTML files, so this is safe
 * on main while the page is still being designed. The page itself lives in
 * components/landing/.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import { MotionGlobalConfig } from 'framer-motion';
import LandingPage from './components/landing/LandingPage';
import './index.css';
import './components/landing/landing.css';

// ?static=1 completes every Framer animation instantly. Screenshot tooling
// drives Chrome tabs that report visibilityState "hidden", where the frame
// loop never ticks and the page would freeze on its initial keyframes.
// ?demo=<markbank|atlas|planner|launchpad>&mode=<sub-tab id> preselects the
// playground (read in sections/Playground.tsx).
const params = new URLSearchParams(window.location.search);
if (params.get('static')) { MotionGlobalConfig.skipAnimations = true; document.documentElement.classList.add('landing-static'); }

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(<LandingPage />);
}
