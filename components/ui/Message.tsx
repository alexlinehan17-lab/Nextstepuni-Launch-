/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The one message system: the toast (components.md, "Sheets, dialogs,
 * toasts"; the kit's .toast). Something finished in the background, or a
 * chance to undo. One line, charcoal, above the tab bar, gone after four
 * seconds, one at a time (a new one replaces the one showing).
 *
 *   <MessageHost />                                    once, near the root
 *   showMessage('Saved to your plan', { action: { label: 'Undo', onPress: undo } });
 *
 * It is placed by the frame (frame-float frame-float-bottom), so it sits above
 * the tab bar while the bar is mounted and above the home indicator always,
 * never under the island. A polite live region reads each one out.
 *
 * Migration: the app's ToastProvider (`useToast().showToast(message, type)`,
 * 28 calls) and the Kobra `toast()` (3 calls in lessons and the paper viewer)
 * keep today's look; each can later call showMessage(message) instead, and
 * their two offline banners become one message.
 */
import { useEffect, useState, useSyncExternalStore } from 'react';
import { FramePortal } from './Frame';
import { TextButton } from './Button';
import './parts.css';

export interface MessageOptions {
  /** One action, such as Undo. */
  action?: { label: string; onPress: () => void };
  /** How long it shows, in ms (default 4000). */
  duration?: number;
}

interface Message extends MessageOptions { id: number; text: string }

/** Four seconds (components.md); it leaves by fading (--t-draw). */
const DEFAULT_MS = 4000;
const LEAVE_MS = 160;

let current: Message | null = null;
let nextId = 1;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach(listener => listener());

/** Show a message. It replaces the one showing, if any. Returns its id. */
export function showMessage(text: string, options: MessageOptions = {}): number {
  current = { id: nextId++, text, ...options };
  emit();
  return current.id;
}

/** Take a message away (the one showing, or only the one with this id). */
export function dismissMessage(id?: number) {
  if (!current || (id !== undefined && current.id !== id)) return;
  current = null;
  emit();
}

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => { listeners.delete(listener); };
}

/** A message that stays while something is true (the app is offline): the same charcoal line in the
 *  same place, placed by the frame at the bottom, so it never covers a bar or the sidebar. It is not
 *  one of the passing messages: one that comes while it shows appears over it. `text` null hides it. */
export function StandingMessage({ text }: { text: string | null }) {
  const [shown, setShown] = useState<string | null>(text);
  const [state, setState] = useState<'entering' | 'open' | 'leaving'>('entering');

  useEffect(() => {
    if (text) {
      setShown(text);
      setState('entering');
      const frame = requestAnimationFrame(() => setState('open'));
      return () => cancelAnimationFrame(frame);
    }
    setState('leaving');
    const timer = window.setTimeout(() => setShown(null), LEAVE_MS);
    return () => window.clearTimeout(timer);
  }, [text]);

  return (
    <FramePortal>
      <div className="sr-only" role="status" aria-live="polite">{text ?? ''}</div>
      {shown ? (
        <div className="ui-part ui-toast ui-toast--standing frame-float frame-float-bottom" data-state={state}>
          <span className="ui-toast-text">{shown}</span>
        </div>
      ) : null}
    </FramePortal>
  );
}

/** Renders the message, if there is one. Mount once. */
export function MessageHost() {
  const message = useSyncExternalStore(subscribe, () => current, () => null);
  const [shown, setShown] = useState<Message | null>(message);
  const [state, setState] = useState<'entering' | 'open' | 'leaving'>('entering');

  useEffect(() => {
    if (message) {
      setShown(message);
      setState('entering');
      const frame = requestAnimationFrame(() => setState('open'));
      const timer = window.setTimeout(() => dismissMessage(message.id), message.duration ?? DEFAULT_MS);
      return () => { cancelAnimationFrame(frame); window.clearTimeout(timer); };
    }
    setState('leaving');
    const timer = window.setTimeout(() => setShown(null), LEAVE_MS);
    return () => window.clearTimeout(timer);
  }, [message]);

  return (
    <FramePortal>
      {/* Always present, so a screen reader hears each new message. */}
      <div className="sr-only" role="status" aria-live="polite">{message?.text ?? ''}</div>
      {shown ? (
        <div className="ui-part ui-toast frame-float frame-float-bottom" data-state={state} key={shown.id}>
          <span className="ui-toast-text">{shown.text}</span>
          {shown.action
            ? <TextButton onClick={() => { shown.action?.onPress(); dismissMessage(shown.id); }}>{shown.action.label}</TextButton>
            : null}
        </div>
      ) : null}
    </FramePortal>
  );
}
