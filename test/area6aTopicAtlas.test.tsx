/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 6a: Topic Atlas in the agreed look. Where a subject files its topics
 * under level headings, Higher and Ordinary can be chosen: each choice shows
 * that level's headings, together they show every topic once, and each row's
 * count is the same count the data gives (topicsForSubject). A topic's
 * questions are grouped by year, newest first, and the bar's one Back returns
 * from a topic to the map.
 */
import React from 'react';
import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, screen, within } from '@testing-library/react';
import { loadAllAtlasModels } from '@/components/PaperTrail/atlasModel';
import ReviseByTopic from '@/components/PaperTrail/ReviseByTopic';
import { strandsFor, taggedSubjects, topicsForSubject } from '@/components/PaperTrail/topics';
import { NavigationProvider, useNavigation } from '@/contexts/NavigationContext';

const label = (id: string) => id.charAt(0).toUpperCase() + id.slice(1);
const noop = vi.fn();
const levelled = (id: string) => strandsFor(id, topicsForSubject(id).map(t => t.subtopicId))
  .some(s => s.name.startsWith('Higher Level')) && strandsFor(id, topicsForSubject(id).map(t => t.subtopicId)).some(s => s.name.startsWith('Ordinary Level'));

beforeAll(() => loadAllAtlasModels());
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('fetch', vi.fn(() => Promise.reject(new Error('no network in jsdom'))));
});

const rows = () => [...document.querySelectorAll<HTMLButtonElement>('.ta-topic')].map(b => ({
  title: b.querySelector('.ta-topic-title')?.textContent ?? '',
  count: Number(b.querySelector('.ta-count')?.textContent ?? NaN),
}));

describe('Topic Atlas in the agreed look', () => {
  it('chooses Higher or Ordinary where the topics are filed by level, keeping every topic and every count', () => {
    const sid = taggedSubjects().find(levelled);
    expect(sid, 'a subject that files its topics by level').toBeTruthy();
    render(<ReviseByTopic subjects={[{ id: sid!, label: label(sid!) }]} mineIds={[]} subjectLabel={label} onOpenQuestion={noop} onBack={noop} />);
    const bar = screen.getByRole('radiogroup', { name: 'Level' });
    expect(within(bar).getByRole('radio', { name: 'Higher' })).toHaveAttribute('aria-checked', 'true');
    const higher = rows();
    expect(screen.getAllByRole('heading', { level: 3 }).every(h => !/^Ordinary Level/.test(h.textContent ?? ''))).toBe(true);
    fireEvent.click(within(bar).getByRole('radio', { name: 'Ordinary' }));
    const ordinary = rows();
    expect(screen.getAllByRole('heading', { level: 3 }).every(h => !/^Higher Level/.test(h.textContent ?? ''))).toBe(true);
    // Every topic once across the two choices, each with the data's count.
    const counts = new Map(topicsForSubject(sid!).map(t => [t.label + '|' + t.count, t]));
    const shown = [...higher, ...ordinary];
    expect(shown.length).toBe(topicsForSubject(sid!).length);
    for (const row of shown) expect(counts.has(row.title + '|' + row.count), `${row.title} ${row.count}`).toBe(true);
  });

  it('marks each year a topic came up, one mark per year of the subject', () => {
    const sid = taggedSubjects()[0];
    render(<ReviseByTopic subjects={[{ id: sid, label: label(sid) }]} mineIds={[]} subjectLabel={label} onOpenQuestion={noop} onBack={noop} />);
    const first = document.querySelector('.ta-topic')!;
    const marks = first.querySelector('.ta-marks')!;
    const t = topicsForSubject(sid).find(x => x.label === first.querySelector('.ta-topic-title')?.textContent)!;
    expect(marks.querySelectorAll('i.on')).toHaveLength(t.years);
  });

  it('groups a topic’s questions by year, newest first, and Back returns to the map', async () => {
    const sid = taggedSubjects().find(levelled) ?? taggedSubjects()[0];
    const FrameBack = () => { const nav = useNavigation(); return <button onClick={nav.goBack}>Back</button>; };
    render(<NavigationProvider><FrameBack /><ReviseByTopic subjects={[{ id: sid, label: label(sid) }]} mineIds={[]} subjectLabel={label} onOpenQuestion={noop} onBack={noop} /></NavigationProvider>);
    fireEvent.click(document.querySelector<HTMLButtonElement>('.ta-topic')!);
    const years = [...document.querySelectorAll('.ta-year-num')].map(n => Number(n.textContent));
    expect(years.length).toBeGreaterThan(0);
    expect([...years].sort((a, b) => b - a)).toEqual(years);
    expect(new Set(years).size).toBe(years.length);
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'Back' })); });
    expect(screen.getByRole('heading', { name: 'Every question, mapped by topic.' })).toBeInTheDocument();
  });
});
