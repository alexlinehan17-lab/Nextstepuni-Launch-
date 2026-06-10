export const meta = {
  name: 'conventions-verify',
  description: 'Independent skeptics fact-check the falsifiable claims in CONVENTIONS.md against the real code; default to REFUTE',
  phases: [
    { title: 'Verify', detail: 'one skeptic per claim, reads the cited code, confirms/refutes' },
    { title: 'Critic', detail: 'anything the per-claim checks missed' },
  ],
}

const ROOT = '/Users/alexlinehan/Nextstepuni-Launch-'

const VERDICT = {
  type: 'object', required: ['claim', 'verdict', 'evidence'],
  properties: {
    claim: { type: 'string' },
    verdict: { type: 'string', enum: ['confirmed', 'refuted', 'partly-wrong'] },
    evidence: { type: 'string', description: 'the exact file:line / quoted code that confirms or refutes' },
    correction: { type: 'string', description: 'if refuted/partly-wrong, the precise correction to apply to CONVENTIONS.md' },
  },
}

const BASE = `You are an INDEPENDENT SKEPTIC fact-checking ONE claim from CONVENTIONS.md (a new conventions doc for the
Nextstepuni codebase at ${ROOT}) against the ACTUAL code. Read the real file(s) named in the claim (Read/Grep/Bash).
Default to REFUTE if the code does not clearly support the claim — a wrong line number, a misquoted literal, a paraphrase
that changes meaning, or an outright false statement all count as refuted/partly-wrong. Only 'confirmed' if the code
matches. Quote the exact code you checked. If wrong, give the precise correction.`

phase('Verify')
const CLAIMS = [
  `The shared IZ "cardShell" literal in CONVENTIONS.md §2/§4 is verbatim: "w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7". Check it against the actual cardShell const in components/CatchUpLane/index.tsx AND components/CommandWordReflex/index.tsx — is the string really that, and is it really shared (same in both)?`,
  `CONVENTIONS.md §4 says CommandWordReflex detects the cue by: split the stem with q.stem.split(/(\\s+)/) (whitespace preserved); const norm = (s) => s.replace(/[^a-zA-Z]/g,'').toLowerCase(); and a sliding window of the command word's tokens to support multi-word cues. Verify each piece against components/CommandWordReflex/index.tsx.`,
  `CONVENTIONS.md §4 says cycleForSubject(id) returns 'junior-cycle' for jc--prefixed ids else 'leaving-cert', and the picker splits into "Junior Cycle"/"Leaving Certificate" groups ONLY when both cycles have content else a flat list. Verify against the cycleForSubject helper + the picker code in commandWordData.ts/catchUpLaneData.ts and components/CommandWordReflex + CatchUpLane.`,
  `CONVENTIONS.md §4 says the level filter predicate is exactly q.level==='common' || q.level===levelFilter (so 'common' shows at both levels), in BOTH tools. Verify in both component files.`,
  `CONVENTIONS.md §4 reproduces the CommandWordQuestion and RecoveryCard TS interfaces. Verify field-for-field against types/commandWord.ts and types/catchUpLane.ts — flag any field missing, renamed, or wrong (esp. figure?, passage?, oneMove, check.needed, marksWeight vs marks).`,
  `CONVENTIONS.md §5 lists COLORS tokens with these hexes: accent #F26B1F, accentDark #B54D14, accentTint #FDEEDF, accentDarkText #8C3A0E, success #3A8D5F, successTint #E8F2EC, successDarkText #1F5F3E, cream #FDF8F0, creamSubtle #F9F9F7, ink #1A1A1A. Verify every hex against design/tokens.ts.`,
  `CONVENTIONS.md §1 says adding a VIEW means touching FIVE sites in contexts/NavigationContext.tsx (ViewState union ~:12-16, VALID_VIEWS ~:65-70, NavigationAction+reducer case ~:107-145, navigateToX ~:273-340) plus a render branch in components/AppRouter.tsx (~:297-644). Verify these sites exist and the line ranges are roughly right (±a few lines ok; badly wrong = refute).`,
  `CONVENTIONS.md §1 states AppRouter's precedence: reset-password params → !userResolved spinner → !user LoginPage → needsPasswordChange → isAdmin → role==='gc' GCDashboard → needsOnboarding Onboarding → per-viewState if-chain → FallbackRedirect to tree. Verify the order against components/AppRouter.tsx.`,
  `CONVENTIONS.md §6 says ModuleProgress is stored FLAT at the progress/{uid} root keyed by moduleId (not under a 'progress' field), and the discriminant is typeof val==='object' && 'unlockedSection' in val, used by ProgressContext. Verify against contexts/ProgressContext.tsx.`,
  `CONVENTIONS.md §6 says all writes use setDoc(ref, partial, {merge:true}); points awarded via pointsData:{ totalEarned: increment(n) }; the staleness fix is useFreshProgress (getDoc-on-mount) with a seededRef gate; golden template hooks/useHowTheyDidIt.ts. Verify against hooks/useFreshProgress.ts, hooks/useHowTheyDidIt.ts, and a points-awarding path.`,
  `CONVENTIONS.md §2 claims components/ToolHeader.tsx and components/SectionCard.tsx are real files with the stated props, AND that the content tools CommandWordReflex + CatchUpLane import NEITHER (no ToolHeader band inside a tool body). Verify the files + their props + grep both tools for ToolHeader/SectionCard imports.`,
  `CONVENTIONS.md §3 names live exemplars: Headspace → components/journey/PeerIslandsList.tsx (+ immersiveDeck/colorWorlds.ts WORLDS palette), Mercury → components/CAOPointsSimulator.tsx, Brilliant → components/ExamCrisisManagementModule.tsx. Open each and confirm it actually exhibits the described register (saturated-bg cards / data-dense neutral / mistake-first bold-border).`,
  `CONVENTIONS.md §1 says provider nesting in index.tsx is ErrorBoundary > ToastProvider > AuthProvider > ProgressProvider > NavigationProvider > MotionConfig > PullToRefresh > App, and that ProgressContext+NavigationContext consume AuthContext. Verify against index.tsx.`,
  `CONVENTIONS.md §5 says moduleThemes.ts can construct theme class strings dynamically ONLY because tailwind.config.ts exhaustively safelists every emitted shade. Verify there is a real safelist in tailwind.config.ts covering moduleThemes' shades.`,
  `CONVENTIONS.md §6 security-rule claims: request.resource.data exists only on writes; pointsData.totalEarned increases by ≤ +1000/write; unlockedAchievements is append-only. Verify against firestore.rules.`,
  `CONVENTIONS.md §1 says per-subject modules are registered via createSubjectModule('<subjectKey>') in moduleRegistry.ts sharing components/SubjectModule.tsx (don't hand-write a file), and the registry key === the courseData id. Verify against moduleRegistry.ts + courseData.ts.`,
]

const verdicts = await parallel(CLAIMS.map((c, i) =>
  () => agent(`${BASE}\n\nCLAIM #${i + 1}:\n${c}`, { label: `verify:${i + 1}`, phase: 'Verify', schema: VERDICT })
))
const got = verdicts.filter(Boolean)
const bad = got.filter((v) => v.verdict !== 'confirmed')
log(`Verified ${got.length}/${CLAIMS.length} — ${got.filter((v) => v.verdict === 'confirmed').length} confirmed, ${bad.length} need correction`)

phase('Critic')
const critic = await agent(
  `You are a completeness critic for a verification of CONVENTIONS.md (at ${ROOT}/CONVENTIONS.md) against the Nextstepuni
code. The per-claim skeptic results:\n${JSON.stringify(got, null, 2)}\n\n
Read CONVENTIONS.md yourself. (1) Is any claim the skeptics marked 'confirmed' actually wrong on a closer read? (2) Are
there OTHER falsifiable claims in the doc nobody checked that look risky (wrong file path, wrong literal, a "verbatim"
that isn't)? Spot-check 3-4 of them against the code. (3) Give a final list of EVERY correction to apply to CONVENTIONS.md
before it ships, each as: location in the doc → what's wrong → the fix. If the doc is accurate, say SHIP.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, corrections: bad, critic }
