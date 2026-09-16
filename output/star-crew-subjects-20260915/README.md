# Star Crew — Leaving Cert subject collection

Open [the subject gallery](http://localhost:3047/output/star-crew-subjects-20260915/index.html).

43 avatars: 42 subject characters plus LCVP / Life, Community and Work. Every subject has its own artwork created with OpenAI built-in image generation, using the approved Star Crew family as the style reference. Music has a new guitar-playing character, **The Performer**. **The Musician** remains in the original account-setup eight.

## Files

- `index.html`, `gallery.css`, `gallery.js`: searchable gallery, subject groups, dark surface preview, larger circular previews, keyboard navigation and PNG downloads.
- `[subject-id].png`: original full-resolution generated artwork, saved in this folder.
- `prompts.json`: the common prompt and the exact direction used for every generated subject.
- `gallery.json`: subject IDs, labels, character names, files and measured framing.
- `catalogue.json`: subject metadata resolved from the app's `curriculumRegistry.ts` for the 2026–2028 cohorts, retaining canonical subject IDs.
- `build-gallery.py`: measures visible ink and rebuilds the gallery manifest; it does not alter image pixels.
- `artwork-overrides.json`: the active revised images and character names; earlier files remain available for comparison.
- `revision-prompts-20260915.json`: exact prompts and saved sources for the feedback revisions.
- `new-directions-prompts-20260915.json`: exact prompts and saved sources for the new Greek, DCG and Religious Education directions; Music and Irish retain their approved artwork.

## Feedback revisions

[View the five updated avatars](http://localhost:3047/output/star-crew-subjects-20260915/index.html?revisions=1).

- Ancient Greek: **The Storyteller**, with an orange laurel, expressive reciting gesture and curled parchment bearing lowercase **α β γ**.
- DCG: **The Drafter**, kneeling on the star and drawing an arc with an oversized compass.
- Irish: a traditional harp replaces the book; the **Dia duit** greeting remains.
- Music: a new acoustic-guitar performer, separate from the account-setup avatars.
- Religious Education: **The Candle Keeper**, a quiet candlelit pose with a small closed book beside the character.
- Latin: **ABC** is the correct start of the Latin alphabet, so its artwork is retained.

Lettering references: [Open University — Greek alphabet](https://www.open.edu/openlearn/mod/oucontent/view.php?id=157789&section=_unit2.1), [Cambridge University Press — Latin alphabet](https://www.cambridge.org/core/books/abs/latin-language/alphabet/93B5C00C90A4C527F41EFFA31774F229).

## Framing

Every circle centres the visible illustration rather than the white image canvas. The longest dimension occupies up to 78% of the bubble, with at least 5% clearance between ink and the circular rim. CSS uses the same measurements for the gallery and 32, 48 and 64 pixel previews.

## Subject coverage

The set covers the app's Leaving Certificate Established subject catalogue, plus LCVP, and adds the two new subjects confirmed on Curriculum Online. It is an artwork collection, not a new curriculum or assessment taxonomy. Names are shortened for the gallery; canonical IDs are retained. DCG / Applied Graphics and Design and Physics and Chemistry / Chemical and Physical Science share their respective subject characters across naming transitions.

Sources:

- [Curriculum Online — Senior Cycle subjects](https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/)
- [Climate Action and Sustainable Development](https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/climate-action-and-sustainable-development/)
- [Drama, Film and Theatre Studies](https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/drama-film-and-theatre-studies/)

The original eight remain available at `../star-crew-20260915/index.html`. This is a local artwork gallery; production app avatars have not been changed.
