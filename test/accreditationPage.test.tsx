import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import AccreditationPage from '@/components/AccreditationPage';

describe('References page', () => {
  test('presents the evidence library with reviewed source detail', () => {
    const openModule = vi.fn();
    render(<AccreditationPage onBack={vi.fn()} onOpenModule={openModule} />);

    expect(screen.getByRole('heading', { name: /The evidence behind\s*every research-led module\./i })).toBeInTheDocument();
    expect(screen.getByRole('tablist', { name: 'Evidence collections' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: "The Driver's Manual", level: 2 })).toBeInTheDocument();
    expect(screen.getByRole('region', { name: 'Module evidence' })).toBeInTheDocument();
    expect(screen.getAllByText('Peer-reviewed').length).toBeGreaterThan(0);
    expect(screen.getByRole('link', { name: /Open DOI record for Possible selves/i })).toHaveAttribute(
      'href',
      'https://doi.org/10.1037/0003-066x.41.9.954',
    );

    fireEvent.click(screen.getByRole('button', { name: /Open the The Driver's Manual module/i }));
    expect(openModule).toHaveBeenCalledWith('agency-protocol');
  });

  test('filters the module index and automatically updates the selected evidence record', () => {
    render(<AccreditationPage onBack={vi.fn()} />);

    fireEvent.change(screen.getByRole('textbox', { name: 'Search modules' }), {
      target: { value: 'Science of Hope' },
    });

    expect(screen.queryByRole('button', { name: "The Driver's Manual, 6 verified sources" })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'The Science of Hope, 5 verified sources' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'The Science of Hope', level: 2 })).toBeInTheDocument();
    expect(screen.getByText('Numbered exactly as the citations inside this module.')).toBeInTheDocument();
  });

  test('does not leave an unrelated evidence record visible when nothing matches', () => {
    render(<AccreditationPage onBack={vi.fn()} />);

    fireEvent.change(screen.getByRole('textbox', { name: 'Search modules' }), {
      target: { value: 'a module that does not exist' },
    });

    expect(screen.getByText('No modules found')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'No evidence record found' })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: "The Driver's Manual", level: 2 })).not.toBeInTheDocument();
  });

  test('switches evidence collections and exposes official source records', () => {
    render(<AccreditationPage onBack={vi.fn()} />);

    const examTab = screen.getByRole('tab', { name: 'Exam' });
    fireEvent.click(examTab);

    expect(examTab).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByRole('heading', { name: 'The Points Playbook', level: 2 })).toBeInTheDocument();
    expect(screen.getAllByText('Official source').length).toBeGreaterThan(0);
    expect(screen.getAllByRole('link', { name: /Open official source/i }).length).toBeGreaterThan(0);

    fireEvent.click(screen.getByRole('button', { name: 'Previous The Context Effect' }));
    expect(screen.getByRole('tab', { name: 'Learning' })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByRole('heading', { name: 'The Context Effect', level: 2 })).toBeInTheDocument();
  });

  test('moves between evidence collection tabs with the keyboard', () => {
    render(<AccreditationPage onBack={vi.fn()} />);

    const allModulesTab = screen.getByRole('tab', { name: 'All modules' });
    allModulesTab.focus();
    fireEvent.keyDown(allModulesTab, { key: 'ArrowRight' });

    const mindsetTab = screen.getByRole('tab', { name: 'Mindset' });
    expect(mindsetTab).toHaveAttribute('aria-selected', 'true');
    expect(mindsetTab).toHaveFocus();
    expect(screen.getByRole('heading', { name: "The Driver's Manual", level: 2 })).toBeInTheDocument();

    fireEvent.keyDown(mindsetTab, { key: 'End' });
    const examTab = screen.getByRole('tab', { name: 'Exam' });
    expect(examTab).toHaveAttribute('aria-selected', 'true');
    expect(examTab).toHaveFocus();
    expect(screen.getByRole('heading', { name: 'The Points Playbook', level: 2 })).toBeInTheDocument();
  });

  test('returns to the module index before leaving on a small screen', () => {
    const originalWidth = window.innerWidth;
    const onBack = vi.fn();
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: 390 });

    try {
      render(<AccreditationPage onBack={onBack} />);
      fireEvent.click(screen.getByRole('button', { name: 'The Science of Hope, 5 verified sources' }));

      fireEvent.click(screen.getByRole('button', { name: 'Go back' }));
      expect(onBack).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole('button', { name: 'Go back' }));
      expect(onBack).toHaveBeenCalledTimes(1);
    } finally {
      Object.defineProperty(window, 'innerWidth', { configurable: true, value: originalWidth });
    }
  });
});
