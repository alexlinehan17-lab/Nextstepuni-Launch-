import React, { useId } from 'react';
import type { ToolIconKey } from '../ToolIconBlob';
import './launchpad.css';

/** Original tool artwork, with white ink on dark surfaces. No backing disc. */
export function ToolArtwork({
  tool,
  dark = false,
  className = '',
}: {
  tool: ToolIconKey;
  dark?: boolean;
  className?: string;
}) {
  const whiteInk =
    dark &&
    [
      'planner',
      'war-room',
      'catch-up-lane',
      'journey',
      'meet-tools',
      'future-finder',
    ].includes(tool);
  const filterId = `tool-ink-${useId().replace(/:/g, '')}`;
  const asset =
    tool === 'topic-atlas'
      ? 'paper-trail'
      : tool === 'cao-simulator'
        ? 'points-passport'
        : tool;
  return (
    <svg
      className={`lp-artwork ${className}`}
      viewBox="100 100 824 824"
      aria-hidden="true"
    >
      {whiteInk && (
        <defs>
          <filter id={filterId} colorInterpolationFilters="sRGB">
            <feColorMatrix
              in="SourceGraphic"
              type="matrix"
              values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  -4 0 0 0 1.5"
              result="whiteInk"
            />
            <feComposite
              in="whiteInk"
              in2="SourceGraphic"
              operator="in"
              result="ink"
            />
            <feMerge>
              <feMergeNode in="SourceGraphic" />
              <feMergeNode in="ink" />
            </feMerge>
          </filter>
        </defs>
      )}
      <image
        href={`/assets/tools/${asset}.png`}
        width="1024"
        height="1024"
        filter={whiteInk ? `url(#${filterId})` : undefined}
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
}: {
  tool: ToolIconKey;
  eyebrow: string;
  title: string;
  subtitle: string;
  children?: React.ReactNode;
  mascot?: boolean;
}) {
  return (
    <header className="lp-masthead">
      <div className="lp-masthead-copy">
        <p className="lp-eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p className="lp-masthead-subtitle">{subtitle}</p>
        {children}
      </div>
      {mascot ? (
        <img
          src="/assets/landing/starguy-512.png"
          alt=""
          className="lp-artwork lp-mascot"
        />
      ) : (
        <ToolArtwork tool={tool} dark />
      )}
    </header>
  );
}
