/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — classroom pilot kit (teacher one-pager).
 *
 * A self-contained, print-friendly HTML sheet a teacher can keep in the staff
 * room: how to run a marking class with a class code, what they'll see, and
 * the privacy guarantee in plain words. Pure string build (unit-testable);
 * the download is a thin browser wrapper, mirroring progressReport.ts.
 */

export const PILOT_KIT_FILENAME = 'run-a-marking-class.html';

/** Build the one-pager. Pure. */
export function buildPilotKitHtml(): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Run a marking class — The Examiner's Chair</title>
<style>
  body { font-family: 'DM Sans', -apple-system, 'Segoe UI', sans-serif; color: #1a1a1a; max-width: 720px; margin: 32px auto; padding: 0 20px; line-height: 1.55; }
  h1 { font-family: Georgia, 'Source Serif 4', serif; font-size: 26px; margin: 0 0 4px; }
  .sub { color: #7a7068; font-size: 14px; margin: 0 0 22px; }
  h2 { font-family: Georgia, 'Source Serif 4', serif; font-size: 16px; margin: 22px 0 8px; }
  ol { padding-left: 20px; margin: 0; }
  li { margin-bottom: 8px; font-size: 14px; }
  .step b { color: #8C3A0E; }
  .box { border: 2px solid #1a1a1a; border-radius: 14px; padding: 14px 16px; margin: 14px 0; }
  .privacy { background: #E8F2EC; border: none; border-left: 3px solid #3A8D5F; border-radius: 0 10px 10px 0; color: #1F5F3E; font-size: 13.5px; }
  .tip { background: #FDEEDF; border: none; border-left: 3px solid #F26B1F; border-radius: 0 10px 10px 0; color: #8C3A0E; font-size: 13.5px; font-style: italic; }
  .muted { color: #7a7068; font-size: 12px; margin-top: 24px; }
  @media print { body { margin: 0 auto; } .noprint { display: none; } }
</style>
</head>
<body>
  <h1>Run a marking class</h1>
  <p class="sub">The Examiner's Chair · Nextstepuni Learning Lab — students mark exam scripts against the real SEC marking rules, and you see exactly what your class mis-marks.</p>

  <h2>The 15-minute starter</h2>
  <ol>
    <li class="step"><b>Pick a class code.</b> Any short word or phrase (e.g. <i>6th-biz-murphy</i>). Students must type it exactly — it's the only thing that links the class together.</li>
    <li class="step"><b>Students mark a session.</b> Launchpad → <i>The Examiner's Chair</i> → your subject → any session. They mark each sample script the way the examiner would, then see the real key, decision by decision.</li>
    <li class="step"><b>Students send their blind spots.</b> On the session summary they tap <i>Send</i> with the class code. One tap, entirely their choice.</li>
    <li class="step"><b>Open the teacher view.</b> Chair home → <i>Teacher view</i> → enter the same code. The marking rules your class most often gets wrong rank live — "64% of your class awards the link mark when the examiner doesn't" — the exact things to reteach.</li>
    <li class="step"><b>Let the class conference.</b> Once classmates have submitted, each script's reveal also shows students how the class called every decision beside the examiner's key — the same moderation conversation real SEC markers have.</li>
  </ol>

  <h2>Also in the room</h2>
  <ol>
    <li><b>The Daily Mark</b> — one shared script a day; students can compare their agreement with the class median, anonymously.</li>
    <li><b>Borderline drill</b> — just the genuinely contested scripts, for the hard-calls conversation.</li>
    <li><b>Shared focus</b> — students running a focus timer with the class code see how many classmates are at their desks too.</li>
  </ol>

  <div class="box privacy">
    <b>Privacy, in plain words.</b> The class features store only anonymous counts under the class code — how many chose what. No names, no student accounts, no individual records exist in the shared data, so neither you nor anyone else can ever see <i>who</i> answered. Students share only when they themselves tap Send.
  </div>

  <div class="box tip">
    Works well as a weekly starter: same session for everyone Monday, reteach the top mis-marked rule Wednesday, re-run the borderline drill Friday and watch the class percentage move.
  </div>

  <p class="muted">Every marking rule in the tool is cited to a filed SEC marking scheme or Chief Examiner's Report. Sample scripts are authored for the exercise and labelled as such — never real candidate work.</p>
</body>
</html>`;
}

/** Build the kit and trigger a browser download. Browser-only. */
export function downloadPilotKit(): void {
  const html = buildPilotKitHtml();
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = PILOT_KIT_FILENAME;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
