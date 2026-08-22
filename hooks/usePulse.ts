/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A flag that turns itself back off, and cancels when the component goes away.
 *
 * The pattern this replaces is written by hand in twenty-one places here:
 *
 *     setFlash(true);
 *     setTimeout(() => setFlash(false), 550);
 *
 * and the timer is never held, so it fires whether or not the component is
 * still mounted. React 19 makes that a no-op in the app, which is why it went
 * unnoticed — but under jsdom it lands after the test environment has torn
 * down, and setState reaches for `window` that is no longer there. That failed
 * a CI run in which all 2,550 tests passed, on a repo where a push to main is a
 * live deploy: a gate that fails for reasons unrelated to the change is a gate
 * people learn to ignore.
 *
 * Firing again before the first has finished also restarts the timer rather
 * than stacking a second one, so rapid taps hold the flag on for the full
 * duration from the LAST tap rather than switching it off from the first.
 *
 *     const [flash, pulseFlash] = usePulse(550);
 *     ...
 *     if (correct) pulseFlash();
 *
 * A third return value cancels it early, for the flags that also have to reset
 * when something else changes underneath them.
 */
import { useCallback, useEffect, useRef, useState } from 'react';

export function usePulse(ms: number): [boolean, () => void, () => void] {
  const [on, setOn] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => () => {
    if (timer.current) clearTimeout(timer.current);
  }, []);

  const pulse = useCallback(() => {
    setOn(true);
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => {
      timer.current = null;
      setOn(false);
    }, ms);
  }, [ms]);

  /** Turn it off now — for the cases that reset on a prop change. */
  const cancel = useCallback(() => {
    if (timer.current) { clearTimeout(timer.current); timer.current = null; }
    setOn(false);
  }, []);

  return [on, pulse, cancel];
}
