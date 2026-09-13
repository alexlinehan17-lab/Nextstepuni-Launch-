import React from 'react';
import { fireEvent, render, screen, within, cleanup } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';
import KanbanBoard from '@/components/activities/KanbanBoard';
import CornellNoteSimulator from '@/components/activities/CornellNoteSimulator';

afterEach(cleanup);
describe('mobile lesson activities', () => {
  it('moves a task through stages, retaining its text and counting each task once', () => {
    render(<KanbanBoard />);
    const name = 'Write Macbeth Quote Bank';
    fireEvent.change(screen.getByRole('combobox', { name: `Move ${name}` }), { target: { value: 'doing' } });
    expect(within(screen.getByRole('region', { name: 'In progress' })).getByText(name)).toBeInTheDocument();
    fireEvent.change(screen.getByRole('combobox', { name: `Move ${name}` }), { target: { value: 'done' } });
    expect(within(screen.getByRole('region', { name: 'Done' })).getByLabelText('1 task')).toBeInTheDocument();
    fireEvent.change(screen.getByRole('combobox', { name: `Move ${name}` }), { target: { value: 'todo' } });
    fireEvent.change(screen.getByRole('combobox', { name: `Move ${name}` }), { target: { value: 'done' } });
    expect(within(screen.getByRole('region', { name: 'Done' })).getByLabelText('1 task')).toBeInTheDocument();
    expect(screen.getAllByRole('combobox')).toHaveLength(3);
  });
  it('keeps Cornell writing through feedback, invalidates feedback on edit, and resets all fields', () => {
    render(<CornellNoteSimulator />);
    const notes = screen.getByRole('textbox', { name: '1. Main notes' });
    const cues = screen.getByRole('textbox', { name: '2. Cue questions' });
    const summary = screen.getByRole('textbox', { name: '3. Summary' });
    fireEvent.click(screen.getByRole('button', { name: 'Check my notes' }));
    expect(screen.getByRole('status')).toHaveTextContent('Main notes are empty');
    fireEvent.change(notes, { target: { value: 'Water moves across a partially permeable membrane without energy.' } });
    fireEvent.change(cues, { target: { value: 'What is osmosis?\nWhy does it need no energy?' } });
    fireEvent.change(summary, { target: { value: 'Water moves passively down its concentration gradient through a membrane.' } });
    fireEvent.click(screen.getByRole('button', { name: 'Check my notes' }));
    expect(screen.getByRole('status')).toHaveTextContent('Ready to practise recall');
    expect(notes).toHaveValue('Water moves across a partially permeable membrane without energy.');
    fireEvent.change(cues, { target: { value: 'What is osmosis?' } });
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reset' }));
    for (const field of [notes, cues, summary]) expect(field).toHaveValue('');
  });
});
