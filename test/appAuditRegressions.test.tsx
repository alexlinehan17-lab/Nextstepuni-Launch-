/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useRef, useState } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import ReflectionModal from '@/components/ReflectionModal';
import { useModal } from '@/hooks/useModal';
import { isProgressReadyForUser } from '@/utils/progressHydration';

const ROOT = resolve(__dirname, '..');

const ModalHarness: React.FC = () => {
  const [open, setOpen] = useState(false);
  const dialogRef = useRef<HTMLDivElement>(null);
  useModal(open, () => setOpen(false), dialogRef);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)}>Open settings</button>
      {open && (
        <div ref={dialogRef} role="dialog" aria-modal="true" aria-labelledby="test-dialog-title" tabIndex={-1}>
          <h2 id="test-dialog-title">Settings</h2>
          <button type="button">First setting</button>
          <button type="button" onClick={() => setOpen(false)}>Close settings</button>
        </div>
      )}
    </>
  );
};

describe('app audit regressions', () => {
  test('shows an accessible loading state instead of a blank route', () => {
    render(<LoadingSpinner />);
    expect(screen.getByRole('status')).toHaveTextContent('Loading your workspace');
  });

  test('moves focus into a modal, closes on Escape, and restores the trigger', async () => {
    render(<ModalHarness />);
    const trigger = screen.getByRole('button', { name: 'Open settings' });
    trigger.focus();
    fireEvent.click(trigger);

    await waitFor(() => expect(screen.getByRole('button', { name: 'First setting' })).toHaveFocus());
    fireEvent.keyDown(document, { key: 'Escape' });

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(trigger).toHaveFocus();
  });

  test('exposes the study debrief as a focus-managed modal', async () => {
    const onCancel = vi.fn();
    render(
      <ReflectionModal
        isOpen
        subjectName="Mathematics"
        sessionType="practice"
        mode="quick"
        onSubmit={vi.fn()}
        onCancel={onCancel}
      />,
    );

    const dialog = screen.getByRole('dialog', { name: 'Quick Debrief' });
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    await waitFor(() => expect(screen.getByRole('button', { name: 'Close' })).toHaveFocus());
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onCancel).toHaveBeenCalledOnce();
  });

  test('does not treat logged-out or another student\'s progress as hydrated', () => {
    expect(isProgressReadyForUser('student-a', true, null)).toBe(false);
    expect(isProgressReadyForUser('student-a', true, 'student-b')).toBe(false);
    expect(isProgressReadyForUser('student-a', false, 'student-a')).toBe(false);
    expect(isProgressReadyForUser('student-a', true, 'student-a')).toBe(true);
  });

  test('keeps login fields labelled and validation errors announced', () => {
    const source = readFileSync(resolve(ROOT, 'components/LoginPage.tsx'), 'utf8');
    expect(source.match(/<label\b/g)?.length).toBeGreaterThan(0);
    expect(source).not.toMatch(/<label(?![^>]*htmlFor)/);
    expect(source).not.toMatch(/errorAnim} className="text-sm text-red-500/);
    expect(source).toContain('role="alert" aria-live="assertive"');
  });

  test('keeps the audited icon buttons and level filters named', () => {
    const router = readFileSync(resolve(ROOT, 'components/AppRouter.tsx'), 'utf8');
    const shop = readFileSync(resolve(ROOT, 'components/journey/IslandShopDrawer.tsx'), 'utf8');
    const profile = readFileSync(resolve(ROOT, 'components/UserProfileMenu.tsx'), 'utf8');
    const catchUp = readFileSync(resolve(ROOT, 'components/CatchUpLane/index.tsx'), 'utf8');
    const commandWords = readFileSync(resolve(ROOT, 'components/CommandWordReflex/index.tsx'), 'utf8');
    expect(router).toContain('aria-label="Back to modules"');
    expect(shop).toContain("'Close Island Shop'");
    expect(profile).toContain('aria-label="Close profile"');
    expect(catchUp).toContain('aria-pressed={levelFilter === lv}');
    expect(commandWords).toContain('aria-pressed={levelFilter === lv}');
  });

  test('does not duplicate Comeback Engine heading chrome or animate theme colours out of sync', () => {
    const innovation = readFileSync(resolve(ROOT, 'components/InnovationZone.tsx'), 'utf8');
    const sectionCard = readFileSync(resolve(ROOT, 'components/SectionCard.tsx'), 'utf8');
    expect(innovation).toMatch(/'comeback':[\s\S]*?showHeader: false/);
    expect(sectionCard).not.toContain('rounded-2xl transition-all duration-200');
  });
});
