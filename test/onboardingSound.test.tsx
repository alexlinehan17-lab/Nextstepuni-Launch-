import type React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import Onboarding from '../components/Onboarding';
import { draftKey, initialDraft } from '../components/onboarding/model';

const audio = vi.hoisted(() => ({ play: vi.fn(), mobile: false }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => audio.mobile }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
// Keep the real interaction listener and mute store; replace only audio output.
vi.mock('@web-kits/audio/react', async () => {
  const React = await import('react');
  const Enabled = React.createContext(true);
  return {
    SoundProvider: ({ enabled, children }: { enabled: boolean; children: React.ReactNode }) =>
      <Enabled.Provider value={enabled}>{children}</Enabled.Provider>,
    usePatch: () => {
      const enabled = React.useContext(Enabled);
      const latest = React.useRef(enabled);
      latest.current = enabled;
      return React.useMemo(() => ({ ready: true, play: (...args: unknown[]) => {
        if (latest.current) audio.play(...args);
      } }), []);
    },
  };
});

function mount() {
  return render(<Onboarding userId="sound-test" userName="Aoife" onComplete={vi.fn()} onSkip={vi.fn()} />);
}

beforeEach(() => {
  localStorage.clear();
  audio.play.mockClear();
  audio.mobile = false;
  vi.stubGlobal('AudioContext', function AudioContext() {});
});
afterEach(() => vi.unstubAllGlobals());

describe('onboarding interface sound', () => {
  it.each([false, true])('plays one cue per action in the %s mobile flow', async mobile => {
    audio.mobile = mobile;
    const view = mount();
    await userEvent.click(screen.getByRole('button', { name: 'Get Started' }));
    expect(audio.play).toHaveBeenCalledTimes(1);
    expect(audio.play).toHaveBeenCalledWith('tap', expect.anything());
    view.unmount();
    audio.play.mockClear();
    const button = document.createElement('button');
    document.body.append(button);
    fireEvent.pointerDown(button, { button: 0 });
    expect(audio.play).not.toHaveBeenCalled();
    button.remove();
  });

  it('honours the saved mute preference and shares changes through the existing setting', async () => {
    localStorage.setItem('kobra-sound-muted', '1');
    mount();
    await userEvent.click(screen.getByRole('button', { name: 'Get Started' }));
    expect(audio.play).not.toHaveBeenCalled();
    await userEvent.click(screen.getByRole('button', { name: 'Turn interface sound on' }));
    expect(localStorage.getItem('kobra-sound-muted')).toBe('0');
    audio.play.mockClear();
    await userEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(audio.play).toHaveBeenCalledTimes(1);
    await userEvent.click(screen.getByRole('button', { name: 'Turn interface sound off' }));
    expect(localStorage.getItem('kobra-sound-muted')).toBe('1');
    audio.play.mockClear();
    await userEvent.click(screen.getByRole('button', { name: 'Get Started' }));
    expect(audio.play).not.toHaveBeenCalled();
  });

  it('covers menu triggers and selections rendered outside the onboarding DOM', async () => {
    localStorage.setItem(draftKey('sound-test', 'fresh'), JSON.stringify({
      ...initialDraft(), step: 'grades', year: '5th', subjects: ['English'],
      configs: { English: { level: 'higher', current: 'H3', target: 'H1', reviewed: true } },
    }));
    mount();
    await userEvent.click(screen.getByRole('combobox', { name: 'English level' }));
    expect(audio.play.mock.calls.map(([name]) => name)).toEqual(['open']);
    await userEvent.click(await screen.findByRole('option', { name: 'Ordinary' }));
    expect(audio.play.mock.calls.map(([name]) => name)).toEqual(['open', 'select']);
  });

  it('keeps setup available when the browser has no audio support', () => {
    vi.stubGlobal('AudioContext', undefined);
    mount();
    expect(screen.getByRole('button', { name: 'Get Started' })).toBeEnabled();
    expect(screen.queryByRole('button', { name: 'Turn interface sound off' })).not.toBeInTheDocument();
  });
});
