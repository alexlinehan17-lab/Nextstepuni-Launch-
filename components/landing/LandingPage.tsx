/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marketing landing page. Composed from sections in ./sections; every
 * word comes from ./copy.ts and every number from ./demoData.ts. Rendered by
 * landing-dev.tsx while it is dev-only.
 */

import React, { useEffect } from 'react';
import Nav from './sections/Nav';
import Hero from './sections/Hero';
import Numbers from './sections/Numbers';
import Chapters from './sections/Chapters';
import Examiner from './sections/Examiner';
import AskThePapers from './sections/AskThePapers';
import Subjects from './sections/Subjects';
import Footer from './sections/Footer';
import { setupSmoothScroll } from './scroll';
import { StarguyProvider } from './starguy/Traveller';

const LandingPage: React.FC = () => {
  useEffect(() => {
    if (['#today', '#certle'].includes(window.location.hash)) { window.location.replace('/certle'); return; }
    return setupSmoothScroll();
  }, []);
  return (
  <StarguyProvider>
  <div className="landing-page">
    <Nav />
    <main>
      <Hero />
      <Numbers />
      <Chapters />
      <Examiner />
      <AskThePapers />
      <Subjects />
    </main>
    <Footer />
  </div>
  </StarguyProvider>
  );
};

export default LandingPage;
