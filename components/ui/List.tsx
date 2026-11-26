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
import { type ReactNode } from 'react';
import { ChevronRight } from 'lucide-react';
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
  /** A subject's character, bare, 40px at the left. */
  art?: string;
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
  /** Or a link. */
  href?: string;
  className?: string;
}

export function Row({ title, over, meta, art, icon, tone, value, trailing, onPress, href, className = '' }: RowProps) {
  const pressable = Boolean(onPress || href);
  const content = (
    <>
      {icon ? <span className="ui-row-icon" aria-hidden="true">{icon}</span> : null}
      {art ? <ThemeArtwork className="ui-row-art" src={art} transparentBackground alt="" /> : null}
      <span className="ui-row-body">
        {over ? <span className="ui-row-over">{over}</span> : null}
        <span className="ui-row-title">{title}</span>
        {meta ? <span className="ui-row-meta">{meta}</span> : null}
      </span>
      {value !== undefined && value !== null ? <span className="ui-row-value ui-readout">{value}</span> : null}
      {trailing ?? null}
      {pressable && !trailing && tone !== 'danger' ? <ChevronRight className="ui-icon ui-row-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" /> : null}
    </>
  );
  const classes = `ui-part ui-row${tone === 'danger' ? ' ui-row--danger' : ''} ${className}`.trim();
  return (
    <li className="ui-row-item">
      {href ? <a className={classes} href={href}>{content}</a>
        : onPress ? <button type="button" className={classes} onClick={onPress}>{content}</button>
          : <div className={classes}>{content}</div>}
    </li>
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
  className?: string;
}

/** A box you press (level 1): a line; it looks pressed when pressed. */
export function PressBox({ children, onPress, href, label, className = '' }: PressBoxProps) {
  const classes = `ui-part ui-press ${className}`.trim();
  if (href) return <a className={classes} href={href} aria-label={label}>{children}</a>;
  return <button type="button" className={classes} onClick={onPress} aria-label={label}>{children}</button>;
}
