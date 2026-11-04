import React, { useId, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import SignatureCard from '../ui/SignatureCard';
import ActionButton from '../ui/ActionButton';
import { TextAreaField } from '../ui/FormControls';
import { useModuleResponses } from '../../hooks/useModuleResponses';
import { useSettingsContext } from '../../contexts/SettingsContext';
import { LEARNING_NOTEBOOK_NAMESPACE, notebookEntry } from '../../utils/learningNotebook';
import { downloadText } from '../../utils/downloadText';
import { ResponseSaveStatus } from './ResponseSaveStatus';

export function ModuleNotesCard({ storageKey, moduleId, title, sectionTitle, sectionIndex, open, onClose }: { storageKey: string; moduleId: string; title: string; sectionTitle: string; sectionIndex: number; open: boolean; onClose: () => void }) {
  const id = useId();
  const { responses, saveResponse, isLoaded, saveStatus, retrySave } = useModuleResponses(LEARNING_NOTEBOOK_NAMESPACE);
  const settings = useSettingsContext();
  const entry = notebookEntry(responses[moduleId], title);
  const [takeaway, setTakeaway] = useState('');
  const [legacy] = useState(() => { try { return localStorage.getItem(storageKey) ?? ''; } catch { return ''; } });
  const saveNotes = (notes: string) => saveResponse(moduleId, { ...entry, notes });
  const saveTakeaway = () => {
    if (!takeaway.trim()) return;
    saveResponse(moduleId, { ...entry, takeaways: [...entry.takeaways, { id: crypto.randomUUID(), text: takeaway.trim(), sectionTitle, sectionIndex, mode: settings?.settings.essentialsMode ? 'essentials' : 'full', savedAt: new Date().toISOString() }] });
    setTakeaway('');
  };
  return <SignatureCard open={open} onClose={onClose} title="Your learning notebook" eyebrow="Module notes" description={title} footer={<>
    <ResponseSaveStatus status={saveStatus} onRetry={retrySave} />
    <ActionButton onClick={() => downloadText('my-module-notes.txt', `${title}\n\n${entry.notes}\n\n${entry.takeaways.map(item => `${item.sectionTitle}\n${item.text}`).join('\n\n')}`)}>Download a copy</ActionButton>
    <ActionButton onClick={onClose}>Done</ActionButton>
  </>}>
    <p className="sc-small">Your notes and takeaways save to your private account and can be searched from Modules. Signing out clears the device recovery copy.</p>
    <label className="sc-note-label" htmlFor={id}>Your notes</label>
    <TextAreaField id={id} className="sc-notes-editor" disabled={!isLoaded} value={entry.notes} placeholder="Something to remember. A question to come back to…" onChange={event => saveNotes(event.target.value)} />
    {legacy && !entry.notes.includes(legacy) && <ActionButton disabled={!isLoaded} onClick={() => saveNotes([entry.notes, legacy].filter(Boolean).join('\n\n'))}>Import your previous device notes</ActionButton>}
    <label className="sc-note-label" htmlFor={`${id}-takeaway`}>An idea to keep from {sectionTitle}</label>
    <TextAreaField id={`${id}-takeaway`} value={takeaway} onChange={event => setTakeaway(event.target.value)} maxLength={2000} placeholder="Write it in your own words…" />
    <ActionButton disabled={!isLoaded || !takeaway.trim()} onClick={saveTakeaway}>Save takeaway</ActionButton>
    {!!entry.takeaways.length && <ul className="mr-saved-takeaways">{entry.takeaways.map(item => <li key={item.id}><strong>{item.sectionTitle}</strong><p>{item.text}</p><button type="button" aria-label={`Remove takeaway: ${item.text.slice(0, 60)}`} onClick={() => saveResponse(moduleId, { ...entry, takeaways: entry.takeaways.filter(candidate => candidate.id !== item.id) })}>Remove</button></li>)}</ul>}
  </SignatureCard>;
}

export function ReaderNotes({ moduleId, title, sectionTitle, sectionIndex, open, onClose }: { moduleId: string; title: string; sectionTitle: string; sectionIndex: number; open: boolean; onClose: () => void }) {
  const { user } = useAuth();
  const storageKey = `nextstepuni:learning-notes:${user?.uid ?? 'guest'}:${moduleId}`;
  return <ModuleNotesCard key={storageKey} storageKey={storageKey} moduleId={moduleId} title={title} sectionTitle={sectionTitle} sectionIndex={sectionIndex} open={open} onClose={onClose} />;
}
