/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Flow-field pen hatching behind a chapter heading — a printer's ornament,
 * a different field per chapter. The SVGs are generated once by
 * scripts/landing/flow-fields.mjs and inlined here so their strokes can be
 * inked in by CSS (fx.css, .fx-field) on the same scroll timeline as the
 * page's drawn rules. Decorative: aria-hidden, no pointer events.
 */

import React, { useMemo } from 'react';
import f1 from './fields/field-1.svg?raw';
import f2 from './fields/field-2.svg?raw';
import f3 from './fields/field-3.svg?raw';
import f4 from './fields/field-4.svg?raw';
import f5 from './fields/field-5.svg?raw';
import f6 from './fields/field-6.svg?raw';

const FIELDS = [f1, f2, f3, f4, f5, f6];

export const Field: React.FC<{ n: number }> = ({ n }) => {
  // A stable object, or React re-sets innerHTML on every chapter re-render and the strokes restart.
  const html = useMemo(() => ({ __html: FIELDS[(n - 1) % FIELDS.length] }), [n]);
  return <div aria-hidden="true" className="fx-field" dangerouslySetInnerHTML={html} />;
};

export default Field;
