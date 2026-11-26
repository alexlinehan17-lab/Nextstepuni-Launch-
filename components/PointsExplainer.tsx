/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { Sheet } from './ui/Sheet';
import { Button } from './ui/Button';
import { EARNING_RATES } from './JourneyPointsGuide';
import './points-explainer.css';

interface PointsExplainerProps {
  isOpen: boolean;
  onDismiss: () => void;
}

/** First-study primer (r5-study-setup, agreed 26 Nov 2026): the same words and
 *  rates on the shared sheet, which rises from the bottom and stops below the
 *  clock; Close at its top left, Got it pinned at its foot. */
const PointsExplainer: React.FC<PointsExplainerProps> = ({ isOpen, onDismiss }) => (
  <Sheet
    open={isOpen}
    onClose={onDismiss}
    title="Journey Points"
    titleSize="small"
    className="jp-sheet"
    footer={<Button kind="main" size="lg" block arrow="forward" onClick={onDismiss}>Got it</Button>}
  >
    <h3 className="t-title">Your study, in points.</h3>
    <p className="t-sub jp-sheet-intro">Earn JP as you study. Use them to build an island of your own.</p>
    <section aria-label="Earn Journey Points">
      <h4 className="t-label jp-sheet-label">How you earn them</h4>
      <dl className="jp-sheet-rates">
        {EARNING_RATES.map(rate => (
          <div key={rate.label}>
            <dt><span className="t-row">{rate.label}</span><span className="t-meta">{rate.detail}</span></dt>
            <dd>
              <span className={rate.unit ? `jp-sheet-amount${rate.featured ? ' jp-sheet-amount--live' : ''}` : 'jp-sheet-varies'}>{rate.amount}</span>
              <span className="jp-sheet-unit">{rate.unit}</span>
            </dd>
          </div>
        ))}
      </dl>
    </section>
    <section aria-label="Spend Journey Points">
      <h4 className="t-label jp-sheet-label">Make them yours</h4>
      <p className="t-heading">Build your island.</p>
      <p className="t-sub jp-sheet-spend">Choose terrain and objects in the Island shop. Each item shows its price in JP.</p>
    </section>
  </Sheet>
);

export default PointsExplainer;
