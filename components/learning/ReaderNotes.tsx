import React, { useId, useRef, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Sheet } from '../ui/Sheet';
import { Button, TextButton } from '../ui/Button';
import { useModuleResponses } from '../../hooks/useModuleResponses';
import { useSettingsContext } from '../../contexts/SettingsContext';
import { LEARNING_NOTEBOOK_NAMESPACE, notebookEntry } from '../../utils/learningNotebook';
import { downloadText } from '../../utils/downloadText';
import { ResponseSaveStatus } from './ResponseSaveStatus';
import { BrandBook } from './BrandBook';

/**
 * Notes (area 5 of the design build; board c-read-flow, "Notes"): the learning notebook as a sheet
 * from the bottom. Notes save as you type, through the same notebook store as before, so there is no
 * Done button: Close (or a swipe, or Escape) only closes the sheet. "Saved" sits at the head once the
 * account has the words; any other state is said in the sheet, with its retry.
 */
export function ModuleNotesCard({ storageKey, moduleId, title, sectionTitle, sectionIndex, open, onClose }: { storageKey: string; moduleId: string; title: string; sectionTitle: string; sectionIndex: number; open: boolean; onClose: () => void }) {
  const id = useId();
  const { responses, saveResponse, isLoaded, saveStatus, retrySave } = useModuleResponses(LEARNING_NOTEBOOK_NAMESPACE);
  const settings = useSettingsContext();
  const entry = notebookEntry(responses[moduleId], title);
  const [takeaway, setTakeaway] = useState('');
  const takeawayRef = useRef<HTMLTextAreaElement>(null);
  const [legacy] = useState(() => { try { return localStorage.getItem(storageKey) ?? ''; } catch { return ''; } });
  const saveNotes = (notes: string) => saveResponse(moduleId, { ...entry, notes });
  const saveTakeaway = () => {
    // Nothing written yet: the button takes you to the field rather than going dead.
    if (!takeaway.trim()) { takeawayRef.current?.focus(); return; }
    saveResponse(moduleId, { ...entry, takeaways: [...entry.takeaways, { id: crypto.randomUUID(), text: takeaway.trim(), sectionTitle, sectionIndex, mode: settings?.settings.essentialsMode ? 'essentials' : 'full', savedAt: new Date().toISOString() }] });
    setTakeaway('');
  };
  return (
    <Sheet open={open} onClose={onClose} title="Notes" titleSize="small" className="rd-sheet rd-notes" titleAlign="start" status={saveStatus === 'saved' ? 'Saved' : saveStatus === 'saving' ? 'Saving…' : undefined}>
      <div className="rd-nb">
        <BrandBook size={40} />
        <div className="rd-nb-copy"><p className="t-label rd-nb-label">Your learning notebook</p><p className="t-row rd-nb-title">{title}</p></div>
      </div>
      <div className="rd-fset">
        <label className="rd-flabel" htmlFor={id}>Your notes</label>
        <textarea id={id} className="rd-area" disabled={!isLoaded} value={entry.notes} placeholder="Something to remember. A question to come back to…" onChange={event => saveNotes(event.target.value)} />
        {legacy && !entry.notes.includes(legacy) ? <Button size="sm" className="rd-fbtn" onClick={() => { if (isLoaded) saveNotes([entry.notes, legacy].filter(Boolean).join('\n\n')); }}>Import your previous device notes</Button> : null}
      </div>
      <div className="rd-fset">
        <label className="rd-flabel" htmlFor={`${id}-takeaway`}>An idea to keep from {sectionTitle}</label>
        <textarea ref={takeawayRef} id={`${id}-takeaway`} className="rd-area rd-area--sm" value={takeaway} onChange={event => setTakeaway(event.target.value)} maxLength={2000} placeholder="Write it in your own words…" />
        <Button className="rd-fbtn" onClick={() => { if (isLoaded) saveTakeaway(); }}>Save takeaway</Button>
      </div>
      {entry.takeaways.length ? (
        <div className="rd-fset">
          <p className="t-label rd-kept-label">Kept from this module</p>
          <ul className="rd-kept">
            {entry.takeaways.map(item => (
              <li key={item.id}>
                <span className="rd-kept-copy"><span className="t-meta">From {item.sectionTitle}</span><span className="t-sub rd-kept-text">{item.text}</span></span>
                <TextButton tone="quiet" aria-label={`Remove takeaway: ${item.text.slice(0, 60)}`} onClick={() => saveResponse(moduleId, { ...entry, takeaways: entry.takeaways.filter(candidate => candidate.id !== item.id) })}>Remove</TextButton>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      {saveStatus === 'saved' || saveStatus === 'saving' ? null : <div className="rd-status"><ResponseSaveStatus status={saveStatus} onRetry={retrySave} /></div>}
      <p className="t-meta rd-notes-foot">Your notes and takeaways save to your private account and can be searched from Modules. Signing out clears the device recovery copy.</p>
      <TextButton className="rd-dl" onClick={() => downloadText('my-module-notes.txt', `${title}\n\n${entry.notes}\n\n${entry.takeaways.map(item => `${item.sectionTitle}\n${item.text}`).join('\n\n')}`)}>Download a copy</TextButton>
    </Sheet>
  );
}

export function ReaderNotes({ moduleId, title, sectionTitle, sectionIndex, open, onClose }: { moduleId: string; title: string; sectionTitle: string; sectionIndex: number; open: boolean; onClose: () => void }) {
  const { user } = useAuth();
  const storageKey = `nextstepuni:learning-notes:${user?.uid ?? 'guest'}:${moduleId}`;
  return <ModuleNotesCard key={storageKey} storageKey={storageKey} moduleId={moduleId} title={title} sectionTitle={sectionTitle} sectionIndex={sectionIndex} open={open} onClose={onClose} />;
}
