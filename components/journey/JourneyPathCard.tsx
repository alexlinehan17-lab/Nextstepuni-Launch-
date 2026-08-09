import React from 'react';
import { Check, Circle, PackageOpen } from 'lucide-react';
import type { getJourneyProgress } from '../../journeyProgression';

type JourneyProgress = ReturnType<typeof getJourneyProgress>;

interface JourneyPathCardProps {
  progress: JourneyProgress;
  onOpenBuildMode: () => void;
}

const JourneyPathCard: React.FC<JourneyPathCardProps> = ({ progress, onOpenBuildMode }) => (
  <section className="mb-4 overflow-hidden rounded-[20px] border-2 border-[#343230] bg-[#FFFDF8] shadow-[0_5px_0_#343230] dark:bg-[#201F1D] dark:border-[#D8D1C8] dark:shadow-[0_5px_0_#D8D1C8]">
    <div className="px-4 py-4 border-b border-[#E5DED5] dark:border-[#46413C]">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#A0978D]">Your Journey</p>
          <h4 className="mt-1 font-serif text-xl font-semibold text-[#242220] dark:text-[#F7F1E8]">{progress.stage.name}</h4>
          <p className="mt-1 text-xs leading-relaxed text-[#756F69] dark:text-[#B8B1A8]">{progress.stage.description}</p>
        </div>
        <span className="shrink-0 rounded-full border border-[#D8D1C8] px-2.5 py-1 font-mono text-[10px] font-bold text-[#756F69] dark:border-[#57524C] dark:text-[#D6CEC4]">
          {progress.nextStage ? `${progress.modulesToNext} to ${progress.nextStage.name}` : 'Final stage'}
        </span>
      </div>
      <div className="mt-3 flex items-center gap-2.5">
        <span className="shrink-0 text-[9px] font-bold uppercase tracking-[0.12em] text-[#A0978D]">Rank progress</span>
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-[#ECE7E0] dark:bg-[#37332F]">
          <div className="h-full rounded-full bg-[#F26B1F] transition-[width] duration-700" style={{ width: `${Math.round(progress.progress * 100)}%` }} />
        </div>
        <span className="font-mono text-[9px] font-bold text-[#756F69] dark:text-[#B8B1A8]">{Math.round(progress.progress * 100)}%</span>
      </div>
    </div>

    <div className="px-4 py-4">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A0978D]">First foundations</p>
        <span className="font-mono text-[10px] font-bold text-[#756F69] dark:text-[#B8B1A8]">
          {progress.foundationCompletedCount}/{progress.foundationSteps.length}
        </span>
      </div>
      <div className="mb-4 h-1.5 overflow-hidden rounded-full bg-[#ECE7E0] dark:bg-[#37332F]">
        <div
          className="h-full rounded-full bg-[#4C9A78] transition-[width] duration-700"
          style={{ width: `${(progress.foundationCompletedCount / progress.foundationSteps.length) * 100}%` }}
        />
      </div>
      <div className="space-y-2.5">
        {progress.foundationSteps.map(step => (
          <div key={step.id} className="flex gap-2.5">
            {step.complete
              ? <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-full bg-[#DDF3E8] text-[#247554]"><Check size={12} strokeWidth={3} /></span>
              : <Circle size={20} className="mt-0.5 shrink-0 text-[#C7BFB6]" />}
            <div>
              <p className={`text-xs font-bold ${step.complete ? 'text-[#756F69] line-through decoration-[#C7BFB6]' : 'text-[#242220] dark:text-[#F7F1E8]'}`}>{step.label}</p>
              {!step.complete && <p className="mt-0.5 text-[10px] text-[#938B83] dark:text-[#AAA198]">{step.detail}</p>}
            </div>
          </div>
        ))}
      </div>
      {progress.unplacedCount > 0 && (
        <button onClick={onOpenBuildMode} className="mt-4 flex w-full items-center justify-between rounded-xl border border-[#D8D1C8] bg-white px-3 py-2.5 text-left dark:border-[#57524C] dark:bg-[#292724]">
          <span className="flex items-center gap-2 text-xs font-bold text-[#343230] dark:text-[#F7F1E8]"><PackageOpen size={15} /> Build Tray</span>
          <span className="font-mono text-[10px] text-[#C94F10] dark:text-[#FF9A62]">{progress.unplacedCount} waiting</span>
        </button>
      )}
    </div>
  </section>
);

export default JourneyPathCard;
