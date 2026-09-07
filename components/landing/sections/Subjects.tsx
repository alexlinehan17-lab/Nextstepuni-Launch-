/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subjects — Brilliant's "From grade 5 to college" switcher in our register.
 * Group tabs over a ruled table of subjects with real Mark Bank card counts
 * and the years each subject's papers span in the Paper Trail
 * (demoData.SUBJECT_GROUPS), and beside it a frame that states the active
 * group as two figures: cards in the bank, and the span of years its papers
 * cover. Tab changes cross-fade the table, stagger the rows in, and remount
 * the numerals; all of it collapses to an instant swap under reduced motion.
 */

import React, { useState } from 'react';
import { AnimatePresence, MotionDiv, MotionSpan, useReducedMotion } from '../../Motion';
import { COPY } from '../copy';
import { SUBJECT_GROUPS, type SubjectGroup } from '../demoData';
import { Body, Container, Display, Eyebrow, Frame, Lede, Rule, TextTabs, SectionRule } from '../primitives';
import { FONT, L, SPACE } from '../theme';

const EASE: [number, number, number, number] = [0.2, 0.8, 0.2, 1];
/**
 * Column tracks. Under 640px the two number columns share the width with the
 * subject column by ratio (their headers wrap to two lines) so a 300px-wide
 * table still gives "Agricultural Science" ~110px and never breaks a word.
 * From sm up the number columns size to their headers and the subject takes
 * the rest. Header and rows share the same -mx-2/px-2 so the solid-ink hover
 * box and the hairlines line up with the header text. Cells set colour only,
 * never a background, so the flip shows through.
 */
const ROW = 'grid grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)_minmax(0,1fr)] sm:grid-cols-[minmax(0,1fr)_auto_auto] gap-x-3 sm:gap-x-5 py-3 px-2 -mx-2';

const CAPTION: React.CSSProperties = {
  fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, lineHeight: 1.2,
};

/** Numbers are identity: tabular serif, even at table size. Both number columns share it so the counts and the year spans line up. */
const NUMERAL: React.CSSProperties = { fontFamily: FONT.serif, fontWeight: 600, fontSize: 15, color: L.ink, fontVariantNumeric: 'tabular-nums' };

const numeral = (n: number): string => n.toLocaleString('en-IE');

const EN_DASH = '–';

/** '2010–2026' -> [2010, 2026]. A single year ('2024') spans itself. Returns null when the string holds no year. */
const parseSpan = (s: string): [number, number] | null => {
  const years = s.split(/[^0-9]+/).filter(Boolean).map(Number).filter(n => Number.isFinite(n));
  if (years.length === 0) return null;
  return [Math.min(...years), Math.max(...years)];
};

/** The group's span in the Paper Trail: earliest first year to latest last year across the rows that have papers. */
const groupSpan = (g: SubjectGroup): string | null => {
  let lo = Infinity;
  let hi = -Infinity;
  for (const s of g.subjects) {
    if (!s.paperTrail) continue;
    const span = parseSpan(s.paperYears);
    if (!span) continue;
    lo = Math.min(lo, span[0]);
    hi = Math.max(hi, span[1]);
  }
  if (!Number.isFinite(lo) || !Number.isFinite(hi)) return null;
  return lo === hi ? String(lo) : `${lo}${EN_DASH}${hi}`;
};

/** The ruled table for one group. Rows rise in with a 30ms stagger. */
const GroupTable: React.FC<{ group: SubjectGroup; reduce: boolean }> = ({ group, reduce }) => (
  <div role="table" aria-label={group.label} style={{ fontFamily: FONT.sans, fontSize: 15 }}>
    <div role="row" className={`${ROW} items-end`} style={CAPTION}>
      <div role="columnheader" className="text-left">{COPY.subjects.columns.subject}</div>
      <div role="columnheader" className="text-right">{COPY.subjects.columns.markBank}</div>
      <div role="columnheader" className="text-right">{COPY.subjects.columns.papers}</div>
    </div>
    <div role="rowgroup">
      {group.subjects.map((s, i) => (
        <MotionDiv
          key={s.id}
          role="row"
          className={`landing-hover-card ${ROW} items-baseline`}
          style={{ borderTop: `1px solid ${L.hairline}`, borderRadius: 6 }}
          initial={reduce ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: reduce ? 0 : i * 0.03, duration: reduce ? 0 : 0.3, ease: EASE }}
        >
          <div role="cell" style={{ fontWeight: 600, color: L.ink, overflowWrap: 'anywhere' }}>{s.label}</div>
          <div
            role="cell"
            className={`text-right whitespace-nowrap${s.markBankCards ? '' : ' landing-faint'}`}
            style={s.markBankCards ? NUMERAL : { color: L.faint }}
          >
            {s.markBankCards ? numeral(s.markBankCards) : COPY.subjects.notYet}
          </div>
          <div
            role="cell"
            className={`text-right whitespace-nowrap${s.paperTrail ? '' : ' landing-faint'}`}
            style={s.paperTrail ? NUMERAL : { color: L.faint }}
          >
            {s.paperTrail ? s.paperYears : COPY.subjects.notYet}
          </div>
        </MotionDiv>
      ))}
    </div>
  </div>
);

/** A display numeral that remounts (and rises) whenever `id` changes. */
const Figure: React.FC<{ id: string; reduce: boolean; children: React.ReactNode }> = ({ id, reduce, children }) => (
  <MotionSpan
    key={id}
    style={{
      display: 'block', fontFamily: FONT.serif, fontWeight: 600, color: L.ink,
      fontSize: 'clamp(44px, 6vw, 72px)', lineHeight: 1, letterSpacing: '-0.03em', fontVariantNumeric: 'tabular-nums',
    }}
    initial={reduce ? false : { opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: reduce ? 0 : 0.32, ease: EASE }}
  >
    {children}
  </MotionSpan>
);

const Subjects: React.FC = () => {
  const reduce = useReducedMotion() === true;
  const [group, setGroup] = useState(SUBJECT_GROUPS[0].id);
  const g = SUBJECT_GROUPS.find(x => x.id === group) ?? SUBJECT_GROUPS[0];

  const cards = g.subjects.reduce((n, s) => n + s.markBankCards, 0);
  const span = groupSpan(g);
  const note = cards === 0 ? COPY.subjects.stillBuilding : (COPY.subjects.groupNotes[g.id] ?? COPY.subjects.stillBuilding);

  return (
    <section id="subjects" className={SPACE.section} style={{ position: 'relative', scrollMarginTop: 70 }}>
    <SectionRule />
      <Container>
        <Eyebrow>{COPY.subjects.eyebrow}</Eyebrow>
        <Display size="section" as="h2" className="mt-4">{COPY.subjects.title}</Display>
        <Lede className="mt-5">{COPY.subjects.lede}</Lede>

        <TextTabs
          className="mt-8 landing-strip"
          ariaLabel="Subject group"
          items={SUBJECT_GROUPS.map(x => ({ id: x.id, label: x.label }))}
          active={group}
          onChange={setGroup}
        />

        <div role="tabpanel" aria-label={g.label} className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 mt-2">
          {/* Table — cross-fades on tab change */}
          <div className="lg:col-span-7 min-w-0">
            <AnimatePresence mode="wait" initial={false}>
              <MotionDiv
                key={g.id}
                initial={reduce ? false : { opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={reduce ? undefined : { opacity: 0 }}
                transition={{ duration: reduce ? 0 : 0.18, ease: 'easeOut' }}
              >
                <GroupTable group={g} reduce={reduce} />
              </MotionDiv>
            </AnimatePresence>
          </div>

          {/* Stat frame — the group as two figures */}
          <div className="lg:col-span-5 min-w-0 lg:pt-3">
            <Frame>
              <div className="p-6 md:p-7" aria-live="polite">
                <div style={CAPTION}>{g.label}</div>

                <div className="mt-6">
                  <Figure id={`${g.id}-cards`} reduce={reduce}>{numeral(cards)}</Figure>
                  <div className="mt-3" style={CAPTION}>{COPY.subjects.stats.cards}</div>
                </div>

                <Rule className="my-6" />

                <div>
                  <Figure id={`${g.id}-papers`} reduce={reduce}>
                    {span ?? <span style={{ color: L.faint }}>{COPY.subjects.notYet}</span>}
                  </Figure>
                  <div className="mt-3" style={CAPTION}>{COPY.subjects.stats.papers}</div>
                </div>

                <Body className="mt-6">{note}</Body>
              </div>
            </Frame>
          </div>
        </div>
      </Container>
    </section>
  );
};

export default Subjects;
