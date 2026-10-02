import React, { createContext, useContext, useEffect, useState } from 'react';
import { X } from 'lucide-react';
import type { ToolIconKey } from '../ToolIconBlob';
import ThemeArtwork from '../ThemeArtwork';
import './launchpad.css';

/** The mobile shell owns the introduction, so nested tools don't repeat it. */
export const ToolIntroductionContext = createContext(false);

export function ToolIntroduction({ tool, title, eyebrow, subtitle, uid }: {
  tool: ToolIconKey; title: string; eyebrow: string; subtitle: string; uid?: string;
}) {
  const key = `nsu:tool-introduction:v1:${uid ?? 'guest'}:${tool}`;
  const [open, setOpen] = useState(() => {
    try { return localStorage.getItem(key) !== 'seen'; } catch { return true; }
  });
  useEffect(() => {
    // Viewing once is enough, even if the student leaves without pressing X.
    try { localStorage.setItem(key, 'seen'); } catch { /* Storage may be unavailable. */ }
  }, [key]);
  return open ? <section className="lp-first-introduction" aria-label={`${title} introduction`}>
    <ToolMasthead headingAs="h2" tool={tool} title={title} eyebrow={eyebrow} subtitle={subtitle} />
    <button className="lp-introduction-close" type="button" aria-label={`Dismiss ${title} introduction`} onClick={() => setOpen(false)}><X size={18} /></button>
  </section> : null;
}

/** Original filled tool artwork; dark surfaces add a fine pale silhouette. */
export function ToolArtwork({
  tool,
  dark = false,
  className = '',
}: {
  tool: ToolIconKey;
  dark?: boolean;
  className?: string;
}) {
  const asset =
    tool === 'topic-atlas'
      ? 'paper-trail'
      : tool === 'cao-simulator'
        ? 'points-passport'
        : tool;
  return (
    <svg
      className={`lp-artwork theme-filled-art ${dark ? 'filled-art-on-dark' : ''} ${className}`}
      viewBox="100 100 824 824"
      aria-hidden="true"
    >
      <image
        href={`/assets/tools/${asset}.png`}
        width="1024"
        height="1024"
      />
    </svg>
  );
}

export default function ToolMasthead({
  tool,
  eyebrow,
  title,
  subtitle,
  children,
  mascot = false,
  headingAs: Heading = 'h1',
}: {
  tool: ToolIconKey;
  eyebrow: string;
  title: string;
  subtitle: string;
  children?: React.ReactNode;
  mascot?: boolean;
  headingAs?: 'h1' | 'h2';
}) {
  const introductionInShell = useContext(ToolIntroductionContext);
  if (introductionInShell) return children ? <>{children}</> : null;
  return (
    <header className="lp-masthead">
      <div className="lp-masthead-copy">
        <p className="lp-eyebrow">{eyebrow}</p>
        <Heading>{title}</Heading>
        <p className="lp-masthead-subtitle">{subtitle}</p>
        {children}
      </div>
      {mascot ? (
        <ThemeArtwork
          src="/assets/landing/starguy-512.png"
          alt=""
          darkSurface
          className="lp-artwork lp-mascot"
        />
      ) : (
        <ToolArtwork tool={tool} dark />
      )}
    </header>
  );
}
