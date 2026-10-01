import React, { useId, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import SignatureCard from '../ui/SignatureCard';
import ActionButton from '../ui/ActionButton';
import { TextAreaField } from '../ui/FormControls';

export function ModuleNotesCard({ storageKey, title, open, onClose }: { storageKey: string; title: string; open: boolean; onClose: () => void }) {
  const id = useId();
  const [value, setValue] = useState(() => { try { return localStorage.getItem(storageKey) ?? ''; } catch { return ''; } });
  const [saved, setSaved] = useState(true);
  return <SignatureCard open={open} onClose={onClose} title="Your learning notebook" eyebrow="Module notes" description={title} footer={<>
    <p id={`${id}-status`} className="sc-small sc-note-status" role="status">{saved ? 'Saved on this device for your account.' : 'Could not save on this device. Keep a copy before leaving.'}</p>
    <ActionButton onClick={onClose}>Done</ActionButton>
  </>}>
    <label className="sc-note-label" htmlFor={id}>Your notes</label>
    <TextAreaField id={id} className="sc-notes-editor" value={value} placeholder="Something to remember. A question to come back to…" aria-describedby={`${id}-status`} onChange={event => {
      setValue(event.target.value);
      try { localStorage.setItem(storageKey, event.target.value); setSaved(true); } catch { setSaved(false); }
    }} />
  </SignatureCard>;
}

export function ReaderNotes({ moduleId, title, open, onClose }: { moduleId: string; title: string; open: boolean; onClose: () => void }) {
  const { user } = useAuth();
  const storageKey = `nextstepuni:learning-notes:${user?.uid ?? 'guest'}:${moduleId}`;
  return <ModuleNotesCard key={storageKey} storageKey={storageKey} title={title} open={open} onClose={onClose} />;
}
