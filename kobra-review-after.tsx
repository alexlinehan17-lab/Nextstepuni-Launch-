/**
 * Dev-only (27 Oct 2026). Mounts ONE Kobra rebuild from kobra-review/sections/
 * on its own, for screenshots of the "With Kobra" pane at any width:
 * /kobra-review-after.html?section=mark-bank-session|progress|onboarding|topic-atlas|legal|command|planner|email-link&theme=dark
 */
import React, { Suspense, lazy, type ComponentType } from 'react';
import { createRoot } from 'react-dom/client';
import KobraScope, { Toasts } from './components/approved-ui-runtime';
import './index.css';
import './kobra-review.css';

const params = new URLSearchParams(window.location.search);
if (params.get('theme') === 'dark') document.documentElement.classList.add('dark');
const FILES: Record<string, string> = {
  'mark-bank-session': 'MarkBankSession', progress: 'Progress', onboarding: 'Onboarding', 'topic-atlas': 'TopicAtlas',
  legal: 'Legal', command: 'CommandPalette', planner: 'Planner', 'email-link': 'EmailLink',
};
const MODULES = import.meta.glob('./kobra-review/sections/*After.tsx') as Record<string, () => Promise<{ default: ComponentType }>>;
const file = FILES[params.get('section') ?? ''];
const loader = file ? MODULES[`./kobra-review/sections/${file}After.tsx`] : undefined;
const After = loader ? lazy(loader) : null;

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(
    <KobraScope className="kr-page">
      <div className="kr-shell" style={{ padding: 20 }}>
        {After ? <Suspense fallback={<p className="kr-pending">Loading…</p>}><After /></Suspense> : <p className="kr-pending">Unknown section.</p>}
        <Toasts />
      </div>
    </KobraScope>,
  );
}
