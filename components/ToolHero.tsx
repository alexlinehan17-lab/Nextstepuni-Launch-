import React from 'react';
import { ToolArtwork, type ToolArtworkKey } from './ToolIconBlob';
import './toolHero.css';

interface ToolHeroProps {
  toolId: ToolArtworkKey;
  eyebrow: string;
  title: string;
  subtitle: React.ReactNode;
  className?: string;
  headingRef?: React.Ref<HTMLHeadingElement>;
  /** Keep the archive's approved two-line wordmark on wider screens too. */
  archiveTitle?: boolean;
}

/** Approved Launchpad entry card. Working screens own their compact navigation. */
export function ToolHero({ toolId, eyebrow, title, subtitle, className = '', archiveTitle = false, headingRef }: ToolHeroProps) {
  const compactTitle = title.length > 22 || title.split(/\s+/).some(word => word.length >= 8);
  return (
    <header className={`tool-hero ${className}`}>
      <p className="tool-hero__eyebrow">{eyebrow}</p>
      <div className="tool-hero__identity">
        <h1 ref={headingRef} tabIndex={headingRef ? -1 : undefined} className={`tool-hero__title ${compactTitle ? 'tool-hero__title--long' : ''}`}>
          {archiveTitle ? <>Paper<br />Trail<span aria-hidden="true">.</span></> : title}
        </h1>
        <div className="tool-hero__art" aria-hidden="true">
          <ToolArtwork toolId={toolId} onDark />
        </div>
      </div>
      <p className="tool-hero__subtitle">{subtitle}</p>
    </header>
  );
}
