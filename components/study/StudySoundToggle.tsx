import React from 'react';
import { Volume2, VolumeX } from 'lucide-react';
import { setSoundMuted } from '../approved-ui-runtime';

export default function StudySoundToggle({ muted }: { muted: boolean }) {
  return <button type="button" className="study-sound-toggle" aria-label={muted ? 'Turn study sound on' : 'Mute study sound'} aria-pressed={!muted} onClick={() => setSoundMuted(!muted)}>
    {muted ? <VolumeX size={17} aria-hidden="true" /> : <Volume2 size={17} aria-hidden="true" />}
    <span>Sound {muted ? 'off' : 'on'}</span>
  </button>;
}
