/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Rows and lists, the sheet of paper, and the pressable box (components.md,
 * "Rows and lists" and "Boxes and the sheet"; tokens.md, "Depth on a white
 * page"; the kit's .list / .row / .card / .press).
 *
 *   <List>                                             ruled rows on the page (level 0): a <ul> of <li> rows
 *     <Row art={crew.accounting} title="Accounting" meta="Practice · 45 min" onPress={open} />   a chevron: it opens something
 *     <Row title="Sessions this week" value="6 / 8" />                                         a value: it shows something
 *     <Row title="Offer me questions when I finish" trailing={<Switch ... />} />              a switch: no chevron
 *   </List>
 *   <List boxed> ...rows that together are one control (study set-up)... </List>
 *   <PaperSheet> ...the one thing this screen is about... </PaperSheet>   level 2, at most one per screen
 *   <PressBox onPress={openPaper}> ...a paper's cover... </PressBox>        level 1
 *
 * A box means "press me": a line. It also reads --lift-ctl, the one token for
 * level-1 lift, which is empty since the owner chose "a line only" over "a line
 * with a hair of lift" (26 Nov 2026). Read-only content is not boxed.
 */
import { type ButtonHTMLAttributes, type ReactNode } from 'react';
import { ArrowRight, ChevronDown, ChevronRight } from 'lucide-react';
import ThemeArtwork from '../ThemeArtwork';
import './parts.css';

export function List({ boxed = false, children, className = '', label }: { boxed?: boolean; children: ReactNode; className?: string; label?: string }) {
  return (
    <ul aria-label={label} className={`ui-part ui-list${boxed ? ' ui-list--boxed' : ''} ${className}`.trim()}>
      {children}
    </ul>
  );
}

export interface RowProps {
  title: ReactNode;
  /** A small line above the title ("Subject" over "Mathematics", in a boxed set-up row). */
  over?: ReactNode;
  /** A second line in meta. */
  meta?: ReactNode;
  /** A subject's character, bare, 40px at the left: its source, or a drawn
   *  element that already picks its own artwork (SubjectAvatar). */
  art?: string | ReactNode;
  /** The row's accessible name, when its visible words do not say what
   *  pressing it does ("Study Irish: Revision, 25 minutes"). */
  label?: string;
  /** A first-visit tour stop on this row (data-coach). */
  coach?: string;
  /** A value or readout at the trailing edge (a row that shows something). */
  value?: ReactNode;
  /** A switch or other control at the trailing edge (no chevron). */
  trailing?: ReactNode;
  /** A bare 20px glyph at the left, in ink-2 (the account sheet's rows). */
  icon?: ReactNode;
  /** A destructive action (Log out): red words, no arrow. */
  tone?: 'danger';
  /** The row opens something: it is a button with a chevron and a pressed state. */
  onPress?: () => void;
  /** The row moves forward to the next part of the same screen ("Next · 2 of 5, Study"):
   *  an arrow-right in place of the chevron. */
  forward?: boolean;
  /** The row opens in place, under itself (a mock's subjects): aria-expanded, and a
   *  chevron-down that turns up while it is open. */
  expanded?: boolean;
  /** Or a link. */
  href?: string;
  className?: string;
}

export function Row({ title, over, meta, art, label, coach, icon, tone, value, trailing, onPress, href, forward = false, expanded, className = '' }: RowProps) {
  const pressable = Boolean(onPress || href);
  const content = (
    <>
      {icon ? <span className="ui-row-icon" aria-hidden="true">{icon}</span> : null}
      {typeof art === 'string' ? <ThemeArtwork className="ui-row-art" src={art} transparentBackground alt="" />
        : art ? <span className="ui-row-art" aria-hidden="true">{art}</span> : null}
      <span className="ui-row-body">
        {over ? <span className="ui-row-over">{over}</span> : null}
        <span className="ui-row-title">{title}</span>
        {meta ? <span className="ui-row-meta">{meta}</span> : null}
      </span>
      {value !== undefined && value !== null ? <span className="ui-row-value ui-readout">{value}</span> : null}
      {trailing ?? null}
      {pressable && !trailing && tone !== 'danger'
        ? forward ? <ArrowRight className="ui-icon ui-row-chev" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />
          : expanded !== undefined ? <ChevronDown className="ui-icon ui-row-chev ui-row-chev--down" data-open={expanded || undefined} width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
            : <ChevronRight className="ui-icon ui-row-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
        : null}
    </>
  );
  const classes = `ui-part ui-row${tone === 'danger' ? ' ui-row--danger' : ''} ${className}`.trim();
  return (
    <li className="ui-row-item">
      {href ? <a className={classes} href={href} aria-label={label} data-coach={coach}>{content}</a>
        : onPress ? <button type="button" className={classes} onClick={onPress} aria-label={label} aria-expanded={expanded} data-coach={coach}>{content}</button>
          : <div className={classes}>{content}</div>}
    </li>
  );
}

export interface CheckRowProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'role' | 'onChange'> {
  checked: boolean;
  onChange: (checked: boolean) => void;
  /** The mark the screen draws for this row (the session's dotted ring). */
  mark: ReactNode;
}

/** A row you tick (Time's up: "tap one you finished to fill it"): the whole row
 *  is the checkbox, with no box round it; its mark is the screen's own. */
export function CheckRow({ checked, onChange, mark, children, className = '', type = 'button', ...props }: CheckRowProps) {
  return (
    <button {...props} type={type} role="checkbox" aria-checked={checked}
      className={`ui-part ui-checkrow ${className}`.trim()} onClick={() => onChange(!checked)}>
      {mark}<span className="ui-checkrow-label">{children}</span>
    </button>
  );
}

/** The one raised sheet of a screen: white, a line, the soft lift, and two
 *  more sheets tilted 1.3 degrees behind it, as on sign-in. */
export function PaperSheet({ children, className = '', label }: { children: ReactNode; className?: string; label?: string }) {
  return (
    <section aria-label={label} className={`ui-part ui-paper ${className}`.trim()}>
      <div className="ui-paper-face">{children}</div>
    </section>
  );
}

export interface PressBoxProps {
  children: ReactNode;
  onPress?: () => void;
  href?: string;
  /** The accessible name, if the box's own text does not say what pressing it does. */
  label?: string;
  /** The box opens a list in place under itself (a world's finished modules): aria-expanded. */
  expanded?: boolean;
  /** The box turns something over in place (a module's "Tap to reframe" card): aria-pressed. */
  pressed?: boolean;
  className?: string;
}

/** A box you press (level 1): a line; it looks pressed when pressed. */
export function PressBox({ children, onPress, href, label, expanded, pressed, className = '' }: PressBoxProps) {
  const classes = `ui-part ui-press ${className}`.trim();
  if (href) return <a className={classes} href={href} aria-label={label}>{children}</a>;
  return <button type="button" className={classes} onClick={onPress} aria-label={label} aria-expanded={expanded} aria-pressed={pressed}>{children}</button>;
}
