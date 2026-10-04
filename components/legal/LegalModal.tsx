/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useId, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import { AnimatePresence, MotionDiv, useReducedMotion } from '../Motion';
import { useModal } from '../../hooks/useModal';
import {
  type LegalDoc,
  LEGAL_TITLES,
  PRIVACY_POLICY_VERSION,
  LEGAL_LAST_UPDATED,
  LEGAL_URL_RE,
  SUPPORT_EMAIL,
} from './legalContent';
import { LEGAL_DRAFT_NOTE, legalBlocks, legalSections, legalSectionId, legalSectionNumber } from './legalPresentation';
import './legal-document.css';

// Keep existing registration/settings import paths and consent version stable.
export { PRIVACY_POLICY_VERSION, LEGAL_LAST_UPDATED, SUPPORT_EMAIL, CONSENT_BASIS } from './legalContent';
export type { LegalDoc } from './legalContent';

interface LegalModalProps {
  doc: LegalDoc | null;
  onClose: () => void;
  onDocumentChange?: (doc: LegalDoc) => void;
}

function withLinks(line: string): React.ReactNode[] {
  LEGAL_URL_RE.lastIndex = 0;
  return line.split(LEGAL_URL_RE).map((part, index) => index % 2 === 1
    ? <a key={index} href={part} target="_blank" rel="noopener noreferrer">{part}</a>
    : part);
}

function LegalReader({ doc, titleId, onDocumentChange }: {
  doc: LegalDoc;
  titleId: string;
  onDocumentChange?: (doc: LegalDoc) => void;
}) {
  const sections = legalSections(doc);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [activeSection, setActiveSection] = useState(0);
  const reducedMotion = useReducedMotion();

  useLayoutEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = 0;
    setActiveSection(0);
  }, [doc]);

  const jumpToSection = (event: React.MouseEvent<HTMLAnchorElement>, index: number) => {
    event.preventDefault();
    event.currentTarget.closest('details')?.removeAttribute('open');
    const heading = scrollRef.current?.querySelector<HTMLElement>(`#${legalSectionId(doc, index)}`);
    heading?.scrollIntoView({ behavior: reducedMotion ? 'instant' : 'smooth', block: 'start' });
    heading?.focus({ preventScroll: true });
    setActiveSection(index);
  };

  const updateActiveSection = () => {
    const scroll = scrollRef.current;
    if (!scroll) return;
    const boundary = scroll.getBoundingClientRect().top + 60;
    const headings = Array.from(scroll.querySelectorAll<HTMLElement>('.legal-section h3'));
    let current = 0;
    headings.forEach((heading, index) => { if (heading.getBoundingClientRect().top <= boundary) current = index; });
    setActiveSection(current);
  };

  const contents = (
    <ol>
      {sections.map((section, index) => (
        <li key={section.heading}>
          <a href={`#${legalSectionId(doc, index)}`} onClick={event => jumpToSection(event, index)} aria-current={activeSection === index ? 'location' : undefined}>
            <span aria-hidden="true">{legalSectionNumber(index)}</span><span>{section.heading}</span>
          </a>
        </li>
      ))}
    </ol>
  );

  return (
    <div className="legal-scroll" ref={scrollRef} onScroll={updateActiveSection}>
      <header className="legal-hero">
        {onDocumentChange && (
          <nav className="legal-switcher" aria-label="Legal documents">
            {(['privacy', 'terms'] as const).map(document => (
              <button key={document} type="button" aria-pressed={doc === document} onClick={() => onDocumentChange(document)}>{LEGAL_TITLES[document]}</button>
            ))}
          </nav>
        )}
        <h2 className="legal-title" id={titleId}>{LEGAL_TITLES[doc]}<span aria-hidden="true">.</span></h2>
        <dl className="legal-meta">
          <div><dt className="legal-label">Last updated</dt><dd>{LEGAL_LAST_UPDATED}</dd></div>
          <div><dt className="legal-label">Version</dt><dd>{PRIVACY_POLICY_VERSION}</dd></div>
        </dl>
        <p className="legal-draft">{LEGAL_DRAFT_NOTE}</p>
      </header>
      <div className="legal-layout">
        <aside className="legal-contents legal-contents-desktop">
          <nav aria-label="On this page"><p className="legal-label">On this page</p>{contents}</nav>
        </aside>
        <details className="legal-contents legal-contents-mobile">
          <summary>Jump to a section</summary>
          <nav aria-label="On this page">{contents}</nav>
        </details>
        <div className="legal-reader">
          {sections.map((section, index) => (
            <section key={section.heading} className="legal-section" aria-labelledby={legalSectionId(doc, index)}>
              <div className="legal-section-header">
                <span className="legal-section-number" aria-hidden="true">{legalSectionNumber(index)}</span>
                <h3 id={legalSectionId(doc, index)} tabIndex={-1}>{section.heading}</h3>
              </div>
              <div className="legal-copy">
                {legalBlocks(section.body).map((block, blockIndex) => block.type === 'paragraph'
                  ? <p key={blockIndex}>{withLinks(block.text)}</p>
                  : <ul key={blockIndex}>{block.items.map((item, itemIndex) => <li key={itemIndex}>{withLinks(item)}</li>)}</ul>)}
              </div>
            </section>
          ))}
        </div>
      </div>
      <footer className="legal-footer">
        <div><p>Questions? Contact <a href={`mailto:${SUPPORT_EMAIL}`}>{SUPPORT_EMAIL}</a>.</p><p>NextStepUni Ltd</p></div>
        <div className="legal-footer-links"><a href={`/${doc}.html`} target="_blank" rel="noopener noreferrer">Open full page ↗</a></div>
      </footer>
    </div>
  );
}

/** The registration and settings reader shares the public documents' typography and copy. */
export const LegalModal: React.FC<LegalModalProps> = ({ doc, onClose, onDocumentChange }) => {
  const dialogRef = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const reducedMotion = useReducedMotion();
  useModal(!!doc, onClose, dialogRef, { initialFocus: 'dialog' });

  return createPortal(
    <AnimatePresence>
      {doc && (
        <MotionDiv
          key="legal-backdrop"
          className="legal-backdrop"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: reducedMotion ? 0 : 0.2 }}
          onClick={onClose}
        >
          <MotionDiv
            ref={dialogRef} role="dialog" aria-modal="true" aria-labelledby={titleId} tabIndex={-1}
            className="legal-document legal-dialog"
            initial={{ opacity: 0, y: reducedMotion ? 0 : 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: reducedMotion ? 0 : 8 }}
            transition={{ duration: reducedMotion ? 0 : 0.25, ease: [0.22, 1, 0.36, 1] }}
            onClick={(event: React.MouseEvent) => event.stopPropagation()}
          >
            <div className="legal-masthead">
              <p className="legal-wordmark">NextStep<span>Uni</span></p>
              <button className="legal-close" type="button" aria-label="Close legal document" onClick={onClose}><X size={18} strokeWidth={1.6} /></button>
            </div>
            <LegalReader doc={doc} titleId={titleId} onDocumentChange={onDocumentChange} />
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default LegalModal;
