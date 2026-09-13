import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight } from 'lucide-react';
import StarGuide from './ui/StarGuide';
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
}

const ModuleCompleteScreen: React.FC<ModuleCompleteScreenProps> = ({
  isOpen, moduleTitle, moduleSubtitle, modulesCompleted, totalModules,
  sectionsCount, northStarStatement, onContinue, onReview,
}) => {
  const reduceMotion = useReducedMotion();
  useModal(isOpen, onContinue);
  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: reduceMotion ? 0 : 0.2 }} className="fixed inset-0 z-[300] overflow-y-auto bg-white text-zinc-900 dark:bg-zinc-950 dark:text-white" role="dialog" aria-modal="true" aria-labelledby="module-complete-title">
          <div className="min-h-[100dvh] flex flex-col justify-center px-5" style={{ paddingTop: 'max(24px, env(safe-area-inset-top))', paddingBottom: 'max(24px, env(safe-area-inset-bottom))' }}>
            <div className="mx-auto w-full max-w-md">
              <div className="flex items-center justify-between gap-4 border-b border-zinc-200 pb-4 dark:border-zinc-700">
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#B54D14] dark:text-orange-400">Module complete</p>
                <StarGuide size={88} className="shrink-0" />
              </div>
              <h1 id="module-complete-title" className="mt-6 font-serif text-4xl font-bold leading-[1.1] tracking-tight">{moduleTitle}</h1>
              {moduleSubtitle && <p className="mt-3 text-base leading-relaxed text-zinc-600 dark:text-zinc-300">{moduleSubtitle}</p>}
              <dl className="my-6 grid grid-cols-2 divide-x divide-zinc-200 border-y border-zinc-200 py-5 dark:divide-zinc-700 dark:border-zinc-700">
                {modulesCompleted !== undefined && totalModules !== undefined && <div className="pr-4"><dd className="text-3xl font-semibold tabular-nums">{modulesCompleted}<span className="text-lg text-zinc-500"> / {totalModules}</span></dd><dt className="mt-1 text-sm text-zinc-600 dark:text-zinc-300">Modules completed</dt></div>}
                <div className={modulesCompleted !== undefined && totalModules !== undefined ? 'pl-4' : ''}><dd className="text-3xl font-semibold tabular-nums">{sectionsCount}</dd><dt className="mt-1 text-sm text-zinc-600 dark:text-zinc-300">Sections explored</dt></div>
              </dl>
              {northStarStatement && <blockquote className="mb-6"><p className="mb-2 text-xs font-bold uppercase tracking-widest text-zinc-500 dark:text-zinc-400">Your North Star</p><p className="font-serif text-xl leading-relaxed">“{northStarStatement}”</p></blockquote>}
              <button autoFocus onClick={onContinue} className="flex min-h-14 w-full items-center justify-between gap-3 rounded-xl bg-[#F26B1F] px-5 py-4 text-base font-bold text-[#1A1A1A] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#B54D14]">Continue <ArrowRight size={20} aria-hidden="true" /></button>
              {onReview && <button onClick={onReview} className="mt-2 min-h-12 w-full rounded-xl text-base font-semibold underline underline-offset-4">Review module</button>}
            </div>
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>, document.body,
  );
};
export default ModuleCompleteScreen;
