import React from 'react';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import Avatar from '../components/Avatar';
import SubjectAvatar from '../components/SubjectAvatar';
import HomeNextStep from '../components/HomeNextStep';
import StudySessionSetup from '../components/study/StudySessionSetup';
import { PERSONAL_STAR_CREW } from '../data/personalStarCrew';
import { SUBJECT_STAR_CREW, getSubjectStarCrew } from '../data/subjectStarCrew';
import { getAvatarUrl } from '../utils/authUtils';

describe('approved Star Crew', () => {
  it('offers exactly the selected eight and packages all 43 subject illustrations', () => {
    expect(PERSONAL_STAR_CREW.map(avatar => avatar.name)).toEqual([
      'The Beanie', 'The Reader', 'The Skater', 'The Maker',
      'The Stargazer', 'The Hugger', 'The Snoozer', 'The Musician',
    ]);
    expect(Object.keys(SUBJECT_STAR_CREW)).toHaveLength(43);
    for (const artwork of [...PERSONAL_STAR_CREW, ...Object.values(SUBJECT_STAR_CREW)]) {
      const path = resolve('public', artwork.src.slice(1));
      expect(existsSync(path), artwork.src).toBe(true);
      expect(readFileSync(path).subarray(1, 4).toString()).toBe('PNG');
    }
    expect(getSubjectStarCrew('Ancient Greek')?.src).toContain('ancient-greek-v4.png');
    expect(getSubjectStarCrew('DCG')?.src).toContain('graphics-v3.png');
    expect(getSubjectStarCrew('Religious Education')?.src).toContain('education-v3.png');
    expect(getSubjectStarCrew('Music')?.src).not.toBe(getAvatarUrl('star-crew:musician'));
  });

  it.each([
    ['irish', 'Irish (Gaeilge)', 'gaeilge'],
    ['mathematics', 'Mathematics', 'Maths'],
    ['applied-mathematics', 'Applied Mathematics', 'Applied Maths'],
    ['politics-and-society', 'Politics & Society', 'Politics and Society'],
    ['design-and-communication-graphics', 'Design & Communication Graphics', 'DCG'],
  ])('resolves existing saved subject names for %s', (id, label, alias) => {
    expect(getSubjectStarCrew(label)).toBe(SUBJECT_STAR_CREW[id]);
    expect(getSubjectStarCrew(alias)).toBe(SUBJECT_STAR_CREW[id]);
  });

  it('keeps legacy and purchased profile seeds working', () => {
    for (const seed of ['Maya Angelou', 'Luna']) {
      expect(getAvatarUrl(seed)).toContain(`seed=${encodeURIComponent(seed)}`);
    }
    expect(getAvatarUrl('star-crew:maker')).toMatch(/^\/assets\/star-crew\//);
  });

  it('falls back if local artwork fails and retries the next character', () => {
    const view = render(<Avatar seed="star-crew:maker" alt="Your character" />);
    fireEvent.error(view.container.querySelector('img')!);
    expect(view.container.querySelector('img')?.src).toMatch(/^data:image\/svg/);
    view.rerender(<Avatar seed="star-crew:reader" alt="Your character" />);
    expect(view.container.querySelector('img')?.getAttribute('src')).toMatch(/original-four.png$/);
    expect(screen.getByRole('img', { name: 'Your character' })).toBeInTheDocument();
  });

  it('keeps unknown subjects readable without substituting unrelated artwork', () => {
    const view = render(<SubjectAvatar subject="Science" />);
    expect(getSubjectStarCrew('Science')).toBeUndefined();
    expect(view.container).toHaveTextContent('SC');
    expect(view.container.querySelector('img')).toBeNull();
  });

  it('retains the existing home row action and accessible subject name', () => {
    const onPlannedStudy = vi.fn();
    const block = { subjectName: 'Irish', durationMinutes: 25, sessionType: 'revision' as const };
    const view = render(<HomeNextStep blocks={[block]} completions={[]} hasProfile onPlannedStudy={onPlannedStudy} onProgress={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Study Irish: Revision, 25 minutes' }));
    expect(onPlannedStudy).toHaveBeenCalledWith(block, 0);
    expect(view.container.querySelector('.home-plan-row img')?.getAttribute('src')).toContain('irish-v3.png');
  });

  it('keeps study subject and timetable selection connected to the original controls', () => {
    const onSubject = vi.fn(), onBlock = vi.fn();
    const block = { subject: 'Music', durationMinutes: 25, sessionType: 'practice' as const, blockId: 'music-1', dateKey: '2026-09-15' };
    const view = render(<StudySessionSetup subjects={[{ subjectName: 'Irish', level: 'higher' }, { subjectName: 'Music', level: 'higher' }]} selectedSubject="Irish" selectedType="practice" selectedMinutes={25} onSubject={onSubject} onBlock={onBlock} todayBlocks={[block]} onType={vi.fn()} onMinutes={vi.fn()} sessionCount={0} todayMinutes={0} reflectionCount={0} onReflections={vi.fn()} onBack={vi.fn()} onStart={vi.fn()} canStart startHint={null} />);
    fireEvent.click(screen.getByRole('button', { name: 'Music' }));
    expect(onSubject).toHaveBeenCalledWith('Music');
    fireEvent.click(screen.getByRole('button', { name: 'Set up Music, 25 minutes' }));
    expect(onBlock).toHaveBeenCalledWith(block);
    expect(view.container.querySelectorAll('.ss-subjects .subject-avatar')).toHaveLength(2);
    expect(screen.getByRole('button', { name: 'Irish' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: 'Start Session' })).toBeEnabled();
  });
});
