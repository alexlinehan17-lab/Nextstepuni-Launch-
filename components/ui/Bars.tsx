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
 * The phone's tab bar (MobileBottomNav in App.tsx) is the TabBar; the shared
 * page headers are the TopBar (area 0, the frame).
 * Placement is the shell's: the top bar is sticky at the top of its scroll
 * area, the tab bar and the footer sticky at the bottom; a shell that fixes
 * them to the glass wraps them in its own frame layer.
 */
import { useEffect, useState, type ReactNode } from 'react';
import { ChevronLeft, X, type LucideIcon } from 'lucide-react';
import { IconButton, TextButton } from './Button';
import { useFrameTabBar, useFrameTaskActive } from './Frame';
import ThemeArtwork from '../ThemeArtwork';
import './parts.css';

export interface LeaveControl {
  /** back: a page you tapped into. close: something that came up over where you were.
   *  cancel: a place that has become a task (study set-up once something is
   *  chosen): the word, which clears what was chosen and gives the place back. */
  kind: 'back' | 'close' | 'cancel';
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
  /** A Launchpad tool's own drawing, 36px at the right end of a phone's bar:
   *  its only appearance there (a source, or a drawn element). A laptop bar
   *  carries no drawing (Alex, 26 Nov 2026). */
  art?: string | ReactNode;
  /** Or one action at the right (an IconButton or one text action). */
  action?: ReactNode;
  /** A place on a laptop: one quiet action at the left end where a leave control would be
   *  ("How it works" on the island). Ignored when there is a leave control or a place label. */
  lead?: ReactNode;
  /** A control centred in the bar instead of a title (the island's selection bar on a laptop):
   *  midway between the bar's ends, with the lead and the action balancing it. */
  center?: ReactNode;
  /** A tool's bar: 52px row, 19px name. */
  tool?: boolean;
  /** A hairline under the bar, once content has scrolled beneath it. */
  ruled?: boolean;
  className?: string;
}

export function TopBar({ leave, title, over, placeLabel, art, action, lead, center, tool = false, ruled = false, className = '', ...rest }: TopBarProps & { 'data-student-page-header'?: boolean }) {
  const LeaveGlyph = leave?.kind === 'close' ? X : ChevronLeft;
  return (
    <header {...rest} className={`ui-part ui-bar frame-bar${tool ? ' ui-bar--tool' : ''}${ruled ? ' ui-bar--ruled' : ''}${art ? ' ui-bar--art' : ''} ${className}`.trim()}>
      <div className="ui-bar-row">
        <span className="ui-bar-slot">
          {leave?.kind === 'cancel'
            ? <TextButton className="ui-bar-cancel" onClick={leave.onPress}>{leave.label ?? 'Cancel'}</TextButton>
            : leave
            ? <IconButton label={leave.label ?? (leave.kind === 'close' ? 'Close' : 'Back')} onClick={leave.onPress}
                icon={<LeaveGlyph className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
            : placeLabel ? <span className="ui-bar-label">{placeLabel}</span> : lead ?? null}
        </span>
        {title ? (
          <span className="ui-bar-mid">
            {over ? <span className="ui-bar-over">{over}</span> : null}
            <h1 className="ui-bar-title">{title}</h1>
          </span>
        ) : center ? <span className="ui-bar-mid ui-bar-mid--control">{center}</span> : null}
        <span className="ui-bar-slot ui-bar-slot--end">
          {typeof art === 'string' ? <ThemeArtwork className="ui-bar-art" src={art} transparentBackground alt="" />
            : art ? <span className="ui-bar-art" aria-hidden="true">{art}</span> : action ?? null}
        </span>
      </div>
    </header>
  );
}

export interface TabBarItem<V extends string = string> {
  id: V;
  label: string;
  icon: LucideIcon;
  /** A first-visit tour stop on this tab (data-coach). */
  coach?: string;
}

export interface TabBarProps<V extends string> {
  /** The five places, always the same five in the same order. */
  items: TabBarItem<V>[];
  current: V | null;
  onSelect: (id: V) => void;
  /** The bar's accessible name (default "Places"). */
  label?: string;
  className?: string;
}

/** A text field has focus on a touch screen: the keyboard is up. */
function isTypingTarget(element: Element | null): boolean {
  if (!element) return false;
  if (element instanceof HTMLTextAreaElement) return true;
  if (element instanceof HTMLInputElement) return !/^(checkbox|radio|range|button|submit|reset|file|color|image|hidden)$/.test(element.type);
  return element instanceof HTMLElement && element.isContentEditable;
}

/** True while the on-screen keyboard is up (a touch screen with a text field
 *  focused). The tab bar steps aside then (navigation.md, "Tab bar"). */
export function useTouchKeyboardOpen(): boolean {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return undefined;
    const touch = window.matchMedia('(pointer: coarse)');
    const update = () => setOpen(touch.matches && isTypingTarget(document.activeElement));
    // Moving from one field to the next blurs, then focuses: read the result
    // once the focus has landed, so the bar does not flicker.
    let pending = 0;
    const later = () => { window.clearTimeout(pending); pending = window.setTimeout(update, 0); };
    document.addEventListener('focusin', later);
    document.addEventListener('focusout', later);
    return () => {
      window.clearTimeout(pending);
      document.removeEventListener('focusin', later);
      document.removeEventListener('focusout', later);
    };
  }, []);
  return open;
}

/** Five places, outline icons over a 10.5px label; the current one is ink with
 *  a 2px ink marker above it. It never starts anything, and it steps aside
 *  while the keyboard is up and while a screen is a task (useFrameTask). */
export function TabBar<V extends string>({ items, current, onSelect, label = 'Places', className = '' }: TabBarProps<V>) {
  const task = useFrameTaskActive();
  // While it is shown the frame knows there is a tab bar, so toasts and
  // floating controls clear it (--edge-bottom).
  useFrameTabBar(!task);
  const typing = useTouchKeyboardOpen();
  return (
    <nav aria-label={label} hidden={typing || task || undefined} className={`ui-part ui-tabbar frame-foot ${className}`.trim()}>
      {items.map(item => {
        const Icon = item.icon;
        return (
          <button key={item.id} type="button" className="ui-tab" data-coach={item.coach} aria-current={item.id === current ? 'page' : undefined} onClick={() => onSelect(item.id)}>
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
  /** An optional line over it that says where it goes ("Next: Your New OS", reading a module). */
  lead?: ReactNode;
  /** A hairline above it, when content scrolls under it. */
  ruled?: boolean;
  className?: string;
}

/** The pinned footer of a task screen. A screen has a tab bar or this, not both. */
export function PinnedFooter({ children, note, lead, ruled = false, className = '' }: PinnedFooterProps) {
  return (
    <div className={`ui-part ui-foot frame-foot${ruled ? ' ui-foot--ruled' : ''} ${className}`.trim()}>
      {lead ? <p className="ui-foot-lead">{lead}</p> : null}
      {children}
      {note ? <p className="ui-foot-note">{note}</p> : null}
    </div>
  );
}
