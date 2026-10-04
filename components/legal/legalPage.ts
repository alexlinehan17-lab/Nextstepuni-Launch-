import { LEGAL_LAST_UPDATED, LEGAL_TITLES, LEGAL_URL_RE, PRIVACY_POLICY_VERSION, SUPPORT_EMAIL, TERMS_VERSION, COMPANY_NAME, COMPANY_NUMBER, COMPANY_ADDRESS, type LegalDoc } from './legalContent';
import { ARCHIVED_PRIVACY_NOTICE, ARCHIVED_TERMS_OF_USE } from './legalArchive';
import { LEGAL_DOCUMENT_NOTE, legalBlocks, legalSections, legalSectionId, legalSectionNumber } from './legalPresentation';

const escapeHtml = (text: string) => text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const linkedText = (text: string) => {
  LEGAL_URL_RE.lastIndex = 0;
  return text.split(LEGAL_URL_RE).map((part, index) => index % 2 === 1
    ? `<a href="${escapeHtml(part)}" target="_blank" rel="noopener noreferrer">${escapeHtml(part)}</a>`
    : escapeHtml(part)).join('');
};

/** Standalone, indexable documents that remain fully usable without JavaScript. */
export function renderLegalPage(doc: LegalDoc, stylesheet: string, archived = false): string {
  const sections = archived ? (doc === 'privacy' ? ARCHIVED_PRIVACY_NOTICE : ARCHIVED_TERMS_OF_USE) : legalSections(doc);
  const version = archived ? '2026-09-24' : doc === 'privacy' ? PRIVACY_POLICY_VERSION : TERMS_VERSION;
  const updated = archived ? '24 September 2026' : LEGAL_LAST_UPDATED;
  const note = archived ? 'Archived version · Historical wording, superseded on 4 October 2026. The links above open the current documents.' : LEGAL_DOCUMENT_NOTE;
  const contents = `<ol>${sections.map((section, index) => `<li><a href="#${legalSectionId(doc, index)}"><span aria-hidden="true">${legalSectionNumber(index)}</span><span>${escapeHtml(section.heading)}</span></a></li>`).join('')}</ol>`;
  const documentLinks = (className: string) => `<nav class="${className}" aria-label="Legal documents">${(['privacy', 'terms'] as const).map(document => `<a href="/${document}.html"${doc === document ? ' aria-current="page"' : ''}>${LEGAL_TITLES[document]}</a>`).join('')}</nav>`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="robots" content="${archived ? 'noindex, follow' : 'index, follow'}" />
  <title>${LEGAL_TITLES[doc]} · NextStepUni</title>
  <link rel="icon" href="/icons/north-star-favicon-32x32.png" />
  <link rel="preload" href="/fonts/abc-diatype-regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/fonts/abc-diatype-bold.woff2" as="font" type="font/woff2" crossorigin />
  <style>${stylesheet}</style>
</head>
<body class="legal-document legal-page">
  <a href="#document" class="legal-skip">Skip to document</a>
  <div class="legal-page-wrap">
    <header class="legal-masthead">
      <p class="legal-wordmark">NextStep<span>Uni</span></p>
      <a class="legal-home" href="/">Back to NextStepUni <span aria-hidden="true">↗</span></a>
    </header>
    <main id="document">
      <header class="legal-hero">
        ${documentLinks('legal-switcher')}
        <h1 class="legal-title">${LEGAL_TITLES[doc]}<span aria-hidden="true">.</span></h1>
        <dl class="legal-meta">
          <div><dt class="legal-label">Last updated</dt><dd>${updated}</dd></div>
          <div><dt class="legal-label">Version</dt><dd>${version}</dd></div>
        </dl>
        <p class="legal-draft">${note}</p>
      </header>
      <div class="legal-layout">
        <aside class="legal-contents legal-contents-desktop"><nav aria-label="On this page"><p class="legal-label">On this page</p>${contents}</nav></aside>
        <details class="legal-contents legal-contents-mobile"><summary>Jump to a section</summary><nav aria-label="On this page">${contents}</nav></details>
        <div class="legal-reader">
          ${sections.map((section, index) => `<section class="legal-section" aria-labelledby="${legalSectionId(doc, index)}">
            <div class="legal-section-header"><span class="legal-section-number" aria-hidden="true">${legalSectionNumber(index)}</span><h2 id="${legalSectionId(doc, index)}" tabindex="-1">${escapeHtml(section.heading)}</h2></div>
            <div class="legal-copy">${legalBlocks(section.body).map(block => block.type === 'paragraph' ? `<p>${linkedText(block.text)}</p>` : `<ul>${block.items.map(item => `<li>${linkedText(item)}</li>`).join('')}</ul>`).join('')}</div>
          </section>`).join('\n')}
        </div>
      </div>
    </main>
    <footer class="legal-footer">
      <div><p>Questions? Contact <a href="mailto:${SUPPORT_EMAIL}">${SUPPORT_EMAIL}</a>.</p><p>${COMPANY_NAME} · Company ${COMPANY_NUMBER}</p><p>${COMPANY_ADDRESS}</p></div>
      <div>${documentLinks('legal-footer-links')}${archived ? '' : `<p><a href="/legal/2026-09-24/${doc}.html">Previous version · 24 September 2026</a></p>`}</div>
    </footer>
  </div>
</body>
</html>`;
}
