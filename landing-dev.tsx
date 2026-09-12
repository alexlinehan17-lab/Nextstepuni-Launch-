/// <reference types="vite/client" />
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marketing landing entry, served at /landing in production and
 * /landing-dev.html during local development.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import { MotionGlobalConfig } from 'framer-motion';
import LandingPage from './components/landing/LandingPage';
import './index.css';
import './components/landing/landing.css';

// Returning app users may already have a worker controlling this document.
// Refresh its routing rules here too, without installing the offline app for
// first-time marketing visitors. Chapter windows recover on controllerchange.
if (import.meta.env.PROD && 'serviceWorker' in navigator) {
  void navigator.serviceWorker.getRegistration()
    .then(registration => registration?.update())
    .catch(() => {});
}

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
