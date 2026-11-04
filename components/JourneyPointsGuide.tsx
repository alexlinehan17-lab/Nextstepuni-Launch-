import React from 'react';
import { X } from 'lucide-react';
import { POINTS } from '../journeyPointsConfig';
import { STUDY_SESSION_POINTS } from '../studySessionData';
import './journey-points-guide.css';

const EARNING_RATES = [
  { label: 'Study session', detail: 'Every 10 minutes', amount: String(STUDY_SESSION_POINTS.PER_10_MINUTES), unit: 'JP', featured: true },
  { label: 'Module section', detail: 'Each section completed', amount: String(POINTS.SECTION_COMPLETE), unit: 'JP' },
  { label: 'Finish a module', detail: 'Completion bonus', amount: `+${POINTS.MODULE_COMPLETE_BONUS}`, unit: 'JP' },
  { label: 'Quests & challenges', detail: 'Reward shown on each activity', amount: 'Varies', unit: '' },
];

/** The same current earning rates in the study primer and Launchpad reference. */
const JourneyPointsGuide: React.FC<{ titleId: string; onClose: () => void; closeLabel?: string }> = ({ titleId, onClose, closeLabel = 'Close' }) => (
  <>
    <header className="jp-guide-header">
      <div>
        <p className="jp-guide-eyebrow">Journey Points</p>
        <h2 id={titleId}>Your study, in points.</h2>
        <p className="jp-guide-intro">Earn JP as you study. Use them to build an island of your own.</p>
      </div>
      <button className="jp-guide-close" type="button" onClick={onClose} aria-label={closeLabel}>
        <X size={20} aria-hidden="true" />
      </button>
    </header>
    <div className="jp-guide-body" data-lenis-prevent>
      <section aria-label="Earn Journey Points">
        <h3 className="jp-guide-eyebrow">How you earn them</h3>
        <dl className="jp-guide-rates">
          {EARNING_RATES.map(rate => (
            <div className="jp-guide-rate" data-featured={rate.featured || undefined} key={rate.label}>
              <dt>{rate.label}<span>{rate.detail}</span></dt>
              <dd className={rate.unit ? undefined : 'jp-guide-variable'}>{rate.amount}{rate.unit && <span>{rate.unit}</span>}</dd>
            </div>
          ))}
        </dl>
      </section>
      <section className="jp-guide-spend" aria-label="Spend Journey Points">
        <h3 className="jp-guide-eyebrow">Make them yours</h3>
        <p className="jp-guide-shop-title">Build your island.</p>
        <p>Choose terrain and objects in the Island shop. Each item shows its price in JP.</p>
      </section>
    </div>
  </>
);

export default JourneyPointsGuide;
