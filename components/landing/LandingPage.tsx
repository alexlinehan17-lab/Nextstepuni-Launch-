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
import HowItWorks from './sections/HowItWorks';
import Subjects from './sections/Subjects';
import Schools from './sections/Schools';
import Footer from './sections/Footer';
import { setupSmoothScroll } from './scroll';

const LandingPage: React.FC = () => {
  useEffect(() => setupSmoothScroll(), []);
  return (
  <div className="landing-page">
    <Nav />
    <main>
      <Hero />
      <Numbers />
      <Chapters />
      <HowItWorks />
      <Subjects />
      <Schools />
    </main>
    <Footer />
  </div>
  );
};

export default LandingPage;
