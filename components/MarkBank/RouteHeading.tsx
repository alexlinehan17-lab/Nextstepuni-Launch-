/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The heading over one mutually exclusive answer route on a point card
 * (see routes.ts): its label from the card data, "OR" before every route
 * after the first, and a "Select all" that acts on this route alone.
 */

import React from 'react';
import type { RouteHead } from './routes';
import './route-heading.css';

/** Renders nothing above the first of several one-row routes: "OR" starts the next. */
const RouteHeading: React.FC<{
  head: RouteHead;
  /** The route the student has claimed from, if any. */
  taken: string | null;
  onSelectAll: (route: string) => void;
}> = ({ head, taken, onSelectAll }) => (!head.titled && head.ordinal === 0 ? null :
  <div className="mb-route-head" data-state={!taken ? 'open' : taken === head.route ? 'taken' : 'other'}>
    {head.ordinal > 0 && <p className="mb-route-or"><span>or</span></p>}
    {head.titled && <div className="mb-route-title">
      <h4>{head.label}</h4>
      {head.rowCount > 1 && (
        <button type="button" aria-label={`Select all in ${head.label}`} onClick={() => onSelectAll(head.route)}>
          Select all in this route
        </button>
      )}
    </div>}
  </div>
);

export default RouteHeading;
