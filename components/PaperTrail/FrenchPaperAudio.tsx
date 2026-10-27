import React from 'react';
import AudioSourcePlayer from '../MarkBank/AudioSourcePlayer';
import type { CardAudioMaterial } from '../../types/markBank';

/** A light paper surface, shared by the Atlas crop and full document viewer. */
export default function FrenchPaperAudio({ source }: { source: CardAudioMaterial }) {
  return <div className="px-3 pb-3 bg-white" style={{
    '--mb-ink': '#1a1a1a', '--mb-label': '#756e66', '--mb-muted': '#756e66',
    '--mb-raised': '#fff', '--mb-muted-border': '#ddd8d1',
  } as React.CSSProperties}>
    <AudioSourcePlayer source={source} />
  </div>;
}
