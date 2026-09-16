import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import CrewIllustration from './CrewIllustration';

export default function CrewEmptyState({ character = 'star-crew:maker', eyebrow = 'A place to begin', title, children, action, onAction }: {
  character?: string; eyebrow?: string; title: string; children: React.ReactNode; action?: string; onAction?: () => void;
}) {
  return <div className="crew-empty"><div className="crew-empty-art" aria-hidden="true"><CrewIllustration character={character} /></div><div><span className="crew-eyebrow">{eyebrow}</span><h3>{title}</h3><p>{children}</p>{action && onAction && <button type="button" className="crew-primary" onClick={onAction}>{action}<ArrowUpRight size={17} aria-hidden="true" /></button>}</div></div>;
}
