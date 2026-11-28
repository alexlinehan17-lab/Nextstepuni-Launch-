import React, { useMemo, useState } from 'react';
import { ChevronDown, LockKeyhole } from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { SearchField } from '../ui/Field';
import LockedButton from '../ui/LockedButton';
import { TextButton } from '../ui/Button';
import { useSubjectAccess } from './SubjectAccess';
import './launchpad.css';

interface Option {
  value: string;
  label: string;
  detail?: string;
}
export default function SubjectPicker({
  value,
  options,
  onChange,
  label = 'Choose a subject',
  art,
  link = false,
}: {
  value: string;
  options: Option[];
  onChange: (value: string) => void;
  label?: string;
  /** The chosen subject's character, bare, at the left of the button (Topic Atlas). */
  art?: React.ReactNode;
  /** The trigger is a text link with the label's words ("All subjects" beside a screen's own
   *  subject choices: Command-Word Reflex, board c-tools2-command). Default: today's button. */
  link?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const canSelectSubject = useSubjectAccess();
  const selected = options.find((option) => option.value === value);
  const filtered = useMemo(
    () =>
      options.filter((option) =>
        option.label
          .toLocaleLowerCase()
          .includes(query.toLocaleLowerCase().trim()),
      ),
    [options, query],
  );
  return (
    <>
      {link ? (
        <TextButton aria-expanded={open} onClick={() => { setQuery(''); setOpen(true); }}>{label}</TextButton>
      ) : <button
        type="button"
        className="lp-button secondary w-full"
        aria-label={label}
        aria-haspopup="dialog"
        aria-expanded={open}
        onClick={() => {
          setQuery('');
          setOpen(true);
        }}
      >
        {art ? <span className="lp-subject-art" aria-hidden="true">{art}</span> : null}
        <span>{selected?.label ?? label}</span>
        <ChevronDown size={16} className="shrink-0" />
      </button>}
      {/* The shared sheet (area 7b): Close at the top left, the system's title, the shared search field,
          the subjects as rows; the chosen one keeps the ink outline. Words, order, locks and picking unchanged. */}
      <Sheet open={open} onClose={() => setOpen(false)} title={label} className="lp-subject-sheet">
        <div className="lp-subject-sheet-body">
          <SearchField
            label="Search subjects"
            placeholder="Search subjects"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <ul className="ui-part ui-list lp-subject-list">
            {filtered.map((option) => {
              const available = canSelectSubject(option.label);
              return (
                <li className="ui-row-item" key={option.value}>
                  <LockedButton
                    type="button"
                    className="ui-part ui-row ui-row--select lp-subject-row"
                    aria-pressed={option.value === value}
                    locked={!available}
                    aria-label={!available ? `${option.label} — available in the app` : undefined}
                    onClick={() => {
                      if (!available) return;
                      onChange(option.value);
                      setOpen(false);
                    }}
                  >
                    <span className="ui-row-body">
                      <span className="ui-row-title">{option.label}</span>
                      {option.detail && <span className="ui-row-meta">{option.detail}</span>}
                    </span>
                    {available ? null : <LockKeyhole size={20} strokeWidth={1.75} aria-hidden="true" className="ui-icon ui-row-chev" />}
                  </LockedButton>
                </li>
              );
            })}
          </ul>
          {options.some(option => !canSelectSubject(option.label)) && <p className="t-meta">More subjects are available in the app.</p>}
          {!filtered.length && (
            <p className="t-sub lp-subject-empty">
              No matching subjects. Try a shorter name.
            </p>
          )}
        </div>
      </Sheet>
    </>
  );
}
