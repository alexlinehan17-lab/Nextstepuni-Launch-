/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The one button (components.md, "Buttons" and "Arrows"; the approved kit's
 * .btn / .link / .icon-btn). Three kinds and the icon button, three heights,
 * one shape. Rank is shown by kind, never by size:
 *
 *   <Button kind="main" size="lg" block arrow="forward">Start session</Button>
 *   <Button>Add a mock result</Button>                       the second kind
 *   <TextButton arrow="forward">Your plan</TextButton>       the text kind
 *   <TextButton tone="danger">Delete account</TextButton>
 *   <IconButton label="Back" icon={<ChevronLeft />} />       a 44 x 44 target
 *
 * A main button never goes dead. While a step is missing it says so directly
 * above itself, and pressing the sentence or the button takes the student to
 * the missing step:
 *
 *   <Button kind="main" size="lg" block arrow="forward"
 *     missing={{ sentence: 'Choose a subject and how long to study.', goTo: subjectRef }}>
 *     Choose your subject
 *   </Button>
 *
 * Something truly unavailable (locked, not for this plan) says why under it:
 *   <Button block unavailable="Opens when you finish Your interests.">Start What matters</Button>
 *
 * There is deliberately no `disabled` prop: a silent disabled button is on the
 * never-ship list. Migration: ActionButton / PrimaryActionButton / the Kobra
 * Button keep today's look for the screens that use them; each screen moves
 * onto this part in stage 2B or 4, with pictures.
 */
import React, { useId, type ButtonHTMLAttributes, type ReactNode, type RefObject } from 'react';
import { ArrowRight, ArrowUpRight, ChevronDown, ChevronRight, type LucideIcon } from 'lucide-react';
import './parts.css';

/** The four arrow meanings, one glyph each (components.md, "Arrows"). */
export type ArrowMeaning = 'opens' | 'forward' | 'menu' | 'leaves';

const ARROW_GLYPH = {
  opens: ChevronRight,   // this row opens a deeper screen
  forward: ArrowRight,   // move forward / go to another place
  menu: ChevronDown,     // opens a menu
  leaves: ArrowUpRight,  // leaves the app for a web page
} as const;

/** One small part for the four arrows. Ink or ink-3 by its parent's colour;
 *  never orange, never in a circle or a box. 1.75 stroke, 2 at 16px. */
export function Arrow({ meaning, size = 16, className = '' }: { meaning: ArrowMeaning; size?: 16 | 20 | 24; className?: string }) {
  const Glyph = ARROW_GLYPH[meaning];
  return (
    <Glyph
      className={`ui-icon ${className}`.trim()}
      width={size}
      height={size}
      strokeWidth={size === 16 ? 2 : 1.75}
      aria-hidden="true"
      focusable="false"
      data-arrow={meaning}
    />
  );
}

/** Where the missing step is: an element to bring into view and focus, or a
 *  function that opens it (a carousel, a sheet). */
export interface MissingStep {
  sentence: string;
  goTo: RefObject<HTMLElement | null> | (() => void);
}

const FOCUSABLE = 'input:not([disabled]), button:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])';
/** How long the missing step is outlined after the student is taken to it. */
const NUDGE_MS = 1100;

/** Bring the missing step into view, outline it for a moment and put focus on
 *  it (its checked option first, if it is a group of choices). */
export function goToMissingStep(goTo: MissingStep['goTo']) {
  if (typeof goTo === 'function') { goTo(); return; }
  const target = goTo.current;
  if (!target) return;
  const reduce = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  target.scrollIntoView?.({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
  const focusable = target.matches(FOCUSABLE)
    ? target
    : target.querySelector<HTMLElement>('[aria-checked="true"], [aria-selected="true"]') ?? target.querySelector<HTMLElement>(FOCUSABLE);
  if (focusable) focusable.focus({ preventScroll: true });
  else { if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true }); }
  target.setAttribute('data-ui-nudge', '');
  window.setTimeout(() => target.removeAttribute('data-ui-nudge'), NUDGE_MS);
}

export interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'disabled'> {
  /** main = charcoal, the one main action of a view; second = white with a line. */
  kind?: 'main' | 'second';
  /** lg 52 (the main action of a task screen), md 44 (everything else), sm 36 (toolbars and rows; still 44 to the finger). */
  size?: 'lg' | 'md' | 'sm';
  /** Full width. In a stack, buttons are the same width as each other. */
  block?: boolean;
  /** A trailing arrow. `forward` sets the label left and the arrow right. */
  arrow?: ArrowMeaning;
  /** The action cannot go yet: say what is missing, and take the student there. */
  missing?: MissingStep;
  /** Truly unavailable (locked, not for this plan): why, and when it opens. */
  unavailable?: string;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { kind = 'second', size = 'md', block = false, arrow, missing, unavailable, className = '', children, type = 'button', onClick, ...props },
  ref,
) {
  const sayId = useId();
  const classes = [
    'ui-part ui-btn',
    kind === 'main' ? 'ui-btn--main' : '',
    size === 'lg' ? 'ui-btn--lg' : size === 'sm' ? 'ui-btn--sm frame-hit' : '',
    block ? 'ui-btn--block' : '',
    arrow === 'forward' && block ? 'ui-btn--split' : '',
    unavailable ? 'ui-btn--unavailable' : '',
    missing ? 'ui-btn--waiting' : '',
    className,
  ].filter(Boolean).join(' ');
  const glyph = arrow ? <Arrow meaning={arrow} size={size === 'sm' ? 16 : 20} /> : null;

  if (unavailable) {
    return (
      <div className={`ui-part ui-unavailable${block ? ' ui-needs--block' : ''}`}>
        <button {...props} ref={ref} type={type} className={classes} aria-disabled="true" aria-describedby={sayId}
          onClick={event => event.preventDefault()}>
          <span>{children}</span>{glyph}
        </button>
        <p id={sayId} className="ui-unavailable-why">{unavailable}</p>
      </div>
    );
  }

  const button = (
    <button
      {...props}
      ref={ref}
      type={type}
      className={classes}
      aria-describedby={missing ? sayId : props['aria-describedby']}
      data-missing={missing ? '' : undefined}
      onClick={event => {
        if (missing) { event.preventDefault(); goToMissingStep(missing.goTo); return; }
        onClick?.(event);
      }}
    >
      <span>{children}</span>{glyph}
    </button>
  );
  if (!missing) return button;
  return (
    <div className={`ui-part ui-needs${block ? ' ui-needs--block' : ''}`}>
      <button id={sayId} type="button" className="ui-need frame-hit" aria-live="polite" onClick={() => goToMissingStep(missing.goTo)}>
        {missing.sentence}
      </button>
      {button}
    </div>
  );
});

export interface TextButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'disabled'> {
  /** ink (default); quiet in ink-2 (Back or Skip in a flow); danger in red text (anything that deletes). */
  tone?: 'ink' | 'quiet' | 'danger';
  arrow?: ArrowMeaning;
}

/** The text button: third-rank actions, a way to another place, destructive actions. */
export const TextButton = React.forwardRef<HTMLButtonElement, TextButtonProps>(function TextButton(
  { tone = 'ink', arrow, className = '', children, type = 'button', ...props },
  ref,
) {
  const classes = ['ui-part ui-link frame-hit', tone === 'quiet' ? 'ui-link--quiet' : tone === 'danger' ? 'ui-link--danger' : '', className].filter(Boolean).join(' ');
  return (
    <button {...props} ref={ref} type={type} className={classes}>
      <span>{children}</span>{arrow ? <Arrow meaning={arrow} size={16} /> : null}
    </button>
  );
});

export interface IconButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'disabled' | 'aria-label'> {
  /** The accessible name: an icon-only control always has one. */
  label: string;
  /** A 24px outline glyph (lucide-react, 1.75 stroke). */
  icon: ReactNode;
}

/** A bare glyph in a 44 x 44 target: bar actions and the one leave control. */
export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(function IconButton(
  { label, icon, className = '', type = 'button', ...props },
  ref,
) {
  return (
    <button {...props} ref={ref} type={type} aria-label={label} className={`ui-part ui-icon-btn ${className}`.trim()}>
      {icon}
    </button>
  );
});

/** A 24px outline glyph for an IconButton, drawn at the system's stroke. */
export function Glyph({ icon: Icon, size = 24 }: { icon: LucideIcon; size?: 16 | 20 | 24 }) {
  return <Icon className="ui-icon" width={size} height={size} strokeWidth={size === 16 ? 2 : 1.75} aria-hidden="true" focusable="false" />;
}
