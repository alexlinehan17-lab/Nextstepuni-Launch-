import React from 'react';
import './lockedControl.css';

const timers = new WeakMap<HTMLElement, ReturnType<typeof setTimeout>>();

/** Restart the small lock feedback even when a visitor taps repeatedly. */
export function shakeLockedControl(element: HTMLElement) {
  clearTimeout(timers.get(element));
  element.classList.remove('locked-control-shake');
  void element.offsetWidth;
  element.classList.add('locked-control-shake');
  timers.set(element, setTimeout(() => {
    element.classList.remove('locked-control-shake');
    timers.delete(element);
  }, 360));
}

/** Aria-disabled keeps a preview control discoverable and able to give feedback. */
export default function LockedButton({ locked = false, className = '', onClick, ...props }:
  React.ButtonHTMLAttributes<HTMLButtonElement> & { locked?: boolean }) {
  return <button {...props} className={`${className}${locked ? ' locked-control' : ''}`}
    aria-disabled={locked || undefined}
    onClick={event => {
      if (locked) {
        event.preventDefault();
        event.stopPropagation();
        shakeLockedControl(event.currentTarget);
        return;
      }
      onClick?.(event);
    }} />;
}
