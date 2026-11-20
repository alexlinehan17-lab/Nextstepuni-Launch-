/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The recording behind a Listening Studio sitting.
 *
 * One <audio> element with the Studio's own controls on top of it. The address
 * is resolved exactly as Mark Bank resolves it (audioStorage.ts): the app's
 * verified copy where one has been uploaded, the card's own address otherwise.
 *
 * A recording still at the SEC's address cannot play inside the app: the SEC
 * refuses its files to other sites and the site's media policy does not list
 * it. Those are reported as not playable up front, so the Studio offers the
 * SEC's own page instead of drawing a player that can only fail.
 *
 * A listening test is one long recording shared by every question on the paper
 * and no card carries a start time yet, so the position is remembered per
 * recording for the visit: a student who works through the questions in order
 * finds the recording where they left it.
 */

import { useCallback, useEffect, useMemo, useRef, useState, type RefObject } from 'react';
import type { CardAudioMaterial } from '../../types/markBank';
import { audioPlaybackUrl } from '../MarkBank/audioStorage';

const SEC_ADDRESS = /^https?:\/\/(www\.)?examinations\.ie\//i;
const positionKey = (source: CardAudioMaterial) => `ls:position:${source.canonicalUrl}`;

const readPosition = (source: CardAudioMaterial): number => {
  try {
    const saved = Number(window.sessionStorage.getItem(positionKey(source)));
    return Number.isFinite(saved) && saved > 0 ? saved : 0;
  } catch {
    return 0;
  }
};

const writePosition = (source: CardAudioMaterial, seconds: number) => {
  try {
    window.sessionStorage.setItem(positionKey(source), String(Math.floor(seconds)));
  } catch {
    /* Private browsing: the position is simply not remembered. */
  }
};

export interface StudioAudio {
  /** Spread onto the one <audio> element the sitting renders. */
  element: {
    ref: RefObject<HTMLAudioElement | null>;
    src: string | undefined;
    preload: 'metadata';
    onLoadedMetadata: () => void;
    onDurationChange: () => void;
    onTimeUpdate: () => void;
    onPlay: () => void;
    onPause: () => void;
    onEnded: () => void;
    onError: () => void;
  };
  /** False where the recording is still only at the SEC's own address. */
  playable: boolean;
  /** The recording should have played and did not load. */
  failed: boolean;
  playing: boolean;
  /** Whole seconds. */
  time: number;
  /** Whole seconds; 0 until the recording has reported its length. */
  duration: number;
  toggle: () => void;
  pause: () => void;
  seek: (seconds: number) => void;
  skip: (seconds: number) => void;
}

export function useStudioAudio(source: CardAudioMaterial): StudioAudio {
  const ref = useRef<HTMLAudioElement | null>(null);
  const url = audioPlaybackUrl(source);
  const playable = !SEC_ADDRESS.test(url);
  const [failed, setFailed] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [time, setTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const sourceRef = useRef(source);
  sourceRef.current = source;

  // A different recording starts from its own remembered place.
  useEffect(() => {
    setFailed(false);
    setPlaying(false);
    setDuration(0);
    setTime(playable ? readPosition(sourceRef.current) : 0);
  }, [url, playable]);

  const readDuration = useCallback(() => {
    const el = ref.current;
    if (el && Number.isFinite(el.duration) && el.duration > 0) setDuration(Math.floor(el.duration));
  }, []);

  const onLoadedMetadata = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    readDuration();
    const saved = readPosition(sourceRef.current);
    if (saved > 0 && Number.isFinite(el.duration) && saved < el.duration - 5) el.currentTime = saved;
    setFailed(false);
  }, [readDuration]);

  const onTimeUpdate = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    const second = Math.floor(el.currentTime);
    setTime(previous => {
      if (previous === second) return previous;
      if (second % 5 === 0) writePosition(sourceRef.current, second);
      return second;
    });
  }, []);

  const onPause = useCallback(() => {
    setPlaying(false);
    const el = ref.current;
    if (el) writePosition(sourceRef.current, el.currentTime);
  }, []);

  const pause = useCallback(() => { ref.current?.pause(); }, []);

  const toggle = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    if (!el.paused) { el.pause(); return; }
    // Playback only ever starts from this tap: nothing in the Studio autoplays.
    const started = el.play();
    if (started && typeof started.catch === 'function') {
      started.catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'NotSupportedError') setFailed(true);
      });
    }
  }, []);

  const seek = useCallback((seconds: number) => {
    const el = ref.current;
    if (!el) return;
    const limit = Number.isFinite(el.duration) && el.duration > 0 ? el.duration : seconds;
    const next = Math.max(0, Math.min(limit, seconds));
    el.currentTime = next;
    setTime(Math.floor(next));
    writePosition(sourceRef.current, next);
  }, []);

  const skip = useCallback((seconds: number) => {
    const el = ref.current;
    if (el) seek(el.currentTime + seconds);
  }, [seek]);

  const element = useMemo(() => ({
    ref,
    src: playable ? url : undefined,
    preload: 'metadata' as const,
    onLoadedMetadata,
    onDurationChange: readDuration,
    onTimeUpdate,
    onPlay: () => setPlaying(true),
    onPause,
    onEnded: () => setPlaying(false),
    onError: () => { setFailed(true); setPlaying(false); },
  }), [playable, url, onLoadedMetadata, readDuration, onTimeUpdate, onPause]);

  return { element, playable, failed, playing, time, duration, toggle, pause, seek, skip };
}

/** 83 -> "1:23"; 3725 -> "1:02:05". */
export const clock = (seconds: number): string => {
  const whole = Math.max(0, Math.floor(seconds));
  const hours = Math.floor(whole / 3600);
  const minutes = Math.floor((whole % 3600) / 60);
  const rest = String(whole % 60).padStart(2, '0');
  return hours > 0 ? `${hours}:${String(minutes).padStart(2, '0')}:${rest}` : `${minutes}:${rest}`;
};
