/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The bars (navigation.md, "The bars"; the kit's .nav / .tabbar / .foot).
 * Each owns its safe area through the frame: the top bar is a frame-bar, the
 * tab bar and the pinned footer are frame-foots.
 *
 *   <TopBar leave={{ kind: 'back', onPress: goBack }} title="Biology" action={<IconButton ... />} />
 *   <TopBar tool leave={{ kind: 'back', onPress: goBack }} over="Start with you" title="Future Finder" art="/assets/tools/future-finder-revamped.png" />
 *   <TopBar leave={{ kind: 'close', onPress: close }} title="Practice" />           an over-screen
 *   <TopBar placeLabel="Tuesday, 24 November" />                                     a place: no leave control
 *   <TabBar items={places} current="home" onSelect={go} />
 *   <PinnedFooter note="Your answers stay as you go back">
 *     <Button kind="main" size="lg" block arrow="forward" missing={...}>Continue</Button>
 *   </PinnedFooter>
 *
 * These are parts only: the live tab bar (MobileBottomNav in App.tsx) and every
 * live header stay as they are until stage 3 moves navigation onto them.
 * Placement is the shell's: the top bar is sticky at the top of its scroll
 * area, the tab bar and the footer sticky at the bottom; a shell that fixes
 * them to the glass wraps them in its own frame layer.
 */
import { type ReactNode } from 'react';
import { ChevronLeft, X, type LucideIcon } from 'lucide-react';
import { IconButton } from './Button';
import { useFrameTabBar } from './Frame';
import ThemeArtwork from '../ThemeArtwork';
import './parts.css';

export interface LeaveControl {
  /** back: a page you tapped into. close: something that came up over where you were. */
  kind: 'back' | 'close';
  onPress: () => void;
  /** Accessible name (default "Back" / "Close"). */
  label?: string;
}

export interface TopBarProps {
  /** The one leave control, top left. A place has none. */
  leave?: LeaveControl;
  /** The screen's name, in the middle. A place leaves it out (the tab bar already says where you are). */
  title?: ReactNode;
  /** The small line over the title ("Start with you" over "Future Finder"). */
  over?: ReactNode;
  /** A place's small capitals label at the left (the date on Home). */
  placeLabel?: ReactNode;
  /** A Launchpad tool's own drawing, 36px at the right end: its only appearance on the screen. */
  art?: string;
  /** Or one action at the right (an IconButton or one text action). */
  action?: ReactNode;
  /** A tool's bar: 52px row, 19px name. */
  tool?: boolean;
  /** A hairline under the bar, once content has scrolled beneath it. */
  ruled?: boolean;
  className?: string;
}

export function TopBar({ leave, title, over, placeLabel, art, action, tool = false, ruled = false, className = '' }: TopBarProps) {
  const LeaveGlyph = leave?.kind === 'close' ? X : ChevronLeft;
  return (
    <header className={`ui-part ui-bar frame-bar${tool ? ' ui-bar--tool' : ''}${ruled ? ' ui-bar--ruled' : ''} ${className}`.trim()}>
      <div className="ui-bar-row">
        <span className="ui-bar-slot">
          {leave
            ? <IconButton label={leave.label ?? (leave.kind === 'close' ? 'Close' : 'Back')} onClick={leave.onPress}
                icon={<LeaveGlyph className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
            : placeLabel ? <span className="ui-bar-label">{placeLabel}</span> : null}
        </span>
        {title ? (
          <span className="ui-bar-mid">
            {over ? <span className="ui-bar-over">{over}</span> : null}
            <h1 className="ui-bar-title">{title}</h1>
          </span>
        ) : null}
        <span className="ui-bar-slot ui-bar-slot--end">
          {art ? <ThemeArtwork className="ui-bar-art" src={art} transparentBackground alt="" /> : action ?? null}
        </span>
      </div>
    </header>
  );
}

export interface TabBarItem<V extends string = string> {
  id: V;
  label: string;
  icon: LucideIcon;
}

export interface TabBarProps<V extends string> {
  /** The five places, always the same five in the same order. */
  items: TabBarItem<V>[];
  current: V | null;
  onSelect: (id: V) => void;
  className?: string;
}

/** Five places, outline icons over a 10.5px label; the current one is ink with
 *  a 2px ink marker above it. It never starts anything. */
export function TabBar<V extends string>({ items, current, onSelect, className = '' }: TabBarProps<V>) {
  // While it is mounted the frame knows there is a tab bar, so toasts and
  // floating controls clear it (--edge-bottom).
  useFrameTabBar();
  return (
    <nav aria-label="Places" className={`ui-part ui-tabbar frame-foot ${className}`.trim()}>
      {items.map(item => {
        const Icon = item.icon;
        return (
          <button key={item.id} type="button" className="ui-tab" aria-current={item.id === current ? 'page' : undefined} onClick={() => onSelect(item.id)}>
            <Icon className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />
            <span>{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
}

export interface PinnedFooterProps {
  /** The one main action: a full-width 52px main Button (give it `missing` to name what is still needed). */
  children: ReactNode;
  /** An optional quiet line under it. */
  note?: ReactNode;
  /** A hairline above it, when content scrolls under it. */
  ruled?: boolean;
  className?: string;
}

/** The pinned footer of a task screen. A screen has a tab bar or this, not both. */
export function PinnedFooter({ children, note, ruled = false, className = '' }: PinnedFooterProps) {
  return (
    <div className={`ui-part ui-foot frame-foot${ruled ? ' ui-foot--ruled' : ''} ${className}`.trim()}>
      {children}
      {note ? <p className="ui-foot-note">{note}</p> : null}
    </div>
  );
}
