/**
 * Launchpad orientation: a quick tool explainer and a short, deterministic
 * recommendation conversation. Recommendations are transparent and never
 * claim a false match score.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight, Check, ChevronLeft, ChevronRight, RotateCcw, X } from 'lucide-react';
import { MotionDiv } from './Motion';
import ToolIconBlob, { type ToolIconKey } from './ToolIconBlob';
import {
  TOOL_GUIDANCE,
  availableRecommendationGoals,
  recommendTool,
  type RecommendationGoalId,
  type ToolRecommendation,
} from './launchpadGuidanceData';

export interface LaunchpadToolSummary {
  id: string;
  title: string;
  description: string;
  tag: string;
  needsProfile: boolean;
}

interface LaunchpadGuidanceProps {
  tools: LaunchpadToolSummary[];
  recommendation: ToolRecommendation | null;
  onRecommendationChange: (recommendation: ToolRecommendation | null) => void;
  onOpenTool: (toolId: string, needsProfile: boolean) => void;
}

type GuidanceMode = 'explain' | 'recommend';

const ACCENT = '#F26B1F';

const LaunchpadGuidance: React.FC<LaunchpadGuidanceProps> = ({
  tools,
  recommendation,
  onRecommendationChange,
  onOpenTool,
}) => {
  const [mode, setMode] = useState<GuidanceMode | null>(null);
  const [toolIndex, setToolIndex] = useState(0);
  const [goalId, setGoalId] = useState<RecommendationGoalId | null>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const availableIds = useMemo(() => tools.map(tool => tool.id), [tools]);
  const goals = useMemo(() => availableRecommendationGoals(availableIds), [availableIds]);
  const activeGoal = goals.find(goal => goal.id === goalId) ?? null;
  const explainedTool = tools[Math.min(toolIndex, Math.max(0, tools.length - 1))];
  const recommendedTool = recommendation ? tools.find(tool => tool.id === recommendation.toolId) : null;

  const open = (nextMode: GuidanceMode) => {
    setMode(nextMode);
    if (nextMode === 'recommend') setGoalId(null);
  };

  const close = () => setMode(null);

  useEffect(() => {
    if (!mode) return;
    closeButtonRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') close();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [mode]);

  const selectAnswer = (answerId: string) => {
    if (!goalId) return;
    const result = recommendTool(goalId, answerId, availableIds);
    if (result) onRecommendationChange(result);
  };

  const launch = (tool: LaunchpadToolSummary) => {
    close();
    onOpenTool(tool.id, tool.needsProfile);
  };

  return (
    <>
      <section aria-labelledby="launchpad-help-heading" className="mb-8">
        <div className="mb-4">
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Not sure where to begin?</p>
          <h2 id="launchpad-help-heading" className="mt-1 text-xl font-semibold text-[var(--ink-primary)]">Find your way around the Launchpad.</h2>
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <button
            type="button"
            onClick={() => open('explain')}
            className="group flex min-h-[116px] items-center gap-4 rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] p-5 text-left transition-all hover:-translate-y-0.5 hover:shadow-[3px_3px_0_0_var(--outline-strong)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.45)]"
          >
            <ToolIconBlob toolId="meet-tools" size={60} />
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-[var(--ink-primary)]">Meet the tools</span>
              <span className="mt-1 block text-xs leading-relaxed text-[var(--ink-secondary)]">A quick, plain-English guide to what each tool is for.</span>
            </span>
            <ArrowRight size={17} className="shrink-0 text-[var(--ink-muted)] transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
          </button>

          <button
            type="button"
            onClick={() => open('recommend')}
            className="group flex min-h-[116px] items-center gap-4 rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] p-5 text-left transition-all hover:-translate-y-0.5 hover:shadow-[3px_3px_0_0_var(--outline-strong)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.45)]"
          >
            <ToolIconBlob toolId="recommend-tool" size={60} />
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-[var(--ink-primary)]">Recommend a tool</span>
              <span className="mt-1 block text-xs leading-relaxed text-[var(--ink-secondary)]">Answer two quick questions and get one clear starting point.</span>
            </span>
            <ArrowRight size={17} className="shrink-0 text-[var(--ink-muted)] transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
          </button>
        </div>

        {recommendedTool && recommendation && (
          <div className="mt-4 flex flex-col gap-4 border-y border-[var(--outline-soft)] py-4 sm:flex-row sm:items-center">
            <ToolIconBlob toolId={recommendedTool.id as ToolIconKey} size={52} />
            <div className="min-w-0 flex-1">
              <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Your current recommendation</p>
              <p className="mt-1 font-semibold text-[var(--ink-primary)]">{recommendedTool.title}</p>
              <p className="mt-0.5 text-xs leading-relaxed text-[var(--ink-secondary)]">Because you said: “{recommendation.answerLabel}”.</p>
            </div>
            <div className="flex shrink-0 gap-2">
              <button type="button" onClick={() => { onRecommendationChange(null); setGoalId(null); open('recommend'); }} className="rounded-lg border border-[var(--outline-soft)] px-3 py-2 text-xs font-medium text-[var(--ink-secondary)] hover:border-[var(--outline-strong)]">Choose again</button>
              <button type="button" onClick={() => launch(recommendedTool)} className="rounded-lg border-[1.5px] border-[var(--outline-strong)] bg-[var(--ink-primary)] px-4 py-2 text-xs font-semibold text-[var(--surface-paper)]">Open tool</button>
            </div>
          </div>
        )}
      </section>

      {createPortal(<AnimatePresence>
        {mode && (
          <div className="fixed inset-0 z-[220] flex items-end justify-center sm:items-center sm:p-5" role="dialog" aria-modal="true" aria-labelledby="launchpad-guidance-title">
            <button type="button" aria-label="Close" onClick={close} className="absolute inset-0 bg-[#1A1A1A]/60" />
            <MotionDiv
              initial={{ opacity: 0, y: 24, scale: 0.99 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 18, scale: 0.99 }}
              transition={{ duration: 0.22 }}
              className="relative flex max-h-[92dvh] w-full max-w-4xl flex-col overflow-hidden rounded-t-[24px] border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-canvas)] shadow-2xl sm:rounded-[24px]"
            >
              <header className="flex items-start justify-between gap-4 border-b border-[var(--outline-soft)] bg-[var(--surface-paper)] px-5 py-4 sm:px-7">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Launchpad guide</p>
                  <h2 id="launchpad-guidance-title" className="mt-1 text-xl font-semibold text-[var(--ink-primary)]">
                    {mode === 'explain'
                      ? 'Meet the tools'
                      : recommendation
                        ? 'Your recommendation'
                        : goalId
                          ? 'One more question'
                          : 'What would help right now?'}
                  </h2>
                </div>
                <button ref={closeButtonRef} type="button" onClick={close} aria-label="Close Launchpad guide" className="flex h-10 w-10 items-center justify-center rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] text-[var(--ink-secondary)]">
                  <X size={18} />
                </button>
              </header>

              {mode === 'explain' && explainedTool && (
                <div className="grid min-h-0 flex-1 overflow-y-auto md:grid-cols-[240px_1fr]">
                  <nav aria-label="Tools in this guide" className="hidden overflow-y-auto border-r border-[var(--outline-soft)] bg-[var(--surface-soft)] p-3 md:block">
                    {tools.map((tool, index) => (
                      <button
                        type="button"
                        key={tool.id}
                        onClick={() => setToolIndex(index)}
                        aria-current={index === toolIndex ? 'true' : undefined}
                        className={`mb-1 w-full rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${index === toolIndex ? 'bg-[var(--surface-paper)] font-semibold text-[var(--ink-primary)] border border-[var(--outline-strong)]' : 'text-[var(--ink-secondary)] hover:bg-[var(--surface-paper)]'}`}
                      >
                        {tool.title}
                      </button>
                    ))}
                  </nav>

                  <div className="flex min-h-[560px] flex-col p-6 sm:p-8">
                    <div className="mb-5 flex items-center justify-between md:hidden">
                      <button type="button" onClick={() => setToolIndex(index => Math.max(0, index - 1))} disabled={toolIndex === 0} aria-label="Previous tool" className="flex h-9 w-9 items-center justify-center rounded-lg border border-[var(--outline-soft)] disabled:opacity-30"><ChevronLeft size={18} /></button>
                      <span className="text-xs tabular-nums text-[var(--ink-muted)]">{toolIndex + 1} of {tools.length}</span>
                      <button type="button" onClick={() => setToolIndex(index => Math.min(tools.length - 1, index + 1))} disabled={toolIndex === tools.length - 1} aria-label="Next tool" className="flex h-9 w-9 items-center justify-center rounded-lg border border-[var(--outline-soft)] disabled:opacity-30"><ChevronRight size={18} /></button>
                    </div>

                    <div className="flex items-start gap-5">
                      <ToolIconBlob toolId={explainedTool.id as ToolIconKey} size={78} />
                      <div className="min-w-0 pt-1">
                        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">{explainedTool.tag}</p>
                        <h3 className="mt-1 text-2xl font-semibold text-[var(--ink-primary)]">{explainedTool.title}</h3>
                      </div>
                    </div>

                    <p className="mt-6 text-lg leading-relaxed text-[var(--ink-primary)]">
                      <strong>Use this when:</strong> {TOOL_GUIDANCE[explainedTool.id]?.useWhen ?? explainedTool.description}
                    </p>

                    <dl className="mt-7 divide-y divide-[var(--outline-soft)] border-y border-[var(--outline-soft)]">
                      <div className="py-4 sm:grid sm:grid-cols-[130px_1fr] sm:gap-5">
                        <dt className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--ink-muted)]">What it does</dt>
                        <dd className="mt-2 text-sm leading-relaxed text-[var(--ink-secondary)] sm:mt-0">{TOOL_GUIDANCE[explainedTool.id]?.whatItDoes ?? explainedTool.description}</dd>
                      </div>
                      <div className="py-4 sm:grid sm:grid-cols-[130px_1fr] sm:gap-5">
                        <dt className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--ink-muted)]">You’ll leave with</dt>
                        <dd className="mt-2 text-sm leading-relaxed text-[var(--ink-secondary)] sm:mt-0">{TOOL_GUIDANCE[explainedTool.id]?.outcome ?? 'A clearer next step and a useful piece of work completed.'}</dd>
                      </div>
                    </dl>

                    <div className="mt-auto flex flex-col-reverse gap-3 pt-7 sm:flex-row sm:items-center sm:justify-between">
                      <button type="button" onClick={() => open('recommend')} className="text-sm font-medium text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4">Still unsure? Get a recommendation</button>
                      <button type="button" onClick={() => launch(explainedTool)} className="rounded-xl border-[1.5px] border-[var(--outline-strong)] px-5 py-3 text-sm font-semibold text-white shadow-[3px_3px_0_0_var(--outline-strong)]" style={{ background: ACCENT }}>Open {explainedTool.title} <ArrowRight size={15} className="ml-1 inline" /></button>
                    </div>
                  </div>
                </div>
              )}

              {mode === 'recommend' && (
                <div className="min-h-[560px] flex-1 overflow-y-auto p-5 sm:p-8">
                  {!goalId && !recommendation && (
                    <div className="mx-auto max-w-2xl">
                      <p className="mb-5 text-sm text-[var(--ink-secondary)]">Choose the thought closest to yours. There is no score and no wrong answer.</p>
                      <div className="grid gap-2 sm:grid-cols-2">
                        {goals.map(goal => (
                          <button key={goal.id} type="button" onClick={() => setGoalId(goal.id)} className="flex min-h-[74px] items-center justify-between gap-3 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-4 py-3 text-left text-sm font-medium text-[var(--ink-primary)] transition-colors hover:border-[var(--outline-strong)]">
                            {goal.label}<ChevronRight size={17} className="shrink-0 text-[var(--ink-muted)]" />
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {goalId && activeGoal && !recommendation && (
                    <div className="mx-auto max-w-2xl">
                      <button type="button" onClick={() => setGoalId(null)} className="mb-6 inline-flex items-center gap-1.5 text-xs font-medium text-[var(--ink-secondary)]"><ArrowLeft size={14} /> Back</button>
                      <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Question 2 of 2</p>
                      <h3 className="mt-2 text-2xl font-semibold text-[var(--ink-primary)]">{activeGoal.question}</h3>
                      <div className="mt-6 space-y-2">
                        {activeGoal.options.map(answer => (
                          <button key={answer.id} type="button" onClick={() => selectAnswer(answer.id)} className="flex w-full items-center justify-between gap-3 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-4 py-4 text-left text-sm font-medium text-[var(--ink-primary)] transition-colors hover:border-[var(--outline-strong)]">
                            {answer.label}<ChevronRight size={17} className="shrink-0 text-[var(--ink-muted)]" />
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {recommendation && recommendedTool && (
                    <div className="mx-auto max-w-2xl">
                      <div className="flex items-center gap-2 text-xs font-semibold text-[var(--ink-secondary)]"><Check size={15} color={ACCENT} /> A clear place to start</div>
                      <div className="mt-6 flex items-start gap-5">
                        <ToolIconBlob toolId={recommendedTool.id as ToolIconKey} size={88} />
                        <div className="min-w-0 pt-1">
                          <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Start with</p>
                          <h3 className="mt-1 text-3xl font-semibold text-[var(--ink-primary)]">{recommendedTool.title}</h3>
                        </div>
                      </div>
                      <p className="mt-7 text-base leading-relaxed text-[var(--ink-primary)]">
                        You said <strong>“{recommendation.answerLabel}”</strong>. {TOOL_GUIDANCE[recommendedTool.id]?.whatItDoes ?? recommendedTool.description}
                      </p>
                      <div className="mt-6 border-y border-[var(--outline-soft)] py-4">
                        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">You’ll leave with</p>
                        <p className="mt-2 text-sm leading-relaxed text-[var(--ink-secondary)]">{TOOL_GUIDANCE[recommendedTool.id]?.outcome ?? 'A clearer next step.'}</p>
                      </div>
                      <div className="mt-7 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                        <button type="button" onClick={() => { onRecommendationChange(null); setGoalId(null); }} className="inline-flex items-center justify-center gap-1.5 text-sm font-medium text-[var(--ink-secondary)]"><RotateCcw size={15} /> Start again</button>
                        <button type="button" onClick={() => launch(recommendedTool)} className="rounded-xl border-[1.5px] border-[var(--outline-strong)] px-6 py-3 text-sm font-semibold text-white shadow-[3px_3px_0_0_var(--outline-strong)]" style={{ background: ACCENT }}>Open {recommendedTool.title} <ArrowRight size={15} className="ml-1 inline" /></button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </MotionDiv>
          </div>
        )}
      </AnimatePresence>, document.body)}
    </>
  );
};

export default LaunchpadGuidance;
