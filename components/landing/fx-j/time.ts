/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The exam hall's two ways of saying how long a sitting is: in words for the
 * picker and the screen reader ("2 hours 50 minutes"), and as the wall
 * clock's face ("2:49:59"), counting whole seconds down.
 */

const plural = (n: number, one: string): string => `${n} ${one}${n === 1 ? '' : 's'}`;

/** "3 hours", "2 hours 50 minutes", "1 hour 50 minutes". */
export const durationWords = (minutes: number): string => {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return [h ? plural(h, 'hour') : '', m ? plural(m, 'minute') : ''].filter(Boolean).join(' ');
};

/** "3 h", "2 h 50 min" — the picker's column. */
export const durationShort = (minutes: number): string => {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return [h ? `${h} h` : '', m ? `${m} min` : ''].filter(Boolean).join(' ');
};

/** The clock face for the time left, H:MM:SS; never below zero. */
export const clockFace = (msLeft: number): string => {
  const s = Math.max(0, Math.ceil(msLeft / 1000));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
};
