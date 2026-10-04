import React, { useState } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import { LegalModal } from '../components/legal/LegalModal';
import { PRIVACY_NOTICE, TERMS_OF_USE, PRIVACY_POLICY_VERSION, type LegalDoc } from '../components/legal/legalContent';
import { renderLegalPage } from '../components/legal/legalPage';

const documents = [
  { doc: 'privacy' as const, sections: PRIVACY_NOTICE },
  { doc: 'terms' as const, sections: TERMS_OF_USE },
];

describe('Legal document readers', () => {
  test.each(documents)('$doc preserves every paragraph and bullet in both readers', ({ doc, sections }) => {
    const { unmount } = render(<LegalModal doc={doc} onClose={vi.fn()} />);
    const publicDocument = new DOMParser().parseFromString(renderLegalPage(doc, ''), 'text/html');
    const expectedCopy = sections.flatMap(section => section.body.map(line => line.replace(/^• /, '')));
    const copy = (root: ParentNode) => Array.from(root.querySelectorAll('.legal-copy p, .legal-copy li')).map(line => line.textContent);
    expect(copy(screen.getByRole('dialog'))).toEqual(expectedCopy);
    expect(copy(publicDocument)).toEqual(expectedCopy);
    expect(publicDocument.querySelector('.legal-meta')?.textContent).toContain(PRIVACY_POLICY_VERSION);
    unmount();
  });

  test('public contents links point to every section and official sources stay clickable', () => {
    const document = new DOMParser().parseFromString(renderLegalPage('terms', ''), 'text/html');
    const links = Array.from(document.querySelectorAll<HTMLAnchorElement>('.legal-contents-desktop a'));
    expect(links).toHaveLength(TERMS_OF_USE.length);
    for (const link of links) expect(document.querySelector(link.getAttribute('href')!)).not.toBeNull();
    const sourceUrls = TERMS_OF_USE.flatMap(section => section.body).join(' ').match(/https?:\/\/[^\s,)]+/g)!;
    const publishedUrls = Array.from(document.querySelectorAll<HTMLAnchorElement>('.legal-copy a')).map(link => link.getAttribute('href'));
    expect(publishedUrls).toEqual(sourceUrls);
  });

  test('section navigation focuses the heading without changing the app URL', () => {
    const scrollIntoView = vi.fn();
    render(<LegalModal doc="privacy" onClose={vi.fn()} />);
    const heading = screen.getByRole('heading', { name: 'What we collect' });
    Object.defineProperty(heading, 'scrollIntoView', { value: scrollIntoView });
    const before = window.location.href;
    fireEvent.click(document.querySelector<HTMLAnchorElement>('.legal-contents-desktop a[href="#privacy-section-3"]')!);
    expect(heading).toHaveFocus();
    expect(scrollIntoView).toHaveBeenCalled();
    expect(window.location.href).toBe(before);
  });

  test('switching documents resets the reader and retains keyboard focus', () => {
    function Reader() {
      const [doc, setDoc] = useState<LegalDoc>('privacy');
      return <LegalModal doc={doc} onClose={vi.fn()} onDocumentChange={setDoc} />;
    }
    render(<Reader />);
    const termsButton = screen.getByRole('button', { name: 'Terms of Use' });
    termsButton.focus();
    const scroll = document.querySelector<HTMLElement>('.legal-scroll')!;
    scroll.scrollTop = 420;
    fireEvent.click(termsButton);
    expect(screen.getByRole('dialog', { name: 'Terms of Use' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Terms of Use' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: 'Terms of Use' })).toHaveFocus();
    expect(document.querySelector('.legal-scroll')?.scrollTop).toBe(0);
    expect(document.querySelector('.legal-contents-desktop a[aria-current="location"]')).toHaveAttribute('href', '#terms-section-1');
  });

  test('closing with Escape returns keyboard focus to the opener', async () => {
    function Reader() {
      const [doc, setDoc] = useState<LegalDoc | null>(null);
      return <><button onClick={() => setDoc('privacy')}>Read privacy</button><LegalModal doc={doc} onClose={() => setDoc(null)} /></>;
    }
    render(<Reader />);
    const opener = screen.getByRole('button', { name: 'Read privacy' });
    opener.focus();
    fireEvent.click(opener);
    await waitFor(() => expect(screen.getByRole('dialog')).toHaveFocus());
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(opener).toHaveFocus();
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
});
