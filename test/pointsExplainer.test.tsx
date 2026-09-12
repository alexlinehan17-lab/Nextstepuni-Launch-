import React, { useState } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import PointsExplainer from '../components/PointsExplainer';

function PrimerHarness() {
  const [open, setOpen] = useState(false);
  return <><button onClick={() => setOpen(true)}>About JP</button><PointsExplainer isOpen={open} onDismiss={() => setOpen(false)} /></>;
}

describe('Journey Points primer', () => {
  it('contains keyboard focus, locks page scrolling and restores the trigger on dismissal', async () => {
    render(<PrimerHarness />);
    const trigger = screen.getByRole('button', { name: 'About JP' });
    trigger.focus();
    fireEvent.click(trigger);
    const close = screen.getByRole('button', { name: 'Close' });
    await waitFor(() => expect(close).toHaveFocus());
    expect(document.body.style.overflow).toBe('hidden');
    fireEvent.keyDown(document, { key: 'Tab', shiftKey: true });
    expect(screen.getByRole('button', { name: 'Got it' })).toHaveFocus();
    fireEvent.keyDown(document, { key: 'Tab' });
    expect(close).toHaveFocus();
    fireEvent.keyDown(document, { key: 'Escape' });
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    expect(document.body.style.overflow).not.toBe('hidden');
    expect(trigger).toHaveFocus();
  });
});
