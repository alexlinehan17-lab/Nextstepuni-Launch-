/** @license SPDX-License-Identifier: Apache-2.0 */
import React, { createContext, useContext } from 'react';
import type { Reference } from '../data/references/types';
import { Citation, type CitationSource } from './approved-ui-runtime';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './approved-ui-runtime';
import { BrandBook } from './learning/BrandBook';

const ModuleReferencesContext = createContext<Reference[]>([]);
export const ModuleReferencesProvider = ModuleReferencesContext.Provider;
export function referenceUrl(reference: Reference) {
  return reference.doi ? `https://doi.org/${reference.doi}` : reference.url ?? (reference.repoPath ? `/${reference.repoPath.replace(/^\//, '')}` : undefined);
}
export function citationSource(reference: Reference): CitationSource {
  return {
    name: reference.source,
    title: reference.title,
    url: referenceUrl(reference) ?? '',
    description: reference.authors,
    date: String(reference.year),
    icon: <BrandBook size={14} />,
  };
}
/** Existing claim-to-reference numbers remain the stable lookup; readers see source bubbles. */
export const Cite: React.FC<{ n: number | number[] }> = ({ n }) => {
  const references = useContext(ModuleReferencesContext);
  const sources = (Array.isArray(n) ? n : [n]).flatMap(index => references[index - 1] ? [citationSource(references[index - 1])] : []);
  return sources.length ? <Citation sources={sources} className="mr-citation" /> : <span className="mr-citation-unavailable" title="Source details unavailable">Source</span>;
};
export const ReferencesModal: React.FC<{ open: boolean; onClose: () => void; references: Reference[] }> = ({ open, onClose, references }) => (
  <Dialog open={open} onOpenChange={value => { if (!value) onClose(); }}>
    <DialogContent className="mr-reference-dialog" size="lg">
      <DialogHeader><DialogTitle>Sources &amp; further reading</DialogTitle><DialogDescription>The sources behind this module.</DialogDescription></DialogHeader>
      <ol className="mr-reference-list">{references.map(reference => <li key={reference.id}>
        <BrandBook size={27} /><div><p>{reference.authors} ({reference.year})</p>
        {referenceUrl(reference) ? <a href={referenceUrl(reference)} target="_blank" rel="noopener noreferrer">{reference.title} ↗</a> : <strong>{reference.title}</strong>}
        <p><em>{reference.source}</em></p></div>
      </li>)}</ol>
    </DialogContent>
  </Dialog>
);
