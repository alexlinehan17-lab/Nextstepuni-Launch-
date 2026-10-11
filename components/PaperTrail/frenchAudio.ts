import recordings from '../../data/frenchAudio.json';
import type { CardAudioMaterial } from '../../types/markBank';

/** Exact booklet identity keeps written papers and other years audio-free. */
export function frenchAudioForPaper(paper: { subjectId: string; year: number; fileid: string }): CardAudioMaterial | null {
  if (paper.subjectId !== 'french') return null;
  const recording = recordings.find(recording => recording.year === paper.year
    && recording.paperFileids.includes(paper.fileid));
  return recording ? { ...recording.source, kind: 'source-audio' } : null;
}
