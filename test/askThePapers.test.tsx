import React from 'react';
import fs from 'node:fs';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import AskThePapers from '../components/landing/sections/AskThePapers';
import { loadAsk, matchingTopics, matches, queryTerms, type AskIndexFile, type AskQuestion } from '../components/landing/fx-e/ask';
import { buildAskTopicIndex } from '../scripts/landing/askTopicIndex';

const dir = path.resolve(__dirname, '../public/assets/landing/ask');
const index: AskIndexFile = JSON.parse(fs.readFileSync(path.join(dir, 'index.json'), 'utf8'));
const fetchIndex = vi.fn(async (url: string) => ({ ok: true, json: async () => JSON.parse(fs.readFileSync(path.join(dir, path.basename(url)), 'utf8')) }));
vi.mock('../components/landing/glass/AskPaperViewer', () => ({
  default: ({ question }: { question: AskQuestion }) => <div role="dialog" aria-label="Selected paper">{question.paper.y}/{question.paper.f}/{question.anchor}</div>,
}));
beforeEach(() => { fetchIndex.mockClear(); vi.stubGlobal('fetch', fetchIndex); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('Ask the papers — real word and topic indexes', () => {
  it('finds Trigonometry across the tagged years independently of the printed word', async () => {
    const data = await loadAsk(index);
    const terms = queryTerms('Trigonometry');
    const wordHits = data.questions.filter(q => q.subject.id === 'mathematics' && matches(q, terms));
    const topicHits = data.topicQuestions.filter(q => q.subject.id === 'mathematics' && matchingTopics(q, terms).length);
    expect([...new Set(wordHits.map(q => q.paper.y))].sort()).toEqual([2010, 2022]);
    // Typing the prefix also finds the printed word “trigonometric” in 2013.
    expect([...new Set(data.questions.filter(q => q.subject.id === 'mathematics' && matches(q, queryTerms('trigonom'))).map(q => q.paper.y))].sort()).toEqual([2010, 2013, 2022]);
    expect([...new Set(topicHits.map(q => q.paper.y))].sort()).toEqual(index.years);
    expect(topicHits).toContainEqual(expect.objectContaining({ anchor: '3', page: 8, paper: expect.objectContaining({ y: 2024, f: 'LC003ALP200EV.pdf' }) }));
    // The newer exam-topic crosswalk calls this Geometry; the original tag
    // still identifies Trigonometry, and must not disappear from search.
    expect(topicHits).toContainEqual(expect.objectContaining({ anchor: '8', paper: expect.objectContaining({ y: 2012, f: 'LC003ALP230EV.pdf' }) }));
  });

  it('keeps the shipped topic index in sync with Paper Trail and its exact anchors', () => {
    const generated = buildAskTopicIndex(index, (year, file) => {
      const anchors = new Map<string, number>();
      for (const base of ['scripts/paper-trail/answers', 'public/paper-anchors']) {
        const p = path.resolve(__dirname, '..', base, String(year), `${file}.json`);
        if (!fs.existsSync(p)) continue;
        for (const q of JSON.parse(fs.readFileSync(p, 'utf8')).q ?? []) {
          if (Number.isInteger(q.pP) && q.pP > 0) anchors.set(q.n, q.pP);
        }
      }
      return anchors;
    });
    expect(generated).toEqual(JSON.parse(fs.readFileSync(path.join(dir, 'topics.json'), 'utf8')));
    expect(generated.q.length).toBeGreaterThan(2000);
    expect(generated.q.every(([, , page, topics]) => page > 0 && topics.length > 0)).toBe(true);
    const identities = generated.q.map(([pi, n]) => `${generated.papers[pi].subjectId}/${generated.papers[pi].y}/${generated.papers[pi].f}/${n}`);
    expect(new Set(identities).size).toBe(identities.length);
  });

  it('does not combine words from unrelated topic tags into a false match', async () => {
    const q = (await loadAsk(index)).topicQuestions[0];
    const withTopics = { ...q, topics: [
      { id: 'a', label: 'Cell structure', aliases: [] },
      { id: 'b', label: 'Plant transport', aliases: [] },
    ] };
    expect(matchingTopics(withTopics, queryTerms('cell transport'))).toEqual([]);
    expect(matchingTopics(withTopics, queryTerms('cell struc'))).toHaveLength(1);
    expect(matchingTopics(withTopics, [])).toEqual([]);
  });

  it('preserves the query when switching modes, clears old results and opens the exact topic question', async () => {
    render(<AskThePapers />);
    const input = screen.getByRole('searchbox', { name: 'Search the papers' });
    fireEvent.change(input, { target: { value: 'Trigonometry' } });
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('across 16 years'));
    fireEvent.click(screen.getByRole('button', { name: /^Maths 2024: \d+ questions?$/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Open Maths 2024 Paper Two Q3' }));
    expect(await screen.findByRole('dialog')).toHaveTextContent('2024/LC003ALP200EV.pdf/3');
    fireEvent.click(screen.getByRole('tab', { name: 'Words' }));
    expect(input).toHaveValue('Trigonometry');
    expect(screen.getByRole('status')).toHaveTextContent('across 2 years');
    expect(screen.queryByRole('button', { name: 'Open Maths 2024 Paper Two Q3' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('tab', { name: 'Topics' }));
    expect(screen.getByRole('status')).toHaveTextContent('across 16 years');
    fireEvent.change(input, { target: { value: '' } });
    expect(screen.getByRole('status')).toHaveTextContent('The grid lights as you type.');
  });

  it('recovers from a failed download without losing the query', async () => {
    render(<AskThePapers />);
    await waitFor(() => expect(screen.getByRole('group', { name: 'Years by subject' })).toBeInTheDocument());
    fetchIndex.mockRejectedValueOnce(new Error('offline'));
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'Trigonometry' } });
    fireEvent.click(await screen.findByRole('button', { name: 'Try again' }));
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('across 16 years'));
  });
});
