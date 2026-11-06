import japaneseRecordings from '../../data/japaneseAudio.json';
import russianRecordings from '../../data/russianAudio.json';
import type { CardAudioMaterial } from '../../types/markBank';
import { frenchAudioForPaper } from './frenchAudio';

/** Resolve only a verified listening booklet, in its exact examination year. */
export function audioForPaper(paper: { subjectId: string; year: number; fileid: string }): CardAudioMaterial | null {
  if (paper.subjectId === 'french') return frenchAudioForPaper(paper);
  const recordings = paper.subjectId === 'japanese' ? japaneseRecordings
    : paper.subjectId === 'russian' ? russianRecordings : [];
  const recording = recordings.find(recording => recording.year === paper.year
    && recording.paperFileids.includes(paper.fileid));
  return recording ? { ...recording.source, kind: 'source-audio' } : null;
}
