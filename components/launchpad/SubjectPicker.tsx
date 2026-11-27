import React, { useMemo, useState } from 'react';
import { ChevronDown, ArrowRight, LockKeyhole } from 'lucide-react';
import ModalFrame from '../ui/ModalFrame';
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
      <ModalFrame
        open={open}
        onClose={() => setOpen(false)}
        title={label}
        labelledBy="subject-picker-title"
      >
        <div>
          <label className="sr-only" htmlFor="subject-picker-search">
            Search subjects
          </label>
          <input
            id="subject-picker-search"
            type="search"
            className="lp-search"
            placeholder="Search subjects"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div className="mt-4 space-y-2">
            {filtered.map((option) => (
              <LockedButton
                key={option.value}
                type="button"
                className="lp-choice"
                aria-pressed={option.value === value}
                locked={!canSelectSubject(option.label)}
                aria-label={!canSelectSubject(option.label) ? `${option.label} — available in the app` : undefined}
                onClick={() => {
                  if (!canSelectSubject(option.label)) return;
                  onChange(option.value);
                  setOpen(false);
                }}
              >
                <span className="flex-1">
                  <strong>{option.label}</strong>
                  {option.detail && <small>{option.detail}</small>}
                </span>
                {canSelectSubject(option.label) ? <ArrowRight size={17} /> : <LockKeyhole size={17} aria-hidden="true" className="shrink-0" />}
              </LockedButton>
            ))}
          </div>
          {options.some(option => !canSelectSubject(option.label)) && <p className="lp-body mt-4">More subjects are available in the app.</p>}
          {!filtered.length && (
            <p className="lp-body py-6">
              No matching subjects. Try a shorter name.
            </p>
          )}
        </div>
      </ModalFrame>
    </>
  );
}
