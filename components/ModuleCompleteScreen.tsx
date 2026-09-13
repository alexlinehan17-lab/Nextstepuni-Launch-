import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, Check } from 'lucide-react';
import './student-screens.css';
import { useModal } from '../hooks/useModal';

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
}

const ModuleCompleteScreen: React.FC<ModuleCompleteScreenProps> = ({
  isOpen, moduleTitle, moduleSubtitle, modulesCompleted, totalModules,
  sectionsCount, northStarStatement, onContinue, onReview, onPractice,
}) => {
  const reduceMotion = useReducedMotion();
  useModal(isOpen, onContinue);
  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: reduceMotion ? 0 : 0.2 }} className="fixed inset-0 z-[300] overflow-y-auto bg-white text-zinc-900 dark:bg-zinc-950 dark:text-white" role="dialog" aria-modal="true" aria-labelledby="module-complete-title">
          <div className="module-completion">
            <img className="completion-character" src="/assets/landing/starguy-512.png" alt="" />
            <p className="student-eyebrow">One chapter further</p>
            <h1 id="module-complete-title">Something to<br /><em>take with you.</em></h1>
            <p className="completion-module">You’ve finished {moduleTitle}.</p>
            {moduleSubtitle && <p className="completion-subtitle">{moduleSubtitle}</p>}
            <div className="completion-record"><Check size={19} aria-hidden="true" /><span>{sectionsCount} sections complete</span><span>Added to your Study Passport</span></div>
            {modulesCompleted !== undefined && totalModules !== undefined && <p className="completion-subtitle">{modulesCompleted} of {totalModules} modules complete</p>}
            {northStarStatement && <p className="completion-north-star">Your North Star: “{northStarStatement}”</p>}
            {onPractice && <button type="button" autoFocus className="student-primary" onClick={onPractice}>Put it into practice <ArrowRight size={20} aria-hidden="true" /></button>}
            <button type="button" autoFocus={!onPractice} onClick={onContinue} className={onPractice ? 'student-text-action' : 'student-primary'}>Back to the programme <ArrowRight size={18} aria-hidden="true" /></button>
            {onReview && <button type="button" onClick={onReview} className="student-text-action">Review module</button>}
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>, document.body,
  );
};
export default ModuleCompleteScreen;
