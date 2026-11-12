/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — mutually exclusive answer routes on a point card, as the
 * session screen shows them.
 *
 * A route (`MarkRow.route`) is one side of the SEC's "//" or "OR": a student
 * takes one route or the other and is never paid for a mix. The screen used
 * to print both routes as one unlabelled list, so a student found out they
 * were alternatives only when the second one locked, and "Select all" ticked
 * both although only one can score.
 *
 * Each route is labelled from the card's own data, never with written words:
 * the printed heading its rows share ("Method A diagram — …", "Method A
 * labels — …" give "Method A"), and where any route on the card has none, the
 * route's own letter ("Route A") or, for a slug id, its place ("Route 1").
 */

import { rowId, type MarkRow } from '../../types/markBank';

export interface RouteHead {
  route: string;
  /** What the heading reads: the printed heading, "Route A" or "Route 1". */
  label: string;
  /** 0 for the first route on the card; every later one is introduced by "OR". */
  ordinal: number;
  /** How many rows the route has; a one-row route needs no "Select all". */
  rowCount: number;
  /**
   * Whether headings are drawn. Where every route is a single row the row IS
   * the branch, often printed with its own label ("Scald — Inflammation …"),
   * so the routes are told apart by "OR" alone; a heading over each would
   * only repeat it.
   */
  titled: boolean;
}

/** The routes a card's rows offer, in the order the scheme first prints them. */
export function cardRoutes(rows: readonly MarkRow[]): string[] {
  const out: string[] = [];
  for (const r of rows) if (r.route && !out.includes(r.route)) out.push(r.route);
  return out;
}

/** The printed label a row carries before its marking point, if any. */
function rowLabel(verbatim: string): string | null {
  const dash = verbatim.split(' — ');
  if (dash.length >= 2 && dash[0].trim()) return dash[0].trim();
  const colon = /^([^:]{2,40}):\s/.exec(verbatim);
  if (colon && colon[1].trim().split(/\s+/).length <= 4) return colon[1].trim();
  return null;
}

/** The words every label starts with: "Method A diagram" + "Method A labels" → "Method A". */
function sharedWords(labels: string[]): string {
  const words = labels.map(label => label.split(/\s+/));
  const out: string[] = [];
  for (let i = 0; i < words[0].length; i++) {
    const word = words[0][i];
    if (!words.every(w => w[i] === word)) break;
    out.push(word);
  }
  return out.join(' ').replace(/[\s,;:·—-]+$/, '');
}

/** The heading each route's rows share, or null where a route has none. */
function printedHeadings(rows: readonly MarkRow[], routes: string[]): string[] | null {
  const headings = routes.map(route => {
    const labels = rows.filter(r => r.route === route).map(r => rowLabel(r.verbatim)).filter((l): l is string => !!l);
    return labels.length ? sharedWords(labels) : '';
  });
  // All or none: "Method" over one route and "Route B" over the other reads as
  // two different kinds of thing. Two routes sharing a heading tell nothing apart.
  if (headings.some(h => !h) || new Set(headings).size !== headings.length) return null;
  return headings;
}

const headCache = new WeakMap<readonly MarkRow[], Map<string, RouteHead>>();

/** Every route's heading, keyed by route; empty unless the card offers two or more. */
export function routeHeads(rows: readonly MarkRow[]): Map<string, RouteHead> {
  const cached = headCache.get(rows);
  if (cached) return cached;
  const routes = cardRoutes(rows);
  const heads = new Map<string, RouteHead>();
  if (routes.length >= 2) {
    const printed = printedHeadings(rows, routes);
    const lettered = routes.every(route => /^[a-z]$/i.test(route));
    const counts = routes.map(route => rows.filter(r => r.route === route).length);
    const titled = counts.some(n => n > 1);
    routes.forEach((route, ordinal) => heads.set(route, {
      route,
      label: printed ? printed[ordinal] : lettered ? `Route ${route.toUpperCase()}` : `Route ${ordinal + 1}`,
      ordinal,
      rowCount: counts[ordinal],
      titled,
    }));
  }
  headCache.set(rows, heads);
  return heads;
}

/**
 * The order rows are shown in: as printed, except that a route's rows are
 * kept together where the scheme interleaves them (Physics 2021 OL
 * Q14(c)(ii) alternates compass and filings steps), so each route sits under
 * one heading. Indexes are the rows' own, so row ids never change.
 */
export function routeDisplayOrder(rows: readonly MarkRow[]): number[] {
  if (cardRoutes(rows).length < 2) return rows.map((_, i) => i);
  const placed = new Set<string>();
  const order: number[] = [];
  rows.forEach((r, i) => {
    if (!r.route) { order.push(i); return; }
    if (placed.has(r.route)) return;
    placed.add(r.route);
    rows.forEach((s, j) => { if (s.route === r.route) order.push(j); });
  });
  return order;
}

/** The route heading to draw above the row at `index`, if it opens a route. */
export function routeHeadAt(rows: readonly MarkRow[], index: number): RouteHead | null {
  const route = rows[index]?.route;
  if (!route) return null;
  const head = routeHeads(rows).get(route);
  if (!head) return null;
  const first = rows.findIndex(r => r.route === route);
  return first === index ? head : null;
}

/**
 * The claims "Select all" makes on one route: every row of that route and
 * every row outside all routes is claimed, menus fill to their cap, and the
 * other routes are cleared, so the student never holds ticks the examiner
 * would not pay.
 */
export function routeSelection(rows: readonly MarkRow[], route: string): {
  claims: Record<string, 'yes' | 'no'>;
  picks: Record<string, number[]>;
} {
  const claims: Record<string, 'yes' | 'no'> = {};
  const picks: Record<string, number[]> = {};
  rows.forEach((r, i) => {
    const id = rowId(r, i);
    const taken = !r.route || r.route === route;
    claims[id] = taken ? 'yes' : 'no';
    if (r.kind === 'anyN' && r.group) {
      picks[id] = taken ? Array.from({ length: r.group.claimMax }, (_, k) => k) : [];
    }
  });
  return { claims, picks };
}
