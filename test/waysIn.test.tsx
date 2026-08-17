/**
 * Ways In — source fidelity, support-path behaviour and answer-leak guards.
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import type { PDFDocumentProxy } from 'pdfjs-dist';

import WaysInWorkspace from '@/components/WaysIn/WaysInWorkspace';
import WaysInHub from '@/components/WaysIn/WaysInHub';
import { buildQuestionModel, findCommandDemand } from '@/components/WaysIn/questionModel';
import { markBankAnswerIdeaCount, waysInSourceFromMarkBank } from '@/components/WaysIn/sources';
import { extractQuestionText } from '@/components/PaperTrail/questionText';
import type { WaysInQuestionSource } from '@/components/WaysIn/types';
import type { MarkRow, SecCard } from '@/types/markBank';

const row = (id: string, verbatim: string, marks = 3): MarkRow => ({
  id, kind: 'point', verbatim, marks,
});

const card: SecCard = {
  source: 'sec', kind: 'question',
  id: 'biology-2025-hl-q7-f', subjectId: 'biology', level: 'higher',
  topicId: 'bio-u1', conceptId: 'scientific-theory',
  year: 2025, paperFileid: 'paper', section: 'A', questionRef: '2025 HL Q7(f)',
  stem: 'Answer the following question in relation to the scientific method.',
  questionText: 'Explain what is meant by the term theory. Give two features in your answer.',
  tariffModel: { kind: 'fixed' }, totalMarks: 6,
  rows: [row('r1', 'Supported hypothesis'), row('r2', 'Repeated experimental evidence')],
  schemeCitation: 'SEC Biology 2025', specVersion: 'lc-biology-2025',
  qa: { gates: [], humanReviewedBy: 'reviewer', humanReviewedAt: '2026-08-01' },
};

const source: WaysInQuestionSource = waysInSourceFromMarkBank(card, 'Biology');

beforeEach(() => window.localStorage.clear());

describe('Ways In question model', () => {
  test('keeps the exact question and finds the job, constraints and answer shape', () => {
    const model = buildQuestionModel(source);
    expect(model.exactText).toBe(card.questionText);
    expect(model.command?.surface.toLowerCase()).toBe('explain');
    expect(model.command?.requiredAction).toMatch(/how or why/i);
    expect(model.constraints.join(' ')).toMatch(/two features/i);
    expect(model.expectedPoints).toBe(2);
    expect(model.steps.map(step => step.id)).toEqual(['meet', 'job', 'boundaries', 'shape', 'attempt', 'return']);
  });

  test('passes only tariff shape into Ways In, never marking-scheme content', () => {
    const serialised = JSON.stringify(source);
    expect(serialised).not.toContain('Supported hypothesis');
    expect(serialised).not.toContain('Repeated experimental evidence');
    expect(source.answerShape).toMatchObject({ points: 2, totalMarks: 6 });
  });

  test('uses the first printed command when a question contains more than one verb', () => {
    expect(findCommandDemand('State one feature. Then explain why it matters.')?.surface.toLowerCase()).toBe('state');
  });

  test('turns any-N and mutually exclusive routes into reachable answer spaces', () => {
    const anyN: SecCard = {
      ...card,
      rows: [{
        id: 'group', kind: 'anyN', verbatim: 'Any four', marks: null,
        group: { claimMax: 4, perOption: 3, options: ['a', 'b', 'c', 'd', 'e'] },
      }],
    };
    expect(markBankAnswerIdeaCount(anyN)).toBe(4);

    const routed = {
      ...card,
      rows: [
        row('common', 'Common'),
        { ...row('a1', 'Route A 1'), route: 'a' },
        { ...row('a2', 'Route A 2'), route: 'a' },
        { ...row('b1', 'Route B'), route: 'b' },
      ],
    } satisfies SecCard;
    expect(markBankAnswerIdeaCount(routed)).toBe(3);
  });

  test('admits when image-only Paper Trail text cannot be parsed', () => {
    const imageOnly = buildQuestionModel({
      ...source,
      id: 'paper-trail:image-only',
      origin: 'paper-trail',
      questionText: '',
      textConfidence: 'image-only',
    });
    expect(imageOnly.command).toBeNull();
    expect(imageOnly.lines).toEqual([]);
  });
});

describe('Paper Trail source handoff', () => {
  test('extracts only searchable text inside the verified crop', async () => {
    const cleanup = vi.fn();
    const pdf = {
      getPage: vi.fn().mockResolvedValue({
        getViewport: () => ({ width: 1000, height: 1000, transform: [1, 0, 0, -1, 0, 1000] }),
        getTextContent: vi.fn().mockResolvedValue({ items: [
          { str: 'Explain', width: 45, height: 10, transform: [10, 0, 0, 10, 100, 800] },
          { str: 'photosynthesis.', width: 92, height: 10, transform: [10, 0, 0, 10, 150, 800] },
          { str: 'Text outside this question crop', width: 180, height: 10, transform: [10, 0, 0, 10, 100, 300] },
        ] }),
        cleanup,
      }),
    } as unknown as PDFDocumentProxy;

    const extracted = await extractQuestionText(pdf, [{ p: 1, r: [0, 0.1, 1, 0.4] }]);
    expect(extracted).toEqual({
      text: 'Explain photosynthesis.',
      lines: ['Explain photosynthesis.'],
      confidence: 'pdf-text',
    });
    expect(cleanup).toHaveBeenCalledTimes(1);
  });
});

describe('Ways In workspace', () => {
  test('runs the six-stage path and preserves an unfinished draft on-device', () => {
    const onClose = vi.fn();
    render(<WaysInWorkspace source={source} onClose={onClose} />);

    expect(screen.getByText('Find a way into this question.')).toBeInTheDocument();
    expect(screen.getByText(card.questionText)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /One step at a time/i }));
    expect(screen.getByRole('heading', { name: 'Meet the exact question' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /go to step 5/i }));
    const draft = screen.getByLabelText('Your attempt');
    fireEvent.change(draft, { target: { value: 'A theory is supported by evidence.' } });
    expect(window.localStorage.getItem(`nextstepuni:ways-in:${source.id}`)).toContain('supported by evidence');
    expect(onClose).not.toHaveBeenCalled();
  });

  test('shows a task map, editable empty answer shape and colour key without scheme answers', () => {
    render(<WaysInWorkspace source={source} initialMode="show-me" onClose={vi.fn()} />);
    expect(screen.getByRole('heading', { name: 'See the shape before you answer.' })).toBeInTheDocument();
    expect(screen.getByRole('list', { name: 'Question task map' })).toBeInTheDocument();
    expect(screen.queryByText('Supported hypothesis')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: /Answer shape/i }));
    expect(screen.getAllByPlaceholderText('Your idea—not the scheme')).toHaveLength(2);
    fireEvent.change(screen.getByLabelText('Plan answer idea 1'), { target: { value: 'First idea' } });
    expect(window.localStorage.getItem(`nextstepuni:ways-in:${source.id}`)).toContain('First idea');

    fireEvent.click(screen.getByRole('tab', { name: /Question colours/i }));
    const actionMark = document.querySelector('.wi-colour-question .wi-mark--action');
    expect(actionMark).toHaveTextContent('Explain');
  });

  test('can return to the source without grading the question', () => {
    const onClose = vi.fn();
    render(<WaysInWorkspace source={source} initialMode="one-step" onClose={onClose} />);
    fireEvent.click(screen.getByRole('button', { name: /go to step 6/i }));
    screen.getAllByRole('button', { name: /My answer|I respected|I can see/i }).forEach(button => fireEvent.click(button));
    fireEvent.click(screen.getByRole('button', { name: /Return to the original question/i }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});

describe('Ways In Launchpad hub', () => {
  test('routes students to the two trusted question sources', () => {
    const onOpenTool = vi.fn();
    render(<WaysInHub onOpenTool={onOpenTool} />);
    fireEvent.click(screen.getByRole('button', { name: /Choose from Mark Bank/i }));
    expect(onOpenTool).toHaveBeenCalledWith('mark-bank');
    fireEvent.click(screen.getByRole('button', { name: /Choose from Paper Trail/i }));
    expect(onOpenTool).toHaveBeenCalledWith('paper-trail');
  });
});
