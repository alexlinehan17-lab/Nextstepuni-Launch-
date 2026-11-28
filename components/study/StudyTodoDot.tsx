/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A session to-do's dot (c-study, agreed 26 Nov 2026: "Absolutely amazing,
 * much, much better"): a dotted ring, grey until the to-do is set and green
 * once it is; it fills green with a drawn tick when the session is done.
 */
import React from 'react';
import './study-marks.css';

export function StudyTodoDot({ set, done }: { set: boolean; done: boolean }) {
  return (
    <svg className="study-dot" viewBox="0 0 20 20" aria-hidden="true" focusable="false" data-set={set || undefined} data-done={done || undefined}>
      <circle className="study-dot-ring" cx="10" cy="10" r="8.5" />
      <circle className="study-dot-fill" cx="10" cy="10" r="9.4" />
      <path className="study-dot-tick" d="M6.3 10.4l2.5 2.5 4.9-5.4" />
    </svg>
  );
}
