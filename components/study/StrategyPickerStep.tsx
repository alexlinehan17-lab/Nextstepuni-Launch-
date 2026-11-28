/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The first step after a session: which strategies helped (r5-post-session,
 * agreed 26 Nov 2026). On the page, not in a card: the subject with its
 * character, the three figures in a line, pick-several tiles with a square mark
 * (the auto-tracked ones checked and locked), and Continue pinned at the bottom
 * saying what it needs. A task: the tab bar steps aside.
 */

import React, { useEffect, useRef, useState } from 'react';
import KobraScope from '../approved-ui-runtime';
import { STRATEGY_REGISTRY } from '../../utils/strategyRegistry';
import SubjectAvatar from '../SubjectAvatar';
import { PinnedFooter, TopBar } from '../ui/Bars';
import { Button, TextButton } from '../ui/Button';
import { ChoiceTile } from '../ui/Choice';
import { useFrameTask } from '../ui/Frame';
import './study-post-session.css';
import './study-after.css';

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

const ALL_IDS = CATEGORIES.flatMap(category => category.ids).filter(id => strategyMap[id]);

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
  const firstGroup = useRef<HTMLDivElement>(null);
  // A task: the tab bar steps aside; and it opens at the top, on its headline.
  useFrameTask(true);
  useEffect(() => { try { window.scrollTo({ top: 0 }); } catch { /* no window to scroll */ } }, []);

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
      <div className="sps-page sps-flow">
        <TopBar className="sps-bar" placeLabel="Before your results" />
        <section className="sps-step" aria-labelledby="study-strategies-title">
          {subject && <p className="sps-subject-line"><SubjectAvatar subject={subject} bare /><span className="t-row">{subject}</span></p>}
          <h1 id="study-strategies-title" className="t-display">What helped you focus?</h1>
          <p className="t-sub">Select the strategies you used.</p>

          <dl className="sps-figures">
            <div><dt>Duration</dt><dd>{durationMin}<small>m</small></dd></div>
            <div><dt>Tracked</dt><dd>{autoTrackedIds.length}</dd></div>
            <div><dt>JP earned</dt><dd>+{pointsEarned}</dd></div>
          </dl>

          {CATEGORIES.map((cat, index) => (
            <div key={cat.label} ref={index === 0 ? firstGroup : undefined} role="group" aria-labelledby={`sps-group-${index}`} className="sps-group-flow">
              <p id={`sps-group-${index}`} className="t-label">{cat.label}</p>
              <div className="sps-tiles">
                {cat.ids.map(id => {
                  const strategy = strategyMap[id];
                  if (!strategy) return null;
                  const isAuto = autoSet.has(id);
                  return (
                    <ChoiceTile key={id} kind="several" chosen={selected.has(id)} label={strategy.strategyName}
                      meta={isAuto ? 'Tracked' : undefined} aria-disabled={isAuto || undefined} onClick={() => toggle(id)} />
                  );
                })}
              </div>
            </div>
          ))}
        </section>
        <PinnedFooter ruled className="sps-foot">
          {count > 0 && <p className="sps-ready">{count} of {ALL_IDS.length} chosen · +5 bonus JP for reflecting</p>}
          <Button kind="main" size="lg" block arrow="forward" className="sps-main"
            missing={count === 0 ? { sentence: 'Select strategies to continue.', goTo: firstGroup } : undefined}
            onClick={() => onContinue([...selected])}>
            {count > 0 ? `Continue with ${count} ${count === 1 ? 'strategy' : 'strategies'}` : 'Continue'}
          </Button>
          <TextButton tone="quiet" className="sps-quiet" onClick={() => onSkip ? onSkip() : onContinue([])}>Skip this step</TextButton>
        </PinnedFooter>
      </div>
    </KobraScope>
  );
};

export default StrategyPickerStep;
