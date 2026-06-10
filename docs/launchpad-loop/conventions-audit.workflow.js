export const meta = {
  name: 'conventions-audit',
  description: 'Audit the Nextstepuni codebase across subsystems to document ACTUAL patterns, then synthesise an outline + inconsistencies list for CONVENTIONS.md',
  phases: [
    { title: 'Read', detail: 'parallel readers, one per subsystem → structured pattern map' },
    { title: 'Synthesise', detail: 'cross-reference findings, surface inconsistencies, propose the 8-section outline' },
  ],
}

const ROOT = '/Users/alexlinehan/Nextstepuni-Launch-'

const FINDING_SCHEMA = {
  type: 'object', required: ['area', 'patterns', 'exemplars'],
  properties: {
    area: { type: 'string' },
    patterns: { type: 'array', description: 'the ACTUAL conventions observed (reality, not aspiration), each a concrete, copyable rule with the file:line or symbol it is drawn from',
      items: { type: 'object', required: ['rule', 'evidence'], properties: {
        rule: { type: 'string' }, evidence: { type: 'string', description: 'file path + symbol/line that proves it' } } } },
    exemplars: { type: 'array', description: 'named files/components a fresh dev should copy as the golden example for this area',
      items: { type: 'object', required: ['name', 'whatItShows'], properties: { name: { type: 'string' }, whatItShows: { type: 'string' } } } },
    schemasOrSignatures: { type: 'array', items: { type: 'string' }, description: 'verbatim TS types/interfaces/prop signatures a dev must match (copy exactly from source)' },
    smells: { type: 'array', items: { type: 'string' }, description: 'inconsistencies, stale code, or deviations noticed within THIS area (feed the Known-inconsistencies section)' },
  },
}

const BASE = `You are auditing the Nextstepuni codebase (React 19 + TS + Vite + Tailwind v3 + Framer Motion + Firebase) at ${ROOT}.
GOAL: document the ACTUAL, current conventions a fresh Claude Code cloud session (zero prior context) would need to build a
new feature INDISTINGUISHABLE from existing work. Document REALITY, not aspiration — if the code contradicts CLAUDE.md,
report what the CODE does and flag the contradiction in "smells". Quote real file paths + symbols as evidence. Read the
actual files (Read/Grep/Bash). Be concrete and copyable: a rule like "cards are white with a 2px #1a1a1a border, radius
14-16px" beats "cards look clean". Return data only; edit nothing.`

phase('Read')
const READERS = [
  { key: 'app-orchestration', label: 'App.tsx orchestration', prompt: `${BASE}

YOUR AREA: App-level orchestration & navigation. Read ${ROOT}/App.tsx (783 lines), ${ROOT}/types.ts.
Document: (1) the state-based navigation model (no router) — how a "view" is represented in state and how view switching
works; (2) auth via Firebase onAuthStateChanged; (3) progress persistence — which Firestore collections/docs
(users/{uid}, progress/{uid}, etc.), when reads/writes happen; (4) how a new top-level view/tool gets wired in (the switch
/ conditional render); (5) mobile vs desktop nav (MobileBottomNav + any desktop sidebar); (6) the ModuleProgress /
UserProgress shapes. Give the exact prop/handler names a new view must accept.` },

  { key: 'registry-metadata', label: 'registry + courseData + themes', prompt: `${BASE}

YOUR AREA: module registration, metadata & theming. Read ${ROOT}/moduleRegistry.ts, ${ROOT}/courseData.ts (skim — 969
lines, focus on the record shape + categoryColorMap), ${ROOT}/moduleThemes.ts, ${ROOT}/types.ts.
Document: (1) how modules are lazy-loaded (React.lazy + default import) and registered; (2) the courseData record shape
(every field a new module needs: id, category, title, subtitle, description, sectionsCount, tags…); (3) the 7 categories +
categoryColorMap; (4) moduleThemes per-colour literal-class objects and WHY (the Tailwind JIT content-scan constraint);
(5) the exact 3-step "add a new module" sequence as the code actually requires it. Quote the ModuleTheme + SectionDefinition
+ courseData record TS shapes verbatim.` },

  { key: 'command-word-tool', label: 'Command-Word Reflex tool', prompt: `${BASE}

YOUR AREA: the Command-Word Reflex Innovation-Zone tool (the "Command Word Decoder"). Read
${ROOT}/components/CommandWordReflex/index.tsx (311 lines), ${ROOT}/commandWordData.ts (just the TYPE + accessors, not the
hundreds of data entries), ${ROOT}/hooks/useCommandWordReflex.ts.
Document: (1) the CommandWordQuestion TS type VERBATIM; (2) the tappability rule + the exact norm()/token-run algorithm
(quote it); (3) the QUESTION DISPLAY pattern — how a stem renders with the tappable command word, the demand/trap reveal,
the figure block + SEC attribution; (4) the subject picker incl. the cycle grouping (cycleForSubject, junior-cycle vs
leaving-cert), level filter (higher/ordinary/common); (5) which visual register this tool uses — the header treatment
(is there a "ToolHeader"-style band?) and the card treatment ("SectionCard"-style). Name the components/primitives it uses.` },

  { key: 'catch-up-tool', label: 'Catch-Up Lane tool', prompt: `${BASE}

YOUR AREA: the Catch-Up Lane Innovation-Zone tool. Read ${ROOT}/components/CatchUpLane/index.tsx (512 lines),
${ROOT}/catchUpLaneData.ts (just the RecoveryCard TYPE + accessors, not the data entries), ${ROOT}/hooks/useCatchUpLane.ts.
Document: (1) the RecoveryCard TS type VERBATIM; (2) the card display pipeline — gist / oneMove / the self-check
(prompt → modelAnswer → needed award points) and how the figure + passage render; (3) the subject + topic picker, the
cycle grouping, the level filter; (4) the visual register (header band? card style?) and which shared primitives it uses;
(5) how it differs structurally from Command-Word Reflex (so the two tools' shared vs divergent patterns are clear).` },

  { key: 'subject-modules', label: 'subject modules + ModuleLayout/Shared', prompt: `${BASE}

YOUR AREA: educational modules. Read ${ROOT}/components/ModuleLayout.tsx, ${ROOT}/components/ModuleShared.tsx, and
${ROOT}/components/SubjectModule.tsx (the shared per-subject module). Skim ONE concrete *Module.tsx for a real usage
example (pick a small one).
Document: (1) the ModuleProps interface VERBATIM (onBack, progress, onProgressUpdate); (2) the SectionDefinition shape and
the progressive-unlock model (unlockedSection); (3) the ModuleShared primitives a module must reuse (Highlight,
ReadingSection, MicroCommitment, ActivityRing, ConceptCardGrid…) — name each + its purpose; (4) the default-export rule;
(5) how a module pulls its theme. This is the "SectionCard / module" visual register — describe its card system.` },

  { key: 'gamification-firestore', label: 'gamification + Firestore hooks', prompt: `${BASE}

YOUR AREA: gamification + Firestore persistence patterns. Read ${ROOT}/hooks/useGamification.ts, ${ROOT}/hooks/usePoints.ts,
${ROOT}/hooks/useStreak.ts, ${ROOT}/hooks/useFreshProgress.ts, ${ROOT}/hooks/useModuleResponses.ts (skim others in hooks/
as needed). Also ${ROOT}/firebase.ts for the client setup.
Document: (1) the Firestore READ/WRITE conventions — getDoc/setDoc/updateDoc, which collection per concern, merge vs
overwrite; (2) the getDoc-on-mount pattern (useFreshProgress) and WHY it exists (the progress-hook staleness bug where a
tool seeds from a stale app-start snapshot); (3) localStorage vs Firestore split — what lives where; (4) the points / streak
/ quest hook API shapes a new gamified feature should follow; (5) the security-rule gotcha (request.resource.data only on
writes). Quote real function signatures.` },

  { key: 'design-system', label: 'design tokens + aesthetic registers', prompt: `${BASE}

YOUR AREA: the design system + the THREE aesthetic registers. Read ${ROOT}/design/tokens.ts and the "Visual Design System"
+ "Aesthetic register" sections of ${ROOT}/CLAUDE.md. Then SAMPLE one real component per register to confirm it is real,
not just documented: a Headspace/bold-colour-environment screen, a Mercury (data-dense/lavender) screen, and a
Brilliant.org (mistake-first/instrument-panel) screen — grep components/ for the named exemplars and open one of each.
Document: (1) the colour tokens VERBATIM (accent #F26B1F, success #3A8D5F, ink #1a1a1a, the tints) + the accent-vs-success
rule; (2) fonts (Source Serif 4 / DM Sans) + sizes; (3) the BANNED list (coloured left borders — confirm via the
no-left-borders rule; saturated extra colours; gradients on cards; dark module backgrounds); (4) the Tailwind class-LITERAL
constraint (no constructed bg-\${x}-500); (5) the THREE aesthetic registers each with a NAMED real exemplar component +
when to use it. Flag any place the CODE diverges from CLAUDE.md's claims (e.g. cream surfaces the memory bans).` },
]

const findings = await parallel(READERS.map((r) => () =>
  agent(r.prompt, { label: `read:${r.key}`, phase: 'Read', schema: FINDING_SCHEMA })
))
const got = findings.filter(Boolean)
log(`Read ${got.length}/${READERS.length} subsystems`)

phase('Synthesise')
const SYNTH_SCHEMA = {
  type: 'object', required: ['outline', 'inconsistencies', 'goldenExamples'],
  properties: {
    outline: { type: 'array', description: 'the proposed CONVENTIONS.md, section by section (8 sections per the brief). Each: section title + the bullet points it will contain (drawn from the findings).',
      items: { type: 'object', required: ['section', 'bullets'], properties: { section: { type: 'string' }, bullets: { type: 'array', items: { type: 'string' } } } } },
    inconsistencies: { type: 'array', description: 'cross-file contradictions for the Known-inconsistencies section — each names BOTH sides and does NOT pick a winner',
      items: { type: 'string' } },
    goldenExamples: { type: 'array', description: 'the golden-examples table rows: a task → the file to copy',
      items: { type: 'object', required: ['task', 'copyThis'], properties: { task: { type: 'string' }, copyThis: { type: 'string' } } } },
    estimatedLines: { type: 'integer', description: 'rough line count of the doc if written at the planned depth (target < 400)' },
  },
}

const synth = await agent(
  `You synthesise an audit of the Nextstepuni codebase into a PLAN for CONVENTIONS.md (a conventions layer letting a fresh
zero-context Claude Code cloud session build features indistinguishable from existing work). Here are the 7 subsystem
findings:\n${JSON.stringify(got, null, 2)}\n\n
The doc MUST have these 8 sections (per the user's brief): (1) Component architecture; (2) The two visual registers —
ToolHeader vs SectionCard; (3) The three aesthetic registers (Headspace / Mercury-Linear / Brilliant.org) with named
exemplars; (4) Question display patterns for Command-Word Reflex + Catch-Up Lane incl. TS schemas/pipelines; (5) Design
system — colour tokens, fonts, no-coloured-left-borders, Tailwind class-literal constraint; (6) Firestore patterns;
(7) Verification = npm run build (+ note the real gate is typecheck/test); (8) Golden examples table.
PRODUCE: (a) the section-by-section outline with the concrete bullets each will hold (grounded in the findings — cite real
files/types); (b) the Known-inconsistencies list — every cross-file contradiction the readers surfaced (incl. CLAUDE.md
saying "Command Word Decoder" lives in the removed ExamStrategiser vs the live CommandWordReflex tool; any cream-surface or
Tailwind-CDN staleness; ToolHeader vs SectionCard naming if the names aren't literal in code) — name BOTH sides, pick no
winner; (c) the golden-examples table rows. Keep it tight — the final doc must be < ~400 lines. Return data only.`,
  { label: 'synthesise', phase: 'Synthesise', schema: SYNTH_SCHEMA },
)

return { findings: got, synth }
