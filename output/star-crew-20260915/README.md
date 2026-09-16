# Star Crew — the final eight

Open http://localhost:3047/output/star-crew-20260915/index.html while the local Vite server is running.

The collection retains the four approved originals and adds eight separately generated characters using OpenAI built-in image generation. Full prompts and saved source paths are recorded in `prompts.json`.

Chosen set: **01 Beanie, 02 Reader, 05 Skater, 07 Maker, 08 Stargazer, 09 Hugger, 11 Snoozer, 12 Musician.**

Tap an illustration to preview circular avatars at 32, 48, 64 and 150 pixels. The light/dark control applies to all eight cards.

`framing.js` centres the visible ink bounds of each illustration, instead of its original canvas. The longest dimension occupies 78% of the circle, with at least 5% clearance from the circular rim. `framing.json` records the measurements and selected IDs. Rendering uses CSS positioning; original PNG pixels are unchanged.

`options.html` preserves the full set of twelve with the same framing corrections, and defaults to the chosen eight. It retains the selection and copy controls.

This folder is the approved artwork preview. Production avatars have not been changed.
