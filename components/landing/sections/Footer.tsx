/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Footer: the brand statement as a caption, then the giant wordmark as a
 * section break (Leonardo / Hermes), then the small print with /privacy,
 * /terms, sign in and a mailto.
 */

import React from 'react';
import { COPY } from '../copy';
import { Container, Display, Starguy } from '../primitives';
import { FONT, L } from '../theme';

const Footer: React.FC = () => (
  <footer style={{ borderTop: `1.5px solid ${L.ink}`, overflow: 'hidden' }}>
    <Container className="pt-14 md:pt-20">
      {/* items-baseline: the image's bottom edge is its flex baseline, so the star lands on the word's baseline. */}
      <div className="flex items-baseline gap-4">
        <Display as="p" size="sub">{COPY.footer.statement}</Display>
        <Starguy size={56} pose="stand" className="shrink-0" />
      </div>
      {/*
        The wordmark as a section break. Sized against its own container
        (container query units, not the viewport): DM Sans 700 'nextstepuni' at
        -0.05em tracking is ≈5.75em wide, so 100cqw / 5.75 ≈ 17.4cqw keeps the
        final i just inside the edge at every width. Sliced at 0.74em so it
        bleeds into the rule beneath.
      */}
      <div className="mt-10 md:mt-14" aria-hidden="true" style={{ containerType: 'inline-size' }}>
        <div style={{ height: '0.74em', overflow: 'hidden', fontSize: 'min(220px, 17.4cqw)' }}>
          <div style={{ fontFamily: FONT.sans, fontWeight: 700, fontSize: '1em', letterSpacing: '-0.05em', lineHeight: 1, color: L.ink, whiteSpace: 'nowrap', marginTop: '-0.1em' }}>nextstepuni</div>
        </div>
      </div>
    </Container>
    <div style={{ borderTop: `1.5px solid ${L.ink}` }}>
      <Container className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 py-5" style={{ fontFamily: FONT.sans, fontSize: 13, color: L.faint }}>
        <nav aria-label="Legal" className="flex flex-wrap gap-x-6 gap-y-2">
          {COPY.footer.links.map(l => <a key={l.href} href={l.href} style={{ color: L.ink, textDecoration: 'none', fontWeight: 600 }}>{l.label}</a>)}
          <a href={`mailto:${COPY.brand.supportEmail}`} style={{ color: L.ink, textDecoration: 'none', fontWeight: 600 }}>{COPY.footer.contact}</a>
        </nav>
        <span>{COPY.footer.small}</span>
      </Container>
    </div>
  </footer>
);

export default Footer;
