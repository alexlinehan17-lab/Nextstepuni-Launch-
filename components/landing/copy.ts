/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every word on the landing page, in one place. Plain, human, Irish. The
 * rules: say what the thing does, use the names the app uses, quote real
 * numbers only (see demoData.ts for where each one comes from), and never
 * reach for a slogan when a sentence will do.
 */

export type ChapterId = 'markbank' | 'papertrail' | 'atlas' | 'planner' | 'launchpad' | 'lab' | 'futurefinder';

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
      { label: 'CERTLE', href: '/certle' },
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
      { id: 'markbank', label: 'Mark Bank', hint: '' },
      { id: 'papertrail', label: 'Paper Trail', hint: 'Biology and Maths are open, with answers on most papers. The other subjects unlock with an account.' },
      { id: 'atlas', label: 'Topic Atlas', hint: 'Real questions, cropped from the printed papers. Tap one for its marking scheme.' },
      { id: 'planner', label: 'Planner & Study', hint: 'A real week, built for a sample sixth-year with seven subjects and Sundays off. Tap a block to study it.' },
      { id: 'reflex', label: 'Command-Word Reflex', hint: 'Pick Biology or Maths. Then tap the word the examiner is marking against.' },
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
    intro: 'Seven things, in the order you’ll probably meet them.',
    /** Mono label inside a chapter frame that has no screenshot yet. */
    placeholder: 'Screenshot · coming',
    /** Chapter I's frame: the real question with the marking scheme under a lens. */
    spotlight: {
      show: 'Show marking',
      hide: 'Hide marking',
      hint: 'Hover the question to see what the examiner saw.',
      scheme: 'Marking scheme',
    },
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
        id: 'planner', numeral: 'IV', word: 'Planner & Study', railLabel: 'Planner & Study',
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
          'Points Passport, Future Finder and College Compass are the CAO end of things. They have a chapter of their own: VII.',
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
      {
        id: 'futurefinder', numeral: 'VII', word: 'Future Finder', railLabel: 'Future Finder',
        line: 'The CAO end of things: courses, points and deadlines.',
        body: [
          'Future Finder asks you to rate short activity cards, works out the kind of work you lean towards, and ranks a hundred and forty-nine courses, PLCs and apprenticeships by how well they fit. Save the ones you like and compare them side by side.',
          'Points Passport turns your grades into CAO points, keeps each set of mock results, and shows which grade moves would return the most points for the effort.',
          'College Compass puts the CAO, HEAR, DARE and scholarship deadlines in order, stage by stage, with a checklist for sixth years.',
        ],
        frameLabel: 'Points Passport · Type a course',
      },
    ] as Chapter[],
  },

  /**
   * Chapter VII's course search (components/landing/fx-f). Type a course from
   * Points Passport's list and the chapter rewrites itself around it. Every
   * figure on the rewritten page comes from components/futureFinderData.ts;
   * the words here are only the furniture around them.
   */
  futurefinder: {
    label: 'Points Passport',
    placeholder: 'Type a course',
    /** {n} is the length of the list in the app. */
    hint: 'A code, a title or a college · {n} courses, PLCs and apprenticeships',
    sample: 'A few to try',
    none: 'No course by that name in the list.',
    matches: '{n} in the list',
    back: 'Back to the landing page',
    tryPassport: 'Try Points Passport in the playground',
    level: 'Level',
    points: 'points',
    card: {
      points: 'Typical points',
      level: 'Level',
      length: 'Length',
      subjects: 'Helpful subjects',
      careers: 'Where it leads',
      source: 'Points as listed in the app · 2025 CAO Round 1',
    },
    routes: { cao: 'CAO', plc: 'PLC', apprenticeship: 'Apprenticeship' },
    /** The app's own words for a route that has no points. */
    noPoints: { plc: 'Open entry', apprenticeship: 'Employer-based' },
    /** One line on what the app does with the course — nothing more. */
    helps: 'Points Passport tracks your grades against this course’s points.',
    helpsNoPoints: 'Future Finder ranks this route beside the CAO courses that fit your interests.',
    /** Read out by a screen reader when the chapter rewrites, and when it is restored. */
    turned: 'Chapter VII is now about {title} at {institution}. {line}.',
    restored: 'Chapter VII is back to Future Finder.',
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
    title: 'Fifteen subjects in the Mark Bank. Fifty-nine Leaving Cert subjects in the Paper Trail.',
    lede: 'The Mark Bank is built subject by subject, from the marking schemes. The Paper Trail holds the SEC’s papers from 2010 on for fifty-nine Leaving Cert subjects, from Accounting to the non-curricular languages, plus Junior Cycle and LCA.',
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
    /** The title in two sentences: the first is bracketed in ink, the way an examiner marks the line that matters. */
    titleJoin: 'One join code for students.',
    titleStaff: 'Two logins for staff.',
    body: 'Your school gets a join code that students use to sign up, plus a shared login for the guidance counsellor and one for the staff room. That is the whole setup.',
    cta: 'Email us',
    /** For a student who already has the code: sign-up in the app asks for it. */
    student: 'Have a code? Sign up in the app',
  },

  /** Hand-lettered notes in the character's line (components/landing/fx/Note.tsx); these are their accessible names. */
  fx: {
    notes: {
      here: 'you are here',
      join: 'join with your school’s code',
      end: 'the end',
    },
  },

  footer: {
    statement: 'Your study. Your way.',
    /** Rides the drawn line the character lands on. The headline, in one breath. */
    caption: 'Past papers, marking schemes, and a plan for the week',
    links: [
      { label: 'Privacy', href: '/privacy' },
      { label: 'Terms', href: '/terms' },
      { label: 'Sign in', href: '/' },
    ],
    contact: 'Email us',
    small: '© 2026 NextStepUni Ltd. Made in Ireland.',
  },
};

export type PlaygroundTabId = 'markbank' | 'papertrail' | 'atlas' | 'planner' | 'reflex' | 'passport' | 'futurefinder';
