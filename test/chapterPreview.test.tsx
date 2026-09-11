import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import ChapterPreview from '../components/landing/glass/ChapterPreview';
import { PREVIEW_PLAYBACK, PREVIEW_READY } from '../components/landing/glass/PreviewReady';

vi.mock('framer-motion', () => ({ useInView: () => true, useReducedMotion: () => false }));
beforeEach(() => vi.useFakeTimers());
afterEach(() => { cleanup(); vi.useRealTimers(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

const ready = (frame: HTMLIFrameElement, origin = window.location.origin, source: MessageEventSource | null = frame.contentWindow) => {
  fireEvent(window, new MessageEvent('message', { origin, source, data: { type: PREVIEW_READY } }));
};

describe('Chapter preview recovery', () => {
  it('does not treat a blocked iframe load as success, and offers a working retry', () => {
    render(<ChapterPreview id="launchpad" />);
    const frame = screen.getByTitle('Launchpad — tools and categories tour') as HTMLIFrameElement;
    fireEvent.load(frame);
    expect(screen.getByRole('status')).toHaveTextContent('Opening preview');
    expect(frame).toHaveStyle({ opacity: '0' });
    act(() => vi.advanceTimersByTime(21_000));
    expect(screen.getByRole('alert')).toHaveTextContent('couldn’t load');
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    const replacement = screen.getByTitle(frame.title) as HTMLIFrameElement;
    expect(replacement).not.toBe(frame);
    ready(replacement);
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(replacement).toHaveStyle({ opacity: '1' });
  });
  it('only accepts readiness from the expected same-origin frame and delivers the chosen playback state', () => {
    render(<ChapterPreview id="lab" />);
    const frame = screen.getByTitle('Mastering Active Recall — memory strength experiment') as HTMLIFrameElement;
    const send = vi.spyOn(frame.contentWindow!, 'postMessage');
    fireEvent.click(screen.getByRole('button', { name: 'Pause Learning Lab preview' }));
    ready(frame, 'https://elsewhere.example');
    ready(frame, window.location.origin, window);
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(send).not.toHaveBeenCalled();
    ready(frame);
    expect(send).toHaveBeenLastCalledWith({ type: PREVIEW_PLAYBACK, playing: false }, window.location.origin);
    act(() => vi.advanceTimersByTime(21_000));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Play Learning Lab preview' }));
    expect(send).toHaveBeenLastCalledWith({ type: PREVIEW_PLAYBACK, playing: true }, window.location.origin);
  });
  it('reopens an interactive paper when a repaired worker takes control, without reloading the parent page', () => {
    const serviceWorker = new EventTarget();
    vi.stubGlobal('navigator', { serviceWorker });
    render(<ChapterPreview id="papertrail" />);
    const frame = screen.getByTitle('Biology 2024 — interactive Paper Trail') as HTMLIFrameElement;
    act(() => vi.advanceTimersByTime(21_000));
    act(() => serviceWorker.dispatchEvent(new Event('controllerchange')));
    const replacement = screen.getByTitle(frame.title) as HTMLIFrameElement;
    expect(replacement).not.toBe(frame);
    ready(replacement);
    expect(replacement).toHaveAttribute('tabindex', '0');
    expect(replacement).not.toHaveAttribute('aria-hidden');
  });
});
