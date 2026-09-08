/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Landing-page primitives. Everything on the marketing page is built from
 * these so the page reads as one system: mono eyebrows, serif display,
 * ink hairlines, one orange. No pills, no chips, no tinted cards.
 */

import React from 'react';
import { FONT, L } from './theme';
import './fx-foundation/foundation.css';

export const Container: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className = '', children, ...rest }) => (
  <div className={`mx-auto w-full max-w-[1200px] px-5 sm:px-8 ${className}`} {...rest}>{children}</div>
);

/** Mono uppercase label. Optional Roman numeral prints in orange before the text. */
export const Eyebrow: React.FC<{ numeral?: string; children: React.ReactNode; className?: string; as?: 'div' | 'span' | 'p' }> = ({ numeral, children, className = '', as = 'div' }) => {
  const Tag = as;
  return (
    <Tag
      className={`flex items-center gap-3 uppercase ${className}`}
      style={{ fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.16em', color: L.faint, lineHeight: 1 }}
    >
      {numeral && <span className="landing-numeral" style={{ color: L.orangeText, fontFamily: FONT.serif, fontSize: 13, letterSpacing: '0.04em', fontWeight: 600 }}>{numeral}</span>}
      <span>{children}</span>
    </Tag>
  );
};

type DisplaySize = 'hero' | 'chapter' | 'section' | 'sub';
export const DISPLAY: Record<DisplaySize, React.CSSProperties> = {
  hero: { fontSize: 'clamp(42px, 7.2vw, 92px)', lineHeight: 0.98, letterSpacing: '-0.025em' },
  chapter: { fontSize: 'clamp(56px, 12vw, 172px)', lineHeight: 0.9, letterSpacing: '-0.035em' },
  section: { fontSize: 'clamp(30px, 4.4vw, 52px)', lineHeight: 1.04, letterSpacing: '-0.02em' },
  sub: { fontSize: 'clamp(22px, 2.6vw, 30px)', lineHeight: 1.15, letterSpacing: '-0.012em' },
};

/** Serif display type. Source Serif 4 at 600, tight, ink. */
export const Display: React.FC<{
  size?: DisplaySize;
  as?: 'h1' | 'h2' | 'h3' | 'p' | 'div';
  className?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
  id?: string;
}> = ({ size = 'section', as = 'h2', className = '', style, children, id }) => {
  const Tag = as;
  return (
    <Tag id={id} className={className} style={{ fontFamily: FONT.serif, fontWeight: 600, color: L.ink, margin: 0, ...DISPLAY[size], ...style }}>
      {children}
    </Tag>
  );
};

/**
 * Italic serif lede that opens on a two-line sunk drop cap — the Editions
 * "Insights, proactively delivered" move, set the way a chapter opening is set.
 * The cap is CSS (::first-letter + initial-letter, a float where the browser
 * has none) so the text stays one string for screen readers and the drop-cap
 * size follows the line count rather than a guessed em. Browsers skip
 * text-wrap: balance on a paragraph with an initial letter, so the last two
 * words are joined with a no-break space instead — a display line never ends
 * on a single word — and the size tops out at 28px, which sets the chapters'
 * 270–325px column in two or three lines beside the cap.
 */
export const DropLine: React.FC<{ children: string; className?: string }> = ({ children, className = '' }) => (
  <p className={`landing-dropline ${className}`} style={{ fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 400, color: L.ink, fontSize: 'clamp(22px, 2.8vw, 28px)', lineHeight: 1.15, margin: 0, letterSpacing: '-0.01em' }}>
    {children.replace(/ (\S+)$/, ' $1')}
  </p>
);

export const Lede: React.FC<{ children: React.ReactNode; className?: string; style?: React.CSSProperties }> = ({ children, className = '', style }) => (
  <p className={`landing-lede landing-prose ${className}`} style={{ fontFamily: FONT.sans, fontSize: 'clamp(16px, 1.35vw, 19px)', lineHeight: 1.55, color: L.muted, margin: 0, maxWidth: '52ch', ...style }}>{children}</p>
);

/** Running copy. Its line-height and margin live in the stylesheet so ruled variants can put it on the grid. */
export const Body: React.FC<{ children: React.ReactNode; className?: string; style?: React.CSSProperties }> = ({ children, className = '', style }) => (
  <p className={`landing-body landing-prose ${className}`} style={{ fontFamily: FONT.sans, fontSize: 15, color: L.muted, ...style }}>{children}</p>
);

type ButtonVariant = 'primary' | 'secondary' | 'ink' | 'ghost';
interface ButtonProps {
  variant?: ButtonVariant;
  href?: string;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  ariaLabel?: string;
}

/**
 * Buttons. Primary is the app's chunky CTA family: orange fill, ink edge, hard
 * 3px offset shadow that collapses on press — reserved for the one conversion
 * action per view. Ink is the same shape filled ink, for actions INSIDE a demo
 * (next card, mark done) so orange stays rare. Secondary is paper. Ghost is an
 * ink text link with an arrow. The shadow and the press physics are in
 * fx-foundation/foundation.css (.landing-btn), not inline, so :hover and
 * :active can change them.
 */
export const Button: React.FC<ButtonProps> = ({ variant = 'primary', href, onClick, children, className = '', size = 'md', ariaLabel }) => {
  const pad = size === 'lg' ? '15px 28px' : size === 'sm' ? '9px 14px' : '12px 22px';
  const fontSize = size === 'lg' ? 16 : size === 'sm' ? 14 : 15;
  if (variant === 'ghost') {
    const ghostStyle: React.CSSProperties = { fontFamily: FONT.sans, fontWeight: 600, fontSize, color: L.ink, textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: 8, padding: '10px 4px', borderBottom: `1.5px solid ${L.ink}` };
    return href
      ? <a href={href} onClick={onClick} className={`landing-ghost ${className}`} style={ghostStyle} aria-label={ariaLabel}>{children}<span aria-hidden="true">→</span></a>
      : <button type="button" onClick={onClick} className={`landing-ghost ${className}`} style={{ ...ghostStyle, background: 'none', cursor: 'pointer' }} aria-label={ariaLabel}>{children}<span aria-hidden="true">→</span></button>;
  }
  const primary = variant === 'primary';
  const ink = variant === 'ink';
  const style: React.CSSProperties = {
    fontFamily: FONT.sans, fontWeight: 600, fontSize, lineHeight: 1,
    color: primary || ink ? '#FFFFFF' : L.ink,
    background: primary ? L.orange : ink ? L.ink : L.paper,
    border: `1.5px solid ${L.ink}`,
    borderRadius: 999,
    padding: pad,
    textDecoration: 'none',
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: 10,
    cursor: 'pointer',
  };
  const cls = `landing-btn ${className}`;
  return href
    ? <a href={href} onClick={onClick} className={cls} style={style} aria-label={ariaLabel}>{children}</a>
    : <button type="button" onClick={onClick} className={cls} style={style} aria-label={ariaLabel}>{children}</button>;
};

/** White card with a 1.5px ink edge. Optional mono title bar (left) and meta (right) make it read as a window without any chrome. */
export const Frame: React.FC<{
  children: React.ReactNode;
  title?: string;
  meta?: string;
  className?: string;
  style?: React.CSSProperties;
  radius?: number;
  padded?: boolean;
}> = ({ children, title, meta, className = '', style, radius = 18, padded = false }) => (
  <div className={className} style={{ background: L.paper, border: `1.5px solid ${L.edge}`, borderRadius: radius, overflow: 'hidden', ...style }}>
    {(title || meta) && (
      <div className="flex items-center justify-between gap-4" style={{ padding: '10px 14px', borderBottom: `1px solid ${L.hairline}`, fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint }}>
        <span>{title}</span>
        {meta && <span style={{ color: L.orangeText }}>{meta}</span>}
      </div>
    )}
    <div style={padded ? { padding: 20 } : undefined}>{children}</div>
  </div>
);

export const Rule: React.FC<{ className?: string; strong?: boolean }> = ({ className = '', strong = false }) => (
  <hr className={`landing-rule my-0 mx-0 ${className}`} style={{ border: 0, height: strong ? 1.5 : 1, background: strong ? L.ink : L.hairline, transformOrigin: 'left center' }} />
);

/**
 * The 1.5px ink rule along a section's top edge, drawn from the left as the
 * reader scrolls to it (CSS scroll-driven animation; a static line where the
 * browser cannot). The section supplies `position: relative`.
 */
export const SectionRule: React.FC<{ strong?: boolean }> = ({ strong = true }) => (
  <span aria-hidden="true" className="landing-rule" style={{ position: 'absolute', left: 0, right: 0, top: 0, height: strong ? 1.5 : 1, background: strong ? L.ink : L.hairline, transformOrigin: 'left center', display: 'block' }} />
);

/**
 * Starguy — the website's one character. Transparent PNG, tight-cropped, and
 * never rotated: he is a figure standing on a star, so a tilt reads as toppling.
 * Placement rule everywhere: his star sits on the baseline of the word he
 * belongs to, at roughly 0.55–0.7em of that word, and he is hidden when he
 * would render smaller than ~44px.
 */
export const Starguy: React.FC<{ size?: number; pose?: 'stand' | 'hang' | 'lean'; className?: string; style?: React.CSSProperties; alt?: string }> = ({ size = 48, className = '', style, alt = '' }) => (
  <img
    src="/assets/landing/starguy-512.png"
    width={size}
    height={Math.round(size * 1.158)}
    alt={alt}
    aria-hidden={alt ? undefined : true}
    draggable={false}
    className={`block ${className}`}
    style={{ userSelect: 'none', ...style }}
  />
);

/** The wordmark: DM Sans Bold, tight, lowercase — matched against the brand sheet. Leave `size` off to size it from a stylesheet. */
export const Wordmark: React.FC<{ size?: number; className?: string }> = ({ size, className = '' }) => (
  <span className={className} style={{ fontFamily: FONT.sans, fontWeight: 700, fontSize: size, letterSpacing: '-0.03em', color: L.ink, lineHeight: 1 }}>nextstepuni</span>
);

/** Text tabs on a hairline with an ink underline on the active one. No pills. */
export const TextTabs: React.FC<{
  items: { id: string; label: string }[];
  active: string;
  onChange: (id: string) => void;
  size?: 'md' | 'sm';
  ariaLabel: string;
  className?: string;
}> = ({ items, active, onChange, size = 'md', ariaLabel, className = '' }) => (
  <div className="landing-tabs-wrap relative min-w-0">
  <div role="tablist" aria-label={ariaLabel} className={`flex gap-1 overflow-x-auto ${className}`} style={{ boxShadow: `inset 0 -1px 0 ${L.hairline}`, scrollbarWidth: 'none' }}>
    {items.map(t => {
      const on = t.id === active;
      return (
        <button
          key={t.id}
          role="tab"
          type="button"
          aria-selected={on}
          onClick={() => onChange(t.id)}
          className={`landing-tab shrink-0 ${size === 'md' ? 'landing-tab-md' : 'landing-tab-sm'}`}
          style={{
            fontFamily: FONT.sans, fontWeight: on ? 700 : 500, fontSize: size === 'md' ? 15 : 13,
            color: on ? L.ink : L.muted, background: 'none', border: 0, cursor: 'pointer',
            padding: size === 'md' ? '12px 14px' : '10px 12px',
            borderBottom: `2px solid ${on ? L.ink : 'transparent'}`,
            transition: 'color 120ms ease',
          }}
        >
          {t.label}
        </button>
      );
    })}
  </div>
  <span aria-hidden="true" className="landing-tabs-fade" />
  </div>
);
