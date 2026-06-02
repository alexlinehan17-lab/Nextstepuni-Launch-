/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Catch-Up Lane — Arm 2 ("Your Comeback") content.
 *
 * The emotional/practical re-entry after absence. Grounded (2026-06-02) in:
 *  - NEPS (Ireland) "School Refusal Behaviour" guidance (graded return; ONE key
 *    adult + safe space; predictability; DO NOT interrogate or shame);
 *  - EBSA toolkits (the avoidance loop; scripts to explain absence without shame);
 *  - self-compassion vs shame research (shame increases avoidance);
 *  - implementation intentions / MCII (if-then plans against a named obstacle —
 *    improved attendance in disadvantaged students; effect strongest when tied to
 *    a personal motivation);
 *  - Irish support structures: year head/tutor + guidance counsellor (all
 *    schools), HSCL coordinator + School Completion Programme keyworker (DEIS),
 *    Tusla Educational Welfare Officer (the supportive 20-day backstop).
 *
 * Tone rule: warm, normalising, present-focused. No "why were you out?",
 * no days-missed counters, no consequence figures aimed at the student.
 */

/** The avoidance loop, shown as a tap-through so the student sees a mechanism, not a personal failing. */
export const LOOP_STEPS: { label: string; note: string }[] = [
  { label: 'School feels hard', note: 'Worry or dread builds up about going in.' },
  { label: 'So you stay home', note: 'Avoiding it makes the worry drop — fast. That relief is real.' },
  { label: 'But the gap grows', note: 'Work piles up and you miss your friends, so school feels even bigger.' },
  { label: 'Which feeds the dread', note: 'Now there’s more to dread — and the loop pulls tighter.' },
];

export interface Obstacle {
  id: string;
  label: string;     // the worry, in the student's voice
  reframe: string;   // self-compassionate, normalising
  firstStep: string; // a tiny, almost-guaranteed graded-exposure step
  ifThen: { trigger: string; action: string };
}

export const OBSTACLES: Obstacle[] = [
  {
    id: 'morning-dread',
    label: 'Mornings are the worst — I can’t make myself go in',
    reframe: 'The dread is loudest in the morning and fades once you’re moving — that’s how avoidance works, not proof you can’t do it. Lots of students find the first morning the hardest part.',
    firstStep: 'Just aim to get to the school gate — you don’t have to decide about the whole day yet.',
    ifThen: { trigger: 'If it’s morning and the dread starts rising', action: 'then I’ll put my shoes on and text my person that I’m on my way' },
  },
  {
    id: 'everyone-asks',
    label: 'Everyone will ask where I’ve been',
    reframe: 'People notice far less than the dread tells you — and you get to decide how little to say. Having one line ready means you’re never caught off guard.',
    firstStep: 'Pick one short line to have ready for “where were you?”.',
    ifThen: { trigger: 'If someone asks where I was', action: 'then I’ll use my ready line and move the chat on' },
  },
  {
    id: 'so-behind',
    label: 'I’m so far behind, there’s no catching up',
    reframe: 'You don’t catch up all at once — you close one gap at a time. That’s exactly what the “Catch up on what you missed” side of this tool is for.',
    firstStep: 'Find the ONE most important thing to catch up on first — ask a teacher or a friend.',
    ifThen: { trigger: 'If catching up feels too big', action: 'then I’ll do one short Catch-Up topic, not the whole pile' },
  },
  {
    id: 'teacher-annoyed',
    label: 'My teacher will be annoyed I was out',
    reframe: 'Teachers and year heads are told their job is to help you come back, not to give out about it — asking for help is exactly what they expect you to do.',
    firstStep: 'Tell one teacher or your year head you’re back and want to catch up.',
    ifThen: { trigger: 'If I’m scared a teacher will be annoyed', action: 'then I’ll send my catch-up line to my year head first, before class' },
  },
  {
    id: 'too-big',
    label: 'The whole thing just feels too big',
    reframe: 'Overwhelm shrinks the moment it becomes one small step instead of everything at once. You don’t need to feel ready first — doing the small thing is what brings the readiness.',
    firstStep: 'Pick the smallest possible first move, and do only that.',
    ifThen: { trigger: 'If it all feels like too much', action: 'then I’ll do just my one tiny step and stop there for today' },
  },
];

/** Low-disclosure lines for the dreaded "where were you?" moment (EBSA: scripts to explain absence without shame). */
export const PEER_SCRIPTS: string[] = [
  'I was out for a bit — good to be back.',
  'I wasn’t great, I’m grand now.',
  'Had some stuff going on — all sorted.',
  'Ah, just out for a while. Anyway — what did I miss?',
];

/** Script for asking a teacher what to prioritise (self-advocacy). */
export const TEACHER_SCRIPT =
  'I missed some classes — could you tell me the most important thing to catch up on? And could I have a bit of extra time on anything that’s overdue?';

export interface SupportPerson {
  id: string;
  role: string;        // who they are
  whatTheyDo: string;
  script: string;      // how to approach them
  deis: boolean;       // true = mainly in DEIS schools
}

export const SUPPORT_PEOPLE: SupportPerson[] = [
  {
    id: 'year-head',
    role: 'Your year head or tutor',
    whatTheyDo: 'Looks after your year day to day — the easiest, most familiar first person to tell you’re back.',
    script: '“I’ve been out and I’m a bit nervous about coming back — could we have a quick chat?”',
    deis: false,
  },
  {
    id: 'guidance',
    role: 'The guidance counsellor',
    whatTheyDo: 'One-to-one support for how you’re feeling. Every school has one, and you can ask for them yourself.',
    script: '“Could I book a few minutes with the guidance counsellor? I’ve been finding things hard.”',
    deis: false,
  },
  {
    id: 'hscl',
    role: 'Your HSCL coordinator',
    whatTheyDo: 'In most DEIS schools — a teacher who links home and school and can talk to your family. A home visit is to help, not to give out.',
    script: '“Is there an HSCL coordinator I could talk to? Things have been tough at home/school.”',
    deis: true,
  },
  {
    id: 'scp',
    role: 'Your School Completion keyworker',
    whatTheyDo: 'In schools with the School Completion Programme — sets up catch-up help, homework club and checks in with you. You can ask for them yourself.',
    script: '“Does our school have a School Completion keyworker I could meet?”',
    deis: true,
  },
];

/** Reassurance about the Tusla 20-day trigger — support, not punishment. */
export const EWO_NOTE =
  'If you’ve missed a lot of school, your school lets Tusla know — that brings an Educational Welfare Officer whose job is to help your family get you back, not to fine you. It’s a support, not a telling-off.';

/** A 30-second grounding option for the dread moment. */
export const GROUNDING = {
  title: 'A 30-second reset for the morning',
  steps: [
    'Box breathing: breathe in for 4, hold for 4, out for 4, hold for 4 — three rounds.',
    'Name it: “this is the dread, and it fades once I’m moving.”',
    'Bring something small in your pocket from someone who’s got your back.',
  ],
};

/** Fallback "why it matters" prompts when the student has no North Star set. */
export const WHY_OPTIONS: string[] = [
  'I want to sit my exams with real options open',
  'I don’t want to fall any further behind',
  'There are people here I actually like seeing',
  'I’ve come too far to stop now',
  'Future me will be glad I went in',
];
