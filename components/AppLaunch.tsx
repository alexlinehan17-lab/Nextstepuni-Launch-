import React from 'react';
import './account-entry.css';

/** Brand entrance while real account hydration runs; never a timed gate. */
export default function AppLaunch() {
  return <div className="account-launch" role="status" aria-label="Opening NextStepUni"><div><img src="/icons/onboarding/star-person.png" alt="" width={260} height={260} /><span>nextstepuni</span><p>Opening your study space…</p></div></div>;
}
