/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Answer like an examiner. One section, four framed boxes in the page's
 * Frame idiom, each with its numbered eyebrow, serif title and one line of
 * copy beside it:
 *   01  the question-vs-scheme compare box (absorbed from sections/Compare)
 *   02  Mark my answer — write, and the scheme's own points mark it
 *   03  What the examiner wants — a full-marks answer, line by line
 *   04  Mark one yourself — the scheme's points, placed on its own answer
 * Every question and every scheme line is lifted, never written
 * (scripts/landing/examiner-cards.mjs). Section copy is local to this file.
 */

import React from 'react';
import { Reveal } from '../motion';
import { Body, Container, Display, Eyebrow, Lede, SectionRule } from '../primitives';
import { SPACE } from '../theme';
import CompareBox, { COMPARE_TEXT } from '../fx-d/CompareBox';
import MarkMyAnswer from '../fx-d/MarkMyAnswer';
import ExaminerWants from '../fx-d/ExaminerWants';
import MarkOneYourself from '../fx-d/MarkOneYourself';
import '../fx-d/fx-d.css';

const TEXT = {
  eyebrow: 'Marking',
  title: 'Answer like an examiner',
  lede: 'Every Leaving Cert paper is marked against a scheme the SEC publishes after the exam. Here it is four ways: beside its question, over an answer of your own, line by line through a full-marks answer, and with the marks in your hand.',
  boxes: {
    compare: { n: '01', eyebrow: COMPARE_TEXT.eyebrow, title: COMPARE_TEXT.line, body: COMPARE_TEXT.body },
    mark: {
      n: '02',
      eyebrow: 'Write it, the scheme marks it',
      title: 'Mark my answer',
      body: 'Twenty questions from five subjects, each with the points its marking scheme awards. Type what you would write in the exam and mark it: a point is earned when your answer says what the scheme says, and a missed one shows what the examiner wanted.',
    },
    wants: {
      n: '03',
      eyebrow: 'A full-marks answer, point by point',
      title: 'What the examiner wants',
      body: 'The scheme’s own possible response, set line by line beside the points it prints and what each is worth. Hover or tab to any line to see the point it earns.',
    },
    place: {
      n: '04',
      eyebrow: 'Now you hold the marks',
      title: 'Mark one yourself',
      body: 'The scheme’s points and its own answer to a different question. Put each point on the line that earns it: drag it there, or select it and then the line.',
    },
  },
} as const;

const Box: React.FC<{ id?: string; n: string; eyebrow: string; title: string; body: string; children: React.ReactNode }> = ({ id, n, eyebrow, title, body, children }) => (
  <div id={id} className="fxd-box grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start" style={{ scrollMarginTop: 90 }}>
    <div className="lg:col-span-4 lg:pt-2">
      <Eyebrow>{n} · {eyebrow}</Eyebrow>
      <Display size="sub" as="h3" className="mt-4" style={{ maxWidth: '18ch' }}>{title}</Display>
      <Body className="mt-5" style={{ maxWidth: '40ch' }}>{body}</Body>
    </div>
    <div className="lg:col-span-8 min-w-0">
      <Reveal>{children}</Reveal>
    </div>
  </div>
);

const Examiner: React.FC = () => (
  <section id="examiner" className={SPACE.section} style={{ position: 'relative', scrollMarginTop: 70 }}>
    <SectionRule />
    <Container>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-16 items-end">
        <div className="lg:col-span-7">
          <Eyebrow>{TEXT.eyebrow}</Eyebrow>
          <Display size="section" as="h2" className="mt-4">{TEXT.title}</Display>
        </div>
        <div className="lg:col-span-5">
          <Lede>{TEXT.lede}</Lede>
        </div>
      </div>

      <div className="mt-14 md:mt-20 flex flex-col gap-16 md:gap-24">
        <Box id="compare" {...TEXT.boxes.compare}><CompareBox /></Box>
        <Box id="mark-my-answer" {...TEXT.boxes.mark}><MarkMyAnswer /></Box>
        <Box id="examiner-wants" {...TEXT.boxes.wants}><ExaminerWants /></Box>
        <Box id="mark-one-yourself" {...TEXT.boxes.place}><MarkOneYourself /></Box>
      </div>
    </Container>
  </section>
);

export default Examiner;
