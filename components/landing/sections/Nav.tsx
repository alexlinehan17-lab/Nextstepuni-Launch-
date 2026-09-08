/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Top bar. Starguy sits left of the wordmark, the way HappyStack seats its
 * mascot. Links are plain text; the active section gets an ink underline.
 * One orange CTA, present at every width so the sticky bar always carries the
 * conversion action. Below 1024px — where four links, sign-in and the CTA no
 * longer fit on one line — the links fold into a text "Menu" toggle.
 *
 * The bar has two states. At rest it is open type on the white canvas; once
 * the hero headline has passed beneath it, `data-condensed` tightens the
 * padding (never the height), drops the wordmark an optical size and draws a
 * hairline under it — all in fx-foundation/foundation.css. An
 * IntersectionObserver on the headline flips the state; there is no scroll
 * listener and no blur.
 *
 * While the bar is condensed and no slot on the page claims starguy, he
 * stands under its bottom-left corner holding it up (starguy/Traveller.tsx
 * sets `data-guest` while he is on his way or there, `data-held` once he has
 * arrived, and `--sg-x` on the header). One of him at a time: the lockup's
 * copy fades while he is the guest. The two elements at the end of the
 * header draw the hold: the hairline with a gap over his head, and a short
 * sag in the gap. Both are display:none otherwise (fx-char/fx-char.css).
 */

import React, { useEffect, useState } from 'react';
import { COPY } from '../copy';
import { Button, Container, Starguy, Wordmark } from '../primitives';
import { APP_SIGNIN_URL, APP_URL, FONT, L } from '../theme';

/**
 * The bar's resting height: the row's 42px content plus 21px of padding each
 * side (foundation.css). Condensed it is 68px, which the sticky chapter strip
 * and every scroll-margin below assume.
 */
const RESTING_HEIGHT = 84;

const Nav: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState<string>('');
  const [condensed, setCondensed] = useState(false);

  useEffect(() => {
    const ids = COPY.nav.links.map(l => l.href.replace('#', ''));
    const els = ids.map(id => document.getElementById(id)).filter((e): e is HTMLElement => Boolean(e));
    if (els.length === 0) return;
    const io = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) setActive(`#${visible[0].target.id}`);
    }, { rootMargin: '-35% 0px -55% 0px', threshold: [0, 0.2, 0.5] });
    els.forEach(el => io.observe(el));
    return () => io.disconnect();
  }, []);

  // Condense once the hero headline is wholly above the resting bar; relax
  // when it comes back. The resting height is the margin on both legs, so the
  // state cannot flap while the bar itself is changing size.
  useEffect(() => {
    const sentinel = document.querySelector<HTMLElement>('.landing-hero-title');
    if (!sentinel || typeof IntersectionObserver === 'undefined') {
      const onScroll = () => setCondensed(window.scrollY > RESTING_HEIGHT);
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
      return () => window.removeEventListener('scroll', onScroll);
    }
    const io = new IntersectionObserver(([entry]) => {
      setCondensed(!entry.isIntersecting && entry.boundingClientRect.bottom < RESTING_HEIGHT);
    }, { rootMargin: `-${RESTING_HEIGHT}px 0px 0px 0px`, threshold: 0 });
    io.observe(sentinel);
    return () => io.disconnect();
  }, []);

  const link = (l: { label: string; href: string }, big = false) => {
    const on = active === l.href;
    return (
      <a
        key={l.href}
        href={l.href}
        onClick={() => setOpen(false)}
        aria-current={on ? 'true' : undefined}
        style={{
          fontFamily: FONT.sans, fontWeight: on ? 700 : 500, fontSize: big ? 22 : 15, color: L.ink, textDecoration: 'none',
          padding: big ? '14px 0' : '6px 2px', borderBottom: big ? `1px solid ${L.hairline}` : `2px solid ${on ? L.ink : 'transparent'}`,
          display: big ? 'block' : 'inline-block', whiteSpace: 'nowrap', transition: 'border-color 120ms ease',
        }}
      >
        {l.label}
      </a>
    );
  };

  return (
    <header className="landing-nav" data-condensed={condensed ? 'true' : 'false'}>
      <Container className="landing-nav-row flex items-center justify-between gap-3">
        <a href="#top" aria-label={`${COPY.brand.name} home`} className="flex items-center gap-2 md:gap-2.5 shrink-0" style={{ textDecoration: 'none' }}>
          {/* Two sizes, one per breakpoint, so the row still fits at 340px without a resize listener. */}
          <Starguy size={30} className="md:hidden landing-nav-guy" />
          <Starguy size={34} className="hidden md:block landing-nav-guy" />
          {/* Sized by the stylesheet, so the condensed state can change its size and optical cut. */}
          <Wordmark className="landing-nav-mark" />
        </a>

        <nav aria-label="Primary" className="hidden lg:flex items-center gap-7">
          {COPY.nav.links.map(l => link(l))}
        </nav>

        <div className="flex items-center gap-3 shrink-0">
          <a href={APP_SIGNIN_URL} className="hidden lg:inline-block" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 15, color: L.ink, textDecoration: 'none', padding: '6px 2px' }}>{COPY.nav.signIn}</a>
          <span className="hidden lg:inline-block"><Button href={APP_URL} size="md">{COPY.nav.cta}</Button></span>
          <span className="lg:hidden inline-block"><Button href={APP_URL} size="sm" ariaLabel={COPY.nav.cta}>{COPY.nav.ctaShort}</Button></span>
          <button
            type="button"
            className="lg:hidden"
            aria-expanded={open}
            aria-controls="landing-mobile-menu"
            onClick={() => setOpen(o => !o)}
            style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 15, color: L.ink, background: 'none', border: 0, padding: '8px 2px', cursor: 'pointer', borderBottom: `2px solid ${open ? L.ink : 'transparent'}` }}
          >
            {open ? COPY.nav.close : COPY.nav.menu}
          </button>
        </div>
      </Container>

      {open && (
        <div id="landing-mobile-menu" className="lg:hidden" style={{ borderTop: `1px solid ${L.hairline}`, background: L.paper }}>
          <Container style={{ paddingTop: 6, paddingBottom: 18 }}>
            {COPY.nav.links.map(l => link(l, true))}
            <a href={APP_SIGNIN_URL} style={{ display: 'block', fontFamily: FONT.sans, fontWeight: 600, fontSize: 22, color: L.ink, textDecoration: 'none', padding: '14px 0' }}>{COPY.nav.signIn}</a>
            <div className="pt-4"><Button href={APP_URL} size="lg" className="w-full">{COPY.nav.cta}</Button></div>
          </Container>
        </div>
      )}
      <span className="fx-nav-line" aria-hidden="true" />
      <svg className="fx-nav-dip" viewBox="0 0 48 8" aria-hidden="true" focusable="false">
        <path d="M0 0.5 C 13 0.5 16 6.5 24 6.5 S 35 0.5 48 0.5" fill="none" stroke="rgba(26, 26, 26, 0.14)" strokeWidth="1" />
      </svg>
    </header>
  );
};

export default Nav;
