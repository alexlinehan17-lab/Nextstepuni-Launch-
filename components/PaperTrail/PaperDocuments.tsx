import React, { useState } from 'react';
import { ArrowLeft, ArrowUpRight } from 'lucide-react';
import { Button } from '../approved-ui-runtime';
import { Attachment, AttachmentMedia, AttachmentContent, AttachmentTitle, AttachmentDescription, AttachmentActions, AttachmentTrigger } from '../approved-ui-runtime';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../approved-ui-runtime';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator } from '../approved-ui-runtime';
import type { PaperEntry, PaperItem, PaperTrailSubject } from '../../types/paperTrail';
import PaperCover from './PaperCover';
import { paperStoragePath, paperUrl, prettyBytes } from './storage';

export type DocumentSide = 'paper' | 'scheme';
export const documentUrl = (subject: PaperTrailSubject, entry: PaperEntry, item: PaperItem, side: DocumentSide) => {
  const file = side === 'scheme' ? item.scheme : item.doc;
  return file ? paperUrl(paperStoragePath(subject.cycle, subject.id, entry.year, side, file.f)) : '';
};

export function PaperDocuments({ subject, entry, item, label, initial, onClose, onRead }: {
  subject: PaperTrailSubject; entry: PaperEntry; item: PaperItem; label: string;
  initial: DocumentSide | 'files'; onClose: () => void; onRead: (side: DocumentSide) => void;
}) {
  const [mode, setMode] = useState<DocumentSide | 'files' | 'pair'>(initial);
  const sides: DocumentSide[] = item.scheme ? ['paper', 'scheme'] : ['paper'];
  const fileName = (side: DocumentSide) => side === 'paper' ? item.label.replace(/\s*\([A-Z]{2}\)\s*$/, '').trim() : 'Marking scheme';
  const isImage = (side: DocumentSide) => /\.(jpg|jpeg|png)$/i.test((side === 'paper' ? item.doc : item.scheme)!.f);
  const details = (side: DocumentSide) => [isImage(side) ? 'Image' : 'PDF', prettyBytes((side === 'paper' ? item.doc : item.scheme)!.b)].filter(Boolean).join(' · ');
  const shown = mode === 'pair' ? sides : sides.filter(side => side === mode);
  return <Dialog open onOpenChange={value => !value && onClose()}>
    <DialogContent className={`pt-documents-dialog ${mode === 'pair' ? 'pt-documents-pair' : ''}`}>
      <DialogHeader>
        <DialogTitle className="pt-documents-title">{mode === 'files' ? 'The paper. The points.' : mode === 'pair' ? 'Paper & marking scheme' : fileName(mode)}</DialogTitle>
        <DialogDescription>{label} · {entry.year} · {entry.level[0].toUpperCase() + entry.level.slice(1)} level · {entry.lang === 'ev' ? 'English' : 'Gaeilge'}</DialogDescription>
      </DialogHeader>
      {mode === 'files' ? <>
        <div className="pt-document-attachments">
          {sides.map(side => <Attachment className="pt-document-attachment" key={side}>
            <AttachmentTrigger aria-label={`Inspect ${fileName(side)}`} onClick={() => setMode(side)} />
            <AttachmentMedia variant="image" className="pt-document-thumbnail">
              <PaperCover url={documentUrl(subject, entry, item, side)} image={isImage(side)} />
            </AttachmentMedia>
            <AttachmentContent><AttachmentTitle>{fileName(side)}</AttachmentTitle><AttachmentDescription>{details(side)}</AttachmentDescription></AttachmentContent>
            <AttachmentActions><Button variant="ghost" size="icon" aria-label={`Open ${fileName(side)} in Paper Trail`} onClick={() => onRead(side)}><ArrowUpRight /></Button></AttachmentActions>
          </Attachment>)}
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger render={<Button variant="outline" />}>Paper options</DropdownMenuTrigger>
          <DropdownMenuContent>
            {sides.map(side => <DropdownMenuItem key={side} onClick={() => setMode(side)}>Inspect {side === 'paper' ? 'the paper' : 'the scheme'}</DropdownMenuItem>)}
            {item.scheme && <><DropdownMenuSeparator /><DropdownMenuItem onClick={() => setMode('pair')}>View as a pair</DropdownMenuItem></>}
          </DropdownMenuContent>
        </DropdownMenu>
      </> : <>
        <Button variant="ghost" className="pt-back-to-files" onClick={() => setMode('files')}><ArrowLeft />Back to files</Button>
        <div className="pt-document-preview-pages">
          {shown.map(side => <figure key={side}>
            <button className="pt-document-preview-cover" aria-label={`Open ${fileName(side)} in Paper Trail`} onClick={() => onRead(side)}>
              <PaperCover url={documentUrl(subject, entry, item, side)} image={isImage(side)} renderWidth={800} />
            </button>
            <figcaption><div><strong>{fileName(side)}</strong><span>{details(side)}</span></div><Button variant="outline" className="nsu-ink-outline" onClick={() => onRead(side)}>{isImage(side) ? 'Open image' : 'Open paper'}<ArrowUpRight /></Button></figcaption>
          </figure>)}
        </div>
      </>}
      <p className="pt-source-note">Examination material © State Examinations Commission.</p>
    </DialogContent>
  </Dialog>;
}
