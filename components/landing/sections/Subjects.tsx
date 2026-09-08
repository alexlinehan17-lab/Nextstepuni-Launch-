/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subjects — the list, and the real papers. The group switch (the app's own
 * pill bar, whose pill glides) sits over a ruled table of that group's
 * subjects with real Mark Bank card counts and the years each subject's
 * papers span in the Paper Trail (demoData.SUBJECT_GROUPS); hover a subject
 * and the first page of its actual paper appears beside the pointer
 * (fx-c/Peek). Two figures state the group: cards in the bank, and the span
 * of years its papers cover. Beside all that on a desktop (after it, on a
 * phone) first pages of six SEC papers pile up as the reader scrolls
 * (fx-c/PaperStack). Tab changes cross-fade the table, stagger the rows in,
 * and remount the numerals; all of it collapses to an instant swap under
 * reduced motion.
 */

import React, { useState } from 'react';
import { AnimatePresence, MotionDiv, MotionSpan, useReducedMotion } from '../../Motion';
import HorizontalTabs from '../../ui/HorizontalTabs';
import { COPY } from '../copy';
import { SUBJECT_GROUPS, type SubjectGroup } from '../demoData';
import PaperStack from '../fx-c/PaperStack';
import { PeekLink, PeekProvider, preload } from '../fx-c/Peek';
import { peekFor } from '../fx-c/papers';
import { Body, Container, Display, Eyebrow, Lede, Rule, SectionRule } from '../primitives';
import { APP_URL, FONT, L, SPACE } from '../theme';
import '../fx-c/fx-c.css';

const EASE: [number, number, number, number] = [0.2, 0.8, 0.2, 1];

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

/** The ruled table for one group. Rows rise in with a 30ms stagger; each subject name peeks its real paper. */
const GroupTable: React.FC<{ group: SubjectGroup; reduce: boolean }> = ({ group, reduce }) => (
  <div role="table" aria-label={group.label} style={{ fontFamily: FONT.sans, fontSize: 15 }}>
    <div role="row" className="fxc-row items-end" style={{ ...CAPTION, borderTop: 0 }}>
      <div role="columnheader" className="text-left">{COPY.subjects.columns.subject}</div>
      <div role="columnheader" className="text-right">{COPY.subjects.columns.markBank}</div>
      <div role="columnheader" className="text-right">{COPY.subjects.columns.papers}</div>
    </div>
    <div role="rowgroup">
      {group.subjects.map((s, i) => {
        const peek = peekFor(s.id, s.label);
        return (
          <MotionDiv
            key={s.id}
            role="row"
            className="landing-hover-card fxc-row"
            initial={reduce ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: reduce ? 0 : i * 0.03, duration: reduce ? 0 : 0.3, ease: EASE }}
          >
            <div role="cell" style={{ fontWeight: 600, color: L.ink, overflowWrap: 'anywhere' }}>
              <PeekLink href={APP_URL} peek={peek}>{s.label}</PeekLink>
            </div>
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
        );
      })}
    </div>
  </div>
);

/** A display numeral that remounts (and rises) whenever `id` changes. */
const Figure: React.FC<{ id: string; reduce: boolean; children: React.ReactNode }> = ({ id, reduce, children }) => (
  <MotionSpan
    key={id}
    style={{
      display: 'block', fontFamily: FONT.serif, fontWeight: 600, color: L.ink,
      fontSize: 'clamp(34px, 3.5vw, 50px)', lineHeight: 1, letterSpacing: '-0.03em', fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap',
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

        <PeekProvider>
        {/* The group switch: the app's own pill bar, its pill gliding between groups */}
        <div
          className="fxc-bar mt-8"
          // Warm the group's plates the moment the pointer reaches the bar, so the first hover shows a page, not a blank.
          onPointerEnter={() => g.subjects.forEach(s => { const p = peekFor(s.id, s.label); if (p) preload(p.src); })}
        >
          <HorizontalTabs
            variant="pill"
            size="md"
            label="Subject group"
            options={SUBJECT_GROUPS.map(x => ({ value: x.id, label: x.label }))}
            value={group}
            onChange={setGroup}
            className="w-fit max-w-full"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 mt-5 items-start">
          {/* The table and the group's two figures — pinned beside the papers on a desktop */}
          <aside className="lg:col-span-5 min-w-0 fxc-aside" role="tabpanel" aria-label={g.label}>
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

            <Rule strong className="mt-2" />

            <div className="grid grid-cols-2 gap-6 mt-6" aria-live="polite">
              <div>
                <Figure id={`${g.id}-cards`} reduce={reduce}>{numeral(cards)}</Figure>
                <div className="mt-3" style={CAPTION}>{COPY.subjects.stats.cards}</div>
              </div>
              <div>
                <Figure id={`${g.id}-papers`} reduce={reduce}>
                  {span ?? <span style={{ color: L.faint }}>{COPY.subjects.notYet}</span>}
                </Figure>
                <div className="mt-3" style={CAPTION}>{COPY.subjects.stats.papers}</div>
              </div>
            </div>

            <Body className="mt-6" style={{ maxWidth: '46ch' }}>{note}</Body>
          </aside>

          {/* The papers themselves, piling up as the reader scrolls */}
          <div className="lg:col-span-7 min-w-0">
            <PaperStack />
          </div>
        </div>
        </PeekProvider>
      </Container>
    </section>
  );
};

export default Subjects;
