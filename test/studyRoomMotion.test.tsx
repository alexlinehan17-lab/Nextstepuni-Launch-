import React, { useEffect } from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import StudySessionRoom from '../components/study/StudySessionRoom';
import { useStudySession } from '../hooks/useStudySession';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { setSoundMuted } from '../components/approved-ui-runtime';
import type * as MotionModule from '../components/Motion';

const preferences = vi.hoisted(() => ({ reduced: false, studySessions: [], updateDemoProgress: vi.fn() }));
vi.mock('../components/Motion', async original => ({ ...await original<typeof MotionModule>(), useReducedMotion: () => preferences.reduced }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ studySessions: preferences.studySessions, progressLoaded: true, updateDemoProgress: preferences.updateDemoProgress }) }));

const effects: { animation: Animation; frames: Keyframe[]; options: KeyframeAnimationOptions }[] = [];
let play: ReturnType<typeof vi.spyOn>;
function Harness() {
  const session = useStudySession(DEMO_STUDENT_UID, {}, []);
  useEffect(() => { session.startSession('Accounting', 'new-learning', 25); }, []);
  return <>
    <output data-testid="clock">{session.phase}:{session.elapsedSeconds}</output>
    <StudySessionRoom subject={session.subject} subjectColor="#ff872b" type="New Learning" totalSeconds={session.totalDuration} elapsedSeconds={session.elapsedSeconds} paused={session.phase === 'paused'} prompt={null} onCompletePrompt={vi.fn()} onSkipPrompt={vi.fn()} onLeave={vi.fn()} onPause={session.pauseSession} onResume={session.resumeSession} />
  </>;
}
async function advance(milliseconds: number) {
  await act(async () => { vi.advanceTimersByTime(milliseconds); });
}
beforeEach(() => {
  vi.useFakeTimers();
  preferences.reduced = false;
  effects.length = 0;
  localStorage.clear();
  setSoundMuted(false);
  play = vi.spyOn(HTMLMediaElement.prototype, 'play').mockResolvedValue(undefined);
  vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => {});
  vi.stubGlobal('Animation', class {});
  Object.defineProperty(Element.prototype, 'animate', { configurable: true, value: function (frames: Keyframe[], options: KeyframeAnimationOptions) {
    let finish: () => void;
    const finished = new Promise<void>(resolve => { finish = resolve; });
    const timer = options.iterations === Infinity ? undefined : window.setTimeout(() => finish(), Number(options.duration) + Number(options.delay ?? 0));
    const animation = { finished, cancel: vi.fn(() => { clearTimeout(timer); }), pause: vi.fn(), play: vi.fn() } as unknown as Animation;
    effects.push({ animation, frames, options });
    return animation;
  } });
});
afterEach(() => { cleanup(); setSoundMuted(false); vi.restoreAllMocks(); vi.unstubAllGlobals(); delete Element.prototype.animate; vi.useRealTimers(); });

describe('the study room bloom and breathing guide', () => {
  it('keeps break and breathing time out of the real clock, and resumes after the bloom', async () => {
    render(<Harness />);
    expect(play).not.toHaveBeenCalled();
    await advance(2000);
    const pause = screen.getByRole('button', { name: 'Pause study session' });
    fireEvent.click(pause);
    fireEvent.click(pause); // Ignore a second press during the transition.
    expect(screen.getByTestId('clock')).toHaveTextContent('paused:2');
    expect(play).toHaveBeenCalledOnce();
    expect(effects.some(effect => effect.frames[0].clipPath)).toBe(true);
    await advance(1300);
    fireEvent.click(screen.getByRole('button', { name: 'Take a few slow breaths' }));
    await advance(1300);
    expect(screen.getByRole('dialog', { name: 'Take a moment.' })).toBeInTheDocument();
    expect(screen.getByText(/^Breathe in/)).toBeInTheDocument();
    expect(effects.filter(effect => effect.options.iterations === Infinity)).toHaveLength(2);
    await advance(4000);
    expect(screen.getByText(/^Breathe out/)).toBeInTheDocument();
    await advance(6000);
    expect(screen.getByText(/^Breathe in/)).toBeInTheDocument();
    expect(screen.getByTestId('clock')).toHaveTextContent('paused:2');
    fireEvent.keyDown(window, { key: 'Escape' });
    await advance(700);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Take a few slow breaths' })).toHaveFocus();
    fireEvent.click(screen.getByRole('button', { name: 'Back to study' }));
    await advance(700);
    expect(screen.getByTestId('clock')).toHaveTextContent('paused:2');
    await advance(500);
    expect(screen.getByTestId('clock')).toHaveTextContent('active:2');
    await advance(1000);
    expect(screen.getByTestId('clock')).toHaveTextContent('active:3');
    expect(play.mock.instances.map(track => (track as HTMLAudioElement).src.split('/').pop())).toEqual(['study-bloom-pause.wav', 'study-bloom-pause.wav', 'study-bloom-return.wav', 'study-bloom-return.wav']);
  });

  it('uses the shared mute preference and stops a cue when sound is turned off', async () => {
    setSoundMuted(true);
    render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: 'Pause study session' }));
    await advance(1300);
    expect(play).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Turn study sound on' }));
    expect(localStorage.getItem('kobra-sound-muted')).toBe('0');
    fireEvent.click(screen.getByRole('button', { name: 'Take a few slow breaths' }));
    expect(play).toHaveBeenCalledOnce();
    const track = play.mock.instances[0] as HTMLAudioElement;
    fireEvent.click(screen.getByRole('button', { name: 'Mute study sound' }));
    expect(track.currentTime).toBe(0);
    expect(localStorage.getItem('kobra-sound-muted')).toBe('1');
  });

  it('keeps the guide usable with reduced motion and rejected audio', async () => {
    preferences.reduced = true;
    play.mockRejectedValue(new DOMException('Unavailable', 'NotAllowedError'));
    render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: 'Pause study session' }));
    await advance(150);
    fireEvent.click(screen.getByRole('button', { name: 'Take a few slow breaths' }));
    await advance(150);
    expect(effects.every(effect => !effect.frames.some(frame => frame.clipPath || frame.transform))).toBe(true);
    expect(effects.some(effect => effect.options.iterations === Infinity)).toBe(false);
    await advance(4000);
    expect(screen.getByText(/^Breathe out/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Back to your break' }));
    await advance(150);
    expect(screen.getByTestId('clock')).toHaveTextContent('paused:0');
  });

  it('cancels motion and clock callbacks when the session unmounts', async () => {
    const view = render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: 'Pause study session' }));
    await advance(1300);
    fireEvent.click(screen.getByRole('button', { name: 'Take a few slow breaths' }));
    await advance(1300);
    const cycles = effects.filter(effect => effect.options.iterations === Infinity);
    view.unmount();
    expect(cycles.every(effect => vi.mocked(effect.animation.cancel).mock.calls.length === 1)).toBe(true);
    expect(document.body.style.overflow).toBe('');
    await advance(10000);
    expect(play).toHaveBeenCalledTimes(2);
  });
});
