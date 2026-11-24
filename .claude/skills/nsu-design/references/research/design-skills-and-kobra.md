# Research: agent design skills + Kobra visual/motion reference

Retrieved 2026-11-24. Everything below was read from the fetched source unless marked UNVERIFIED.
Method: public repos shallow-cloned and read as files; sites fetched with curl (server-rendered HTML + CSS bundle parsed).
Local copies: `/tmp/claude-0/-home-user-Nextstepuni-Launch-/ecf9bd20-fb4e-53bb-9674-cf2921911154/scratchpad/dl/`

---

## 1. emilkowalski/skills

- Repo: https://github.com/emilkowalski/skills (install: `npx skills@latest add emilkowalski/skills`; skill pages at https://aiforui.dev/skills)
- 19 skills: emil-design-eng (main), animate, animate-expo, review-animations, improve-animations, find-animation-opportunities, remove-animations, choreograph, animation-performance, animation-vocabulary, apple-design, gestures, pick-ui-library, prototype, mobile-native, break-ui, learn-taste, ask-emil, ask-sonner. Plus `ui-cheatsheet.md`, `performance-cheatsheet.md`.
- Articles also fetched: https://emilkowal.ski/ui/7-practical-animation-tips , https://emilkowal.ski/ui/great-animations (consistent with the skills).

### 1.1 Decision order (animate/SKILL.md "Build Sequence")
1. Should it animate at all? 2. Purpose? 3. Cheapest tool that works. 4. Properties. 5. Easing + duration (or spring). 6. Interruption + exit. 7. Reduced motion + pointer gating (ships WITH the animation, not as follow-up).
"The gate exists to produce zero lines of code sometimes. That's a success."

### 1.2 Frequency gate (exact table)
| Frequency | Decision |
|---|---|
| 100+ times/day (keyboard shortcuts, command palette toggle) | No animation. Ever. |
| Tens of times/day (hover effects, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, feedback, celebrations) | Can add delight |

- Never animate keyboard-initiated actions.
- Valid purposes only: spatial consistency, state indication, explanation, feedback, preventing jarring change. "It looks cool" on a frequently seen element is not valid.

### 1.3 Easing
- Entering or exiting -> ease-out. Moving/morphing on screen -> ease-in-out. Hover/colour -> `ease`. Constant motion (marquee, progress) -> linear. Default -> ease-out.
- Never `ease-in` on UI.
- Built-in CSS easings are "too weak"; use:
  - `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` (strong ease-out for UI)
  - `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)` (on-screen movement)
  - `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)` (iOS-like sheet curve, from Ionic; Vaul uses it over 500ms)
  - small floating drawer override: `0.2s cubic-bezier(0.165, 0.84, 0.44, 1)`
- Hard rule: "No approximated values... Never invent `cubic-bezier(0.4, 0, 0.2, 1)` because it looks familiar." Extend existing tokens, never fork a parallel system.

### 1.4 Durations
| Element | Duration |
|---|---|
| Button press feedback | 100-160ms |
| Tooltips, small popovers | 125-200ms |
| Dropdowns, selects | 150-250ms |
| Modals, drawers | 200-500ms |
| Marketing/explanatory | can be longer |

- UI animations stay under 300ms; modals, drawers, sheets, toasts are the documented exceptions (toast = Sonner's 400ms `ease`; sheet = 500ms drawer curve).
- Exit faster than enter (e.g. enter 250ms, exit 200ms). Exits are "simultaneous, shorter and simpler"; never reverse-stagger on close.
- Exit the way it entered (same direction).
- Asymmetric timing: slow where the user is deciding (hold-to-confirm 2s linear), fast where the system responds (release 200ms ease-out).
- Spinners/skeleton shimmer on operations that resolve in <300ms should be removed ("the flash reads as a glitch").

### 1.5 Recipes (animate/RECIPES.md, exact values)
- Button press: `transition: transform 160ms var(--ease-out)`; `:active { transform: scale(0.97) }` (range 0.95-0.98).
- Dropdown/popover/menu: opacity + transform 200ms ease-out, from `scale(0.95)` + `opacity:0`, `transform-origin: var(--transform-origin)` (from trigger).
- Tooltip: 125ms, from `scale(0.97)`; first tooltip delayed, subsequent ones in the group instant (`transition-duration: 0ms`).
- Modal: 250ms, from `scale(0.96)`, origin stays centre (modals are exempt from origin-awareness); animate backdrop opacity with it.
- Sheet: `transform 500ms cubic-bezier(0.32,0.72,0,1)`; hide with `translateY(100%)` (percent = own size).
- Toast: `opacity/transform 400ms ease` via `@starting-style` (transition, not keyframes).
- Accordion: height + opacity 200ms ease-out (height tolerated only here).
- Stagger: `translateY(8px)` + fade, 300ms, delays 0/50/90/120ms (non-uniform).
- Tab indicator: clip-path 250ms ease-in-out (duplicate list + clip the active copy).
- Scroll reveal: clip-path 600ms ease-in-out, fire once (`once: true, margin: "-100px"`).
- Crossfade that looks wrong: add `filter: blur(2px)` + `opacity: 0.7` for 200ms. Keep blur under 20px.

### 1.6 Physicality
- Never `scale(0)`; start from `scale(0.9-0.97)` + opacity 0.
- Popovers scale from their trigger; modals stay centred.
- Use transitions (interruptible, retarget from current value) for anything rapidly triggered; keyframes restart from zero.
- `transition: all` is banned; list properties.
- Only `transform` and `opacity` (clip-path is the sanctioned extra; height only for accordions).
- Gate hover behind `@media (hover: hover) and (pointer: fine)`.
- Reduced motion = fewer and gentler, not zero: keep opacity/colour, drop movement. For choreography: drop delays and movement, group appears together.

### 1.7 Springs
- Apple-style config (recommended): `{ type: "spring", duration: 0.5, bounce: 0.2 }`. Physics: `{ mass: 1, stiffness: 100, damping: 10 }`.
- Bounce 0.1-0.3 and only when a gesture carried momentum (drag release, flick). Same element closed by a button gets zero bounce.
- apple-design: default UI spring = critically damped (damping ratio 1.0, response 0.3-0.4); momentum spring = damping ~0.8. Web house style: `bounce: 0` everywhere by default.
- Smaller elements need more bounce to read the same.
- Velocity dismissal: dismiss if `|distance|/elapsedMs > ~0.11` even under the distance threshold.
- Momentum projection: `current + (v/1000)*d/(1-d)`, d ~ 0.998; snap to point nearest projected endpoint.
- Rubber-band at boundaries (progressive resistance), never a hard stop. Pointer capture on drag; ignore extra touch points.
- Tap: highlight on touch-down, commit on touch-up; ~10px hysteresis before a drag commits to a direction.

### 1.8 Choreography (choreograph/SKILL.md)
- One entrance per container: never animate a parent in AND stagger its children.
- Never stagger on high-frequency / keyboard-triggered UI (menus, tab content, list rows).
- Uniform stagger is forbidden; vary by importance.
- Product UI: 30-80ms between items, total under ~300ms; long lists stagger only the first handful.
- Marketing/first-run: 100-150ms steps on 0.5-0.6s entrances allowed.
- Example timeline: Title lead 0ms/600ms fade + 12px rise; subtitle 80ms/500ms + 8px; CTAs 140ms/500ms + 6px.
- Sub-animations of one component share one timing family.
- Scale duration by distance: `clamp(0.15s, deltaHeight/500, 0.27s)`.
- Direction follows mental model: forward = content enters from right; back = from left.
- Attention loops: first run after ~2.5s, repeat every ~6s, stop during interaction.
- Accents (sparkles) land in the last ~20% of the lead's timeline, ~40ms apart.
- Test: "imagine the 50th use of the day. If you'd skip it, cut it."

### 1.9 remove-animations reductions
- Hover with scale/lift/shadow growth -> colour/opacity only, <=150ms.
- Slide/scale entrance on a frequent surface -> opacity only, 150ms.
- Stagger >80ms per item or >300ms total -> cap at 30ms per item or drop.
- Hazard: deleting an animation but leaving its `opacity: 0` start state leaves the element invisible.

### 1.10 UI + performance cheatsheets (non-motion)
- Timestamps: switch to absolute date after a week. Changing numbers: `tabular-nums`. Large headings: tracking `-0.02em`. Body: `max-width: 65ch`. Avatar: `flex-shrink: 0`. Pluralise with `Intl.PluralRules`. Eased gradients (extra stops).
- Animated blur under 20px. Don't drive child transforms through a CSS variable on the parent. Write to `ref.current.style`, not React state, per frame. `will-change` only after you see a problem. Motion `x`/`y` shorthands only hardware-accelerated from motion 14.2 (repo's claim; UNVERIFIED against Motion's changelog).
- apple-design typography: tracking is size-specific (display negative, body ~0); leading inverse to size (display `line-height: 1.05`, body 1.5); hierarchy from weight+size+leading as a set; spacing in rem so text scaling doesn't break layout.

### 1.11 mobile-native (directly relevant to a Capacitor app)
Baseline to ship before the first component:
- `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">`
- `html { -webkit-tap-highlight-color: transparent; -webkit-text-size-adjust: 100%; overscroll-behavior: none }`
- `input, textarea, select { font-size: 16px }` (iOS zooms below 16px). Never `user-scalable=no` / `maximum-scale=1`.
- `button, a, [role=button] { touch-action: manipulation }`; controls get `user-select: none` + `-webkit-touch-callout: none` (never on body).
- `100dvh` for app shell, `100svh` for hero, never `100vh` for bottom-pinned UI.
- `env(safe-area-inset-*)` on fixed header / tab bar / sheets / toasts (needs `viewport-fit=cover`).
- Inner scrollers: `overscroll-behavior: contain`.
- Press feedback on `:active`/`pointerdown`, 100-160ms ease-out, `scale(0.97)`; never on click only.
- Carousels: `touch-action: pan-y`, or native `scroll-snap-type: x mandatory`.
- `theme-color` per colour scheme.
- Hit targets >= 44x44px; enlarge with invisible `::before`.
- Set keyboards: `inputmode`, `enterkeyhint`, `autocapitalize="none"` on codes.
- Test on real hardware; device emulation reproduces none of this.

### 1.12 Haptics (animate-expo; maps onto Capacitor Haptics conceptually)
- Selection tick for detents/pickers; light impact for snap/commit; medium for heavy landing or destructive; notification success/error for outcomes.
- Fire on the same frame as the visual, at the causal moment. One per commit, never per frame, never the only feedback.

### 1.13 break-ui worst-case data
Test with: long hyphenated names with diacritics, 1-2 letter names, CJK, RTL, emoji-first names, missing name; long emails/URLs; German compounds (`Benachrichtigungseinstellungen`), ~30% longer translations; counts 0 / 1 / 1284 / 1000000; `0.1+0.2`; empty title; 2,000-char paste.

---

## 2. kobra.systems

- URL: https://kobra.systems/ (server-rendered; fully retrievable). Author: Harsh Singh. Tagline (og:image alt): "Polished components for teams building exceptional products and experiences."
- What it is: a paid shadcn-compatible React component gallery (Tailwind v4 + Base UI + `motion/react`), 100+ components, "Motion tuned per component", "Interface sound design", RTL support. Pricing page: https://kobra.systems/pricing . Component pages: `https://kobra.systems/components/<slug>` (90 fetched).
- Sources parsed: home HTML, `/assets/app-D5EwLcYl.css` (554 KB), all component page meta descriptions, button page markup.
- NOT observed: the rendered pixels. Everything below is from markup/CSS/source text, not from watching the site.

### 2.1 Colour
- Fully achromatic neutral system in OKLCH with zero chroma:
  - light: background `oklch(100% 0 0)`, foreground `oklch(14.5% 0 0)`, primary `oklch(20.5% 0 0)`, muted `oklch(97% 0 0)`, muted-foreground `oklch(55.6% 0 0)`, border `oklch(92.2% 0 0)`, ring `oklch(62% 0 0)`.
  - dark: background `oklch(14.5% 0 0)`, card `oklch(20.5% 0 0)`, border `oklch(100% 0 0 / .1)` (translucent white), input `/ .15`.
- Shell (the gallery chrome): `--shell #f0f0f0`, panel `#fff`, canvas `#fafafa`, line `#e6e6e6`, line-strong `#dcdcdc`, fg `#171717`, muted `#333`, subtle `#5c5c5c`, faint `#6d6d6d`. Dark: `#171717 / #1c1c1c / #191919 / #2b2b2b / #ededed`.
- Primary button is near-black (white in dark mode). No brand hue in chrome.
- Colour appears only semantically, all at one lightness: `--error oklch(50% .21 27.3)`, `--warning oklch(50% .14 70)`, `--success oklch(50% .13 152)`, `--info oklch(50% .17 255)` (dark: all at 70.4%). Badges = 12-14% alpha tint of the hue + darker text of the same hue.
- Nav sections carry a per-section hue via `--accent-hue` (e.g. 158) into `oklch(var(--accent-l) var(--accent-c) var(--accent-hue))`.
- Interactive tints are foreground alphas: `bg-foreground/[0.03]`, hover `/6`, active `/9`; borders `foreground/10` -> hover `/20`.
- Alert component description: "each with its own mark shape so meaning survives without color".

### 2.2 Typography
- Sans: "ABC Diatype" (self-hosted woff2, weights 400 and 700 only; `font-weight-medium` is mapped to 400 and semibold to 700, so the system is effectively two weights).
- Mono: "Departure Mono" (pixel-style mono) declared as `--font-mono`; code uses a separate system mono stack (`--font-code`). In the page markup mono is used only for the install command, prop names and types at `text-xs` — i.e. for code-like data, not decoration.
- Sizes: Tailwind scale; on the button page `text-base` (16px) x93, `text-sm` x38, `text-xs` x30, one `text-2xl`. Nav rows are 16px at 26px line height; section heads 14px bold.
- Casing: sentence/title case. Zero `uppercase` classes in page markup; one `text-transform: uppercase` rule in the whole CSS. One `tracking-tight` use. Tracking tokens: tight -0.025em, wide 0.025em.
- Antialiased rendering on body. `tabular-nums` cited in Progress ("tabular numbers that hold still").

### 2.3 Borders, radius, depth
- `--radius: .625rem` (10px); md = 8px, xl = 14px, 2xl = 16px, 3xl = 24px. Buttons `rounded-lg` or `rounded-full` (pill option); icon buttons plain `rounded` 4px; nested elements use `rounded-[inherit]`.
- Hairlines: 1px `border-shell-line`; separators are "a one-pixel line in a faint foreground tint". Card is described as "a ringed surface" (ring instead of heavy border).
- Depth is carried by stacked micro-shadows, not a single blur. Primary button ("t-raise") shadow = inset top highlight + 1px outline of the fill colour + six stacked drops from `0 .5px .5px` to `0 12px 12px -6px` at 5-8% black. Sliding tab face: `0 0 0 .5px #0000000a, 0 1px 2px #0000000f`.
- Hover does not move the button; it swaps to a "lifted" shadow and optional brightness filter.

### 2.4 Layout / density
- Desktop app shell is a fixed 3-column grid: `285px` nav | `minmax(360px,1fr)` stage | right rail `min(440px, 100vw - 645px)`; rows `52px` header | content | resizable source dock (240px default, 120-480). Min width 1024px, below that a stacked `min-h-dvh` layout with sticky 52px header and nav in a drawer.
- Dense: nav rows 26px, icon buttons 28px (`size-7`), search field 32px, standard button 36px (`h-9`), kbd 20px, compact menu rows 28px. Padding 28px in nav, 48px on the stage.
- 4px spacing base (`--spacing: .25rem`).
- Preview stage is a flat `#fafafa` canvas with the component centred; no cards around content.

### 2.5 Component styling
- Button: 36px, `text-sm font-medium`, `px-4`, focus ring 3px at 50% ring colour; press = `scale(0.985)` on a `::before` layer (so the label does not scale), 150ms ease-out; full-width buttons scale `0.997 x 0.985`. Disabled = 50% opacity. Variants: default, outline, secondary, ghost, destructive, link, and "push" (raised key).
- Push key: `--push-lift: 5px`, `--push-travel: 4px`, press `.11s` ease-out, release `.19s` with overshoot `cubic-bezier(.22, 1.32, .36, 1)`.
- Switch: thumb moves by `clip-path` (not translate), `.22s cubic-bezier(.23,1,.32,1)`, stretches on hover; hit area enlarged with an `::after` (-12px x, -8px y).
- Small icon buttons: `active:scale-[0.96]`, 100ms ease-out.
- Tooltips/popovers/tabs: shared element that travels between triggers instead of closing and reopening.

### 2.6 Motion language
Tokens (global):
- `--ease-out: cubic-bezier(.23, 1, .32, 1)` (used 70x) and `--ease-in-out: cubic-bezier(.77, 0, .175, 1)` — identical to Emil Kowalski's two curves.
- `--ease-exit: cubic-bezier(.4, 0, .6, 1)`; `--ease-glide: cubic-bezier(.77,0,.175,1)` at `--glide-duration: .3s`; `--ease-raise: cubic-bezier(.6,.6,0,1)` at `.2s`.
- Also frequent: `cubic-bezier(.22,1,.36,1)` (27x, most per-component eases), `cubic-bezier(.16,1,.3,1)` (12x), `cubic-bezier(.32,.72,0,1)` (7x, sheet/toast morph).
- Overshoot curves are reserved for small "pop" moments: `(.34,1.56,.64,1)` drag return, `(.34,1.96,.64,1)` like pop, `(.34,1.35,.64,1)` check fill, `(.34,3.85,.64,1)` avatar settle.
- Default transition `.15s`. Literal durations cluster at 150-300ms: .2s x14, .15s x12, .3s x6, .25s x5, .28s x5, .18s x4. Longest UI values ~.5-.55s (drag return, check draw, pill).

Per-component values (named CSS custom properties — the system tunes each component separately):
- Ring/focus: `.15s`. Tabs indicator: `.25s (.22,1,.36,1)`. Nav tooltip travel: `.18s`. Toggle: `.22s`.
- Checkbox: box `.15s`, tick draw `.35s`, uncheck `.15s` (exit faster than enter).
- Command dialog in: `.25s cubic-bezier(.16,1,.3,1)` from `scale(.96) translateY(-4px)`; nested level scale `.99`.
- Popover: flip-in `.3s` from `scale(.94)` with a perspective tilt + fade `.16s` (fade finishes before the transform).
- Calendar month change: `.22s` ease-out directional slide.
- Digit pop-in: 4px rise + 1.5px blur, `.26s`, 40ms stagger (large variant 8px / 2px / `.5s` / 70ms).
- OTP: paste sweep `.4s`, 45ms stagger; success `.34s`, 48ms stagger; bounce `.42s`, 8px lift.
- Invalid shake: 6px, overshoot 4px, segments 80ms/60ms (total ~280ms).
- Text swap / reveal: 2px blur crossfade, `.15s` / `.4s`.
- Drag: lift scale 1.05 in `.2s`; return `.5s` with overshoot; land `.18s`.
- Like: fill `.15s`, pop `.35s` (scale 1 -> .82 -> 1), particles `.6s`.
- Toast check: draw `.55s` after 80ms delay; toast morph `.3s (.32,.72,0,1)`.
- Skeleton shimmer `1.6s` linear loop; spinner bars `1.2s`; typing dots `.55s` cycle, 0.1s stagger, 4px lift.
- Streaming text: each new word fades in `.18s`; settled words never replay.
- Starting scales in use: 96%, 95%, 94%, 97%, 90% — never 0 for UI surfaces.

Character (from component descriptions + values):
- Continuity over appearance: things travel/morph rather than blink — radio dot "travels between options along an arch instead of blinking across", tooltip "can travel between triggers, its caption morphing into the new text", popover "can glide between several triggers instead of reopening", pagination highlight "slides to the current page", nav pill "slides behind items", chevron "morphs into a cross", tick "draws in when checked and un-draws when cleared", dialog "rises and scales in", sheet "drifts in".
- Fast, strongly decelerated ease-out; overshoot only on small physical moments (press release, like, drag return).
- Blur (1.5-2px) used as a crossfade aid.
- Rejection/invalid = short shake; success = sweep/draw. State has a motion signature as well as a colour.
- Reduced motion is everywhere: `prefers-reduced-motion` appears 63 times in the CSS; `motion-reduce:transition-none` on nearly every transition; descriptions say "instant under reduced motion", "holds still under reduced motion". Hover gated by `(hover:hover)` 28 times.
- Sound is a paired layer: `data-sound="tap|copy|swoosh|notification"` attributes on controls, "Synthesized cues ... with pitch jitter, slider ticks, and a saved mute and volume"; "Short, quiet and synthesized".
- Expressive set-pieces exist but are isolated to showcase components (halftone dots on springs, WebGL QR/liquid glass, particle input dissolve, gooey slider).

### 2.7 Kobra gaps
- Easing/duration values inside the JS bundles (`motion/react` spring configs) were not systematically extracted; only one was seen in page source: `DIGIT_SPRING = { type: 'spring', duration: 0.3, bounce: 0.2 }` and OTP sweep `duration 0.4, stagger 0.045`.
- `prompt.md` / "AI skills for motion, sound and migration" content was not retrieved (appears to be Pro/tab-loaded).
- Visual impressions (how it actually looks/feels in a browser) are inferred from code, not seen.

---

## 3. Other skills / guideline sets

### 3.1 Anthropic `frontend-design`
- https://github.com/anthropics/skills/tree/main/skills/frontend-design (SKILL.md read in full)
- Rules worth adopting:
  1. Ground the design in the subject matter; identify subject, audience, primary job before designing.
  2. Two-pass process: write a compact token plan (4-6 named hex colours, typefaces + roles, layout concept with ASCII wireframes, principles), review it against the brief for generic defaults, then build.
  3. One family or two; if two, clearly distinct.
  4. Line length under 80 characters; serif body gets slightly more line-height.
  5. Typographic "tells" to avoid: one accented word in a headline; all-caps labels; unnecessary eyebrow labels above content.
  6. Numbered markers (01/02/03) only when content is truly a sequence.
  7. Non-user-triggered motion sparingly: one orchestrated moment beats scattered effects; fade-and-slide-up on every section and hover transitions on every card read as generated. Motion answering a user action is welcome.
  8. "Spend your boldness in one place"; remove one accessory.
  9. Quality floor without announcing it: responsive, visible keyboard focus, reduced motion, accessible contrast.
  10. Copy: user's vocabulary, active voice, CTA says what happens ("Save changes" not "Submit"), same action name through the flow ("Publish" -> "Published"), errors say what happened and how to fix, never apologise or stay vague; empty screen is an invitation to act; sentence case.
  11. Listed AI-default clusters include: warm cream background (~#F4F1EA) + serif display + terracotta accent (~#D97757); identical rounded cards with one radius and the same soft shadow; tracked-out ALL-CAPS eyebrows; monospace for small data labels; "->" appended to buttons. The brief's own words win where it specifies one of these.
- NOTE for this project: the existing house style (serif headings, orange accent, uppercase 0.12em section labels) overlaps several of those listed defaults. It is a specified brand system, so it stands, but the skill should not add more of these on free axes.

### 3.2 Vercel Web Interface Guidelines
- https://vercel.com/design/guidelines and https://github.com/vercel-labs/web-interface-guidelines (AGENTS.md read in full; MUST/SHOULD/NEVER format is itself a good template)
- Adopt:
  1. Hit target >=24px, mobile >=44px; expand hit area if the visual is smaller.
  2. Mobile input font-size >=16px; never disable zoom; `touch-action: manipulation`.
  3. Visible `:focus-visible` rings; never `outline: none` without replacement.
  4. Loading buttons keep their label and show a spinner; keep submit enabled until the request starts.
  5. Never block paste; validate after typing, don't block typing; errors inline, focus the first error on submit.
  6. Optimistic UI with rollback or Undo; confirm destructive actions or give an Undo window.
  7. Delay first tooltip, subsequent peers instant.
  8. Animation: honour reduced motion; compositor props only; never `transition: all`; interruptible and input-driven; correct `transform-origin`.
  9. Skeletons mirror final content (no layout shift). Design empty/sparse/dense/error states. No dead ends.
  10. `tabular-nums` for comparisons; `…` character; non-breaking spaces in `10 MB`; `text-wrap: balance`.
  11. Status never colour-only.
  12. Layered shadows (ambient + direct); semi-transparent borders; nested radii concentric (child <= parent); tint borders/shadows toward the background hue.
  13. Increase contrast on hover/active/focus; prefer APCA.
  14. Flex children need `min-w-0` to truncate; resilient to short/average/very long content.
  15. Respect safe areas; `overscroll-behavior: contain` in modals/drawers; mutations target <500ms; virtualise lists >50 items.

### 3.3 Rauno Freiberg, Web Interface Guidelines
- https://interfaces.rauno.me/ (read in full)
- Adopt:
  1. Interaction animation no longer than 200ms "to feel immediate".
  2. Animation values proportional to trigger size: dialog from ~0.8 scale + fade (not 0 -> 1); button press ~0.96 (not 0.8).
  3. Frequent, low-novelty actions get no extra animation (context menu open, list add/delete, trivial hovers). macOS context menu animates out only.
  4. Theme switching must not trigger transitions.
  5. Pause looping animations when off screen.
  6. Font weight must not change on hover/selected (layout shift); no weights below 400; medium headings 500-600.
  7. `clamp()` for fluid sizes, e.g. `clamp(48px, 5vw, 72px)`.
  8. No dead areas between list items: increase padding rather than gap.
  9. Toggles take effect immediately, no confirm.
  10. Feedback relative to trigger: inline checkmark on copy, not a toast; highlight the offending input.
  11. Hover via `@media (hover: hover)`; replace the iOS tap highlight, don't just remove it; no autofocus on touch.
  12. Disabled buttons should not carry tooltips; box-shadow for focus rings.
  13. Decorative layers `pointer-events: none`; interactive inner content `user-select: none`.
  14. Empty states prompt to create an item.

### 3.4 ibelick/ui-skills
- https://github.com/ibelick/ui-skills , https://www.ui-skills.com/ (baseline-ui SKILL.md read in full; other skills: fixing-accessibility, fixing-motion-performance, fixing-metadata, improve-ui, create-design-md)
- Adopt (it is the most conservative set; useful as a default floor):
  1. Never add animation unless explicitly requested.
  2. Never exceed 200ms for interaction feedback; ease-out on entrance.
  3. Never introduce custom easing curves unless requested (conflicts with Emil; resolve by defining tokens once).
  4. Compositor props only; avoid animating background/colour except small local UI.
  5. Never animate large blur/backdrop-filter surfaces; no `will-change` outside an active animation; pause off-screen loops.
  6. `h-dvh` not `h-screen`; safe-area insets on fixed elements.
  7. `text-balance` headings, `text-pretty` body, `tabular-nums` data; don't touch letter-spacing unless asked.
  8. Fixed z-index scale; `size-*` for squares.
  9. AlertDialog for destructive actions; errors next to the action; structural skeletons.
  10. No gradients unless requested; never purple/multicolour gradients; no glow as primary affordance; one accent colour per view; empty states get one clear next action.
  11. Use accessible primitives (Base UI / React Aria / Radix); never hand-roll keyboard/focus behaviour; never mix primitive systems in one surface.

### 3.5 pbakaus/impeccable
- https://github.com/pbakaus/impeccable , https://impeccable.style/ (read: reference/craft-floor.md, ios.md, animate.md, typeset.md, layout.md; SKILL.md itself not read in full)
- Adopt:
  1. Contrast: body and placeholder >=4.5:1, large text >=3:1; on coloured surfaces tint secondary text from that hue, never grey.
  2. Spacing: tight groups, generous separation, more space above a heading than below; 4-unit base scale.
  3. Type: body measure 65-75ch (prose 45-75ch), display max 6rem, tracking floor -0.04em (-0.02 to -0.03em usually better), 16px body floor.
  4. Motion durations: 100-150ms immediate feedback; 150-300ms routine state change; 300-500ms layout/overlay/view transition; 500-800ms one authored focal entrance. Exit faster than entrance. Suggested arrival curve `cubic-bezier(0.16, 1, 0.3, 1)`. No bounce by reflex.
  5. Hover must not move the hovered element out from under the pointer: move a child (`.card:hover .card-surface { transform: translateY(-2px) }`).
  6. Declare elevation once: border OR shadow. Card radii 12-16px; pills for small controls.
  7. Check every state: hover, disabled, loading, error, empty.
  8. Theme the browser surfaces: selection, caret, scrollbars, focus rings.
  9. "Refuse" list: identical icon+heading+text card grids; nested cards; hero-metric template; eyebrow above heading; gradient text; decorative glass; monospace as costume; emoji as icons; modal for a task needing no interruption; a bar down one side of a rounded box; hard offset shadows (`4px 4px 0`) outside a truly neobrutalist system.
  10. iOS: 44x44pt targets; inside safe areas; tab bar for 2-5 sections (sections, never actions); never disable edge-swipe back; large titles collapsing on top-level screens; sheets for self-contained tasks with clear Cancel/Done; 11pt floor, body 17pt; Dynamic Type; one tint colour for interactive elements; system materials rather than hand-rolled glass; grouped/inset lists for settings; SF Symbols.
- NOTE for this project: two "Refuse" items collide with the app's documented house style — the left-border callout (3px accent bar on a rounded box) and the chunky primary CTA (`box-shadow: 0 4px 0 #B54D14`). Impeccable itself says the brief's words can earn these; the skill should state the house style wins and confine both to their documented uses.

### 3.6 Not retrieved
- Apple HIG (developer.apple.com) — page requires JavaScript; a Markdown variant is advertised but was not fetched. iOS rules above come from Emil's apple-design skill and impeccable's ios.md, not from Apple directly.
- Refactoring UI — not fetched (paid book); no rules from it are included.
- animations.dev course content — paywalled; only the landing page loaded.
- vercel.com/design/guidelines prose page — loaded, but rules were taken from the repo's AGENTS.md; not diffed against the page.

---

## 4. Points of disagreement between sources (decide once in the skill)
- Custom easing: Emil says built-ins are too weak, use the two custom curves; ibelick says never introduce custom curves unless asked. Kobra follows Emil exactly.
- Duration ceiling for feedback: Rauno and ibelick 200ms; Emil <300ms with sheet/toast exceptions; impeccable 150-300ms routine.
- Press scale: Emil 0.97 (0.95-0.98); Rauno ~0.96; Kobra 0.985 on standard buttons, 0.96 on small icon buttons.
- Dialog start scale: Rauno ~0.8; Emil 0.96 (modal) / 0.95 (popover); Kobra 0.94-0.96.
- Springs: Emil's recipe default has bounce 0.2 for drag release; his apple-design skill says bounce 0 by default, bounce only after momentum.
- Uppercase labels / mono labels: flagged as generated-look tells by Anthropic and impeccable; Kobra uses neither.
