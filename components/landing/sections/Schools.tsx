/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * For schools: one short band. Two shared logins per school is the whole
 * pitch. An ink bracket marks the join-code sentence (one of the page's three
 * examiner's marks), and a hand-lettered note points a student with a code
 * at the sign-up link — the app's sign-up asks for the code.
 */

import React from 'react';
import { COPY } from '../copy';
import { Button, Container, Display, Eyebrow, Lede, SectionRule } from '../primitives';
import { APP_URL, SPACE } from '../theme';
import { Mark } from '../fx/marks';
import { Note } from '../fx/Note';

const Schools: React.FC = () => (
  <section id="schools" className={SPACE.sectionTight} style={{ position: 'relative', scrollMarginTop: 70 }}>
    <SectionRule />
    <Container className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-end">
      <div className="lg:col-span-8">
        <Eyebrow>{COPY.schools.eyebrow}</Eyebrow>
        <Display size="section" as="h2" className="mt-4">
          <Mark type="bracket" brackets="left" padding={[0, 6, 0, 10]} strokeWidth={1.5} style={{ display: 'inline-block' }}>{COPY.schools.titleJoin}</Mark>
          {' '}
          {COPY.schools.titleStaff}
        </Display>
        <Lede className="mt-5">{COPY.schools.body}</Lede>
        <div className="mt-8 flex flex-wrap items-end gap-x-5 gap-y-3">
          <Note id="join" mode="scroll" style={{ width: 'clamp(170px, 18vw, 228px)' }} />
          <Button variant="ghost" href={APP_URL}>{COPY.schools.student}</Button>
        </div>
      </div>
      <div className="lg:col-span-4 lg:text-right">
        <Button variant="secondary" href={`mailto:${COPY.brand.supportEmail}`} size="lg">{COPY.schools.cta}</Button>
      </div>
    </Container>
  </section>
);

export default Schools;
