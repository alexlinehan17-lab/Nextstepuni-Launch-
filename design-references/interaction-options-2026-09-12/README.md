# Nextstepuni — topic and motion options

Open http://127.0.0.1:3045/ while the local review server is running.

To restart:

    python3 -m http.server 3045 --bind 127.0.0.1 --directory /Users/alexlinehan/Documents/Nextstepuni-Interaction-Options-20260912

These are review concepts, not deployed application changes.

- T01: The contents page — editorial rows with distinct question/year counts and expandable years. Recommended.
- T02: The year map — common desktop year axis; mobile year calendar for one topic.
- T03: The topic desk — topic index and detail pane; compact topic selector on mobile.
- R01: The paper lift — quiet fade and small upward movement.
- R02: The rising window — clean bottom-to-top reveal. Recommended.
- R03: The opening spread — the portal opens from the centre.
- R04: The drawn frame — an orange outline draws, then the portal arrives.

The motion preview includes a full-page scroll test, replay, progress scrubbing, a reduced-motion option and a comparison against the original ink-blot mask. Shortlist choices are local to this board. The Copy button prepares text to paste into the chat; it does not publish or send anything.

Data: the app's `components/PaperTrail/topics.ts`, `topicsForSubject`, `topicYearSets`, `strandsFor`, and `questionsForTopics`, exported on 12 September 2026. The displayed group is Biology Higher Level, New Course, Strand 1: Organisation of Life. Historical questions are grouped under these topic labels. Counts are distinct tagged questions and distinct tagged exam years. A topic with zero tagged questions is retained.

Assets: original Nextstepuni artwork, Source Serif 4, Apercu Mono, supplied screenshots and the current ink-blot mask.

## Chosen, and changed — 12 September 2026

**T03 The topic desk** and **R03 The opening spread** are the picks. Two notes
from that review, both acted on here.

**"It's very italiccy, doesn't feel very nextstepuni."** It was not italic — it
was Times. The board declares `@font-face { font-family: Serif }`, and `Serif`
is the CSS *generic* keyword, so every `font: … Serif, Georgia, serif` resolved
to the browser's default serif and the Source Serif 4 file was never requested.
`document.fonts` listed only Mono. A custom family cannot be named after a
generic (`serif`, `sans-serif`, `monospace`, `cursive`, `fantasy`, `system-ui`,
`math`). Renamed to `"Nextstep Serif"` in all three stylesheets — 13 of the uses
were inside the `font:` shorthand rather than `font-family:`, which is why the
first pass only fixed half of them. Every heading, topic name and count on the
board and in both previews now renders in the real face.

**"The orange line in the middle that briefly appears doesn't work."** Gone. It
was a 1px `#f76818` rule down the centre, and orange is the brand's accent being
spent on a transient artefact in the middle of the screen, where it reads as an
error rather than as an opening. `.edge` is now the gutter shadow two pages make
as they part: ink at low alpha, 40px wide, widest at the start and gone by the
time the spread is open. No colour, and the sense of an opening survives.

### The year row — ink chips, orange marker

The desk's year strip was fifteen-plus solid `#ff6b1b` fills in a row: the accent
doing a job a hairline could do, and so much of it that the genuinely orange thing
on the page (the question count) stopped reading as the accent at all. The number
also sat as ink-on-orange, which is a weak contrast for 11px mono.

Now the chip is white with ink type and a 24px orange rule under the year — the
mark, not the fill, carries "asked". Tagged and untagged are still separable at a
glance because the encoding is doubled: ink type *and* a marker versus grey type
and nothing. Applied to the base `.year-cell`, so the contents direction inherits
it and the board speaks one language; the matrix keeps its solid fills, which are
correct for a dense heat-grid. Footnote copy updated to describe what the page
actually does.

Backups: `/tmp/preview.css.bak2`, `/tmp/preview.html.bak`.

## The reveal changed — R02, not R03

The pair is now **T03 · The topic desk** and **R02 · The rising window** (the
board's own shortlist reads this, set in `nsu-direction-shortlist`).

That makes the `.edge` gutter-shadow work above moot for the chosen direction —
`.edge` is only drawn by `spread`. It stays as an improvement to R03 on the board;
it does nothing for the pick.

### The rising window carried its content the wrong way

Reviewed with the same eye and found a defect of the same class as the orange
line. `inset((1-p)*100% 0 0 0)` grew the window upward over a card that never
moved, so the reveal delivered the card **bottom-up**: at 22% the viewer met
"Or choose a topic" and a horizontally sliced "Start a practice session"; the
masthead and the headline arrived last. A chapter opening was reading in reverse,
and the leading edge sliced a line of type through its x-height, which reads as a
rendering fault rather than as a reveal.

Fixed by letting the content rise with the window: the children are wrapped in
`.portal-inner`, which is translated down by `(1-p)*100%` against the same clip.
The window's top edge and the card's top edge now travel together, so the frame
still grows upward — the name still describes it — but the masthead is first out
and the CTA last, in reading order. The cut now falls at the **bottom** of the
visible band, where an incomplete edge reads as "more still arriving".

Verified at 22% and 55% on the slider and down the full scroll study, and all four
other reveals confirmed untouched (`inner` resets to `none` for each).

Backups: `/tmp/motion.html.bak`, `/tmp/motion.js.bak2`, `/tmp/motion.css.bak2`.
Reverting is one line: drop the `inner.style.transform` in the `window` branch.
