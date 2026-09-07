/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Numbers as identity: a hairline-divided strip of serif tabular numerals.
 * Every figure is computed from repo data (see demoData.ts header).
 */

import React from 'react';
import { COPY } from '../copy';
import { Reveal } from '../motion';
import { Container, Eyebrow } from '../primitives';
import { FONT, L } from '../theme';

const Numbers: React.FC = () => (
  <section aria-label={COPY.numbers.eyebrow} style={{ borderTop: `1.5px solid ${L.ink}`, borderBottom: `1.5px solid ${L.ink}` }}>
    <Container>
      <div className="grid grid-cols-2 lg:grid-cols-4">
        {COPY.numbers.items.map((n, i) => (
          <Reveal key={n.label} delay={i * 0.06} className={`py-7 md:py-9 pr-4 ${i % 2 === 1 ? 'pl-5' : ''} ${i >= 2 ? 'lg:pl-5' : ''}`} style={{ borderLeft: i % 2 === 1 ? `1px solid ${L.hairline}` : undefined, borderTop: i >= 2 ? `1px solid ${L.hairline}` : undefined }}>
            <div style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 'clamp(36px, 4.6vw, 60px)', lineHeight: 1, letterSpacing: '-0.03em', color: L.ink, fontVariantNumeric: 'tabular-nums' }}>{n.value}</div>
            <div className="mt-2" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 15, color: L.ink }}>{n.label}</div>
            <div className="mt-1" style={{ fontFamily: FONT.sans, fontSize: 13, color: L.faint, lineHeight: 1.4 }}>{n.note}</div>
          </Reveal>
        ))}
      </div>
    </Container>
    <span className="sr-only"><Eyebrow>{COPY.numbers.eyebrow}</Eyebrow></span>
  </section>
);

export default Numbers;
