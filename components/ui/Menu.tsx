/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The menu button and its menu (components.md, "Menus and dropdowns"; the
 * kit's .menu-btn / .menu): up to about seven short options. The button shows
 * the current value and a chevron-down; the menu grows from the button, the
 * current option has a tick, and choosing applies at once and closes it.
 *
 *   <Menu label="Subject" value={subject} onChange={setSubject}
 *     options={[{ value: 'all', label: 'All subjects' }, { value: 'acc', label: 'Accounting' }]} />
 *   <Menu label="Progress section" count value={section} onChange={go} options={sections} />   "Overview · 1 of 5"
 *
 * Why it is built this way. Today's hand-built menus close when focus leaves
 * them; on an iPhone a tapped button never takes focus, so the menu sees focus
 * "leave" at touch-down and closes before the tap lands (the dead My Progress
 * picker, audit 03 F.3). This menu never closes on focus loss: it is the Base
 * UI Menu, the same primitive the Kobra DropdownMenu wraps, which closes only
 * on a choice, Escape, a tap outside or the button (its focus-out close needs
 * a real element to have taken focus, and a tap gives none). It is used
 * directly rather than through the compiled Kobra wrapper because the wrapper
 * does not pass `collisionPadding` through, and the menu must open inside the
 * safe box: never under the Dynamic Island, never on the tab bar or the home
 * indicator. (The Mark Bank subject dropdown today is a Kobra Select that
 * lines its list up over the button and can open up under the island.)
 *
 * More than about seven options, options that need explaining, or several
 * filters together: a Sheet of choice tiles instead.
 */
import { useState, type ReactNode } from 'react';
import { Menu as BaseMenu } from '@base-ui/react/menu';
import { Check, ChevronDown } from 'lucide-react';
import { readSafeArea } from './Frame';
import './parts.css';

export interface MenuOption<V extends string = string> {
  value: V;
  label: ReactNode;
  /** The text read in the button when this option is current (defaults to label). */
  short?: ReactNode;
}

export interface MenuProps<V extends string> {
  /** What the menu chooses, for screen readers ("Subject", "Progress section"). */
  label: string;
  options: MenuOption<V>[];
  value: V;
  /** Called the moment an option is tapped; the menu closes itself. */
  onChange: (value: V) => void;
  /** Show the position after the value: "Overview · 1 of 5" (moving between the parts of a screen).
   *  In a full-width button the position sits at the trailing edge in the readout mono. */
  count?: boolean;
  /** Number the options "01", "02" in the readout mono, before each name (the parts of a screen). */
  numbered?: boolean;
  /** A readout at the trailing edge of a full-width button, about the current value ("2 entries"). */
  detail?: ReactNode;
  /** Full width, the chevron at the trailing edge. */
  block?: boolean;
  /** Which side of the button it prefers; it moves to the other when there is no room. */
  side?: 'bottom' | 'top';
  /** The button shows this instead of the current value: a row that opens a menu of choices
   *  ("Find a starting point" on Modules on a laptop). Its chevron-down stays at the trailing edge. */
  face?: ReactNode;
  className?: string;
}

/** The gap kept between a menu and the edges of the safe box. */
const MENU_GAP = 8;

/** The safe box as collision padding: the insets, the tab bar while it is
 *  mounted, and a small gap. Read when the menu opens. */
export function menuCollisionPadding() {
  const safe = readSafeArea();
  const tabbar = typeof document === 'undefined' ? 0
    : parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--tabbar-h')) || 0;
  return {
    top: safe.top + MENU_GAP,
    right: safe.right + MENU_GAP,
    bottom: safe.bottom + tabbar + MENU_GAP,
    left: safe.left + MENU_GAP,
  };
}

export function Menu<V extends string>({ label, options, value, onChange, count = false, numbered = false, detail, block = false, side = 'bottom', face, className = '' }: MenuProps<V>) {
  const [open, setOpen] = useState(false);
  const index = options.findIndex(option => option.value === value);
  const current = options[index];
  const position = count && index >= 0 ? `${index + 1} of ${options.length}` : null;
  return (
    <BaseMenu.Root open={open} onOpenChange={setOpen}>
      <BaseMenu.Trigger className={`ui-part ui-menu-btn${block ? ' ui-menu-btn--block' : ''} ${className}`.trim()}>
        <span className="ui-menu-btn-text">
          {face ? null : <span className="sr-only">{label}: </span>}
          {face ?? current?.short ?? current?.label}
          {position && !block ? <span className="ui-menu-btn-count">{` · ${position}`}</span> : null}
        </span>
        {position && block ? <span className="ui-menu-btn-count ui-menu-btn-count--end ui-readout"><span className="sr-only"> · </span>{position}</span> : null}
        {detail && !position ? <span className="ui-menu-btn-count ui-menu-btn-count--end ui-readout"><span className="sr-only"> · </span>{detail}</span> : null}
        <ChevronDown className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" focusable="false" />
      </BaseMenu.Trigger>
      <BaseMenu.Portal>
        <BaseMenu.Positioner
          className="ui-menu-layer"
          side={side}
          align="start"
          sideOffset={6}
          collisionPadding={open ? menuCollisionPadding() : MENU_GAP}
        >
          <BaseMenu.Popup className="ui-part ui-menu" aria-label={label}>
            <BaseMenu.RadioGroup value={value} onValueChange={next => onChange(next as V)}>
              {options.map((option, place) => (
                <BaseMenu.RadioItem key={option.value} value={option.value} closeOnClick className="ui-menu-item">
                  <span className={numbered ? 'ui-menu-item-text' : undefined}>
                    {numbered ? <i className="ui-menu-num ui-readout" aria-hidden="true">{String(place + 1).padStart(2, '0')}</i> : null}
                    {numbered ? <span>{option.label}</span> : option.label}
                  </span>
                  <Check className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
                </BaseMenu.RadioItem>
              ))}
            </BaseMenu.RadioGroup>
          </BaseMenu.Popup>
        </BaseMenu.Positioner>
      </BaseMenu.Portal>
    </BaseMenu.Root>
  );
}
