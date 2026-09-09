/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Certle: the band at the top that leads down to the day's Leaving Cert
 * question (sections/TodaysQuestion.tsx, #today). One real question a day,
 * marked by its own scheme, shared as squares — Wordle's shape, the SEC's
 * content. The name is Alex's brief ("something wordle adjacent"); it is one
 * constant here.
 */

import React from 'react';
import { Body, Button, Container, Display, Eyebrow } from '../primitives';
import { Reveal } from '../motion';
import { L } from '../theme';

export const CERTLE = {
  name: 'Certle',
  eyebrow: 'One a day',
  line: 'One real Leaving Cert question a day, marked by its own scheme.',
  body: 'Answer it, see the marks the scheme gives, and share your squares. A new one lands at midnight, Irish time.',
  cta: 'Play today’s question',
} as const;

const Certle: React.FC = () => (
  <section id="certle" aria-labelledby="certle-title" className="py-10 md:py-14" style={{ borderTop: `1px solid ${L.hairline}`, borderBottom: `1px solid ${L.hairline}` }}>
    <Container>
      <Reveal>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-12 items-center">
          <div className="lg:col-span-8">
            <Eyebrow>{CERTLE.name} · {CERTLE.eyebrow}</Eyebrow>
            <Display size="sub" as="h2" id="certle-title" className="mt-3">{CERTLE.line}</Display>
            <Body className="mt-3" style={{ maxWidth: '52ch' }}>{CERTLE.body}</Body>
          </div>
          <div className="lg:col-span-4 lg:justify-self-end">
            <Button href="#today" size="lg">{CERTLE.cta} ↓</Button>
          </div>
        </div>
      </Reveal>
    </Container>
  </section>
);

export default Certle;
