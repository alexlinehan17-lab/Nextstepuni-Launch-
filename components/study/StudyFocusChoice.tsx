import React, { useId } from 'react';
import { Button, Switch } from '../approved-ui-runtime';
import { useStudyFocus } from '../../hooks/useStudyFocus';
import { configureStudyFocus, setStudyFocusEnabled } from '../../services/studyFocus';

/** Uses the Study Room's existing option row and controls. iOS only. */
export default function StudyFocusChoice() {
  const focus = useStudyFocus();
  const id = useId();
  if (!focus.available) return null;
  return <div className="ks-appearance-choice">
    <div>
      <label htmlFor={id}>Block distracting apps</label>
      <p id={`${id}-help`}>Choose apps and websites to block while studying. Pausing or finishing releases them. Keep your notes available.</p>
      {focus.selectionCount > 0 && <p>{focus.selectionCount} selection{focus.selectionCount === 1 ? '' : 's'} · saved only on this device</p>}
      <Button variant="outline" size="sm" onClick={() => { void configureStudyFocus(); }} disabled={focus.busy}>
        {focus.busy ? 'Opening Screen Time…' : focus.selectionCount ? 'Change apps' : 'Choose apps'}
      </Button>
      {focus.error && <p role="alert">{focus.error}</p>}
    </div>
    <Switch id={id} checked={focus.enabled} disabled={focus.busy} aria-label="Block distracting apps" aria-describedby={`${id}-help`}
      onCheckedChange={value => { void setStudyFocusEnabled(value); }} />
  </div>;
}

export function StudyFocusStatus() {
  const focus = useStudyFocus();
  if (!focus.available || (!focus.enabled && !focus.error)) return null;
  return <div className="ss-notify" role="status">
    <p>{focus.error ?? (focus.active ? 'Your selected apps are blocked while you study.' : 'Your selected apps are currently unblocked.')}</p>
    {focus.enabled && <div className="ss-notify-actions">
      <button type="button" className="ss-notify-no" disabled={focus.busy} onClick={() => { void setStudyFocusEnabled(false); }}>Turn off app blocking</button>
    </div>}
  </div>;
}
