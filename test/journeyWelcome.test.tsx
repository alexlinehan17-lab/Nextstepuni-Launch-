import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import JourneyWelcome from '../components/journey/JourneyWelcome';
import SettingsModal from '../components/SettingsModal';
import type { UserSettings } from '../types';

describe('Journey introduction', () => {
  it('opens on first entry, records dismissal, and can be reopened without saving again', async () => {
    const dismiss = vi.fn();
    const view = render(<JourneyWelcome hasSeenWelcome={false} onDismissWelcome={dismiss} />);
    expect(screen.getByRole('dialog')).toHaveTextContent('Journey Points (JP)');
    expect(screen.getByRole('dialog')).toHaveTextContent('Fieldbook');
    expect(document.body.style.overflow).toBe('hidden');
    fireEvent.click(screen.getByRole('button', { name: 'Explore my island' }));
    expect(dismiss).toHaveBeenCalledOnce();
    view.rerender(<JourneyWelcome hasSeenWelcome onDismissWelcome={dismiss} />);
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    expect(document.body.style.overflow).not.toBe('hidden');
    fireEvent.click(screen.getByRole('button', { name: 'How Journey works' }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Close Journey introduction' }));
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    expect(dismiss).toHaveBeenCalledOnce();
  });

  it('respects a returning student’s saved dismissal and introduces a different student', () => {
    const view = render(<JourneyWelcome key="returning-student" hasSeenWelcome onDismissWelcome={vi.fn()} />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    view.rerender(<JourneyWelcome key="new-student" hasSeenWelcome={false} onDismissWelcome={vi.fn()} />);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('contains keyboard focus, closes with Escape, and returns focus to the help button', async () => {
    const dismiss = vi.fn();
    render(<JourneyWelcome hasSeenWelcome onDismissWelcome={dismiss} />);
    const help = screen.getByRole('button', { name: 'How Journey works' });
    help.focus();
    fireEvent.click(help);
    const first = screen.getByRole('button', { name: 'Close Journey introduction' });
    const last = screen.getByRole('button', { name: 'Explore my island' });
    await waitFor(() => expect(first).toHaveFocus());
    fireEvent.keyDown(first, { key: 'Tab', shiftKey: true });
    expect(last).toHaveFocus();
    fireEvent.keyDown(last, { key: 'Tab' });
    expect(first).toHaveFocus();
    fireEvent.keyDown(first, { key: 'Escape' });
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    expect(help).toHaveFocus();
    expect(dismiss).not.toHaveBeenCalled();
  });

  it('treats Escape on first entry as a dismissal', async () => {
    const dismiss = vi.fn();
    render(<JourneyWelcome hasSeenWelcome={false} onDismissWelcome={dismiss} />);
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(dismiss).toHaveBeenCalledOnce();
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
});

it('Settings offers only the eight Star Crew characters and saves the selected character', () => {
  const updateSetting = vi.fn();
  const settings: UserSettings = { language: 'en', avatar: 'star-crew:reader', darkMode: false, defaultWorkMinutes: 25, showDashboard: false };
  render(<SettingsModal isOpen onClose={vi.fn()} settings={settings} updateSetting={updateSetting} />);
  expect(screen.getAllByRole('button', { name: /^Select .* avatar$/ })).toHaveLength(8);
  expect(screen.queryByRole('button', { name: /Unlock avatar/ })).not.toBeInTheDocument();
  expect(screen.queryByText(/JP available/)).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Select The Reader avatar' })).toHaveAttribute('aria-pressed', 'true');
  fireEvent.click(screen.getByRole('button', { name: 'Select The Musician avatar' }));
  expect(updateSetting).toHaveBeenCalledExactlyOnceWith('avatar', 'star-crew:musician');
});
