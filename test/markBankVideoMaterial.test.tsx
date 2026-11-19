import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import VideoSourcePlayer from '@/components/MarkBank/VideoSourcePlayer';
import SessionScreen from '@/components/MarkBank/SessionScreen';
import { isQuizCard } from '@/components/study/quiz/studyQuizPlan';
import { sessionExerciseCount } from '@/components/MarkBank/sessionPlanning';
import { videoMaterialFault } from '../scripts/markbank/videoMaterial.mjs';
import type { CardVideoMaterial, SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

// The identity is from the verified SEC listing. The question and answer
// below are explicitly synthetic runtime fixtures, never examination content.
const official: CardVideoMaterial = {
  kind: 'source-video', label: 'Section A', title: '2026 LCVP examination video',
  secFileid: 'LC462CLP031EV.mov',
  canonicalUrl: 'https://www.examinations.ie/archive/exampapers/2026/LC462CLP031EV.mov',
  playbackUrl: 'https://www.examinations.ie/archive/exampapers/2026/LC462CLP031EV.mov',
  attribution: '© State Examinations Commission.', presentationNote: 'Full official video, including its original sound.',
};
const fixture: SecQuestionCard = {
  id: 'synthetic-lcvp-video-runtime', source: 'sec', kind: 'question', subjectId: 'lcvp',
  year: 2026, level: 'common', section: 'A', paperFileid: null,
  topicId: 'fixture', conceptId: 'fixture', specVersion: 'fixture',
  questionRef: 'Synthetic video fixture', questionText: 'Synthetic prompt for the runtime check.',
  schemeCitation: 'Synthetic fixture; no examination answer asserted.',
  totalMarks: 2, tariffModel: { kind: 'fixed' },
  rows: [{ id: 'answer', kind: 'point', verbatim: 'Fixture answer', marks: 2 }],
  videoMaterial: official, qa: { gates: [], humanReviewedBy: 'fixture', humanReviewedAt: '2026-11-10' },
};
const forFile = (year: number, secFileid: string, deferred = false): SecQuestionCard => ({
  ...fixture, year, id: deferred ? 'synthetic-lcvp-deferred-video' : fixture.id,
  videoMaterial: { ...official, secFileid,
    canonicalUrl: `https://www.examinations.ie/archive/${deferred ? 'deferredexams' : 'exampapers'}/${year}/${secFileid}`,
    playbackUrl: `https://www.examinations.ie/archive/${deferred ? 'deferredexams' : 'exampapers'}/${year}/${secFileid}` },
});

describe('source-bound LCVP video', () => {
  it('retains the official MOV, MP4, original letter-O and deferred identities', () => {
    for (const card of [fixture, forFile(2020, 'LC462CLP031EV.mp4'),
      forFile(2015, 'LC462CLPO31EV.mp4'), forFile(2023, 'LC462CLP031EV.mov', true)]) {
      expect(videoMaterialFault(card, 'lcvp')).toBeNull();
    }
    expect(videoMaterialFault({ ...fixture, videoMaterial: undefined }, 'lcvp')).toBeNull();
  });

  it('rejects another year, sitting, subject, level, language or silently corrected filename', () => {
    expect(videoMaterialFault({ ...fixture, year: 2025 }, 'lcvp')).toContain('examination year');
    expect(videoMaterialFault({ ...fixture, id: 'lcvp-deferred-fixture' }, 'lcvp')).toContain('sitting');
    expect(videoMaterialFault(fixture, 'home-economics')).toContain('LCVP');
    expect(videoMaterialFault({ ...fixture, level: 'higher' }, 'lcvp')).toContain('common-level');
    expect(videoMaterialFault(forFile(2026, 'LC462CLP031IV.mov'), 'lcvp')).toContain('English');
    const original = forFile(2015, 'LC462CLPO31EV.mp4');
    expect(videoMaterialFault({ ...original, videoMaterial: { ...original.videoMaterial!, secFileid: 'LC462CLP031EV.mp4' } }, 'lcvp')).toContain('filename');
  });

  it('refuses incomplete metadata, unsafe URLs and non-video substitutions', () => {
    const invalid = [
      { kind: 'source-audio' }, { presentationNote: ' ' }, { attribution: '' },
      { playbackUrl: 'javascript:alert(1)' }, { playbackUrl: 'https://name:secret@example.test/video.mp4' },
      { canonicalUrl: official.canonicalUrl.replace('www.examinations.ie', 'example.test') },
      { canonicalUrl: official.canonicalUrl + '?year=2026' }, { secFileid: 'LC462CLP000EV.pdf' },
    ];
    for (const patch of invalid) {
      expect(videoMaterialFault({ ...fixture, videoMaterial: { ...official, ...patch } }, 'lcvp')).not.toBeNull();
    }
    expect(videoMaterialFault({ ...fixture, audioMaterial: { kind: 'source-audio' } }, 'lcvp')).toContain('own audio');
  });

  it('shows a native video before reveal even when the printed image replaces the prompt', () => {
    const card: SecQuestionCard = { ...fixture, questionFigure: {
      candId: 'synthetic', src: '/fixture/printed-question.png', srcHash: 'synthetic',
      alt: 'Synthetic printed question', lettersVisible: [], attribution: 'Synthetic test image',
    } };
    const onGrade = vi.fn();
    const { baseElement } = render(<SessionScreen cards={[card]} subjectLabel="LCVP"
      onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    const video = baseElement.querySelector('video')!;
    expect(video).toHaveAttribute('controls');
    expect(video).toHaveAttribute('playsinline');
    expect(video).toHaveAttribute('preload', 'metadata');
    expect(video).toHaveAttribute('src', official.playbackUrl);
    expect(video).not.toHaveAttribute('autoplay');
    expect(video.muted).toBe(false);
    expect(baseElement.querySelector('audio')).toBeNull();
    expect(screen.queryByText(fixture.questionText)).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Fixture answer/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(baseElement.querySelectorAll('video')).toHaveLength(1);
    expect(baseElement.querySelector('video')).toBe(video);
    fireEvent.click(screen.getByRole('button', { name: /Fixture answer/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ marksClaimed: 2, marksAvailable: 2 }));
  });

  it('keeps source guidance and the official link available when playback fails, and recovers for another source', () => {
    const { container, rerender } = render(<VideoSourcePlayer source={official} />);
    fireEvent.error(container.querySelector('video')!);
    expect(screen.getByRole('status')).toHaveTextContent('could not be played');
    expect(screen.getByText(official.presentationNote)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open the official SEC video' })).toHaveAttribute('href', official.canonicalUrl);
    const next = forFile(2020, 'LC462CLP031EV.mp4').videoMaterial!;
    rerender(<VideoSourcePlayer source={next} />);
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
    expect(container.querySelector('video')).toHaveAttribute('src', next.playbackUrl);
  });

  it('keeps separately scored video tasks distinct and excludes them from quick quizzes', () => {
    expect(sessionExerciseCount([fixture, { ...fixture, id: 'synthetic-second-video-task' }])).toBe(2);
    expect(isQuizCard(fixture)).toBe(false);
    expect(isQuizCard({ ...fixture, videoMaterial: undefined })).toBe(true);
  });
});
