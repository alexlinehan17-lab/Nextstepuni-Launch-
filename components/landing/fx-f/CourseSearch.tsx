/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Type a course" — a combobox over Points Passport's list. The field is
 * the combobox; the rows under it are the listbox (in flow, so the frame
 * grows with them and nothing is clipped). Arrow keys move, Enter chooses,
 * Escape closes then clears; an empty field offers a few rows to try. The
 * hint line is a polite status: the count of matches, or that there are none.
 */

import React, { useCallback, useEffect, useId, useMemo, useRef, useState } from 'react';
import { COPY } from '../copy';
import { COURSE_COUNT, SAMPLE, searchCourses, type CAOCourse } from './courses';

const T = COPY.futurefinder;

/** A row's short meta: the college and its points, or its level where it has none. */
const meta = (c: CAOCourse): string => `${c.institution} · ${c.typicalPoints > 0 ? `${c.typicalPoints} ${T.points}` : `${T.level} ${c.level}`}`;

const Row: React.FC<{ course: CAOCourse }> = ({ course }) => (
  <>
    <span className="fxf-option-code">{course.code}</span>
    <span className="fxf-option-title">{course.title}</span>
    <span className="fxf-option-meta">{meta(course)}</span>
  </>
);

export const CourseSearch: React.FC<{
  /** The course the chapter is showing, if any: it fills the field so the reader can see what they picked. */
  course: CAOCourse | null;
  onChoose: (course: CAOCourse) => void;
  inputRef: React.RefObject<HTMLInputElement | null>;
}> = ({ course, onChoose, inputRef }) => {
  const id = useId();
  const listId = `${id}-list`;
  const hintId = `${id}-hint`;
  const optionId = (i: number) => `${id}-o${i}`;
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const typed = useRef(false);

  // The chosen course's title fills the field; typing replaces it.
  useEffect(() => { setQuery(course ? course.title : ''); typed.current = false; }, [course]);

  const results = useMemo(() => (typed.current && query.trim() ? searchCourses(query) : null), [query]);
  const options: CAOCourse[] = results ?? (query.trim() ? [] : SAMPLE);
  const sampling = results === null && !query.trim();
  const expanded = open && options.length > 0;
  const none = results !== null && results.length === 0;
  // With nothing typed and no course chosen, the rows to try are plain buttons; on focus they become the listbox.
  const invite = !expanded && sampling && !course;

  useEffect(() => { setActive(0); }, [query]);

  const choose = useCallback((c: CAOCourse) => {
    setOpen(false);
    onChoose(c);
  }, [onChoose]);

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const n = options.length;
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!open) setOpen(true); else if (n) setActive(a => (a + 1) % n);
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (!open) setOpen(true); else if (n) setActive(a => (a - 1 + n) % n);
        break;
      case 'Enter':
        if (expanded) { e.preventDefault(); choose(options[active]); }
        break;
      case 'Escape':
        if (open) { e.preventDefault(); setOpen(false); }
        else if (query) { e.preventDefault(); typed.current = true; setQuery(''); }
        break;
      case 'Tab':
        setOpen(false);
        break;
    }
  };

  const hint = none
    ? T.none
    : results !== null
      ? T.matches.replace('{n}', String(results.length))
      : T.hint.replace('{n}', String(COURSE_COUNT));

  return (
    <div className="fxf-search">
      <label htmlFor={id} className="fxf-label">{T.label}</label>
      <input
        ref={inputRef}
        id={id}
        className="fxf-field"
        type="text"
        role="combobox"
        aria-autocomplete="list"
        aria-expanded={expanded}
        aria-controls={listId}
        aria-activedescendant={expanded ? optionId(active) : undefined}
        aria-describedby={hintId}
        autoComplete="off"
        autoCorrect="off"
        autoCapitalize="off"
        spellCheck={false}
        placeholder={T.placeholder}
        value={query}
        onChange={e => { typed.current = true; setQuery(e.target.value); setOpen(true); }}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
        onKeyDown={onKeyDown}
      />
      <p id={hintId} className="fxf-hint" role="status" aria-live="polite">{hint}</p>
      {(expanded && sampling) || invite ? <p className="fxf-list-head" aria-hidden={expanded || undefined}>{T.sample}</p> : null}
      <ul id={listId} role="listbox" aria-label={T.label} className="fxf-list" hidden={!expanded}>
        {expanded && options.map((c, i) => (
          <li
            key={c.code}
            id={optionId(i)}
            role="option"
            aria-selected={i === active}
            className="fxf-option"
            onMouseDown={e => { e.preventDefault(); choose(c); }}
            onMouseMove={() => { if (active !== i) setActive(i); }}
          >
            <Row course={c} />
          </li>
        ))}
      </ul>
      {invite && (
        <ul className="fxf-list" aria-label={T.sample}>
          {SAMPLE.map(c => (
            <li key={c.code}>
              <button type="button" className="fxf-option fxf-option--button" onClick={() => choose(c)}>
                <Row course={c} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CourseSearch;
