/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Hero. The headline builds word by word (Shopify Design), starguy stands on
 * the baseline at the end of its last word, and the product playground sits
 * directly underneath (ElevenLabs) so the first scroll lands on something you
 * can use.
 */

import React from 'react';
import { COPY } from '../copy';
import { LineRise } from '../motion';
import { StarguySlot } from '../starguy/Traveller';
import { Button, Container, Eyebrow, Lede, Starguy } from '../primitives';
import { APP_URL, FONT, L } from '../theme';
import Playground from './Playground';

const Hero: React.FC = () => {
  return (
  <section id="top" aria-labelledby="hero-title" style={{ position: 'relative', paddingTop: 'clamp(32px, 5vw, 64px)', paddingBottom: 'clamp(40px, 5vw, 64px)' }}>
    <Container>
      <Eyebrow>{COPY.hero.eyebrow}</Eyebrow>
      <div className="mt-6 md:mt-8 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-end">
        <div className="lg:col-span-8">
          <LineRise
            as="h1"
            text={COPY.hero.headline}
            className="m-0 landing-hero-title"
            style={{ fontFamily: FONT.serif, fontWeight: 600, color: L.ink, fontSize: 'clamp(42px, 6.6vw, 86px)', lineHeight: 0.98, letterSpacing: '-0.025em' }}
            tail={
              <span aria-hidden="true" className="landing-starguy-lg" style={{ position: 'absolute', left: 'calc(100% + 0.06em)', bottom: '0.02em', width: '0.6em', lineHeight: 0 }}>
                <StarguySlot id="hero"><Starguy size={0} style={{ width: '100%', height: 'auto' }} /></StarguySlot>
              </span>
            }
          />
        </div>
        <div className="lg:col-span-4 lg:pb-2">
          <Lede>{COPY.hero.lede}</Lede>
          <div className="mt-7 flex flex-wrap items-center gap-4">
            <Button href={APP_URL} size="lg">{COPY.hero.primary}</Button>
            <Button variant="ghost" href="#playground">{COPY.hero.secondary}</Button>
          </div>
        </div>
      </div>
    </Container>
    <Container className="mt-10 md:mt-12">
      <Playground />
    </Container>
  </section>
  );
};

export default Hero;
