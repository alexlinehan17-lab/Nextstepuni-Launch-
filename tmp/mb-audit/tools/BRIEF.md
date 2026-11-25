# Mark Bank visual audit — reviewer brief

Mark Bank is a revision tool for Irish Leaving Certificate students. Each "card" shows ONE past exam question part
(lifted from an SEC paper) and, after the student taps "Reveal the marking scheme", the official marking scheme for it.
The owner wants to know, per subject: is the question asked clearly, is anything attached to it correct and limited to
THIS question, is the marking scheme presented clearly and does it answer THIS question, and does it look good on
desktop and on a phone.

For each subject you are given a folder `review/<subject>/` with `manifest.json` and screenshots of sampled cards taken
from the real app. Per card (NN = card number in the manifest):
- `NN_phone_answer.png` — the whole card on a 390px-wide phone AFTER the reveal. A long screen is cut into columns
  laid left to right (read column 1 top to bottom, then column 2...). Question is at the top, scheme below it.
- `NN_desktop_answer.png` — the same card on a 1280px desktop after the reveal (question left, scheme right).
- `NN_phone_first_screen.png` — what the phone shows first, before the reveal (390x844).
- `NN_attached_page.png` — only where the card attaches a page of the exam paper: the reader that opens when the
  student taps the attachment button (top of the first attached page).

Look at EVERY card's phone_answer and desktop_answer image, and its attached_page where present. Use the Read tool
on the PNG paths. The first-screen image is optional; open it for a few cards per subject.

## What to judge on each card
1. QUESTION: Is the question clear and complete as text? Any mangled notation, flattened tables/lists, run-on text,
   stray dashes/slashes/dots, missing symbols, part labels of OTHER parts pasted in, or text that needs the picture to make sense?
2. OTHER QUESTIONS SHOWN: Does any picture/crop in the question area, or the attached page, show questions or parts
   OTHER than the one this card asks (compare with `questionRef` and `topic` in the manifest)? Say exactly what else is
   visible (e.g. "attached page also shows Q4 and Q5 in full"). A reading passage, map, source document or data the
   question depends on is fine; other QUESTIONS are the problem. Sibling parts of the same question are a lesser issue
   — note them separately from different questions.
3. ATTACHMENT: Is the figure/crop the right one for this question, legible, sensibly cropped (not cut off, not tiny)?
4. MARKING SCHEME: Is it presented clearly? Does it plainly answer THIS question? Any strings of text joined with
   slashes, flattened tables, raw examiner shorthand, numbers that lost their layout, confusing mark arithmetic,
   walls of text? Would a scheme IMAGE (a crop of the official scheme) be clearer than this text? Where a scheme image
   is shown, is it legible and limited to this question?
5. PHONE vs DESKTOP: Anything that works on desktop but not on the phone (tiny text inside images, sideways overflow,
   cramped tables, enormous scroll length, controls pushed far away)? Estimate legibility honestly: text inside a crop
   that is much smaller than the app's own body text is a problem on a phone.
6. LOOK: Does it look clean and deliberate, or like random text strung together?

Be concrete and critical; the owner wants real faults, not reassurance. But do not invent faults: if a card is good, say so.
You cannot hear audio; for listening cards judge only what is on screen.

## Output
Write ONE JSON file per subject to `reviews/<subject>.json` (path given in your task), exactly this shape:
{
 "subject": "...",
 "verdict": "works" | "minor-issues" | "needs-work",
 "summary": "3-5 plain sentences on how this subject's questions and schemes look and the main faults",
 "scores": {"question": 1-5, "attachments": 1-5 or null if none, "scheme": 1-5, "phone": 1-5, "desktop": 1-5},
 "issues": [ {"title": "short name", "detail": "what is wrong, plainly", "severity": "high|medium|low",
              "cards": [card numbers], "best_evidence_image": "NN_xxx.png", "suggested_fix": "how to present it instead"} ],
 "good_examples": [ {"card": NN, "why": "one line", "image": "NN_phone_answer.png or NN_desktop_answer.png"} ],   // 2-3 cards that show the subject at its best
 "cards": [ {"n": NN, "question": "ok|minor|bad", "other_questions_shown": "none|same-question-parts|different-question",
             "other_detail": "", "attachment": "ok|minor|bad|none", "scheme": "ok|minor|bad", "phone": "ok|minor|bad",
             "desktop": "ok|minor|bad", "note": "one or two lines, specific"} ]
}
Then reply with a 5-10 line summary across your subjects. Do not edit any file in the repository.
