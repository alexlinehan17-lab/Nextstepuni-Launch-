import type { ReactNode } from 'react';
import ThemeArtwork from '../../ThemeArtwork';
import { Button } from '../../approved-ui-runtime';
import { Tabs, TabsList, TabsTrigger } from '../../approved-ui-runtime';

export function Artwork({ src, size = 120 }: { src: string; size?: number }) {
  return <ThemeArtwork src={src} transparentBackground alt="" width={size} height={size} className="pr-art" />;
}
export function Eyebrow({ children }: { children: ReactNode }) { return <p className="pr-eyebrow">{children}</p>; }
export function Surface({ children, className = '', label }: { children: ReactNode; className?: string; label?: string }) {
  return <article className={`pr-surface ${className}`} aria-label={label}>{children}</article>;
}
export function ProgressTabs({ value, onChange, options, label }: { value: string; onChange: (value: string) => void; options: { value: string; label: string }[]; label: string }) {
  return <Tabs value={value} onValueChange={value => onChange(String(value))}><TabsList aria-label={label}>{options.map(option => <TabsTrigger key={option.value} value={option.value}>{option.label}</TabsTrigger>)}</TabsList></Tabs>;
}
export function Empty({ title, children, onStartStudy }: { title: string; children: ReactNode; onStartStudy?: () => void }) {
  return <div className="pr-empty"><h3>{title}</h3><p>{children}</p>{onStartStudy && <Button variant="outline" className="nsu-ink-outline" onClick={onStartStudy}>Plan your next session</Button>}</div>;
}
