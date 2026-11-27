/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared parts extended for Mark Bank (area 6b, 27 Nov 2026): a row with its
 * number, a thin bar and a count, a row chosen in place, and a menu whose
 * button is a screen's own box with a selection bar and rows with a character.
 */
import { describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, screen } from '@testing-library/react';
import { List, Row } from '../components/ui/List';
import { MenuLabel, MenuPanel, MenuRadioRows, MenuSegment } from '../components/ui/Menu';

describe('Row: a number, a bar and a count', () => {
  it('draws the number at the left, a bar for the share done, and the count', () => {
    render(<List><Row lead="2.1" title="Enzymes" progress={41 / 151} value="41 / 151" onPress={() => {}} /></List>);
    const row = screen.getByRole('button', { name: /Enzymes/ });
    expect(row.querySelector('.ui-row-lead')).toHaveTextContent('2.1');
    expect((row.querySelector('.ui-row-bar > i') as HTMLElement).style.width).toBe(`${(41 / 151) * 100}%`);
    expect(row.querySelector('.ui-row-value')).toHaveTextContent('41 / 151');
    expect(row.querySelector('.ui-row-chev')).not.toBeNull();
  });

  it('keeps the bar inside 0 to 1', () => {
    render(<List><Row title="All topics" progress={3} /><Row title="None" progress={-1} /></List>);
    const bars = document.querySelectorAll<HTMLElement>('.ui-row-bar > i');
    expect(bars[0].style.width).toBe('100%');
    expect(bars[1].style.width).toBe('0%');
  });

  it('a row chosen in place says so and carries no chevron', () => {
    const press = vi.fn();
    render(<List>
      <Row title="Photosynthesis" selected onPress={press} />
      <Row title="Respiration" selected={false} onPress={press} />
    </List>);
    const chosen = screen.getByRole('button', { name: 'Photosynthesis' });
    expect(chosen).toHaveAttribute('aria-pressed', 'true');
    expect(chosen).toHaveClass('ui-row--select');
    expect(chosen.querySelector('.ui-row-chev')).toBeNull();
    expect(screen.getByRole('button', { name: 'Respiration' })).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(screen.getByRole('button', { name: 'Respiration' }));
    expect(press).toHaveBeenCalledOnce();
  });
});

describe('MenuPanel with a box for its button, a selection bar and rows with a character', () => {
  const setup = () => {
    const onLevel = vi.fn();
    const onSubject = vi.fn();
    render(
      <MenuPanel label="Change subject or level" buttonLabel="Change subject or level: Biology" face={<span>Biology</span>}
        align="start" buttonClassName="mb-subject" className="mb-subject-menu">
        <MenuLabel>Paper level</MenuLabel>
        <MenuSegment label="Paper level" value="higher" onChange={onLevel} options={[{ value: 'higher', label: 'Higher' }, { value: 'ordinary', label: 'Ordinary' }]} />
        <MenuLabel>Your subjects</MenuLabel>
        <MenuRadioRows label="Your subjects" value="biology" onChange={onSubject}
          options={[{ value: 'accounting', label: 'Accounting', art: <img alt="" /> }, { value: 'biology', label: 'Biology', art: <img alt="" /> }]} />
      </MenuPanel>,
    );
    return { onLevel, onSubject };
  };

  it('the button is the screen\'s own box', () => {
    setup();
    const button = screen.getByRole('button', { name: 'Change subject or level: Biology' });
    expect(button).toHaveClass('mb-subject');
    expect(button).not.toHaveClass('ui-menu-btn');
  });

  it('opens with the level as a selection bar and the subjects ticked, and a choice applies at once', async () => {
    const { onLevel, onSubject } = setup();
    await tap(screen.getByRole('button', { name: 'Change subject or level: Biology' }));
    const menu = await screen.findByRole('menu', { name: /Change subject or level/ });
    expect(menu).toHaveClass('mb-subject-menu');
    expect(screen.getByRole('menuitemradio', { name: 'Higher' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('menuitemradio', { name: 'Biology' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('menuitemradio', { name: 'Accounting' })).toHaveAttribute('aria-checked', 'false');
    await tap(screen.getByRole('menuitemradio', { name: 'Ordinary' }));
    expect(onLevel).toHaveBeenCalledWith('ordinary');
    await tap(screen.getByRole('button', { name: 'Change subject or level: Biology' }));
    await tap(await screen.findByRole('menuitemradio', { name: 'Accounting' }));
    expect(onSubject).toHaveBeenCalledWith('accounting');
  });
});

async function tap(element: Element) {
  fireEvent.pointerDown(element, { pointerType: 'touch', pointerId: 1, isPrimary: true, button: 0, buttons: 1 });
  fireEvent.pointerUp(element, { pointerType: 'touch', pointerId: 1, isPrimary: true, button: 0, buttons: 0 });
  fireEvent.mouseDown(element, { button: 0 });
  fireEvent.mouseUp(element, { button: 0 });
  fireEvent.click(element, { button: 0, detail: 1 });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 20)); });
}

describe('OverScreen: a task over where you were', () => {
  it('is a named dialog, modal on a phone, that hands Escape to its screen and gives focus back', async () => {
    const { OverScreen } = await import('../components/ui/OverScreen');
    const { TopBar } = await import('../components/ui/Bars');
    const onEscape = vi.fn();
    const opener = document.createElement('button');
    document.body.appendChild(opener); opener.focus();
    const view = render(<OverScreen label="Practice: Photosynthesis" onEscape={onEscape} data-expanded="false">
      <TopBar leave={{ kind: 'close', onPress: () => {}, label: 'Close practice' }} title="Biology" />
    </OverScreen>);
    const over = screen.getByRole('dialog', { name: 'Practice: Photosynthesis' });
    expect(over).toHaveAttribute('aria-modal', 'true');
    expect(over).toHaveAttribute('data-expanded', 'false');
    expect(over).toHaveClass('ui-over', 'frame-takeover');
    await act(async () => { await new Promise(resolve => setTimeout(resolve, 40)); });
    expect(screen.getByRole('button', { name: 'Close practice' })).toHaveFocus();
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onEscape).toHaveBeenCalledOnce();
    view.unmount();
    expect(opener).toHaveFocus();
    opener.remove();
  });

  it('beside sidebar B it starts at the sidebar\'s edge and is not modal', async () => {
    const { OverScreen } = await import('../components/ui/OverScreen');
    render(<OverScreen label="Practice" onEscape={() => {}} modal={false} left={264}><p>Task</p></OverScreen>);
    const over = screen.getByRole('dialog', { name: 'Practice' });
    expect(over).not.toHaveAttribute('aria-modal');
    expect(over.style.left).toBe('264px');
  });
});
