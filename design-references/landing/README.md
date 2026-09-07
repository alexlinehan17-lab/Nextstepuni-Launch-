# Landing page references (2026-09-07)

Alex's Mobbin-style references for the marketing landing page, with what he
liked about each and what the page takes from it. The screen recordings
(44–414 MB each) are gitignored and live at `~/Desktop/Screen Recording
2026-09-07 at <time>.mov` on Alex's Mac; `sheets/` holds contact sheets of every
recording, one frame every two seconds.

| Recording | Site | What Alex liked | What the page takes |
|---|---|---|---|
| 10.01.49 | Shopify Design (design.shopify.com) | "the text popping up… sleek… cutting edge" | `WordPop`: the hero headline builds word by word behind an ink square marker (`motion.tsx`) |
| 10.03.23 | Shopify Editions Winter '26, "The Renaissance Edition" | "feels like different chapters of a book"; wants click-through demos of real app parts | `Chapters`: numbered rail (I–VI), one giant serif word per chapter, drop-cap line, frame, alternating sides |
| 10.12.34 | Leonardo.AI | "the wording collapses in a satisfying way, the coloured wording" | `CollapseWord`: the chapter word folds away as the chapter scrolls out; numbers-as-identity strip |
| 10.14.54 | Hermes Agent (Nous Research) | "the colouring, the way the boxes highlight" | One-hue discipline (paper + ink + one orange); rows flip to the orange tint on hover (`landing-hover-card`); mono numbered eyebrows |
| 10.16.57 | Brilliant | doesn't love the branding, LOVES seeing product parts in action | Scripted-cursor autoplay in the Mark Bank demo; interactive demos in every chapter; subject switcher |
| 10.39.21 | ElevenLabs | "The way I can interact with the product and see it in action is AMAZING" — the important one | `Playground`: product tabs on top, live mini-product in the middle, mode tabs along the bottom, CTA inside the frame |

## Brand inputs

- `brand-icon-star-guy.png` — the app icon: **starguy**, the website's one character (transparent source: `public/icons/onboarding/star-person.png`, tight crop at `public/assets/landing/starguy*.png`). He sits left of the wordmark in the nav (HappyStack pattern) and hangs off headline words.
- `brand-wordmark-nextstepuni.png` — the lowercase wordmark. Matched against Google Fonts in Chrome: **DM Sans 700, letter-spacing −0.03em** (already the app's sans).
- Palette sheet from Alex: Paper `#FFFFFF`, Charcoal `#1A1A1A`, Orange `#F26B1F`, Orange text `#B84A0C`. Tagline "Your study. Your way." (`components/landing/theme.ts`).

## Rules Alex set

- Translate STRUCTURE and rhythm, never colours or fonts. White is a staple; no cream. Ink hairlines. Orange sparingly.
- Real copy, no invented stats, no fake testimonials. Placeholder frames for screenshots (real captures already exist under `public/assets/guide/`; `CAPTURES` in `demoData.ts` swaps them in).
- "Keep it real, keep it human" — no slogan fragments ("Every question… Answered." was rejected as "such an AI thing to say").
- Puifín is not on the website; starguy is the only character.
