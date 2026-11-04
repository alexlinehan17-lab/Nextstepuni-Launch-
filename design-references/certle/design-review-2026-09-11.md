# CERTLE: daily puzzle design review

Reviewed 11 September 2026. Scope: public desktop play flows, help/navigation and visual hierarchy. No reference site's daily puzzle was solved and no social posts were sent. Wordle's NYT page was blocked by the browser's site policy, so this review does not claim a live inspection of it.

## The problem with the old CERTLE

The daily question competed with a statistics sidebar, three repeated instructions, multiple mottos, a back link duplicating the main navigation, and tiny supporting labels. Everything was contained in the same soft card treatment. The static mascot appeared beside the logo without participating in the experience. Completion offered text sharing, but no designed image or explicit social destinations.

The six-tile CERTLE logo is already distinctive. The game mechanic also has a useful identity of its own: earn SEC scheme marks, improve an answer, keep the best attempt. Those are the anchors to preserve.

## Reference sweep

| Reference | Observed strengths | What CERTLE takes | What it leaves behind |
| --- | --- | --- | --- |
| [Puzzmo](https://www.puzzmo.com/) | Newspaper masthead, real puzzle previews, individual titles and author credits. Strong identity comes from typography and the puzzles themselves. | Put the actual question on the page immediately. Keep the exam reference as meaningful provenance. Move secondary record/help into optional dialogs. | Multiple game promotions and a portal-style layout around a single daily question. |
| [Waffle](https://wafflegame.net/) | Large tactile letter tiles; remaining swaps close to the board; compact identity and controls. The board explains the game visually. | Three visible attempt rows, physical mark tiles, restrained reveal motion and a score beside each row. | Its colours, advertising, navigation density and any implication that marks are independent guesses rather than scheme groups. |
| [LinkedIn Queens](https://www.linkedin.com/games/queens/) | Bold coloured entry screen; compact play toolbar; clear board focus; rules and hints close to the task. | One strong brand-colour question surface, precise help/record controls, an uncluttered answer workspace. | A start gate or timer that adds friction or pressure to an exam-learning task. |
| [Minute Cryptic](https://www.minutecryptic.com/) | Distinctive typographic personality, a single prominent clue, physical answer cells, optional scribble/hints and a clear check action. | Treat the question as the hero. Make the primary action unmistakable. Add character through the existing brand, not decorative stock icons. | The promotional interruption before play, multiple colours unrelated to Nextstepuni, and an onscreen letter keyboard unsuitable for full responses. |
| [Contexto](https://contexto.me/en/daily) | Immediate input, visible guess count and plain explanation of its semantic scoring. | Keep scoring understandable and close to the response. Preserve the answer so improving it is easy. | A long how-to panel occupying the play space and an opaque numeric similarity score. CERTLE shows actual scheme marks. |
| [Framed](https://framed.wtf/) | One large image establishes the task; numbered progress, input and submit are tightly grouped. The clue dominates the page. | Keep the question and response as one cohesive game sheet; no unrelated sidebar between the player and the task. | Advertising, competing challenge promotions and tiny utility type. |

Wordle's familiar daily edition, limited attempts and spoiler-free square results remain useful conventions. CERTLE must interpret them through its own free-text, partial-credit mechanic rather than imitate a five-letter keyboard game.

## Primary-source design rationale

Puzzmo's own [redesign explanation](https://blog.puzzmo.com/posts/2025/02/06/redesign/) describes freeing space for play, reducing unnecessary chrome and allowing players to collapse secondary information. Its [essay on pre-solving](https://blog.puzzmo.com/posts/2025/07/11/on-pre-solving/) explains why seeing the actual puzzle is a better invitation than hiding it behind an entry step. These support showing today's real question immediately and making record/help optional. They are rationale, not a reason to copy Puzzmo's styling.

## CERTLE direction

- Preserve the original logo's orange, charcoal and white tiles, proportions and bottom edge.
- Use a bold orange question sheet with large Source Serif 4 text, source/year/level and a clear mark tariff. A white workspace sits beside it on desktop and directly below on mobile.
- Keep the three-attempt board, answer and check action in one place. Remove repeated motivational filler. Partial feedback says what was matched and what the player can do next.
- Use the existing Starguy Rive rig and landing page floating-motion function. Desktop has a reserved outer margin; mobile reserves space beside the logo. Reduced-motion users see the still illustration. Motion never crosses inputs.
- Completion has a large best-score treatment, the final three-row board and an explicit sharing action. The full scheme remains hidden until the game is finished.
- Share a spoiler-free result as text or an actual PNG, with Facebook, LinkedIn, X, WhatsApp, email and supported native share sheets. Do not upload answers or add score data to public query parameters.
- Keep the date, next-question time and records honest. No invented player counts, rankings, streaks or claims that an automatic marker is infallible.

## Sharing behaviour and limits

[Web Share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share) depends on browser support, secure context and a user gesture. Prepare the image before the button is clicked; use `canShare` for files and keep text/copy fallbacks. Cancel is not an error.

Facebook and LinkedIn own the final post composer. The share buttons open a canonical CERTLE link; the result text is copied for the player to paste, with a selectable fallback if clipboard access fails. Their link previews use the page's static Open Graph artwork. The downloadable PNG carries the individual score. The UI must not claim that an individual score image or comment was automatically attached to those websites.

The score export contains edition, date, subject, marks and attempt rows only. It excludes the question, typed response and scheme. The production URL is used even in a local preview. Sharing does not happen until a player acts.

## Validation and the marking edge case found during review

Browser review covered desktop, 390px mobile and 320px narrow layouts; the real 15-mark image question; the longest prompt; partial credit followed by a full-mark improvement; saved statistics; keyboard dialog dismissal and focus return; copying; the generated image; and Rive rendering. Dense mobile mark rows wrap rather than shrinking into unreadable dots. No public posts were sent.

The Business 2022 OL three-image question exposed a pre-existing error: the printed part-label separator was being required as answer content. CERTLE now removes that separator for matching while retaining the original scheme text for review. Points are bound to an explicit part label, or to the student's list order, so swapping the categories does not earn full marks. This is a narrow correction; it does not replace the marker or claim exhaustive semantic understanding.

The local verification suite passed 246 tests across CERTLE, the shared marking components, the curriculum registry, Mark Bank decks and card preservation. App/test TypeScript checks, repository lint and a production build are also required before release. Social-post delivery itself depends on the user's account and platform composer; URL payloads and cancellation/failure fallbacks are tested without publishing anything.
