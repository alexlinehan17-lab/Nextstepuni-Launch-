/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Choosing (components.md, "Choices and the selection mark" and "Selection
 * bar"; motion.md, "The selection mark"; the kit's .choice / .pick / .switch /
 * .seg).
 *
 *   <ChoiceGroup legend="How much would you enjoy doing this?" value={v} onChange={setV}
 *     options={[{ value: 'love', label: "I'd love it" }, ...]} />
 *   <ChoiceGroup kind="several" tiles legend="Your subjects" value={picked} onChange={setPicked}
 *     options={[{ value: 'bio', label: 'Biology', meta: 'Add', metaChosen: 'Added' }, ...]} />
 *   <Switch checked={on} onChange={setOn} label="Offer me questions when I finish" />
 *   <SelectionBar label="Show" value={v} onChange={setV} options={[{ value: 'paper', label: 'Paper' }, ...]} />
 *
 * Chosen is an ink outline and a ring that fills ink while its tick draws.
 * Pick-one is a round ring, pick-several a rounded square with a count. A
 * switch is ink when on. The selection bar is for two to four one-word
 * choices; its white pill slides. Under reduced motion the tick simply
 * appears and nothing slides.
 *
 * Migration: HorizontalTabs (pill) keeps today's look for its 13 sites (a
 * spring with a little bounce, a 4px tray); each moves onto SelectionBar
 * screen by screen. ChoiceControl is unreachable today and can be deleted when
 * the first screen moves.
 */
import React, { useId, useRef, type KeyboardEvent, type ReactNode } from 'react';
import ThemeArtwork from '../ThemeArtwork';
import './parts.css';

/** The selection mark: a 22px ring (or rounded square) that fills ink and
 *  draws a white tick. */
export function SelectionMark({ on, shape = 'round' }: { on: boolean; shape?: 'round' | 'square' }) {
  return (
    <span className={`ui-mark${shape === 'square' ? ' ui-mark--square' : ''}${on ? ' ui-mark--on' : ''}`} aria-hidden="true" data-mark={on ? 'on' : 'off'}>
      <svg viewBox="0 0 12 12" focusable="false"><path d="M2.5 6.2l2.4 2.4 4.6-5" /></svg>
    </span>
  );
}

export interface ChoiceOption<V extends string = string> {
  value: V;
  label: ReactNode;
  /** A second line under the label. */
  meta?: ReactNode;
  /** The second line once chosen: say the state in words ("Add" becomes "Added"). */
  metaChosen?: ReactNode;
  /** A subject's Star Crew character, bare, 40px at the left. */
  art?: string;
}

export interface ChoiceTileProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'role'> {
  chosen: boolean;
  /** one: a radio (round mark); several: a checkbox (square mark); toggle: a button that stays
   *  pressed (aria-pressed, round mark), for a screen whose choice is not part of a group. */
  kind?: 'one' | 'several' | 'toggle';
  tile?: boolean;
  label: ReactNode;
  meta?: ReactNode;
  art?: string;
  /** The answer line under a chosen answer (a module's own words for it). The words are
   *  ink, never green; `ok` puts the green tick beside them (Alex, 26 Nov 2026: "can be
   *  black. Don't like the dark green text"); `plain` is a quieter line with no tick. */
  note?: ReactNode;
  noteTone?: 'ok' | 'plain';
  /** Short choices in a row (self-mark's Blank to Full, why marks were lost): 44px tall, the
   *  words centred, no ring until chosen, then the ink outline and the tick drawn before the
   *  words. Not with `art`, `meta`, `note` or `tile`. */
  compact?: boolean;
}

/** The green tick that sits beside an answer line: the only green on an answer. */
export function AnswerTick({ className = '' }: { className?: string }) {
  return (
    <svg className={`ui-tick ${className}`.trim()} viewBox="0 0 12 12" aria-hidden="true" focusable="false">
      <path d="M2.5 6.2l2.4 2.4 4.6-5" />
    </svg>
  );
}

/** One choice: an outlined tile before it is touched; chosen, an ink outline. */
export const ChoiceTile = React.forwardRef<HTMLButtonElement, ChoiceTileProps>(function ChoiceTile(
  { chosen, kind = 'one', tile = false, label, meta, art, note, noteTone = 'ok', compact = false, className = '', type = 'button', ...props },
  ref,
) {
  if (compact) {
    return (
      <button
        {...props}
        ref={ref}
        type={type}
        role={kind === 'one' ? 'radio' : kind === 'several' ? 'checkbox' : undefined}
        aria-checked={kind === 'toggle' ? undefined : chosen}
        aria-pressed={kind === 'toggle' ? chosen : undefined}
        className={`ui-part ui-choice ui-choice--compact ${className}`.trim()}
      >
        <SelectionMark on={chosen} shape={kind === 'several' ? 'square' : 'round'} />
        <span className="ui-choice-label">{label}</span>
      </button>
    );
  }
  return (
    <button
      {...props}
      ref={ref}
      type={type}
      role={kind === 'one' ? 'radio' : kind === 'several' ? 'checkbox' : undefined}
      aria-checked={kind === 'toggle' ? undefined : chosen}
      aria-pressed={kind === 'toggle' ? chosen : undefined}
      className={`ui-part ui-choice${tile ? ' ui-choice--tile' : ''} ${className}`.trim()}
    >
      {art ? <ThemeArtwork className="ui-choice-art" src={art} transparentBackground alt="" /> : null}
      <span className="ui-choice-body">
        <span className="ui-choice-label">{label}</span>
        {/* The space keeps the accessible name two words apart ("Practice Work
            through questions"); a flex column does not draw it. */}
        {meta ? <>{' '}<span className="ui-choice-meta">{meta}</span></> : null}
        {note ? <>{' '}<span className={`ui-choice-note${noteTone === 'ok' ? ' ui-choice-note--ok' : ''}`}>{noteTone === 'ok' ? <AnswerTick /> : null}<span>{note}</span></span></> : null}
      </span>
      <SelectionMark on={chosen} shape={kind === 'several' ? 'square' : 'round'} />
    </button>
  );
});

/** Arrow keys move through a row of radios; the one they land on is chosen.
 *  Exported for a screen that lays out its own radios (study set-up's subject
 *  names and its time presets) with ChoiceTile. */
export function useRovingRadios(count: number, current: number, choose: (index: number) => void) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const onKeyDown = (event: KeyboardEvent, index: number) => {
    const step = event.key === 'ArrowRight' || event.key === 'ArrowDown' ? 1
      : event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? -1 : 0;
    let next = step ? (index + step + count) % count : index;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = count - 1;
    if (next === index && !step) return;
    event.preventDefault();
    choose(next);
    refs.current[next]?.focus();
  };
  const tabIndexOf = (index: number) => (index === (current >= 0 ? current : 0) ? 0 : -1);
  return { refs, onKeyDown, tabIndexOf };
}

type OneProps<V extends string> = { kind?: 'one'; value: V | null; onChange: (value: V) => void };
type SeveralProps<V extends string> = { kind: 'several'; value: V[]; onChange: (value: V[]) => void };
export type ChoiceGroupProps<V extends string> = (OneProps<V> | SeveralProps<V>) & {
  legend: ReactNode;
  options: ChoiceOption<V>[];
  /** Two columns of tiles at least 88px tall, instead of a column of rows. */
  tiles?: boolean;
  className?: string;
};

/** A question and its answers. Pick-one is a radio group with arrow keys;
 *  pick-several shows "2 of 4 chosen". */
export function ChoiceGroup<V extends string>(props: ChoiceGroupProps<V>) {
  const { legend, options, tiles = false, className = '' } = props;
  const legendId = useId();
  const several = props.kind === 'several';
  const isChosen = (value: V) => (several ? (props.value as V[]).includes(value) : props.value === value);
  const current = several ? -1 : options.findIndex(option => option.value === props.value);
  const chooseOne = (index: number) => { if (!several) (props.onChange as (v: V) => void)(options[index].value); };
  const roving = useRovingRadios(options.length, current, chooseOne);
  const toggle = (value: V) => {
    if (several) {
      const list = props.value as V[];
      (props.onChange as (v: V[]) => void)(list.includes(value) ? list.filter(v => v !== value) : [...list, value]);
    } else (props.onChange as (v: V) => void)(value);
  };
  const count = several ? (props.value as V[]).length : 0;
  return (
    <div className={`ui-part ui-choices-group ${className}`.trim()}>
      <div className="ui-choices-head">
        <p id={legendId} className="ui-choices-legend">{legend}</p>
        {several ? <span className="ui-choices-count ui-readout" aria-live="polite">{`${count} of ${options.length} chosen`}</span> : null}
      </div>
      <div role={several ? 'group' : 'radiogroup'} aria-labelledby={legendId} className={tiles ? 'ui-choices ui-choices--tiles' : 'ui-choices'}>
        {options.map((option, index) => {
          const chosen = isChosen(option.value);
          return (
            <ChoiceTile
              key={option.value}
              ref={several ? undefined : element => { roving.refs.current[index] = element; }}
              kind={several ? 'several' : 'one'}
              tile={tiles}
              chosen={chosen}
              label={option.label}
              meta={chosen && option.metaChosen ? option.metaChosen : option.meta}
              art={option.art}
              tabIndex={several ? undefined : roving.tabIndexOf(index)}
              onKeyDown={several ? undefined : event => roving.onKeyDown(event, index)}
              onClick={() => toggle(option.value)}
            />
          );
        })}
      </div>
    </div>
  );
}

export interface SwitchProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'onChange' | 'role'> {
  checked: boolean;
  onChange: (checked: boolean) => void;
  /** The setting's name, if no visible label points at the switch (aria-labelledby). */
  label?: string;
}

/** For a setting that applies at once. Track line; ink when on. 44 tall to the finger. */
export const Switch = React.forwardRef<HTMLButtonElement, SwitchProps>(function Switch(
  { checked, onChange, label, className = '', type = 'button', onClick, ...props },
  ref,
) {
  return (
    <button
      {...props}
      ref={ref}
      type={type}
      role="switch"
      aria-checked={checked}
      aria-label={label ?? props['aria-label']}
      className={`ui-part ui-switch frame-hit ${className}`.trim()}
      onClick={event => { onClick?.(event); if (!event.defaultPrevented) onChange(!checked); }}
    >
      <span className="ui-switch-knob" />
    </button>
  );
});

export interface SelectionBarProps<V extends string> {
  /** What the bar chooses, for screen readers ("Show", "Questions"). */
  label: string;
  /** Two to four one-word choices. */
  options: { value: V; label: ReactNode }[];
  /** The current choice; a value not in `options` ("") means none chosen yet. */
  value: V | '';
  onChange: (value: V) => void;
  /** sm 36 (inside boxes) or md 44 (section level). */
  size?: 'sm' | 'md';
  className?: string;
}

export interface SelectionWordsProps<V extends string> {
  /** What the words choose, for screen readers ("Period", "Fieldbook page"). */
  label: string;
  /** Two to four short words. */
  options: { value: V; label: ReactNode }[];
  value: V;
  onChange: (value: V) => void;
  className?: string;
}

/** Choices as plain words (components.md, "Selection bar": Week / Month / Year,
 *  agreed 25 Nov 2026): the current word in ink with a short ink line under it,
 *  the others quieter; no tray. The line draws in under the new word; what it
 *  controls changes at once. A radio group with arrow keys, like the bar. */
export function SelectionWords<V extends string>({ label, options, value, onChange, className = '' }: SelectionWordsProps<V>) {
  const current = options.findIndex(option => option.value === value);
  const roving = useRovingRadios(options.length, current, index => onChange(options[index].value));
  return (
    <div role="radiogroup" aria-label={label} className={`ui-part ui-words ${className}`.trim()}>
      {options.map((option, index) => (
        <button
          key={option.value}
          ref={element => { roving.refs.current[index] = element; }}
          type="button"
          role="radio"
          aria-checked={index === current}
          tabIndex={roving.tabIndexOf(index)}
          className="ui-word"
          onKeyDown={event => roving.onKeyDown(event, index)}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

/** The selection bar: a tray with a white pill on the current choice. The pill
 *  slides (260ms, the move curve); what it controls changes at once. */
export function SelectionBar<V extends string>({ label, options, value, onChange, size = 'sm', className = '' }: SelectionBarProps<V>) {
  // Nothing chosen yet: no pill, and the first choice takes the keyboard.
  const current = options.findIndex(option => option.value === value);
  const roving = useRovingRadios(options.length, current, index => onChange(options[index].value));
  return (
    <div
      role="radiogroup"
      aria-label={label}
      className={`ui-part ui-seg${size === 'md' ? ' ui-seg--md' : ''} ${className}`.trim()}
      style={{ '--seg-n': options.length, '--seg-i': Math.max(0, current) } as React.CSSProperties}
      data-count={options.length}
    >
      {current >= 0 ? <i className="ui-seg-pill" aria-hidden="true" /> : null}
      {options.map((option, index) => (
        <button
          key={option.value}
          ref={element => { roving.refs.current[index] = element; }}
          type="button"
          role="radio"
          aria-checked={index === current}
          tabIndex={roving.tabIndexOf(index)}
          className="ui-seg-item frame-hit"
          onKeyDown={event => roving.onKeyDown(event, index)}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

export interface RulerOption<V extends string = string> {
  value: V;
  label: ReactNode;
  /** The choice's accessible name when its label is short ("Mathematics H3"). */
  name?: string;
  /** A small dot under the label (today's grade, on Points Passport's What if?). */
  marked?: boolean;
}

export interface ChoiceRulerProps<V extends string> {
  /** What the ruler chooses, for screen readers ("Mathematics grade"). */
  label: string;
  options: RulerOption<V>[];
  /** The chosen value; a value not in `options` means none chosen yet. */
  value: V | '';
  onChange: (value: V) => void;
  className?: string;
}

/** A ruler of short choices in one row (grades H1 to H8; the boards' c-tools1 "Tap a grade to try
 *  it"): one box you press, divided by hairlines; the chosen one gains the ink outline. For more
 *  than four short choices of one kind, where a selection bar would jam. A radio group with arrow
 *  keys; 44px tall to the finger. */
export function ChoiceRuler<V extends string>({ label, options, value, onChange, className = '' }: ChoiceRulerProps<V>) {
  const current = options.findIndex(option => option.value === value);
  const roving = useRovingRadios(options.length, current, index => onChange(options[index].value));
  return (
    <div role="radiogroup" aria-label={label} className={`ui-part ui-ruler ${className}`.trim()} style={{ '--ruler-n': options.length } as React.CSSProperties}>
      {options.map((option, index) => (
        <button
          key={option.value}
          ref={element => { roving.refs.current[index] = element; }}
          type="button"
          role="radio"
          aria-checked={index === current}
          aria-label={option.name}
          tabIndex={roving.tabIndexOf(index)}
          className="ui-ruler-item"
          onKeyDown={event => roving.onKeyDown(event, index)}
          onClick={() => onChange(option.value)}
        >
          <span>{option.label}</span>
          {option.marked ? <i className="ui-ruler-dot" aria-hidden="true" /> : null}
        </button>
      ))}
    </div>
  );
}

