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
import { Images, ListChecks, Mic, SpellCheck, Stamp } from 'lucide-react';
import PageHeader from './ui/PageHeader';
import { List, Row } from './ui/List';
import './launchpad/workshop-7.css';

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

/** The frame's bar with its one Back and the page's name (area 7b); the tools as the shared rows,
 *  "In progress" said in a small line rather than a pill; words and links unchanged. */
const WipTools: React.FC<WipToolsProps> = ({ onBack, onOpenTool }) => (
  <div className="product-shell ws7-page min-h-screen">
    <div className="ws7-page-bar"><div className="ws7-page-width"><PageHeader onBack={onBack} title="Workshop" backLabel="Back to home" /></div></div>
    <div className="ws7-page-width ws7-page-body">
      <p className="t-sub ws7-page-lead">
        Tools we&rsquo;re actively building. Everything here works — it&rsquo;s just not finished. Expect rough edges,
        and expect them to get better week by week.
      </p>
      <List label="Workshop tools">
        {WIP_TOOLS.map(t => {
          const Icon = t.icon;
          return <Row key={t.id} icon={<Icon size={20} />} over="In progress" title={t.title} meta={t.description} onPress={() => onOpenTool(t.id)} />;
        })}
      </List>
    </div>
  </div>
);

export default WipTools;
