import React from 'react';
import { ArrowRight, Lock } from 'lucide-react';
import { type ToolIconKey } from '../ToolIconBlob';
import { ToolArtwork } from './ToolMasthead';

interface LaunchpadToolCardProps {
  tool: ToolIconKey;
  title: string;
  description: string;
  locked: boolean;
  pending: boolean;
  recommendation?: string;
  onClick: () => void;
}
export default function LaunchpadToolCard({ tool, title, description, locked, pending, recommendation, onClick }: LaunchpadToolCardProps) {
  return <button type="button" className="lp-tool-card" disabled={pending} aria-label={pending ? `Loading profile for ${title}` : locked ? `Set up profile to unlock ${title}` : `Open ${title}`} onClick={onClick}>
    <ToolArtwork tool={tool} /><h3>{title}</h3><ArrowRight size={19} aria-hidden="true" /><p>{description}</p>
    {(locked || pending) && <span className="lp-tool-status">{locked && <Lock size={13} aria-hidden="true" />}{pending ? 'Checking your profile…' : 'Add your subjects to unlock'}</span>}
    {recommendation && <p>Recommended by {recommendation}</p>}
  </button>;
}
