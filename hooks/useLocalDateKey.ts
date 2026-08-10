/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useState } from 'react';
import { toDateKey } from '../utils/weekDates';

/**
 * The current local calendar day, kept fresh when an open app crosses
 * midnight. Timetables and study records use local YYYY-MM-DD keys, so a
 * long-lived screen must not keep yesterday's focus or countdown.
 */
export function useLocalDateKey(): string {
  const [dateKey, setDateKey] = useState(() => toDateKey(new Date()));

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout> | undefined;

    const scheduleMidnightRefresh = () => {
      if (timer) clearTimeout(timer);
      const now = new Date();
      const nextMidnight = new Date(now);
      nextMidnight.setHours(24, 0, 0, 50);
      timer = setTimeout(() => {
        setDateKey(toDateKey(new Date()));
        scheduleMidnightRefresh();
      }, Math.max(1000, nextMidnight.getTime() - now.getTime()));
    };

    const refreshFromClock = () => {
      setDateKey(toDateKey(new Date()));
      scheduleMidnightRefresh();
    };

    const handleVisibility = () => {
      if (!document.hidden) refreshFromClock();
    };

    scheduleMidnightRefresh();
    window.addEventListener('focus', refreshFromClock);
    document.addEventListener('visibilitychange', handleVisibility);
    return () => {
      if (timer) clearTimeout(timer);
      window.removeEventListener('focus', refreshFromClock);
      document.removeEventListener('visibilitychange', handleVisibility);
    };
  }, []);

  return dateKey;
}
