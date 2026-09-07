/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every word on the landing page, in one place. Plain, human, Irish. The
 * rules: say what the thing does, use the names the app uses, quote real
 * numbers only (see demoData.ts for where each one comes from), and never
 * reach for a slogan when a sentence will do.
 */

export type ChapterId = 'markbank' | 'papertrail' | 'atlas' | 'planner' | 'launchpad' | 'lab';

export interface Chapter {
  id: ChapterId;
  numeral: string;
  /** The one giant word (or two) that opens the chapter. */
  word: string;
  /** The italic drop-cap line under it. */
  line: string;
  body: string[];
  /** Mono caption on the placeholder screenshot frame. */
  frameLabel: string;
  /** Short label for the rail. */
  railLabel: string;
}

export const COPY = {
  brand: {
    name: 'Nextstepuni',
    tagline: 'Your study. Your way.',
    supportEmail: 'nextstepuniinfo@gmail.com',
  },

  nav: {
    links: [
      { label: "What's inside", href: '#chapters' },
      { label: 'How it works', href: '#how' },
      { label: 'Subjects', href: '#subjects' },
      { label: 'Schools', href: '#schools' },
    ],
    signIn: 'Sign in',
    cta: 'Open the app',
    ctaShort: 'Open app',
    menu: 'Menu',
    close: 'Close',
  },

  hero: {
    eyebrow: 'For the Leaving Cert · Made in Ireland',
    headline: 'Past papers,\nmarking schemes,\nand a plan\nfor the week.',
    lede: 'Nextstepuni is built around the real exam. You answer questions from actual papers, see how the marking scheme scores them, and get a week planned around what needs work.',
    primary: 'Open the app',
    secondary: 'Try it below',
  },

  playground: {
    eyebrow: 'Have a go. No account needed.',
    cta: 'Open the app',
    tabs: [
      { id: 'markbank', label: 'Mark Bank', hint: 'The real Mark Bank. Biology, Economics and Maths are open; the rest unlock with an account.' },
      { id: 'papertrail', label: 'Paper Trail', hint: 'Mathematics is open, with answers on most papers. The other subjects unlock with an account.' },
      { id: 'atlas', label: 'Topic Atlas', hint: 'Real questions, cropped from the printed papers. Tap one for its marking scheme.' },
      { id: 'planner', label: 'Planner', hint: 'A real week, built for a sample sixth-year with six subjects and Sundays off.' },
      { id: 'reflex', label: 'Command-Word Reflex', hint: 'Under All Subjects, pick Biology, Economics or Maths. Then tap the word the examiner is marking against.' },
      { id: 'passport', label: 'Points Passport', hint: 'The Grade Planner is open. The other tabs unlock with an account.' },
      { id: 'futurefinder', label: 'Future Finder', hint: 'A sample student who finished the quiz. Three courses are queued to compare.' },
    ],
    live: 'Live · the actual app',
  },

  numbers: {
    eyebrow: 'What’s in it',
    items: [
      { value: '10,495', label: 'marking-scheme cards', note: '15 subjects, Higher and Ordinary' },
      { value: '4,621', label: 'past papers', note: '100 subjects across the Leaving Cert, LCA and Junior Cycle, 2010 to 2026. Most have the marking scheme beside them.' },
      { value: '19,565', label: 'Leaving Cert questions mapped by topic', note: 'across 58 subjects and 1,716 topics' },
      { value: '566', label: 'command-word questions', note: 'real exam questions, with the examiner’s trap explained' },
    ],
  },

  chapters: {
    tryIt: 'Try it in the playground',
    eyebrow: 'Inside the app',
    intro: 'Six things, in the order you’ll probably meet them.',
    /** Mono label inside a chapter frame that has no screenshot yet. */
    placeholder: 'Screenshot · coming',
    items: [
      {
        id: 'markbank', numeral: 'I', word: 'Mark Bank', railLabel: 'Mark Bank',
        line: 'Answer the real question, then read the real marking scheme.',
        body: [
          'Each card is a question, or a part of one, from an actual paper. The marking points underneath are transcribed from that year’s scheme, not summarised.',
          'You answer first, in your head or on paper. Then you reveal the scheme beside the question and tick the marks you actually got.',
          'Cards you missed come back sooner. Cards you got come back later. Progress is counted in marks, never percentages.',
        ],
        frameLabel: 'Mark Bank · Biology, Higher',
      },
      {
        id: 'papertrail', numeral: 'II', word: 'Paper Trail', railLabel: 'Paper Trail',
        line: 'Past papers back to 2010, with the marking scheme beside them.',
        body: [
          'Open a paper from 2010 on, with its marking scheme beside it where the SEC published one. On most papers you can tap a question and see just that question’s part of the scheme.',
          'Build a mock from real questions, sit it against the clock, and mark it afterwards.',
        ],
        frameLabel: 'Paper Trail · 2024, Higher',
      },
      {
        id: 'atlas', numeral: 'III', word: 'Topic Atlas', railLabel: 'Topic Atlas',
        line: 'Seventeen years of exam questions, sorted by topic.',
        body: [
          'Nineteen and a half thousand Leaving Cert questions, tagged to the topics on the syllabus. You can see which topics come up every year and which have hardly come up at all.',
          'Revise one topic across seventeen years of papers, instead of one paper across every topic.',
        ],
        frameLabel: 'Topic Atlas · Biology',
      },
      {
        id: 'planner', numeral: 'IV', word: 'Planner', railLabel: 'Planner',
        line: 'A week built around your weakest subjects.',
        body: [
          'Give it your subjects, your current and target grades, and your exam date. It builds a weekly timetable weighted towards the subjects with the biggest gap between the two. Rest days stay rest days.',
          'Today’s plan sits on the home screen. Cards due for review come back through the Mark Bank on their own schedule.',
        ],
        frameLabel: 'Today’s plan',
      },
      {
        id: 'launchpad', numeral: 'V', word: 'Launchpad', railLabel: 'Launchpad',
        line: 'Small tools for the sharp end of the exam.',
        body: [
          'Command-Word Reflex: find the word the examiner is marking against before you write a line.',
          'Catch-Up Lane: missed a class? Pick the topic you missed. Each one takes about three minutes, with a quick check at the end.',
          'Points Passport, Future Finder and College Compass for the CAO end of things: your grades as points, a shortlist of courses matched to your interests, and the CAO, HEAR and DARE deadlines in order.',
        ],
        frameLabel: 'The Launchpad',
      },
      {
        id: 'lab', numeral: 'VI', word: 'Learning Lab', railLabel: 'Learning Lab',
        line: 'How studying works, with the sources cited.',
        body: [
          'Short modules on how memory, recall and revision actually work, read one section at a time.',
          'Forty-eight of them list their sources, with a link to each one. Read one before your next session.',
        ],
        frameLabel: 'Learning Lab · Mastering Active Recall',
      },
    ] as Chapter[],
  },

  cta: {
    line: 'Open the app, or have a go at the Mark Bank above first.',
    primary: 'Open the app',
    secondary: 'Try the Mark Bank',
  },

  how: {
    eyebrow: 'How it works',
    title: 'Three steps, then it runs itself.',
    steps: [
      { n: '1', title: 'Pick your subjects and levels', body: 'Higher or Ordinary, any mix. Change it whenever.' },
      { n: '2', title: 'Work the real questions', body: 'A few cards a day from the Mark Bank, or a full paper from the Paper Trail.' },
      { n: '3', title: 'Let the schedule do its job', body: 'Cards you missed come back sooner. Your week is built around the subjects that need it.' },
    ],
  },

  subjects: {
    eyebrow: 'Subjects',
    title: 'Fifteen subjects in the Mark Bank. A hundred in the Paper Trail.',
    lede: 'The Mark Bank is built subject by subject, from the marking schemes. The Paper Trail holds the SEC’s papers from 2010 on, for the Leaving Cert, LCA and Junior Cycle.',
    columns: { subject: 'Subject', markBank: 'Mark Bank cards', paperTrail: 'Paper Trail', papers: 'Papers' },
    yes: 'Yes',
    notYet: 'Not yet',
    stats: { cards: 'Mark Bank cards', inTrail: 'In the Paper Trail', papers: 'Papers in the Paper Trail', of: 'of' },
    groupNotes: {
      sciences: 'Higher and Ordinary science papers back to 2010, and the biggest Mark Bank decks.',
      business: 'Business and Economics are carded from their marking schemes. Accounting is in the Paper Trail while its cards are still being built.',
      maths: 'Maths and Computer Science have cards. Applied Maths is in the Paper Trail but has no cards yet.',
      languages: 'English and Irish have cards. French, German, Spanish and Italian are in the Paper Trail but have no cards yet.',
      humanities: 'Geography has cards. History, Politics and Society, Religious Education and Classical Studies are in the Paper Trail but have no cards yet.',
      practical: 'Art, Construction Studies, Engineering and Home Economics have cards. DCG, Technology, Music and PE are in the Paper Trail but have no cards yet.',
    } as Record<string, string>,
    stillBuilding: 'No Mark Bank cards for this group yet. The papers are already in the Paper Trail.',
  },

  schools: {
    eyebrow: 'For schools',
    title: 'One join code for students. Two logins for staff.',
    body: 'Your school gets a join code that students use to sign up, plus a shared login for the guidance counsellor and one for the staff room. That is the whole setup.',
    cta: 'Email us',
  },

  footer: {
    statement: 'Your study. Your way.',
    links: [
      { label: 'Privacy', href: '/privacy' },
      { label: 'Terms', href: '/terms' },
      { label: 'Sign in', href: '/' },
    ],
    contact: 'Email us',
    small: '© 2026 NextStepUni Ltd. Made in Ireland.',
    attribution: 'Examination material © State Examinations Commission.',
  },
};

export type PlaygroundTabId = 'markbank' | 'papertrail' | 'atlas' | 'planner' | 'reflex' | 'passport' | 'futurefinder';
