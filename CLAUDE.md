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

**App.tsx** (~916 lines) is the central orchestrator. It manages:
- Authentication state via Firebase `onAuthStateChanged`
- User progress persistence (Firestore `users/{uid}` and `progress/{uid}` collections)
- Route-like navigation via local state (no router library — views switch based on state)
- Lazy loading of all 43 educational modules via `React.lazy()`

**Key components in `components/`:**
- `Auth.tsx` — Login/registration modal with Firebase Auth. Has a dev bypass login button. Local admin account: username "admin", password "admin123".
- `KnowledgeTree.tsx` — Main navigation hub showing categories with activity ring progress indicators
- `Library.tsx` — Grid view of modules within a category using `BentoModuleTile` components
- `AdminDashboard.tsx` — Admin-only analytics view
- `*Module.tsx` (43 files) — Individual educational modules, each following the same props interface

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
- Reusable patterns: `Highlight` (interactive tooltip), `ReadingSection` (content block), `ActivityRing` (SVG progress)
- All source files carry Apache-2.0 license headers
- Constants use UPPER_SNAKE_CASE; components use PascalCase; handlers use `handle` prefix

## Notable Details

- `nextstepuni-app/` subdirectory is a duplicate/mirror of the root project structure
- `types.ts` exists at root but is empty — shared types are defined inline in `App.tsx`
- User avatars generated via DiceBear API (`api.dicebear.com/7.x/adventurer/svg`)
- Firebase config is in `firebase.ts`; hosting config in `firebase.json`
- Tailwind theme customization (fonts, colors) is in `index.html` via CDN config, not a tailwind.config file
