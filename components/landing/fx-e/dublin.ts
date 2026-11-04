/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Today's Question runs on Irish time: the question changes at midnight in
 * Europe/Dublin wherever the visitor is, and question #1 fell on a real day.
 * Everything here is pure so the day → number → label chain can be checked
 * without a browser.
 */

/** The day of question #1. */
export const EPOCH = '2026-09-01';

const DAY_MS = 86400000;

const dublinFormat = (): Intl.DateTimeFormat =>
  new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Dublin', year: 'numeric', month: '2-digit', day: '2-digit' });

/** Today's date in Dublin as YYYY-MM-DD. */
export const dublinDay = (now: Date = new Date()): string => {
  const parts = dublinFormat().formatToParts(now);
  const get = (type: string) => parts.find(p => p.type === type)?.value ?? '';
  return `${get('year')}-${get('month')}-${get('day')}`;
};

const utc = (iso: string): number => {
  const [y, m, d] = iso.split('-').map(Number);
  return Date.UTC(y, m - 1, d);
};

/** The question number for a Dublin day: #1 on EPOCH, one more each day, never below 1. */
export const questionNumber = (iso: string): number => Math.max(1, Math.round((utc(iso) - utc(EPOCH)) / DAY_MS) + 1);

/** The day before, YYYY-MM-DD — the streak asks whether yesterday was answered. */
export const dayBefore = (iso: string): string => new Date(utc(iso) - DAY_MS).toISOString().slice(0, 10);

/** "8 September 2026". */
export const formatDay = (iso: string): string =>
  new Intl.DateTimeFormat('en-IE', { timeZone: 'UTC', day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(utc(iso)));

/** Find the next Irish midnight, including the 23/25-hour DST days. */
export function nextDublinMidnight(now:Date=new Date()):number {
  const day=dublinDay(now);
  let low=now.getTime(),high=low+27*60*60*1000;
  while(high-low>1){const middle=Math.floor((low+high)/2);if(dublinDay(new Date(middle))===day)low=middle;else high=middle;}
  return high;
}
