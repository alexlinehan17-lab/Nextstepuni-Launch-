import React, { useRef, useState } from 'react';
import { Search } from 'lucide-react';
import { SCHOOLS, getSchoolName, type SchoolId } from '../schoolData';
import { SCHOOL_IDENTITY } from '../data/schoolIdentity';
import SchoolCrest from './SchoolCrest';
import { Combobox, ComboboxTrigger, ComboboxValue, ComboboxContent, ComboboxInput, ComboboxEmpty, ComboboxList, ComboboxItem } from './account-ui-runtime';
import './account-ui-runtime.css';
import './account-controls.css';

const schoolIds = SCHOOLS.map(school => school.id);
export default function AccountSchoolPicker({ id, value, onChange, disabled = false }: {
  id: string; value: string; onChange: (value: string) => void; disabled?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const trigger = useRef<HTMLButtonElement>(null);
  return <div className="nsu-kobra account-school-field">
    <Combobox items={schoolIds} value={value || null} open={open} onOpenChange={setOpen} disabled={disabled}
      itemToStringLabel={school => `${getSchoolName(school)} ${SCHOOL_IDENTITY[school as SchoolId]?.fullName ?? ''}`}
      onValueChange={value => onChange(value || '')}>
      <ComboboxTrigger id={id} ref={trigger} className="account-school-trigger" data-account-sound="tap">
        <SchoolCrest school={value as SchoolId} />
        <span><small>{value ? 'Your school' : 'Find your school'}</small><ComboboxValue>{() => value ? getSchoolName(value) : 'Choose a school'}</ComboboxValue></span>
      </ComboboxTrigger>
      <ComboboxContent anchor={trigger} sideOffset={9} className="account-school-popup">
        <div className="account-school-search"><Search size={18} aria-hidden="true" /><ComboboxInput showTrigger={false} placeholder="Search schools…" aria-label="Search schools" autoComplete="off" /></div>
        <ComboboxEmpty>No schools found. Try another name.</ComboboxEmpty>
        <ComboboxList>{(school: SchoolId) => <ComboboxItem key={school} value={school} data-account-sound="tap">
          <SchoolCrest school={school} /><span><span>{getSchoolName(school)}</span>{SCHOOL_IDENTITY[school].fullName !== getSchoolName(school) && <small>{SCHOOL_IDENTITY[school].fullName}</small>}</span>
        </ComboboxItem>}</ComboboxList>
        <div className="account-school-hint"><span>↑ ↓ to explore</span><span>↵ to choose</span></div>
      </ComboboxContent>
    </Combobox>
  </div>;
}
