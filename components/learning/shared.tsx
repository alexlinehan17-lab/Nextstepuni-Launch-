import type { ReactNode } from 'react';
import { ArrowLeft } from 'lucide-react';
import KobraScope from '../approved-ui-runtime';
import { Button } from '../approved-ui-runtime';
import ThemeArtwork from '../ThemeArtwork';
import './learning.css';

export function Artwork({ src, size = 120, className = '' }: { src: string; size?: number; className?: string }) {
  return <ThemeArtwork src={src} alt="" width={size} height={size} className={`rs-art ${className}`} />;
}
export function Eyebrow({ children }: { children: ReactNode }) {
  return <p className="rs-eyebrow">{children}</p>;
}
export function LearningShell({ children, title, onBack }: { children: ReactNode; title: string; onBack: () => void }) {
  return <KobraScope className="nsu-learning"><header className="kl-navigation"><Button variant="outline" size="icon" aria-label="Back" onClick={onBack}><ArrowLeft /></Button><span>{title}</span></header>{children}</KobraScope>;
}
