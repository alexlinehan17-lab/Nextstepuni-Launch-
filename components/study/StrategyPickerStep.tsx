/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The first step after a session: which strategies helped. A Kobra paper card
 * (approved review, 25 Oct 2026): Checkbox rows grouped by category, the
 * auto-tracked ones checked and locked, and the session in a hairline strip of
 * serif numerals. Styles: study-post-session.css.
 */

import React, { useState, type CSSProperties } from 'react';
import KobraScope, { Button, Checkbox } from '../approved-ui-runtime';
import { STRATEGY_REGISTRY } from '../../utils/strategyRegistry';
import { getSubjectFill } from '../../utils/subjectColors';
import './study-post-session.css';

// ── Strategy categories ─────────────────────────────────────

const CATEGORIES: { label: string; ids: string[] }[] = [
  {
    label: 'Recall and retention',
    ids: [
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'mastering-interleaving-protocol',
      'elaborative-interrogation-protocol',
    ],
  },
  {
    label: 'Mindset and focus',
    ids: [
      'agency-protocol',
      'growth-mindset-protocol',
      'digital-distraction-protocol',
      'learning-radar-protocol',
    ],
  },
  {
    label: 'Exam prep',
    ids: ['exam-hall-strategies-protocol'],
  },
];

const strategyMap = Object.fromEntries(STRATEGY_REGISTRY.map(s => [s.moduleId, s]));

// ── Component ───────────────────────────────────────────────

interface StrategyPickerStepProps {
  learnedStrategyIds: string[];
  autoTrackedIds: string[];
  onContinue: (selectedIds: string[]) => void;
  onSkip?: () => void;
  subject?: string;
  durationSeconds?: number;
  pointsEarned?: number;
}

const StrategyPickerStep: React.FC<StrategyPickerStepProps> = ({
  learnedStrategyIds: _learnedStrategyIds,
  autoTrackedIds,
  onContinue,
  onSkip,
  subject,
  durationSeconds = 0,
  pointsEarned = 0,
}) => {
  const autoSet = new Set(autoTrackedIds);
  const [selected, setSelected] = useState<Set<string>>(new Set(autoTrackedIds));

  const toggle = (moduleId: string) => {
    if (autoSet.has(moduleId)) return;
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(moduleId)) next.delete(moduleId);
      else next.add(moduleId);
      return next;
    });
  };

  const count = selected.size;
  const durationMin = Math.round(durationSeconds / 60);

  return (
    <KobraScope className="nsu-post-session">
      <div className="sps-page sps-solo">
        <section className="sps-card sps-strategies nsu-paper-card" aria-labelledby="study-strategies-title">
          {subject && (
            <header className="sps-head">
              <span className="sps-subject" style={{ '--sps-subject': getSubjectFill(subject) } as CSSProperties}>
                <span className="sps-subject-dot" aria-hidden="true" />
                {subject}
              </span>
            </header>
          )}
          <p className="sps-kicker">Before your results</p>
          <h2 id="study-strategies-title" className="sps-title">What helped you focus?</h2>
          <p className="sps-lede">Select the strategies you used.</p>

          <dl className="sps-stats">
            <div><dt>Duration</dt><dd>{durationMin}m</dd></div>
            <div><dt>Tracked</dt><dd>{autoTrackedIds.length}</dd></div>
            <div><dt>JP earned</dt><dd className="sps-accent">+{pointsEarned}</dd></div>
          </dl>

          {CATEGORIES.map(cat => (
            <fieldset key={cat.label} className="sps-group">
              <legend className="sps-group-label">{cat.label}</legend>
              <div className="sps-choices">
                {cat.ids.map(id => {
                  const strategy = strategyMap[id];
                  if (!strategy) return null;
                  const isSelected = selected.has(id);
                  const isAuto = autoSet.has(id);
                  return (
                    <label key={id} className="sps-choice" data-checked={isSelected || undefined} data-locked={isAuto || undefined}>
                      <Checkbox checked={isSelected} disabled={isAuto} onCheckedChange={() => toggle(id)} />
                      <span className="sps-choice-label">{strategy.strategyName}</span>
                      {isAuto && <span className="sps-tracked">Tracked</span>}
                    </label>
                  );
                })}
              </div>
            </fieldset>
          ))}

          <div className="sps-actions">
            <Button className="sps-primary" disabled={count === 0} onClick={() => onContinue([...selected])}>
              {count > 0
                ? `Continue with ${count} ${count === 1 ? 'strategy' : 'strategies'}`
                : 'Select strategies to continue'}
            </Button>
            {count > 0 && <p className="sps-bonus"><em>+5</em> bonus JP for reflecting</p>}
            <Button variant="ghost" className="sps-quiet" onClick={() => onSkip ? onSkip() : onContinue([])}>
              Skip this step
            </Button>
          </div>
        </section>
      </div>
    </KobraScope>
  );
};

export default StrategyPickerStep;
