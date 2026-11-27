import React from 'react';
import { ChevronRight, Lock } from 'lucide-react';
import { type ToolIconKey } from '../ToolIconBlob';
import { ToolArtwork } from './ToolMasthead';
import { PressBox } from '../ui/List';
import './catalogue.css';

interface LaunchpadToolCardProps {
  tool: ToolIconKey;
  title: string;
  description: string;
  locked: boolean;
  pending: boolean;
  recommendation?: string;
  onClick: () => void;
}
/** One tool on the Launchpad (boards c-launch-header, r5-launchpad): its drawing, its name with the
 *  chevron and its own line. A row on a phone; a box you press, three a row, on a laptop. */
export default function LaunchpadToolCard({ tool, title, description, locked, pending, recommendation, onClick }: LaunchpadToolCardProps) {
  return <PressBox className={`lp7-tool${locked ? ' lp7-tool--locked' : ''}`} label={pending ? `Loading profile for ${title}` : locked ? `Set up profile to unlock ${title}` : `Open ${title}`} onPress={pending ? undefined : onClick}>
    <ToolArtwork tool={tool} className="lp7-tool-art" />
    <span className="lp7-tool-name"><h3 className="lp7-tool-title">{title}</h3><ChevronRight className="ui-icon lp7-tool-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" /></span>
    <span className="lp7-tool-line">{description}</span>
    {(locked || pending) && <span className="lp7-tool-meta">{locked && <Lock width={16} height={16} strokeWidth={2} aria-hidden="true" />}{pending ? 'Checking your profile…' : 'Add your subjects to unlock'}</span>}
    {recommendation && <span className="lp7-tool-meta">Recommended by {recommendation}</span>}
  </PressBox>;
}
