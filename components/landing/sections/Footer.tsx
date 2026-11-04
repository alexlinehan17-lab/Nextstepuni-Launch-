/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Footer: the brand statement as a caption, then the giant wordmark as a
 * section break (Leonardo / Hermes), then the small print with /privacy,
 * /terms, sign in and a mailto.
 *
 * It is the floor the page lifts off. The footer is pinned to the bottom of
 * the window beneath the opaque main (fx.css, .fx-floor) and shows as the
 * last section scrolls away. Everything that moves in here runs off that
 * reveal, measured by useFloorReveal: the line under the statement draws,
 * the brand caption sits at its right end, the statement
 * rises once the sheet has lifted a little, and the character's footer slot
 * only exists once the sheet has cleared the line — so he lands on it the
 * moment the floor is there. The page's own view-timeline rules would stick
 * in a pinned footer, so the rules here are plain.
 */

import React, { useRef } from 'react';
import { COPY } from '../copy';
import { Container, DISPLAY, Starguy } from '../primitives';
import { LineRise } from '../motion';
import { StarguySlot, useTravellerLive } from '../starguy/Traveller';
import { FONT, L } from '../theme';
import { FooterLine } from '../fx/FooterLine';
import { useFloorReveal } from '../fx/floor';
import '../fx/fx.css';

const Footer: React.FC = () => {
  const ref = useRef<HTMLElement>(null);
  const lineRef = useRef<SVGSVGElement>(null);
  const live = useTravellerLive();
  const { progress, cleared, revealed } = useFloorReveal(ref, lineRef);
  // While the traveller is live his slot has no width until the sheet has cleared the line, so he cannot arrive early.
  const slotWidth = live && !cleared ? 0 : 56;
  return (
    <footer id="landing-footer" ref={ref} className="fx-floor" style={{ overflow: 'hidden' }}>
      <Container className="pt-14 md:pt-20">
        <div className="landing-footer-statement-row">
          {/* items-baseline: the image's bottom edge is its flex baseline, so the star lands on the word's baseline. */}
          <LineRise
            as="p"
            when={revealed}
            padTop="1.3em"
            text={COPY.footer.statement}
            className="m-0"
            style={{ fontFamily: FONT.serif, fontWeight: 600, color: L.ink, ...DISPLAY.sub }}
            tail={
              <span aria-hidden="true" style={{ position: 'absolute', left: 'calc(100% + 0.35em)', bottom: 0, width: slotWidth, lineHeight: 0 }}>
                <StarguySlot id="footer"><Starguy size={0} pose="stand" style={{ width: '100%', height: 'auto' }} /></StarguySlot>
              </span>
            }
          />
          <p className="landing-footer-caption">{COPY.footer.caption}</p>
        </div>
        <FooterLine ref={lineRef} progress={progress} />
        {/*
          The wordmark as a section break. Sized against its own container
          (container query units, not the viewport): DM Sans 700 'nextstepuni' at
          -0.05em tracking is ≈5.75em wide, so 100cqw / 5.75 ≈ 17.4cqw keeps the
          final i just inside the edge at every width. Sliced at 0.74em so it
          bleeds into the rule beneath.
        */}
        <div className="mt-2 md:mt-4" aria-hidden="true" style={{ containerType: 'inline-size' }}>
          <div style={{ height: '0.74em', overflow: 'hidden', fontSize: 'min(220px, 17.4cqw)' }}>
            <div style={{ fontFamily: FONT.sans, fontWeight: 700, fontSize: '1em', letterSpacing: '-0.05em', lineHeight: 1, color: L.ink, whiteSpace: 'nowrap', marginTop: '-0.1em' }}>nextstepuni</div>
          </div>
        </div>
      </Container>
      <div style={{ position: 'relative' }}>
        <span aria-hidden="true" className="fx-floor-rule" />
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
};

export default Footer;
