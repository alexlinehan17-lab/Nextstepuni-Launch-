/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How it works: three numbered steps set on the page's ruled paper — numeral
 * and title on one rule, the line beneath on the next, a blank rule closing
 * each step (fx-foundation/foundation.css) — then the page's one CTA row:
 * open the app, or go back up and try the Mark Bank.
 */

import React from 'react';
import { COPY } from '../copy';
import { Reveal } from '../motion';
import { Body, Button, Container, Display, Eyebrow, Lede, SectionRule } from '../primitives';
import { APP_URL, FONT, L, SPACE } from '../theme';
import { openDemo } from './Playground';

const HowItWorks: React.FC = () => (
  <section id="how" className={SPACE.section} style={{ position: 'relative', scrollMarginTop: 70 }}>
    <SectionRule />
    <Container>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16">
        <div className="lg:col-span-4">
          <Eyebrow>{COPY.how.eyebrow}</Eyebrow>
          <Display size="section" as="h2" className="mt-4">{COPY.how.title}</Display>
        </div>
        <ol className="landing-steps lg:col-span-8">
          {COPY.how.steps.map((s, i) => (
            <li key={s.n} className="landing-step">
              <Reveal delay={i * 0.08}>
                <div className="landing-step-row">
                  <div className="landing-step-n" aria-hidden="true" style={{ fontFamily: FONT.serif, fontWeight: 600, color: L.ink }}>{s.n}</div>
                  <div>
                    <h3 className="landing-step-title" style={{ fontFamily: FONT.serif, fontWeight: 600, color: L.ink }}>
                      <span className="sr-only">{s.n}. </span>{s.title}
                    </h3>
                    <Body className="landing-step-body" style={{ fontSize: 16 }}>{s.body}</Body>
                  </div>
                </div>
              </Reveal>
            </li>
          ))}
        </ol>
      </div>

      {/* CTA row */}
      <div className="pt-8 mt-6" style={{ borderTop: `1px solid ${L.hairline}` }}>
        <Lede>{COPY.cta.line}</Lede>
        <div className="mt-6 flex flex-wrap items-center gap-4">
          <Button href={APP_URL} size="lg">{COPY.cta.primary}</Button>
          <Button variant="ghost" onClick={() => openDemo('markbank')}>{COPY.cta.secondary}</Button>
        </div>
      </div>
    </Container>
  </section>
);

export default HowItWorks;
