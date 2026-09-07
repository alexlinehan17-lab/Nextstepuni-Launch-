/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * For schools: one short band. Two shared logins per school is the whole pitch.
 */

import React from 'react';
import { COPY } from '../copy';
import { Button, Container, Display, Eyebrow, Lede, SectionRule } from '../primitives';
import { SPACE } from '../theme';

const Schools: React.FC = () => (
  <section id="schools" className={SPACE.sectionTight} style={{ position: 'relative', scrollMarginTop: 70 }}>
    <SectionRule />
    <Container className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-end">
      <div className="lg:col-span-8">
        <Eyebrow>{COPY.schools.eyebrow}</Eyebrow>
        <Display size="section" as="h2" className="mt-4">{COPY.schools.title}</Display>
        <Lede className="mt-5">{COPY.schools.body}</Lede>
      </div>
      <div className="lg:col-span-4 lg:text-right">
        <Button variant="secondary" href={`mailto:${COPY.brand.supportEmail}`} size="lg">{COPY.schools.cta}</Button>
      </div>
    </Container>
  </section>
);

export default Schools;
