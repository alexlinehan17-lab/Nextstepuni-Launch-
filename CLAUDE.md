# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nextstepuni is an educational platform ("Learning Lab") that teaches university-bound students advanced learning strategies through interactive modules. It's a React SPA with Firebase backend for auth and data persistence.

## Commands

```bash
npm install          # Install dependencies
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build via Vite
npm run preview      # Preview production build
```

No test runner or linter is configured. There are no test or lint commands.

## Environment

Requires `GEMINI_API_KEY` set in `.env.local` for Google Gemini API integration.

## Architecture

**Stack:** React 19 + TypeScript, Vite, Tailwind CSS (CDN), Framer Motion, Three.js (@react-three/fiber), Firebase (Auth + Firestore)

**Entry flow:** `index.html` → `index.tsx` → `App.tsx`

**App.tsx** (~310 lines) is the central orchestrator. It manages:
- Authentication state via Firebase `onAuthStateChanged`
- User progress persistence (Firestore `users/{uid}` and `progress/{uid}` collections)
- Route-like navigation via local state (no router library — views switch based on state)

**Root-level modules:**
- `moduleRegistry.ts` — Lazy-loads all 43 educational modules + InnovationZone via `React.lazy()` with default imports
- `courseData.ts` — Course metadata definitions (titles, descriptions, categories, tags) and `categoryColorMap`
- `moduleThemes.ts` — Per-color Tailwind theme objects (literal class strings required for CDN scanning)
- `types.ts` — Shared types: `ModuleProgress`, `UserProgress`, `SectionDefinition`, `ModuleTheme`

**Key components in `components/`:**
- `Auth.tsx` — Login/registration modal with Firebase Auth. Admin login uses Firebase Auth with the `admin@nextstep.app` account (password managed in Firebase Console, not in code).
- `KnowledgeTree.tsx` — Main navigation hub showing categories with activity ring progress indicators
- `Library.tsx` — Grid view of modules within a category using `BentoModuleTile` components
- `AdminDashboard.tsx` — Admin-only analytics view
- `ModuleLayout.tsx` — Shared sidebar + content layout used by all educational modules
- `ModuleShared.tsx` — Reusable UI primitives: `Highlight`, `ReadingSection`, `MicroCommitment`, `ActivityRing`
- `*Module.tsx` (43 files) — Individual educational modules, each using `ModuleLayout` with default exports

**Module component interface:**
```typescript
interface ModuleProps {
  onBack: () => void;
  progress: ModuleProgress;                        // { unlockedSection: number }
  onProgressUpdate: (progress: ModuleProgress) => void;
}
```

**7 course categories:** `architecture-mindset`, `science-growth`, `learning-cheat-codes`, `subject-specific-science`, `exam-zone`, `the-shield`, `the-launchpad`

**Navigation flow:** KnowledgeTree (category selection) → Library (module grid) → Module (content sections with progressive unlock)

## Conventions

- All components are functional with hooks; no class components
- Styling: Tailwind utility classes with dark mode (`dark:` prefix), glass-morphism effects, custom gradients
- Animations: Framer Motion wrappers (`MotionDiv`, `MotionButton` with `as any` cast)
- Reusable UI primitives in `ModuleShared.tsx`: `Highlight` (interactive tooltip), `ReadingSection` (content block), `MicroCommitment` (action prompt), `ActivityRing` (SVG progress)
- All source files carry Apache-2.0 license headers
- Constants use UPPER_SNAKE_CASE; components use PascalCase; handlers use `handle` prefix

## Notable Details

- User avatars generated via DiceBear API (`api.dicebear.com/9.x/notionists-neutral/svg`)
- Firebase config is in `firebase.ts`; hosting config in `firebase.json`
- Tailwind theme customization (fonts, colors) is in `index.html` via CDN config, not a tailwind.config file
- All module components use default exports for clean lazy-loading in `moduleRegistry.ts`
