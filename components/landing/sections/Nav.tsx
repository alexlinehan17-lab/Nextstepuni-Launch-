/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Top bar. Starguy sits left of the wordmark, the way HappyStack seats its
 * mascot. Links are plain text; the active section gets an ink underline.
 * One orange CTA, present at every width so the sticky bar always carries the
 * conversion action. On phones the links fold into a text "Menu" toggle.
 */

import React, { useEffect, useState } from 'react';
import { COPY } from '../copy';
import { Button, Container, Starguy, Wordmark } from '../primitives';
import { APP_SIGNIN_URL, APP_URL, FONT, L } from '../theme';

const Nav: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState<string>('');
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const ids = COPY.nav.links.map(l => l.href.replace('#', ''));
    const els = ids.map(id => document.getElementById(id)).filter((e): e is HTMLElement => Boolean(e));
    if (els.length === 0) return;
    const io = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) setActive(`#${visible[0].target.id}`);
    }, { rootMargin: '-35% 0px -55% 0px', threshold: [0, 0.2, 0.5] });
    els.forEach(el => io.observe(el));
    const onScroll = () => setScrolled(window.scrollY > 8);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => { io.disconnect(); window.removeEventListener('scroll', onScroll); };
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
          display: big ? 'block' : 'inline-block', transition: 'border-color 120ms ease',
        }}
      >
        {l.label}
      </a>
    );
  };

  return (
    <header
      style={{ position: 'sticky', top: 0, zIndex: 50, background: 'rgba(255,255,255,0.92)', backdropFilter: 'saturate(1.2) blur(10px)', WebkitBackdropFilter: 'saturate(1.2) blur(10px)', borderBottom: `1px solid ${scrolled ? L.hairline : 'transparent'}`, transition: 'border-color 160ms ease' }}
    >
      <Container className="flex items-center justify-between gap-3" style={{ height: 68 }}>
        <a href="#top" aria-label={`${COPY.brand.name} home`} className="flex items-center gap-2 md:gap-2.5 shrink-0" style={{ textDecoration: 'none' }}>
          {/* Two sizes, one per breakpoint, so the row still fits at 340px without a resize listener. */}
          <Starguy size={30} className="md:hidden" />
          <Starguy size={34} className="hidden md:block" />
          <Wordmark size={20} className="md:hidden" />
          <Wordmark size={23} className="hidden md:inline" />
        </a>

        <nav aria-label="Primary" className="hidden md:flex items-center gap-7">
          {COPY.nav.links.map(l => link(l))}
        </nav>

        <div className="flex items-center gap-3 shrink-0">
          <a href={APP_SIGNIN_URL} className="hidden md:inline-block" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 15, color: L.ink, textDecoration: 'none', padding: '6px 2px' }}>{COPY.nav.signIn}</a>
          <span className="hidden md:inline-block"><Button href={APP_URL} size="md">{COPY.nav.cta}</Button></span>
          <span className="md:hidden inline-block"><Button href={APP_URL} size="sm" ariaLabel={COPY.nav.cta}>{COPY.nav.ctaShort}</Button></span>
          <button
            type="button"
            className="md:hidden"
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
        <div id="landing-mobile-menu" className="md:hidden" style={{ borderTop: `1px solid ${L.hairline}`, background: L.paper }}>
          <Container style={{ paddingTop: 6, paddingBottom: 18 }}>
            {COPY.nav.links.map(l => link(l, true))}
            <a href={APP_SIGNIN_URL} style={{ display: 'block', fontFamily: FONT.sans, fontWeight: 600, fontSize: 22, color: L.ink, textDecoration: 'none', padding: '14px 0' }}>{COPY.nav.signIn}</a>
            <div className="pt-4"><Button href={APP_URL} size="lg" className="w-full">{COPY.nav.cta}</Button></div>
          </Container>
        </div>
      )}
    </header>
  );
};

export default Nav;
