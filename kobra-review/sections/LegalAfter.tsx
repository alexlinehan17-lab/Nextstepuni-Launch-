/**
 * The legal reader and the consent gate, rebuilt on Kobra (review section 05).
 *
 * Same words, order and documents as components/legal/LegalModal.tsx and
 * LegalAgreementGate.tsx: the copy is the real legalContent / legalPresentation
 * module, not a transcription. The reader is the runtime Dialog (opened from
 * the gate's "Read …" rows or "Open as a dialog"), with Privacy / Terms as the
 * house pill Tabs; the same reader also sits in place as a hairline card so
 * the page shows it without a click. The gate is a hairline card with square
 * ink Checkboxes and Kobra Buttons, in the house fonts (Source Serif 4 and
 * DM Sans; LegalDiatype, LegalMono and the green-grey legal inks are gone).
 *
 * "Jump to a section" (the narrow contents) is a <details> drawn as a hairline
 * disclosure: the Kobra Accordion needs compiling into the runtime.
 * Everything is local review state; Agree & continue records nothing.
 */
import React, { useId, useLayoutEffect, useRef, useState } from 'react';
import { AppWindow, ArrowUpRight, ChevronDown, X } from 'lucide-react';
import KobraScope, {
  Button, Checkbox, Dialog, DialogContent, DialogTitle, Tabs, TabsList, TabsTrigger, toast,
} from '../../components/approved-ui-runtime';
import {
  COMPANY_ADDRESS, COMPANY_NAME, COMPANY_NUMBER, LEGAL_LAST_UPDATED, LEGAL_TITLES, LEGAL_URL_RE,
  PRIVACY_POLICY_VERSION, SUPPORT_EMAIL, TERMS_VERSION, type LegalDoc,
} from '../../components/legal/legalContent';
import { LEGAL_DOCUMENT_NOTE, legalBlocks, legalSectionNumber, legalSections } from '../../components/legal/legalPresentation';
import './legal.css';

function withLinks(line: string): React.ReactNode[] {
  LEGAL_URL_RE.lastIndex = 0;
  return line.split(LEGAL_URL_RE).map((part, index) => index % 2 === 1
    ? <a key={index} href={part} target="_blank" rel="noopener noreferrer">{part}</a>
    : part);
}

/** The reader: masthead, the pill Tabs, the document and its contents. */
function LegalReader({ doc, onDocumentChange, onClose, inDialog = false }: {
  doc: LegalDoc;
  onDocumentChange: (doc: LegalDoc) => void;
  onClose?: () => void;
  inDialog?: boolean;
}) {
  const id = useId();
  const sections = legalSections(doc);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [activeSection, setActiveSection] = useState(0);
  const sectionId = (index: number) => `${id}-${doc}-${index + 1}`;

  useLayoutEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = 0;
    setActiveSection(0);
  }, [doc]);

  // Scroll the reader only, never the page around it.
  const jumpToSection = (event: React.MouseEvent<HTMLAnchorElement>, index: number) => {
    event.preventDefault();
    event.currentTarget.closest('details')?.removeAttribute('open');
    const scroll = scrollRef.current;
    const heading = scroll?.querySelector<HTMLElement>(`[id="${sectionId(index)}"]`);
    if (!scroll || !heading) return;
    const top = heading.getBoundingClientRect().top - scroll.getBoundingClientRect().top + scroll.scrollTop - 20;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    scroll.scrollTo({ top, behavior: reduced ? 'auto' : 'smooth' });
    heading.focus({ preventScroll: true });
    setActiveSection(index);
  };

  const updateActiveSection = () => {
    const scroll = scrollRef.current;
    if (!scroll) return;
    const boundary = scroll.getBoundingClientRect().top + 60;
    const headings = Array.from(scroll.querySelectorAll<HTMLElement>('.kr-lg-section h3'));
    let current = 0;
    headings.forEach((heading, index) => { if (heading.getBoundingClientRect().top <= boundary) current = index; });
    setActiveSection(current);
  };

  const contents = (
    <ol className="kr-lg-contents-list">
      {sections.map((section, index) => (
        <li key={section.heading}>
          <a href={`#${sectionId(index)}`} onClick={event => jumpToSection(event, index)} aria-current={activeSection === index ? 'location' : undefined}>
            <span aria-hidden="true">{legalSectionNumber(index)}</span><span>{section.heading}</span>
          </a>
        </li>
      ))}
    </ol>
  );

  const title = <>{LEGAL_TITLES[doc]}<span aria-hidden="true">.</span></>;

  return (
    <div className="kr-lg-reader">
      <div className="kr-lg-masthead">
        <p className="kr-lg-wordmark">nextstepuni</p>
        {onClose && (
          <Button variant="outline" size="icon" className="nsu-ink-outline kr-lg-close" aria-label="Close legal document" onClick={onClose}>
            <X aria-hidden="true" />
          </Button>
        )}
      </div>
      <div className="kr-lg-scroll" ref={scrollRef} onScroll={updateActiveSection}>
        <header className="kr-lg-hero">
          <Tabs value={doc} onValueChange={value => onDocumentChange(value as LegalDoc)} className="kr-lg-tabs">
            <TabsList aria-label="Legal documents">
              {(['privacy', 'terms'] as const).map(document => (
                <TabsTrigger key={document} value={document}>{LEGAL_TITLES[document]}</TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
          {inDialog ? <DialogTitle className="kr-lg-title">{title}</DialogTitle> : <h2 className="kr-lg-title">{title}</h2>}
          <dl className="kr-lg-meta">
            <div><dt className="kr-lg-label">Last updated</dt><dd>{LEGAL_LAST_UPDATED}</dd></div>
            <div><dt className="kr-lg-label">Version</dt><dd>{doc === 'privacy' ? PRIVACY_POLICY_VERSION : TERMS_VERSION}</dd></div>
          </dl>
          <p className="kr-lg-draft">{LEGAL_DOCUMENT_NOTE}</p>
        </header>
        <div className="kr-lg-layout">
          <aside className="kr-lg-contents kr-lg-contents-wide">
            <nav aria-label="On this page"><p className="kr-lg-label">On this page</p>{contents}</nav>
          </aside>
          {/* Hairline disclosure; the Kobra Accordion needs compiling into the runtime. */}
          <details className="kr-lg-contents kr-lg-jump">
            <summary>Jump to a section<ChevronDown aria-hidden="true" /></summary>
            <nav aria-label="On this page">{contents}</nav>
          </details>
          <div className="kr-lg-sections">
            {sections.map((section, index) => (
              <section key={section.heading} className="kr-lg-section" aria-labelledby={sectionId(index)}>
                <div className="kr-lg-section-head">
                  <span className="kr-lg-section-number" aria-hidden="true">{legalSectionNumber(index)}</span>
                  <h3 id={sectionId(index)} tabIndex={-1}>{section.heading}</h3>
                </div>
                <div className="kr-lg-copy">
                  {legalBlocks(section.body).map((block, blockIndex) => block.type === 'paragraph'
                    ? <p key={blockIndex}>{withLinks(block.text)}</p>
                    : <ul key={blockIndex}>{block.items.map((item, itemIndex) => <li key={itemIndex}>{withLinks(item)}</li>)}</ul>)}
                </div>
              </section>
            ))}
          </div>
        </div>
        <footer className="kr-lg-footer">
          <div>
            <p>Questions? Contact <a href={`mailto:${SUPPORT_EMAIL}`}>{SUPPORT_EMAIL}</a>.</p>
            <p>{COMPANY_NAME} · Company {COMPANY_NUMBER}</p>
            <p>{COMPANY_ADDRESS}</p>
            <p><a href={`/legal/2026-09-24/${doc}.html`} target="_blank" rel="noopener noreferrer">Previous version · 24 September 2026</a></p>
          </div>
          <a className="kr-lg-full" href={`/${doc}.html`} target="_blank" rel="noopener noreferrer">Open full page<ArrowUpRight aria-hidden="true" /></a>
        </footer>
      </div>
    </div>
  );
}

/** The consent gate (student, review state), as a hairline card. */
function LegalGate({ onRead }: { onRead: (doc: LegalDoc) => void }) {
  const id = useId();
  const student = true;
  const [agreed, setAgreed] = useState(false);
  const [ageConfirmed, setAgeConfirmed] = useState(false);
  const [saving, setSaving] = useState(false);

  const submit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!agreed || (student && !ageConfirmed) || saving) return;
    setSaving(true);
    window.setTimeout(() => {
      setSaving(false);
      toast({ message: 'Sample only: nothing was saved.' });
    }, 900);
  };

  return (
    // In the app this is the full-screen modal layer; here it sits in the pane.
    <section className="kr-lg-card kr-lg-gate" role="dialog" aria-labelledby={`${id}-title`} aria-describedby={`${id}-description`}>
      <p className="kr-lg-wordmark">nextstepuni</p>
      <p className="kr-lg-label kr-lg-gate-label">Your account · Updated documents</p>
      <h2 id={`${id}-title`} className="kr-lg-gate-title">Before you begin<span aria-hidden="true">.</span></h2>
      <p id={`${id}-description`} className="kr-lg-gate-lede">Review how your information is handled and the rules for using your school workspace.</p>
      <nav className="kr-lg-documents" aria-label="Review documents">
        <Button variant="outline" className="nsu-ink-outline kr-lg-doc-row" onClick={() => onRead('privacy')}>
          Read Privacy Notice<ArrowUpRight aria-hidden="true" />
        </Button>
        <Button variant="outline" className="nsu-ink-outline kr-lg-doc-row" onClick={() => onRead('terms')}>
          Read Terms of Use<ArrowUpRight aria-hidden="true" />
        </Button>
      </nav>
      <form onSubmit={submit} className="kr-lg-form">
        <label className="kr-lg-check" data-checked={agreed || undefined}>
          <Checkbox checked={agreed} disabled={saving} onCheckedChange={checked => setAgreed(checked === true)} />
          <span>I have read the Privacy Notice and agree to the Terms of Use.</span>
        </label>
        {student && (
          <label className="kr-lg-check" data-checked={ageConfirmed || undefined}>
            <Checkbox checked={ageConfirmed} disabled={saving} onCheckedChange={checked => setAgeConfirmed(checked === true)} />
            <span>I am aged 16 or over and eligible for my school’s programme.</span>
          </label>
        )}
        <p className="kr-lg-note">This records your acknowledgement and agreement. It is not blanket consent to use your information.</p>
        <Button type="submit" className="kr-lg-continue" disabled={!agreed || (student && !ageConfirmed) || saving}>
          {saving ? 'Saving…' : 'Agree & continue'}<ArrowUpRight aria-hidden="true" />
        </Button>
      </form>
      <div className="kr-lg-exit">
        <Button type="button" variant="ghost" className="kr-lg-quiet">Sign out</Button>
        <a className="kr-lg-quiet-link" href={`mailto:${SUPPORT_EMAIL}`}>Need help?</a>
      </div>
      <p className="kr-lg-note">Prefer not to agree? You can <a href={`mailto:${SUPPORT_EMAIL}?subject=Account%20data%20request`}>request a data copy or account deletion</a> by email.</p>
    </section>
  );
}

export default function LegalAfter() {
  const [inlineDoc, setInlineDoc] = useState<LegalDoc>('privacy');
  // The dialog keeps its last document while it animates closed.
  const [dialogDoc, setDialogDoc] = useState<LegalDoc>('privacy');
  const [dialogOpen, setDialogOpen] = useState(false);
  const openDialog = (doc: LegalDoc) => { setDialogDoc(doc); setDialogOpen(true); };

  return (
    <section className="kr-section kr-lg" aria-label="Legal modal and consent gate on Kobra">
      <div className="kr-lg-toolbar">
        <Button variant="outline" className="nsu-ink-outline kr-lg-action" onClick={() => openDialog(inlineDoc)}>
          Open as a dialog<AppWindow aria-hidden="true" />
        </Button>
      </div>

      <div className="kr-lg-card kr-lg-inline">
        <LegalReader doc={inlineDoc} onDocumentChange={setInlineDoc} />
      </div>

      <LegalGate onRead={openDialog} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent size="xl" showCloseButton={false} className="kr-lg-dialog">
          {/* The dialog portals out of the page scope, so it carries its own. */}
          <KobraScope className="kr-lg kr-lg-portal">
            <LegalReader doc={dialogDoc} onDocumentChange={setDialogDoc} onClose={() => setDialogOpen(false)} inDialog />
          </KobraScope>
        </DialogContent>
      </Dialog>
    </section>
  );
}
