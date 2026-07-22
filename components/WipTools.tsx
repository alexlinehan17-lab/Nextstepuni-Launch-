/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * WIP — the workshop shelf. Launchpad tools that are being actively built but
 * aren't polished enough for the main grid yet. They stay fully usable from
 * here (each opens the real tool via the Launchpad deep-link); they're just
 * honestly labelled as in-progress so students know what they're getting.
 */

import React from 'react';
import { MotionDiv } from './Motion';
import { ArrowLeft, Hammer, Images, ListChecks, Mic, SpellCheck, Stamp } from 'lucide-react';

const SERIF: React.CSSProperties = { fontFamily: "'Source Serif 4', serif" };
const SANS: React.CSSProperties = { fontFamily: "'DM Sans', system-ui, sans-serif" };

/** The tools currently parked in the workshop. Keep ids in sync with
 *  InnovationZone's WIP_TOOL_IDS — that set hides them from the main grid. */
const WIP_TOOLS: { id: string; title: string; description: string; icon: React.ComponentType<{ size?: number; className?: string }> }[] = [
  { id: 'diagram-vault', title: 'Diagram Vault', description: 'Every diagram, graph, map and chart that has come up in the exams — decoded.', icon: Images },
  { id: 'answer-architect', title: 'Answer Architect', description: 'The mark-earning skeleton of a top answer — the beats a full-marks answer is built from, in order.', icon: ListChecks },
  { id: 'definition-drill', title: 'Definition Drill', description: 'Drill the exact mark-earning wording the SEC scheme awards the definition marks for.', icon: SpellCheck },
  { id: 'oral-trainer', title: 'Irish Oral Trainer', description: 'Rehearse the Irish oral out loud, record yourself, and track your readiness on every part.', icon: Mic },
  { id: 'examiners-chair', title: 'The Examiner’s Chair', description: 'Mark scripts against the real SEC rules — and learn exactly where marks are won and lost.', icon: Stamp },
];

interface WipToolsProps {
  onBack: () => void;
  /** Opens the tool inside the Launchpad (deep-link). */
  onOpenTool: (toolId: string) => void;
}

const WipTools: React.FC<WipToolsProps> = ({ onBack, onOpenTool }) => (
  <div className="min-h-screen bg-[#FAFBF6] dark:bg-zinc-950 pt-16 md:pt-20 pb-32 px-4 sm:px-6 transition-colors duration-500">
    <div className="max-w-3xl mx-auto">
      {/* ── Header ── */}
      <div className="flex items-center gap-4 mb-4">
        <button
          onClick={onBack}
          aria-label="Back"
          className="w-10 h-10 rounded-xl flex items-center justify-center bg-white border border-[#EDEBE8] hover:bg-[#F8F4EC] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(242,107,31,0.35)]"
          style={{ boxShadow: '0 1px 2px rgba(28,25,23,0.04)' }}
        >
          <ArrowLeft size={18} className="text-[#1a1a1a]" />
        </button>
        <h1
          style={{
            ...SERIF,
            fontSize: 'clamp(32px, 5vw, 44px)',
            fontWeight: 500,
            letterSpacing: '-0.6px',
            color: '#1a1a1a',
            margin: 0,
            lineHeight: 1.05,
          }}
        >
          Workshop
        </h1>
      </div>
      <p className="mb-10" style={{ ...SANS, fontSize: 14.5, lineHeight: 1.6, color: 'rgba(0,0,0,0.55)', maxWidth: '56ch' }}>
        Tools we&rsquo;re actively building. Everything here works — it&rsquo;s just not finished. Expect rough edges,
        and expect them to get better week by week.
      </p>

      {/* ── Tool list ── */}
      <div className="space-y-3">
        {WIP_TOOLS.map((t, i) => {
          const Icon = t.icon;
          return (
            <MotionDiv
              key={t.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] as number[] }}
            >
              <button
                onClick={() => onOpenTool(t.id)}
                className="w-full flex items-center gap-4 text-left rounded-2xl bg-white px-5 py-4 transition-transform hover:-translate-y-0.5 active:translate-y-0"
                style={{ border: '1px solid #E8E2D8', boxShadow: '0 4px 28px rgba(28,25,23,0.06), 0 1px 3px rgba(28,25,23,0.04)' }}
              >
                <span className="shrink-0 w-11 h-11 rounded-xl flex items-center justify-center" style={{ backgroundColor: '#FDEEDF' }}>
                  <Icon size={20} className="text-[#F26B1F]" />
                </span>
                <span className="flex-1 min-w-0">
                  <span className="flex items-center gap-2">
                    <span style={{ ...SERIF, fontSize: 17, fontWeight: 600, color: '#1a1a1a' }}>{t.title}</span>
                    <span
                      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9.5px] font-bold uppercase tracking-[0.08em]"
                      style={{ ...SANS, backgroundColor: '#f0eeec', color: '#9e9186' }}
                    >
                      <Hammer size={9} /> In progress
                    </span>
                  </span>
                  <span className="block mt-0.5" style={{ ...SANS, fontSize: 13, lineHeight: 1.5, color: 'rgba(0,0,0,0.55)' }}>
                    {t.description}
                  </span>
                </span>
                <span className="shrink-0" style={{ color: '#F26B1F', fontSize: 18, lineHeight: 1 }}>→</span>
              </button>
            </MotionDiv>
          );
        })}
      </div>
    </div>
  </div>
);

export default WipTools;
