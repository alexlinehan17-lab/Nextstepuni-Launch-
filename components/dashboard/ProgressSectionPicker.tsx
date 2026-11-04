import React, { useEffect, useId, useRef, useState } from 'react';
import { Check, ChevronDown } from 'lucide-react';
import type { DashboardSection } from '../../contexts/NavigationContext';

export default function ProgressSectionPicker({ value, options, onChange }: {
  value: DashboardSection;
  options: Array<{ id: DashboardSection; label: string }>;
  onChange: (value: DashboardSection) => void;
}) {
  const [open, setOpen] = useState(false);
  const root = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const id = useId();
  const selected = options.findIndex(option => option.id === value);
  useEffect(() => {
    if (!open) return;
    root.current?.querySelector<HTMLButtonElement>('[aria-selected="true"]')?.focus();
    const closeOutside = (event: PointerEvent) => {
      if (!root.current?.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener('pointerdown', closeOutside);
    return () => document.removeEventListener('pointerdown', closeOutside);
  }, [open]);
  const choose = (next: DashboardSection) => {
    onChange(next);
    setOpen(false);
    trigger.current?.focus();
  };
  return <div ref={root} className="dashboard-section-picker" onBlur={event => {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setOpen(false);
  }}>
    <span>Explore your record</span>
    <button ref={trigger} type="button" className="dashboard-section-trigger" aria-label="Progress section"
      aria-haspopup="listbox" aria-expanded={open} aria-controls={id}
      onClick={() => setOpen(current => !current)} onKeyDown={event => {
        if (event.key === 'ArrowDown' || event.key === 'ArrowUp') { event.preventDefault(); setOpen(true); }
      }}>
      <strong>{options[selected]?.label}</strong><small>{selected + 1} / {options.length}</small><ChevronDown size={17} aria-hidden="true" />
    </button>
    {open && <div id={id} role="listbox" aria-label="Progress sections" className="dashboard-section-menu" onKeyDown={event => {
      const buttons = Array.from(event.currentTarget.querySelectorAll<HTMLButtonElement>('[role="option"]'));
      const current = buttons.indexOf(document.activeElement as HTMLButtonElement);
      const next = event.key === 'ArrowDown' ? (current + 1) % buttons.length
        : event.key === 'ArrowUp' ? (current - 1 + buttons.length) % buttons.length
        : event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : null;
      if (next !== null) { event.preventDefault(); buttons[next]?.focus(); }
      if (event.key === 'Escape') { event.preventDefault(); setOpen(false); trigger.current?.focus(); }
    }}>
      {options.map((option, index) => <button key={option.id} type="button" role="option"
        aria-selected={option.id === value} onClick={() => choose(option.id)}>
        <small>0{index + 1}</small><span>{option.label}</span>{option.id === value && <Check size={16} aria-hidden="true" />}
      </button>)}
    </div>}
  </div>;
}
