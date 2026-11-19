import { describe, expect, it } from 'vitest';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import frenchRecordings from '../data/frenchAudio.json';
import japaneseRecordings from '../data/japaneseAudio.json';
import russianRecordings from '../data/russianAudio.json';
import { audioForPaper } from '../components/PaperTrail/paperRecording';
import { frenchAudioForPaper } from '../components/PaperTrail/frenchAudio';

describe('official recordings in Topic Atlas and the paper viewer', () => {
  it.each(['japanese', 'russian'] as const)('finds every indexed %s listening booklet and excludes written papers and schemes', subjectId => {
    const recordings = subjectId === 'japanese' ? japaneseRecordings : russianRecordings;
    const matched = new Set<string>();
    for (const sitting of PAPER_TRAIL_INDEX[subjectId]) {
      if (sitting.lang !== 'ev' || sitting.year < 2010 || sitting.year > 2026) continue;
      for (const booklet of sitting.papers) {
        const identity = { subjectId, year: sitting.year, fileid: booklet.doc.f };
        const source = audioForPaper(identity);
        if (booklet.label === 'Aural Paper') {
          expect(source, JSON.stringify(identity)).not.toBeNull();
          const recording = recordings.find(recording => recording.year === sitting.year)!;
          expect(source?.canonicalUrl).toBe(recording.source.canonicalUrl);
          expect(source?.canonicalUrl).toContain(`/exampapers/${sitting.year}/`);
          expect(recording.verification.sha256).toMatch(/^[a-f0-9]{64}$/);
          expect(recording.verification.bytes).toBeGreaterThan(0);
          expect(recording.verification.durationSeconds).toBeGreaterThan(0);
          expect(recording.verification.browserPlayback).toBe(false);
          matched.add(`${sitting.year}/${booklet.doc.f}`);
        } else {
          expect(source, JSON.stringify(identity)).toBeNull();
        }
        if (booklet.scheme) expect(audioForPaper({ ...identity, fileid: booklet.scheme.f })).toBeNull();
      }
    }
    expect(recordings).toHaveLength(17);
    expect(matched.size).toBe(33); // No 2020 Ordinary booklet is indexed.
    expect(new Set(recordings.flatMap(recording => recording.paperFileids.map(fileid => `${recording.year}/${fileid}`)))).toEqual(matched);
  });

  it('does not substitute another subject, year, booklet edition or sitting', () => {
    const paper = { subjectId: 'russian', year: 2026, fileid: 'LC099ALPA00BV.pdf' };
    expect(audioForPaper({ ...paper, subjectId: 'japanese' })).toBeNull();
    expect(audioForPaper({ ...paper, subjectId: 'irish' })).toBeNull();
    expect(audioForPaper({ ...paper, year: 2009 })).toBeNull();
    expect(audioForPaper({ ...paper, fileid: 'LC099ALPA00EV.pdf' })).toBeNull();
    expect(audioForPaper({ ...paper, fileid: 'LC099ALPA00BV-deferred.pdf' })).toBeNull();
    expect(audioForPaper({ ...paper, year: 2020, fileid: 'LC099GLPA00BV.pdf' })).toBeNull();
  });

  it('preserves the established French recording selection', () => {
    for (const recording of frenchRecordings) {
      for (const fileid of recording.paperFileids) {
        const paper = { subjectId: 'french', year: recording.year, fileid };
        expect(audioForPaper(paper)).toEqual(frenchAudioForPaper(paper));
      }
    }
    expect(audioForPaper({ subjectId: 'french', year: 2026, fileid: 'LC010ALP000BV.pdf' })).toBeNull();
  });
});
