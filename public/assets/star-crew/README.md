# Star Crew — approved 15 September 2026

The app uses eight personal avatars and 43 subject illustrations. PNGs are the
approved originals; CSS framing centres visible ink within a white circular
bubble without modifying the artwork. Only visible images are lazy-loaded;
the whole collection is not part of the service-worker precache.

- Personal IDs and framing: `data/personalStarCrew.ts`.
- Subject IDs, label aliases and framing: `data/subjectStarCrew.ts`.
- Renderer: `components/StarCrewArtwork.tsx`.
- `original-four.png` is a 2×2 source sheet. Only its Beanie and Reader tiles are
  selectable. The other six choices use individual files.
- Personal `12-musician.png` was previously called The Wave. Subject Music
  uses the separately approved guitarist, `music-v2.png`.
- Active revisions: Ancient Greek v4, DCG v3, Irish v3, Music v2 and Religious
  Education v3. Other subjects use their approved first-direction PNGs.

Existing saved DiceBear seeds and purchased avatars remain supported. New
profile choices store stable `star-crew:*` IDs; no saved-account migration is
required. Unknown subject names render initials instead of unrelated artwork.

Grade-goal screens retain their existing implementation and styling.
