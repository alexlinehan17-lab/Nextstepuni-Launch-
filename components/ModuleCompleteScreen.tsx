import React, { useRef } from 'react';
import { useReducedMotion } from 'framer-motion';
import { Stamp } from 'lucide-react';
import './student-screens.css';
import { useModal } from '../hooks/useModal';
import { FramePortal } from './ui/Frame';
import { TopBar, PinnedFooter } from './ui/Bars';
import { Button, TextButton, Arrow } from './ui/Button';
import { PaperSheet, PressBox } from './ui/List';
import { Readout, worldOf } from './moduleWorlds';
import type { ModuleFinish } from './learning/readerContext';
import { moduleReadingTime } from '../utils/moduleDiscovery';

/**
 * Finishing a module (area 5 of the design build; board c-read-flow, "Finishing a module").
 * Starguy steps in once and the ticks of what you read draw in, one after another. Start a study
 * session stays the main action, charcoal; the next module in the world is one tap away; Close is
 * the way out. Reduced motion: everything is simply there.
 */
interface ModuleCompleteScreenProps {
  isOpen: boolean;
  moduleTitle: string;
  moduleSubtitle?: string;
  categoryColor: string;
  modulesCompleted?: number;
  totalModules?: number;
  sectionsCount: number;
  northStarStatement?: string;
  onContinue: () => void;
  onReview?: () => void;
  onPractice?: () => void;
  /** The steps read, in order (their titles). */
  sections?: { title: string }[];
  /** The module's world and its next module (the app provides it). */
  finish?: ModuleFinish | null;
}

const pad = (n: number) => String(n).padStart(2, '0');

const ModuleCompleteScreen: React.FC<ModuleCompleteScreenProps> = ({
  isOpen, moduleTitle, modulesCompleted, totalModules,
  sectionsCount, northStarStatement, onContinue, onReview, onPractice, sections, finish,
}) => {
  const reduceMotion = useReducedMotion();
  const panel = useRef<HTMLDivElement>(null);
  useModal(isOpen, onContinue, panel);
  if (!isOpen) return null;
  const steps = sections?.length ? sections : Array.from({ length: sectionsCount }, (_, i) => ({ title: `Section ${i + 1}` }));
  return (
    <FramePortal>
      <div ref={panel} className={`rd-finish frame-takeover${reduceMotion ? '' : ' rd-finish--play'}`} role="dialog" aria-modal="true" aria-labelledby="module-complete-title">
        <TopBar leave={{ kind: 'close', onPress: onContinue, label: 'Back to the programme' }} />
        <main className="rd-finish-page">
          <div className="rd-finish-head">
            <div className="rd-finish-row">
              <div className="rd-finish-copy">
                <p className="t-label rd-finish-label">One chapter further</p>
                <h1 id="module-complete-title" className="t-display">Something to take with you.</h1>
              </div>
              <img className="rd-finish-crew" src="/assets/landing/starguy-512.png" alt="" />
            </div>
            <p className="t-sub">You’ve finished reading {moduleTitle}.</p>
          </div>
          <section className="rd-finish-sec">
            <PaperSheet className="rd-receipt" label="What you read">
              <div className="rd-receipt-head"><p className="t-label">What you read</p><Readout className="mw-ink3">{steps.length} / {sectionsCount}</Readout></div>
              <ol className="rd-receipt-list">
                {steps.map((step, i) => (
                  <li key={`${i}-${step.title}`}>
                    <span className="rd-dtick" style={{ ['--i' as string]: i }} aria-hidden="true"><svg viewBox="0 0 12 12" focusable="false"><path d="M2.5 6.2l2.4 2.4 4.6-5" /></svg></span>
                    <Readout className="mw-ink3">{pad(i + 1)}</Readout>
                    <span>{step.title}</span>
                  </li>
                ))}
              </ol>
              <p className="rd-receipt-foot">
                <Stamp className="ui-icon" width={18} height={18} strokeWidth={1.75} aria-hidden="true" focusable="false" />
                <span>Reading recorded in your Study Passport. Practice is recorded when you try it yourself.</span>
              </p>
            </PaperSheet>
          </section>
          {modulesCompleted !== undefined && totalModules !== undefined ? <p className="t-meta rd-finish-extra">{modulesCompleted} of {totalModules} modules complete</p> : null}
          {northStarStatement ? <p className="t-meta rd-finish-extra">Your North Star: “{northStarStatement}”</p> : null}
          {finish?.next ? (
            <section className="rd-finish-sec" aria-labelledby="rd-finish-next">
              <div className="mw-sec-head"><h2 id="rd-finish-next" className="t-heading">Up next in {worldOf(finish.category)?.name ?? 'this world'}</h2><Readout className="mw-ink3">{finish.done} of {finish.total} done</Readout></div>
              <PressBox className="mw-mod" onPress={() => finish.openModule(finish.next!.course.id)}>
                <span className="mw-mod-in">
                  <Readout className="mw-mod-no">{pad(finish.next.number)}</Readout>{' '}
                  <span className="mw-mod-copy"><span className="mw-mod-title">{finish.next.course.title}</span>{' '}<span className="t-meta">{moduleReadingTime(finish.next.course)}</span></span>
                  <Arrow meaning="opens" size={20} className="mw-chev" />
                </span>
              </PressBox>
            </section>
          ) : null}
          {onReview ? <div className="rd-finish-review"><TextButton tone="quiet" onClick={onReview}>Review module</TextButton></div> : null}
        </main>
        {onPractice ? (
          <PinnedFooter ruled>
            <Button kind="main" size="lg" block arrow="forward" autoFocus onClick={onPractice}>Start a study session</Button>
          </PinnedFooter>
        ) : null}
      </div>
    </FramePortal>
  );
};
export default ModuleCompleteScreen;
