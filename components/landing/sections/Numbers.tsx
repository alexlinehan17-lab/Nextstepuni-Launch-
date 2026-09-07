/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Numbers as identity, Leonardo's way: one full-width ink band that breaks
 * the white page, four numerals at display size that count up as they arrive.
 * Every figure is computed from repo data (see demoData.ts header). This is
 * the page's one dark surface.
 */

import React from 'react';
import { COPY } from '../copy';
import { CountUp, Reveal } from '../motion';
import { Container } from '../primitives';
import { FONT, L } from '../theme';

const Numbers: React.FC = () => (
  <section aria-label={COPY.numbers.eyebrow} style={{ background: L.ink, color: L.paper }}>
    <Container className="py-14 md:py-20">
      <div className="flex items-center gap-4 mb-10 md:mb-14">
        <span style={{ fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.16em', textTransform: 'uppercase', color: L.orange }}>{COPY.numbers.eyebrow}</span>
        <span aria-hidden="true" style={{ flex: 1, height: 1, background: 'rgba(255,255,255,0.18)' }} />
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-y-12 gap-x-8">
        {COPY.numbers.items.map((n, i) => (
          <Reveal key={n.label} delay={i * 0.08}>
            <div style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 'clamp(52px, 7.4vw, 112px)', lineHeight: 0.92, letterSpacing: '-0.04em', color: L.paper, fontVariantNumeric: 'tabular-nums' }}>
              <CountUp value={n.value} duration={1400 + i * 200} />
            </div>
            <div className="mt-4" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 16, color: L.paper }}>{n.label}</div>
            <div className="mt-1" style={{ fontFamily: FONT.sans, fontSize: 13, color: 'rgba(255,255,255,0.62)', lineHeight: 1.45, maxWidth: '26ch' }}>{n.note}</div>
          </Reveal>
        ))}
      </div>
    </Container>
  </section>
);

export default Numbers;
