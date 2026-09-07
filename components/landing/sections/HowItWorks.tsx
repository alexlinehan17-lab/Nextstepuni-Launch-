/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How it works: three numbered steps on a stepped rail — the app's own
 * sequence idiom (done / current / upcoming on a hairline spine) — then the
 * page's one CTA row: open the app, or go back up and try the Mark Bank.
 */

import React from 'react';
import { COPY } from '../copy';
import { Reveal } from '../motion';
import { Body, Button, Container, Display, Eyebrow, Lede } from '../primitives';
import { APP_URL, FONT, L, SPACE } from '../theme';
import { openDemo } from './Playground';

const HowItWorks: React.FC = () => (
  <section id="how" className={SPACE.section} style={{ borderTop: `1.5px solid ${L.ink}`, scrollMarginTop: 70 }}>
    <Container>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16">
        <div className="lg:col-span-4">
          <Eyebrow>{COPY.how.eyebrow}</Eyebrow>
          <Display size="section" as="h2" className="mt-4">{COPY.how.title}</Display>
        </div>
        <ol className="lg:col-span-8 m-0 p-0 list-none">
          {COPY.how.steps.map((s, i) => (
            <Reveal key={s.n} delay={i * 0.08}>
              <li className="grid gap-5" style={{ gridTemplateColumns: '48px 1fr', borderTop: `1px solid ${L.hairline}`, padding: '26px 0' }}>
                <div style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 40, lineHeight: 1, color: L.ink, letterSpacing: '-0.03em' }}>{s.n}</div>
                <div>
                  <h3 className="m-0" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 24, color: L.ink, lineHeight: 1.15, letterSpacing: '-0.015em' }}>{s.title}</h3>
                  <Body className="mt-2" style={{ fontSize: 16 }}>{s.body}</Body>
                </div>
              </li>
            </Reveal>
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
