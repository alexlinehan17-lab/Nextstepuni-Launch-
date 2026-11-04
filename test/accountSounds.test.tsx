import React from 'react';
import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import AccountCrewPicker from '../components/AccountCrewPicker';
import AccountCard from '../components/AccountCard';

const contexts: FakeAudioContext[] = [];
const automation = () => ({ setValueAtTime: vi.fn(), exponentialRampToValueAtTime: vi.fn() });
class FakeAudioContext {
  state = 'running';
  currentTime = 0;
  destination = {};
  constructor() { contexts.push(this); }
  resume = vi.fn(async () => { this.state = 'running'; });
  close = vi.fn(async () => { this.state = 'closed'; });
  createOscillator = vi.fn(() => ({ frequency: automation(), connect: vi.fn(), disconnect: vi.fn(), start: vi.fn(), stop: vi.fn(), type: 'sine', onended: null }));
  createGain = vi.fn(() => ({ gain: automation(), connect: vi.fn(), disconnect: vi.fn() }));
}
function Harness({ onPress = vi.fn() }: { onPress?: () => void }) {
  return <AccountCard view="welcome" registerStep={1} avatar="" name="" school="" busy={false} onAvatarChange={vi.fn()} onWelcome={vi.fn()} onSchoolAccess={vi.fn()}>
    <button type="button" onClick={onPress}>Continue</button>
    <button type="button" data-account-sound="save">Choose character</button>
    <button type="button" disabled>Disabled action</button>
    <AccountCrewPicker value="" onChange={vi.fn()} />
  </AccountCard>;
}
beforeEach(() => {
  localStorage.clear(); contexts.length = 0;
  vi.useFakeTimers(); vi.stubGlobal('AudioContext', FakeAudioContext);
});
afterEach(() => { vi.useRealTimers(); vi.unstubAllGlobals(); });

describe('account interaction sounds', () => {
  it('starts only on a user action and ignores disabled controls', () => {
    const { unmount } = render(<Harness />);
    expect(contexts).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: 'Disabled action' }));
    expect(contexts).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(contexts).toHaveLength(1);
    expect(contexts[0].createOscillator).toHaveBeenCalledOnce();
    unmount();
    expect(contexts[0].close).toHaveBeenCalledOnce();
  });
  it('plays one cue for a tile label and ignores its hidden forwarded input', () => {
    const { container } = render(<Harness />);
    fireEvent.click(screen.getByText('Maker', { selector: 'label > span' }));
    expect(contexts).toHaveLength(1);
    expect(contexts[0].createOscillator).toHaveBeenCalledOnce();
    fireEvent.click(container.querySelector('input[value="star-crew:maker"]')!);
    expect(contexts[0].createOscillator).toHaveBeenCalledOnce();
  });
  it('mutes current and queued cues, remembers the preference, and can be turned back on', () => {
    const { unmount } = render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: 'Choose character' }));
    const first = contexts[0];
    expect(first.createOscillator).toHaveBeenCalledOnce();
    fireEvent.click(screen.getByRole('button', { name: 'Mute sounds' }));
    act(() => { vi.advanceTimersByTime(500); });
    expect(first.close).toHaveBeenCalledOnce();
    expect(first.createOscillator).toHaveBeenCalledOnce();
    expect(localStorage.getItem('nextstepuni:account-sound')).toBe('off');
    unmount();
    render(<Harness />);
    expect(screen.getByRole('button', { name: 'Turn sounds on' })).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(contexts).toHaveLength(1);
    fireEvent.click(screen.getByRole('button', { name: 'Turn sounds on' }));
    expect(contexts).toHaveLength(2);
    expect(contexts[1].createOscillator).toHaveBeenCalledOnce();
    expect(localStorage.getItem('nextstepuni:account-sound')).toBe('on');
  });
  it('does not leave delayed sound callbacks after leaving the account screen', () => {
    const { unmount } = render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: 'Choose character' }));
    unmount();
    act(() => { vi.advanceTimersByTime(500); });
    expect(contexts).toHaveLength(1);
    expect(contexts[0].createOscillator).toHaveBeenCalledOnce();
    expect(contexts[0].close).toHaveBeenCalledOnce();
  });
  it('keeps controls working when the browser has no Web Audio support', () => {
    vi.stubGlobal('AudioContext', undefined);
    const onPress = vi.fn();
    render(<Harness onPress={onPress} />);
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(onPress).toHaveBeenCalledOnce();
    expect(contexts).toHaveLength(0);
  });
});
