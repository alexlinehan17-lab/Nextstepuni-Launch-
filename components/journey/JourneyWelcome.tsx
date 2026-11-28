import React, { useState } from 'react';
import { HelpCircle } from 'lucide-react';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import { Button, IconButton, TextButton } from '../ui/Button';
import { Sheet } from '../ui/Sheet';
import CrewIllustration from '../CrewIllustration';
import './journey-welcome.css';

/** The island's welcome (c-world.html "c-world-island"; r5-b2.html "r5-island-welcome"):
 *  the shared sheet, rising from the bottom on a phone and a centred window on a laptop,
 *  Close at its top left, the bold headline (Alex, 26 Nov 2026) and a charcoal "Explore my
 *  island" in view without scrolling. "How it works" brings it back.
 *  Mounted only after this student's saved progress has loaded. */
export default function JourneyWelcome({ hasSeenWelcome, onDismissWelcome, trigger = 'icon' }: {
  hasSeenWelcome: boolean;
  onDismissWelcome: () => void;
  /** How it is brought back: the "?" in the phone's top row, or "How it works" at the left end of the laptop's bar. */
  trigger?: 'icon' | 'text';
}) {
  const [open, setOpen] = useState(!hasSeenWelcome);
  const phone = useMobileAppDesign();
  const close = () => {
    setOpen(false);
    if (!hasSeenWelcome) onDismissWelcome();
  };
  const explore = <Button kind="main" size="lg" block arrow="forward" onClick={close}>Explore my island</Button>;
  const headline = <h2 id="journey-welcome-title" className={`jw-title${phone ? ' t-title' : ' t-display'}`}>Your effort.<br />A world of<br />your own.</h2>;

  return <>
    {trigger === 'text'
      ? <TextButton tone="quiet" className="jw-help-text" aria-label="How Journey works" onClick={() => setOpen(true)}><HelpCircle className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />How it works</TextButton>
      : <IconButton label="How Journey works" onClick={() => setOpen(true)} icon={<HelpCircle className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" />} />}
    <Sheet open={open} onClose={close} title="How it works" titleSize="small" closeLabel="Close Journey introduction"
      className={`journey-welcome-sheet${phone ? '' : ' journey-welcome-sheet--wide'}`}
      footer={phone ? <div className="jw-foot"><p className="t-meta">No rush. No upkeep. Your island will be here when you come back.</p>{explore}</div> : undefined}>
      {phone ? (
        <div className="jw-body">
          <p className="t-label jw-label">Welcome to Journey Mode</p>
          <div className="jw-hello">
            <div className="jw-hello-text">
              {headline}
            </div>
            <CrewIllustration character="star-crew:stargazer" className="jw-crew" />
          </div>
          <p id="journey-welcome-description" className="t-sub">A little island that grows with the work you put in. A place to make your progress visible, one small step at a time.</p>
          <ol className="jw-how">
            <li><span className="t-readout">01</span><div><span className="t-row">Study. Earn. Grow.</span><span className="t-meta">Study sessions and lessons earn Journey Points (JP).</span></div></li>
            <li><span className="t-readout">02</span><div><span className="t-row">Build a place that’s yours.</span><span className="t-meta">Choose a tile, tap an open corner, then confirm.</span></div></li>
            <li><span className="t-readout">03</span><div><span className="t-row">See what’s out there.</span><span className="t-meta">Growing your island reveals hidden stories and mythic stickers.</span></div></li>
          </ol>
        </div>
      ) : (
        <div className="jw-cols">
          <div className="jw-left">
            <p className="t-label jw-label">Welcome to Journey Mode</p>
            {headline}
            <p id="journey-welcome-description" className="t-sub">A little island that grows with the work you put in. A place to make your progress visible, one small step at a time.</p>
            <div className="jw-crewline" aria-hidden="true">
              <CrewIllustration character="star-crew:stargazer" className="jw-crew jw-crew--big" />
              <p className="t-sub">Small steps.<br />New horizons.</p>
            </div>
          </div>
          <div className="jw-right">
            <p className="t-label jw-label">Here’s how it works</p>
            <ol className="jw-how jw-how--wide">
              <li><span className="t-readout">01</span><div><span className="t-row">Study. Earn. Grow.</span><span className="t-sub">Complete study sessions and lessons to earn Journey Points (JP). Your balance is at the top of your island.</span></div></li>
              <li><span className="t-readout">02</span><div><span className="t-row">Build a place that’s yours.</span><span className="t-sub">Open <strong>Build</strong>, choose a tile and tap an open corner. Preview it, then confirm to use your points.</span></div></li>
              <li><span className="t-readout">03</span><div><span className="t-row">See what’s out there.</span><span className="t-sub">Growing your island reveals hidden stories and mythic stickers. Collect your discoveries in your <strong>Fieldbook</strong>.</span></div></li>
            </ol>
            <div className="jw-deskfoot">
              <p className="t-sub">No rush. No upkeep.<br />Your island will be here when you come back.</p>
              {explore}
              <p className="t-meta">Revisit this guide any time with “How it works”.</p>
            </div>
          </div>
        </div>
      )}
    </Sheet>
  </>;
}
