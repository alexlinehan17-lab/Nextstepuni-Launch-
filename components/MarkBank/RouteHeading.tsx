/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The heading over one mutually exclusive answer route on a point card
 * (see routes.ts): its label from the card data, "OR" before every route
 * after the first, a "Select all" that acts on this route alone, and, once
 * the student has claimed from another route, one line saying this route is
 * not marked with it.
 */

import React from 'react';
import type { RouteHead } from './routes';
import './route-heading.css';

/** Said once per route not taken. It used to sit under every one of the route's rows. */
export const ROUTE_LOCKED_NOTE = 'The examiner marks one route or the other — not a mix of both.';

/** Renders nothing above the first of several one-row routes: "OR" starts the next. */
const RouteHeading: React.FC<{
  head: RouteHead;
  /** The route the student has claimed from, if any. */
  taken: string | null;
  onSelectAll: (route: string) => void;
}> = ({ head, taken, onSelectAll }) => {
  const locked = !!taken && taken !== head.route;
  if (!head.titled && head.ordinal === 0 && !locked) return null;
  return (
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
      {locked && <p className="mb-route-locked">{ROUTE_LOCKED_NOTE}</p>}
    </div>
  );
};

export default RouteHeading;
