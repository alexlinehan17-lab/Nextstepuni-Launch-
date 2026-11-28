/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A Launchpad tool's say over its one top bar (navigation.md, "Top bar").
 * The Launchpad draws the bar; a tool with pages of its own (Mark Bank: the
 * subject home, a strand, a topic) names the page it is on and may put one
 * action at the right end, where the phone bar otherwise shows the tool's
 * drawing (the Mark Bank boards: search in the bar on the subject home, an
 * empty end on a strand or a topic).
 *
 *   useToolBar({ over: 'Mark Bank', title: 'Biology' });
 *   useToolBar({ over: 'The practice library', title: 'Mark Bank', search: { label: 'Search topics', onPress: openSearch } });
 *
 * Outside the Launchpad (a test, the parts sheet) it does nothing.
 */
import { createContext, useContext, useEffect, useRef } from 'react';

export interface ToolBarSearch { label: string; onPress: () => void }

export interface ToolBarWords {
  /** The small line over the name. */
  over: string;
  /** The page's name. */
  title: string;
  /** One search action at the right end, in place of the tool's drawing. */
  search?: ToolBarSearch;
}

/** What the Launchpad holds: the words, and the search action by its label (the press is read through a ref). */
export interface ToolBarState { over: string; title: string; searchLabel?: string; onSearch?: () => void }

export const ToolBarContext = createContext<((bar: ToolBarState | null) => void) | null>(null);

/** Name the tool's current page in the Launchpad's bar while this is mounted; null gives the bar back. */
export function useToolBar(bar: ToolBarWords | null) {
  const set = useContext(ToolBarContext);
  const press = useRef<(() => void) | undefined>(undefined);
  press.current = bar?.search?.onPress;
  const over = bar?.over;
  const title = bar?.title;
  const searchLabel = bar?.search?.label;
  const hasSearch = Boolean(bar?.search);
  const shown = Boolean(bar);
  useEffect(() => {
    if (!set) return undefined;
    set(shown && over !== undefined && title !== undefined
      ? { over, title, searchLabel, onSearch: hasSearch ? () => press.current?.() : undefined }
      : null);
    return () => set(null);
  }, [set, shown, over, title, searchLabel, hasSearch]);
}
