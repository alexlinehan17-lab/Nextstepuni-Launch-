import React, { useMemo, useState } from 'react';
import { ChevronDown, ArrowRight, LockKeyhole } from 'lucide-react';
import ModalFrame from '../ui/ModalFrame';
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
}: {
  value: string;
  options: Option[];
  onChange: (value: string) => void;
  label?: string;
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
      <button
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
        <span>{selected?.label ?? label}</span>
        <ChevronDown size={16} className="shrink-0" />
      </button>
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
              <button
                key={option.value}
                type="button"
                className="lp-choice"
                aria-pressed={option.value === value}
                disabled={!canSelectSubject(option.label)}
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
              </button>
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
