/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The field (components.md, "Fields"; the kit's .field). 48px, radius 9, a
 * 1px line, white, 16px text so iOS never zooms. The label sits above it,
 * 8px away; help or an error sits below. Focus is the approved quiet edge
 * (design/quiet-focus.css): the border turns to the focus ink with a 1px line
 * inside it, nothing moves, nothing turns orange. An error is a plain ink
 * sentence that says what is wrong and what to do.
 *
 *   <Field label="First name" autoComplete="given-name" help="This is the name we greet you with." />
 *   <Field label="School code" error="That code is not one we know. Check it with your teacher." />
 *   <SearchField label="Search topics" placeholder="Search topics" />
 *
 * Set `autoComplete`, `inputMode` and `enterKeyHint` for every use.
 * Migration: FormControls (TextField, SelectField, FieldShell) and the Kobra
 * Input keep today's look; forms move onto this part screen by screen.
 */
import React, { useId, type InputHTMLAttributes, type ReactNode, type TextareaHTMLAttributes } from 'react';
import { Search } from 'lucide-react';
import './parts.css';

export interface FieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** The label above the field. Left out only where the screen shows none of its own (a
   *  module's field under its own heading); then give the field an accessible name. */
  label?: ReactNode;
  /** A line under the field that helps. */
  help?: ReactNode;
  /** What is wrong and what to do; marks the field invalid. */
  error?: ReactNode;
  /** A control at the trailing edge inside the field (an IconButton: a password's Show / Hide). */
  end?: ReactNode;
}

export const Field = React.forwardRef<HTMLInputElement, FieldProps>(function Field(
  { label, help, error, end, id, className = '', type = 'text', ...props },
  ref,
) {
  const ownId = useId();
  const inputId = id ?? ownId;
  const noteId = `${inputId}-note`;
  return (
    <div className={`ui-part ui-field ${className}`.trim()}>
      {label ? <label className="ui-field-label" htmlFor={inputId}>{label}</label> : null}
      {(() => {
        const input = (
          <input
            {...props}
            ref={ref}
            id={inputId}
            type={type}
            className="ui-field-input"
            aria-invalid={error ? true : undefined}
            aria-describedby={error || help ? noteId : undefined}
          />
        );
        return end ? <span className="ui-field-wrap">{input}<span className="ui-field-end">{end}</span></span> : input;
      })()}
      {error ? <p id={noteId} className="ui-field-error" role="alert">{error}</p>
        : help ? <p id={noteId} className="ui-field-help">{help}</p> : null}
    </div>
  );
});

export interface AreaFieldProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** The label above the field, if the screen shows one (a module's own words). */
  label?: ReactNode;
  /** A line under the field that helps (for example "Saved as you type.", only where it is true). */
  help?: ReactNode;
}

/** A field for a written answer: the same white field with a line, several lines tall,
 *  17px words on 26 (board c-read-write). In use it takes the quiet ink edge, like
 *  every field (design/quiet-focus.css). */
export const AreaField = React.forwardRef<HTMLTextAreaElement, AreaFieldProps>(function AreaField(
  { label, help, id, className = '', ...props },
  ref,
) {
  const ownId = useId();
  const areaId = id ?? ownId;
  const noteId = `${areaId}-note`;
  return (
    <div className={`ui-part ui-field ${className}`.trim()}>
      {label ? <label className="ui-field-label" htmlFor={areaId}>{label}</label> : null}
      <textarea {...props} ref={ref} id={areaId} className="ui-field-input ui-field-input--area" aria-describedby={help ? noteId : props['aria-describedby']} />
      {help ? <p id={noteId} className="ui-field-help">{help}</p> : null}
    </div>
  );
});

export interface SearchFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size' | 'type'> {
  /** The field's name for screen readers (the placeholder is not a label). */
  label: string;
}

/** A white field with a line like any other, 44 tall, a search glyph at the front. Never a grey well. */
export const SearchField = React.forwardRef<HTMLInputElement, SearchFieldProps>(function SearchField(
  { label, className = '', enterKeyHint = 'search', ...props },
  ref,
) {
  return (
    <div className={`ui-part ui-field ui-field--search ${className}`.trim()}>
      <span className="ui-field-wrap">
        <Search className="ui-icon ui-field-glyph" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
        <input {...props} ref={ref} type="search" aria-label={label} enterKeyHint={enterKeyHint} className="ui-field-input" />
      </span>
    </div>
  );
});
