/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * KnowledgeModuleShell — shared wrapper for every Necessary Knowledge
 * module. Provides:
 *   - Breadcrumb back to the tab landing
 *   - Header (eyebrow + title + subtitle)
 *   - "Why this matters" expandable explainer (optional, prop-driven)
 *   - Module body (children)
 *   - "What you learned" summary card (optional)
 *   - Footer back-link
 *
 * Aesthetic register matches CAO Simulator / Strategiser: warm cream
 * panels, 1px #EDEBE8 borders, teal #2A7D6F accent.
 */

import React, { useState } from 'react';

const TEAL = '#2A7D6F';

interface Props {
  /** Module title shown in the header. */
  title: string;
  /** One-line subtitle / framing. */
  subtitle?: string;
  /** Short explainer (~150-200 words) shown in the "Why this matters" card. */
  whyThisMatters?: React.ReactNode;
  /** Default state for the why-card. Defaults to expanded. */
  whyDefaultOpen?: boolean;
  /** Optional summary text shown in the "What you learned" card after the body. */
  summary?: React.ReactNode;
  /** Called when the back-to-landing CTA is clicked. */
  onBackToLanding: () => void;
  /** The interactive module body. */
  children: React.ReactNode;
}

const KnowledgeModuleShell: React.FC<Props> = ({
  title,
  subtitle,
  whyThisMatters,
  whyDefaultOpen = true,
  summary,
  onBackToLanding,
  children,
}) => {
  return (
    <div className="space-y-6">
      <button
        type="button"
        onClick={onBackToLanding}
        className="font-sans flex items-center gap-1.5 transition-colors"
        style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
      >
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
          <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        Necessary Knowledge
      </button>

      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Necessary Knowledge
        </p>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: '#1A1A1A', marginTop: 4, lineHeight: 1.2 }}>
          {title}
        </h1>
        {subtitle && (
          <p className="font-sans max-w-xl" style={{ fontSize: 14, color: '#78716C', marginTop: 8, lineHeight: 1.55 }}>
            {subtitle}
          </p>
        )}
      </header>

      {whyThisMatters && <WhyThisMattersCard defaultOpen={whyDefaultOpen}>{whyThisMatters}</WhyThisMattersCard>}

      {children}

      {summary && (
        <section
          className="rounded-2xl"
          style={{
            backgroundColor: '#FAF7F4',
            border: `1px solid ${TEAL}33`,
            padding: '20px 24px',
          }}
        >
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
            What you just learned
          </p>
          <div className="font-sans" style={{ fontSize: 13.5, color: '#3F3B36', lineHeight: 1.6 }}>
            {summary}
          </div>
        </section>
      )}

      <div className="pt-2">
        <button
          type="button"
          onClick={onBackToLanding}
          className="font-sans rounded-full transition-colors"
          style={{
            backgroundColor: '#FFFFFF',
            color: TEAL,
            border: `1px solid ${TEAL}55`,
            padding: '9px 20px',
            fontSize: 13,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          ← Back to Necessary Knowledge
        </button>
      </div>
    </div>
  );
};

const WhyThisMattersCard: React.FC<{ defaultOpen: boolean; children: React.ReactNode }> = ({ defaultOpen, children }) => {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #EDEBE8',
      }}
    >
      <button
        type="button"
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between gap-3"
        style={{ padding: '14px 18px', cursor: 'pointer', background: 'transparent', border: 'none' }}
        aria-expanded={open}
      >
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Why this matters
        </p>
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          aria-hidden
          style={{ color: '#78716C', transform: open ? 'rotate(0deg)' : 'rotate(-90deg)', transition: 'transform 200ms ease' }}
        >
          <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      {open && (
        <div style={{ padding: '0 22px 22px 22px' }} className="font-sans" >
          <div style={{ fontSize: 13.5, color: '#3F3B36', lineHeight: 1.6 }}>
            {children}
          </div>
        </div>
      )}
    </section>
  );
};

export default KnowledgeModuleShell;
