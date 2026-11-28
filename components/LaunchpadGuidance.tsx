/**
 * Launchpad orientation: a quick tool explainer and a short, deterministic
 * recommendation conversation. Recommendations are transparent and never
 * claim a false match score.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Check, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';
import ToolIconBlob, { type ToolIconKey } from './ToolIconBlob';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import { Sheet } from './ui/Sheet';
import { Button, Glyph, IconButton, TextButton } from './ui/Button';
import { List, Row } from './ui/List';
import { Menu } from './ui/Menu';
import { ToolArtwork } from './launchpad/ToolMasthead';
import './launchpad/catalogue.css';
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
  compact?: boolean;
  tools: LaunchpadToolSummary[];
  /** Tools the student can launch in their current setup state. The explainer
   * still shows the full catalogue, but recommendations never point at a
   * profile-gated dead end. */
  availableToolIds?: string[];
  recommendation: ToolRecommendation | null;
  onRecommendationChange: (recommendation: ToolRecommendation | null) => void;
  onOpenTool: (toolId: string, needsProfile: boolean) => void;
}

type GuidanceMode = 'explain' | 'recommend';


const LaunchpadGuidance: React.FC<LaunchpadGuidanceProps> = ({
  tools,
  compact = false,
  availableToolIds,
  recommendation,
  onRecommendationChange,
  onOpenTool,
}) => {
  const [mode, setMode] = useState<GuidanceMode | null>(null);
  const [toolIndex, setToolIndex] = useState(0);
  const [goalId, setGoalId] = useState<RecommendationGoalId | null>(null);
  const guideBodyRef = useRef<HTMLDivElement>(null);
  const guideTitleRef = useRef<HTMLSpanElement>(null);
  const availableIds = useMemo(
    () => availableToolIds ?? tools.map(tool => tool.id),
    [availableToolIds, tools],
  );
  const goals = useMemo(() => availableRecommendationGoals(availableIds), [availableIds]);
  const activeGoal = goals.find(goal => goal.id === goalId) ?? null;
  const explainedTool = tools[Math.min(toolIndex, Math.max(0, tools.length - 1))];
  const recommendedTool = recommendation && availableIds.includes(recommendation.toolId)
    ? tools.find(tool => tool.id === recommendation.toolId)
    : null;

  const open = (nextMode: GuidanceMode) => {
    setMode(nextMode);
    if (nextMode === 'recommend') setGoalId(null);
  };

  const mobileAppDesign = useMobileAppDesign();
  const close = () => setMode(null);

  // Moving to another tool or question starts at the top of the sheet; on a phone the
  // sheet's title takes focus so a screen reader hears where it is (the shared Sheet
  // holds focus inside, locks the page and closes on Escape).
  useEffect(() => {
    if (!mode) return;
    const scroller = guideBodyRef.current?.closest('.ui-sheet-body') as HTMLElement | null;
    if (scroller) scroller.scrollTop = 0;
    if (mobileAppDesign) guideTitleRef.current?.focus({ preventScroll: true });
  }, [mobileAppDesign, mode, toolIndex, goalId, recommendation?.toolId]);

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
      {compact ? <div className="lp7-guide">
        <TextButton arrow="forward" onClick={() => open('explain')}>Meet the tools</TextButton>
        <TextButton arrow="forward" onClick={() => open('recommend')}>Help me choose</TextButton>
      </div> : <>
      <section aria-labelledby="launchpad-help-heading" className={`mb-6 sm:mb-8 ${mobileAppDesign ? '[&_button]:min-h-11' : ''}`}>
        <div className="mb-3 sm:mb-4">
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Not sure where to begin?</p>
          <h2 id="launchpad-help-heading" className="mt-1 text-lg font-semibold text-[var(--ink-primary)] sm:text-xl">Find your way around the Launchpad.</h2>
        </div>

        <div className={mobileAppDesign ? "grid grid-cols-1 gap-3 sm:grid-cols-2" : "grid auto-cols-[minmax(270px,86vw)] grid-flow-col gap-3 overflow-x-auto snap-x snap-mandatory pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden sm:grid-flow-row sm:grid-cols-2 sm:overflow-visible sm:pb-0"}>
          <button
            type="button"
            onClick={() => open('explain')}
            className="group flex min-h-[96px] snap-start items-center gap-3 rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] p-4 text-left transition-all hover:-translate-y-0.5 hover:shadow-[3px_3px_0_0_var(--outline-strong)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.45)] sm:min-h-[116px] sm:gap-4 sm:p-5"
          >
            <ToolIconBlob toolId="meet-tools" size={56} />
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-[var(--ink-primary)]">Meet the tools</span>
              <span className="mt-1 block text-xs leading-relaxed text-[var(--ink-secondary)]">A quick, plain-English guide to what each tool is for.</span>
            </span>
            <ArrowRight size={17} className="shrink-0 text-[var(--ink-muted)] transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
          </button>

          <button
            type="button"
            onClick={() => open('recommend')}
            className="group flex min-h-[96px] snap-start items-center gap-3 rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] p-4 text-left transition-all hover:-translate-y-0.5 hover:shadow-[3px_3px_0_0_var(--outline-strong)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.45)] sm:min-h-[116px] sm:gap-4 sm:p-5"
          >
            <ToolIconBlob toolId="recommend-tool" size={56} />
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
      </>}

      {/* The guide: the shared sheet (a bottom sheet on a phone, a dialog on a laptop), Close at
          its top left, the one main action pinned at its foot in charcoal. */}
      <Sheet open={Boolean(mode)} onClose={close} closeLabel="Close Launchpad guide" className="lp7-guide-sheet"
        title={<span ref={guideTitleRef} tabIndex={-1} id="launchpad-guidance-title">{mode === 'explain'
          ? 'Meet the tools'
          : recommendation
            ? 'Your recommendation'
            : goalId
              ? 'One more question'
              : 'What would help right now?'}</span>}
        footer={mode === 'explain' && explainedTool
          ? <div className="lp7-guide-foot"><TextButton tone="quiet" onClick={() => open('recommend')}>Still unsure? Get a recommendation</TextButton><Button kind="main" size="lg" block arrow="forward" onClick={() => launch(explainedTool)}>{`Open ${explainedTool.title}`}</Button></div>
          : mode === 'recommend' && recommendation && recommendedTool
            ? <div className="lp7-guide-foot"><TextButton tone="quiet" onClick={() => { onRecommendationChange(null); setGoalId(null); }}><span className="lp7-inline"><Glyph icon={RotateCcw} size={16} />Start again</span></TextButton><Button kind="main" size="lg" block arrow="forward" onClick={() => launch(recommendedTool)}>{`Open ${recommendedTool.title}`}</Button></div>
            : undefined}>
        <div ref={guideBodyRef} className="lp7-guide-body">
          {mode === 'explain' && explainedTool && (
            <div className="lp7-guide-explain">
              <List className="lp7-guide-list" label="Tools in this guide">
                {tools.map((tool, index) => <Row key={tool.id} title={tool.title} selected={index === toolIndex} onPress={() => setToolIndex(index)} />)}
              </List>
              <div className="lp7-guide-tool">
                <div className="lp7-guide-step">
                  <IconButton label="Previous tool" icon={<Glyph icon={ChevronLeft} />} aria-disabled={toolIndex === 0 || undefined} onClick={() => setToolIndex(index => Math.max(0, index - 1))} />
                  <Menu label="Choose a tool" block count value={explainedTool.id} options={tools.map(tool => ({ value: tool.id, label: tool.title }))} onChange={id => setToolIndex(tools.findIndex(tool => tool.id === id))} />
                  <IconButton label="Next tool" icon={<Glyph icon={ChevronRight} />} aria-disabled={toolIndex === tools.length - 1 || undefined} onClick={() => setToolIndex(index => Math.min(tools.length - 1, index + 1))} />
                </div>
                <div className="lp7-guide-head">
                  <ToolArtwork tool={explainedTool.id as ToolIconKey} className="lp7-guide-art" />
                  <div className="lp7-guide-name">
                    <p className="t-label">{explainedTool.tag}</p>
                    <h3 className="t-name-sm">{explainedTool.title}</h3>
                  </div>
                </div>
                <p className="t-body lp7-guide-when">Use this when: {TOOL_GUIDANCE[explainedTool.id]?.useWhen ?? explainedTool.description}</p>
                <dl className="lp7-guide-facts">
                  <div><dt className="t-label">What it does</dt><dd className="t-sub">{TOOL_GUIDANCE[explainedTool.id]?.whatItDoes ?? explainedTool.description}</dd></div>
                  <div><dt className="t-label">You’ll leave with</dt><dd className="t-sub">{TOOL_GUIDANCE[explainedTool.id]?.outcome ?? 'A clearer next step and a useful piece of work completed.'}</dd></div>
                </dl>
              </div>
            </div>
          )}

          {mode === 'recommend' && !goalId && !recommendation && (
            <div className="lp7-guide-ask">
              <p className="t-sub">Choose the thought closest to yours. There is no score and no wrong answer.</p>
              <List boxed label="What would help right now?">
                {goals.map(goal => <Row key={goal.id} title={goal.label} onPress={() => setGoalId(goal.id)} />)}
              </List>
            </div>
          )}

          {mode === 'recommend' && goalId && activeGoal && !recommendation && (
            <div className="lp7-guide-ask">
              <TextButton tone="quiet" onClick={() => setGoalId(null)}><span className="lp7-inline"><Glyph icon={ArrowLeft} size={16} />Back</span></TextButton>
              <p className="t-label">Question 2 of 2</p>
              <h3 className="t-title">{activeGoal.question}</h3>
              <List boxed label={activeGoal.question}>
                {activeGoal.options.map(answer => <Row key={answer.id} title={answer.label} onPress={() => selectAnswer(answer.id)} />)}
              </List>
            </div>
          )}

          {mode === 'recommend' && recommendation && recommendedTool && (
            <div className="lp7-guide-ask">
              <p className="lp7-guide-clear t-sub"><Check width={16} height={16} strokeWidth={2} aria-hidden="true" /> A clear place to start</p>
              <div className="lp7-guide-head">
                <ToolArtwork tool={recommendedTool.id as ToolIconKey} className="lp7-guide-art lp7-guide-art--lg" />
                <div className="lp7-guide-name">
                  <p className="t-label">Start with</p>
                  <h3 className="t-name">{recommendedTool.title}</h3>
                </div>
              </div>
              <p className="t-body">You said “{recommendation.answerLabel}”. {TOOL_GUIDANCE[recommendedTool.id]?.whatItDoes ?? recommendedTool.description}</p>
              <dl className="lp7-guide-facts">
                <div><dt className="t-label">You’ll leave with</dt><dd className="t-sub">{TOOL_GUIDANCE[recommendedTool.id]?.outcome ?? 'A clearer next step.'}</dd></div>
              </dl>
            </div>
          )}
        </div>
      </Sheet>
    </>
  );
};

export default LaunchpadGuidance;
