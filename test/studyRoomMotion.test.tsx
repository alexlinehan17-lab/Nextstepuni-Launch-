import React, { useEffect } from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import StudySessionRoom from '../components/study/StudySessionRoom';
import StudyTimeUp from '../components/study/StudyTimeUp';
import StudyQuizInvitation from '../components/study/StudyQuizInvitation';
import { useStudyTransitionSound } from '../hooks/useStudyTransitionSound';
import { useStudySession } from '../hooks/useStudySession';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { setSoundMuted } from '../components/approved-ui-runtime';
import type * as MotionModule from '../components/Motion';

const preferences = vi.hoisted(() => ({ reduced: false, studySessions: [], updateDemoProgress: vi.fn() }));
vi.mock('../components/Motion', async original => ({ ...await original<typeof MotionModule>(), useReducedMotion: () => preferences.reduced }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ studySessions: preferences.studySessions, progressLoaded: true, updateDemoProgress: preferences.updateDemoProgress }) }));

const audible: string[] = [];
const effects: { animation: Animation; frames: Keyframe[]; options: KeyframeAnimationOptions }[] = [];
let play: ReturnType<typeof vi.spyOn>;
function Harness() {
  const session = useStudySession(DEMO_STUDENT_UID, {}, []);
  const sound = useStudyTransitionSound();
  useEffect(() => { session.startSession('Accounting', 'new-learning', 25); }, []);
  return <>
    <output data-testid="clock">{session.phase}:{session.elapsedSeconds}</output>
    <StudySessionRoom sound={sound} completion={session.phase === 'complete' ? <StudyTimeUp subject={session.subject} elapsedSeconds={session.elapsedSeconds} extendedMinutes={session.extendedMinutes} extensionBonus={session.extensionBonus} sessionPoints={session.basePointsEarned} onKeepGoing={session.extendSession} onFinish={vi.fn()} /> : undefined} subject={session.subject} subjectColor="#ff872b" type="New Learning" totalSeconds={session.totalDuration} elapsedSeconds={session.elapsedSeconds} paused={session.phase === 'paused'} prompt={null} onCompletePrompt={vi.fn()} onSkipPrompt={vi.fn()} onLeave={vi.fn()} onPause={session.pauseSession} onResume={session.resumeSession} />
  </>;
}
async function advance(milliseconds: number) {
  await act(async () => { vi.advanceTimersByTime(milliseconds); });
}
beforeEach(() => {
  vi.useFakeTimers();
  preferences.reduced = false;
  effects.length = 0;
  audible.length = 0;
  localStorage.clear();
  setSoundMuted(false);
  play = vi.spyOn(HTMLMediaElement.prototype, 'play').mockImplementation(function (this: HTMLAudioElement) { if (this.volume > 0) audible.push(this.src.split('/').pop()!); return Promise.resolve(); });
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
  it('reveals completion from the real timer, plays one cue and can keep going', async () => {
    const view = render(<Harness />);
    const clock = screen.getByRole('timer');
    await advance(25 * 60 * 1000);
    expect(screen.getByTestId('clock')).toHaveTextContent('complete:1500');
    expect(clock).toBeInTheDocument(); // The outgoing timer stays painted during the reveal.
    expect(screen.queryByRole('timer')).not.toBeInTheDocument();
    expect(effects.some(effect => effect.frames[0].clipPath)).toBe(true);
    expect(audible).toHaveLength(1);
    expect((play.mock.instances[0] as HTMLAudioElement).src).toContain('study-bloom-pause.wav');
    await advance(1200);
    await advance(20); // Focus follows the committed removal of inert on the next frame.
    expect(screen.getByRole('heading', { name: 'Time’s up.' })).toHaveFocus();
    view.rerender(<Harness />);
    expect(audible).toHaveLength(1);
    fireEvent.click(screen.getByRole('button', { name: 'Keep going for 5 more minutes' }));
    expect(screen.getByTestId('clock')).toHaveTextContent('active:1500');
    await advance(5 * 60 * 1000);
    await advance(1200);
    expect(screen.getByRole('heading', { name: 'You kept going.' })).toBeInTheDocument();
    expect(audible).toHaveLength(2);
  });

  it('finishes quietly with reduced motion and sound off', async () => {
    preferences.reduced = true;
    setSoundMuted(true);
    render(<Harness />);
    await advance(25 * 60 * 1000);
    await advance(150);
    expect(screen.getByRole('button', { name: 'Finish and log' })).toBeEnabled();
    expect(play).not.toHaveBeenCalled();
    expect(effects.every(effect => !effect.frames.some(frame => frame.clipPath || frame.transform))).toBe(true);
  });

  it('opens an already-completed session without replaying the transition', () => {
    function Restored() {
      const sound = useStudyTransitionSound();
      return <StudySessionRoom sound={sound} subject="Mathematics" subjectColor="#ff872b" type="Practice" totalSeconds={1500} elapsedSeconds={1500} paused={false} prompt={null} onCompletePrompt={vi.fn()} onSkipPrompt={vi.fn()} onLeave={vi.fn()} onPause={vi.fn()} onResume={vi.fn()} completion={<h1>Already complete</h1>} />;
    }
    render(<Restored />);
    expect(screen.getByRole('heading', { name: 'Already complete' })).toBeInTheDocument();
    expect(effects).toHaveLength(0);
    expect(play).not.toHaveBeenCalled();
  });

  it('settles completion when a background browser suspends animation timelines', async () => {
    Object.defineProperty(Element.prototype, 'animate', { configurable: true, value: () => ({ finished: new Promise(() => {}), cancel: vi.fn() }) });
    render(<Harness />);
    await advance(25 * 60 * 1000);
    await advance(1200);
    await advance(20);
    expect(screen.getByRole('heading', { name: 'Time’s up.' })).toHaveFocus();
    expect(screen.getByRole('button', { name: 'Finish and log' })).toBeEnabled();
    expect(audible).toHaveLength(1);
  });

  it('prepares the completion audio silently in the Start gesture', async () => {
    const volumes: number[] = [];
    play.mockImplementation(function (this: HTMLAudioElement) { volumes.push(this.volume); return Promise.resolve(); });
    function Start() {
      const sound = useStudyTransitionSound();
      return <button onClick={sound.prepare}>Start study</button>;
    }
    render(<Start />);
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'Start study' })); });
    expect(volumes).toEqual([0, 0]);
    fireEvent.click(screen.getByRole('button', { name: 'Start study' }));
    expect(volumes).toHaveLength(2);
  });

  it.each([false, true])('animates the optional invitation once, respecting reduced motion: %s', async reduced => {
    preferences.reduced = reduced;
    const open = vi.fn(), decline = vi.fn();
    const props = { subject: 'Mathematics', questionCount: 4, hasStudiedTopics: true, onAccept: vi.fn(), onDecline: decline, onOpen: open };
    const view = render(<StudyQuizInvitation {...props} />);
    view.rerender(<StudyQuizInvitation {...props} />);
    expect(open).toHaveBeenCalledOnce();
    expect(effects.some(effect => effect.frames.some(frame => frame.transform))).toBe(!reduced);
    await advance(1000);
    expect(effects.every(effect => vi.mocked(effect.animation.cancel).mock.calls.length === 1)).toBe(true);
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(decline).toHaveBeenCalledOnce();
  });

  it('keeps break and breathing time out of the real clock, and resumes after the bloom', async () => {
    render(<Harness />);
    expect(play).not.toHaveBeenCalled();
    await advance(2000);
    const pause = screen.getByRole('button', { name: 'Pause study session' });
    fireEvent.click(pause);
    fireEvent.click(pause); // Ignore a second press during the transition.
    expect(screen.getByTestId('clock')).toHaveTextContent('paused:2');
    expect(audible).toHaveLength(1);
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
    expect(audible).toEqual(['study-bloom-pause.wav', 'study-bloom-pause.wav', 'study-bloom-return.wav', 'study-bloom-return.wav']);
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
    expect(audible).toHaveLength(1);
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
    expect(audible).toHaveLength(2);
  });
});
