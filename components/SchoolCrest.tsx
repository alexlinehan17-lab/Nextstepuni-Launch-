import React, { useState } from 'react';
import { GraduationCap } from 'lucide-react';
import { SCHOOL_IDENTITY } from '../data/schoolIdentity';
import type { SchoolId } from '../schoolData';

export default function SchoolCrest({ school }: { school?: SchoolId | '' }) {
  const [failed, setFailed] = useState<string>();
  const identity = school ? SCHOOL_IDENTITY[school] : undefined;
  return <span className={`account-school-crest account-school-crest--${school || 'empty'}`} aria-hidden="true">
    {identity && failed !== school ? <img src={`/assets/schools/${identity.crest}`} alt="" onError={() => setFailed(school)} /> : <GraduationCap size={23} />}
  </span>;
}
