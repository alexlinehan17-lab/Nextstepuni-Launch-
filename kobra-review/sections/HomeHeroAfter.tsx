/**
 * Home hero, rebuilt on Kobra (AFTER for the design review).
 *
 * The words of components/StudentHomeContent.tsx and dashboard/FieldNotes.tsx:
 * the date, the serif greeting, one primary Kobra Button, and two hairline
 * paper cards ("Your week so far" and "Pick up where you left off"). The week
 * is review sample data that adds up to the before's numbers.
 */

import { useId, type CSSProperties } from 'react';
import { ArrowRight, ArrowUpRight } from 'lucide-react';
import { Button, Progress, ProgressLabel } from '../../components/approved-ui-runtime';
import ThemeArtwork from '../../components/ThemeArtwork';
import { ModulesIcon } from '../../components/sectionIcons';
import './home-hero.css';

/** Sample week: 414 minutes (6h 54m) over 9 sessions on 5 days. */
const WEEK = [
  { label: 'Mon', minutes: 75, sessions: 2 },
  { label: 'Tue', minutes: 48, sessions: 1 },
  { label: 'Wed', minutes: 102, sessions: 2 },
  { label: 'Thu', minutes: 64, sessions: 2 },
  { label: 'Fri', minutes: 125, sessions: 2 },
  { label: 'Sat', minutes: 0, sessions: 0 },
  { label: 'Sun', minutes: 0, sessions: 0 },
];
/** The bars share one scale with headroom, so a full track is not a full day. */
const SCALE_MINUTES = 150;
const TOTAL = WEEK.reduce((sum, day) => sum + day.minutes, 0);
const SESSIONS = WEEK.reduce((sum, day) => sum + day.sessions, 0);
const ACTIVE_DAYS = WEEK.filter(day => day.sessions > 0).length;
const STREAK = 7;
const MODULE = { read: 3, sections: 5 };

function dayDetail(day: (typeof WEEK)[number]) {
  return `${day.label}: ${day.minutes} minutes across ${day.sessions} session${day.sessions === 1 ? '' : 's'}`;
}

export default function HomeHeroAfter() {
  const id = useId();
  const now = new Date();
  const greeting = now.getHours() < 12 ? 'Good morning' : now.getHours() < 18 ? 'Good afternoon' : 'Good evening';
  const hours = Math.floor(TOTAL / 60);
  const minutes = TOTAL % 60;
  const left = MODULE.sections - MODULE.read;

  return (
    <section className="kr-section kr-hh" aria-label="Home hero on Kobra">
      <div className="kr-hh-frame">
        <p className="kr-hh-eyebrow">
          {now.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })}
        </p>

        <div className="kr-hh-hero">
          <div className="kr-hh-greeting">
            <h2>{greeting},<br /><em>Demo.</em></h2>
            <p>Make a little room for what comes next.</p>
            <Button className="kr-hh-primary">
              Start a study session<ArrowUpRight aria-hidden="true" />
            </Button>
          </div>

          <aside className="kr-hh-card kr-hh-week nsu-paper-card" aria-labelledby={`${id}-week`}>
            <p id={`${id}-week`} className="kr-hh-eyebrow">Your week so far</p>
            <div className="kr-hh-week-head">
              <div>
                <h3>Making time.</h3>
                <p className="kr-hh-time" aria-label={`${hours} hours ${minutes} minutes`}>
                  <span>{hours}<small>h</small></span>
                  <span>{minutes}<small>m</small></span>
                </p>
                <p className="kr-hh-detail">{SESSIONS} sessions of focused study.</p>
              </div>
              <ThemeArtwork
                src="/assets/star-crew/companions/thinker.png"
                alt=""
                width={130}
                height={130}
                className="kr-hh-week-art"
              />
            </div>

            <ol className="kr-hh-bars" aria-label="Study days this week">
              {WEEK.map((day, index) => (
                <li key={day.label} aria-label={dayDetail(day)}>
                  <span className="kr-hh-bar-value" aria-hidden="true">{day.minutes ? `${day.minutes}m` : ' '}</span>
                  <span className="kr-hh-bar-track" aria-hidden="true">
                    <span
                      className="kr-hh-bar-fill"
                      style={{ '--kr-hh-fill': `${(day.minutes / SCALE_MINUTES) * 100}%`, '--kr-hh-i': index } as CSSProperties}
                    />
                  </span>
                  <span className="kr-hh-bar-day" aria-hidden="true">{day.label}</span>
                </li>
              ))}
            </ol>

            <div className="kr-hh-facts">
              <span><strong>{ACTIVE_DAYS}</strong> active days</span>
              <span><strong>{STREAK}</strong>-day study streak</span>
            </div>
            <Button variant="outline" className="nsu-ink-outline kr-hh-action kr-hh-progress">
              Your progress<ArrowUpRight aria-hidden="true" />
            </Button>
          </aside>
        </div>

        <section className="kr-hh-card kr-hh-continue nsu-paper-card" aria-labelledby={`${id}-module`}>
          <div className="kr-hh-continue-art" aria-hidden="true"><ModulesIcon /></div>
          <div className="kr-hh-continue-copy">
            <p className="kr-hh-eyebrow">Pick up where you left off</p>
            <p className="kr-hh-world">The Architecture of your Mindset</p>
            <h3 id={`${id}-module`}>Controlling the Controllables</h3>
            <p className="kr-hh-detail">The Attribution Retraining Guide</p>
          </div>
          <div className="kr-hh-continue-actions">
            <Progress
              value={MODULE.read}
              max={MODULE.sections}
              className="kr-hh-reading"
              getAriaValueText={() => `${MODULE.read} of ${MODULE.sections} sections read. ${left} sections to go`}
            >
              <ProgressLabel><strong>{MODULE.read}</strong> of {MODULE.sections} read</ProgressLabel>
              <span className="kr-hh-reading-left" aria-hidden="true">{left} to go</span>
            </Progress>
            <Button variant="outline" className="nsu-ink-outline kr-hh-action">
              Continue learning<ArrowUpRight aria-hidden="true" />
            </Button>
            <Button variant="ghost" className="kr-hh-quiet">
              Browse all five module worlds<ArrowRight aria-hidden="true" />
            </Button>
          </div>
        </section>
      </div>
    </section>
  );
}
